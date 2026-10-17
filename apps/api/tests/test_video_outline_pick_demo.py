"""An outline pick asks for a demonstration only of a tutorial-shaped video (docs/videos/HANDS-OFF.md
§Jev 挑大綱; ticket 2026-10-10-outline-pick-demo-exempts-explainers).

The first MiniMax episode of 原來如此事務所, an explainer, was picked with certainty (A, 1.00;
stance 0.92, advice 0.02) and still waited for the owner because 「有示範 0.33 低於 0.6」. The
final gate's policy item already left the question out for an explainer or a story
(test_video_judge.py); the outline gate now reads the same row. A video the site has no row for,
or has not categorised, is judged as before. The rows live in an in-memory SQLite database.
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

from app.ai.jev import ChoiceAnswer, NoulAnswer
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
URL = "/api/v1/video/automation/judge/outline"
BODY = {
    "brief": "為什麼便利商店的飯糰包裝要分兩層？",
    "options": [
        {"key": "A", "title": "從海苔受潮講起"},
        {"key": "B", "title": "從專利講起"},
    ],
}
# What sothatswhy-b26 scored: a certain pick, a demonstration nobody could find in an explainer.
SCORES = {"stance_A": 0.92, "demo_A": 0.33, "stance_B": 0.7, "demo_B": 0.2, "advice": 0.02}
NOT_ASKED_NOTE = "Jev 挑了 A（1.00）：符合立場 0.92、有示範：不適用（解說）、建議 0.02，依設定自動核准"
ASKED_NOTE = (
    "Jev 挑了 A（1.00）：符合立場 0.92、有示範 0.33、建議 0.02；沒過關（有示範 0.33 低於 0.6）"
)


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
        settings.auto_pick_outline = True
        session.add_all(
            VideoProject(slug=slug, title=slug, stage="outline", format=fmt, category=category)
            for slug, fmt, category in (
                ("sothatswhy-b26", "slides", "explainer"),
                ("brand-told-once", "slides", "story"),
                ("hands-on-mcp", "slides", "tutorial"),
                ("no-category-yet", "slides", None),
            )
        )
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


def _jev(monkeypatch: pytest.MonkeyPatch) -> list[list[str]]:
    """Jev picks A with certainty and scores from SCORES; the list records what was asked."""
    asked: list[list[str]] = []

    async def ask(
        settings: Settings,
        redis: Any,
        state: dict[str, Any],
        questions: dict[str, Any],
        client: httpx.AsyncClient | None,
    ) -> dict[str, Any]:
        asked.append(list(questions))
        answers: dict[str, Any] = {
            name: NoulAnswer(type="noul", noul=SCORES[name]) for name in questions if name != "pick"
        }
        answers["pick"] = ChoiceAnswer(
            type="choice", choice="A", confidence=1.0, probabilities={"A": 1.0, "B": 0.0}
        )
        return answers

    monkeypatch.setattr(judging, "_ask", ask)
    monkeypatch.setattr(automation_api, "load_runtime_settings", AsyncMock(return_value=Settings()))
    monkeypatch.setattr(automation_api, "get_redis", lambda: object())
    monkeypatch.setattr(automation_api, "enforce_named_rate_limit", AsyncMock())
    return asked


async def _judge(
    factory: async_sessionmaker[AsyncSession], slug: str, **extra: Any
) -> httpx.Response:
    async with AsyncClient(transport=ASGITransport(app=_app(factory)), base_url="http://t") as c:
        return await c.post(URL, json={**BODY, "slug": slug, **extra})


@pytest.mark.parametrize("slug", ["sothatswhy-b26", "brand-told-once"])
async def test_an_explainer_or_a_story_outline_is_picked_on_stance_and_advice(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch, slug: str
) -> None:
    asked = _jev(monkeypatch)
    response = await _judge(db, slug)
    assert response.status_code == 200, response.text
    assert asked == [["pick", "stance_A", "stance_B", "advice"]]
    pick = response.json()
    assert pick["options"] == {"A": {"stance": 0.92, "demo": None}, "B": {"stance": 0.7, "demo": None}}
    assert pick["passed"] is True
    assert pick["note"] == NOT_ASKED_NOTE


@pytest.mark.parametrize("slug", ["hands-on-mcp", "no-category-yet", "never-seen"])
async def test_a_tutorial_an_uncategorised_video_and_an_unknown_one_are_still_asked(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch, slug: str
) -> None:
    asked = _jev(monkeypatch)
    response = await _judge(db, slug)
    assert response.status_code == 200, response.text
    assert asked == [["pick", "stance_A", "demo_A", "stance_B", "demo_B", "advice"]]
    pick = response.json()
    assert pick["options"]["A"] == {"stance": 0.92, "demo": 0.33}
    assert pick["passed"] is False
    assert pick["note"] == ASKED_NOTE


async def test_the_request_cannot_say_which_category_it_is(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch
) -> None:
    asked = _jev(monkeypatch)
    for extra in ({"category": "explainer"}, {"demo": False}):
        response = await _judge(db, "hands-on-mcp", **extra)
        assert response.status_code == 422, extra
    assert asked == []


def _payload(demo: Any = 0.33) -> dict[str, Any]:
    chosen: dict[str, Any] = {"stance": 0.92}
    if demo is not ...:
        chosen["demo"] = demo
    return {
        "options": [{"key": "A"}, {"key": "B"}],
        "pick": {
            "choice": "A",
            "probabilities": {"A": 1.0, "B": 0.0},
            "options": {"A": chosen, "B": {"stance": 0.7, "demo": None}},
            "advice": 0.02,
        },
    }


def test_the_server_s_rule_reads_the_demonstration_only_when_it_was_asked() -> None:
    for demo in (0.33, None, ...):
        assert judging.outline_pick_passed(_payload(demo), demo=False), demo
        assert not judging.outline_pick_passed(_payload(demo)), demo
    assert judging.outline_pick_passed(_payload(0.6))
    # Stance and advice still hold an explainer back.
    low = _payload(None)
    low["pick"]["options"]["A"]["stance"] = 0.59
    assert not judging.outline_pick_passed(low, demo=False)
    advised = _payload(None)
    advised["pick"]["advice"] = 0.31
    assert not judging.outline_pick_passed(advised, demo=False)
    assert judging.pick_reason(_payload(0.33), demo=False) == NOT_ASKED_NOTE
    assert judging.pick_reason(_payload(None), demo=False) == NOT_ASKED_NOTE


@pytest.mark.parametrize(
    ("category", "approved"),
    [("explainer", True), ("story", True), ("tutorial", False), (None, False)],
)
async def test_the_approval_reads_the_category_from_the_row_it_is_given(
    db: async_sessionmaker[AsyncSession], category: str | None, approved: bool
) -> None:
    async with db() as session:
        assert await settings_service.auto_picks_outline(session, _payload(), category) is approved
        # The switch still decides first.
        row = await settings_service.settings_row(session)
        row.auto_pick_outline = False
        assert not await settings_service.auto_picks_outline(session, _payload(), category)
