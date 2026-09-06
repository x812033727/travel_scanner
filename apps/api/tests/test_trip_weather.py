from datetime import UTC, date, datetime, timedelta
from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest

import app.trips.router as trips_router
from app.config import Settings
from app.weather.schemas import (
    CurrentWeather,
    DailyWeather,
    TripWeather,
    WeatherCondition,
)


@pytest.mark.asyncio
async def test_trip_weather_uses_an_owned_trip_coordinate_and_marks_future_dates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    trip_id = uuid4()
    user_id = uuid4()
    observed_owner: list[tuple[UUID, UUID]] = []
    observed_limits: list[tuple[str, str, int, int]] = []
    trip = SimpleNamespace(
        id=trip_id,
        name="東京五日",
        destination_name="東京",
        start_date=date(2026, 12, 20),
        end_date=date(2026, 12, 24),
        timezone="Asia/Tokyo",
    )
    item = SimpleNamespace(
        item_type="activity",
        latitude=35.6812,
        longitude=139.7671,
        location_name="東京車站",
    )
    now = datetime(2026, 9, 1, tzinfo=UTC)
    forecast = TripWeather(
        location_name="東京",
        latitude=35.6812,
        longitude=139.7671,
        timezone="Asia/Tokyo",
        current=CurrentWeather(
            observed_at=now,
            is_daytime=True,
            condition=WeatherCondition(description="晴", type="CLEAR"),
            temperature_c=28,
            feels_like_c=29,
        ),
        days=[
            DailyWeather(
                date=date(2026, 9, 1),
                condition=WeatherCondition(description="晴", type="CLEAR"),
                min_temperature_c=23,
                max_temperature_c=31,
            )
        ],
        available_start_date=date(2026, 9, 1),
        available_end_date=date(2026, 9, 10),
        retrieved_at=now,
        expires_at=now + timedelta(minutes=15),
    )

    async def owned_trip(_session: object, owner_id: UUID, requested_id: UUID) -> object:
        observed_owner.append((owner_id, requested_id))
        return trip

    async def load_settings(_session: object) -> Settings:
        return Settings(google_maps_api_key="key")

    async def load_items(_session: object, _trip_id: UUID) -> list[object]:
        return [item]

    async def hydrate(_session: object, _trip: object, rows: list[object]) -> list[object]:
        return rows

    async def enforce_limit(
        namespace: str,
        identifier: str,
        *,
        limit: int,
        window_seconds: int,
    ) -> None:
        observed_limits.append((namespace, identifier, limit, window_seconds))

    class WeatherStub:
        configured = True

        def __init__(self, *_args: object) -> None:
            pass

        async def lookup(self, **kwargs: object) -> TripWeather:
            assert kwargs["latitude"] == 35.6812
            assert kwargs["longitude"] == 139.7671
            assert kwargs["location_name"] == "東京"
            # The trip's own timezone and the request locale reach the provider, so
            # MET Norway can bucket hours into the traveller's days and label them.
            assert kwargs["timezone"] == "Asia/Tokyo"
            assert kwargs["language_code"] == "ja"
            return forecast

    monkeypatch.setattr(trips_router, "owned_trip", owned_trip)
    monkeypatch.setattr(trips_router, "load_runtime_settings", load_settings)
    monkeypatch.setattr(trips_router, "load_items", load_items)
    monkeypatch.setattr(trips_router, "hydrate_legacy_items", hydrate)
    monkeypatch.setattr(trips_router, "TripWeatherService", WeatherStub)
    monkeypatch.setattr(trips_router, "get_redis", lambda: object())
    monkeypatch.setattr(trips_router, "enforce_named_rate_limit", enforce_limit)

    result = await trips_router.get_trip_weather(
        trip_id,
        SimpleNamespace(id=user_id),  # type: ignore[arg-type]
        object(),  # type: ignore[arg-type]
        "ja",
    )

    assert observed_owner == [(user_id, trip_id)]
    assert observed_limits == [
        (
            "trip-weather-user",
            str(user_id),
            trips_router.TRIP_WEATHER_USER_LIMIT,
            trips_router.TRIP_WEATHER_USER_WINDOW_SECONDS,
        )
    ]
    assert result.location_name == "東京"
    assert result.warnings == ["旅程日期超出目前 10 日預報範圍"]
