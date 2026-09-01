from __future__ import annotations

import base64
import binascii
from collections import Counter, defaultdict
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.destinations.catalog import destination_for_id
from app.foods.catalog import COUNTRY_NAMES, FOOD_SEEDS
from app.hotspots.maps import build_map_links
from app.models import (
    FoodDestination,
    FoodHotspot,
    FoodLocalization,
    HotspotLocalization,
    TravelFood,
    TravelHotspot,
)
from app.problems import AppError
from app.trips.itinerary import ItineraryFood

PUBLIC_FOOD_STATUS = "approved"
PUBLIC_HOTSPOT_STATUSES = ("approved", "auto_approved")


def _encode_cursor(offset: int) -> str:
    return base64.urlsafe_b64encode(str(offset).encode()).decode().rstrip("=")


def _decode_cursor(cursor: str | None) -> int:
    if not cursor:
        return 0
    try:
        value = cursor + "=" * (-len(cursor) % 4)
        offset = int(base64.urlsafe_b64decode(value).decode())
    except (binascii.Error, ValueError, UnicodeDecodeError) as exc:
        raise AppError(422, "invalid_food_cursor", "美食分頁游標格式不正確") from exc
    if offset < 0:
        raise AppError(422, "invalid_food_cursor", "美食分頁游標格式不正確")
    return offset


def _destination_item(destination_id: str) -> dict[str, Any]:
    profile = destination_for_id(destination_id)
    if profile is None:
        return {"id": destination_id, "name": destination_id, "country_code": None}
    country_codes = {
        "Japan": "JP",
        "South Korea": "KR",
        "Thailand": "TH",
        "Taiwan": "TW",
        "Singapore": "SG",
        "Hong Kong": "HK",
        "Vietnam": "VN",
    }
    return {
        "id": profile.id,
        "name": profile.city,
        "local_name": profile.local_name,
        "english_name": profile.english_name,
        "country_code": country_codes[profile.country],
        "role": profile.role,
        "parent_destination_id": profile.parent_destination_id,
    }


async def seed_food_catalog(session: AsyncSession) -> int:
    """Upsert the reviewed catalog and its approved public food-area links."""

    existing_foods = {row.slug: row for row in (await session.scalars(select(TravelFood))).all()}
    localization_rows = (await session.scalars(select(FoodLocalization))).all()
    localizations = {(row.food_id, row.locale): row for row in localization_rows}
    existing_destinations: dict[UUID, list[FoodDestination]] = defaultdict(list)
    for destination_relation in (await session.scalars(select(FoodDestination))).all():
        existing_destinations[destination_relation.food_id].append(destination_relation)
    existing_hotspot_links: dict[UUID, list[FoodHotspot]] = defaultdict(list)
    for hotspot_relation in (await session.scalars(select(FoodHotspot))).all():
        existing_hotspot_links[hotspot_relation.food_id].append(hotspot_relation)
    seeded: list[tuple[TravelFood, Any]] = []
    for seed in FOOD_SEEDS:
        food = existing_foods.get(seed.slug)
        if food is None:
            food = TravelFood(slug=seed.slug)
            food.country_code = seed.country_code
            food.local_name = seed.local_name
            food.romanized_name = seed.romanized_name
            food.food_kind = seed.food_kind
            food.meal_types = list(seed.meal_types)
            food.ingredient_tags = list(seed.ingredient_tags)
            food.dietary_notes = list(seed.dietary_notes)
            food.search_text = seed.search_text
            food.source_urls = list(seed.source_urls)
            food.review_status = PUBLIC_FOOD_STATUS
            food.is_active = True
            food.display_order = seed.display_order
            session.add(food)
            await session.flush()
        for locale, name in seed.localized_names.items():
            localization = localizations.get((food.id, locale))
            if localization is None:
                localization = FoodLocalization(food_id=food.id, locale=locale)
                localization.name = name
                localization.summary = seed.localized_summaries[locale]
                session.add(localization)
        if not existing_destinations.get(food.id):
            for order, destination_id in enumerate(seed.destination_ids, start=1):
                session.add(
                    FoodDestination(
                        food_id=food.id,
                        destination_id=destination_id,
                        display_order=order,
                    )
                )
        seeded.append((food, seed))
    await session.flush()

    food_areas = list(
        (
            await session.scalars(
                select(TravelHotspot).where(
                    TravelHotspot.category == "food",
                    TravelHotspot.is_active.is_(True),
                    TravelHotspot.review_status.in_(PUBLIC_HOTSPOT_STATUSES),
                    TravelHotspot.latitude.is_not(None),
                    TravelHotspot.longitude.is_not(None),
                )
            )
        ).all()
    )
    areas_by_destination: dict[str, list[TravelHotspot]] = defaultdict(list)
    for hotspot in sorted(food_areas, key=lambda item: (item.destination_id, item.name)):
        areas_by_destination[hotspot.destination_id].append(hotspot)
    for food, seed in seeded:
        if existing_hotspot_links.get(food.id):
            continue
        seen: set[UUID] = set()
        order = 0
        for destination_id in seed.destination_ids:
            for hotspot in areas_by_destination[destination_id][:2]:
                if hotspot.id in seen:
                    continue
                seen.add(hotspot.id)
                order += 1
                session.add(
                    FoodHotspot(food_id=food.id, hotspot_id=hotspot.id, display_order=order)
                )
    await session.flush()
    return len(seeded)


async def _serialize_foods(
    session: AsyncSession, foods: list[TravelFood], locale: str
) -> list[dict[str, Any]]:
    if not foods:
        return []
    food_ids = [food.id for food in foods]
    localization_rows = list(
        (
            await session.scalars(
                select(FoodLocalization).where(
                    FoodLocalization.food_id.in_(food_ids),
                    FoodLocalization.locale == locale,
                )
            )
        ).all()
    )
    localization_by_food = {row.food_id: row for row in localization_rows}
    destination_rows = list(
        (
            await session.scalars(
                select(FoodDestination)
                .where(FoodDestination.food_id.in_(food_ids))
                .order_by(FoodDestination.display_order)
            )
        ).all()
    )
    destinations_by_food: dict[UUID, list[FoodDestination]] = defaultdict(list)
    for row in destination_rows:
        destinations_by_food[row.food_id].append(row)

    hotspot_rows = (
        await session.execute(
            select(FoodHotspot, TravelHotspot)
            .join(TravelHotspot, TravelHotspot.id == FoodHotspot.hotspot_id)
            .where(
                FoodHotspot.food_id.in_(food_ids),
                TravelHotspot.category == "food",
                TravelHotspot.is_active.is_(True),
                TravelHotspot.review_status.in_(PUBLIC_HOTSPOT_STATUSES),
            )
            .order_by(FoodHotspot.display_order)
        )
    ).all()
    hotspot_ids = [hotspot.id for _, hotspot in hotspot_rows]
    hotspot_names = {
        row.hotspot_id: row.name
        for row in (
            await session.scalars(
                select(HotspotLocalization).where(
                    HotspotLocalization.hotspot_id.in_(hotspot_ids),
                    HotspotLocalization.locale == locale,
                )
            )
        ).all()
    }
    hotspots_by_food: dict[UUID, list[dict[str, Any]]] = defaultdict(list)
    for relation, hotspot in hotspot_rows:
        name = hotspot_names.get(hotspot.id, hotspot.name)
        local_name = hotspot.metadata_json.get("local_name")
        hotspots_by_food[relation.food_id].append(
            {
                "hotspot_id": str(hotspot.id),
                "slug": hotspot.slug,
                "name": name,
                "local_name": local_name,
                "destination_id": hotspot.destination_id,
                "latitude": float(hotspot.latitude) if hotspot.latitude is not None else None,
                "longitude": float(hotspot.longitude) if hotspot.longitude is not None else None,
                "map_links": build_map_links(
                    name=name,
                    local_name=local_name,
                    city_name=hotspot.city_name,
                    country_code=hotspot.country_code,
                    latitude=hotspot.latitude,
                    longitude=hotspot.longitude,
                    google_place_id=hotspot.google_place_id,
                ),
            }
        )
    return [
        {
            "id": str(food.id),
            "slug": food.slug,
            "country_code": food.country_code,
            "country_name": COUNTRY_NAMES[food.country_code].get(
                locale, COUNTRY_NAMES[food.country_code]["en"]
            ),
            "name": (
                localization_by_food[food.id].name
                if food.id in localization_by_food
                else food.romanized_name
            ),
            "local_name": food.local_name,
            "romanized_name": food.romanized_name,
            "summary": (
                localization_by_food[food.id].summary if food.id in localization_by_food else ""
            ),
            "food_kind": food.food_kind,
            "meal_types": food.meal_types,
            "ingredient_tags": food.ingredient_tags,
            "dietary_notes": food.dietary_notes,
            "source_urls": food.source_urls,
            "destinations": [
                _destination_item(row.destination_id)
                for row in destinations_by_food.get(food.id, [])
            ],
            "food_hotspots": hotspots_by_food.get(food.id, []),
        }
        for food in foods
    ]


async def list_foods(
    session: AsyncSession,
    *,
    locale: str,
    q: str | None = None,
    country_code: str | None = None,
    destination_id: str | None = None,
    food_kind: str | None = None,
    meal_type: str | None = None,
    cursor: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    foods = list(
        (
            await session.scalars(
                select(TravelFood)
                .where(
                    TravelFood.review_status == PUBLIC_FOOD_STATUS,
                    TravelFood.is_active.is_(True),
                )
                .order_by(TravelFood.display_order, TravelFood.slug)
            )
        ).all()
    )
    ids_for_destination: set[UUID] | None = None
    if destination_id:
        ids_for_destination = set(
            (
                await session.scalars(
                    select(FoodDestination.food_id).where(
                        FoodDestination.destination_id == destination_id.casefold()
                    )
                )
            ).all()
        )
    localized = {
        row.food_id: row
        for row in (
            await session.scalars(select(FoodLocalization).where(FoodLocalization.locale == locale))
        ).all()
    }
    term = (q or "").strip().casefold()
    filtered = [
        food
        for food in foods
        if (not country_code or food.country_code == country_code.upper())
        and (ids_for_destination is None or food.id in ids_for_destination)
        and (not food_kind or food.food_kind == food_kind)
        and (not meal_type or meal_type in food.meal_types)
        and (
            not term
            or term in food.search_text.casefold()
            or (
                food.id in localized
                and term in f"{localized[food.id].name} {localized[food.id].summary}".casefold()
            )
        )
    ]
    offset = _decode_cursor(cursor)
    page = filtered[offset : offset + limit]
    next_offset = offset + len(page)
    return {
        "total": len(filtered),
        "has_more": next_offset < len(filtered),
        "next_cursor": _encode_cursor(next_offset) if next_offset < len(filtered) else None,
        "items": await _serialize_foods(session, page, locale),
    }


async def food_facets(session: AsyncSession, locale: str = "zh-TW") -> dict[str, Any]:
    foods = list(
        (
            await session.scalars(
                select(TravelFood).where(
                    TravelFood.review_status == PUBLIC_FOOD_STATUS,
                    TravelFood.is_active.is_(True),
                )
            )
        ).all()
    )
    food_ids = {food.id for food in foods}
    destination_counts = Counter(
        row.destination_id
        for row in (
            await session.scalars(
                select(FoodDestination).where(FoodDestination.food_id.in_(food_ids))
            )
        ).all()
    )
    country_counts = Counter(food.country_code for food in foods)
    kind_counts = Counter(food.food_kind for food in foods)
    meal_counts = Counter(meal for food in foods for meal in food.meal_types)
    return {
        "total": len(foods),
        "countries": [
            {
                "code": code,
                "name": COUNTRY_NAMES[code].get(locale, COUNTRY_NAMES[code]["en"]),
                "count": count,
            }
            for code, count in sorted(country_counts.items())
        ],
        "destinations": [
            {**_destination_item(destination_id), "count": count}
            for destination_id, count in sorted(destination_counts.items())
        ],
        "food_kinds": [
            {"code": code, "count": count} for code, count in sorted(kind_counts.items())
        ],
        "meal_types": [
            {"code": code, "count": count} for code, count in sorted(meal_counts.items())
        ],
    }


async def foods_for_planner(
    session: AsyncSession,
    *,
    destination_id: str,
    locale: str,
    days: int,
    limit: int,
) -> dict[str, Any]:
    result = await list_foods(
        session,
        locale=locale,
        destination_id=destination_id,
        limit=min(limit, max(1, days)),
    )
    recommendations = []
    for item in result["items"]:
        hotspot = next(
            (
                candidate
                for candidate in item["food_hotspots"]
                if candidate["destination_id"] == destination_id
            ),
            None,
        )
        recommendations.append(
            {
                "food_id": item["id"],
                "name": item["name"],
                "local_name": item["local_name"],
                "food_kind": item["food_kind"],
                "meal_types": item["meal_types"],
                "hotspot_id": hotspot["hotspot_id"] if hotspot else None,
                "hotspot_name": hotspot["name"] if hotspot else None,
                "latitude": hotspot["latitude"] if hotspot else None,
                "longitude": hotspot["longitude"] if hotspot else None,
                "map_links": hotspot["map_links"] if hotspot else [],
                "merchant_status": "area_confirmed" if hotspot else "merchant_pending",
            }
        )
    return {
        "destination_id": destination_id,
        "days": days,
        "recommendations": recommendations,
        "planner_note": "每個完整日最多安排一道代表料理；實際店家、營業時間與評價請於地圖確認。",
    }


async def load_planner_foods(
    session: AsyncSession,
    *,
    destination_id: str,
    locale: str,
    days: int,
    limit: int = 10,
) -> list[ItineraryFood]:
    result = await foods_for_planner(
        session,
        destination_id=destination_id,
        locale=locale,
        days=days,
        limit=limit,
    )
    return [ItineraryFood.model_validate(item) for item in result["recommendations"]]
