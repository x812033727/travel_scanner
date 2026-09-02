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
