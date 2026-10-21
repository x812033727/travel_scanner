"""The job state machine with fake vendors: budgets, dedupe, retries, locks, downloads, expiry."""

from __future__ import annotations

import asyncio
import base64
import copy
import hashlib
import json
import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import fakeredis
import httpx
import pytest
import pytest_asyncio
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import Settings
from app.db import engine as postgres_engine
from app.models import VideoToolToken
from app.video_automation.models import DEFAULT_DRAMA, DEFAULT_SLIDES, VideoAutomationSettings
from app.video_budget.models import VideoPilotBudget
from app.video_budget.service import A01_ADMISSION_SLUG, Reservation, assert_a01_admission_open
from app.video_media import cutover_intake, meter
from app.video_media import jobs as service
from app.video_media.catalog import find_model
from app.video_media.dispatch_fence import PINNED_JOB_ID, expected_manifest, fence_path
from app.video_media.jobs import MediaContext, MediaJobFailed, advance_job, job_view, submit_job
from app.video_media.models import VideoMediaJob
from app.video_media.providers import Download, MediaRequest, MediaUpstreamError, Polled, Submitted
from app.video_media.providers.minimax import MiniMaxImages, MiniMaxMusic
from app.video_media.schemas import ClipJobIn, ImageJobIn, MusicJobIn
from app.video_media.settings import MediaSettings
from app.video_media.storage import MediaStore

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 30
JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 30
MP4 = b"\x00\x00\x00\x18ftypisom" + b"\x00" * 30


class FakeSession:
    """Just enough of AsyncSession for the state machine: one lookup, add, commit."""

    def __init__(self) -> None:
        self.found: VideoMediaJob | None = None
        self.added: list[VideoMediaJob] = []
        self.commits = 0
        self.last_statement: Any = None

    async def scalar(self, _statement: Any) -> VideoMediaJob | None:
        self.last_statement = _statement
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


@pytest.mark.parametrize(
    "extra",
    [{"seconds": 4}, {"seconds": 6}, {"references": [{"sha256": "b" * 64}]}],
)
@pytest.mark.asyncio
async def test_lite_incompatible_jobs_spend_nothing(tmp_path: Path, extra: dict[str, Any]) -> None:
    provider = FakeProvider()
    ctx = _context(
        tmp_path,
        provider,
        row=_row(clip_model="veo-3.1-lite-generate-preview", clip_resolution="1080p"),
    )
    payload = ClipJobIn.model_validate(
        {
            "slug": "v",
            "shot_id": "opening",
            "prompt": "push in",
            "first_frame": "a" * 64,
            "seconds": 8,
            **extra,
        }
    )
    with pytest.raises(MediaJobFailed) as refused:
        await submit_job(ctx, "clip", payload)
    assert refused.value.code == "video_media_model_not_allowed"
    assert provider.requests == [] and ctx.session.added == []  # type: ignore[attr-defined]
    assert ctx.session.commits == 0  # type: ignore[attr-defined]


@pytest.mark.parametrize("role", ["character", "style", "previous_frame"])
@pytest.mark.asyncio
async def test_h3_refuses_a_reference_its_v2_request_could_never_carry(
    tmp_path: Path, role: str
) -> None:
    """H3's v2 image-to-video request holds no reference beside the first frame every clip has
    (providers/minimax.py), so the catalog gives it 0 and a reference is refused, unspent,
    instead of being stored, counted and dropped; its frames alone pass."""
    model = find_model("minimax", "clip", "MiniMax-H3")
    assert model is not None and model.reference_images == 0
    provider = FakeProvider()
    row = _row(clip_provider="minimax", clip_model="MiniMax-H3", clip_resolution="2k")
    ctx = _context(tmp_path, provider, row=row)
    clip = {
        "slug": "v",
        "shot_id": "opening",
        "prompt": "push in",
        "first_frame": "a" * 64,
        "last_frame": "c" * 64,
        "seconds": 8,
    }
    payload = ClipJobIn.model_validate({**clip, "references": [{"sha256": "b" * 64, "role": role}]})
    with pytest.raises(MediaJobFailed) as refused:
        await submit_job(ctx, "clip", payload)
    assert (refused.value.status, refused.value.code) == (422, "video_media_model_not_allowed")
    assert refused.value.detail.startswith("MiniMax H3")
    assert provider.requests == [] and ctx.session.added == []  # type: ignore[attr-defined]
    assert ctx.session.commits == 0  # type: ignore[attr-defined]
    assert await meter.used(ctx.redis, meter.CLIP_SECONDS) == 0
    fields = service._request_fields(ClipJobIn.model_validate(clip), row, model)
    assert [ref["role"] for ref in fields["references"]] == ["first_frame", "last_frame"]


def _row(**changes: Any) -> VideoAutomationSettings:
    values = {
        **copy.deepcopy(DEFAULT_DRAMA),
        **copy.deepcopy(DEFAULT_SLIDES),
        "drama_enabled": True,
        **changes,
    }
    return VideoAutomationSettings(id=1, **values)


def test_a_2k_picture_is_refused_for_a_model_priced_at_1k_only() -> None:
    minimax = find_model("minimax", "image", "image-01")
    assert minimax is not None and minimax.usd_per_image_2k is None
    with pytest.raises(MediaJobFailed) as refused:
        service._request_fields(_image(size="2K"), _row(), minimax)
    assert refused.value.status == 422 and refused.value.code == "video_media_model_not_allowed"
    assert "2K" in refused.value.detail
    pro = find_model("gemini", "image", "gemini-3-pro-image")
    assert pro is not None
    assert service._request_fields(_image(size="2K"), _row(), pro)["resolution"] == "2K"
    assert "resolution" not in service._request_fields(_image(size="1K"), _row(), pro)
    assert meter.usd_for(pro, "image", 0, "2K") == meter.usd_for(pro, "image", 0), (
        "Pro's 2K costs the 1K price"
    )


def test_lite_job_records_always_on_native_audio_even_when_final_edit_discards_it() -> None:
    model = find_model("gemini", "clip", "veo-3.1-lite-generate-preview")
    assert model is not None
    payload = ClipJobIn.model_validate(
        {
            "slug": "v",
            "shot_id": "opening",
            "prompt": "push in",
            "first_frame": "a" * 64,
            "seconds": 8,
            "native_audio": False,
        }
    )
    fields = service._request_fields(payload, _row(clip_resolution="1080p"), model)
    assert fields["native_audio"] is True and fields["seconds"] == 8


def _context(
    tmp_path: Path,
    provider: FakeProvider,
    row: VideoAutomationSettings | None = None,
    http: httpx.AsyncClient | None = None,
    **changes: Any,
) -> MediaContext:
    marker_dir = tmp_path / cutover_intake.INTAKE_DIR
    marker_dir.mkdir(mode=0o755, exist_ok=True)
    (marker_dir / cutover_intake.MARKER).write_bytes(
        cutover_intake.canonical_json(
            {
                "schema_version": 1,
                "state": "BOOTSTRAP_ALLOW",
                "bootstrap_id": "a" * 64,
                "plan_sha256": None,
                "target_sha": None,
                "nonce_sha256": None,
            }
        )
    )
    ctx = MediaContext(
        session=FakeSession(),  # type: ignore[arg-type]
        redis=fakeredis.aioredis.FakeRedis(),
        store=MediaStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000),
        runtime=Settings(
            hotspot_guide_gemini_api_key="g", minimax_api_key="m", video_work_dir=str(tmp_path)
        ),
        media=MediaSettings(video_media_dir=str(tmp_path), video_media_keep_days=3),
        row=row or _row(),
        token_id=uuid4(),
        http=http,
        **changes,
    )
    return ctx


def _pause_intake(root: Path) -> None:
    folder = root / cutover_intake.INTAKE_DIR
    (folder / cutover_intake.ARMED).write_bytes(
        cutover_intake.canonical_json(
            {
                "schema_version": 1,
                "bootstrap_id": "a" * 64,
                "plan_sha256": "b" * 64,
                "target_sha": "c" * 40,
            }
        )
    )
    (folder / cutover_intake.MARKER).write_bytes(
        cutover_intake.canonical_json(
            {
                "schema_version": 1,
                "state": "PAUSED_ALL",
                "bootstrap_id": "a" * 64,
                "plan_sha256": "b" * 64,
                "target_sha": "c" * 40,
                "nonce_sha256": None,
            }
        )
    )


async def _allow_a01_intake(root: Path, redis: Any) -> None:
    nonce = b"durable-suncatcher-hold"
    await redis.set(cutover_intake.NONCE_KEY, nonce)
    folder = root / cutover_intake.INTAKE_DIR
    (folder / cutover_intake.ARMED).write_bytes(
        cutover_intake.canonical_json(
            {
                "schema_version": 1,
                "bootstrap_id": "a" * 64,
                "plan_sha256": "b" * 64,
                "target_sha": "c" * 40,
            }
        )
    )
    (folder / cutover_intake.MARKER).write_bytes(
        cutover_intake.canonical_json(
            {
                "schema_version": 1,
                "state": "ALLOW_A01_ONLY",
                "bootstrap_id": "a" * 64,
                "plan_sha256": "b" * 64,
                "target_sha": "c" * 40,
                "nonce_sha256": hashlib.sha256(nonce).hexdigest(),
            }
        )
    )


@pytest.fixture(autouse=True)
def local_marker_owner(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    if os.name == "posix":
        monkeypatch.setattr(cutover_intake, "ROOT_UID", tmp_path.stat().st_uid)


@pytest.fixture
def fake_provider(monkeypatch: pytest.MonkeyPatch) -> FakeProvider:
    provider = FakeProvider()
    monkeypatch.setattr(service, "provider_for", lambda runtime, vendor, kind: provider)
    return provider


@pytest.mark.asyncio
async def test_allow_a01_closing_during_pilot_reserve_stops_submit_without_uncertain_charge(
    tmp_path: Path, fake_provider: FakeProvider, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "assert_a01_admission_open", AsyncMock())
    ctx = _context(
        tmp_path,
        fake_provider,
        row=_row(image_provider="minimax", image_model="image-01"),
    )
    await _allow_a01_intake(tmp_path, ctx.redis)
    released = AsyncMock()
    uncertain = AsyncMock()
    monkeypatch.setattr(service, "release", released)
    monkeypatch.setattr(service, "mark_uncertain", uncertain)

    async def reserve_then_pause(
        _session: Any, *, slug: str, operation_id: str, max_usd: Decimal, **_rest: Any
    ) -> Reservation:
        _pause_intake(tmp_path)
        return Reservation(slug, operation_id, max_usd, "reserved", True, True, 1)

    monkeypatch.setattr(service, "reserve", reserve_then_pause)
    with pytest.raises(MediaJobFailed) as refused:
        await submit_job(ctx, "image", _image(slug="story-rolling-suitcase-v2"))
    assert (refused.value.status, refused.value.code) == (423, "video_media_cutover_paused")
    assert fake_provider.requests == []
    queued = ctx.session.added[0]  # type: ignore[attr-defined]
    assert queued.status == "queued" and "pilot_budget_operation_id" not in queued.request
    assert await meter.used(ctx.redis, meter.IMAGES) == 1, "queued job keeps its monthly slot"
    assert released.await_args.kwargs["reason"] == "paid intake paused before vendor dispatch"
    uncertain.assert_not_awaited()


@pytest.mark.asyncio
async def test_bootstrap_closing_while_lock_is_acquired_stops_queued_submit(
    tmp_path: Path, fake_provider: FakeProvider, monkeypatch: pytest.MonkeyPatch
) -> None:
    ctx = _context(tmp_path, fake_provider)
    original_set = ctx.redis.set

    async def set_then_pause(key: Any, *args: Any, **kwargs: Any) -> Any:
        result = await original_set(key, *args, **kwargs)
        if str(key).startswith("video-media:lock:"):
            _pause_intake(tmp_path)
        return result

    monkeypatch.setattr(ctx.redis, "set", set_then_pause)
    with pytest.raises(MediaJobFailed) as refused:
        await submit_job(ctx, "image", _image())
    assert refused.value.code == "video_media_cutover_paused"
    assert fake_provider.requests == []
    assert ctx.session.added[0].status == "queued"  # type: ignore[attr-defined]
    assert await meter.used(ctx.redis, meter.IMAGES) == 1


@pytest.mark.asyncio
async def test_submitted_poll_rechecks_after_lock_wait(
    tmp_path: Path, fake_provider: FakeProvider, monkeypatch: pytest.MonkeyPatch
) -> None:
    ctx = _context(tmp_path, fake_provider)
    job = VideoMediaJob(
        id=uuid4(), slug="v", kind="image", purpose="keyframe", provider="minimax",
        model="image-01", request={}, request_hash="h", status="submitted", attempts=1,
        polls=0, seconds=0, usd_estimate=Decimal("0.0035"), vendor_ref="task-1",
    )
    fake_provider.polls = [Polled("running")]
    original_set = ctx.redis.set

    async def set_then_pause(key: Any, *args: Any, **kwargs: Any) -> Any:
        result = await original_set(key, *args, **kwargs)
        if str(key).startswith("video-media:lock:"):
            _pause_intake(tmp_path)
        return result

    monkeypatch.setattr(ctx.redis, "set", set_then_pause)
    with pytest.raises(MediaJobFailed) as refused:
        await advance_job(ctx, job)
    assert refused.value.code == "video_media_cutover_paused"
    assert fake_provider.polls == [Polled("running")]
    assert job.status == "submitted" and job.vendor_ref == "task-1"


@pytest.mark.asyncio
async def test_completed_vendor_poll_cannot_start_download_after_pause(
    tmp_path: Path, fake_provider: FakeProvider, monkeypatch: pytest.MonkeyPatch
) -> None:
    ctx = _context(tmp_path, fake_provider)
    job = VideoMediaJob(
        id=uuid4(), slug="v", kind="image", purpose="keyframe", provider="minimax",
        model="image-01", request={}, request_hash="h", status="submitted", attempts=1,
        polls=0, seconds=0, usd_estimate=Decimal("0.0035"), vendor_ref="task-1",
    )

    async def poll_then_pause(_ref: str, _client: httpx.AsyncClient) -> Polled:
        _pause_intake(tmp_path)
        return Polled("done", download=Download("https://example.com/p.png"))

    monkeypatch.setattr(fake_provider, "poll", poll_then_pause)
    with pytest.raises(MediaJobFailed) as refused:
        await advance_job(ctx, job)
    assert refused.value.code == "video_media_cutover_paused"
    assert job.status == "submitted" and job.vendor_ref == "task-1"
    assert job.file_sha256 is None


@pytest.mark.asyncio
async def test_accepted_image_url_survives_pause_and_resumes_without_second_paid_submit(
    tmp_path: Path, fake_provider: FakeProvider, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "assert_a01_admission_open", AsyncMock())
    slug = "story-rolling-suitcase-v2"
    payload = _image(slug=slug)
    url = "https://example.com/accepted-image.png"
    asked: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        asked.append(request)
        return httpx.Response(200, content=PNG, headers={"Content-Type": "image/png"})

    async def accepted_then_pause(request: MediaRequest, _client: httpx.AsyncClient) -> Submitted:
        fake_provider.requests.append(request)
        _pause_intake(tmp_path)
        return Submitted(download=Download(url, content_type_hint="image/png"))

    monkeypatch.setattr(fake_provider, "submit", accepted_then_pause)
    reserve_mock = AsyncMock(
        side_effect=lambda _session, **kwargs: Reservation(
            slug,
            kwargs["operation_id"],
            kwargs["max_usd"],
            "reserved",
            True,
            True,
            1,
        )
    )
    release_mock = AsyncMock()
    uncertain_mock = AsyncMock()
    settle_mock = AsyncMock()
    monkeypatch.setattr(service, "reserve", reserve_mock)
    monkeypatch.setattr(service, "release", release_mock)
    monkeypatch.setattr(service, "mark_uncertain", uncertain_mock)
    monkeypatch.setattr(service, "settle", settle_mock)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        ctx = _context(
            tmp_path,
            fake_provider,
            http=http,
            row=_row(image_provider="minimax", image_model="image-01"),
        )
        with pytest.raises(MediaJobFailed) as paused:
            await submit_job(ctx, "image", payload)
        assert paused.value.code == "video_media_cutover_paused"
        job = ctx.session.added[0]  # type: ignore[attr-defined]
        assert job.status == "submitted" and job.submitted_at is not None
        assert job.request[service.ACCEPTED_DOWNLOAD_KEY]["url"] == url
        assert len(fake_provider.requests) == 1 and asked == []
        assert await meter.used(ctx.redis, meter.IMAGES) == 1
        release_mock.assert_not_awaited()
        uncertain_mock.assert_not_awaited()
        settle_mock.assert_not_awaited()

        await _allow_a01_intake(tmp_path, ctx.redis)
        ctx.session.found = job  # type: ignore[attr-defined]
        resumed, created = await submit_job(ctx, "image", payload)
        assert resumed is job and not created and job.status == "ready"
        assert job.file_sha256 == hashlib.sha256(PNG).hexdigest()
        assert service.ACCEPTED_DOWNLOAD_KEY not in job.request
        assert len(fake_provider.requests) == 1 and len(asked) == 1
        assert asked[0].method == "GET" and str(asked[0].url) == url
        assert await meter.used(ctx.redis, meter.IMAGES) == 1
        reserve_mock.assert_awaited_once()
        settle_mock.assert_awaited_once()
        release_mock.assert_not_awaited()
        uncertain_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_minimax_music_accepted_url_stays_submitted_under_pause(
    tmp_path: Path, fake_provider: FakeProvider, monkeypatch: pytest.MonkeyPatch
) -> None:
    ctx = _context(
        tmp_path,
        fake_provider,
        row=_row(music_provider="minimax", music_model="music-3.0"),
    )
    payload = MusicJobIn.model_validate({"slug": "v", "prompt": "solo guqin", "seconds": 60})
    url = "https://example.com/accepted-music.mp3"

    async def accepted_then_pause(request: MediaRequest, _client: httpx.AsyncClient) -> Submitted:
        fake_provider.requests.append(request)
        _pause_intake(tmp_path)
        return Submitted(download=Download(url, content_type_hint="audio/mpeg"))

    monkeypatch.setattr(fake_provider, "submit", accepted_then_pause)
    with pytest.raises(MediaJobFailed) as paused:
        await submit_job(ctx, "music", payload)
    assert paused.value.code == "video_media_cutover_paused"
    job = ctx.session.added[0]  # type: ignore[attr-defined]
    assert job.status == "submitted"
    assert job.request[service.ACCEPTED_DOWNLOAD_KEY]["url"] == url
    assert job.usd_estimate > 0 and await meter.used(ctx.redis, meter.MUSIC) == 1
    assert len(fake_provider.requests) == 1
    ctx.session.found = job  # type: ignore[attr-defined]
    with pytest.raises(MediaJobFailed) as still_paused:
        await submit_job(ctx, "music", payload)
    assert still_paused.value.code == "video_media_cutover_paused"
    assert len(fake_provider.requests) == 1
    # A later reviewed release may reopen non-A01 intake; this unit test isolates
    # the already-accepted recovery path because the current marker has no ALLOW_ALL.
    monkeypatch.setattr(service, "refuse_unapproved_paid_intake", AsyncMock())

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET" and str(request.url) == url
        return httpx.Response(200, content=MP3, headers={"Content-Type": "audio/mpeg"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        ctx.http = http
        resumed, created = await submit_job(ctx, "music", payload)
    assert resumed is job and not created and job.status == "ready"
    assert job.file_sha256 == hashlib.sha256(MP3).hexdigest()
    assert service.ACCEPTED_DOWNLOAD_KEY not in job.request
    assert await meter.used(ctx.redis, meter.MUSIC) == 1
    assert len(fake_provider.requests) == 1


@pytest.mark.asyncio
async def test_failed_accepted_download_cannot_rebuy_the_same_request(
    tmp_path: Path, fake_provider: FakeProvider
) -> None:
    url = "https://example.com/expired-image.png"
    fake_provider.submit_result = Submitted(download=Download(url))

    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == url
        return httpx.Response(503)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        ctx = _context(tmp_path, fake_provider, http=http)
        payload = _image()
        job, created = await submit_job(ctx, "image", payload)
        assert created and job.status == "failed"
        assert service.ACCEPTED_DOWNLOAD_KEY in job.request
        assert job.usd_estimate > 0 and await meter.used(ctx.redis, meter.IMAGES) == 1
        ctx.session.found = job  # type: ignore[attr-defined]
        with pytest.raises(MediaJobFailed) as refused:
            await submit_job(ctx, "image", payload)
        assert (refused.value.status, refused.value.code) == (
            409,
            "video_media_outcome_uncertain",
        )
        assert len(fake_provider.requests) == 1


def _sheet(store: MediaStore, data: bytes = PNG) -> str:
    sha = hashlib.sha256(data).hexdigest()
    (store.root / "v").mkdir(exist_ok=True)
    (store.root / "v" / sha).write_bytes(data)
    return sha


def _image(**extra: Any) -> ImageJobIn:
    return ImageJobIn.model_validate(
        {"slug": "v", "purpose": "keyframe", "prompt": "a ridge at dawn", **extra}
    )


@pytest_asyncio.fixture
async def a01_media_sessions(
    tmp_path: Path,
) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    database = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'a01-media.sqlite'}")
    async with database.begin() as connection:
        await connection.run_sync(
            lambda sync: VideoPilotBudget.metadata.create_all(
                sync,
                tables=[
                    VideoToolToken.__table__,
                    VideoPilotBudget.__table__,
                    VideoMediaJob.__table__,
                ],
            )
        )
        await connection.execute(
            sa.insert(VideoPilotBudget).values(
                slug=A01_ADMISSION_SLUG, limit_usd=Decimal("25")
            )
        )
    yield async_sessionmaker(database, expire_on_commit=False)
    await database.dispose()


@pytest.mark.parametrize("status", ["queued", "ready"])
@pytest.mark.asyncio
async def test_a01_existing_receipt_is_read_under_account_lock(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, status: str
) -> None:
    monkeypatch.setattr(service, "project_format", AsyncMock(return_value=None))
    monkeypatch.setattr(service, "series_image_model", AsyncMock(return_value=None))
    admission = AsyncMock()
    monkeypatch.setattr(service, "assert_a01_admission_open", admission)
    fenced = MagicMock()
    monkeypatch.setattr(service, "_refuse_fenced_dispatch", fenced)
    advance = AsyncMock()
    monkeypatch.setattr(service, "advance_job", advance)
    receipt = VideoMediaJob(
        id=uuid4(),
        slug=A01_ADMISSION_SLUG,
        kind="image",
        purpose="keyframe",
        provider="minimax",
        model="image-01",
        request={},
        request_hash="a" * 64,
        status=status,
        attempts=1,
        polls=0,
        usd_estimate=Decimal("0.0035"),
    )
    ctx = _context(
        tmp_path,
        FakeProvider(),
        row=_row(image_provider="minimax", image_model="image-01"),
    )
    lookups = 0

    async def lookup_row(_statement: Any) -> VideoMediaJob | None:
        nonlocal lookups
        lookups += 1
        if lookups == 2:
            assert admission.await_count == 1, "the A01 account lock must precede the job lock"
        else:
            assert admission.await_count == 0, "ready probe must not take the account lock"
        return receipt

    lookup = AsyncMock(side_effect=lookup_row)
    monkeypatch.setattr(ctx.session, "scalar", lookup)
    found, created = await submit_job(ctx, "image", _image(slug=A01_ADMISSION_SLUG))
    assert found is receipt and not created
    assert lookup.await_count == (1 if status == "ready" else 2)
    assert admission.await_count == (0 if status == "ready" else 1)
    fenced.assert_called_once_with(ctx, receipt)
    assert ctx.session.added == []  # type: ignore[attr-defined]
    assert await meter.used(ctx.redis, meter.IMAGES) == 0
    advance.assert_awaited_once()


@pytest.mark.asyncio
async def test_a01_locked_accepted_download_receipt_cannot_rebuy(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "project_format", AsyncMock(return_value=None))
    monkeypatch.setattr(service, "series_image_model", AsyncMock(return_value=None))
    admission = AsyncMock()
    monkeypatch.setattr(service, "assert_a01_admission_open", admission)
    monthly_reserve = AsyncMock()
    monkeypatch.setattr(meter, "reserve", monthly_reserve)
    advance = AsyncMock()
    monkeypatch.setattr(service, "advance_job", advance)
    provider = FakeProvider()
    receipt = VideoMediaJob(
        id=uuid4(),
        slug=A01_ADMISSION_SLUG,
        kind="image",
        purpose="keyframe",
        provider="minimax",
        model="image-01",
        request={
            service.ACCEPTED_DOWNLOAD_KEY: {
                "url": "https://example.com/already-paid.png",
                "needs_key": False,
                "content_type_hint": "image/png",
            }
        },
        request_hash="b" * 64,
        status="failed",
        attempts=1,
        polls=0,
        usd_estimate=Decimal("0.0035"),
    )
    ctx = _context(
        tmp_path,
        provider,
        row=_row(image_provider="minimax", image_model="image-01"),
    )
    lookups = 0

    async def lookup_row(_statement: Any) -> VideoMediaJob:
        nonlocal lookups
        lookups += 1
        assert admission.await_count == (1 if lookups == 2 else 0)
        return receipt

    lookup = AsyncMock(side_effect=lookup_row)
    monkeypatch.setattr(ctx.session, "scalar", lookup)

    with pytest.raises(MediaJobFailed) as refused:
        await submit_job(ctx, "image", _image(slug=A01_ADMISSION_SLUG))
    assert (refused.value.status, refused.value.code) == (409, "video_media_outcome_uncertain")
    assert lookup.await_count == 2 and admission.await_count == 1
    monthly_reserve.assert_not_awaited()
    advance.assert_not_awaited()
    assert ctx.session.added == [] and ctx.session.commits == 0  # type: ignore[attr-defined]
    assert await meter.used(ctx.redis, meter.IMAGES) == 0
    assert provider.requests == []


@pytest.mark.asyncio
async def test_a01_cutover_pause_while_account_lock_waits_refuses_new_queue(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "project_format", AsyncMock(return_value=None))
    monkeypatch.setattr(service, "series_image_model", AsyncMock(return_value=None))
    provider = FakeProvider()
    ctx = _context(
        tmp_path,
        provider,
        row=_row(image_provider="minimax", image_model="image-01"),
    )

    async def pause_during_account_lock(_session: Any, *, slug: str) -> None:
        assert slug == A01_ADMISSION_SLUG
        _pause_intake(tmp_path)

    monkeypatch.setattr(service, "assert_a01_admission_open", pause_during_account_lock)
    monthly_reserve = AsyncMock()
    monkeypatch.setattr(meter, "reserve", monthly_reserve)
    with pytest.raises(MediaJobFailed) as refused:
        await submit_job(ctx, "image", _image(slug=A01_ADMISSION_SLUG))
    assert (refused.value.status, refused.value.code) == (423, "video_media_cutover_paused")
    monthly_reserve.assert_not_awaited()
    assert ctx.session.added == [] and ctx.session.commits == 0  # type: ignore[attr-defined]
    assert await meter.used(ctx.redis, meter.IMAGES) == 0
    assert provider.requests == []


@pytest.mark.asyncio
async def test_a01_media_queue_can_commit_on_0133_without_token_column(
    tmp_path: Path,
    a01_media_sessions: async_sessionmaker[AsyncSession],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(service, "project_format", AsyncMock(return_value=None))
    monkeypatch.setattr(service, "series_image_model", AsyncMock(return_value=None))
    advance = AsyncMock(side_effect=lambda _ctx, job: job)
    monkeypatch.setattr(service, "advance_job", advance)
    async with a01_media_sessions() as session:
        ctx = _context(
            tmp_path,
            FakeProvider(),
            row=_row(image_provider="minimax", image_model="image-01"),
        )
        ctx.session = session
        job, created = await submit_job(
            ctx, "image", _image(slug=A01_ADMISSION_SLUG)
        )
        assert created and job.status == "queued"
        assert await meter.used(ctx.redis, meter.IMAGES) == 1
        advance.assert_awaited_once()
        connection = await session.connection()
        assert not await connection.run_sync(
            lambda sync: "admission_token"
            in {column["name"] for column in sa.inspect(sync).get_columns("video_pilot_budgets")}
        )
    async with a01_media_sessions() as session:
        stored = await session.get(VideoMediaJob, job.id)
        assert stored is not None and stored.status == "queued"


@pytest.mark.asyncio
async def test_held_a01_media_queue_blocks_post_retry_and_poll_but_reads_terminal_result(
    tmp_path: Path,
    a01_media_sessions: async_sessionmaker[AsyncSession],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(service, "project_format", AsyncMock(return_value=None))
    monkeypatch.setattr(service, "series_image_model", AsyncMock(return_value=None))
    original_advance = service.advance_job
    advance = AsyncMock(side_effect=lambda _ctx, job: job)
    monkeypatch.setattr(service, "advance_job", advance)
    payload = _image(slug=A01_ADMISSION_SLUG)
    async with a01_media_sessions() as session:
        ctx = _context(
            tmp_path,
            FakeProvider(),
            row=_row(image_provider="minimax", image_model="image-01"),
        )
        ctx.session = session
        queued, created = await submit_job(ctx, "image", payload)
        assert created and queued.status == "queued"
    advance.reset_mock()
    async with a01_media_sessions() as session:
        await session.execute(
            sa.text("ALTER TABLE video_pilot_budgets ADD COLUMN admission_token VARCHAR(36)")
        )
        await session.execute(
            sa.text(
                "UPDATE video_pilot_budgets SET admission_token=:token WHERE slug=:slug"
            ),
            {"token": str(uuid4()), "slug": A01_ADMISSION_SLUG},
        )
        await session.commit()

    for blocked_payload in (payload, _image(slug=A01_ADMISSION_SLUG, seed=17)):
        async with a01_media_sessions() as session:
            ctx = _context(
                tmp_path,
                FakeProvider(),
                row=_row(image_provider="minimax", image_model="image-01"),
            )
            ctx.session = session
            with pytest.raises(MediaJobFailed) as refused:
                await submit_job(ctx, "image", blocked_payload)
            assert (refused.value.status, refused.value.code) == (
                409,
                "video_budget_admission_held",
            )
            assert await meter.used(ctx.redis, meter.IMAGES) == 0
            assert not await ctx.redis.exists(f"video-media:lock:{queued.id}")
            advance.assert_not_awaited()

    monkeypatch.setattr(service, "advance_job", original_advance)
    monkeypatch.setattr(
        service,
        "provider_for",
        lambda *_args: (_ for _ in ()).throw(AssertionError("provider must not be opened")),
    )
    async with a01_media_sessions() as session:
        queued_row = await session.get(VideoMediaJob, queued.id)
        assert queued_row is not None and queued_row.status == "queued"
        ctx = _context(tmp_path, FakeProvider())
        ctx.session = session
        with pytest.raises(MediaJobFailed) as refused:
            await original_advance(ctx, queued_row)
        assert refused.value.code == "video_budget_admission_held"
        assert not await ctx.redis.exists(f"video-media:lock:{queued.id}")

    async with a01_media_sessions() as session:
        submitted = await session.get(VideoMediaJob, queued.id)
        assert submitted is not None
        submitted.status = "submitted"
        submitted.vendor_ref = "already-sent"
        await session.commit()
    async with a01_media_sessions() as session:
        submitted = await session.get(VideoMediaJob, queued.id)
        assert submitted is not None
        ctx = _context(tmp_path, FakeProvider())
        ctx.session = session
        with pytest.raises(MediaJobFailed) as refused:
            await original_advance(ctx, submitted)
        assert refused.value.code == "video_budget_admission_held"
        assert not await ctx.redis.exists(f"video-media:lock:{queued.id}")

    async with a01_media_sessions() as session:
        failed = await session.get(VideoMediaJob, queued.id)
        assert failed is not None
        failed.status = "failed"
        await session.commit()
    async with a01_media_sessions() as session:
        ctx = _context(
            tmp_path,
            FakeProvider(),
            row=_row(image_provider="minimax", image_model="image-01"),
        )
        ctx.session = session
        with pytest.raises(MediaJobFailed) as refused:
            await submit_job(ctx, "image", payload)
        assert refused.value.code == "video_budget_admission_held"
        assert await meter.used(ctx.redis, meter.IMAGES) == 0
    async with a01_media_sessions() as session:
        terminal = await session.get(VideoMediaJob, queued.id)
        assert terminal is not None and terminal.status == "failed" and terminal.attempts == 1
        terminal.status = "ready"
        await session.commit()
    async with a01_media_sessions() as session:
        terminal = await session.get(VideoMediaJob, queued.id)
        assert terminal is not None
        ctx = _context(
            tmp_path,
            FakeProvider(),
            row=_row(image_provider="minimax", image_model="image-01"),
        )
        ctx.session = session
        assert await original_advance(ctx, terminal) is terminal
        same, created = await submit_job(ctx, "image", payload)
        assert same.id == terminal.id and not created and same.status == "ready"


@pytest.mark.parametrize("other_slug", ["unrelated-film", "story-conveyor-belt-sushi-v2"])
@pytest.mark.asyncio
async def test_a01_hold_does_not_block_an_unrelated_media_queue(
    tmp_path: Path,
    a01_media_sessions: async_sessionmaker[AsyncSession],
    monkeypatch: pytest.MonkeyPatch,
    other_slug: str,
) -> None:
    monkeypatch.setattr(service, "project_format", AsyncMock(return_value=None))
    monkeypatch.setattr(service, "series_image_model", AsyncMock(return_value=None))
    advance = AsyncMock(side_effect=lambda _ctx, job: job)
    monkeypatch.setattr(service, "advance_job", advance)
    async with a01_media_sessions() as session:
        await session.execute(
            sa.text("ALTER TABLE video_pilot_budgets ADD COLUMN admission_token VARCHAR(36)")
        )
        await session.execute(
            sa.text("UPDATE video_pilot_budgets SET admission_token=:token WHERE slug=:slug"),
            {"token": str(uuid4()), "slug": A01_ADMISSION_SLUG},
        )
        await session.commit()
    async with a01_media_sessions() as session:
        ctx = _context(
            tmp_path,
            FakeProvider(),
            row=_row(image_provider="minimax", image_model="image-01"),
        )
        ctx.session = session
        job, created = await submit_job(ctx, "image", _image(slug=other_slug))
        assert created and job.status == "queued"
        assert await meter.used(ctx.redis, meter.IMAGES) == 1
        advance.assert_awaited_once()


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.asyncio
async def test_a01_media_queue_and_token_acquire_serialize_on_postgresql(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Whichever transaction takes the A01 row first determines the safe outcome."""
    await postgres_engine.dispose(close=False)
    sessions = async_sessionmaker(postgres_engine, expire_on_commit=False)
    slug = A01_ADMISSION_SLUG
    monkeypatch.setattr(service, "project_format", AsyncMock(return_value=None))
    monkeypatch.setattr(service, "series_image_model", AsyncMock(return_value=None))
    monkeypatch.setattr(service, "advance_job", AsyncMock(side_effect=lambda _ctx, job: job))
    row = _row(image_provider="minimax", image_model="image-01")
    payload = _image(slug=slug, prompt=f"a01-media-admission-race-{uuid4()}")
    duplicate_payload = _image(slug=slug, prompt=f"a01-media-duplicate-race-{uuid4()}")
    model = find_model("minimax", "image", "image-01")
    assert model is not None
    digest = service.request_hash(
        {
            "kind": "image",
            "vendor": "minimax",
            "model": model.id,
            **service._request_fields(payload, row, model),
        }
    )
    duplicate_digest = service.request_hash(
        {
            "kind": "image",
            "vendor": "minimax",
            "model": model.id,
            **service._request_fields(duplicate_payload, row, model),
        }
    )
    async with postgres_engine.begin() as connection:
        had_column = await connection.run_sync(
            lambda sync: "admission_token"
            in {column["name"] for column in sa.inspect(sync).get_columns("video_pilot_budgets")}
        )
        if not had_column:
            await connection.execute(
                sa.text("ALTER TABLE video_pilot_budgets ADD COLUMN admission_token UUID")
            )
        previous = (
            await connection.execute(
                sa.text("SELECT admission_token FROM video_pilot_budgets WHERE slug=:slug"),
                {"slug": slug},
            )
        ).first()
        if previous is None:
            await connection.execute(
                sa.text("INSERT INTO video_pilot_budgets (slug, limit_usd) VALUES (:slug, 25)"),
                {"slug": slug},
            )
        else:
            await connection.execute(
                sa.text("UPDATE video_pilot_budgets SET admission_token=NULL WHERE slug=:slug"),
                {"slug": slug},
            )

    gate_entered = asyncio.Event()
    real_gate = assert_a01_admission_open

    async def witnessed_gate(session: AsyncSession, *, slug: str) -> None:
        gate_entered.set()
        await real_gate(session, slug=slug)

    monkeypatch.setattr(service, "assert_a01_admission_open", witnessed_gate)
    token_written = asyncio.Event()
    finish_token = asyncio.Event()
    finish_submit = asyncio.Event()
    reached_meter = asyncio.Event()
    arm_task: asyncio.Task[None] | None = None
    denied_task: asyncio.Task[Any] | None = None
    inserted_task: asyncio.Task[Any] | None = None
    token_task: asyncio.Task[bool] | None = None
    duplicate_first_task: asyncio.Task[Any] | None = None
    duplicate_second_task: asyncio.Task[Any] | None = None
    finish_duplicate = asyncio.Event()
    try:
        async def arm_first() -> None:
            async with sessions() as session:
                await session.scalar(
                    sa.select(VideoPilotBudget)
                    .where(VideoPilotBudget.slug == slug)
                    .with_for_update()
                )
                await session.execute(
                    sa.text(
                        "UPDATE video_pilot_budgets SET admission_token=CAST(:token AS uuid) "
                        "WHERE slug=:slug"
                    ),
                    {"token": str(uuid4()), "slug": slug},
                )
                token_written.set()
                await finish_token.wait()
                await session.commit()

        async def submit(body: ImageJobIn = payload) -> tuple[VideoMediaJob, bool]:
            async with sessions() as session:
                ctx = _context(tmp_path, FakeProvider(), row=row)
                ctx.session = session
                ctx.token_id = None
                return await submit_job(ctx, "image", body)

        arm_task = asyncio.create_task(arm_first())
        await asyncio.wait_for(token_written.wait(), timeout=10)
        denied_task = asyncio.create_task(submit())
        await asyncio.wait_for(gate_entered.wait(), timeout=10)
        await asyncio.sleep(0.05)
        assert not denied_task.done(), "media submit must wait for the account-row lock"
        finish_token.set()
        await asyncio.wait_for(arm_task, timeout=10)
        with pytest.raises(MediaJobFailed) as denied:
            await asyncio.wait_for(denied_task, timeout=10)
        assert denied.value.code == "video_budget_admission_held"
        async with sessions() as session:
            assert await session.scalar(
                sa.select(VideoMediaJob.id).where(
                    VideoMediaJob.slug == slug, VideoMediaJob.request_hash == digest
                )
            ) is None

        async with postgres_engine.begin() as connection:
            await connection.execute(
                sa.text("UPDATE video_pilot_budgets SET admission_token=NULL WHERE slug=:slug"),
                {"slug": slug},
            )

        async def paused_meter(*_args: Any, **_kwargs: Any) -> bool:
            reached_meter.set()
            await finish_submit.wait()
            return True

        monkeypatch.setattr(meter, "reserve", paused_meter)
        inserted_task = asyncio.create_task(submit())
        await asyncio.wait_for(reached_meter.wait(), timeout=10)

        async def token_attempt() -> bool:
            async with sessions() as session:
                await session.scalar(
                    sa.select(VideoPilotBudget)
                    .where(VideoPilotBudget.slug == slug)
                    .with_for_update()
                )
                queued = await session.scalar(
                    sa.select(VideoMediaJob.id).where(
                        VideoMediaJob.slug == slug,
                        VideoMediaJob.request_hash == digest,
                        VideoMediaJob.status == "queued",
                    )
                )
                if queued is not None:
                    await session.rollback()
                    return False
                await session.execute(
                    sa.text(
                        "UPDATE video_pilot_budgets SET admission_token=CAST(:token AS uuid) "
                        "WHERE slug=:slug"
                    ),
                    {"token": str(uuid4()), "slug": slug},
                )
                await session.commit()
                return True

        token_task = asyncio.create_task(token_attempt())
        await asyncio.sleep(0.05)
        assert not token_task.done(), "token acquire must wait for queued media commit"
        finish_submit.set()
        queued, created = await asyncio.wait_for(inserted_task, timeout=10)
        assert created and queued.status == "queued"
        assert await asyncio.wait_for(token_task, timeout=10) is False

        # Both duplicate POSTs initially miss a distinct request hash. The first
        # pauses after locking the budget row; the second waits, then must reselect
        # the first receipt instead of reserving another monthly unit or inserting.
        duplicate_meter_entered = asyncio.Event()
        duplicate_gate_entered = asyncio.Event()
        meter_calls = 0

        async def counted_meter(*_args: Any, **_kwargs: Any) -> bool:
            nonlocal meter_calls
            meter_calls += 1
            duplicate_meter_entered.set()
            await finish_duplicate.wait()
            return True

        async def duplicate_gate(session: AsyncSession, *, slug: str) -> None:
            duplicate_gate_entered.set()
            await real_gate(session, slug=slug)

        monkeypatch.setattr(meter, "reserve", counted_meter)
        duplicate_first_task = asyncio.create_task(submit(duplicate_payload))
        await asyncio.wait_for(duplicate_meter_entered.wait(), timeout=10)
        monkeypatch.setattr(service, "assert_a01_admission_open", duplicate_gate)
        duplicate_second_task = asyncio.create_task(submit(duplicate_payload))
        await asyncio.wait_for(duplicate_gate_entered.wait(), timeout=10)
        await asyncio.sleep(0.05)
        assert not duplicate_second_task.done(), "duplicate must wait on the account row"
        finish_duplicate.set()
        first_job, first_created = await asyncio.wait_for(duplicate_first_task, timeout=10)
        second_job, second_created = await asyncio.wait_for(duplicate_second_task, timeout=10)
        assert first_created and not second_created
        assert first_job.id == second_job.id and first_job.status == "queued"
        assert meter_calls == 1, "only the first identical POST reserves a monthly unit"
        async with sessions() as session:
            assert len(
                (
                    await session.scalars(
                        sa.select(VideoMediaJob.id).where(
                            VideoMediaJob.slug == slug,
                            VideoMediaJob.request_hash == duplicate_digest,
                        )
                    )
                ).all()
            ) == 1
    finally:
        finish_token.set()
        finish_submit.set()
        finish_duplicate.set()
        for task in (
            arm_task,
            denied_task,
            inserted_task,
            token_task,
            duplicate_first_task,
            duplicate_second_task,
        ):
            if task is not None and not task.done():
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)
        try:
            async with postgres_engine.begin() as connection:
                await connection.execute(
                    sa.delete(VideoMediaJob).where(
                        VideoMediaJob.slug == slug,
                        VideoMediaJob.request_hash.in_((digest, duplicate_digest)),
                    )
                )
                if previous is None:
                    await connection.execute(
                        sa.text("DELETE FROM video_pilot_budgets WHERE slug=:slug"),
                        {"slug": slug},
                    )
                else:
                    await connection.execute(
                        sa.text(
                            "UPDATE video_pilot_budgets "
                            "SET admission_token=CAST(:token AS uuid) WHERE slug=:slug"
                        ),
                        {
                            "slug": slug,
                            "token": str(previous[0]) if previous[0] is not None else None,
                        },
                    )
                if not had_column:
                    await connection.execute(
                        sa.text("ALTER TABLE video_pilot_budgets DROP COLUMN admission_token")
                    )
        finally:
            await postgres_engine.dispose()


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.asyncio
async def test_a01_existing_and_missing_posts_never_lock_job_before_budget_on_postgresql(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Opposing existing/missing POSTs must wait for the budget before any job row lock."""
    await postgres_engine.dispose(close=False)
    sessions = async_sessionmaker(postgres_engine, expire_on_commit=False)
    slug = A01_ADMISSION_SLUG
    row = _row(image_provider="minimax", image_model="image-01")
    model = find_model("minimax", "image", "image-01")
    assert model is not None
    existing_payload = _image(slug=slug, prompt=f"a01-existing-lock-order-{uuid4()}")
    missing_payload = _image(slug=slug, prompt=f"a01-missing-lock-order-{uuid4()}")

    def request(body: ImageJobIn) -> tuple[dict[str, Any], str]:
        fields = service._request_fields(body, row, model)
        return fields, service.request_hash(
            {"kind": "image", "vendor": "minimax", "model": model.id, **fields}
        )

    existing_fields, existing_digest = request(existing_payload)
    _, missing_digest = request(missing_payload)
    monkeypatch.setattr(service, "project_format", AsyncMock(return_value=None))
    monkeypatch.setattr(service, "series_image_model", AsyncMock(return_value=None))
    monkeypatch.setattr(service, "advance_job", AsyncMock(side_effect=lambda _ctx, job: job))
    async with postgres_engine.begin() as connection:
        had_column = await connection.run_sync(
            lambda sync: "admission_token"
            in {column["name"] for column in sa.inspect(sync).get_columns("video_pilot_budgets")}
        )
        if not had_column:
            await connection.execute(
                sa.text("ALTER TABLE video_pilot_budgets ADD COLUMN admission_token UUID")
            )
        previous = (
            await connection.execute(
                sa.text("SELECT admission_token FROM video_pilot_budgets WHERE slug=:slug"),
                {"slug": slug},
            )
        ).first()
        if previous is None:
            await connection.execute(
                sa.text("INSERT INTO video_pilot_budgets (slug, limit_usd) VALUES (:slug, 25)"),
                {"slug": slug},
            )
        else:
            await connection.execute(
                sa.text("UPDATE video_pilot_budgets SET admission_token=NULL WHERE slug=:slug"),
                {"slug": slug},
            )
        await connection.execute(
            sa.insert(VideoMediaJob).values(
                id=uuid4(),
                slug=slug,
                kind="image",
                purpose="keyframe",
                provider="minimax",
                model=model.id,
                request=existing_fields,
                request_hash=existing_digest,
                status="queued",
                attempts=1,
                polls=0,
                usd_estimate=Decimal("0.0035"),
            )
        )

    real_gate = assert_a01_admission_open
    both_at_gate = asyncio.Event()
    gate_calls = 0

    async def witnessed_gate(session: AsyncSession, *, slug: str) -> None:
        nonlocal gate_calls
        gate_calls += 1
        if gate_calls == 2:
            both_at_gate.set()
        await real_gate(session, slug=slug)

    monkeypatch.setattr(service, "assert_a01_admission_open", witnessed_gate)
    budget_locked = asyncio.Event()
    release_budget = asyncio.Event()
    holder: asyncio.Task[None] | None = None
    existing_task: asyncio.Task[Any] | None = None
    missing_task: asyncio.Task[Any] | None = None
    try:
        async def hold_budget() -> None:
            async with sessions() as session:
                await session.scalar(
                    sa.select(VideoPilotBudget)
                    .where(VideoPilotBudget.slug == slug)
                    .with_for_update()
                )
                budget_locked.set()
                await release_budget.wait()
                await session.commit()

        async def submit(body: ImageJobIn, label: str) -> tuple[VideoMediaJob, bool]:
            async with sessions() as session:
                root = tmp_path / label
                root.mkdir(exist_ok=True)
                ctx = _context(root, FakeProvider(), row=row)
                ctx.session = session
                ctx.token_id = None
                return await submit_job(ctx, "image", body)

        holder = asyncio.create_task(hold_budget())
        await asyncio.wait_for(budget_locked.wait(), timeout=10)
        existing_task = asyncio.create_task(submit(existing_payload, "existing"))
        missing_task = asyncio.create_task(submit(missing_payload, "missing"))
        await asyncio.wait_for(both_at_gate.wait(), timeout=10)
        await asyncio.sleep(0.05)
        assert not existing_task.done() and not missing_task.done()
        # On the old path the existing POST already held this row and waited for
        # budget, while the missing POST would later take budget then this row.
        async with sessions() as probe:
            locked = await asyncio.wait_for(
                probe.scalar(
                    sa.select(VideoMediaJob)
                    .where(
                        VideoMediaJob.slug == slug,
                        VideoMediaJob.request_hash == existing_digest,
                    )
                    .with_for_update(nowait=True)
                ),
                timeout=10,
            )
            assert locked is not None
            await probe.rollback()
        release_budget.set()
        await asyncio.wait_for(holder, timeout=10)
        same, same_created = await asyncio.wait_for(existing_task, timeout=10)
        fresh, fresh_created = await asyncio.wait_for(missing_task, timeout=10)
        assert same.request_hash == existing_digest and not same_created
        assert fresh.request_hash == missing_digest and fresh_created
    finally:
        release_budget.set()
        for task in (holder, existing_task, missing_task):
            if task is not None and not task.done():
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)
        try:
            async with postgres_engine.begin() as connection:
                await connection.execute(
                    sa.delete(VideoMediaJob).where(
                        VideoMediaJob.slug == slug,
                        VideoMediaJob.request_hash.in_((existing_digest, missing_digest)),
                    )
                )
                if previous is None:
                    await connection.execute(
                        sa.text("DELETE FROM video_pilot_budgets WHERE slug=:slug"), {"slug": slug}
                    )
                else:
                    await connection.execute(
                        sa.text(
                            "UPDATE video_pilot_budgets "
                            "SET admission_token=CAST(:token AS uuid) WHERE slug=:slug"
                        ),
                        {
                            "slug": slug,
                            "token": str(previous[0]) if previous[0] is not None else None,
                        },
                    )
                if not had_column:
                    await connection.execute(
                        sa.text("ALTER TABLE video_pilot_budgets DROP COLUMN admission_token")
                    )
        finally:
            await postgres_engine.dispose()


def _pinned_queued_job() -> VideoMediaJob:
    return VideoMediaJob(
        id=PINNED_JOB_ID,
        slug="google-project-suncatcher-prototype-what-it-tests",
        kind="image",
        purpose="keyframe",
        provider="minimax",
        model="image-01",
        request={},
        request_hash="52b39c04a45f39b4101bcd7e401c31cd0e6083f3c8390b729afd2a83569379e6",
        status="queued",
        attempts=1,
        polls=0,
        seconds=0,
        usd_estimate=Decimal("0.0035"),
    )


def _install_pinned_fence(root: Path, job: VideoMediaJob) -> None:
    path = fence_path(root)
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(expected_manifest(job), sort_keys=True) + "\n", encoding="utf-8")


@pytest.mark.asyncio
async def test_exact_queued_job_is_fenced_before_get_or_repeated_post_mutates_it(
    tmp_path: Path, fake_provider: FakeProvider
) -> None:
    job = _pinned_queued_job()
    ctx = _context(
        tmp_path,
        fake_provider,
        row=_row(image_provider="minimax", image_model="image-01"),
    )
    ctx.runtime = Settings(minimax_api_key="m", video_work_dir=str(tmp_path))
    ctx.session.found = job  # type: ignore[attr-defined]
    _install_pinned_fence(tmp_path, job)
    original = (job.status, job.attempts, job.polls, job.vendor_ref, dict(job.request))
    for _ in range(2):
        with pytest.raises(MediaJobFailed) as refused:
            await advance_job(ctx, job)
        assert (refused.value.status, refused.value.code) == (423, "video_media_dispatch_fenced")
        with pytest.raises(MediaJobFailed) as repeated:
            await submit_job(
                ctx,
                "image",
                _image(slug=job.slug, prompt="a reflective panel above earth"),
            )
        assert repeated.value.code == "video_media_dispatch_fenced"
    assert (job.status, job.attempts, job.polls, job.vendor_ref, job.request) == original
    assert ctx.session.commits == 0  # type: ignore[attr-defined]
    assert fake_provider.requests == []
    assert await ctx.redis.exists(f"video-media:lock:{job.id}") == 0


@pytest.mark.asyncio
async def test_pinned_job_missing_marker_fails_closed_but_other_job_still_dispatches(
    tmp_path: Path, fake_provider: FakeProvider
) -> None:
    ctx = _context(
        tmp_path,
        fake_provider,
        row=_row(image_provider="minimax", image_model="image-01"),
    )
    ctx.runtime = Settings(minimax_api_key="m", video_work_dir=str(tmp_path))
    job = _pinned_queued_job()
    with pytest.raises(MediaJobFailed) as refused:
        await advance_job(ctx, job)
    assert (refused.value.status, refused.value.code) == (
        503,
        "video_media_dispatch_fence_invalid",
    )
    assert job.status == "queued" and ctx.session.commits == 0  # type: ignore[attr-defined]
    fake_provider.submit_result = Submitted(inline=PNG, content_type="image/png")
    other, created = await submit_job(ctx, "image", _image(prompt="another film"))
    assert created and other.id != PINNED_JOB_ID and other.status == "ready"
    assert len(fake_provider.requests) == 1


@pytest.mark.asyncio
async def test_b25_direct_generation_and_poll_refuse_before_any_state_or_vendor_change(
    tmp_path: Path, fake_provider: FakeProvider
) -> None:
    ctx = _context(tmp_path, fake_provider)
    job = _pinned_queued_job()
    job.id = uuid4()
    job.slug = service.B25_CUTOVER_SLUG
    original = (job.status, job.attempts, job.polls, job.vendor_ref, dict(job.request))
    for _ in range(2):
        with pytest.raises(MediaJobFailed) as polled:
            await advance_job(ctx, job)
        assert (polled.value.status, polled.value.code) == (
            423,
            "video_media_b25_cutover_paused",
        )
        with pytest.raises(MediaJobFailed) as submitted:
            await submit_job(ctx, "image", _image(slug=job.slug))
        assert (submitted.value.status, submitted.value.code) == (
            423,
            "video_media_b25_cutover_paused",
        )
    assert (job.status, job.attempts, job.polls, job.vendor_ref, job.request) == original
    assert ctx.session.commits == 0 and ctx.session.added == []  # type: ignore[attr-defined]
    assert fake_provider.requests == []
    assert await ctx.redis.exists(f"video-media:lock:{job.id}") == 0
    assert await meter.used(ctx.redis, meter.IMAGES) == 0


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
async def test_pilot_media_uncertain_failure_keeps_charge_and_blocks_same_request_retry(
    tmp_path: Path, fake_provider: FakeProvider, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "assert_a01_admission_open", AsyncMock())
    slug = "story-rolling-suitcase-v2"
    ctx = _context(
        tmp_path,
        fake_provider,
        row=_row(image_provider="minimax", image_model="image-01"),
    )
    operations: list[str] = []

    async def fake_reserve(
        _session: Any, *, slug: str, operation_id: str, max_usd: Any, **_rest: Any
    ) -> Reservation:
        assert slug == "story-rolling-suitcase-v2" and max_usd > 0
        operations.append(operation_id)
        return Reservation(slug, operation_id, max_usd, "reserved", True, True, 1)

    mark = AsyncMock()
    settle = AsyncMock()
    monkeypatch.setattr(service, "reserve", fake_reserve)
    monkeypatch.setattr(service, "mark_uncertain", mark)
    monkeypatch.setattr(service, "settle", settle)
    fake_provider.submit_result = MediaUpstreamError(502, "lost answer", "failed")
    payload = _image(slug=slug)
    failed, created = await submit_job(ctx, "image", payload)
    assert created and failed.status == "failed"
    assert failed.error_code == "video_media_outcome_uncertain"
    assert failed.usd_estimate == Decimal("0.0035")
    assert len(operations) == 1 and mark.await_count >= 1
    assert settle.await_count == 0
    assert len(fake_provider.requests) == 1

    ctx.session.found = failed  # type: ignore[attr-defined]
    fake_provider.submit_result = Submitted(inline=PNG, content_type="image/png")
    with pytest.raises(MediaJobFailed) as blocked:
        await submit_job(ctx, "image", payload)
    assert blocked.value.code == "video_media_outcome_uncertain"
    assert len(operations) == 1
    assert len(fake_provider.requests) == 1
    settle.assert_not_awaited()


@pytest.mark.asyncio
async def test_pilot_gemini_image_is_refused_before_a_paid_call(
    tmp_path: Path, fake_provider: FakeProvider
) -> None:
    ctx = _context(tmp_path, fake_provider)
    with pytest.raises(MediaJobFailed) as refused:
        await submit_job(ctx, "image", _image(slug="story-rolling-suitcase"))
    assert refused.value.code == "video_pilot_budget_unknown_price"
    assert fake_provider.requests == []
    assert ctx.session.commits == 0  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_pilot_clip_is_refused_before_a_paid_call(
    tmp_path: Path, fake_provider: FakeProvider
) -> None:
    ctx = _context(tmp_path, fake_provider)
    with pytest.raises(MediaJobFailed) as refused:
        await submit_job(
            ctx,
            "clip",
            ClipJobIn.model_validate(
                {
                    "slug": "story-conveyor-belt-sushi-v2",
                    "shot_id": "opening",
                    "prompt": "moving belt",
                    "first_frame": "a" * 64,
                    "seconds": 8,
                }
            ),
        )
    assert refused.value.code == "video_pilot_clip_not_allowed"
    assert fake_provider.requests == []
    assert ctx.session.commits == 0  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_pilot_vendor_busy_answer_keeps_the_budget_hold(
    tmp_path: Path, fake_provider: FakeProvider, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "assert_a01_admission_open", AsyncMock())
    ctx = _context(
        tmp_path,
        fake_provider,
        row=_row(image_provider="minimax", image_model="image-01"),
    )
    reservation = Reservation(
        "story-rolling-suitcase-v2",
        "media-1",
        Decimal("0.0035"),
        "reserved",
        True,
        True,
        1,
    )
    monkeypatch.setattr(service, "reserve", AsyncMock(return_value=reservation))
    mark = AsyncMock()
    monkeypatch.setattr(service, "mark_uncertain", mark)
    fake_provider.submit_result = MediaUpstreamError(429, "vendor busy", "busy")
    failed, created = await submit_job(ctx, "image", _image(slug="story-rolling-suitcase-v2"))
    assert created and failed.status == "failed"
    assert failed.error_code == "video_media_outcome_uncertain"
    assert failed.usd_estimate == Decimal("0.0035")
    assert len(fake_provider.requests) == 1
    mark.assert_awaited()


@pytest.mark.asyncio
async def test_a_minimax_picture_is_stored_from_the_answer_like_a_gemini_one(
    tmp_path: Path,
) -> None:
    """image-01 through the real adapter. The bytes in the answer are stored as any inline
    picture is: the type read from the bytes, the catalog's price, one image on the meter. An
    answer that holds no picture gives the budget back; one that holds only a link the download
    check refuses fails as it did before the adapter asked for bytes, and keeps the charge."""
    answers: list[dict[str, Any]] = [
        {"image_base64": [base64.b64encode(JPEG).decode()]},
        {"image_base64": ["VENDOR-TEXT, not a picture"]},
        {"image_urls": ["http://insecure.example/p.jpeg"]},
    ]
    asked: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "https://api.minimaxi.com/v1/image_generation", (
            "nothing is downloaded"
        )
        asked.append(json.loads(request.content))
        return httpx.Response(
            200, json={"data": answers[len(asked) - 1], "base_resp": {"status_code": 0}}
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        ctx = _context(
            tmp_path,
            FakeProvider(),
            row=_row(image_provider="minimax", image_model="image-01"),
            http=http,
        )
        stored, created = await submit_job(ctx, "image", _image())
        assert created and stored.status == "ready"
        assert (stored.provider, stored.model) == ("minimax", "image-01")
        assert stored.content_type == "image/jpeg" and stored.file_bytes == len(JPEG)
        assert stored.file_sha256 == hashlib.sha256(JPEG).hexdigest()
        assert ctx.store.path("v", stored.file_sha256) is not None
        assert float(stored.usd_estimate) == 0.0035
        assert await meter.used(ctx.redis, meter.IMAGES) == 1
        assert asked[0]["response_format"] == "base64" and asked[0]["model"] == "image-01"

        garbled, _created = await submit_job(ctx, "image", _image(prompt="another"))
        assert garbled.status == "failed" and garbled.error_code == "video_media_upstream_failed"
        assert garbled.error_detail == "MiniMax's image is not valid base64"
        assert float(garbled.usd_estimate) == 0
        assert await meter.used(ctx.redis, meter.IMAGES) == 1, "only the stored picture counts"

        linked, _created = await submit_job(ctx, "image", _image(prompt="a third"))
        assert linked.status == "failed" and linked.error_code == "video_media_upstream_invalid"
        assert linked.error_detail == "the vendor's download URL is not an https address"
        assert float(linked.usd_estimate) == 0.0035
        assert await meter.used(ctx.redis, meter.IMAGES) == 2, "the vendor made it: no refund"
    assert len(asked) == 3


MP3 = b"ID3\x04\x00\x00\x00\x00\x00\x00" + b"\xff\xfb\x90\x00" * 16


@pytest.mark.asyncio
async def test_a_minimax_track_is_stored_from_its_hex_answer_and_a_shut_account_says_why(
    tmp_path: Path,
) -> None:
    """MiniMax music through the real adapter, on image-01's key: the hex in the answer is
    stored as an MP3 at the catalog's price, one track on the meter. An account the
    2026-08-20 rule shuts out fails as a key error naming the rule, and the track is given back
    to the month's budget."""
    answers: list[dict[str, Any]] = [
        {
            "data": {"audio": MP3.hex(), "status": 2},
            "extra_info": {"music_duration": 61000, "music_sample_rate": 44100},
            "base_resp": {"status_code": 0, "status_msg": "success"},
        },
        {
            "data": None,
            "base_resp": {
                "status_code": 2061,
                "status_msg": "Music generation is no longer available to new users",
            },
        },
    ]
    asked: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "https://api.minimaxi.com/v1/music_generation"
        asked.append(request)
        return httpx.Response(200, json=answers[len(asked) - 1])

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        ctx = _context(
            tmp_path,
            FakeProvider(),
            row=_row(music_provider="minimax", music_model="music-3.0"),
            http=http,
        )
        music = MusicJobIn.model_validate({"slug": "v", "prompt": "solo guqin", "seconds": 60})
        stored, created = await submit_job(ctx, "music", music)
        assert created and stored.status == "ready"
        assert (stored.provider, stored.model) == ("minimax", "music-3.0")
        assert stored.content_type == "audio/mpeg" and stored.file_bytes == len(MP3)
        assert stored.file_sha256 == hashlib.sha256(MP3).hexdigest()
        assert float(stored.usd_estimate) == 0.15
        assert await meter.used(ctx.redis, meter.MUSIC) == 1
        assert asked[0].headers["authorization"] == "Bearer m"
        sent = json.loads(asked[0].content)
        assert sent["model"] == "music-3.0" and sent["is_instrumental"] is True
        assert "About 60 seconds long" in sent["prompt"]

        other = MusicJobIn.model_validate({"slug": "v", "prompt": "taiko", "seconds": 60})
        shut, _created = await submit_job(ctx, "music", other)
        assert shut.status == "failed" and shut.error_code == "video_media_upstream_rejected_key"
        assert "new users" in (shut.error_detail or "")
        assert "since 2026-08-20" in (shut.error_detail or "")
        assert float(shut.usd_estimate) == 0
        assert await meter.used(ctx.redis, meter.MUSIC) == 1, "a refused track is given back"
    assert len(asked) == 2


@pytest.mark.asyncio
async def test_an_illustrated_slides_video_draws_under_its_own_switch_model_and_cap(
    tmp_path: Path, fake_provider: FakeProvider, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A slides project (docs/videos/ILLUSTRATED.md) draws with the slides' switch and image
    model; with that switch off it draws under the drama's switch as before; it never asks for
    a clip; a drama and a video the site does not know keep reading the drama's switch."""
    formats: dict[str, str | None] = {"v": "slides"}

    async def project_format(_session: Any, slug: str) -> str | None:
        return formats.get(slug)

    monkeypatch.setattr(service, "project_format", project_format)
    fake_provider.submit_result = Submitted(inline=PNG, content_type="image/png")

    ctx = _context(tmp_path, fake_provider, row=_row(drama_enabled=False))
    with pytest.raises(MediaJobFailed) as both_off:
        await submit_job(ctx, "image", _image())
    assert both_off.value.code == "video_media_disabled" and "插畫" in both_off.value.detail

    slides_on = _row(drama_enabled=False, slides_media_enabled=True)
    ctx = _context(tmp_path, fake_provider, row=slides_on)
    job, created = await submit_job(ctx, "image", _image())
    assert created and job.status == "ready"
    assert job.model == "gemini-3.1-flash-image"
    assert float(job.usd_estimate) == 0.067, "Flash, not the drama's Pro"
    # A still asked at 2K (docs/videos/ILLUSTRATED.md) is another request, sent to the vendor as
    # its resolution and priced at the model's 2K price.
    large, created = await submit_job(ctx, "image", _image(size="2K"))
    assert created and large.id != job.id and large.status == "ready"
    assert float(large.usd_estimate) == 0.101 and large.request["resolution"] == "2K"
    assert fake_provider.requests[-1].resolution == "2K"
    assert fake_provider.requests[-2].resolution is None, "no size, no resolution: the 1K default"
    with pytest.raises(MediaJobFailed) as clip:
        await submit_job(
            ctx,
            "clip",
            ClipJobIn.model_validate(
                {"slug": "v", "shot_id": "a", "prompt": "p", "first_frame": "a" * 64, "seconds": 8}
            ),
        )
    assert clip.value.code == "video_media_model_not_allowed" and "片段" in clip.value.detail

    # The slides' image model NULL follows the drama's choice; the drama's switch alone also
    # lets a slides video draw, on the drama's model.
    following = _row(slides_media_enabled=True, slides_image_model=None)
    ctx = _context(tmp_path, fake_provider, row=following)
    job, _ = await submit_job(ctx, "image", _image(seed=2))
    assert job.model == "gemini-3-pro-image"
    ctx = _context(tmp_path, fake_provider, row=_row(slides_media_enabled=False))
    job, _ = await submit_job(ctx, "image", _image(seed=3))
    assert job.model == "gemini-3-pro-image"

    # A drama, and a slug the site has no project for, read the drama's switch as before.
    formats["v"] = "drama"
    ctx = _context(tmp_path, fake_provider, row=slides_on)
    with pytest.raises(MediaJobFailed) as drama_off:
        await submit_job(ctx, "image", _image())
    assert drama_off.value.code == "video_media_disabled" and "漫劇" in drama_off.value.detail
    del formats["v"]
    with pytest.raises(MediaJobFailed):
        await submit_job(ctx, "image", _image())
    ctx = _context(tmp_path, fake_provider, row=_row(slides_media_enabled=True))
    job, _ = await submit_job(ctx, "image", _image(seed=4))
    assert job.model == "gemini-3-pro-image", "a drama never draws with the slides' model"

    # A slides model retired since it was chosen is refused by name.
    formats["v"] = "slides"
    retired = _row(slides_media_enabled=True, slides_image_model="nope")
    ctx = _context(tmp_path, fake_provider, row=retired)
    with pytest.raises(MediaJobFailed) as unknown:
        await submit_job(ctx, "image", _image())
    assert unknown.value.code == "video_media_model_not_allowed"
    assert "投影片" in unknown.value.detail


@pytest.mark.asyncio
async def test_the_project_format_comes_from_the_project_row_or_is_unknown() -> None:
    session = FakeSession()
    assert await service.project_format(session, "v") is None, "a job row is not a format"  # type: ignore[arg-type]

    class Found:
        async def scalar(self, _statement: Any) -> str:
            return "slides"

    assert await service.project_format(Found(), "v") == "slides"  # type: ignore[arg-type]


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
    lookup = str(ctx.session.last_statement.compile(dialect=postgresql.dialect()))  # type: ignore[attr-defined]
    assert "FOR UPDATE" in lookup, "concurrent failed-job resets must serialize on the row"
    job.attempts = 3
    with pytest.raises(MediaJobFailed) as exhausted:
        await submit_job(ctx, "image", _image())
    assert exhausted.value.code == "video_media_job_exhausted"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("series_model", "expected_model", "expected_usd"),
    [
        (None, "gemini-3-pro-image", 0.134),
        ("gemini-3.1-flash-image", "gemini-3.1-flash-image", 0.067),
        ("image-01", "image-01", 0.0035),
    ],
    ids=["pro-default", "flash-series-override", "minimax-one-off-override"],
)
async def test_a_refunded_retry_restores_the_selected_model_price_on_the_same_job(
    tmp_path: Path,
    fake_provider: FakeProvider,
    monkeypatch: pytest.MonkeyPatch,
    series_model: str | None,
    expected_model: str,
    expected_usd: float,
) -> None:
    monkeypatch.setattr(service, "series_image_model", AsyncMock(return_value=series_model))
    ctx = _context(tmp_path, fake_provider, row=_row(image_model="gemini-3-pro-image"))
    payload = _image()
    fake_provider.submit_result = MediaUpstreamError(422, "rejected before generation", "blocked")
    job, created = await submit_job(ctx, "image", payload)
    original_id = job.id
    assert created and job.status == "failed" and job.attempts == 1
    assert job.model == expected_model and float(job.usd_estimate) == 0
    if series_model == "image-01":
        assert job.provider == "minimax", "a one-off explainer's image-01 is asked of MiniMax"
    assert await meter.used(ctx.redis, meter.IMAGES) == 0

    ctx.session.found = job  # type: ignore[attr-defined]
    fake_provider.submit_result = Submitted(inline=PNG, content_type="image/png")
    retried, created_again = await submit_job(ctx, "image", payload)
    assert retried is job and retried.id == original_id and not created_again
    assert retried.status == "ready" and retried.attempts == 2
    assert retried.model == expected_model
    assert float(retried.usd_estimate) == expected_usd
    assert job_view(retried).usd_estimate == expected_usd
    assert await meter.used(ctx.redis, meter.IMAGES) == 1
    assert [request.model for request in fake_provider.requests] == [expected_model] * 2

    same, repeated = await submit_job(ctx, "image", payload)
    assert same is retried and not repeated and same.attempts == 2
    assert job_view(same).usd_estimate == expected_usd
    assert await meter.used(ctx.redis, meter.IMAGES) == 1
    assert len(fake_provider.requests) == 2, "a ready job is returned without another purchase"


@pytest.mark.asyncio
async def test_a_series_model_whose_vendor_has_no_key_is_refused_before_anything_is_spent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "series_image_model", AsyncMock(return_value="image-01"))
    ctx = _context(tmp_path, FakeProvider(), row=_row(image_model="gemini-3-pro-image"))
    ctx.runtime = Settings(
        hotspot_guide_gemini_api_key="g", minimax_api_key="", video_work_dir=str(tmp_path)
    )
    with pytest.raises(MediaJobFailed) as refused:
        await submit_job(ctx, "image", _image())
    assert (refused.value.status, refused.value.code) == (503, "video_media_not_configured")
    assert await meter.used(ctx.redis, meter.IMAGES) == 0


def test_the_vendor_of_a_series_model_is_chosen_as_the_first_picture_will_choose_it() -> None:
    assert service.series_image_vendor(_row(), "image-01") == "minimax"
    on_minimax = _row(image_provider="minimax", image_model="image-01")
    assert service.series_image_vendor(on_minimax, "gemini-3-pro-image") == "gemini"
    with pytest.raises(MediaJobFailed) as refused:
        service.series_image_vendor(_row(), "nope")
    assert (refused.value.status, refused.value.code) == (422, "video_media_model_not_allowed")


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


@pytest.mark.asyncio
async def test_pilot_vendor_task_expiry_keeps_its_charge_hold(
    tmp_path: Path, fake_provider: FakeProvider, monkeypatch: pytest.MonkeyPatch
) -> None:
    slug = "story-conveyor-belt-sushi-v2"
    ctx = _context(
        tmp_path, fake_provider, row=_row(image_provider="minimax", image_model="image-01")
    )
    monkeypatch.setattr(
        service,
        "reserve",
        AsyncMock(
            return_value=Reservation(
                slug, "expired-operation", Decimal("0.0035"), "reserved", True, True, 1
            )
        ),
    )
    mark = AsyncMock()
    monkeypatch.setattr(service, "mark_uncertain", mark)
    job, _created = await submit_job(ctx, "image", _image(slug=slug))
    assert job.status == "submitted"
    ctx.now = lambda: datetime.now(UTC) + timedelta(hours=25)
    await advance_job(ctx, job)
    assert job.status == "failed" and job.error_code == "video_media_outcome_uncertain"
    assert job.usd_estimate == Decimal("0.0035")
    mark.assert_awaited()


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
    assert type(service.provider_for(runtime, "gemini", "music")).__name__ == "GeminiMusic"
    # MiniMax music rides on image-01's key and base URL.
    music = service.provider_for(runtime, "minimax", "music")
    image = service.provider_for(runtime, "minimax", "image")
    assert isinstance(music, MiniMaxMusic) and isinstance(image, MiniMaxImages)
    assert music.name == "minimax" and (music.base_url, music.key) == (image.base_url, image.key)
    assert (music.base_url, music.key) == (runtime.minimax_api_base_url, "m")
    with pytest.raises(MediaJobFailed) as no_key:
        service.provider_for(Settings(), "gemini", "image")
    assert no_key.value.code == "video_media_not_configured"
    with pytest.raises(MediaJobFailed) as no_music_key:
        service.provider_for(Settings(minimax_api_key=None), "minimax", "music")
    assert no_music_key.value.code == "video_media_not_configured"
    _ = (AsyncMock, MagicMock)
