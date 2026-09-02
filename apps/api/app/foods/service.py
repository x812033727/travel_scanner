from __future__ import annotations

import base64
import binascii
from collections import Counter, defaultdict
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.destinations.catalog import destination_for_id
from app.foods.catalog import COUNTRY_NAMES, FOOD_SEEDS
from app.foods.merchant_catalog import MERCHANT_DIRECT_SOURCE_SEEDS, MERCHANT_SEEDS
from app.hotspots.maps import build_map_links, has_exact_map_identity
from app.locations.coordinates import has_durable_coordinates
from app.models import (
    FoodDestination,
    FoodHotspot,
    FoodLocalization,
    FoodMerchant,
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
        limit=min(limit, max(1, days)),
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
