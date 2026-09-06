from __future__ import annotations

from datetime import date
from typing import Any

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.problems import AppError
from app.weather.met_norway import MetNorwayWeatherService, describe_symbol


def _entry(
    time: str,
    *,
    temperature: float,
    humidity: float,
    wind: float,
    uv: float,
    feels_like: float | None = None,
    hourly: tuple[str, float] | None = None,
    six_hourly: tuple[str, float, float, float] | None = None,
) -> dict[str, Any]:
    instant: dict[str, Any] = {
        "air_temperature": temperature,
        "relative_humidity": humidity,
        "wind_speed": wind,
        "ultraviolet_index_clear_sky": uv,
    }
    if feels_like is not None:
        instant["apparent_air_temperature"] = feels_like
    data: dict[str, Any] = {"instant": {"details": instant}}
    if hourly is not None:
        data["next_1_hours"] = {
            "summary": {"symbol_code": hourly[0]},
            "details": {"precipitation_amount": hourly[1]},
        }
    if six_hourly is not None:
        data["next_6_hours"] = {
            "summary": {"symbol_code": six_hourly[0]},
            "details": {
                "air_temperature_min": six_hourly[1],
                "air_temperature_max": six_hourly[2],
                "precipitation_amount": six_hourly[3],
            },
        }
    return {"time": time, "data": data}


def forecast_fixture() -> dict[str, Any]:
    """Two Tokyo days: a rainy hourly morning that thins out to six-hour steps."""
    return {
        "type": "Feature",
        "properties": {
            "meta": {"units": {"air_temperature": "celsius", "wind_speed": "m/s"}},
            "timeseries": [
                _entry(
                    "2026-09-06T00:00:00Z",
                    temperature=22.2,
                    feels_like=24.0,
                    humidity=88.5,
                    wind=2.5,
                    uv=3.2,
                    hourly=("heavyrain", 4.6),
                    six_hourly=("heavyrain", 21.9, 22.7, 28.6),
                ),
                _entry(
                    "2026-09-06T01:00:00Z",
                    temperature=22.5,
                    humidity=90,
                    wind=3.0,
                    uv=4.0,
                    hourly=("rain", 2.0),
                    six_hourly=("rain", 22.0, 23.0, 10.0),
                ),
                _entry(
                    "2026-09-06T02:00:00Z",
                    temperature=23.0,
                    humidity=85,
                    wind=4.0,
                    uv=5.6,
                    hourly=("lightrain", 0.4),
                    six_hourly=("partlycloudy_day", 22.5, 26.0, 1.0),
                ),
                _entry(
                    "2026-09-06T06:00:00Z",
                    temperature=25.5,
                    humidity=70,
                    wind=5.0,
                    uv=6.0,
                    six_hourly=("partlycloudy_day", 21.0, 26.5, 0.6),
                ),
                _entry(
                    "2026-09-06T12:00:00Z",
                    temperature=21.0,
                    humidity=80,
                    wind=2.0,
                    uv=0.0,
                    six_hourly=("cloudy", 19.5, 21.5, 0.0),
                ),
                _entry(
                    "2026-09-07T03:00:00Z",
                    temperature=27.0,
                    humidity=60,
                    wind=3.0,
                    uv=7.4,
                    six_hourly=("clearsky_day", 24.0, 29.0, 0.0),
                ),
                _entry(
                    "2026-09-07T09:00:00Z",
                    temperature=25.0,
                    humidity=65,
                    wind=2.0,
                    uv=1.0,
                    six_hourly=("fair_night", 22.0, 25.5, 0.0),
                ),
            ],
        },
    }


def _service(
    handler: httpx.MockTransport, settings: Settings | None = None
) -> tuple[MetNorwayWeatherService, fakeredis.aioredis.FakeRedis]:
    redis = fakeredis.aioredis.FakeRedis()
    client = httpx.AsyncClient(transport=handler)
    return MetNorwayWeatherService(redis, settings or Settings(), client), redis


@pytest.mark.asyncio
async def test_met_norway_identifies_itself_and_buckets_the_forecast_into_trip_days() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=forecast_fixture())

    service, redis = _service(httpx.MockTransport(handler))
    weather = await service.lookup(
        latitude=35.68123,
        longitude=139.76712,
        location_name="東京車站",
        language_code="zh-TW",
        timezone="Asia/Tokyo",
    )

    # Terms of service: an identifying User-Agent, coordinates with at most four decimals.
    assert requests[0].headers["user-agent"] == "Mokaair/1.0 (+https://mokaair.com)"
    assert requests[0].url.params["lat"] == "35.6812"
    assert requests[0].url.params["lon"] == "139.7671"
    assert requests[0].url.path == "/weatherapi/locationforecast/2.0/complete"

    assert weather.source == "met_norway"
    assert weather.attribution == "MET Norway"
    assert weather.timezone == "Asia/Tokyo"
    assert weather.current is not None
    assert weather.current.temperature_c == 22.2
    assert weather.current.feels_like_c == 24.0
    assert weather.current.relative_humidity_percent == 89
    assert weather.current.wind_speed_kph == 9.0
    assert weather.current.uv_index == 3
    assert weather.current.condition.type == "HEAVY_RAIN"
    assert weather.current.condition.description == "大雨"
    # 00:00Z is 09:00 in Tokyo, so a symbol without a day/night suffix still reads as day.
    assert weather.current.is_daytime is True

    assert [day.date for day in weather.days] == [date(2026, 9, 6), date(2026, 9, 7)]
    first, second = weather.days
    assert (first.min_temperature_c, first.max_temperature_c) == (19.5, 26.5)
    assert first.relative_humidity_percent == 90
    assert first.wind_speed_kph == 18.0
    # UV only counts daytime hours: the 21:00 entry is left out.
    assert first.uv_index == 6
    # Hourly totals cover the morning, six-hour totals the rest; nothing is counted twice.
    assert first.precipitation_mm == 7.6
    assert first.precipitation_probability_percent is None
    # The symbol closest to noon (11:00) describes the day.
    assert first.condition.type == "PARTLY_CLOUDY"
    assert first.condition.description == "多雲時晴"
    assert (second.min_temperature_c, second.max_temperature_c) == (22.0, 29.0)
    assert second.condition.type == "CLEAR"
    assert second.uv_index == 7
    assert weather.available_start_date == date(2026, 9, 6)
    assert weather.available_end_date == date(2026, 9, 7)

    cached = await service.lookup(
        latitude=35.68123,
        longitude=139.76712,
        location_name="東京",
        language_code="zh-TW",
        timezone="Asia/Tokyo",
    )
    assert cached.cache_status == "hit"
    assert cached.location_name == "東京"
    assert len(requests) == 1
    assert await redis.ttl(next(iter(await redis.keys("weather:met:*")))) > 0


@pytest.mark.asyncio
async def test_met_norway_rejection_and_outages_become_planner_errors() -> None:
    rejected, _ = _service(httpx.MockTransport(lambda _request: httpx.Response(403)))
    with pytest.raises(AppError) as forbidden:
        await rejected.lookup(latitude=35.6812, longitude=139.7671, location_name="東京")
    assert forbidden.value.code == "weather_provider_rejected"

    throttled, _ = _service(httpx.MockTransport(lambda _request: httpx.Response(429)))
    with pytest.raises(AppError) as limited:
        await throttled.lookup(latitude=35.6812, longitude=139.7671, location_name="東京")
    assert limited.value.code == "weather_rate_limited"

    empty, _ = _service(
        httpx.MockTransport(
            lambda _request: httpx.Response(200, json={"properties": {"timeseries": []}})
        )
    )
    with pytest.raises(AppError) as invalid:
        await empty.lookup(latitude=35.6812, longitude=139.7671, location_name="東京")
    assert invalid.value.code == "weather_response_invalid"


def test_met_norway_is_not_configured_without_a_user_agent() -> None:
    service = MetNorwayWeatherService(
        fakeredis.aioredis.FakeRedis(), Settings(met_norway_user_agent="  ")
    )
    assert service.configured is False


def test_symbol_codes_map_to_planner_conditions_in_every_locale() -> None:
    assert describe_symbol("lightrainshowers_night", "zh-TW").model_dump() == {
        "description": "小陣雨",
        "type": "LIGHT_RAIN_SHOWERS",
    }
    assert describe_symbol("lightrainshowers_night", "en").description == "Light rain showers"
    assert describe_symbol("heavysnow", "ja").model_dump() == {
        "description": "強い雪",
        "type": "HEAVY_SNOW",
    }
    assert describe_symbol("rainandthunder", "ko").model_dump() == {
        "description": "뇌우",
        "type": "THUNDERSTORM",
    }
    # MET's own misspelling keeps its meaning, and thunder never carries an intensity.
    assert describe_symbol("lightssleetshowersandthunder", "en").description == "Thunderstorm"
    assert describe_symbol("fair_day", "zh-CN").model_dump() == {
        "description": "晴时多云",
        "type": "MOSTLY_CLEAR",
    }
    assert describe_symbol("sleetshowers_day", "en").type == "SLEET_SHOWERS"
    assert describe_symbol("fog", "ja").description == "霧"
    assert describe_symbol(None, "en").type == "WEATHER_CONDITION_UNSPECIFIED"
    assert describe_symbol("clearsky_day", "fr").description == "Clear sky"
