from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


class Timestamped:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class User(Timestamped, Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    auth_version: Mapped[int] = mapped_column(Integer, default=1)
    preferred_locale: Mapped[str] = mapped_column(String(16), default="zh-TW")


class UsagePackage(Timestamped, Base):
    __tablename__ = "usage_packages"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    localized_names: Mapped[dict[str, str]] = mapped_column(JSON, default=dict, server_default="{}")
    uses: Mapped[int] = mapped_column(Integer)
    price_twd: Mapped[int] = mapped_column(Integer, default=0)
    display_order: Mapped[int] = mapped_column(Integer, default=100, server_default="100")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    purchasable: Mapped[bool] = mapped_column(Boolean, default=False)


class UsageOperationCost(Timestamped, Base):
    __tablename__ = "usage_operation_costs"
    __table_args__ = (
        CheckConstraint("uses >= 0 AND uses <= 100", name="ck_usage_operation_cost_range"),
    )
    operation: Mapped[str] = mapped_column(String(64), primary_key=True)
    uses: Mapped[int] = mapped_column(Integer, default=1)
    updated_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )


class UsageAccount(Timestamped, Base):
    __tablename__ = "usage_accounts"
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_usage_account_user"),
        CheckConstraint("remaining_uses >= 0", name="ck_usage_account_remaining_nonnegative"),
        CheckConstraint("reserved_uses >= 0", name="ck_usage_account_reserved_nonnegative"),
        CheckConstraint(
            "reserved_uses <= remaining_uses", name="ck_usage_account_reserved_within_balance"
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    remaining_uses: Mapped[int] = mapped_column(Integer, default=0)
    reserved_uses: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(32), default="active")


class UsageLedger(Base):
    __tablename__ = "usage_ledger"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "reference", "entry_type", name="uq_ledger_user_reference_type"
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    account_id: Mapped[UUID] = mapped_column(ForeignKey("usage_accounts.id"), index=True)
    package_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("usage_packages.id"), nullable=True, index=True
    )
    entry_type: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32))
    amount: Mapped[int] = mapped_column(Integer)
    balance_after: Mapped[int] = mapped_column(Integer)
    reference: Mapped[str] = mapped_column(String(255), index=True)
    operation: Mapped[str | None] = mapped_column(String(64), nullable=True)
    summary: Mapped[str] = mapped_column(String(255))
    resource_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    unit: Mapped[str] = mapped_column(String(32), default="use")
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class UsageReservation(Timestamped, Base):
    __tablename__ = "usage_reservations"
    __table_args__ = (UniqueConstraint("user_id", "idempotency_key", name="uq_usage_idempotency"),)
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    account_id: Mapped[UUID] = mapped_column(ForeignKey("usage_accounts.id"), index=True)
    idempotency_key: Mapped[str] = mapped_column(String(255))
    operation: Mapped[str] = mapped_column(String(64))
    summary: Mapped[str] = mapped_column(String(255))
    uses: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(32), default="reserved")
    resource_id: Mapped[UUID | None] = mapped_column(nullable=True)


class SearchRequest(Timestamped, Base):
    __tablename__ = "search_requests"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(32), default="processing", index=True)
    progress: Mapped[int] = mapped_column(Integer, default=0)
    operation: Mapped[str] = mapped_column(String(64))
    request_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    result_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    warnings_json: Mapped[list[str]] = mapped_column(JSON, default=list)


class FlightStatusLookup(Timestamped, Base):
    __tablename__ = "flight_status_lookups"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    reservation_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("usage_reservations.id"), nullable=True, index=True
    )
    provider: Mapped[str] = mapped_column(String(64), default="flightaware")
    query_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    result_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    cache_hit: Mapped[bool] = mapped_column(Boolean, default=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class SearchConstraint(Base):
    __tablename__ = "search_constraints"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    search_id: Mapped[UUID] = mapped_column(
        ForeignKey("search_requests.id", ondelete="CASCADE"), index=True
    )
    key: Mapped[str] = mapped_column(String(64))
    value: Mapped[Any] = mapped_column(JSON)


class SearchJob(Timestamped, Base):
    __tablename__ = "search_jobs"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    search_id: Mapped[UUID] = mapped_column(
        ForeignKey("search_requests.id", ondelete="CASCADE"), index=True
    )
    queue_job_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="queued")
    error: Mapped[str | None] = mapped_column(Text, nullable=True)


class ProviderRequest(Timestamped, Base):
    __tablename__ = "provider_requests"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    search_id: Mapped[UUID] = mapped_column(
        ForeignKey("search_requests.id", ondelete="CASCADE"), index=True
    )
    provider: Mapped[str] = mapped_column(String(64))
    module: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), default="started")
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)


class ProviderResponse(Base):
    __tablename__ = "provider_responses"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    provider_request_id: Mapped[UUID] = mapped_column(
        ForeignKey("provider_requests.id", ondelete="CASCADE"), index=True
    )
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class AffiliateClick(Base):
    __tablename__ = "affiliate_clicks"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(index=True)
    search_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    trip_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    offer_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    partner: Mapped[str] = mapped_column(String(64), index=True)
    module: Mapped[str] = mapped_column(String(32), index=True)
    sub_id: Mapped[str] = mapped_column(String(64), index=True)
    destination_summary: Mapped[str] = mapped_column(String(128))
    target_host: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="redirected")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class FlightOfferRecord(Timestamped, Base):
    __tablename__ = "flight_offers"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    search_id: Mapped[UUID] = mapped_column(
        ForeignKey("search_requests.id", ondelete="CASCADE"), index=True
    )
    provider: Mapped[str] = mapped_column(String(64))
    provider_offer_id: Mapped[str] = mapped_column(String(128))
    public_offer_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    data: Mapped[dict[str, Any]] = mapped_column(JSON)
    total_price: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3), default="TWD")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class FlightSegment(Base):
    __tablename__ = "flight_segments"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    flight_offer_id: Mapped[UUID] = mapped_column(
        ForeignKey("flight_offers.id", ondelete="CASCADE"), index=True
    )
    position: Mapped[int] = mapped_column(Integer)
    data: Mapped[dict[str, Any]] = mapped_column(JSON)


class HotelProperty(Timestamped, Base):
    __tablename__ = "hotel_properties"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    provider: Mapped[str] = mapped_column(String(64))
    provider_hotel_id: Mapped[str] = mapped_column(String(128))
    name: Mapped[str] = mapped_column(String(255))
    data: Mapped[dict[str, Any]] = mapped_column(JSON)


class HotelOfferRecord(Timestamped, Base):
    __tablename__ = "hotel_offers"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    search_id: Mapped[UUID] = mapped_column(
        ForeignKey("search_requests.id", ondelete="CASCADE"), index=True
    )
    hotel_property_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("hotel_properties.id"), nullable=True
    )
    provider: Mapped[str] = mapped_column(String(64))
    provider_offer_id: Mapped[str] = mapped_column(String(128))
    public_offer_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    data: Mapped[dict[str, Any]] = mapped_column(JSON)
    total_price: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3), default="TWD")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ActivityOfferRecord(Timestamped, Base):
    __tablename__ = "activity_offers"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    search_id: Mapped[UUID] = mapped_column(
        ForeignKey("search_requests.id", ondelete="CASCADE"), index=True
    )
    provider: Mapped[str] = mapped_column(String(64))
    provider_offer_id: Mapped[str] = mapped_column(String(128))
    data: Mapped[dict[str, Any]] = mapped_column(JSON)
    price: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3), default="TWD")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class TransportOfferRecord(Timestamped, Base):
    __tablename__ = "transport_offers"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    search_id: Mapped[UUID] = mapped_column(
        ForeignKey("search_requests.id", ondelete="CASCADE"), index=True
    )
    provider: Mapped[str] = mapped_column(String(64))
    provider_offer_id: Mapped[str] = mapped_column(String(128))
    data: Mapped[dict[str, Any]] = mapped_column(JSON)
    price: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3), default="TWD")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class TravelHotspot(Timestamped, Base):
    __tablename__ = "travel_hotspots"
    __table_args__ = (
        CheckConstraint(
            "map_match_status IN ('unverified', 'verified', 'ambiguous', 'disabled')",
            name="ck_travel_hotspot_map_match_status",
        ),
        CheckConstraint(
            "(latitude IS NULL) = (longitude IS NULL)",
            name="ck_travel_hotspot_coordinate_pair",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    city_code: Mapped[str] = mapped_column(String(8), index=True)
    destination_id: Mapped[str] = mapped_column(String(64), index=True, default="unknown")
    city_name: Mapped[str] = mapped_column(String(100))
    country_code: Mapped[str] = mapped_column(String(2), index=True)
    country_name: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(32), index=True)
    search_text: Mapped[str] = mapped_column(Text)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    plus_code_global: Mapped[str | None] = mapped_column(String(16), nullable=True, index=True)
    coordinate_source_type: Mapped[str | None] = mapped_column(String(32), nullable=True)
    coordinate_source_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    coordinate_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    wikipedia_project: Mapped[str | None] = mapped_column(String(64), nullable=True)
    wikipedia_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    google_place_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, unique=True, index=True
    )
    naver_map_url: Mapped[str | None] = mapped_column(String(2048), nullable=True, unique=True)
    map_match_status: Mapped[str] = mapped_column(String(24), default="unverified", index=True)
    map_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    map_verified_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    wikidata_item_id: Mapped[str | None] = mapped_column(
        String(32), nullable=True, unique=True, index=True
    )
    origin: Mapped[str] = mapped_column(String(32), default="curated", index=True)
    review_status: Mapped[str] = mapped_column(String(24), default="approved", index=True)
    review_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    discovery_distance_km: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    discovered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reviewed_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    source_urls: Mapped[list[str]] = mapped_column(JSON, default=list)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    is_deep_travel: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    depth_kind: Mapped[str | None] = mapped_column(String(24), nullable=True)
    depth_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)


class HotspotPlaceProfile(Timestamped, Base):
    __tablename__ = "hotspot_place_profiles"
    __table_args__ = (
        CheckConstraint(
            "match_status IN ('unmatched', 'pending', 'auto_approved', 'approved', "
            "'rejected', 'failed')",
            name="ck_hotspot_place_profile_match_status",
        ),
        CheckConstraint(
            "place_id_source IN ('none', 'legacy', 'automatic', 'manual')",
            name="ck_hotspot_place_profile_place_id_source",
        ),
        CheckConstraint(
            "website_review_status IN ('none', 'pending', 'auto_approved', 'approved', 'rejected')",
            name="ck_hotspot_place_profile_website_review_status",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    hotspot_id: Mapped[UUID] = mapped_column(
        ForeignKey("travel_hotspots.id", ondelete="CASCADE"), unique=True, index=True
    )
    place_id_source: Mapped[str] = mapped_column(String(16), default="none")
    match_status: Mapped[str] = mapped_column(String(24), default="unmatched", index=True)
    match_confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)
    match_evidence_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    candidate_place_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    candidate_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    candidate_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    candidate_latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    candidate_longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    manual_official_website_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    manual_official_website_source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    website_review_status: Mapped[str] = mapped_column(String(24), default="none", index=True)
    google_maps_uri: Mapped[str | None] = mapped_column(Text, nullable=True)
    formatted_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    google_latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    google_longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    plus_code_global: Mapped[str | None] = mapped_column(String(32), nullable=True)
    plus_code_compound: Mapped[str | None] = mapped_column(String(255), nullable=True)
    opening_hours_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    provider_website_uri: Mapped[str | None] = mapped_column(Text, nullable=True)
    provider_locale: Mapped[str | None] = mapped_column(String(16), nullable=True)
    provider_attributions_json: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    provider_fetched_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    provider_refresh_after: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    provider_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reviewed_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    review_reason: Mapped[str | None] = mapped_column(Text, nullable=True)


class HotspotPlaceEnrichmentRun(Timestamped, Base):
    __tablename__ = "hotspot_place_enrichment_runs"
    __table_args__ = (
        UniqueConstraint(
            "actor_user_id", "idempotency_key", name="uq_hotspot_place_enrichment_idempotency"
        ),
        CheckConstraint(
            "status IN ('queued', 'running', 'partial', 'completed', 'failed')",
            name="ck_hotspot_place_enrichment_status",
        ),
        CheckConstraint(
            "mode IN ('missing_or_expired', 'force')",
            name="ck_hotspot_place_enrichment_mode",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    actor_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    idempotency_key: Mapped[str] = mapped_column(String(255))
    mode: Mapped[str] = mapped_column(String(32), default="missing_or_expired")
    scope_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(16), default="queued", index=True)
    total_count: Mapped[int] = mapped_column(Integer, default=0)
    processed_count: Mapped[int] = mapped_column(Integer, default=0)
    published_count: Mapped[int] = mapped_column(Integer, default=0)
    pending_count: Mapped[int] = mapped_column(Integer, default=0)
    unmatched_count: Mapped[int] = mapped_column(Integer, default=0)
    failed_count: Mapped[int] = mapped_column(Integer, default=0)
    estimated_google_calls: Mapped[int] = mapped_column(Integer, default=0)
    actual_google_calls: Mapped[int] = mapped_column(Integer, default=0)
    progress_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    result_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    error_json: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class TravelFood(Timestamped, Base):
    __tablename__ = "travel_foods"
    __table_args__ = (
        CheckConstraint(
            "food_kind IN ('main', 'noodle_soup', 'street_food', 'dessert', 'drink')",
            name="ck_travel_food_kind",
        ),
        CheckConstraint(
            "review_status IN ('pending', 'approved', 'rejected', 'disabled')",
            name="ck_travel_food_review_status",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    country_code: Mapped[str] = mapped_column(String(2), index=True)
    local_name: Mapped[str] = mapped_column(String(255))
    romanized_name: Mapped[str] = mapped_column(String(255))
    food_kind: Mapped[str] = mapped_column(String(24), index=True)
    meal_types: Mapped[list[str]] = mapped_column(JSON, default=list)
    ingredient_tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    dietary_notes: Mapped[list[str]] = mapped_column(JSON, default=list)
    search_text: Mapped[str] = mapped_column(Text)
    source_urls: Mapped[list[str]] = mapped_column(JSON, default=list)
    review_status: Mapped[str] = mapped_column(String(24), default="approved", index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    display_order: Mapped[int] = mapped_column(Integer, default=100)


class FoodLocalization(Timestamped, Base):
    __tablename__ = "food_localizations"
    __table_args__ = (
        UniqueConstraint("food_id", "locale", name="uq_food_localization_locale"),
        CheckConstraint(
            "locale IN ('en', 'ja', 'ko', 'zh-TW', 'zh-CN')",
            name="ck_food_localization_locale",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    food_id: Mapped[UUID] = mapped_column(
        ForeignKey("travel_foods.id", ondelete="CASCADE"), index=True
    )
    locale: Mapped[str] = mapped_column(String(16), index=True)
    name: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(Text)


class FoodDestination(Base):
    __tablename__ = "food_destinations"
    __table_args__ = (UniqueConstraint("food_id", "destination_id", name="uq_food_destination"),)
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    food_id: Mapped[UUID] = mapped_column(
        ForeignKey("travel_foods.id", ondelete="CASCADE"), index=True
    )
    destination_id: Mapped[str] = mapped_column(String(64), index=True)
    display_order: Mapped[int] = mapped_column(Integer, default=100)


class FoodHotspot(Base):
    __tablename__ = "food_hotspots"
    __table_args__ = (UniqueConstraint("food_id", "hotspot_id", name="uq_food_hotspot"),)
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    food_id: Mapped[UUID] = mapped_column(
        ForeignKey("travel_foods.id", ondelete="CASCADE"), index=True
    )
    hotspot_id: Mapped[UUID] = mapped_column(
        ForeignKey("travel_hotspots.id", ondelete="CASCADE"), index=True
    )
    display_order: Mapped[int] = mapped_column(Integer, default=100)


class FoodMerchant(Timestamped, Base):
    __tablename__ = "food_merchants"
    __table_args__ = (
        CheckConstraint(
            "review_status IN ('pending', 'approved', 'rejected', 'disabled')",
            name="ck_food_merchant_review_status",
        ),
        CheckConstraint(
            "map_match_status IN ('unverified', 'verified', 'ambiguous', 'disabled')",
            name="ck_food_merchant_map_match_status",
        ),
        CheckConstraint(
            "(latitude IS NULL) = (longitude IS NULL)",
            name="ck_food_merchant_coordinate_pair",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    destination_id: Mapped[str] = mapped_column(String(64), index=True)
    country_code: Mapped[str] = mapped_column(String(2), index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    local_name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    plus_code_global: Mapped[str | None] = mapped_column(String(16), nullable=True, index=True)
    coordinate_source_type: Mapped[str | None] = mapped_column(String(32), nullable=True)
    coordinate_source_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    coordinate_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    google_place_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, unique=True, index=True
    )
    naver_map_url: Mapped[str | None] = mapped_column(String(2048), nullable=True, unique=True)
    official_website_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    official_website_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    map_match_status: Mapped[str] = mapped_column(String(24), default="unverified", index=True)
    review_status: Mapped[str] = mapped_column(String(24), default="pending", index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    verified_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    display_order: Mapped[int] = mapped_column(Integer, default=100)


class FoodMerchantFood(Base):
    __tablename__ = "food_merchant_foods"
    __table_args__ = (UniqueConstraint("merchant_id", "food_id", name="uq_food_merchant_food"),)
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    merchant_id: Mapped[UUID] = mapped_column(
        ForeignKey("food_merchants.id", ondelete="CASCADE"), index=True
    )
    food_id: Mapped[UUID] = mapped_column(
        ForeignKey("travel_foods.id", ondelete="CASCADE"), index=True
    )
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    display_order: Mapped[int] = mapped_column(Integer, default=100)


class FoodMerchantSource(Timestamped, Base):
    __tablename__ = "food_merchant_sources"
    __table_args__ = (
        UniqueConstraint(
            "merchant_id", "source_url", "edition_year", name="uq_food_merchant_source"
        ),
        CheckConstraint(
            "source_type IN ('official_tourism', 'merchant_official', 'michelin_licensed')",
            name="ck_food_merchant_source_type",
        ),
        CheckConstraint(
            "source_scope IN ('destination_context', 'merchant_listing', "
            "'merchant_website', 'coordinates')",
            name="ck_food_merchant_source_scope",
        ),
        CheckConstraint(
            "distinction IS NULL OR distinction IN "
            "('three_star', 'two_star', 'one_star', 'green_star', "
            "'bib_gourmand', 'selected')",
            name="ck_food_merchant_distinction",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    merchant_id: Mapped[UUID] = mapped_column(
        ForeignKey("food_merchants.id", ondelete="CASCADE"), index=True
    )
    source_type: Mapped[str] = mapped_column(String(32), index=True)
    source_scope: Mapped[str] = mapped_column(String(32), default="destination_context", index=True)
    source_title: Mapped[str] = mapped_column(String(255))
    source_url: Mapped[str] = mapped_column(String(2048))
    claims_json: Mapped[list[str]] = mapped_column(JSON, default=list)
    edition_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    distinction: Mapped[str | None] = mapped_column(String(24), nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    last_verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class RestaurantPlace(Timestamped, Base):
    """Durable restaurant identity.

    Google Place IDs are the only provider content kept indefinitely. The Maps
    URL is an app-generated value derived from that ID, not a provider response.
    Display fields such as the name, rating and opening hours are fetched live
    and are intentionally absent from this table.
    """

    __tablename__ = "restaurant_places"
    __table_args__ = (
        CheckConstraint(
            "identity_status IN ('unknown', 'active', 'moved', 'not_found')",
            name="ck_restaurant_place_identity_status",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    google_place_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    generated_maps_url: Mapped[str] = mapped_column(String(2048))
    identity_status: Mapped[str] = mapped_column(String(24), default="unknown", index=True)
    successor_place_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    identity_checked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    identity_error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_suppressed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    suppression_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    suppressed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    suppressed_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )


class RestaurantFavorite(Timestamped, Base):
    __tablename__ = "restaurant_favorites"
    __table_args__ = (
        UniqueConstraint("user_id", "restaurant_place_id", name="uq_restaurant_favorite"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    restaurant_place_id: Mapped[UUID] = mapped_column(
        ForeignKey("restaurant_places.id", ondelete="CASCADE"), index=True
    )


class RestaurantEditorialProfile(Timestamped, Base):
    """Independently sourced restaurant data owned by Travel Scanner."""

    __tablename__ = "restaurant_editorial_profiles"
    __table_args__ = (
        CheckConstraint(
            "review_status IN ('pending', 'approved', 'rejected', 'disabled')",
            name="ck_restaurant_editorial_review_status",
        ),
        CheckConstraint(
            "(ride_latitude IS NULL) = (ride_longitude IS NULL)",
            name="ck_restaurant_editorial_coordinate_pair",
        ),
        UniqueConstraint("restaurant_place_id", name="uq_restaurant_editorial_place"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    restaurant_place_id: Mapped[UUID] = mapped_column(
        ForeignKey("restaurant_places.id", ondelete="CASCADE"), index=True
    )
    display_name: Mapped[str] = mapped_column(String(255), index=True)
    local_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    official_website_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    ride_latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    ride_longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    review_status: Mapped[str] = mapped_column(String(24), default="pending", index=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    verified_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )


class RestaurantEditorialSource(Timestamped, Base):
    __tablename__ = "restaurant_editorial_sources"
    __table_args__ = (
        CheckConstraint(
            "source_type IN ('merchant_official', 'official_tourism')",
            name="ck_restaurant_editorial_source_type",
        ),
        UniqueConstraint("profile_id", "source_url", name="uq_restaurant_editorial_source_url"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    profile_id: Mapped[UUID] = mapped_column(
        ForeignKey("restaurant_editorial_profiles.id", ondelete="CASCADE"), index=True
    )
    source_type: Mapped[str] = mapped_column(String(32), index=True)
    source_title: Mapped[str] = mapped_column(String(255))
    source_url: Mapped[str] = mapped_column(String(2048))
    claims_json: Mapped[list[str]] = mapped_column(JSON, default=list)
    last_verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class RestaurantScanRun(Timestamped, Base):
    __tablename__ = "restaurant_scan_runs"
    __table_args__ = (
        CheckConstraint(
            "status IN ('queued', 'running', 'partial', 'completed', 'failed', 'quota_paused')",
            name="ck_restaurant_scan_status",
        ),
        CheckConstraint("radius_meters IN (5000, 10000)", name="ck_restaurant_scan_radius"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    hotspot_id: Mapped[UUID] = mapped_column(
        ForeignKey("travel_hotspots.id", ondelete="CASCADE"), index=True
    )
    actor_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    idempotency_key: Mapped[str] = mapped_column(String(255), unique=True)
    status: Mapped[str] = mapped_column(String(24), default="queued", index=True)
    radius_meters: Mapped[int] = mapped_column(Integer, default=10_000)
    cells_total: Mapped[int] = mapped_column(Integer, default=1)
    cells_completed: Mapped[int] = mapped_column(Integer, default=0)
    candidate_count: Mapped[int] = mapped_column(Integer, default=0)
    aggregate_calls: Mapped[int] = mapped_column(Integer, default=0)
    details_calls: Mapped[int] = mapped_column(Integer, default=0)
    failure_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    failure_detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class RestaurantScanCell(Timestamped, Base):
    __tablename__ = "restaurant_scan_cells"
    __table_args__ = (
        CheckConstraint(
            "status IN ('queued', 'running', 'split', 'completed', 'partial', 'failed')",
            name="ck_restaurant_scan_cell_status",
        ),
        UniqueConstraint(
            "run_id",
            "center_latitude",
            "center_longitude",
            "radius_meters",
            "depth",
            name="uq_restaurant_scan_cell_geometry",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    run_id: Mapped[UUID] = mapped_column(
        ForeignKey("restaurant_scan_runs.id", ondelete="CASCADE"), index=True
    )
    parent_cell_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("restaurant_scan_cells.id", ondelete="CASCADE"), nullable=True, index=True
    )
    status: Mapped[str] = mapped_column(String(24), default="queued", index=True)
    center_latitude: Mapped[Decimal] = mapped_column(Numeric(9, 6))
    center_longitude: Mapped[Decimal] = mapped_column(Numeric(9, 6))
    radius_meters: Mapped[int] = mapped_column(Integer)
    depth: Mapped[int] = mapped_column(Integer, default=0)
    provider_place_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    details_cursor: Mapped[int] = mapped_column(Integer, default=0)
    error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)


class HotspotRestaurantCandidate(Timestamped, Base):
    __tablename__ = "hotspot_restaurant_candidates"
    __table_args__ = (
        UniqueConstraint(
            "hotspot_id", "restaurant_place_id", name="uq_hotspot_restaurant_candidate"
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    hotspot_id: Mapped[UUID] = mapped_column(
        ForeignKey("travel_hotspots.id", ondelete="CASCADE"), index=True
    )
    restaurant_place_id: Mapped[UUID] = mapped_column(
        ForeignKey("restaurant_places.id", ondelete="CASCADE"), index=True
    )
    scan_run_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("restaurant_scan_runs.id", ondelete="SET NULL"), nullable=True, index=True
    )
    discovery_radius_meters: Mapped[int] = mapped_column(Integer, default=10_000)


class HotspotLocalization(Timestamped, Base):
    __tablename__ = "hotspot_localizations"
    __table_args__ = (
        UniqueConstraint("hotspot_id", "locale", name="uq_hotspot_localization_locale"),
        CheckConstraint(
            "locale IN ('en', 'ja', 'ko', 'zh-TW', 'zh-CN')",
            name="ck_hotspot_localization_locale",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    hotspot_id: Mapped[UUID] = mapped_column(
        ForeignKey("travel_hotspots.id", ondelete="CASCADE"), index=True
    )
    locale: Mapped[str] = mapped_column(String(16), index=True)
    name: Mapped[str] = mapped_column(String(255))
    aliases: Mapped[list[str]] = mapped_column(JSON, default=list)
    search_terms: Mapped[list[str]] = mapped_column(JSON, default=list)


class HotspotGuide(Timestamped, Base):
    __tablename__ = "hotspot_guides"
    __table_args__ = (
        UniqueConstraint("hotspot_id", "canonical_url", name="uq_hotspot_guide_canonical_url"),
        CheckConstraint(
            "content_type IN ('article', 'video')", name="ck_hotspot_guide_content_type"
        ),
        CheckConstraint(
            "locale IN ('en', 'ja', 'ko', 'zh-TW', 'zh-CN')",
            name="ck_hotspot_guide_locale",
        ),
        CheckConstraint(
            "review_status IN ('pending', 'approved', 'rejected', 'disabled')",
            name="ck_hotspot_guide_review_status",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    hotspot_id: Mapped[UUID] = mapped_column(
        ForeignKey("travel_hotspots.id", ondelete="CASCADE"), index=True
    )
    content_type: Mapped[str] = mapped_column(String(16), index=True)
    provider: Mapped[str] = mapped_column(String(32), index=True)
    locale: Mapped[str] = mapped_column(String(16), index=True)
    title: Mapped[str] = mapped_column(String(500))
    creator_name: Mapped[str] = mapped_column(String(255))
    canonical_url: Mapped[str] = mapped_column(Text)
    provider_content_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    view_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    language_confidence: Mapped[Decimal] = mapped_column(Numeric(4, 3), default=1)
    discovery_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    review_status: Mapped[str] = mapped_column(String(24), default="pending", index=True)
    review_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reviewed_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    last_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    metadata_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class HotspotGuideClickDaily(Base):
    __tablename__ = "hotspot_guide_click_daily"
    __table_args__ = (
        UniqueConstraint("guide_id", "observed_on", name="uq_hotspot_guide_click_day"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    guide_id: Mapped[UUID] = mapped_column(
        ForeignKey("hotspot_guides.id", ondelete="CASCADE"), index=True
    )
    observed_on: Mapped[date] = mapped_column(Date, index=True)
    unique_opens: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class HotspotGuideAISearchRun(Timestamped, Base):
    __tablename__ = "hotspot_guide_ai_search_runs"
    __table_args__ = (
        UniqueConstraint(
            "actor_user_id", "idempotency_key", name="uq_hotspot_guide_ai_search_idempotency"
        ),
        CheckConstraint(
            "provider IN ('minimax', 'openai', 'anthropic')",
            name="ck_hotspot_guide_ai_search_provider",
        ),
        CheckConstraint(
            "depth IN ('economy', 'balanced', 'deep')",
            name="ck_hotspot_guide_ai_search_depth",
        ),
        CheckConstraint(
            "status IN ('queued', 'running', 'partial', 'completed', 'failed')",
            name="ck_hotspot_guide_ai_search_status",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    actor_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    hotspot_id: Mapped[UUID] = mapped_column(
        ForeignKey("travel_hotspots.id", ondelete="CASCADE"), index=True
    )
    idempotency_key: Mapped[str] = mapped_column(String(255))
    requested_locales: Mapped[list[str]] = mapped_column(JSON, default=list)
    content_types: Mapped[list[str]] = mapped_column(JSON, default=list)
    provider: Mapped[str] = mapped_column(String(16), index=True)
    model: Mapped[str] = mapped_column(String(128))
    depth: Mapped[str] = mapped_column(String(16))
    only_missing: Mapped[bool] = mapped_column(Boolean, default=True)
    custom_instructions: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(16), default="queued", index=True)
    progress: Mapped[int] = mapped_column(Integer, default=0)
    progress_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    query_plan_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    usage_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    result_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    queue_job_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class HotspotSignal(Base):
    __tablename__ = "hotspot_signals"
    __table_args__ = (
        UniqueConstraint(
            "hotspot_id",
            "source",
            "metric",
            "observed_on",
            name="uq_hotspot_signal_observation",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    hotspot_id: Mapped[UUID] = mapped_column(
        ForeignKey("travel_hotspots.id", ondelete="CASCADE"), index=True
    )
    source: Mapped[str] = mapped_column(String(64), index=True)
    metric: Mapped[str] = mapped_column(String(64), index=True)
    value: Mapped[Decimal] = mapped_column(Numeric(18, 4))
    observed_on: Mapped[date] = mapped_column(Date, index=True)
    window_days: Mapped[int] = mapped_column(Integer, default=30)
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_estimate: Mapped[bool] = mapped_column(Boolean, default=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class HotspotRanking(Base):
    __tablename__ = "hotspot_rankings"
    __table_args__ = (
        UniqueConstraint(
            "hotspot_id",
            "scope",
            "scope_key",
            "window_days",
            "observed_on",
            name="uq_hotspot_ranking_snapshot",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    hotspot_id: Mapped[UUID] = mapped_column(
        ForeignKey("travel_hotspots.id", ondelete="CASCADE"), index=True
    )
    scope: Mapped[str] = mapped_column(String(16), index=True)
    scope_key: Mapped[str] = mapped_column(String(32), index=True)
    window_days: Mapped[int] = mapped_column(Integer, default=30)
    rank: Mapped[int] = mapped_column(Integer)
    score: Mapped[Decimal] = mapped_column(Numeric(6, 2))
    interest_score: Mapped[Decimal] = mapped_column(Numeric(6, 2))
    growth_score: Mapped[Decimal] = mapped_column(Numeric(6, 2))
    quality_score: Mapped[Decimal] = mapped_column(Numeric(6, 2))
    confidence_score: Mapped[Decimal] = mapped_column(Numeric(6, 2))
    observed_on: Mapped[date] = mapped_column(Date, index=True)
    explanation: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class TripPlan(Timestamped, Base):
    __tablename__ = "trip_plans"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    search_id: Mapped[UUID | None] = mapped_column(ForeignKey("search_requests.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(255))
    mode: Mapped[str] = mapped_column(String(32))
    total_price: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3), default="TWD")
    data: Mapped[dict[str, Any]] = mapped_column(JSON)
    version: Mapped[int] = mapped_column(Integer, default=1)
    destination_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    destination_place_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    timezone: Mapped[str] = mapped_column(String(64), default="UTC")
    route_preference: Mapped[str] = mapped_column(String(32), default="FEWER_TRANSFERS")


class TripPlanItem(Base):
    __tablename__ = "trip_plan_items"
    __table_args__ = (
        CheckConstraint(
            "system_role IS NULL OR system_role IN "
            "('outbound_flight', 'hotel_start', 'lunch', 'dinner', "
            "'hotel_end', 'return_flight')",
            name="ck_trip_plan_item_system_role",
        ),
        UniqueConstraint(
            "trip_plan_id",
            "day_date",
            "system_role",
            name="uq_trip_plan_item_system_role",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    trip_plan_id: Mapped[UUID] = mapped_column(
        ForeignKey("trip_plans.id", ondelete="CASCADE"), index=True
    )
    item_type: Mapped[str] = mapped_column(String(32))
    offer_id: Mapped[UUID | None] = mapped_column(nullable=True)
    day_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    position: Mapped[int] = mapped_column(Integer, default=0)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    plus_code_global: Mapped[str | None] = mapped_column(String(16), nullable=True, index=True)
    coordinate_source_type: Mapped[str | None] = mapped_column(String(32), nullable=True)
    coordinate_source_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    coordinate_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    locked: Mapped[bool] = mapped_column(Boolean, default=False)
    is_estimated: Mapped[bool] = mapped_column(Boolean, default=False)
    data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    provider_place_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location_source: Mapped[str | None] = mapped_column(String(32), nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    fixed_time: Mapped[bool] = mapped_column(Boolean, default=False)
    system_role: Mapped[str | None] = mapped_column(String(24), nullable=True)
    is_skipped: Mapped[bool] = mapped_column(Boolean, default=False)


class TripRouteDaySetting(Timestamped, Base):
    __tablename__ = "trip_route_day_settings"
    __table_args__ = (
        UniqueConstraint("trip_plan_id", "day_date", name="uq_trip_route_day_setting"),
        CheckConstraint(
            "default_travel_mode IN ('transit', 'walk', 'drive')",
            name="ck_trip_route_day_mode",
        ),
        CheckConstraint(
            "default_buffer_minutes >= 0 AND default_buffer_minutes <= 180",
            name="ck_trip_route_day_buffer",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    trip_plan_id: Mapped[UUID] = mapped_column(
        ForeignKey("trip_plans.id", ondelete="CASCADE"), index=True
    )
    day_date: Mapped[date] = mapped_column(Date, index=True)
    default_travel_mode: Mapped[str] = mapped_column(String(16), default="transit")
    default_buffer_minutes: Mapped[int] = mapped_column(Integer, default=10)
    route_preference: Mapped[str] = mapped_column(String(32), default="FEWER_TRANSFERS")
    auto_compute: Mapped[bool] = mapped_column(Boolean, default=True)


class TripRouteSegment(Timestamped, Base):
    __tablename__ = "trip_route_segments"
    __table_args__ = (
        UniqueConstraint(
            "trip_plan_id",
            "from_item_id",
            "to_item_id",
            name="uq_trip_route_segment_pair",
        ),
        CheckConstraint(
            "travel_mode IN ('transit', 'walk', 'drive')",
            name="ck_trip_route_segment_mode",
        ),
        CheckConstraint(
            "buffer_minutes >= 0 AND buffer_minutes <= 180",
            name="ck_trip_route_segment_buffer",
        ),
        CheckConstraint("duration_minutes > 0", name="ck_trip_route_segment_duration"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    trip_plan_id: Mapped[UUID] = mapped_column(
        ForeignKey("trip_plans.id", ondelete="CASCADE"), index=True
    )
    day_date: Mapped[date] = mapped_column(Date, index=True)
    from_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("trip_plan_items.id", ondelete="CASCADE"), index=True
    )
    to_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("trip_plan_items.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[str] = mapped_column(String(24), default="resolved")
    travel_mode: Mapped[str] = mapped_column(String(16), default="transit")
    is_override: Mapped[bool] = mapped_column(Boolean, default=False)
    provider: Mapped[str] = mapped_column(String(64))
    attribution: Mapped[str] = mapped_column(String(255))
    preference: Mapped[str] = mapped_column(String(32), default="FEWER_TRANSFERS")
    schedule_mode: Mapped[str] = mapped_column(String(24), default="scheduled")
    requested_departure_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    departure_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    arrival_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ready_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    buffer_minutes: Mapped[int] = mapped_column(Integer, default=10)
    distance_meters: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fare: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    encoded_polyline: Mapped[str | None] = mapped_column(Text, nullable=True)
    maps_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    steps: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    details_available: Mapped[list[str]] = mapped_column(JSON, default=list)
    warnings: Mapped[list[str]] = mapped_column(JSON, default=list)
    manual_note: Mapped[str | None] = mapped_column(String(255), nullable=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class TripShare(Timestamped, Base):
    __tablename__ = "trip_shares"
    __table_args__ = (UniqueConstraint("trip_plan_id", name="uq_trip_share_trip"),)
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    trip_plan_id: Mapped[UUID] = mapped_column(
        ForeignKey("trip_plans.id", ondelete="CASCADE"), index=True
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class OptimizationScoreRecord(Base):
    __tablename__ = "optimization_scores"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    trip_plan_id: Mapped[UUID] = mapped_column(
        ForeignKey("trip_plans.id", ondelete="CASCADE"), index=True
    )
    profile: Mapped[str] = mapped_column(String(32))
    total_score: Mapped[Decimal] = mapped_column(Numeric(8, 4))
    components: Mapped[dict[str, Any]] = mapped_column(JSON)


class PriceComponentRecord(Base):
    __tablename__ = "price_components"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    trip_plan_id: Mapped[UUID] = mapped_column(
        ForeignKey("trip_plans.id", ondelete="CASCADE"), index=True
    )
    category: Mapped[str] = mapped_column(String(64))
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3), default="TWD")
    confidence: Mapped[str] = mapped_column(String(16))


class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    resource_type: Mapped[str] = mapped_column(String(32))
    resource_id: Mapped[UUID] = mapped_column(index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3), default="TWD")
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class PriceAlert(Timestamped, Base):
    __tablename__ = "price_alerts"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "resource_type", "resource_id", name="uq_price_alert_user_resource"
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    resource_type: Mapped[str] = mapped_column(String(32))
    resource_id: Mapped[UUID] = mapped_column(index=True)
    target_price: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="TWD")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    provider: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    monitoring_mode: Mapped[str] = mapped_column(String(24), default="manual_only", index=True)
    monitoring_status: Mapped[str] = mapped_column(String(32), default="manual_only", index=True)
    monitor_key: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    baseline_price: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    last_observed_price: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    last_notified_price: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_check_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    armed: Mapped[bool] = mapped_column(Boolean, default=True)
    consecutive_failures: Mapped[int] = mapped_column(Integer, default=0)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class LineConnection(Timestamped, Base):
    __tablename__ = "line_connections"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True
    )
    line_user_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(255))
    friend_status: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    linked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    last_delivery_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_delivery_error: Mapped[str | None] = mapped_column(Text, nullable=True)


class PriceAlertCheck(Base):
    __tablename__ = "price_alert_checks"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    alert_id: Mapped[UUID] = mapped_column(
        ForeignKey("price_alerts.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[str] = mapped_column(String(32), index=True)
    previous_price: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    observed_price: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="TWD")
    provider: Mapped[str | None] = mapped_column(String(64), nullable=True)
    detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, index=True
    )


class AlertNotificationDelivery(Base):
    __tablename__ = "alert_notification_deliveries"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    alert_id: Mapped[UUID] = mapped_column(
        ForeignKey("price_alerts.id", ondelete="CASCADE"), index=True
    )
    line_connection_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("line_connections.id", ondelete="SET NULL"), nullable=True, index=True
    )
    dedupe_key: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    event_type: Mapped[str] = mapped_column(String(32))
    observed_price: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    status: Mapped[str] = mapped_column(String(24), default="pending", index=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    next_attempt_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class ProviderHealth(Timestamped, Base):
    __tablename__ = "provider_health"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    provider: Mapped[str] = mapped_column(String(64), unique=True)
    status: Mapped[str] = mapped_column(String(32), default="healthy")
    consecutive_failures: Mapped[int] = mapped_column(Integer, default=0)
    circuit_open_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class ProviderConfig(Timestamped, Base):
    __tablename__ = "provider_configs"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    provider: Mapped[str] = mapped_column(String(64), unique=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    priority: Mapped[int] = mapped_column(Integer, default=100)
    config: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    secret_config_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    last_tested_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_test_status: Mapped[str | None] = mapped_column(String(32), nullable=True)
    last_test_message: Mapped[str | None] = mapped_column(Text, nullable=True)


class AdminAuditLog(Base):
    __tablename__ = "admin_audit_logs"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    actor_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    action: Mapped[str] = mapped_column(String(64), index=True)
    target: Mapped[str] = mapped_column(String(128), index=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


DEPLOYMENT_STATUSES = (
    "queued",
    "preflight",
    "building",
    "backing_up",
    "migrating",
    "activating",
    "verifying",
    "rolling_back",
    "succeeded",
    "failed",
    "rolled_back",
    "manual_intervention_required",
)
ACTIVE_DEPLOYMENT_STATUSES = DEPLOYMENT_STATUSES[:8]


class DeploymentRun(Timestamped, Base):
    __tablename__ = "deployment_runs"
    __table_args__ = (
        UniqueConstraint(
            "requested_by_user_id",
            "idempotency_key",
            name="uq_deployment_request_idempotency",
        ),
        CheckConstraint(
            "status IN (" + ", ".join(f"'{status}'" for status in DEPLOYMENT_STATUSES) + ")",
            name="ck_deployment_run_status",
        ),
        Index(
            "uq_deployment_one_active",
            text("(1)"),
            unique=True,
            postgresql_where=text(
                "status IN ("
                + ", ".join(f"'{status}'" for status in ACTIVE_DEPLOYMENT_STATUSES)
                + ")"
            ),
            sqlite_where=text(
                "status IN ("
                + ", ".join(f"'{status}'" for status in ACTIVE_DEPLOYMENT_STATUSES)
                + ")"
            ),
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    requested_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    idempotency_key: Mapped[str] = mapped_column(String(255))
    agent_job_id: Mapped[str | None] = mapped_column(String(64), nullable=True, unique=True)
    status: Mapped[str] = mapped_column(String(32), default="queued", index=True)
    stage: Mapped[str] = mapped_column(String(32), default="queued")
    previous_sha: Mapped[str | None] = mapped_column(String(40), nullable=True)
    target_sha: Mapped[str] = mapped_column(String(40), index=True)
    target_commit_subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ci_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    backup_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    rollback_status: Mapped[str | None] = mapped_column(String(32), nullable=True)
    failure_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    failure_detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class DeploymentEvent(Base):
    __tablename__ = "deployment_events"
    __table_args__ = (UniqueConstraint("run_id", "sequence", name="uq_deployment_event_sequence"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    run_id: Mapped[UUID] = mapped_column(
        ForeignKey("deployment_runs.id", ondelete="CASCADE"), index=True
    )
    sequence: Mapped[int] = mapped_column(Integer)
    stage: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32))
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
