import os
from datetime import UTC, datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, select

from app.analytics.service import dashboard, rollup_day
from app.db import SessionFactory, engine
from app.main import app
from app.models import AnalyticsDailyRollup, AnalyticsEvent, ProviderConfig

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL and Redis services",
)


@pytest.mark.asyncio(loop_scope="module")
async def test_ingest_replay_privacy_rollup_and_dashboard() -> None:
    async with SessionFactory() as session:
        await session.execute(delete(AnalyticsDailyRollup))
        await session.execute(delete(AnalyticsEvent))
        row = await session.scalar(
            select(ProviderConfig).where(ProviderConfig.provider == "analytics")
        )
        if row is None:
            row = ProviderConfig(
                provider="analytics",
                enabled=True,
                priority=100,
                config={"analytics_trust_country_header": True},
            )
            session.add(row)
        else:
            row.enabled = True
            row.config = {"analytics_trust_country_header": True}
        await session.commit()

    event_id = uuid4()
    session_id = uuid4()
    trip_id = uuid4()
    body = {
        "session_id": str(session_id),
        "events": [
            {
                "event_id": str(event_id),
                "name": "page_view",
                "occurred_at": datetime.now(UTC).isoformat(),
                "path": f"/zh-TW/trips/{trip_id}?email=private@example.com#token",
                "locale": "zh-TW",
                "referrer": "https://www.google.com/search?q=private",
                "utm_source": "newsletter<script>",
            }
        ],
    }
    transport = ASGITransport(app=app)
    headers = {
        "X-Travel-User-Agent": "Mozilla/5.0 (iPhone) AppleWebKit Safari/605.1",
        "X-Travel-Country": "TW",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        first = await client.post("/api/v1/analytics/events", json=body, headers=headers)
        replay = await client.post("/api/v1/analytics/events", json=body, headers=headers)
        blocked_body = {**body, "events": [{**body["events"][0], "event_id": str(uuid4())}]}
        blocked = await client.post(
            "/api/v1/analytics/events",
            json=blocked_body,
            headers={**headers, "Sec-GPC": "1"},
        )
    assert first.status_code == 202
    assert first.json()["accepted"] == 1
    assert replay.status_code == 202
    assert replay.json()["duplicates"] == 1
    assert blocked.status_code == 202
    assert blocked.json() == {"accepted": 0, "duplicates": 0, "enabled": False}

    async with SessionFactory() as session:
        event = await session.scalar(
            select(AnalyticsEvent).where(AnalyticsEvent.event_id == event_id)
        )
        assert event is not None
        assert event.normalized_path == "/trips/:id"
        assert event.country_code == "TW"
        assert event.device_type == "mobile"
        persisted = " ".join(
            str(value)
            for value in (
                event.normalized_path,
                event.referrer_host,
                event.utm_source,
                event.properties_json,
            )
        )
        assert "private@example.com" not in persisted
        assert str(trip_id) not in persisted
        target_day = event.occurred_at.astimezone(ZoneInfo("Asia/Taipei")).date()
        await rollup_day(session, target_day)
        result = await dashboard(session, "12m", True, False)
        assert result["source"] == "daily_rollup"
        assert result["summary"]["page_views"] >= 1
        assert result["top_pages"][0]["key"] == "/trips/:id"

    await engine.dispose(close=False)


@pytest.mark.asyncio(loop_scope="module")
async def test_a_server_event_joins_the_browser_session_it_came_from() -> None:
    """The claim the whole funnel rests on: both halves of a step are one session.

    A browser reports `discover_requested` through visitor ingest. The server reports
    `trip_created` itself, from inside the request that created the trip. Unless those
    two rows carry the same `session_hash`, the funnel is comparing one person against
    themselves and every conversion rate below the first step is wrong.
    """
    async with SessionFactory() as session:
        await session.execute(delete(AnalyticsDailyRollup))
        await session.execute(delete(AnalyticsEvent))
        row = await session.scalar(
            select(ProviderConfig).where(ProviderConfig.provider == "analytics")
        )
        if row is None:
            session.add(ProviderConfig(provider="analytics", enabled=True, priority=100, config={}))
        else:
            row.enabled = True
        await session.commit()

    browser_session = uuid4()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        email = f"analytics-funnel-{uuid4()}@example.com"
        registered = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "integration-password-123"},
        )
        assert registered.status_code == 201
        token = registered.json()["access_token"]
        # Every call the browser makes carries the header the BFF forwards.
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Travel-Analytics-Session": str(browser_session),
            "X-Travel-User-Agent": "Mozilla/5.0 (iPhone) Safari/605.1",
        }
        ingested = await client.post(
            "/api/v1/analytics/events",
            headers=headers,
            json={
                "session_id": str(browser_session),
                "events": [
                    {
                        "event_id": str(uuid4()),
                        "name": "discover_requested",
                        "occurred_at": datetime.now(UTC).isoformat(),
                        "path": "/",
                        "locale": "zh-TW",
                    }
                ],
            },
        )
        assert ingested.status_code == 202, ingested.text
        assert ingested.json()["accepted"] == 1

        created = await client.post(
            "/api/v1/trips",
            headers=headers,
            json={
                "source": "blank",
                "planning_mode": "manual_blank",
                "name": "觀測用旅程",
                "destination_name": "日本東京",
                "start_date": "2026-11-10",
                "end_date": "2026-11-12",
            },
        )
        assert created.status_code == 201, created.text

        # An old bundle still sending trip_created must not add a second one.
        echoed = await client.post(
            "/api/v1/analytics/events",
            headers=headers,
            json={
                "session_id": str(browser_session),
                "events": [
                    {
                        "event_id": str(uuid4()),
                        "name": "trip_created",
                        "occurred_at": datetime.now(UTC).isoformat(),
                        "path": "/trips",
                        "locale": "zh-TW",
                    }
                ],
            },
        )
        assert echoed.status_code == 202
        assert echoed.json()["accepted"] == 0

    async with SessionFactory() as session:
        events = list((await session.scalars(select(AnalyticsEvent))).all())
        by_name = {event.event_name: event for event in events}
        assert sorted(by_name) == ["discover_requested", "trip_created"]
        assert len([event for event in events if event.event_name == "trip_created"]) == 1
        assert by_name["discover_requested"].session_hash == by_name["trip_created"].session_hash

        server_event = by_name["trip_created"]
        # Recorded against the product surface, not /api/v1/trips — normalize_path
        # refuses anything under /api, so an API path would have dropped the row.
        assert server_event.normalized_path == "/trips"
        assert server_event.is_authenticated is True
        assert server_event.properties_json == {"source": "blank", "planning_mode": "manual_blank"}
        assert str(created.json()["id"]) not in str(server_event.properties_json)

        report = await dashboard(session, "24h", False, False)
        funnel = {step["step"]: step for step in report["funnel"]}
        assert funnel["discover_requested"]["sessions"] == 1
        assert funnel["trip_created"]["sessions"] == 1
        assert funnel["trip_created"]["conversion_rate"] == 100.0

    await engine.dispose(close=False)
