"""A binge series (docs/videos/BINGE.md): the shape the button derives, the retention rules
on a chapter outline, the hands-off decision on a filed document, the compilation job, the
quote, and the routes that carry them."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.auth.service import current_user
from app.db import get_session
from app.models import User, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api
from app.video_automation import series as service
from app.video_automation import settings as settings_service
from app.video_automation.judge import REQUIRED_VERDICTS
from app.video_automation.models import (
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaSeries,
)
from app.video_automation.schemas import (
    SeriesCompilationStartOut,
    SeriesContextOut,
    SeriesDocSubmitIn,
    SeriesIn,
    SeriesOut,
)
from app.video_speech import admin_api as speech_api

WHEN = datetime(2026, 9, 27, 1, 0, tzinfo=UTC)


def _series(**changes: Any) -> VideoDramaSeries:
    values: dict[str, Any] = {
        "id": uuid4(),
        "slug": "rebirth-20260927-ab12",
        "title": "重生復仇合集 （企劃命名中）",
        "premise": "由企劃依「重生復仇」題材預設自擬前提",
        "aspects": [],
        "tone": "hetero-leads",
        "style_preset": "cinematic-3d",
        "target_minutes": 3,
        "planned_episodes": 40,
        "episodes_per_chapter": 8,
        "open_ended": False,
        "status": "active",
        "note": None,
        "requested_chapter": None,
        "force_next": False,
        "genre": "rebirth-revenge",
        "lead": "female",
        "hands_off": True,
        "compilation": True,
        "visual_tier": "hybrid",
        "total_minutes": 120,
        "compilation_slug": None,
        "compilation_started_at": None,
        "compilation_finished_at": None,
        "created_at": WHEN,
        "updated_at": WHEN,
    }
    values.update(changes)
    return VideoDramaSeries(**values)


def _episode(number: int, status: str = "done") -> VideoDramaEpisode:
    return VideoDramaEpisode(
        id=uuid4(),
        series_id=uuid4(),
        number=number,
        chapter_number=(number - 1) // 8 + 1,
        title=f"第 {number} 集",
        logline="",
        beats={},
        status=status,
        state_json={},
        created_at=WHEN,
        updated_at=WHEN,
    )


def _settings(**changes: Any) -> VideoAutomationSettings:
    values: dict[str, Any] = {
        "series_max_in_flight": 1,
        "series_script_gate": True,
        "series_auto_continue": True,
        "series_chapter_ahead": 2,
        "series_doc_rewrites": 2,
        "series_episodes_per_month": 30,
        "clip_provider": "gemini",
        "clip_model": "gemini-omni-1.1-flash",
        "image_provider": "gemini",
        "image_model": "gemini-3-pro-image",
        "monthly_clip_seconds_budget": 3000,
        "monthly_images_budget": 1500,
        "monthly_judge_calls_budget": 3000,
    }
    values.update(changes)
    return VideoAutomationSettings(**values)


def _beats(number: int, **changes: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "number": number,
        "hook": "h",
        "conflict": "c",
        "turn": "t",
        "cliffhanger": {"type": "danger" if number % 2 else "reveal", "text": "x"},
        "tension": [2, 3, 3, 4, 5],
        "setups": ["m1"],
        "payoffs": ["m1"] if number % 3 == 0 else [],
        "hook_type": "danger" if number % 2 else "question",
        "lead_arc": "wins" if number % 2 else "mixed",
        "satisfaction": [
            {"beat": "opening", "type": "face_slap"},
            {"beat": "ending", "type": "reversal"},
        ],
    }
    row.update(changes)
    return row


def test_the_button_cuts_the_minutes_into_episodes_and_chapters() -> None:
    assert service.binge_shape(120, 3) == (40, 10)
    assert service.binge_shape(30, 3) == (10, 10), "one chapter for the pilot"
    assert service.binge_shape(60, 3) == (20, 10)
    assert service.binge_shape(90, 3) == (30, 10)
    assert service.binge_shape(240, 4) == (60, 10)
    assert service.binge_shape(35, 2) == (18, 9), "as even as six to ten allow"
    assert service.binge_shape(128, 4) == (32, 8)
    planned, per_chapter = service.binge_shape(480, 2)
    assert planned == 240 and 6 <= per_chapter <= 10


def test_a_blank_form_is_named_after_the_genre_and_shaped_from_the_minutes() -> None:
    payload = SeriesIn(
        genre="rebirth-revenge",
        lead="female",
        total_minutes=120,
        target_minutes=3,
        visual_tier="hybrid",
        hands_off=True,
        compilation=True,
        open_ended=False,
    )
    values = service.series_values(payload, WHEN)
    assert values["planned_episodes"] == 40 and values["episodes_per_chapter"] == 10
    assert values["slug"].startswith("rebirth-revenge-20260927-") and len(values["slug"]) <= 40
    assert values["title"] == "重生復仇合集 （企劃命名中）"
    assert "重生復仇" in values["premise"] and values["hands_off"] and values["compilation"]
    named = service.series_values(
        SeriesIn(slug="wenjian", title="問劍", premise="兩個少年", planned_episodes=25), WHEN
    )
    assert (named["slug"], named["title"], named["planned_episodes"]) == ("wenjian", "問劍", 25)
    with pytest.raises(ValueError, match="custom series needs a premise"):
        SeriesIn(genre="custom", total_minutes=60)
    with pytest.raises(ValueError, match="premise must not be blank"):
        SeriesIn(slug="xx", title="x")


def test_the_retention_rules_hold_only_for_a_genre_that_has_them() -> None:
    series = _series()

    def doc(episodes: list[dict[str, Any]]) -> SeriesDocSubmitIn:
        return SeriesDocSubmitIn(
            kind="chapter", chapter_number=1, body_md="# 1", body_json={"episodes": episodes}
        )

    good = [_beats(n) for n in range(1, 9)]
    assert service.doc_problem(series, doc(good)) is None
    no_hook = [dict(_beats(n)) for n in range(1, 9)]
    del no_hook[2]["hook_type"]
    assert "episode 3 needs hook_type" in str(service.doc_problem(series, doc(no_hook)))
    few = [
        _beats(n, satisfaction=[{"beat": "ending", "type": "reversal"}]) if n == 4 else _beats(n)
        for n in range(1, 9)
    ]
    assert "episode 4 needs at least 2" in str(service.doc_problem(series, doc(few)))
    late = [
        _beats(
            n,
            satisfaction=[
                {"beat": "ending", "type": "reversal"},
                {"beat": "ending", "type": "face_slap"},
            ],
        )
        if n == 5
        else _beats(n)
        for n in range(1, 9)
    ]
    assert "first half" in str(service.doc_problem(series, doc(late)))
    unknown = [
        _beats(
            n,
            satisfaction=[
                {"beat": "opening", "type": "kiss"},
                {"beat": "ending", "type": "reversal"},
            ],
        )
        if n == 6
        else _beats(n)
        for n in range(1, 9)
    ]
    assert "genre's types" in str(service.doc_problem(series, doc(unknown)))
    suffering = [_beats(n, lead_arc="suffers") if n in (2, 3) else _beats(n) for n in range(1, 9)]
    assert "episodes 2 and 3 both leave the lead suffering" in str(
        service.doc_problem(series, doc(suffering))
    )
    dry = [_beats(n, payoffs=[]) for n in range(1, 9)]
    assert "pay nothing off" in str(service.doc_problem(series, doc(dry)))
    classic = _series(genre="xianxia-bonds", planned_episodes=25, episodes_per_chapter=10)
    plain = [
        {"number": n, "hook": "h", "conflict": "c", "turn": "t", "cliffhanger": "x"}
        for n in range(1, 11)
    ]
    assert service.doc_problem(classic, doc(plain)) is None, "the classic series keeps its rules"


def test_a_finished_compilation_series_asks_for_its_compilation_once() -> None:
    finished = _series(status="finished", planned_episodes=10, episodes_per_chapter=10)
    done = [_episode(n) for n in range(1, 11)]
    job = service.next_job_for(finished, [], done, _settings(), started_this_month=0)
    assert job is not None and job.kind == "compilation"
    with_skip = [_episode(n, "skipped" if n == 4 else "done") for n in range(1, 11)]
    job = service.next_job_for(finished, [], with_skip, _settings(), started_this_month=0)
    assert job is not None and job.kind == "compilation", "a skipped episode is left out"
    started = _series(status="finished", compilation_slug="rebirth-20260927-ab12-full")
    assert service.next_job_for(started, [], done, _settings(), started_this_month=0) is None
    classic = _series(status="finished", compilation=False)
    assert service.next_job_for(classic, [], done, _settings(), started_this_month=0) is None
    nothing = [_episode(n, "skipped") for n in range(1, 11)]
    assert service.next_job_for(finished, [], nothing, _settings(), started_this_month=0) is None
    paused = _series(status="paused")
    assert service.next_job_for(paused, [], done, _settings(), started_this_month=0) is None


@pytest.mark.asyncio
async def test_a_series_keeps_the_one_compilation_the_worker_named_after_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """做合集 sets up a finished series that has none; it never clears an existing one, since the
    worker's <series>-full slug is taken and the first cut's download hangs on the column."""
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    session = AsyncMock()
    session.add = lambda _row: None
    monkeypatch.setattr(service, "_docs", AsyncMock(return_value=[]))
    monkeypatch.setattr(service, "series_view", AsyncMock(return_value="view"))

    async def refused(series: Any) -> str:
        monkeypatch.setattr(service, "_series", AsyncMock(return_value=series))
        with pytest.raises(service.SeriesRefused) as failure:
            await service.act(session, owner, series.slug, "compile")
        return str(failure.value.code)

    finished = datetime(2026, 9, 27, 3, tzinfo=UTC)
    started = datetime(2026, 9, 27, 2, tzinfo=UTC)
    done = _series(
        status="finished",
        compilation_slug="rebirth-20260927-ab12-full",
        compilation_started_at=started,
        compilation_finished_at=finished,
    )
    assert await refused(done) == "video_series_compiled"
    assert done.compilation_slug == "rebirth-20260927-ab12-full", "the first cut keeps its slug"
    making = _series(
        status="finished",
        compilation_slug="rebirth-20260927-ab12-full",
        compilation_started_at=started,
        compilation_finished_at=None,
    )
    assert await refused(making) == "video_series_compiling"
    assert await refused(_series(status="active")) == "video_series_not_finished"

    classic = _series(status="finished", compilation=False, compilation_slug=None)
    monkeypatch.setattr(service, "_series", AsyncMock(return_value=classic))
    view, detail = await service.act(session, owner, classic.slug, "compile")
    assert (view, detail) == ("view", "工人的下一輪會開始做合集")
    assert classic.compilation is True and classic.compilation_slug is None


def test_the_series_finishes_when_its_last_open_episode_is_done_or_skipped() -> None:
    now = datetime(2026, 9, 27, 4, tzinfo=UTC)
    series = _series(status="active", planned_episodes=10, episodes_per_chapter=10)
    open_last = [_episode(n, "done" if n < 10 else "ready") for n in range(1, 11)]
    assert service.finish_if_complete(series, open_last, now) is False
    assert series.status == "active"
    skipped_last = [_episode(n, "done" if n < 10 else "skipped") for n in range(1, 11)]
    assert service.finish_if_complete(series, skipped_last, now) is True
    assert series.status == "finished" and series.updated_at == now
    short = _series(status="active", planned_episodes=10, episodes_per_chapter=10)
    assert service.finish_if_complete(short, [_episode(n) for n in range(1, 10)], now) is False
    paused = _series(status="paused", planned_episodes=10, episodes_per_chapter=10)
    assert service.finish_if_complete(paused, skipped_last, now) is False, "a paused series stays"


def _verdict(kind: str, **changes: Any) -> dict[str, Any]:
    judge: dict[str, Any] = {
        "verdicts": {key: "有" for key in REQUIRED_VERDICTS[kind]},
        "problems": [],
        "similar_works": [],
        "notes": "ok",
    }
    judge.update(changes)
    return judge


def test_a_hands_off_document_is_decided_from_the_verdict_as_it_arrives() -> None:
    series = _series()
    passing = SeriesDocSubmitIn(
        kind="setting", body_md="# x", body_json={}, judge=_verdict("setting")
    )
    status, note = service.auto_doc_status(series, passing, 1, 2)
    assert status == "approved" and note is not None
    assert note.startswith("查核：originality 有、conflict_engine 有") and note.endswith(
        "依作品設定自動核准"
    )
    failing = SeriesDocSubmitIn(
        kind="setting",
        body_md="# x",
        body_json={},
        judge=_verdict("setting", problems=["反派沒有動機"]),
    )
    status, note = service.auto_doc_status(series, failing, 1, 2)
    assert (
        status == "rejected"
        and note is not None
        and note.startswith("[auto]")
        and "反派沒有動機" in note
    )
    assert service.auto_doc_status(series, failing, 2, 2) == ("rejected", note), "the last rewrite"
    assert service.auto_doc_status(series, failing, 3, 2) == ("review", note), "then the owner"
    silent = SeriesDocSubmitIn(kind="setting", body_md="# x", body_json={})
    assert service.auto_doc_status(series, silent, 1, 2) == ("review", None), (
        "no verdict, no decision"
    )
    classic = _series(hands_off=False)
    assert service.auto_doc_status(classic, passing, 1, 2) == ("review", None)


def test_the_setting_book_names_a_series_the_form_left_blank() -> None:
    series = _series()
    doc = VideoDramaDoc(
        id=uuid4(),
        series_id=series.id,
        kind="setting",
        chapter_number=0,
        version=1,
        body_md="# x",
        body_json={"title": "她磨好了刀"},
        status="approved",
        created_at=WHEN,
    )

    import asyncio

    session = AsyncMock()
    asyncio.run(
        service._apply_approval(session, _series(status="setting", title=series.title), doc)
    )
    named = _series(status="setting")
    asyncio.run(service._apply_approval(session, named, doc))
    assert named.title == "她磨好了刀" and named.status == "outline"
    kept = _series(status="setting", title="問劍")
    asyncio.run(service._apply_approval(session, kept, doc))
    assert kept.title == "問劍", "a title the owner typed stays"


def test_the_quote_prices_the_run_at_the_settings_prices_against_the_budgets() -> None:
    quote = service.binge_quote(_settings(), 120, 3, "hybrid")
    assert (quote.episodes, quote.chapters, quote.episodes_per_chapter) == (40, 4, 10)
    assert quote.clip_seconds == 4320 and quote.images == 1578 and quote.judge_calls == 1698
    assert quote.usd == pytest.approx(916.43, abs=0.01)
    assert not quote.ok and not quote.budgets["clip_seconds"].ok
    assert quote.budgets["episodes_per_month"].needed == 40
    stills = service.binge_quote(
        _settings(monthly_images_budget=3000, series_episodes_per_month=60), 120, 3, "stills"
    )
    assert stills.clip_seconds == 1080 and stills.budgets["clip_seconds"].ok and stills.ok
    clips = service.binge_quote(_settings(), 120, 3, "clips")
    assert clips.clip_seconds == 10800 and clips.usd > stills.usd


def test_the_summary_carries_the_binge_columns_and_an_older_row_reads_as_classic() -> None:
    view = service.summary_view(_series(), [], [])
    assert (view.genre, view.lead, view.hands_off, view.compilation, view.visual_tier) == (
        "rebirth-revenge",
        "female",
        True,
        True,
        "hybrid",
    )
    assert view.total_minutes == 120 and view.compilation_slug is None
    older = _series(
        genre=None,
        lead=None,
        hands_off=None,
        compilation=None,
        visual_tier=None,
        total_minutes=None,
    )
    view = service.summary_view(older, [], [])
    assert (view.genre, view.lead, view.hands_off, view.visual_tier) == (
        "xianxia-bonds",
        "dual-male",
        False,
        "clips",
    )


def _app(user: User | None = None) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.tool_router, prefix="/api/v1")
    app.include_router(admin_api.admin_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    if user is not None:
        app.dependency_overrides[current_user] = lambda: user
    return app


def _user(role: str) -> User:
    user = User(id=uuid4(), email=f"{role}@example.com", password_hash="unused")
    user._admin_roles_cache = frozenset({role})  # type: ignore[attr-defined]
    return user


@pytest.mark.asyncio
async def test_the_quote_route_answers_before_the_button_and_the_form_creates_a_binge_series(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        settings_service, "settings_row", AsyncMock(return_value=_settings(drama_enabled=True))
    )
    row = _series()
    out = SeriesOut(**service.summary_view(row, [], []).model_dump(), docs=[], episodes=[])
    create = AsyncMock(return_value=out)
    monkeypatch.setattr(service, "create_series", create)
    base = "/api/v1/admin/video-automation/series"
    async with AsyncClient(
        transport=ASGITransport(app=_app(_user("viewer"))), base_url="http://t"
    ) as client:
        quote = await client.get(
            f"{base}/binge-quote",
            params={"total_minutes": 120, "episode_minutes": 3, "visual_tier": "hybrid"},
        )
        too_short = await client.get(f"{base}/binge-quote", params={"total_minutes": 10})
    assert (
        quote.status_code == 200 and quote.json()["episodes"] == 40 and quote.json()["ok"] is False
    )
    assert too_short.status_code == 422
    async with AsyncClient(
        transport=ASGITransport(app=_app(_user("owner"))), base_url="http://t"
    ) as client:
        created = await client.post(
            base,
            json={
                "genre": "rebirth-revenge",
                "lead": "female",
                "total_minutes": 120,
                "target_minutes": 3,
                "visual_tier": "hybrid",
                "hands_off": True,
                "compilation": True,
                "open_ended": False,
            },
        )
    assert created.status_code == 201 and created.json()["genre"] == "rebirth-revenge"
    sent = create.await_args.args[2]
    assert sent.slug is None and sent.total_minutes == 120 and sent.hands_off


@pytest.mark.asyncio
async def test_the_worker_files_documents_with_the_settings_and_starts_and_finishes_the_compilation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = _app()
    app.dependency_overrides[speech_api.video_tool] = lambda: VideoToolToken(
        id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x"
    )
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", AsyncMock())
    settings = _settings()
    monkeypatch.setattr(settings_service, "settings_row", AsyncMock(return_value=settings))
    row = _series(status="finished")
    summary = service.summary_view(row, [], [])
    context = SeriesContextOut(
        series=summary,
        setting=None,
        outline=None,
        chapter=None,
        chapter_number=None,
        chapter_range=None,
        episode=None,
        episodes=[],
        recaps=[],
        mysteries=[],
    )
    start = AsyncMock(
        return_value=SeriesCompilationStartOut(series=summary, episodes=[], context=context)
    )
    finish = AsyncMock(return_value=summary)
    submit = AsyncMock(side_effect=service.SeriesRefused(422, "video_series_doc_invalid", "x"))
    monkeypatch.setattr(service, "start_compilation", start)
    monkeypatch.setattr(service, "finish_compilation", finish)
    monkeypatch.setattr(service, "submit_doc", submit)
    base = "/api/v1/video/automation/series/rebirth-20260927-ab12"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        started = await client.post(
            f"{base}/compilation/start", json={"slug": "rebirth-20260927-ab12-full"}
        )
        finished = await client.post(f"{base}/compilation/done")
        refused = await client.post(
            f"{base}/docs",
            json={
                "kind": "setting",
                "body_md": "# x",
                "body_json": {},
                "judge": _verdict("setting"),
            },
        )
    assert started.status_code == 200 and started.json()["series"]["compilation"] is True
    assert start.await_args.args[2:] == ("rebirth-20260927-ab12", "rebirth-20260927-ab12-full")
    assert finished.status_code == 200 and finished.json()["slug"] == "rebirth-20260927-ab12"
    assert refused.status_code == 422
    assert submit.await_args.args[3] is settings, "the rewrite count comes from the settings"
    assert submit.await_args.args[2].judge == _verdict("setting")
