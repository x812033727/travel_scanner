"""Public catalog references, never client-provided names, URLs or provider payloads."""

from typing import Any
from urllib.parse import urlencode
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.community.pet_models import PetPlace
from app.community.schemas import PlaceInput
from app.foods.publication import publishable_merchant_filters
from app.hotspots.service import load_hotspot_names
from app.models import FoodMerchant, TravelHotspot


def canonical_refs(places: list[PlaceInput]) -> list[dict[str, str]]:
    return [
        {"kind": kind, "id": identifier}
        for kind, identifier in dict.fromkeys((place.kind, str(place.id)) for place in places)
    ]


async def public_places(session: AsyncSession, refs: list[dict[str, str]]) -> list[dict[str, Any]]:
    """Re-check publication on every read, including old approved post versions."""
    ids: dict[str, list[UUID]] = {"pet_place": [], "hotspot": [], "merchant": []}
    for ref in refs:
        if ref["kind"] in ids:
            ids[ref["kind"]].append(UUID(ref["id"]))
    results: dict[tuple[str, str], dict[str, Any]] = {}

    if ids["pet_place"]:
        for pet in (
            await session.scalars(
                select(PetPlace).where(
                    PetPlace.id.in_(ids["pet_place"]), PetPlace.status == "approved"
                )
            )
        ).all():
            identifier = str(pet.id)
            results[("pet_place", identifier)] = {
                "kind": "pet_place",
                "id": identifier,
                "name": pet.name,
                "names": pet.names,
                "destination": pet.destination,
                "href": f"/pet-friendly/{identifier}",
            }
    if ids["hotspot"]:
        hotspots = list(
            (
                await session.scalars(
                    select(TravelHotspot).where(
                        TravelHotspot.id.in_(ids["hotspot"]),
                        TravelHotspot.is_active.is_(True),
                        TravelHotspot.review_status == "approved",
                    )
                )
            ).all()
        )
        names = await load_hotspot_names(session, hotspots)
        for hotspot in hotspots:
            identifier = str(hotspot.id)
            results[("hotspot", identifier)] = {
                "kind": "hotspot",
                "id": identifier,
                "name": hotspot.name,
                "names": names.get(hotspot.id, {}),
                "destination": hotspot.city_name,
                "href": "/hotspots?"
                + urlencode(
                    {
                        "hotspot": identifier,
                        "destination": hotspot.destination_id,
                    }
                ),
            }
    if ids["merchant"]:
        for merchant in (
            await session.scalars(
                select(FoodMerchant).where(
                    FoodMerchant.id.in_(ids["merchant"]),
                    *publishable_merchant_filters(),
                )
            )
        ).all():
            identifier = str(merchant.id)
            results[("merchant", identifier)] = {
                "kind": "merchant",
                "id": identifier,
                "name": merchant.name,
                "names": merchant.names_json,
                "destination": merchant.destination_id,
                "href": "/foods?"
                + urlencode(
                    {
                        "merchant": identifier,
                        "destination": merchant.destination_id,
                    }
                ),
            }
    return [results[key] for ref in refs if (key := (ref["kind"], ref["id"])) in results]
