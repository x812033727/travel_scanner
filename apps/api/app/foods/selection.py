"""Write a verified merchant into a trip's lunch or dinner slot."""

from __future__ import annotations

from datetime import date
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.destinations.catalog import destination_for_id
from app.hotspots.maps import build_map_links
from app.models import FoodMerchant, TravelFood
from app.problems import AppError
from app.trips.router import (
    hydrate_legacy_items,
    load_items,
    owned_trip,
    persist_system_schedule_change,
)


async def apply_merchant_meal_selection(
    session: AsyncSession,
    user_id: UUID,
    *,
    merchant: FoodMerchant,
    food: TravelFood | None,
    trip_id: UUID,
    version: int,
    day_date: date,
    meal_role: str,
) -> dict[str, Any]:
    """Point a trip meal card at ``merchant`` (optionally naming the dish) and re-plan the day.

    The selection is recorded as a user choice so AI re-planning keeps it, the same
    way restaurant picks are protected.
    """

    trip = await owned_trip(session, user_id, trip_id)
    if (
        trip.start_date is None
        or trip.end_date is None
        or not trip.start_date <= day_date <= trip.end_date
    ):
        raise AppError(422, "itinerary_date_out_of_range", "用餐日期超出旅程範圍")
    rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    meal = next(
        (item for item in rows if item.day_date == day_date and item.system_role == meal_role),
        None,
    )
    if meal is None:
        raise AppError(422, "trip_meal_slot_unavailable", "這一天沒有可設定的餐食卡")
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
    meal.title = f"{food.local_name} · {merchant.name}" if food else merchant.name
    meal.location_name = merchant.address or merchant.name
    meal.provider_place_id = merchant.google_place_id
    meal.latitude = merchant.latitude
    meal.longitude = merchant.longitude
    meal.coordinate_source_type = merchant.coordinate_source_type
    meal.coordinate_source_url = merchant.coordinate_source_url
    meal.coordinate_verified_at = merchant.coordinate_verified_at
    meal.location_source = merchant.coordinate_source_type
    meal.is_estimated = False
    meal.is_skipped = False
    meal.data = {
        **meal.data,
        "meal_selection_source": "user",
        "meal_selection_kind": "food_merchant",
        "food_id": str(food.id) if food else None,
        "merchant_id": str(merchant.id),
        "merchant_area_id": str(merchant.area_id) if merchant.area_id else None,
        "merchant_map_links": map_links,
    }
    return await persist_system_schedule_change(
        session,
        trip,
        user_id,
        version,
        rows,
        warning="料理與店家已更新，請重新計算這一天的路線。",
        target_day=day_date,
    )
