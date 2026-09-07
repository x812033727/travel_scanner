from __future__ import annotations

from datetime import date
from typing import Any
from uuid import UUID

from fastapi import APIRouter
from pydantic import Field
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.itinerary import AIPlannerCandidate
from app.auth.service import CurrentUser
from app.community.pet_models import PetPlace, PlaceReference
from app.community.pet_schemas import PetRequirements
from app.community.pets import eligibility, get_place
from app.community.policy import fail, require_open, settings_for
from app.community.router import OpenSession
from app.community.schemas import Input
from app.localized_names import item_names
from app.models import TripPlan, TripPlanItem

router = APIRouter(prefix="/community/trips", tags=["pet-friendly trip planning"])


async def filter_candidates(
    session: AsyncSession, candidates: list[AIPlannerCandidate], requirements: PetRequirements
) -> list[AIPlannerCandidate]:
    settings = await require_open(session)
    references = (
        await session.execute(
            select(PlaceReference, PetPlace)
            .join(PetPlace, PetPlace.id == PlaceReference.place_id)
            .where(PetPlace.status == "approved")
        )
    ).all()
    valid_keys = {
        f"{ref.kind}:{ref.target}"
        for ref, place in references
        if not eligibility(place, requirements, settings.pet_verification_days)
    }
    result = [candidate for candidate in candidates if candidate.key in valid_keys]
    if not result:
        raise fail("pet_candidates_insufficient", 422)
    return result


class PetPreferencesInput(Input):
    version: int = Field(ge=1)
    requirements: PetRequirements | None


async def trip_conflicts(
    session: AsyncSession, items: list[TripPlanItem], requirements: PetRequirements | None
) -> list[dict[str, Any]]:
    if requirements is None:
        return []
    days = (await settings_for(session)).pet_verification_days
    references = (
        await session.execute(
            select(PlaceReference, PetPlace).join(PetPlace, PetPlace.id == PlaceReference.place_id)
        )
    ).all()
    by_key = {f"{ref.kind}:{ref.target}": place for ref, place in references}
    conflicts = []
    for item in items:
        if item.is_skipped or item.item_type in {"flight", "transport"} or not item.location_name:
            continue
        data = item.data or {}
        place = by_key.get(str(data.get("candidate_key", "")))
        if data.get("pet_place_id"):
            try:
                place = await session.get(PetPlace, UUID(data["pet_place_id"]))
            except ValueError:
                place = None
        reasons = eligibility(place, requirements, days) if place else ["verification_required"]
        if reasons:
            conflicts.append({"item_id": str(item.id), "title": item.title, "conflicts": reasons})
    return conflicts


@router.put("/{trip_id}/pet-preferences")
async def set_pet_preferences(
    trip_id: UUID, payload: PetPreferencesInput, user: CurrentUser, session: OpenSession
) -> dict[str, Any]:
    from app.trips.router import load_items, owned_trip

    trip = await owned_trip(session, user.id, trip_id)
    if trip.version != payload.version:
        raise fail("trip_version_conflict", 409)
    preferences = dict(trip.data.get("preferences") or {})
    preferences["pet_companion"] = (
        payload.requirements.model_dump() if payload.requirements else None
    )
    next_version = await session.scalar(
        update(TripPlan)
        .where(
            TripPlan.id == trip.id, TripPlan.user_id == user.id, TripPlan.version == payload.version
        )
        .values(data={**trip.data, "preferences": preferences}, version=TripPlan.version + 1)
        .returning(TripPlan.version)
    )
    if next_version is None:
        await session.rollback()
        raise fail("trip_version_conflict", 409)
    conflicts = await trip_conflicts(
        session, await load_items(session, trip.id), payload.requirements
    )
    await session.commit()
    return {
        "version": next_version,
        "requirements": preferences["pet_companion"],
        "conflicts": conflicts,
    }


@router.get("/{trip_id}/pet-preferences")
async def pet_preferences(trip_id: UUID, user: CurrentUser, session: OpenSession) -> dict[str, Any]:
    from app.trips.router import load_items, owned_trip

    trip = await owned_trip(session, user.id, trip_id)
    raw = trip.data.get("preferences", {}).get("pet_companion")
    requirements = PetRequirements.model_validate(raw) if raw else None
    return {
        "version": trip.version,
        "requirements": raw,
        "conflicts": await trip_conflicts(
            session, await load_items(session, trip.id), requirements
        ),
    }


class AddPetPlaceInput(Input):
    place_id: UUID
    day: date
    version: int = Field(ge=1)
    confirm_conflicts: bool = False


@router.post("/{trip_id}/pet-places", status_code=201)
async def add_pet_place(
    trip_id: UUID, payload: AddPetPlaceInput, user: CurrentUser, session: OpenSession
) -> dict[str, Any]:
    from app.trips.router import load_items, owned_trip

    trip = await owned_trip(session, user.id, trip_id)
    if trip.version != payload.version:
        raise fail("trip_version_conflict", 409)
    if (
        not trip.start_date
        or not trip.end_date
        or not trip.start_date <= payload.day <= trip.end_date
    ):
        raise fail("itinerary_date_out_of_range", 422)
    place = await get_place(session, payload.place_id)
    raw = trip.data.get("preferences", {}).get("pet_companion")
    requirements = PetRequirements.model_validate(raw) if raw else None
    reasons = (
        eligibility(place, requirements, (await settings_for(session)).pet_verification_days)
        if requirements
        else []
    )
    if reasons and not payload.confirm_conflicts:
        return {"confirmation_required": True, "conflicts": reasons, "version": trip.version}
    items = await load_items(session, trip.id)
    position = (
        max((item.position for item in items if item.day_date == payload.day), default=-1) + 1
    )
    item = TripPlanItem(
        trip_plan_id=trip.id,
        item_type="hotspot",
        day_date=payload.day,
        position=position,
        title=place.name,
        location_name=place.name,
        duration_minutes=60,
        names_json=item_names(title=place.names, location_name=place.names),
        latitude=place.latitude,
        longitude=place.longitude,
        coordinate_source_type="admin_verified",
        coordinate_source_url=place.coordinate_source_url,
        coordinate_verified_at=place.verified_at if place.coordinate_source_url else None,
        locked=True,
        data={"pet_place_id": str(place.id)},
    )
    session.add(item)
    next_version = await session.scalar(
        update(TripPlan)
        .where(
            TripPlan.id == trip.id, TripPlan.user_id == user.id, TripPlan.version == payload.version
        )
        .values(
            data={**trip.data, "routing": {"status": "stale", "total": 0, "completed": 0}},
            version=TripPlan.version + 1,
        )
        .returning(TripPlan.version)
    )
    if next_version is None:
        await session.rollback()
        raise fail("trip_version_conflict", 409)
    await session.commit()
    return {
        "item_id": str(item.id),
        "version": trip.version,
        "conflicts": reasons,
        "confirmation_required": False,
    }
