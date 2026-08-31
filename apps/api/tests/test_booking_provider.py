import json
from datetime import date
from typing import Any

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.providers.booking import BookingHotelProvider
from app.providers.registry import (
    build_module_provider_candidates,
    hotel_provider_status,
    provider_status,
)
from app.search.schemas import SearchCreate, SearchModule, Travelers


def query() -> SearchCreate:
    return SearchCreate(
        origin="TPE",
        destination="NRT",
        departure_date=date(2026, 11, 10),
        return_date=date(2026, 11, 12),
        travelers=Travelers(adults=2, children=1, children_ages=[8], rooms=1),
        modules=[SearchModule.HOTEL],
    )


def booking_settings(**updates: Any) -> Settings:
    return Settings.model_validate(
        {
            "booking_demand_enabled": True,
            "booking_demand_affiliate_id": "affiliate-123",
            "booking_demand_api_token": "booking-secret",
            "booking_demand_env": "sandbox",
            **updates,
        }
    )


@pytest.mark.asyncio
async def test_booking_search_authenticates_maps_location_and_normalizes_offer() -> None:
    requests: list[tuple[str, dict[str, object], httpx.Headers]] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        requests.append((request.url.path, payload, request.headers))
        if request.url.path.endswith("/common/locations/cities"):
            return httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": -246227,
                            "name": "Tokyo",
                        }
                    ]
                },
            )
        if request.url.path.endswith("/accommodations/search"):
            return httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": 10004,
                            "currency": "TWD",
                            "url": "https://www.booking.com/hotel/jp/test.html?aid=123",
                            "price": {"base": 8500, "total": 10000},
                            "products": [
                                {
                                    "id": "room-rate-1",
                                    "number_of_adults": 2,
                                    "room": {"zh-tw": "標準雙人房"},
                                    "policies": {
                                        "cancellation": {"type": "free_cancellation"},
                                        "meal_plan": {"plan": "breakfast_included"},
                                    },
                                    "price": {"base": 8500, "total": 10000},
                                }
                            ],
                        }
                    ]
                },
            )
        return httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": 10004,
                        "name": {"zh-tw": "東京測試飯店"},
                        "coordinates": {"latitude": 35.68, "longitude": 139.76},
                        "rating": {"stars": 4},
                        "review_score": {"score": 8.9, "number_of_reviews": 321},
                        "address": {
                            "address_line": "千代田區 1-1",
                            "city": "東京",
                            "postal_code": "100-0001",
                        },
                        "type": "hotel",
                        "facilities": [{"zh-tw": "免費 Wi-Fi"}],
                    }
                ]
            },
        )

    redis = fakeredis.aioredis.FakeRedis()
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    try:
        provider = BookingHotelProvider(redis, booking_settings(), client)
        offers = await provider.search_hotels(query())
    finally:
        await client.aclose()
        await redis.aclose()

    assert [item[0] for item in requests] == [
        "/3.1/common/locations/cities",
        "/3.1/accommodations/search",
        "/3.1/accommodations/details",
    ]
    assert requests[0][1] == {
        "airport": "NRT",
        "languages": ["zh-tw", "en-gb"],
        "rows": 10,
    }
    assert requests[1][1]["guests"] == {
        "number_of_adults": 2,
        "number_of_rooms": 1,
        "children": [8],
    }
    assert requests[1][2]["authorization"] == "Bearer booking-secret"
    assert requests[1][2]["x-affiliate-id"] == "affiliate-123"
    assert len(offers) == 1
    offer = offers[0]
    assert offer.provider == "booking"
    assert offer.hotel_name == "東京測試飯店"
    assert offer.total_price == 10000
    assert offer.taxes == 1500
    assert offer.breakfast_included is True
    assert offer.refundable is True
    assert offer.review_score == 8.9
    assert offer.review_count == 321
    assert offer.booking_url == "https://www.booking.com/hotel/jp/test.html?aid=123"
    assert offer.is_bookable is True


@pytest.mark.asyncio
async def test_booking_location_mapping_is_cached_and_empty_result_is_not_an_error() -> None:
    autocomplete_calls = 0

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal autocomplete_calls
        if request.url.path.endswith("/common/locations/cities"):
            autocomplete_calls += 1
            return httpx.Response(
                200,
                json={"data": [{"id": -246227, "name": "Tokyo"}]},
            )
        return httpx.Response(200, json={"data": []})

    redis = fakeredis.aioredis.FakeRedis()
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    try:
        provider = BookingHotelProvider(redis, booking_settings(), client)
        assert await provider.search_hotels(query()) == []
        assert await provider.search_hotels(query()) == []
    finally:
        await client.aclose()
        await redis.aclose()

    assert autocomplete_calls == 1


@pytest.mark.asyncio
async def test_booking_errors_do_not_expose_token() -> None:
    async def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"errors": [{"message": "invalid token"}]})

    redis = fakeredis.aioredis.FakeRedis()
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    try:
        provider = BookingHotelProvider(redis, booking_settings(), client)
        with pytest.raises(ConnectionError) as error:
            await provider.search_hotels(query())
    finally:
        await client.aclose()
        await redis.aclose()

    assert "booking-secret" not in str(error.value)
    assert "HTTP 401" in str(error.value)


@pytest.mark.asyncio
async def test_auto_provider_priority_and_technical_fallback_candidates() -> None:
    settings = booking_settings(
        skyscanner_api_key="sky-key",
        amadeus_client_id="amadeus-id",
        amadeus_client_secret="amadeus-secret",
        flight_provider_mode="auto",
        hotel_provider_mode="auto",
        travel_provider_mode="amadeus",
    )
    redis = fakeredis.aioredis.FakeRedis()
    try:
        candidates = build_module_provider_candidates(redis, settings)
    finally:
        await redis.aclose()

    assert [provider.name for provider in candidates["flight"]] == [  # type: ignore[attr-defined]
        "skyscanner",
        "amadeus",
    ]
    assert [provider.name for provider in candidates["hotel"]] == [  # type: ignore[attr-defined]
        "booking",
        "amadeus",
    ]
    assert hotel_provider_status(settings).fallback_provider == "amadeus"
    public = provider_status(settings)
    assert public.module_statuses["flight"].selected_provider == "skyscanner"
    assert public.module_statuses["hotel"].selected_provider == "booking"
    assert "booking-secret" not in public.model_dump_json()


def test_auto_hotel_uses_amadeus_until_booking_is_enabled() -> None:
    settings = Settings(
        hotel_provider_mode="auto",
        booking_demand_enabled=False,
        booking_demand_affiliate_id="affiliate-123",
        booking_demand_api_token="booking-secret",
        amadeus_client_id="amadeus-id",
        amadeus_client_secret="amadeus-secret",
    )

    status = hotel_provider_status(settings)

    assert status.selected_provider == "amadeus"
    assert status.available is True
