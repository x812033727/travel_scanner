"""Describe a verified merchant (optionally with a dish) as a trip place."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.destinations.catalog import destination_for_id
from app.foods.service import load_food_names, merchant_names
from app.hotspots.maps import build_map_links
from app.localized_names import item_names, join_localized_names
from app.models import FoodMerchant, TravelFood
from app.trips.selections import SelectionPlace, TripSelectionRequest, place_trip_selection
from app.warnings import warning_code


async def apply_merchant_selection(
    session: AsyncSession,
    user_id: UUID,
    *,
    merchant: FoodMerchant,
    food: TravelFood | None,
    request: TripSelectionRequest,
) -> dict[str, Any]:
    """Put ``merchant`` (optionally naming the dish) on the trip day ``request`` asks for.

    Both ``/foods`` endpoints land here, so one adapter covers the dish card and the
    merchant card. The place stores the dish and merchant in every site locale plus
    their original script, so the label follows the traveller's language afterwards;
    where it lands (a new stop, or the day's lunch or dinner card) is the shared
    placement's business — see :mod:`app.trips.selections`.
    """

    city = destination_for_id(merchant.destination_id)
    map_links = build_map_links(
        name=merchant.name,
        local_name=merchant.local_name,
        city_name=city.city if city else merchant.destination_id,
        country_code=merchant.country_code,
        latitude=merchant.latitude,
        longitude=merchant.longitude,
        google_place_id=merchant.google_place_id,
        naver_map_url=merchant.naver_map_url,
        map_match_status=merchant.map_match_status,
    )
    merchant_labels = merchant_names(merchant)
    dish_labels = (await load_food_names(session, [food]))[food.id] if food else None
    place = SelectionPlace(
        title=f"{food.local_name} · {merchant.name}" if food else merchant.name,
        location_name=merchant.address or merchant.name,
        names_json=item_names(
            title=join_localized_names(dish_labels, merchant_labels) if food else merchant_labels,
            # An address is written once, in the local script; only a bare merchant
            # name follows the locale.
            location_name=None if merchant.address else merchant_labels,
        ),
        latitude=merchant.latitude,
        longitude=merchant.longitude,
        coordinate_source_type=merchant.coordinate_source_type,
        coordinate_source_url=merchant.coordinate_source_url,
        coordinate_verified_at=merchant.coordinate_verified_at,
        provider_place_id=merchant.google_place_id,
        location_source=merchant.coordinate_source_type,
        # An appended merchant is an ordinary stop, the way the trip editor's own
        # place browser adds one; a meal card keeps its type and duration.
        item_type="custom",
        duration_minutes=60,
        data={
            "meal_selection_kind": "food_merchant",
            "food_id": str(food.id) if food else None,
            "merchant_id": str(merchant.id),
            "merchant_area_id": str(merchant.area_id) if merchant.area_id else None,
            "merchant_map_links": map_links,
        },
    )
    return await place_trip_selection(
        session,
        user_id,
        request=request,
        place=place,
        warning=warning_code("food_selection_changed"),
        event_path="/foods",
        event_properties={"kind": "food_merchant", "from_dish": food is not None},
    )
