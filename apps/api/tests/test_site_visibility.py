from collections.abc import AsyncIterator, Iterator

import pytest
from httpx import ASGITransport, AsyncClient

import app.admin.router as admin_router
from app.admin.schemas import SiteVisibility
from app.db import get_session
from app.main import app


@pytest.fixture
def session_override() -> Iterator[None]:
    async def provide_session() -> AsyncIterator[object]:
        yield object()

    app.dependency_overrides[get_session] = provide_session
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_site_visibility_is_public_and_not_cached(
    monkeypatch: pytest.MonkeyPatch,
    session_override: None,
) -> None:
    async def visibility(_session: object) -> SiteVisibility:
        return SiteVisibility(trips_enabled=False, pricing_enabled=False)

    monkeypatch.setattr(admin_router, "effective_site_visibility", visibility)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/runtime/site-visibility")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert response.json() == {
        "hotspots_enabled": True,
        "trips_enabled": False,
        "alerts_enabled": True,
        "flight_status_enabled": True,
        "airline_fares_enabled": True,
        "pricing_enabled": False,
    }
