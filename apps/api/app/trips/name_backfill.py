"""Give trip items saved before ``names_json`` existed their per-locale labels.

Migration ``0039_localized_names`` added the column empty, so every stop that
was already in a plan keeps showing the single language it was saved in. The
rows still reference the catalog (``data.hotspot_id``, ``data.merchant_id``,
``data.food_id``) and their titles were built from catalog text by the same
code paths that now write the map, so the map can be rebuilt after the fact:
a stop whose stored title still equals the catalog's canonical text gets the
catalog labels; one the traveller renamed is left alone, exactly as a rename
today drops the map. Run once after deploying the migration:

    uv run python -m app.cli backfill-trip-item-names --dry-run
    uv run python -m app.cli backfill-trip-item-names
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.foods.service import load_food_names, merchant_names
from app.hotspots.service import load_hotspot_names
from app.localized_names import item_names, join_localized_names
from app.models import FoodMerchant, TravelFood, TravelHotspot, TripPlanItem
from app.restaurants.user_router import SAVED_RESTAURANT_LABELS
from app.trips.itinerary import CROSS_CITY_TITLE_SUFFIX, MERCHANT_PENDING_LABELS
from app.trips.schedule import MEAL_PLACEHOLDER_LABELS

Names = Mapping[str, str]
CatalogRow = tuple[Any, Names]
BATCH_SIZE = 500


def rebuild_item_names(
    item: TripPlanItem,
    *,
    hotspot: tuple[TravelHotspot, Names] | None = None,
    merchant: tuple[FoodMerchant, Names] | None = None,
    dish: tuple[TravelFood, Names] | None = None,
) -> dict[str, dict[str, str]]:
    """The ``names_json`` a row would carry today, or ``{}`` when its text no longer matches."""

    title = item.title or ""
    location = item.location_name or ""
    title_names: Names | None = None
    location_names: Names | None = None
    if hotspot is not None:
        row, names = hotspot
        if title == row.name:
            title_names = names
        elif title == f"{row.name}{CROSS_CITY_TITLE_SUFFIX['zh-TW']}":
            title_names = join_localized_names(names, CROSS_CITY_TITLE_SUFFIX, separator=" ")
        if location == row.name:
            location_names = names
    elif merchant is not None or dish is not None:
        merchant_row, merchant_labels = merchant if merchant else (None, {})
        dish_row, dish_labels = dish if dish else (None, {})
        if merchant_row is not None and dish_row is not None:
            if title == f"{dish_row.local_name} · {merchant_row.name}":
                title_names = join_localized_names(dish_labels, merchant_labels)
        if title_names is None and merchant_row is not None and title == merchant_row.name:
            title_names = merchant_labels
        if title_names is None and dish_row is not None:
            dish_titles = {dish_row.local_name, dish_row.romanized_name, dish_labels.get("zh-TW")}
            if title in dish_titles:
                title_names = dish_labels
        if merchant_row is not None and location == merchant_row.name:
            location_names = merchant_labels
        elif location == MERCHANT_PENDING_LABELS["zh-TW"]:
            location_names = MERCHANT_PENDING_LABELS
    elif item.system_role in MEAL_PLACEHOLDER_LABELS:
        labels = MEAL_PLACEHOLDER_LABELS[item.system_role]
        if title == labels["zh-TW"]:
            title_names = labels
        elif title in SAVED_RESTAURANT_LABELS.values():
            title_names = SAVED_RESTAURANT_LABELS
            if location == title:
                location_names = SAVED_RESTAURANT_LABELS
    return item_names(title=title_names, location_name=location_names)


def _uuid(value: object) -> UUID | None:
    try:
        return UUID(str(value)) if value else None
    except ValueError:
        return None


async def _load_catalog(
    session: AsyncSession, rows: Iterable[TripPlanItem]
) -> tuple[dict[UUID, CatalogRow], dict[UUID, CatalogRow], dict[UUID, CatalogRow]]:
    hotspot_ids: set[UUID] = set()
    merchant_ids: set[UUID] = set()
    food_ids: set[UUID] = set()
    for row in rows:
        for key, bucket in (
            ("hotspot_id", hotspot_ids),
            ("merchant_id", merchant_ids),
            ("food_id", food_ids),
        ):
            parsed = _uuid(row.data.get(key))
            if parsed is not None:
                bucket.add(parsed)
    hotspots: dict[UUID, CatalogRow] = {}
    if hotspot_ids:
        found = list(
            (
                await session.scalars(
                    select(TravelHotspot).where(TravelHotspot.id.in_(hotspot_ids))
                )
            ).all()
        )
        names = await load_hotspot_names(session, found)
        hotspots = {row.id: (row, names[row.id]) for row in found}
    merchants: dict[UUID, CatalogRow] = {}
    if merchant_ids:
        merchants = {
            row.id: (row, merchant_names(row))
            for row in (
                await session.scalars(select(FoodMerchant).where(FoodMerchant.id.in_(merchant_ids)))
            ).all()
        }
    dishes: dict[UUID, CatalogRow] = {}
    if food_ids:
        found_foods = list(
            (await session.scalars(select(TravelFood).where(TravelFood.id.in_(food_ids)))).all()
        )
        dish_names = await load_food_names(session, found_foods)
        dishes = {row.id: (row, dish_names[row.id]) for row in found_foods}
    return hotspots, merchants, dishes


async def backfill_trip_item_names(
    session: AsyncSession, *, dry_run: bool = False
) -> dict[str, int]:
    """Fill ``names_json`` on catalog-backed rows that still have none; return counts."""

    candidate_ids = list(
        (
            await session.scalars(
                select(TripPlanItem.id)
                .where(
                    or_(
                        TripPlanItem.system_role.in_(list(MEAL_PLACEHOLDER_LABELS)),
                        TripPlanItem.item_type.in_(["activity", "hotspot", "meal", "food"]),
                    )
                )
                .order_by(TripPlanItem.id)
            )
        ).all()
    )
    counts = {"scanned": 0, "already_labelled": 0, "filled": 0, "left_alone": 0}
    for start in range(0, len(candidate_ids), BATCH_SIZE):
        chunk = candidate_ids[start : start + BATCH_SIZE]
        rows = list(
            (await session.scalars(select(TripPlanItem).where(TripPlanItem.id.in_(chunk)))).all()
        )
        counts["scanned"] += len(rows)
        pending = [row for row in rows if not row.names_json]
        counts["already_labelled"] += len(rows) - len(pending)
        hotspots, merchants, dishes = await _load_catalog(session, pending)
        for row in pending:
            hotspot_id = _uuid(row.data.get("hotspot_id"))
            merchant_id = _uuid(row.data.get("merchant_id"))
            food_id = _uuid(row.data.get("food_id"))
            names = rebuild_item_names(
                row,
                hotspot=hotspots.get(hotspot_id) if hotspot_id else None,
                merchant=merchants.get(merchant_id) if merchant_id else None,
                dish=dishes.get(food_id) if food_id else None,
            )
            if names:
                counts["filled"] += 1
                if not dry_run:
                    row.names_json = names
            else:
                counts["left_alone"] += 1
        if dry_run:
            session.expunge_all()
        else:
            await session.commit()
    return counts
