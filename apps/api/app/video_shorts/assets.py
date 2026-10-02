"""The owner's material for a topic: photos they took, a sketch they drew.

A file arrives in 4 MiB parts, the way review files do (``ReviewStore.put_part``), since a
phone photo can pass the API's request limit and nginx's; it is kept in the media store under
the topic's slug, where the worker reads it with its token (``/video/media/files``), and the
media prune leaves it there (``app.video_media.jobs.prune``). Every part names who made the
file and on what terms it may be used: material whose rights are not written down is not
taken. When the last part is in and checked, the topic is settled again, so a topic whose
material is complete becomes ready.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User
from app.video_media.storage import MediaStore, sniff_type
from app.video_reviews.storage import StorageRefused
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.models import VideoShortsAsset
from app.video_shorts.schemas import AssetPartOut
from app.video_shorts.topics import asset_out, resettle, topic_row, topic_view

# Pictures only: the experiments that need the owner's material show it on screen and hand it
# to a model that looks at it.
ASSET_TYPES = frozenset({"image/png", "image/jpeg", "image/webp"})
TAKES_ASSETS = ("idea", "ready", "needs_assets")


@dataclass(frozen=True)
class AssetPart:
    """One part of an upload and what the owner wrote about the file."""

    sha256: str
    part: int
    parts: int
    size: int
    data: bytes
    need: str
    filename: str
    author: str
    rights_note: str
    taken_on: date | None = None


def _head(store: MediaStore, slug: str, sha256: str) -> bytes:
    path = store.path(slug, sha256)
    if path is None:
        return b""
    with path.open("rb") as file:
        return file.read(16)


async def upload_part(
    session: AsyncSession,
    store: MediaStore,
    actor: User,
    slug: str,
    upload: AssetPart,
    now: datetime | None = None,
) -> AssetPartOut:
    moment = now or datetime.now(UTC)
    topic = await topic_row(session, slug)
    if topic.status not in TAKES_ASSETS:
        raise ShortsRefused(409, "video_shorts_topic_taken", "這個題目已經在做、做完或放棄了")
    keys = {str(need.get("key")) for need in topic.assets_needed or []}
    if upload.need not in keys:
        raise ShortsRefused(
            422, "video_shorts_asset_need_unknown", f"這個題目沒有要「{upload.need}」這項素材"
        )
    if not upload.author.strip() or not upload.rights_note.strip():
        raise ShortsRefused(
            422, "video_shorts_asset_rights_missing", "請寫拍攝者（或作者）與授權說明"
        )
    try:
        result = store.put_part(
            topic.slug,
            upload.sha256,
            index=upload.part,
            count=upload.parts,
            size=upload.size,
            data=upload.data,
        )
    except StorageRefused as error:
        raise ShortsRefused(
            error.status, error.code.replace("video_review_", "video_shorts_asset_"), error.detail
        ) from error
    if not result.complete:
        return AssetPartOut(received=result.received, complete=False)
    content_type = sniff_type(_head(store, topic.slug, upload.sha256))
    if content_type not in ASSET_TYPES:
        existing = await session.scalar(
            select(VideoShortsAsset.id).where(
                VideoShortsAsset.topic_slug == topic.slug,
                VideoShortsAsset.sha256 == upload.sha256,
            )
        )
        if existing is None:
            path = store.path(topic.slug, upload.sha256)
            if path is not None:
                path.unlink(missing_ok=True)
        raise ShortsRefused(415, "video_shorts_asset_type", "素材只收 PNG、JPEG 或 WebP 圖片")
    asset = await session.scalar(
        select(VideoShortsAsset).where(
            VideoShortsAsset.topic_slug == topic.slug,
            VideoShortsAsset.sha256 == upload.sha256,
        )
    )
    if asset is None:
        asset = VideoShortsAsset(
            id=uuid4(),
            topic_slug=topic.slug,
            need=upload.need,
            sha256=upload.sha256,
            filename=upload.filename,
            content_type=content_type,
            size=upload.size,
            author=upload.author.strip(),
            taken_on=upload.taken_on,
            rights_note=upload.rights_note.strip(),
            uploaded_by_user_id=actor.id,
            created_at=moment,
        )
        session.add(asset)
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action="video_shorts_asset_added",
                target=f"video_shorts_topic:{topic.slug}",
                metadata_json={
                    "need": upload.need,
                    "sha256": upload.sha256,
                    "size": upload.size,
                },
            )
        )
        await session.flush()
        await resettle(session, topic)
        topic.updated_at = moment
        await session.commit()
    return AssetPartOut(
        received=result.received,
        complete=True,
        asset=asset_out(asset),
        topic=await topic_view(session, topic),
    )
