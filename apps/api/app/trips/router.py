import asyncio
import hashlib
import json
import secrets
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Annotated, Any, Literal, cast
from uuid import UUID, uuid4, uuid5

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
from app.infra import enforce_named_rate_limit, get_redis
from app.models import (
    SearchRequest,
    TripPlan,
    TripPlanItem,
    TripShare,
    UsageReservation,
)
from app.optimization.engine import TripOptimizer, TripPlanResult
from app.places.google import GoogleTravelService
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
from app.trips.routing import RoutePoint, RouteSegment, RouteService, is_japan_trip
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
    duration_minutes: int | None = Field(default=None, ge=1, le=1440)
    notes: str | None = Field(default=None, max_length=4000)
    fixed_time: bool = False


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
    )


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
        "duration_minutes": item.duration_minutes,
        "notes": item.notes,
        "fixed_time": item.fixed_time,
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
    if items:
        return items
    raw_days = trip.data.get("itinerary", [])
    for raw_day in raw_days:
        for raw_item in raw_day.get("items", []):
            parsed = ItineraryItem.model_validate(raw_item)
            session.add(item_record(trip.id, parsed, preserve_source_id=False))
    if raw_days:
        await session.commit()
        return await load_items(session, trip.id)
    return []


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
    if include_items:
        cached_routes = await get_redis().get(f"routes:trip:{trip.id}")
        if cached_routes:
            raw = cached_routes.decode() if isinstance(cached_routes, bytes) else str(cached_routes)
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
        "planning": trip.data.get("planning"),
        "version": trip.version,
        "destination_name": trip.destination_name,
        "destination_place_id": trip.destination_place_id,
        "start_date": trip.start_date,
        "end_date": trip.end_date,
        "timezone": trip.timezone,
        "route_preference": trip.route_preference,
        "items": [serialize_item(item) for item in items],
        "route_segments": route_segments,
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
            }
            for item in (preserved_items or [])
        ],
    )


async def _enrich_ai_places(
    planning: AIPlanningResult,
    service: GoogleTravelService,
) -> None:
    if not service.configured:
        return
    suggestions = [
        item for day in planning.itinerary for item in day.items if item.item_type == "suggestion"
    ][:24]
    semaphore = asyncio.Semaphore(4)

    async def resolve(item: ItineraryItem) -> bool:
        async with semaphore:
            place = await service.search_place(item.location_name or item.title, None, None)
        if not place:
            item.data = {**item.data, "places_status": "unavailable"}
            return False
        location = cast(dict[str, Any], place.get("location", {}))
        display = cast(dict[str, Any], place.get("displayName", {}))
        latitude = location.get("latitude")
        longitude = location.get("longitude")
        if latitude is None or longitude is None:
            item.data = {**item.data, "places_status": "unavailable"}
            return False
        item.location_name = str(
            display.get("text") or place.get("formattedAddress") or item.location_name
        )
        item.latitude = float(latitude)
        item.longitude = float(longitude)
        item.provider_place_id = str(place.get("id") or "") or None
        item.location_source = "google_places"
        item.is_estimated = False
        item.data = {
            **item.data,
            "places_status": "resolved",
            "needs_place_confirmation": False,
            "google_maps_url": place.get("googleMapsUri"),
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
    )


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
    refresh: bool = False,
) -> tuple[list[RouteSegment], list[tuple[UUID, UUID]]]:
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
        japan=is_japan_trip(trip.timezone, trip.destination_name, trip.data),
        refresh=refresh,
    )
    segments = [result for result in results if result is not None]
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
                    offers = [
                        offer.model_copy(update={"is_fallback": True}) for offer in offers
                    ]
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
    place_service = GoogleTravelService(redis, settings)
    hotels = [item for item in offers.get("hotel", []) if isinstance(item, HotelOffer)]
    activities = [item for item in offers.get("activities", []) if isinstance(item, ActivityOffer)]
    if place_service.configured:
        hotels, activities = await asyncio.gather(
            place_service.enrich_hotels(hotels),
            place_service.enrich_activities(activities),
        )
    plans = TripOptimizer().optimize(
        query,
        [item for item in offers.get("flight", []) if isinstance(item, FlightOffer)],
        hotels,
        activities,
        [item for item in offers.get("transport", []) if isinstance(item, TransportOffer)],
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
        await _enrich_ai_places(planning, GoogleTravelService(get_redis(), settings))
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
        return await serialize_trip(session, trip)

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
    if trip.start_date and any(
        item.day_date < trip.start_date or (trip.end_date and item.day_date > trip.end_date)
        for item in payload.items
    ):
        raise AppError(422, "itinerary_date_out_of_range", "行程項目日期超出旅程範圍")
    next_data = {**trip.data, "edited": True}
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
    await session.execute(delete(TripPlanItem).where(TripPlanItem.trip_plan_id == trip.id))
    for item in payload.items:
        session.add(item_record(trip.id, item))
    if payload.route_preference:
        trip.route_preference = payload.route_preference
    await session.commit()
    await get_redis().delete(f"routes:trip:{trip.id}")
    await session.refresh(trip)
    return await serialize_trip(session, trip)


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
            item for item in preserved if target_date is None or item.day_date == target_date
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
        await _enrich_ai_places(planning, GoogleTravelService(get_redis(), settings))
        preserved_keys = {(item.day_date, (item.title or "").casefold()) for item in preserved}
        generated = [
            item
            for day in planning.itinerary
            for item in day.items
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
        for day_value in sorted({item.day_date for item in all_rows if item.day_date is not None}):
            day_rows = sorted(
                (item for item in all_rows if item.day_date == day_value),
                key=lambda item: (
                    item.start_time is None,
                    item.start_time or datetime.max.replace(tzinfo=UTC),
                    item.position,
                ),
            )
            for position, item in enumerate(day_rows):
                item.position = position
        planning_data = {
            **planning.planning.model_dump(mode="json"),
            "scope": payload.scope,
            "day_date": target_date.isoformat() if target_date else None,
        }
        trip.data = {
            **trip.data,
            "planning": planning_data,
            "ai_regenerated": True,
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
        return result
    except Exception:
        await session.rollback()
        current = await session.get(UsageReservation, reservation_id)
        if current is not None:
            await release_reservation(session, current, "ai_itinerary_generation_failed")
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
        trip, rows, preference, settings, refresh=payload.refresh
    )
    if not segments:
        if not settings.google_maps_api_key and not (
            is_japan_trip(trip.timezone, trip.destination_name, trip.data)
            and settings.navitime_configured
        ):
            raise AppError(
                503,
                "google_routes_not_configured",
                "Google Maps 路線服務尚未啟用，請先設定伺服器 API 金鑰",
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
            day_rows = [row for row in all_rows if row.day_date == target_day]
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
                japan=is_japan_trip(trip.timezone, trip.destination_name, trip.data),
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
                    or following.locked
                    or following.fixed_time
                ):
                    continue
                following.start_time = previous.end_time + timedelta(
                    minutes=segment.duration_minutes
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
    for day in plan.itinerary:
        # User-locked anchors remain byte-for-byte intact. Fresh movable items are
        # rebuilt around them, and provider-generated fixed duplicates are omitted.
        for item in day.items:
            if item.locked:
                continue
            row = item_record(trip.id, item, preserve_source_id=False)
            if day.date in locked_dates:
                row.position += 100
            row.data = {**row.data, "reoptimized_at": checked_at}
            session.add(row)
    plan_data = plan.model_dump(mode="json")
    trip.mode = plan.mode
    trip.total_price = plan.total_cost.total_cost
    trip.currency = plan.total_cost.currency
    trip.data = {
        **plan_data,
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
