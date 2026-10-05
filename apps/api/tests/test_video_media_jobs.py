"""The job state machine with fake vendors: budgets, dedupe, retries, locks, downloads, expiry."""

from __future__ import annotations

import base64
import copy
import hashlib
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import fakeredis
import httpx
import pytest

from app.config import Settings
from app.video_automation.models import DEFAULT_DRAMA, DEFAULT_SLIDES, VideoAutomationSettings
from app.video_media import jobs as service
from app.video_media import meter
from app.video_media.catalog import find_model
from app.video_media.jobs import MediaContext, MediaJobFailed, advance_job, job_view, submit_job
from app.video_media.models import VideoMediaJob
from app.video_media.providers import Download, MediaRequest, MediaUpstreamError, Polled, Submitted
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


@pytest.mark.parametrize(
    "extra",
    [{"seconds": 4}, {"seconds": 6}, {"references": [{"sha256": "b" * 64}]}],
)
@pytest.mark.asyncio
async def test_lite_incompatible_jobs_spend_nothing(
    tmp_path: Path, extra: dict[str, Any]
) -> None:
    provider = FakeProvider()
    ctx = _context(
        tmp_path, provider,
        row=_row(clip_model="veo-3.1-lite-generate-preview", clip_resolution="1080p"),
    )
    payload = ClipJobIn.model_validate(
        {"slug": "v", "shot_id": "opening", "prompt": "push in",
         "first_frame": "a" * 64, "seconds": 8, **extra}
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
    clip = {"slug": "v", "shot_id": "opening", "prompt": "push in", "first_frame": "a" * 64,
            "last_frame": "c" * 64, "seconds": 8}
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
        {"slug": "v", "shot_id": "opening", "prompt": "push in", "first_frame": "a" * 64,
         "seconds": 8, "native_audio": False}
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
    ],
    ids=["pro-default", "flash-series-override"],
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
