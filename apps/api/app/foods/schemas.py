"""Response and request models for the merchant directory endpoints."""

from __future__ import annotations

from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class MapLink(BaseModel):
    provider: str
    label: str
    url: str
    primary: bool = False


class MerchantSourceView(BaseModel):
    source_type: str
    source_scope: str
    title: str
    url: str
    claims: list[str] = Field(default_factory=list)
    edition_year: int | None = None
    distinction: str | None = None
    last_verified_at: str | None = None


class CoordinateSourceView(BaseModel):
    type: str | None = None
    url: str | None = None
    verified_at: str | None = None


class FoodAreaRef(BaseModel):
    id: str
    slug: str
    name: str
    local_name: str | None = None


class FoodCategoryRef(BaseModel):
    slug: str
    name: str
    is_primary: bool = False


class SignatureDishView(BaseModel):
    food_id: str
    slug: str
    name: str
    local_name: str
    food_kind: str
    meal_types: list[str] = Field(default_factory=list)


class MerchantCard(BaseModel):
    id: str
    slug: str
    name: str
    local_name: str
    destination_id: str
    destination_name: str
    country_code: str
    area: FoodAreaRef | None = None
    categories: list[FoodCategoryRef] = Field(default_factory=list)
    signature_dishes: list[SignatureDishView] = Field(default_factory=list)
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    coordinate_source: CoordinateSourceView
    official_website_url: str | None = None
    map_links: list[MapLink] = Field(default_factory=list)
    verified_at: str | None = None
    sources: list[MerchantSourceView] = Field(default_factory=list)


class FacetAreaView(BaseModel):
    id: str
    slug: str
    name: str
    local_name: str | None = None
    merchant_count: int


class FacetCategoryView(BaseModel):
    slug: str
    name: str
    merchant_count: int


class MerchantFacets(BaseModel):
    areas: list[FacetAreaView] = Field(default_factory=list)
    unassigned_area_count: int = 0
    categories: list[FacetCategoryView] = Field(default_factory=list)


class MerchantListResponse(BaseModel):
    total: int
    has_more: bool
    next_cursor: str | None = None
    items: list[MerchantCard]
    facets: MerchantFacets


class FoodCityView(BaseModel):
    id: str
    name: str
    local_name: str | None = None
    english_name: str | None = None
    country_code: str
    role: str
    parent_destination_id: str | None = None
    merchant_count: int
    area_count: int


class FoodCountryView(BaseModel):
    code: str
    name: str
    merchant_count: int
    cities: list[FoodCityView]


class FoodCitiesResponse(BaseModel):
    total_merchants: int
    countries: list[FoodCountryView]


class FoodCategoriesResponse(BaseModel):
    items: list[FacetCategoryView]


class MerchantTripSelectionRequest(BaseModel):
    trip_id: UUID
    version: int = Field(ge=1)
    day_date: date
    meal_role: Literal["lunch", "dinner"]
    food_id: UUID | None = None
