import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import cast
from uuid import uuid4
from zoneinfo import ZoneInfo

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings, official_provider_url_ok
from app.providers.usage_meter import navitime_usage_snapshot
from app.trips.routing import (
    EkispertProbeResult,
    EkispertRouteProvider,
    GoogleRouteProvider,
    GoogleRoutesProbeResult,
    NavitimeProbeResult,
    NavitimeRouteProvider,
    OdsayProbeResult,
    OdsayRouteProvider,
    RoutePoint,
    RouteSegment,
    RouteService,
    estimate_leg_minutes,
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
                    },
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


NAVITIME_GINZA_ROUTE = {
    "items": [
        {
            "summary": {
                "no": "1",
                "start": {
                    "type": "point",
                    "name": "start",
                    "coord": {"lat": 35.6653, "lon": 139.7126},
                },
                "goal": {
                    "type": "point",
                    "name": "goal",
                    "coord": {"lat": 35.6713, "lon": 139.7651},
                },
                "move": {
                    "type": "move",
                    "from_time": "2026-10-03T08:01:00+09:00",
                    "to_time": "2026-10-03T08:24:00+09:00",
                    "time": 23,
                    "distance": 6400,
                    "transit_count": 0,
                    "fare": {"unit_0": 170.0, "unit_48": 165.0},
                },
            },
            "sections": [
                {"type": "point", "name": "start", "coord": {"lat": 35.6653, "lon": 139.7126}},
                {
                    "type": "move",
                    "move": "walk",
                    "line_name": "徒歩",
                    "time": 5,
                    "distance": 400,
                    "from_time": "2026-10-03T08:01:00+09:00",
                    "to_time": "2026-10-03T08:06:00+09:00",
                },
                {
                    "type": "point",
                    "name": "表参道",
                    "node_id": "00007820",
                    "node_types": ["station"],
                    "start_platform": "1",
                    "gateway": "B1",
                },
                {
                    "type": "move",
                    "move": "local_train",
                    "line_name": "東京メトロ銀座線",
                    "time": 13,
                    "distance": 5900,
                    "from_time": "2026-10-03T08:06:00+09:00",
                    "to_time": "2026-10-03T08:19:00+09:00",
                    "next_transit": False,
                    "transport": {
                        "id": "00000559",
                        "name": "東京メトロ銀座線",
                        "color": "#FF9500",
                        "company": {"id": "00000113", "name": "東京地下鉄（メトロ）"},
                        "type": "普通",
                        "fare": {"unit_0": 170.0, "unit_48": 165.0},
                        "destination": {"name": "浅草", "id": "00005270"},
                        "getoff": "前方第 2 節",
                    },
                },
                {
                    "type": "point",
                    "name": "銀座",
                    "node_id": "00001908",
                    "node_types": ["station"],
                    "gateway": "A3",
                },
                {
                    "type": "move",
                    "move": "walk",
                    "line_name": "徒歩",
                    "time": 5,
                    "distance": 100,
                    "from_time": "2026-10-03T08:19:00+09:00",
                    "to_time": "2026-10-03T08:24:00+09:00",
                },
                {"type": "point", "name": "goal", "coord": {"lat": 35.6713, "lon": 139.7651}},
            ],
            "shapes": {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [[139.7126, 35.6653], [139.7651, 35.6713]],
                        },
                    }
                ],
            },
        }
    ],
    "unit": {
        "datum": "wgs84",
        "coord_unit": "degree",
        "distance": "m",
        "time": "minute",
        "currency": "JPY",
    },
}


EKISPERT_TOKYO_ROUTE = {
    "ResultSet": {
        "Course": [
            {
                "searchType": "plain",
                "dataType": "plain",
                "SerializeData": "stable-ekispert-route-a",
                "Price": {"kind": "FareSummary", "Oneway": "210"},
                "Route": {
                    "timeOnBoard": "12",
                    "timeOther": "4",
                    "timeWalk": "6",
                    "distance": "31",
                    "transferCount": "0",
                    "Point": [
                        {"Name": "東京車站"},
                        {
                            "Station": {"Name": "東京"},
                            "GeoPoint": {"lati_d": "35.681236", "longi_d": "139.767125"},
                        },
                        {
                            "Station": {"Name": "淺草"},
                            "GeoPoint": {"lati_d": "35.710733", "longi_d": "139.797592"},
                        },
                    ],
                    "Line": [
                        {
                            # The official response may omit Type for the
                            # coordinate-to-station walking leg.
                            "Name": "徒歩",
                            "timeOnBoard": "6",
                            "distance": "4",
                        },
                        {
                            "Name": "東京メトロ銀座線",
                            "Type": "train",
                            "timeOnBoard": "12",
                            "distance": "27",
                            "stopStationCount": "7",
                            "Color": "255149000",
                            "LineSymbol": {"Name": "G"},
                            "Destination": "浅草",
                        },
                    ],
                },
            }
        ]
    }
}


ODSAY_SEOUL_ROUTES = {
    "result": {
        "path": [
            {
                "pathType": 1,
                "info": {
                    "totalTime": 18,
                    "totalDistance": 4100,
                    "payment": 1400,
                    "mapObj": "1:2@3:4",
                },
                "subPath": [
                    {
                        "trafficType": 3,
                        "sectionTime": 4,
                        "distance": 280,
                        "endName": "首爾站",
                    },
                    {
                        "trafficType": 1,
                        "sectionTime": 11,
                        "distance": 3500,
                        "stationCount": 3,
                        "startName": "首爾站",
                        "startX": 126.9707,
                        "startY": 37.5547,
                        "endName": "景福宮",
                        "endX": 126.9770,
                        "endY": 37.5796,
                        "way": "독립문 방면",
                        "door": "4-1",
                        "lane": [{"name": "수도권 3호선"}],
                        "passStopList": {
                            "stations": [{"stationName": "종로3가", "x": 126.9910, "y": 37.5716}]
                        },
                    },
                    {
                        "trafficType": 3,
                        "sectionTime": 3,
                        "distance": 220,
                        "endName": "景福宮",
                    },
                ],
            },
            {
                "pathType": 2,
                "info": {
                    "totalTime": 24,
                    "totalDistance": 4500,
                    "payment": 1500,
                    "mapObj": "5:6@7:8",
                },
                "subPath": [
                    {
                        "trafficType": 2,
                        "sectionTime": 20,
                        "distance": 4200,
                        "stationCount": 9,
                        "startName": "首爾站",
                        "endName": "景福宮",
                        "lane": [{"busNo": "1711"}],
                    }
                ],
            },
        ]
    }
}


@pytest.mark.asyncio
async def test_ekispert_uses_wgs84_points_and_parses_plain_route() -> None:
    seen: dict[str, str] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen.update(dict(request.url.params))
        assert request.url.path == "/v1/json/search/course/extreme"
        return httpx.Response(200, json=EKISPERT_TOKYO_ROUTE)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    settings = Settings(ekispert_api_key="ekispert-key", ekispert_monthly_request_limit=10)
    provider = EkispertRouteProvider(settings, client)
    departure = datetime(2026, 10, 3, 8, 30, tzinfo=ZoneInfo("Asia/Tokyo"))
    segment = await provider.compute(
        point("東京車站", 35.681236, 139.767125),
        point("淺草寺", 35.710733, 139.797592),
        departure,
        "FEWER_TRANSFERS",
    )
    await client.aclose()

    assert seen["key"] == "ekispert-key"
    assert seen["viaList"] == ("35.681236,139.767125,wgs84:35.710733,139.797592,wgs84")
    assert seen["gcs"] == "wgs84"
    assert seen["searchType"] == "plain"
    assert seen["date"] == "20261003"
    assert seen["sort"] == "transfer"
    assert segment is not None
    assert segment.provider == "ekispert" and segment.attribution == "Ekispert"
    assert segment.schedule_mode == "preview"
    assert segment.duration_minutes == 22 and segment.distance_meters == 3100
    assert segment.fare == Decimal("210") and segment.currency == "JPY"
    assert [step.travel_mode for step in segment.steps] == ["WALK", "TRANSIT"]
    assert segment.steps[1].line_short_name == "G"
    assert segment.steps[1].line_color == "#FF9500"
    assert segment.steps[1].headsign == "浅草"
    assert "headsign" in segment.details_available
    assert segment.encoded_polyline
    assert "平均等待時間" in segment.warnings[0]


@pytest.mark.asyncio
async def test_ekispert_probe_reports_provider_error_without_leaking_key() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            403,
            json={"ResultSet": {"Error": {"Message": "Access key is invalid"}}},
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = EkispertRouteProvider(Settings(ekispert_api_key="secret"), client)
    result = await provider.probe(
        point("東京", 35.6812, 139.7671), point("淺草", 35.7148, 139.7967)
    )
    await client.aclose()

    assert result == EkispertProbeResult(False, False, 403, "Access key is invalid")


@pytest.mark.asyncio
async def test_odsay_returns_multiple_korean_transit_options_from_one_request() -> None:
    calls = 0
    seen: dict[str, str] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        seen.update(dict(request.url.params))
        return httpx.Response(200, json=ODSAY_SEOUL_ROUTES)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = OdsayRouteProvider(Settings(odsay_api_key="server-key"), client)
    departure = datetime(2026, 10, 3, 9, 0, tzinfo=ZoneInfo("Asia/Seoul"))
    options = await provider.compute_options(
        point("首爾站", 37.5547, 126.9707),
        point("景福宮", 37.5796, 126.9770),
        departure,
        "FASTEST",
        max_options=3,
    )
    await client.aclose()

    assert calls == 1
    assert seen == {
        "apiKey": "server-key",
        "SX": "126.9707000",
        "SY": "37.5547000",
        "EX": "126.9770000",
        "EY": "37.5796000",
        "OPT": "0",
        "SearchType": "0",
        "SearchPathType": "0",
        "lang": "0",
        "output": "json",
    }
    assert len(options) == 2
    assert options[0].provider == "odsay" and options[0].attribution == "ODsay"
    assert options[0].duration_minutes == 18
    assert options[0].fare == Decimal("1400") and options[0].currency == "KRW"
    assert options[0].steps[1].line_name == "수도권 3호선"
    assert options[0].steps[1].recommended_car == "4-1"
    assert options[0].encoded_polyline
    assert "naver.com" in str(options[0].maps_url)
    assert options[0].schedule_mode == "preview"


@pytest.mark.asyncio
async def test_odsay_probe_handles_structured_no_result_error() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"error": {"code": "-99", "msg": "no result"}})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = OdsayRouteProvider(Settings(odsay_api_key="server-key"), client)
    result = await provider.probe(
        point("首爾", 37.5547, 126.9707), point("景福宮", 37.5796, 126.9770)
    )
    await client.aclose()

    assert result == OdsayProbeResult(False, False, 200, "-99")


def rapidapi_navitime(
    client: httpx.AsyncClient,
    redis: fakeredis.aioredis.FakeRedis | None = None,
    **overrides: int,
) -> NavitimeRouteProvider:
    return NavitimeRouteProvider(
        Settings(
            navitime_api_base_url="https://navitime-route-totalnavi.p.rapidapi.com",
            navitime_api_key="rapid-key",
            **overrides,
        ),
        client,
        redis,
    )


@pytest.mark.asyncio
async def test_navitime_rapidapi_request_and_section_parsing() -> None:
    seen: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url.copy_with(query=None))
        seen["headers"] = dict(request.headers)
        seen["params"] = dict(request.url.params)
        return httpx.Response(200, json=NAVITIME_GINZA_ROUTE)

    departure = (datetime.now(UTC) + timedelta(days=3)).replace(
        hour=23, minute=30, second=0, microsecond=0
    )
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    segment = await rapidapi_navitime(client).compute(
        point("表參道之丘", 35.6653, 139.7126),
        point("銀座三越", 35.6713, 139.7651),
        departure,
        "FEWER_TRANSFERS",
    )
    await client.aclose()

    assert seen["url"] == "https://navitime-route-totalnavi.p.rapidapi.com/route_transit"
    headers = cast(dict[str, str], seen["headers"])
    assert headers["x-rapidapi-key"] == "rapid-key"
    assert headers["x-rapidapi-host"] == "navitime-route-totalnavi.p.rapidapi.com"
    params = cast(dict[str, str], seen["params"])
    assert params["start"] == "35.665300,139.712600"
    assert params["goal"] == "35.671300,139.765100"
    # 23:30 UTC is 08:30 the next day in Japan; NAVITIME wants naive JST.
    assert params["start_time"] == (departure + timedelta(hours=9)).strftime("%Y-%m-%dT%H:%M:%S")
    assert params["order"] == "transit"
    assert params["limit"] == "1"
    assert params["shape"] == "true"
    assert "lang" not in params

    assert segment is not None
    assert segment.provider == "navitime" and segment.attribution == "NAVITIME"
    assert segment.schedule_mode == "scheduled"
    assert segment.duration_minutes == 23 and segment.distance_meters == 6400
    assert segment.fare == Decimal("170") and str(segment.fare) == "170"
    assert segment.currency == "JPY"
    assert segment.provider_route_key == "1"
    assert segment.encoded_polyline
    assert segment.maps_url and segment.maps_url.startswith("https://www.google.com/maps/dir/?")
    assert [step.travel_mode for step in segment.steps] == ["WALK", "TRANSIT", "WALK"]
    walk_in, ride, walk_out = segment.steps
    assert walk_in.instruction == "步行前往 表参道"
    assert walk_in.departure_stop is None and walk_in.line_name is None
    assert walk_in.duration_minutes == 5 and walk_in.distance_meters == 400
    assert ride.instruction == "搭乘 東京メトロ銀座線（普通）"
    assert ride.line_name == "東京メトロ銀座線" and ride.line_color == "#FF9500"
    assert ride.departure_stop == "表参道" and ride.arrival_stop == "銀座"
    assert ride.headsign == "浅草"
    assert ride.platform == "1" and ride.exit_name == "A3"
    assert ride.recommended_car == "前方第 2 節"
    assert ride.departure_time == datetime(2026, 10, 3, 8, 6, tzinfo=ZoneInfo("Asia/Tokyo"))
    assert ride.arrival_time == datetime(2026, 10, 3, 8, 19, tzinfo=ZoneInfo("Asia/Tokyo"))
    assert walk_out.instruction == "步行前往 銀座三越"
    assert {"steps", "stops", "headsign", "platform", "exit", "recommended_car"} <= set(
        segment.details_available
    )


@pytest.mark.asyncio
async def test_navitime_direct_contract_uses_client_id_path_and_language() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url.copy_with(query=None)) == (
            "https://api.navitime.biz/cid-1/v1/route_transit"
        )
        assert request.headers["x-api-key"] == "secret"
        assert "x-rapidapi-key" not in request.headers
        assert request.url.params["lang"] == "zh-TW"
        return httpx.Response(200, json=NAVITIME_GINZA_ROUTE)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = NavitimeRouteProvider(
        Settings(
            navitime_api_base_url="https://api.navitime.biz/",
            navitime_client_id="cid-1",
            navitime_api_key="secret",
        ),
        client,
    )
    segment = await provider.compute(
        point("表參道", 35.6653, 139.7126),
        point("銀座", 35.6713, 139.7651),
        None,
        "FASTEST",
    )
    await client.aclose()

    assert segment is not None and segment.schedule_mode == "live"
    assert segment.steps[1].line_name == "東京メトロ銀座線"


@pytest.mark.asyncio
async def test_navitime_returns_multiple_routes_with_provider_shapes() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["shape"] == "true"
        assert request.url.params["limit"] == "3"
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "summary": {
                            "no": str(index),
                            "move": {"type": "move", "time": 10 + index, "distance": 1000 + index},
                        },
                        "sections": [],
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
    options = await rapidapi_navitime(client).compute_options(
        point("上野", 35.7, 139.7),
        point("淺草", 35.71, 139.8),
        datetime.now(UTC),
        "FEWER_TRANSFERS",
        max_options=3,
    )
    await client.aclose()

    assert len(options) == 3
    assert [option.provider_route_key for option in options] == ["1", "2", "3"]
    assert [option.route_option_rank for option in options] == [1, 2, 3]
    assert [option.duration_minutes for option in options] == [11, 12, 13]
    assert all(option.encoded_polyline for option in options)
    assert all(option.fare is None and option.currency is None for option in options)


@pytest.mark.asyncio
async def test_navitime_reports_gateway_errors_without_inventing_routes() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"message": "You are not subscribed to this API."})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = rapidapi_navitime(client)
    probe = await provider.probe(point("東京", 35.6812, 139.7671), point("淺草", 35.7148, 139.7967))
    options = await provider.compute_options(
        point("東京", 35.6812, 139.7671),
        point("淺草", 35.7148, 139.7967),
        None,
        "FEWER_TRANSFERS",
    )
    await client.aclose()

    assert probe == NavitimeProbeResult(
        False, False, status_code=403, error_code="You are not subscribed to this API."
    )
    assert options == []


@pytest.mark.asyncio
async def test_navitime_probe_distinguishes_empty_routes_from_failures() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"items": [], "unit": {"currency": "JPY"}})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    probe = await rapidapi_navitime(client).probe(
        point("東京", 35.6812, 139.7671), point("淺草", 35.7148, 139.7967)
    )
    await client.aclose()

    assert probe == NavitimeProbeResult(True, False, status_code=200)
    assert await NavitimeRouteProvider(Settings()).probe(
        point("東京", 35.6812, 139.7671), point("淺草", 35.7148, 139.7967)
    ) == NavitimeProbeResult(False, False, error_code="NOT_CONFIGURED")


@pytest.mark.asyncio
async def test_navitime_monthly_budget_stops_requests_when_exhausted() -> None:
    calls = 0

    async def handler(_: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(200, json=NAVITIME_GINZA_ROUTE)

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = rapidapi_navitime(client, redis, navitime_monthly_request_limit=1)
    origin, destination = point("東京", 35.6812, 139.7671), point("淺草", 35.7148, 139.7967)
    first = await provider.compute_options(origin, destination, None, "FEWER_TRANSFERS")
    second = await provider.compute_options(origin, destination, None, "FEWER_TRANSFERS")
    probe = await provider.probe(origin, destination)
    await client.aclose()

    assert len(first) == 1 and second == []
    assert probe == NavitimeProbeResult(False, False, error_code="MONTHLY_BUDGET_EXHAUSTED")
    assert calls == 1
    usage = await navitime_usage_snapshot(redis, monthly_limit=1)
    assert usage.used == 1 and usage.remaining == 0
    assert usage.breakdown == {"route_transit": 1}


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
async def test_japan_transit_prefers_ekispert_when_configured() -> None:
    service = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(ekispert_api_key="key", route_cache_ttl_seconds=300),
        google=UnexpectedProvider(),
        navitime=UnexpectedProvider(),
        ekispert=WorkingProvider(),
    )
    segment = await service.compute(
        point("A", 35.1, 139.1),
        point("B", 35.2, 139.2),
        None,
        "FEWER_TRANSFERS",
        region_code="JP",
    )
    assert segment is not None and segment.provider == "working"


@pytest.mark.asyncio
async def test_korean_transit_uses_odsay_and_not_naver_directions() -> None:
    service = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(odsay_api_key="server-key", route_cache_ttl_seconds=300),
        google=UnexpectedProvider(),
        naver=UnexpectedProvider(),
        odsay=WorkingProvider(),
    )
    segment = await service.compute(
        point("A", 37.55, 126.97),
        point("B", 37.58, 126.98),
        None,
        "FEWER_TRANSFERS",
        region_code="KR",
        travel_mode="transit",
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
    rapidapi = Settings(
        navitime_api_base_url="https://navitime-route-totalnavi.p.rapidapi.com",
        navitime_api_key="secret",
    )
    direct_without_client = Settings(
        navitime_api_base_url="https://api.navitime.biz",
        navitime_api_key="secret",
    )
    direct = Settings(
        navitime_api_base_url="https://api.navitime.biz",
        navitime_client_id="client",
        navitime_api_key="secret",
    )

    assert route_provider_configured(google_only, "JP", "transit") is False
    assert route_provider_configured(rapidapi, "JP", "transit") is True
    assert rapidapi.navitime_rapidapi is True
    assert route_provider_configured(direct_without_client, "JP", "transit") is False
    assert route_provider_configured(direct, "JP", "transit") is True
    assert direct.navitime_rapidapi is False
    assert route_provider_configured(google_only, "JP", "walk") is True
    assert route_provider_configured(Settings(ekispert_api_key="key"), "JP", "transit") is True
    assert route_provider_configured(Settings(odsay_api_key="key"), "KR", "transit") is True
    assert route_provider_configured(google_only, "KR", "transit") is False


def test_navitime_base_url_is_pinned_to_official_gateways() -> None:
    field = "navitime_api_base_url"
    assert official_provider_url_ok(field, "https://navitime-route-totalnavi.p.rapidapi.com")
    assert official_provider_url_ok(field, "https://api.navitime.biz")
    assert official_provider_url_ok(field, "https://api-sdk.navitime.co.jp")
    assert not official_provider_url_ok(field, "https://other-api.p.rapidapi.com")
    assert not official_provider_url_ok(field, "https://navitime.co.jp.example.test")
    assert not official_provider_url_ok(field, "http://navitime-route-totalnavi.p.rapidapi.com")
    assert official_provider_url_ok("line_api_base_url", "https://api.line.me")
    assert not official_provider_url_ok("line_api_base_url", "https://evil.api.line.me")
    assert official_provider_url_ok("ekispert_api_base_url", "https://api.ekispert.jp")
    assert not official_provider_url_ok(
        "ekispert_api_base_url", "https://api.ekispert.jp.example.test"
    )
    assert official_provider_url_ok("odsay_api_base_url", "https://api.odsay.com/v1/api")
    assert not official_provider_url_ok("odsay_api_base_url", "https://odsay.example.test")


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
async def test_route_cache_keys_ekispert_plain_search_by_date_only() -> None:
    provider = CountingProvider()
    service = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(ekispert_api_key="key", ekispert_search_type="plain"),
        google=UnexpectedProvider(),
        navitime=UnexpectedProvider(),
        ekispert=provider,
    )
    morning = datetime(2026, 11, 10, 9, 0, tzinfo=ZoneInfo("Asia/Tokyo"))

    # ``plain`` only sends the date, so every departure on the same day is one request.
    for departure in (morning, morning + timedelta(minutes=47), morning + timedelta(hours=6)):
        await service.compute(
            point("A", 35.1, 139.1),
            point("B", 35.2, 139.2),
            departure,
            "FEWER_TRANSFERS",
            region_code="JP",
            travel_mode="transit",
        )
    assert provider.calls == 1

    await service.compute(
        point("A", 35.1, 139.1),
        point("B", 35.2, 139.2),
        morning + timedelta(days=1),
        "FEWER_TRANSFERS",
        region_code="JP",
        travel_mode="transit",
    )
    assert provider.calls == 2


@pytest.mark.asyncio
async def test_route_cache_buckets_ekispert_departure_search_by_ten_minutes() -> None:
    provider = CountingProvider()
    service = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(ekispert_api_key="key", ekispert_search_type="departure"),
        google=UnexpectedProvider(),
        navitime=UnexpectedProvider(),
        ekispert=provider,
    )
    morning = datetime(2026, 11, 10, 9, 0, tzinfo=ZoneInfo("Asia/Tokyo"))

    for minutes, expected_calls in ((0, 1), (5, 1), (12, 2)):
        await service.compute(
            point("A", 35.1, 139.1),
            point("B", 35.2, 139.2),
            morning + timedelta(minutes=minutes),
            "FEWER_TRANSFERS",
            region_code="JP",
            travel_mode="transit",
        )
        assert provider.calls == expected_calls


@pytest.mark.asyncio
async def test_route_cache_ignores_departure_time_for_odsay_and_walking() -> None:
    odsay = CountingProvider()
    korea = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(odsay_api_key="server-key"),
        google=UnexpectedProvider(),
        naver=UnexpectedProvider(),
        odsay=odsay,
    )
    seoul_morning = datetime(2026, 11, 10, 9, 0, tzinfo=ZoneInfo("Asia/Seoul"))
    for departure in (None, seoul_morning, seoul_morning + timedelta(days=3)):
        await korea.compute(
            point("A", 37.55, 126.97),
            point("B", 37.58, 126.98),
            departure,
            "FEWER_TRANSFERS",
            region_code="KR",
            travel_mode="transit",
        )
    assert odsay.calls == 1

    google = CountingProvider()
    walking = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(),
        google=google,
    )
    tokyo_morning = datetime(2026, 11, 10, 9, 0, tzinfo=ZoneInfo("Asia/Tokyo"))
    for departure in (None, tokyo_morning, tokyo_morning + timedelta(hours=5)):
        await walking.compute(
            point("A", 35.1, 139.1),
            point("B", 35.2, 139.2),
            departure,
            "FEWER_TRANSFERS",
            japan=False,
            travel_mode="walk",
        )
    assert google.calls == 1


@pytest.mark.asyncio
async def test_route_cache_buckets_google_transit_and_driving_departures() -> None:
    provider = CountingProvider()
    service = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(),
        google=provider,
    )
    origin, destination = point("A", 35.1, 139.1), point("B", 35.2, 139.2)
    nine = datetime(2026, 11, 10, 9, 0, tzinfo=ZoneInfo("Asia/Tokyo"))

    await service.compute(origin, destination, nine, "FASTEST", japan=False, travel_mode="transit")
    await service.compute(
        origin,
        destination,
        nine + timedelta(minutes=9),
        "FASTEST",
        japan=False,
        travel_mode="transit",
    )
    assert provider.calls == 1
    await service.compute(
        origin,
        destination,
        nine + timedelta(minutes=10),
        "FASTEST",
        japan=False,
        travel_mode="transit",
    )
    assert provider.calls == 2

    # A different mode at the same time is a different request.
    await service.compute(origin, destination, nine, "FASTEST", japan=False, travel_mode="drive")
    assert provider.calls == 3
    await service.compute(
        origin,
        destination,
        nine + timedelta(minutes=14),
        "FASTEST",
        japan=False,
        travel_mode="drive",
    )
    assert provider.calls == 3
    await service.compute(
        origin,
        destination,
        nine + timedelta(minutes=15),
        "FASTEST",
        japan=False,
        travel_mode="drive",
    )
    assert provider.calls == 4


def test_estimate_leg_minutes_matches_the_web_planner() -> None:
    station = point("東京車站", 35.6812, 139.7671)
    temple = point("淺草寺", 35.7148, 139.7967)

    # About 4.6 km apart: 61 minutes on foot, 24 by transit, 14 by car, each rounded up
    # to five minutes; the same figures ``estimateLegMinutes`` returns in the web app.
    assert estimate_leg_minutes(station, temple, "walk") == 65
    assert estimate_leg_minutes(station, temple, "transit") == 25
    assert estimate_leg_minutes(station, temple, "drive") == 15
    assert estimate_leg_minutes(station, point("隔壁", 35.6815, 139.7675), "walk") == 5


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
    daytime_utc = datetime.fromisoformat(str(bodies[-2]["departureTime"]).replace("Z", "+00:00"))
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
