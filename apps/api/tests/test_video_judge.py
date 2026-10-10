"""The demonstration question is a tutorial's rule (docs/videos/HANDS-OFF.md §自動品管; ticket
2026-10-10-policy-demo-exempts-explainer-slides).

The first history episode, told from court records, scored 0.16-0.18 three times on "walks the
viewer through a demonstration they can follow along with" while every other check passed, so
its final cut could not approve itself. A video the site's own row files as an explainer or a
story, or whose format is a drama, is asked the other three; a video the site does not know or
has not categorised is asked all four as before. The rows live in an in-memory SQLite database
built from the models, so this runs on every machine.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.ai.jev import NoulAnswer
from app.config import Settings
from app.db import Base, get_session
from app.models import VideoProject, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api as automation_api
from app.video_automation import judge as judging
from app.video_automation import settings as settings_service
from app.video_automation.models import (
    VideoAutomationSettings,
    VideoDramaEpisode,
    VideoDramaSeries,
)
from app.video_speech import admin_api as speech_api

TABLES = (
    VideoToolToken,
    VideoProject,
    VideoAutomationSettings,
    VideoDramaSeries,
    VideoDramaEpisode,
)
URL = "/api/v1/video/automation/judge/policy"
BODY = {"script": "一八七二年，瑪麗．賽勒斯特號被發現時，船上一個人也沒有。", "viewpoint": ""}
TUTORIAL_ASKED = ["stance", "demo", "advice", "sponsored"]
EXPLAINER_ASKED = ["stance", "advice", "sponsored"]
# What the pilot scored: a demonstration nobody could find, everything else well inside.
ANSWERS = {"stance": 0.85, "demo": 0.17, "advice": 0.05, "sponsored": 0.1}
EXPLAINER_NOTE = "Jev：符合立場 0.85、有示範：不適用（解說）、建議 0.05、業配 0.10，通過"
EXPLAINER_VERDICT = {
    "stance": 0.85,
    "demo": None,
    "advice": 0.05,
    "sponsored": 0.1,
    "passed": True,
    "note": EXPLAINER_NOTE,
    "questions": "explainer",
    "observation": None,
    "disparage": None,
}
TUTORIAL_VERDICT = {
    "stance": 0.85,
    "demo": 0.17,
    "advice": 0.05,
    "sponsored": 0.1,
    "passed": False,
    "note": ("Jev：符合立場 0.85、有示範 0.17、建議 0.05、業配 0.10；沒過（有示範低於 0.6）"),
    "questions": "tutorial",
    "observation": None,
    "disparage": None,
}


def _answers(**scores: float) -> dict[str, Any]:
    return {name: NoulAnswer(type="noul", noul=value) for name, value in scores.items()}


@pytest.fixture
async def db() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync: Base.metadata.create_all(
                sync, tables=[model.__table__ for model in TABLES]
            )
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        settings = await settings_service.settings_row(session)
        settings.channel_stance = "只講查得到出處的事，傳說與事實分開講。"
        await session.commit()
    try:
        yield factory
    finally:
        await engine.dispose()


def _app(factory: async_sessionmaker[AsyncSession]) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(automation_api.tool_router, prefix="/api/v1")

    async def session() -> AsyncIterator[AsyncSession]:
        async with factory() as opened:
            yield opened

    app.dependency_overrides[get_session] = session
    app.dependency_overrides[speech_api.video_tool] = lambda: VideoToolToken(
        id=uuid4(), name="worker", token_hash="h", token_prefix="mkv_w"
    )
    return app


async def _projects(
    factory: async_sessionmaker[AsyncSession], *rows: tuple[str, str, str | None]
) -> None:
    """Videos as (slug, format, category) rows."""
    async with factory() as session:
        for slug, video_format, category in rows:
            session.add(
                VideoProject(
                    slug=slug, title=slug, stage="final", format=video_format, category=category
                )
            )
        await session.commit()


def _jev(monkeypatch: pytest.MonkeyPatch) -> list[list[str]]:
    """Jev answers every question it is asked from ANSWERS; the list records what was asked."""
    asked: list[list[str]] = []

    async def ask(
        settings: Settings,
        redis: Any,
        state: dict[str, Any],
        questions: dict[str, Any],
        client: httpx.AsyncClient | None,
    ) -> dict[str, Any]:
        asked.append(list(questions))
        return _answers(**{name: ANSWERS[name] for name in questions})

    monkeypatch.setattr(judging, "_ask", ask)
    monkeypatch.setattr(automation_api, "load_runtime_settings", AsyncMock(return_value=Settings()))
    monkeypatch.setattr(automation_api, "get_redis", lambda: object())
    monkeypatch.setattr(automation_api, "enforce_named_rate_limit", AsyncMock())
    return asked


async def _judge(factory: async_sessionmaker[AsyncSession], *slugs: str) -> list[httpx.Response]:
    async with AsyncClient(transport=ASGITransport(app=_app(factory)), base_url="http://t") as c:
        return [await c.post(URL, json={**BODY, "slug": slug}) for slug in slugs]


async def test_an_explainer_and_a_story_are_not_asked_for_a_demonstration(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch
) -> None:
    await _projects(
        db, ("curio-h01", "slides", "explainer"), ("brand-told-once", "slides", "story")
    )
    asked = _jev(monkeypatch)
    explainer, story = await _judge(db, "curio-h01", "brand-told-once")
    assert asked == [EXPLAINER_ASKED, EXPLAINER_ASKED]
    for answer in (explainer, story):
        assert answer.status_code == 200, answer.text
        assert answer.json() == EXPLAINER_VERDICT


async def test_a_drama_is_not_asked_whatever_its_category(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch
) -> None:
    await _projects(db, ("saga-one", "drama", None), ("saga-two", "drama", "long-drama"))
    asked = _jev(monkeypatch)
    answers = await _judge(db, "saga-one", "saga-two")
    assert asked == [EXPLAINER_ASKED, EXPLAINER_ASKED]
    assert [answer.json() for answer in answers] == [EXPLAINER_VERDICT, EXPLAINER_VERDICT]


async def test_a_tutorial_an_uncategorised_video_and_one_the_site_never_saw_are_still_asked(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch
) -> None:
    await _projects(
        db,
        ("ai-agent-permissions", "slides", "tutorial"),
        ("ai-term-context-window", "slides", "ai-terms"),
        ("not-sorted-yet", "slides", None),
    )
    asked = _jev(monkeypatch)
    answers = await _judge(
        db, "ai-agent-permissions", "ai-term-context-window", "not-sorted-yet", "never-reported"
    )
    assert asked == [TUTORIAL_ASKED] * 4
    for answer in answers:
        assert answer.status_code == 200, answer.text
        assert answer.json() == TUTORIAL_VERDICT


async def test_the_request_cannot_say_which_category_it_is(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch
) -> None:
    await _projects(db, ("ai-agent-permissions", "slides", "tutorial"))
    asked = _jev(monkeypatch)
    async with AsyncClient(transport=ASGITransport(app=_app(db)), base_url="http://t") as c:
        for extra in ({"category": "explainer"}, {"format": "drama"}, {"questions": "explainer"}):
            refused = await c.post(URL, json={**BODY, "slug": "ai-agent-permissions", **extra})
            assert refused.status_code == 422, refused.text
    assert asked == []


async def test_a_cut_short_keeps_its_own_note_even_when_it_is_filed_as_an_explainer(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch
) -> None:
    async with db() as session:
        session.add(
            VideoProject(
                slug="curio-h01-short-1",
                title="t",
                stage="final",
                format="shorts",
                shorts_line="cut",
                category="explainer",
            )
        )
        await session.commit()
    asked = _jev(monkeypatch)
    (cut,) = await _judge(db, "curio-h01-short-1")
    assert asked == [EXPLAINER_ASKED]
    assert cut.json()["questions"] == "cut" and cut.json()["note"].startswith("Jev（精華）")


def test_an_explainer_s_verdict_ignores_the_demonstration_and_keeps_the_other_thresholds() -> None:
    passed = judging.read_policy_answers(
        _answers(stance=0.85, advice=0.05, sponsored=0.1), "explainer"
    )
    assert passed.passed and passed.demo is None and passed.questions == "explainer"
    assert passed.note == EXPLAINER_NOTE
    failed = judging.read_policy_answers(
        _answers(stance=0.5, advice=0.4, sponsored=0.6), "explainer"
    )
    assert not failed.passed and failed.demo is None
    assert failed.note == (
        "Jev：符合立場 0.50、有示範：不適用（解說）、建議 0.40、業配 0.60；"
        "沒過（符合立場低於 0.6；建議高於 0.3；業配高於 0.3）"
    )


def test_a_tutorial_s_verdict_and_note_are_what_they_were() -> None:
    verdict = judging.read_policy_answers(_answers(stance=0.8, demo=0.7, advice=0.1, sponsored=0.2))
    assert verdict.passed and verdict.demo == 0.7 and verdict.questions == "tutorial"
    assert verdict.note == "Jev：符合立場 0.80、有示範 0.70、建議 0.10、業配 0.20，通過"
    assert judging.policy_note(0.8, 0.5, 0.1, 0.2, False) == (
        "Jev：符合立場 0.80、有示範 0.50、建議 0.10、業配 0.20；沒過（有示範低於 0.6）"
    )
    assert not judging.read_policy_answers(
        _answers(stance=0.8, demo=0.5, advice=0.1, sponsored=0.2)
    ).passed
