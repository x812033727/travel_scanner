from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Annotated, Literal, cast
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.db import get_session
from app.localized_names import item_names
from app.models import RestaurantFavorite, RestaurantPlace, TripPlan
from app.problems import AppError
from app.restaurants.editorial import editorial_by_google_place_id
from app.trips.router import (
    hydrate_legacy_items,
    load_items,
    owned_trip,
    persist_system_schedule_change,
)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])
Session = Annotated[AsyncSession, Depends(get_session)]
# Title of a meal card that points at a Google place without editorial data.
SAVED_RESTAURANT_LABELS: dict[str, str] = {
    "en": "Saved restaurant",
    "ja": "保存したレストラン",
    "ko": "저장한 음식점",
    "zh-CN": "已保存餐厅",
    "zh-TW": "已儲存餐廳",
}


class RestaurantTripSelectionRequest(BaseModel):
    trip_id: UUID
    version: int = Field(ge=1)
    day_date: date
    meal_role: Literal["lunch", "dinner"]


async def _place(session: AsyncSession, place_id: str) -> RestaurantPlace:
    place = await session.scalar(
        select(RestaurantPlace).where(
            RestaurantPlace.google_place_id == place_id,
            RestaurantPlace.is_suppressed.is_(False),
            RestaurantPlace.identity_status.not_in(("moved", "not_found")),
        )
    )
    if place is None:
        raise AppError(404, "restaurant_place_not_found", "找不到這個餐飲地點")
    return place


@router.get("/favorites")
async def list_restaurant_favorites(
    user: CurrentUser,
    session: Session,
) -> dict[str, object]:
    rows = (
        await session.execute(
            select(RestaurantFavorite, RestaurantPlace)
            .join(
                RestaurantPlace,
                RestaurantPlace.id == RestaurantFavorite.restaurant_place_id,
            )
            .where(
                RestaurantFavorite.user_id == user.id,
                RestaurantPlace.is_suppressed.is_(False),
            )
            .order_by(RestaurantFavorite.updated_at.desc())
        )
    ).all()
    editorial = await editorial_by_google_place_id(
        session, [place.google_place_id for _, place in rows]
    )
    return {
        "place_ids": [place.google_place_id for _, place in rows],
        "items": [
            {
                "place_id": place.google_place_id,
                "maps_url": place.generated_maps_url,
                "identity_status": place.identity_status,
                "editorial": editorial.get(place.google_place_id),
                "favorited_at": favorite.created_at,
            }
            for favorite, place in rows
        ],
    }


@router.put("/favorites/{place_id}", status_code=201)
async def save_restaurant_favorite(
    place_id: str,
    user: CurrentUser,
    session: Session,
) -> dict[str, object]:
    place = await _place(session, place_id)
    favorite = await session.scalar(
        select(RestaurantFavorite).where(
            RestaurantFavorite.user_id == user.id,
            RestaurantFavorite.restaurant_place_id == place.id,
        )
    )
    if favorite is None:
        favorite = RestaurantFavorite(user_id=user.id, restaurant_place_id=place.id)
        session.add(favorite)
        await session.commit()
    return {"place_id": place.google_place_id, "favorite": True}


@router.delete("/favorites/{place_id}", status_code=204)
async def delete_restaurant_favorite(
    place_id: str,
    user: CurrentUser,
    session: Session,
) -> None:
    place = await session.scalar(
        select(RestaurantPlace).where(RestaurantPlace.google_place_id == place_id)
    )
    if place is None:
        return
    await session.execute(
        delete(RestaurantFavorite).where(
            RestaurantFavorite.user_id == user.id,
            RestaurantFavorite.restaurant_place_id == place.id,
        )
    )
    await session.commit()


@router.get("/trip-options")
async def restaurant_trip_options(
    user: CurrentUser,
    session: Session,
) -> dict[str, object]:
    trips = list(
        (
            await session.scalars(
                select(TripPlan)
                .where(TripPlan.user_id == user.id)
                .order_by(TripPlan.updated_at.desc())
            )
        ).all()
    )
    return {
        "items": [
            {
                "trip_id": str(trip.id),
                "name": trip.name,
                "version": trip.version,
                "start_date": trip.start_date,
                "end_date": trip.end_date,
            }
            for trip in trips
            if trip.start_date is not None and trip.end_date is not None
        ]
    }


@router.post("/{place_id}/trip-selections")
async def select_restaurant_for_trip(
    place_id: str,
    payload: RestaurantTripSelectionRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, object]:
    place = await _place(session, place_id)
    trip = await owned_trip(session, user.id, payload.trip_id)
    if (
        trip.start_date is None
        or trip.end_date is None
        or not trip.start_date <= payload.day_date <= trip.end_date
    ):
        raise AppError(422, "itinerary_date_out_of_range", "餐廳日期超出旅程範圍")
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
    editorial = (await editorial_by_google_place_id(session, [place.google_place_id])).get(
        place.google_place_id
    )
    locale = user.preferred_locale
    fallback_names = SAVED_RESTAURANT_LABELS
    title = str(editorial["name"]) if editorial else fallback_names.get(locale, "已儲存餐廳")
    ride_location = cast(
        dict[str, float] | None,
        editorial.get("ride_location") if editorial else None,
    )
    meal.title = title
    meal.location_name = str(editorial.get("address") or editorial["name"]) if editorial else title
    # Editorial names are single-language source text; the placeholder label
    # exists in every site locale, so store it and let the card follow the UI.
    meal.names_json = (
        {} if editorial else item_names(title=fallback_names, location_name=fallback_names)
    )
    meal.provider_place_id = place.google_place_id
    meal.latitude = Decimal(str(ride_location["latitude"])) if ride_location is not None else None
    meal.longitude = Decimal(str(ride_location["longitude"])) if ride_location is not None else None
    meal.location_source = "travel_scanner_editorial" if editorial else "google_place_id"
    meal.is_estimated = editorial is None
    meal.is_skipped = False
    meal.data = {
        **meal.data,
        "meal_selection_source": "user",
        "restaurant_place_id": place.google_place_id,
        "restaurant_maps_url": place.generated_maps_url,
        "restaurant_editorial_source": editorial.get("source_kind") if editorial else None,
    }
    result = await persist_system_schedule_change(
        session,
        trip,
        user.id,
        payload.version,
        rows,
        warning="餐廳已更新，請重新計算這一天的路線。",
        target_day=payload.day_date,
    )
    return cast(dict[str, object], result)
