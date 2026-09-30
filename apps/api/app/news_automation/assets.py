from __future__ import annotations

import asyncio
import hashlib
import io
from datetime import UTC, datetime
from typing import TYPE_CHECKING, cast
from uuid import UUID

from botocore.exceptions import BotoCoreError, ClientError
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.community.media import storage
from app.config import get_settings
from app.guides.schemas import GuideDocument, HeroImage, ImageCredit
from app.i18n import Locale
from app.news_automation.models import NewsAsset, NewsCandidate
from app.problems import AppError

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client

PUBLIC_PREFIX = "/guides/news-assets"
MAX_PUBLIC_ASSET_BYTES = 5 * 1024 * 1024
ALLOWED_CONTENT_TYPES = {"image/webp", "image/svg+xml"}
LOCALE_TOKEN: dict[Locale, str] = {
    "zh-TW": "zh-tw",
    "zh-CN": "zh-cn",
    "en": "en",
    "ja": "ja",
    "ko": "ko",
}
PALETTE = {
    "ai": (65, 49, 136),
    "tech": (11, 92, 106),
    "crypto": (126, 74, 20),
}


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def render_brand_raster(vertical: str, size: tuple[int, int]) -> bytes:
    """Render deterministic original artwork; no source-site image is fetched or copied."""

    width, height = size
    base = PALETTE[vertical]
    image = Image.new("RGB", size, base)
    draw = ImageDraw.Draw(image)
    for index in range(7):
        inset = 45 + index * 58
        # Seven rings fit the 1600x900 hero; on the 1200x630 social card the later ones
        # would invert (y1 < y0), which PIL rejects, so a ring that no longer fits ends it.
        if inset >= min(width, height) // 2 - 20:
            break
        color = tuple(min(255, channel + 18 + index * 7) for channel in base)
        draw.rounded_rectangle(
            (inset, inset, width - inset, height - inset),
            radius=max(18, 80 - index * 7),
            outline=color,
            width=max(2, 12 - index),
        )
    draw.ellipse(
        (width * 0.67, height * 0.12, width * 0.9, height * 0.53),
        fill=(245, 182, 62),
    )
    draw.text((width * 0.07, height * 0.6), "MOKAAIR", fill="white", font=_font(76))
    draw.text(
        (width * 0.075, height * 0.73),
        f"{vertical.upper()} NEWS",
        fill=(235, 237, 246),
        font=_font(42),
    )
    output = io.BytesIO()
    image.save(output, format="WEBP", quality=88, method=6)
    return output.getvalue()


def object_storage() -> S3Client | None:
    """The S3 client, or None on a host without object storage configured."""
    try:
        return storage()
    except AppError:
        return None


async def _put(key: str, body: bytes, content_type: str) -> bytes | None:
    """Store an image in S3 and return None, or return the bytes for the database row when
    the host has no object storage. Before this, every candidate failed at this step on
    such a host, after all of its model calls had been spent."""
    client = object_storage()
    if client is None:
        return body
    try:
        await asyncio.to_thread(
            client.put_object,
            Bucket=get_settings().community_s3_bucket,
            Key=key,
            Body=body,
            ContentType=content_type,
            CacheControl="private, no-store",
        )
    except (BotoCoreError, ClientError) as error:
        raise AppError(503, "news_asset_storage_unavailable", "新聞圖片儲存暫時無法使用") from error
    return None


async def ensure_assets(
    session: AsyncSession,
    candidate: NewsCandidate,
    documents: dict[Locale, GuideDocument],
) -> dict[Locale, GuideDocument]:
    existing = {
        (row.variant, cast(Locale | None, row.locale)): row
        for row in await session.scalars(
            select(NewsAsset).where(NewsAsset.candidate_id == candidate.id)
        )
    }

    async def create(
        variant: str,
        locale: Locale | None,
        body: bytes,
        content_type: str,
        width: int,
        height: int,
    ) -> NewsAsset:
        found = existing.get((variant, locale))
        digest = hashlib.sha256(body).hexdigest()
        if found is not None and found.sha256 == digest:
            return found
        suffix = "webp" if content_type == "image/webp" else "svg"
        locale_suffix = f"-{LOCALE_TOKEN[locale]}" if locale else ""
        filename = f"{candidate.id.hex}-{variant}{locale_suffix}.{suffix}"
        key = f"news/{candidate.id}/{filename}"
        inline = await _put(key, body, content_type)
        if found is not None:
            found.content = inline
            found.storage_key = key
            found.public_filename = filename
            found.content_type = content_type
            found.sha256 = digest
            found.size = len(body)
            found.width = width
            found.height = height
            found.deleted_at = None
            return found
        row = NewsAsset(
            candidate_id=candidate.id,
            variant=variant,
            locale=locale,
            storage_key=key,
            public_filename=filename,
            content_type=content_type,
            sha256=digest,
            size=len(body),
            width=width,
            height=height,
            content=inline,
        )
        session.add(row)
        existing[(variant, locale)] = row
        return row

    hero = await create(
        "hero", None, render_brand_raster(candidate.vertical, (1600, 900)), "image/webp", 1600, 900
    )
    await create(
        "social",
        None,
        render_brand_raster(candidate.vertical, (1200, 630)),
        "image/webp",
        1200,
        630,
    )
    # Articles used to carry a fixed "editorial verification flow" figure that named an
    # internal tool and took the article title as its alt text; it told readers nothing about
    # the story. It is no longer drawn, and a candidate processed again loses the old one.
    now = datetime.now(UTC)
    for (variant, _), row in existing.items():
        if variant == "diagram" and row.deleted_at is None:
            row.deleted_at = now
            row.is_public = False
    credit = ImageCredit(author="Mokaair", license="Original editorial artwork")
    output: dict[Locale, GuideDocument] = {}
    for locale, document in documents.items():
        encoded = document.model_dump(mode="json")
        encoded["hero"] = HeroImage(
            src=f"{PUBLIC_PREFIX}/{hero.public_filename}",
            alt=document.title,
            width=1600,
            height=900,
            credit=credit,
        ).model_dump(mode="json")
        encoded["blocks"] = [
            block
            for block in encoded["blocks"]
            if not (block.get("type") == "image" and block.get("src", "").startswith(PUBLIC_PREFIX))
        ]
        output[locale] = GuideDocument.model_validate(encoded)
    return output


async def mark_assets_public(session: AsyncSession, candidate_id: UUID) -> None:
    rows = await session.scalars(select(NewsAsset).where(NewsAsset.candidate_id == candidate_id))
    for row in rows:
        row.is_public = True


async def public_asset(session: AsyncSession, filename: str) -> tuple[bytes, str, str]:
    if (
        not filename
        or len(filename) > 160
        or any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789-." for ch in filename)
    ):
        raise AppError(404, "news_asset_not_found", "找不到新聞圖片")
    row = await session.scalar(
        select(NewsAsset).where(
            NewsAsset.public_filename == filename,
            NewsAsset.is_public.is_(True),
            NewsAsset.deleted_at.is_(None),
        )
    )
    if row is None or row.content_type not in ALLOWED_CONTENT_TYPES:
        raise AppError(404, "news_asset_not_found", "找不到新聞圖片")
    if row.content is not None:
        body = row.content
    else:
        body = await _object_body(row)
    if len(body) > MAX_PUBLIC_ASSET_BYTES or hashlib.sha256(body).hexdigest() != row.sha256:
        raise AppError(404, "news_asset_not_found", "找不到新聞圖片")
    return body, row.content_type, row.sha256


async def _object_body(row: NewsAsset) -> bytes:
    try:
        response = await asyncio.to_thread(
            storage().get_object,
            Bucket=get_settings().community_s3_bucket,
            Key=row.storage_key,
        )
        if int(response.get("ContentLength", MAX_PUBLIC_ASSET_BYTES + 1)) > MAX_PUBLIC_ASSET_BYTES:
            raise AppError(404, "news_asset_not_found", "找不到新聞圖片")
        body: bytes = await asyncio.to_thread(response["Body"].read, MAX_PUBLIC_ASSET_BYTES + 1)
        response["Body"].close()
    except (BotoCoreError, ClientError) as error:
        raise AppError(503, "news_asset_storage_unavailable", "新聞圖片儲存暫時無法使用") from error
    return body
