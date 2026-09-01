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
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
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


class UsagePackage(Timestamped, Base):
    __tablename__ = "usage_packages"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    uses: Mapped[int] = mapped_column(Integer)
    price_twd: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    purchasable: Mapped[bool] = mapped_column(Boolean, default=False)


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
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    city_code: Mapped[str] = mapped_column(String(8), index=True)
    city_name: Mapped[str] = mapped_column(String(100))
    country_code: Mapped[str] = mapped_column(String(2), index=True)
    country_name: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(32), index=True)
    search_text: Mapped[str] = mapped_column(Text)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    wikipedia_project: Mapped[str | None] = mapped_column(String(64), nullable=True)
    wikipedia_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    google_place_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
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
    locked: Mapped[bool] = mapped_column(Boolean, default=False)
    is_estimated: Mapped[bool] = mapped_column(Boolean, default=False)
    data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    provider_place_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location_source: Mapped[str | None] = mapped_column(String(32), nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    fixed_time: Mapped[bool] = mapped_column(Boolean, default=False)


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
