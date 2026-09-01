from typing import Annotated, Any, Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.destinations.catalog import destination_for_id
from app.foods.service import food_facets, foods_for_planner, list_foods
from app.i18n import Locale, current_locale
from app.problems import AppError

router = APIRouter(prefix="/foods", tags=["foods"])
Session = Annotated[AsyncSession, Depends(get_session)]
RequestLocale = Annotated[Locale, Depends(current_locale)]
FoodKind = Literal["main", "noodle_soup", "street_food", "dessert", "drink"]
MealType = Literal["breakfast", "lunch", "dinner", "snack", "dessert", "drink"]


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
