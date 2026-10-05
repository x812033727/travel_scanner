"""Until the API audit passes, the owner uploads the files and the site finds them
(docs/videos/SHORTS.md §稽核通過前).

An upload through the API by a project that has not passed YouTube's audit is locked private
for good, so the owner drags the mp4 files of the coming days into YouTube Studio, as private
videos, and changes nothing else. Each file is named ``mokaair-short-<slug>.mp4``. "I uploaded
them" then reads the channel's newest uploads and matches them to the Shorts that wait: by the
file name YouTube kept (only the owner can read it), or by the title Studio made from it. A
match must be private and as long as the cut, to the second; its id is then the Short's.

``match_uploads`` is the decision, as a pure function; the rest loads what it decides from.
"""

from __future__ import annotations

import re
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User, VideoProject, VideoReview
from app.video_reviews.storage import ReviewStore
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.models import VideoShortsSettings, VideoShortsSlot
from app.video_shorts.quota import QUOTA_REASONS, Quota
from app.video_shorts.schemas import ClaimItem, ClaimOut, UploadsOut, UploadWaiting
from app.video_shorts.settings import channel_facts, settings_row
from app.video_youtube import connection
from app.video_youtube.client import YoutubeClient, YoutubeError
from app.video_youtube.errors import Refused
from app.video_youtube.requests import as_dict

FILE_PREFIX = "mokaair-short-"
# How far a cut and its upload may differ in length: YouTube reports whole seconds.
LENGTH_TOLERANCE = 1.0
# How many of the channel's newest uploads are read: one page.
NEWEST_UPLOADS = 50
DURATION = re.compile(r"^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?$")
CLAIM_PARTS = "snippet,status,contentDetails,fileDetails"


@dataclass(frozen=True)
class Waiting:
    """A Short that holds a slot and has no video on YouTube yet."""

    slug: str
    title: str
    line: str | None
    slot_at: datetime
    seconds: float | None
    final_sha256: str | None
    size: int | None


def file_name(slug: str) -> str:
    return f"{FILE_PREFIX}{slug}.mp4"


def duration_seconds(value: object) -> float | None:
    """An ISO 8601 duration as YouTube writes it (PT35S, PT1M2S), in seconds."""
    match = DURATION.fullmatch(value) if isinstance(value, str) else None
    if match is None or not any(match.groups()):
        return None
    hours, minutes, seconds = (float(part) if part else 0.0 for part in match.groups())
    return hours * 3600 + minutes * 60 + seconds


def _named(video: dict[str, Any], slug: str) -> bool:
    """Whether an upload is this Short's file: by the file name YouTube kept, else by the
    title Studio made from the file name."""
    wanted = file_name(slug).lower()
    kept = as_dict(video.get("fileDetails")).get("fileName")
    if isinstance(kept, str) and kept.strip():
        return kept.strip().lower() == wanted
    title = as_dict(video.get("snippet")).get("title")
    return isinstance(title, str) and title.strip().lower() in (wanted, wanted[: -len(".mp4")])


def match_uploads(
    waiting: list[Waiting], videos: list[dict[str, Any]], channel_id: str, taken: set[str]
) -> list[ClaimItem]:
    """For every Short that waits, what the channel's uploads say. ``videos`` are newest
    first; ``taken`` are the ids other videos of the site already have.

    Of several uploads of the same file the newest that is private and of the right length
    is the Short's, and the answer says the others are there to be deleted.
    """
    results: list[ClaimItem] = []
    for short in waiting:
        name = file_name(short.slug)
        named = [
            video
            for video in videos
            if _named(video, short.slug)
            and as_dict(video.get("snippet")).get("channelId") == channel_id
            and str(video.get("id")) not in taken
        ]
        if not named:
            results.append(
                ClaimItem(
                    slug=short.slug,
                    file_name=name,
                    result="not_found",
                    detail="頻道最近上傳的影片裡沒有這個檔名",
                )
            )
            continue
        private = [
            video
            for video in named
            if as_dict(video.get("status")).get("privacyStatus") == "private"
        ]
        if not private:
            shown = as_dict(named[0].get("status")).get("privacyStatus")
            results.append(
                ClaimItem(
                    slug=short.slug,
                    file_name=name,
                    result="not_private",
                    detail=(
                        f"上傳的那一支不是私人（現在是 {shown}）；"
                        "網站只排程從來沒有公開過的私人影片"
                    ),
                    youtube_video_id=str(named[0].get("id")),
                )
            )
            continue
        fitting = []
        for video in private:
            length = duration_seconds(as_dict(video.get("contentDetails")).get("duration"))
            if (
                short.seconds is None
                or length is None
                or abs(length - short.seconds) <= LENGTH_TOLERANCE
            ):
                fitting.append(video)
        if not fitting:
            length = duration_seconds(as_dict(private[0].get("contentDetails")).get("duration"))
            results.append(
                ClaimItem(
                    slug=short.slug,
                    file_name=name,
                    result="length_differs",
                    detail=(
                        f"上傳的那一支長 {length:g} 秒，成片是 {short.seconds:g} 秒：不是同一個檔"
                    ),
                    youtube_video_id=str(private[0].get("id")),
                )
            )
            continue
        chosen = str(fitting[0].get("id"))
        others = [str(video.get("id")) for video in named if str(video.get("id")) != chosen]
        results.append(
            ClaimItem(
                slug=short.slug,
                file_name=name,
                result="duplicate" if others else "matched",
                detail=(
                    f"這個檔上傳了 {len(named)} 次，用最新的那一支；"
                    f"其餘的請在 Studio 刪掉：{'、'.join(others)}"
                    if others
                    else "對到了"
                ),
                youtube_video_id=chosen,
            )
        )
    return results


def _final_of(reviews: list[VideoReview]) -> tuple[float | None, str | None, int | None]:
    """The length, hash and size of the cut, from the approved reviews (newest first)."""
    seconds: float | None = None
    sha: str | None = None
    size: int | None = None
    for review in reviews:
        if review.status != "approved":
            continue
        if review.gate == "final" and seconds is None:
            value = review.payload.get("duration_seconds") if review.payload else None
            seconds = float(value) if isinstance(value, int | float) else None
        if review.gate == "publish" and sha is None:
            for item in review.files:
                if isinstance(item, dict) and item.get("role") == "final":
                    sha = str(item.get("sha256"))
                    size = int(item["size"]) if isinstance(item.get("size"), int) else None
    return seconds, sha, size


async def waiting_uploads(
    session: AsyncSession, row: VideoShortsSettings, now: datetime | None = None
) -> list[Waiting]:
    """The Shorts that hold a slot in the coming days and have no video on YouTube yet,
    in the order of their slots."""
    moment = now or datetime.now(UTC)
    slots = list(
        await session.scalars(
            select(VideoShortsSlot)
            .where(
                VideoShortsSlot.status.in_(("assigned", "locked")),
                VideoShortsSlot.project_slug.is_not(None),
                VideoShortsSlot.starts_at > moment,
                VideoShortsSlot.starts_at <= moment + timedelta(days=row.upload_ahead_days),
            )
            .order_by(VideoShortsSlot.starts_at)
        )
    )
    if not slots:
        return []
    projects = {
        project.slug: project
        for project in await session.scalars(
            select(VideoProject).where(
                VideoProject.slug.in_([str(slot.project_slug) for slot in slots]),
                VideoProject.youtube_video_id.is_(None),
                VideoProject.dropped_at.is_(None),
            )
        )
    }
    reviews: dict[Any, list[VideoReview]] = {}
    if projects:
        for review in await session.scalars(
            select(VideoReview)
            .where(VideoReview.project_id.in_([project.id for project in projects.values()]))
            .order_by(VideoReview.created_at.desc())
        ):
            reviews.setdefault(review.project_id, []).append(review)
    waiting: list[Waiting] = []
    for slot in slots:
        project = projects.get(str(slot.project_slug))
        if project is None:
            continue
        seconds, sha, size = _final_of(reviews.get(project.id, []))
        waiting.append(
            Waiting(
                slug=project.slug,
                title=project.title,
                line=project.shorts_line,
                slot_at=slot.starts_at,
                seconds=seconds,
                final_sha256=sha,
                size=size,
            )
        )
    return waiting


async def uploads_view(session: AsyncSession, now: datetime | None = None) -> UploadsOut:
    row = await settings_row(session)
    await session.commit()
    return UploadsOut(
        ahead_days=row.upload_ahead_days,
        items=[
            UploadWaiting(
                slug=short.slug,
                title=short.title,
                line=cast(Any, short.line),
                slot_at=short.slot_at,
                file_name=file_name(short.slug),
                size=short.size,
                seconds=short.seconds,
            )
            for short in await waiting_uploads(session, row, now)
        ],
    )


def batch_zip(store: ReviewStore, waiting: list[Waiting], directory: Path | None = None) -> Path:
    """The waiting Shorts' files in one archive, each under the name the claim looks for. An
    mp4 does not compress, so the files are stored as they are."""
    wanted = [short for short in waiting if short.final_sha256]
    paths = [(short, store.path(short.slug, str(short.final_sha256))) for short in wanted]
    found = [(short, path) for short, path in paths if path is not None]
    if not found:
        raise ShortsRefused(
            404, "video_shorts_nothing_to_upload", "接下來幾天沒有等你上傳的 Shorts"
        )
    handle = tempfile.NamedTemporaryFile(  # noqa: SIM115 -- the response closes it when sent
        prefix="mokaair-shorts-", suffix=".zip", delete=False, dir=directory
    )
    with handle, zipfile.ZipFile(handle, "w", compression=zipfile.ZIP_STORED) as archive:
        for short, path in found:
            archive.write(path, arcname=file_name(short.slug))
    return Path(handle.name)


async def claim(
    session: AsyncSession,
    http: httpx.AsyncClient,
    user: User,
    quota: Quota,
    now: datetime | None = None,
) -> ClaimOut:
    """Read the channel's newest uploads and give the waiting Shorts their videos."""
    moment = now or datetime.now(UTC)
    row = await settings_row(session)
    channel = await channel_facts(session)
    if not channel.linked or channel.channel_id is None:
        raise ShortsRefused(
            409, "video_shorts_no_channel", "還沒有連結 YouTube 頻道：先到設定分頁連結"
        )
    waiting = await waiting_uploads(session, row, moment)
    if not waiting:
        await session.commit()
        return ClaimOut(claimed=0, items=[])
    if not await quota.allows_sending():
        raise ShortsRefused(
            429,
            "video_shorts_quota_exhausted",
            "今天的 YouTube API 配額用完了（每天太平洋時間午夜重置），明天再按一次",
        )
    try:
        client = YoutubeClient(http, await connection.access_token(session, http))
        playlist = await client.uploads_playlist()
        await quota.add("channels.list")
        ids = await client.playlist_videos(playlist, limit=NEWEST_UPLOADS) if playlist else []
        await quota.add("playlistItems.list", 1 if playlist else 0)
        videos = await client.videos(ids, parts=CLAIM_PARTS)
        await quota.add("videos.list", 1 if ids else 0)
    except Refused as refused:
        raise ShortsRefused(refused.status, refused.code, refused.detail) from refused
    except YoutubeError as error:
        if error.reason in QUOTA_REASONS:
            await quota.mark_refused()
            raise ShortsRefused(
                429,
                "video_shorts_quota_exhausted",
                "今天的 YouTube API 配額用完了（每天太平洋時間午夜重置），明天再按一次",
            ) from error
        raise ShortsRefused(
            502, "video_shorts_youtube_failed", f"YouTube 回覆：{error.message}"
        ) from error
    except httpx.HTTPError as error:
        raise ShortsRefused(
            502, "video_shorts_youtube_unreachable", "連不到 YouTube，請再試一次"
        ) from error
    # videos.list answers in the order of the ids, which the playlist gave newest first.
    order = {video_id: index for index, video_id in enumerate(ids)}
    videos.sort(key=lambda video: order.get(str(video.get("id")), len(order)))
    taken = {
        str(video_id)
        for video_id in await session.scalars(
            select(VideoProject.youtube_video_id).where(VideoProject.youtube_video_id.is_not(None))
        )
    }
    results = match_uploads(waiting, videos, channel.channel_id, taken)
    claimed = 0
    for item in results:
        if item.result not in ("matched", "duplicate") or item.youtube_video_id is None:
            continue
        # The Studio sync or a review may have given the Short its video while YouTube was
        # asked. This session loaded the project before that, and a re-read keeps the values
        # a loaded object has (SQLAlchemy 2.1.0-2.1.3 keep it loaded, sqlalchemy#13639), so
        # the locked row's values replace them.
        project = await session.scalar(
            select(VideoProject)
            .where(VideoProject.slug == item.slug)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        if project is None or project.youtube_video_id is not None:
            continue
        project.youtube_video_id = item.youtube_video_id
        project.updated_at = moment
        claimed += 1
        session.add(
            AdminAuditLog(
                actor_user_id=user.id,
                action="video_shorts_upload_claimed",
                target=f"video_project:{item.slug}",
                metadata_json={
                    "slug": item.slug,
                    "youtube_video_id": item.youtube_video_id,
                    "file_name": item.file_name,
                    "result": item.result,
                },
            )
        )
    await session.commit()
    return ClaimOut(claimed=claimed, items=results)
