from __future__ import annotations

import asyncio
import hashlib
import io
from html import escape
from typing import TYPE_CHECKING, cast
from uuid import UUID

from botocore.exceptions import BotoCoreError, ClientError
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.community.media import storage
from app.config import get_settings
from app.guides.schemas import GuideDocument, HeroImage, ImageBlock, ImageCredit
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
DIAGRAM_COPY: dict[Locale, tuple[str, str]] = {
    "zh-TW": ("Mokaair 編輯查核流程", "消息會先蒐集來源、獨立查核，再交由 Jev 判斷。"),
    "zh-CN": ("Mokaair 编辑核查流程", "消息会先收集来源、独立核查，再交由 Jev 判断。"),
    "en": (
        "Mokaair editorial verification flow",
        "Sources are collected, independently checked, then reviewed by Jev.",
    ),
    "ja": ("Mokaair 編集検証フロー", "情報源を収集し、独立検証を行ってから Jev が判断します。"),
    "ko": ("Mokaair 편집 검증 절차", "출처를 수집하고 독립적으로 검증한 뒤 Jev가 판단합니다."),
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


def render_diagram(title: str, vertical: str, locale: Locale) -> bytes:
    label = {
        "zh-TW": ("來源", "獨立查核", "Jev 判斷"),
        "zh-CN": ("来源", "独立核查", "Jev 判断"),
        "en": ("Sources", "Independent check", "Jev decision"),
        "ja": ("情報源", "独立検証", "Jev 判断"),
        "ko": ("출처", "독립 검증", "Jev 판단"),
    }[locale]
    safe_title = escape(title[:120])
    boxes = "".join(
        f'<rect x="{70 + index * 500}" y="300" width="400" height="220" rx="32" '
        f'fill="#ffffff" opacity="0.94"/><text x="{270 + index * 500}" y="420" '
        f'text-anchor="middle" font-size="38" font-family="sans-serif" fill="#172033">'
        f"{escape(text)}</text>"
        for index, text in enumerate(label)
    )
    arrows = "".join(
        f'<path d="M {470 + index * 500} 410 L {550 + index * 500} 410" '
        'stroke="#f5b63e" stroke-width="18" marker-end="url(#arrow)"/>'
        for index in range(2)
    )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" '
        'viewBox="0 0 1600 900">'
        f"<title>{safe_title}</title>"
        f"<desc>Mokaair {escape(vertical)} news evidence workflow</desc>"
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" '
        'refY="4" orient="auto"><path d="M0 0 L8 4 L0 8z" fill="#f5b63e"/>'
        "</marker></defs>"
        '<rect width="1600" height="900" fill="#172033"/>'
        '<text x="800" y="155" text-anchor="middle" font-size="46" '
        f'font-family="sans-serif" fill="white">{safe_title}</text>'
        f"{boxes}{arrows}"
        '<text x="800" y="720" text-anchor="middle" font-size="30" '
        f'font-family="sans-serif" fill="#d8dfef">MOKAAIR · '
        f"{escape(vertical.upper())} NEWS</text></svg>"
    )
    return svg.encode()


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
    credit = ImageCredit(author="Mokaair", license="Original editorial artwork")
    output: dict[Locale, GuideDocument] = {}
    for locale, document in documents.items():
        diagram_caption, diagram_description = DIAGRAM_COPY[locale]
        diagram = await create(
            "diagram",
            locale,
            render_diagram(document.title, candidate.vertical, locale),
            "image/svg+xml",
            1600,
            900,
        )
        diagram_src = f"{PUBLIC_PREFIX}/{diagram.public_filename}"
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
        insert_at = min(4, len(encoded["blocks"]))
        encoded["blocks"].insert(
            insert_at,
            ImageBlock(
                type="image",
                src=diagram_src,
                alt=document.title,
                width=1600,
                height=900,
                caption=diagram_caption,
                description=diagram_description,
                credit=credit,
            ).model_dump(mode="json"),
        )
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
