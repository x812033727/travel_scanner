import asyncio
import hashlib
import json
import secrets
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Annotated, Any, Literal, cast
from uuid import UUID, uuid4, uuid5
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import httpx
from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, Field, model_validator
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.ai.itinerary import AIItineraryPlanner, AIItineraryRequest, AIPlanningResult
from app.auth.service import CurrentUser
from app.config import Settings, get_settings
from app.db import get_session
from app.destinations.catalog import destination_for_code
from app.foods.service import load_planner_foods
from app.hotspots.service import load_planner_hotspots
from app.infra import enforce_named_rate_limit, get_redis
from app.models import (
    SearchRequest,
    TripPlan,
    TripPlanItem,
    TripRouteSegment,
    TripShare,
    UsageReservation,
)
from app.optimization.engine import TripOptimizer, TripPlanResult
from app.places.google import GoogleTravelService
from app.places.naver import NaverPlaceService
from app.problems import AppError
from app.providers.base import ActivityProvider, FlightProvider, HotelProvider, TransportProvider
from app.providers.registry import (
    build_module_provider_candidates,
    provider_status_for_modules,
)
from app.providers.runner import ProviderRunner, ProviderUnavailableError
from app.providers.schemas import ActivityOffer, FlightOffer, HotelOffer, Offer, TransportOffer
from app.search.schemas import SearchCreate, SearchPreferences, Travelers
from app.trips.itinerary import ItineraryItem
from app.trips.route_planner import (
    DEFAULT_BUFFER_MINUTES,
    ROUTE_PREVIEW_TTL_SECONDS,
    RoutingOptions,
    get_or_create_day_setting,
    load_day_settings,
    load_route_segments,
    persist_projected_segments,
    project_day_schedule,
    routing_summary,
    segment_from_record,
)
from app.trips.route_tasks import enqueue_trip_routing
from app.trips.routing import (
    ExternalNavigation,
    RoutePoint,
    RouteSegment,
    RouteService,
    TravelMode,
    infer_place_provider,
    naver_external_navigation,
    route_provider_configured,
    trip_region_code,
)
from app.trips.schedule import (
    active_route_rows,
    apply_schedule_defaults,
    canonicalize_positions,
    ensure_system_slots,
    primary_lodging,
    route_pair_count,
    schedule_defaults,
    sync_primary_lodging,
)
from app.usage.service import (
    COMMON_LIMITS,
    commit_reservation,
    release_reservation,
    reserve_use,
    usage_status,
)
from app.weather.google import GoogleWeatherService
from app.weather.schemas import TripWeather

router = APIRouter(prefix="/trips", tags=["trips"])
public_router = APIRouter(prefix="/shared-trips", tags=["shared trips"])
Session = Annotated[AsyncSession, Depends(get_session)]
TRIP_WEATHER_USER_LIMIT = 30
TRIP_WEATHER_USER_WINDOW_SECONDS = 3_600
TRIP_ROUTE_USER_LIMIT = 60
TRIP_ROUTE_REFRESH_USER_LIMIT = 10
TRIP_ROUTE_USER_WINDOW_SECONDS = 3_600
TRIP_ROUTE_MAX_ITEMS = 12


class SaveTripRequest(BaseModel):
    source: str = "search"
    search_id: UUID | None = None
    plan_id: UUID | None = None
    name: str = Field(min_length=1, max_length=255)
    destination_name: str | None = Field(default=None, min_length=1, max_length=255)
    destination_place_id: str | None = Field(default=None, max_length=255)
    start_date: date | None = None
    end_date: date | None = None
    timezone: str | None = Field(default=None, max_length=64)
    route_preference: str = "FEWER_TRANSFERS"
    travelers: Travelers = Field(default_factory=Travelers)
    preferences: SearchPreferences = Field(default_factory=SearchPreferences)
    notes: str | None = Field(default=None, max_length=1000)
    routing: RoutingOptions = Field(default_factory=RoutingOptions)

    @model_validator(mode="after")
    def validate_source(self) -> "SaveTripRequest":
        if self.source not in {"search", "blank"}:
            raise ValueError("source must be search or blank")
        if self.source == "search" and (self.search_id is None or self.plan_id is None):
            raise ValueError("search_id and plan_id are required for a search trip")
        if self.source == "blank":
            if not self.destination_name or not self.start_date or not self.end_date:
                raise ValueError("destination_name, start_date and end_date are required")
            if self.end_date < self.start_date:
                raise ValueError("end_date must not be before start_date")
            if (self.end_date - self.start_date).days > 60:
                raise ValueError("blank trips may be at most 61 days")
        if self.route_preference not in {"FEWER_TRANSFERS", "LESS_WALKING", "FASTEST"}:
            raise ValueError("unsupported route preference")
        if self.notes is not None:
            self.notes = self.notes.strip() or None
        return self


def destination_timezone(destination: str) -> str:
    rules = (
        (("日本", "東京", "大阪", "京都", "北海道", "沖繩", "福岡", "名古屋"), "Asia/Tokyo"),
        (("韓國", "首爾", "釜山", "濟州"), "Asia/Seoul"),
        (("泰國", "曼谷", "清邁", "普吉", "喀比"), "Asia/Bangkok"),
    )
    return next(
        (timezone for tokens, timezone in rules if any(token in destination for token in tokens)),
        "UTC",
    )


def localize_itinerary_time(value: datetime | None, timezone_name: str) -> datetime | None:
    """Interpret offset-free editor values as wall-clock times in the trip timezone."""
    if value is None or (value.tzinfo is not None and value.utcoffset() is not None):
        return value
    try:
        timezone = ZoneInfo(timezone_name or "UTC")
    except ZoneInfoNotFoundError:
        timezone = ZoneInfo("UTC")
    return value.replace(tzinfo=timezone)


class ItineraryItemRequest(BaseModel):
    id: UUID | None = None
    item_type: str = Field(min_length=1, max_length=32)
    offer_id: UUID | None = None
    day_date: date
    position: int = Field(ge=0, le=500)
    title: str = Field(min_length=1, max_length=255)
    location_name: str | None = Field(default=None, max_length=255)
    start_time: datetime | None = None
    end_time: datetime | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    locked: bool = False
    is_estimated: bool = False
    data: dict[str, Any] = Field(default_factory=dict)
    provider_place_id: str | None = Field(default=None, max_length=255)
    location_source: str | None = Field(default=None, max_length=32)
    duration_minutes: int | None = Field(default=None, ge=0, le=1440)
    notes: str | None = Field(default=None, max_length=4000)
    fixed_time: bool = False
    system_role: Literal[
        "outbound_flight",
        "hotel_start",
        "lunch",
        "dinner",
        "hotel_end",
        "return_flight",
    ] | None = None
    is_skipped: bool = False


class PrimaryLodgingUpdateRequest(BaseModel):
    version: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=255)
    location_name: str = Field(min_length=1, max_length=255)
    provider_place_id: str | None = Field(default=None, max_length=255)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    location_source: str = Field(default="google_places", min_length=1, max_length=32)

    @model_validator(mode="after")
    def validate_coordinates(self) -> "PrimaryLodgingUpdateRequest":
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("latitude and longitude must be provided together")
        return self


class ScheduleDefaultsUpdateRequest(BaseModel):
    version: int = Field(ge=1)
    lunch_time: str = Field(pattern=r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    lunch_duration_minutes: int = Field(ge=30, le=180)
    dinner_time: str = Field(pattern=r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    dinner_duration_minutes: int = Field(ge=30, le=180)

    @model_validator(mode="after")
    def validate_order(self) -> "ScheduleDefaultsUpdateRequest":
        if self.lunch_time >= self.dinner_time:
            raise ValueError("lunch_time must be before dinner_time")
        return self


class MealSkipRequest(BaseModel):
    version: int = Field(ge=1)
    skipped: bool


class FlightAnchorDetails(BaseModel):
    airline: str = Field(min_length=1, max_length=120)
    flight_number: str = Field(min_length=1, max_length=32)
    origin: str = Field(min_length=1, max_length=16)
    destination: str = Field(min_length=1, max_length=16)
    departure_local: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T(?:[01]\d|2[0-3]):[0-5]\d$"
    )
    arrival_local: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T(?:[01]\d|2[0-3]):[0-5]\d$"
    )
    departure_timezone: str | None = Field(default=None, min_length=1, max_length=64)
    arrival_timezone: str | None = Field(default=None, min_length=1, max_length=64)

    @model_validator(mode="after")
    def normalize_local_details(self) -> "FlightAnchorDetails":
        for field_name in ("airline", "flight_number", "origin", "destination"):
            value = cast(str, getattr(self, field_name)).strip()
            if not value:
                raise ValueError(f"{field_name} must not be blank")
            setattr(self, field_name, value)
        self.origin = self.origin.upper()
        self.destination = self.destination.upper()
        for field_name in ("departure_local", "arrival_local"):
            datetime.fromisoformat(cast(str, getattr(self, field_name)))
        if self.departure_timezone is not None:
            self.departure_timezone = self.departure_timezone.strip() or None
        if self.arrival_timezone is not None:
            self.arrival_timezone = self.arrival_timezone.strip() or None
        return self


class FlightAnchorUpdateRequest(BaseModel):
    version: int = Field(ge=1)
    flight: FlightAnchorDetails | None


class ItineraryUpdateRequest(BaseModel):
    version: int = Field(ge=1)
    items: list[ItineraryItemRequest] = Field(max_length=500)
    route_preference: str | None = None

    @model_validator(mode="after")
    def validate_items(self) -> "ItineraryUpdateRequest":
        if self.route_preference and self.route_preference not in {
            "FEWER_TRANSFERS",
            "LESS_WALKING",
            "FASTEST",
        }:
            raise ValueError("unsupported route preference")
        positions: set[tuple[date, int]] = set()
        for item in self.items:
            key = (item.day_date, item.position)
            if key in positions:
                raise ValueError("positions must be unique within each day")
            positions.add(key)
            if item.start_time and item.end_time and item.end_time <= item.start_time:
                zero_duration_hotel_anchor = (
                    item.system_role in {"hotel_start", "hotel_end"}
                    and item.duration_minutes == 0
                    and item.end_time == item.start_time
                )
                if not zero_duration_hotel_anchor:
                    raise ValueError("end_time must be after start_time")
        return self


class ItineraryGenerateRequest(BaseModel):
    version: int = Field(ge=1)
    scope: Literal["day", "trip"] = "trip"
    day_date: date | None = None

    @model_validator(mode="after")
    def validate_scope(self) -> "ItineraryGenerateRequest":
        if self.scope == "day" and self.day_date is None:
            raise ValueError("day_date is required for day scope")
        if self.scope == "trip" and self.day_date is not None:
            raise ValueError("day_date is only supported for day scope")
        return self


class RouteComputeRequest(BaseModel):
    version: int = Field(ge=1)
    day_date: date | None = None
    from_item_id: UUID | None = None
    to_item_id: UUID | None = None
    route_preference: str | None = None
    travel_mode: TravelMode = "transit"
    buffer_minutes: int = Field(default=DEFAULT_BUFFER_MINUTES, ge=0, le=180)
    refresh: bool = False

    @model_validator(mode="after")
    def validate_scope(self) -> "RouteComputeRequest":
        if (self.from_item_id is None) != (self.to_item_id is None):
            raise ValueError("from_item_id and to_item_id must be provided together")
        if self.route_preference and self.route_preference not in {
            "FEWER_TRANSFERS",
            "LESS_WALKING",
            "FASTEST",
        }:
            raise ValueError("unsupported route preference")
        return self


class RouteDayComputeRequest(BaseModel):
    version: int = Field(ge=1)
    day_date: date
    default_travel_mode: TravelMode = "transit"
    default_buffer_minutes: int = Field(default=DEFAULT_BUFFER_MINUTES, ge=0, le=180)
    route_preference: str = "FEWER_TRANSFERS"
    refresh: bool = False

    @model_validator(mode="after")
    def validate_preference(self) -> "RouteDayComputeRequest":
        if self.route_preference not in {"FEWER_TRANSFERS", "LESS_WALKING", "FASTEST"}:
            raise ValueError("unsupported route preference")
        return self


class TripLocationResolveRequest(BaseModel):
    version: int = Field(ge=1)
    item_ids: list[UUID] | None = Field(default=None, min_length=1, max_length=24)
    day_date: date | None = None

    @model_validator(mode="after")
    def validate_scope(self) -> "TripLocationResolveRequest":
        if self.item_ids is not None and self.day_date is not None:
            raise ValueError("item_ids and day_date cannot be used together")
        return self


class RoutePreviewRequest(BaseModel):
    version: int = Field(ge=1)
    from_item_id: UUID
    to_item_id: UUID
    travel_mode: TravelMode
    buffer_minutes: int = Field(default=DEFAULT_BUFFER_MINUTES, ge=0, le=180)
    route_preference: str | None = None

    @model_validator(mode="after")
    def validate_preference(self) -> "RoutePreviewRequest":
        if self.route_preference and self.route_preference not in {
            "FEWER_TRANSFERS",
            "LESS_WALKING",
            "FASTEST",
        }:
            raise ValueError("unsupported route preference")
        return self


class RouteApplyRequest(BaseModel):
    version: int = Field(ge=1)
    source: Literal["provider", "manual"] = "provider"
    preview_id: UUID | None = None
    from_item_id: UUID | None = None
    to_item_id: UUID | None = None
    travel_mode: TravelMode = "transit"
    duration_minutes: int | None = Field(default=None, ge=1, le=1440)
    buffer_minutes: int = Field(default=DEFAULT_BUFFER_MINUTES, ge=0, le=180)
    note: str | None = Field(default=None, max_length=255)
    inherit_day_default: bool = False

    @model_validator(mode="after")
    def validate_source(self) -> "RouteApplyRequest":
        if self.source == "provider" and self.preview_id is None:
            raise ValueError("preview_id is required for provider routes")
        if self.source == "manual" and (
            self.from_item_id is None
            or self.to_item_id is None
            or self.duration_minutes is None
        ):
            raise ValueError("manual routes require item ids and duration_minutes")
        return self


async def limit_for(session: AsyncSession, user_id: UUID, key: str) -> int:
    _ = session, user_id
    return COMMON_LIMITS.get(key, 0)


def item_record(
    trip_id: UUID,
    item: ItineraryItem | ItineraryItemRequest,
    *,
    preserve_source_id: bool = True,
) -> TripPlanItem:
    item_id = item.id or uuid4()
    if item.id is not None and not preserve_source_id:
        # Optimized itinerary IDs are deterministic for a search. Scope them to
        # the saved trip so two users can persist the same provider result.
        item_id = uuid5(trip_id, str(item.id))
    return TripPlanItem(
        id=item_id,
        trip_plan_id=trip_id,
        item_type=item.item_type,
        offer_id=item.offer_id,
        day_date=item.day_date,
        position=item.position,
        title=item.title,
        location_name=item.location_name,
        start_time=item.start_time,
        end_time=item.end_time,
        latitude=Decimal(str(item.latitude)) if item.latitude is not None else None,
        longitude=Decimal(str(item.longitude)) if item.longitude is not None else None,
        locked=item.locked,
        is_estimated=item.is_estimated,
        data=item.data,
        provider_place_id=getattr(item, "provider_place_id", None),
        location_source=getattr(item, "location_source", None),
        duration_minutes=getattr(item, "duration_minutes", None),
        notes=getattr(item, "notes", None),
        fixed_time=getattr(item, "fixed_time", False),
        system_role=getattr(item, "system_role", None),
        is_skipped=getattr(item, "is_skipped", False),
    )


def apply_item_request(record: TripPlanItem, item: ItineraryItemRequest) -> None:
    record.item_type = item.item_type
    record.offer_id = item.offer_id
    record.day_date = item.day_date
    record.position = item.position
    record.title = item.title
    record.location_name = item.location_name
    record.start_time = item.start_time
    record.end_time = item.end_time
    record.latitude = Decimal(str(item.latitude)) if item.latitude is not None else None
    record.longitude = Decimal(str(item.longitude)) if item.longitude is not None else None
    record.locked = item.locked
    record.is_estimated = item.is_estimated
    record.data = item.data
    record.provider_place_id = item.provider_place_id
    record.location_source = item.location_source
    record.duration_minutes = item.duration_minutes
    record.notes = item.notes
    record.fixed_time = item.fixed_time
    record.system_role = item.system_role
    record.is_skipped = item.is_skipped


def serialize_item(item: TripPlanItem) -> dict[str, Any]:
    return {
        "id": str(item.id),
        "item_type": item.item_type,
        "offer_id": str(item.offer_id) if item.offer_id else None,
        "day_date": item.day_date,
        "position": item.position,
        "title": item.title or item.item_type,
        "location_name": item.location_name,
        "start_time": item.start_time,
        "end_time": item.end_time,
        "latitude": float(item.latitude) if item.latitude is not None else None,
        "longitude": float(item.longitude) if item.longitude is not None else None,
        "locked": item.locked,
        "is_estimated": item.is_estimated,
        "data": item.data,
        "provider_place_id": item.provider_place_id,
        "location_source": item.location_source,
        "location_provider": infer_place_provider(item.location_source, item.data),
        "duration_minutes": item.duration_minutes,
        "notes": item.notes,
        "fixed_time": item.fixed_time,
        "system_role": item.system_role,
        "is_skipped": item.is_skipped,
    }


async def load_items(session: AsyncSession, trip_id: UUID) -> list[TripPlanItem]:
    return list(
        (
            await session.scalars(
                select(TripPlanItem)
                .where(TripPlanItem.trip_plan_id == trip_id)
                .order_by(TripPlanItem.day_date, TripPlanItem.position)
            )
        ).all()
    )


async def hydrate_legacy_items(
    session: AsyncSession, trip: TripPlan, items: list[TripPlanItem]
) -> list[TripPlanItem]:
    changed = False
    if not items:
        raw_days = trip.data.get("itinerary", [])
        for raw_day in raw_days:
            for raw_item in raw_day.get("items", []):
                parsed = ItineraryItem.model_validate(raw_item)
                session.add(item_record(trip.id, parsed, preserve_source_id=False))
        if raw_days:
            await session.flush()
            items = await load_items(session, trip.id)
            changed = True
    if ensure_system_slots(session, trip, items):
        changed = True
    if changed:
        await session.commit()
        return await load_items(session, trip.id)
    return items


async def serialize_trip(
    session: AsyncSession, trip: TripPlan, *, include_items: bool = True
) -> dict[str, Any]:
    items: list[TripPlanItem] = []
    if include_items:
        items = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    share = await session.scalar(
        select(TripShare).where(TripShare.trip_plan_id == trip.id, TripShare.revoked_at.is_(None))
    )
    route_segments: list[dict[str, Any]] = []
    route_records = []
    day_route_settings = []
    if include_items:
        route_records = await load_route_segments(session, trip.id)
        day_route_settings = await load_day_settings(session, trip.id)
        route_segments = [
            segment_from_record(record).model_dump(mode="json") for record in route_records
        ]
        if not route_segments:
            cached_routes = await get_redis().get(f"routes:trip:{trip.id}")
            if cached_routes:
                raw = (
                    cached_routes.decode()
                    if isinstance(cached_routes, bytes)
                    else str(cached_routes)
                )
                try:
                    route_segments = cast(list[dict[str, Any]], json.loads(raw))
                except json.JSONDecodeError:
                    route_segments = []
    return {
        "id": str(trip.id),
        "name": trip.name,
        "mode": trip.mode,
        "total_price": trip.total_price,
        "currency": trip.currency,
        "data": trip.data,
        "primary_lodging": (
            primary_lodging(trip, items)
            if include_items
            else trip.data.get("primary_lodging")
        ),
        "schedule_defaults": schedule_defaults(trip),
        "planning": trip.data.get("planning"),
        "version": trip.version,
        "destination_name": trip.destination_name,
        "destination_place_id": trip.destination_place_id,
        "start_date": trip.start_date,
        "end_date": trip.end_date,
        "timezone": trip.timezone,
        "destination_country_code": trip_region_code(
            trip.timezone, trip.destination_name, trip.data
        ),
        "route_preference": trip.route_preference,
        "items": [serialize_item(item) for item in items],
        "route_segments": route_segments,
        "routing": routing_summary(trip, day_route_settings, route_records),
        "share_enabled": share is not None,
        "created_at": trip.created_at,
        "updated_at": trip.updated_at,
    }


async def owned_trip(session: AsyncSession, user_id: UUID, trip_id: UUID) -> TripPlan:
    trip = await session.scalar(
        select(TripPlan).where(TripPlan.id == trip_id, TripPlan.user_id == user_id)
    )
    if trip is None:
        raise AppError(404, "trip_not_found", "找不到這個已儲存旅程")
    return trip


async def persist_system_schedule_change(
    session: AsyncSession,
    trip: TripPlan,
    user_id: UUID,
    expected_version: int,
    rows: list[TripPlanItem],
    *,
    warning: str,
    target_day: date | None = None,
) -> dict[str, Any]:
    with session.no_autoflush:
        runtime = await load_runtime_settings(session)
        routing_defaults = RoutingOptions.model_validate(
            trip.data.get("routing_defaults") or {}
        )
        routing_available = route_provider_configured(
            runtime,
            trip_region_code(trip.timezone, trip.destination_name, trip.data),
            routing_defaults.default_travel_mode,
        )
        total = route_pair_count(rows)
        status = (
            "queued"
            if routing_defaults.auto_compute and routing_available and total
            else "unavailable"
            if routing_defaults.auto_compute and total
            else "idle"
        )
        next_data = {
            **trip.data,
            "edited": True,
            "routing": {
                "status": status,
                "total": total,
                "completed": 0,
                "warnings": [] if status == "queued" else [warning] if total else [],
                "updated_at": datetime.now(UTC).isoformat(),
            },
        }
        next_version = await session.scalar(
            update(TripPlan)
            .where(
                TripPlan.id == trip.id,
                TripPlan.user_id == user_id,
                TripPlan.version == expected_version,
            )
            .values(version=TripPlan.version + 1, data=next_data)
            .returning(TripPlan.version)
        )
    if next_version is None:
        await session.rollback()
        raise AppError(409, "trip_version_conflict", "旅程已被更新，請重新載入後再操作")
    route_delete = delete(TripRouteSegment).where(TripRouteSegment.trip_plan_id == trip.id)
    if target_day is not None:
        route_delete = route_delete.where(TripRouteSegment.day_date == target_day)
    await session.execute(route_delete)
    await session.commit()
    await get_redis().delete(f"routes:trip:{trip.id}")
    await session.refresh(trip)
    if status == "queued":
        try:
            await asyncio.to_thread(
                enqueue_trip_routing,
                trip.id,
                int(next_version),
                target_day,
            )
        except Exception:
            trip.data = {
                **trip.data,
                "routing": {
                    **cast(dict[str, Any], trip.data.get("routing") or {}),
                    "status": "stale",
                    "warnings": [warning],
                    "updated_at": datetime.now(UTC).isoformat(),
                },
            }
            await session.commit()
            await session.refresh(trip)
    return await serialize_trip(session, trip)


async def persist_information_anchor_change(
    session: AsyncSession,
    trip: TripPlan,
    user_id: UUID,
    expected_version: int,
) -> dict[str, Any]:
    next_version = await session.scalar(
        update(TripPlan)
        .where(
            TripPlan.id == trip.id,
            TripPlan.user_id == user_id,
            TripPlan.version == expected_version,
        )
        .values(
            version=TripPlan.version + 1,
            data={**trip.data, "edited": True},
        )
        .returning(TripPlan.version)
    )
    if next_version is None:
        await session.rollback()
        raise AppError(409, "trip_version_conflict", "旅程已被更新，請重新載入後再操作")
    await session.commit()
    await session.refresh(trip)
    return await serialize_trip(session, trip)


def apply_flight_anchor_details(
    item: TripPlanItem,
    role: Literal["outbound_flight", "return_flight"],
    flight: FlightAnchorDetails | None,
) -> None:
    label = "去程" if role == "outbound_flight" else "回程"
    item.item_type = "flight"
    item.locked = True
    item.fixed_time = True
    item.is_skipped = False
    item.offer_id = None
    item.start_time = None
    item.end_time = None
    item.duration_minutes = None
    item.latitude = None
    item.longitude = None
    item.provider_place_id = None
    item.location_source = None
    item.is_estimated = flight is None
    if flight is None:
        item.title = f"{label}航班尚未設定"
        item.location_name = None
        item.data = {
            **item.data,
            "source_mode": "system",
            "timeline_section": "flight_anchor",
            "flight_selection_source": "unset",
            "flight_info": None,
        }
        return
    details = flight.model_dump()
    item.title = f"{flight.airline.strip()} {flight.flight_number.strip()}"
    item.location_name = f"{flight.origin.strip()} → {flight.destination.strip()}"
    item.data = {
        **item.data,
        "source_mode": "manual",
        "timeline_section": "flight_anchor",
        "flight_leg": "outbound" if role == "outbound_flight" else "return",
        "flight_selection_source": "manual",
        "flight_info": {
            key: value.strip() if isinstance(value, str) else value
            for key, value in details.items()
        },
    }


def _planning_request(
    *,
    destination_name: str,
    start_date: date,
    end_date: date,
    timezone: str,
    route_preference: str,
    travelers: Travelers,
    preferences: SearchPreferences,
    notes: str | None,
    preserved_items: list[TripPlanItem] | None = None,
) -> AIItineraryRequest:
    return AIItineraryRequest(
        destination_name=destination_name,
        start_date=start_date,
        end_date=end_date,
        timezone=timezone,
        route_preference=route_preference,
        travelers=travelers,
        preferences=preferences,
        notes=notes,
        preserved_items=[
            {
                "date": item.day_date.isoformat() if item.day_date else None,
                "title": item.title,
                "location": item.location_name,
                "start_time": item.start_time.isoformat() if item.start_time else None,
                "duration_minutes": item.duration_minutes,
                "locked": item.locked,
                "fixed_time": item.fixed_time,
                "system_role": item.system_role,
                "is_skipped": item.is_skipped,
            }
            for item in (preserved_items or [])
        ],
    )


async def _enrich_ai_places(
    planning: AIPlanningResult,
    google: GoogleTravelService,
    *,
    naver: NaverPlaceService | None = None,
    destination_name: str,
    timezone: str,
) -> None:
    region = _destination_region_values(destination_name, timezone)
    if not google.configured and not (region == "kr" and naver and naver.configured):
        return
    suggestions = [
        item
        for day in planning.itinerary
        for item in day.items
        if item.item_type in {"suggestion", "meal"}
    ][:24]
    semaphore = asyncio.Semaphore(4)

    async def resolve(item: ItineraryItem) -> bool:
        query = f"{item.location_name or item.title}, {destination_name}"
        place: dict[str, Any] = {}
        if region == "kr" and naver and naver.configured:
            async with semaphore:
                place = await naver.search_place(query)
        if not place and google.configured:
            async with semaphore:
                raw_google = await google.search_place(
                    query,
                    None,
                    None,
                    detailed=False,
                    region_code=region,
                )
            if raw_google and _place_matches_region(raw_google, region):
                location = cast(dict[str, Any], raw_google.get("location") or {})
                display = cast(dict[str, Any], raw_google.get("displayName") or {})
                place = {
                    "provider": "google_places",
                    "place_id": raw_google.get("id"),
                    "name": display.get("text") or raw_google.get("formattedAddress"),
                    "address": raw_google.get("formattedAddress"),
                    "latitude": location.get("latitude"),
                    "longitude": location.get("longitude"),
                    "google_maps_url": raw_google.get("googleMapsUri"),
                }
        latitude = place.get("latitude")
        longitude = place.get("longitude")
        if not place or latitude is None or longitude is None:
            item.data = {**item.data, "places_status": "unavailable"}
            return False
        provider = str(place.get("provider") or "google_places")
        item.location_name = str(place.get("name") or place.get("address") or item.location_name)
        item.latitude = float(latitude)
        item.longitude = float(longitude)
        item.provider_place_id = str(place.get("place_id") or "") or None
        item.location_source = f"{provider}_auto"
        item.is_estimated = True
        item.data = {
            **item.data,
            "places_status": "resolved",
            "place_match_status": "auto_matched",
            "needs_place_confirmation": True,
            "place_provider": provider,
            "google_maps_url": place.get("google_maps_url"),
            "naver_maps_url": place.get("naver_maps_url"),
        }
        return True

    try:
        async with asyncio.timeout(10):
            outcomes = await asyncio.gather(*(resolve(item) for item in suggestions))
    except (TimeoutError, httpx.HTTPError):
        planning.planning.status = "partial"
        planning.planning.warnings.append("部分 AI 地點未能在等待時間內完成確認")
        return
    if outcomes and not all(outcomes):
        planning.planning.status = "partial"
        planning.planning.warnings.append("部分 AI 地點仍需由使用者確認")


def route_point(item: TripPlanItem) -> RoutePoint | None:
    if item.latitude is None or item.longitude is None:
        return None
    return RoutePoint(
        item_id=item.id,
        name=item.location_name or item.title or item.item_type,
        latitude=float(item.latitude),
        longitude=float(item.longitude),
        provider_place_id=item.provider_place_id,
        place_provider=infer_place_provider(item.location_source, item.data),
    )


def _destination_region_values(destination_name: str | None, timezone: str | None) -> str | None:
    destination = f"{destination_name or ''} {timezone or ''}"
    japan_tokens = ("日本", "東京", "大阪", "京都", "Japan", "Tokyo", "Asia/Tokyo")
    korea_tokens = ("韓國", "首爾", "釜山", "Korea", "Seoul", "Asia/Seoul")
    thailand_tokens = ("泰國", "曼谷", "Thailand", "Bangkok", "Asia/Bangkok")
    if any(token in destination for token in japan_tokens):
        return "jp"
    if any(token in destination for token in korea_tokens):
        return "kr"
    if any(token in destination for token in thailand_tokens):
        return "th"
    return None


def _destination_region(trip: TripPlan) -> str | None:
    return _destination_region_values(trip.destination_name, trip.timezone)


def _place_matches_region(place: dict[str, Any], region: str | None) -> bool:
    if region is None:
        return True
    address = str(place.get("formattedAddress") or "").casefold()
    region_tokens = {
        "jp": ("日本", "japan", " jp"),
        "kr": ("韓國", "韩国", "korea", " kr"),
        "th": ("泰國", "泰国", "thailand", " th"),
    }
    return bool(address) and any(token in address for token in region_tokens.get(region, ()))


def _unresolved_location(item: TripPlanItem, reason: str) -> dict[str, str]:
    return {
        "item_id": str(item.id),
        "title": item.title or item.item_type,
        "reason": reason,
    }


async def _resolve_trip_locations(
    session: AsyncSession,
    trip: TripPlan,
    rows: list[TripPlanItem],
    *,
    item_ids: set[UUID] | None = None,
    day_value: date | None = None,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    candidates = [
        row
        for row in rows
        if (item_ids is None or row.id in item_ids)
        and (day_value is None or row.day_date == day_value)
        and (row.latitude is None or row.longitude is None)
    ]
    if not candidates:
        return [], []
    runtime = await load_runtime_settings(session)
    redis = get_redis()
    google = GoogleTravelService(redis, runtime)
    naver = NaverPlaceService(redis, runtime)
    region = _destination_region(trip)
    if not google.configured and not (region == "kr" and naver.configured):
        return [], [
            _unresolved_location(item, "旅程目的地的地點搜尋服務尚未設定")
            for item in candidates
        ]
    reference = next(
        (row for row in rows if row.latitude is not None and row.longitude is not None),
        None,
    )
    latitude = float(reference.latitude) if reference and reference.latitude is not None else None
    longitude = (
        float(reference.longitude) if reference and reference.longitude is not None else None
    )
    matched: list[dict[str, str]] = []
    unresolved: list[dict[str, str]] = []
    changed_ids: set[UUID] = set()
    for item in candidates[:24]:
        label = (item.location_name or item.title or "").strip()
        if not label or label in {"新的行程安排", "尚未選擇地點"}:
            unresolved.append(_unresolved_location(item, "尚未輸入可辨識的地點名稱"))
            continue
        query = label
        destination = (trip.destination_name or "").strip()
        if destination and destination.casefold() not in query.casefold():
            query = f"{query}, {destination}"
        try:
            place: dict[str, Any] = {}
            if region == "kr" and naver.configured:
                place = await naver.search_place(query)
            if not place and google.configured:
                raw_google = await google.search_place(
                    query,
                    latitude,
                    longitude,
                    detailed=False,
                    region_code=region,
                )
                if raw_google and _place_matches_region(raw_google, region):
                    location = cast(dict[str, Any], raw_google.get("location") or {})
                    display = cast(dict[str, Any], raw_google.get("displayName") or {})
                    place = {
                        "provider": "google_places",
                        "place_id": raw_google.get("id"),
                        "name": display.get("text") or raw_google.get("formattedAddress"),
                        "address": raw_google.get("formattedAddress"),
                        "latitude": location.get("latitude"),
                        "longitude": location.get("longitude"),
                        "google_maps_url": raw_google.get("googleMapsUri"),
                    }
        except (httpx.HTTPError, TimeoutError):
            unresolved.append(_unresolved_location(item, "地點搜尋服務暫時無法回應"))
            continue
        place_latitude = place.get("latitude")
        place_longitude = place.get("longitude")
        if (
            not place
            or place_latitude is None
            or place_longitude is None
        ):
            unresolved.append(_unresolved_location(item, "找不到位於旅程目的地的可靠候選"))
            continue
        provider = str(place.get("provider") or "google_places")
        item.location_name = str(place.get("name") or place.get("address") or label)
        item.latitude = Decimal(str(place_latitude))
        item.longitude = Decimal(str(place_longitude))
        item.provider_place_id = str(place.get("place_id") or "") or None
        item.location_source = f"{provider}_auto"
        item.is_estimated = True
        item.data = {
            **(item.data or {}),
            "places_status": "resolved",
            "place_match_status": "auto_matched",
            "needs_place_confirmation": True,
            "place_provider": provider,
            "google_maps_url": place.get("google_maps_url"),
            "naver_maps_url": place.get("naver_maps_url"),
        }
        changed_ids.add(item.id)
        matched.append({"item_id": str(item.id), "title": item.title or item.item_type})
    if changed_ids:
        await session.execute(
            delete(TripRouteSegment).where(
                TripRouteSegment.trip_plan_id == trip.id,
                TripRouteSegment.from_item_id.in_(changed_ids),
            )
        )
        await session.execute(
            delete(TripRouteSegment).where(
                TripRouteSegment.trip_plan_id == trip.id,
                TripRouteSegment.to_item_id.in_(changed_ids),
            )
        )
    return matched, unresolved


async def cache_trip_routes(trip_id: UUID, segments: list[RouteSegment]) -> None:
    redis = get_redis()
    key = f"routes:trip:{trip_id}"
    existing: list[dict[str, Any]] = []
    cached = await redis.get(key)
    if cached:
        raw = cached.decode() if isinstance(cached, bytes) else str(cached)
        try:
            existing = cast(list[dict[str, Any]], json.loads(raw))
        except json.JSONDecodeError:
            existing = []
    replacements = {(str(row.from_item_id), str(row.to_item_id)) for row in segments}
    merged = [
        row
        for row in existing
        if (str(row.get("from_item_id")), str(row.get("to_item_id"))) not in replacements
    ]
    merged.extend(segment.model_dump(mode="json") for segment in segments)
    await redis.set(key, json.dumps(merged, ensure_ascii=False), ex=86_400)


async def compute_routes_for_rows(
    trip: TripPlan,
    rows: list[TripPlanItem],
    preference: str,
    settings: Settings,
    *,
    travel_mode: TravelMode = "transit",
    buffer_minutes: int = DEFAULT_BUFFER_MINUTES,
    refresh: bool = False,
) -> tuple[list[RouteSegment], list[tuple[UUID, UUID]]]:
    rows = active_route_rows(rows)
    pairs: list[tuple[RoutePoint, RoutePoint, datetime | None]] = []
    pair_ids: list[tuple[UUID, UUID]] = []
    for first, second in zip(rows, rows[1:], strict=False):
        origin, destination = route_point(first), route_point(second)
        if origin is None or destination is None:
            pair_ids.append((first.id, second.id))
            continue
        pairs.append((origin, destination, first.end_time or first.start_time))
    service = RouteService(get_redis(), settings)
    results = await service.compute_many(
        pairs,
        preference,
        region_code=trip_region_code(trip.timezone, trip.destination_name, trip.data),
        travel_mode=travel_mode,
        refresh=refresh,
    )
    segments = [
        result.model_copy(update={"buffer_minutes": buffer_minutes})
        for result in results
        if result is not None
    ]
    failed = [
        (pair[0].item_id, pair[1].item_id)
        for pair, result in zip(pairs, results, strict=True)
        if result is None
    ]
    failed.extend(pair_ids)
    return segments, failed


async def run_provider_module(
    provider: object,
    runner: ProviderRunner,
    module: str,
    query: SearchCreate,
) -> list[Offer]:
    if module == "flight":
        flight_provider = cast(FlightProvider, provider)
        return cast(
            list[Offer],
            await runner.run(
                flight_provider.name, module, lambda: flight_provider.search_flights(query)
            ),
        )
    if module == "hotel":
        hotel_provider = cast(HotelProvider, provider)
        return cast(
            list[Offer],
            await runner.run(
                hotel_provider.name, module, lambda: hotel_provider.search_hotels(query)
            ),
        )
    if module == "activities":
        activity_provider = cast(ActivityProvider, provider)
        return cast(
            list[Offer],
            await runner.run(
                activity_provider.name,
                module,
                lambda: activity_provider.search_activities(query),
            ),
        )
    if module == "transport":
        transport_provider = cast(TransportProvider, provider)
        return cast(
            list[Offer],
            await runner.run(
                transport_provider.name,
                module,
                lambda: transport_provider.search_transport(query),
            ),
        )
    return []


async def refreshed_plan(session: AsyncSession, trip: TripPlan) -> tuple[TripPlanResult, list[str]]:
    search = await session.get(SearchRequest, trip.search_id)
    if search is None:
        raise AppError(409, "trip_search_missing", "原始搜尋已無法使用")
    query = SearchCreate.model_validate(search.request_json)
    redis = get_redis()
    settings = await load_runtime_settings(session)
    providers = build_module_provider_candidates(redis, settings)
    status = provider_status_for_modules([str(module) for module in query.modules], settings)
    if not any(providers.get(str(module)) for module in query.modules):
        raise AppError(503, "travel_provider_unavailable", status.message)
    runner = ProviderRunner(redis, settings)

    async def collect(module: str) -> tuple[str, list[Offer], str | None]:
        candidates = providers.get(module, [])
        if not candidates:
            module_status = status.module_statuses.get(module)
            return module, [], module_status.message if module_status else "供應商尚未設定"
        primary_name = str(getattr(candidates[0], "name", "unknown"))
        for index, provider in enumerate(candidates):
            try:
                offers = await run_provider_module(provider, runner, module, query)
                warning = None
                if index > 0:
                    offers = [offer.model_copy(update={"is_fallback": True}) for offer in offers]
                    warning = (
                        f"{module} 主要供應商 {primary_name} 暫時無法使用，"
                        f"已切換至 {getattr(provider, 'name', 'backup')}。"
                    )
                return module, offers, warning
            except ProviderUnavailableError as exc:
                if index + 1 == len(candidates):
                    return module, [], str(exc)
        return module, [], "供應商目前無法使用"

    refreshed = await asyncio.gather(*(collect(str(module)) for module in query.modules))
    offers = {module: rows for module, rows, _ in refreshed}
    warnings = [warning for _, _, warning in refreshed if warning]
    place_service = GoogleTravelService(redis, settings, locale=query.locale)
    hotels = [item for item in offers.get("hotel", []) if isinstance(item, HotelOffer)]
    activities = [item for item in offers.get("activities", []) if isinstance(item, ActivityOffer)]
    if place_service.configured:
        hotels, activities = await asyncio.gather(
            place_service.enrich_hotels(hotels),
            place_service.enrich_activities(activities),
        )
    trip_days = (
        (query.return_date - query.departure_date).days + 1
        if query.return_date and query.departure_date
        else 4
    )
    hotspots = (
        await load_planner_hotspots(
            session,
            city_code=query.destination,
            interests=query.preferences.interests,
            limit=12,
            extension_destination_ids=query.preferences.extension_destination_ids,
            days=trip_days,
        )
        if (
            "deep_travel" in query.preferences.interests
            or query.preferences.extension_destination_ids
        )
        and query.destination
        else []
    )
    destination = destination_for_code(query.destination)
    foods = (
        await load_planner_foods(
            session,
            destination_id=destination.id,
            locale=query.locale,
            days=trip_days,
            limit=10,
        )
        if "food" in query.preferences.interests and destination
        else []
    )
    plans = TripOptimizer().optimize(
        query,
        [item for item in offers.get("flight", []) if isinstance(item, FlightOffer)],
        hotels,
        activities,
        [item for item in offers.get("transport", []) if isinstance(item, TransportOffer)],
        hotspots,
        foods,
    )
    if not plans:
        detail = "；".join(warnings) or "供應商目前沒有可用組合"
        raise AppError(503, "trip_reoptimization_unavailable", detail)
    selected = next((plan for plan in plans if plan.mode == trip.mode), plans[0])
    if place_service.configured:
        await place_service.enrich_itinerary(selected.itinerary)
    return selected, warnings


@router.post("", status_code=201)
async def save_trip(
    payload: SaveTripRequest, user: CurrentUser, session: Session
) -> dict[str, Any]:
    count = await session.scalar(
        select(func.count()).select_from(TripPlan).where(TripPlan.user_id == user.id)
    )
    if int(count or 0) >= await limit_for(session, user.id, "saved_trips"):
        raise AppError(403, "trip_limit_reached", "已達所有會員共用的 20 筆儲存旅程上限")
    if payload.source == "blank":
        destination = payload.destination_name or "未命名目的地"
        timezone = payload.timezone or destination_timezone(destination)
        preferences = payload.preferences.model_dump(mode="json")
        settings = await load_runtime_settings(session)
        planning = await AIItineraryPlanner(settings).generate(
            _planning_request(
                destination_name=destination,
                start_date=cast(date, payload.start_date),
                end_date=cast(date, payload.end_date),
                timezone=timezone,
                route_preference=payload.route_preference,
                travelers=payload.travelers,
                preferences=payload.preferences,
                notes=payload.notes,
            )
        )
        await _enrich_ai_places(
            planning,
            GoogleTravelService(get_redis(), settings),
            naver=NaverPlaceService(get_redis(), settings),
            destination_name=destination,
            timezone=timezone,
        )
        # The two hotel anchors are reconciled immediately after persistence, so
        # each day has one more adjacent pair than the generated activity/meal rows.
        route_pairs = sum(len(day.items) + 1 for day in planning.itinerary)
        routing_available = route_provider_configured(
            settings,
            trip_region_code(timezone, destination, {}),
            payload.routing.default_travel_mode,
        )
        routing_status = (
            "queued"
            if payload.routing.auto_compute and route_pairs and routing_available
            else "unavailable"
            if payload.routing.auto_compute and route_pairs
            else "idle"
        )
        trip = TripPlan(
            user_id=user.id,
            search_id=None,
            name=payload.name,
            mode="manual",
            total_price=Decimal(0),
            currency="TWD",
            data={
                "source": "blank",
                "destination_city": destination,
                "destination_country": {
                    "Asia/Tokyo": "日本",
                    "Asia/Seoul": "韓國",
                    "Asia/Bangkok": "泰國",
                }.get(timezone),
                "travelers": payload.travelers.model_dump(mode="json"),
                "preferences": preferences,
                "notes": payload.notes,
                "planning": planning.planning.model_dump(mode="json"),
                "routing_defaults": payload.routing.model_dump(mode="json"),
                "routing": {
                    "status": routing_status,
                    "total": route_pairs,
                    "completed": 0,
                    "warnings": (
                        []
                        if routing_status != "unavailable"
                        else ["路線服務尚未啟用，可先使用手動移動時間。"]
                    ),
                    "updated_at": datetime.now(UTC).isoformat(),
                },
            },
            version=1,
            destination_name=destination,
            destination_place_id=payload.destination_place_id,
            start_date=payload.start_date,
            end_date=payload.end_date,
            timezone=timezone,
            route_preference=payload.route_preference,
        )
        session.add(trip)
        await session.flush()
        for day in planning.itinerary:
            for item in day.items:
                session.add(item_record(trip.id, item, preserve_source_id=False))
        await session.commit()
        await session.refresh(trip)
        result = await serialize_trip(session, trip)
        if routing_status == "queued":
            try:
                await asyncio.to_thread(enqueue_trip_routing, trip.id, trip.version)
            except Exception:
                trip.data = {
                    **trip.data,
                    "routing": {
                        "status": "failed",
                        "total": route_pairs,
                        "completed": 0,
                        "warnings": ["背景路線服務暫時無法使用，可在行程頁重新計算。"],
                        "updated_at": datetime.now(UTC).isoformat(),
                    },
                }
                await session.commit()
                result["routing"] = trip.data["routing"]
        return result

    search = await session.scalar(
        select(SearchRequest).where(
            SearchRequest.id == payload.search_id, SearchRequest.user_id == user.id
        )
    )
    if search is None:
        raise AppError(404, "search_not_found", "找不到這次搜尋")
    plan = next(
        (
            item
            for item in search.result_json.get("plans", [])
            if item.get("id") == str(payload.plan_id)
        ),
        None,
    )
    if plan is None:
        raise AppError(404, "plan_not_found", "找不到最佳化方案")
    itinerary_days = cast(list[dict[str, Any]], plan.get("itinerary", []))
    first_item_data = next(
        (
            cast(dict[str, Any], raw_item.get("data") or {})
            for raw_day in itinerary_days
            for raw_item in cast(list[dict[str, Any]], raw_day.get("items", []))
        ),
        {},
    )
    trip = TripPlan(
        user_id=user.id,
        search_id=search.id,
        name=payload.name,
        mode=plan["mode"],
        total_price=Decimal(str(plan["total_cost"]["total_cost"])),
        data=plan,
        version=1,
        destination_name=first_item_data.get("destination_city"),
        start_date=next(
            (date.fromisoformat(str(day["date"])) for day in itinerary_days if day.get("date")),
            None,
        ),
        end_date=next(
            (
                date.fromisoformat(str(day["date"]))
                for day in reversed(itinerary_days)
                if day.get("date")
            ),
            None,
        ),
        timezone=first_item_data.get("destination_timezone", "UTC"),
        route_preference="FEWER_TRANSFERS",
    )
    session.add(trip)
    await session.flush()
    for raw_day in itinerary_days:
        for raw_item in raw_day.get("items", []):
            session.add(
                item_record(
                    trip.id,
                    ItineraryItem.model_validate(raw_item),
                    preserve_source_id=False,
                )
            )
    await session.commit()
    await session.refresh(trip)
    return await serialize_trip(session, trip)


@router.get("")
async def list_trips(user: CurrentUser, session: Session) -> list[dict[str, Any]]:
    trips = list(
        (
            await session.scalars(
                select(TripPlan)
                .where(TripPlan.user_id == user.id)
                .order_by(TripPlan.created_at.desc())
            )
        ).all()
    )
    return [await serialize_trip(session, trip, include_items=False) for trip in trips]


@router.get("/{trip_id}")
async def get_trip(trip_id: UUID, user: CurrentUser, session: Session) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    return await serialize_trip(session, trip)


@router.get("/{trip_id}/weather", response_model=TripWeather)
async def get_trip_weather(
    trip_id: UUID,
    user: CurrentUser,
    session: Session,
) -> TripWeather:
    trip = await owned_trip(session, user.id, trip_id)
    settings = await load_runtime_settings(session)
    if not settings.google_maps_api_key:
        raise AppError(
            503,
            "weather_not_configured",
            "Google Weather 尚未設定，請先在管理後台設定伺服器 API 金鑰",
        )
    await enforce_named_rate_limit(
        "trip-weather-user",
        str(user.id),
        limit=TRIP_WEATHER_USER_LIMIT,
        window_seconds=TRIP_WEATHER_USER_WINDOW_SECONDS,
    )
    rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    located_rows = [
        item for item in rows if item.latitude is not None and item.longitude is not None
    ]
    preferred_types = {"activity", "hotel", "suggestion", "accommodation"}
    located = next(
        (item for item in located_rows if item.item_type in preferred_types),
        located_rows[0] if located_rows else None,
    )
    location_name = trip.destination_name or (
        located.location_name if located and located.location_name else trip.name
    )
    latitude = float(located.latitude) if located and located.latitude is not None else None
    longitude = float(located.longitude) if located and located.longitude is not None else None
    if latitude is None or longitude is None:
        place = await GoogleTravelService(get_redis(), settings).search_place(
            trip.destination_name or trip.name,
            None,
            None,
            detailed=False,
        )
        location = cast(dict[str, Any], place.get("location") or {})
        if location.get("latitude") is not None and location.get("longitude") is not None:
            latitude = float(location["latitude"])
            longitude = float(location["longitude"])
            display = cast(dict[str, Any], place.get("displayName") or {})
            location_name = str(display.get("text") or location_name)
    if latitude is None or longitude is None:
        raise AppError(
            422,
            "weather_location_unavailable",
            "旅程尚無可用座標，請先確認至少一個行程地點",
        )

    weather = await GoogleWeatherService(get_redis(), settings).lookup(
        latitude=latitude,
        longitude=longitude,
        location_name=location_name,
    )
    warnings = list(weather.warnings)
    if (
        weather.available_start_date
        and weather.available_end_date
        and trip.start_date
        and trip.end_date
    ):
        if trip.end_date < weather.available_start_date:
            warnings.append("旅程日期已過，Google Weather 不提供這段期間的歷史預報")
        elif trip.start_date > weather.available_end_date:
            warnings.append("旅程日期超出目前 10 日預報範圍")
        elif (
            trip.start_date < weather.available_start_date
            or trip.end_date > weather.available_end_date
        ):
            warnings.append("目前只能顯示旅程中落在 10 日預報範圍內的日期")
    return weather.model_copy(update={"warnings": list(dict.fromkeys(warnings))})


@router.put("/{trip_id}/itinerary")
async def update_itinerary(
    trip_id: UUID,
    payload: ItineraryUpdateRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    previous_routing = cast(dict[str, Any], trip.data.get("routing") or {})
    existing_rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    existing_by_id = {row.id: row for row in existing_rows}
    incoming_items = [
        item.model_copy(
            update={
                "start_time": localize_itinerary_time(item.start_time, trip.timezone),
                "end_time": localize_itinerary_time(item.end_time, trip.timezone),
            }
        )
        for item in payload.items
    ]
    incoming_ids = {item.id for item in incoming_items if item.id is not None}
    incoming_items.extend(
        ItineraryItemRequest.model_validate(serialize_item(row))
        for row in existing_rows
        if row.system_role is not None and row.id not in incoming_ids
    )
    for item in incoming_items:
        existing = existing_by_id.get(item.id) if item.id is not None else None
        if existing is None and item.system_role is not None:
            raise AppError(
                422,
                "system_itinerary_item_immutable",
                "固定航班、飯店與餐食卡只能由系統建立",
            )
        if existing is not None and existing.system_role is not None and (
            item.system_role != existing.system_role or item.day_date != existing.day_date
        ):
            raise AppError(
                422,
                "system_itinerary_item_immutable",
                "固定航班、飯店與餐食卡不可改變日期或類型",
            )
    if trip.start_date and any(
        item.day_date < trip.start_date or (trip.end_date and item.day_date > trip.end_date)
        for item in incoming_items
    ):
        raise AppError(422, "itinerary_date_out_of_range", "行程項目日期超出旅程範圍")
    next_data = {
        **trip.data,
        "edited": True,
        "routing": {
            "status": "stale",
            "total": route_pair_count(existing_rows),
            "completed": 0,
            "warnings": ["行程已變更，受影響的移動時間需要重新計算。"],
            "updated_at": datetime.now(UTC).isoformat(),
        },
    }
    next_version = await session.scalar(
        update(TripPlan)
        .where(
            TripPlan.id == trip.id,
            TripPlan.user_id == user.id,
            TripPlan.version == payload.version,
        )
        .values(version=TripPlan.version + 1, data=next_data)
        .returning(TripPlan.version)
    )
    if next_version is None:
        await session.rollback()
        raise AppError(409, "trip_version_conflict", "旅程已被更新，請重新載入後再儲存")
    def adjacent_pairs(values: list[TripPlanItem]) -> set[tuple[UUID, UUID]]:
        pairs: set[tuple[UUID, UUID]] = set()
        for day_value in {row.day_date for row in values}:
            day_rows = active_route_rows(values, day_value)
            pairs.update(
                (first.id, second.id)
                for first, second in zip(day_rows, day_rows[1:], strict=False)
            )
        return pairs

    old_pairs = adjacent_pairs(existing_rows)
    incoming_ids = {item.id for item in incoming_items if item.id is not None}
    removed_ids = {
        item_id
        for item_id, row in existing_by_id.items()
        if item_id not in incoming_ids and row.system_role is None
    }
    if removed_ids:
        await session.execute(
            delete(TripPlanItem).where(
                TripPlanItem.trip_plan_id == trip.id,
                TripPlanItem.id.in_(removed_ids),
            )
        )
    route_impact_ids: set[UUID] = set(removed_ids)
    next_rows: list[TripPlanItem] = []
    new_route_rows: list[TripPlanItem] = []
    for item in incoming_items:
        row = existing_by_id.get(item.id) if item.id is not None else None
        if row is None:
            row = item_record(trip.id, item)
            session.add(row)
            new_route_rows.append(row)
        else:
            before = (
                row.day_date,
                row.position,
                row.start_time,
                row.end_time,
                row.latitude,
                row.longitude,
                row.provider_place_id,
                row.duration_minutes,
                row.fixed_time,
                row.is_skipped,
            )
            if row.system_role is not None:
                protected: dict[str, Any] = {
                    "position": row.position,
                    "locked": True,
                    "fixed_time": row.system_role
                    in {
                        "outbound_flight",
                        "hotel_start",
                        "lunch",
                        "dinner",
                        "return_flight",
                    },
                    "start_time": row.start_time,
                    "end_time": row.end_time,
                    "duration_minutes": row.duration_minutes,
                    "is_skipped": row.is_skipped,
                }
                if row.system_role in {
                    "outbound_flight",
                    "hotel_start",
                    "hotel_end",
                    "return_flight",
                }:
                    protected.update(
                        {
                            "title": row.title,
                            "location_name": row.location_name,
                            "latitude": row.latitude,
                            "longitude": row.longitude,
                            "provider_place_id": row.provider_place_id,
                            "location_source": row.location_source,
                            "is_estimated": row.is_estimated,
                            "notes": row.notes,
                            "data": row.data,
                        }
                    )
                item = item.model_copy(update=protected)
            after = (
                item.day_date,
                item.position,
                item.start_time,
                item.end_time,
                Decimal(str(item.latitude)) if item.latitude is not None else None,
                Decimal(str(item.longitude)) if item.longitude is not None else None,
                item.provider_place_id,
                item.duration_minutes,
                item.fixed_time,
                item.is_skipped,
            )
            if before != after:
                route_impact_ids.add(row.id)
            apply_item_request(row, item)
        next_rows.append(row)

    canonicalize_positions(next_rows)

    if new_route_rows:
        await session.flush()
        route_impact_ids.update(row.id for row in new_route_rows)
    new_pairs = adjacent_pairs(next_rows)
    invalid_pairs = (old_pairs - new_pairs) | {
        pair for pair in old_pairs | new_pairs if set(pair) & route_impact_ids
    }
    if payload.route_preference and payload.route_preference != trip.route_preference:
        invalid_pairs.update(new_pairs)
    for from_id, to_id in invalid_pairs:
        await session.execute(
            delete(TripRouteSegment).where(
                TripRouteSegment.trip_plan_id == trip.id,
                TripRouteSegment.from_item_id == from_id,
                TripRouteSegment.to_item_id == to_id,
            )
        )
    if not invalid_pairs:
        trip.data = {**trip.data, "routing": previous_routing}
    if payload.route_preference:
        trip.route_preference = payload.route_preference
    await session.commit()
    await get_redis().delete(f"routes:trip:{trip.id}")
    await session.refresh(trip)
    if invalid_pairs:
        routing_defaults = RoutingOptions.model_validate(
            trip.data.get("routing_defaults") or {}
        )
        runtime = await load_runtime_settings(session)
        routing_available = route_provider_configured(
            runtime,
            trip_region_code(trip.timezone, trip.destination_name, trip.data),
            routing_defaults.default_travel_mode,
        )
        if routing_defaults.auto_compute and routing_available:
            trip.data = {
                **trip.data,
                "routing": {
                    "status": "queued",
                    "total": max(
                        0,
                        route_pair_count(next_rows),
                    ),
                    "completed": 0,
                    "warnings": [],
                    "updated_at": datetime.now(UTC).isoformat(),
                },
            }
            await session.commit()
            try:
                await asyncio.to_thread(enqueue_trip_routing, trip.id, int(next_version))
            except Exception:
                trip.data = {
                    **trip.data,
                    "routing": {
                        "status": "stale",
                        "total": max(
                            0,
                            route_pair_count(next_rows),
                        ),
                        "completed": 0,
                        "warnings": ["行程已變更，請在行程頁重新計算移動時間。"],
                        "updated_at": datetime.now(UTC).isoformat(),
                    },
                }
                await session.commit()
            await session.refresh(trip)
    return await serialize_trip(session, trip)


@router.put("/{trip_id}/primary-lodging")
async def update_primary_lodging(
    trip_id: UUID,
    payload: PrimaryLodgingUpdateRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    lodging = {
        "name": payload.name.strip(),
        "location_name": payload.location_name.strip(),
        "provider_place_id": payload.provider_place_id,
        "latitude": payload.latitude,
        "longitude": payload.longitude,
        "location_source": payload.location_source,
    }
    sync_primary_lodging(trip, rows, lodging)
    return await persist_system_schedule_change(
        session,
        trip,
        user.id,
        payload.version,
        rows,
        warning="主要飯店已更新，請重新計算每日來回路線。",
    )


@router.put("/{trip_id}/schedule-defaults")
async def update_schedule_defaults(
    trip_id: UUID,
    payload: ScheduleDefaultsUpdateRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    trip.data = {
        **trip.data,
        "schedule_defaults": {
            **schedule_defaults(trip),
            **payload.model_dump(exclude={"version"}),
        },
    }
    apply_schedule_defaults(trip, rows)
    return await persist_system_schedule_change(
        session,
        trip,
        user.id,
        payload.version,
        rows,
        warning="餐食時間已更新，請重新計算受影響的移動時間。",
    )


@router.put("/{trip_id}/flight-anchors/{direction}")
async def update_flight_anchor(
    trip_id: UUID,
    direction: Literal["outbound", "return"],
    payload: FlightAnchorUpdateRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    role: Literal["outbound_flight", "return_flight"] = (
        "outbound_flight" if direction == "outbound" else "return_flight"
    )
    item = next((row for row in rows if row.system_role == role), None)
    if item is None:
        raise AppError(422, "flight_anchor_unavailable", "旅程日期不完整，無法設定航班")
    apply_flight_anchor_details(item, role, payload.flight)
    return await persist_information_anchor_change(
        session,
        trip,
        user.id,
        payload.version,
    )


@router.patch("/{trip_id}/items/{item_id}/skip")
async def update_meal_skip(
    trip_id: UUID,
    item_id: UUID,
    payload: MealSkipRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    item = next((row for row in rows if row.id == item_id), None)
    if item is None:
        raise AppError(404, "trip_item_not_found", "找不到這張餐食卡")
    if item.system_role not in {"lunch", "dinner"}:
        raise AppError(422, "meal_skip_not_supported", "只有午餐與晚餐可以跳過")
    item.is_skipped = payload.skipped
    return await persist_system_schedule_change(
        session,
        trip,
        user.id,
        payload.version,
        rows,
        warning="餐食狀態已更新，請重新計算這一天的路線。",
        target_day=item.day_date,
    )


@router.post("/{trip_id}/itinerary/generate")
async def generate_trip_itinerary(
    trip_id: UUID,
    payload: ItineraryGenerateRequest,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    if not trip.destination_name or not trip.start_date or not trip.end_date:
        raise AppError(422, "trip_planning_fields_missing", "旅程缺少目的地或日期，無法重新排行程")
    target_date = payload.day_date if payload.scope == "day" else None
    if target_date and not (trip.start_date <= target_date <= trip.end_date):
        raise AppError(422, "itinerary_date_out_of_range", "AI 單日安排的日期超出旅程範圍")
    scope_label = target_date.isoformat() if target_date else "全行程"
    reservation, created = await reserve_use(
        session,
        user.id,
        idempotency_key,
        "ai_itinerary_generation",
        f"AI 重新排行程：{trip.name}（{scope_label}）",
    )
    if not created and reservation.resource_id == trip.id:
        replay = await serialize_trip(session, trip)
        replay["usage"] = usage_status(reservation).model_dump()
        return replay
    reservation.resource_id = trip.id
    reservation_id = reservation.id
    try:
        if trip.version != payload.version:
            raise AppError(409, "trip_version_conflict", "旅程已被更新，請重新載入後再讓 AI 重排")
        existing = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
        replaceable = [
            item
            for item in existing
            if item.data.get("generated_by") == "ai_planner"
            and not item.locked
            and not item.fixed_time
            and (target_date is None or item.day_date == target_date)
        ]
        replaceable_ids = {item.id for item in replaceable}
        preserved = [item for item in existing if item.id not in replaceable_ids]
        planning_preserved = [
            item
            for item in preserved
            if (target_date is None or item.day_date == target_date)
            and item.system_role not in {"outbound_flight", "return_flight"}
            and (
                item.system_role not in {"lunch", "dinner"}
                or item.data.get("meal_selection_source") == "user"
            )
        ]
        travelers = Travelers.model_validate(trip.data.get("travelers", {}))
        preferences = SearchPreferences.model_validate(trip.data.get("preferences", {}))
        settings = await load_runtime_settings(session)
        planning = await AIItineraryPlanner(settings).generate(
            _planning_request(
                destination_name=trip.destination_name,
                start_date=target_date or trip.start_date,
                end_date=target_date or trip.end_date,
                timezone=trip.timezone or "UTC",
                route_preference=trip.route_preference,
                travelers=travelers,
                preferences=preferences,
                notes=cast(str | None, trip.data.get("notes")),
                preserved_items=planning_preserved,
            )
        )
        await _enrich_ai_places(
            planning,
            GoogleTravelService(get_redis(), settings),
            naver=NaverPlaceService(get_redis(), settings),
            destination_name=trip.destination_name,
            timezone=trip.timezone or "UTC",
        )
        meals_by_role = {
            (item.day_date, item.system_role): item
            for item in preserved
            if item.system_role in {"lunch", "dinner"}
        }
        generated_meals = [
            item
            for day in planning.itinerary
            for item in day.items
            if item.system_role in {"lunch", "dinner"}
        ]
        for meal in generated_meals:
            meal_role = cast(str, meal.system_role)
            current_meal = meals_by_role.get((meal.day_date, meal_role))
            if (
                current_meal is None
                or current_meal.data.get("meal_selection_source") == "user"
            ):
                continue
            current_meal.title = meal.title
            current_meal.location_name = meal.location_name
            current_meal.latitude = (
                Decimal(str(meal.latitude)) if meal.latitude is not None else None
            )
            current_meal.longitude = (
                Decimal(str(meal.longitude)) if meal.longitude is not None else None
            )
            current_meal.provider_place_id = meal.provider_place_id
            current_meal.location_source = meal.location_source
            current_meal.is_estimated = meal.is_estimated
            current_meal.notes = meal.notes
            current_meal.data = {
                **current_meal.data,
                **meal.data,
                "meal_selection_source": "ai",
            }
        preserved_keys = {(item.day_date, (item.title or "").casefold()) for item in preserved}
        generated = [
            item
            for day in planning.itinerary
            for item in day.items
            if item.system_role is None
            if (item.day_date, item.title.casefold()) not in preserved_keys
        ]
        if replaceable_ids:
            await session.execute(
                delete(TripPlanItem).where(
                    TripPlanItem.trip_plan_id == trip.id,
                    TripPlanItem.id.in_(replaceable_ids),
                )
            )
        generated_records = [
            item_record(trip.id, item, preserve_source_id=False) for item in generated
        ]
        for record in generated_records:
            session.add(record)
        all_rows = [*preserved, *generated_records]
        canonicalize_positions(all_rows)
        planning_data = {
            **planning.planning.model_dump(mode="json"),
            "scope": payload.scope,
            "day_date": target_date.isoformat() if target_date else None,
        }
        routing_defaults = RoutingOptions.model_validate(trip.data.get("routing_defaults") or {})
        route_rows = [
            item for item in all_rows if target_date is None or item.day_date == target_date
        ]
        route_pairs = route_pair_count(route_rows)
        routing_available = route_provider_configured(
            settings,
            trip_region_code(trip.timezone, trip.destination_name, trip.data),
            routing_defaults.default_travel_mode,
        )
        routing_status = (
            "queued"
            if routing_defaults.auto_compute and route_pairs and routing_available
            else "unavailable"
            if routing_defaults.auto_compute and route_pairs
            else "idle"
        )
        trip.data = {
            **trip.data,
            "planning": planning_data,
            "ai_regenerated": True,
            "routing": {
                "status": routing_status,
                "total": route_pairs,
                "completed": 0,
                "warnings": (
                    []
                    if routing_status != "unavailable"
                    else ["路線服務尚未啟用，可先使用手動移動時間。"]
                ),
                "updated_at": datetime.now(UTC).isoformat(),
            },
        }
        trip.version += 1
        if planning.planning.provider == "catalog":
            await release_reservation(session, reservation, "ai_planner_fallback_used")
        else:
            await commit_reservation(session, reservation, trip.id)
        await session.commit()
        await get_redis().delete(f"routes:trip:{trip.id}")
        await session.refresh(trip)
        result = await serialize_trip(session, trip)
        result["usage"] = usage_status(reservation).model_dump()
        if routing_status == "queued":
            try:
                await asyncio.to_thread(
                    enqueue_trip_routing,
                    trip.id,
                    trip.version,
                    target_date,
                )
            except Exception:
                trip.data = {
                    **trip.data,
                    "routing": {
                        "status": "failed",
                        "total": route_pairs,
                        "completed": 0,
                        "warnings": ["背景路線服務暫時無法使用，可在行程頁重新計算。"],
                        "updated_at": datetime.now(UTC).isoformat(),
                    },
                }
                await session.commit()
                result["routing"] = trip.data["routing"]
        return result
    except Exception:
        await session.rollback()
        reservation_row = await session.get(UsageReservation, reservation_id)
        if reservation_row is not None:
            await release_reservation(
                session, reservation_row, "ai_itinerary_generation_failed"
            )
        await session.commit()
        raise


@router.post("/{trip_id}/routes/compute")
async def compute_trip_routes(
    trip_id: UUID,
    payload: RouteComputeRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    if trip.version != payload.version:
        raise AppError(409, "trip_version_conflict", "旅程已被更新，請重新載入後再計算路線")
    rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    if payload.from_item_id and payload.to_item_id:
        selected = [
            item
            for item_id in (payload.from_item_id, payload.to_item_id)
            for item in rows
            if item.id == item_id
        ]
        if len(selected) != 2 or selected[0].day_date != selected[1].day_date:
            raise AppError(422, "route_items_invalid", "起點與終點必須是同一天的行程項目")
        rows = selected
    elif payload.day_date:
        rows = [item for item in rows if item.day_date == payload.day_date]
    rows = active_route_rows(rows)
    if len(rows) < 2:
        raise AppError(422, "route_items_insufficient", "至少需要兩個有位置的行程項目")
    if len(rows) > TRIP_ROUTE_MAX_ITEMS:
        raise AppError(
            422,
            "route_items_limit",
            f"每次最多計算 {TRIP_ROUTE_MAX_ITEMS} 個行程地點，請指定單日或較小範圍",
        )
    preference = payload.route_preference or trip.route_preference
    settings = await load_runtime_settings(session)
    await enforce_named_rate_limit(
        "trip-routes-refresh-user" if payload.refresh else "trip-routes-user",
        str(user.id),
        limit=TRIP_ROUTE_REFRESH_USER_LIMIT if payload.refresh else TRIP_ROUTE_USER_LIMIT,
        window_seconds=TRIP_ROUTE_USER_WINDOW_SECONDS,
    )
    segments, failed = await compute_routes_for_rows(
        trip,
        rows,
        preference,
        settings,
        travel_mode=payload.travel_mode,
        buffer_minutes=payload.buffer_minutes,
        refresh=payload.refresh,
    )
    if not segments:
        if not route_provider_configured(
            settings,
            trip_region_code(trip.timezone, trip.destination_name, trip.data),
            payload.travel_mode,
        ):
            raise AppError(
                503,
                "route_provider_not_configured",
                "此交通方式的路線服務尚未啟用，請先設定對應 Provider",
            )
        raise AppError(503, "route_unavailable", "目前無法取得可用路線，請稍後再試")
    trip.route_preference = preference
    await session.commit()
    await cache_trip_routes(trip.id, segments)
    return {
        "segments": [segment.model_dump(mode="json") for segment in segments],
        "failed_pairs": [
            {"from_item_id": str(origin), "to_item_id": str(destination)}
            for origin, destination in failed
        ],
        "partial": bool(failed),
    }


def _adjacent_route_rows(
    rows: list[TripPlanItem],
    from_item_id: UUID,
    to_item_id: UUID,
) -> tuple[TripPlanItem, TripPlanItem]:
    for first, second in zip(rows, rows[1:], strict=False):
        if first.id == from_item_id and second.id == to_item_id:
            return first, second
    raise AppError(422, "route_items_not_adjacent", "只能計算同一天相鄰行程之間的路線")


def _preview_key(user_id: UUID, trip_id: UUID, preview_id: UUID) -> str:
    return f"routes:preview:{user_id}:{trip_id}:{preview_id}"


def _route_idempotency_key(user_id: UUID, trip_id: UUID, operation: str, key: str) -> str:
    digest = hashlib.sha256(key.encode()).hexdigest()
    return f"routes:idempotency:{operation}:{user_id}:{trip_id}:{digest}"


@router.post("/{trip_id}/locations/resolve")
async def resolve_trip_locations(
    trip_id: UUID,
    payload: TripLocationResolveRequest,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    redis = get_redis()
    idem_key = _route_idempotency_key(user.id, trip_id, "locations", idempotency_key)
    marker = await redis.get(idem_key)
    trip = await owned_trip(session, user.id, trip_id)
    if marker == "complete":
        rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
        unresolved = [
            _unresolved_location(row, "仍需手動確認地點")
            for row in rows
            if (payload.item_ids is None or row.id in set(payload.item_ids))
            and (payload.day_date is None or row.day_date == payload.day_date)
            and (row.latitude is None or row.longitude is None)
        ]
        return {
            "trip": await serialize_trip(session, trip),
            "matched_items": [],
            "unresolved_items": unresolved,
        }
    if not await redis.set(idem_key, "processing", ex=86_400, nx=True):
        raise AppError(409, "location_resolve_in_progress", "相同地點正在配對，請稍候")
    try:
        if trip.version != payload.version:
            raise AppError(409, "trip_version_conflict", "旅程已更新，請重新載入後再配對地點")
        rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
        matched, unresolved = await _resolve_trip_locations(
            session,
            trip,
            rows,
            item_ids=set(payload.item_ids) if payload.item_ids is not None else None,
            day_value=payload.day_date,
        )
        if matched:
            previous = cast(dict[str, Any], trip.data.get("routing") or {})
            next_data = {
                **trip.data,
                "routing": {
                    **previous,
                    "status": "stale",
                    "warnings": ["地點已更新，受影響路段需要重新查詢。"],
                    "updated_at": datetime.now(UTC).isoformat(),
                },
            }
            next_version = await session.scalar(
                update(TripPlan)
                .where(
                    TripPlan.id == trip.id,
                    TripPlan.user_id == user.id,
                    TripPlan.version == payload.version,
                )
                .values(version=TripPlan.version + 1, data=next_data)
                .returning(TripPlan.version)
            )
            if next_version is None:
                await session.rollback()
                raise AppError(
                    409,
                    "trip_version_conflict",
                    "旅程在配對地點期間已更新，請重新載入後再試",
                )
            await session.commit()
            await redis.delete(f"routes:trip:{trip.id}")
            await session.refresh(trip)
        await redis.set(idem_key, "complete", ex=86_400)
        return {
            "trip": await serialize_trip(session, trip),
            "matched_items": matched,
            "unresolved_items": unresolved,
        }
    except Exception:
        await session.rollback()
        await redis.delete(idem_key)
        raise


@router.get("/{trip_id}/routes/status")
async def trip_route_status(
    trip_id: UUID,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    records = await load_route_segments(session, trip.id)
    settings = await load_day_settings(session, trip.id)
    return {"version": trip.version, **routing_summary(trip, settings, records)}


@router.post("/{trip_id}/routes/preview")
async def preview_trip_route(
    trip_id: UUID,
    payload: RoutePreviewRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    if trip.version != payload.version:
        raise AppError(409, "trip_version_conflict", "旅程已更新，請重新載入後再預覽路線")
    rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    first, second = _adjacent_route_rows(
        active_route_rows(rows), payload.from_item_id, payload.to_item_id
    )
    origin, destination = route_point(first), route_point(second)
    if origin is None or destination is None:
        raise AppError(422, "route_location_unavailable", "請先確認這兩個行程地點後再查路")
    await enforce_named_rate_limit(
        "trip-routes-user",
        str(user.id),
        limit=TRIP_ROUTE_USER_LIMIT,
        window_seconds=TRIP_ROUTE_USER_WINDOW_SECONDS,
    )
    setting = await get_or_create_day_setting(
        session,
        trip,
        cast(date, first.day_date),
        update_existing=False,
    )
    preference = payload.route_preference or setting.route_preference
    settings = await load_runtime_settings(session)
    segment = await RouteService(get_redis(), settings).compute(
        origin,
        destination,
        first.end_time or first.start_time,
        preference,
        region_code=trip_region_code(trip.timezone, trip.destination_name, trip.data),
        travel_mode=payload.travel_mode,
    )
    if segment is None:
        region = trip_region_code(trip.timezone, trip.destination_name, trip.data)
        if region == "KR":
            reason = (
                "NAVER 官方 Directions API 不提供可保存的大眾運輸班次；請到 NAVER Maps 查看。"
                if payload.travel_mode == "transit"
                else "目前沒有可套用的站內步行路線；請到 NAVER Maps 查看。"
                if payload.travel_mode == "walk"
                else "目前沒有可套用的汽車路線；請到 NAVER Maps 查看即時導航。"
            )
            external: ExternalNavigation = naver_external_navigation(
                origin,
                destination,
                payload.travel_mode,
                reason=reason,
            )
            await session.rollback()
            return {
                "kind": "external_only",
                "preview_id": None,
                "expires_at": None,
                "segment": None,
                "schedule_impact": None,
                "external_navigation": external.model_dump(mode="json"),
            }
        if not route_provider_configured(settings, region, payload.travel_mode):
            raise AppError(
                503,
                "route_provider_not_configured",
                "此交通方式的路線服務尚未啟用，可先輸入手動移動時間",
            )
        raise AppError(503, "route_unavailable", "目前找不到這個交通方式的可用路線")
    expires_at = datetime.now(UTC) + timedelta(seconds=ROUTE_PREVIEW_TTL_SECONDS)
    segment = segment.model_copy(
        update={
            "buffer_minutes": payload.buffer_minutes,
            "expires_at": expires_at,
            "is_override": payload.travel_mode != setting.default_travel_mode,
        }
    )
    day_rows = active_route_rows(rows, first.day_date)
    persisted = [
        segment_from_record(record)
        for record in await load_route_segments(session, trip.id, day_date=first.day_date)
        if (record.from_item_id, record.to_item_id) != (first.id, second.id)
    ]
    projection = project_day_schedule(day_rows, [*persisted, segment])
    projected = next(
        item
        for item in projection.segments
        if item.from_item_id == first.id and item.to_item_id == second.id
    )
    preview_id = uuid4()
    preview_payload = {
        "user_id": str(user.id),
        "trip_id": str(trip.id),
        "version": trip.version,
        "day_date": cast(date, first.day_date).isoformat(),
        "segment": projected.model_dump(mode="json"),
        "impact": projection.impact.model_dump(mode="json"),
        "expires_at": expires_at.isoformat(),
    }
    await get_redis().set(
        _preview_key(user.id, trip.id, preview_id),
        json.dumps(preview_payload, ensure_ascii=False),
        ex=ROUTE_PREVIEW_TTL_SECONDS,
    )
    await session.rollback()
    return {
        "kind": "provider",
        "preview_id": str(preview_id),
        "expires_at": expires_at,
        "segment": projected.model_dump(mode="json"),
        "schedule_impact": projection.impact.model_dump(mode="json"),
    }


@router.post("/{trip_id}/routes/apply")
async def apply_trip_route(
    trip_id: UUID,
    payload: RouteApplyRequest,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    redis = get_redis()
    idem_key = _route_idempotency_key(user.id, trip_id, "apply", idempotency_key)
    marker = await redis.get(idem_key)
    if marker == "complete":
        return await serialize_trip(session, await owned_trip(session, user.id, trip_id))
    if not await redis.set(idem_key, "processing", ex=86_400, nx=True):
        raise AppError(409, "route_apply_in_progress", "相同路線正在套用，請稍候")
    try:
        trip = await owned_trip(session, user.id, trip_id)
        if trip.version != payload.version:
            raise AppError(409, "trip_version_conflict", "旅程已更新，請重新載入後再套用路線")
        rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
        manual_note: str | None = None
        if payload.source == "provider":
            preview_key = _preview_key(user.id, trip.id, cast(UUID, payload.preview_id))
            raw_preview = await redis.get(preview_key)
            if not raw_preview:
                raise AppError(409, "route_preview_expired", "路線預覽已過期，請重新查詢")
            preview_data = cast(dict[str, Any], json.loads(str(raw_preview)))
            if int(preview_data.get("version") or 0) != trip.version:
                raise AppError(409, "trip_version_conflict", "旅程已更新，請重新預覽路線")
            segment = RouteSegment.model_validate(preview_data["segment"])
        else:
            first_id = cast(UUID, payload.from_item_id)
            second_id = cast(UUID, payload.to_item_id)
            segment = RouteSegment(
                from_item_id=first_id,
                to_item_id=second_id,
                status="manual",
                travel_mode=payload.travel_mode,
                provider="manual",
                attribution="使用者手動輸入",
                generated_at=datetime.now(UTC),
                preference=trip.route_preference,
                duration_minutes=cast(int, payload.duration_minutes),
                buffer_minutes=payload.buffer_minutes,
                details_available=[],
                warnings=["此移動時間由使用者手動輸入，未經地圖服務驗證。"],
            )
            manual_note = payload.note.strip() if payload.note else None
        first, second = _adjacent_route_rows(
            active_route_rows(rows), segment.from_item_id, segment.to_item_id
        )
        day_value = cast(date, first.day_date)
        setting = await get_or_create_day_setting(
            session,
            trip,
            day_value,
            update_existing=False,
        )
        if payload.inherit_day_default and segment.travel_mode != setting.default_travel_mode:
            raise AppError(422, "route_default_mode_mismatch", "請先預覽當日預設交通方式")
        day_records = await load_route_segments(session, trip.id, day_date=day_value)
        current_segments = [
            segment_from_record(record)
            for record in day_records
            if (record.from_item_id, record.to_item_id) != (first.id, second.id)
        ]
        override_pairs = {
            (record.from_item_id, record.to_item_id)
            for record in day_records
            if record.is_override
        }
        pair = (first.id, second.id)
        if payload.inherit_day_default:
            override_pairs.discard(pair)
        else:
            override_pairs.add(pair)
        segment = segment.model_copy(
            update={
                "is_override": pair in override_pairs,
                "buffer_minutes": payload.buffer_minutes
                if payload.source == "manual"
                else segment.buffer_minutes,
            }
        )
        day_rows = active_route_rows(rows, day_value)
        projection = project_day_schedule(day_rows, [*current_segments, segment])
        next_data = {
            **trip.data,
            "routing": {
                "status": "complete",
                "total": max(0, len(day_rows) - 1),
                "completed": len(projection.segments),
                "warnings": [],
                "conflicts": projection.impact.model_dump(mode="json")["conflicts"],
                "updated_at": datetime.now(UTC).isoformat(),
            },
        }
        next_version = await session.scalar(
            update(TripPlan)
            .where(
                TripPlan.id == trip.id,
                TripPlan.user_id == user.id,
                TripPlan.version == payload.version,
            )
            .values(version=TripPlan.version + 1, data=next_data)
            .returning(TripPlan.version)
        )
        if next_version is None:
            await session.rollback()
            raise AppError(409, "trip_version_conflict", "旅程已更新，請重新載入後再套用路線")
        for row in day_rows:
            if row.fixed_time or row.id not in projection.item_times:
                continue
            row.start_time, row.end_time = projection.item_times[row.id]
        await persist_projected_segments(
            session,
            trip.id,
            day_value,
            projection.segments,
            override_pairs=override_pairs,
            manual_notes={pair: manual_note},
            ttl_seconds=get_settings().route_cache_ttl_seconds,
        )
        await session.commit()
        await redis.set(idem_key, "complete", ex=86_400)
        await redis.delete(f"routes:trip:{trip.id}")
        await session.refresh(trip)
        result = await serialize_trip(session, trip)
        result["route_schedule_impact"] = projection.impact.model_dump(mode="json")
        return result
    except Exception:
        await session.rollback()
        await redis.delete(idem_key)
        raise


@router.post("/{trip_id}/routes/compute-day", status_code=202)
async def compute_trip_routes_for_day(
    trip_id: UUID,
    payload: RouteDayComputeRequest,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    redis = get_redis()
    idem_key = _route_idempotency_key(user.id, trip_id, "day", idempotency_key)
    previous = await redis.get(idem_key)
    if previous:
        trip = await owned_trip(session, user.id, trip_id)
        records = await load_route_segments(session, trip.id)
        settings = await load_day_settings(session, trip.id)
        return {"version": trip.version, **routing_summary(trip, settings, records)}
    if not await redis.set(idem_key, "processing", ex=86_400, nx=True):
        raise AppError(409, "route_compute_in_progress", "相同日期的路線正在計算")
    try:
        trip = await owned_trip(session, user.id, trip_id)
        if trip.version != payload.version:
            raise AppError(409, "trip_version_conflict", "旅程已更新，請重新載入後再計算路線")
        rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
        day_rows = active_route_rows(rows, payload.day_date)
        if len(day_rows) < 2:
            raise AppError(422, "route_items_insufficient", "這一天至少需要兩個行程地點")
        _, unresolved = await _resolve_trip_locations(
            session,
            trip,
            rows,
            day_value=payload.day_date,
        )
        routable_pairs = [
            (first, second)
            for first, second in zip(day_rows, day_rows[1:], strict=False)
            if route_point(first) is not None and route_point(second) is not None
        ]
        await enforce_named_rate_limit(
            "trip-routes-refresh-user" if payload.refresh else "trip-routes-user",
            str(user.id),
            limit=TRIP_ROUTE_REFRESH_USER_LIMIT if payload.refresh else TRIP_ROUTE_USER_LIMIT,
            window_seconds=TRIP_ROUTE_USER_WINDOW_SECONDS,
        )
        await get_or_create_day_setting(
            session,
            trip,
            payload.day_date,
            travel_mode=payload.default_travel_mode,
            buffer_minutes=payload.default_buffer_minutes,
            route_preference=payload.route_preference,
        )
        next_version = trip.version + 1
        trip.version = next_version
        trip.route_preference = payload.route_preference
        if not routable_pairs:
            warnings = [
                f"{item['title']}：{item['reason']}" for item in unresolved
            ] or ["這一天沒有可定位的相鄰行程，請先補上地點。"]
            trip.data = {
                **trip.data,
                "routing": {
                    "status": "needs_locations",
                    "total": len(day_rows) - 1,
                    "completed": 0,
                    "warnings": warnings,
                    "unresolved_items": unresolved,
                    "updated_at": datetime.now(UTC).isoformat(),
                },
            }
            await session.commit()
            await redis.delete(f"routes:trip:{trip.id}")
            await redis.set(idem_key, "complete", ex=86_400)
            return {
                "version": next_version,
                "status": "needs_locations",
                "total": len(day_rows) - 1,
                "completed": 0,
                "unresolved_items": unresolved,
            }
        trip.data = {
            **trip.data,
            "routing": {
                "status": "queued",
                "total": len(day_rows) - 1,
                "completed": 0,
                "warnings": [
                    f"{item['title']}：{item['reason']}" for item in unresolved
                ],
                "unresolved_items": unresolved,
                "updated_at": datetime.now(UTC).isoformat(),
            },
        }
        await session.commit()
        try:
            job_id = await asyncio.to_thread(
                enqueue_trip_routing,
                trip.id,
                next_version,
                payload.day_date,
            )
        except Exception as exc:
            trip.data = {
                **trip.data,
                "routing": {
                    "status": "failed",
                    "total": len(day_rows) - 1,
                    "completed": 0,
                    "warnings": ["背景路線服務暫時無法使用，請稍後重試。"],
                    "updated_at": datetime.now(UTC).isoformat(),
                },
            }
            await session.commit()
            raise AppError(503, "route_queue_unavailable", "背景路線服務暫時無法使用") from exc
        await redis.set(idem_key, "complete", ex=86_400)
        return {
            "version": next_version,
            "status": "queued",
            "total": len(day_rows) - 1,
            "completed": 0,
            "job_id": job_id,
            "unresolved_items": unresolved,
        }
    except Exception:
        await redis.delete(idem_key)
        raise


@router.post("/{trip_id}/routes/refresh")
async def refresh_trip_routes(
    trip_id: UUID,
    payload: RouteComputeRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    return await compute_trip_routes(
        trip_id,
        payload.model_copy(update={"refresh": True}),
        user,
        session,
    )


@router.post("/{trip_id}/itinerary/optimize")
async def optimize_trip_itinerary(
    trip_id: UUID,
    payload: RouteComputeRequest,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    reservation, created = await reserve_use(
        session,
        user.id,
        idempotency_key,
        "itinerary_optimization",
        f"行程動線最佳化：{trip.name}",
    )
    if not created and reservation.resource_id == trip.id:
        replay = await serialize_trip(session, trip)
        replay["usage"] = usage_status(reservation).model_dump()
        return replay
    reservation.resource_id = trip.id
    try:
        if trip.version != payload.version:
            raise AppError(409, "trip_version_conflict", "旅程已被更新，請重新載入後再最佳化")
        all_rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
        target_days = (
            [payload.day_date]
            if payload.day_date
            else sorted({row.day_date for row in all_rows if row.day_date is not None})
        )
        changed = False
        any_route = False
        preference = payload.route_preference or trip.route_preference
        settings = await load_runtime_settings(session)
        final_segments: list[RouteSegment] = []
        for target_day in target_days:
            day_rows = active_route_rows(all_rows, target_day)
            movable_slots = [
                index
                for index, row in enumerate(day_rows)
                if not row.locked and not row.fixed_time and route_point(row) is not None
            ]
            if len(movable_slots) < 2:
                continue
            if len(movable_slots) > 12:
                raise AppError(
                    422,
                    "itinerary_optimization_limit",
                    "每天最多最佳化 12 個可移動地點，請先鎖定部分項目",
                )
            movable = [day_rows[index] for index in movable_slots]
            point_by_id = {
                row.id: point for row in movable if (point := route_point(row)) is not None
            }
            pairs = [
                (point_by_id[first.id], point_by_id[second.id], first.end_time or first.start_time)
                for first in movable
                for second in movable
                if first.id != second.id
            ]
            results = await RouteService(get_redis(), settings).compute_many(
                pairs,
                preference,
                region_code=trip_region_code(
                    trip.timezone, trip.destination_name, trip.data
                ),
            )
            costs = {
                (segment.from_item_id, segment.to_item_id): segment.duration_minutes
                for segment in results
                if segment is not None
            }
            if not costs:
                continue
            any_route = True
            remaining = movable.copy()
            ordered = [remaining.pop(0)]
            while remaining:
                previous = ordered[-1]
                next_row = min(
                    remaining,
                    key=lambda row: costs.get((previous.id, row.id), 10**9),
                )
                ordered.append(next_row)
                remaining.remove(next_row)
            if [row.id for row in ordered] != [row.id for row in movable]:
                changed = True
            for slot, row in zip(movable_slots, ordered, strict=True):
                day_rows[slot] = row
            for position, row in enumerate(day_rows):
                row.position = position
            segments, _ = await compute_routes_for_rows(trip, day_rows, preference, settings)
            by_pair = {(segment.from_item_id, segment.to_item_id): segment for segment in segments}
            for previous, following in zip(day_rows, day_rows[1:], strict=False):
                segment = by_pair.get((previous.id, following.id))
                if (
                    segment is None
                    or previous.end_time is None
                    or following.fixed_time
                ):
                    continue
                following.start_time = previous.end_time + timedelta(
                    minutes=segment.duration_minutes + segment.buffer_minutes
                )
                following.end_time = following.start_time + timedelta(
                    minutes=following.duration_minutes or 60
                )
            final_segments.extend(segments)
        if not any_route or not final_segments:
            raise AppError(
                503,
                "itinerary_optimization_unavailable",
                "沒有取得可套用的完整動線結果",
            )
        trip.route_preference = preference
        trip.data = {**trip.data, "route_optimized": True, "route_order_changed": changed}
        trip.version += 1
        await commit_reservation(session, reservation, trip.id)
        await session.commit()
        await cache_trip_routes(trip.id, final_segments)
        await session.refresh(trip)
        result = await serialize_trip(session, trip)
        result["usage"] = usage_status(reservation).model_dump()
        return result
    except Exception:
        await release_reservation(session, reservation, "itinerary_optimization_failed")
        await session.commit()
        raise


@router.delete("/{trip_id}", status_code=204)
async def delete_trip(trip_id: UUID, user: CurrentUser, session: Session) -> None:
    trip = await owned_trip(session, user.id, trip_id)
    await session.delete(trip)
    await session.commit()


@router.post("/{trip_id}/reoptimize")
async def reoptimize_trip(
    trip_id: UUID,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    reservation, created = await reserve_use(
        session,
        user.id,
        idempotency_key,
        "price_reoptimization",
        f"重新最佳化：{trip.name}",
    )
    if not created and reservation.resource_id == trip.id:
        replay = await serialize_trip(session, trip)
        replay["usage"] = usage_status(reservation).model_dump()
        return replay
    reservation.resource_id = trip.id
    existing_items = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    try:
        plan, warnings = await refreshed_plan(session, trip)
    except Exception:
        await release_reservation(session, reservation, "reoptimization_failed")
        await session.commit()
        raise

    await commit_reservation(session, reservation, trip.id)
    checked_at = datetime.now(UTC).isoformat()
    await session.execute(
        delete(TripPlanItem).where(
            TripPlanItem.trip_plan_id == trip.id,
            TripPlanItem.locked.is_(False),
        )
    )
    locked_dates = {item.day_date for item in existing_items if item.locked}
    flight_anchors = {
        item.system_role: item
        for item in existing_items
        if item.system_role in {"outbound_flight", "return_flight"}
    }
    for day in plan.itinerary:
        # User-locked anchors remain byte-for-byte intact. Fresh movable items are
        # rebuilt around them, and provider-generated fixed duplicates are omitted.
        for item in day.items:
            if item.system_role in {"outbound_flight", "return_flight"}:
                current = flight_anchors.get(item.system_role)
                if (
                    current is not None
                    and current.data.get("flight_selection_source") != "manual"
                ):
                    current.item_type = item.item_type
                    current.offer_id = item.offer_id
                    current.title = item.title
                    current.location_name = item.location_name
                    current.start_time = item.start_time
                    current.end_time = item.end_time
                    current.is_estimated = item.is_estimated
                    current.data = item.data
                continue
            if item.locked:
                continue
            row = item_record(trip.id, item, preserve_source_id=False)
            if day.date in locked_dates:
                row.position += 100
            row.data = {**row.data, "reoptimized_at": checked_at}
            session.add(row)
    plan_data = plan.model_dump(mode="json")
    next_lodging = primary_lodging(trip, existing_items)
    if plan.hotel is not None:
        next_lodging = {
            "name": plan.hotel.hotel_name,
            "location_name": plan.hotel.address or plan.hotel.hotel_name,
            "provider_place_id": None,
            "latitude": plan.hotel.latitude,
            "longitude": plan.hotel.longitude,
            "location_source": "provider",
            "offer_id": str(plan.hotel.id),
        }
        sync_primary_lodging(trip, existing_items, next_lodging)
    canonicalize_positions(existing_items)
    trip.mode = plan.mode
    trip.total_price = plan.total_cost.total_cost
    trip.currency = plan.total_cost.currency
    trip.data = {
        **plan_data,
        "primary_lodging": next_lodging,
        "schedule_defaults": schedule_defaults(trip),
        "reoptimized_at": checked_at,
        "prices_checked": True,
        "provider_warnings": warnings,
        "locked_items_preserved": sum(1 for item in existing_items if item.locked),
    }
    trip.version += 1
    await session.commit()
    await session.refresh(trip)
    result = await serialize_trip(session, trip)
    result["usage"] = usage_status(reservation).model_dump()
    return result


@router.post("/{trip_id}/share")
async def create_share(trip_id: UUID, user: CurrentUser, session: Session) -> dict[str, str]:
    trip = await owned_trip(session, user.id, trip_id)
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    share = await session.scalar(select(TripShare).where(TripShare.trip_plan_id == trip.id))
    if share is None:
        share = TripShare(trip_plan_id=trip.id, token_hash=token_hash)
        session.add(share)
    else:
        share.token_hash = token_hash
        share.revoked_at = None
    await session.commit()
    origin = get_settings().next_public_site_url.rstrip("/")
    return {"token": token, "share_url": f"{origin}/share/{token}"}


@router.delete("/{trip_id}/share", status_code=204)
async def revoke_share(trip_id: UUID, user: CurrentUser, session: Session) -> None:
    trip = await owned_trip(session, user.id, trip_id)
    share = await session.scalar(select(TripShare).where(TripShare.trip_plan_id == trip.id))
    if share is not None:
        share.revoked_at = datetime.now(UTC)
        await session.commit()


@public_router.get("/{token}")
async def shared_trip(token: str, session: Session) -> dict[str, Any]:
    if len(token) < 32 or len(token) > 128:
        raise AppError(404, "shared_trip_not_found", "找不到這個分享旅程")
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    share = await session.scalar(
        select(TripShare).where(
            TripShare.token_hash == token_hash,
            TripShare.revoked_at.is_(None),
        )
    )
    if share is None:
        raise AppError(404, "shared_trip_not_found", "找不到這個分享旅程")
    trip = await session.get(TripPlan, share.trip_plan_id)
    if trip is None:
        raise AppError(404, "shared_trip_not_found", "找不到這個分享旅程")
    payload = await serialize_trip(session, trip)
    return {
        key: payload[key]
        for key in (
            "id",
            "name",
            "mode",
            "total_price",
            "currency",
            "data",
            "version",
            "destination_name",
            "destination_place_id",
            "start_date",
            "end_date",
            "timezone",
            "route_preference",
            "items",
            "route_segments",
            "updated_at",
        )
    }
