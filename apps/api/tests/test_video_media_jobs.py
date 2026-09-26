"""The job state machine with fake vendors: budgets, dedupe, retries, locks, downloads, expiry."""

from __future__ import annotations

import copy
import hashlib
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import fakeredis
import httpx
import pytest

from app.config import Settings
from app.video_automation.models import DEFAULT_DRAMA, VideoAutomationSettings
from app.video_media import jobs as service
from app.video_media import meter
from app.video_media.jobs import MediaContext, MediaJobFailed, advance_job, job_view, submit_job
from app.video_media.models import VideoMediaJob
from app.video_media.providers import Download, MediaRequest, MediaUpstreamError, Polled, Submitted
from app.video_media.schemas import ClipJobIn, ImageJobIn, MusicJobIn
from app.video_media.settings import MediaSettings
from app.video_media.storage import MediaStore

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 30
MP4 = b"\x00\x00\x00\x18ftypisom" + b"\x00" * 30


class FakeSession:
    """Just enough of AsyncSession for the state machine: one lookup, add, commit."""

    def __init__(self) -> None:
        self.found: VideoMediaJob | None = None
        self.added: list[VideoMediaJob] = []
        self.commits = 0

    async def scalar(self, _statement: Any) -> VideoMediaJob | None:
        return self.found

    def add(self, row: VideoMediaJob) -> None:
        self.added.append(row)

    async def commit(self) -> None:
        self.commits += 1


class FakeProvider:
    def __init__(self, *, submit: Any = None, polls: list[Polled] | None = None) -> None:
        self.name = "fake"
        self.submit_result = submit
        self.polls = list(polls or [])
        self.requests: list[MediaRequest] = []

    async def submit(self, request: MediaRequest, client: httpx.AsyncClient) -> Submitted:
        self.requests.append(request)
        if isinstance(self.submit_result, Exception):
            raise self.submit_result
        return self.submit_result or Submitted(vendor_ref="task-1")

    async def poll(self, vendor_ref: str, client: httpx.AsyncClient) -> Polled:
        result = self.polls.pop(0)
        if isinstance(result, Exception):
            raise result
        return result

    def fetch(self, download: Download) -> tuple[str, dict[str, str]]:
        return download.url, {}


def _row(**changes: Any) -> VideoAutomationSettings:
    values = {**copy.deepcopy(DEFAULT_DRAMA), "drama_enabled": True, **changes}
    return VideoAutomationSettings(id=1, **values)


def _context(
    tmp_path: Path,
    provider: FakeProvider,
    row: VideoAutomationSettings | None = None,
    http: httpx.AsyncClient | None = None,
    **changes: Any,
) -> MediaContext:
    ctx = MediaContext(
        session=FakeSession(),  # type: ignore[arg-type]
        redis=fakeredis.aioredis.FakeRedis(),
        store=MediaStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000),
        runtime=Settings(hotspot_guide_gemini_api_key="g", minimax_api_key="m"),
        media=MediaSettings(video_media_dir=str(tmp_path), video_media_keep_days=3),
        row=row or _row(),
        token_id=uuid4(),
        http=http,
        **changes,
    )
    return ctx


@pytest.fixture
def fake_provider(monkeypatch: pytest.MonkeyPatch) -> FakeProvider:
    provider = FakeProvider()
    monkeypatch.setattr(service, "provider_for", lambda runtime, vendor, kind: provider)
    return provider


def _sheet(store: MediaStore, data: bytes = PNG) -> str:
    sha = hashlib.sha256(data).hexdigest()
    (store.root / "v").mkdir(exist_ok=True)
    (store.root / "v" / sha).write_bytes(data)
    return sha


def _image(**extra: Any) -> ImageJobIn:
    return ImageJobIn.model_validate(
        {"slug": "v", "purpose": "keyframe", "prompt": "a ridge at dawn", **extra}
    )


@pytest.mark.asyncio
async def test_a_synchronous_image_is_stored_and_ready_after_one_call(
    tmp_path: Path, fake_provider: FakeProvider
) -> None:
    fake_provider.submit_result = Submitted(inline=PNG, content_type="image/png")
    ctx = _context(tmp_path, fake_provider)
    sheet = _sheet(ctx.store)
    job, created = await submit_job(
        ctx, "image", _image(references=[{"sha256": sheet, "role": "character"}], seed=3)
    )
    assert created and job.status == "ready" and job.file_sha256 == hashlib.sha256(PNG).hexdigest()
    assert job.content_type == "image/png" and job.file_bytes == len(PNG)
    assert job.expires_at is not None and job.expires_at - job.ready_at == timedelta(days=3)  # type: ignore[operator]
    assert (
        fake_provider.requests[0].references[0].data == PNG and fake_provider.requests[0].seed == 3
    )
    assert float(job.usd_estimate) == 0.134
    assert await meter.used(ctx.redis, meter.IMAGES) == 1
    view = job_view(job)
    assert (
        view.retry_after_seconds == 0
        and view.file is not None
        and view.file.sha256 == job.file_sha256
    )
    assert ctx.session.added == [job] and ctx.session.commits >= 2  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_submissions_are_refused_before_the_vendor_when_they_cannot_run(
    tmp_path: Path, fake_provider: FakeProvider
) -> None:
    ctx = _context(tmp_path, fake_provider, row=_row(drama_enabled=False))
    with pytest.raises(MediaJobFailed) as disabled:
        await submit_job(ctx, "image", _image())
    assert disabled.value.code == "video_media_disabled"
    ctx = _context(tmp_path, fake_provider, row=_row(clip_model="nope"))
    with pytest.raises(MediaJobFailed) as unknown:
        await submit_job(
            ctx,
            "clip",
            ClipJobIn.model_validate(
                {"slug": "v", "shot_id": "a", "prompt": "p", "first_frame": "a" * 64, "seconds": 8}
            ),
        )
    assert unknown.value.code == "video_media_model_not_allowed"
    ctx = _context(tmp_path, fake_provider)
    with pytest.raises(MediaJobFailed) as missing:
        await submit_job(ctx, "image", _image(references=[{"sha256": "b" * 64}]))
    assert missing.value.code == "video_media_reference_missing"
    with pytest.raises(MediaJobFailed) as seconds:
        await submit_job(
            ctx,
            "clip",
            ClipJobIn.model_validate(
                {
                    "slug": "v",
                    "shot_id": "a",
                    "prompt": "p",
                    "first_frame": _sheet(ctx.store),
                    "seconds": 3,
                }
            ),
        )
    assert seconds.value.code == "video_media_model_not_allowed" and "秒" in seconds.value.detail
    ctx = _context(
        tmp_path,
        fake_provider,
        row=_row(monthly_images_budget=0),
    )
    ctx.row.monthly_images_budget = 1
    await meter.reserve(ctx.redis, meter.IMAGES, 1, 1)
    with pytest.raises(MediaJobFailed) as budget:
        await submit_job(ctx, "image", _image())
    assert budget.value.code == "video_media_budget_exhausted"
    assert fake_provider.requests == [], "nothing reached the vendor"
    ctx = _context(tmp_path, fake_provider, row=_row(music_enabled=False))
    with pytest.raises(MediaJobFailed):
        await submit_job(
            ctx, "music", MusicJobIn.model_validate({"slug": "v", "prompt": "guqin", "seconds": 60})
        )


@pytest.mark.asyncio
async def test_a_refused_generation_fails_and_gives_the_budget_back_but_a_busy_vendor_keeps_the_job(
    tmp_path: Path, fake_provider: FakeProvider
) -> None:
    fake_provider.submit_result = MediaUpstreamError(422, "sensitive", "blocked")
    ctx = _context(tmp_path, fake_provider)
    job, _created = await submit_job(ctx, "image", _image())
    assert job.status == "failed" and job.error_code == "video_media_rejected"
    assert await meter.used(ctx.redis, meter.IMAGES) == 0 and float(job.usd_estimate) == 0
    fake_provider.submit_result = MediaUpstreamError(429, "later", "busy", "20")
    ctx = _context(tmp_path, fake_provider)
    job, _created = await submit_job(ctx, "image", _image(prompt="another"))
    assert job.status == "queued" and job_view(job).retry_after_seconds == 20
    assert await meter.used(ctx.redis, meter.IMAGES) == 1, (
        "the budget stays reserved while it waits"
    )


@pytest.mark.asyncio
async def test_an_asynchronous_clip_is_polled_then_downloaded_into_the_store(
    tmp_path: Path, fake_provider: FakeProvider
) -> None:
    fake_provider.submit_result = Submitted(vendor_ref="task-7")
    fake_provider.polls = [
        Polled("running", retry_after=15),
        Polled("done", download=Download(url="https://cdn.example/clip.mp4")),
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "https://cdn.example/clip.mp4"
        return httpx.Response(200, content=MP4)

    ctx = _context(
        tmp_path, fake_provider, http=httpx.AsyncClient(transport=httpx.MockTransport(handler))
    )
    frame = _sheet(ctx.store, PNG)
    payload = ClipJobIn.model_validate(
        {"slug": "v", "shot_id": "opening", "prompt": "push in", "first_frame": frame, "seconds": 8}
    )
    job, _created = await submit_job(ctx, "clip", payload)
    assert job.status == "submitted" and job.vendor_ref == "task-7" and job.seconds == 8
    assert (
        fake_provider.requests[0].first_frame is not None
        and fake_provider.requests[0].resolution == "1080p"
    )
    assert await meter.used(ctx.redis, meter.CLIP_SECONDS) == 8 and float(job.usd_estimate) == 1.2
    await advance_job(ctx, job)
    assert job.status == "submitted" and job.polls == 1 and job_view(job).retry_after_seconds == 15
    await advance_job(ctx, job)
    assert job.status == "ready" and job.content_type == "video/mp4" and job.polls == 2
    assert ctx.store.path("v", job.file_sha256 or "") is not None
    await advance_job(ctx, job)
    assert job.status == "ready", "a finished job is left alone"


@pytest.mark.asyncio
async def test_a_failed_download_keeps_the_charge_and_a_failed_task_refunds_it(
    tmp_path: Path, fake_provider: FakeProvider
) -> None:
    fake_provider.polls = [
        Polled("done", download=Download(url="http://insecure.example/clip.mp4"))
    ]
    ctx = _context(tmp_path, fake_provider)
    job, _created = await submit_job(
        ctx,
        "clip",
        ClipJobIn.model_validate(
            {
                "slug": "v",
                "shot_id": "a",
                "prompt": "p",
                "first_frame": _sheet(ctx.store),
                "seconds": 8,
            }
        ),
    )
    monkeypatch_fetch = fake_provider.fetch

    def refusing_fetch(download: Download) -> tuple[str, dict[str, str]]:
        raise MediaUpstreamError(502, "not https", "invalid")

    fake_provider.fetch = refusing_fetch  # type: ignore[method-assign]
    await advance_job(ctx, job)
    assert job.status == "failed" and job.error_code == "video_media_upstream_invalid"
    assert await meter.used(ctx.redis, meter.CLIP_SECONDS) == 8, (
        "the vendor made the clip: no refund"
    )
    fake_provider.fetch = monkeypatch_fetch  # type: ignore[method-assign]
    fake_provider.polls = [Polled("failed", reason="task failed")]
    ctx = _context(tmp_path, fake_provider)
    job, _created = await submit_job(
        ctx,
        "clip",
        ClipJobIn.model_validate(
            {
                "slug": "v",
                "shot_id": "b",
                "prompt": "q",
                "first_frame": _sheet(ctx.store),
                "seconds": 8,
            }
        ),
    )
    await advance_job(ctx, job)
    assert job.status == "failed" and job.error_detail == "task failed"
    assert await meter.used(ctx.redis, meter.CLIP_SECONDS) == 0


@pytest.mark.asyncio
async def test_the_same_request_is_one_job_and_a_failed_one_is_retried_three_times(
    tmp_path: Path, fake_provider: FakeProvider
) -> None:
    fake_provider.submit_result = Submitted(inline=PNG, content_type="image/png")
    ctx = _context(tmp_path, fake_provider)
    job, created = await submit_job(ctx, "image", _image())
    ctx.session.found = job  # type: ignore[attr-defined]
    same, again = await submit_job(ctx, "image", _image())
    assert same is job and created and not again
    assert await meter.used(ctx.redis, meter.IMAGES) == 1, "no second reservation"
    job.status = "failed"
    job.attempts = 1
    fake_provider.submit_result = MediaUpstreamError(500, "boom", "failed")
    retried, _again = await submit_job(ctx, "image", _image())
    assert retried is job and job.attempts == 2 and job.status == "failed"
    job.attempts = 3
    with pytest.raises(MediaJobFailed) as exhausted:
        await submit_job(ctx, "image", _image())
    assert exhausted.value.code == "video_media_job_exhausted"


@pytest.mark.asyncio
async def test_a_second_poll_under_the_lock_waits_and_an_old_operation_expires(
    tmp_path: Path, fake_provider: FakeProvider
) -> None:
    fake_provider.polls = [Polled("running")]
    ctx = _context(tmp_path, fake_provider)
    job, _created = await submit_job(
        ctx,
        "clip",
        ClipJobIn.model_validate(
            {
                "slug": "v",
                "shot_id": "a",
                "prompt": "p",
                "first_frame": _sheet(ctx.store),
                "seconds": 8,
            }
        ),
    )
    await ctx.redis.set(f"video-media:lock:{job.id}", "1", ex=60)
    await advance_job(ctx, job)
    assert job.polls == 0 and job_view(job).retry_after_seconds == 5, "somebody else holds the lock"
    await ctx.redis.delete(f"video-media:lock:{job.id}")
    ctx.now = lambda: datetime.now(UTC) + timedelta(hours=25)
    await advance_job(ctx, job)
    assert job.status == "expired" and job.error_code == "video_media_upstream_expired"
    assert fake_provider.polls == [Polled("running")], "an expired job asks the vendor nothing"


def test_request_hashes_ignore_key_order_and_change_with_the_seed() -> None:
    a = service.request_hash(
        {"prompt": "x", "seed": 1, "references": [{"sha256": "a", "role": "character"}]}
    )
    b = service.request_hash(
        {"references": [{"role": "character", "sha256": "a"}], "seed": 1, "prompt": "x"}
    )
    assert a == b and a != service.request_hash({"prompt": "x", "seed": 2, "references": []})


def test_providers_are_built_from_the_site_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    runtime = Settings(hotspot_guide_gemini_api_key="g", minimax_api_key="m")
    assert service.provider_for(runtime, "gemini", "image").name == "gemini"
    assert type(service.provider_for(runtime, "gemini", "clip")).__name__ == "GeminiVideo"
    assert type(service.provider_for(runtime, "minimax", "clip")).__name__ == "MiniMaxVideo"
    with pytest.raises(MediaJobFailed) as no_music:
        service.provider_for(runtime, "minimax", "music")
    assert no_music.value.code == "video_media_model_not_allowed"
    with pytest.raises(MediaJobFailed) as no_key:
        service.provider_for(Settings(), "gemini", "image")
    assert no_key.value.code == "video_media_not_configured"
    _ = (AsyncMock, MagicMock)
