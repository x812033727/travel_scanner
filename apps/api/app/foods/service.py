from __future__ import annotations

import base64
import binascii
from collections import Counter, defaultdict
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import escape_like
from app.destinations.catalog import DESTINATIONS, destination_for_id
from app.foods.area_catalog import AREA_SEEDS
from app.foods.catalog import COUNTRY_NAMES, FOOD_SEEDS
from app.foods.category_catalog import CATEGORY_SEEDS
from app.foods.merchant_catalog import MERCHANT_DIRECT_SOURCE_SEEDS, MERCHANT_SEEDS
from app.foods.publication import merchant_is_publishable, publishable_merchant_filters
from app.hotspots.maps import build_map_links, has_exact_map_identity
from app.locations.coordinates import has_durable_coordinates
from app.models import (
    FoodArea,
    FoodCategory,
    FoodDestination,
    FoodHotspot,
    FoodLocalization,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantFood,
    FoodMerchantSource,
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


def destination_country_code(destination_id: str) -> str | None:
    """ISO country code for a supported destination id, or None when unknown."""

    if destination_for_id(destination_id) is None:
        return None
    return str(_destination_item(destination_id)["country_code"])


LOCAL_NAME_LOCALES: dict[str, str] = {
    "JP": "ja",
    "KR": "ko",
    "TW": "zh-TW",
    "HK": "zh-TW",
    "SG": "en",
    "TH": "en",
    "VN": "en",
}


def localized_name(names: Mapping[str, Any], locale: str) -> str:
    """Resolve a ``names_json`` label with the locale → en → zh-TW → any fallback chain."""

    for candidate in (locale, "en", "zh-TW"):
        value = names.get(candidate)
        if value:
            return str(value)
    return next((str(value) for value in names.values() if value), "")


def _area_ref(area: FoodArea, locale: str) -> dict[str, Any]:
    local_locale = LOCAL_NAME_LOCALES.get(area.country_code.upper(), "en")
    local_name = area.names_json.get(local_locale)
    return {
        "id": str(area.id),
        "slug": area.slug,
        "name": localized_name(area.names_json, locale),
        "local_name": str(local_name) if local_name else None,
    }


def _category_ref(category: FoodCategory, locale: str, *, is_primary: bool) -> dict[str, Any]:
    return {
        "slug": category.slug,
        "name": localized_name(category.names_json, locale),
        "is_primary": is_primary,
    }


async def _merchant_taxonomy(
    session: AsyncSession, merchant_ids: set[UUID], locale: str
) -> tuple[dict[UUID, dict[str, Any]], dict[UUID, list[dict[str, Any]]]]:
    """Area and active category refs for a batch of merchants, keyed by merchant id."""

    if not merchant_ids:
        return {}, {}
    area_rows = (
        await session.execute(
            select(FoodMerchant.id, FoodArea)
            .join(FoodArea, FoodArea.id == FoodMerchant.area_id)
            .where(FoodMerchant.id.in_(merchant_ids), FoodArea.is_active.is_(True))
        )
    ).all()
    areas = {merchant_id: _area_ref(area, locale) for merchant_id, area in area_rows}
    category_rows = (
        await session.execute(
            select(FoodMerchantCategory, FoodCategory)
            .join(FoodCategory, FoodCategory.id == FoodMerchantCategory.category_id)
            .where(
                FoodMerchantCategory.merchant_id.in_(merchant_ids),
                FoodCategory.is_active.is_(True),
            )
            .order_by(
                FoodMerchantCategory.merchant_id,
                FoodMerchantCategory.is_primary.desc(),
                FoodMerchantCategory.display_order,
            )
        )
    ).all()
    categories: dict[UUID, list[dict[str, Any]]] = defaultdict(list)
    for link, category in category_rows:
        categories[link.merchant_id].append(
            _category_ref(category, locale, is_primary=link.is_primary)
        )
    return areas, dict(categories)


async def seed_food_taxonomy(
    session: AsyncSession,
) -> tuple[dict[str, FoodCategory], dict[str, FoodArea]]:
    """Create missing categories and areas; rows that already exist are never touched."""

    categories = {row.slug: row for row in (await session.scalars(select(FoodCategory))).all()}
    for category_seed in CATEGORY_SEEDS:
        if category_seed.slug in categories:
            continue
        category = FoodCategory(
            slug=category_seed.slug,
            names_json=dict(category_seed.names),
            display_order=category_seed.display_order,
            is_active=True,
            source="seed",
        )
        session.add(category)
        categories[category_seed.slug] = category
    areas = {row.slug: row for row in (await session.scalars(select(FoodArea))).all()}
    for area_seed in AREA_SEEDS:
        if area_seed.slug in areas:
            continue
        area = FoodArea(
            slug=area_seed.slug,
            destination_id=area_seed.destination_id,
            country_code=str(_destination_item(area_seed.destination_id)["country_code"] or ""),
            names_json=dict(area_seed.names),
            match_terms_json=list(area_seed.match_terms),
            latitude=area_seed.center[0] if area_seed.center else None,
            longitude=area_seed.center[1] if area_seed.center else None,
            display_order=area_seed.display_order,
            is_active=True,
            source="seed",
        )
        session.add(area)
        areas[area_seed.slug] = area
    await session.flush()
    return categories, areas


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
        # Add the links the seed lists that are missing, rather than only filling in a dish
        # that has none. Extending an existing dish to another city is how a city joins the
        # catalog, and the previous "all or nothing" test made that a silent no-op. Links
        # the seed no longer lists are left alone: an administrator may have added them.
        linked = {row.destination_id for row in existing_destinations.get(food.id, [])}
        next_order = max((row.display_order for row in existing_destinations[food.id]), default=0)
        for destination_id in seed.destination_ids:
            if destination_id in linked:
                continue
            next_order += 1
            relation = FoodDestination(
                food_id=food.id,
                destination_id=destination_id,
                display_order=next_order,
            )
            session.add(relation)
            existing_destinations[food.id].append(relation)
        seeded.append((food, seed))
    await session.flush()

    food_by_slug = {food.slug: food for food, _ in seeded}
    existing_merchants = {
        row.slug: row for row in (await session.scalars(select(FoodMerchant))).all()
    }
    existing_merchant_foods = {
        (row.merchant_id, row.food_id)
        for row in (await session.scalars(select(FoodMerchantFood))).all()
    }
    source_rows = list((await session.scalars(select(FoodMerchantSource))).all())
    existing_sources = {
        (row.merchant_id, row.source_url, row.edition_year): row for row in source_rows
    }
    seed_context_sources = {
        row.merchant_id: row
        for row in source_rows
        if row.source_type == "official_tourism"
        and row.source_scope == "destination_context"
        and row.edition_year is None
        and row.source_title
        in {
            "Official destination food guide",
            "Official destination food guide (regional context only)",
        }
    }
    direct_sources_by_slug: dict[str, list[Any]] = defaultdict(list)
    for direct_source_seed in MERCHANT_DIRECT_SOURCE_SEEDS:
        direct_sources_by_slug[direct_source_seed.merchant_slug].append(direct_source_seed)
    categories_by_slug, areas_by_slug = await seed_food_taxonomy(session)
    merchant_category_counts = Counter(
        (await session.scalars(select(FoodMerchantCategory.merchant_id))).all()
    )
    for merchant_seed in MERCHANT_SEEDS:
        merchant = existing_merchants.get(merchant_seed.slug)
        if merchant is None:
            merchant = FoodMerchant(
                slug=merchant_seed.slug,
                destination_id=merchant_seed.destination_id,
                country_code=merchant_seed.country_code,
                name=merchant_seed.name,
                local_name=merchant_seed.local_name,
                google_place_id=None,
                naver_map_url=None,
                map_match_status="unverified",
                review_status="pending",
                is_active=False,
                verified_at=None,
                display_order=merchant_seed.display_order,
            )
            session.add(merchant)
            await session.flush()
        # Taxonomy backfill never overrides an administrator: a cleared area is marked
        # ``admin`` and any existing category link means the set was curated.
        if (
            merchant.area_id is None
            and merchant.area_source is None
            and merchant_seed.area_slug in areas_by_slug
        ):
            merchant.area_id = areas_by_slug[merchant_seed.area_slug].id
            merchant.area_source = "seed"
        if merchant_category_counts.get(merchant.id, 0) == 0:
            for order, category_slug in enumerate(merchant_seed.category_slugs, start=1):
                session.add(
                    FoodMerchantCategory(
                        merchant_id=merchant.id,
                        category_id=categories_by_slug[category_slug].id,
                        is_primary=order == 1,
                        display_order=order,
                        source="seed",
                    )
                )
            merchant_category_counts[merchant.id] = len(merchant_seed.category_slugs)
        for order, food_slug in enumerate(merchant_seed.food_slugs, start=1):
            food = food_by_slug[food_slug]
            key = (merchant.id, food.id)
            if key not in existing_merchant_foods:
                session.add(
                    FoodMerchantFood(
                        merchant_id=merchant.id,
                        food_id=food.id,
                        is_primary=True,
                        display_order=order,
                    )
                )
                existing_merchant_foods.add(key)
        source_key = (merchant.id, merchant_seed.source_url, None)
        source = existing_sources.get(source_key) or seed_context_sources.get(merchant.id)
        if source is None:
            source = FoodMerchantSource(
                merchant_id=merchant.id,
                source_type="official_tourism",
                source_scope="destination_context",
                source_title=merchant_seed.source_title,
                source_url=merchant_seed.source_url,
                claims_json=[],
                edition_year=None,
                distinction=None,
                is_current=True,
                last_verified_at=datetime.now(UTC),
            )
            session.add(source)
            existing_sources[source_key] = source
        else:
            source_url_changed = source.source_url != merchant_seed.source_url
            source.source_url = merchant_seed.source_url
            source.source_type = "official_tourism"
            source.source_scope = "destination_context"
            source.source_title = merchant_seed.source_title
            source.claims_json = []
            source.is_current = True
            if source_url_changed:
                source.last_verified_at = datetime.now(UTC)
            existing_sources[source_key] = source

        for direct_source_seed in direct_sources_by_slug.get(merchant_seed.slug, []):
            direct_source_key = (merchant.id, direct_source_seed.source_url, None)
            direct_source = existing_sources.get(direct_source_key)
            if direct_source is None:
                direct_source = FoodMerchantSource(
                    merchant_id=merchant.id,
                    source_type=direct_source_seed.source_type,
                    source_scope=direct_source_seed.source_scope,
                    source_title=direct_source_seed.source_title,
                    source_url=direct_source_seed.source_url,
                    claims_json=list(direct_source_seed.claims),
                    edition_year=None,
                    distinction=None,
                    is_current=True,
                    last_verified_at=datetime.now(UTC),
                )
                session.add(direct_source)
                existing_sources[direct_source_key] = direct_source
            else:
                source_changed = any(
                    (
                        direct_source.source_type != direct_source_seed.source_type,
                        direct_source.source_scope != direct_source_seed.source_scope,
                        direct_source.source_title != direct_source_seed.source_title,
                        direct_source.claims_json != list(direct_source_seed.claims),
                        not direct_source.is_current,
                    )
                )
                direct_source.source_type = direct_source_seed.source_type
                direct_source.source_scope = direct_source_seed.source_scope
                direct_source.source_title = direct_source_seed.source_title
                direct_source.claims_json = list(direct_source_seed.claims)
                direct_source.is_current = True
                if source_changed:
                    direct_source.last_verified_at = datetime.now(UTC)
            if direct_source_seed.official_website_url and merchant.official_website_url is None:
                merchant.official_website_url = direct_source_seed.official_website_url
                merchant.official_website_verified_at = datetime.now(UTC)

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
    session: AsyncSession,
    foods: list[TravelFood],
    locale: str,
    merchant_destination_id: str | None = None,
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
                    naver_map_url=hotspot.naver_map_url,
                    map_match_status=hotspot.map_match_status,
                ),
            }
        )

    merchant_filters = [
        FoodMerchantFood.food_id.in_(food_ids),
        FoodMerchant.review_status == PUBLIC_FOOD_STATUS,
        FoodMerchant.is_active.is_(True),
        FoodMerchant.map_match_status == "verified",
        FoodMerchant.latitude.is_not(None),
        FoodMerchant.longitude.is_not(None),
        FoodMerchant.coordinate_source_type.is_not(None),
        FoodMerchant.coordinate_source_url.is_not(None),
    ]
    if merchant_destination_id:
        merchant_filters.append(FoodMerchant.destination_id == merchant_destination_id)
    merchant_rows = (
        await session.execute(
            select(FoodMerchantFood, FoodMerchant)
            .join(FoodMerchant, FoodMerchant.id == FoodMerchantFood.merchant_id)
            .where(*merchant_filters)
            .order_by(
                FoodMerchantFood.food_id,
                FoodMerchantFood.display_order,
                FoodMerchant.display_order,
                FoodMerchant.name,
            )
        )
    ).all()
    merchant_ids = {merchant.id for _, merchant in merchant_rows}
    areas_by_merchant, categories_by_merchant = await _merchant_taxonomy(
        session, merchant_ids, locale
    )
    source_rows = list(
        (
            await session.scalars(
                select(FoodMerchantSource)
                .where(
                    FoodMerchantSource.merchant_id.in_(merchant_ids),
                    FoodMerchantSource.is_current.is_(True),
                )
                .order_by(FoodMerchantSource.edition_year.desc().nullslast())
            )
        ).all()
    )
    sources_by_merchant: dict[UUID, list[dict[str, Any]]] = defaultdict(list)
    for source in source_rows:
        sources_by_merchant[source.merchant_id].append(
            {
                "source_type": source.source_type,
                "source_scope": source.source_scope,
                "title": source.source_title,
                "url": source.source_url,
                "claims": source.claims_json,
                "edition_year": source.edition_year,
                "distinction": source.distinction,
                "last_verified_at": source.last_verified_at.isoformat(),
            }
        )
    merchants_by_food: dict[UUID, list[dict[str, Any]]] = defaultdict(list)
    destinations_seen: dict[UUID, set[str]] = defaultdict(set)
    for relation, merchant in merchant_rows:
        merchant_sources = sources_by_merchant.get(merchant.id, [])
        if not merchant_sources:
            continue
        if not has_exact_map_identity(
            merchant.country_code, merchant.google_place_id, merchant.naver_map_url
        ) or not has_durable_coordinates(
            merchant.latitude,
            merchant.longitude,
            merchant.coordinate_source_type,
            merchant.coordinate_source_url,
        ):
            continue
        if merchant_destination_id:
            if len(merchants_by_food[relation.food_id]) >= 3:
                continue
        elif merchant.destination_id in destinations_seen[relation.food_id]:
            continue
        destinations_seen[relation.food_id].add(merchant.destination_id)
        profile = destination_for_id(merchant.destination_id)
        city_name = profile.city if profile else merchant.destination_id
        merchants_by_food[relation.food_id].append(
            {
                "merchant_id": str(merchant.id),
                "slug": merchant.slug,
                "name": merchant.name,
                "local_name": merchant.local_name,
                "destination_id": merchant.destination_id,
                "address": merchant.address,
                "latitude": float(merchant.latitude) if merchant.latitude is not None else None,
                "longitude": float(merchant.longitude) if merchant.longitude is not None else None,
                "coordinate_source": {
                    "type": merchant.coordinate_source_type,
                    "url": merchant.coordinate_source_url,
                    "verified_at": merchant.coordinate_verified_at.isoformat()
                    if merchant.coordinate_verified_at is not None
                    else None,
                },
                "official_website_url": merchant.official_website_url,
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
                "verified_at": merchant.verified_at.isoformat()
                if merchant.verified_at is not None
                else None,
                "sources": merchant_sources,
                "area": areas_by_merchant.get(merchant.id),
                "categories": categories_by_merchant.get(merchant.id, []),
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
            "recommended_merchants": merchants_by_food.get(food.id, []),
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
        "items": await _serialize_foods(
            session,
            page,
            locale,
            merchant_destination_id=destination_id.casefold() if destination_id else None,
        ),
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
        limit=min(limit, max(1, days * 2 - 2)),
    )
    recommendations = []
    for item in result["items"]:
        merchant = next(
            (
                candidate
                for candidate in item["recommended_merchants"]
                if candidate["destination_id"] == destination_id
            ),
            None,
        )
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
                "merchant_id": merchant["merchant_id"] if merchant else None,
                "merchant_name": merchant["name"] if merchant else None,
                "hotspot_id": hotspot["hotspot_id"] if hotspot else None,
                "hotspot_name": hotspot["name"] if hotspot else None,
                "latitude": merchant["latitude"] if merchant else None,
                "longitude": merchant["longitude"] if merchant else None,
                "map_links": merchant["map_links"] if merchant else [],
                "merchant_status": "verified" if merchant else "merchant_pending",
            }
        )
    return {
        "destination_id": destination_id,
        "days": days,
        "recommendations": recommendations,
        "planner_note": "每個完整日最多安排一道代表料理；店家來自核准目錄，營業時間請於地圖確認。",
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


def _merchant_source_view(source: FoodMerchantSource) -> dict[str, Any]:
    return {
        "source_type": source.source_type,
        "source_scope": source.source_scope,
        "title": source.source_title,
        "url": source.source_url,
        "claims": source.claims_json,
        "edition_year": source.edition_year,
        "distinction": source.distinction,
        "last_verified_at": source.last_verified_at.isoformat(),
    }


async def _serialize_merchant_cards(
    session: AsyncSession, merchants: list[FoodMerchant], locale: str
) -> list[dict[str, Any]]:
    if not merchants:
        return []
    merchant_ids = {merchant.id for merchant in merchants}
    areas_by_merchant, categories_by_merchant = await _merchant_taxonomy(
        session, merchant_ids, locale
    )
    sources_by_merchant: dict[UUID, list[dict[str, Any]]] = defaultdict(list)
    for source in (
        await session.scalars(
            select(FoodMerchantSource)
            .where(
                FoodMerchantSource.merchant_id.in_(merchant_ids),
                FoodMerchantSource.is_current.is_(True),
            )
            .order_by(FoodMerchantSource.edition_year.desc().nullslast())
        )
    ).all():
        sources_by_merchant[source.merchant_id].append(_merchant_source_view(source))
    dish_rows = (
        await session.execute(
            select(FoodMerchantFood, TravelFood)
            .join(TravelFood, TravelFood.id == FoodMerchantFood.food_id)
            .where(
                FoodMerchantFood.merchant_id.in_(merchant_ids),
                TravelFood.review_status == PUBLIC_FOOD_STATUS,
                TravelFood.is_active.is_(True),
            )
            .order_by(
                FoodMerchantFood.merchant_id,
                FoodMerchantFood.is_primary.desc(),
                FoodMerchantFood.display_order,
            )
        )
    ).all()
    dish_names = {
        row.food_id: row.name
        for row in (
            await session.scalars(
                select(FoodLocalization).where(
                    FoodLocalization.food_id.in_({food.id for _, food in dish_rows}),
                    FoodLocalization.locale == locale,
                )
            )
        ).all()
    }
    dishes_by_merchant: dict[UUID, list[dict[str, Any]]] = defaultdict(list)
    for link, food in dish_rows:
        dishes_by_merchant[link.merchant_id].append(
            {
                "food_id": str(food.id),
                "slug": food.slug,
                "name": dish_names.get(food.id, food.romanized_name),
                "local_name": food.local_name,
                "food_kind": food.food_kind,
                "meal_types": food.meal_types,
            }
        )
    cards: list[dict[str, Any]] = []
    for merchant in merchants:
        merchant_sources = sources_by_merchant.get(merchant.id, [])
        if not merchant_is_publishable(merchant, has_current_source=bool(merchant_sources)):
            continue
        profile = destination_for_id(merchant.destination_id)
        city_name = profile.city if profile else merchant.destination_id
        cards.append(
            {
                "id": str(merchant.id),
                "slug": merchant.slug,
                "name": merchant.name,
                "local_name": merchant.local_name,
                "destination_id": merchant.destination_id,
                "destination_name": city_name,
                "country_code": merchant.country_code,
                "area": areas_by_merchant.get(merchant.id),
                "categories": categories_by_merchant.get(merchant.id, []),
                "signature_dishes": dishes_by_merchant.get(merchant.id, []),
                "address": merchant.address,
                "latitude": float(merchant.latitude) if merchant.latitude is not None else None,
                "longitude": float(merchant.longitude) if merchant.longitude is not None else None,
                "coordinate_source": {
                    "type": merchant.coordinate_source_type,
                    "url": merchant.coordinate_source_url,
                    "verified_at": merchant.coordinate_verified_at.isoformat()
                    if merchant.coordinate_verified_at is not None
                    else None,
                },
                "official_website_url": merchant.official_website_url,
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
                "verified_at": merchant.verified_at.isoformat()
                if merchant.verified_at is not None
                else None,
                "sources": merchant_sources,
            }
        )
    return cards


async def _resolve_area(session: AsyncSession, area_slug: str) -> FoodArea:
    area = await session.scalar(
        select(FoodArea).where(FoodArea.slug == area_slug, FoodArea.is_active.is_(True))
    )
    if area is None:
        raise AppError(404, "food_area_not_found", "找不到這個區域")
    return area


async def _category_counts(
    session: AsyncSession, *, destination_id: str | None, area_id: UUID | None, unassigned: bool
) -> dict[UUID, int]:
    filters = list(publishable_merchant_filters())
    if destination_id:
        filters.append(FoodMerchant.destination_id == destination_id)
    if unassigned:
        filters.append(FoodMerchant.area_id.is_(None))
    elif area_id is not None:
        filters.append(FoodMerchant.area_id == area_id)
    rows = (
        await session.execute(
            select(FoodMerchantCategory.category_id, func.count(func.distinct(FoodMerchant.id)))
            .join(FoodMerchant, FoodMerchant.id == FoodMerchantCategory.merchant_id)
            .where(*filters)
            .group_by(FoodMerchantCategory.category_id)
        )
    ).all()
    return {category_id: int(count) for category_id, count in rows}


async def merchant_categories(
    session: AsyncSession,
    *,
    locale: str,
    destination_id: str | None = None,
    area_slug: str | None = None,
) -> dict[str, Any]:
    """Every active category with the number of publishable merchants in scope."""

    area_id: UUID | None = None
    if area_slug and area_slug != "other":
        area_id = (await _resolve_area(session, area_slug)).id
    counts = await _category_counts(
        session,
        destination_id=destination_id,
        area_id=area_id,
        unassigned=area_slug == "other",
    )
    categories = (
        await session.scalars(
            select(FoodCategory)
            .where(FoodCategory.is_active.is_(True))
            .order_by(FoodCategory.display_order, FoodCategory.slug)
        )
    ).all()
    return {
        "items": [
            {
                "slug": category.slug,
                "name": localized_name(category.names_json, locale),
                "merchant_count": counts.get(category.id, 0),
            }
            for category in categories
        ]
    }


async def _merchant_facets(
    session: AsyncSession, *, locale: str, destination_id: str
) -> dict[str, Any]:
    """Area and category counts for one city, independent of the other active filters."""

    area_rows = (
        await session.execute(
            select(FoodMerchant.area_id, func.count(FoodMerchant.id))
            .where(*publishable_merchant_filters(), FoodMerchant.destination_id == destination_id)
            .group_by(FoodMerchant.area_id)
        )
    ).all()
    area_counts = {area_id: int(count) for area_id, count in area_rows}
    areas = (
        await session.scalars(
            select(FoodArea)
            .where(FoodArea.destination_id == destination_id, FoodArea.is_active.is_(True))
            .order_by(FoodArea.display_order, FoodArea.slug)
        )
    ).all()
    return {
        "areas": [
            {**_area_ref(area, locale), "merchant_count": area_counts.get(area.id, 0)}
            for area in areas
        ],
        "unassigned_area_count": area_counts.get(None, 0),
        "categories": (
            await merchant_categories(session, locale=locale, destination_id=destination_id)
        )["items"],
    }


async def list_merchants(
    session: AsyncSession,
    *,
    locale: str,
    destination_id: str | None = None,
    area_slug: str | None = None,
    category_slug: str | None = None,
    q: str | None = None,
    cursor: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Publishable merchants filtered by city, area (``other`` = unassigned), category and text."""

    filters = list(publishable_merchant_filters())
    if destination_id:
        filters.append(FoodMerchant.destination_id == destination_id)
    if area_slug == "other":
        filters.append(FoodMerchant.area_id.is_(None))
    elif area_slug:
        filters.append(FoodMerchant.area_id == (await _resolve_area(session, area_slug)).id)
    if category_slug:
        filters.append(
            FoodMerchant.id.in_(
                select(FoodMerchantCategory.merchant_id)
                .join(FoodCategory, FoodCategory.id == FoodMerchantCategory.category_id)
                .where(FoodCategory.slug == category_slug, FoodCategory.is_active.is_(True))
            )
        )
    term = (q or "").strip()
    if term:
        pattern = f"%{escape_like(term)}%"
        dish_match = FoodMerchant.id.in_(
            select(FoodMerchantFood.merchant_id)
            .join(TravelFood, TravelFood.id == FoodMerchantFood.food_id)
            .where(TravelFood.search_text.ilike(pattern, escape="\\"))
        )
        filters.append(
            or_(
                FoodMerchant.name.ilike(pattern, escape="\\"),
                FoodMerchant.local_name.ilike(pattern, escape="\\"),
                FoodMerchant.slug.ilike(pattern, escape="\\"),
                FoodMerchant.address.ilike(pattern, escape="\\"),
                dish_match,
            )
        )
    total = int(await session.scalar(select(func.count(FoodMerchant.id)).where(*filters)) or 0)
    offset = _decode_cursor(cursor)
    merchants = list(
        (
            await session.scalars(
                select(FoodMerchant)
                .where(*filters)
                .order_by(
                    FoodMerchant.destination_id,
                    FoodMerchant.display_order,
                    FoodMerchant.name,
                    FoodMerchant.id,
                )
                .offset(offset)
                .limit(limit)
            )
        ).all()
    )
    if destination_id:
        facets = await _merchant_facets(session, locale=locale, destination_id=destination_id)
    else:
        facets = {
            "areas": [],
            "unassigned_area_count": 0,
            "categories": (await merchant_categories(session, locale=locale))["items"],
        }
    next_offset = offset + len(merchants)
    return {
        "total": total,
        "has_more": next_offset < total,
        "next_cursor": _encode_cursor(next_offset) if next_offset < total else None,
        "items": await _serialize_merchant_cards(session, merchants, locale),
        "facets": facets,
    }


async def merchant_cities(session: AsyncSession, *, locale: str) -> dict[str, Any]:
    """All supported destinations grouped by country, with publishable merchant counts."""

    merchant_counts = {
        destination_id: int(count)
        for destination_id, count in (
            await session.execute(
                select(FoodMerchant.destination_id, func.count(FoodMerchant.id))
                .where(*publishable_merchant_filters())
                .group_by(FoodMerchant.destination_id)
            )
        ).all()
    }
    area_counts = {
        destination_id: int(count)
        for destination_id, count in (
            await session.execute(
                select(FoodArea.destination_id, func.count(FoodArea.id))
                .where(FoodArea.is_active.is_(True))
                .group_by(FoodArea.destination_id)
            )
        ).all()
    }
    countries: dict[str, dict[str, Any]] = {}
    for profile in DESTINATIONS:
        item = _destination_item(profile.id)
        code = str(item["country_code"])
        country = countries.setdefault(
            code,
            {
                "code": code,
                "name": COUNTRY_NAMES[code].get(locale, COUNTRY_NAMES[code]["en"]),
                "merchant_count": 0,
                "cities": [],
            },
        )
        merchant_count = merchant_counts.get(profile.id, 0)
        country["merchant_count"] += merchant_count
        country["cities"].append(
            {
                **item,
                "merchant_count": merchant_count,
                "area_count": area_counts.get(profile.id, 0),
            }
        )
    ordered = sorted(countries.values(), key=lambda entry: -int(entry["merchant_count"]))
    for country in ordered:
        country["cities"].sort(key=lambda city: -int(city["merchant_count"]))
    return {"total_merchants": sum(merchant_counts.values()), "countries": ordered}
