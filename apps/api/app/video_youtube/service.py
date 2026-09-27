"""Sending one video's package to YouTube, and when that happens.

A sync runs after the owner pastes the video's address, after the worker sends a language
batch for a video already on YouTube, or when the owner presses "send again"; each runs as a
job on the ``video-youtube`` queue, since the captions go up one file at a time. What it did is
kept on the project row (``youtube_sync``) for the video's page, and a retry never uploads a
caption track YouTube already has.
"""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import httpx
from redis import Redis as SyncRedis
from redis.exceptions import RedisError
from rq import Queue
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.config import get_settings
from app.db import SessionFactory, engine
from app.infra import get_redis
from app.models import AdminAuditLog, VideoProject, VideoReview
from app.video_reviews import admin_service as reviews
from app.video_reviews.schemas import ProjectOut
from app.video_reviews.storage import ReviewStore
from app.video_youtube import oauth
from app.video_youtube.client import TIMEOUT_SECONDS, YouTubeClient, YouTubeError
from app.video_youtube.schemas import StepId, SyncReason, SyncRecord, SyncStep
from app.video_youtube.sync import (
    caption_locales,
    description_locales,
    missing_captions,
    schedule_problem,
    update_body,
)

logger = logging.getLogger(__name__)

QUEUE = "video-youtube"
JOB_TIMEOUT_SECONDS = 600
ClientFactory = Callable[[], httpx.AsyncClient]


def enqueue_sync(slug: str, reason: SyncReason) -> str | None:
    """Queue a sync; None (and a log line) when the queue cannot be reached, so the request
    that asked for it still succeeds and the owner can press "send again" later."""
    connection = SyncRedis.from_url(get_settings().redis_url)
    try:
        job = Queue(QUEUE, connection=connection).enqueue(
            "app.video_youtube.service.run_sync", slug, reason, job_timeout=JOB_TIMEOUT_SECONDS
        )
        return str(job.id)
    except RedisError:
        logger.warning("video-youtube: could not queue the sync of %s (%s)", slug, reason)
        return None
    finally:
        connection.close()


async def enqueue_after_languages(session: AsyncSession, slug: str) -> str | None:
    """A language batch arrived: a video already on YouTube gets its new localizations and
    captions sent, and a scheduled one its publish time once every language is made."""
    video_id = await session.scalar(
        select(VideoProject.youtube_video_id).where(VideoProject.slug == slug)
    )
    return enqueue_sync(slug, "languages") if video_id else None


def run_sync(slug: str, reason: str) -> None:
    """The queue's entry: one sync in its own session, resources closed after."""

    async def run_and_close_resources() -> None:
        try:
            async with SessionFactory() as session:
                store = reviews.review_store(await load_runtime_settings(session))
                await sync_project(session, store, slug, reason=_reason(reason))
        finally:
            try:
                await get_redis().aclose()
            finally:
                get_redis.cache_clear()
                await engine.dispose()

    asyncio.run(run_and_close_resources())


def _reason(value: str) -> SyncReason:
    return "languages" if value == "languages" else "manual" if value == "manual" else "linked"


def _file(review: VideoReview, role: str) -> dict[str, Any] | None:
    for item in review.files:
        if isinstance(item, dict) and item.get("role") == role:
            return item
    return None


def _read(store: ReviewStore, slug: str, item: dict[str, Any]) -> bytes | None:
    path = store.path(slug, str(item.get("sha256") or ""))
    return path.read_bytes() if path is not None else None


def languages_done(project: VideoProject, reviews_of: list[VideoReview]) -> bool:
    """Every chosen part is ready, skipped or uploaded, and the owner has decided
    (docs/videos/LANGUAGES.md): the condition for sending the publish time."""
    if project.locales_decided_at is None:
        return False
    states = reviews.language_states(reviews.locale_choices(project), reviews_of)
    return all(part.state != "working" for parts in states.values() for part in parts.values())


def _default_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=TIMEOUT_SECONDS, trust_env=False)


async def sync_project(
    session: AsyncSession,
    store: ReviewStore,
    slug: str,
    *,
    reason: SyncReason,
    client_factory: ClientFactory = _default_client,
    now: datetime | None = None,
) -> ProjectOut:
    """Send the package to YouTube and record each step on the project (HANDS-OFF.md §YouTube
    API 第一步): ``videos.update`` with the zh-TW fields, the chosen languages' localizations,
    the disclosure and, once every chosen language is made, ``publishAt``; ``captions.insert``
    for zh-TW and the chosen caption locales YouTube lacks; ``thumbnails.set`` when the
    thumbnail changed. The video stays private: YouTube makes it public at the time set."""
    now = now or datetime.now(UTC)
    project = await reviews._project(session, slug)  # noqa: SLF001 -- one module's helpers
    history = await reviews._reviews(session, project)  # noqa: SLF001
    settings = await load_runtime_settings(session)
    steps: list[SyncStep] = []
    record = SyncRecord(
        at=now, video_id=project.youtube_video_id, reason=reason, ok=False, steps=steps
    )
    previous = project.youtube_sync if isinstance(project.youtube_sync, dict) else {}

    async def finish() -> ProjectOut:
        record.steps = list(steps)
        record.ok = bool(steps) and all(step.ok for step in steps)
        project.youtube_sync = json.loads(record.model_dump_json())
        project.updated_at = now
        session.add(
            AdminAuditLog(
                actor_user_id=None,
                action="video_youtube_synced",
                target=f"video_project:{slug}",
                metadata_json={
                    "slug": slug,
                    "reason": reason,
                    "ok": record.ok,
                    "steps": [step.model_dump() for step in steps],
                },
            )
        )
        await session.commit()
        return await reviews.project_view(session, slug)

    def fail(step: StepId, detail: str) -> None:
        steps.append(SyncStep(id=step, ok=False, detail=detail))

    video_id = project.youtube_video_id
    if not video_id:
        fail("video", "還沒有 YouTube 影片 id：先在影片頁貼上網址")
        return await finish()
    row = await oauth.channel(session)
    if row is None or not oauth.configured(settings):
        fail("video", "還沒連結 YouTube 頻道（影片審核 › 設定 › 共用）")
        return await finish()
    confirmation = next(
        (review for review in history if review.gate == "publish" and review.status == "approved"),
        None,
    )
    if confirmation is None:
        fail("video", "上傳包還沒核准，沒有東西可送")
        return await finish()
    metadata_file = _file(confirmation, "metadata")
    if metadata_file is None or metadata_file.get("sha256") != confirmation.content_sha256:
        fail("video", "上傳包不是核准的那一份（metadata.json 的雜湊對不上）")
        return await finish()
    raw = _read(store, slug, metadata_file)
    if raw is None:
        fail("video", "上傳包的 metadata.json 已不在審核區；工人重送上傳包後再試")
        return await finish()
    try:
        metadata = json.loads(raw)
    except ValueError:
        metadata = None
    if not isinstance(metadata, dict):
        fail("video", "上傳包的 metadata.json 讀不出來")
        return await finish()

    choices = reviews.locale_choices(project)
    roles = {str(item.get("role")) for item in confirmation.files if isinstance(item, dict)}
    locales = description_locales(choices, metadata)
    tracks = caption_locales(choices, roles)
    done = languages_done(project, history)
    publish_at = project.youtube_publish_at
    step: StepId = "video"
    try:
        async with client_factory() as http:
            token = await oauth.access_token(http, settings, oauth.refresh_token_of(row, settings))
            client = YouTubeClient(http, token)
            current = await client.video(video_id)
            if current is None:
                fail("video", f"這個頻道上找不到影片 {video_id}：id 或頻道不對")
                return await finish()
            # The publish time goes only once every chosen language is made
            # (docs/videos/LANGUAGES.md): waiting for them is not a failure, a video that is
            # not private or a time already past is.
            schedule: datetime | None = None
            problem: str | None = None
            waiting = publish_at is not None and not done
            if publish_at is not None and not waiting:
                status = current.get("status")
                problem = schedule_problem(
                    status if isinstance(status, dict) else {}, publish_at, now
                )
                if problem is None:
                    schedule = publish_at
            await client.update_video(
                update_body(
                    video_id=video_id,
                    current=current,
                    metadata=metadata,
                    locales=locales,
                    publish_at=schedule,
                )
            )
            record.localizations = locales
            steps.append(
                SyncStep(
                    id="video",
                    ok=True,
                    detail=f"標題與說明：zh-TW{''.join(f'、{locale}' for locale in locales)}；"
                    f"{'揭露已勾' if metadata.get('contains_synthetic_media') else '不用揭露'}",
                )
            )
            if publish_at is not None:
                if schedule is not None:
                    record.scheduled_at = schedule
                    steps.append(
                        SyncStep(
                            id="schedule",
                            ok=True,
                            detail=f"排定 {schedule.astimezone(UTC).isoformat()} 由 YouTube 公開",
                        )
                    )
                elif waiting:
                    steps.append(
                        SyncStep(
                            id="schedule", ok=True, detail="語言還沒都做好，排程等做好那一輪再送"
                        )
                    )
                else:
                    steps.append(SyncStep(id="schedule", ok=False, detail=str(problem)))
            step = "captions"
            existing = await client.captions(video_id)
            missing = missing_captions(existing, tracks)
            uploaded: list[str] = []
            for locale in missing:
                item = _file(confirmation, f"captions_{locale}")
                srt = _read(store, slug, item) if item else None
                if srt is None:
                    fail("captions", f"{locale} 的字幕檔已不在審核區")
                    return await finish()
                await client.insert_caption(video_id, locale, srt)
                uploaded.append(locale)
            record.captions = tracks
            already = [locale for locale in tracks if locale not in missing]
            steps.append(
                SyncStep(
                    id="captions",
                    ok=True,
                    detail=f"字幕：新上傳 {'、'.join(uploaded) or '無'}"
                    f"{'；已有 ' + '、'.join(already) if already else ''}",
                )
            )
            step = "thumbnail"
            thumbnail = _file(confirmation, "thumbnail")
            kept = previous.get("thumbnail_sha256") if isinstance(previous, dict) else None
            if thumbnail is None:
                steps.append(SyncStep(id="thumbnail", ok=True, detail="上傳包沒有縮圖"))
            elif thumbnail.get("sha256") == kept:
                record.thumbnail_sha256 = str(kept)
                steps.append(SyncStep(id="thumbnail", ok=True, detail="縮圖沒變，沒有再上傳"))
            else:
                jpeg = _read(store, slug, thumbnail)
                if jpeg is None:
                    fail("thumbnail", "縮圖已不在審核區")
                    return await finish()
                await client.set_thumbnail(video_id, jpeg)
                record.thumbnail_sha256 = str(thumbnail.get("sha256"))
                steps.append(SyncStep(id="thumbnail", ok=True, detail="縮圖已上傳"))
    except YouTubeError as error:
        fail(step, f"YouTube 回 {error.status}：{error.detail}")
    except httpx.HTTPError as error:
        fail(step, f"連不上 YouTube：{error}")
    return await finish()
