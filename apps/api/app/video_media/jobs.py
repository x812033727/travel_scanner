"""The job state machine: submitted by the tool, advanced one step per poll, stored on success.

Why poll-driven: the API has one uvicorn and no background task runner, and a vendor takes
between thirty seconds and several minutes per clip. So the tool asks, and each ask moves the
job one step: a queued job is sent to the vendor, a submitted one is checked, a finished one
is downloaded into the store. The row is written before the vendor is called and every state
change is committed, so a restart loses nothing and the vendor is never asked twice for the
same request. The budget is reserved before the vendor call and given back only when the
vendor refused or failed: a generation that succeeded is billed even when our download fails.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

import httpx
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models import VideoProject
from app.video_automation.models import VideoAutomationSettings
from app.video_media import meter
from app.video_media.catalog import MediaModel, find_model
from app.video_media.models import LIVE_STATUSES, MAX_ATTEMPTS, VideoMediaJob
from app.video_media.providers import (
    USER_AGENT,
    Download,
    MediaProvider,
    MediaRequest,
    MediaUpstreamError,
    ReferenceImage,
    Submitted,
    raise_for_status,
)
from app.video_media.providers.gemini_images import GeminiImages
from app.video_media.providers.gemini_music import GeminiMusic
from app.video_media.providers.gemini_video import GeminiVideo
from app.video_media.providers.minimax import MiniMaxImages, MiniMaxVideo
from app.video_media.schemas import (
    ClipJobIn,
    ImageJobIn,
    JobError,
    JobFile,
    JobOut,
    MusicJobIn,
    PruneOut,
)
from app.video_media.settings import MediaSettings
from app.video_media.storage import MediaStore
from app.video_reviews.storage import StorageRefused

LOCK_TTL_SECONDS = 240
LOCK_RETRY_SECONDS = 5
SUBMITTED_TTL = timedelta(hours=24)
MAX_REFERENCE_BYTES = 7_000_000
MAX_REFERENCES_TOTAL_BYTES = 20_000_000
TERMINAL = ("ready", "failed", "expired")
ERROR_CODES = {
    "blocked": "video_media_rejected",
    "key": "video_media_upstream_rejected_key",
    "invalid": "video_media_upstream_invalid",
    "failed": "video_media_upstream_failed",
    "expired": "video_media_upstream_expired",
    "busy": "video_media_upstream_busy",
}


class MediaJobFailed(Exception):
    """A submission the server refuses; ``admin_api`` turns it into the HTTP answer."""

    def __init__(self, status: int, code: str, detail: str, retry_after: str | None = None) -> None:
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail
        self.retry_after = retry_after


@dataclass
class MediaContext:
    session: AsyncSession
    redis: Redis
    store: MediaStore
    runtime: Settings
    media: MediaSettings
    row: VideoAutomationSettings
    token_id: UUID | None = None
    # Tests pass a client with a mock transport; otherwise one is opened per vendor call.
    http: httpx.AsyncClient | None = None
    now: Callable[[], datetime] = lambda: datetime.now(UTC)


def request_hash(fields: dict[str, Any]) -> str:
    canonical = json.dumps(fields, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def choice_for(row: VideoAutomationSettings, kind: str) -> tuple[str, str]:
    return {
        "image": (row.image_provider, row.image_model),
        "clip": (row.clip_provider, row.clip_model),
        "music": (row.music_provider, row.music_model),
    }[kind]


def key_for(runtime: Settings, vendor: str) -> str | None:
    if vendor == "gemini":
        return runtime.hotspot_guide_gemini_api_key or None
    if vendor == "minimax":
        return runtime.minimax_api_key or None
    return None


def provider_for(runtime: Settings, vendor: str, kind: str) -> MediaProvider:
    key = key_for(runtime, vendor)
    if not key:
        raise MediaJobFailed(503, "video_media_not_configured", f"網站還沒有 {vendor} 的金鑰")
    if vendor == "gemini":
        base = runtime.hotspot_guide_gemini_base_url
        if kind == "image":
            return GeminiImages(base, key)
        if kind == "clip":
            return GeminiVideo(base, key)
        return GeminiMusic(base, key)
    base = runtime.minimax_api_base_url
    if kind == "image":
        return MiniMaxImages(base, key)
    if kind == "clip":
        return MiniMaxVideo(base, key)
    raise MediaJobFailed(422, "video_media_model_not_allowed", "MiniMax 沒有音樂模型")


def _model(row: VideoAutomationSettings, kind: str) -> tuple[str, MediaModel]:
    vendor, model_id = choice_for(row, kind)
    model = find_model(vendor, kind, model_id)  # type: ignore[arg-type]
    if model is None or model.status == "retired":
        raise MediaJobFailed(
            422,
            "video_media_model_not_allowed",
            f"設定裡的{kind}模型 {model_id} 不能用；請到影片審核的設定分頁換一個",
        )
    return vendor, model


def _references(payload: ImageJobIn | ClipJobIn | MusicJobIn) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    if isinstance(payload, ClipJobIn):
        refs.append({"sha256": payload.first_frame, "role": "first_frame"})
        if payload.last_frame:
            refs.append({"sha256": payload.last_frame, "role": "last_frame"})
    if isinstance(payload, ImageJobIn | ClipJobIn):
        refs.extend({"sha256": ref.sha256, "role": ref.role} for ref in payload.references)
    return refs


def _check_references(store: MediaStore, slug: str, refs: list[dict[str, str]]) -> None:
    total = 0
    for ref in refs:
        path = store.path(slug, ref["sha256"])
        if path is None:
            raise MediaJobFailed(
                409,
                "video_media_reference_missing",
                f"參考檔 {ref['sha256'][:12]}… 不在媒體庫裡，請先上傳",
            )
        size = path.stat().st_size
        total += size
        if size > MAX_REFERENCE_BYTES or total > MAX_REFERENCES_TOTAL_BYTES:
            raise MediaJobFailed(
                413, "video_media_reference_too_large", "參考圖太大：每張最多 7 MB、合計 20 MB"
            )


def _request_fields(
    payload: ImageJobIn | ClipJobIn | MusicJobIn, row: VideoAutomationSettings, model: MediaModel
) -> dict[str, Any]:
    fields: dict[str, Any] = {
        "prompt": payload.prompt,
        "negative_prompt": payload.negative_prompt,
        "seed": payload.seed,
        "references": _references(payload),
    }
    if isinstance(payload, ImageJobIn):
        fields.update(
            aspect=payload.aspect, purpose=payload.purpose, shot_id=payload.shot_id, seconds=0
        )
    elif isinstance(payload, ClipJobIn):
        resolution = payload.resolution or row.clip_resolution
        if payload.seconds not in model.durations:
            raise MediaJobFailed(
                422,
                "video_media_model_not_allowed",
                f"{model.id} 一次只能做 {'、'.join(map(str, model.durations))} 秒",
            )
        if resolution not in model.resolutions:
            raise MediaJobFailed(
                422,
                "video_media_model_not_allowed",
                f"{model.id} 沒有 {resolution}，只有 {'、'.join(model.resolutions)}",
            )
        fields.update(
            aspect=row.drama_aspect,
            shot_id=payload.shot_id,
            seconds=payload.seconds,
            resolution=resolution,
            native_audio=payload.native_audio,
        )
    else:
        fields.update(seconds=payload.seconds)
    return fields


async def submit_job(
    ctx: MediaContext, kind: str, payload: ImageJobIn | ClipJobIn | MusicJobIn
) -> tuple[VideoMediaJob, bool]:
    """Create (or find) the job for this request and advance it once; returns (job, created)."""
    row = ctx.row
    if not row.drama_enabled:
        raise MediaJobFailed(
            503, "video_media_disabled", "漫劇還沒開啟：請到影片審核的設定分頁打開"
        )
    if kind == "music" and not row.music_enabled:
        raise MediaJobFailed(503, "video_media_disabled", "配樂生成已關閉")
    vendor, model = _model(row, kind)
    if not key_for(ctx.runtime, vendor):
        raise MediaJobFailed(503, "video_media_not_configured", f"網站還沒有 {vendor} 的金鑰")
    fields = _request_fields(payload, row, model)
    _check_references(ctx.store, payload.slug, fields["references"])
    digest = request_hash({"kind": kind, "vendor": vendor, "model": model.id, **fields})
    existing = await ctx.session.scalar(
        select(VideoMediaJob).where(
            VideoMediaJob.slug == payload.slug, VideoMediaJob.request_hash == digest
        )
    )
    seconds = int(fields.get("seconds") or 0)
    units = meter.units_of(kind, seconds)
    meter_name = meter.METER_BY_KIND[kind]
    if existing is not None:
        if existing.status in LIVE_STATUSES:
            await advance_job(ctx, existing)
            return existing, False
        if existing.attempts >= MAX_ATTEMPTS:
            raise MediaJobFailed(
                409,
                "video_media_job_exhausted",
                f"這個請求已經失敗 {existing.attempts} 次；改提示詞或 seed 再試",
            )
        if not await meter.reserve(ctx.redis, meter_name, units, meter.budget_of(row, meter_name)):
            raise MediaJobFailed(
                429, "video_media_budget_exhausted", _budget_message(meter_name, row)
            )
        existing.status = "queued"
        existing.attempts += 1
        existing.error_code = None
        existing.error_detail = None
        existing.vendor_ref = None
        existing.submitted_at = None
        existing.polls = 0
        existing.updated_at = ctx.now()
        await ctx.session.commit()
        await advance_job(ctx, existing)
        return existing, False
    if not await meter.reserve(ctx.redis, meter_name, units, meter.budget_of(row, meter_name)):
        raise MediaJobFailed(429, "video_media_budget_exhausted", _budget_message(meter_name, row))
    job = VideoMediaJob(
        id=uuid4(),
        slug=payload.slug,
        kind=kind,
        purpose=fields.get("purpose") or kind,
        shot_id=fields.get("shot_id"),
        provider=vendor,
        model=model.id,
        request=fields,
        request_hash=digest,
        idempotency_key=payload.idempotency_key,
        status="queued",
        attempts=1,
        polls=0,
        seconds=seconds,
        usd_estimate=meter.usd_for(model, kind, seconds),
        token_id=ctx.token_id,
        created_at=ctx.now(),
        updated_at=ctx.now(),
    )
    ctx.session.add(job)
    await ctx.session.commit()
    await advance_job(ctx, job)
    return job, True


def _budget_message(meter_name: str, row: VideoAutomationSettings) -> str:
    return (
        f"本月的{meter.BUDGET_NAMES[meter_name]}預算（{meter.budget_of(row, meter_name)} "
        f"{meter.UNITS[meter_name]}）不夠這次的請求；可到影片審核的設定分頁調高，或等下個月"
    )


async def advance_job(ctx: MediaContext, job: VideoMediaJob) -> VideoMediaJob:
    """Move the job one step, under a short lock so two polls do not both call the vendor."""
    if job.status in TERMINAL:
        return job
    lock = f"video-media:lock:{job.id}"
    if not await ctx.redis.set(lock, "1", nx=True, ex=LOCK_TTL_SECONDS):
        job.retry_after_seconds = LOCK_RETRY_SECONDS  # type: ignore[attr-defined]
        return job
    try:
        provider = provider_for(ctx.runtime, job.provider, job.kind)
        if job.status == "queued":
            await _submit(ctx, job, provider)
        elif job.status == "submitted":
            await _poll(ctx, job, provider)
    finally:
        await ctx.redis.delete(lock)
    return job


def _client(ctx: MediaContext, timeout: float) -> tuple[httpx.AsyncClient, bool]:
    if ctx.http is not None:
        return ctx.http, False
    return httpx.AsyncClient(timeout=timeout, trust_env=False), True


def _reference_image(ctx: MediaContext, slug: str, ref: dict[str, str]) -> ReferenceImage:
    path = ctx.store.path(slug, ref["sha256"])
    if path is None:
        raise MediaUpstreamError(
            409, f"reference {ref['sha256'][:12]} is gone from the store", "invalid"
        )
    return ReferenceImage(
        role=ref["role"], content_type=ctx.store.content_type_of(path), data=path.read_bytes()
    )


def _media_request(ctx: MediaContext, job: VideoMediaJob) -> MediaRequest:
    fields = job.request
    images = [_reference_image(ctx, job.slug, ref) for ref in fields.get("references", [])]
    first = next((image for image in images if image.role == "first_frame"), None)
    last = next((image for image in images if image.role == "last_frame"), None)
    others = tuple(image for image in images if image.role not in ("first_frame", "last_frame"))
    return MediaRequest(
        kind=job.kind,  # type: ignore[arg-type]
        model=job.model,
        prompt=str(fields.get("prompt") or ""),
        negative_prompt=fields.get("negative_prompt"),
        aspect=str(fields.get("aspect") or "16:9"),
        seconds=int(fields.get("seconds") or 0),
        resolution=fields.get("resolution"),
        native_audio=bool(fields.get("native_audio")),
        seed=fields.get("seed"),
        first_frame=first,
        last_frame=last,
        references=others,
    )


async def _submit(ctx: MediaContext, job: VideoMediaJob, provider: MediaProvider) -> None:
    try:
        request = _media_request(ctx, job)
    except MediaUpstreamError as error:
        await _fail(ctx, job, error, refund=True)
        return
    client, owned = _client(ctx, ctx.media.video_media_submit_timeout_seconds)
    try:
        submitted = await provider.submit(request, client)
    except MediaUpstreamError as error:
        if error.kind == "busy":
            job.retry_after_seconds = _retry_after(error, 30)  # type: ignore[attr-defined]
            return
        await _fail(ctx, job, error, refund=True)
        return
    finally:
        if owned:
            await client.aclose()
    await _settle(ctx, job, provider, submitted)


async def _settle(
    ctx: MediaContext, job: VideoMediaJob, provider: MediaProvider, submitted: Submitted
) -> None:
    now = ctx.now()
    if submitted.inline is not None:
        await _store_bytes(ctx, job, submitted.inline)
        return
    if submitted.download is not None:
        await _download(ctx, job, provider, submitted.download)
        return
    job.status = "submitted"
    job.vendor_ref = submitted.vendor_ref
    job.submitted_at = now
    job.polls = 0
    job.updated_at = now
    job.retry_after_seconds = 10  # type: ignore[attr-defined]
    await ctx.session.commit()


async def _poll(ctx: MediaContext, job: VideoMediaJob, provider: MediaProvider) -> None:
    now = ctx.now()
    if job.submitted_at is not None and now - job.submitted_at > SUBMITTED_TTL:
        job.status = "expired"
        job.error_code = ERROR_CODES["expired"]
        job.error_detail = "the vendor's operation is older than a day; submit it again"
        job.updated_at = now
        await ctx.session.commit()
        return
    client, owned = _client(ctx, ctx.media.video_media_poll_timeout_seconds)
    try:
        polled = await provider.poll(job.vendor_ref or "", client)
    except MediaUpstreamError as error:
        if error.kind == "busy":
            job.retry_after_seconds = _retry_after(error, 30)  # type: ignore[attr-defined]
            return
        await _fail(ctx, job, error, refund=error.kind != "invalid")
        return
    finally:
        if owned:
            await client.aclose()
    job.polls += 1
    job.updated_at = now
    if polled.state == "running":
        job.retry_after_seconds = polled.retry_after  # type: ignore[attr-defined]
        await ctx.session.commit()
        return
    if polled.state == "failed" or polled.download is None:
        await _fail(
            ctx,
            job,
            MediaUpstreamError(502, polled.reason or "the vendor's task failed", "failed"),
            refund=True,
        )
        return
    await _download(ctx, job, provider, polled.download)


async def _download(
    ctx: MediaContext, job: VideoMediaJob, provider: MediaProvider, download: Download
) -> None:
    try:
        url, headers = provider.fetch(download)
    except MediaUpstreamError as error:
        # The vendor made the file: billed, so no refund; the tool may ask again.
        await _fail(ctx, job, error, refund=False)
        return
    client, owned = _client(ctx, ctx.media.video_media_fetch_timeout_seconds)
    try:
        async with client.stream(
            "GET", url, headers={**headers, "User-Agent": USER_AGENT}
        ) as response:
            raise_for_status(response, provider.name)
            stored = await ctx.store.put_stream(job.slug, str(job.id), response.aiter_bytes())
    except MediaUpstreamError as error:
        await _fail(ctx, job, error, refund=False)
        return
    except StorageRefused as error:
        await _fail(
            ctx,
            job,
            MediaUpstreamError(error.status, error.detail, "failed"),
            refund=False,
            code=error.code,
        )
        return
    except httpx.HTTPError as error:
        await _fail(
            ctx,
            job,
            MediaUpstreamError(502, f"download failed: {type(error).__name__}", "failed"),
            refund=False,
        )
        return
    finally:
        if owned:
            await client.aclose()
    await _ready(ctx, job, stored.sha256, stored.size, stored.content_type)


async def _store_bytes(ctx: MediaContext, job: VideoMediaJob, data: bytes) -> None:
    async def chunks() -> Any:
        yield data

    try:
        stored = await ctx.store.put_stream(job.slug, str(job.id), chunks())
    except StorageRefused as error:
        await _fail(
            ctx,
            job,
            MediaUpstreamError(error.status, error.detail, "failed"),
            refund=False,
            code=error.code,
        )
        return
    await _ready(ctx, job, stored.sha256, stored.size, stored.content_type)


async def _ready(
    ctx: MediaContext, job: VideoMediaJob, sha256: str, size: int, content_type: str
) -> None:
    now = ctx.now()
    job.status = "ready"
    job.file_sha256 = sha256
    job.file_bytes = size
    job.content_type = content_type
    job.ready_at = now
    job.expires_at = now + timedelta(days=ctx.media.video_media_keep_days)
    job.error_code = None
    job.error_detail = None
    job.updated_at = now
    await ctx.session.commit()


async def _fail(
    ctx: MediaContext,
    job: VideoMediaJob,
    error: MediaUpstreamError,
    *,
    refund: bool,
    code: str | None = None,
) -> None:
    job.status = "failed"
    job.error_code = code or ERROR_CODES.get(error.kind, "video_media_upstream_failed")
    job.error_detail = error.message[:2000]
    job.updated_at = ctx.now()
    if refund:
        job.usd_estimate = Decimal("0")
        await meter.release(
            ctx.redis, meter.METER_BY_KIND[job.kind], meter.units_of(job.kind, job.seconds)
        )
    await ctx.session.commit()


def _retry_after(error: MediaUpstreamError, default: int) -> int:
    try:
        value = int(error.retry_after or default)
    except ValueError:
        value = default
    return max(1, min(value, 120))


def job_view(job: VideoMediaJob) -> JobOut:
    if job.status in TERMINAL:
        retry = 0
    else:
        retry = int(getattr(job, "retry_after_seconds", 10 if job.status == "submitted" else 5))
    file = (
        JobFile(
            sha256=job.file_sha256,
            size=int(job.file_bytes or 0),
            content_type=job.content_type or "application/octet-stream",
        )
        if job.status == "ready" and job.file_sha256
        else None
    )
    error = JobError(code=job.error_code, detail=job.error_detail or "") if job.error_code else None
    return JobOut(
        id=job.id,
        slug=job.slug,
        kind=job.kind,
        status=job.status,
        provider=job.provider,
        model=job.model,
        seconds=job.seconds,
        file=file,
        error=error,
        retry_after_seconds=retry,
        attempts=job.attempts,
        polls=job.polls,
        usd_estimate=float(job.usd_estimate or 0),
        created_at=job.created_at,
        submitted_at=job.submitted_at,
        ready_at=job.ready_at,
        expires_at=job.expires_at,
    )


async def prune(
    session: AsyncSession,
    store: MediaStore,
    media: MediaSettings,
    now: datetime | None = None,
    *,
    dry_run: bool = False,
) -> PruneOut:
    """Expire old jobs and delete what no live job names: the store is a cache, not an archive."""
    moment = now or datetime.now(UTC)
    cutoff = moment - timedelta(days=media.video_media_keep_days)
    expired = 0
    deleted = 0
    freed = 0
    finished = await session.scalars(
        select(VideoProject.slug).where(
            (VideoProject.dropped_at.is_not(None)) | (VideoProject.youtube_video_id.is_not(None))
        )
    )
    done_slugs = set(finished)
    jobs = list(
        await session.scalars(select(VideoMediaJob).where(VideoMediaJob.status.in_(LIVE_STATUSES)))
    )
    keep: dict[str, set[str]] = {}
    for job in jobs:
        stale = job.status == "ready" and job.ready_at is not None and job.ready_at < cutoff
        if job.slug in done_slugs or stale:
            expired += 1
            if not dry_run:
                job.status = "expired"
                job.updated_at = moment
            continue
        if job.file_sha256:
            keep.setdefault(job.slug, set()).add(job.file_sha256)
    for slug in store.slugs():
        if slug in done_slugs:
            for path in store.files(slug).values():
                freed += path.stat().st_size
                deleted += 1
            if not dry_run:
                store.delete_project(slug)
            continue
        if dry_run:
            for name, path in store.files(slug).items():
                if (
                    name not in keep.get(slug, set())
                    and datetime.fromtimestamp(path.stat().st_mtime, tz=UTC) < cutoff
                ):
                    deleted += 1
                    freed += path.stat().st_size
            continue
        for _name, size in store.prune_files(slug, keep.get(slug, set()), cutoff):
            deleted += 1
            freed += size
    if not dry_run:
        await session.commit()
    return PruneOut(expired_jobs=expired, deleted_files=deleted, freed_bytes=freed)
