"""One locked account and one durable operation row per billable pilot request.

Every service mutation locks the account row first. PostgreSQL serializes reservations for a
slug on that row, while operation rows retain the price ceiling, outcome, and reconciliation
receipt across process restarts. An uncertain outcome remains charged against the ceiling.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


PILOT_LIMIT_USD = Decimal("25.000000")
FOLLOWON_LIMIT_USD = Decimal("5.000000")
FOLLOWON_SLUGS = frozenset(
    (
        "story-five-lego-legoland",
        "story-five-costco-hot-dog",
        "story-five-adidas-puma-brothers",
        "story-five-ajinomoto-chip-film",
        "story-five-pringles-vat-case",
    )
)
# Register follow-on stories before their accounts exist, so a rollback cannot silently
# send one of their paid calls without a durable per-film reservation.
PILOT_LIMITS_USD = {
    "story-rolling-suitcase": PILOT_LIMIT_USD,
    "story-conveyor-belt-sushi": PILOT_LIMIT_USD,
    "story-rolling-suitcase-v2": PILOT_LIMIT_USD,
    "story-conveyor-belt-sushi-v2": FOLLOWON_LIMIT_USD,
    **{slug: FOLLOWON_LIMIT_USD for slug in FOLLOWON_SLUGS},
}
# The everyday-object series has its own per-film USD 25 accounts (0138). PILOT_LIMITS_USD
# stays the reviewed 0133 set the migration guard reads back for the 0132 rollback image.
EVERYDAY_STORY_PREFIX = "story-everyday-"
# These four called paid providers before they had accounts. 0138 opens each with one
# uncertain USD 25 hold for that unrecorded history, so nothing is spendable until an
# operator settles it against provider evidence (RECONCILE.md).
UNRECONCILED_STORY_SLUGS = frozenset(
    (
        "story-everyday-moleskine-c03",
        "story-everyday-bubble-wrap-c04",
        "story-everyday-kincho-c05",
        "story-everyday-play-doh-c06",
    )
)
HISTORICAL_HOLD_OPERATION_ID = "pre-ledger-history"
# Plus the owner-approved local pilots that made no paid call before their accounts existed.
EVERYDAY_PILOT_SLUGS = UNRECONCILED_STORY_SLUGS | frozenset(
    (
        "story-everyday-dr-martens-c07",
        "story-everyday-oxo-c10",
        "story-everyday-frixion-c15",
    )
)
BUDGET_LIMITS_USD = {
    **PILOT_LIMITS_USD,
    **{slug: PILOT_LIMIT_USD for slug in sorted(EVERYDAY_PILOT_SLUGS)},
}
PILOT_SLUGS = frozenset(BUDGET_LIMITS_USD)
OPERATION_STATUSES = ("reserved", "uncertain", "settled", "released")


class VideoPilotBudget(Base):
    __tablename__ = "video_pilot_budgets"
    # This application release serves both the current 0132 schema and the reviewed
    # 0133 rollback state. The actual database constraint is widened by 0133.
    __table_args__ = (
        CheckConstraint(
            "limit_usd IN (5.000000, 25.000000)", name="ck_video_pilot_budget_limit"
        ),
    )

    slug: Mapped[str] = mapped_column(String(80), primary_key=True)
    limit_usd: Mapped[Decimal] = mapped_column(Numeric(12, 6), default=PILOT_LIMIT_USD)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, server_default=func.now()
    )


class VideoPilotBudgetOperation(Base):
    __tablename__ = "video_pilot_budget_operations"
    __table_args__ = (
        UniqueConstraint("slug", "operation_id", name="uq_video_pilot_budget_operation"),
        CheckConstraint(
            "status IN ('reserved', 'uncertain', 'settled', 'released')",
            name="ck_video_pilot_budget_operation_status",
        ),
        CheckConstraint("max_usd > 0", name="ck_video_pilot_budget_operation_max"),
        CheckConstraint(
            "actual_usd IS NULL OR actual_usd >= 0",
            name="ck_video_pilot_budget_operation_actual",
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(
        ForeignKey("video_pilot_budgets.slug", ondelete="RESTRICT"), index=True
    )
    operation_id: Mapped[str] = mapped_column(String(160))
    category: Mapped[str] = mapped_column(String(40))
    provider: Mapped[str] = mapped_column(String(40))
    model: Mapped[str] = mapped_column(String(128))
    max_usd: Mapped[Decimal] = mapped_column(Numeric(12, 6))
    actual_usd: Mapped[Decimal | None] = mapped_column(Numeric(12, 6), nullable=True)
    status: Mapped[str] = mapped_column(String(12), default="reserved")
    attempts: Mapped[int] = mapped_column(Integer, default=1)
    receipt_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    release_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, server_default=func.now()
    )
