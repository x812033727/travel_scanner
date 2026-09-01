from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class WeatherCondition(BaseModel):
    description: str
    type: str


class CurrentWeather(BaseModel):
    observed_at: datetime
    is_daytime: bool
    condition: WeatherCondition
    temperature_c: float
    feels_like_c: float
    relative_humidity_percent: int | None = Field(default=None, ge=0, le=100)
    precipitation_probability_percent: int | None = Field(default=None, ge=0, le=100)
    wind_speed_kph: float | None = Field(default=None, ge=0)
    uv_index: int | None = Field(default=None, ge=0)


class DailyWeather(BaseModel):
    date: date
    condition: WeatherCondition
    min_temperature_c: float
    max_temperature_c: float
    relative_humidity_percent: int | None = Field(default=None, ge=0, le=100)
    precipitation_probability_percent: int | None = Field(default=None, ge=0, le=100)
    wind_speed_kph: float | None = Field(default=None, ge=0)
    uv_index: int | None = Field(default=None, ge=0)
    sunrise_at: datetime | None = None
    sunset_at: datetime | None = None


class TripWeather(BaseModel):
    source: str = "google_weather"
    attribution: str = "Google Weather"
    location_name: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone: str | None = None
    current: CurrentWeather | None = None
    days: list[DailyWeather] = Field(default_factory=list)
    available_start_date: date | None = None
    available_end_date: date | None = None
    retrieved_at: datetime
    expires_at: datetime
    cache_status: str = "fresh"
    warnings: list[str] = Field(default_factory=list)
