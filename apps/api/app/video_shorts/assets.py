"""The owner's material for a topic: photos they took, a sketch they drew.

A file arrives in 4 MiB parts, the way review files do (``ReviewStore.put_part``), since a
phone photo can pass the API's request limit and nginx's; it is kept in the media store under
the topic's slug, where the worker reads it with its token (``/video/media/files``), and the
media prune leaves it there (``app.video_media.jobs.prune``) once it is an asset. The parts
carry only what names the bytes; who made the file and on what terms it may be used come
after, once, in a JSON body (``add_asset``), so a person's name never sits in a URL and the
logs that keep URLs. Material whose rights are not written down is not taken: a file that
never gets them stays a stray the prune removes. When the asset is added, the topic is
settled again, so a topic whose material is complete becomes ready.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User
from app.video_media.storage import MediaStore, sniff_type
from app.video_reviews.storage import PART_BYTES, StorageRefused
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.models import VideoShortsAsset, VideoShortsTopic
from app.video_shorts.schemas import AssetPartOut
from app.video_shorts.topics import asset_out, resettle, topic_row, topic_view

# Pictures only: the experiments that need the owner's material show it on screen and hand it
# to a model that looks at it.
ASSET_TYPES = frozenset({"image/png", "image/jpeg", "image/webp"})
TAKES_ASSETS = ("idea", "ready", "needs_assets")


@dataclass(frozen=True)
class AssetPart:
    """One part of an upload: the bytes and what names them, and nothing about a person."""

    sha256: str
    part: int
    parts: int
    size: int
    data: bytes
    need: str


@dataclass(frozen=True)
class AssetInfo:
    """What the owner wrote about a file whose parts are all in."""

    sha256: str
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


def _store_refused(error: StorageRefused) -> ShortsRefused:
    return ShortsRefused(
        error.status, error.code.replace("video_review_", "video_shorts_asset_"), error.detail
    )


async def _taking_topic(session: AsyncSession, slug: str, need: str) -> VideoShortsTopic:
    """The topic, when it still takes material and asks for this one."""
    topic = await topic_row(session, slug)
    if topic.status not in TAKES_ASSETS:
        raise ShortsRefused(409, "video_shorts_topic_taken", "這個題目已經在做、做完或放棄了")
    keys = {str(item.get("key")) for item in topic.assets_needed or []}
    if need not in keys:
        raise ShortsRefused(
            422, "video_shorts_asset_need_unknown", f"這個題目沒有要「{need}」這項素材"
        )
    return topic


async def upload_part(
    session: AsyncSession, store: MediaStore, slug: str, upload: AssetPart
) -> AssetPartOut:
    """Keep one part; when the last is in, the file must be a picture or it is thrown away.
    The file becomes the topic's material only with ``add_asset``."""
    topic = await _taking_topic(session, slug, upload.need)
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
        raise _store_refused(error) from error
    if not result.complete:
        return AssetPartOut(received=result.received, complete=False)
    if sniff_type(_head(store, topic.slug, upload.sha256)) not in ASSET_TYPES:
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
    return AssetPartOut(received=result.received, complete=True)


async def add_asset(
    session: AsyncSession,
    store: MediaStore,
    actor: User,
    slug: str,
    info: AssetInfo,
    now: datetime | None = None,
) -> AssetPartOut:
    """Make a file whose parts are all in the topic's material, with who made it and on what
    terms. The same file again is the asset it already is."""
    moment = now or datetime.now(UTC)
    topic = await _taking_topic(session, slug, info.need)
    if not info.author.strip() or not info.rights_note.strip():
        raise ShortsRefused(
            422, "video_shorts_asset_rights_missing", "請寫拍攝者（或作者）與授權說明"
        )
    try:
        path = store.path(topic.slug, info.sha256)
    except StorageRefused as error:
        raise _store_refused(error) from error
    if path is None:
        raise ShortsRefused(
            409, "video_shorts_asset_not_uploaded", "這個檔案還沒傳完：先把每一段傳上來"
        )
    content_type = sniff_type(_head(store, topic.slug, info.sha256))
    if content_type not in ASSET_TYPES:
        # Left where it is: a file the part upload did not check may be another job's.
        raise ShortsRefused(415, "video_shorts_asset_type", "素材只收 PNG、JPEG 或 WebP 圖片")
    size = path.stat().st_size
    asset = await session.scalar(
        select(VideoShortsAsset).where(
            VideoShortsAsset.topic_slug == topic.slug,
            VideoShortsAsset.sha256 == info.sha256,
        )
    )
    if asset is None:
        asset = VideoShortsAsset(
            id=uuid4(),
            topic_slug=topic.slug,
            need=info.need,
            sha256=info.sha256,
            filename=info.filename,
            content_type=content_type,
            size=size,
            author=info.author.strip(),
            taken_on=info.taken_on,
            rights_note=info.rights_note.strip(),
            uploaded_by_user_id=actor.id,
            created_at=moment,
        )
        session.add(asset)
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action="video_shorts_asset_added",
                target=f"video_shorts_topic:{topic.slug}",
                metadata_json={"need": info.need, "sha256": info.sha256, "size": size},
            )
        )
        await session.flush()
        await resettle(session, topic)
        topic.updated_at = moment
        await session.commit()
    return AssetPartOut(
        received=list(range(-(-size // PART_BYTES))),
        complete=True,
        asset=asset_out(asset),
        topic=await topic_view(session, topic),
    )
