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
    record_youtube_request,
    youtube_usage_snapshot,
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
    assert snapshot.free_limit == 38_000  # +5,000 for the Pro-tier text_search_pro SKU
    assert snapshot.free_usage == 3
    assert snapshot.free_remaining == 37_997
    assert snapshot.billable_overage == 0
    assert snapshot.percentage == 0.0
    assert snapshot.breakdown["places_autocomplete"] == 2
    assert snapshot.breakdown["routes"] == 1
    assert snapshot.breakdown["places_photo"] == 0
    assert snapshot.breakdown["places_text_search_locate"] == 0
    assert snapshot.breakdown["weather_current"] == 0
    assert snapshot.breakdown["weather_daily_forecast"] == 0
    autocomplete = next(item for item in snapshot.sku_usage if item.sku == "autocomplete_requests")
    routes = next(item for item in snapshot.sku_usage if item.sku == "compute_routes_essentials")
    assert autocomplete.used == 2
    assert autocomplete.free_limit == 10_000
    assert routes.used == 1
    assert len(snapshot.monthly_history) == 6
    assert snapshot.monthly_history[1].period == "2026-07"
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
    before_pacific_reset = datetime(2026, 9, 1, 6, 59, tzinfo=UTC)
    september = datetime(2026, 9, 1, 7, 0, tzinfo=UTC)

    august_snapshot = await google_maps_usage_snapshot(redis, now=before_pacific_reset)
    snapshot = await google_maps_usage_snapshot(redis, now=september)

    assert august_snapshot.period == "2026-08"
    assert august_snapshot.used == 1
    assert snapshot.period == "2026-09"
    assert snapshot.used == 0
    assert snapshot.free_remaining == 38_000
    assert snapshot.tracking_started_at is None
    await redis.aclose()


@pytest.mark.asyncio
async def test_google_maps_usage_reports_overage_per_sku() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    observed_at = datetime(2026, 8, 1, 12, tzinfo=UTC)
    for _ in range(3):
        await record_google_maps_request(redis, "place_details", now=observed_at)

    snapshot = await google_maps_usage_snapshot(
        redis,
        enterprise_free_limit=2,
        now=observed_at,
    )

    assert snapshot.used == 3
    assert snapshot.billable_overage == 1
    details = next(item for item in snapshot.sku_usage if item.sku == "place_details_enterprise")
    assert details.free_usage == 2
    assert details.free_remaining == 0
    assert details.billable_overage == 1
    assert details.percentage == 150.0
    await redis.aclose()


@pytest.mark.asyncio
async def test_google_maps_usage_returns_recent_month_history() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    await record_google_maps_request(
        redis,
        "weather_current",
        now=datetime(2026, 7, 20, 12, tzinfo=UTC),
    )
    await record_google_maps_request(
        redis,
        "weather_daily_forecast",
        now=datetime(2026, 8, 20, 12, tzinfo=UTC),
    )

    snapshot = await google_maps_usage_snapshot(
        redis,
        history_months=2,
        now=datetime(2026, 8, 31, 12, tzinfo=UTC),
    )

    assert [month.period for month in snapshot.monthly_history] == ["2026-08", "2026-07"]
    assert [month.used for month in snapshot.monthly_history] == [1, 1]
    weather = next(item for item in snapshot.sku_usage if item.sku == "weather_usage")
    assert weather.used == 1
    assert weather.operations == ("weather_current", "weather_daily_forecast")
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


@pytest.mark.asyncio
async def test_youtube_usage_counts_daily_quota_buckets() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    observed_at = datetime(2026, 9, 1, 12, tzinfo=UTC)
    await record_youtube_request(redis, "search_list", now=observed_at)
    await record_youtube_request(redis, "search_list", now=observed_at)
    await record_youtube_request(redis, "videos_list", now=observed_at)

    snapshot = await youtube_usage_snapshot(
        redis,
        search_daily_free_limit=2,
        core_daily_free_limit=10,
        now=observed_at,
    )

    assert snapshot.available
    assert snapshot.period_kind == "day"
    assert snapshot.period == "2026-09-01"
    assert snapshot.period_start == snapshot.period_end
    assert snapshot.used == 3
    assert snapshot.breakdown == {"search_list": 2, "videos_list": 1}
    search = next(item for item in snapshot.sku_usage if item.sku == "search_queries")
    core = next(item for item in snapshot.sku_usage if item.sku == "core_api_units")
    assert search.used == 2
    assert search.free_remaining == 0
    assert core.used == 1
    assert core.free_remaining == 9
    assert await redis.ttl("provider-usage:youtube_guides:2026-09-01") > 0
    await redis.aclose()


@pytest.mark.asyncio
async def test_youtube_usage_resets_at_pacific_midnight() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    await record_youtube_request(
        redis,
        "search_list",
        now=datetime(2026, 9, 1, 6, 59, tzinfo=UTC),
    )

    august = await youtube_usage_snapshot(redis, now=datetime(2026, 9, 1, 6, 59, tzinfo=UTC))
    september = await youtube_usage_snapshot(redis, now=datetime(2026, 9, 1, 7, 0, tzinfo=UTC))

    assert august.period == "2026-08-31"
    assert august.used == 1
    assert september.period == "2026-09-01"
    assert september.used == 0
    assert september.free_remaining == 10_100
    await redis.aclose()
