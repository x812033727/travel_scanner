from __future__ import annotations

from datetime import UTC, datetime, timedelta

import fakeredis.aioredis
import pytest

from app.config import Settings
from app.problems import AppError
from app.weather.schemas import TripWeather
from app.weather.service import TripWeatherService


def _forecast(source: str) -> TripWeather:
    now = datetime.now(UTC)
    return TripWeather(
        source=source,
        attribution=source,
        location_name="東京",
        latitude=35.6812,
        longitude=139.7671,
        retrieved_at=now,
        expires_at=now + timedelta(minutes=15),
    )


class Provider:
    def __init__(self, name: str, *, configured: bool = True, error: AppError | None = None):
        self.name = name
        self._configured = configured
        self.error = error
        self.calls = 0

    @property
    def configured(self) -> bool:
        return self._configured

    async def lookup(self, **_kwargs: object) -> TripWeather:
        self.calls += 1
        if self.error is not None:
            raise self.error
        return _forecast(self.name)


def _service(settings: Settings, met: Provider, google: Provider) -> TripWeatherService:
    return TripWeatherService(
        fakeredis.aioredis.FakeRedis(), settings, met_norway=met, google=google
    )


@pytest.mark.asyncio
async def test_met_norway_answers_first_and_google_is_only_a_fallback() -> None:
    met, google = Provider("met_norway"), Provider("google_weather")
    weather = await _service(Settings(), met, google).lookup(
        latitude=35.6812, longitude=139.7671, location_name="東京"
    )
    assert weather.source == "met_norway"
    assert (met.calls, google.calls) == (1, 0)

    failing = Provider("met_norway", error=AppError(502, "weather_provider_unavailable", "down"))
    weather = await _service(Settings(), failing, google).lookup(
        latitude=35.6812, longitude=139.7671, location_name="東京"
    )
    assert weather.source == "google_weather"


@pytest.mark.asyncio
async def test_weather_provider_setting_puts_google_first() -> None:
    met, google = Provider("met_norway"), Provider("google_weather")
    weather = await _service(Settings(weather_provider="google"), met, google).lookup(
        latitude=35.6812, longitude=139.7671, location_name="東京"
    )
    assert weather.source == "google_weather"
    assert (met.calls, google.calls) == (0, 1)


@pytest.mark.asyncio
async def test_first_provider_error_is_reported_when_every_provider_fails() -> None:
    met = Provider("met_norway", error=AppError(503, "weather_provider_rejected", "ua"))
    google = Provider("google_weather", error=AppError(502, "weather_provider_unavailable", "x"))
    with pytest.raises(AppError) as failure:
        await _service(Settings(), met, google).lookup(
            latitude=35.6812, longitude=139.7671, location_name="東京"
        )
    assert failure.value.code == "weather_provider_rejected"

    nothing = _service(
        Settings(),
        Provider("met_norway", configured=False),
        Provider("google_weather", configured=False),
    )
    assert nothing.configured is False
    with pytest.raises(AppError) as unconfigured:
        await nothing.lookup(latitude=35.6812, longitude=139.7671, location_name="東京")
    assert unconfigured.value.code == "weather_not_configured"
