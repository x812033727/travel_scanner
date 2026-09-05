from __future__ import annotations

from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.db import get_session
from app.destinations.catalog import destination_for_id
from app.foods.publication import publishable_merchant_filters
from app.foods.service import localized_name
from app.hotspots.maps import build_map_links
from app.hotspots.service import load_hotspot_names
from app.i18n import Locale, current_locale
from app.localized_names import resolve_localized_name
from app.models import (
    FoodArea,
    FoodCategory,
    FoodFavorite,
    FoodLocalization,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantFavorite,
    HotspotFavorite,
    RestaurantFavorite,
    RestaurantPlace,
    TravelFood,
    TravelHotspot,
)
from app.problems import AppError

router = APIRouter(prefix="/saved-items", tags=["saved items"])
Session = Annotated[AsyncSession, Depends(get_session)]
RequestLocale = Annotated[Locale, Depends(current_locale)]
SavedType = Literal["hotspot", "food", "restaurant", "merchant"]


async def _hotspot(session: AsyncSession, item_id: str) -> TravelHotspot:
    try:
        parsed = UUID(item_id)
    except ValueError as exc:
        raise AppError(404, "saved_item_not_found", "找不到這個景點") from exc
    item = await session.scalar(
        select(TravelHotspot).where(
            TravelHotspot.id == parsed,
            TravelHotspot.is_active.is_(True),
            TravelHotspot.review_status.in_(("approved", "auto_approved")),
        )
    )
    if item is None:
        raise AppError(404, "saved_item_not_found", "找不到這個景點")
    return item


async def _food(session: AsyncSession, item_id: str) -> TravelFood:
    try:
        parsed = UUID(item_id)
    except ValueError as exc:
        raise AppError(404, "saved_item_not_found", "找不到這道料理") from exc
    item = await session.scalar(
        select(TravelFood).where(
            TravelFood.id == parsed,
            TravelFood.is_active.is_(True),
            TravelFood.review_status == "approved",
        )
    )
    if item is None:
        raise AppError(404, "saved_item_not_found", "找不到這道料理")
    return item


async def _merchant(session: AsyncSession, item_id: str) -> FoodMerchant:
    try:
        parsed = UUID(item_id)
    except ValueError as exc:
        raise AppError(404, "saved_item_not_found", "找不到這家店家") from exc
    item = await session.scalar(
        select(FoodMerchant).where(FoodMerchant.id == parsed, *publishable_merchant_filters())
    )
    if item is None:
        raise AppError(404, "saved_item_not_found", "找不到這家店家")
    return item


async def _restaurant(session: AsyncSession, item_id: str) -> RestaurantPlace:
    item = await session.scalar(
        select(RestaurantPlace).where(
            RestaurantPlace.google_place_id == item_id,
            RestaurantPlace.is_suppressed.is_(False),
            RestaurantPlace.identity_status.not_in(("moved", "not_found")),
        )
    )
    if item is None:
        raise AppError(404, "saved_item_not_found", "找不到這間餐廳")
    return item


@router.get("")
async def list_saved_items(
    user: CurrentUser,
    session: Session,
    locale: RequestLocale,
    type: Annotated[Literal["all", "hotspot", "food", "restaurant", "merchant"], Query()] = "all",
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    if type in {"all", "hotspot"}:
        hotspot_rows = (
            await session.execute(
                select(HotspotFavorite, TravelHotspot)
                .join(TravelHotspot, TravelHotspot.id == HotspotFavorite.hotspot_id)
                .where(
                    HotspotFavorite.user_id == user.id,
                    TravelHotspot.is_active.is_(True),
                    TravelHotspot.review_status.in_(("approved", "auto_approved")),
                )
            )
        ).all()
        hotspot_names = await load_hotspot_names(session, (hotspot for _, hotspot in hotspot_rows))
        for favorite, hotspot in hotspot_rows:
            items.append(
                {
                    "type": "hotspot",
                    "id": str(hotspot.id),
                    "title": resolve_localized_name(
                        hotspot_names.get(hotspot.id), locale, fallback=hotspot.name
                    ),
                    "subtitle": f"{hotspot.city_name} · {hotspot.category}",
                    "map_links": build_map_links(
                        name=hotspot.name,
                        local_name=hotspot.metadata_json.get("local_name"),
                        city_name=hotspot.city_name,
                        country_code=hotspot.country_code,
                        latitude=hotspot.latitude,
                        longitude=hotspot.longitude,
                        google_place_id=hotspot.google_place_id,
                        naver_map_url=hotspot.naver_map_url,
                        map_match_status=hotspot.map_match_status,
                    ),
                    "saved_at": favorite.created_at,
                }
            )
    if type in {"all", "food"}:
        food_rows = (
            await session.execute(
                select(FoodFavorite, TravelFood, FoodLocalization)
                .join(TravelFood, TravelFood.id == FoodFavorite.food_id)
                .outerjoin(
                    FoodLocalization,
                    (FoodLocalization.food_id == TravelFood.id)
                    & (FoodLocalization.locale == locale),
                )
                .where(
                    FoodFavorite.user_id == user.id,
                    TravelFood.is_active.is_(True),
                    TravelFood.review_status == "approved",
                )
            )
        ).all()
        for favorite, food, localization in food_rows:
            items.append(
                {
                    "type": "food",
                    "id": str(food.id),
                    "title": localization.name if localization else food.romanized_name,
                    "subtitle": food.local_name,
                    "map_links": [],
                    "saved_at": favorite.created_at,
                }
            )
    if type in {"all", "merchant"}:
        merchant_rows = (
            await session.execute(
                select(FoodMerchantFavorite, FoodMerchant, FoodArea)
                .join(FoodMerchant, FoodMerchant.id == FoodMerchantFavorite.merchant_id)
                .outerjoin(
                    FoodArea,
                    (FoodArea.id == FoodMerchant.area_id) & FoodArea.is_active.is_(True),
                )
                .where(FoodMerchantFavorite.user_id == user.id, *publishable_merchant_filters())
            )
        ).all()
        primary_categories: dict[UUID, str] = {}
        for link, category in (
            await session.execute(
                select(FoodMerchantCategory, FoodCategory)
                .join(FoodCategory, FoodCategory.id == FoodMerchantCategory.category_id)
                .where(
                    FoodMerchantCategory.merchant_id.in_(
                        [merchant.id for _, merchant, _ in merchant_rows]
                    ),
                    FoodCategory.is_active.is_(True),
                )
                .order_by(
                    FoodMerchantCategory.is_primary.desc(),
                    FoodMerchantCategory.display_order,
                )
            )
        ).all():
            primary_categories.setdefault(
                link.merchant_id, localized_name(category.names_json, locale)
            )
        for favorite, merchant, area in merchant_rows:
            profile = destination_for_id(merchant.destination_id)
            city_name = profile.city if profile else merchant.destination_id
            detail = (
                localized_name(area.names_json, locale)
                if area is not None
                else primary_categories.get(merchant.id)
            )
            items.append(
                {
                    "type": "merchant",
                    "id": str(merchant.id),
                    "title": resolve_localized_name(
                        merchant.names_json, locale, fallback=merchant.name
                    ),
                    "subtitle": f"{city_name} · {detail}" if detail else city_name,
                    "map_links": build_map_links(
                        name=merchant.name,
                        local_name=merchant.local_name,
                        city_name=city_name,
                        country_code=merchant.country_code,
                        latitude=merchant.latitude,
                        longitude=merchant.longitude,
                        google_place_id=merchant.google_place_id,
                        naver_map_url=merchant.naver_map_url,
                        map_match_status=merchant.map_match_status,
                    ),
                    "saved_at": favorite.created_at,
                }
            )
    if type in {"all", "restaurant"}:
        restaurant_rows = (
            await session.execute(
                select(RestaurantFavorite, RestaurantPlace)
                .join(RestaurantPlace, RestaurantPlace.id == RestaurantFavorite.restaurant_place_id)
                .where(
                    RestaurantFavorite.user_id == user.id,
                    RestaurantPlace.is_suppressed.is_(False),
                )
            )
        ).all()
        for favorite, place in restaurant_rows:
            items.append(
                {
                    "type": "restaurant",
                    "id": place.google_place_id,
                    "title": "已收藏餐廳",
                    "subtitle": "Google Maps 地點",
                    "map_links": [
                        {
                            "provider": "google",
                            "label": "Google Maps",
                            "url": place.generated_maps_url,
                            "primary": True,
                        }
                    ],
                    "saved_at": favorite.created_at,
                }
            )
    items.sort(key=lambda item: item["saved_at"], reverse=True)
    items = items[:limit]
    return {"total": len(items), "has_more": False, "next_cursor": None, "items": items}


@router.put("/{item_type}/{item_id}", status_code=201)
async def save_item(
    item_type: SavedType,
    item_id: str,
    user: CurrentUser,
    session: Session,
) -> dict[str, object]:
    if item_type == "hotspot":
        hotspot = await _hotspot(session, item_id)
        existing_hotspot = await session.scalar(
            select(HotspotFavorite).where(
                HotspotFavorite.user_id == user.id,
                HotspotFavorite.hotspot_id == hotspot.id,
            )
        )
        if existing_hotspot is None:
            session.add(HotspotFavorite(user_id=user.id, hotspot_id=hotspot.id))
    elif item_type == "food":
        food = await _food(session, item_id)
        existing_food = await session.scalar(
            select(FoodFavorite).where(
                FoodFavorite.user_id == user.id,
                FoodFavorite.food_id == food.id,
            )
        )
        if existing_food is None:
            session.add(FoodFavorite(user_id=user.id, food_id=food.id))
    elif item_type == "merchant":
        merchant = await _merchant(session, item_id)
        existing_merchant = await session.scalar(
            select(FoodMerchantFavorite).where(
                FoodMerchantFavorite.user_id == user.id,
                FoodMerchantFavorite.merchant_id == merchant.id,
            )
        )
        if existing_merchant is None:
            session.add(FoodMerchantFavorite(user_id=user.id, merchant_id=merchant.id))
    else:
        restaurant = await _restaurant(session, item_id)
        existing_restaurant = await session.scalar(
            select(RestaurantFavorite).where(
                RestaurantFavorite.user_id == user.id,
                RestaurantFavorite.restaurant_place_id == restaurant.id,
            )
        )
        if existing_restaurant is None:
            session.add(RestaurantFavorite(user_id=user.id, restaurant_place_id=restaurant.id))
    await session.commit()
    return {"type": item_type, "id": item_id, "saved": True}


@router.delete("/{item_type}/{item_id}", status_code=204)
async def delete_item(
    item_type: SavedType,
    item_id: str,
    user: CurrentUser,
    session: Session,
) -> None:
    if item_type == "hotspot":
        hotspot = await _hotspot(session, item_id)
        await session.execute(
            delete(HotspotFavorite).where(
                HotspotFavorite.user_id == user.id,
                HotspotFavorite.hotspot_id == hotspot.id,
            )
        )
    elif item_type == "food":
        food = await _food(session, item_id)
        await session.execute(
            delete(FoodFavorite).where(
                FoodFavorite.user_id == user.id,
                FoodFavorite.food_id == food.id,
            )
        )
    elif item_type == "merchant":
        merchant = await _merchant(session, item_id)
        await session.execute(
            delete(FoodMerchantFavorite).where(
                FoodMerchantFavorite.user_id == user.id,
                FoodMerchantFavorite.merchant_id == merchant.id,
            )
        )
    else:
        restaurant = await _restaurant(session, item_id)
        await session.execute(
            delete(RestaurantFavorite).where(
                RestaurantFavorite.user_id == user.id,
                RestaurantFavorite.restaurant_place_id == restaurant.id,
            )
        )
    await session.commit()
