"""Catalog snapshots, strict publication gates and pending-only discovery imports."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from datetime import date, datetime
from decimal import Decimal
from typing import Any, cast
from urllib.parse import urlsplit
from uuid import UUID, uuid4

from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.catalog_review.evidence import normalize_source_url
from app.catalog_review.schemas import DiscoveryDraft
from app.destinations.catalog import destination_for_id
from app.foods.admin_router import FoodWritePayload
from app.foods.service import destination_country_code
from app.hotspots.maps import has_exact_map_identity
from app.i18n import LOCALES
from app.locations.coordinates import has_durable_coordinates
from app.models import (
    AdminAuditLog,
    CatalogReviewItem,
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
from app.restaurants.editorial import validate_editorial_url

Entity = TravelHotspot | TravelFood | FoodMerchant
ENTITY_TYPES: dict[str, type[TravelHotspot] | type[TravelFood] | type[FoodMerchant]] = {
    "hotspot": TravelHotspot,
    "food": TravelFood,
    "merchant": FoodMerchant,
}
CATEGORIES = frozenset(
    {"culture", "food", "nature", "beach", "family", "viewpoint", "shopping", "nightlife"}
)
TRUSTED_SOURCE_HOSTS = frozenset(
    {
        "www.wikidata.org",
        "wikidata.org",
        "en.wikipedia.org",
        "ja.wikipedia.org",
        "zh.wikipedia.org",
        "ko.wikipedia.org",
        "th.wikipedia.org",
        "vi.wikipedia.org",
        "www.japan.travel",
        "japan.travel",
        "www.gotokyo.org",
        "osaka-info.jp",
        "kyoto.travel",
        "www.welcome.city.yokohama.jp",
        "english.visitkorea.or.kr",
        "big5chinese.visitkorea.or.kr",
        "chinese.visitkorea.or.kr",
        "korean.visitkorea.or.kr",
        "www.visitbusan.net",
        "www.visitjeju.net",
        "www.taiwan.net.tw",
        "www.travel.taipei",
        "eng.taiwan.net.tw",
        "travel.taichung.gov.tw",
        "khh.travel",
        "www.twtainan.net",
        "www.visitsingapore.com",
        "www.discoverhongkong.com",
        "vietnam.travel",
        "www.tourismthailand.org",
    }
)


def json_value(value: Any) -> Any:
    if isinstance(value, (UUID, datetime, date, Decimal)):
        return str(value)
    if isinstance(value, dict):
        return {str(key): json_value(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_value(item) for item in value]
    return value


def row_data(row: Any) -> dict[str, Any]:
    return {
        field.key: json_value(getattr(row, field.key)) for field in inspect(type(row)).column_attrs
    }


def fingerprint(data: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            json_value(data), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()


def normalized_name(value: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFKC", value).casefold() if char.isalnum()
    )


async def load_entity(
    session: AsyncSession, kind: str, entity_id: UUID, *, lock: bool = False
) -> Entity | None:
    model = ENTITY_TYPES[kind]
    statement = select(model).where(model.id == entity_id)
    if lock:
        statement = statement.with_for_update()
    return cast(Entity | None, await session.scalar(statement))


async def entity_snapshot(session: AsyncSession, row: Entity) -> dict[str, Any]:
    data = row_data(row)
    if isinstance(row, TravelHotspot):
        data["localizations"] = [
            row_data(item)
            for item in (
                await session.scalars(
                    select(HotspotLocalization)
                    .where(HotspotLocalization.hotspot_id == row.id)
                    .order_by(HotspotLocalization.locale)
                )
            ).all()
        ]
    if isinstance(row, TravelFood):
        data["localizations"] = [
            row_data(item)
            for item in (
                await session.scalars(
                    select(FoodLocalization)
                    .where(FoodLocalization.food_id == row.id)
                    .order_by(FoodLocalization.locale)
                )
            ).all()
        ]
        data["destinations"] = [
            row_data(item)
            for item in (
                await session.scalars(
                    select(FoodDestination)
                    .where(FoodDestination.food_id == row.id)
                    .order_by(FoodDestination.destination_id)
                )
            ).all()
        ]
        data["hotspots"] = [
            row_data(item)
            for item in (
                await session.scalars(
                    select(FoodHotspot)
                    .where(FoodHotspot.food_id == row.id)
                    .order_by(FoodHotspot.id)
                )
            ).all()
        ]
    if isinstance(row, FoodMerchant):
        for name, model in (
            ("sources", FoodMerchantSource),
            ("foods", FoodMerchantFood),
            ("categories", FoodMerchantCategory),
        ):
            data[name] = [
                row_data(item)
                for item in (
                    await session.scalars(
                        select(model).where(model.merchant_id == row.id).order_by(model.id)
                    )
                ).all()
            ]
        # AI discovery URLs are historical references, not verified source claims.
        # The immutable import audit is their durable home: FoodMerchantSource has
        # no unverified source type and requires a last_verified_at timestamp.
        imported = await session.scalar(
            select(AdminAuditLog.metadata_json)
            .where(
                AdminAuditLog.action == "catalog_candidate_imported",
                AdminAuditLog.target == f"merchant:{row.id}",
            )
            .order_by(AdminAuditLog.created_at, AdminAuditLog.id)
            .limit(1)
        )
        if isinstance(imported, dict):
            references = imported.get("source_urls")
            if isinstance(references, list):
                data["discovery_reference_urls"] = list(
                    dict.fromkeys(
                        normalized
                        for url in references
                        if isinstance(url, str)
                        and (normalized := normalize_source_url(url)) is not None
                    )
                )[:5]
    return data


def source_urls(data: dict[str, Any]) -> list[str]:
    urls = list(data.get("source_urls") or [])
    urls.extend(data.get("discovery_reference_urls") or [])
    urls.extend(
        source["source_url"]
        for source in data.get("sources", [])
        if source.get("is_current")
        and isinstance(source.get("source_url"), str)
        and source.get("source_type") != "michelin_licensed"
    )
    for field in ("coordinate_source_url", "official_website_url"):
        if data.get(field):
            urls.append(data[field])
    qid = data.get("wikidata_item_id")
    if isinstance(qid, str) and re.fullmatch(r"Q[1-9][0-9]*", qid):
        urls.insert(0, f"https://www.wikidata.org/wiki/{qid}")
    return list(dict.fromkeys(url for url in urls if isinstance(url, str)))[:5]


def publication_gaps(kind: str, data: dict[str, Any]) -> list[str]:
    gaps = []
    if not source_urls(data):
        gaps.append("missing_source")
    if kind == "food":
        localizations = data.get("localizations", [])
        if {entry.get("locale") for entry in localizations} != set(LOCALES) or any(
            not entry.get("name") or not entry.get("summary") for entry in localizations
        ):
            gaps.append("missing_five_locale_content")
        destinations = data.get("destinations", [])
        if not destinations or any(
            not destination_for_id(entry.get("destination_id", "")) for entry in destinations
        ):
            gaps.append("missing_destination")
        if not data.get("meal_types"):
            gaps.append("missing_meal_type")
        return gaps
    if not destination_for_id(data.get("destination_id", "")):
        gaps.append("missing_destination")
    if kind == "hotspot" and not data.get("wikidata_item_id"):
        gaps.append("missing_wikidata_identity")
    if not has_exact_map_identity(
        data.get("country_code", ""), data.get("google_place_id"), data.get("naver_map_url")
    ):
        gaps.append("missing_exact_map_identity")
    stamp = data.get("map_verified_at") if kind == "hotspot" else data.get("verified_at")
    if data.get("map_match_status") != "verified" or not stamp:
        gaps.append("map_not_independently_verified")
    if not has_durable_coordinates(
        data.get("latitude"),
        data.get("longitude"),
        data.get("coordinate_source_type"),
        data.get("coordinate_source_url"),
    ):
        gaps.append("missing_durable_coordinates")
    if not data.get("coordinate_verified_at"):
        gaps.append("coordinates_not_verified")
    if kind == "merchant":
        if not any(
            source.get("is_current")
            and source.get("source_scope") in {"merchant_listing", "merchant_website"}
            and "display_name" in source.get("claims_json", [])
            for source in data.get("sources", [])
        ):
            gaps.append("missing_direct_merchant_source")
        if not data.get("categories"):
            gaps.append("missing_food_category")
    return gaps


async def make_review_item(
    session: AsyncSession, run_id: UUID, kind: str, row: Entity, phase: str
) -> CatalogReviewItem:
    data = await entity_snapshot(session, row)
    name = row.local_name if isinstance(row, TravelFood) else row.name
    destination = None if isinstance(row, TravelFood) else row.destination_id
    item = CatalogReviewItem(
        id=uuid4(),
        run_id=run_id,
        kind=kind,
        entity_id=row.id,
        name=name,
        destination_id=destination,
        phase=phase,
        snapshot_hash=fingerprint(data),
        snapshot_json=data,
        status="pending",
        gaps_json=publication_gaps(kind, data),
    )
    session.add(item)
    return item


async def trusted_hosts(session: AsyncSession) -> set[str]:
    hosts = set(TRUSTED_SOURCE_HOSTS)
    # Only a previously verified, published merchant may extend the allowlist with
    # its own official website. An AI-proposed URL never vouches for itself.
    urls = (
        await session.scalars(
            select(FoodMerchant.official_website_url).where(
                FoodMerchant.review_status == "approved",
                FoodMerchant.is_active.is_(True),
                FoodMerchant.map_match_status == "verified",
                FoodMerchant.official_website_verified_at.is_not(None),
            )
        )
    ).all()
    for url in urls:
        if url and url.startswith("https://") and urlsplit(url).hostname:
            hosts.add(cast(str, urlsplit(url).hostname))
    return hosts


async def duplicate_draft(session: AsyncSession, draft: DiscoveryDraft) -> bool:
    model = ENTITY_TYPES[draft.kind]
    if await session.scalar(select(model.id).where(model.slug == draft.slug)):
        return True
    # Includes rejected and disabled tombstones. Never resurrect by proposing a new slug.
    profile = destination_for_id(draft.destination_id)
    if profile is None:
        return True
    if draft.kind == "food":
        food_rows = (
            await session.scalars(
                select(TravelFood).where(
                    TravelFood.country_code == destination_country_code(profile.id)
                )
            )
        ).all()
        existing = {
            normalized_name(value)
            for row in food_rows
            for value in (row.local_name, row.romanized_name)
        }
        translated = (
            await session.scalars(
                select(FoodLocalization.name).where(
                    FoodLocalization.food_id.in_([row.id for row in food_rows])
                )
            )
        ).all()
        existing.update(normalized_name(name) for name in translated)
    else:
        entity_model = TravelHotspot if draft.kind == "hotspot" else FoodMerchant
        place_rows = cast(
            list[TravelHotspot | FoodMerchant],
            list(
                (
                    await session.scalars(
                        select(entity_model).where(entity_model.destination_id == profile.id)
                    )
                ).all()
            ),
        )
        existing = {normalized_name(row.name) for row in place_rows}
        if draft.kind == "merchant":
            existing.update(
                normalized_name(cast(FoodMerchant, row).local_name) for row in place_rows
            )
            for merchant in place_rows:
                existing.update(
                    normalized_name(value)
                    for value in (cast(FoodMerchant, merchant).names_json or {}).values()
                )
        else:
            for hotspot in place_rows:
                metadata = cast(TravelHotspot, hotspot).metadata_json or {}
                aliases = [metadata.get("local_name", ""), *metadata.get("aliases", [])]
                existing.update(
                    normalized_name(value) for value in aliases if isinstance(value, str)
                )
            hotspot_translations = (
                await session.scalars(
                    select(HotspotLocalization).where(
                        HotspotLocalization.hotspot_id.in_([row.id for row in place_rows])
                    )
                )
            ).all()
            existing.update(
                normalized_name(value)
                for localization in hotspot_translations
                for value in [localization.name, *(localization.aliases or [])]
                if isinstance(value, str)
            )
            for url in draft.source_urls:
                parts = urlsplit(url)
                qid = parts.path.removeprefix("/wiki/")
                if (
                    parts.hostname in {"www.wikidata.org", "wikidata.org"}
                    and re.fullmatch(r"Q[1-9][0-9]*", qid)
                    and await session.scalar(
                        select(TravelHotspot.id).where(TravelHotspot.wikidata_item_id == qid)
                    )
                ):
                    return True
    return bool(
        {normalized_name(draft.name), normalized_name(draft.local_name)} & (existing - {""})
    )


def _relation_slugs(data: dict[str, Any], field: str, maximum: int) -> list[str]:
    values = data.get(field, [])
    if (
        not isinstance(values, list)
        or len(values) > maximum
        or any(
            not isinstance(value, str)
            or len(value) > 128
            or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value)
            for value in values
        )
    ):
        raise AppError(422, "catalog_relation_invalid", "探索候選的料理或分類 slug 格式不合法")
    return list(dict.fromkeys(values))


async def _merchant_draft_relations(
    session: AsyncSession,
    draft: DiscoveryDraft,
) -> tuple[list[FoodCategory], list[TravelFood]]:
    category_slugs = _relation_slugs(draft.data, "category_slugs", 6)
    food_slugs = _relation_slugs(draft.data, "food_slugs", 70)
    categories = (
        {
            row.slug: row
            for row in (
                await session.scalars(
                    select(FoodCategory)
                    .where(
                        FoodCategory.slug.in_(category_slugs),
                        FoodCategory.is_active.is_(True),
                    )
                    .with_for_update()
                )
            ).all()
        }
        if category_slugs
        else {}
    )
    if any(slug not in categories for slug in category_slugs):
        raise AppError(422, "catalog_relation_invalid", "探索候選使用了不存在或已停用的美食分類")
    foods = (
        {
            row.slug: row
            for row in (
                await session.scalars(
                    select(TravelFood)
                    .join(FoodDestination, FoodDestination.food_id == TravelFood.id)
                    .where(
                        TravelFood.slug.in_(food_slugs),
                        TravelFood.review_status == "approved",
                        TravelFood.is_active.is_(True),
                        TravelFood.country_code == destination_country_code(draft.destination_id),
                        FoodDestination.destination_id == draft.destination_id,
                    )
                    .with_for_update()
                )
            ).all()
        }
        if food_slugs
        else {}
    )
    if any(slug not in foods for slug in food_slugs):
        raise AppError(
            422, "catalog_relation_invalid", "探索候選的料理必須已核准、啟用且屬於相同目的地"
        )
    return [categories[slug] for slug in category_slugs], [foods[slug] for slug in food_slugs]


async def import_draft(
    session: AsyncSession, draft: DiscoveryDraft, actor_id: UUID, run_id: UUID
) -> Entity | None:
    """Create an unverified candidate, never trust generated POI identifiers/coordinates."""
    profile = destination_for_id(draft.destination_id)
    if profile is None or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", draft.slug):
        raise AppError(422, "invalid_catalog_draft", "探索候選的目的地或 slug 不合法")
    if not draft.source_urls:
        raise AppError(422, "catalog_source_required", "探索候選缺少可追溯來源")
    for url in draft.source_urls:
        validate_editorial_url(url)
    reference_urls = list(draft.source_urls)
    if draft.kind == "merchant":
        normalized = [normalize_source_url(url) for url in reference_urls]
        if any(url is None for url in normalized):
            raise AppError(422, "catalog_source_invalid", "探索候選來源網址不支援或格式不合法")
        reference_urls = list(dict.fromkeys(cast(list[str], normalized)))
    if await duplicate_draft(session, draft):
        return None
    country = destination_country_code(profile.id)
    row: Entity
    if draft.kind == "food":
        payload = FoodWritePayload.model_validate(
            {
                **draft.data,
                "slug": draft.slug,
                "local_name": draft.local_name,
                "country_code": country,
                "destination_ids": [profile.id],
                "source_urls": draft.source_urls,
                "review_status": "pending",
                "is_active": False,
            }
        )
        row = TravelFood(
            id=uuid4(),
            slug=draft.slug,
            country_code=country,
            local_name=payload.local_name,
            romanized_name=payload.romanized_name,
            food_kind=payload.food_kind,
            meal_types=payload.meal_types,
            ingredient_tags=payload.ingredient_tags,
            dietary_notes=payload.dietary_notes,
            search_text=f"{draft.name} {draft.local_name}",
            source_urls=draft.source_urls,
            review_status="pending",
            is_active=False,
            source="admin",
        )
        session.add(row)
        await session.flush()
        for entry in payload.localizations:
            session.add(
                FoodLocalization(
                    food_id=row.id,
                    locale=entry.locale,
                    name=entry.name,
                    summary=entry.summary,
                    source="admin",
                )
            )
        session.add(FoodDestination(food_id=row.id, destination_id=profile.id))
    elif draft.kind == "hotspot":
        category = str(draft.data.get("category", ""))
        if category not in CATEGORIES:
            raise AppError(422, "invalid_catalog_category", "探索景點分類不合法")
        row = TravelHotspot(
            id=uuid4(),
            slug=draft.slug,
            name=draft.name,
            city_code=profile.code,
            destination_id=profile.id,
            city_name=profile.city,
            country_code=country,
            country_name=profile.country_label,
            category=category,
            search_text=f"{draft.name} {draft.local_name} {profile.city}",
            source_urls=draft.source_urls,
            review_status="pending",
            is_active=False,
            origin="gemini_candidate",
            map_match_status="unverified",
            metadata_json={
                "local_name": draft.local_name,
                "catalog_review_run_id": str(run_id),
                "discovery_data": draft.data,
            },
        )
        session.add(row)
    else:
        categories, foods = await _merchant_draft_relations(session, draft)
        row = FoodMerchant(
            id=uuid4(),
            slug=draft.slug,
            name=draft.name,
            local_name=draft.local_name,
            destination_id=profile.id,
            country_code=country,
            review_status="pending",
            is_active=False,
            map_match_status="unverified",
        )
        session.add(row)
        await session.flush()
        for order, merchant_category in enumerate(categories):
            session.add(
                FoodMerchantCategory(
                    merchant_id=row.id,
                    category_id=merchant_category.id,
                    is_primary=order == 0,
                    display_order=order,
                    source="gemini",
                )
            )
        for order, food in enumerate(foods):
            session.add(
                FoodMerchantFood(
                    merchant_id=row.id,
                    food_id=food.id,
                    is_primary=order == 0,
                    display_order=order,
                )
            )
    await session.flush()
    session.add(
        AdminAuditLog(
            actor_user_id=actor_id,
            action="catalog_candidate_imported",
            target=f"{draft.kind}:{row.id}",
            metadata_json={
                "run_id": str(run_id),
                "source_urls": reference_urls,
                "review_status": "pending",
                "is_active": False,
            },
        )
    )
    # make_review_item immediately snapshots the import audit in the same transaction.
    await session.flush()
    return row
