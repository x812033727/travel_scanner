import asyncio
import json
import math
from dataclasses import replace
from datetime import UTC, datetime

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.models import RestaurantPlace
from app.providers.usage_meter import (
    google_maps_usage_snapshot,
    record_google_maps_request,
    reserve_google_maps_request,
)
from app.restaurants.google import (
    DINING_PLACE_TYPES,
    GoogleRestaurantProvider,
    RestaurantSnapshot,
)
from app.restaurants.service import (
    RESTAURANT_LOCATION_CACHE_PREFIX,
    _sort_items,
    build_place_maps_url,
    cache_restaurant_location,
    haversine_km,
    recommendation_score,
    split_circle,
)


@pytest.mark.asyncio
async def test_nearby_restaurants_requests_all_dining_types_and_live_fields() -> None:
    body: dict[str, object] = {}
    field_mask = ""

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal field_mask
        body.update(json.loads(request.content))
        field_mask = request.headers["X-Goog-FieldMask"]
        return httpx.Response(
            200,
            json={
                "places": [
                    {
                        "id": "ChIJ-food",
                        "displayName": {"text": "Okonomiyaki Example"},
                        "formattedAddress": "Hiroshima, Japan",
                        "location": {"latitude": 34.397, "longitude": 132.455},
                        "rating": 4.6,
                        "userRatingCount": 2345,
                        "regularOpeningHours": {"weekdayDescriptions": ["Mon: 11:00-22:00"]},
                        "currentOpeningHours": {"openNow": True},
                        "websiteUri": "https://restaurant.example/",
                        "googleMapsUri": "https://maps.google.com/?cid=1",
                        "primaryType": "japanese_restaurant",
                        "businessStatus": "OPERATIONAL",
                    }
                ]
            },
        )

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = GoogleRestaurantProvider(
        redis,
        Settings(google_maps_api_key="key"),
        locale="ja",
        client=client,
    )
    results = await provider.nearby(34.3955, 132.451, 5_000)

    assert body["includedTypes"] == list(DINING_PLACE_TYPES)
    assert body["rankPreference"] == "POPULARITY"
    assert body["languageCode"] == "ja"
    assert body["locationRestriction"] == {
        "circle": {
            "center": {"latitude": 34.3955, "longitude": 132.451},
            "radius": 5000.0,
        }
    }
    assert "places.rating" in field_mask
    assert "places.userRatingCount" in field_mask
    assert results[0].qualified
    assert results[0].rating == 4.6
    assert results[0].review_count == 2345
    assert "plusCode" not in field_mask
    assert not replace(results[0], rating=3.79).qualified
    assert not replace(results[0], review_count=999).qualified
    await client.aclose()
    await redis.aclose()


@pytest.mark.asyncio
async def test_aggregate_filters_rating_and_returns_only_place_ids() -> None:
    body: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers.get("X-Goog-FieldMask") is None
        body.update(json.loads(request.content))
        return httpx.Response(
            200,
            json={
                "count": "2",
                "placeInsights": [
                    {"place": "places/ChIJ-one"},
                    {"place": "places/ChIJ-two"},
                ],
            },
        )

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = GoogleRestaurantProvider(redis, Settings(google_maps_api_key="key"), client=client)
    result = await provider.aggregate(34.3955, 132.451, 10_000)

    request_filter = body["filter"]
    assert isinstance(request_filter, dict)
    assert request_filter["ratingFilter"] == {"minRating": 3.8, "maxRating": 5.0}
    assert request_filter["operatingStatus"] == ["OPERATING_STATUS_OPERATIONAL"]
    assert result.count == 2
    assert result.place_ids == ("ChIJ-one", "ChIJ-two")
    usage = await google_maps_usage_snapshot(redis)
    aggregate = next(item for item in usage.sku_usage if item.sku == "places_aggregate")
    assert aggregate.used == 1
    assert aggregate.free_limit == 5_000
    await client.aclose()
    await redis.aclose()


@pytest.mark.asyncio
async def test_restaurant_budget_reservation_is_atomic_and_fails_closed() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    observed_at = datetime(2026, 9, 1, 12, tzinfo=UTC)
    assert await reserve_google_maps_request(redis, "places_nearby_restaurants", 2, now=observed_at)
    assert await reserve_google_maps_request(redis, "places_nearby_restaurants", 2, now=observed_at)
    assert not await reserve_google_maps_request(
        redis, "places_nearby_restaurants", 2, now=observed_at
    )
    snapshot = await google_maps_usage_snapshot(redis, now=observed_at)
    nearby = next(item for item in snapshot.sku_usage if item.sku == "nearby_search_enterprise")
    assert nearby.used == 2
    await redis.aclose()


@pytest.mark.asyncio
async def test_concurrent_restaurant_budget_cannot_exceed_limit() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    observed_at = datetime(2026, 9, 1, 12, tzinfo=UTC)
    results = await asyncio.gather(
        *(
            reserve_google_maps_request(redis, "places_aggregate_restaurants", 3, now=observed_at)
            for _ in range(10)
        )
    )
    assert sum(results) == 3
    snapshot = await google_maps_usage_snapshot(redis, now=observed_at)
    assert snapshot.breakdown["places_aggregate_restaurants"] == 3
    await redis.aclose()


@pytest.mark.asyncio
async def test_restaurant_details_budget_counts_the_shared_place_details_sku() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    observed_at = datetime(2026, 9, 1, 12, tzinfo=UTC)
    await record_google_maps_request(redis, "place_details", now=observed_at)

    assert await reserve_google_maps_request(
        redis,
        "place_details_restaurant",
        3,
        shared_operations=("place_details", "place_details_restaurant"),
        shared_monthly_budget=2,
        now=observed_at,
    )
    assert not await reserve_google_maps_request(
        redis,
        "place_details_restaurant",
        3,
        shared_operations=("place_details", "place_details_restaurant"),
        shared_monthly_budget=2,
        now=observed_at,
    )
    snapshot = await google_maps_usage_snapshot(redis, now=observed_at)
    details = next(item for item in snapshot.sku_usage if item.sku == "place_details_enterprise")
    assert details.used == 2
    await redis.aclose()


@pytest.mark.asyncio
async def test_restaurant_coordinates_use_an_enforced_30_day_redis_ttl() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    observed_at = datetime(2026, 9, 2, 12, tzinfo=UTC)
    snapshot = RestaurantSnapshot(
        place_id="ChIJ-location-cache",
        name="Must not be cached",
        address="Must not be cached",
        latitude=34.397,
        longitude=132.455,
        rating=4.6,
        review_count=2_345,
        opening_hours=("Must not be cached",),
        open_now=True,
        official_website_url="https://restaurant.example/",
        google_maps_url="https://maps.example/",
        primary_type="japanese_restaurant",
        business_status="OPERATIONAL",
    )

    await cache_restaurant_location(redis, snapshot, Settings(), observed_at)

    key = f"{RESTAURANT_LOCATION_CACHE_PREFIX}:{snapshot.place_id}"
    cached = json.loads(await redis.get(key))
    assert cached == {
        "latitude": 34.397,
        "longitude": 132.455,
        "fetched_at": observed_at.isoformat(),
    }
    ttl = await redis.ttl(key)
    assert 0 < ttl <= 30 * 86_400
    await redis.aclose()


def test_rating_threshold_distance_and_transparent_recommendation_sort() -> None:
    assert recommendation_score(5.0, 1_000) == 4.5
    assert recommendation_score(4.7, 100_000) > recommendation_score(4.9, 1_000)
    assert math.isclose(
        haversine_km(34.3955, 132.451, 34.397, 132.455),
        0.405,
        abs_tol=0.02,
    )
    rows = [
        {"rating": 4.9, "review_count": 1_000, "distance_km": 0.5, "recommendation_score": 4.45},
        {"rating": 4.7, "review_count": 100_000, "distance_km": 1.0, "recommendation_score": 4.69},
    ]
    assert _sort_items(rows, "recommended")[0]["review_count"] == 100_000
    assert _sort_items(rows, "rating")[0]["rating"] == 4.9
    assert _sort_items(rows, "reviews")[0]["review_count"] == 100_000
    assert _sort_items(rows, "distance")[0]["distance_km"] == 0.5


def test_maps_url_is_generated_from_place_id_without_provider_content() -> None:
    assert build_place_maps_url("ChIJ-food") == (
        "https://www.google.com/maps/search/"
        "?api=1&query=ChIJ-food&query_place_id=ChIJ-food"
    )


def test_adaptive_circle_split_covers_parent_boundary_samples() -> None:
    children = split_circle(0.0, 0.0, 10_000)
    assert len(children) == 7
    assert {child[2] for child in children} == {5_000}
    for angle in range(0, 360, 5):
        latitude = math.sin(math.radians(angle)) * 10_000 / 111_320
        longitude = math.cos(math.radians(angle)) * 10_000 / 111_320
        assert any(
            haversine_km(latitude, longitude, child_lat, child_lon) <= radius / 1_000 + 0.01
            for child_lat, child_lon, radius in children
        )


def test_restaurant_identity_table_contains_no_google_display_fields() -> None:
    columns = set(RestaurantPlace.__table__.columns.keys())
    assert "google_place_id" in columns
    assert "generated_maps_url" in columns
    assert columns.isdisjoint(
        {
            "name",
            "rating",
            "review_count",
            "opening_hours",
            "official_website_url",
            "latitude",
            "longitude",
            "google_maps_url",
            "recommendation_score",
        }
    )
