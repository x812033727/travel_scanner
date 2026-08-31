import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_guest_can_discover_estimated_destinations_without_authentication() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/destinations/discover",
            json={
                "origin": "TPE",
                "destination_countries": ["JP"],
                "travel_window": {"start_date": "2026-11-01", "end_date": "2026-12-20"},
                "trip_length_range": {"min_days": 4, "max_days": 6},
                "travelers": {"adults": 2, "children": 0, "rooms": 1},
                "top_n": 3,
            },
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["source"] == "curated_estimate"
    assert len(payload["recommendations"]) == 3
    assert all(item["country_code"] == "JP" for item in payload["recommendations"])
    assert "即時" in payload["assumptions"][0] or "估算" in payload["assumptions"][0]


@pytest.mark.asyncio
async def test_validation_problem_details_are_localized() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "not-an-email", "password": "short"},
        )
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["code"] == "validation_error"
    assert "Email" in response.json()["detail"]
    assert "密碼" in response.json()["detail"]
    assert response.json()["request_id"]
