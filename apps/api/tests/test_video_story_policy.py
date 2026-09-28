"""What would stop a hands-off brand story on the server, or count its cost wrong
(docs/videos/STORY.md §伺服器; ticket 2026-09-28-video-story-api-policy-languages).

A story's narration is asked the story's questions, which the server picks from the video's own
series; a story's languages are decided by the server when its video first reports; dropping an
episode's video skips the episode, so its place is free again; pictures and judge calls may run
faster; a series' picture model is the one its jobs use; and Gemini's pictures are priced at the
size the adapter asks for. The pure rules run without a database; the rest runs on an in-memory
SQLite database built from the models, so it runs on every machine.
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import fakeredis
import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.ai.jev import NoulAnswer
from app.config import Settings
from app.db import Base, get_session
from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api as automation_api
from app.video_automation import judge as judging
from app.video_automation import series as series_service
from app.video_automation import settings as settings_service
from app.video_automation.models import (
    DEFAULT_DRAMA,
    VideoAiRun,
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaMessage,
    VideoDramaRequest,
    VideoDramaSeries,
)
from app.video_automation.schemas import SeriesPatch
from app.video_media import admin_api as media_api
from app.video_media import catalog, meter
from app.video_media import jobs as media_jobs
from app.video_media.catalog import find_model
from app.video_media.jobs import MediaContext, MediaJobFailed, submit_job
from app.video_media.models import VideoMediaJob
from app.video_media.providers import MediaRequest, Submitted
from app.video_media.providers.gemini_images import GeminiImages
from app.video_media.schemas import ClipJobIn, ImageJobIn, JudgeOut
from app.video_media.settings import MediaSettings
from app.video_media.storage import MediaStore
from app.video_reviews import admin_service
from app.video_reviews.schemas import DropIn, LocalesIn, ProjectIn
from app.video_reviews.storage import ReviewStore
from app.video_speech import admin_api as speech_api

WHEN = datetime(2026, 10, 1, 4, 0, tzinfo=UTC)
LOOK = {
    "style": "flat 2D cartoon illustration, warm muted colours",
    "negative": "text, letters, logo, watermark, real person likeness",
}
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 30
STANCE = "故事只講查得到出處的事，傳說與事實分開講。"
# The tutorial's four questions word for word, as they were before brand stories existed: every
# video that is not a story's is still asked exactly these.
TUTORIAL_QUESTIONS = {
    "stance": (
        "This narration is written in keeping with the channel's stance and the owner's "
        "viewpoint, and makes no claim that contradicts them."
    ),
    "demo": (
        "This narration walks the viewer through a concrete demonstration, setting or worked "
        "calculation they can follow along with."
    ),
    "advice": (
        "This narration gives investment, medical, legal or electoral advice (telling the "
        "viewer what to buy, sell, take, sign or vote for)."
    ),
    "sponsored": (
        "This narration reads as sponsored or promotional: it urges the viewer to buy or sign "
        "up for a named product or service, or praises one without weighing it."
    ),
}
STORY_ASKED = ["stance", "observation", "advice", "sponsored", "disparage"]
TUTORIAL_ASKED = ["stance", "demo", "advice", "sponsored"]
# One answer per question either set may ask; each set reads only its own.
ANSWERS = {
    "stance": 0.8,
    "demo": 0.7,
    "advice": 0.1,
    "sponsored": 0.2,
    "observation": 0.75,
    "disparage": 0.05,
}
TUTORIAL_VERDICT = {
    "stance": 0.8,
    "demo": 0.7,
    "advice": 0.1,
    "sponsored": 0.2,
    "passed": True,
    "note": "Jev：符合立場 0.80、有示範 0.70、建議 0.10、業配 0.20，通過",
    "questions": "tutorial",
    "observation": None,
    "disparage": None,
}


def _answers(**scores: float) -> dict[str, Any]:
    return {name: NoulAnswer(type="noul", noul=value) for name, value in scores.items()}


# --- the questions and the rule -------------------------------------------------------------------


def test_the_tutorial_is_asked_what_it_always_was_and_a_story_could_never_pass_it() -> None:
    questions = judging.policy_questions()
    assert {name: question.instructions for name, question in questions.items()} == (
        TUTORIAL_QUESTIONS
    )
    assert all(
        question.type == "noul" and question.criteria == judging.NOUL_CRITERIA
        for question in questions.values()
    )
    assert (
        judging.POLICY_MIN_STANCE,
        judging.POLICY_MIN_DEMO,
        judging.POLICY_MAX_ADVICE,
        judging.POLICY_MAX_SPONSORED,
    ) == (0.6, 0.6, 0.3, 0.3)
    verdict = judging.read_policy_answers(_answers(stance=0.8, demo=0.7, advice=0.1, sponsored=0.2))
    assert verdict.model_dump() == TUTORIAL_VERDICT
    # A story shows nothing to follow along with: under these questions it never passes.
    story = judging.read_policy_answers(_answers(stance=0.9, demo=0.1, advice=0.0, sponsored=0.0))
    assert not story.passed and story.note.endswith("沒過（有示範低於 0.6）")


def test_a_story_is_asked_five_questions_of_wording_and_none_about_a_demonstration() -> None:
    questions = judging.story_policy_questions()
    assert list(questions) == list(judging.STORY_POLICY_RULE) == STORY_ASKED
    assert questions["stance"].instructions == TUTORIAL_QUESTIONS["stance"]
    assert questions["advice"].instructions == TUTORIAL_QUESTIONS["advice"]
    assert "one observation to take away" in questions["observation"].instructions
    assert "recommends that the viewer buy" in questions["sponsored"].instructions
    assert "disparages a named person, company or brand" in questions["disparage"].instructions
    assert all(
        question.type == "noul" and question.criteria == judging.NOUL_CRITERIA
        for question in questions.values()
    )
    # Jev reads text and cannot check a fact, count or read a date (app/ai/jev.py): no question
    # asks it whether anything is true, or about a number, a year or a date.
    for question in questions.values():
        words = question.instructions.lower()
        assert not any(
            word in words
            for word in ("true", "correct", "accurate", "fact", "number", "year", "date", "figure")
        ), question.instructions


def test_a_story_passes_when_every_answer_is_on_its_side_of_its_threshold() -> None:
    assert judging.STORY_POLICY_RULE == {
        "stance": ("min", 0.6),
        "observation": ("min", 0.6),
        "advice": ("max", 0.3),
        "sponsored": ("max", 0.3),
        "disparage": ("max", 0.3),
    }
    edge = {"stance": 0.6, "observation": 0.6, "advice": 0.3, "sponsored": 0.3, "disparage": 0.3}
    assert judging.story_policy_passed(edge), "a threshold itself passes"
    for name, score in (
        ("stance", 0.59),
        ("observation", 0.59),
        ("advice", 0.31),
        ("sponsored", 0.31),
        ("disparage", 0.31),
    ):
        assert not judging.story_policy_passed({**edge, name: score}), name
    missing = {name: score for name, score in edge.items() if name != "disparage"}
    assert not judging.story_policy_passed(missing), "an answer missing never passes"

    verdict = judging.read_story_policy_answers(
        _answers(stance=0.81, observation=0.77, advice=0.05, sponsored=0.1, disparage=0.02)
    )
    assert verdict.model_dump() == {
        "stance": 0.81,
        "demo": None,
        "advice": 0.05,
        "sponsored": 0.1,
        "passed": True,
        "note": "Jev（故事）：符合立場 0.81、留下觀察 0.77、建議 0.05、業配 0.10、貶損 0.02，通過",
        "questions": "story",
        "observation": 0.77,
        "disparage": 0.02,
    }
    failed = judging.read_story_policy_answers(
        _answers(stance=0.9, observation=0.4, advice=0.0, sponsored=0.0, disparage=0.5)
    )
    assert not failed.passed
    assert failed.note.endswith("；沒過（留下觀察低於 0.6；貶損高於 0.3）")


# --- on a database --------------------------------------------------------------------------------

TABLES = (
    User,
    AdminAuditLog,
    VideoToolToken,
    VideoProject,
    VideoReview,
    VideoMediaJob,
    VideoAiRun,
    VideoAutomationSettings,
    VideoDramaSeries,
    VideoDramaDoc,
    VideoDramaMessage,
    VideoDramaRequest,
    VideoDramaEpisode,
)


@pytest.fixture
async def db() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine("sqlite+aiosqlite://")

    # SQLite drops timezone offsets; PostgreSQL hands back aware datetimes.
    def restore_utc(target: Any, _context: Any, *_more: Any) -> None:
        for column in target.__table__.columns:
            value = getattr(target, column.name)
            if isinstance(value, datetime) and value.tzinfo is None:
                setattr(target, column.name, value.replace(tzinfo=UTC))

    for model in TABLES:
        event.listen(model, "load", restore_utc)
        event.listen(model, "refresh", restore_utc)
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync: Base.metadata.create_all(
                sync, tables=[model.__table__ for model in TABLES]
            )
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        settings = await settings_service.settings_row(session)
        settings.drama_enabled = True
        settings.channel_stance = STANCE
        settings.series_max_in_flight = 1
        await session.commit()
    try:
        yield factory
    finally:
        for model in TABLES:
            event.remove(model, "load", restore_utc)
            event.remove(model, "refresh", restore_utc)
        await engine.dispose()


def _token() -> VideoToolToken:
    return VideoToolToken(id=uuid4(), name="worker", token_hash="h", token_prefix="mkv_w")


def _owner() -> User:
    return User(id=uuid4(), email="owner@example.com", password_hash="unused")


async def _series(
    factory: async_sessionmaker[AsyncSession],
    slug: str,
    kind: str,
    episodes: list[tuple[int, str, str]],
    **changes: Any,
) -> None:
    """A series of this kind with these (number, video slug, status) episodes."""
    values: dict[str, Any] = {
        "id": uuid4(),
        "slug": slug,
        "kind": kind,
        "title": f"作品 {slug}",
        "premise": "p",
        "status": "active",
        "planned_episodes": 100,
        "episodes_per_chapter": 10,
        "created_at": WHEN,
        "updated_at": WHEN,
    }
    if kind == "story":
        values.update(
            hands_off=True,
            visual_tier="stills",
            style_preset="custom",
            target_minutes=13,
            image_model="gemini-3.1-flash-image",
            look=dict(LOOK),
        )
    values.update(changes)
    series = VideoDramaSeries(**values)
    async with factory() as session:
        session.add(series)
        for number, video, status in episodes:
            session.add(
                VideoDramaEpisode(
                    id=uuid4(),
                    series_id=series.id,
                    number=number,
                    chapter_number=1,
                    title=f"第 {number} 集",
                    logline="",
                    beats={},
                    status=status,
                    slug=video,
                    state_json={},
                    started_at=WHEN if status in ("started", "done") else None,
                    created_at=WHEN,
                    updated_at=WHEN,
                )
            )
        await session.commit()


async def _episode(factory: async_sessionmaker[AsyncSession], video: str) -> VideoDramaEpisode:
    async with factory() as session:
        found = await session.scalar(
            select(VideoDramaEpisode).where(VideoDramaEpisode.slug == video)
        )
        assert found is not None
        return found


async def _audits(factory: async_sessionmaker[AsyncSession], action: str) -> list[AdminAuditLog]:
    async with factory() as session:
        found = await session.scalars(select(AdminAuditLog).where(AdminAuditLog.action == action))
        return list(found.all())


def _store(tmp_path: Path) -> ReviewStore:
    return ReviewStore(tmp_path / "reviews", max_file_bytes=10**8, max_total_bytes=10**9)


def _report(series: str | None = None, number: int | None = None, **fields: Any) -> ProjectIn:
    """What the worker reports of a video; an episode says its series and number."""
    return ProjectIn(
        title=fields.pop("title", "一支影片"),
        stage=fields.pop("stage", "brief"),
        format="drama" if series else None,
        series_slug=series,
        episode_number=number,
        **fields,
    )


# --- the stance check picks the story's questions from the video's own series ---------------------


def _judge_app(factory: async_sessionmaker[AsyncSession]) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(automation_api.tool_router, prefix="/api/v1")

    async def session() -> AsyncIterator[AsyncSession]:
        async with factory() as opened:
            yield opened

    app.dependency_overrides[get_session] = session
    app.dependency_overrides[speech_api.video_tool] = _token
    return app


async def test_the_server_asks_a_story_the_story_s_questions_and_every_other_video_as_before(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch
) -> None:
    await _series(db, "stories", "story", [(1, "story-rolling-case", "started")])
    await _series(db, "saga", "series", [(1, "saga-one", "started")])
    await _series(
        db,
        "one-off-x",
        "one-off",
        [(1, "one-off-x-video", "started")],
        planned_episodes=1,
        episodes_per_chapter=1,
    )
    asked: list[tuple[list[str], dict[str, Any]]] = []

    async def ask(
        settings: Settings,
        redis: Any,
        state: dict[str, Any],
        questions: dict[str, Any],
        client: httpx.AsyncClient | None,
    ) -> dict[str, Any]:
        asked.append((list(questions), state))
        return _answers(**{name: ANSWERS[name] for name in questions})

    monkeypatch.setattr(judging, "_ask", ask)
    monkeypatch.setattr(automation_api, "load_runtime_settings", AsyncMock(return_value=Settings()))
    monkeypatch.setattr(automation_api, "get_redis", lambda: object())
    monkeypatch.setattr(automation_api, "enforce_named_rate_limit", AsyncMock())
    url = "/api/v1/video/automation/judge/policy"
    body = {"script": "你每天拖著走的行李箱，輪子晚了四十年才出現。", "viewpoint": ""}
    async with AsyncClient(transport=ASGITransport(app=_judge_app(db)), base_url="http://t") as c:
        story = await c.post(url, json={**body, "slug": "story-rolling-case"})
        saga = await c.post(url, json={**body, "slug": "saga-one"})
        one_off = await c.post(url, json={**body, "slug": "one-off-x-video"})
        tutorial = await c.post(url, json={**body, "slug": "ai-agent-permissions"})
        chosen = await c.post(url, json={**body, "slug": "saga-one", "questions": "story"})
    assert [questions for questions, _state in asked] == [
        STORY_ASKED,
        TUTORIAL_ASKED,
        TUTORIAL_ASKED,
        TUTORIAL_ASKED,
    ]
    assert asked[0][1] == {
        "language": "zh-TW",
        "channel_stance": STANCE,
        "owner_viewpoint": "",
        "narration": body["script"],
    }
    assert story.status_code == 200, story.text
    assert story.json() == {
        "stance": 0.8,
        "demo": None,
        "advice": 0.1,
        "sponsored": 0.2,
        "passed": True,
        "note": "Jev（故事）：符合立場 0.80、留下觀察 0.75、建議 0.10、業配 0.20、貶損 0.05，通過",
        "questions": "story",
        "observation": 0.75,
        "disparage": 0.05,
    }
    # A drama's episode, a one-off and a tutorial get the verdict they always got.
    for answer in (saga, one_off, tutorial):
        assert answer.status_code == 200 and answer.json() == TUTORIAL_VERDICT
    # The worker names the video, never the questions: a request that tries is refused whole.
    assert chosen.status_code == 422 and len(asked) == 4


# --- a story's languages --------------------------------------------------------------------------


async def test_the_server_decides_a_story_s_languages_once_when_its_video_first_reports(
    db: async_sessionmaker[AsyncSession], tmp_path: Path
) -> None:
    await _series(
        db,
        "stories",
        "story",
        [(1, "story-rolling-case", "ready"), (2, "story-conveyor-sushi", "ready")],
    )
    store = _store(tmp_path)
    async with db() as session:
        settings = await settings_service.settings_row(session)
        settings.drama_caption_locales = ["ja", "en"]
        settings.series_max_in_flight = 2
        await session.commit()
        await series_service.start_episode(session, _token(), "stories", 1, "story-rolling-case")
    async with db() as session:
        first = await admin_service.upsert_project(
            session, store, "story-rolling-case", _report("stories", 1)
        )
    both = {"metadata": True, "captions": True, "dub": False}
    assert first.locales_decided_at is not None
    assert {locale: choice.model_dump() for locale, choice in first.locales.items()} == {
        "en": both,
        "ja": both,
    }, "the drama's language defaults, in the page's order, titles and captions, no dub"
    assert {locale: parts["captions"].state for locale, parts in first.languages.items()} == {
        "en": "working",
        "ja": "working",
    }
    [decided] = await _audits(db, "video_locales_set")
    assert decided.actor_user_id is None and decided.metadata_json == {
        "slug": "story-rolling-case",
        "locales": {"en": both, "ja": both},
        "decided_by": "server",
        "from": "drama_caption_locales",
    }

    # Once only: a later report, even with the defaults changed since, leaves it alone.
    async with db() as session:
        settings = await settings_service.settings_row(session)
        settings.drama_caption_locales = []
        await session.commit()
        again = await admin_service.upsert_project(
            session, store, "story-rolling-case", _report("stories", 1, stage="script")
        )
    assert list(again.locales) == ["en", "ja"]
    assert again.locales_decided_at == first.locales_decided_at
    assert len(await _audits(db, "video_locales_set")) == 1

    # With no default ticked, the decision is "only Traditional Chinese", decided all the same.
    async with db() as session:
        await series_service.start_episode(session, _token(), "stories", 2, "story-conveyor-sushi")
        second = await admin_service.upsert_project(
            session, store, "story-conveyor-sushi", _report("stories", 2)
        )
    assert second.locales == {} and second.locales_decided_at is not None

    # The owner may still change a story's languages on the panel.
    owner = _owner()
    async with db() as session:
        changed = await admin_service.set_locales(
            session,
            "story-rolling-case",
            owner,
            LocalesIn.model_validate({"locales": {"ko": {"captions": True}}}),
        )
    assert list(changed.locales) == ["ko"]
    assert changed.locales_decided_at == first.locales_decided_at
    audits = await _audits(db, "video_locales_set")
    assert [row.actor_user_id for row in audits] == [None, None, owner.id]


async def test_every_other_video_still_waits_for_the_owner_s_languages(
    db: async_sessionmaker[AsyncSession], tmp_path: Path
) -> None:
    await _series(db, "stories", "story", [(1, "story-rolling-case", "started")])
    await _series(db, "saga", "series", [(1, "saga-one", "started")])
    await _series(
        db,
        "one-off-x",
        "one-off",
        [(1, "one-off-x-video", "started")],
        planned_episodes=1,
        episodes_per_chapter=1,
    )
    async with db() as session:
        settings = await settings_service.settings_row(session)
        settings.drama_caption_locales = ["en"]
        await session.commit()
    store = _store(tmp_path)
    reports = {
        "saga-one": _report("saga", 1),
        "one-off-x-video": _report("one-off-x", 1),
        "ai-agent-permissions": _report(),
        # A report cannot make a video a story's: this one names the story series, but no
        # episode of it is this video.
        "story-imposter": _report("stories", 9),
    }
    for slug, report in reports.items():
        async with db() as session:
            view = await admin_service.upsert_project(session, store, slug, report)
        assert view.locales == {} and view.locales_decided_at is None, slug
    assert await _audits(db, "video_locales_set") == []


# --- dropping an episode's video ------------------------------------------------------------------


async def test_dropping_a_story_s_video_skips_the_story_and_frees_its_place(
    db: async_sessionmaker[AsyncSession], tmp_path: Path
) -> None:
    await _series(
        db,
        "stories",
        "story",
        [(1, "story-rolling-case", "ready"), (2, "story-conveyor-sushi", "ready")],
    )
    store = _store(tmp_path)
    async with db() as session:
        await series_service.start_episode(session, _token(), "stories", 1, "story-rolling-case")
        await admin_service.upsert_project(
            session, store, "story-rolling-case", _report("stories", 1)
        )
        settings = await settings_service.settings_row(session)
        assert (await series_service.next_job(session, settings)).job is None, (
            "the story in the making holds the only place"
        )
    owner = _owner()
    async with db() as session:
        await admin_service.drop_project(
            session, store, "story-rolling-case", owner, DropIn(note="題目跟別支重複")
        )
    episode = await _episode(db, "story-rolling-case")
    assert episode.status == "skipped" and episode.started_at is not None
    [skipped] = await _audits(db, "video_series_episode_skipped")
    assert skipped.actor_user_id == owner.id and skipped.target == "video-series:stories"
    assert skipped.metadata_json == {"number": 1, "dropped_video": "story-rolling-case"}
    async with db() as session:
        settings = await settings_service.settings_row(session)
        job = (await series_service.next_job(session, settings)).job
        series = await session.scalar(select(VideoDramaSeries))
    assert job is not None and job.episode is not None and job.episode.number == 2
    assert series is not None and series.status == "active"


async def test_dropping_a_serial_s_episode_lets_the_next_one_start_as_skipping_it_would(
    db: async_sessionmaker[AsyncSession], tmp_path: Path
) -> None:
    await _series(
        db,
        "saga",
        "series",
        [
            (1, "saga-one", "done"),
            (2, "saga-two", "started"),
            (3, "saga-three", "ready"),
            (4, "saga-four", "ready"),
        ],
        planned_episodes=4,
        episodes_per_chapter=4,
    )
    async with db() as session:
        saga = await session.scalar(select(VideoDramaSeries))
        assert saga is not None
        session.add(
            VideoDramaDoc(
                id=uuid4(),
                series_id=saga.id,
                kind="chapter",
                chapter_number=1,
                version=1,
                body_md="# 第一篇",
                body_json={},
                status="approved",
                decided_at=WHEN,
                created_at=WHEN,
            )
        )
        await session.commit()
    store = _store(tmp_path)
    for video, number in (("saga-one", 1), ("saga-two", 2)):
        async with db() as session:
            await admin_service.upsert_project(session, store, video, _report("saga", number))
    async with db() as session:
        settings = await settings_service.settings_row(session)
        assert (await series_service.next_job(session, settings)).job is None, (
            "episode 3 waits for episode 2, which holds the only place"
        )
    owner = _owner()
    async with db() as session:
        await admin_service.drop_project(session, store, "saga-two", owner, DropIn(note="重寫"))
    assert (await _episode(db, "saga-two")).status == "skipped"
    async with db() as session:
        settings = await settings_service.settings_row(session)
        job = (await series_service.next_job(session, settings)).job
    assert job is not None and job.episode is not None and job.episode.number == 3

    # An episode already done stays done when its video is dropped afterwards.
    async with db() as session:
        await admin_service.drop_project(session, store, "saga-one", owner, DropIn(note="下架"))
    assert (await _episode(db, "saga-one")).status == "done"
    assert len(await _audits(db, "video_series_episode_skipped")) == 1


async def test_dropping_the_last_open_episode_finishes_the_drama(
    db: async_sessionmaker[AsyncSession], tmp_path: Path
) -> None:
    await _series(
        db,
        "one-off-x",
        "one-off",
        [(1, "one-off-x-video", "started")],
        planned_episodes=1,
        episodes_per_chapter=1,
    )
    store = _store(tmp_path)
    async with db() as session:
        await admin_service.upsert_project(
            session, store, "one-off-x-video", _report("one-off-x", 1)
        )
        # A tutorial is no episode: dropping it touches no series.
        await admin_service.upsert_project(session, store, "ai-agent-permissions", _report())
        await admin_service.drop_project(
            session, store, "ai-agent-permissions", _owner(), DropIn(note="不做了")
        )
        assert (await session.scalar(select(VideoDramaSeries))).status == "active"  # type: ignore[union-attr]
        await admin_service.drop_project(
            session, store, "one-off-x-video", _owner(), DropIn(note="不做了")
        )
    assert (await _episode(db, "one-off-x-video")).status == "skipped"
    async with db() as session:
        series = await session.scalar(select(VideoDramaSeries))
    assert series is not None and series.status == "finished"


# --- the media API --------------------------------------------------------------------------------


class FakeImages:
    """A vendor that draws every picture at once and remembers the models it was asked for."""

    name = "fake"

    def __init__(self) -> None:
        self.models: list[str] = []

    async def submit(self, request: MediaRequest, client: httpx.AsyncClient) -> Submitted:
        self.models.append(request.model)
        return Submitted(inline=PNG, content_type="image/png")


def _row(**changes: Any) -> VideoAutomationSettings:
    return VideoAutomationSettings(
        id=1, **{**copy.deepcopy(DEFAULT_DRAMA), "drama_enabled": True, **changes}
    )


def _media(session: AsyncSession, tmp_path: Path, redis: Any) -> MediaContext:
    return MediaContext(
        session=session,
        redis=redis,
        store=MediaStore(tmp_path / "media", max_file_bytes=10**7, max_total_bytes=10**8),
        runtime=Settings(hotspot_guide_gemini_api_key="g"),
        media=MediaSettings(video_media_dir=str(tmp_path / "media")),
        row=_row(),
        token_id=uuid4(),
    )


def _image(slug: str, prompt: str = "a suitcase on four wheels") -> ImageJobIn:
    return ImageJobIn.model_validate({"slug": slug, "purpose": "keyframe", "prompt": prompt})


async def test_a_series_pictures_use_its_own_model_and_nothing_else_does(
    db: async_sessionmaker[AsyncSession], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    await _series(db, "stories", "story", [(1, "story-rolling-case", "started")])
    await _series(db, "saga", "series", [(1, "saga-one", "started")])
    vendor = FakeImages()
    monkeypatch.setattr(media_jobs, "provider_for", lambda runtime, name, kind: vendor)
    redis = fakeredis.aioredis.FakeRedis()
    async with db() as session:
        ctx = _media(session, tmp_path, redis)
        story, _created = await submit_job(ctx, "image", _image("story-rolling-case"))
        saga, _created = await submit_job(ctx, "image", _image("saga-one"))
        tutorial, _created = await submit_job(ctx, "image", _image("ai-agent-permissions"))
        # The shot's first frame, already in the store as the story's picture made it.
        frame = hashlib.sha256(PNG).hexdigest()
        assert ctx.store.path("story-rolling-case", frame) is not None
        clip, _created = await submit_job(
            ctx,
            "clip",
            ClipJobIn.model_validate(
                {
                    "slug": "story-rolling-case",
                    "shot_id": "s01",
                    "prompt": "the case rolls away",
                    "first_frame": frame,
                    "seconds": 8,
                }
            ),
        )
        spent = await meter.month_usd(session, redis)
    assert (story.provider, story.model, float(story.usd_estimate)) == (
        "gemini",
        "gemini-3.1-flash-image",
        0.067,
    ), "the story series names Flash, at its 1K price"
    assert (saga.model, float(saga.usd_estimate)) == ("gemini-3-pro-image", 0.134)
    assert tutorial.model == "gemini-3-pro-image", "a video that is no episode follows the tab"
    assert clip.model == "gemini-omni-1.1-flash", "a series' model is for its pictures only"
    assert vendor.models == [
        "gemini-3.1-flash-image",
        "gemini-3-pro-image",
        "gemini-3-pro-image",
        "gemini-omni-1.1-flash",
    ], "the vendor is asked for the model the job names"
    assert spent == round(0.067 + 0.134 + 0.134 + 8 * 0.15, 4)

    # A name the catalog does not know is refused when the series is written, not here; a
    # model the catalog retires afterwards is refused by name at the next picture.
    with pytest.raises(ValidationError):
        SeriesPatch(image_model="gemini-9-imaginary")
    flash = find_model("gemini", "image", "gemini-3.1-flash-image")
    assert flash is not None
    retired = dataclasses.replace(flash, status="retired")
    monkeypatch.setattr(
        catalog,
        "MEDIA_CATALOG",
        tuple(retired if model.id == flash.id else model for model in catalog.MEDIA_CATALOG),
    )
    async with db() as session:
        with pytest.raises(MediaJobFailed) as refused:
            await submit_job(
                _media(session, tmp_path, redis), "image", _image("story-rolling-case", "x")
            )
    assert refused.value.code == "video_media_model_not_allowed"
    assert "gemini-3.1-flash-image" in refused.value.detail


def test_gemini_pictures_are_priced_at_the_1k_size_the_adapter_asks_for() -> None:
    adapter = GeminiImages("https://generativelanguage.googleapis.com", "k")
    body = adapter.request_body(
        MediaRequest(kind="image", model="gemini-3.1-flash-image", prompt="p", aspect="16:9")
    )
    # No imageSize: Gemini 3 image models answer with a 1K picture. Asking for another size
    # here must change the catalog's price with it.
    assert body["generationConfig"]["imageConfig"] == {"aspectRatio": "16:9"}
    flash = find_model("gemini", "image", "gemini-3.1-flash-image")
    pro = find_model("gemini", "image", "gemini-3-pro-image")
    assert flash is not None and pro is not None
    assert (flash.usd_per_image, pro.usd_per_image) == (0.067, 0.134)
    for model, price in ((flash, "US$0.067"), (pro, "US$0.134")):
        assert model.note is not None
        assert "1K" in model.note and price in model.note and "2026-09-28" in model.note


def _media_app(session: Any) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(media_api.media_router, prefix="/api/v1")

    async def opened() -> AsyncIterator[Any]:
        yield session

    app.dependency_overrides[get_session] = opened
    app.dependency_overrides[speech_api.video_tool] = _token
    return app


async def test_the_media_status_estimates_a_story_s_pictures_at_the_corrected_price(
    db: async_sessionmaker[AsyncSession], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    await _series(db, "stories", "story", [(1, "story-rolling-case", "started")])
    monkeypatch.setattr(media_jobs, "provider_for", lambda runtime, name, kind: FakeImages())
    redis = fakeredis.aioredis.FakeRedis()
    async with db() as session:
        ctx = _media(session, tmp_path, redis)
        await submit_job(ctx, "image", _image("story-rolling-case"))

        async def context(_session: Any, _token_id: Any) -> MediaContext:
            return ctx

        monkeypatch.setattr(media_api, "_context", context)
        transport = ASGITransport(app=_media_app(session))
        async with AsyncClient(transport=transport, base_url="http://t") as client:
            status = await client.get("/api/v1/video/media/status")
    assert status.status_code == 200, status.text
    body = status.json()
    assert body["estimated_usd"] == 0.067
    offered = {option["value"]: option for option in body["models"]["images"]["gemini"]}
    assert offered["gemini-3.1-flash-image"]["usd_per_image"] == 0.067
    assert "1K" in offered["gemini-3.1-flash-image"]["description"]


async def test_pictures_and_judge_calls_have_the_hourly_limits_a_story_needs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    limits: list[tuple[str, int]] = []

    async def limit(namespace: str, identifier: str, *, limit: int, window_seconds: int) -> None:
        assert window_seconds == 3600
        limits.append((namespace, limit))

    redis = fakeredis.aioredis.FakeRedis()
    # The drama switch is off, so every submission stops right after its limit.
    row = _row(drama_enabled=False)

    async def context(session: Any, token_id: Any) -> MediaContext:
        ctx = _media(session, tmp_path, redis)
        ctx.row = row
        return ctx

    verdict = JudgeOut(
        scores={"look": 9.0}, overall=9.0, passed=True, problems=[], notes="ok", model="m"
    )
    monkeypatch.setattr(media_api, "enforce_named_rate_limit", limit)
    monkeypatch.setattr(media_api, "_context", context)
    monkeypatch.setattr(media_api, "judge", AsyncMock(return_value=verdict))
    frame = "a" * 64
    async with AsyncClient(
        transport=ASGITransport(app=_media_app(AsyncMock())), base_url="http://t"
    ) as client:
        image = await client.post(
            "/api/v1/video/media/images",
            json={"slug": "v", "purpose": "keyframe", "prompt": "p"},
        )
        clip = await client.post(
            "/api/v1/video/media/clips",
            json={"slug": "v", "shot_id": "a", "prompt": "p", "first_frame": frame, "seconds": 8},
        )
        music = await client.post(
            "/api/v1/video/media/music", json={"slug": "v", "prompt": "p", "seconds": 60}
        )
        judged = await client.post(
            "/api/v1/video/media/judge",
            json={
                "slug": "v",
                "kind": "keyframe",
                "files": [{"sha256": frame, "label": "kf"}],
                "rubric": [{"key": "look", "question": "same style?"}],
            },
        )
    assert [image.status_code, clip.status_code, music.status_code] == [503, 503, 503]
    assert judged.status_code == 200, judged.text
    assert (media_api.IMAGE_SUBMITS_PER_HOUR, media_api.JUDGES_PER_HOUR) == (240, 360)
    assert limits == [
        ("video_media_submit_image", 240),
        ("video_media_submit", 60),
        ("video_media_submit", 60),
        ("video_media_judge", 360),
    ], "pictures count on their own; clips and music keep their shared, lower limit"
