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


class FlightOfferRecord(Timestamped, Base):
    __tablename__ = "flight_offers"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    search_id: Mapped[UUID] = mapped_column(
        ForeignKey("search_requests.id", ondelete="CASCADE"), index=True
    )
    provider: Mapped[str] = mapped_column(String(64))
    provider_offer_id: Mapped[str] = mapped_column(String(128))
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
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    resource_type: Mapped[str] = mapped_column(String(32))
    resource_id: Mapped[UUID] = mapped_column(index=True)
    target_price: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="TWD")
    active: Mapped[bool] = mapped_column(Boolean, default=True)


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
