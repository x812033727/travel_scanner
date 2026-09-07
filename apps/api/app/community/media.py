from __future__ import annotations

import asyncio
import io
import warnings
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from PIL import Image, ImageOps, UnidentifiedImageError
from sqlalchemy import Text, cast, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.community.models import Media, Post, PostRevision, Profile, Report
from app.community.policy import fail, visible_profile
from app.community.schemas import UploadInput
from app.config import get_settings
from app.models import User

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client

MAX_BYTES = 10 * 1024 * 1024
MAX_PIXELS = 25_000_000


def storage(*, public: bool = False) -> S3Client:
    settings = get_settings()
    endpoint = settings.community_s3_endpoint
    if public:
        endpoint = settings.community_s3_public_endpoint or endpoint
    if not endpoint or not settings.community_s3_access_key or not settings.community_s3_secret_key:
        raise fail("community_storage_unavailable", 503)
    if settings.production and not endpoint.startswith("https://"):
        raise fail("community_storage_unavailable", 503)
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        region_name=settings.community_s3_region,
        aws_access_key_id=settings.community_s3_access_key,
        aws_secret_access_key=settings.community_s3_secret_key,
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style": "path"},
            connect_timeout=5,
            read_timeout=15,
            retries={"max_attempts": 2},
        ),
    )


def raw_key(media: Media) -> str:
    return f"quarantine/{media.owner_id}/{media.id}"


def clean_image(raw: bytes) -> tuple[bytes, bytes, int, int]:
    if not raw or len(raw) > MAX_BYTES:
        raise fail("community_image_invalid", 422)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(raw), formats=["JPEG", "PNG", "WEBP"]) as original:
                if (
                    original.width * original.height > MAX_PIXELS
                    or getattr(original, "n_frames", 1) > 1
                ):
                    raise ValueError("image exceeds decoded limits")
                original.load()
                oriented = ImageOps.exif_transpose(original)
                # A new raster strips EXIF, XMP, comments, profiles and other metadata.
                clean = Image.new("RGB", oriented.size, (255, 255, 255))
                if oriented.mode == "RGBA":
                    clean.paste(oriented, mask=oriented.getchannel("A"))
                else:
                    clean.paste(oriented.convert("RGB"))
                clean.thumbnail((2400, 2400))
                width, height = clean.size
                full = io.BytesIO()
                clean.save(full, format="WEBP", quality=85)
                clean.thumbnail((640, 640))
                thumb = io.BytesIO()
                clean.save(thumb, format="WEBP", quality=80)
                return full.getvalue(), thumb.getvalue(), width, height
    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ) as exc:
        raise fail("community_image_invalid", 422) from exc


async def create_upload(session: AsyncSession, user: User, payload: UploadInput) -> dict[str, Any]:
    identifier = uuid4()
    media = Media(
        id=identifier,
        owner_id=user.id,
        object_key=f"images/{identifier}.webp",
        thumbnail_key=f"thumbs/{identifier}.webp",
        width=0,
        height=0,
        size=0,
        alt=payload.alt,
    )
    client = storage(public=True)
    try:
        upload = await asyncio.to_thread(
            client.generate_presigned_post,
            Bucket=get_settings().community_s3_bucket,
            Key=raw_key(media),
            Fields={"Content-Type": payload.content_type},
            Conditions=[
                {"Content-Type": payload.content_type},
                ["content-length-range", 1, payload.size],
            ],
            ExpiresIn=300,
        )
    except (BotoCoreError, ClientError) as exc:
        raise fail("community_storage_unavailable", 503) from exc
    session.add(media)
    await session.commit()
    return {"id": str(media.id), "upload": upload}


def process_upload(media: Media) -> tuple[int, int, int]:
    client = storage()
    bucket = get_settings().community_s3_bucket
    try:
        response = client.get_object(Bucket=bucket, Key=raw_key(media))
        with response["Body"] as stream:
            if response.get("ContentLength", MAX_BYTES + 1) > MAX_BYTES:
                raise fail("community_image_invalid", 422)
            raw = stream.read(MAX_BYTES + 1)
        full, thumbnail, width, height = clean_image(raw)
        for key, body in ((media.object_key, full), (media.thumbnail_key, thumbnail)):
            client.put_object(
                Bucket=bucket,
                Key=key,
                Body=body,
                ContentType="image/webp",
                CacheControl="private, no-store",
            )
        client.delete_object(Bucket=bucket, Key=raw_key(media))
        return width, height, len(full) + len(thumbnail)
    except (BotoCoreError, ClientError) as exc:
        raise fail("community_storage_unavailable", 503) from exc


async def complete_upload(session: AsyncSession, user: User, identifier: UUID) -> dict[str, Any]:
    row = await session.scalar(
        select(Media)
        .where(
            Media.id == identifier,
            Media.owner_id == user.id,
            Media.deleted_at.is_(None),
        )
        .with_for_update()
    )
    if row is None:
        raise fail("community_not_found", 404)
    if row.width == 0:
        row.width, row.height, row.size = await asyncio.to_thread(process_upload, row)
    await session.commit()
    return {"id": str(row.id), "width": row.width, "height": row.height, "alt": row.alt}


async def check_media(session: AsyncSession, user: User, identifiers: list[UUID]) -> None:
    if len(set(identifiers)) != len(identifiers):
        raise fail("community_image_invalid", 422)
    if not identifiers:
        return
    found = list(
        (
            await session.scalars(
                select(Media.id).where(
                    Media.id.in_(identifiers),
                    Media.owner_id == user.id,
                    Media.deleted_at.is_(None),
                    Media.width > 0,
                )
            )
        ).all()
    )
    if len(found) != len(identifiers):
        raise fail("community_image_invalid", 422)


async def media_url(
    session: AsyncSession,
    identifier: UUID,
    viewer: User | None,
    *,
    thumbnail: bool = False,
    review: bool = False,
) -> dict[str, Any]:
    media = await session.get(Media, identifier)
    if media is None or media.deleted_at is not None or media.width == 0:
        raise fail("community_not_found", 404)
    from app.community.pet_models import PetPlace, PetReport

    if not review:
        await visible_profile(session, media.owner_id, viewer)
    if review or viewer is None or viewer.id != media.owner_id:
        avatar = await session.scalar(
            select(Profile.user_id).where(Profile.avatar_id == identifier)
        )
        publication = await session.scalar(
            select(Post.id)
            .join(
                PostRevision,
                PostRevision.id == Post.published_revision_id,
            )
            .where(
                Post.author_id == media.owner_id,
                Post.state.in_(["published", "pending", "hidden"] if review else ["published"]),
                cast(PostRevision.media_ids, Text).contains(f'"{identifier}"'),
            )
            .limit(1)
        )
        report_query = (
            select(PetReport.id)
            .join(PetPlace, PetPlace.id == PetReport.place_id)
            .where(
                PetReport.reporter_id == media.owner_id,
                cast(PetReport.media_ids, Text).contains(f'"{identifier}"'),
            )
        )
        if not review:
            report_query = report_query.where(
                PetReport.status == "approved", PetPlace.status == "approved"
            )
        experience = await session.scalar(report_query.limit(1))
        pending = None
        reported = None
        if review:
            reported = await session.scalar(
                select(Report.id)
                .where(
                    Report.kind == "post",
                    # Only the server-captured attachment list grants review
                    # access. User-authored titles/bodies can contain arbitrary IDs.
                    cast(Report.evidence["media_ids"], Text).contains(f'"{identifier}"'),
                )
                .limit(1)
            )
            pending = await session.scalar(
                select(Post.id)
                .join(PostRevision, PostRevision.id == Post.pending_revision_id)
                .where(
                    Post.author_id == media.owner_id,
                    Post.state != "deleted",
                    cast(PostRevision.media_ids, Text).contains(f'"{identifier}"'),
                )
                .limit(1)
            )
        if all(value is None for value in (avatar, publication, pending, experience, reported)):
            raise fail("community_not_found", 404)
    url = await asyncio.to_thread(
        storage(public=True).generate_presigned_url,
        "get_object",
        Params={
            "Bucket": get_settings().community_s3_bucket,
            "Key": media.thumbnail_key if thumbnail else media.object_key,
            "ResponseCacheControl": "private, no-store",
        },
        ExpiresIn=60,
    )
    return {"url": url, "expires_in": 60, "alt": media.alt}
