from decimal import Decimal
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.db import get_session
from app.models import (
    Plan,
    PlanEntitlement,
    SearchRequest,
    Subscription,
    TripPlan,
)
from app.problems import AppError
from app.usage.service import commit_reservation, reserve_credits

router = APIRouter(prefix="/trips", tags=["trips"])
Session = Annotated[AsyncSession, Depends(get_session)]


class SaveTripRequest(BaseModel):
    search_id: UUID
    plan_id: UUID
    name: str = Field(min_length=1, max_length=255)


async def limit_for(session: AsyncSession, user_id: UUID, key: str) -> int:
    value = await session.scalar(
        select(PlanEntitlement.value)
        .join(Plan, PlanEntitlement.plan_id == Plan.id)
        .join(Subscription, Subscription.plan_id == Plan.id)
        .where(Subscription.user_id == user_id, PlanEntitlement.key == key)
    )
    return int(value or 0)


def serialize(trip: TripPlan) -> dict[str, Any]:
    return {
        "id": str(trip.id),
        "name": trip.name,
        "mode": trip.mode,
        "total_price": trip.total_price,
        "currency": trip.currency,
        "data": trip.data,
        "created_at": trip.created_at,
    }


@router.post("", status_code=201)
async def save_trip(
    payload: SaveTripRequest, user: CurrentUser, session: Session
) -> dict[str, Any]:
    count = await session.scalar(
        select(func.count()).select_from(TripPlan).where(TripPlan.user_id == user.id)
    )
    if int(count or 0) >= await limit_for(session, user.id, "saved_trips"):
        raise AppError(403, "trip_limit_reached", "The saved-trip limit for this plan was reached")
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
    )
    session.add(trip)
    await session.commit()
    await session.refresh(trip)
    return serialize(trip)


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
    return [serialize(trip) for trip in trips]


@router.get("/{trip_id}")
async def get_trip(trip_id: UUID, user: CurrentUser, session: Session) -> dict[str, Any]:
    trip = await session.scalar(
        select(TripPlan).where(TripPlan.id == trip_id, TripPlan.user_id == user.id)
    )
    if trip is None:
        raise AppError(404, "trip_not_found", "Saved trip was not found")
    return serialize(trip)


@router.delete("/{trip_id}", status_code=204)
async def delete_trip(trip_id: UUID, user: CurrentUser, session: Session) -> None:
    trip = await session.scalar(
        select(TripPlan).where(TripPlan.id == trip_id, TripPlan.user_id == user.id)
    )
    if trip is None:
        raise AppError(404, "trip_not_found", "Saved trip was not found")
    await session.delete(trip)
    await session.commit()


@router.post("/{trip_id}/reoptimize")
async def reoptimize_trip(
    trip_id: UUID,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    trip = await session.scalar(
        select(TripPlan).where(TripPlan.id == trip_id, TripPlan.user_id == user.id)
    )
    if trip is None:
        raise AppError(404, "trip_not_found", "Saved trip was not found")
    reservation, created = await reserve_credits(
        session, user.id, idempotency_key, "price_reoptimization", 3
    )
    if not created and reservation.resource_id == trip.id:
        return serialize(trip)
    reservation.resource_id = trip.id
    await commit_reservation(session, reservation, trip.id)
    trip.data = {
        **trip.data,
        "reoptimized": True,
        "note": "Mock offers were refreshed and rescored.",
    }
    await session.commit()
    return serialize(trip)
