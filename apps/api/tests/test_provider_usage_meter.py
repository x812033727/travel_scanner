from datetime import UTC, datetime
from uuid import uuid4

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.places.google import GoogleTravelService
from app.providers.usage_meter import (
    google_maps_usage_snapshot,
    record_google_maps_request,
)
from app.trips.routing import GoogleRouteProvider, RoutePoint


@pytest.mark.asyncio
async def test_google_maps_usage_counts_requests_by_month_and_operation() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    observed_at = datetime(2026, 8, 31, 12, 0, tzinfo=UTC)
    await record_google_maps_request(redis, "places_autocomplete", now=observed_at)
    await record_google_maps_request(redis, "places_autocomplete", now=observed_at)
    await record_google_maps_request(redis, "routes", now=observed_at)

    snapshot = await google_maps_usage_snapshot(redis, 10_000, now=observed_at)

    assert snapshot.available
    assert snapshot.period == "2026-08"
    assert snapshot.period_start.isoformat() == "2026-08-01"
    assert snapshot.period_end.isoformat() == "2026-08-31"
    assert snapshot.used == 3
    assert snapshot.remaining == 9_997
    assert snapshot.percentage == 0.0
    assert snapshot.breakdown["places_autocomplete"] == 2
    assert snapshot.breakdown["routes"] == 1
    assert snapshot.breakdown["places_photo"] == 0
    assert snapshot.tracking_started_at == observed_at
    assert await redis.ttl("provider-usage:google_maps:2026-08") > 0
    await redis.aclose()


@pytest.mark.asyncio
async def test_google_maps_usage_starts_a_new_counter_each_month() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    await record_google_maps_request(
        redis,
        "place_details",
        now=datetime(2026, 8, 31, 23, 59, tzinfo=UTC),
    )
    september = datetime(2026, 9, 1, 0, 0, tzinfo=UTC)

    snapshot = await google_maps_usage_snapshot(redis, 10_000, now=september)

    assert snapshot.period == "2026-09"
    assert snapshot.used == 0
    assert snapshot.remaining == 10_000
    assert snapshot.tracking_started_at is None
    await redis.aclose()


@pytest.mark.asyncio
async def test_google_maps_usage_can_exceed_the_reference_limit() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    observed_at = datetime(2026, 8, 1, tzinfo=UTC)
    for _ in range(3):
        await record_google_maps_request(redis, "routes", now=observed_at)

    snapshot = await google_maps_usage_snapshot(redis, 2, now=observed_at)

    assert snapshot.used == 3
    assert snapshot.remaining == 0
    assert snapshot.percentage == 150.0
    await redis.aclose()


@pytest.mark.asyncio
async def test_google_clients_record_successful_and_rejected_outbound_requests() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith(":autocomplete"):
            return httpx.Response(403, json={"error": {"status": "PERMISSION_DENIED"}})
        return httpx.Response(200, json={})

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    settings = Settings(google_maps_api_key="key")
    places = GoogleTravelService(redis, settings, client)
    await places.autocomplete("東京")
    await places.place_details("ChIJ-test")
    routes = GoogleRouteProvider(settings, client, redis)
    await routes.probe(
        RoutePoint(item_id=uuid4(), name="東京車站", latitude=35.6812, longitude=139.7671),
        RoutePoint(item_id=uuid4(), name="淺草寺", latitude=35.7148, longitude=139.7967),
    )

    snapshot = await google_maps_usage_snapshot(redis, 10_000)

    assert snapshot.used == 3
    assert snapshot.breakdown["places_autocomplete"] == 1
    assert snapshot.breakdown["place_details"] == 1
    assert snapshot.breakdown["routes"] == 1
    await client.aclose()
    await redis.aclose()
