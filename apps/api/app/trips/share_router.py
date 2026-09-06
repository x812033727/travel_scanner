"""Turning a shared link into a trip of your own.

A shared link is read-only, and co-editing would mean rewriting ``owned_trip()`` and
every caller of it. Copying is the cheap half of that idea and the half that turns a
shared link into an account: the reader gets their own trip, the author's copy is
untouched, and nothing the author kept private travels with it.
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.db import get_session
from app.models import TripPlan, TripPlanItem, TripRouteDaySetting, TripShare
from app.problems import AppError
from app.trips.router import limit_for, serialize_trip

router = APIRouter(prefix="/shared-trips", tags=["shared trips"])
Session = Annotated[AsyncSession, Depends(get_session)]

# What a copied stop keeps from the author's ``data``. Anything else is the author's own
# working state: their price snapshots, their AI prompt, their private notes.
COPIED_ITEM_DATA_KEYS = frozenset(
    {
        "timeline_section",
        "flight_info",
        "source_mode",
        "needs_place_confirmation",
        "generated_by",
        "destination_city",
        "destination_country",
    }
)


async def shared_trip_for(session: AsyncSession, token: str) -> TripPlan:
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
    return trip


def copied_item(trip_id: Any, source: TripPlanItem) -> TripPlanItem:
    return TripPlanItem(
        trip_plan_id=trip_id,
        item_type=source.item_type,
        day_date=source.day_date,
        position=source.position,
        title=source.title,
        location_name=source.location_name,
        names_json=dict(source.names_json or {}),
        start_time=source.start_time,
        end_time=source.end_time,
        latitude=source.latitude,
        longitude=source.longitude,
        coordinate_source_type=source.coordinate_source_type,
        coordinate_source_url=source.coordinate_source_url,
        coordinate_verified_at=source.coordinate_verified_at,
        locked=source.locked,
        is_estimated=source.is_estimated,
        provider_place_id=source.provider_place_id,
        location_source=source.location_source,
        duration_minutes=source.duration_minutes,
        fixed_time=source.fixed_time,
        system_role=source.system_role,
        is_skipped=source.is_skipped,
        # notes stay with the author, as they do on the share payload itself.
        notes=None,
        data={
            key: value
            for key, value in (source.data or {}).items()
            if key in COPIED_ITEM_DATA_KEYS
        },
    )


@router.post("/{token}/fork", status_code=201)
async def fork_shared_trip(
    token: str,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    """Copy a shared trip into the reader's own account."""
    source = await shared_trip_for(session, token)
    count = await session.scalar(
        select(func.count()).select_from(TripPlan).where(TripPlan.user_id == user.id)
    )
    if int(count or 0) >= await limit_for(session, user.id, "saved_trips"):
        raise AppError(403, "trip_limit_reached", "已達所有會員共用的 20 筆儲存旅程上限")

    now = datetime.now(UTC)
    trip = TripPlan(
        user_id=user.id,
        search_id=None,
        name=source.name,
        mode="manual",
        # The author's prices came from their own search on their own dates; a copy that
        # carried the number would be quoting a price nobody checked.
        total_price=0,
        currency=source.currency,
        destination_name=source.destination_name,
        destination_place_id=source.destination_place_id,
        start_date=source.start_date,
        end_date=source.end_date,
        timezone=source.timezone,
        route_preference=source.route_preference,
        data={
            "source": "shared_trip",
            "creation_mode": "shared_trip",
            "forked_from": str(source.id),
            "forked_at": now.isoformat(),
            "destination_city": (source.data or {}).get("destination_city"),
            "destination_country": (source.data or {}).get("destination_country"),
            "prices_checked": False,
            "routing": {
                "status": "stale",
                "total": 0,
                "completed": 0,
                "warnings": ["這是從分享連結存下的行程，移動時間需要重新計算。"],
                "updated_at": now.isoformat(),
            },
        },
    )
    session.add(trip)
    await session.flush()

    items = list(
        (
            await session.scalars(
                select(TripPlanItem)
                .where(TripPlanItem.trip_plan_id == source.id)
                .order_by(TripPlanItem.day_date, TripPlanItem.position)
            )
        ).all()
    )
    for item in items:
        session.add(copied_item(trip.id, item))
    settings = list(
        (
            await session.scalars(
                select(TripRouteDaySetting).where(
                    TripRouteDaySetting.trip_plan_id == source.id
                )
            )
        ).all()
    )
    for setting in settings:
        session.add(
            TripRouteDaySetting(
                trip_plan_id=trip.id,
                day_date=setting.day_date,
                default_travel_mode=setting.default_travel_mode,
                default_buffer_minutes=setting.default_buffer_minutes,
                route_preference=setting.route_preference,
                # Routes are never copied: a saved segment carries absolute times and a
                # provider's attribution. The copy computes its own when asked.
                auto_compute=False,
            )
        )
    await session.commit()
    await session.refresh(trip)
    return await serialize_trip(session, trip)
