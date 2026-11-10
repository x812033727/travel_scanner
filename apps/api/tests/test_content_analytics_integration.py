"""Real PostgreSQL JSON aggregation and idempotent browser ingestion for continuation links."""

import os
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, select

from app.analytics import content, service
from app.analytics.router import router
from app.config import Settings
from app.db import SessionFactory, engine
from app.models import AnalyticsEvent

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL and Redis services"
)


@pytest.mark.asyncio(loop_scope="module")
async def test_content_ingest_replay_privacy_and_postgresql_grouping(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = Settings(analytics_enabled=True, app_env="production")

    async def load(_session):
        return settings

    monkeypatch.setattr(service, "load_runtime_settings", load)
    monkeypatch.setattr(content, "load_runtime_settings", load)
    source = f"/life/news-{uuid4().hex}"
    target = f"/life/guide-{uuid4().hex}"
    ids = [uuid4() for _ in range(6)]
    now = datetime.now(UTC)
    click = {
        "event_id": str(ids[1]),
        "name": "content_link_click",
        "occurred_at": now.isoformat(),
        "path": f"/zh-TW{source}",
        "locale": "zh-TW",
        "content_link": {"placement": "related", "target_path": target},
    }
    page = {**click, "event_id": str(ids[0]), "name": "page_view"}
    page.pop("content_link")
    body = {"session_id": str(uuid4()), "events": [page, click]}
    app = FastAPI()
    app.include_router(router)
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            config = await client.get("/analytics/config")
            assert config.json()["content_link_click_enabled"] is True
            first = await client.post("/analytics/events", json=body)
            assert first.status_code == 202 and first.json()["accepted"] == 2
            replay = await client.post("/analytics/events", json=body)
            assert replay.json()["accepted"] == 0 and replay.json()["duplicates"] == 2
            another = {
                "session_id": body["session_id"],
                "events": [{**click, "event_id": str(ids[2])}],
            }
            assert (await client.post("/analytics/events", json=another)).json()["accepted"] == 1
            for index, header in [(3, "Sec-GPC"), (4, "DNT")]:
                blocked = await client.post(
                    "/analytics/events",
                    json={
                        "session_id": body["session_id"],
                        "events": [{**click, "event_id": str(ids[index])}],
                    },
                    headers={header: "1"},
                )
                assert blocked.json() == {"accepted": 0, "duplicates": 0, "enabled": False}
            unsafe = {
                **click,
                "event_id": str(ids[5]),
                "content_link": {"placement": "related", "target_path": "/admin/secrets"},
            }
            assert (
                await client.post(
                    "/analytics/events", json={"session_id": body["session_id"], "events": [unsafe]}
                )
            ).status_code == 422
        async with SessionFactory() as session:
            stored = list(
                await session.scalars(
                    select(AnalyticsEvent).where(AnalyticsEvent.event_id.in_(ids))
                )
            )
            assert {row.event_id for row in stored} == set(ids[:3])
            assert next(row for row in stored if row.event_id == ids[1]).properties_json == {
                "placement": "related",
                "target_path": target,
            }
            report = await content.content_report(session, "24h", now=now + timedelta(seconds=5))
            selected = [row for row in report["rows"] if row["source_path"] == source]
            assert selected == [
                {
                    "source_path": source,
                    "target_path": target,
                    "placement": "related",
                    "locale": "zh-TW",
                    "clicks": 2,
                }
            ]
    finally:
        async with SessionFactory() as session:
            await session.execute(delete(AnalyticsEvent).where(AnalyticsEvent.event_id.in_(ids)))
            await session.commit()
        await engine.dispose(close=False)
