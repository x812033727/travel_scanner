"""The paste box: links in, candidates out."""

from __future__ import annotations

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.db import get_session
from app.infra import enforce_named_rate_limit
from app.models import TripPlaceCandidate
from app.problems import AppError
from app.trips.ingest import (
    DAILY_PLACE_LIMIT,
    MAX_LINES_PER_PASTE,
    candidate_from,
    catalogue_names,
    hotspots_by_place_id,
    parse_line,
    serialize_candidate,
    split_lines,
)
from app.trips.router import owned_trip

router = APIRouter(prefix="/trips/{trip_id}/places", tags=["trips"])
Session = Annotated[AsyncSession, Depends(get_session)]

DAY_SECONDS = 86_400


class PlaceIngestRequest(BaseModel):
    """What the traveller pasted, one place per line."""

    text: str = Field(min_length=1, max_length=8_000)


async def _candidates(session: AsyncSession, trip_id: UUID) -> list[TripPlaceCandidate]:
    return list(
        (
            await session.scalars(
                select(TripPlaceCandidate)
                .where(
                    TripPlaceCandidate.trip_plan_id == trip_id,
                    TripPlaceCandidate.status == "inbox",
                )
                .order_by(TripPlaceCandidate.created_at)
            )
        ).all()
    )


@router.get("")
async def list_place_candidates(
    trip_id: UUID,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    trip = await owned_trip(session, user.id, trip_id)
    return {"items": [serialize_candidate(row) for row in await _candidates(session, trip.id)]}


@router.post("/ingest", status_code=201)
async def ingest_places(
    trip_id: UUID,
    payload: PlaceIngestRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    """Read every pasted line into the waiting list, without planning anything."""
    trip = await owned_trip(session, user.id, trip_id)
    lines = split_lines(payload.text)
    if not lines:
        raise AppError(422, "trip_places_empty", "請至少貼上一個地點或 Google Maps 連結")
    if len(lines) > MAX_LINES_PER_PASTE:
        raise AppError(
            422,
            "trip_places_too_many_lines",
            f"一次最多貼上 {MAX_LINES_PER_PASTE} 個地點，請分批貼",
        )

    parsed = []
    for line in lines:
        # Counted per line, before any redirect is followed, so a long paste cannot spend
        # more of the day's budget than it is allowed to.
        await enforce_named_rate_limit(
            "trip-place-ingest",
            str(user.id),
            limit=DAILY_PLACE_LIMIT,
            window_seconds=DAY_SECONDS,
        )
        parsed.append(await parse_line(line))

    catalogue = await hotspots_by_place_id(
        session, [item.place_id for item in parsed if item.place_id]
    )
    names_by_hotspot = await catalogue_names(session, list(catalogue.values()))
    created = []
    for item in parsed:
        hotspot = catalogue.get(item.place_id or "")
        names = names_by_hotspot.get(hotspot.id) if hotspot else None
        created.append(candidate_from(trip.id, item, hotspot, names))
    for row in created:
        session.add(row)
    await session.commit()
    for row in created:
        await session.refresh(row)
    return {
        "created": [serialize_candidate(row) for row in created],
        "matched": sum(1 for row in created if row.hotspot_id is not None),
        "items": [serialize_candidate(row) for row in await _candidates(session, trip.id)],
    }


@router.delete("/{candidate_id}", status_code=204)
async def dismiss_place_candidate(
    trip_id: UUID,
    candidate_id: UUID,
    user: CurrentUser,
    session: Session,
) -> None:
    trip = await owned_trip(session, user.id, trip_id)
    candidate = await session.get(TripPlaceCandidate, candidate_id)
    if candidate is None or candidate.trip_plan_id != trip.id:
        raise AppError(404, "trip_place_not_found", "找不到這個待安排地點")
    candidate.status = "dismissed"
    await session.commit()


@router.post("/{candidate_id}/used", status_code=200)
async def mark_place_candidate_used(
    trip_id: UUID,
    candidate_id: UUID,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    """Called once the traveller has dropped this place into a day."""
    trip = await owned_trip(session, user.id, trip_id)
    candidate = await session.get(TripPlaceCandidate, candidate_id)
    if candidate is None or candidate.trip_plan_id != trip.id:
        raise AppError(404, "trip_place_not_found", "找不到這個待安排地點")
    candidate.status = "used"
    await session.commit()
    return {"items": [serialize_candidate(row) for row in await _candidates(session, trip.id)]}
