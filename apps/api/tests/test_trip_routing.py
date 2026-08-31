from datetime import UTC, datetime, timedelta
from uuid import uuid4

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.trips.routing import (
    GoogleRouteProvider,
    GoogleRoutesProbeResult,
    NavitimeRouteProvider,
    RoutePoint,
    RouteSegment,
    RouteService,
    supported_transit_time,
)


def point(
    name: str,
    latitude: float,
    longitude: float,
    provider_place_id: str | None = None,
) -> RoutePoint:
    return RoutePoint(
        item_id=uuid4(),
        name=name,
        latitude=latitude,
        longitude=longitude,
        provider_place_id=provider_place_id,
    )


@pytest.mark.asyncio
async def test_google_route_normalizes_transit_steps_and_preview_warning() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["x-goog-fieldmask"]
        body = request.read().decode()
        assert '"origin":{"placeId":"google-origin"}' in body
        assert '"destination":{"placeId":"google-destination"}' in body
        return httpx.Response(
            200,
            json={
                "routes": [
                    {
                        "duration": "1500s",
                        "distanceMeters": 9200,
                        "polyline": {"encodedPolyline": "abc"},
                        "travelAdvisory": {"transitFare": {"currencyCode": "JPY", "units": "210"}},
                        "legs": [
                            {
                                "steps": [
                                    {
                                        "travelMode": "TRANSIT",
                                        "staticDuration": "1200s",
                                        "transitDetails": {
                                            "stopDetails": {
                                                "departureStop": {"name": "新宿"},
                                                "arrivalStop": {"name": "淺草"},
                                                "departureTime": "2026-09-05T01:00:00Z",
                                                "arrivalTime": "2026-09-05T01:20:00Z",
                                            },
                                            "headsign": "淺草方向",
                                            "transitLine": {
                                                "name": "銀座線",
                                                "nameShort": "G",
                                                "color": "#f39700",
                                            },
                                            "stopCount": 8,
                                        },
                                    }
                                ]
                            }
                        ],
                    }
                ]
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = GoogleRouteProvider(Settings(google_maps_api_key="key"), client)
    segment = await provider.compute(
        point("新宿", 35.69, 139.70, "google-origin"),
        point("淺草", 35.71, 139.80, "google-destination"),
        datetime.now(UTC) + timedelta(days=150),
        "FEWER_TRANSFERS",
    )
    await client.aclose()
    assert segment is not None
    assert segment.duration_minutes == 25
    assert segment.schedule_mode == "preview"
    assert segment.fare == 210
    assert segment.steps[0].line_short_name == "G"
    assert segment.steps[0].headsign == "淺草方向"
    assert "exit" not in segment.details_available
    assert "origin_place_id=google-origin" in str(segment.maps_url)


@pytest.mark.asyncio
async def test_google_routes_probe_treats_empty_success_as_reachable() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["x-goog-fieldmask"] == "routes.duration"
        assert request.headers["x-goog-api-key"] == "key"
        body = request.read().decode()
        assert '"travelMode":"TRANSIT"' in body
        assert '"placeId"' not in body
        return httpx.Response(200, json={})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = GoogleRouteProvider(Settings(google_maps_api_key="key"), client)
    result = await provider.probe(
        point("東京車站", 35.6812, 139.7671),
        point("淺草寺", 35.7148, 139.7967),
    )
    await client.aclose()
    assert result == GoogleRoutesProbeResult(
        reachable=True,
        route_available=False,
        status_code=200,
    )


@pytest.mark.asyncio
async def test_google_routes_probe_reports_sanitized_api_error() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            403,
            json={
                "error": {
                    "status": "PERMISSION_DENIED",
                    "message": "request contained a secret value",
                }
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = GoogleRouteProvider(Settings(google_maps_api_key="secret-key"), client)
    result = await provider.probe(
        point("東京車站", 35.6812, 139.7671),
        point("淺草寺", 35.7148, 139.7967),
    )
    await client.aclose()
    assert result == GoogleRoutesProbeResult(
        reachable=False,
        route_available=False,
        status_code=403,
        error_code="PERMISSION_DENIED",
    )


@pytest.mark.asyncio
async def test_navitime_route_preserves_sourced_exit_platform_and_car() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "time": 18,
                        "distance": 6400,
                        "nodes": [
                            {
                                "departure": {"name": "表參道", "start_platform": "1"},
                                "arrival": {"name": "澀谷", "gateway": "B3"},
                                "transport": {
                                    "name": "東京地下鐵銀座線",
                                    "destination": {"name": "澀谷"},
                                    "getoff": "前方第 2 節",
                                },
                            }
                        ],
                    }
                ]
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = NavitimeRouteProvider(
        Settings(
            navitime_api_base_url="https://example.test",
            navitime_client_id="client",
            navitime_api_key="key",
        ),
        client,
    )
    segment = await provider.compute(
        point("表參道", 35.66, 139.71),
        point("澀谷", 35.65, 139.70),
        datetime.now(UTC),
        "FEWER_TRANSFERS",
    )
    await client.aclose()
    assert segment is not None
    assert segment.steps[0].platform == "1"
    assert segment.steps[0].exit_name == "B3"
    assert segment.steps[0].recommended_car == "前方第 2 節"
    assert {"platform", "exit", "recommended_car"} <= set(segment.details_available)


class EmptyProvider:
    name = "empty"

    async def compute(self, *_args: object) -> None:
        return None


class WorkingProvider:
    name = "working"

    async def compute(
        self,
        origin: RoutePoint,
        destination: RoutePoint,
        *_args: object,
    ) -> RouteSegment:
        return RouteSegment(
            from_item_id=origin.item_id,
            to_item_id=destination.item_id,
            provider=self.name,
            attribution="test",
            generated_at=datetime.now(UTC),
            duration_minutes=12,
        )


class UnexpectedProvider:
    name = "unexpected"

    async def compute(self, *_args: object) -> None:
        raise AssertionError("fallback provider should not run when Google returned a route")


class CountingProvider:
    name = "counting"

    def __init__(self) -> None:
        self.calls = 0

    async def compute(
        self,
        origin: RoutePoint,
        destination: RoutePoint,
        *_args: object,
    ) -> RouteSegment:
        self.calls += 1
        return RouteSegment(
            from_item_id=origin.item_id,
            to_item_id=destination.item_id,
            provider=self.name,
            attribution="test",
            generated_at=datetime.now(UTC),
            duration_minutes=self.calls,
        )


@pytest.mark.asyncio
async def test_japan_routes_prefer_google_before_navitime() -> None:
    service = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(route_cache_ttl_seconds=300),
        google=WorkingProvider(),
        navitime=UnexpectedProvider(),
    )
    segment = await service.compute(
        point("A", 35.1, 139.1),
        point("B", 35.2, 139.2),
        None,
        "FEWER_TRANSFERS",
        japan=True,
    )
    assert segment is not None and segment.provider == "working"


@pytest.mark.asyncio
async def test_japan_provider_falls_back_and_cached_ids_are_rebound() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    service = RouteService(
        redis,
        Settings(route_cache_ttl_seconds=300),
        google=EmptyProvider(),
        navitime=WorkingProvider(),
    )
    first = await service.compute(
        point("A", 35.1, 139.1),
        point("B", 35.2, 139.2),
        None,
        "FEWER_TRANSFERS",
        japan=True,
    )
    second_origin, second_destination = point("A2", 35.1, 139.1), point("B2", 35.2, 139.2)
    second = await service.compute(
        second_origin,
        second_destination,
        None,
        "FEWER_TRANSFERS",
        japan=True,
    )
    assert first is not None and first.provider == "working"
    assert second is not None and second.from_item_id == second_origin.item_id
    assert second.to_item_id == second_destination.item_id


@pytest.mark.asyncio
async def test_route_cache_separates_different_google_place_ids_at_same_coordinates() -> None:
    provider = CountingProvider()
    service = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(route_cache_ttl_seconds=300),
        google=provider,
        navitime=UnexpectedProvider(),
    )
    first = await service.compute(
        point("A", 35.1, 139.1, "google-a"),
        point("B", 35.2, 139.2, "google-b"),
        None,
        "FEWER_TRANSFERS",
        japan=False,
    )
    second = await service.compute(
        point("A2", 35.1, 139.1, "google-a2"),
        point("B2", 35.2, 139.2, "google-b2"),
        None,
        "FEWER_TRANSFERS",
        japan=False,
    )
    assert provider.calls == 2
    assert first is not None and first.duration_minutes == 1
    assert second is not None and second.duration_minutes == 2


def test_transit_time_window_marks_far_future_as_preview() -> None:
    effective, mode, warnings = supported_transit_time(datetime.now(UTC) + timedelta(days=101))
    assert effective is not None
    assert mode == "preview"
    assert warnings
