"""HTTP surface of the media stages. Operator-only: the pipeline calls it with a video tool token.

Every ``AppError`` of the package is raised here (the modules raise their own exceptions), the
way ``video_speech`` and ``video_reviews`` do, so the operator-path exemption of the error
localization test holds for the whole package. Reached through apps/web/app/api/video/media
(ticket 2026-09-26-video-drama-media-web-routes); nginx exposes only the web app.
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, Response
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.db import get_session
from app.infra import enforce_named_rate_limit, get_redis
from app.problems import AppError
from app.video_automation.models import STYLE_PRESETS
from app.video_automation.settings import media_options_view, settings_row
from app.video_media import meter
from app.video_media.jobs import (
    MediaContext,
    MediaJobFailed,
    advance_job,
    job_view,
    key_for,
    prune,
    submit_job,
)
from app.video_media.judge import JudgeError, judge
from app.video_media.models import VideoMediaJob
from app.video_media.schemas import (
    MAX_PROMPT_CHARS,
    MAX_REFERENCES,
    ChoiceView,
    ClipJobIn,
    ImageJobIn,
    JobOut,
    JudgeIn,
    JudgeOut,
    MediaStatus,
    MusicJobIn,
    StoreView,
)
from app.video_media.settings import MediaSettings, get_media_settings
from app.video_media.storage import MediaStore
from app.video_reviews.schemas import PartOut
from app.video_reviews.storage import PART_BYTES, StorageRefused
from app.video_speech.admin_api import VideoTool

_ = STYLE_PRESETS  # the tab's presets are named in the settings row; kept here for readers

media_router = APIRouter(prefix="/video/media", tags=["video media (pipeline)"])
Session = Annotated[AsyncSession, Depends(get_session)]

SUBMITS_PER_HOUR = 60
POLLS_PER_HOUR = 900
JUDGES_PER_HOUR = 120
UPLOADS_PER_HOUR = 600
DOWNLOADS_PER_HOUR = 600
PRUNE_MARK = "video-media:prune-ran"
PRUNE_EVERY_SECONDS = 3600


def media_store(media: MediaSettings) -> MediaStore:
    return MediaStore(
        media.video_media_dir,
        max_file_bytes=media.video_media_max_file_bytes,
        max_total_bytes=media.video_media_max_total_bytes,
    )


async def _context(session: AsyncSession, token_id: UUID | None) -> MediaContext:
    media = get_media_settings()
    return MediaContext(
        session=session,
        redis=get_redis(),
        store=media_store(media),
        runtime=await load_runtime_settings(session),
        media=media,
        row=await settings_row(session),
        token_id=token_id,
    )


def _refused(error: MediaJobFailed | JudgeError) -> AppError:
    return AppError(
        error.status,
        error.code,
        error.detail,
        headers={"Retry-After": error.retry_after} if error.retry_after else None,
    )


def _storage_refused(error: StorageRefused) -> AppError:
    # The store is shared with the reviews; its codes are renamed for this surface.
    return AppError(error.status, error.code.replace("video_review_", "video_media_"), error.detail)


async def _limit(name: str, tool_id: UUID, limit: int) -> None:
    await enforce_named_rate_limit(
        f"video_media_{name}", str(tool_id), limit=limit, window_seconds=3600
    )


async def _prune_sometimes(ctx: MediaContext) -> None:
    """Expire and delete old files at most once an hour, from a request that is writing anyway."""
    try:
        if await ctx.redis.set(PRUNE_MARK, "1", nx=True, ex=PRUNE_EVERY_SECONDS):
            await prune(ctx.session, ctx.store, ctx.media)
    except Exception:  # noqa: BLE001 -- housekeeping never fails the request that triggered it
        return


@media_router.get("/status", response_model=MediaStatus)
async def media_status(tool: VideoTool, session: Session) -> MediaStatus:
    ctx = await _context(session, tool.id)
    row = ctx.row
    media = ctx.media

    def choice(kind: str, provider: str, model: str) -> ChoiceView:
        return ChoiceView(
            provider=provider,
            model=model,
            configured=bool(key_for(ctx.runtime, provider)),
            resolution=row.clip_resolution if kind == "clip" else None,
            seconds=row.clip_seconds_default if kind == "clip" else None,
        )

    return MediaStatus(
        enabled=row.drama_enabled,
        music_enabled=row.music_enabled,
        image=choice("image", row.image_provider, row.image_model),
        clip=choice("clip", row.clip_provider, row.clip_model),
        music=choice("music", row.music_provider, row.music_model),
        models=media_options_view(),
        budgets=await meter.budgets_view(ctx.redis, row),
        estimated_usd=await meter.month_usd(session, ctx.redis),
        max_usd_per_video=row.max_usd_per_video,
        max_clips_per_video=row.max_clips_per_video,
        max_retakes_per_shot=row.max_retakes_per_shot,
        judge_min_score=row.judge_min_score,
        style_preset=row.style_preset,
        store=StoreView(
            used_bytes=ctx.store.used_bytes(),
            max_file_bytes=media.video_media_max_file_bytes,
            max_total_bytes=media.video_media_max_total_bytes,
            writable=ctx.store.writable(),
        ),
        limits={
            "max_reference_images": MAX_REFERENCES,
            "max_prompt_chars": MAX_PROMPT_CHARS,
            "part_bytes": PART_BYTES,
            "inline_judge_bytes": media.video_media_inline_judge_bytes,
            "max_file_bytes": media.video_media_max_file_bytes,
        },
    )


async def _submit(
    session: AsyncSession,
    tool_id: UUID,
    kind: str,
    payload: ImageJobIn | ClipJobIn | MusicJobIn,
    response: Response,
) -> JobOut:
    await _limit("submit", tool_id, SUBMITS_PER_HOUR)
    ctx = await _context(session, tool_id)
    try:
        job, created = await submit_job(ctx, kind, payload)
    except MediaJobFailed as error:
        raise _refused(error) from error
    if not created:
        response.status_code = 200
    await _prune_sometimes(ctx)
    return job_view(job)


@media_router.post("/images", response_model=JobOut, status_code=202)
async def submit_image(
    payload: ImageJobIn, tool: VideoTool, session: Session, response: Response
) -> JobOut:
    return await _submit(session, tool.id, "image", payload, response)


@media_router.post("/clips", response_model=JobOut, status_code=202)
async def submit_clip(
    payload: ClipJobIn, tool: VideoTool, session: Session, response: Response
) -> JobOut:
    return await _submit(session, tool.id, "clip", payload, response)


@media_router.post("/music", response_model=JobOut, status_code=202)
async def submit_music(
    payload: MusicJobIn, tool: VideoTool, session: Session, response: Response
) -> JobOut:
    return await _submit(session, tool.id, "music", payload, response)


@media_router.get("/jobs/{job_id}", response_model=JobOut)
async def poll_job(job_id: UUID, tool: VideoTool, session: Session) -> JobOut:
    """The job's state now; asking also moves it one step (vendor poll, download)."""
    await _limit("poll", tool.id, POLLS_PER_HOUR)
    job = await session.scalar(select(VideoMediaJob).where(VideoMediaJob.id == job_id))
    if job is None:
        raise AppError(404, "video_media_job_not_found", "找不到這個生成工作")
    ctx = await _context(session, tool.id)
    try:
        await advance_job(ctx, job)
    except MediaJobFailed as error:
        raise _refused(error) from error
    return job_view(job)


@media_router.put("/files/{slug}/{sha256}", response_model=PartOut)
async def upload_part(
    slug: str,
    sha256: str,
    request: Request,
    tool: VideoTool,
    part: Annotated[int, Query(ge=0, le=10_000)],
    parts: Annotated[int, Query(ge=1, le=10_000)],
    size: Annotated[int, Query(ge=1)],
) -> PartOut:
    """A file the tool made itself (a shot's last frame, an owner's reference), in parts."""
    await _limit("upload", tool.id, UPLOADS_PER_HOUR)
    body = await request.body()
    if len(body) > PART_BYTES:
        raise AppError(413, "video_media_part_too_large", f"每一段最多 {PART_BYTES} 位元組")
    store = media_store(get_media_settings())
    try:
        result = store.put_part(slug, sha256, index=part, count=parts, size=size, data=body)
    except StorageRefused as error:
        raise _storage_refused(error) from error
    return PartOut(received=result.received, complete=result.complete)


@media_router.get("/files/{slug}/{sha256}")
async def download_file(slug: str, sha256: str, tool: VideoTool) -> FileResponse:
    """A generated or uploaded file, with byte ranges; never cached outside the tool."""
    await _limit("download", tool.id, DOWNLOADS_PER_HOUR)
    store = media_store(get_media_settings())
    try:
        path = store.path(slug, sha256)
    except StorageRefused as error:
        raise _storage_refused(error) from error
    if path is None:
        raise AppError(404, "video_media_file_not_found", "媒體庫裡沒有這個檔案（可能已經清理）")
    return FileResponse(
        path,
        media_type=store.content_type_of(path),
        headers={
            "Cache-Control": "private, no-store",
            "ETag": f'"{sha256}"',
            "X-Content-Type-Options": "nosniff",
        },
    )


@media_router.post("/judge", response_model=JudgeOut)
async def judge_media(payload: JudgeIn, tool: VideoTool, session: Session) -> JudgeOut:
    """Gemini scores a sheet, a keyframe or a clip against the rubric; one call, one budget unit."""
    await _limit("judge", tool.id, JUDGES_PER_HOUR)
    ctx = await _context(session, tool.id)
    budget = meter.budget_of(ctx.row, meter.JUDGE_CALLS)
    if not await meter.reserve(ctx.redis, meter.JUDGE_CALLS, 1, budget):
        raise AppError(
            429,
            "video_media_budget_exhausted",
            f"本月的 judge 次數預算（{budget} 次）用完了；可到影片審核的設定分頁調高",
        )
    min_score = payload.min_score if payload.min_score is not None else ctx.row.judge_min_score
    try:
        return await judge(ctx.runtime, ctx.media, ctx.store, payload, min_score)
    except JudgeError as error:
        await meter.release(ctx.redis, meter.JUDGE_CALLS, 1)
        raise _refused(error) from error
