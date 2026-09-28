"""The admin page's way to the brand-story backlog (docs/videos/STORY.md): a compiled
stories.json checked and imported through the API, dry run first, and a skipped story brought
back.

The routes run against the in-memory SQLite database of test_video_story.py, each request on a
session of its own, so what a request wrote, or did not, is counted in the tables. The
backlog's rules and the import itself are tested there; here, only what the endpoints add: who
may do what, the dry run that writes nothing, the 422 that carries the whole report, the size
limit, the audit record, and the way back from a skip that the day's count and the worker see.
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.auth.service import current_user
from app.config import Settings
from app.db import get_session
from app.models import AdminAuditLog, User, VideoToolToken
from app.problems import AppError, app_error_handler, validation_error_handler
from app.video_automation import admin_api, stories
from app.video_automation import series as service
from app.video_automation import settings as settings_service
from app.video_automation.models import VideoDramaEpisode, VideoDramaSeries
from tests.test_video_story import THREE, _episode, _file, _series
from tests.test_video_story import db as story_db

db = story_db

BASE = "/api/v1/admin/video-automation/series"
IMPORT = f"{BASE}/stories-test/stories/import"
# The tables an import may write to: the series, its episodes, and the audit log.
WRITTEN = (VideoDramaSeries, VideoDramaEpisode, AdminAuditLog)


def _app(factory: async_sessionmaker[AsyncSession], user: User) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.admin_router, prefix="/api/v1")

    async def session() -> AsyncIterator[AsyncSession]:
        async with factory() as opened:
            yield opened

    app.dependency_overrides[get_session] = session
    app.dependency_overrides[current_user] = lambda: user
    return app


def _client(factory: async_sessionmaker[AsyncSession], user: User) -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=_app(factory, user)), base_url="http://t")


async def _user(factory: async_sessionmaker[AsyncSession], role: str | None) -> User:
    """An account with one admin role (or none), stored, so an audit record can point at it."""
    user = User(id=uuid4(), email=f"{role or 'member'}@example.com", password_hash="unused")
    async with factory() as session:
        session.add(user)
        await session.commit()
    user._admin_roles_cache = frozenset({role} if role else ())  # type: ignore[attr-defined]
    return user


async def _counts(factory: async_sessionmaker[AsyncSession]) -> list[int]:
    async with factory() as session:
        return [
            int(await session.scalar(select(func.count()).select_from(model)) or 0)
            for model in WRITTEN
        ]


async def _audits(factory: async_sessionmaker[AsyncSession], action: str) -> list[AdminAuditLog]:
    async with factory() as session:
        found = await session.scalars(select(AdminAuditLog).where(AdminAuditLog.action == action))
        return list(found.all())


async def _episodes(factory: async_sessionmaker[AsyncSession]) -> list[tuple[int, str]]:
    """Every episode's number and status, of every series, in order."""
    async with factory() as session:
        found = await session.scalars(select(VideoDramaEpisode))
        return sorted((row.number, row.status) for row in found.all())


# --- the import ----------------------------------------------------------------------------------


async def test_a_dry_run_answers_the_report_and_writes_nothing(
    db: async_sessionmaker[AsyncSession],
) -> None:
    viewer = await _user(db, "viewer")
    owner = await _user(db, "owner")
    assert await _counts(db) == [0, 0, 0]
    async with _client(db, viewer) as client:
        dry = await client.post(IMPORT, json={"file": _file(), "limit": 2, "episodes_per_day": 1})
    assert dry.status_code == 200, dry.text
    assert await _counts(db) == [0, 0, 0], "no series, no episode, no audit record"
    body = dry.json()
    assert (body["dry_run"], body["accepted"], body["written"]) == (True, True, False)
    assert (body["series_created"], body["create"], body["stories_imported"]) == (True, 2, 2)
    assert body["rows"]["create"] == ["A01", "B01"]
    # The answer is the import's own report, field for field.
    async with db() as session:
        report = await stories.import_story_rows(
            session, _file(), series_slug="stories-test", limit=2, episodes_per_day=1
        )
    assert body == report.as_dict()

    # Against a series that exists: the rows it would change stay as they are.
    async with _client(db, owner) as client:
        applied = await client.post(IMPORT, json={"file": _file(), "apply": True})
    assert applied.status_code == 200 and applied.json()["written"] is True
    before = await _counts(db)
    renamed = [THREE[0], {**THREE[1], "title": "A title the owner has not applied"}, THREE[2]]
    async with _client(db, viewer) as client:
        again = await client.post(IMPORT, json={"file": _file(renamed)})
    assert again.status_code == 200
    assert (again.json()["update"], again.json()["leave_alone"], again.json()["written"]) == (
        1,
        2,
        False,
    )
    assert await _counts(db) == before
    async with db() as session:
        titles = await session.scalars(
            select(VideoDramaEpisode.title).order_by(VideoDramaEpisode.number)
        )
        assert list(titles.all()) == [story["title"] for story in THREE]


async def test_writing_needs_what_creating_a_series_needs_and_is_audited(
    db: async_sessionmaker[AsyncSession],
) -> None:
    member = await _user(db, None)
    support = await _user(db, "support")
    viewer = await _user(db, "viewer")
    editor = await _user(db, "content")
    async with _client(db, member) as client:
        stranger = await client.post(IMPORT, json={"file": _file()})
    async with _client(db, support) as client:
        unread = await client.post(IMPORT, json={"file": _file()})
    async with _client(db, viewer) as client:
        read_only = await client.post(IMPORT, json={"file": _file(), "apply": True})
    assert stranger.status_code == 403 and stranger.json()["code"] == "admin_required"
    assert unread.status_code == 403 and unread.json()["code"] == "admin_capability_required"
    assert read_only.status_code == 403
    assert read_only.json()["code"] == "admin_capability_required"
    assert await _counts(db) == [0, 0, 0]

    # The pilot: two stories, one a day, by an account that may manage content.
    async with _client(db, editor) as client:
        pilot = await client.post(
            IMPORT, json={"file": _file(), "apply": True, "limit": 2, "episodes_per_day": 1}
        )
        rest = await client.post(IMPORT, json={"file": _file(), "apply": True})
        nothing_new = await client.post(IMPORT, json={"file": _file(), "apply": True})
    assert pilot.status_code == 200, pilot.text
    assert (pilot.json()["written"], pilot.json()["series_created"]) == (True, True)
    assert pilot.json()["rows"]["create"] == ["A01", "B01"]
    assert (rest.json()["create"], rest.json()["leave_alone"]) == (1, 2)
    assert nothing_new.json()["written"] is False, "a run that changes nothing writes nothing"
    async with db() as session:
        series = await session.scalar(select(VideoDramaSeries))
        assert series is not None
        assert (series.kind, series.status, series.episodes_per_day) == ("story", "active", 1)
        assert series.created_by_user_id == editor.id
    assert await _episodes(db) == [(1, "ready"), (2, "ready"), (3, "ready")]

    created = await _audits(db, "video_series_created")
    assert [row.actor_user_id for row in created] == [editor.id]
    imported = sorted(
        await _audits(db, "video_story_imported"), key=lambda row: len(row.metadata_json["created"])
    )
    assert [(row.actor_user_id, row.target) for row in imported] == [
        (editor.id, "video-series:stories-test"),
        (editor.id, "video-series:stories-test"),
    ]
    assert imported[0].metadata_json == {
        "series_created": False,
        "created": ["C01"],
        "updated": [],
        "renumbered": [],
        "left_alone": 2,
        "limit": None,
    }
    assert imported[1].metadata_json == {
        "series_created": True,
        "created": ["A01", "B01"],
        "updated": [],
        "renumbered": [],
        "left_alone": 0,
        "limit": 2,
    }


async def test_the_host_command_records_its_limit_with_no_one_as_the_actor(
    db: async_sessionmaker[AsyncSession],
) -> None:
    """``story_cli`` calls the import with no actor; its record names the limit it ran with."""
    async with db() as session:
        report = await stories.import_story_rows(
            session, _file(), series_slug="stories-test", apply=True, limit=1
        )
    assert report.written and report.create == ["A01"]
    [record] = await _audits(db, "video_story_imported")
    assert record.actor_user_id is None
    assert (record.metadata_json["created"], record.metadata_json["limit"]) == (["A01"], 1)


async def test_a_file_with_a_problem_is_refused_whole_with_the_report(
    db: async_sessionmaker[AsyncSession],
) -> None:
    owner = await _user(db, "owner")
    bad = [THREE[0], {**THREE[1], "sources": THREE[1]["sources"][:2]}, THREE[2]]
    async with _client(db, owner) as client:
        applied = await client.post(IMPORT, json={"file": _file(bad), "apply": True})
        dry = await client.post(IMPORT, json={"file": _file(bad)})
        elsewhere = await client.post(
            f"{BASE}/other-stories/stories/import", json={"file": _file(), "apply": True}
        )
        not_an_object = await client.post(IMPORT, json={"file": [1, 2], "apply": True})
        no_limit = await client.post(IMPORT, json={"file": _file(), "apply": True, "limit": 0})
        no_file = await client.post(IMPORT, json={"apply": True})
    for refused in (applied, dry):
        assert refused.status_code == 422, refused.text
        assert refused.headers["content-type"].startswith("application/problem+json")
        body = refused.json()
        assert (body["status"], body["code"]) == (422, "video_story_import_refused")
        # Two sources left: the claims that cited the third are wrong too, and all are listed.
        assert "B01: sources has 2 entries, at least 3" in body["problems"]
        assert len(body["problems"]) == 3
        assert body["detail"].startswith("企劃清單有 3 個問題，整份都沒有寫入")
        assert (body["refuse"], body["rows"]["refused"]) == (1, ["B01"])
        assert (body["accepted"], body["written"], body["create"]) == (False, False, 0)
        # Every field of the report is there, beside the problem's own.
        assert set(admin_api.StoryImportOut.model_fields) <= set(body)
    assert (applied.json()["dry_run"], dry.json()["dry_run"]) == (False, True)
    # The path names the series; a file for another one is a problem like any other.
    assert elsewhere.status_code == 422
    mismatch = "series.slug is 'stories-test', but --series is 'other-stories'"
    assert mismatch in elsewhere.json()["problems"]
    assert not_an_object.status_code == 422
    assert not_an_object.json()["problems"] == ["the file is not a JSON object"]
    assert no_limit.status_code == 422
    assert no_limit.json()["problems"] == ["--limit must be 1 or more"]
    assert no_file.status_code == 422 and no_file.json()["code"] == "validation_error"
    assert await _counts(db) == [0, 0, 0], "nothing of any of them was written"


async def test_the_request_has_a_named_size_limit_with_room_for_the_real_file(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch
) -> None:
    # The real backlog is about 1.4 MB; the limit is under the API's own 5 MiB cap, so the
    # page hears this endpoint's refusal and not the middleware's.
    assert 3 * 1024 * 1024 <= admin_api.STORY_IMPORT_MAX_BYTES
    assert admin_api.STORY_IMPORT_MAX_BYTES < Settings.model_fields["api_max_request_bytes"].default
    owner = await _user(db, "owner")
    body = json.dumps({"file": _file(), "apply": True}, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    monkeypatch.setattr(admin_api, "STORY_IMPORT_MAX_BYTES", len(body) - 1)
    async with _client(db, owner) as client:
        too_big = await client.post(IMPORT, content=body, headers=headers)
    assert too_big.status_code == 413
    assert too_big.json()["code"] == "video_story_import_too_large"
    assert await _counts(db) == [0, 0, 0]
    monkeypatch.setattr(admin_api, "STORY_IMPORT_MAX_BYTES", len(body))
    async with _client(db, owner) as client:
        just_fits = await client.post(IMPORT, content=body, headers=headers)
    assert just_fits.status_code == 200 and just_fits.json()["written"] is True


# --- bringing a skipped story back ------------------------------------------------------------


async def test_a_skipped_story_comes_back_and_the_worker_sees_it_at_once(
    db: async_sessionmaker[AsyncSession],
) -> None:
    owner = await _user(db, "owner")
    async with _client(db, owner) as client:
        imported = await client.post(IMPORT, json={"file": _file(), "apply": True})
        assert imported.status_code == 200
        for number in (1, 2, 3):
            skipped = await client.post(f"{BASE}/stories-test/episodes/{number}/skip")
            assert skipped.status_code == 200
    async with db() as session:
        settings = await settings_service.settings_row(session)
        assert (await service.next_job(session, settings)).job is None
        view = await service.series_view(session, "stories-test")
        assert view.status == "finished", "skipping the last story finished the series"
        assert view.quota is not None and (view.quota.hold, view.quota.ready) == ("not_active", 0)

    async with _client(db, owner) as client:
        restored = await client.post(f"{BASE}/stories-test/episodes/2/restore")
    assert restored.status_code == 200, restored.text
    body = restored.json()
    assert body["status"] == "active", "the series has a story to make again"
    assert [(e["number"], e["status"]) for e in body["episodes"]] == [
        (1, "skipped"),
        (2, "ready"),
        (3, "skipped"),
    ]
    assert (body["quota"]["ready"], body["quota"]["hold"]) == (1, None)
    async with db() as session:
        token = VideoToolToken(name="story-admin", token_hash=uuid4().hex, token_prefix="mkv_a")
        session.add(token)
        await session.commit()
        settings = await settings_service.settings_row(session)
        job = (await service.next_job(session, settings)).job
        assert job is not None and job.episode is not None
        assert (job.episode.number, job.episode.slug) == (2, "story-conveyor-sushi")
        # And it starts like any other story, through the checks a start makes.
        started = await service.start_episode(
            session, token, "stories-test", 2, "story-conveyor-sushi"
        )
        assert started.episode.status == "started"
    [record] = await _audits(db, "video_series_episode_restored")
    assert (record.actor_user_id, record.target) == (owner.id, "video-series:stories-test")
    assert record.metadata_json == {"number": 2, "story": "B01", "reopened": True}


async def test_a_story_brought_back_waits_for_the_days_count_like_any_other(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch
) -> None:
    clock = {"now": datetime(2026, 10, 1, 4, 0, tzinfo=UTC)}  # noon in Taipei
    monkeypatch.setattr(service, "_now", lambda: clock["now"])
    owner = await _user(db, "owner")
    async with _client(db, owner) as client:
        await client.post(IMPORT, json={"file": _file(), "apply": True, "episodes_per_day": 1})
        await client.post(f"{BASE}/stories-test/episodes/1/skip")
    async with db() as session:
        token = VideoToolToken(name="story-admin", token_hash=uuid4().hex, token_prefix="mkv_a")
        session.add(token)
        await session.commit()
        settings = await settings_service.settings_row(session)
        job = (await service.next_job(session, settings)).job
        assert job is not None and job.episode is not None and job.episode.number == 2
        await service.start_episode(session, token, "stories-test", 2, "story-conveyor-sushi")

    async with _client(db, owner) as client:
        restored = await client.post(f"{BASE}/stories-test/episodes/1/restore")
    assert restored.status_code == 200
    quota = restored.json()["quota"]
    assert (quota["ready"], quota["started_today"], quota["hold"]) == (2, 1, "per_day")
    async with db() as session:
        settings = await settings_service.settings_row(session)
        assert (await service.next_job(session, settings)).job is None, "today's one has started"
        clock["now"] = datetime(2026, 10, 1, 16, 0, tzinfo=UTC)  # midnight in Taipei
        job = (await service.next_job(session, settings)).job
        assert job is not None and job.episode is not None
        assert job.episode.number == 1, "the story brought back is the lowest ready number"
        started = await service.start_episode(
            session, token, "stories-test", 1, "story-rolling-case"
        )
        assert started.episode.started_at == clock["now"]


async def test_only_a_skipped_story_that_never_started_comes_back(
    db: async_sessionmaker[AsyncSession],
) -> None:
    owner = await _user(db, "owner")
    viewer = await _user(db, "viewer")
    async with _client(db, owner) as client:
        await client.post(IMPORT, json={"file": _file(), "apply": True})
    started_at = datetime(2026, 9, 30, 2, 0, tzinfo=UTC)
    async with db() as session:
        # A story that started and was skipped when its video was dropped.
        dropped = await session.scalar(
            select(VideoDramaEpisode).where(VideoDramaEpisode.number == 3)
        )
        assert dropped is not None
        dropped.status = "skipped"
        dropped.started_at = started_at
        # A long series and a one-off, each with a skipped episode that never started.
        for series in (
            _series(
                slug="xianxia",
                kind="series",
                hands_off=False,
                visual_tier="clips",
                target_minutes=3,
                look=None,
                image_model=None,
            ),
            _series(
                slug="one-off-1a2b3c4d",
                kind="one-off",
                hands_off=False,
                visual_tier="clips",
                target_minutes=3,
                planned_episodes=1,
                episodes_per_chapter=1,
                look=None,
                image_model=None,
            ),
        ):
            session.add(series)
            await session.flush()
            episode = _episode(1, "skipped")
            episode.series_id = series.id
            session.add(episode)
        await session.commit()
    before = await _episodes(db)

    async with _client(db, viewer) as client:
        forbidden = await client.post(f"{BASE}/stories-test/episodes/3/restore")
    async with _client(db, owner) as client:
        ready = await client.post(f"{BASE}/stories-test/episodes/1/restore")
        was_started = await client.post(f"{BASE}/stories-test/episodes/3/restore")
        missing = await client.post(f"{BASE}/stories-test/episodes/9/restore")
        serial = await client.post(f"{BASE}/xianxia/episodes/1/restore")
        one_off = await client.post(f"{BASE}/one-off-1a2b3c4d/episodes/1/restore")
        nowhere = await client.post(f"{BASE}/no-such-series/episodes/1/restore")
    assert forbidden.status_code == 403
    assert ready.status_code == 409
    assert ready.json()["code"] == "video_series_episode_not_skipped"
    assert was_started.status_code == 409
    assert was_started.json()["code"] == "video_series_episode_was_started"
    assert "09/30" in was_started.json()["detail"]
    assert "story-first-mouse" in was_started.json()["detail"]
    assert missing.status_code == 404
    for other in (serial, one_off):
        assert other.status_code == 409
        assert other.json()["code"] == "video_series_restore_story_only"
    assert nowhere.status_code == 404
    assert await _episodes(db) == before, "nothing came back"
    assert await _audits(db, "video_series_episode_restored") == []
