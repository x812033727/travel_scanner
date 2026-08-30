import asyncio
import hashlib
import secrets
from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Annotated, Any, cast
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, Field
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.config import get_settings
from app.db import get_session
from app.infra import get_redis
from app.models import (
    SearchRequest,
    TripPlan,
    TripPlanItem,
    TripShare,
)
from app.optimization.engine import TripOptimizer, TripPlanResult
from app.places.google import GoogleTravelService
from app.problems import AppError
from app.providers.base import TravelProvider
from app.providers.registry import build_provider, provider_status
from app.providers.runner import ProviderRunner, ProviderUnavailableError
from app.providers.schemas import ActivityOffer, FlightOffer, HotelOffer, Offer, TransportOffer
from app.search.schemas import SearchCreate
from app.trips.itinerary import ItineraryItem
from app.usage.service import (
    COMMON_LIMITS,
    commit_reservation,
    release_reservation,
    reserve_use,
    usage_status,
)

router = APIRouter(prefix="/trips", tags=["trips"])
public_router = APIRouter(prefix="/shared-trips", tags=["shared trips"])
Session = Annotated[AsyncSession, Depends(get_session)]


class SaveTripRequest(BaseModel):
    search_id: UUID
    plan_id: UUID
    name: str = Field(min_length=1, max_length=255)


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


class ItineraryUpdateRequest(BaseModel):
    version: int = Field(ge=1)
    items: list[ItineraryItemRequest] = Field(max_length=500)


async def limit_for(session: AsyncSession, user_id: UUID, key: str) -> int:
    _ = session, user_id
    return COMMON_LIMITS.get(key, 0)


def item_record(trip_id: UUID, item: ItineraryItem | ItineraryItemRequest) -> TripPlanItem:
    return TripPlanItem(
        id=item.id or uuid4(),
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
            session.add(item_record(trip.id, parsed))
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
    return {
        "id": str(trip.id),
        "name": trip.name,
        "mode": trip.mode,
        "total_price": trip.total_price,
        "currency": trip.currency,
        "data": trip.data,
        "version": trip.version,
        "items": [serialize_item(item) for item in items],
        "share_enabled": share is not None,
        "created_at": trip.created_at,
        "updated_at": trip.updated_at,
    }


async def owned_trip(session: AsyncSession, user_id: UUID, trip_id: UUID) -> TripPlan:
    trip = await session.scalar(
        select(TripPlan).where(TripPlan.id == trip_id, TripPlan.user_id == user_id)
    )
    if trip is None:
        raise AppError(404, "trip_not_found", "Saved trip was not found")
    return trip


async def run_provider_module(
    provider: TravelProvider,
    runner: ProviderRunner,
    module: str,
    query: SearchCreate,
) -> list[Offer]:
    if module == "flight":
        return cast(
            list[Offer],
            await runner.run(provider.name, module, lambda: provider.search_flights(query)),
        )
    if module == "hotel":
        return cast(
            list[Offer],
            await runner.run(provider.name, module, lambda: provider.search_hotels(query)),
        )
    if module == "activities":
        return cast(
            list[Offer],
            await runner.run(provider.name, module, lambda: provider.search_activities(query)),
        )
    if module == "transport":
        return cast(
            list[Offer],
            await runner.run(provider.name, module, lambda: provider.search_transport(query)),
        )
    return []


async def refreshed_plan(session: AsyncSession, trip: TripPlan) -> tuple[TripPlanResult, list[str]]:
    search = await session.get(SearchRequest, trip.search_id)
    if search is None:
        raise AppError(409, "trip_search_missing", "The original search is unavailable")
    query = SearchCreate.model_validate(search.request_json)
    redis = get_redis()
    provider = build_provider(redis)
    status = provider_status()
    if provider is None:
        raise AppError(503, "travel_provider_unavailable", status.message)
    runner = ProviderRunner(redis)

    async def collect(module: str) -> tuple[str, list[Offer], str | None]:
        try:
            return module, await run_provider_module(provider, runner, module, query), None
        except ProviderUnavailableError as exc:
            return module, [], str(exc)

    refreshed = await asyncio.gather(*(collect(str(module)) for module in query.modules))
    offers = {module: rows for module, rows, _ in refreshed}
    warnings = [warning for _, _, warning in refreshed if warning]
    place_service = GoogleTravelService(redis)
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
    search = await session.scalar(
        select(SearchRequest).where(
            SearchRequest.id == payload.search_id, SearchRequest.user_id == user.id
        )
    )
    if search is None:
        raise AppError(404, "search_not_found", "Search was not found")
    plan = next(
        (
            item
            for item in search.result_json.get("plans", [])
            if item.get("id") == str(payload.plan_id)
        ),
        None,
    )
    if plan is None:
        raise AppError(404, "plan_not_found", "Optimized plan was not found")
    trip = TripPlan(
        user_id=user.id,
        search_id=search.id,
        name=payload.name,
        mode=plan["mode"],
        total_price=Decimal(str(plan["total_cost"]["total_cost"])),
        data=plan,
        version=1,
    )
    session.add(trip)
    await session.flush()
    for raw_day in plan.get("itinerary", []):
        for raw_item in raw_day.get("items", []):
            session.add(item_record(trip.id, ItineraryItem.model_validate(raw_item)))
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


@router.put("/{trip_id}/itinerary")
async def update_itinerary(
    trip_id: UUID,
    payload: ItineraryUpdateRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
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
        raise AppError(409, "trip_version_conflict", "Trip changed; reload before saving again")
    await session.execute(delete(TripPlanItem).where(TripPlanItem.trip_plan_id == trip.id))
    for item in payload.items:
        session.add(item_record(trip.id, item))
    await session.commit()
    await session.refresh(trip)
    return await serialize_trip(session, trip)


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
            row = item_record(trip.id, item)
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
        raise AppError(404, "shared_trip_not_found", "Shared trip was not found")
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    share = await session.scalar(
        select(TripShare).where(
            TripShare.token_hash == token_hash,
            TripShare.revoked_at.is_(None),
        )
    )
    if share is None:
        raise AppError(404, "shared_trip_not_found", "Shared trip was not found")
    trip = await session.get(TripPlan, share.trip_plan_id)
    if trip is None:
        raise AppError(404, "shared_trip_not_found", "Shared trip was not found")
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
            "items",
            "updated_at",
        )
    }
