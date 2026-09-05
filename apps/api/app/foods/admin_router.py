from __future__ import annotations

import re
from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field, model_validator
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.listing import (
    COUNTRY_ORDER,
    FOOD_KIND_ORDER,
    country_name_for,
    country_rank,
    ranked,
)
from app.admin.service import load_runtime_settings
from app.auth.service import AdminUser
from app.db import escape_like, get_session
from app.destinations.catalog import destination_for_id
from app.foods.category_catalog import categories_for_dishes
from app.foods.coordinate_queue import (
    apply_approval,
    coordinate_queue_statement,
    queue_total,
    resolve_queue_page,
)
from app.foods.service import destination_country_code, localized_name
from app.hotspots.maps import has_exact_map_identity
from app.i18n import DEFAULT_LOCALE, LOCALES, Locale, current_locale
from app.infra import get_redis
from app.locations.coordinates import (
    has_durable_coordinates,
    is_durable_coordinate_source,
    valid_coordinate_pair,
)
from app.locations.google_match import preview_google_place_match
from app.models import (
    AdminAuditLog,
    FoodArea,
    FoodCategory,
    FoodDestination,
    FoodHotspot,
    FoodLocalization,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantFood,
    FoodMerchantSource,
    TravelFood,
    TravelHotspot,
)
from app.places.google import GoogleTravelService
from app.problems import AppError
from app.restaurants.editorial import validate_editorial_url

router = APIRouter(prefix="/admin/foods", tags=["admin foods"])
Session = Annotated[AsyncSession, Depends(get_session)]
RequestLocale = Annotated[Locale, Depends(current_locale)]
FoodKind = Literal["main", "noodle_soup", "street_food", "dessert", "drink"]
ReviewStatus = Literal["pending", "approved", "rejected", "disabled"]
MapMatchStatus = Literal["unverified", "verified", "ambiguous", "disabled"]
MerchantSourceType = Literal["official_tourism", "merchant_official", "michelin_licensed"]
MerchantSourceScope = Literal[
    "destination_context", "merchant_listing", "merchant_website", "coordinates"
]
MichelinDistinction = Literal[
    "three_star", "two_star", "one_star", "green_star", "bib_gourmand", "selected"
]


class FoodLocalizationPayload(BaseModel):
    locale: Locale
    name: str = Field(min_length=1, max_length=255)
    summary: str = Field(min_length=1, max_length=2000)


class FoodWritePayload(BaseModel):
    slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=128)
    country_code: str = Field(min_length=2, max_length=2)
    local_name: str = Field(min_length=1, max_length=255)
    romanized_name: str = Field(min_length=1, max_length=255)
    food_kind: FoodKind
    meal_types: list[str] = Field(min_length=1, max_length=5)
    ingredient_tags: list[str] = Field(default_factory=list, max_length=20)
    dietary_notes: list[str] = Field(default_factory=list, max_length=20)
    source_urls: list[str] = Field(min_length=1, max_length=10)
    review_status: ReviewStatus = "pending"
    is_active: bool = True
    display_order: int = Field(default=100, ge=0, le=10_000)
    localizations: list[FoodLocalizationPayload] = Field(min_length=5, max_length=5)
    destination_ids: list[str] = Field(min_length=1, max_length=31)
    hotspot_ids: list[UUID] = Field(default_factory=list, max_length=50)

    @model_validator(mode="after")
    def validate_locales(self) -> FoodWritePayload:
        locales = [item.locale for item in self.localizations]
        if set(locales) != set(LOCALES) or len(locales) != len(set(locales)):
            raise ValueError("美食內容必須包含且僅包含五種網站語系")
        return self

    @model_validator(mode="after")
    def validate_source_urls(self) -> FoodWritePayload:
        # Rendered as public links on the dish cards; hold them to the same
        # public-HTTPS bar as the restaurant editorial sources.
        for url in self.source_urls:
            validate_editorial_url(url)
        return self


class FoodUpdatePayload(BaseModel):
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    local_name: str | None = Field(default=None, min_length=1, max_length=255)
    romanized_name: str | None = Field(default=None, min_length=1, max_length=255)
    food_kind: FoodKind | None = None
    meal_types: list[str] | None = Field(default=None, min_length=1, max_length=5)
    ingredient_tags: list[str] | None = Field(default=None, max_length=20)
    dietary_notes: list[str] | None = Field(default=None, max_length=20)
    source_urls: list[str] | None = Field(default=None, min_length=1, max_length=10)
    review_status: ReviewStatus | None = None
    is_active: bool | None = None
    display_order: int | None = Field(default=None, ge=0, le=10_000)
    localizations: list[FoodLocalizationPayload] | None = Field(default=None, max_length=5)
    destination_ids: list[str] | None = Field(default=None, min_length=1, max_length=31)
    hotspot_ids: list[UUID] | None = Field(default=None, max_length=50)

    @model_validator(mode="after")
    def validate_source_urls(self) -> FoodUpdatePayload:
        for url in self.source_urls or []:
            validate_editorial_url(url)
        return self


class FoodBatchPayload(BaseModel):
    ids: list[UUID] = Field(min_length=1, max_length=100)
    action: Literal["approve", "reject", "disable", "activate"]
    reason: str | None = Field(default=None, max_length=500)


class FoodMerchantSourcePayload(BaseModel):
    source_type: MerchantSourceType
    source_scope: MerchantSourceScope = "destination_context"
    source_title: str = Field(min_length=1, max_length=255)
    source_url: str = Field(pattern=r"^https://", max_length=2048)
    claims: list[Literal["display_name", "address", "official_website", "coordinates"]] = Field(
        default_factory=list, max_length=4
    )
    edition_year: int | None = Field(default=None, ge=1900, le=2100)
    distinction: MichelinDistinction | None = None
    is_current: bool = True

    @model_validator(mode="after")
    def validate_michelin_fields(self) -> FoodMerchantSourcePayload:
        validate_editorial_url(self.source_url)
        if self.source_type != "michelin_licensed" and (
            self.edition_year is not None or self.distinction is not None
        ):
            raise ValueError("只有取得授權的米其林來源可設定年度與級別")
        if self.source_type == "michelin_licensed" and (
            self.edition_year is None or self.distinction is None
        ):
            raise ValueError("米其林授權來源必須同時填寫年度與級別")
        if self.source_scope == "destination_context" and self.claims:
            raise ValueError("目的地背景來源不可佐證特定店家欄位")
        return self


class FoodMerchantWritePayload(BaseModel):
    slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=128)
    destination_id: str = Field(min_length=2, max_length=64)
    country_code: str = Field(min_length=2, max_length=2)
    name: str = Field(min_length=1, max_length=255)
    local_name: str = Field(min_length=1, max_length=255)
    address: str | None = Field(default=None, max_length=1000)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    coordinate_source_type: (
        Literal["curated", "wikidata", "official_tourism", "merchant_official", "admin_verified"]
        | None
    ) = None
    coordinate_source_url: str | None = Field(default=None, max_length=2048)
    google_place_id: str | None = Field(default=None, max_length=255)
    naver_map_url: str | None = Field(
        default=None, pattern=r"^https://map\.naver\.com/", max_length=2048
    )
    official_website_url: str | None = Field(default=None, max_length=2048)
    map_match_status: MapMatchStatus = "unverified"
    review_status: ReviewStatus = "pending"
    is_active: bool = True
    display_order: int = Field(default=100, ge=0, le=10_000)
    food_ids: list[UUID] = Field(default_factory=list, max_length=70)
    sources: list[FoodMerchantSourcePayload] = Field(min_length=1, max_length=20)
    area_slug: str | None = Field(default=None, min_length=2, max_length=128)
    category_slugs: list[str] = Field(default_factory=list, max_length=6)

    @model_validator(mode="after")
    def validate_location_fields(self) -> FoodMerchantWritePayload:
        _validate_category_slugs(self.category_slugs)
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("緯度與經度必須同時提供")
        if self.coordinate_source_url and not self.coordinate_source_url.startswith("https://"):
            raise ValueError("座標來源必須是 HTTPS 網址")
        if self.official_website_url:
            validate_editorial_url(self.official_website_url)
            if not any(
                source.source_scope == "merchant_website" and "official_website" in source.claims
                for source in self.sources
            ):
                raise ValueError("店家官網必須附上 merchant_website 來源佐證")
        return self


class FoodMerchantUpdatePayload(BaseModel):
    destination_id: str | None = Field(default=None, min_length=2, max_length=64)
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    local_name: str | None = Field(default=None, min_length=1, max_length=255)
    address: str | None = Field(default=None, max_length=1000)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    coordinate_source_type: (
        Literal["curated", "wikidata", "official_tourism", "merchant_official", "admin_verified"]
        | None
    ) = None
    coordinate_source_url: str | None = Field(default=None, max_length=2048)
    google_place_id: str | None = Field(default=None, max_length=255)
    naver_map_url: str | None = Field(
        default=None, pattern=r"^https://map\.naver\.com/", max_length=2048
    )
    official_website_url: str | None = Field(default=None, max_length=2048)
    map_match_status: MapMatchStatus | None = None
    review_status: ReviewStatus | None = None
    is_active: bool | None = None
    display_order: int | None = Field(default=None, ge=0, le=10_000)
    food_ids: list[UUID] | None = Field(default=None, max_length=70)
    sources: list[FoodMerchantSourcePayload] | None = Field(
        default=None, min_length=1, max_length=20
    )
    area_slug: str | None = Field(default=None, min_length=2, max_length=128)
    category_slugs: list[str] | None = Field(default=None, max_length=6)

    @model_validator(mode="after")
    def validate_source_url(self) -> FoodMerchantUpdatePayload:
        if self.category_slugs is not None:
            _validate_category_slugs(self.category_slugs)
        if self.coordinate_source_url and not self.coordinate_source_url.startswith("https://"):
            raise ValueError("座標來源必須是 HTTPS 網址")
        if self.official_website_url:
            validate_editorial_url(self.official_website_url)
            if not self.sources or not any(
                source.source_scope == "merchant_website" and "official_website" in source.claims
                for source in self.sources
            ):
                raise ValueError("更新店家官網時必須一併提供 merchant_website 來源佐證")
        return self


class FoodMerchantBatchPayload(BaseModel):
    ids: list[UUID] = Field(min_length=1, max_length=100)
    action: Literal[
        "approve",
        "reject",
        "disable",
        "activate",
        "verify",
        "verify_activate",
        "ambiguous",
    ]
    reason: str | None = Field(default=None, max_length=500)


class GoogleMapCandidateRequest(BaseModel):
    query: str = Field(min_length=2, max_length=255)
    country_code: str = Field(min_length=2, max_length=2)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @model_validator(mode="after")
    def validate_coordinate_pair(self) -> GoogleMapCandidateRequest:
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("緯度與經度必須同時提供")
        return self


SLUG_FIELD_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
TaxonomyStatus = Literal["active", "disabled"]
MerchantTaxonomyFilter = Literal["missing_area", "missing_category"]


def _validate_names(names: dict[str, str]) -> dict[str, str]:
    cleaned = {locale: value.strip() for locale, value in names.items()}
    if set(cleaned) != set(LOCALES):
        raise ValueError("名稱必須包含且僅包含五種網站語系")
    if any(not value or len(value) > 255 for value in cleaned.values()):
        raise ValueError("每個語系的名稱都必須填寫且不超過 255 字")
    return cleaned


def _validate_category_slugs(slugs: list[str]) -> None:
    if len(set(slugs)) != len(slugs):
        raise ValueError("美食分類不可重複")
    if any(not re.match(SLUG_FIELD_PATTERN, slug) for slug in slugs):
        raise ValueError("美食分類 slug 格式不正確")


class FoodAreaWritePayload(BaseModel):
    slug: str = Field(pattern=SLUG_FIELD_PATTERN, max_length=128)
    destination_id: str = Field(min_length=2, max_length=64)
    names: dict[str, str]
    match_terms: list[str] = Field(default_factory=list, max_length=20)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    is_active: bool = True
    display_order: int = Field(default=100, ge=0, le=10_000)

    @model_validator(mode="after")
    def validate_fields(self) -> FoodAreaWritePayload:
        self.names = _validate_names(self.names)
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("緯度與經度必須同時提供")
        return self


class FoodAreaUpdatePayload(BaseModel):
    destination_id: str | None = Field(default=None, min_length=2, max_length=64)
    names: dict[str, str] | None = None
    match_terms: list[str] | None = Field(default=None, max_length=20)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    is_active: bool | None = None
    display_order: int | None = Field(default=None, ge=0, le=10_000)

    @model_validator(mode="after")
    def validate_fields(self) -> FoodAreaUpdatePayload:
        if self.names is not None:
            self.names = _validate_names(self.names)
        return self


class FoodCategoryWritePayload(BaseModel):
    slug: str = Field(pattern=SLUG_FIELD_PATTERN, max_length=128)
    names: dict[str, str]
    is_active: bool = True
    display_order: int = Field(default=100, ge=0, le=10_000)

    @model_validator(mode="after")
    def validate_fields(self) -> FoodCategoryWritePayload:
        self.names = _validate_names(self.names)
        return self


class FoodCategoryUpdatePayload(BaseModel):
    names: dict[str, str] | None = None
    is_active: bool | None = None
    display_order: int | None = Field(default=None, ge=0, le=10_000)

    @model_validator(mode="after")
    def validate_fields(self) -> FoodCategoryUpdatePayload:
        if self.names is not None:
            self.names = _validate_names(self.names)
        return self


class TaxonomyBatchPayload(BaseModel):
    ids: list[UUID] = Field(min_length=1, max_length=100)
    action: Literal["activate", "deactivate"]
    reason: str | None = Field(default=None, max_length=500)


def build_food_search_text(
    slug: str,
    country_code: str,
    local_name: str,
    romanized_name: str,
    localized_names: list[str],
    ingredient_tags: list[str],
) -> str:
    """Mirror ``FoodSeed.search_text`` so admin edits stay searchable in every locale."""

    parts = [slug, country_code, local_name, romanized_name, *localized_names, *ingredient_tags]
    return " ".join(part for part in parts if part).casefold()


async def _derived_category_slugs(session: AsyncSession, food_ids: list[UUID]) -> list[str]:
    if not food_ids:
        return []
    slugs = tuple(
        (await session.scalars(select(TravelFood.slug).where(TravelFood.id.in_(food_ids)))).all()
    )
    return list(categories_for_dishes(slugs))


async def _validate_merchant_taxonomy(
    session: AsyncSession,
    *,
    destination_id: str,
    area_slug: str | None,
    category_slugs: list[str],
) -> tuple[FoodArea | None, list[FoodCategory]]:
    area: FoodArea | None = None
    if area_slug:
        area = await session.scalar(select(FoodArea).where(FoodArea.slug == area_slug))
        if area is None:
            raise AppError(404, "food_area_not_found", "找不到這個區域")
        if not area.is_active:
            raise AppError(422, "food_area_inactive", "這個區域已停用")
        if area.destination_id != destination_id.casefold():
            raise AppError(
                422, "merchant_area_destination_mismatch", "區域必須屬於店家所在的目的地"
            )
    categories: list[FoodCategory] = []
    if category_slugs:
        rows = {
            row.slug: row
            for row in (
                await session.scalars(
                    select(FoodCategory).where(FoodCategory.slug.in_(category_slugs))
                )
            ).all()
        }
        if any(slug not in rows for slug in category_slugs):
            raise AppError(404, "food_category_not_found", "部分美食分類不存在")
        if any(not rows[slug].is_active for slug in category_slugs):
            raise AppError(422, "food_category_inactive", "部分美食分類已停用")
        categories = [rows[slug] for slug in category_slugs]
    return area, categories


def _require_merchant_categories(count: int) -> None:
    if count <= 0:
        raise AppError(422, "merchant_category_required", "發布前必須至少指定一個美食分類")


async def _replace_merchant_categories(
    session: AsyncSession,
    merchant: FoodMerchant,
    categories: list[FoodCategory],
    *,
    source: str,
) -> None:
    rows = list(
        (
            await session.scalars(
                select(FoodMerchantCategory).where(FoodMerchantCategory.merchant_id == merchant.id)
            )
        ).all()
    )
    for row in rows:
        await session.delete(row)
    await session.flush()
    for order, category in enumerate(categories, start=1):
        session.add(
            FoodMerchantCategory(
                merchant_id=merchant.id,
                category_id=category.id,
                is_primary=order == 1,
                display_order=order,
                source=source,
            )
        )


async def _ensure_merchant_categories(
    session: AsyncSession, merchant: FoodMerchant, category_counts: dict[UUID, int]
) -> None:
    """Publishing requires a category; derive one from the linked dishes when none is set."""

    if category_counts.get(merchant.id, 0) > 0:
        return
    food_ids = list(
        (
            await session.scalars(
                select(FoodMerchantFood.food_id).where(FoodMerchantFood.merchant_id == merchant.id)
            )
        ).all()
    )
    _, categories = await _validate_merchant_taxonomy(
        session,
        destination_id=merchant.destination_id,
        area_slug=None,
        category_slugs=await _derived_category_slugs(session, food_ids),
    )
    _require_merchant_categories(len(categories))
    await _replace_merchant_categories(session, merchant, categories, source="seed")
    category_counts[merchant.id] = len(categories)


def _area_admin_item(area: FoodArea, merchant_count: int = 0) -> dict[str, object]:
    profile = destination_for_id(area.destination_id)
    return {
        "id": str(area.id),
        "slug": area.slug,
        "destination_id": area.destination_id,
        "destination_name": profile.city if profile else area.destination_id,
        "country_code": area.country_code,
        "name": localized_name(area.names_json, "zh-TW"),
        "names": area.names_json,
        "match_terms": area.match_terms_json,
        "latitude": float(area.latitude) if area.latitude is not None else None,
        "longitude": float(area.longitude) if area.longitude is not None else None,
        "is_active": area.is_active,
        "display_order": area.display_order,
        "source": area.source,
        "merchant_count": merchant_count,
        "updated_at": area.updated_at,
    }


def _category_admin_item(category: FoodCategory, merchant_count: int = 0) -> dict[str, object]:
    return {
        "id": str(category.id),
        "slug": category.slug,
        "name": localized_name(category.names_json, "zh-TW"),
        "names": category.names_json,
        "is_active": category.is_active,
        "display_order": category.display_order,
        "source": category.source,
        "merchant_count": merchant_count,
        "updated_at": category.updated_at,
    }


async def _validate_relations(
    session: AsyncSession, destination_ids: list[str], hotspot_ids: list[UUID]
) -> None:
    if any(destination_for_id(item) is None for item in destination_ids):
        raise AppError(422, "unsupported_destination", "目的地關聯包含不支援的項目")
    if not hotspot_ids:
        return
    rows = list(
        (
            await session.scalars(select(TravelHotspot).where(TravelHotspot.id.in_(hotspot_ids)))
        ).all()
    )
    if len(rows) != len(set(hotspot_ids)):
        raise AppError(404, "food_hotspot_not_found", "部分美食景點不存在")
    if any(
        row.category != "food"
        or row.review_status not in ("approved", "auto_approved")
        or not row.is_active
        for row in rows
    ):
        raise AppError(422, "invalid_food_hotspot", "只能關聯已核准且啟用的美食景點")


async def _replace_relations(
    session: AsyncSession,
    food: TravelFood,
    destination_ids: list[str] | None,
    hotspot_ids: list[UUID] | None,
) -> None:
    if destination_ids is not None:
        destination_relations = list(
            (
                await session.scalars(
                    select(FoodDestination).where(FoodDestination.food_id == food.id)
                )
            ).all()
        )
        for destination_relation in destination_relations:
            await session.delete(destination_relation)
        await session.flush()
        for order, destination_id in enumerate(destination_ids, start=1):
            session.add(
                FoodDestination(
                    food_id=food.id,
                    destination_id=destination_id.casefold(),
                    display_order=order,
                )
            )
    if hotspot_ids is not None:
        hotspot_relations = list(
            (await session.scalars(select(FoodHotspot).where(FoodHotspot.food_id == food.id))).all()
        )
        for hotspot_relation in hotspot_relations:
            await session.delete(hotspot_relation)
        await session.flush()
        for order, hotspot_id in enumerate(hotspot_ids, start=1):
            session.add(FoodHotspot(food_id=food.id, hotspot_id=hotspot_id, display_order=order))


async def _upsert_localizations(
    session: AsyncSession,
    food: TravelFood,
    values: list[FoodLocalizationPayload] | None,
) -> None:
    if values is None:
        return
    existing = {
        row.locale: row
        for row in (
            await session.scalars(
                select(FoodLocalization).where(FoodLocalization.food_id == food.id)
            )
        ).all()
    }
    for value in values:
        row = existing.get(value.locale)
        if row is None:
            row = FoodLocalization(food_id=food.id, locale=value.locale)
        row.name = value.name
        row.summary = value.summary
        session.add(row)


async def _admin_item(
    session: AsyncSession, food: TravelFood, locale: Locale = DEFAULT_LOCALE
) -> dict[str, object]:
    localizations = list(
        (
            await session.scalars(
                select(FoodLocalization)
                .where(FoodLocalization.food_id == food.id)
                .order_by(FoodLocalization.locale)
            )
        ).all()
    )
    destinations = list(
        (
            await session.scalars(
                select(FoodDestination)
                .where(FoodDestination.food_id == food.id)
                .order_by(FoodDestination.display_order)
            )
        ).all()
    )
    hotspots = (
        await session.execute(
            select(FoodHotspot.hotspot_id, TravelHotspot.name)
            .join(TravelHotspot, TravelHotspot.id == FoodHotspot.hotspot_id)
            .where(FoodHotspot.food_id == food.id)
            .order_by(FoodHotspot.display_order)
        )
    ).all()
    return {
        "id": str(food.id),
        "slug": food.slug,
        "country_code": food.country_code,
        "country_name": country_name_for(food.country_code, locale),
        "local_name": food.local_name,
        "romanized_name": food.romanized_name,
        "food_kind": food.food_kind,
        "meal_types": food.meal_types,
        "ingredient_tags": food.ingredient_tags,
        "dietary_notes": food.dietary_notes,
        "source_urls": food.source_urls,
        "review_status": food.review_status,
        "is_active": food.is_active,
        "display_order": food.display_order,
        "localizations": [
            {"locale": row.locale, "name": row.name, "summary": row.summary}
            for row in localizations
        ],
        "destination_ids": [row.destination_id for row in destinations],
        "hotspots": [{"id": str(hotspot_id), "name": name} for hotspot_id, name in hotspots],
    }


@router.get("")
async def list_admin_foods(
    user: AdminUser,
    session: Session,
    locale: RequestLocale,
    country_code: Annotated[str | None, Query(min_length=2, max_length=2)] = None,
    destination_id: Annotated[str | None, Query(min_length=2, max_length=64)] = None,
    status: ReviewStatus | None = None,
    food_kind: FoodKind | None = None,
    q: Annotated[str | None, Query(max_length=100)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 30,
) -> dict[str, object]:
    _ = user
    # Keyed by dimension so each facet can drop only its own filter.
    filters: dict[str, Any] = {}
    if country_code:
        filters["country_code"] = TravelFood.country_code == country_code.upper()
    if status:
        filters["status"] = TravelFood.review_status == status
    if food_kind:
        filters["food_kind"] = TravelFood.food_kind == food_kind
    if q:
        filters["q"] = TravelFood.search_text.ilike(f"%{escape_like(q.strip())}%", escape="\\")
    if destination_id:
        food_ids = select(FoodDestination.food_id).where(
            FoodDestination.destination_id == destination_id.casefold()
        )
        filters["destination_id"] = TravelFood.id.in_(food_ids)
    where = list(filters.values())

    def without(dimension: str) -> list[Any]:
        return [clause for key, clause in filters.items() if key != dimension]

    total = int(await session.scalar(select(func.count(TravelFood.id)).where(*where)) or 0)
    rows = list(
        (
            await session.scalars(
                select(TravelFood)
                .where(*where)
                .order_by(
                    country_rank(TravelFood.country_code),
                    TravelFood.country_code,
                    TravelFood.display_order,
                    TravelFood.slug,
                )
                .offset((page - 1) * limit)
                .limit(limit)
            )
        ).all()
    )
    country_rows = (
        await session.execute(
            select(TravelFood.country_code, func.count(TravelFood.id).label("count"))
            .where(*without("country_code"))
            .group_by(TravelFood.country_code)
        )
    ).all()
    kind_rows = (
        await session.execute(
            select(TravelFood.food_kind, func.count(TravelFood.id).label("count"))
            .where(*without("food_kind"))
            .group_by(TravelFood.food_kind)
        )
    ).all()
    return {
        "items": [await _admin_item(session, food, locale) for food in rows],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
        "facets": {
            "countries": [
                {
                    "code": row.country_code,
                    "name": country_name_for(row.country_code, locale),
                    "count": int(row.count),
                }
                for row in ranked(country_rows, "country_code", COUNTRY_ORDER)
            ],
            "food_kinds": [
                {"code": row.food_kind, "count": int(row.count)}
                for row in ranked(kind_rows, "food_kind", FOOD_KIND_ORDER)
            ],
        },
    }


@router.post("", status_code=201)
async def create_food(
    payload: FoodWritePayload, user: AdminUser, session: Session
) -> dict[str, object]:
    if await session.scalar(select(TravelFood.id).where(TravelFood.slug == payload.slug)):
        raise AppError(409, "food_slug_exists", "美食 slug 已存在")
    await _validate_relations(session, payload.destination_ids, payload.hotspot_ids)
    food = TravelFood(
        slug=payload.slug,
        country_code=payload.country_code.upper(),
        local_name=payload.local_name,
        romanized_name=payload.romanized_name,
        food_kind=payload.food_kind,
        meal_types=payload.meal_types,
        ingredient_tags=payload.ingredient_tags,
        dietary_notes=payload.dietary_notes,
        search_text=build_food_search_text(
            payload.slug,
            payload.country_code.upper(),
            payload.local_name,
            payload.romanized_name,
            [item.name for item in payload.localizations],
            payload.ingredient_tags,
        ),
        source_urls=payload.source_urls,
        review_status=payload.review_status,
        is_active=payload.is_active,
        display_order=payload.display_order,
    )
    session.add(food)
    await session.flush()
    await _upsert_localizations(session, food, payload.localizations)
    await _replace_relations(session, food, payload.destination_ids, payload.hotspot_ids)
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="food_created",
            target=f"food:{food.id}",
            metadata_json={"slug": food.slug},
        )
    )
    await session.commit()
    return await _admin_item(session, food)


@router.patch("/{food_id}")
async def update_food(
    food_id: UUID, payload: FoodUpdatePayload, user: AdminUser, session: Session
) -> dict[str, object]:
    food = await session.get(TravelFood, food_id)
    if food is None:
        raise AppError(404, "food_not_found", "找不到這筆美食資料")
    destinations = payload.destination_ids
    if destinations is None:
        destinations = list(
            (
                await session.scalars(
                    select(FoodDestination.destination_id).where(FoodDestination.food_id == food.id)
                )
            ).all()
        )
    await _validate_relations(session, destinations, payload.hotspot_ids or [])
    scalar_fields = (
        "country_code",
        "local_name",
        "romanized_name",
        "food_kind",
        "meal_types",
        "ingredient_tags",
        "dietary_notes",
        "source_urls",
        "review_status",
        "is_active",
        "display_order",
    )
    for field in scalar_fields:
        value = getattr(payload, field)
        if value is not None:
            setattr(food, field, value.upper() if field == "country_code" else value)
    await _upsert_localizations(session, food, payload.localizations)
    await _replace_relations(session, food, payload.destination_ids, payload.hotspot_ids)
    localized_names = [
        row.name
        for row in (
            await session.scalars(
                select(FoodLocalization).where(FoodLocalization.food_id == food.id)
            )
        ).all()
    ]
    food.search_text = build_food_search_text(
        food.slug,
        food.country_code,
        food.local_name,
        food.romanized_name,
        localized_names,
        food.ingredient_tags,
    )
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="food_updated",
            target=f"food:{food.id}",
            metadata_json={"fields": sorted(payload.model_fields_set)},
        )
    )
    await session.commit()
    return await _admin_item(session, food)


@router.post("/batch")
async def batch_foods(
    payload: FoodBatchPayload, user: AdminUser, session: Session
) -> dict[str, int | str]:
    foods = list(
        (await session.scalars(select(TravelFood).where(TravelFood.id.in_(payload.ids)))).all()
    )
    if len(foods) != len(set(payload.ids)):
        raise AppError(404, "food_not_found", "部分美食資料不存在")
    statuses = {
        "approve": ("approved", True),
        "reject": ("rejected", False),
        "disable": ("disabled", False),
        "activate": ("approved", True),
    }
    status, active = statuses[payload.action]
    for food in foods:
        food.review_status = status
        food.is_active = active
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="foods_batch_updated",
            target=f"foods:{len(foods)}",
            metadata_json={
                "action": payload.action,
                "ids": [str(food.id) for food in foods],
                "reason": payload.reason,
                "at": datetime.now(UTC).isoformat(),
            },
        )
    )
    await session.commit()
    return {"updated": len(foods), "status": status}


async def _validate_merchant_relations(
    session: AsyncSession,
    *,
    destination_id: str,
    food_ids: list[UUID],
    google_place_id: str | None,
    naver_map_url: str | None,
    current_id: UUID | None = None,
) -> None:
    if destination_for_id(destination_id) is None:
        raise AppError(422, "unsupported_destination", "目前不支援這個目的地")
    foods = list(
        (await session.scalars(select(TravelFood.id).where(TravelFood.id.in_(food_ids)))).all()
    )
    if len(foods) != len(set(food_ids)):
        raise AppError(404, "merchant_food_not_found", "部分料理資料不存在")
    for field, value in (
        (FoodMerchant.google_place_id, google_place_id),
        (FoodMerchant.naver_map_url, naver_map_url),
    ):
        if not value:
            continue
        query = select(FoodMerchant.id).where(field == value)
        if current_id:
            query = query.where(FoodMerchant.id != current_id)
        if await session.scalar(query):
            raise AppError(409, "merchant_map_identity_exists", "地圖識別已由其他店家使用")


def _validate_publishable_merchant(
    *,
    country_code: str,
    latitude: float | Decimal | None,
    longitude: float | Decimal | None,
    coordinate_source_type: str | None,
    coordinate_source_url: str | None,
    google_place_id: str | None,
    naver_map_url: str | None,
) -> None:
    if not has_exact_map_identity(country_code, google_place_id, naver_map_url):
        provider = "Naver 精準地點頁" if country_code.upper() == "KR" else "Google Place ID"
        raise AppError(422, "exact_map_identity_required", f"發布前必須提供{provider}")
    if not valid_coordinate_pair(latitude, longitude):
        raise AppError(422, "permanent_coordinates_required", "發布前必須提供永久 WGS84 座標")
    if not is_durable_coordinate_source(coordinate_source_type, coordinate_source_url):
        raise AppError(422, "coordinate_source_required", "發布前必須提供可稽核的永久座標來源")


async def _replace_merchant_relations(
    session: AsyncSession,
    merchant: FoodMerchant,
    food_ids: list[UUID] | None,
    sources: list[FoodMerchantSourcePayload] | None,
) -> None:
    if food_ids is not None:
        rows = list(
            (
                await session.scalars(
                    select(FoodMerchantFood).where(FoodMerchantFood.merchant_id == merchant.id)
                )
            ).all()
        )
        for row in rows:
            await session.delete(row)
        await session.flush()
        for order, food_id in enumerate(food_ids, start=1):
            session.add(
                FoodMerchantFood(
                    merchant_id=merchant.id,
                    food_id=food_id,
                    is_primary=True,
                    display_order=order,
                )
            )
    if sources is not None:
        source_rows = list(
            (
                await session.scalars(
                    select(FoodMerchantSource).where(FoodMerchantSource.merchant_id == merchant.id)
                )
            ).all()
        )
        for source_row in source_rows:
            await session.delete(source_row)
        await session.flush()
        for source in sources:
            session.add(
                FoodMerchantSource(
                    merchant_id=merchant.id,
                    source_type=source.source_type,
                    source_scope=source.source_scope,
                    source_title=source.source_title,
                    source_url=source.source_url,
                    claims_json=list(source.claims),
                    edition_year=source.edition_year,
                    distinction=source.distinction,
                    is_current=source.is_current,
                    last_verified_at=datetime.now(UTC),
                )
            )


async def _merchant_admin_item(session: AsyncSession, merchant: FoodMerchant) -> dict[str, object]:
    foods = (
        await session.execute(
            select(FoodMerchantFood.food_id, TravelFood.slug, TravelFood.local_name)
            .join(TravelFood, TravelFood.id == FoodMerchantFood.food_id)
            .where(FoodMerchantFood.merchant_id == merchant.id)
            .order_by(FoodMerchantFood.display_order)
        )
    ).all()
    sources = list(
        (
            await session.scalars(
                select(FoodMerchantSource)
                .where(FoodMerchantSource.merchant_id == merchant.id)
                .order_by(FoodMerchantSource.created_at)
            )
        ).all()
    )
    area = await session.get(FoodArea, merchant.area_id) if merchant.area_id else None
    category_rows = (
        await session.execute(
            select(FoodMerchantCategory, FoodCategory)
            .join(FoodCategory, FoodCategory.id == FoodMerchantCategory.category_id)
            .where(FoodMerchantCategory.merchant_id == merchant.id)
            .order_by(FoodMerchantCategory.is_primary.desc(), FoodMerchantCategory.display_order)
        )
    ).all()
    return {
        "id": str(merchant.id),
        "slug": merchant.slug,
        "destination_id": merchant.destination_id,
        "country_code": merchant.country_code,
        "name": merchant.name,
        "local_name": merchant.local_name,
        "address": merchant.address,
        "latitude": float(merchant.latitude) if merchant.latitude is not None else None,
        "longitude": float(merchant.longitude) if merchant.longitude is not None else None,
        "coordinate_source_type": merchant.coordinate_source_type,
        "coordinate_source_url": merchant.coordinate_source_url,
        "coordinate_verified_at": merchant.coordinate_verified_at,
        "google_place_id": merchant.google_place_id,
        "naver_map_url": merchant.naver_map_url,
        "official_website_url": merchant.official_website_url,
        "official_website_verified_at": merchant.official_website_verified_at,
        "map_match_status": merchant.map_match_status,
        "review_status": merchant.review_status,
        "is_active": merchant.is_active,
        "verified_at": merchant.verified_at,
        "display_order": merchant.display_order,
        "area": (
            {
                "id": str(area.id),
                "slug": area.slug,
                "name": localized_name(area.names_json, "zh-TW"),
                "destination_id": area.destination_id,
            }
            if area
            else None
        ),
        "area_source": merchant.area_source,
        "categories": [
            {
                "id": str(category.id),
                "slug": category.slug,
                "name": localized_name(category.names_json, "zh-TW"),
                "is_primary": link.is_primary,
                "source": link.source,
            }
            for link, category in category_rows
        ],
        "foods": [
            {"id": str(food_id), "slug": slug, "name": name} for food_id, slug, name in foods
        ],
        "sources": [
            {
                "id": str(source.id),
                "source_type": source.source_type,
                "source_scope": source.source_scope,
                "source_title": source.source_title,
                "source_url": source.source_url,
                "claims": source.claims_json,
                "edition_year": source.edition_year,
                "distinction": source.distinction,
                "is_current": source.is_current,
                "last_verified_at": source.last_verified_at,
            }
            for source in sources
        ],
    }


@router.get("/merchants")
async def list_food_merchants(
    user: AdminUser,
    session: Session,
    destination_id: Annotated[str | None, Query(min_length=2, max_length=64)] = None,
    status: ReviewStatus | None = None,
    map_status: MapMatchStatus | None = None,
    official_data: Literal["filled", "missing"] | None = None,
    area_slug: Annotated[str | None, Query(min_length=2, max_length=128)] = None,
    category: Annotated[str | None, Query(min_length=2, max_length=128)] = None,
    taxonomy: MerchantTaxonomyFilter | None = None,
    q: Annotated[str | None, Query(max_length=100)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 30,
) -> dict[str, object]:
    _ = user
    filters = []
    if destination_id:
        filters.append(FoodMerchant.destination_id == destination_id.casefold())
    if status:
        filters.append(FoodMerchant.review_status == status)
    if map_status:
        filters.append(FoodMerchant.map_match_status == map_status)
    if area_slug:
        filters.append(
            FoodMerchant.area_id.in_(select(FoodArea.id).where(FoodArea.slug == area_slug))
        )
    if category:
        filters.append(
            FoodMerchant.id.in_(
                select(FoodMerchantCategory.merchant_id)
                .join(FoodCategory, FoodCategory.id == FoodMerchantCategory.category_id)
                .where(FoodCategory.slug == category)
            )
        )
    if taxonomy == "missing_area":
        filters.append(FoodMerchant.area_id.is_(None))
    elif taxonomy == "missing_category":
        filters.append(FoodMerchant.id.not_in(select(FoodMerchantCategory.merchant_id)))
    if official_data == "filled":
        filters.append(FoodMerchant.official_website_url.is_not(None))
    elif official_data == "missing":
        filters.append(FoodMerchant.official_website_url.is_(None))
    if q:
        term = f"%{escape_like(q.strip())}%"
        filters.append(
            FoodMerchant.name.ilike(term, escape="\\")
            | FoodMerchant.local_name.ilike(term, escape="\\")
            | FoodMerchant.slug.ilike(term, escape="\\")
        )
    total = int(await session.scalar(select(func.count(FoodMerchant.id)).where(*filters)) or 0)
    merchants = list(
        (
            await session.scalars(
                select(FoodMerchant)
                .where(*filters)
                .order_by(
                    FoodMerchant.destination_id, FoodMerchant.display_order, FoodMerchant.name
                )
                .offset((page - 1) * limit)
                .limit(limit)
            )
        ).all()
    )
    return {
        "items": [await _merchant_admin_item(session, item) for item in merchants],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


class CoordinateQueueApprovalItem(BaseModel):
    merchant_id: UUID
    place_id: str = Field(min_length=10, max_length=255)


class CoordinateQueueApprovePayload(BaseModel):
    items: list[CoordinateQueueApprovalItem] = Field(min_length=1, max_length=50)

    @model_validator(mode="after")
    def unique_merchants(self) -> CoordinateQueueApprovePayload:
        ids = [item.merchant_id for item in self.items]
        if len(set(ids)) != len(ids):
            raise ValueError("同一店家在批次中重複出現")
        return self


async def _queue_google(session: AsyncSession) -> GoogleTravelService:
    settings = await load_runtime_settings(session)
    return GoogleTravelService(get_redis(), settings, locale="zh-TW")


@router.get("/merchants/coordinate-queue")
async def merchant_coordinate_queue(
    user: AdminUser,
    session: Session,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=20)] = 10,
) -> dict[str, object]:
    """A page of merchants without durable coordinates, each beside Google's best match.

    Resolution happens per page rather than for the whole backlog so one screen costs at
    most ``limit`` Pro-tier searches, and the Redis provider cache makes revisits and the
    subsequent approval free.
    """
    _ = user
    google = await _queue_google(session)
    total = await queue_total(session)
    if not google.configured:
        return {"configured": False, "items": [], "total": total, "page": page, "limit": limit}
    merchants = list(
        (
            await session.scalars(
                coordinate_queue_statement().offset((page - 1) * limit).limit(limit)
            )
        ).all()
    )
    items = await resolve_queue_page(session, google, merchants)
    return {"configured": True, "items": items, "total": total, "page": page, "limit": limit}


@router.post("/merchants/coordinate-queue/approve")
async def approve_merchant_coordinates(
    payload: CoordinateQueueApprovePayload, user: AdminUser, session: Session
) -> dict[str, object]:
    google = await _queue_google(session)
    if not google.configured:
        raise AppError(503, "google_places_not_configured", "Google Places 金鑰未設定")
    outcomes: list[dict[str, str]] = []
    written = 0
    # The whole batch is one transaction, so the IntegrityError from a concurrent admin
    # claiming the same Place ID can surface either at commit or mid-loop, when a later
    # item's SELECT autoflushes the conflicting UPDATE. Both paths land here.
    try:
        for item in payload.items:
            merchant = await session.get(FoodMerchant, item.merchant_id)
            if merchant is None:
                outcomes.append({"merchant_id": str(item.merchant_id), "outcome": "not_found"})
                continue
            outcome = await apply_approval(
                session,
                google,
                merchant,
                expected_place_id=item.place_id,
                actor_id=user.id,
            )
            if outcome in ("verified", "coordinates_saved"):
                written += 1
            outcomes.append({"merchant_id": str(item.merchant_id), "outcome": outcome})
        if written:
            session.add(
                AdminAuditLog(
                    actor_user_id=user.id,
                    action="food_merchant_coordinates_approved",
                    target=f"food_merchants:{written}",
                    metadata_json={"outcomes": outcomes},
                )
            )
        await session.commit()
    except IntegrityError as exc:
        # The batch rolls back whole rather than half-landing.
        await session.rollback()
        raise AppError(
            409, "place_id_conflict", "有 Place ID 剛被其他管理員寫入，請重新整理佇列後再試"
        ) from exc
    return {"written": written, "outcomes": outcomes}


@router.post("/merchants/map-candidates")
async def food_merchant_map_candidates(
    payload: GoogleMapCandidateRequest,
    user: AdminUser,
    session: Session,
) -> dict[str, object]:
    _ = user
    return await preview_google_place_match(
        session,
        get_redis(),
        query=payload.query,
        country_code=payload.country_code,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )


@router.post("/merchants", status_code=201)
async def create_food_merchant(
    payload: FoodMerchantWritePayload, user: AdminUser, session: Session
) -> dict[str, object]:
    if await session.scalar(select(FoodMerchant.id).where(FoodMerchant.slug == payload.slug)):
        raise AppError(409, "merchant_slug_exists", "店家 slug 已存在")
    await _validate_merchant_relations(
        session,
        destination_id=payload.destination_id,
        food_ids=payload.food_ids,
        google_place_id=payload.google_place_id,
        naver_map_url=payload.naver_map_url,
    )
    category_slugs = payload.category_slugs or await _derived_category_slugs(
        session, payload.food_ids
    )
    area, categories = await _validate_merchant_taxonomy(
        session,
        destination_id=payload.destination_id,
        area_slug=payload.area_slug,
        category_slugs=category_slugs,
    )
    if payload.review_status == "approved" and payload.is_active:
        _require_merchant_categories(len(categories))
    if (
        payload.review_status == "approved"
        and payload.is_active
        and payload.map_match_status != "verified"
    ):
        raise AppError(422, "map_verification_required", "發布前必須完成精準地點比對")
    if payload.map_match_status == "verified" or (
        payload.review_status == "approved" and payload.is_active
    ):
        _validate_publishable_merchant(
            country_code=payload.country_code,
            latitude=payload.latitude,
            longitude=payload.longitude,
            coordinate_source_type=payload.coordinate_source_type,
            coordinate_source_url=payload.coordinate_source_url,
            google_place_id=payload.google_place_id,
            naver_map_url=payload.naver_map_url,
        )
    now = datetime.now(UTC)
    merchant = FoodMerchant(
        slug=payload.slug,
        destination_id=payload.destination_id.casefold(),
        country_code=payload.country_code.upper(),
        name=payload.name,
        local_name=payload.local_name,
        address=payload.address,
        latitude=payload.latitude,
        longitude=payload.longitude,
        coordinate_source_type=payload.coordinate_source_type,
        coordinate_source_url=payload.coordinate_source_url,
        coordinate_verified_at=(
            now
            if has_durable_coordinates(
                payload.latitude,
                payload.longitude,
                payload.coordinate_source_type,
                payload.coordinate_source_url,
            )
            else None
        ),
        google_place_id=payload.google_place_id,
        naver_map_url=payload.naver_map_url,
        official_website_url=payload.official_website_url,
        official_website_verified_at=now if payload.official_website_url else None,
        map_match_status=payload.map_match_status,
        review_status=payload.review_status,
        is_active=payload.is_active,
        verified_at=now if payload.map_match_status == "verified" else None,
        verified_by_user_id=user.id if payload.map_match_status == "verified" else None,
        display_order=payload.display_order,
        area_id=area.id if area else None,
        area_source="admin" if area else None,
    )
    session.add(merchant)
    await session.flush()
    await _replace_merchant_relations(session, merchant, payload.food_ids, payload.sources)
    await _replace_merchant_categories(
        session, merchant, categories, source="admin" if payload.category_slugs else "seed"
    )
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="food_merchant_created",
            target=f"food_merchant:{merchant.id}",
            metadata_json={"slug": merchant.slug, "destination_id": merchant.destination_id},
        )
    )
    await session.commit()
    return await _merchant_admin_item(session, merchant)


@router.patch("/merchants/{merchant_id}")
async def update_food_merchant(
    merchant_id: UUID,
    payload: FoodMerchantUpdatePayload,
    user: AdminUser,
    session: Session,
) -> dict[str, object]:
    merchant = await session.get(FoodMerchant, merchant_id)
    if merchant is None:
        raise AppError(404, "food_merchant_not_found", "找不到這筆店家資料")
    existing_food_ids = list(
        (
            await session.scalars(
                select(FoodMerchantFood.food_id).where(FoodMerchantFood.merchant_id == merchant.id)
            )
        ).all()
    )
    food_ids = payload.food_ids if payload.food_ids is not None else existing_food_ids
    destination_id = payload.destination_id or merchant.destination_id
    google_place_id = (
        payload.google_place_id
        if "google_place_id" in payload.model_fields_set
        else merchant.google_place_id
    )
    naver_map_url = (
        payload.naver_map_url
        if "naver_map_url" in payload.model_fields_set
        else merchant.naver_map_url
    )
    latitude = payload.latitude if "latitude" in payload.model_fields_set else merchant.latitude
    longitude = payload.longitude if "longitude" in payload.model_fields_set else merchant.longitude
    coordinate_source_type = (
        payload.coordinate_source_type
        if "coordinate_source_type" in payload.model_fields_set
        else merchant.coordinate_source_type
    )
    coordinate_source_url = (
        payload.coordinate_source_url
        if "coordinate_source_url" in payload.model_fields_set
        else merchant.coordinate_source_url
    )
    official_website_url = (
        payload.official_website_url
        if "official_website_url" in payload.model_fields_set
        else merchant.official_website_url
    )
    if official_website_url:
        validate_editorial_url(official_website_url)
        if payload.sources is not None:
            has_website_evidence = any(
                source.source_scope == "merchant_website"
                and "official_website" in source.claims
                and source.is_current
                for source in payload.sources
            )
        else:
            website_sources = list(
                (
                    await session.scalars(
                        select(FoodMerchantSource).where(
                            FoodMerchantSource.merchant_id == merchant.id,
                            FoodMerchantSource.source_scope == "merchant_website",
                            FoodMerchantSource.is_current.is_(True),
                        )
                    )
                ).all()
            )
            has_website_evidence = any(
                "official_website" in source.claims_json for source in website_sources
            )
        if not has_website_evidence:
            raise AppError(
                422,
                "restaurant_source_evidence_missing",
                "店家官網缺少仍有效的 merchant_website 來源佐證",
            )
    country_code = payload.country_code or merchant.country_code
    map_status = payload.map_match_status or merchant.map_match_status
    review_status = payload.review_status or merchant.review_status
    is_active = payload.is_active if payload.is_active is not None else merchant.is_active
    if (latitude is None) != (longitude is None):
        raise AppError(422, "coordinate_pair_required", "緯度與經度必須同時提供")
    if review_status == "approved" and is_active and map_status != "verified":
        raise AppError(422, "map_verification_required", "發布前必須完成精準地點比對")
    if map_status == "verified" or (review_status == "approved" and is_active):
        _validate_publishable_merchant(
            country_code=country_code,
            latitude=latitude,
            longitude=longitude,
            coordinate_source_type=coordinate_source_type,
            coordinate_source_url=coordinate_source_url,
            google_place_id=google_place_id,
            naver_map_url=naver_map_url,
        )
    await _validate_merchant_relations(
        session,
        destination_id=destination_id,
        food_ids=food_ids,
        google_place_id=google_place_id,
        naver_map_url=naver_map_url,
        current_id=merchant.id,
    )
    current_area = await session.get(FoodArea, merchant.area_id) if merchant.area_id else None
    area_slug = (
        payload.area_slug
        if "area_slug" in payload.model_fields_set
        else (current_area.slug if current_area else None)
    )
    area, categories = await _validate_merchant_taxonomy(
        session,
        destination_id=destination_id,
        area_slug=area_slug,
        category_slugs=payload.category_slugs or [],
    )
    existing_category_count = int(
        await session.scalar(
            select(func.count(FoodMerchantCategory.id)).where(
                FoodMerchantCategory.merchant_id == merchant.id
            )
        )
        or 0
    )
    new_categories: list[FoodCategory] | None = None
    new_category_source = "admin"
    if payload.category_slugs is not None:
        new_categories = categories
    elif existing_category_count == 0 and food_ids:
        _, new_categories = await _validate_merchant_taxonomy(
            session,
            destination_id=destination_id,
            area_slug=None,
            category_slugs=await _derived_category_slugs(session, food_ids),
        )
        new_category_source = "seed"
    if review_status == "approved" and is_active:
        _require_merchant_categories(
            len(new_categories) if new_categories is not None else existing_category_count
        )
    scalar_fields = (
        "destination_id",
        "country_code",
        "name",
        "local_name",
        "address",
        "latitude",
        "longitude",
        "coordinate_source_type",
        "coordinate_source_url",
        "google_place_id",
        "naver_map_url",
        "official_website_url",
        "map_match_status",
        "review_status",
        "is_active",
        "display_order",
    )
    for field in scalar_fields:
        if field not in payload.model_fields_set:
            continue
        value = getattr(payload, field)
        if field == "country_code" and value:
            value = value.upper()
        if field == "destination_id" and value:
            value = value.casefold()
        setattr(merchant, field, value)
    if "official_website_url" in payload.model_fields_set:
        merchant.official_website_verified_at = (
            datetime.now(UTC) if payload.official_website_url else None
        )
    if any(
        field in payload.model_fields_set
        for field in ("latitude", "longitude", "coordinate_source_type", "coordinate_source_url")
    ):
        merchant.coordinate_verified_at = (
            datetime.now(UTC)
            if has_durable_coordinates(
                latitude,
                longitude,
                coordinate_source_type,
                coordinate_source_url,
            )
            else None
        )
    if payload.map_match_status == "verified":
        merchant.verified_at = datetime.now(UTC)
        merchant.verified_by_user_id = user.id
    elif payload.map_match_status in {"unverified", "ambiguous", "disabled"}:
        merchant.verified_at = None
        merchant.verified_by_user_id = None
    await _replace_merchant_relations(session, merchant, payload.food_ids, payload.sources)
    if "area_slug" in payload.model_fields_set:
        merchant.area_id = area.id if area else None
        merchant.area_source = "admin"
    if new_categories is not None:
        await _replace_merchant_categories(
            session, merchant, new_categories, source=new_category_source
        )
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="food_merchant_updated",
            target=f"food_merchant:{merchant.id}",
            metadata_json={"fields": sorted(payload.model_fields_set)},
        )
    )
    await session.commit()
    return await _merchant_admin_item(session, merchant)


@router.post("/merchants/batch")
async def batch_food_merchants(
    payload: FoodMerchantBatchPayload, user: AdminUser, session: Session
) -> dict[str, int | str]:
    merchants = list(
        (await session.scalars(select(FoodMerchant).where(FoodMerchant.id.in_(payload.ids)))).all()
    )
    if len(merchants) != len(set(payload.ids)):
        raise AppError(404, "food_merchant_not_found", "部分店家資料不存在")
    now = datetime.now(UTC)
    category_counts = {
        merchant_id: int(count)
        for merchant_id, count in (
            await session.execute(
                select(FoodMerchantCategory.merchant_id, func.count(FoodMerchantCategory.id))
                .where(FoodMerchantCategory.merchant_id.in_([item.id for item in merchants]))
                .group_by(FoodMerchantCategory.merchant_id)
            )
        ).all()
    }
    for merchant in merchants:
        if payload.action in {"approve", "activate"}:
            if merchant.map_match_status != "verified":
                raise AppError(422, "map_verification_required", "發布前必須完成精準地點比對")
            _validate_publishable_merchant(
                country_code=merchant.country_code,
                latitude=merchant.latitude,
                longitude=merchant.longitude,
                coordinate_source_type=merchant.coordinate_source_type,
                coordinate_source_url=merchant.coordinate_source_url,
                google_place_id=merchant.google_place_id,
                naver_map_url=merchant.naver_map_url,
            )
            await _ensure_merchant_categories(session, merchant, category_counts)
            merchant.review_status = "approved"
            merchant.is_active = True
        elif payload.action == "reject":
            merchant.review_status = "rejected"
            merchant.is_active = False
        elif payload.action == "disable":
            merchant.review_status = "disabled"
            merchant.is_active = False
        elif payload.action in {"verify", "verify_activate"}:
            _validate_publishable_merchant(
                country_code=merchant.country_code,
                latitude=merchant.latitude,
                longitude=merchant.longitude,
                coordinate_source_type=merchant.coordinate_source_type,
                coordinate_source_url=merchant.coordinate_source_url,
                google_place_id=merchant.google_place_id,
                naver_map_url=merchant.naver_map_url,
            )
            merchant.map_match_status = "verified"
            merchant.verified_at = now
            merchant.verified_by_user_id = user.id
            if payload.action == "verify_activate":
                await _ensure_merchant_categories(session, merchant, category_counts)
                merchant.review_status = "approved"
                merchant.is_active = True
        elif payload.action == "ambiguous":
            merchant.map_match_status = "ambiguous"
            merchant.verified_at = None
            merchant.verified_by_user_id = None
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="food_merchants_batch_updated",
            target=f"food_merchants:{len(merchants)}",
            metadata_json={
                "action": payload.action,
                "ids": [str(item.id) for item in merchants],
                "reason": payload.reason,
            },
        )
    )
    await session.commit()
    return {"updated": len(merchants), "status": payload.action}


async def _area_merchant_counts(session: AsyncSession, area_ids: list[UUID]) -> dict[UUID, int]:
    if not area_ids:
        return {}
    rows = (
        await session.execute(
            select(FoodMerchant.area_id, func.count(FoodMerchant.id))
            .where(FoodMerchant.area_id.in_(area_ids))
            .group_by(FoodMerchant.area_id)
        )
    ).all()
    return {area_id: int(count) for area_id, count in rows if area_id is not None}


@router.get("/areas")
async def list_food_areas(
    user: AdminUser,
    session: Session,
    destination_id: Annotated[str | None, Query(min_length=2, max_length=64)] = None,
    status: TaxonomyStatus | None = None,
    q: Annotated[str | None, Query(max_length=100)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
) -> dict[str, object]:
    _ = user
    filters = []
    if destination_id:
        filters.append(FoodArea.destination_id == destination_id.casefold())
    if status:
        filters.append(FoodArea.is_active.is_(status == "active"))
    if q:
        term = f"%{escape_like(q.strip())}%"
        filters.append(
            FoodArea.slug.ilike(term, escape="\\")
            | FoodArea.names_json["zh-TW"].as_string().ilike(term, escape="\\")
            | FoodArea.names_json["en"].as_string().ilike(term, escape="\\")
        )
    total = int(await session.scalar(select(func.count(FoodArea.id)).where(*filters)) or 0)
    areas = list(
        (
            await session.scalars(
                select(FoodArea)
                .where(*filters)
                .order_by(FoodArea.destination_id, FoodArea.display_order, FoodArea.slug)
                .offset((page - 1) * limit)
                .limit(limit)
            )
        ).all()
    )
    counts = await _area_merchant_counts(session, [area.id for area in areas])
    return {
        "items": [_area_admin_item(area, counts.get(area.id, 0)) for area in areas],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.post("/areas", status_code=201)
async def create_food_area(
    payload: FoodAreaWritePayload, user: AdminUser, session: Session
) -> dict[str, object]:
    if await session.scalar(select(FoodArea.id).where(FoodArea.slug == payload.slug)):
        raise AppError(409, "food_area_slug_exists", "區域 slug 已存在")
    destination_id = payload.destination_id.casefold()
    country_code = destination_country_code(destination_id)
    if country_code is None:
        raise AppError(422, "unsupported_destination", "目前不支援這個目的地")
    area = FoodArea(
        slug=payload.slug,
        destination_id=destination_id,
        country_code=country_code,
        names_json=payload.names,
        match_terms_json=payload.match_terms,
        latitude=payload.latitude,
        longitude=payload.longitude,
        display_order=payload.display_order,
        is_active=payload.is_active,
        source="admin",
    )
    session.add(area)
    await session.flush()
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="food_area_created",
            target=f"food_area:{area.id}",
            metadata_json={"slug": area.slug, "destination_id": area.destination_id},
        )
    )
    await session.commit()
    return _area_admin_item(area)


@router.patch("/areas/{area_id}")
async def update_food_area(
    area_id: UUID, payload: FoodAreaUpdatePayload, user: AdminUser, session: Session
) -> dict[str, object]:
    area = await session.get(FoodArea, area_id)
    if area is None:
        raise AppError(404, "food_area_not_found", "找不到這個區域")
    if payload.destination_id and payload.destination_id.casefold() != area.destination_id:
        destination_id = payload.destination_id.casefold()
        country_code = destination_country_code(destination_id)
        if country_code is None:
            raise AppError(422, "unsupported_destination", "目前不支援這個目的地")
        attached = await session.scalar(
            select(func.count(FoodMerchant.id)).where(FoodMerchant.area_id == area.id)
        )
        if attached:
            raise AppError(422, "food_area_has_merchants", "已有店家使用這個區域，無法更換城市")
        area.destination_id = destination_id
        area.country_code = country_code
    latitude = payload.latitude if "latitude" in payload.model_fields_set else area.latitude
    longitude = payload.longitude if "longitude" in payload.model_fields_set else area.longitude
    if (latitude is None) != (longitude is None):
        raise AppError(422, "coordinate_pair_required", "緯度與經度必須同時提供")
    if "latitude" in payload.model_fields_set or "longitude" in payload.model_fields_set:
        area.latitude = Decimal(str(latitude)) if latitude is not None else None
        area.longitude = Decimal(str(longitude)) if longitude is not None else None
    if payload.names is not None:
        area.names_json = payload.names
    if payload.match_terms is not None:
        area.match_terms_json = payload.match_terms
    if payload.is_active is not None:
        area.is_active = payload.is_active
    if payload.display_order is not None:
        area.display_order = payload.display_order
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="food_area_updated",
            target=f"food_area:{area.id}",
            metadata_json={"fields": sorted(payload.model_fields_set)},
        )
    )
    await session.commit()
    counts = await _area_merchant_counts(session, [area.id])
    return _area_admin_item(area, counts.get(area.id, 0))


@router.post("/areas/batch")
async def batch_food_areas(
    payload: TaxonomyBatchPayload, user: AdminUser, session: Session
) -> dict[str, int | str]:
    areas = list(
        (await session.scalars(select(FoodArea).where(FoodArea.id.in_(payload.ids)))).all()
    )
    if len(areas) != len(set(payload.ids)):
        raise AppError(404, "food_area_not_found", "部分區域不存在")
    for area in areas:
        area.is_active = payload.action == "activate"
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="food_areas_batch_updated",
            target=f"food_areas:{len(areas)}",
            metadata_json={
                "action": payload.action,
                "ids": [str(area.id) for area in areas],
                "reason": payload.reason,
            },
        )
    )
    await session.commit()
    return {"updated": len(areas), "status": payload.action}


@router.get("/categories")
async def list_food_categories(
    user: AdminUser,
    session: Session,
    status: TaxonomyStatus | None = None,
) -> dict[str, object]:
    _ = user
    filters = []
    if status:
        filters.append(FoodCategory.is_active.is_(status == "active"))
    categories = list(
        (
            await session.scalars(
                select(FoodCategory)
                .where(*filters)
                .order_by(FoodCategory.display_order, FoodCategory.slug)
            )
        ).all()
    )
    counts = {
        category_id: int(count)
        for category_id, count in (
            await session.execute(
                select(FoodMerchantCategory.category_id, func.count(FoodMerchantCategory.id))
                .where(FoodMerchantCategory.category_id.in_([item.id for item in categories]))
                .group_by(FoodMerchantCategory.category_id)
            )
        ).all()
    }
    return {
        "items": [_category_admin_item(item, counts.get(item.id, 0)) for item in categories],
        "total": len(categories),
        "page": 1,
        "pages": 1,
    }


@router.post("/categories", status_code=201)
async def create_food_category(
    payload: FoodCategoryWritePayload, user: AdminUser, session: Session
) -> dict[str, object]:
    if await session.scalar(select(FoodCategory.id).where(FoodCategory.slug == payload.slug)):
        raise AppError(409, "food_category_slug_exists", "分類 slug 已存在")
    category = FoodCategory(
        slug=payload.slug,
        names_json=payload.names,
        display_order=payload.display_order,
        is_active=payload.is_active,
        source="admin",
    )
    session.add(category)
    await session.flush()
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="food_category_created",
            target=f"food_category:{category.id}",
            metadata_json={"slug": category.slug},
        )
    )
    await session.commit()
    return _category_admin_item(category)


@router.patch("/categories/{category_id}")
async def update_food_category(
    category_id: UUID, payload: FoodCategoryUpdatePayload, user: AdminUser, session: Session
) -> dict[str, object]:
    category = await session.get(FoodCategory, category_id)
    if category is None:
        raise AppError(404, "food_category_not_found", "找不到這個美食分類")
    if payload.names is not None:
        category.names_json = payload.names
    if payload.is_active is not None:
        category.is_active = payload.is_active
    if payload.display_order is not None:
        category.display_order = payload.display_order
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="food_category_updated",
            target=f"food_category:{category.id}",
            metadata_json={"fields": sorted(payload.model_fields_set)},
        )
    )
    await session.commit()
    count = int(
        await session.scalar(
            select(func.count(FoodMerchantCategory.id)).where(
                FoodMerchantCategory.category_id == category.id
            )
        )
        or 0
    )
    return _category_admin_item(category, count)


@router.post("/categories/batch")
async def batch_food_categories(
    payload: TaxonomyBatchPayload, user: AdminUser, session: Session
) -> dict[str, int | str]:
    categories = list(
        (await session.scalars(select(FoodCategory).where(FoodCategory.id.in_(payload.ids)))).all()
    )
    if len(categories) != len(set(payload.ids)):
        raise AppError(404, "food_category_not_found", "部分美食分類不存在")
    for category in categories:
        category.is_active = payload.action == "activate"
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="food_categories_batch_updated",
            target=f"food_categories:{len(categories)}",
            metadata_json={
                "action": payload.action,
                "ids": [str(category.id) for category in categories],
                "reason": payload.reason,
            },
        )
    )
    await session.commit()
    return {"updated": len(categories), "status": payload.action}
