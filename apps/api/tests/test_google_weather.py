from __future__ import annotations

import logging
from datetime import date
from typing import Any

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.hotspots.guides import GOOGLE_API_KEY_HEADER
from app.problems import AppError
from app.providers.usage_meter import google_maps_usage_snapshot
from app.weather.google import GoogleWeatherService


def current_fixture() -> dict[str, Any]:
    return {
        "currentTime": "2026-09-01T03:15:00Z",
        "timeZone": {"id": "Asia/Tokyo"},
        "isDaytime": True,
        "weatherCondition": {
            "description": {"text": "晴時多雲", "languageCode": "zh-TW"},
            "type": "PARTLY_CLOUDY",
        },
        "temperature": {"degrees": 28.4, "unit": "CELSIUS"},
        "feelsLikeTemperature": {"degrees": 30.1, "unit": "CELSIUS"},
        "relativeHumidity": 66,
        "uvIndex": 5,
        "precipitation": {"probability": {"percent": 20, "type": "RAIN"}},
        "wind": {"speed": {"value": 12, "unit": "KILOMETERS_PER_HOUR"}},
    }


def daily_fixture() -> dict[str, Any]:
    return {
        "timeZone": {"id": "Asia/Tokyo"},
        "forecastDays": [
            {
                "displayDate": {"year": 2026, "month": 9, "day": 1},
                "daytimeForecast": {
                    "weatherCondition": {
                        "description": {"text": "局部短暫雨", "languageCode": "zh-TW"},
                        "type": "SHOWERS",
                    },
                    "relativeHumidity": 70,
                    "uvIndex": 6,
                    "precipitation": {"probability": {"percent": 45, "type": "RAIN"}},
                    "wind": {"speed": {"value": 14, "unit": "KILOMETERS_PER_HOUR"}},
                },
                "nighttimeForecast": {
                    "relativeHumidity": 82,
                    "uvIndex": 0,
                    "precipitation": {"probability": {"percent": 60, "type": "RAIN"}},
                    "wind": {"speed": {"value": 9, "unit": "KILOMETERS_PER_HOUR"}},
                },
                "maxTemperature": {"degrees": 31.2, "unit": "CELSIUS"},
                "minTemperature": {"degrees": 24.8, "unit": "CELSIUS"},
                "sunEvents": {
                    "sunriseTime": "2026-08-31T20:12:00Z",
                    "sunsetTime": "2026-09-01T09:05:00Z",
                },
            }
        ],
    }


@pytest.mark.asyncio
@pytest.mark.parametrize("borrowed_client", [True, False], ids=["borrowed", "owned"])
async def test_google_weather_normalizes_and_caches_current_and_daily_results(
    borrowed_client: bool, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    calls: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if request.url.path.endswith("currentConditions:lookup"):
            return httpx.Response(200, json=current_fixture())
        return httpx.Response(200, json=daily_fixture())

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    real_client = httpx.AsyncClient
    created: list[httpx.AsyncClient] = []

    def make_client(**kwargs: Any) -> httpx.AsyncClient:
        client = real_client(transport=httpx.MockTransport(handler), **kwargs)
        created.append(client)
        return client

    client = (
        make_client(headers={GOOGLE_API_KEY_HEADER: "unrelated-caller-key", "X-Caller": "keep"})
        if borrowed_client
        else None
    )
    if not borrowed_client:
        monkeypatch.setattr(httpx, "AsyncClient", make_client)
    service = GoogleWeatherService(
        redis,
        Settings(google_maps_api_key="server-key", weather_cache_ttl_seconds=900),
        client,
    )

    try:
        with caplog.at_level(logging.INFO, logger="httpx"):
            weather = await service.lookup(
                latitude=35.6812,
                longitude=139.7671,
                location_name="東京車站",
            )
            cached = await service.lookup(
                latitude=35.6812,
                longitude=139.7671,
                location_name="東京都",
            )
        if client is not None:
            assert not client.is_closed
            assert client.headers[GOOGLE_API_KEY_HEADER] == "unrelated-caller-key"
            assert all(request.headers["X-Caller"] == "keep" for request in calls)
        else:
            assert len(created) == 2
            assert all(item.is_closed for item in created)
    finally:
        if client is not None:
            await client.aclose()

    assert len(calls) == 2
    assert {request.url.path for request in calls} == {
        "/v1/currentConditions:lookup",
        "/v1/forecast/days:lookup",
    }
    for request in calls:
        assert request.headers.get(GOOGLE_API_KEY_HEADER) == "server-key"
        assert "key" not in request.url.params
        assert "server-key" not in str(request.url)
        assert request.url.params["location.latitude"] == "35.681200"
        assert request.url.params["location.longitude"] == "139.767100"
        assert request.url.params["unitsSystem"] == "METRIC"
        if request.url.path.endswith("days:lookup"):
            assert request.url.params["days"] == request.url.params["pageSize"] == "10"
    request_logs = [record.getMessage() for record in caplog.records if record.name == "httpx"]
    assert len(request_logs) == 2
    assert all("server-key" not in message for message in request_logs)
    assert all(request.url.params["languageCode"] == "zh-TW" for request in calls)
    assert weather.current is not None
    assert weather.current.temperature_c == 28.4
    assert weather.current.feels_like_c == 30.1
    assert weather.days[0].date == date(2026, 9, 1)
    assert weather.days[0].precipitation_probability_percent == 60
    assert weather.days[0].relative_humidity_percent == 82
    assert weather.days[0].wind_speed_kph == 14
    assert weather.available_start_date == date(2026, 9, 1)
    assert cached.cache_status == "hit"
    assert cached.location_name == "東京都"
    assert await redis.ttl(next(iter(await redis.keys("weather:google:*")))) > 0

    usage = await google_maps_usage_snapshot(redis, 10_000)
    assert usage.breakdown["weather_current"] == 1
    assert usage.breakdown["weather_daily_forecast"] == 1
    await redis.aclose()


@pytest.mark.asyncio
async def test_google_weather_returns_partial_result_when_daily_forecast_fails() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("currentConditions:lookup"):
            return httpx.Response(200, json=current_fixture())
        return httpx.Response(503, json={"error": {"status": "UNAVAILABLE"}})

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = GoogleWeatherService(redis, Settings(google_maps_api_key="key"), client)

    weather = await service.lookup(
        latitude=35.6812,
        longitude=139.7671,
        location_name="東京車站",
    )

    assert weather.current is not None
    assert weather.days == []
    assert weather.warnings == ["weather_daily_unavailable"]
    await client.aclose()
    await redis.aclose()


@pytest.mark.asyncio
async def test_google_weather_reports_disabled_api_without_leaking_provider_detail() -> None:
    async def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            403,
            json={
                "error": {
                    "status": "PERMISSION_DENIED",
                    "message": "secret project and key details",
                }
            },
        )

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = GoogleWeatherService(redis, Settings(google_maps_api_key="key"), client)

    with pytest.raises(AppError) as captured:
        await service.lookup(
            latitude=35.6812,
            longitude=139.7671,
            location_name="東京車站",
        )

    assert captured.value.code == "weather_api_not_enabled"
    assert "secret" not in captured.value.detail
    await client.aclose()
    await redis.aclose()
