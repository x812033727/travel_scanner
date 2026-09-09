from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI, Header
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.analytics.discovery import MEASURED_EVENTS, USEFUL_EVENTS, event_summary, router
from app.analytics.schemas import AnalyticsEventInput
from app.analytics.service import EVENT_NAMES, _properties
from app.auth.service import current_user
from app.config import Settings
from app.db import get_session
from app.i18n import ERROR_DETAILS, LOCALES
from app.models import AnalyticsEvent, User
from app.problems import AppError, app_error_handler


def test_discovery_metrics_empty_is_unknown_not_zero_rate() -> None:
    assert event_summary({})["empty_search_rate"] is None
    summary = event_summary({"discovery_search": 4, "discovery_empty": 1, "content_saved": 2})
    assert summary["empty_search_rate"] == 0.25
    assert summary["saves"] == 2
    assert summary["published_posts"] == 0


def test_measurement_is_server_owned_and_never_needs_search_or_member_properties() -> None:
    assert set(MEASURED_EVENTS) <= set(EVENT_NAMES)
    assert set(USEFUL_EVENTS) <= set(MEASURED_EVENTS)
    browser_names = AnalyticsEventInput.model_json_schema()["properties"]["name"]["enum"]
    assert "content_saved" not in browser_names
    assert "post_published" not in browser_names
    assert _properties({"query": "京都 下雨 帶小孩", "email": "private@example.test"}) == {}


def test_discovery_errors_have_five_locale_messages() -> None:
    for locale in LOCALES:
        assert ERROR_DETAILS[locale]["discovery_unavailable"]
        assert ERROR_DETAILS[locale]["discovery_version_conflict"]


@pytest.mark.asyncio
async def test_admin_metrics_enforce_permissions_environment_bots_window_and_disable(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(AnalyticsEvent.__table__.create)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    now = datetime.now(UTC)
    settings = Settings(analytics_enabled=True, app_env="production")
    monkeypatch.setattr(
        "app.analytics.discovery.load_runtime_settings", AsyncMock(return_value=settings)
    )

    def event(name, owner, days=0, **fields):
        return AnalyticsEvent(
            event_id=uuid4(),
            event_name=name,
            occurred_at=now - timedelta(days=days),
            normalized_path="/explore",
            locale="en",
            session_hash=owner,
            visitor_day_hash="daily",
            environment="production",
            **fields,
        )

    async with factory() as session:
        session.add_all(
            [
                event("discovery_search", "reader"),
                event("discovery_search", "reader", 1),
                event("discovery_empty", "reader"),
                event("content_saved", "reader"),
                event("content_saved", "reader", 2),
                event("post_published", "second", properties_json={"publication_source": "author"}),
                event(
                    "post_published",
                    "moderator",
                    properties_json={"publication_source": "moderator"},
                ),
                event("content_saved", "bot", is_bot=True),
                event("content_saved", "expired", 9),
            ]
        )
        staging = event("content_saved", "staging")
        staging.environment = "staging"
        session.add(staging)
        await session.commit()

    async def database():
        async with factory() as session:
            yield session

    async def authenticate(x_test_role: str | None = Header(default=None)):
        if not x_test_role:
            raise AppError(401, "authentication_required", "Sign in")
        return User(id=uuid4(), email="metrics@example.test", is_admin=x_test_role == "admin")

    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)
    app.include_router(router)
    app.dependency_overrides[get_session] = database
    app.dependency_overrides[current_user] = authenticate
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            assert (await client.get("/admin/discovery/metrics")).status_code == 401
            assert (
                await client.get("/admin/discovery/metrics", headers={"X-Test-Role": "member"})
            ).status_code == 403
            response = await client.get(
                "/admin/discovery/metrics", headers={"X-Test-Role": "admin"}
            )
            assert response.status_code == 200
            assert response.headers["Cache-Control"] == "no-store"
            result = response.json()
            assert result["saves"] == 2
            assert result["empty_search_rate"] == 0.5
            assert result["engaged_sessions"] == 2
            assert result["returning_engaged_sessions"] == 1
            assert result["member_day7_retention"] is None
            assert result["save_to_trip_conversion"] is None
            assert "reader" not in response.text
            settings.analytics_enabled = False
            result = (
                await client.get("/admin/discovery/metrics", headers={"X-Test-Role": "admin"})
            ).json()
            assert result["enabled"] is False
            assert result["saves"] == 0
            assert result["empty_search_rate"] is None
    finally:
        await engine.dispose()
