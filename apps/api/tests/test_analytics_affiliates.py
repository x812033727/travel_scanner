"""The affiliate click report counts redirects by surface and never echoes an identifier."""

import json
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI, Header
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.analytics.affiliates import LIMIT, affiliate_report
from app.analytics.router import admin_router
from app.auth.service import current_user
from app.db import get_session
from app.models import AffiliateClick, User
from app.problems import AppError, app_error_handler

NOW = datetime(2026, 9, 12, 12, 0, tzinfo=UTC)
MEMBER = uuid4()


def click(days: float = 0, **fields: object) -> AffiliateClick:
    values: dict[str, object] = {
        "partner": "travelpayouts",
        "module": "hotel",
        "sub_id": "dst_hotel_tokyo_zh-TW_guide",
        "destination_summary": "tokyo",
        "target_host": "tp.media",
        "created_at": NOW - timedelta(days=days),
    }
    values.update(fields)
    return AffiliateClick(**values)


async def _factory():
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(AffiliateClick.__table__.create)
    return engine, async_sessionmaker(engine, expire_on_commit=False)


@pytest.mark.asyncio
async def test_report_groups_the_window_by_surface_and_folds_legacy_sub_ids() -> None:
    engine, factory = await _factory()
    try:
        async with factory() as session:
            session.add_all(
                [
                    click(placement="guide", destination_id="tokyo", brand="klook"),
                    click(
                        placement="guide",
                        destination_id="tokyo",
                        brand="klook",
                        module="activities",
                    ),
                    click(placement="city", destination_id="seoul", partner="klook", brand="klook"),
                    click(
                        partner="stay22",
                        brand="booking",
                        placement="hotspot",
                        target_host="www.stay22.com",
                    ),
                    # Legacy rows: no placement, and a member-derived sub_id from before the guard.
                    click(days=2, sub_id=f"user-{MEMBER}", user_id=MEMBER, search_id=uuid4()),
                    click(days=3, sub_id=f"aff_hotel_{uuid4().hex}", trip_id=uuid4()),
                    # Outside the window, and in the comparison window before it.
                    click(days=8, placement="guide"),
                    click(days=9, placement="guide"),
                    click(days=40, placement="guide"),
                ]
            )
            await session.commit()
        async with factory() as session:
            report = await affiliate_report(session, "7d", now=NOW)
    finally:
        await engine.dispose()

    assert report["total"] == 6
    assert report["previous_total"] == 2
    assert report["change"] == 200.0
    assert report["by_placement"] == [
        {"key": "guide", "value": 2},
        {"key": "unknown", "value": 2},
        {"key": "city", "value": 1},
        {"key": "hotspot", "value": 1},
    ]
    assert report["by_partner"][0] == {"key": "travelpayouts", "value": 4}
    assert {row["key"] for row in report["by_brand"]} == {"klook", "booking", "unknown"}
    # Rows without a destination (the Stay22 row and the two legacy rows) are counted, not
    # dropped: they are what makes an "unknown" share visible to the owner.
    assert report["by_destination"] == [
        {"key": "unknown", "value": 3},
        {"key": "tokyo", "value": 2},
        {"key": "seoul", "value": 1},
    ]
    assert report["top_sub_ids"] == [
        {"key": "dst_hotel_tokyo_zh-TW_guide", "value": 4},
        {"key": "unknown", "value": 2},
    ]
    text = json.dumps(report)
    assert str(MEMBER) not in text
    assert "user-" not in text
    assert "search_id" not in text and "trip_id" not in text


@pytest.mark.asyncio
async def test_report_caps_each_dimension_and_tolerates_an_empty_ledger() -> None:
    engine, factory = await _factory()
    try:
        async with factory() as session:
            empty = await affiliate_report(session, "30d", now=NOW)
            assert empty["total"] == 0 and empty["previous_total"] == 0
            assert empty["change"] is None
            assert empty["by_partner"] == [] and empty["top_sub_ids"] == []
            session.add_all(
                [click(destination_id=f"city-{index}") for index in range(LIMIT + 5)]
            )
            await session.commit()
        async with factory() as session:
            report = await affiliate_report(session, "30d", now=NOW)
    finally:
        await engine.dispose()
    assert len(report["by_destination"]) == LIMIT
    assert report["total"] == LIMIT + 5


@pytest.mark.asyncio
async def test_report_route_requires_an_administrator_and_is_never_cached() -> None:
    engine, factory = await _factory()

    async def database():
        async with factory() as session:
            yield session

    async def authenticate(x_test_role: str | None = Header(default=None)):
        if not x_test_role:
            raise AppError(401, "authentication_required", "Sign in")
        return User(id=uuid4(), email="report@example.test", is_admin=x_test_role == "admin")

    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)
    app.include_router(admin_router)
    app.dependency_overrides[get_session] = database
    app.dependency_overrides[current_user] = authenticate
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            assert (await client.get("/admin/analytics/affiliates")).status_code == 401
            member = await client.get(
                "/admin/analytics/affiliates", headers={"X-Test-Role": "member"}
            )
            assert member.status_code == 403
            response = await client.get(
                "/admin/analytics/affiliates?range=7d", headers={"X-Test-Role": "admin"}
            )
            assert response.status_code == 200
            assert response.headers["Cache-Control"] == "no-store"
            assert response.json()["range"] == "7d"
            assert (
                await client.get(
                    "/admin/analytics/affiliates?range=forever",
                    headers={"X-Test-Role": "admin"},
                )
            ).status_code == 422
    finally:
        await engine.dispose()
