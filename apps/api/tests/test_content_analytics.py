"""Closed continuation payloads and portable raw-data aggregation, without a new schema."""

from datetime import UTC, datetime, timedelta
from typing import cast
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI, Header
from pydantic import ValidationError
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.analytics import content
from app.analytics.router import admin_router
from app.analytics.schemas import AnalyticsEventInput, ContentLinkInput, content_path
from app.auth.service import current_user
from app.config import Settings
from app.db import get_session
from app.models import AnalyticsEvent, User
from app.problems import AppError, app_error_handler

NOW = datetime(2026, 11, 10, 12, tzinfo=UTC)


def payload(**updates: object) -> dict[str, object]:
    return {
        "event_id": str(uuid4()),
        "name": "content_link_click",
        "occurred_at": NOW,
        "path": "/zh-TW/life/news-story",
        "locale": "zh-TW",
        "content_link": {"placement": "related", "target_path": "/en/life/next-guide"},
        **updates,
    }


@pytest.mark.parametrize(
    "target",
    [
        "https://example.test/life/next-guide",
        "//example.test/life/next-guide",
        "/admin/settings",
        "/life/next-guide?email=private",
        "/life/next-guide#token",
        "/life/../admin",
        "/life/%61",
        "/life/" + "a" * 125,
        "/trips/123",
        "/life/Uppercase",
    ],
)
def test_content_targets_are_only_bounded_public_canonical_paths(target: str) -> None:
    with pytest.raises(ValidationError):
        ContentLinkInput(placement="related", target_path=target)


def test_fields_belong_only_to_content_clicks_and_never_accept_arbitrary_properties() -> None:
    parsed = AnalyticsEventInput.model_validate(payload())
    assert parsed.content_link and parsed.content_link.target_path == "/life/next-guide"
    for invalid in (
        payload(content_link=None),
        payload(name="page_view"),
        payload(path="/zh-TW/admin/users"),
        payload(path="/zh-TW/life/news-story?token=private"),
        payload(properties={"email": "private"}),
        payload(
            content_link={
                "placement": "related",
                "target_path": "/life/next-guide",
                "email": "private",
            }
        ),
        payload(content_link={"placement": "topic", "target_path": "/life/next-guide"}),
        payload(content_link={"placement": "related", "target_path": "/life/topics/ai-news"}),
    ):
        with pytest.raises(ValidationError):
            AnalyticsEventInput.model_validate(invalid)
    assert ContentLinkInput(placement="topic", target_path="/zh-TW/ai").target_path == "/ai"
    assert content_path("/ja/guides/topics/connectivity") == "/guides/topics/connectivity"
    assert AnalyticsEventInput.model_validate(payload(name="page_view", content_link=None))


def event(days: float = 0, **updates: object) -> AnalyticsEvent:
    values: dict[str, object] = {
        "event_id": uuid4(),
        "event_name": "content_link_click",
        "occurred_at": NOW - timedelta(days=days),
        "normalized_path": "/life/news-story",
        "locale": "zh-TW",
        "session_hash": "a" * 64,
        "visitor_day_hash": "b" * 64,
        "environment": "production",
        "is_bot": False,
        "properties_json": {"placement": "related", "target_path": "/life/next-guide"},
    }
    values.update(updates)
    return AnalyticsEvent(**values)


@pytest.fixture
def settings(monkeypatch: pytest.MonkeyPatch) -> Settings:
    value = Settings(app_env="production", analytics_retention_days=90)

    async def load(_session):
        return value

    monkeypatch.setattr(content, "load_runtime_settings", load)
    return value


async def factory():
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(cast(Table, AnalyticsEvent.__table__).create)
    return engine, async_sessionmaker(engine, expire_on_commit=False)


@pytest.mark.asyncio
async def test_report_groups_exact_pairs_language_and_position_with_environment_bot_and_time_bounds(
    settings,
) -> None:
    engine, sessions = await factory()
    try:
        async with sessions() as session:
            session.add_all(
                [
                    event(1),
                    event(2),
                    event(3, locale="en"),
                    event(
                        2,
                        properties_json={
                            "placement": "topic",
                            "target_path": "/life/topics/ai-news",
                        },
                    ),
                    event(2, normalized_path="/life/other-story"),
                    event(8),
                    event(1, is_bot=True),
                    event(1, environment="staging"),
                    event(-1),
                    event(1, event_name="page_view", properties_json={}),
                ]
            )
            await session.commit()
            report = await content.content_report(session, "7d", now=NOW)
            bots = await content.content_report(session, "7d", True, now=NOW)
    finally:
        await engine.dispose()
    assert report["total_clicks"] == 5
    assert bots["total_clicks"] == 6
    assert report["rows"][0] == {
        "source_path": "/life/news-story",
        "target_path": "/life/next-guide",
        "placement": "related",
        "locale": "zh-TW",
        "clicks": 2,
    }
    assert len(report["rows"]) == 4
    assert report["first_recorded_at"] == (NOW - timedelta(days=8)).isoformat()
    assert not report["window_clipped"]


@pytest.mark.asyncio
async def test_report_preserves_unknown_history_clips_retention_and_refuses_twelve_months(
    settings,
) -> None:
    settings.analytics_retention_days = 30
    engine, sessions = await factory()
    try:
        async with sessions() as session:
            empty = await content.content_report(session, "30d", now=NOW)
            assert empty["first_recorded_at"] is None and empty["rows"] == []
            session.add_all([event(29), event(31)])
            await session.commit()
            clipped = await content.content_report(session, "90d", now=NOW)
            long = await content.content_report(session, "12m", now=NOW)
    finally:
        await engine.dispose()
    assert clipped["total_clicks"] == 1 and clipped["window_clipped"]
    assert clipped["from"] == (NOW - timedelta(days=30)).isoformat()
    assert long["available"] is False and long["reason"] == "raw_window_only"
    assert long["rows"] == []


@pytest.mark.asyncio
async def test_report_route_requires_analytics_capability_and_has_no_cache(settings) -> None:
    engine, sessions = await factory()

    async def database():
        async with sessions() as session:
            yield session

    async def authenticate(x_test_role: str | None = Header(default=None)):
        if not x_test_role:
            raise AppError(401, "authentication_required", "Sign in")
        return User(id=uuid4(), email="report@example.test", is_admin=x_test_role == "admin")

    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_router)
    app.dependency_overrides[get_session] = database
    app.dependency_overrides[current_user] = authenticate
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            assert (await client.get("/admin/analytics/content")).status_code == 401
            assert (
                await client.get("/admin/analytics/content", headers={"X-Test-Role": "member"})
            ).status_code == 403
            response = await client.get(
                "/admin/analytics/content?range=7d", headers={"X-Test-Role": "admin"}
            )
            assert response.status_code == 200 and response.headers["Cache-Control"] == "no-store"
            assert response.json()["range"] == "7d"
            assert (
                await client.get(
                    "/admin/analytics/content?range=forever", headers={"X-Test-Role": "admin"}
                )
            ).status_code == 422
    finally:
        await engine.dispose()
