"""A long drama series: what the worker does next, the documents' shapes, and the routes."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, select

from app.auth.service import current_user
from app.db import SessionFactory, engine, get_session
from app.models import User, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api
from app.video_automation import series as service
from app.video_automation import settings as settings_service
from app.video_automation.models import (
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaRequest,
    VideoDramaSeries,
)
from app.video_automation.schemas import (
    SeriesDocSubmitIn,
    SeriesEpisodeRecapIn,
    SeriesIn,
    SeriesJobOut,
    SeriesOut,
)
from app.video_speech import admin_api as speech_api

WHEN = datetime(2026, 9, 27, 1, 0, tzinfo=UTC)


def _series(**changes: Any) -> VideoDramaSeries:
    values: dict[str, Any] = {
        "id": uuid4(),
        "slug": "xianxia",
        "title": "問劍",
        "premise": "兩個少年在正道與魔道之間",
        "aspects": ["world", "bonds"],
        "tone": "dual-male-leads-subtext",
        "style_preset": "cinematic-3d",
        "target_minutes": 3,
        "planned_episodes": 25,
        "episodes_per_chapter": 10,
        "open_ended": True,
        "status": "active",
        "note": None,
        "requested_chapter": None,
        "force_next": False,
        "created_at": WHEN,
        "updated_at": WHEN,
    }
    values.update(changes)
    return VideoDramaSeries(**values)


def _doc(kind: str, chapter: int = 0, version: int = 1, status: str = "approved") -> VideoDramaDoc:
    return VideoDramaDoc(
        id=uuid4(),
        kind=kind,
        chapter_number=chapter,
        version=version,
        body_md="# doc",
        body_json={},
        status=status,
        note="再緊一點" if status == "rejected" else None,
        created_at=WHEN,
    )


def _episode(number: int, status: str = "ready", series: VideoDramaSeries | None = None) -> Any:
    return VideoDramaEpisode(
        id=uuid4(),
        series_id=series.id if series else uuid4(),
        number=number,
        chapter_number=(number - 1) // 10 + 1,
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
    }
    values.update(changes)
    return VideoAutomationSettings(**values)


def _next(
    series: VideoDramaSeries,
    docs: list[VideoDramaDoc],
    episodes: list[Any],
    settings: VideoAutomationSettings | None = None,
    started_this_month: int = 0,
) -> service.NextJob | None:
    return service.next_job_for(
        series, docs, episodes, settings or _settings(), started_this_month=started_this_month
    )


def test_chapters_are_cut_from_the_episode_count_and_the_last_one_may_be_short() -> None:
    series = _series()
    assert service.chapter_count(25, 10) == 3
    assert service.chapter_count(100, 10) == 10
    assert service.chapter_range(series, 1) == (1, 10)
    assert service.chapter_range(series, 3) == (21, 25)
    assert service.chapter_of(series, 11) == 2


def test_documents_are_planned_in_order_and_rewritten_from_a_note_a_limited_number_of_times() -> (
    None
):
    setting = _series(status="setting")
    first = _next(setting, [], [])
    assert first is not None and (first.kind, first.previous, first.rewrites_left) == (
        "setting",
        None,
        2,
    )
    rejected = _doc("setting", status="rejected")
    again = _next(setting, [rejected], [])
    assert again is not None and again.previous is rejected and again.rewrites_left == 2
    twice = _doc("setting", version=3, status="rejected")
    assert _next(setting, [_doc("setting", version=2, status="rejected"), twice], []) is None
    assert _next(setting, [_doc("setting", status="review")], []) is None, "the owner is reading it"
    outline = _series(status="outline")
    job = _next(outline, [_doc("setting")], [])
    assert job is not None and job.kind == "outline"
    assert _next(_series(status="paused"), [], []) is None


def test_chapter_one_is_planned_before_any_episode_and_the_next_when_its_turn_is_near() -> None:
    series = _series()
    approved = [_doc("setting"), _doc("outline")]
    job = _next(series, approved, [_episode(n, "planned") for n in range(1, 26)])
    assert job is not None and (job.kind, job.chapter_number) == ("chapter", 1)

    chapter_one = approved + [_doc("chapter", 1)]
    episodes = [_episode(n, "ready") for n in range(1, 11)] + [
        _episode(n, "planned") for n in range(11, 26)
    ]
    job = _next(series, chapter_one, episodes)
    assert job is not None and (job.kind, job.episode_number) == ("episode", 1)

    # Episodes 1-7 are done: chapter 2 is not due yet (10 - 2 = 8), so episode 8 goes first.
    done = [_episode(n, "done") for n in range(1, 8)] + [_episode(n, "ready") for n in range(8, 11)]
    job = _next(series, chapter_one, done + episodes[10:])
    assert job is not None and (job.kind, job.episode_number) == ("episode", 8)
    # Episode 8 started: chapter 2 is due, and it is planned while episode 8 is in the making.
    near = (
        [_episode(n, "done") for n in range(1, 8)]
        + [_episode(8, "started")]
        + [_episode(n, "ready") for n in (9, 10)]
    )
    job = _next(series, chapter_one, near + episodes[10:])
    assert job is not None and (job.kind, job.chapter_number) == ("chapter", 2)
    # The owner asked for chapter 2 early.
    early = _series(requested_chapter=2)
    job = _next(
        early, chapter_one, done[:3] + [_episode(n, "ready") for n in range(4, 11)] + episodes[10:]
    )
    assert job is not None and (job.kind, job.chapter_number) == ("chapter", 2)
    # Chapter 2 waits for the owner: no chapter job, the episodes still move.
    waiting = chapter_one + [_doc("chapter", 2, status="review")]
    job = _next(series, waiting, done + episodes[10:])
    assert job is not None and (job.kind, job.episode_number) == ("episode", 8)


def test_episodes_start_one_at_a_time_after_the_previous_is_done_unless_the_owner_pushes() -> None:
    series = _series()
    docs = [_doc("setting"), _doc("outline"), _doc("chapter", 1)]
    ready = [_episode(n, "ready") for n in range(1, 11)]
    in_flight = [_episode(1, "started")] + ready[1:]
    assert _next(series, docs, in_flight) is None, "one at a time"
    assert _next(series, docs, in_flight, _settings(series_max_in_flight=2)) is None, (
        "episode 1 is not done"
    )
    job = _next(_series(force_next=True), docs, in_flight, _settings(series_max_in_flight=2))
    assert job is not None and job.episode_number == 2, "the owner said start the next one"
    finished = [_episode(1, "done")] + ready[1:]
    job = _next(series, docs, finished)
    assert job is not None and job.episode_number == 2
    assert _next(series, docs, finished, _settings(series_auto_continue=False)) is None
    skipped = [_episode(1, "done"), _episode(2, "skipped")] + ready[2:]
    job = _next(series, docs, skipped)
    assert job is not None and job.episode_number == 3
    assert _next(series, docs, finished, started_this_month=30) is None, "the month's cap"
    assert _next(series, docs, [_episode(n, "planned") for n in range(1, 11)]) is None, (
        "nothing ready"
    )


def test_a_document_the_worker_sends_must_have_the_shape_the_owner_reads() -> None:
    series = _series()

    def doc(kind: str, chapter: int = 0, **body: Any) -> SeriesDocSubmitIn:
        return SeriesDocSubmitIn(kind=kind, chapter_number=chapter, body_md="# x", body_json=body)

    assert "characters" in str(service.doc_problem(series, doc("setting")))
    assert (
        service.doc_problem(
            series, doc("setting", characters=[{"id": "a", "name": "阿", "appearance": "x"}])
        )
        is None
    )
    assert "3 chapters" in str(service.doc_problem(series, doc("outline", chapters=[])))
    chapters = [
        {
            "number": k,
            "title": f"第 {k} 篇",
            "episodes": [
                {"number": n, "title": f"第 {n} 集", "logline": "…"}
                for n in range(*service.chapter_range(series, k))
            ]
            + [{"number": service.chapter_range(series, k)[1], "title": "尾", "logline": "…"}],
        }
        for k in (1, 2, 3)
    ]
    assert service.doc_problem(series, doc("outline", chapters=chapters)) is None
    beats = {"hook": "h", "conflict": "c", "turn": "t", "cliffhanger": "x"}
    short = [{"number": n, **beats} for n in range(1, 10)]
    assert "covers episodes 1 to 10" in str(
        service.doc_problem(series, doc("chapter", 1, episodes=short))
    )
    lacking = [{"number": n, **beats} for n in range(1, 11)]
    lacking[3] = {"number": 4, "hook": "h"}
    assert "episode 4 lacks conflict, turn, cliffhanger" in str(
        service.doc_problem(series, doc("chapter", 1, episodes=lacking))
    )
    assert (
        service.doc_problem(
            series, doc("chapter", 1, episodes=[{"number": n, **beats} for n in range(1, 11)])
        )
        is None
    )
    assert "outside" in str(service.doc_problem(series, doc("chapter", 9, episodes=[])))

    rows = service.episode_rows_from_outline(series, {"chapters": chapters[:1]})
    assert rows[1]["title"] == "第 1 集" and rows[25]["title"] == "第 25 集" and len(rows) == 25
    planned = service.beats_from_chapter(
        {"episodes": [{"number": 2, **beats, "tension": [2, 3, 3, 4, 5]}]}
    )
    assert planned[2]["tension"] == [2, 3, 3, 4, 5]


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


def _series_in() -> dict[str, Any]:
    return {
        "slug": "xianxia",
        "title": "問劍",
        "premise": "兩個少年",
        "aspects": ["world", "bonds"],
    }


@pytest.mark.asyncio
async def test_the_owner_routes_need_the_content_capabilities_and_the_drama_switch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    row = _series()
    view = service.summary_view(row, [], [])
    out = SeriesOut(**view.model_dump(), docs=[], episodes=[])
    monkeypatch.setattr(service, "list_series", AsyncMock(return_value=[view]))
    monkeypatch.setattr(service, "create_series", AsyncMock(return_value=out))
    monkeypatch.setattr(service, "decide_doc", AsyncMock(return_value=out))
    monkeypatch.setattr(
        settings_service,
        "settings_row",
        AsyncMock(return_value=VideoAutomationSettings(drama_enabled=False)),
    )
    base = "/api/v1/admin/video-automation/series"
    async with AsyncClient(
        transport=ASGITransport(app=_app(_user("viewer"))), base_url="http://t"
    ) as client:
        listed = await client.get(base)
        refused = await client.post(base, json=_series_in())
    assert listed.status_code == 200 and listed.json()["series"][0]["slug"] == "xianxia"
    assert listed.json()["series"][0]["chapters"] == 3
    assert refused.status_code == 403
    async with AsyncClient(
        transport=ASGITransport(app=_app(_user("owner"))), base_url="http://t"
    ) as client:
        off = await client.post(base, json=_series_in())
        monkeypatch.setattr(
            settings_service,
            "settings_row",
            AsyncMock(return_value=VideoAutomationSettings(drama_enabled=True)),
        )
        created = await client.post(base, json=_series_in())
        bad = await client.post(base, json={**_series_in(), "aspects": ["world", "world"]})
        decided = await client.post(
            f"{base}/xianxia/docs/chapter/2/decision", json={"decision": "approve"}
        )
        unknown = await client.post(
            f"{base}/xianxia/docs/boss/decision", json={"decision": "approve"}
        )
    assert off.status_code == 409 and off.json()["code"] == "video_drama_disabled"
    assert created.status_code == 201 and created.json()["status"] == "active"
    assert bad.status_code == 422
    assert decided.status_code == 200
    assert service.decide_doc.await_args.args[3:] == ("chapter", 2, "approve", None)  # type: ignore[attr-defined]
    assert unknown.status_code == 404


@pytest.mark.asyncio
async def test_the_worker_routes_need_a_token_and_ask_for_the_next_job(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = _app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        anonymous = await client.get("/api/v1/video/automation/series/next")
    assert anonymous.status_code == 401
    app.dependency_overrides[speech_api.video_tool] = lambda: VideoToolToken(
        id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x"
    )
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(settings_service, "settings_row", AsyncMock(return_value=_settings()))
    monkeypatch.setattr(service, "next_job", AsyncMock(return_value=SeriesJobOut(job=None)))
    problem = service.SeriesRefused(
        422, "video_series_doc_invalid", "a setting book needs a characters list"
    )
    monkeypatch.setattr(service, "submit_doc", AsyncMock(side_effect=problem))
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        nothing = await client.get("/api/v1/video/automation/series/next")
        refused = await client.post(
            "/api/v1/video/automation/series/xianxia/docs",
            json={"kind": "setting", "body_md": "# x", "body_json": {}},
        )
    assert nothing.status_code == 200 and nothing.json() == {"job": None}
    assert refused.status_code == 422 and refused.json()["code"] == "video_series_doc_invalid"


integration = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


@pytest_asyncio.fixture(loop_scope="module")
async def clean_series() -> AsyncIterator[str]:
    slug = f"it-{uuid4().hex[:8]}"
    yield slug
    async with SessionFactory() as session:
        found = await session.scalar(select(VideoDramaSeries).where(VideoDramaSeries.slug == slug))
        if found is not None:
            await session.execute(
                delete(VideoDramaRequest).where(VideoDramaRequest.series_id == found.id)
            )
            await session.delete(found)
            await session.commit()
    await engine.dispose()


@integration
@pytest.mark.asyncio(loop_scope="module")
async def test_a_series_is_planned_document_by_document_and_made_episode_by_episode(
    clean_series: str,
) -> None:
    slug = clean_series
    async with SessionFactory() as session:
        owner = User(email=f"series-{uuid4()}@example.com", password_hash="unused")
        session.add(owner)
        token = VideoToolToken(name="series-test", token_hash=uuid4().hex, token_prefix="mkv_t")
        session.add(token)
        await session.commit()
        settings = await settings_service.settings_row(session)
        created = await service.create_series(
            session,
            owner,
            SeriesIn(
                slug=slug,
                title="問劍",
                premise="兩個少年",
                planned_episodes=25,
                episodes_per_chapter=10,
            ),
        )
        assert created.status == "setting" and created.chapters == 3

        job = (await service.next_job(session, settings)).job
        assert job is not None and job.kind == "setting" and job.series.slug == slug
        await service.submit_doc(
            session,
            slug,
            SeriesDocSubmitIn(
                kind="setting",
                body_md="# 設定集",
                body_json={
                    "characters": [{"id": "a", "name": "阿", "appearance": "x"}],
                    "mysteries": [{"id": "m1"}],
                },
            ),
        )
        assert (await service.next_job(session, settings)).job is None, "the owner is reading it"
        sent_back = await service.decide_doc(
            session, owner, slug, "setting", 0, "reject", "再暗一點"
        )
        assert sent_back.docs[0].status == "rejected"
        job = (await service.next_job(session, settings)).job
        assert job is not None and job.kind == "setting" and job.previous is not None
        assert job.previous.note == "再暗一點" and job.rewrites_left == 2
        await service.submit_doc(
            session,
            slug,
            SeriesDocSubmitIn(
                kind="setting",
                body_md="# 設定集 v2",
                body_json={
                    "characters": [{"id": "a", "name": "阿", "appearance": "x"}],
                    "mysteries": [{"id": "m1"}],
                },
            ),
        )
        approved = await service.decide_doc(session, owner, slug, "setting", 0, "approve", None)
        assert approved.status == "outline" and approved.docs[0].version == 2

        job = (await service.next_job(session, settings)).job
        assert job is not None and job.kind == "outline"
        plan = _series(planned_episodes=25)
        chapters = [
            {
                "number": k,
                "title": f"第 {k} 篇",
                "episodes": [
                    {"number": n, "title": f"第 {n} 集", "logline": f"L{n}"}
                    for n in range(
                        service.chapter_range(plan, k)[0],
                        service.chapter_range(plan, k)[1] + 1,
                    )
                ],
            }
            for k in (1, 2, 3)
        ]
        await service.submit_doc(
            session,
            slug,
            SeriesDocSubmitIn(kind="outline", body_md="# 總綱", body_json={"chapters": chapters}),
        )
        active = await service.decide_doc(session, owner, slug, "outline", 0, "approve", None)
        assert active.status == "active" and len(active.episodes) == 25
        assert active.episodes[24].title == "第 25 集" and active.episodes[0].status == "planned"

        job = (await service.next_job(session, settings)).job
        assert job is not None and (job.kind, job.chapter_number) == ("chapter", 1)
        assert job.context.setting is not None and job.context.mysteries == [{"id": "m1"}]
        beats = {
            "hook": "h",
            "conflict": "c",
            "turn": "t",
            "cliffhanger": "x",
            "tension": [2, 3, 3, 4, 5],
        }
        await service.submit_doc(
            session,
            slug,
            SeriesDocSubmitIn(
                kind="chapter",
                chapter_number=1,
                body_md="# 第一篇",
                body_json={
                    "episodes": [{"number": n, "title": f"E{n}", **beats} for n in range(1, 11)]
                },
            ),
        )
        ready = await service.decide_doc(session, owner, slug, "chapter", 1, "approve", None)
        assert [e.status for e in ready.episodes[:11]] == ["ready"] * 10 + ["planned"]
        assert ready.episodes[0].title == "E1" and ready.episodes[0].beats["tension"] == [
            2,
            3,
            3,
            4,
            5,
        ]

        job = (await service.next_job(session, settings)).job
        assert (
            job is not None
            and job.kind == "episode"
            and job.episode is not None
            and job.episode.number == 1
        )
        started = await service.start_episode(session, token, slug, 1, f"{slug}-e001")
        assert started.request.status == "started" and started.request.slug == f"{slug}-e001"
        assert started.episode.status == "started" and started.context.chapter is not None
        assert (await service.next_job(session, settings)).job is None, "one at a time"
        await service.recap_episode(
            session, slug, 1, SeriesEpisodeRecapIn(recap="阿下山了", state={"a": "下山"})
        )
        finished = await service.finish_episode(session, slug, 1)
        assert finished.status == "done" and finished.recap == "阿下山了"
        request = await session.scalar(
            select(VideoDramaRequest).where(VideoDramaRequest.slug == f"{slug}-e001")
        )
        assert request is not None and request.status == "done" and request.episode_number == 1

        job = (await service.next_job(session, settings)).job
        assert (
            job is not None
            and job.kind == "episode"
            and job.episode is not None
            and job.episode.number == 2
        )
        assert job.context.recaps == [
            {"number": 1, "title": "E1", "recap": "阿下山了", "state": {"a": "下山"}}
        ]

        view = await service.series_view(session, slug)
        assert (view.episodes_done, view.episodes_ready, view.docs_pending) == (1, 9, 0)
        await session.delete(owner)
        await session.delete(token)
        await session.commit()
