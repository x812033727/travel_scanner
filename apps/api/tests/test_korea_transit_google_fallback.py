import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any
from urllib.parse import parse_qs, urlparse
from uuid import uuid4
from zoneinfo import ZoneInfo

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.i18n import Locale
from app.providers.usage_meter import google_maps_usage_snapshot
from app.trips.routing import (
    GoogleRouteProvider,
    RoutePoint,
    RouteSegment,
    RouteService,
    TravelMode,
    korean_external_route_reason,
    route_provider_configured,
)


def korea_points(
    origin_google_id: str | None = None, destination_google_id: str | None = None
) -> tuple[RoutePoint, RoutePoint]:
    return (
        RoutePoint(
            item_id=uuid4(),
            name="테스트 호텔",
            latitude=37.56,
            longitude=126.98,
            provider_place_id="naver:local:origin-hash",
            place_provider="naver_local",
            google_place_id=origin_google_id,
        ),
        RoutePoint(
            item_id=uuid4(),
            name="테스트 박물관",
            latitude=37.58,
            longitude=126.97,
            provider_place_id="naver:local:destination-hash",
            place_provider="naver_local",
            google_place_id=destination_google_id,
        ),
    )


@pytest.fixture
def korean_google_response() -> dict[str, Any]:
    """Synthetic provider-shaped data, not retained Google response content."""
    return {
        "routes": [
            {
                "duration": "1440s",
                "distanceMeters": 3100,
                "polyline": {"encodedPolyline": "synthetic-polyline"},
                "travelAdvisory": {"transitFare": {"currencyCode": "KRW", "units": "1500"}},
                "legs": [
                    {
                        "steps": [
                            {
                                "travelMode": "WALK",
                                "staticDuration": "300s",
                                "distanceMeters": 320,
                                "navigationInstruction": {"instructions": "테스트 정류장까지 도보"},
                            },
                            {
                                "travelMode": "TRANSIT",
                                "staticDuration": "360s",
                                "distanceMeters": 2400,
                                "transitDetails": {
                                    "stopDetails": {
                                        "departureStop": {"name": "테스트 출발 정류장"},
                                        "arrivalStop": {"name": "테스트 도착 정류장"},
                                        "departureTime": "2026-09-17T00:10:00Z",
                                        "arrivalTime": "2026-09-17T00:16:00Z",
                                    },
                                    "headsign": "테스트 종점",
                                    "transitLine": {
                                        "name": "테스트 버스",
                                        "nameShort": "9912",
                                        "color": "#dd1122",
                                        "vehicle": {"type": "BUS"},
                                    },
                                    "stopCount": 4,
                                },
                            },
                            {
                                "travelMode": "WALK",
                                "staticDuration": "360s",
                                "distanceMeters": 380,
                                "navigationInstruction": {"instructions": "테스트 박물관까지 도보"},
                            },
                        ]
                    }
                ],
            }
        ]
    }


class CountingProvider:
    def __init__(self, name: str, *, returns_route: bool = False) -> None:
        self.name = name
        self.returns_route = returns_route
        self.calls = 0

    async def compute(
        self,
        origin: RoutePoint,
        destination: RoutePoint,
        departure_time: datetime | None,
        preference: str,
        travel_mode: TravelMode,
    ) -> RouteSegment | None:
        self.calls += 1
        if not self.returns_route:
            return None
        return RouteSegment(
            from_item_id=origin.item_id,
            to_item_id=destination.item_id,
            provider=self.name,
            attribution="Synthetic test provider",
            generated_at=datetime.now(UTC),
            duration_minutes=20,
            travel_mode=travel_mode,
        )


@pytest.mark.parametrize("odsay_key", [None, "test-odsay-key"])
@pytest.mark.parametrize("google_key", [None, "test-google-key"])
def test_korean_mode_configuration_preserves_walk_and_drive_policy(
    odsay_key: str | None, google_key: str | None
) -> None:
    settings = Settings(
        odsay_api_key=odsay_key,
        google_maps_api_key=google_key,
        naver_maps_client_id=None,
        naver_maps_client_secret=None,
    )
    assert route_provider_configured(settings, "KR", "transit") is bool(odsay_key or google_key)
    assert route_provider_configured(settings, "KR", "walk") is False
    assert route_provider_configured(settings, "KR", "drive") is False
    naver_settings = settings.model_copy(
        update={"naver_maps_client_id": "test-id", "naver_maps_client_secret": "test-secret"}
    )
    assert route_provider_configured(naver_settings, "KR", "drive") is True


@pytest.mark.asyncio
@pytest.mark.parametrize("returns_route", [False, True])
async def test_configured_odsay_is_chosen_without_a_google_paid_retry(returns_route: bool) -> None:
    google = CountingProvider("google_routes", returns_route=True)
    odsay = CountingProvider("odsay", returns_route=returns_route)
    service = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(odsay_api_key="test-odsay-key", google_maps_api_key="test-google-key"),
        google=google,
        odsay=odsay,
    )
    origin, destination = korea_points()
    segment = await service.compute(origin, destination, None, "FASTEST", region_code="KR")
    assert (segment is not None) is returns_route
    if segment is not None:
        assert segment.provider == "odsay"
    assert odsay.calls == 1
    assert google.calls == 0


@pytest.mark.asyncio
async def test_google_fallback_does_not_change_korean_walk_or_drive_providers() -> None:
    google = CountingProvider("google_routes", returns_route=True)
    naver = CountingProvider("naver_directions", returns_route=True)
    service = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(odsay_api_key=None, google_maps_api_key="test-google-key"),
        google=google,
        naver=naver,
    )
    origin, destination = korea_points()
    assert (
        await service.compute(
            origin, destination, None, "FASTEST", region_code="KR", travel_mode="walk"
        )
        is None
    )
    driving = await service.compute(
        origin, destination, None, "FASTEST", region_code="KR", travel_mode="drive"
    )
    assert driving is not None and driving.provider == "naver_directions"
    assert naver.calls == 1
    assert google.calls == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("origin_google_id", "destination_google_id"),
    [(None, None), ("google-origin", None), ("google-origin", "google-destination")],
)
async def test_korean_google_fallback_normalizes_steps_and_isolates_provider_ids(
    korean_google_response: dict[str, Any],
    origin_google_id: str | None,
    destination_google_id: str | None,
) -> None:
    requests: list[dict[str, Any]] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(json.loads(request.read()))
        assert "transitDetails" in request.headers["x-goog-fieldmask"]
        return httpx.Response(200, json=korean_google_response)

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(odsay_api_key=None, google_maps_api_key="test-google-key")
    origin, destination = korea_points(origin_google_id, destination_google_id)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = RouteService(redis, settings, google=GoogleRouteProvider(settings, client, redis))
        segment = await service.compute(origin, destination, None, "FASTEST", region_code="KR")
        cached = await service.compute(origin, destination, None, "FASTEST", region_code="KR")

    assert segment is not None and cached == segment
    assert segment.provider == "google_routes"
    assert segment.attribution == "Google Maps"
    assert segment.duration_minutes == 24
    assert segment.fare == Decimal("1500") and segment.currency == "KRW"
    assert [step.travel_mode for step in segment.steps] == ["WALK", "TRANSIT", "WALK"]
    assert [step.duration_minutes for step in segment.steps] == [5, 6, 6]
    assert [step.distance_meters for step in segment.steps] == [320, 2400, 380]
    assert segment.steps[0].instruction == "테스트 정류장까지 도보"
    ride = segment.steps[1]
    assert ride.departure_stop == "테스트 출발 정류장"
    assert ride.arrival_stop == "테스트 도착 정류장"
    assert ride.line_name == "테스트 버스" and ride.line_short_name == "9912"
    assert ride.line_color == "#dd1122" and ride.headsign == "테스트 종점"
    assert ride.stop_count == 4
    assert ride.departure_time == datetime(2026, 9, 17, 0, 10, tzinfo=UTC)
    assert ride.arrival_time == datetime(2026, 9, 17, 0, 16, tzinfo=UTC)
    assert ride.platform is None and ride.exit_name is None
    assert len(requests) == 1
    assert requests[0]["travelMode"] == "TRANSIT"
    assert "naver" not in json.dumps(requests)
    for key, point in (("origin", origin), ("destination", destination)):
        assert requests[0][key] == (
            {"placeId": point.google_place_id}
            if point.google_place_id
            else {
                "location": {"latLng": {"latitude": point.latitude, "longitude": point.longitude}}
            }
        )
    links = parse_qs(urlparse(segment.maps_url or "").query)
    assert links.get("origin_place_id") == ([origin_google_id] if origin_google_id else None)
    assert links.get("destination_place_id") == (
        [destination_google_id] if destination_google_id else None
    )
    assert "naver" not in str(segment.maps_url)
    assert (await google_maps_usage_snapshot(redis)).breakdown.get("routes") == 1


@pytest.mark.asyncio
async def test_korean_google_fallback_obeys_existing_monthly_budget(
    korean_google_response: dict[str, Any],
) -> None:
    calls = 0

    async def handler(_: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(200, json=korean_google_response)

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(
        odsay_api_key=None,
        google_maps_api_key="test-google-key",
        google_maps_essentials_free_limit=1,
    )
    odsay = CountingProvider("odsay", returns_route=True)
    origin, destination = korea_points()
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = RouteService(
            redis, settings, google=GoogleRouteProvider(settings, client, redis), odsay=odsay
        )
        first = await service.compute(origin, destination, None, "FASTEST", region_code="KR")
        second = await service.compute(
            origin, destination, None, "FASTEST", region_code="KR", refresh=True
        )
    assert first is not None and second is None
    assert calls == 1 and odsay.calls == 0
    assert (await google_maps_usage_snapshot(redis)).breakdown.get("routes") == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("google_key", [None, "test-google-key"])
async def test_unconfigured_or_unavailable_google_returns_no_fabricated_route(
    google_key: str | None,
) -> None:
    calls = 0

    async def handler(_: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(200, json={"routes": []})

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(odsay_api_key=None, google_maps_api_key=google_key)
    odsay = CountingProvider("odsay", returns_route=True)
    origin, destination = korea_points()
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = RouteService(
            redis, settings, google=GoogleRouteProvider(settings, client, redis), odsay=odsay
        )
        segment = await service.compute(origin, destination, None, "FASTEST", region_code="KR")
    assert segment is None
    assert calls == int(bool(google_key))
    assert odsay.calls == 0
    assert (await google_maps_usage_snapshot(redis)).breakdown.get("routes", 0) == calls


@pytest.mark.asyncio
@pytest.mark.parametrize("days_ahead", [21, 150])
async def test_korean_google_far_future_routes_remain_same_weekday_reference_previews(
    korean_google_response: dict[str, Any], days_ahead: int
) -> None:
    requests: list[dict[str, Any]] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(json.loads(request.read()))
        return httpx.Response(200, json=korean_google_response)

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(odsay_api_key=None, google_maps_api_key="test-google-key")
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    requested = (now + timedelta(days=days_ahead)).replace(
        hour=9, minute=0, second=0, microsecond=0
    )
    origin, destination = korea_points()
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = RouteService(redis, settings, google=GoogleRouteProvider(settings, client, redis))
        segment = await service.compute(origin, destination, requested, "FASTEST", region_code="KR")
    assert segment is not None
    assert segment.schedule_mode == "preview"
    assert segment.requested_departure_time == requested
    assert segment.warnings and any("相同星期" in warning for warning in segment.warnings)
    assert len(requests) == 1
    effective = datetime.fromisoformat(requests[0]["departureTime"]).astimezone(now.tzinfo)
    assert now < effective < now + timedelta(days=8)
    assert effective.weekday() == requested.weekday()
    assert (effective.hour, effective.minute) == (9, 0)
    assert effective.date() != requested.date()
    assert (await google_maps_usage_snapshot(redis)).breakdown.get("routes") == 1


@pytest.mark.parametrize("locale", ["zh-TW", "zh-CN", "en", "ja", "ko"])
def test_external_transit_reasons_match_selected_provider_in_each_locale(locale: Locale) -> None:
    odsay = korean_external_route_reason(
        "transit", odsay_configured=True, google_configured=True, locale=locale
    )
    google = korean_external_route_reason(
        "transit", odsay_configured=False, google_configured=True, locale=locale
    )
    unconfigured = korean_external_route_reason("transit", odsay_configured=False, locale=locale)
    assert "ODsay" in odsay and "ODsay" not in google and "ODsay" not in unconfigured
    assert len({odsay, google, unconfigured}) == 3
    assert google.count("Google") == 2
    for mode in ("walk", "drive"):
        assert korean_external_route_reason(
            mode, odsay_configured=False, google_configured=True, locale=locale
        ) == korean_external_route_reason(mode, odsay_configured=False, locale=locale)
