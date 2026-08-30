import asyncio
import os
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.db import SessionFactory
from app.main import app
from app.models import SearchRequest, User

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL and Redis services",
)


@pytest.mark.asyncio
async def test_registration_and_concurrent_idempotent_charge() -> None:
    email = f"integration-{uuid4()}@example.com"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        registered = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "integration-password-123"},
        )
        assert registered.status_code == 201
        token = registered.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "Idempotency-Key": f"integration-{uuid4()}",
        }
        payload = {
            "trip_type": "round_trip",
            "origin": "TPE",
            "destination": "NRT",
            "departure_date": "2026-11-10",
            "return_date": "2026-11-15",
            "travelers": {"adults": 2, "children": 0},
            "modules": ["flight", "hotel"],
            "preferences": {},
        }
        first, replay = await asyncio.gather(
            client.post("/api/v1/searches", json=payload, headers=headers),
            client.post("/api/v1/searches", json=payload, headers=headers),
        )
        assert first.status_code == replay.status_code == 202
        assert first.json()["search_id"] == replay.json()["search_id"]
        usage = await client.get("/api/v1/usage", headers={"Authorization": f"Bearer {token}"})
        assert usage.status_code == 200
        assert usage.json()["credits_remaining"] == 15


@pytest.mark.asyncio
async def test_trip_edit_share_and_revoke_flow() -> None:
    email = f"trip-integration-{uuid4()}@example.com"
    plan_id = uuid4()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        registered = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "integration-password-123"},
        )
        token = registered.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        async with SessionFactory() as session:
            user = await session.scalar(select(User).where(User.email == email))
            assert user is not None
            search = SearchRequest(
                user_id=user.id,
                status="completed",
                progress=100,
                operation="full_trip_optimization",
                request_json={},
                result_json={
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
                                            "id": str(uuid4()),
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
                },
            )
            session.add(search)
            await session.commit()
            await session.refresh(search)

        saved = await client.post(
            "/api/v1/trips",
            headers=headers,
            json={"search_id": str(search.id), "plan_id": str(plan_id), "name": "東京測試旅程"},
        )
        assert saved.status_code == 201
        trip = saved.json()
        update = await client.put(
            f"/api/v1/trips/{trip['id']}/itinerary",
            headers=headers,
            json={"version": 1, "items": trip["items"]},
        )
        assert update.status_code == 200
        assert update.json()["version"] == 2
        stale = await client.put(
            f"/api/v1/trips/{trip['id']}/itinerary",
            headers=headers,
            json={"version": 1, "items": trip["items"]},
        )
        assert stale.status_code == 409
        shared = await client.post(f"/api/v1/trips/{trip['id']}/share", headers=headers)
        assert shared.status_code == 200
        token_value = shared.json()["token"]
        public = await client.get(f"/api/v1/shared-trips/{token_value}")
        assert public.status_code == 200
        assert "user_id" not in public.json()
        revoked = await client.delete(f"/api/v1/trips/{trip['id']}/share", headers=headers)
        assert revoked.status_code == 204
        assert (await client.get(f"/api/v1/shared-trips/{token_value}")).status_code == 404
