import asyncio
import hashlib
import json
import secrets
from collections.abc import Mapping
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from typing import Annotated, Any, Literal, cast
from uuid import UUID, uuid4, uuid5
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import httpx
from fastapi import APIRouter, Depends, Header, Query
from pydantic import BaseModel, Field, model_validator
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.ai.itinerary import (
    AIItineraryPlanner,
    AIItineraryRequest,
    AIPlannerCandidate,
    AIPlanningResult,
)
from app.auth.schemas import Currency
from app.auth.service import CurrentUser
from app.config import Settings, get_settings
from app.db import get_session
from app.destinations.catalog import destination_for_code, match_destination
from app.foods.service import load_planner_foods
from app.hotspots.service import load_planner_hotspots
from app.i18n import active_locale
from app.infra import enforce_named_rate_limit, get_redis
from app.localized_names import (
    ITEM_LOCATION_KEY,
    ITEM_TITLE_KEY,
    resolve_item_field,
)
from app.models import (
    SearchRequest,
    TripDayNote,
    TripExpense,
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
from app.trips.expenses import (
    EXPENSE_CATEGORIES,
    MAX_EXPENSES,
    cost_summary,
    seed_rows,
)
from app.trips.itinerary import ItineraryItem
from app.trips.pricing import lodging_from_offer, offer_price_snapshot, trip_pricing
from app.trips.replan import (
    ReplanWrite,
    apply_carried_values,
    apply_meal_writes,
    build_replan_write,
    replaceable_ai_items,
    reuse_rows,
)
from app.trips.reschedule import (
    MAX_SHIFT_DAYS,
    apply_reschedule,
    ensure_shrink_confirmed,
    plan_reschedule,
    reschedule_summary,
    reschedule_trip_data,
    resolve_target_range,
)
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
    google_external_navigation,
    infer_place_provider,
    naver_external_navigation,
    route_provider_configured,
    trip_region_code,
)
from app.trips.schedule import (
    FLIGHT_SYSTEM_ROLES,
    active_route_rows,
    apply_schedule_defaults,
    canonicalize_positions,
    clear_flight_anchor,
    ensure_system_slots,
    merge_reoptimized_lodging,
    primary_lodging,
    route_pair_count,
    schedule_defaults,
    sync_primary_lodging,
)
from app.usage.service import (
    COMMON_LIMITS,
    USAGE_OPERATIONS,
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
    planning_mode: Literal["ai_draft", "manual_blank"] = "ai_draft"
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
    # Home airport for a blank trip, so a later flight search can start from the trip.
    origin_airport: str | None = Field(default=None, min_length=3, max_length=3)

    @model_validator(mode="after")
    def validate_source(self) -> "SaveTripRequest":
        if self.source not in {"search", "blank"}:
            raise ValueError("source must be search or blank")
        if self.origin_airport is not None:
            self.origin_airport = self.origin_airport.strip().upper()
            if not self.origin_airport.isalpha():
                raise ValueError("origin_airport must be an IATA code")
        if self.source == "search" and (self.search_id is None or self.plan_id is None):
            raise ValueError("search_id and plan_id are required for a search trip")
        if self.source == "blank":
            if not self.destination_name or not self.start_date or not self.end_date:
                raise ValueError("destination_name, start_date and end_date are required")
            if self.end_date < self.start_date:
                raise ValueError("end_date must not be before start_date")
            # One day of slack so a client just west of UTC is not rejected.
            if self.start_date < datetime.now(UTC).date() - timedelta(days=1):
                raise ValueError("開始日期不可早於今天")
            if (self.end_date - self.start_date).days > 60:
                raise ValueError("blank trips may be at most 61 days")
        elif self.planning_mode != "ai_draft":
            raise ValueError("manual_blank planning is only available for blank trips")
        if self.route_preference not in {"FEWER_TRANSFERS", "LESS_WALKING", "FASTEST"}:
            raise ValueError("unsupported route preference")
        if self.notes is not None:
            self.notes = self.notes.strip() or None
        return self


class TripMetadataPatchRequest(BaseModel):
    """`PATCH /trips/{id}` — rename a trip, or move its day grid.

    `shift_days` moves the whole trip and keeps its length; `start_date` /
    `end_date` set an absolute range (missing side keeps its current value)
    and leave surviving rows on the calendar days they already occupy. The
    two forms are mutually exclusive. `route_preference` is deliberately NOT
    here: `PUT /trips/{id}/itinerary` already writes it together with the
    all-pairs route invalidation that must accompany it.
    """

    version: int = Field(ge=1)
    name: str | None = Field(default=None, max_length=255)
    status: Literal["planning", "ready", "travelling", "closed"] | None = None
    cover_image_url: str | None = Field(default=None, max_length=1024)
    notes: str | None = Field(default=None, max_length=4000)
    budget_amount: Decimal | None = Field(default=None, ge=0, le=Decimal("99999999999"))
    cost_currency: Currency | None = None
    start_date: date | None = None
    end_date: date | None = None
    shift_days: int | None = Field(default=None, ge=-MAX_SHIFT_DAYS, le=MAX_SHIFT_DAYS)
    confirm_removed_days: bool = False

    @model_validator(mode="after")
    def validate_patch(self) -> "TripMetadataPatchRequest":
        if self.name is not None:
            self.name = self.name.strip()
            if not self.name:
                raise ValueError("name must not be blank")
        if self.cover_image_url is not None:
            self.cover_image_url = self.cover_image_url.strip() or None
        if self.notes is not None:
            # An emptied box clears the note rather than storing whitespace.
            self.notes = self.notes.strip() or None
        if self.cover_image_url is not None and not self.cover_image_url.startswith("https://"):
            raise ValueError("cover_image_url must be an https URL")
        if not self.model_fields_set - {"version", "confirm_removed_days"}:
            raise ValueError("nothing to update")
        return self


def destination_timezone(destination: str) -> str:
    # The catalog carries the authoritative zone for every supported city
    # (仙台, "Tokyo", 台中 …); the keyword rules below only cover free text.
    matched = match_destination(destination)
    if matched is not None:
        return matched.timezone
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
    system_role: (
        Literal[
            "outbound_flight",
            "hotel_start",
            "lunch",
            "dinner",
            "hotel_end",
            "return_flight",
        ]
        | None
    ) = None
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
    day_start_time: str | None = Field(default=None, pattern=r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    lunch_time: str = Field(pattern=r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    lunch_duration_minutes: int = Field(ge=30, le=180)
    dinner_time: str = Field(pattern=r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    dinner_duration_minutes: int = Field(ge=30, le=180)

    @model_validator(mode="after")
    def validate_order(self) -> "ScheduleDefaultsUpdateRequest":
        if self.lunch_time >= self.dinner_time:
            raise ValueError("lunch_time must be before dinner_time")
        if self.day_start_time is not None and self.day_start_time >= self.lunch_time:
            raise ValueError("day_start_time must be before lunch_time")
        return self


class MealSkipRequest(BaseModel):
    version: int = Field(ge=1)
    skipped: bool


class FlightAnchorDetails(BaseModel):
    airline: str = Field(min_length=1, max_length=120)
    flight_number: str = Field(min_length=1, max_length=32)
    origin: str = Field(min_length=1, max_length=16)
    destination: str = Field(min_length=1, max_length=16)
    departure_local: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}T(?:[01]\d|2[0-3]):[0-5]\d$")
    arrival_local: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}T(?:[01]\d|2[0-3]):[0-5]\d$")
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


class ItineraryApplyRequest(BaseModel):
    version: int = Field(ge=1)
    preview_id: UUID


AI_ITINERARY_PREVIEW_TTL_SECONDS = 15 * 60
# AI-drafted creation can outlive the browser's patience; a retry within a day
# must return the trip that was already created, not a duplicate.
TRIP_CREATE_REPLAY_TTL_SECONDS = 24 * 60 * 60

# The two prices an itinerary write can carry. They live here, next to the
# charge point, so the rule that decides between them cannot drift away from
# the code that applies it — see ``apply_usage_operation``.
GENERATE_OPERATION = "ai_itinerary_generation"
REFINE_OPERATION = "ai_itinerary_refine"


class OptimizationApplyRequest(BaseModel):
    version: int = Field(ge=1)
    preview_id: UUID


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
    include_alternatives: bool = False
    max_options: int = Field(default=3, ge=1, le=3)

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
            self.from_item_id is None or self.to_item_id is None or self.duration_minutes is None
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
        # Only planner output carries per-locale labels; client rows are free text.
        names_json=dict(getattr(item, "names", None) or {}),
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


def apply_item_request(
    record: TripPlanItem, item: ItineraryItemRequest, *, locale: str | None = None
) -> None:
    # The client echoes the label it was shown (the stored text or its
    # translation for the request locale); the stored text then stays as it
    # is, so a catalog stop keeps one canonical title however often it is
    # saved from other languages. Anything else is a rename by the traveller,
    # and the catalog's per-locale labels no longer describe the row.
    shown_in = locale or active_locale()
    names = dict(record.names_json or {})
    title: str | None = item.title
    location_name = item.location_name
    for field, incoming in (
        (ITEM_TITLE_KEY, item.title),
        (ITEM_LOCATION_KEY, item.location_name),
    ):
        if field not in names:
            continue
        stored = cast(str | None, getattr(record, field))
        localized = resolve_item_field(names, field, shown_in, fallback=stored)
        if (incoming or "") in {stored or "", localized or ""}:
            if field == ITEM_TITLE_KEY:
                title = stored
            else:
                location_name = stored
        else:
            names.pop(field)
    record.names_json = names
    record.item_type = item.item_type
    record.offer_id = item.offer_id
    record.day_date = item.day_date
    record.position = item.position
    record.title = title
    record.location_name = location_name
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


def serialize_item(
    item: TripPlanItem, *, locale: str | None = None, localized: bool = True
) -> dict[str, Any]:
    """Serialize one row, labelling catalog-backed stops in the request locale.

    ``names`` always carries every stored label (five site locales plus the
    original script) so a client can show the original text next to the title.
    ``localized=False`` returns the stored text, for server-side round trips.
    """

    names = item.names_json or {}
    title = item.title
    location_name = item.location_name
    if localized:
        shown_in = locale or active_locale()
        title = resolve_item_field(names, ITEM_TITLE_KEY, shown_in, fallback=item.title)
        location_name = resolve_item_field(
            names, ITEM_LOCATION_KEY, shown_in, fallback=item.location_name
        )
    return {
        "id": str(item.id),
        "item_type": item.item_type,
        "offer_id": str(item.offer_id) if item.offer_id else None,
        "day_date": item.day_date,
        "position": item.position,
        "title": title or item.item_type,
        "location_name": location_name,
        "names": names,
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


# What GET /shared-trips/{token} hands to whoever holds the link. serialize_item is
# also the owner's round trip back into the editor (ItineraryItemRequest is built from
# it), so it has to keep notes and the whole data blob; the share link is read-only
# sightseeing and gets an allowlist instead. Anything the owner typed for themselves
# (notes), paid (price_snapshot, offer_id) or that names how the row was produced
# (reason, provider, source) stays out.
PUBLIC_TRIP_KEYS = (
    "id",
    "name",
    "destination_name",
    "start_date",
    "end_date",
    "timezone",
    "route_segments",
    "updated_at",
)
PUBLIC_ITEM_KEYS = (
    "id",
    "item_type",
    "day_date",
    "position",
    "title",
    "location_name",
    "names",
    "start_time",
    "end_time",
    "latitude",
    "longitude",
    "locked",
    "is_estimated",
    "duration_minutes",
    "fixed_time",
    "system_role",
    "is_skipped",
)
# The two data keys the shared timeline reads: which section a row is drawn in, and
# the flight card. The flight card itself only gets the schedule, not the quote.
PUBLIC_FLIGHT_INFO_KEYS = (
    "airline",
    "flight_number",
    "origin",
    "destination",
    "departure_local",
    "arrival_local",
    "departure_timezone",
    "arrival_timezone",
)


def public_item(item: Mapping[str, Any]) -> dict[str, Any]:
    """Trim one serialized row down to what a share-link recipient may see."""
    data = item.get("data") or {}
    public_data: dict[str, Any] = {}
    if "timeline_section" in data:
        public_data["timeline_section"] = data["timeline_section"]
    flight_info = data.get("flight_info")
    if isinstance(flight_info, Mapping):
        public_data["flight_info"] = {
            key: flight_info[key] for key in PUBLIC_FLIGHT_INFO_KEYS if key in flight_info
        }
    return {**{key: item[key] for key in PUBLIC_ITEM_KEYS}, "data": public_data}


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


async def load_day_notes(session: AsyncSession, trip_id: UUID) -> list[TripDayNote]:
    return list(
        (
            await session.scalars(
                select(TripDayNote)
                .where(TripDayNote.trip_plan_id == trip_id)
                .order_by(TripDayNote.day_date)
            )
        ).all()
    )


async def load_expenses(session: AsyncSession, trip_id: UUID) -> list[TripExpense]:
    return list(
        (
            await session.scalars(
                select(TripExpense)
                .where(TripExpense.trip_plan_id == trip_id)
                .order_by(TripExpense.day_date, TripExpense.position)
            )
        ).all()
    )


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
    day_notes: dict[str, str] = {}
    cost: dict[str, Any] | None = None
    # Gated with the items: list_trips() serialises every trip a member owns,
    # and an ungated ledger query there would be a 2xN fan-out.
    if include_items:
        day_notes = {
            row.day_date.isoformat(): row.notes
            for row in await load_day_notes(session, trip.id)
        }
        cost = cost_summary(trip, await load_expenses(session, trip.id))
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
        "status": trip.status,
        "cover_image_url": trip.cover_image_url,
        "mode": trip.mode,
        "total_price": trip.total_price,
        "currency": trip.currency,
        "data": trip.data,
        "primary_lodging": (
            primary_lodging(trip, items) if include_items else trip.data.get("primary_lodging")
        ),
        "pricing": trip_pricing(trip, items) if include_items else None,
        "optimization": optimization_summary(items) if include_items else None,
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
        "notes": trip.notes,
        "day_notes": day_notes,
        "cost": cost,
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
        routing_defaults = RoutingOptions.model_validate(trip.data.get("routing_defaults") or {})
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
    if flight is None:
        clear_flight_anchor(item, role)
        return
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
    item.is_estimated = False
    # A hand-typed flight is not the flight that was quoted: the snapshot goes with the offer.
    item.data = {key: value for key, value in item.data.items() if key != "price_snapshot"}
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
    candidates: list[AIPlannerCandidate] | None = None,
    first_day_available_from: str = "14:00",
    last_day_available_until: str = "16:00",
    trip_start_date: date | None = None,
    trip_end_date: date | None = None,
) -> AIItineraryRequest:
    return AIItineraryRequest(
        destination_name=destination_name,
        start_date=start_date,
        end_date=end_date,
        trip_start_date=trip_start_date or start_date,
        trip_end_date=trip_end_date or end_date,
        timezone=timezone,
        route_preference=route_preference,
        travelers=travelers,
        preferences=preferences,
        notes=notes,
        candidates=candidates or [],
        first_day_available_from=first_day_available_from,
        last_day_available_until=last_day_available_until,
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


def _planner_availability(
    items: list[TripPlanItem],
    *,
    trip_start: date,
    trip_end: date,
    target_date: date | None,
) -> dict[str, str | bool]:
    first_day = target_date or trip_start
    last_day = target_date or trip_end
    first_from = "14:00" if first_day == trip_start else "09:00"
    last_until = "16:00" if last_day == trip_end else "21:30"
    used_outbound = False
    used_return = False

    for item in items:
        info = item.data.get("flight_info")
        if not isinstance(info, dict):
            continue
        if item.system_role == "outbound_flight" and first_day == trip_start:
            value = info.get("arrival_local")
            if isinstance(value, str):
                try:
                    arrival = datetime.fromisoformat(value)
                except ValueError:
                    pass
                else:
                    if arrival.date() == trip_start:
                        available = min(
                            arrival + timedelta(minutes=120),
                            datetime.combine(trip_start, time(23, 59)),
                        )
                        first_from = available.strftime("%H:%M")
                        used_outbound = True
        if item.system_role == "return_flight" and last_day == trip_end:
            value = info.get("departure_local")
            if isinstance(value, str):
                try:
                    departure = datetime.fromisoformat(value)
                except ValueError:
                    pass
                else:
                    if departure.date() == trip_end:
                        available = max(
                            departure - timedelta(minutes=180),
                            datetime.combine(trip_end, time(0, 0)),
                        )
                        last_until = available.strftime("%H:%M")
                        used_return = True
    return {
        "first_day_available_from": first_from,
        "last_day_available_until": last_until,
        "used_outbound_flight": used_outbound,
        "used_return_flight": used_return,
    }


async def _load_ai_planner_candidates(
    session: AsyncSession,
    destination_name: str,
    preferences: SearchPreferences,
    *,
    start_date: date,
    end_date: date,
    locale: str = "zh-TW",
) -> list[AIPlannerCandidate]:
    destination = match_destination(destination_name)
    if destination is None:
        return []
    day_count = max(1, (end_date - start_date).days + 1)
    hotspots, foods = await asyncio.gather(
        load_planner_hotspots(
            session,
            destination_id=destination.id,
            interests=preferences.interests,
            limit=40,
            extension_destination_ids=preferences.extension_destination_ids,
            days=day_count,
            style="all",
        ),
        load_planner_foods(
            session,
            destination_id=destination.id,
            locale=locale,
            days=day_count,
            limit=20,
        ),
    )
    deep_requested = "deep_travel" in preferences.interests
    requested_extensions = set(preferences.extension_destination_ids)
    eligible_hotspots = [
        hotspot
        for hotspot in hotspots
        if (deep_requested or hotspot.depth_kind != "day_trip")
        and (not hotspot.is_cross_city or hotspot.destination_id in requested_extensions)
    ]
    candidates = [
        AIPlannerCandidate(
            key=f"hotspot:{hotspot.hotspot_id}",
            kind="hotspot",
            name=hotspot.name,
            names=hotspot.names,
            category=hotspot.category,
            latitude=hotspot.latitude,
            longitude=hotspot.longitude,
            duration_minutes=hotspot.recommended_duration_minutes,
            map_links=hotspot.map_links,
            hotspot_id=hotspot.hotspot_id,
            depth_kind=("day_trip" if hotspot.depth_kind == "day_trip" else "urban_local"),
            access_minutes=hotspot.access_minutes,
            is_cross_city=hotspot.is_cross_city,
            rank=rank,
        )
        for rank, hotspot in enumerate(eligible_hotspots, 1)
    ]
    seen_merchants: set[UUID] = set()
    for rank, food in enumerate(foods, 1):
        if (
            food.merchant_status != "verified"
            or food.merchant_id is None
            or food.merchant_name is None
            or food.latitude is None
            or food.longitude is None
            or not food.map_links
            or food.merchant_id in seen_merchants
        ):
            continue
        meal_types = [meal for meal in food.meal_types if meal in {"lunch", "dinner"}]
        if not meal_types:
            continue
        seen_merchants.add(food.merchant_id)
        candidates.append(
            AIPlannerCandidate(
                key=f"merchant:{food.merchant_id}",
                kind="merchant",
                name=food.merchant_name,
                local_name=food.local_name or food.name,
                names=food.merchant_names,
                dish_names=food.names,
                category="food",
                latitude=food.latitude,
                longitude=food.longitude,
                duration_minutes=75,
                map_links=food.map_links,
                food_id=food.food_id,
                merchant_id=food.merchant_id,
                meal_types=meal_types,
                rank=rank,
            )
        )
    return candidates


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
        # The provider label replaces the catalog one, in the provider's language.
        item.names = {key: value for key, value in item.names.items() if key != ITEM_LOCATION_KEY}
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
            _unresolved_location(item, "旅程目的地的地點搜尋服務尚未設定") for item in candidates
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
        if not place or place_latitude is None or place_longitude is None:
            unresolved.append(_unresolved_location(item, "找不到位於旅程目的地的可靠候選"))
            continue
        provider = str(place.get("provider") or "google_places")
        item.location_name = str(place.get("name") or place.get("address") or label)
        item.names_json = {
            key: value for key, value in (item.names_json or {}).items() if key != ITEM_LOCATION_KEY
        }
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


def search_dates_diverged(
    trip_start: date | None,
    trip_end: date | None,
    departure_date: date | None,
    return_date: date | None,
) -> bool:
    """True when a trip's dates no longer match the search it was built from.

    A reprice rebuilds the whole itinerary from the ORIGINAL SearchRequest
    dates, so running it after `PATCH /trips/{id}` moved the trip would
    re-insert every row at the old dates — outside the new range, which
    permanently 422s the itinerary save. The SearchRequest may be shared by
    several trips, so it cannot simply be rewritten to match.
    """
    return (
        trip_start is not None and departure_date is not None and trip_start != departure_date
    ) or (trip_end is not None and return_date is not None and trip_end != return_date)


async def refreshed_plan(session: AsyncSession, trip: TripPlan) -> tuple[TripPlanResult, list[str]]:
    search = await session.get(SearchRequest, trip.search_id)
    if search is None:
        raise AppError(409, "trip_search_missing", "原始搜尋已無法使用")
    query = SearchCreate.model_validate(search.request_json)
    if search_dates_diverged(
        trip.start_date, trip.end_date, query.departure_date, query.return_date
    ):
        raise AppError(
            409,
            "trip_search_dates_diverged",
            "旅程日期已與原始搜尋不同，無法用舊搜尋重新查價；請重新搜尋後另存旅程",
        )
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
    payload: SaveTripRequest,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[
        str | None, Header(alias="Idempotency-Key", min_length=8, max_length=255)
    ] = None,
) -> dict[str, Any]:
    redis = get_redis()
    request_key = _trip_create_request_key(user.id, idempotency_key) if idempotency_key else None
    if request_key:
        replay_id = await redis.get(request_key)
        if replay_id:
            existing = await session.scalar(
                select(TripPlan).where(
                    TripPlan.id == UUID(str(replay_id)), TripPlan.user_id == user.id
                )
            )
            if existing is not None:
                return await serialize_trip(session, existing)
    count = await session.scalar(
        select(func.count()).select_from(TripPlan).where(TripPlan.user_id == user.id)
    )
    if int(count or 0) >= await limit_for(session, user.id, "saved_trips"):
        raise AppError(403, "trip_limit_reached", "已達所有會員共用的 20 筆儲存旅程上限")
    if payload.source == "blank":
        destination = payload.destination_name or "未命名目的地"
        timezone = payload.timezone or destination_timezone(destination)
        preferences = payload.preferences.model_dump(mode="json")
        planning: AIPlanningResult | None = None
        settings: Settings | None = None
        routing_options = payload.routing
        if payload.planning_mode == "manual_blank":
            routing_options = payload.routing.model_copy(update={"auto_compute": False})
        else:
            settings = await load_runtime_settings(session)
            candidates = await _load_ai_planner_candidates(
                session,
                destination,
                payload.preferences,
                start_date=cast(date, payload.start_date),
                end_date=cast(date, payload.end_date),
            )
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
                    candidates=candidates,
                )
            )
        # Only exact adjacent locations enter routing; unset hotel anchors are excluded.
        route_pairs = (
            sum(max(0, len(day.items) - 1) for day in planning.itinerary) if planning else 0
        )
        routing_available = False
        if planning is not None and settings is not None:
            routing_available = route_provider_configured(
                settings,
                trip_region_code(timezone, destination, {}),
                routing_options.default_travel_mode,
            )
        routing_status = (
            "queued"
            if routing_options.auto_compute and route_pairs and routing_available
            else "unavailable"
            if routing_options.auto_compute and route_pairs
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
                "creation_mode": payload.planning_mode,
                "destination_city": destination,
                "destination_country": {
                    "Asia/Tokyo": "日本",
                    "Asia/Seoul": "韓國",
                    "Asia/Bangkok": "泰國",
                }.get(timezone),
                "travelers": payload.travelers.model_dump(mode="json"),
                "preferences": preferences,
                "origin_airport": payload.origin_airport,
                "notes": payload.notes,
                "planning": (
                    {
                        **planning.planning.model_dump(mode="json"),
                        "unscheduled_slots": planning.unscheduled_slots,
                    }
                    if planning
                    else None
                ),
                "routing_defaults": routing_options.model_dump(mode="json"),
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
        if planning is not None:
            for day in planning.itinerary:
                for item in day.items:
                    session.add(item_record(trip.id, item, preserve_source_id=False))
        else:
            ensure_system_slots(session, trip, [])
        await session.commit()
        await session.refresh(trip)
        if request_key:
            await redis.set(request_key, str(trip.id), ex=TRIP_CREATE_REPLAY_TTL_SECONDS)
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
    # A trip saved from a search keeps the plan verbatim, plus the keys a blank trip
    # has: who travels, what they prefer and where they fly from. That is what lets a
    # later price search start from the trip instead of the home page. The quotes the
    # plan was built on survive as snapshots, because the offers themselves expire.
    request_json: dict[str, Any] = search.request_json or {}
    flight_offer = plan.get("flight") if isinstance(plan.get("flight"), dict) else None
    hotel_offer = plan.get("hotel") if isinstance(plan.get("hotel"), dict) else None
    flight_snapshot = offer_price_snapshot(flight_offer)
    lodging = (
        lodging_from_offer(hotel_offer, selection_source="search") if hotel_offer else None
    )
    shared_keys: dict[str, Any] = {
        "source": "search",
        "origin_airport": request_json.get("origin"),
        "destination_code": request_json.get("destination"),
        "destination_country": first_item_data.get("destination_country"),
        "travelers": request_json.get("travelers") or Travelers().model_dump(mode="json"),
        "preferences": (
            request_json.get("preferences") or SearchPreferences().model_dump(mode="json")
        ),
        "search_criteria": {
            key: request_json.get(key)
            for key in (
                "trip_type",
                "departure_date",
                "return_date",
                "cabin_class",
                "flexible_dates",
                "flex_days",
            )
        },
    }
    if lodging is not None:
        shared_keys["primary_lodging"] = lodging
    trip = TripPlan(
        user_id=user.id,
        search_id=search.id,
        name=payload.name,
        mode=plan["mode"],
        total_price=Decimal(str(plan["total_cost"]["total_cost"])),
        data={**plan, **shared_keys},
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
    quoted_flight_id = str(flight_offer.get("id")) if flight_offer else None
    for raw_day in itinerary_days:
        for raw_item in raw_day.get("items", []):
            record = item_record(
                trip.id,
                ItineraryItem.model_validate(raw_item),
                preserve_source_id=False,
            )
            if (
                flight_snapshot is not None
                and record.system_role in FLIGHT_SYSTEM_ROLES
                and record.offer_id is not None
                and str(record.offer_id) == quoted_flight_id
            ):
                record.data = {**record.data, "price_snapshot": flight_snapshot}
            session.add(record)
    await session.commit()
    await session.refresh(trip)
    if request_key:
        await redis.set(request_key, str(trip.id), ex=TRIP_CREATE_REPLAY_TTL_SECONDS)
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


@router.get("/options")
async def trip_options(user: CurrentUser, session: Session) -> dict[str, object]:
    """Compact, shared trip picker used by cards across the public app.

    Carries the saved-trip cap alongside the items so a picker can say "已建立 18／20"
    before the member runs into the 403, and counts the trips it had to leave out
    because they have no dates yet.
    """
    trips = list(
        (
            await session.scalars(
                select(TripPlan)
                .where(TripPlan.user_id == user.id)
                .order_by(TripPlan.updated_at.desc())
            )
        ).all()
    )
    limit = await limit_for(session, user.id, "saved_trips")
    dated = [trip for trip in trips if trip.start_date is not None and trip.end_date is not None]
    return {
        "items": [
            {
                "trip_id": str(trip.id),
                "name": trip.name,
                "version": trip.version,
                "start_date": trip.start_date,
                "end_date": trip.end_date,
                "destination_name": trip.destination_name,
            }
            for trip in dated
        ],
        "count": len(trips),
        "limit": limit,
        "can_create": len(trips) < limit,
        "undated_count": len(trips) - len(dated),
    }


@router.get("/{trip_id}")
async def get_trip(trip_id: UUID, user: CurrentUser, session: Session) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    return await serialize_trip(session, trip)


class TripExpenseRequest(BaseModel):
    """One ledger line. Currency lives on the trip, never on the row."""

    version: int = Field(ge=1)
    day_date: date
    label: str = Field(min_length=1, max_length=120)
    amount: Decimal = Field(ge=0, le=Decimal("99999999999"))
    category: Literal[EXPENSE_CATEGORIES] = "other"  # type: ignore[valid-type]

    @model_validator(mode="after")
    def clean(self) -> "TripExpenseRequest":
        self.label = self.label.strip()
        if not self.label:
            raise ValueError("label must not be blank")
        return self


class TripExpensePatchRequest(BaseModel):
    version: int = Field(ge=1)
    day_date: date | None = None
    label: str | None = Field(default=None, min_length=1, max_length=120)
    amount: Decimal | None = Field(default=None, ge=0, le=Decimal("99999999999"))
    category: Literal[EXPENSE_CATEGORIES] | None = None  # type: ignore[valid-type]

    @model_validator(mode="after")
    def clean(self) -> "TripExpensePatchRequest":
        if self.label is not None:
            self.label = self.label.strip()
            if not self.label:
                raise ValueError("label must not be blank")
        if not self.model_fields_set - {"version"}:
            raise ValueError("nothing to update")
        return self


class TripExpenseSeedRequest(BaseModel):
    version: int = Field(ge=1)


async def _bump_trip_version(
    session: AsyncSession, trip: TripPlan, user_id: UUID, expected: int
) -> None:
    """Win the trip's compare-and-swap, or refuse to touch the ledger."""
    next_version = await session.scalar(
        update(TripPlan)
        .where(
            TripPlan.id == trip.id,
            TripPlan.user_id == user_id,
            TripPlan.version == expected,
        )
        .values(version=TripPlan.version + 1)
        .returning(TripPlan.version)
    )
    if next_version is None:
        await session.rollback()
        raise AppError(409, "trip_version_conflict", "旅程已被更新，請重新載入後再操作")


def _check_expense_day(trip: TripPlan, day_date: date) -> None:
    if trip.start_date and trip.end_date and not (trip.start_date <= day_date <= trip.end_date):
        raise AppError(422, "day_outside_trip", "這一天不在旅程日期範圍內")


@router.post("/{trip_id}/expenses", status_code=201)
async def create_trip_expense(
    trip_id: UUID,
    payload: TripExpenseRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    _check_expense_day(trip, payload.day_date)
    existing = await load_expenses(session, trip.id)
    if len(existing) >= MAX_EXPENSES:
        raise AppError(422, "trip_ledger_full", f"每趟旅程最多 {MAX_EXPENSES} 筆帳目")
    await _bump_trip_version(session, trip, user.id, payload.version)
    position = max(
        (row.position for row in existing if row.day_date == payload.day_date),
        default=-1,
    )
    session.add(
        TripExpense(
            trip_plan_id=trip.id,
            day_date=payload.day_date,
            label=payload.label,
            amount=payload.amount,
            category=payload.category,
            source="manual",
            position=position + 1,
        )
    )
    await session.commit()
    await session.refresh(trip)
    return await serialize_trip(session, trip)


@router.patch("/{trip_id}/expenses/{expense_id}")
async def update_trip_expense(
    trip_id: UUID,
    expense_id: UUID,
    payload: TripExpensePatchRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    row = await session.scalar(
        select(TripExpense).where(
            TripExpense.id == expense_id, TripExpense.trip_plan_id == trip.id
        )
    )
    if row is None:
        raise AppError(404, "expense_not_found", "找不到這筆帳目")
    if payload.day_date is not None:
        _check_expense_day(trip, payload.day_date)
    await _bump_trip_version(session, trip, user.id, payload.version)
    if payload.day_date is not None:
        row.day_date = payload.day_date
    if payload.label is not None:
        row.label = payload.label
    if payload.amount is not None:
        row.amount = payload.amount
    if payload.category is not None:
        row.category = payload.category
    await session.commit()
    await session.refresh(trip)
    return await serialize_trip(session, trip)


@router.delete("/{trip_id}/expenses/{expense_id}")
async def delete_trip_expense(
    trip_id: UUID,
    expense_id: UUID,
    user: CurrentUser,
    session: Session,
    # DELETE bodies are not universally supported, so the version rides the
    # query string while still being mandatory.
    version: Annotated[int, Query(ge=1)],
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    row = await session.scalar(
        select(TripExpense).where(
            TripExpense.id == expense_id, TripExpense.trip_plan_id == trip.id
        )
    )
    if row is None:
        raise AppError(404, "expense_not_found", "找不到這筆帳目")
    await _bump_trip_version(session, trip, user.id, version)
    await session.delete(row)
    await session.commit()
    await session.refresh(trip)
    return await serialize_trip(session, trip)


@router.post("/{trip_id}/expenses/seed")
async def seed_trip_expenses(
    trip_id: UUID,
    payload: TripExpenseSeedRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    """Fill the ledger from prices this trip already knows.

    Idempotent by construction: every seeded row carries a `source_key`, and a
    key already present is skipped, so pressing the button twice adds nothing.
    """
    trip = await owned_trip(session, user.id, trip_id)
    existing = await load_expenses(session, trip.id)
    seeds = seed_rows(
        trip,
        existing_keys={row.source_key for row in existing if row.source_key},
        day=trip.start_date or date.today(),
    )
    if len(existing) + len(seeds) > MAX_EXPENSES:
        raise AppError(422, "trip_ledger_full", f"每趟旅程最多 {MAX_EXPENSES} 筆帳目")
    await _bump_trip_version(session, trip, user.id, payload.version)
    day_positions: dict[date, int] = {}
    for row in existing:
        day_positions[row.day_date] = max(day_positions.get(row.day_date, -1), row.position)
    for seed in seeds:
        day = cast(date, seed["day_date"])
        position = day_positions.get(day, -1) + 1
        day_positions[day] = position
        session.add(
            TripExpense(
                trip_plan_id=trip.id,
                day_date=day,
                label=cast(str, seed["label"]),
                amount=cast(Decimal, seed["amount"]),
                category=cast(str, seed["category"]),
                source="seeded",
                source_key=cast(str, seed["source_key"]),
                position=position,
            )
        )
    await session.commit()
    await session.refresh(trip)
    return await serialize_trip(session, trip)


class TripDayNoteRequest(BaseModel):
    """`PUT /trips/{id}/days/{day}/notes` — the note for one day.

    An empty body deletes the row: a day with nothing written on it should not
    keep an empty string around to serialise back.
    """

    version: int = Field(ge=1)
    notes: str | None = Field(default=None, max_length=4000)


@router.put("/{trip_id}/days/{day_date}/notes")
async def set_trip_day_note(
    trip_id: UUID,
    day_date: date,
    payload: TripDayNoteRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    if trip.start_date and trip.end_date and not (trip.start_date <= day_date <= trip.end_date):
        raise AppError(422, "day_outside_trip", "這一天不在旅程日期範圍內")
    text = (payload.notes or "").strip()
    # Win the compare-and-swap before writing, exactly like every other
    # mutating trip endpoint, so two tabs cannot both think they saved.
    next_version = await session.scalar(
        update(TripPlan)
        .where(
            TripPlan.id == trip.id,
            TripPlan.user_id == user.id,
            TripPlan.version == payload.version,
        )
        .values(version=TripPlan.version + 1)
        .returning(TripPlan.version)
    )
    if next_version is None:
        await session.rollback()
        raise AppError(409, "trip_version_conflict", "旅程已被更新，請重新載入後再操作")
    existing = await session.scalar(
        select(TripDayNote).where(
            TripDayNote.trip_plan_id == trip.id, TripDayNote.day_date == day_date
        )
    )
    if not text:
        if existing is not None:
            await session.delete(existing)
    elif existing is None:
        session.add(TripDayNote(trip_plan_id=trip.id, day_date=day_date, notes=text))
    else:
        existing.notes = text
    await session.commit()
    await session.refresh(trip)
    return await serialize_trip(session, trip)


@router.patch("/{trip_id}")
async def update_trip_metadata(
    trip_id: UUID,
    payload: TripMetadataPatchRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    """Rename a trip, change its lifecycle status, or move its day grid.

    A metadata-only change touches nothing but the trip row. A date change
    runs as one transaction that wins the version compare-and-swap first,
    then moves every day-keyed row two-phase (items and per-day route
    settings), re-homes the two flight anchors, clears bookings whose
    calendar day changed, deletes everything a shrink drops (after
    `confirm_removed_days`), drops every route segment plus the Redis route
    cache, and rebuilds the date-stamped blobs in `trip.data`. The version
    bump is also what makes any in-flight routing job or planning preview
    discard itself instead of writing rows against the old dates.
    """
    trip = await owned_trip(session, user.id, trip_id)
    target = resolve_target_range(
        old_start=trip.start_date,
        old_end=trip.end_date,
        shift_days=payload.shift_days,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )
    scalar_values: dict[str, Any] = {}
    if payload.name is not None:
        scalar_values["name"] = payload.name
    if payload.status is not None:
        scalar_values["status"] = payload.status
    if "cover_image_url" in payload.model_fields_set:
        scalar_values["cover_image_url"] = payload.cover_image_url
    if "notes" in payload.model_fields_set:
        scalar_values["notes"] = payload.notes
    if "budget_amount" in payload.model_fields_set:
        scalar_values["budget_amount"] = payload.budget_amount
    if payload.cost_currency is not None and payload.cost_currency != trip.cost_currency:
        # Every row is denominated in this currency and there is no converter
        # that could restate them, so the switch is only offered while the
        # ledger is empty. Refusing beats silently relabelling real numbers.
        booked = await session.scalar(
            select(func.count())
            .select_from(TripExpense)
            .where(TripExpense.trip_plan_id == trip.id)
        )
        if booked:
            raise AppError(
                422,
                "trip_ledger_not_empty",
                "帳目已有紀錄，無法更改幣別。請先清空帳目再切換。",
            )
        scalar_values["cost_currency"] = payload.cost_currency

    if target is None and not scalar_values:
        # The requested dates are the ones the trip already has. Report the
        # current state instead of bumping the version, which would only 409
        # other tabs — but still refuse to answer against a stale version.
        if trip.version != payload.version:
            raise AppError(409, "trip_version_conflict", "旅程已被更新，請重新載入後再操作")
        return await serialize_trip(session, trip)

    if target is None:
        next_version = await session.scalar(
            update(TripPlan)
            .where(
                TripPlan.id == trip.id,
                TripPlan.user_id == user.id,
                TripPlan.version == payload.version,
            )
            .values(version=TripPlan.version + 1, **scalar_values)
            .returning(TripPlan.version)
        )
        if next_version is None:
            await session.rollback()
            raise AppError(409, "trip_version_conflict", "旅程已被更新，請重新載入後再操作")
        await session.commit()
        await session.refresh(trip)
        return await serialize_trip(session, trip)

    items = await load_items(session, trip.id)
    day_settings = await load_day_settings(session, trip.id)
    segments = await load_route_segments(session, trip.id)
    plan = plan_reschedule(
        old_start=trip.start_date,
        old_end=trip.end_date,
        target=target,
        items=items,
        day_settings=day_settings,
    )
    ensure_shrink_confirmed(plan, confirmed=payload.confirm_removed_days)
    # The CAS runs before any ORM attribute is written, so a lost race leaves
    # nothing to roll back beyond the statement itself.
    next_version = await session.scalar(
        update(TripPlan)
        .where(
            TripPlan.id == trip.id,
            TripPlan.user_id == user.id,
            TripPlan.version == payload.version,
        )
        .values(version=TripPlan.version + 1, **scalar_values)
        .returning(TripPlan.version)
    )
    if next_version is None:
        await session.rollback()
        raise AppError(409, "trip_version_conflict", "旅程已被更新，請重新載入後再操作")
    segments_cleared = len(segments)
    rows = await apply_reschedule(
        session,
        trip,
        items=items,
        day_settings=day_settings,
        segments=segments,
        plan=plan,
    )
    trip.data = reschedule_trip_data(trip.data, rows)
    await session.commit()
    # After the deletes above, an empty segment table is exactly the state in
    # which serialize_trip falls back to this cache — clear it or the API
    # serves the pre-move routes back as if nothing changed.
    await get_redis().delete(f"routes:trip:{trip.id}")
    await session.refresh(trip)
    response = await serialize_trip(session, trip)
    response["reschedule"] = reschedule_summary(plan, segments_cleared=segments_cleared)
    return response


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
        ItineraryItemRequest.model_validate(serialize_item(row, localized=False))
        for row in existing_rows
        if row.system_role is not None and row.id not in incoming_ids
    )
    for item in incoming_items:
        existing = existing_by_id.get(item.id) if item.id is not None else None
        if item.system_role is not None and (existing is None or existing.system_role is None):
            # Neither a new row nor a promoted ordinary row: a client-minted system slot
            # would dodge the immutability rules below and collide with the per-day
            # unique constraint on system roles.
            raise AppError(
                422,
                "system_itinerary_item_immutable",
                "固定航班、飯店與餐食卡只能由系統建立",
            )
        if (
            existing is not None
            and existing.system_role is not None
            and (item.system_role != existing.system_role or item.day_date != existing.day_date)
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
                (first.id, second.id) for first, second in zip(day_rows, day_rows[1:], strict=False)
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
        routing_defaults = RoutingOptions.model_validate(trip.data.get("routing_defaults") or {})
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
        "selection_source": "user",
        "selected_at": datetime.now(UTC).isoformat(),
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
            **payload.model_dump(exclude={"version"}, exclude_none=True),
        },
    }
    apply_schedule_defaults(trip, rows)
    return await persist_system_schedule_change(
        session,
        trip,
        user.id,
        payload.version,
        rows,
        warning="每日時間已更新，請重新計算受影響的移動時間。",
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


def _itinerary_preview_key(user_id: UUID, trip_id: UUID, preview_id: UUID) -> str:
    return f"itinerary:preview:{user_id}:{trip_id}:{preview_id}"


def _itinerary_preview_request_key(user_id: UUID, trip_id: UUID, idempotency_key: str) -> str:
    digest = hashlib.sha256(idempotency_key.encode()).hexdigest()
    return f"itinerary:preview-request:{user_id}:{trip_id}:{digest}"


def _trip_create_request_key(user_id: UUID, idempotency_key: str) -> str:
    digest = hashlib.sha256(idempotency_key.encode()).hexdigest()
    return f"trip:create-request:{user_id}:{digest}"


def _candidate_signatures(
    candidates: list[AIPlannerCandidate], selected_keys: set[str]
) -> dict[str, str]:
    return {
        candidate.key: hashlib.sha256(
            json.dumps(
                candidate.model_dump(mode="json"),
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode()
        ).hexdigest()
        for candidate in candidates
        if candidate.key in selected_keys
    }


def _planning_preserved_items(
    preserved: list[TripPlanItem], target_date: date | None
) -> list[TripPlanItem]:
    return [
        item
        for item in preserved
        if (target_date is None or item.day_date == target_date)
        and item.system_role not in {"outbound_flight", "return_flight"}
        and (
            item.system_role not in {"lunch", "dinner"}
            or item.data.get("meal_selection_source") == "user"
        )
    ]


def _replan_records(trip_id: UUID, plan: ReplanWrite) -> list[TripPlanItem]:
    """The rows a re-plan inserts, with the traveller's own edits carried over.

    Apply rebuilds the replaceable rows from the draft. A stop the planner
    proposes again is the same stop, so a note, a stay length, a rename or a
    hand-picked place written on it survives the rebuild; the planner's own
    reason and catalog coordinates are refreshed.

    Reused pairs are not here. A row nothing would change keeps its id instead
    — ``replan.reuse_rows`` refreshes it in place — because a new id cascades
    the traveller's route segments away.
    """
    records: list[TripPlanItem] = []
    for pair in plan.pairs:
        if pair.planned is None or pair.reused:
            continue
        record = item_record(trip_id, pair.planned, preserve_source_id=False)
        apply_carried_values(record, pair.carried)
        records.append(record)
    return records


def _compose_planner_notes(trip_notes: str | None, extra_notes: str | None) -> str | None:
    parts = [part.strip() for part in (trip_notes, extra_notes) if part and part.strip()]
    return "\n".join(parts) or None


async def _build_ai_planning(
    session: AsyncSession,
    trip: TripPlan,
    payload: ItineraryGenerateRequest,
    *,
    extra_notes: str | None = None,
) -> tuple[AIPlanningResult, list[TripPlanItem], list[TripPlanItem], list[AIPlannerCandidate]]:
    """Load candidates and run the planner for a trip or a single day.

    ``extra_notes`` is appended to the trip's own note as additional traveller
    preference text. It reaches the provider only through the user-content
    payload's ``notes`` field, never the system prompt, and is never written
    back to ``trip.data``.
    """
    if not trip.destination_name or not trip.start_date or not trip.end_date:
        raise AppError(422, "trip_planning_fields_missing", "旅程缺少目的地或日期，無法重新排行程")
    target_date = payload.day_date if payload.scope == "day" else None
    if target_date and not (trip.start_date <= target_date <= trip.end_date):
        raise AppError(422, "itinerary_date_out_of_range", "AI 單日安排的日期超出旅程範圍")
    if trip.version != payload.version:
        raise AppError(409, "trip_version_conflict", "旅程已被更新，請重新載入後再讓 AI 重排")
    # Hydrated, exactly as apply loads them: a legacy trip whose rows still
    # live in trip.data, or a day whose meal slots have never been
    # materialised, would otherwise plan against a set apply does not see.
    existing = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    _, preserved = replaceable_ai_items(existing, target_date)
    planning_preserved = _planning_preserved_items(preserved, target_date)
    availability = _planner_availability(
        preserved,
        trip_start=trip.start_date,
        trip_end=trip.end_date,
        target_date=target_date,
    )
    travelers = Travelers.model_validate(trip.data.get("travelers", {}))
    preferences = SearchPreferences.model_validate(trip.data.get("preferences", {}))
    candidates = await _load_ai_planner_candidates(
        session,
        trip.destination_name or "",
        preferences,
        start_date=target_date or trip.start_date,
        end_date=target_date or trip.end_date,
        locale=str(trip.data.get("locale") or "zh-TW"),
    )
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
            notes=_compose_planner_notes(
                trip.notes or cast(str | None, trip.data.get("notes")), extra_notes
            ),
            preserved_items=planning_preserved,
            candidates=candidates,
            first_day_available_from=cast(str, availability["first_day_available_from"]),
            last_day_available_until=cast(str, availability["last_day_available_until"]),
            trip_start_date=trip.start_date,
            trip_end_date=trip.end_date,
        )
    )
    return planning, preserved, planning_preserved, candidates


@router.post("/{trip_id}/itinerary/preview")
async def preview_trip_itinerary(
    trip_id: UUID,
    payload: ItineraryGenerateRequest,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    redis = get_redis()
    request_key = _itinerary_preview_request_key(user.id, trip_id, idempotency_key)
    replay_id = await redis.get(request_key)
    if replay_id:
        cached = await redis.get(_itinerary_preview_key(user.id, trip_id, UUID(str(replay_id))))
        if cached:
            return cast(dict[str, Any], json.loads(str(cached)))
    await enforce_named_rate_limit(
        "ai-itinerary-preview-user",
        str(user.id),
        limit=12,
        window_seconds=3_600,
    )
    trip = await owned_trip(session, user.id, trip_id)
    planning, preserved, planning_preserved, candidates = await _build_ai_planning(
        session, trip, payload
    )
    result, cached_payload = await build_itinerary_preview_envelope(
        session,
        trip,
        payload,
        planning=planning,
        preserved=preserved,
        planning_preserved=planning_preserved,
        candidates=candidates,
    )
    await redis.set(
        _itinerary_preview_key(user.id, trip.id, UUID(str(result["preview_id"]))),
        json.dumps(cached_payload, ensure_ascii=False),
        ex=AI_ITINERARY_PREVIEW_TTL_SECONDS,
    )
    await redis.set(
        request_key,
        str(result["preview_id"]),
        ex=AI_ITINERARY_PREVIEW_TTL_SECONDS,
    )
    return result


async def build_itinerary_preview_envelope(
    session: AsyncSession,
    trip: TripPlan,
    payload: ItineraryGenerateRequest,
    *,
    planning: AIPlanningResult,
    preserved: list[TripPlanItem],
    planning_preserved: list[TripPlanItem],
    candidates: list[AIPlannerCandidate],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build the (client result, Redis payload) pair that ``/itinerary/apply`` consumes.

    Every producer of a plan writes this exact envelope so there is a single
    apply path. The returned Redis payload adds ``candidate_keys`` and
    ``candidate_signatures``, which apply re-derives from the database and
    compares before it writes anything.
    """
    preview_id = uuid4()
    expires_at = datetime.now(UTC) + timedelta(seconds=AI_ITINERARY_PREVIEW_TTL_SECONDS)
    has_lodging = primary_lodging(trip, await load_items(session, trip.id)) is not None
    candidate_keys = {candidate.key for candidate in candidates}
    selected_keys = {
        str(item.data.get("candidate_key"))
        for day in planning.itinerary
        for item in day.items
        if item.data.get("candidate_key")
    }
    if not selected_keys.issubset(candidate_keys):
        raise AppError(422, "itinerary_candidate_invalid", "AI 回傳了不存在的正式地點")
    assumptions = []
    if not has_lodging:
        assumptions.append("尚未設定飯店；本次只依景點區域分組，不建立飯店往返路線。")
    target_date = payload.day_date if payload.scope == "day" else None
    availability = _planner_availability(
        preserved,
        trip_start=cast(date, trip.start_date),
        trip_end=cast(date, trip.end_date),
        target_date=target_date,
    )
    if not availability["used_outbound_flight"] and (
        target_date is None or target_date == trip.start_date
    ):
        assumptions.append("未設定抵達時間；首日採 14:00 後的保守時段。")
    if not availability["used_return_flight"] and (
        target_date is None or target_date == trip.end_date
    ):
        assumptions.append("未設定離開時間；末日採 16:00 前的保守時段。")
    exact_items = sum(len(day.items) for day in planning.itinerary)
    preview_days: list[dict[str, Any]] = []
    for day in planning.itinerary:
        day_payload = day.model_dump(mode="json")
        anchor = next(
            (
                item
                for item in day.items
                if item.system_role not in {"lunch", "dinner"} and item.location_name
            ),
            None,
        )
        day_payload["label"] = f"{anchor.location_name}周邊" if anchor else "當日相近區域"
        preview_days.append(day_payload)
    result: dict[str, Any] = {
        "preview_id": str(preview_id),
        "base_version": trip.version,
        "expires_at": expires_at.isoformat(),
        "scope": payload.scope,
        "day_date": payload.day_date.isoformat() if payload.day_date else None,
        "planning": planning.planning.model_dump(mode="json"),
        "days": preview_days,
        "unscheduled_slots": planning.unscheduled_slots,
        "readiness": {
            "status": planning.planning.readiness,
            "has_lodging": has_lodging,
            "exact_item_count": exact_items,
            "hotspot_candidate_count": sum(candidate.kind == "hotspot" for candidate in candidates),
            "merchant_candidate_count": sum(
                candidate.kind == "merchant" for candidate in candidates
            ),
            "preserved_item_count": len(planning_preserved),
            "assumptions": assumptions,
            "first_day_available_from": availability["first_day_available_from"],
            "last_day_available_until": availability["last_day_available_until"],
            "uses_flight_times": bool(
                availability["used_outbound_flight"] or availability["used_return_flight"]
            ),
        },
        "routing_summary": {
            "exact_items": exact_items,
            "eligible_pairs": sum(max(0, len(day.items) - 1) for day in planning.itinerary),
            "hotel_pairs_deferred": 0 if has_lodging else len(planning.itinerary) * 2,
        },
    }
    cached_payload = {
        **result,
        "candidate_keys": sorted(selected_keys),
        "candidate_signatures": _candidate_signatures(candidates, selected_keys),
    }
    return result, cached_payload


@router.post("/{trip_id}/itinerary/generate", deprecated=True)
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
        _, preserved = replaceable_ai_items(existing, target_date)
        planning_preserved = _planning_preserved_items(preserved, target_date)
        availability = _planner_availability(
            preserved,
            trip_start=trip.start_date,
            trip_end=trip.end_date,
            target_date=target_date,
        )
        travelers = Travelers.model_validate(trip.data.get("travelers", {}))
        preferences = SearchPreferences.model_validate(trip.data.get("preferences", {}))
        settings = await load_runtime_settings(session)
        candidates = await _load_ai_planner_candidates(
            session,
            trip.destination_name or "",
            preferences,
            start_date=target_date or trip.start_date,
            end_date=target_date or trip.end_date,
            locale=str(trip.data.get("locale") or "zh-TW"),
        )
        planning = await AIItineraryPlanner(settings).generate(
            _planning_request(
                destination_name=trip.destination_name,
                start_date=target_date or trip.start_date,
                end_date=target_date or trip.end_date,
                timezone=trip.timezone or "UTC",
                route_preference=trip.route_preference,
                travelers=travelers,
                preferences=preferences,
                notes=trip.notes or cast(str | None, trip.data.get("notes")),
                preserved_items=planning_preserved,
                candidates=candidates,
                first_day_available_from=cast(str, availability["first_day_available_from"]),
                last_day_available_until=cast(str, availability["last_day_available_until"]),
                trip_start_date=trip.start_date,
                trip_end_date=trip.end_date,
            )
        )
        if planning.planning.readiness == "needs_setup":
            raise AppError(
                422,
                "itinerary_exact_locations_required",
                "正式景點或店家不足，原行程保持不變",
            )
        plan = build_replan_write(
            existing, planning.itinerary, target_date, timezone=trip.timezone
        )
        apply_meal_writes(plan.meals)
        # Only the rows that really change are rebuilt; the rest keep their ids
        # so the route segments hanging off them survive — see replan.reuse_rows.
        kept_rows = reuse_rows(plan.pairs)
        deleted_ids = {item.id for item in plan.deleted}
        if deleted_ids:
            await session.execute(
                delete(TripPlanItem).where(
                    TripPlanItem.trip_plan_id == trip.id,
                    TripPlanItem.id.in_(deleted_ids),
                )
            )
        generated_records = _replan_records(trip.id, plan)
        for record in generated_records:
            session.add(record)
        all_rows = [*plan.preserved, *kept_rows, *generated_records]
        canonicalize_positions(all_rows)
        planning_data = {
            **planning.planning.model_dump(mode="json"),
            "scope": payload.scope,
            "day_date": target_date.isoformat() if target_date else None,
            "unscheduled_slots": planning.unscheduled_slots,
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
            await release_reservation(session, reservation_row, "ai_itinerary_generation_failed")
        await session.commit()
        raise


def apply_usage_operation(preview: dict[str, Any], *, refinable: bool) -> str:
    """Which metered operation this write charges.

    A producer names its own operation so a refinement can price separately
    from a first generation, but the envelope only *proposes* the free price —
    the two conditions that make it a refinement are checked here, against the
    write apply is about to perform:

    * the envelope is scoped to one day, not the whole trip;
    * that day already holds an AI plan to nudge (``refinable``).

    Either one missing and this is a generation by another name — a stale
    envelope from a pod mid-rollout, or a day being planned from scratch
    through the free door. Anything unrecognised, including every envelope
    written before this key existed, charges the original operation, which
    keeps apply's behaviour unchanged by default.
    """
    operation = str(preview.get("usage_operation") or GENERATE_OPERATION)
    if operation not in USAGE_OPERATIONS:
        return GENERATE_OPERATION
    if operation != REFINE_OPERATION:
        return operation
    if not refinable or str(preview.get("scope") or "trip") != "day":
        return GENERATE_OPERATION
    return REFINE_OPERATION


@router.post("/{trip_id}/itinerary/apply")
async def apply_trip_itinerary_preview(
    trip_id: UUID,
    payload: ItineraryApplyRequest,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    redis = get_redis()
    replay_key = _route_idempotency_key(user.id, trip_id, "itinerary-apply", idempotency_key)
    replay_usage = await redis.get(replay_key)
    if replay_usage:
        replay_trip = await serialize_trip(session, await owned_trip(session, user.id, trip_id))
        replay_trip["usage"] = json.loads(str(replay_usage))
        return replay_trip
    preview_key = _itinerary_preview_key(user.id, trip_id, payload.preview_id)
    raw_preview = await redis.get(preview_key)
    if not raw_preview:
        raise AppError(409, "itinerary_preview_expired", "行程預覽已過期，請重新產生")
    preview = cast(dict[str, Any], json.loads(str(raw_preview)))
    trip = await owned_trip(session, user.id, trip_id)
    if trip.version != payload.version or int(preview.get("base_version") or 0) != trip.version:
        raise AppError(409, "trip_version_conflict", "旅程已更新，請重新預覽後再套用")
    scope = cast(Literal["day", "trip"], preview.get("scope") or "trip")
    day_date_value = preview.get("day_date")
    target_date = date.fromisoformat(str(day_date_value)) if day_date_value else None
    generation_payload = ItineraryGenerateRequest(
        version=payload.version,
        scope=scope,
        day_date=target_date,
    )
    preferences = SearchPreferences.model_validate(trip.data.get("preferences", {}))
    candidates = await _load_ai_planner_candidates(
        session,
        trip.destination_name or "",
        preferences,
        start_date=target_date or cast(date, trip.start_date),
        end_date=target_date or cast(date, trip.end_date),
        locale=str(trip.data.get("locale") or "zh-TW"),
    )
    selected_keys = set(preview.get("candidate_keys") or [])
    expected_signatures = preview.get("candidate_signatures") or {}
    if _candidate_signatures(candidates, selected_keys) != expected_signatures:
        raise AppError(409, "itinerary_candidates_changed", "部分景點或店家已變更，請重新預覽")
    planning = AIPlanningResult.model_validate(
        {
            "itinerary": preview.get("days") or [],
            "planning": preview.get("planning") or {},
            "unscheduled_slots": preview.get("unscheduled_slots") or [],
        }
    )
    if planning.planning.readiness == "needs_setup":
        raise AppError(
            422,
            "itinerary_exact_locations_required",
            "正式景點或店家不足，暫時無法套用",
        )
    scope_label = target_date.isoformat() if target_date else "全行程"
    existing = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    # One projection of the write, shared with the diff the traveller approved
    # on the intent path — see app/trips/replan.py. Built before the charge so
    # the price is read off what apply will really do, not off what the
    # envelope claims it is.
    plan = build_replan_write(existing, planning.itinerary, target_date, timezone=trip.timezone)
    reservation, created = await reserve_use(
        session,
        user.id,
        idempotency_key,
        apply_usage_operation(preview, refinable=bool(plan.replaceable)),
        f"AI 重新排行程：{trip.name}（{scope_label}）",
    )
    if not created and reservation.resource_id == trip.id:
        replay = await serialize_trip(session, trip)
        replay["usage"] = usage_status(reservation).model_dump()
        return replay
    reservation.resource_id = trip.id
    reservation_id = reservation.id
    try:
        apply_meal_writes(plan.meals)
        kept_rows = reuse_rows(plan.pairs)
        deleted_ids = {item.id for item in plan.deleted}
        if deleted_ids:
            await session.execute(
                delete(TripPlanItem).where(
                    TripPlanItem.trip_plan_id == trip.id,
                    TripPlanItem.id.in_(deleted_ids),
                )
            )
        generated_records = _replan_records(trip.id, plan)
        session.add_all(generated_records)
        all_rows = [*plan.preserved, *kept_rows, *generated_records]
        canonicalize_positions(all_rows)
        settings = await load_runtime_settings(session)
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
            "planning": {
                **planning.planning.model_dump(mode="json"),
                "scope": generation_payload.scope,
                "day_date": target_date.isoformat() if target_date else None,
                "unscheduled_slots": planning.unscheduled_slots,
            },
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
        await redis.delete(f"routes:trip:{trip.id}", preview_key)
        await session.refresh(trip)
        result = await serialize_trip(session, trip)
        result["usage"] = usage_status(reservation).model_dump()
        await redis.set(
            replay_key,
            json.dumps(result["usage"], ensure_ascii=False),
            ex=86_400,
        )
        if routing_status == "queued":
            try:
                await asyncio.to_thread(enqueue_trip_routing, trip.id, trip.version, target_date)
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
            await release_reservation(session, reservation_row, "ai_itinerary_apply_failed")
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
    region = trip_region_code(trip.timezone, trip.destination_name, trip.data)
    option_limit = payload.max_options if payload.include_alternatives else 1
    route_departure_time = first.end_time or first.start_time
    if route_departure_time is not None:
        try:
            trip_timezone = ZoneInfo(trip.timezone or "UTC")
        except ZoneInfoNotFoundError:
            trip_timezone = ZoneInfo("UTC")
        route_departure_time = (
            route_departure_time.replace(tzinfo=trip_timezone)
            if route_departure_time.tzinfo is None
            else route_departure_time.astimezone(trip_timezone)
        )
    segments = await RouteService(get_redis(), settings).compute_options(
        origin,
        destination,
        route_departure_time,
        preference,
        region_code=region,
        travel_mode=payload.travel_mode,
        max_options=option_limit,
    )
    if not segments:
        if region == "KR":
            reason = (
                "ODsay 目前沒有回傳可套用的大眾運輸路線；請到 NAVER Maps 查看。"
                if payload.travel_mode == "transit" and settings.odsay_configured
                else "韓國站內大眾運輸需先設定 ODsay Server Key；請到 NAVER Maps 查看。"
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
                "options": [],
                "origin": origin.model_dump(mode="json"),
                "destination": destination.model_dump(mode="json"),
                "external_navigation": external.model_dump(mode="json"),
            }
        if region == "JP" and payload.travel_mode == "transit":
            japanese_provider = (
                "Ekispert"
                if settings.ekispert_configured
                else "NAVITIME"
                if settings.navitime_configured
                else None
            )
            reason = (
                f"{japanese_provider} 目前沒有回傳可套用的路線；Google Maps Platform 的 Routes API "
                "不提供日本大眾運輸資料，可先到 Google Maps 查看即時路線。"
                if japanese_provider
                else "Google Maps Platform 的 Routes API 不提供日本大眾運輸資料；"
                "站內路線需先設定 Ekispert（或 NAVITIME 備援），可先到 Google Maps 查看即時路線。"
            )
            external = google_external_navigation(
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
                "options": [],
                "origin": origin.model_dump(mode="json"),
                "destination": destination.model_dump(mode="json"),
                "external_navigation": external.model_dump(mode="json"),
            }
        if not route_provider_configured(settings, region, payload.travel_mode):
            raise AppError(
                503,
                "route_provider_not_configured",
                "此交通方式的路線服務尚未啟用，可先輸入手動移動時間",
            )
        external = google_external_navigation(
            origin,
            destination,
            payload.travel_mode,
            reason=(
                "目前無法取得可套用的站內大眾運輸班次；已保留精準起訖點，"
                "可先到 Google Maps 查看，並在接近旅程時重新查詢。"
                if payload.travel_mode == "transit"
                else "目前無法取得可套用的站內路線；已保留精準起訖點，可先到 Google Maps 查看。"
            ),
        )
        await session.rollback()
        return {
            "kind": "external_only",
            "preview_id": None,
            "expires_at": None,
            "segment": None,
            "schedule_impact": None,
            "options": [],
            "origin": origin.model_dump(mode="json"),
            "destination": destination.model_dump(mode="json"),
            "external_navigation": external.model_dump(mode="json"),
        }
    expires_at = datetime.now(UTC) + timedelta(seconds=ROUTE_PREVIEW_TTL_SECONDS)
    day_rows = active_route_rows(rows, first.day_date)
    persisted = [
        segment_from_record(record)
        for record in await load_route_segments(session, trip.id, day_date=first.day_date)
        if (record.from_item_id, record.to_item_id) != (first.id, second.id)
    ]
    redis = get_redis()
    options: list[dict[str, Any]] = []
    for index, raw_segment in enumerate(segments[:option_limit]):
        ranked_segment = raw_segment.model_copy(
            update={
                "buffer_minutes": payload.buffer_minutes,
                "expires_at": expires_at,
                "is_override": payload.travel_mode != setting.default_travel_mode,
                "route_option_rank": index + 1,
            }
        )
        projection = project_day_schedule(day_rows, [*persisted, ranked_segment])
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
        await redis.set(
            _preview_key(user.id, trip.id, preview_id),
            json.dumps(preview_payload, ensure_ascii=False),
            ex=ROUTE_PREVIEW_TTL_SECONDS,
        )
        options.append(
            {
                "preview_id": str(preview_id),
                "provider_route_key": projected.provider_route_key,
                "rank": index + 1,
                "expires_at": expires_at,
                "segment": projected.model_dump(mode="json"),
                "schedule_impact": projection.impact.model_dump(mode="json"),
            }
        )
    recommended = options[0]
    await session.rollback()
    return {
        "kind": "provider",
        "preview_id": recommended["preview_id"],
        "expires_at": recommended["expires_at"],
        "segment": recommended["segment"],
        "schedule_impact": recommended["schedule_impact"],
        "options": options,
        "origin": origin.model_dump(mode="json"),
        "destination": destination.model_dump(mode="json"),
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
            (record.from_item_id, record.to_item_id) for record in day_records if record.is_override
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
            warnings = [f"{item['title']}：{item['reason']}" for item in unresolved] or [
                "這一天沒有可定位的相鄰行程，請先補上地點。"
            ]
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
                "warnings": [f"{item['title']}：{item['reason']}" for item in unresolved],
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


OPTIMIZATION_PREVIEW_TTL_SECONDS = 15 * 60
OPTIMIZATION_MOVABLE_LIMIT = 12


def movable_slots(day_rows: list[TripPlanItem]) -> list[int]:
    """Indexes of the rows the optimiser may reorder: unlocked, not fixed, and located."""
    return [
        index
        for index, row in enumerate(day_rows)
        if not row.locked and not row.fixed_time and route_point(row) is not None
    ]


def optimization_summary(rows: list[TripPlanItem]) -> dict[str, Any]:
    """Per-day movable counts against the limit, so the planner can warn before a 422."""
    days = sorted({row.day_date for row in rows if row.day_date is not None})
    return {
        "movable_limit": OPTIMIZATION_MOVABLE_LIMIT,
        "days": [
            {
                "date": day_value.isoformat(),
                "movable_count": len(movable_slots(active_route_rows(rows, day_value))),
            }
            for day_value in days
        ],
    }


def _optimization_preview_key(user_id: UUID, trip_id: UUID, preview_id: UUID) -> str:
    return f"itinerary:optimize-preview:{user_id}:{trip_id}:{preview_id}"


def _optimization_request_key(user_id: UUID, trip_id: UUID, idempotency_key: str) -> str:
    digest = hashlib.sha256(idempotency_key.encode()).hexdigest()
    return f"itinerary:optimize-request:{user_id}:{trip_id}:{digest}"


def _chain_minutes(rows: list[TripPlanItem], costs: dict[tuple[UUID, UUID], int]) -> int:
    return sum(
        costs.get((first.id, second.id), 0) for first, second in zip(rows, rows[1:], strict=False)
    )


def _nearest_neighbour(
    movable: list[TripPlanItem], costs: dict[tuple[UUID, UUID], int]
) -> list[TripPlanItem]:
    remaining = movable.copy()
    ordered = [remaining.pop(0)]
    while remaining:
        previous = ordered[-1]
        following = min(remaining, key=lambda row: costs.get((previous.id, row.id), 10**9))
        ordered.append(following)
        remaining.remove(following)
    return ordered


def _preview_item(item: TripPlanItem, position: int) -> dict[str, Any]:
    return {
        "id": str(item.id),
        "title": item.title or "",
        "position": position,
        "start_time": item.start_time.isoformat() if item.start_time else None,
        "locked": bool(item.locked),
        "fixed_time": bool(item.fixed_time),
    }


async def plan_itinerary_optimization(
    trip: TripPlan,
    all_rows: list[TripPlanItem],
    target_days: list[date],
    preference: str,
    settings: Settings,
) -> dict[str, Any]:
    """Work out a better order for each day without touching a single row.

    Preview and apply both go through here so they can never disagree about what
    "optimised" means. Rows are only ever read; the reordering is expressed as a list
    of item ids per day, which apply replays.
    """

    days: list[dict[str, Any]] = []
    warnings: list[str] = []
    segments: list[RouteSegment] = []
    changed = False
    for target_day in target_days:
        day_rows = active_route_rows(all_rows, target_day)
        movable_indexes = movable_slots(day_rows)
        if len(movable_indexes) < 2:
            continue
        if len(movable_indexes) > OPTIMIZATION_MOVABLE_LIMIT:
            raise AppError(
                422,
                "itinerary_optimization_limit",
                f"每天最多最佳化 {OPTIMIZATION_MOVABLE_LIMIT} 個可移動地點，請先鎖定部分項目",
            )
        movable = [day_rows[index] for index in movable_indexes]
        point_by_id = {row.id: point for row in movable if (point := route_point(row)) is not None}
        pairs = [
            (point_by_id[first.id], point_by_id[second.id], first.end_time or first.start_time)
            for first in movable
            for second in movable
            if first.id != second.id
        ]
        results = await RouteService(get_redis(), settings).compute_many(
            pairs,
            preference,
            region_code=trip_region_code(trip.timezone, trip.destination_name, trip.data),
        )
        costs = {
            (segment.from_item_id, segment.to_item_id): segment.duration_minutes
            for segment in results
            if segment is not None
        }
        if not costs:
            warnings.append(f"{target_day.isoformat()} 沒有取得可比較的移動時間，這天維持原樣。")
            continue
        ordered = _nearest_neighbour(movable, costs)
        day_changed = [row.id for row in ordered] != [row.id for row in movable]
        changed = changed or day_changed
        reordered = list(day_rows)
        for slot, row in zip(movable_indexes, ordered, strict=True):
            reordered[slot] = row
        day_segments, _ = await compute_routes_for_rows(trip, reordered, preference, settings)
        segments.extend(day_segments)
        before_minutes = _chain_minutes(movable, costs)
        after_minutes = _chain_minutes(ordered, costs)
        days.append(
            {
                "date": target_day.isoformat(),
                "order": [str(row.id) for row in reordered],
                "before": [_preview_item(row, index) for index, row in enumerate(day_rows)],
                "after": [_preview_item(row, index) for index, row in enumerate(reordered)],
                "duration_before_minutes": before_minutes,
                "duration_after_minutes": after_minutes,
                "saved_minutes": max(0, before_minutes - after_minutes),
            }
        )
    return {
        "changed": changed,
        "warnings": warnings,
        "days": days,
        "segments": segments,
        "route_preference": preference,
        "total_duration_before_minutes": sum(day["duration_before_minutes"] for day in days),
        "total_duration_after_minutes": sum(day["duration_after_minutes"] for day in days),
    }


@router.post("/{trip_id}/itinerary/optimize/preview")
async def preview_trip_itinerary_optimization(
    trip_id: UUID,
    payload: RouteComputeRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    """Show the reordering before anything is charged or written."""

    trip = await owned_trip(session, user.id, trip_id)
    if trip.version != payload.version:
        raise AppError(409, "trip_version_conflict", "旅程已被更新，請重新載入後再最佳化")
    all_rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    target_days = (
        [payload.day_date]
        if payload.day_date
        else sorted({row.day_date for row in all_rows if row.day_date is not None})
    )
    settings = await load_runtime_settings(session)
    plan = await plan_itinerary_optimization(
        trip,
        all_rows,
        target_days,
        payload.route_preference or trip.route_preference,
        settings,
    )
    if not plan["days"]:
        raise AppError(
            503,
            "itinerary_optimization_unavailable",
            "沒有取得可比較的動線結果",
        )
    preview_id = uuid4()
    expires_at = datetime.now(UTC) + timedelta(seconds=OPTIMIZATION_PREVIEW_TTL_SECONDS)
    result = {
        "preview_id": str(preview_id),
        "expires_at": expires_at.isoformat(),
        "base_version": trip.version,
        "charge_on_apply": 1,
        **plan,
        "segments": [segment.model_dump(mode="json") for segment in plan["segments"]],
    }
    await get_redis().set(
        _optimization_preview_key(user.id, trip.id, preview_id),
        json.dumps(result, ensure_ascii=False),
        ex=OPTIMIZATION_PREVIEW_TTL_SECONDS,
    )
    # The preview only read rows; make sure nothing it touched can be flushed later.
    await session.rollback()
    return result


@router.post("/{trip_id}/itinerary/optimize/apply")
async def apply_trip_itinerary_optimization(
    trip_id: UUID,
    payload: OptimizationApplyRequest,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    """Replay a preview. The routes were already computed, so this costs no provider calls."""

    redis = get_redis()
    replay_key = _route_idempotency_key(user.id, trip_id, "optimize-apply", idempotency_key)
    replay_usage = await redis.get(replay_key)
    if replay_usage:
        replay_trip = await serialize_trip(session, await owned_trip(session, user.id, trip_id))
        replay_trip["usage"] = json.loads(str(replay_usage))
        return replay_trip
    preview_key = _optimization_preview_key(user.id, trip_id, payload.preview_id)
    raw_preview = await redis.get(preview_key)
    if not raw_preview:
        raise AppError(409, "itinerary_preview_expired", "最佳化預覽已過期，請重新預覽")
    preview = cast(dict[str, Any], json.loads(str(raw_preview)))
    trip = await owned_trip(session, user.id, trip_id)
    if trip.version != payload.version or int(preview.get("base_version") or 0) != trip.version:
        raise AppError(409, "trip_version_conflict", "旅程已更新，請重新預覽後再套用")
    if not preview.get("changed"):
        raise AppError(422, "itinerary_optimization_unchanged", "目前已是建議安排，不需要套用")
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
        all_rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
        by_id = {row.id: row for row in all_rows}
        segments = [RouteSegment.model_validate(item) for item in preview.get("segments") or []]
        by_pair = {(segment.from_item_id, segment.to_item_id): segment for segment in segments}
        for day in preview.get("days") or []:
            ordered_ids = [UUID(value) for value in day.get("order") or []]
            if any(item_id not in by_id for item_id in ordered_ids):
                raise AppError(409, "itinerary_preview_stale", "行程項目已變更，請重新預覽")
            day_rows = [by_id[item_id] for item_id in ordered_ids]
            for position, row in enumerate(day_rows):
                row.position = position
            for previous, following in zip(day_rows, day_rows[1:], strict=False):
                segment = by_pair.get((previous.id, following.id))
                if segment is None or previous.end_time is None or following.fixed_time:
                    continue
                following.start_time = previous.end_time + timedelta(
                    minutes=segment.duration_minutes + segment.buffer_minutes
                )
                following.end_time = following.start_time + timedelta(
                    minutes=following.duration_minutes or 60
                )
        trip.route_preference = str(preview.get("route_preference") or trip.route_preference)
        trip.data = {**trip.data, "route_optimized": True, "route_order_changed": True}
        trip.version += 1
        await commit_reservation(session, reservation, trip.id)
        await session.commit()
        await cache_trip_routes(trip.id, segments)
        await session.refresh(trip)
        result = await serialize_trip(session, trip)
        result["usage"] = usage_status(reservation).model_dump()
        await redis.set(
            replay_key,
            json.dumps(result["usage"], ensure_ascii=False),
            ex=OPTIMIZATION_PREVIEW_TTL_SECONDS,
        )
        await redis.delete(preview_key)
        return result
    except Exception:
        await release_reservation(session, reservation, "itinerary_optimization_failed")
        await session.commit()
        raise


@router.post("/{trip_id}/itinerary/optimize")
async def optimize_trip_itinerary(
    trip_id: UUID,
    payload: RouteComputeRequest,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    """Optimise and apply in one call.

    Kept for clients that cannot show a preview first; the planner UI uses the
    preview/apply pair instead so the credit is only spent once the user has seen
    what changes.
    """

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
        preference = payload.route_preference or trip.route_preference
        plan = await plan_itinerary_optimization(
            trip,
            all_rows,
            target_days,
            preference,
            await load_runtime_settings(session),
        )
        segments = cast(list[RouteSegment], plan["segments"])
        if not plan["days"] or not segments:
            raise AppError(
                503,
                "itinerary_optimization_unavailable",
                "沒有取得可套用的完整動線結果",
            )
        by_id = {row.id: row for row in all_rows}
        by_pair = {(segment.from_item_id, segment.to_item_id): segment for segment in segments}
        for day in plan["days"]:
            day_rows = [by_id[UUID(value)] for value in day["order"]]
            for position, row in enumerate(day_rows):
                row.position = position
            for previous, following in zip(day_rows, day_rows[1:], strict=False):
                segment = by_pair.get((previous.id, following.id))
                if segment is None or previous.end_time is None or following.fixed_time:
                    continue
                following.start_time = previous.end_time + timedelta(
                    minutes=segment.duration_minutes + segment.buffer_minutes
                )
                following.end_time = following.start_time + timedelta(
                    minutes=following.duration_minutes or 60
                )
        trip.route_preference = preference
        trip.data = {
            **trip.data,
            "route_optimized": True,
            "route_order_changed": bool(plan["changed"]),
        }
        trip.version += 1
        await commit_reservation(session, reservation, trip.id)
        await session.commit()
        await cache_trip_routes(trip.id, segments)
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
                if current is not None and current.data.get("flight_selection_source") != "manual":
                    current.item_type = item.item_type
                    current.offer_id = item.offer_id
                    current.title = item.title
                    current.location_name = item.location_name
                    current.start_time = item.start_time
                    current.end_time = item.end_time
                    current.is_estimated = item.is_estimated
                    current.data = item.data
                    if plan.flight is not None and item.offer_id == plan.flight.id:
                        current.data = {
                            **item.data,
                            "price_snapshot": offer_price_snapshot(
                                plan.flight.model_dump(mode="json")
                            ),
                        }
                continue
            if item.locked:
                continue
            row = item_record(trip.id, item, preserve_source_id=False)
            if day.date in locked_dates:
                row.position += 100
            row.data = {**row.data, "reoptimized_at": checked_at}
            session.add(row)
    plan_data = plan.model_dump(mode="json")
    next_lodging, lodging_warning = merge_reoptimized_lodging(
        primary_lodging(trip, existing_items), plan.hotel
    )
    if (
        next_lodging is not None
        and plan.hotel is not None
        and next_lodging.get("selection_source") == "reoptimize"
    ):
        next_lodging = {
            **next_lodging,
            "provider": plan.hotel.provider,
            "hotel_id": plan.hotel.hotel_id,
            "price_snapshot": offer_price_snapshot(plan.hotel.model_dump(mode="json")),
        }
    if lodging_warning:
        warnings = [*warnings, lodging_warning]
    if plan.hotel is not None and next_lodging is not None:
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
    # Additive allowlist: a new field on the owner's payload never reaches the share
    # link until it is named here. trip.data (preferences, budget, cost breakdown,
    # planner provider) and every per-item note stay with the owner.
    return {
        **{key: payload[key] for key in PUBLIC_TRIP_KEYS},
        "items": [public_item(item) for item in payload["items"]],
    }
