"""MET Norway Locationforecast as the trip weather source.

The Norwegian Meteorological Institute publishes a global forecast for free, commercial
use included, under CC BY 4.0. The terms of service ask for three things this module
honours: identify the application in the User-Agent, never send coordinates with more
than four decimals, and cache instead of re-requesting the same place every minute.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from datetime import UTC, date, datetime, timedelta
from typing import Any, cast
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import httpx
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import Settings
from app.problems import AppError
from app.weather.schemas import CurrentWeather, DailyWeather, TripWeather, WeatherCondition

MET_NORWAY_SOURCE = "met_norway"
MET_NORWAY_ATTRIBUTION = "MET Norway"

# Family -> (condition type the planner renders, description per locale). Intensity and
# showers are layered on top by ``describe_symbol`` so the table stays short.
_FAMILIES: dict[str, tuple[str, dict[str, str]]] = {
    "clearsky": (
        "CLEAR",
        {"zh-TW": "晴朗", "zh-CN": "晴朗", "en": "Clear sky", "ja": "快晴", "ko": "맑음"},
    ),
    "fair": (
        "MOSTLY_CLEAR",
        {
            "zh-TW": "晴時多雲",
            "zh-CN": "晴时多云",
            "en": "Fair",
            "ja": "晴れ時々曇り",
            "ko": "대체로 맑음",
        },
    ),
    "partlycloudy": (
        "PARTLY_CLOUDY",
        {
            "zh-TW": "多雲時晴",
            "zh-CN": "多云时晴",
            "en": "Partly cloudy",
            "ja": "曇り時々晴れ",
            "ko": "구름 조금",
        },
    ),
    "cloudy": (
        "CLOUDY",
        {"zh-TW": "陰天", "zh-CN": "阴天", "en": "Cloudy", "ja": "曇り", "ko": "흐림"},
    ),
    "fog": ("FOG", {"zh-TW": "霧", "zh-CN": "雾", "en": "Fog", "ja": "霧", "ko": "안개"}),
    "rain": ("RAIN", {"zh-TW": "雨", "zh-CN": "雨", "en": "Rain", "ja": "雨", "ko": "비"}),
    "rainshowers": (
        "RAIN_SHOWERS",
        {"zh-TW": "陣雨", "zh-CN": "阵雨", "en": "Rain showers", "ja": "にわか雨", "ko": "소나기"},
    ),
    "sleet": (
        "SLEET",
        {"zh-TW": "雨夾雪", "zh-CN": "雨夹雪", "en": "Sleet", "ja": "みぞれ", "ko": "진눈깨비"},
    ),
    "sleetshowers": (
        "SLEET_SHOWERS",
        {
            "zh-TW": "陣雨夾雪",
            "zh-CN": "阵雨夹雪",
            "en": "Sleet showers",
            "ja": "にわかみぞれ",
            "ko": "진눈깨비 소나기",
        },
    ),
    "snow": ("SNOW", {"zh-TW": "雪", "zh-CN": "雪", "en": "Snow", "ja": "雪", "ko": "눈"}),
    "snowshowers": (
        "SNOW_SHOWERS",
        {"zh-TW": "陣雪", "zh-CN": "阵雪", "en": "Snow showers", "ja": "にわか雪", "ko": "소낙눈"},
    ),
    "thunder": (
        "THUNDERSTORM",
        {"zh-TW": "雷雨", "zh-CN": "雷雨", "en": "Thunderstorm", "ja": "雷雨", "ko": "뇌우"},
    ),
}
_INTENSITY: dict[str, dict[str, str]] = {
    "light": {"zh-TW": "小", "zh-CN": "小", "en": "Light ", "ja": "弱い", "ko": "약한 "},
    "heavy": {"zh-TW": "大", "zh-CN": "大", "en": "Heavy ", "ja": "強い", "ko": "강한 "},
}


def describe_symbol(symbol_code: str | None, language_code: str) -> WeatherCondition:
    """Turn a MET ``symbol_code`` such as ``lightrainshowers_day`` into a condition."""
    language = language_code if language_code in {"zh-TW", "zh-CN", "en", "ja", "ko"} else "en"
    unknown = WeatherCondition(
        description=_unknown(language), type="WEATHER_CONDITION_UNSPECIFIED"
    )
    code = (symbol_code or "").split("_", 1)[0].lower()
    if not code:
        return unknown
    intensity = (
        "light" if code.startswith("light") else "heavy" if code.startswith("heavy") else None
    )
    stripped = code.removeprefix("light").removeprefix("heavy")
    # MET spells two of its codes with a doubled "s" (``lightssleetshowersandthunder``).
    if stripped.startswith(("ssleet", "ssnow")):
        stripped = stripped.removeprefix("s")
    showers = "showers" in stripped
    if "thunder" in stripped:
        family = "thunder"
    elif "sleet" in stripped:
        family = "sleetshowers" if showers else "sleet"
    elif "snow" in stripped:
        family = "snowshowers" if showers else "snow"
    elif "rain" in stripped:
        family = "rainshowers" if showers else "rain"
    elif stripped in _FAMILIES:
        family = stripped
    else:
        return unknown
    condition_type, descriptions = _FAMILIES[family]
    description = descriptions[language]
    if intensity and family != "thunder":
        condition_type = f"{intensity.upper()}_{condition_type}"
        description = f"{_INTENSITY[intensity][language]}{description}".strip()
        if language == "en":
            description = description[0] + description[1:].lower()
    return WeatherCondition(description=description, type=condition_type)


def _unknown(language: str) -> str:
    return {
        "zh-TW": "天氣狀況未提供",
        "zh-CN": "天气状况未提供",
        "en": "Conditions unavailable",
        "ja": "天気情報なし",
        "ko": "날씨 정보 없음",
    }[language]


def _round_half_up(value: float) -> int:
    return int(value + 0.5)


class MetNorwayWeatherService:
    """Locationforecast 2.0 ``complete`` reduced to the planner's ``TripWeather`` shape."""

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
        # No credential: the service only needs an identifying User-Agent.
        return bool(self.settings.met_norway_user_agent.strip())

    @property
    def forecast_url(self) -> str:
        base = self.settings.met_norway_base_url.rstrip("/")
        return f"{base}/weatherapi/locationforecast/2.0/complete"

    def _cache_key(self, latitude: float, longitude: float, timezone: str, language: str) -> str:
        raw = f"{latitude:.4f}:{longitude:.4f}:{timezone}:{language}"
        return f"weather:met:{hashlib.sha256(raw.encode()).hexdigest()}"

    async def _request(self, latitude: float, longitude: float) -> dict[str, Any]:
        params = {"lat": f"{latitude:.4f}", "lon": f"{longitude:.4f}"}
        headers = {
            "User-Agent": self.settings.met_norway_user_agent,
            "Accept": "application/json",
        }
        try:
            if self.client is not None:
                response = await self.client.get(self.forecast_url, params=params, headers=headers)
            else:
                async with httpx.AsyncClient(
                    timeout=self.settings.provider_timeout_seconds
                ) as client:
                    response = await client.get(self.forecast_url, params=params, headers=headers)
        except httpx.HTTPError as exc:
            raise AppError(502, "weather_provider_unavailable", "MET Norway 暫時無法回應") from exc
        if response.status_code == 403:
            raise AppError(
                503,
                "weather_provider_rejected",
                "MET Norway 拒絕了請求，請檢查 User-Agent 設定",
            )
        if response.status_code == 429:
            raise AppError(503, "weather_rate_limited", "MET Norway 查詢額度暫時不足")
        if response.is_error:
            raise AppError(502, "weather_provider_unavailable", "MET Norway 暫時無法回應")
        try:
            payload = response.json()
        except ValueError as exc:
            raise AppError(502, "weather_response_invalid", "MET Norway 回應格式不完整") from exc
        if not isinstance(payload, dict):
            raise AppError(502, "weather_response_invalid", "MET Norway 回應格式不完整")
        return cast(dict[str, Any], payload)

    @staticmethod
    def _zone(timezone: str | None) -> ZoneInfo:
        try:
            return ZoneInfo(timezone or "UTC")
        except ZoneInfoNotFoundError:
            return ZoneInfo("UTC")

    @staticmethod
    def _entries(payload: dict[str, Any]) -> list[dict[str, Any]]:
        properties = cast(dict[str, Any], payload.get("properties") or {})
        raw = properties.get("timeseries")
        return [entry for entry in cast(list[Any], raw or []) if isinstance(entry, dict)]

    @staticmethod
    def _details(entry: dict[str, Any], block: str) -> dict[str, Any]:
        data = cast(dict[str, Any], entry.get("data") or {})
        section = cast(dict[str, Any], data.get(block) or {})
        return cast(dict[str, Any], section.get("details") or {})

    @staticmethod
    def _symbol(entry: dict[str, Any], *blocks: str) -> str | None:
        data = cast(dict[str, Any], entry.get("data") or {})
        for block in blocks:
            section = cast(dict[str, Any], data.get(block) or {})
            summary = cast(dict[str, Any], section.get("summary") or {})
            code = summary.get("symbol_code")
            if code:
                return str(code)
        return None

    @staticmethod
    def _time(entry: dict[str, Any]) -> datetime | None:
        raw = entry.get("time")
        if not raw:
            return None
        try:
            return datetime.fromisoformat(str(raw).replace("Z", "+00:00")).astimezone(UTC)
        except ValueError:
            return None

    @staticmethod
    def _number(value: object) -> float | None:
        if value is None or isinstance(value, bool):
            return None
        try:
            return float(cast(Any, value))
        except (TypeError, ValueError):
            return None

    def _parse_current(
        self, entry: dict[str, Any], language: str, zone: ZoneInfo
    ) -> CurrentWeather | None:
        observed_at = self._time(entry)
        instant = self._details(entry, "instant")
        temperature = self._number(instant.get("air_temperature"))
        if observed_at is None or temperature is None:
            return None
        feels_like = self._number(instant.get("apparent_air_temperature"))
        humidity = self._number(instant.get("relative_humidity"))
        wind = self._number(instant.get("wind_speed"))
        uv = self._number(instant.get("ultraviolet_index_clear_sky"))
        symbol = self._symbol(entry, "next_1_hours", "next_6_hours", "next_12_hours")
        probability = self._number(
            self._details(entry, "next_1_hours").get("probability_of_precipitation")
        )
        return CurrentWeather(
            observed_at=observed_at,
            is_daytime=(
                symbol.endswith("_day")
                if symbol and symbol.endswith(("_day", "_night"))
                else 6 <= observed_at.astimezone(zone).hour < 18
            ),
            condition=describe_symbol(symbol, language),
            temperature_c=round(temperature, 1),
            feels_like_c=round(feels_like if feels_like is not None else temperature, 1),
            relative_humidity_percent=(
                min(100, max(0, _round_half_up(humidity))) if humidity is not None else None
            ),
            precipitation_probability_percent=(
                min(100, max(0, _round_half_up(probability))) if probability is not None else None
            ),
            wind_speed_kph=round(wind * 3.6, 1) if wind is not None else None,
            uv_index=max(0, _round_half_up(uv)) if uv is not None else None,
        )

    def _parse_days(
        self, entries: list[dict[str, Any]], zone: ZoneInfo, language: str
    ) -> list[DailyWeather]:
        by_day: dict[date, list[tuple[datetime, dict[str, Any]]]] = defaultdict(list)
        for entry in entries:
            moment = self._time(entry)
            if moment is None:
                continue
            by_day[moment.astimezone(zone).date()].append((moment.astimezone(zone), entry))

        days: list[DailyWeather] = []
        for day_value in sorted(by_day):
            samples = by_day[day_value]
            temperatures: list[float] = []
            humidity: list[float] = []
            wind: list[float] = []
            uv: list[float] = []
            probability: list[float] = []
            precipitation = 0.0
            has_precipitation = False
            covered_until: datetime | None = None
            for moment, entry in samples:
                instant = self._details(entry, "instant")
                temperature = self._number(instant.get("air_temperature"))
                if temperature is not None:
                    temperatures.append(temperature)
                for block in ("next_6_hours", "next_1_hours"):
                    block_details = self._details(entry, block)
                    for key in ("air_temperature_min", "air_temperature_max"):
                        value = self._number(block_details.get(key))
                        if value is not None:
                            temperatures.append(value)
                    chance = self._number(block_details.get("probability_of_precipitation"))
                    if chance is not None:
                        probability.append(chance)
                value = self._number(instant.get("relative_humidity"))
                if value is not None:
                    humidity.append(value)
                value = self._number(instant.get("wind_speed"))
                if value is not None:
                    wind.append(value)
                value = self._number(instant.get("ultraviolet_index_clear_sky"))
                if value is not None and 6 <= moment.hour < 18:
                    uv.append(value)
                # Hourly entries carry a one-hour total, the sparser tail of the forecast a
                # six-hour total; take whichever covers time nobody has summed yet.
                hourly = self._number(
                    self._details(entry, "next_1_hours").get("precipitation_amount")
                )
                six_hourly = self._number(
                    self._details(entry, "next_6_hours").get("precipitation_amount")
                )
                if hourly is not None:
                    precipitation += hourly
                    has_precipitation = True
                    covered_until = moment + timedelta(hours=1)
                elif six_hourly is not None and (covered_until is None or moment >= covered_until):
                    precipitation += six_hourly
                    has_precipitation = True
                    covered_until = moment + timedelta(hours=6)
            if not temperatures:
                continue
            # The daytime symbol closest to noon describes the day best.
            noon_first = sorted(samples, key=lambda pair: abs(pair[0].hour - 12))
            blocks = ("next_6_hours", "next_1_hours", "next_12_hours")
            symbol = next(
                (code for _, entry in noon_first if (code := self._symbol(entry, *blocks))),
                None,
            )
            days.append(
                DailyWeather(
                    date=day_value,
                    condition=describe_symbol(symbol, language),
                    min_temperature_c=round(min(temperatures), 1),
                    max_temperature_c=round(max(temperatures), 1),
                    relative_humidity_percent=(
                        min(100, max(0, _round_half_up(max(humidity)))) if humidity else None
                    ),
                    precipitation_probability_percent=(
                        min(100, max(0, _round_half_up(max(probability)))) if probability else None
                    ),
                    precipitation_mm=round(precipitation, 1) if has_precipitation else None,
                    wind_speed_kph=round(max(wind) * 3.6, 1) if wind else None,
                    uv_index=max(0, _round_half_up(max(uv))) if uv else None,
                )
            )
        return days

    async def lookup(
        self,
        *,
        latitude: float,
        longitude: float,
        location_name: str,
        language_code: str = "zh-TW",
        timezone: str | None = None,
    ) -> TripWeather:
        if not self.configured:
            raise AppError(503, "weather_not_configured", "MET Norway 尚未設定 User-Agent")
        zone = self._zone(timezone)
        key = self._cache_key(latitude, longitude, str(zone.key), language_code)
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

        payload = await self._request(latitude, longitude)
        entries = self._entries(payload)
        if not entries:
            raise AppError(502, "weather_response_invalid", "MET Norway 回應格式不完整")
        warnings: list[str] = []
        current = self._parse_current(entries[0], language_code, zone)
        if current is None:
            warnings.append("目前天氣資料格式不完整")
        days = self._parse_days(entries, zone, language_code)
        if current is None and not days:
            raise AppError(502, "weather_response_invalid", "MET Norway 回應格式不完整")

        retrieved_at = datetime.now(UTC)
        response = TripWeather(
            source=MET_NORWAY_SOURCE,
            attribution=MET_NORWAY_ATTRIBUTION,
            location_name=location_name,
            latitude=latitude,
            longitude=longitude,
            timezone=str(zone.key),
            current=current,
            days=days,
            available_start_date=days[0].date if days else None,
            available_end_date=days[-1].date if days else None,
            retrieved_at=retrieved_at,
            expires_at=retrieved_at + timedelta(seconds=self.settings.weather_cache_ttl_seconds),
            warnings=warnings,
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
