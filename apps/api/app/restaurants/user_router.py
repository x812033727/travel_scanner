from __future__ import annotations

from decimal import Decimal
from typing import Annotated, cast

from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.db import get_session
from app.localized_names import item_names
from app.models import RestaurantFavorite, RestaurantPlace, TripPlan
from app.problems import AppError
from app.restaurants.editorial import editorial_by_google_place_id
from app.trips.selections import SelectionPlace, TripSelectionRequest, place_trip_selection
from app.warnings import warning_code

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


class RestaurantTripSelectionRequest(TripSelectionRequest):
    """``mode``, ``meal`` and ``overwrite`` are the shared placement contract.

    ``meal_role`` alone still fills that meal card, as it did before ``mode`` existed.
    """


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
    selection = SelectionPlace(
        title=title,
        location_name=str(editorial.get("address") or editorial["name"]) if editorial else title,
        # Editorial names are single-language source text; the placeholder label
        # exists in every site locale, so store it and let the card follow the UI.
        names_json=(
            {} if editorial else item_names(title=fallback_names, location_name=fallback_names)
        ),
        latitude=Decimal(str(ride_location["latitude"])) if ride_location is not None else None,
        longitude=Decimal(str(ride_location["longitude"])) if ride_location is not None else None,
        provider_place_id=place.google_place_id,
        location_source="travel_scanner_editorial" if editorial else "google_place_id",
        is_estimated=editorial is None,
        # An appended restaurant is an ordinary stop, the way the trip editor's own
        # place browser adds one; a meal card keeps its type and duration.
        item_type="custom",
        duration_minutes=60,
        data={
            "restaurant_place_id": place.google_place_id,
            "restaurant_maps_url": place.generated_maps_url,
            "restaurant_editorial_source": editorial.get("source_kind") if editorial else None,
        },
    )
    result = await place_trip_selection(
        session,
        user.id,
        request=payload,
        place=selection,
        warning=warning_code("restaurant_changed"),
        event_path="/restaurants",
        event_properties={"kind": "restaurant"},
    )
    return cast(dict[str, object], result)
