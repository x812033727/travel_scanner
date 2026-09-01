from __future__ import annotations

import asyncio
import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Any, Literal, Protocol, cast
from urllib.parse import urlencode
from uuid import UUID

import httpx
from pydantic import BaseModel, Field
from redis.asyncio import Redis

from app.config import Settings, get_settings
from app.providers.usage_meter import record_google_maps_request

TravelMode = Literal["transit", "walk", "drive"]
TRAVEL_MODES: set[str] = {"transit", "walk", "drive"}


class RoutePoint(BaseModel):
    item_id: UUID
    name: str
    latitude: float
    longitude: float
    provider_place_id: str | None = None


class RouteStep(BaseModel):
    travel_mode: str
    instruction: str
    duration_minutes: int | None = None
    distance_meters: int | None = None
    departure_stop: str | None = None
    arrival_stop: str | None = None
    departure_time: datetime | None = None
    arrival_time: datetime | None = None
    line_name: str | None = None
    line_short_name: str | None = None
    line_color: str | None = None
    headsign: str | None = None
    stop_count: int | None = None
    platform: str | None = None
    exit_name: str | None = None
    recommended_car: str | None = None


class RouteSegment(BaseModel):
    from_item_id: UUID
    to_item_id: UUID
    status: str = "resolved"
    travel_mode: TravelMode = "transit"
    is_override: bool = False
    provider: str
    attribution: str
    generated_at: datetime
    requested_departure_time: datetime | None = None
    schedule_mode: str = "scheduled"
    preference: str = "FEWER_TRANSFERS"
    duration_minutes: int
    buffer_minutes: int = 0
    departure_time: datetime | None = None
    arrival_time: datetime | None = None
    ready_time: datetime | None = None
    expires_at: datetime | None = None
    distance_meters: int | None = None
    fare: Decimal | None = None
    currency: str | None = None
    encoded_polyline: str | None = None
    maps_url: str | None = None
    steps: list[RouteStep] = Field(default_factory=list)
    details_available: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


@dataclass(frozen=True)
class GoogleRoutesProbeResult:
    reachable: bool
    route_available: bool
    status_code: int | None = None
    error_code: str | None = None


class RouteProvider(Protocol):
    name: str

    async def compute(
        self,
        origin: RoutePoint,
        destination: RoutePoint,
        departure_time: datetime | None,
        preference: str,
        travel_mode: TravelMode,
    ) -> RouteSegment | None: ...


def duration_minutes(value: object) -> int | None:
    raw = str(value or "")
    if not raw.endswith("s"):
        return None
    try:
        return max(1, round(float(raw[:-1]) / 60))
    except ValueError:
        return None


def _money(payload: object) -> tuple[Decimal | None, str | None]:
    if not isinstance(payload, dict):
        return None, None
    units = Decimal(str(payload.get("units") or 0))
    nanos = Decimal(str(payload.get("nanos") or 0)) / Decimal("1000000000")
    return units + nanos, cast(str | None, payload.get("currencyCode"))


def supported_transit_time(value: datetime | None) -> tuple[datetime | None, str, list[str]]:
    if value is None:
        return None, "live", []
    now = datetime.now(UTC)
    requested = value.astimezone(UTC)
    if now - timedelta(days=7) <= requested <= now + timedelta(days=100):
        return requested, "scheduled", []
    if requested > now + timedelta(days=100):
        days_until_weekday = (requested.weekday() - now.weekday()) % 7
        preview_day = (now + timedelta(days=max(1, days_until_weekday))).date()
        preview = datetime.combine(preview_day, requested.timetz()).astimezone(UTC)
        return preview, "preview", ["旅程超過可查班次範圍，這是相同星期與時段的預覽路線。"]
    return now, "preview", ["日期已超過可查班次範圍，顯示目前可用的參考路線。"]


class GoogleRouteProvider:
    name = "google_routes"
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    def __init__(
        self,
        settings: Settings,
        client: httpx.AsyncClient | None = None,
        redis: Redis | None = None,
    ) -> None:
        self.settings = settings
        self.client = client
        self.redis = redis

    @staticmethod
    def waypoint(point: RoutePoint) -> dict[str, Any]:
        if point.provider_place_id:
            return {"placeId": point.provider_place_id}
        return {"location": {"latLng": {"latitude": point.latitude, "longitude": point.longitude}}}

    async def _post(self, body: dict[str, Any], field_mask: str) -> httpx.Response:
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.settings.google_maps_api_key or "",
            "X-Goog-FieldMask": field_mask,
        }
        try:
            if self.client is not None:
                return await self.client.post(self.url, json=body, headers=headers)
            async with httpx.AsyncClient(timeout=self.settings.provider_timeout_seconds) as client:
                return await client.post(self.url, json=body, headers=headers)
        finally:
            if self.redis is not None:
                await record_google_maps_request(self.redis, "routes")

    async def probe(
        self,
        origin: RoutePoint,
        destination: RoutePoint,
    ) -> GoogleRoutesProbeResult:
        """Verify Routes API authorization without treating an empty route as a connection error."""
        if not self.settings.google_maps_api_key:
            return GoogleRoutesProbeResult(False, False, error_code="NOT_CONFIGURED")
        body: dict[str, Any] = {
            "origin": self.waypoint(origin),
            "destination": self.waypoint(destination),
            "travelMode": "TRANSIT",
            "languageCode": "zh-TW",
            "units": "METRIC",
            "computeAlternativeRoutes": False,
        }
        try:
            response = await self._post(body, "routes.duration")
        except httpx.HTTPError:
            return GoogleRoutesProbeResult(False, False, error_code="NETWORK_ERROR")
        try:
            raw_payload = response.json()
        except ValueError:
            return GoogleRoutesProbeResult(
                False,
                False,
                status_code=response.status_code,
                error_code="INVALID_RESPONSE",
            )
        payload = cast(dict[str, Any], raw_payload) if isinstance(raw_payload, dict) else {}
        if response.status_code >= 400:
            error = payload.get("error")
            raw_code = error.get("status") if isinstance(error, dict) else None
            error_code = str(raw_code) if raw_code else f"HTTP_{response.status_code}"
            return GoogleRoutesProbeResult(
                False,
                False,
                status_code=response.status_code,
                error_code=error_code,
            )
        routes = payload.get("routes")
        return GoogleRoutesProbeResult(
            True,
            isinstance(routes, list) and bool(routes),
            status_code=response.status_code,
        )

    async def compute(
        self,
        origin: RoutePoint,
        destination: RoutePoint,
        departure_time: datetime | None,
        preference: str,
        travel_mode: TravelMode = "transit",
    ) -> RouteSegment | None:
        if not self.settings.google_maps_api_key:
            return None
        if travel_mode == "transit":
            effective_time, schedule_mode, warnings = supported_transit_time(departure_time)
        elif travel_mode == "drive" and departure_time is not None:
            effective_time = max(departure_time.astimezone(UTC), datetime.now(UTC))
            schedule_mode, warnings = "scheduled", []
        else:
            effective_time, schedule_mode, warnings = None, "live", []
        if travel_mode == "walk":
            warnings.append("步行路線為測試版，請依現場道路與安全狀況調整。")
        transit_preference = (
            preference
            if travel_mode == "transit"
            and preference in {"FEWER_TRANSFERS", "LESS_WALKING"}
            else None
        )
        body: dict[str, Any] = {
            "origin": self.waypoint(origin),
            "destination": self.waypoint(destination),
            "travelMode": travel_mode.upper(),
            "languageCode": "zh-TW",
            "units": "METRIC",
            "computeAlternativeRoutes": False,
        }
        if effective_time is not None and travel_mode in {"transit", "drive"}:
            body["departureTime"] = effective_time.isoformat().replace("+00:00", "Z")
        if transit_preference:
            body["transitPreferences"] = {"routingPreference": transit_preference}
        if travel_mode == "drive":
            body["routingPreference"] = "TRAFFIC_AWARE"
        fields = (
            "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline,"
            "routes.travelAdvisory.transitFare,routes.legs.steps.travelMode,"
            "routes.legs.steps.distanceMeters,routes.legs.steps.staticDuration,"
            "routes.legs.steps.navigationInstruction.instructions,"
            "routes.legs.steps.transitDetails"
        )
        try:
            response = await self._post(body, fields)
            response.raise_for_status()
            payload = cast(dict[str, Any], response.json())
        except (httpx.HTTPError, ValueError):
            return None
        routes = cast(list[dict[str, Any]], payload.get("routes", []))
        if not routes:
            return None
        route = routes[0]
        total_minutes = duration_minutes(route.get("duration"))
        if total_minutes is None:
            return None
        steps: list[RouteStep] = []
        for leg in cast(list[dict[str, Any]], route.get("legs", [])):
            for raw in cast(list[dict[str, Any]], leg.get("steps", [])):
                transit = cast(dict[str, Any], raw.get("transitDetails") or {})
                stop_details = cast(dict[str, Any], transit.get("stopDetails") or {})
                line = cast(dict[str, Any], transit.get("transitLine") or {})
                departure_stop = cast(dict[str, Any], stop_details.get("departureStop") or {})
                arrival_stop = cast(dict[str, Any], stop_details.get("arrivalStop") or {})
                navigation = cast(dict[str, Any], raw.get("navigationInstruction") or {})
                mode = str(raw.get("travelMode") or "WALK")
                instruction = str(navigation.get("instructions") or "")
                if not instruction and transit:
                    instruction = f"搭乘 {line.get('name') or line.get('nameShort') or '大眾運輸'}"
                steps.append(
                    RouteStep(
                        travel_mode=mode,
                        instruction=instruction
                        or ("步行前往下一站" if mode == "WALK" else "前往下一段"),
                        duration_minutes=duration_minutes(raw.get("staticDuration")),
                        distance_meters=raw.get("distanceMeters"),
                        departure_stop=departure_stop.get("name"),
                        arrival_stop=arrival_stop.get("name"),
                        departure_time=stop_details.get("departureTime"),
                        arrival_time=stop_details.get("arrivalTime"),
                        line_name=line.get("name"),
                        line_short_name=line.get("nameShort"),
                        line_color=line.get("color"),
                        headsign=transit.get("headsign"),
                        stop_count=transit.get("stopCount"),
                    )
                )
        fare, currency = _money(
            cast(dict[str, Any], route.get("travelAdvisory") or {}).get("transitFare")
        )
        params = urlencode(
            {
                "api": 1,
                "origin": origin.name or f"{origin.latitude},{origin.longitude}",
                "destination": destination.name
                or f"{destination.latitude},{destination.longitude}",
                "travelmode": travel_mode,
                **(
                    {"origin_place_id": origin.provider_place_id}
                    if origin.provider_place_id
                    else {}
                ),
                **(
                    {"destination_place_id": destination.provider_place_id}
                    if destination.provider_place_id
                    else {}
                ),
            }
        )
        details = ["steps", "stops", "headsign"] if steps else []
        return RouteSegment(
            from_item_id=origin.item_id,
            to_item_id=destination.item_id,
            travel_mode=travel_mode,
            provider=self.name,
            attribution="Google Maps",
            generated_at=datetime.now(UTC),
            requested_departure_time=departure_time,
            schedule_mode=schedule_mode,
            preference=preference,
            duration_minutes=total_minutes,
            distance_meters=route.get("distanceMeters"),
            fare=fare,
            currency=currency,
            encoded_polyline=cast(dict[str, Any], route.get("polyline") or {}).get(
                "encodedPolyline"
            ),
            maps_url=f"https://www.google.com/maps/dir/?{params}",
            steps=steps,
            details_available=details,
            warnings=warnings,
        )


class NavitimeRouteProvider:
    name = "navitime"

    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None) -> None:
        self.settings = settings
        self.client = client

    async def compute(
        self,
        origin: RoutePoint,
        destination: RoutePoint,
        departure_time: datetime | None,
        preference: str,
        travel_mode: TravelMode = "transit",
    ) -> RouteSegment | None:
        if travel_mode != "transit" or not self.settings.navitime_configured:
            return None
        base = str(self.settings.navitime_api_base_url).rstrip("/")
        url = f"{base}/{self.settings.navitime_client_id}/v1/route_transit"
        effective_time, schedule_mode, warnings = supported_transit_time(departure_time)
        params: dict[str, Any] = {
            "start": f"{origin.latitude},{origin.longitude}",
            "goal": f"{destination.latitude},{destination.longitude}",
            "lang": "zh-TW",
        }
        if effective_time:
            params["start_time"] = effective_time.isoformat()
        headers = {"X-Api-Key": str(self.settings.navitime_api_key)}
        try:
            if self.client is not None:
                response = await self.client.get(url, params=params, headers=headers)
            else:
                async with httpx.AsyncClient(
                    timeout=self.settings.provider_timeout_seconds
                ) as client:
                    response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            payload = cast(dict[str, Any], response.json())
        except (httpx.HTTPError, ValueError):
            return None
        candidates = cast(list[dict[str, Any]], payload.get("items", []))
        if not candidates:
            return None
        route = candidates[0]
        summary = cast(dict[str, Any], route.get("summary") or {})
        raw_nodes = cast(list[dict[str, Any]], route.get("nodes") or route.get("sections") or [])
        steps: list[RouteStep] = []
        for raw in raw_nodes:
            transport = cast(dict[str, Any], raw.get("transport") or raw)
            departure = cast(dict[str, Any], raw.get("departure") or raw.get("from") or {})
            arrival = cast(dict[str, Any], raw.get("arrival") or raw.get("to") or {})
            line_name = transport.get("name") or transport.get("line_name")
            mode = "TRANSIT" if line_name else "WALK"
            steps.append(
                RouteStep(
                    travel_mode=mode,
                    instruction=str(
                        raw.get("instruction")
                        or (f"搭乘 {line_name}" if line_name else "步行前往下一站")
                    ),
                    duration_minutes=raw.get("time") or raw.get("duration"),
                    distance_meters=raw.get("distance"),
                    departure_stop=departure.get("name"),
                    arrival_stop=arrival.get("name"),
                    line_name=line_name,
                    headsign=cast(dict[str, Any], transport.get("destination") or {}).get("name"),
                    platform=departure.get("start_platform") or raw.get("start_platform"),
                    exit_name=arrival.get("gateway") or raw.get("gateway"),
                    recommended_car=transport.get("getoff"),
                )
            )
        total = route.get("time") or summary.get("move_time") or summary.get("time")
        try:
            total_minutes = max(1, int(str(total)))
        except (TypeError, ValueError):
            total_minutes = sum(step.duration_minutes or 0 for step in steps)
        if total_minutes <= 0:
            return None
        details = ["steps", "stops", "headsign"]
        if any(step.platform for step in steps):
            details.append("platform")
        if any(step.exit_name for step in steps):
            details.append("exit")
        if any(step.recommended_car for step in steps):
            details.append("recommended_car")
        return RouteSegment(
            from_item_id=origin.item_id,
            to_item_id=destination.item_id,
            travel_mode="transit",
            provider=self.name,
            attribution="NAVITIME JAPAN",
            generated_at=datetime.now(UTC),
            requested_departure_time=departure_time,
            schedule_mode=schedule_mode,
            preference=preference,
            duration_minutes=total_minutes,
            distance_meters=route.get("distance") or summary.get("move_distance"),
            steps=steps,
            details_available=details,
            warnings=warnings,
        )


class RouteService:
    def __init__(
        self,
        redis: Redis,
        settings: Settings | None = None,
        google: RouteProvider | None = None,
        navitime: RouteProvider | None = None,
    ) -> None:
        self.redis = redis
        self.settings = settings or get_settings()
        self.google = google or GoogleRouteProvider(self.settings, None, redis)
        self.navitime = navitime or NavitimeRouteProvider(self.settings)

    def _providers(self, japan: bool, travel_mode: TravelMode) -> list[RouteProvider]:
        if japan and travel_mode == "transit":
            return [self.navitime, self.google]
        return [self.google]

    async def compute(
        self,
        origin: RoutePoint,
        destination: RoutePoint,
        departure_time: datetime | None,
        preference: str,
        *,
        japan: bool,
        travel_mode: TravelMode = "transit",
        refresh: bool = False,
    ) -> RouteSegment | None:
        raw_key = json.dumps(
            {
                "o": [round(origin.latitude, 6), round(origin.longitude, 6)],
                "d": [round(destination.latitude, 6), round(destination.longitude, 6)],
                "opi": origin.provider_place_id,
                "dpi": destination.provider_place_id,
                "t": departure_time.isoformat() if departure_time else None,
                "p": preference,
                "j": japan,
                "m": travel_mode,
            },
            sort_keys=True,
        ).encode()
        key = f"routes:segment:{hashlib.sha256(raw_key).hexdigest()}"
        if not refresh:
            cached = await self.redis.get(key)
            if cached:
                value = cached.decode() if isinstance(cached, bytes) else str(cached)
                cached_segment = RouteSegment.model_validate_json(value)
                return cached_segment.model_copy(
                    update={"from_item_id": origin.item_id, "to_item_id": destination.item_id}
                )
        for provider in self._providers(japan, travel_mode):
            provider_segment = await provider.compute(
                origin, destination, departure_time, preference, travel_mode
            )
            if provider_segment is not None:
                await self.redis.set(
                    key,
                    provider_segment.model_dump_json(),
                    ex=self.settings.route_cache_ttl_seconds,
                )
                return provider_segment
        return None

    async def compute_many(
        self,
        pairs: list[tuple[RoutePoint, RoutePoint, datetime | None]],
        preference: str,
        *,
        japan: bool,
        travel_mode: TravelMode = "transit",
        refresh: bool = False,
    ) -> list[RouteSegment | None]:
        semaphore = asyncio.Semaphore(4)

        async def one(pair: tuple[RoutePoint, RoutePoint, datetime | None]) -> RouteSegment | None:
            async with semaphore:
                return await self.compute(
                    pair[0], pair[1], pair[2], preference, japan=japan, refresh=refresh
                    , travel_mode=travel_mode
                )

        return await asyncio.gather(*(one(pair) for pair in pairs))


def is_japan_trip(timezone: str, destination_name: str | None, data: dict[str, Any]) -> bool:
    country = str(data.get("destination_country") or "")
    return (
        timezone == "Asia/Tokyo"
        or country in {"日本", "Japan"}
        or "日本" in (destination_name or "")
    )


def preview_date_for(day: date, reference: datetime) -> datetime:
    return datetime.combine(day, reference.timetz())
