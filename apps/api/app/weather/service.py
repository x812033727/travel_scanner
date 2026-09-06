"""Pick the trip weather provider and fall back to the other one when it fails."""

from __future__ import annotations

from typing import Protocol

from redis.asyncio import Redis

from app.config import Settings
from app.problems import AppError
from app.weather.google import GoogleWeatherService
from app.weather.met_norway import MetNorwayWeatherService
from app.weather.schemas import TripWeather


class WeatherProvider(Protocol):
    @property
    def configured(self) -> bool: ...

    async def lookup(
        self,
        *,
        latitude: float,
        longitude: float,
        location_name: str,
        language_code: str = "zh-TW",
        timezone: str | None = None,
    ) -> TripWeather: ...


class TripWeatherService:
    """MET Norway by default (free, commercial use allowed); Google Weather as backup.

    ``weather_provider`` flips the order. A provider that is not configured is skipped,
    and the first provider's error is what the caller sees when every one of them fails,
    so the admin panel keeps pointing at the provider that was actually asked first.
    """

    def __init__(
        self,
        redis: Redis,
        settings: Settings,
        *,
        met_norway: WeatherProvider | None = None,
        google: WeatherProvider | None = None,
    ) -> None:
        self.settings = settings
        self.met_norway: WeatherProvider = met_norway or MetNorwayWeatherService(redis, settings)
        self.google: WeatherProvider = google or GoogleWeatherService(redis, settings)

    @property
    def providers(self) -> list[WeatherProvider]:
        if self.settings.weather_provider == "google":
            return [self.google, self.met_norway]
        return [self.met_norway, self.google]

    @property
    def configured(self) -> bool:
        return any(provider.configured for provider in self.providers)

    async def lookup(
        self,
        *,
        latitude: float,
        longitude: float,
        location_name: str,
        language_code: str = "zh-TW",
        timezone: str | None = None,
    ) -> TripWeather:
        first_error: AppError | None = None
        for provider in self.providers:
            if not provider.configured:
                continue
            try:
                return await provider.lookup(
                    latitude=latitude,
                    longitude=longitude,
                    location_name=location_name,
                    language_code=language_code,
                    timezone=timezone,
                )
            except AppError as exc:
                first_error = first_error or exc
        if first_error is not None:
            raise first_error
        raise AppError(503, "weather_not_configured", "天氣服務尚未設定")
