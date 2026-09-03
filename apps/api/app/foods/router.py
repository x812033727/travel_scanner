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
from app.foods.publication import publishable_merchant_filters
from app.foods.schemas import (
    FoodCategoriesResponse,
    FoodCitiesResponse,
    MerchantListResponse,
    MerchantTripSelectionRequest,
)
from app.foods.selection import apply_merchant_meal_selection
from app.foods.service import (
    food_facets,
    foods_for_planner,
    list_foods,
    list_merchants,
    merchant_categories,
    merchant_cities,
)
from app.hotspots.maps import has_exact_map_identity
from app.i18n import Locale, current_locale
from app.locations.coordinates import has_durable_coordinates
from app.models import FoodMerchant, FoodMerchantFood, TravelFood
from app.problems import AppError

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


@router.get("/cities", response_model=FoodCitiesResponse)
async def food_cities(session: Session, locale: RequestLocale) -> dict[str, Any]:
    return await merchant_cities(session, locale=locale)


@router.get("/categories", response_model=FoodCategoriesResponse)
async def food_categories(
    session: Session,
    locale: RequestLocale,
    destination_id: Annotated[str | None, Query(min_length=2, max_length=64)] = None,
    area: Annotated[str | None, Query(min_length=2, max_length=128)] = None,
) -> dict[str, Any]:
    if destination_id and destination_for_id(destination_id) is None:
        raise AppError(422, "unsupported_destination", "目前不支援這個目的地")
    return await merchant_categories(
        session,
        locale=locale,
        destination_id=destination_id.casefold() if destination_id else None,
        area_slug=area,
    )


@router.get("/merchants", response_model=MerchantListResponse)
async def food_merchants(
    session: Session,
    locale: RequestLocale,
    destination_id: Annotated[str | None, Query(min_length=2, max_length=64)] = None,
    area: Annotated[str | None, Query(min_length=2, max_length=128)] = None,
    category: Annotated[str | None, Query(min_length=2, max_length=128)] = None,
    q: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    cursor: Annotated[str | None, Query(max_length=100)] = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
) -> dict[str, Any]:
    if destination_id and destination_for_id(destination_id) is None:
        raise AppError(422, "unsupported_destination", "目前不支援這個目的地")
    return await list_merchants(
        session,
        locale=locale,
        destination_id=destination_id.casefold() if destination_id else None,
        area_slug=area,
        category_slug=category,
        q=q,
        cursor=cursor,
        limit=limit,
    )


@router.post("/merchants/{merchant_id}/trip-selections")
async def select_merchant_for_trip(
    merchant_id: UUID,
    payload: MerchantTripSelectionRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    merchant = await session.scalar(
        select(FoodMerchant).where(FoodMerchant.id == merchant_id, *publishable_merchant_filters())
    )
    if merchant is None:
        raise AppError(404, "food_merchant_not_found", "找不到可加入行程的店家")
    dish_query = (
        select(TravelFood)
        .join(FoodMerchantFood, FoodMerchantFood.food_id == TravelFood.id)
        .where(
            FoodMerchantFood.merchant_id == merchant.id,
            TravelFood.review_status == "approved",
            TravelFood.is_active.is_(True),
        )
        .order_by(FoodMerchantFood.is_primary.desc(), FoodMerchantFood.display_order)
    )
    if payload.food_id is not None:
        dish_query = dish_query.where(TravelFood.id == payload.food_id)
    food = await session.scalar(dish_query.limit(1))
    if payload.food_id is not None and food is None:
        raise AppError(404, "food_merchant_not_found", "這家店沒有這道料理")
    return await apply_merchant_meal_selection(
        session,
        user.id,
        merchant=merchant,
        food=food,
        trip_id=payload.trip_id,
        version=payload.version,
        day_date=payload.day_date,
        meal_role=payload.meal_role,
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
        merchant.coordinate_source_type,
        merchant.coordinate_source_url,
    ):
        raise AppError(422, "food_merchant_location_unverified", "店家地點尚未完成驗證")
    return await apply_merchant_meal_selection(
        session,
        user.id,
        merchant=merchant,
        food=food,
        trip_id=payload.trip_id,
        version=payload.version,
        day_date=payload.day_date,
        meal_role=payload.meal_role,
    )
