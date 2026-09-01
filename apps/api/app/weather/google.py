from __future__ import annotations

import asyncio
import hashlib
from datetime import UTC, date, datetime, timedelta
from typing import Any, cast

import httpx
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import Settings
from app.problems import AppError
from app.providers.usage_meter import record_google_maps_request
from app.weather.schemas import CurrentWeather, DailyWeather, TripWeather, WeatherCondition


class WeatherProviderError(Exception):
    def __init__(self, status_code: int, provider_code: str, detail: str) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.provider_code = provider_code


class GoogleWeatherService:
    current_url = "https://weather.googleapis.com/v1/currentConditions:lookup"
    daily_url = "https://weather.googleapis.com/v1/forecast/days:lookup"

    def __init__(
        self,
        redis: Redis,
        settings: Settings,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.redis = redis
        self.settings = settings
        self.client = client

    @property
    def configured(self) -> bool:
        return bool(self.settings.google_maps_api_key)

    def _cache_key(self, latitude: float, longitude: float, language_code: str) -> str:
        coordinates = f"{latitude:.4f}:{longitude:.4f}:{language_code}:10"
        digest = hashlib.sha256(coordinates.encode()).hexdigest()
        return f"weather:google:{digest}"

    async def _request(
        self,
        url: str,
        *,
        latitude: float,
        longitude: float,
        language_code: str,
        operation: str,
        days: int | None = None,
    ) -> dict[str, Any]:
        if not self.settings.google_maps_api_key:
            raise AppError(
                503,
                "weather_not_configured",
                "Google Weather 尚未設定，請先在管理後台設定伺服器 API 金鑰",
            )
        params: dict[str, str | int] = {
            "key": self.settings.google_maps_api_key,
            "location.latitude": f"{latitude:.6f}",
            "location.longitude": f"{longitude:.6f}",
            "languageCode": language_code,
            "unitsSystem": "METRIC",
        }
        if days is not None:
            params["days"] = days
            params["pageSize"] = days
        try:
            if self.client is not None:
                response = await self.client.get(url, params=params)
            else:
                async with httpx.AsyncClient(
                    timeout=self.settings.provider_timeout_seconds
                ) as client:
                    response = await client.get(url, params=params)
            if response.is_error:
                provider_code = f"HTTP_{response.status_code}"
                detail = "Google Weather 暫時無法回應"
                try:
                    error = cast(dict[str, Any], response.json().get("error") or {})
                    provider_code = str(error.get("status") or provider_code)
                    detail = str(error.get("message") or detail)
                except (ValueError, AttributeError):
                    pass
                raise WeatherProviderError(response.status_code, provider_code, detail)
            return cast(dict[str, Any], response.json())
        except WeatherProviderError:
            raise
        except (httpx.HTTPError, ValueError) as exc:
            raise WeatherProviderError(502, "UPSTREAM_UNAVAILABLE", str(exc)) from exc
        finally:
            await record_google_maps_request(self.redis, operation)

    @staticmethod
    def _condition(value: object) -> WeatherCondition:
        raw = cast(dict[str, Any], value or {})
        description = cast(dict[str, Any], raw.get("description") or {})
        return WeatherCondition(
            description=str(description.get("text") or "天氣狀況未提供"),
            type=str(raw.get("type") or "WEATHER_CONDITION_UNSPECIFIED"),
        )

    @staticmethod
    def _temperature(value: object) -> float:
        raw = cast(dict[str, Any], value or {})
        return round(float(raw.get("degrees") or 0), 1)

    @staticmethod
    def _precipitation_percent(value: object) -> int | None:
        raw = cast(dict[str, Any], value or {})
        probability = cast(dict[str, Any], raw.get("probability") or {})
        percent = probability.get("percent")
        return int(percent) if percent is not None else None

    @staticmethod
    def _wind_speed(value: object) -> float | None:
        raw = cast(dict[str, Any], value or {})
        speed = cast(dict[str, Any], raw.get("speed") or {})
        raw_value = speed.get("value")
        return round(float(raw_value), 1) if raw_value is not None else None

    def _parse_current(self, payload: dict[str, Any]) -> CurrentWeather:
        observed_at = payload.get("currentTime")
        if not observed_at:
            raise ValueError("Google Weather currentTime missing")
        return CurrentWeather(
            observed_at=datetime.fromisoformat(str(observed_at).replace("Z", "+00:00")),
            is_daytime=bool(payload.get("isDaytime")),
            condition=self._condition(payload.get("weatherCondition")),
            temperature_c=self._temperature(payload.get("temperature")),
            feels_like_c=self._temperature(payload.get("feelsLikeTemperature")),
            relative_humidity_percent=payload.get("relativeHumidity"),
            precipitation_probability_percent=self._precipitation_percent(
                payload.get("precipitation")
            ),
            wind_speed_kph=self._wind_speed(payload.get("wind")),
            uv_index=payload.get("uvIndex"),
        )

    def _parse_day(self, payload: dict[str, Any]) -> DailyWeather:
        display = cast(dict[str, Any], payload.get("displayDate") or {})
        daytime = cast(dict[str, Any], payload.get("daytimeForecast") or {})
        nighttime = cast(dict[str, Any], payload.get("nighttimeForecast") or {})
        sun = cast(dict[str, Any], payload.get("sunEvents") or {})
        humidity_values = [
            int(value)
            for value in (daytime.get("relativeHumidity"), nighttime.get("relativeHumidity"))
            if value is not None
        ]
        rain_values = [
            value
            for value in (
                self._precipitation_percent(daytime.get("precipitation")),
                self._precipitation_percent(nighttime.get("precipitation")),
            )
            if value is not None
        ]
        wind_values = [
            value
            for value in (
                self._wind_speed(daytime.get("wind")),
                self._wind_speed(nighttime.get("wind")),
            )
            if value is not None
        ]
        uv_values = [
            int(value)
            for value in (daytime.get("uvIndex"), nighttime.get("uvIndex"))
            if value is not None
        ]
        return DailyWeather(
            date=date(int(display["year"]), int(display["month"]), int(display["day"])),
            condition=self._condition(daytime.get("weatherCondition")),
            min_temperature_c=self._temperature(payload.get("minTemperature")),
            max_temperature_c=self._temperature(payload.get("maxTemperature")),
            relative_humidity_percent=max(humidity_values) if humidity_values else None,
            precipitation_probability_percent=max(rain_values) if rain_values else None,
            wind_speed_kph=max(wind_values) if wind_values else None,
            uv_index=max(uv_values) if uv_values else None,
            sunrise_at=(
                datetime.fromisoformat(str(sun["sunriseTime"]).replace("Z", "+00:00"))
                if sun.get("sunriseTime")
                else None
            ),
            sunset_at=(
                datetime.fromisoformat(str(sun["sunsetTime"]).replace("Z", "+00:00"))
                if sun.get("sunsetTime")
                else None
            ),
        )

    @staticmethod
    def _public_error(error: WeatherProviderError) -> AppError:
        if error.status_code in {401, 403}:
            return AppError(
                503,
                "weather_api_not_enabled",
                "Google Weather API 尚未啟用，或伺服器 API 金鑰限制不允許此服務",
            )
        if error.status_code == 429:
            return AppError(503, "weather_rate_limited", "Google Weather 查詢額度暫時不足")
        return AppError(502, "weather_provider_unavailable", "Google Weather 暫時無法回應")

    async def lookup(
        self,
        *,
        latitude: float,
        longitude: float,
        location_name: str,
        language_code: str = "zh-TW",
    ) -> TripWeather:
        if not self.configured:
            raise AppError(
                503,
                "weather_not_configured",
                "Google Weather 尚未設定，請先在管理後台設定伺服器 API 金鑰",
            )
        key = self._cache_key(latitude, longitude, language_code)
        try:
            cached = await self.redis.get(key)
        except RedisError:
            cached = None
        if cached:
            raw = cached.decode() if isinstance(cached, bytes) else str(cached)
            try:
                return TripWeather.model_validate_json(raw).model_copy(
                    update={
                        "cache_status": "hit",
                        "location_name": location_name,
                        "latitude": latitude,
                        "longitude": longitude,
                    }
                )
            except (ValueError, TypeError):
                pass

        results = await asyncio.gather(
            self._request(
                self.current_url,
                latitude=latitude,
                longitude=longitude,
                language_code=language_code,
                operation="weather_current",
            ),
            self._request(
                self.daily_url,
                latitude=latitude,
                longitude=longitude,
                language_code=language_code,
                operation="weather_daily_forecast",
                days=10,
            ),
            return_exceptions=True,
        )
        current_result: object = results[0]
        daily_result: object = results[1]
        errors = [
            value
            for value in (current_result, daily_result)
            if isinstance(value, WeatherProviderError)
        ]
        if len(errors) == 2:
            raise self._public_error(errors[0])

        warnings: list[str] = []
        current: CurrentWeather | None = None
        days: list[DailyWeather] = []
        timezone: str | None = None
        if isinstance(current_result, dict):
            try:
                current_payload = cast(dict[str, Any], current_result)
                current = self._parse_current(current_payload)
                timezone = str(
                    cast(dict[str, Any], current_payload.get("timeZone") or {}).get("id") or ""
                ) or None
            except (KeyError, TypeError, ValueError):
                warnings.append("目前天氣資料格式不完整")
        else:
            warnings.append("目前天氣暫時無法取得")
        if isinstance(daily_result, dict):
            daily_payload = cast(dict[str, Any], daily_result)
            timezone = timezone or str(
                cast(dict[str, Any], daily_payload.get("timeZone") or {}).get("id") or ""
            ) or None
            for value in cast(list[dict[str, Any]], daily_payload.get("forecastDays") or []):
                try:
                    days.append(self._parse_day(value))
                except (KeyError, TypeError, ValueError):
                    warnings.append("部分每日預報資料格式不完整")
        else:
            warnings.append("10 日天氣預報暫時無法取得")
        if current is None and not days:
            if errors:
                raise self._public_error(errors[0])
            raise AppError(502, "weather_response_invalid", "Google Weather 回應格式不完整")

        retrieved_at = datetime.now(UTC)
        response = TripWeather(
            location_name=location_name,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            current=current,
            days=days,
            available_start_date=days[0].date if days else None,
            available_end_date=days[-1].date if days else None,
            retrieved_at=retrieved_at,
            expires_at=retrieved_at + timedelta(seconds=self.settings.weather_cache_ttl_seconds),
            warnings=list(dict.fromkeys(warnings)),
        )
        try:
            await self.redis.set(
                key,
                response.model_dump_json(),
                ex=self.settings.weather_cache_ttl_seconds,
            )
        except RedisError:
            pass
        return response
