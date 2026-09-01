import json
from datetime import UTC, datetime
from uuid import uuid4

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.places.naver import NaverPlaceService
from app.providers.usage_meter import naver_maps_usage_snapshot, record_naver_maps_request
from app.trips.routing import (
    GoogleRouteProvider,
    NaverDirectionsProvider,
    RoutePoint,
    RouteSegment,
    RouteService,
    naver_external_navigation,
    trip_region_code,
)


def naver_settings() -> Settings:
    return Settings(
        naver_maps_client_id="client-id",
        naver_maps_client_secret="client-secret",
        naver_place_cache_ttl_seconds=900,
    )


@pytest.mark.asyncio
async def test_naver_usage_uses_korean_month_and_optional_internal_limit() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    august = datetime(2026, 8, 31, 14, 59, tzinfo=UTC)
    september = datetime(2026, 8, 31, 15, 0, tzinfo=UTC)
    await record_naver_maps_request(redis, "local_search", now=august)
    await record_naver_maps_request(redis, "directions", now=september)

    august_snapshot = await naver_maps_usage_snapshot(redis, monthly_limit=5, now=august)
    september_snapshot = await naver_maps_usage_snapshot(
        redis, monthly_limit=5, now=september
    )
    assert august_snapshot.period == "2026-08"
    assert august_snapshot.used == 1
    assert august_snapshot.remaining == 4
    assert september_snapshot.period == "2026-09"
    assert september_snapshot.used == 1
    assert september_snapshot.breakdown["directions"] == 1
    await redis.aclose()


@pytest.mark.asyncio
async def test_naver_local_search_cleans_html_normalizes_coordinates_and_caches_details() -> None:
    seen_headers: dict[str, str] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen_headers.update(request.headers)
        assert request.url.params["display"] == "5"
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "title": "<b>景福宮</b> &amp; 國立古宮博物館",
                        "roadAddress": "서울특별시 종로구 사직로 161",
                        "mapx": "1269770160",
                        "mapy": "375794951",
                    },
                    {
                        "title": "不應出現的東京候選",
                        "roadAddress": "東京",
                        "mapx": "1397671000",
                        "mapy": "356812000",
                    },
                ]
            },
        )

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = NaverPlaceService(redis, naver_settings(), client)
    results = await service.autocomplete("景福宮", "session-1")

    assert len(results) == 1
    result = results[0]
    assert result["provider"] == "naver_local"
    assert result["name"] == "景福宮 & 國立古宮博物館"
    assert result["latitude"] == pytest.approx(37.5794951)
    assert result["longitude"] == pytest.approx(126.977016)
    assert len(result["place_id"]) == 32
    assert seen_headers["x-ncp-apigw-api-key-id"] == "client-id"
    assert await service.place_details(result["place_id"], "session-1") == result
    assert await service.place_details(result["place_id"], "another-session") == {}
    assert await redis.ttl(service._detail_key(result["place_id"], "session-1")) > 0
    usage = await naver_maps_usage_snapshot(redis)
    assert usage.breakdown["local_search"] == 1
    await client.aclose()
    await redis.aclose()


@pytest.mark.asyncio
async def test_naver_place_search_falls_back_to_geocode_and_rejects_http_failures() -> None:
    calls: list[str] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        if "search/v1/local" in request.url.path:
            return httpx.Response(200, json={"items": []})
        return httpx.Response(
            200,
            json={
                "addresses": [
                    {
                        "roadAddress": "서울특별시 종로구 계동길 37",
                        "jibunAddress": "서울특별시 종로구 계동 105",
                        "x": "126.9849",
                        "y": "37.5826",
                    }
                ]
            },
        )

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = NaverPlaceService(redis, naver_settings(), client)
    results = await service.autocomplete("北村韓屋村", "session-2")
    assert len(results) == 1
    assert results[0]["address"] == "서울특별시 종로구 계동길 37"
    assert len(calls) == 2

    failing_client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda _request: httpx.Response(429, json={}))
    )
    failing = NaverPlaceService(redis, naver_settings(), failing_client)
    assert await failing.autocomplete("景福宮", "session-3") == []
    await client.aclose()
    await failing_client.aclose()
    await redis.aclose()


@pytest.mark.asyncio
async def test_naver_directions_parses_drive_path_steps_and_usage() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["option"] == "trafast"
        assert request.url.params["start"] == "126.9770000,37.5796000"
        return httpx.Response(
            200,
            json={
                "code": 0,
                "route": {
                    "trafast": [
                        {
                            "summary": {"duration": 720_000, "distance": 4300},
                            "path": [[126.977, 37.5796], [126.982, 37.582], [126.985, 37.5826]],
                            "guide": [
                                {
                                    "instructions": "사직로 방면으로 우회전",
                                    "duration": 180_000,
                                    "distance": 900,
                                }
                            ],
                        }
                    ]
                },
            },
        )

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = NaverDirectionsProvider(naver_settings(), client, redis)
    origin = RoutePoint(item_id=uuid4(), name="景福宮", latitude=37.5796, longitude=126.977)
    destination = RoutePoint(
        item_id=uuid4(), name="北村韓屋村", latitude=37.5826, longitude=126.985
    )
    result = await provider.compute(
        origin, destination, datetime(2026, 11, 10, 1, tzinfo=UTC), "FASTEST", "drive"
    )

    assert result is not None
    assert result.provider == "naver_maps"
    assert result.duration_minutes == 12
    assert result.distance_meters == 4300
    assert result.encoded_polyline
    assert result.steps[0].instruction == "사직로 방면으로 우회전"
    assert result.maps_url and result.maps_url.startswith("https://map.naver.com/p/directions/")
    assert any("目前路況" in warning for warning in result.warnings)
    assert await provider.compute(origin, destination, None, "FASTEST", "transit") is None
    usage = await naver_maps_usage_snapshot(redis)
    assert usage.breakdown["directions"] == 1
    await client.aclose()
    await redis.aclose()


class RecordingProvider:
    def __init__(self, name: str, result: RouteSegment | None) -> None:
        self.name = name
        self.result = result
        self.calls: list[str] = []

    async def compute(
        self,
        _origin: RoutePoint,
        _destination: RoutePoint,
        _departure: datetime | None,
        _preference: str,
        travel_mode: str,
    ) -> RouteSegment | None:
        self.calls.append(travel_mode)
        return self.result


@pytest.mark.asyncio
async def test_korean_route_matrix_uses_naver_only_for_drive_then_google_fallback() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    naver = RecordingProvider("naver", None)
    google_result = RouteSegment(
        from_item_id=uuid4(),
        to_item_id=uuid4(),
        provider="google",
        attribution="Google Maps",
        generated_at=datetime.now(UTC),
        duration_minutes=20,
    )
    google = RecordingProvider("google", google_result)
    service = RouteService(redis, Settings(route_cache_ttl_seconds=300), google=google, naver=naver)
    origin = RoutePoint(item_id=uuid4(), name="A", latitude=37.57, longitude=126.97)
    destination = RoutePoint(item_id=uuid4(), name="B", latitude=37.58, longitude=126.98)

    assert (
        await service.compute(
            origin, destination, None, "FASTEST", region_code="KR", travel_mode="drive"
        )
        is google_result
    )
    assert naver.calls == ["drive"]
    assert google.calls == ["drive"]
    await service.compute(
        origin, destination, None, "FASTEST", region_code="KR", travel_mode="transit"
    )
    assert naver.calls == ["drive"]
    assert google.calls == ["drive", "transit"]
    await redis.aclose()


@pytest.mark.asyncio
async def test_google_routes_never_sends_a_naver_place_id() -> None:
    captured: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured.update(json.loads(request.read()))
        return httpx.Response(200, json={"routes": []})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = GoogleRouteProvider(Settings(google_maps_api_key="key"), client)
    point = RoutePoint(
        item_id=uuid4(),
        name="景福宮",
        latitude=37.5796,
        longitude=126.977,
        provider_place_id="naver-opaque-id",
        place_provider="naver_local",
    )
    await provider.compute(
        point, point.model_copy(update={"item_id": uuid4()}), None, "FASTEST", "walk"
    )
    assert "location" in captured["origin"]  # type: ignore[operator]
    assert "placeId" not in captured["origin"]  # type: ignore[operator]
    await client.aclose()


def test_naver_external_navigation_and_region_detection_are_scoped_to_official_targets() -> None:
    origin = RoutePoint(
        item_id=uuid4(), name="景福宮 & 광화문", latitude=37.5796, longitude=126.977
    )
    destination = RoutePoint(
        item_id=uuid4(), name="北村韓屋村", latitude=37.5826, longitude=126.985
    )
    external = naver_external_navigation(origin, destination, "transit", reason="外部班次")
    assert external.app_url.startswith("nmap://route/public?")
    assert external.web_url.startswith("https://map.naver.com/p/directions/")
    assert "%26" in external.app_url
    assert trip_region_code("Asia/Seoul", "首爾", {}) == "KR"
    assert trip_region_code("Asia/Tokyo", "東京", {}) == "JP"
