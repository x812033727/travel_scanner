import asyncio
import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.db import SessionFactory, engine
from app.infra import get_redis
from app.main import app
from app.models import FlightOfferRecord, PriceAlert, SearchRequest, TripPlan, User

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL and Redis services",
)


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    yield
    await engine.dispose()
    await get_redis().aclose()
    get_redis.cache_clear()


async def register(client: AsyncClient, prefix: str) -> tuple[str, UUID]:
    email = f"{prefix}-{uuid4()}@example.com"
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "integration-password-123"},
    )
    assert response.status_code == 201
    async with SessionFactory() as session:
        user = await session.scalar(select(User).where(User.email == email))
        assert user is not None
        user_id = user.id
    return response.json()["access_token"], user_id


@pytest.mark.asyncio(loop_scope="module")
async def test_alert_ownership_duplicate_update_delete_and_currency() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        token, user_id = await register(client, "alert-owner")
        other_token, _ = await register(client, "alert-other")
        public_offer_id = uuid4()
        now = datetime.now(UTC)
        async with SessionFactory() as session:
            search = SearchRequest(
                user_id=user_id,
                status="completed",
                progress=100,
                operation="full_trip_optimization",
                request_json={},
            )
            session.add(search)
            await session.flush()
            session.add(
                FlightOfferRecord(
                    search_id=search.id,
                    provider="fixture",
                    provider_offer_id=f"fixture-{uuid4()}",
                    public_offer_id=public_offer_id,
                    data={
                        "id": str(public_offer_id),
                        "marketing_airline": "測試航空",
                        "origin": "TPE",
                        "destination": "NRT",
                        "source_mode": "mock",
                        "retrieved_at": now.isoformat(),
                    },
                    total_price=Decimal("52000"),
                    currency="JPY",
                    expires_at=now + timedelta(minutes=5),
                )
            )
            await session.commit()

        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "resource_type": "flight",
            "resource_id": str(public_offer_id),
            "target_price": 50000,
        }
        created = await client.post("/api/v1/alerts", headers=headers, json=payload)
        assert created.status_code == 201
        assert created.json()["title"] == "測試航空"
        assert created.json()["subtitle"] == "TPE → NRT"
        assert created.json()["currency"] == "JPY"
        assert created.json()["current_price"] == "52000.00"
        duplicate = await client.post("/api/v1/alerts", headers=headers, json=payload)
        assert duplicate.status_code == 409
        assert duplicate.json()["code"] == "alert_exists"
        isolated = await client.post(
            "/api/v1/alerts",
            headers={"Authorization": f"Bearer {other_token}"},
            json=payload,
        )
        assert isolated.status_code == 404
        assert isolated.json()["code"] == "alert_resource_not_found"

        alert_id = created.json()["id"]
        patched = await client.patch(
            f"/api/v1/alerts/{alert_id}",
            headers=headers,
            json={"target_price": None, "active": False},
        )
        assert patched.status_code == 200
        assert patched.json()["target_price"] is None
        assert patched.json()["active"] is False
        other_read = await client.get(
            f"/api/v1/alerts/{alert_id}",
            headers={"Authorization": f"Bearer {other_token}"},
        )
        assert other_read.status_code == 404
        deleted = await client.delete(f"/api/v1/alerts/{alert_id}", headers=headers)
        assert deleted.status_code == 204
        assert (await client.get(f"/api/v1/alerts/{alert_id}", headers=headers)).status_code == 404


@pytest.mark.asyncio(loop_scope="module")
async def test_concurrent_alert_creation_is_idempotently_rejected() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        token, user_id = await register(client, "alert-concurrent")
        trip_id = uuid4()
        async with SessionFactory() as session:
            session.add(
                TripPlan(
                    id=trip_id,
                    user_id=user_id,
                    name="東京價格追蹤",
                    mode="balanced",
                    total_price=Decimal("38000"),
                    currency="TWD",
                    data={},
                )
            )
            await session.commit()

    headers = {"Authorization": f"Bearer {token}"}
    payload = {"resource_type": "trip", "resource_id": str(trip_id), "target_price": 35000}

    async def create_once() -> int:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            return (await client.post("/api/v1/alerts", headers=headers, json=payload)).status_code

    statuses = await asyncio.gather(create_once(), create_once())
    assert sorted(statuses) == [201, 409]
    async with SessionFactory() as session:
        alerts = list(
            (
                await session.scalars(
                    select(PriceAlert).where(
                        PriceAlert.user_id == user_id,
                        PriceAlert.resource_type == "trip",
                        PriceAlert.resource_id == trip_id,
                    )
                )
            ).all()
        )
        assert len(alerts) == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_two_users_can_save_the_same_deterministic_itinerary() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        first_token, first_user_id = await register(client, "trip-owner-first")
        second_token, second_user_id = await register(client, "trip-owner-second")
        plan_id = uuid4()
        source_item_id = uuid4()
        result_json = {
            "plans": [
                {
                    "id": str(plan_id),
                    "mode": "balanced",
                    "title": "整體最佳",
                    "total_cost": {"total_cost": "32000"},
                    "itinerary": [
                        {
                            "date": "2026-11-10",
                            "label": "抵達",
                            "items": [
                                {
                                    "id": str(source_item_id),
                                    "item_type": "custom",
                                    "day_date": "2026-11-10",
                                    "position": 0,
                                    "title": "抵達東京",
                                    "locked": True,
                                    "is_estimated": False,
                                    "data": {},
                                }
                            ],
                        }
                    ],
                }
            ]
        }
        async with SessionFactory() as session:
            searches = [
                SearchRequest(
                    user_id=user_id,
                    status="completed",
                    progress=100,
                    operation="full_trip_optimization",
                    request_json={},
                    result_json=result_json,
                )
                for user_id in (first_user_id, second_user_id)
            ]
            session.add_all(searches)
            await session.commit()
            for search in searches:
                await session.refresh(search)

        saved_trips = []
        for index, (token, search) in enumerate(
            zip((first_token, second_token), searches, strict=True), start=1
        ):
            response = await client.post(
                "/api/v1/trips",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "search_id": str(search.id),
                    "plan_id": str(plan_id),
                    "name": f"東京測試旅程 {index}",
                },
            )
            assert response.status_code == 201
            saved_trips.append(response.json())

        first_item_id = saved_trips[0]["items"][0]["id"]
        second_item_id = saved_trips[1]["items"][0]["id"]
        assert first_item_id != second_item_id
        assert first_item_id != str(source_item_id)
        assert second_item_id != str(source_item_id)
