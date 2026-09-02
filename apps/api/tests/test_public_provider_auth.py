from unittest.mock import AsyncMock
from uuid import uuid4

import fakeredis.aioredis
import httpx
import pytest
from httpx import ASGITransport, AsyncClient
from starlette.requests import Request

from app.config import Settings
from app.hotspots import router as hotspots_router
from app.main import app
from app.models import User
from app.places import router as places_router
from app.restaurants import router as restaurants_router
from app.restaurants.router import RestaurantSearchRequest


def make_user() -> User:
    return User(
        id=uuid4(),
        email="member@example.com",
        password_hash="not-used",
        auth_version=1,
    )


@pytest.mark.asyncio
async def test_anonymous_provider_endpoints_stop_before_external_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    restaurant_search = AsyncMock()
    photo_usage = AsyncMock()
    restaurant_limiter = AsyncMock()
    photo_limiter = AsyncMock()
    monkeypatch.setattr(restaurants_router, "search_restaurants", restaurant_search)
    monkeypatch.setattr(restaurants_router, "enforce_named_rate_limit", restaurant_limiter)
    monkeypatch.setattr(places_router, "record_google_maps_request", photo_usage)
    monkeypatch.setattr(places_router, "enforce_named_rate_limit", photo_limiter)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        restaurant_response = await client.post(
            f"/api/v1/hotspots/{uuid4()}/restaurant-searches",
            headers={"Idempotency-Key": "anonymous-request"},
            json={"radius_km": 5},
        )
        photo_response = await client.get(
            "/api/v1/places/photo",
            params={"name": "places/ChIJ-test/photos/AZm-test"},
        )

    assert restaurant_response.status_code == 401
    assert restaurant_response.json()["code"] == "authentication_required"
    assert photo_response.status_code == 401
    assert photo_response.json()["code"] == "authentication_required"
    restaurant_search.assert_not_awaited()
    restaurant_limiter.assert_not_awaited()
    photo_usage.assert_not_awaited()
    photo_limiter.assert_not_awaited()


@pytest.mark.asyncio
async def test_anonymous_hotspot_content_stops_before_protected_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    place_payload = AsyncMock()
    guides = AsyncMock()
    guide_open = AsyncMock()
    guide_limiter = AsyncMock()
    monkeypatch.setattr(hotspots_router, "place_detail_payload", place_payload)
    monkeypatch.setattr(hotspots_router, "list_guides", guides)
    monkeypatch.setattr(hotspots_router, "resolve_guide_open", guide_open)
    monkeypatch.setattr(hotspots_router, "enforce_named_rate_limit", guide_limiter)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        hotspot_id = uuid4()
        place_response = await client.get(f"/api/v1/hotspots/{hotspot_id}/place")
        guides_response = await client.get(f"/api/v1/hotspots/{hotspot_id}/guides")
        source_response = await client.get(f"/api/v1/hotspots/{hotspot_id}/source")
        guide_response = await client.post(f"/api/v1/hotspots/guides/{uuid4()}/open")

    for response in (place_response, guides_response, source_response, guide_response):
        assert response.status_code == 401
        assert response.json()["code"] == "authentication_required"
    place_payload.assert_not_awaited()
    guides.assert_not_awaited()
    guide_open.assert_not_awaited()
    guide_limiter.assert_not_awaited()


@pytest.mark.asyncio
async def test_public_rankings_hide_source_urls(monkeypatch: pytest.MonkeyPatch) -> None:
    rankings = AsyncMock(return_value={"items": [{"id": "one", "source_urls": ["https://example.com"]}]})
    monkeypatch.setattr(hotspots_router, "list_rankings", rankings)
    monkeypatch.setattr(
        hotspots_router,
        "load_runtime_settings",
        AsyncMock(return_value=Settings()),
    )

    result = await hotspots_router.hotspot_rankings(AsyncMock(), "zh-TW")

    assert result["items"] == [{"id": "one", "has_source": True}]


@pytest.mark.asyncio
async def test_restaurant_search_rate_limit_is_scoped_to_user(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user = make_user()
    limiter = AsyncMock()
    search = AsyncMock(return_value={"items": []})
    monkeypatch.setattr(restaurants_router, "enforce_named_rate_limit", limiter)
    monkeypatch.setattr(
        restaurants_router,
        "load_runtime_settings",
        AsyncMock(return_value=Settings()),
    )
    monkeypatch.setattr(restaurants_router, "search_restaurants", search)

    result = await restaurants_router.restaurant_search(
        uuid4(),
        RestaurantSearchRequest(),
        user,
        AsyncMock(),
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        "zh-TW",
        "authenticated-request",
    )

    assert result == {"items": []}
    limiter.assert_awaited_once_with(
        "hotspot-restaurant-search-user",
        str(user.id),
        limit=30,
        window_seconds=3_600,
    )
    search.assert_awaited_once()


class PhotoClient:
    def __init__(self) -> None:
        self.calls = 0

    async def __aenter__(self) -> "PhotoClient":
        return self

    async def __aexit__(self, *_args: object) -> None:
        return None

    async def get(self, *_args: object, **_kwargs: object) -> httpx.Response:
        self.calls += 1
        return httpx.Response(
            200,
            json={"photoUri": "https://lh3.googleusercontent.com/photo"},
        )


@pytest.mark.asyncio
async def test_authenticated_photo_miss_calls_google_once_then_uses_cache(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    provider = PhotoClient()
    usage = AsyncMock()
    limiter = AsyncMock()
    monkeypatch.setattr(places_router, "get_redis", lambda: redis)
    monkeypatch.setattr(
        places_router,
        "load_runtime_settings",
        AsyncMock(return_value=Settings(google_maps_api_key="key")),
    )
    monkeypatch.setattr(places_router.httpx, "AsyncClient", lambda **_kwargs: provider)
    monkeypatch.setattr(places_router, "record_google_maps_request", usage)
    monkeypatch.setattr(places_router, "enforce_named_rate_limit", limiter)
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/api/v1/places/photo",
            "headers": [],
            "client": ("127.0.0.1", 1234),
        }
    )
    args = (
        "places/ChIJ-test/photos/AZm-test",
        request,
        AsyncMock(),
        make_user(),
    )

    first = await places_router.place_photo(*args)
    second = await places_router.place_photo(*args)

    assert first.headers["location"] == "https://lh3.googleusercontent.com/photo"
    assert second.headers["location"] == first.headers["location"]
    assert provider.calls == 1
    usage.assert_awaited_once_with(redis, "places_photo")
    limiter.assert_awaited_once()
