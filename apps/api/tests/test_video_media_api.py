"""/video/media: the token, the answers, the file routes, and where the package's errors live."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from decimal import Decimal
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import fakeredis
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.config import Settings
from app.db import get_session
from app.models import VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation.models import DEFAULT_DRAMA, DEFAULT_SLIDES, VideoAutomationSettings
from app.video_budget.models import FOLLOWON_SLUGS
from app.video_budget.service import BudgetError, BudgetSummary, Reservation
from app.video_media import admin_api, cutover_intake, meter
from app.video_media import jobs as media_jobs
from app.video_media.dispatch_fence import (
    PINNED_JOB_ID,
    PINNED_REQUEST_HASH,
    expected_manifest,
    fence_path,
)
from app.video_media.jobs import MediaContext
from app.video_media.models import VideoMediaJob
from app.video_media.schemas import JudgeOut
from app.video_media.settings import MediaSettings
from app.video_media.storage import MediaStore
from app.video_speech import admin_api as speech_api

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 30
PACKAGE = Path(__file__).resolve().parents[1] / "app" / "video_media"


def test_only_the_router_raises_app_errors() -> None:
    """The error-localization test exempts operator paths by file name; keep the codes there."""
    offenders = sorted(
        str(path.relative_to(PACKAGE))
        for path in PACKAGE.rglob("*.py")
        if path.name != "admin_api.py" and "AppError(" in path.read_text(encoding="utf-8")
    )
    assert offenders == []


def _app(
    token: VideoToolToken | None = None,
    *,
    schema_revision: str = "0132_video_pilot_budget",
) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.media_router, prefix="/api/v1")

    async def session() -> Any:
        fake = AsyncMock()

        async def scalar(statement: Any) -> str | None:
            if "alembic_version" in str(statement):
                return schema_revision
            return None

        fake.scalar = AsyncMock(side_effect=scalar)
        yield fake

    app.dependency_overrides[get_session] = session
    if token is not None:
        app.dependency_overrides[speech_api.video_tool] = lambda: token
    return app


def _row(**changes: Any) -> VideoAutomationSettings:
    return VideoAutomationSettings(
        id=1,
        **{
            **copy.deepcopy(DEFAULT_DRAMA),
            **copy.deepcopy(DEFAULT_SLIDES),
            "drama_enabled": True,
            **changes,
        },
    )


@pytest.fixture
def media(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict[str, Any]:
    marker_dir = tmp_path / cutover_intake.INTAKE_DIR
    marker_dir.mkdir(mode=0o755)
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
    if os.name == "posix":
        monkeypatch.setattr(cutover_intake, "ROOT_UID", tmp_path.stat().st_uid)
    monkeypatch.setattr(
        admin_api, "get_settings", lambda: Settings(video_work_dir=str(tmp_path))
    )
    settings = MediaSettings(video_media_dir=str(tmp_path))
    store = MediaStore(
        tmp_path,
        max_file_bytes=settings.video_media_max_file_bytes,
        max_total_bytes=settings.video_media_max_total_bytes,
    )
    state: dict[str, Any] = {
        "row": _row(),
        "store": store,
        "redis": fakeredis.aioredis.FakeRedis(),
        "settings": settings,
    }

    async def context(session: Any, token_id: Any) -> MediaContext:
        return MediaContext(
            session=session,
            redis=state["redis"],
            store=store,
            runtime=Settings(hotspot_guide_gemini_api_key="g", video_work_dir=str(tmp_path)),
            media=settings,
            row=state["row"],
            token_id=token_id,
        )

    monkeypatch.setattr(admin_api, "_context", context)
    monkeypatch.setattr(admin_api, "get_media_settings", lambda: settings)
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(meter, "month_usd", AsyncMock(return_value=1.25))

    async def pilot_summary(_session: Any, slug: str) -> BudgetSummary:
        if slug in FOLLOWON_SLUGS:
            raise BudgetError(503, "video_budget_missing_account", "follow-on not seeded yet")
        return BudgetSummary(
            slug=slug,
            limit_usd=Decimal("25.000000"),
            reserved_usd=Decimal("1.500000"),
            settled_usd=Decimal("2.000000"),
            remaining_usd=Decimal("21.500000"),
            uncertain_operations=1,
            settled_operations=2,
            released_operations=0,
            overrun_operations=0,
            total_over_limit=False,
            over_limit_usd=Decimal("0.000000"),
        )

    monkeypatch.setattr(admin_api, "summary", pilot_summary)
    return state


def _pause_intake(media: dict[str, Any]) -> None:
    folder = Path(media["settings"].video_media_dir) / cutover_intake.INTAKE_DIR
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


def _token() -> VideoToolToken:
    return VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")


@pytest.mark.asyncio
async def test_every_route_needs_a_video_tool_token() -> None:
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://t") as client:
        for method, path in (
            ("GET", "/status"),
            ("POST", "/images"),
            ("GET", f"/jobs/{uuid4()}"),
            ("POST", "/judge"),
            ("GET", f"/files/v/{'a' * 64}"),
        ):
            response = await client.request(method, f"/api/v1/video/media{path}", json={})
            assert response.status_code == 401, path


@pytest.mark.asyncio
async def test_status_reports_the_choices_budgets_store_and_limits(media: dict[str, Any]) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=_app(_token())), base_url="http://t"
    ) as client:
        response = await client.get("/api/v1/video/media/status")
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["enabled"] and body["clip"] == {
        "provider": "gemini",
        "model": "gemini-omni-1.1-flash",
        "configured": True,
        "resolution": "1080p",
        "seconds": 8,
        "usd_per_image_2k": None,
    }
    assert body["image"]["configured"] and not body["models"]["clips"]["minimax"] == []
    # The tool draws a style plate only for an image model that takes one (media/stages.mjs
    # takesStyleReference): both Gemini image models do, MiniMax image-01 does not.
    images = {
        entry["value"]: entry["style_references"]
        for vendor in body["models"]["images"].values()
        for entry in vendor
    }
    assert images["gemini-3-pro-image"] == 1 and images["gemini-3.1-flash-image"] == 1
    assert images["image-01"] == 0
    # The image choices say what a 2K picture costs, which is how the tool knows to ask for one.
    assert body["image"]["usd_per_image_2k"] == 0.134
    assert body["budgets"]["clip_seconds"] == {
        "unit": "seconds",
        "limit": 3000,
        "used": 0,
        "remaining": 3000,
    }
    assert body["estimated_usd"] == 1.25 and body["max_usd_per_video"] == 200
    assert set(body["pilot_budgets"]) == {
        "story-rolling-suitcase",
        "story-conveyor-belt-sushi",
        "story-rolling-suitcase-v2",
        "story-conveyor-belt-sushi-v2",
    }
    assert body["pilot_budgets"]["story-rolling-suitcase"] == {
        "limit_usd": "25.000000",
        "reserved_usd": "1.500000",
        "settled_usd": "2.000000",
        "remaining_usd": "21.500000",
        "uncertain_operations": 1,
        "settled_operations": 2,
        "released_operations": 0,
        "overrun_operations": 0,
        "total_over_limit": False,
        "over_limit_usd": "0.000000",
    }
    # Illustrated slides (docs/videos/ILLUSTRATED.md): their own switch, Flash and cap, which the
    # tool's media/stages.mjs reads; a row from before migration 0114 reads the defaults.
    assert body["slides_enabled"] is False and body["slides_max_usd_per_video"] == 20
    assert body["slides_image"] == {
        "provider": "gemini",
        "model": "gemini-3.1-flash-image",
        "configured": True,
        "resolution": None,
        "seconds": None,
        "usd_per_image_2k": 0.101,
    }
    assert body["slides_auto_approve_storyboard"] is True
    assert (body["slides_music_track"], body["slides_sfx_set"]) == (None, None)
    assert body["store"]["writable"] and body["limits"]["max_reference_images"] == 4
    assert body["limits"]["judge_checks"] == 1, "the tools ask yes/no only of a server that says so"
    # The tool composes each shot's prompt under the chosen image model's limit, counting the
    # avoidance text minimax.py appends (tools/video/media/prompt-budget.mjs reads these).
    assert body["limits"]["image_prompt_chars"] == 4000
    assert body["limits"]["image_prompt_chars_minimax"] == 1500


@pytest.mark.asyncio
async def test_status_shows_followon_budgets_after_all_five_accounts_exist(
    media: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    previous_summary = vars(admin_api)["summary"]

    async def migrated_summary(session: Any, slug: str) -> BudgetSummary:
        if slug not in FOLLOWON_SLUGS:
            return await previous_summary(session, slug)
        return BudgetSummary(
            slug=slug,
            limit_usd=Decimal("5"),
            reserved_usd=Decimal("0"),
            settled_usd=Decimal("0"),
            remaining_usd=Decimal("5"),
            uncertain_operations=0,
            settled_operations=0,
            released_operations=0,
            overrun_operations=0,
            total_over_limit=False,
            over_limit_usd=Decimal("0"),
        )

    monkeypatch.setattr(admin_api, "summary", migrated_summary)
    async with AsyncClient(
        transport=ASGITransport(app=_app(_token())), base_url="http://t"
    ) as client:
        response = await client.get("/api/v1/video/media/status")
    assert response.status_code == 200, response.text
    budgets = response.json()["pilot_budgets"]
    assert len(budgets) == 9
    assert {slug: budgets[slug]["limit_usd"] for slug in FOLLOWON_SLUGS} == {
        slug: "5" for slug in FOLLOWON_SLUGS
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("slug", "code", "schema_revision"),
    [
        (
            "story-rolling-suitcase",
            "video_budget_missing_account",
            "0132_video_pilot_budget",
        ),
        (
            "story-five-lego-legoland",
            "video_budget_invalid_account",
            "0132_video_pilot_budget",
        ),
        (
            "story-five-lego-legoland",
            "video_budget_missing_account",
            "0133_story_followon_budget",
        ),
    ],
)
async def test_status_never_hides_missing_legacy_or_invalid_followon_account(
    media: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    slug: str,
    code: str,
    schema_revision: str,
) -> None:
    previous_summary = vars(admin_api)["summary"]

    async def broken_summary(session: Any, checked_slug: str) -> BudgetSummary:
        if checked_slug == slug:
            raise BudgetError(503, code, "account not ready")
        return await previous_summary(session, checked_slug)

    monkeypatch.setattr(admin_api, "summary", broken_summary)
    async with AsyncClient(
        transport=ASGITransport(app=_app(_token(), schema_revision=schema_revision)),
        base_url="http://t",
    ) as client:
        response = await client.get("/api/v1/video/media/status")
    assert response.status_code == 503
    assert response.json()["code"] == code


@pytest.mark.asyncio
async def test_a_submission_is_refused_when_the_drama_is_off_or_the_budget_is_gone(
    media: dict[str, Any],
) -> None:
    media["row"] = _row(drama_enabled=False)
    payload = {"slug": "v", "purpose": "keyframe", "prompt": "a ridge"}
    async with AsyncClient(
        transport=ASGITransport(app=_app(_token())), base_url="http://t"
    ) as client:
        off = await client.post("/api/v1/video/media/images", json=payload)
        media["row"] = _row(monthly_images_budget=0)
        await meter.reserve(media["redis"], meter.IMAGES, 1, 1)
        media["row"].monthly_images_budget = 1
        spent = await client.post("/api/v1/video/media/images", json=payload)
        bad = await client.post("/api/v1/video/media/clips", json={"slug": "v", "prompt": "p"})
    assert off.status_code == 503 and off.json()["code"] == "video_media_disabled"
    assert spent.status_code == 429 and spent.json()["code"] == "video_media_budget_exhausted"
    assert bad.status_code == 422


@pytest.mark.asyncio
async def test_a_job_can_be_polled_and_an_unknown_one_is_404(
    media: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    job = VideoMediaJob(
        id=uuid4(),
        slug="v",
        kind="image",
        purpose="keyframe",
        provider="gemini",
        model="m",
        request={},
        request_hash="h",
        status="ready",
        attempts=1,
        seconds=0,
        polls=0,
        file_sha256="a" * 64,
        file_bytes=3,
        content_type="image/png",
        usd_estimate=0,
    )
    from datetime import UTC, datetime

    job.created_at = datetime.now(UTC)
    app = _app(_token())

    async def session() -> Any:
        fake = AsyncMock()
        fake.scalar = AsyncMock(return_value=job)
        yield fake

    app.dependency_overrides[get_session] = session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        found = await client.get(f"/api/v1/video/media/jobs/{job.id}")
    assert (
        found.status_code == 200
        and found.json()["status"] == "ready"
        and found.json()["file"]["sha256"] == "a" * 64
    )

    async def none() -> Any:
        fake = AsyncMock()
        fake.scalar = AsyncMock(return_value=None)
        yield fake

    app.dependency_overrides[get_session] = none
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        missing = await client.get(f"/api/v1/video/media/jobs/{uuid4()}")
    assert missing.status_code == 404 and missing.json()["code"] == "video_media_job_not_found"


@pytest.mark.asyncio
async def test_exact_fence_refuses_get_and_repeated_post_without_vendor_or_row_change(
    media: dict[str, Any], monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    slug = "google-project-suncatcher-prototype-what-it-tests"
    payload = {"slug": slug, "purpose": "keyframe", "prompt": "orbital mirror"}
    media["row"] = _row(image_provider="minimax", image_model="image-01")
    # The live request body is deliberately not stored in this test. The hash lookup is
    # pinned to the observed existing row so both POSTs exercise its dedupe branch.
    monkeypatch.setattr(media_jobs, "request_hash", lambda _fields: PINNED_REQUEST_HASH)
    job = VideoMediaJob(
        id=PINNED_JOB_ID,
        slug=slug,
        kind="image",
        purpose="keyframe",
        provider="minimax",
        model="image-01",
        request={},
        request_hash=PINNED_REQUEST_HASH,
        status="queued",
        attempts=1,
        polls=0,
        seconds=0,
        usd_estimate=Decimal("0.0035"),
    )
    from datetime import UTC, datetime

    job.created_at = datetime.now(UTC)
    path = fence_path(tmp_path)
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(expected_manifest(job), sort_keys=True) + "\n", encoding="utf-8")
    session_obj = AsyncMock()

    async def scalar(statement: Any) -> Any:
        return job if "video_media_jobs" in str(statement) else None

    session_obj.scalar = AsyncMock(side_effect=scalar)
    app = _app(_token())

    async def session() -> Any:
        yield session_obj

    app.dependency_overrides[get_session] = session

    async def context(session: Any, token_id: Any) -> MediaContext:
        return MediaContext(
            session=session,
            redis=media["redis"],
            store=media["store"],
            runtime=Settings(minimax_api_key="m", video_work_dir=str(tmp_path)),
            media=media["settings"],
            row=media["row"],
            token_id=token_id,
        )

    monkeypatch.setattr(admin_api, "_context", context)
    monkeypatch.setattr(
        media_jobs,
        "provider_for",
        lambda *_args: pytest.fail("fenced job reached the vendor adapter"),
    )
    original = (job.status, job.attempts, job.polls, job.vendor_ref, dict(job.request))
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        got = await client.get(f"/api/v1/video/media/jobs/{job.id}")
        repeated = [
            await client.post("/api/v1/video/media/images", json=payload) for _ in range(2)
        ]
    for response in [got, *repeated]:
        assert response.status_code == 423
        assert response.json()["code"] == "video_media_dispatch_fenced"
    assert (job.status, job.attempts, job.polls, job.vendor_ref, job.request) == original
    session_obj.commit.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("route", "payload"),
    [
        ("images", {"purpose": "keyframe", "prompt": "a watch"}),
        (
            "clips",
            {"shot_id": "opening", "prompt": "pan", "first_frame": "a" * 64, "seconds": 8},
        ),
        ("music", {"prompt": "quiet music", "seconds": 10}),
        (
            "judge",
            {
                "kind": "keyframe",
                "files": [{"sha256": "a" * 64, "label": "kf"}],
                "rubric": [{"key": "identity", "question": "same watch?"}],
            },
        ),
        ("locate", {"sha256": "a" * 64}),
    ],
)
async def test_b25_direct_paid_routes_refuse_before_context_or_quota(
    monkeypatch: pytest.MonkeyPatch, route: str, payload: dict[str, Any]
) -> None:
    async def unexpected(*_args: Any, **_kwargs: Any) -> Any:
        pytest.fail("paused B25 reached a quota or paid-call context")

    monkeypatch.setattr(admin_api, "_limit", unexpected)
    monkeypatch.setattr(admin_api, "_context", unexpected)
    async with AsyncClient(
        transport=ASGITransport(app=_app(_token())), base_url="http://t"
    ) as client:
        answers = [
            await client.post(
                f"/api/v1/video/media/{route}",
                json={"slug": media_jobs.B25_CUTOVER_SLUG, **payload},
            )
            for _ in range(2)
        ]
    for response in answers:
        assert response.status_code == 423, response.text
        assert response.json()["code"] == "video_media_b25_cutover_paused"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("route", "payload"),
    [
        ("images", {"purpose": "keyframe", "prompt": "orbital mirror"}),
        (
            "clips",
            {"shot_id": "opening", "prompt": "pan", "first_frame": "a" * 64, "seconds": 8},
        ),
        ("music", {"prompt": "quiet music", "seconds": 10}),
        (
            "judge",
            {
                "kind": "keyframe",
                "files": [{"sha256": "a" * 64, "label": "kf"}],
                "rubric": [{"key": "identity", "question": "same watch?"}],
            },
        ),
        ("locate", {"sha256": "a" * 64}),
    ],
)
async def test_global_pause_refuses_direct_paid_routes_before_quota_or_context(
    media: dict[str, Any], monkeypatch: pytest.MonkeyPatch, route: str, payload: dict[str, Any]
) -> None:
    _pause_intake(media)

    async def unexpected(*_args: Any, **_kwargs: Any) -> Any:
        pytest.fail("paused direct route reached quota or paid-call context")

    monkeypatch.setattr(admin_api, "_limit", unexpected)
    monkeypatch.setattr(admin_api, "_context", unexpected)
    async with AsyncClient(
        transport=ASGITransport(app=_app(_token())), base_url="http://t"
    ) as client:
        result = await client.post(
            f"/api/v1/video/media/{route}", json={"slug": "another-film", **payload}
        )
    assert result.status_code == 423, result.text
    assert result.json()["code"] == "video_media_cutover_paused"


@pytest.mark.asyncio
async def test_global_pause_refuses_live_get_before_poll_quota(
    media: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    _pause_intake(media)
    job = VideoMediaJob(
        id=uuid4(),
        slug="another-film",
        kind="image",
        purpose="keyframe",
        provider="minimax",
        model="image-01",
        request={},
        request_hash="h",
        status="queued",
        attempts=0,
        polls=0,
        seconds=0,
        usd_estimate=Decimal("0.0035"),
    )
    session_obj = AsyncMock()
    session_obj.scalar.return_value = job
    app = _app(_token())

    async def session() -> Any:
        yield session_obj

    app.dependency_overrides[get_session] = session

    async def unexpected(*_args: Any, **_kwargs: Any) -> Any:
        pytest.fail("paused live GET reached poll quota or vendor context")

    monkeypatch.setattr(admin_api, "_limit", unexpected)
    monkeypatch.setattr(admin_api, "_context", unexpected)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        result = await client.get(f"/api/v1/video/media/jobs/{job.id}")
    assert result.status_code == 423
    assert result.json()["code"] == "video_media_cutover_paused"
    session_obj.commit.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("route", "fields"),
    [
        (
            "judge",
            {
                "kind": "keyframe",
                "files": [{"sha256": "a" * 64, "label": "kf"}],
                "rubric": [{"key": "identity", "question": "same subject?"}],
            },
        ),
        ("locate", {"sha256": "a" * 64}),
    ],
)
@pytest.mark.parametrize("pilot", [False, True])
async def test_paid_direct_route_rechecks_after_awaited_booking(
    media: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    route: str,
    fields: dict[str, Any],
    pilot: bool,
) -> None:
    slug = "story-rolling-suitcase-v2" if pilot else "another-film"
    release_mock = AsyncMock()
    uncertain_mock = AsyncMock()
    vendor_mock = AsyncMock(side_effect=AssertionError("paid Gemini call escaped pause"))
    monkeypatch.setattr(admin_api, "release", release_mock)
    monkeypatch.setattr(admin_api, "mark_uncertain", uncertain_mock)
    monkeypatch.setattr(admin_api, route, vendor_mock)
    if pilot:

        async def reserve_then_pause(
            _session: Any, *, operation_id: str, max_usd: Decimal, **_rest: Any
        ) -> Reservation:
            _pause_intake(media)
            return Reservation(slug, operation_id, max_usd, "reserved", True, True, 1)

        monkeypatch.setattr(admin_api, "reserve", reserve_then_pause)
    else:
        original_book = admin_api._book_judge_call

        async def book_then_pause(ctx: MediaContext) -> None:
            await original_book(ctx)
            _pause_intake(media)

        monkeypatch.setattr(admin_api, "_book_judge_call", book_then_pause)

    body = {"slug": slug, "operation_id": str(uuid4()), **fields}
    async with AsyncClient(
        transport=ASGITransport(app=_app(_token())), base_url="http://t"
    ) as client:
        result = await client.post(f"/api/v1/video/media/{route}", json=body)
    assert result.status_code == 423 and result.json()["code"] == "video_media_cutover_paused"
    vendor_mock.assert_not_awaited()
    uncertain_mock.assert_not_awaited()
    assert await meter.used(media["redis"], meter.JUDGE_CALLS) == 0
    if pilot:
        assert release_mock.await_args.kwargs["reason"] == (
            "paid intake paused before vendor dispatch"
        )
    else:
        release_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_b25_direct_poll_refuses_before_vendor_or_row_change(
    media: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    job = VideoMediaJob(
        id=uuid4(),
        slug=media_jobs.B25_CUTOVER_SLUG,
        kind="image",
        purpose="keyframe",
        provider="minimax",
        model="image-01",
        request={},
        request_hash="h",
        status="queued",
        attempts=1,
        polls=0,
        seconds=0,
        usd_estimate=Decimal("0.0035"),
    )
    session_obj = AsyncMock()
    session_obj.scalar = AsyncMock(return_value=job)
    app = _app(_token())

    async def session() -> Any:
        yield session_obj

    app.dependency_overrides[get_session] = session
    monkeypatch.setattr(
        media_jobs, "provider_for", lambda *_args: pytest.fail("B25 reached vendor adapter")
    )
    original = (job.status, job.attempts, job.polls, job.vendor_ref)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        response = await client.get(f"/api/v1/video/media/jobs/{job.id}")
    assert response.status_code == 423
    assert response.json()["code"] == "video_media_b25_cutover_paused"
    assert (job.status, job.attempts, job.polls, job.vendor_ref) == original
    session_obj.commit.assert_not_awaited()
    assert await media["redis"].exists(f"video-media:lock:{job.id}") == 0


@pytest.mark.asyncio
async def test_files_are_uploaded_in_parts_and_served_with_ranges(media: dict[str, Any]) -> None:
    sha = hashlib.sha256(PNG).hexdigest()
    async with AsyncClient(
        transport=ASGITransport(app=_app(_token())), base_url="http://t"
    ) as client:
        put = await client.put(
            f"/api/v1/video/media/files/v/{sha}",
            params={"part": 0, "parts": 1, "size": len(PNG)},
            content=PNG,
        )
        wrong = await client.put(
            f"/api/v1/video/media/files/v/{'b' * 64}",
            params={"part": 0, "parts": 1, "size": len(PNG)},
            content=PNG,
        )
        got = await client.get(f"/api/v1/video/media/files/v/{sha}", headers={"Range": "bytes=0-7"})
        gone = await client.get(f"/api/v1/video/media/files/v/{'c' * 64}")
    assert put.status_code == 200 and put.json() == {"received": [0], "complete": True}
    assert wrong.status_code == 422 and wrong.json()["code"] == "video_media_hash_mismatch"
    assert got.status_code == 206 and got.content == PNG[:8]
    assert got.headers["content-type"] == "image/png" and got.headers["etag"] == f'"{sha}"'
    assert got.headers["cache-control"] == "private, no-store"
    assert gone.status_code == 404 and gone.json()["code"] == "video_media_file_not_found"


@pytest.mark.asyncio
async def test_a_judge_call_spends_one_unit_and_gives_it_back_when_the_judge_fails(
    media: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    verdict = JudgeOut(
        scores={"identity": 9.0}, overall=9.0, passed=True, problems=[], notes="ok", model="m"
    )
    calls: list[int] = []

    async def fake_judge(
        runtime: Any, settings: Any, store: Any, payload: Any, min_score: int, client: Any = None
    ) -> JudgeOut:
        calls.append(min_score)
        if min_score == 9:
            from app.video_media.judge import JudgeError

            raise JudgeError(502, "video_media_judge_failed", "no answer")
        return verdict

    monkeypatch.setattr(admin_api, "judge", fake_judge)
    body = {
        "slug": "v",
        "kind": "keyframe",
        "files": [{"sha256": "a" * 64, "label": "kf"}],
        "rubric": [{"key": "identity", "question": "same girl?"}],
    }
    async with AsyncClient(
        transport=ASGITransport(app=_app(_token())), base_url="http://t"
    ) as client:
        ok = await client.post("/api/v1/video/media/judge", json=body)
        failed = await client.post("/api/v1/video/media/judge", json={**body, "min_score": 9})
        lower = await client.post("/api/v1/video/media/judge", json={**body, "min_score": 3})
    assert ok.status_code == 200 and ok.json()["passed"] and calls[0] == 7, (
        "the settings row's threshold by default"
    )
    assert failed.status_code == 502 and failed.json()["code"] == "video_media_judge_failed"
    assert calls[1] == 9, "a call may raise the bar for itself"
    assert lower.status_code == 200 and calls[2] == 7, (
        "a call cannot lower the owner's threshold: the settings row is the floor"
    )
    assert await meter.used(media["redis"], meter.JUDGE_CALLS) == 2


@pytest.mark.asyncio
async def test_pilot_judge_requires_a_durable_operation_and_settles_reported_usage(
    media: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    called = 0
    operation = uuid4()
    pilot_slug = "story-rolling-suitcase"
    body = {
        "slug": pilot_slug,
        "kind": "keyframe",
        "files": [{"sha256": "a" * 64, "label": "kf"}],
        "rubric": [{"key": "identity", "question": "same subject?"}],
    }

    async def fake_judge(*_args: Any, **_kwargs: Any) -> JudgeOut:
        nonlocal called
        called += 1
        return JudgeOut(
            scores={"identity": 9},
            overall=9,
            passed=True,
            problems=[],
            notes="ok",
            model="gemini-3.8-flash",
            usage_input_tokens=1000,
            usage_total_tokens=1200,
        )

    reserve_mock = AsyncMock(
        return_value=Reservation(
            pilot_slug,
            f"media-judge:{operation}",
            Decimal("1.032192"),
            "reserved",
            True,
            False,
            1,
        )
    )
    settle_mock = AsyncMock()
    monkeypatch.setattr(admin_api, "judge", fake_judge)
    monkeypatch.setattr(admin_api, "reserve", reserve_mock)
    monkeypatch.setattr(admin_api, "settle", settle_mock)
    async with AsyncClient(
        transport=ASGITransport(app=_app(_token())), base_url="http://t"
    ) as client:
        missing = await client.post("/api/v1/video/media/judge", json=body)
        duplicate = await client.post(
            "/api/v1/video/media/judge", json={**body, "operation_id": str(operation)}
        )
        reserve_mock.return_value = Reservation(
            pilot_slug,
            f"media-judge:{operation}",
            Decimal("1.032192"),
            "reserved",
            True,
            True,
            1,
        )
        accepted = await client.post(
            "/api/v1/video/media/judge", json={**body, "operation_id": str(operation)}
        )

    assert (
        missing.status_code == 422
        and missing.json()["code"] == "video_pilot_budget_operation_required"
    )
    assert (
        duplicate.status_code == 409
        and duplicate.json()["code"] == "video_pilot_budget_operation_reused"
    )
    assert called == 1 and accepted.status_code == 200
    assert "usage_input_tokens" not in accepted.json()
    assert reserve_mock.await_args.kwargs["max_usd"] == Decimal("1.032192")
    assert settle_mock.await_args.kwargs["actual_usd"] == Decimal("0.001500")
