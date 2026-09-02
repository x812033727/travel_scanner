from datetime import date
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.db import get_session
from app.destinations.catalog import destination_for_id
from app.foods.service import food_facets, foods_for_planner, list_foods
from app.hotspots.maps import build_map_links, has_exact_map_identity
from app.i18n import Locale, current_locale
from app.locations.plus_codes import has_durable_coordinates
from app.models import FoodMerchant, FoodMerchantFood, TravelFood
from app.problems import AppError
from app.trips.router import (
    hydrate_legacy_items,
    load_items,
    owned_trip,
    persist_system_schedule_change,
)

router = APIRouter(prefix="/foods", tags=["foods"])
Session = Annotated[AsyncSession, Depends(get_session)]
RequestLocale = Annotated[Locale, Depends(current_locale)]
FoodKind = Literal["main", "noodle_soup", "street_food", "dessert", "drink"]
MealType = Literal["breakfast", "lunch", "dinner", "snack", "dessert", "drink"]


class FoodTripSelectionRequest(BaseModel):
    trip_id: UUID
    merchant_id: UUID
    version: int = Field(ge=1)
    day_date: date
    meal_role: Literal["lunch", "dinner"]


@router.get("")
async def foods(
    session: Session,
    locale: RequestLocale,
    q: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    country_code: Annotated[str | None, Query(min_length=2, max_length=2)] = None,
    destination_id: Annotated[str | None, Query(min_length=2, max_length=64)] = None,
    food_kind: FoodKind | None = None,
    meal_type: MealType | None = None,
    cursor: Annotated[str | None, Query(max_length=100)] = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
) -> dict[str, Any]:
    if destination_id and destination_for_id(destination_id) is None:
        raise AppError(422, "unsupported_destination", "目前不支援這個目的地")
    return await list_foods(
        session,
        locale=locale,
        q=q,
        country_code=country_code,
        destination_id=destination_id,
        food_kind=food_kind,
        meal_type=meal_type,
        cursor=cursor,
        limit=limit,
    )


@router.get("/facets")
async def foods_facets(session: Session, locale: RequestLocale) -> dict[str, Any]:
    return await food_facets(session, locale)


@router.get("/for-planner")
async def planner_foods(
    session: Session,
    locale: RequestLocale,
    destination_id: Annotated[str, Query(min_length=2, max_length=64)],
    days: Annotated[int, Query(ge=1, le=30)] = 4,
    limit: Annotated[int, Query(ge=1, le=30)] = 10,
) -> dict[str, Any]:
    if destination_for_id(destination_id) is None:
        raise AppError(422, "unsupported_destination", "目前不支援這個目的地")
    return await foods_for_planner(
        session,
        destination_id=destination_id.casefold(),
        locale=locale,
        days=days,
        limit=limit,
    )


@router.post("/{food_id}/trip-selections")
async def select_food_for_trip(
    food_id: UUID,
    payload: FoodTripSelectionRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    row = (
        await session.execute(
            select(TravelFood, FoodMerchant)
            .join(FoodMerchantFood, FoodMerchantFood.food_id == TravelFood.id)
            .join(FoodMerchant, FoodMerchant.id == FoodMerchantFood.merchant_id)
            .where(
                TravelFood.id == food_id,
                TravelFood.review_status == "approved",
                TravelFood.is_active.is_(True),
                FoodMerchant.id == payload.merchant_id,
                FoodMerchant.review_status == "approved",
                FoodMerchant.is_active.is_(True),
                FoodMerchant.map_match_status == "verified",
            )
        )
    ).first()
    if row is None:
        raise AppError(404, "food_merchant_not_found", "找不到可加入行程的推薦店家")
    food, merchant = row
    if not has_exact_map_identity(
        merchant.country_code, merchant.google_place_id, merchant.naver_map_url
    ) or not has_durable_coordinates(
        merchant.latitude,
        merchant.longitude,
        merchant.plus_code_global,
        merchant.coordinate_source_type,
        merchant.coordinate_source_url,
    ):
        raise AppError(422, "food_merchant_location_unverified", "店家地點尚未完成驗證")
    trip = await owned_trip(session, user.id, payload.trip_id)
    if (
        trip.start_date is None
        or trip.end_date is None
        or not trip.start_date <= payload.day_date <= trip.end_date
    ):
        raise AppError(422, "itinerary_date_out_of_range", "用餐日期超出旅程範圍")
    rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    meal = next(
        (
            item
            for item in rows
            if item.day_date == payload.day_date and item.system_role == payload.meal_role
        ),
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
    meal.title = f"{food.local_name} · {merchant.name}"
    meal.location_name = merchant.address or merchant.name
    meal.provider_place_id = merchant.google_place_id
    meal.latitude = merchant.latitude
    meal.longitude = merchant.longitude
    meal.plus_code_global = merchant.plus_code_global
    meal.coordinate_source_type = merchant.coordinate_source_type
    meal.coordinate_source_url = merchant.coordinate_source_url
    meal.coordinate_verified_at = merchant.coordinate_verified_at
    meal.location_source = merchant.coordinate_source_type
    meal.is_estimated = False
    meal.is_skipped = False
    meal.data = {
        **meal.data,
        "meal_selection_source": "food_card",
        "food_id": str(food.id),
        "merchant_id": str(merchant.id),
        "merchant_map_links": map_links,
        "plus_code_global": merchant.plus_code_global,
    }
    result = await persist_system_schedule_change(
        session,
        trip,
        user.id,
        payload.version,
        rows,
        warning="料理與店家已更新，請重新計算這一天的路線。",
        target_day=payload.day_date,
    )
    return result
