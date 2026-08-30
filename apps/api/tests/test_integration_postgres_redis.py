import asyncio
import os
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

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
