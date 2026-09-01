import json

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.problems import AppError
from app.providers.usage_meter import google_maps_usage_snapshot
from app.restaurants.editorial import (
    build_uber_url,
    validate_editorial_url,
    validate_profile_evidence,
)
from app.restaurants.google import GoogleRestaurantProvider
from app.restaurants.imports import extract_place_id, resolve_maps_input

PLACE_ID = "ChIJN1t_tDeuEmsRUsoyG83frY4"
MOVED_PLACE_ID = "ChIJN1t_tDeuEmsRUsoyG83frY5"


def test_extracts_place_id_without_persisting_url_name() -> None:
    url = (
        "https://www.google.com/maps/search/?api=1&query=Example+Restaurant"
        f"&query_place_id={PLACE_ID}"
    )
    assert extract_place_id(PLACE_ID) == PLACE_ID
    assert extract_place_id(url) == PLACE_ID


@pytest.mark.asyncio
async def test_short_maps_url_rejects_redirect_outside_google() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(302, headers={"location": "https://127.0.0.1/private"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(AppError) as raised:
            await resolve_maps_input("https://maps.app.goo.gl/abc", client=client)
    assert raised.value.code == "restaurant_maps_url_host_invalid"


@pytest.mark.asyncio
async def test_ids_only_search_requests_only_ids_and_is_tracked_separately() -> None:
    captured: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["mask"] = request.headers["X-Goog-FieldMask"]
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json={"places": [{"id": PLACE_ID}]})

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = GoogleRestaurantProvider(
            redis,
            Settings(google_maps_api_key="key", restaurant_scan_enabled=False),
            client=client,
        )
        place_ids = await provider.search_ids_only(
            "Example Restaurant",
            latitude=25.03,
            longitude=121.56,
        )
    assert place_ids == (PLACE_ID,)
    assert captured["mask"] == "places.id"
    assert captured["body"] == {
        "textQuery": "Example Restaurant",
        "languageCode": "zh-TW",
        "pageSize": 5,
        "locationBias": {
            "circle": {
                "center": {"latitude": 25.03, "longitude": 121.56},
                "radius": 10000.0,
            }
        },
    }
    usage = await google_maps_usage_snapshot(redis)
    assert usage.breakdown["places_text_search_ids_only"] == 1
    assert all(
        "places_text_search_ids_only" not in sku.operations for sku in usage.sku_usage
    )
    await redis.aclose()


@pytest.mark.asyncio
async def test_identity_refresh_uses_ids_only_and_reports_move() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["X-Goog-FieldMask"] == "id,movedPlaceId"
        return httpx.Response(
            200,
            json={"id": PLACE_ID, "movedPlaceId": MOVED_PLACE_ID},
        )

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = GoogleRestaurantProvider(
            redis,
            Settings(google_maps_api_key="key", restaurant_scan_enabled=False),
            client=client,
        )
        result = await provider.refresh_identity(PLACE_ID)
    assert result.status == "moved"
    assert result.moved_place_id == MOVED_PLACE_ID
    usage = await google_maps_usage_snapshot(redis)
    assert usage.breakdown["place_id_refresh"] == 1
    await redis.aclose()


def test_editorial_fields_require_specific_official_evidence() -> None:
    with pytest.raises(AppError) as raised:
        validate_profile_evidence(
            display_name="Example",
            address=None,
            official_website_url="https://restaurant.example/",
            ride_latitude=None,
            ride_longitude=None,
            sources=[
                {
                    "source_url": "https://tourism.example/dining",
                    "claims": ["display_name"],
                }
            ],
        )
    assert raised.value.code == "restaurant_source_evidence_missing"


def test_google_maps_cannot_be_an_editorial_source_and_uber_uses_owned_coordinates() -> None:
    with pytest.raises(AppError) as raised:
        validate_editorial_url("https://www.google.com/maps/place/example")
    assert raised.value.code == "restaurant_source_provider_owned"
    uber = build_uber_url(25.033, 121.5654, "Example Restaurant")
    assert uber.startswith("https://m.uber.com/ul/?")
    assert "dropoff%5Blatitude%5D=25.033" in uber
    assert "dropoff%5Bnickname%5D=Example+Restaurant" in uber
