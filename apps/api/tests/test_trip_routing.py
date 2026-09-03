import json
from datetime import UTC, datetime, timedelta
from typing import cast
from uuid import uuid4
from zoneinfo import ZoneInfo

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
    google_external_navigation,
    route_provider_configured,
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
                    None,
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
async def test_google_route_returns_up_to_three_unique_alternatives() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        payload = cast(dict[str, object], json.loads(request.read()))
        assert payload["computeAlternativeRoutes"] is True
        return httpx.Response(
            200,
            json={
                "routes": [
                    {
                        "duration": "600s",
                        "distanceMeters": 1000,
                        "routeLabels": ["DEFAULT_ROUTE"],
                        "polyline": {"encodedPolyline": "route-a"},
                    },
                    {
                        "duration": "600s",
                        "distanceMeters": 1000,
                        "routeLabels": ["DEFAULT_ROUTE_ALTERNATE"],
                        "polyline": {"encodedPolyline": "route-a"},
                    },
                    {
                        "duration": "720s",
                        "distanceMeters": 900,
                        "routeLabels": ["DEFAULT_ROUTE_ALTERNATE"],
                        "polyline": {"encodedPolyline": "route-b"},
                    },
                    {
                        "duration": "780s",
                        "distanceMeters": 800,
                        "polyline": {"encodedPolyline": "route-c"},
                    },
                ]
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = GoogleRouteProvider(Settings(google_maps_api_key="key"), client)
    options = await provider.compute_options(
        point("上野", 35.7, 139.7),
        point("淺草", 35.71, 139.8),
        None,
        "FASTEST",
        "walk",
        max_options=3,
    )
    await client.aclose()

    assert [option.duration_minutes for option in options] == [10, 12, 13]
    assert [option.route_option_rank for option in options] == [1, 2, 3]
    assert options[0].provider_route_key == "DEFAULT_ROUTE"
    assert "origin=35.7000000%2C139.7000000" in str(options[0].maps_url)
    assert "destination=35.7100000%2C139.8000000" in str(options[0].maps_url)
    assert "travelmode=walking" in str(options[0].maps_url)
    assert "%E4%B8%8A%E9%87%8E" not in str(options[0].maps_url)


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


@pytest.mark.asyncio
async def test_navitime_returns_multiple_routes_with_provider_shapes() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["shape"] == "true"
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "no": index,
                        "time": 10 + index,
                        "distance": 1000 + index,
                        "nodes": [],
                        "shapes": {
                            "features": [
                                {
                                    "geometry": {
                                        "type": "LineString",
                                        "coordinates": [
                                            [139.7, 35.7],
                                            [139.7 + index / 1000, 35.71],
                                        ],
                                    }
                                }
                            ]
                        },
                    }
                    for index in range(1, 4)
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
    options = await provider.compute_options(
        point("上野", 35.7, 139.7),
        point("淺草", 35.71, 139.8),
        datetime.now(UTC),
        "FEWER_TRANSFERS",
        max_options=3,
    )
    await client.aclose()

    assert len(options) == 3
    assert [option.provider_route_key for option in options] == ["1", "2", "3"]
    assert all(option.encoded_polyline for option in options)


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


class MalformedProvider:
    name = "malformed"

    async def compute(self, *_args: object) -> None:
        raise TypeError("unexpected provider payload")


class UnsortedOptionsProvider:
    name = "unsorted"

    async def compute_options(
        self,
        origin: RoutePoint,
        destination: RoutePoint,
        *_args: object,
        **_kwargs: object,
    ) -> list[RouteSegment]:
        return [
            RouteSegment(
                from_item_id=origin.item_id,
                to_item_id=destination.item_id,
                provider=self.name,
                attribution="test",
                generated_at=datetime.now(UTC),
                travel_mode="walk",
                duration_minutes=duration,
                distance_meters=distance,
            )
            for duration, distance in ((11, 780), (10, 805), (12, 700))
        ]


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
async def test_japan_transit_routes_prefer_navitime_before_google() -> None:
    service = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(route_cache_ttl_seconds=300),
        google=UnexpectedProvider(),
        navitime=WorkingProvider(),
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
async def test_japan_transit_does_not_send_google_routes_requests() -> None:
    service = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(google_maps_api_key="key", route_cache_ttl_seconds=300),
        google=UnexpectedProvider(),
        navitime=EmptyProvider(),
    )

    segment = await service.compute(
        point("谷中靈園", 35.725278, 139.770556),
        point("淺草寺", 35.714722, 139.796750),
        datetime.now(ZoneInfo("Asia/Tokyo")) + timedelta(days=2),
        "FEWER_TRANSFERS",
        japan=True,
    )

    assert segment is None


@pytest.mark.asyncio
async def test_route_cache_rebinds_item_ids() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    service = RouteService(
        redis,
        Settings(route_cache_ttl_seconds=300),
        google=WorkingProvider(),
        navitime=EmptyProvider(),
    )
    first = await service.compute(
        point("A", 35.1, 139.1),
        point("B", 35.2, 139.2),
        None,
        "FEWER_TRANSFERS",
        japan=False,
    )
    second_origin, second_destination = point("A2", 35.1, 139.1), point("B2", 35.2, 139.2)
    second = await service.compute(
        second_origin,
        second_destination,
        None,
        "FEWER_TRANSFERS",
        japan=False,
    )
    assert first is not None and first.provider == "working"
    assert second is not None and second.from_item_id == second_origin.item_id
    assert second.to_item_id == second_destination.item_id


def test_japan_transit_requires_navitime_configuration() -> None:
    google_only = Settings(google_maps_api_key="key")
    with_navitime = Settings(
        navitime_api_base_url="https://example.test/navitime",
        navitime_client_id="client",
        navitime_api_key="secret",
    )

    assert route_provider_configured(google_only, "JP", "transit") is False
    assert route_provider_configured(with_navitime, "JP", "transit") is True
    assert route_provider_configured(google_only, "JP", "walk") is True


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


@pytest.mark.asyncio
async def test_route_service_converts_provider_exceptions_to_unavailable_options() -> None:
    service = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(route_cache_ttl_seconds=300),
        google=MalformedProvider(),
    )
    options = await service.compute_options(
        point("A", 35.1, 139.1),
        point("B", 35.2, 139.2),
        None,
        "FASTEST",
        travel_mode="walk",
        max_options=3,
    )
    assert options == []


@pytest.mark.asyncio
async def test_route_service_recommends_the_fastest_non_transit_option() -> None:
    service = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(route_cache_ttl_seconds=300),
        google=UnsortedOptionsProvider(),
    )

    options = await service.compute_options(
        point("A", 35.1, 139.1),
        point("B", 35.2, 139.2),
        None,
        "FEWER_TRANSFERS",
        travel_mode="walk",
        max_options=3,
    )

    assert [option.duration_minutes for option in options] == [10, 11, 12]
    assert [option.route_option_rank for option in options] == [1, 2, 3]


def test_transit_time_window_marks_far_future_as_preview() -> None:
    effective, mode, warnings = supported_transit_time(datetime.now(UTC) + timedelta(days=101))
    assert effective is not None
    assert mode == "preview"
    assert warnings


def test_far_future_transit_preview_preserves_destination_weekday_and_time() -> None:
    tokyo = ZoneInfo("Asia/Tokyo")
    requested = (datetime.now(tokyo) + timedelta(days=180)).replace(
        hour=10,
        minute=35,
        second=0,
        microsecond=0,
    )
    effective, mode, _ = supported_transit_time(requested)
    assert effective is not None
    preview_local = effective.astimezone(tokyo)
    assert mode == "preview"
    assert preview_local.weekday() == requested.weekday()
    assert (preview_local.hour, preview_local.minute) == (10, 35)


@pytest.mark.asyncio
async def test_google_transit_retries_once_without_empty_preference() -> None:
    bodies: list[str] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        body = request.read().decode()
        bodies.append(body)
        if "transitPreferences" in body:
            return httpx.Response(200, json={"routes": []})
        return httpx.Response(
            200,
            json={"routes": [{"duration": "720s", "legs": []}]},
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = GoogleRouteProvider(Settings(google_maps_api_key="key"), client)
    segment = await provider.compute(
        point("東京車站", 35.6812, 139.7671),
        point("淺草寺", 35.7148, 139.7967),
        datetime.now(ZoneInfo("Asia/Tokyo")) + timedelta(days=2),
        "FEWER_TRANSFERS",
    )
    await client.aclose()
    assert segment is not None and segment.duration_minutes == 12
    assert len(bodies) == 2
    assert "transitPreferences" in bodies[0]
    assert "transitPreferences" not in bodies[1]
    assert any("已改用一般大眾運輸" in warning for warning in segment.warnings)


@pytest.mark.asyncio
async def test_scheduled_transit_without_published_timetable_uses_near_term_preview() -> None:
    tokyo = ZoneInfo("Asia/Tokyo")
    requested = (datetime.now(tokyo) + timedelta(days=45)).replace(
        hour=11,
        minute=30,
        second=0,
        microsecond=0,
    )
    bodies: list[dict[str, object]] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        body = cast(dict[str, object], json.loads(request.read()))
        bodies.append(body)
        if len(bodies) < 3:
            return httpx.Response(200, json={"routes": []})
        return httpx.Response(
            200,
            json={"routes": [{"duration": "1320s", "legs": []}]},
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = GoogleRouteProvider(Settings(google_maps_api_key="key"), client)
    segment = await provider.compute(
        point("谷中靈園", 35.725278, 139.770556),
        point("淺草寺", 35.714722, 139.796750),
        requested,
        "FEWER_TRANSFERS",
    )
    await client.aclose()

    assert segment is not None and segment.duration_minutes == 22
    assert segment.schedule_mode == "preview"
    assert segment.requested_departure_time == requested
    assert len(bodies) == 3
    requested_utc = requested.astimezone(UTC)
    fallback_utc = datetime.fromisoformat(str(bodies[-1]["departureTime"]).replace("Z", "+00:00"))
    fallback_local = fallback_utc.astimezone(tokyo)
    assert fallback_utc != requested_utc
    assert datetime.now(UTC) < fallback_utc <= datetime.now(UTC) + timedelta(days=8)
    assert fallback_local.weekday() == requested.weekday()
    assert (fallback_local.hour, fallback_local.minute) == (11, 30)
    assert any("可以先套用移動時間" in warning for warning in segment.warnings)


@pytest.mark.asyncio
async def test_scheduled_transit_uses_current_google_schedule_after_empty_references() -> None:
    tokyo = ZoneInfo("Asia/Tokyo")
    requested = (datetime.now(tokyo) + timedelta(days=45)).replace(
        hour=11,
        minute=30,
        second=0,
        microsecond=0,
    )
    bodies: list[dict[str, object]] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        body = cast(dict[str, object], json.loads(request.read()))
        bodies.append(body)
        if "departureTime" in body:
            return httpx.Response(200, json={"routes": []})
        return httpx.Response(
            200,
            json={"routes": [{"duration": "1380s", "legs": []}]},
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = GoogleRouteProvider(Settings(google_maps_api_key="key"), client)
    segment = await provider.compute(
        point("谷中靈園", 35.725278, 139.770556),
        point("淺草寺", 35.714722, 139.796750),
        requested,
        "FEWER_TRANSFERS",
    )
    await client.aclose()

    assert segment is not None and segment.duration_minutes == 23
    assert segment.schedule_mode == "preview"
    assert segment.requested_departure_time == requested
    assert len(bodies) == 5
    daytime_utc = datetime.fromisoformat(
        str(bodies[-2]["departureTime"]).replace("Z", "+00:00")
    )
    daytime_local = daytime_utc.astimezone(tokyo)
    assert daytime_local.weekday() == requested.weekday()
    assert (daytime_local.hour, daytime_local.minute) == (10, 0)
    assert "departureTime" not in bodies[-1]
    assert any("Google 目前可取得" in warning for warning in segment.warnings)
    assert any("可以先套用移動時間" in warning for warning in segment.warnings)


@pytest.mark.asyncio
async def test_far_future_transit_retries_with_current_schedule() -> None:
    bodies: list[dict[str, object]] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        body = cast(dict[str, object], json.loads(request.read()))
        bodies.append(body)
        if "departureTime" in body:
            return httpx.Response(200, json={"routes": []})
        return httpx.Response(200, json={"routes": [{"duration": "1800s", "legs": []}]})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = GoogleRouteProvider(Settings(google_maps_api_key="key"), client)
    segment = await provider.compute(
        point("成田國際機場", 35.772, 140.392),
        point("東京晴空塔", 35.710, 139.811),
        datetime.now(ZoneInfo("Asia/Tokyo")) + timedelta(days=180),
        "FEWER_TRANSFERS",
    )
    await client.aclose()

    assert segment is not None and segment.duration_minutes == 30
    assert segment.schedule_mode == "preview"
    assert len(bodies) == 3
    assert "departureTime" not in bodies[-1]
    assert any("目前可取得的參考路線" in warning for warning in segment.warnings)


@pytest.mark.asyncio
async def test_google_route_retries_coordinates_when_place_ids_have_no_route() -> None:
    bodies: list[dict[str, object]] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        body = cast(dict[str, object], json.loads(request.read()))
        bodies.append(body)
        origin = cast(dict[str, object], body["origin"])
        if "placeId" in origin:
            return httpx.Response(200, json={"routes": []})
        return httpx.Response(200, json={"routes": [{"duration": "900s", "legs": []}]})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = GoogleRouteProvider(Settings(google_maps_api_key="key"), client)
    segment = await provider.compute(
        point("東京站", 35.6812, 139.7671, "google-origin"),
        point("淺草寺", 35.7148, 139.7967, "google-destination"),
        datetime.now(ZoneInfo("Asia/Tokyo")) + timedelta(days=2),
        "FEWER_TRANSFERS",
    )
    await client.aclose()

    assert segment is not None and segment.duration_minutes == 15
    assert len(bodies) == 3
    assert "location" in cast(dict[str, object], bodies[-1]["origin"])
    assert any("座標重試" in warning for warning in segment.warnings)


def test_google_external_navigation_preserves_exact_place_ids() -> None:
    origin = point("成田國際機場", 35.772, 140.392, "google-origin")
    destination = point("東京晴空塔", 35.710, 139.811, "google-destination")
    navigation = google_external_navigation(
        origin,
        destination,
        "transit",
        reason="站內路線暫時無法取得",
    )

    assert navigation.provider == "google_maps"
    assert navigation.label == "Google Maps"
    assert "origin_place_id=google-origin" in navigation.web_url
    assert "destination_place_id=google-destination" in navigation.web_url
    assert "travelmode=transit" in navigation.web_url
    assert navigation.app_url == navigation.web_url


def test_google_external_navigation_uses_confirmed_coordinates_without_place_ids() -> None:
    navigation = google_external_navigation(
        point("谷中靈園", 35.7272, 139.7710),
        point("淺草寺", 35.7148, 139.7967),
        "walk",
        reason="站內路線暫時無法取得",
    )

    assert "origin=35.7272000%2C139.7710000" in navigation.web_url
    assert "destination=35.7148000%2C139.7967000" in navigation.web_url
    assert "travelmode=walking" in navigation.web_url
    assert "%E8%B0%B7%E4%B8%AD%E9%9D%88%E5%9C%92" not in navigation.web_url
