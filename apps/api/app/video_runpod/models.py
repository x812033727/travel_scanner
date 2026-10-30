"""One row per RunPod pod the site started for a video tool (migration 0144).

The row is written before RunPod is asked, so a pod whose answer was lost still has a row the
reaper can find. ``stopped_at`` and ``stop_reason`` are set together; ``usd`` is settled from
the pod's hourly price and how long it ran.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

STOP_REASONS: tuple[str, ...] = ("manual", "idle", "max_hours", "cap", "gone", "failed")


def utcnow() -> datetime:
    return datetime.now(UTC)


class VideoRunpodSession(Base):
    __tablename__ = "video_runpod_sessions"
    __table_args__ = (
        CheckConstraint(
            "stop_reason IS NULL OR stop_reason IN "
            "('manual', 'idle', 'max_hours', 'cap', 'gone', 'failed')",
            name="ck_video_runpod_sessions_stop_reason",
        ),
        CheckConstraint(
            "(stopped_at IS NULL) = (stop_reason IS NULL)",
            name="ck_video_runpod_sessions_stopped",
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    token_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("video_tool_tokens.id", ondelete="SET NULL"), nullable=True, index=True
    )
    # Null only between the row being written and RunPod answering the create.
    pod_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    label: Mapped[str] = mapped_column(String(80))
    slug: Mapped[str | None] = mapped_column(String(120), nullable=True)
    gpu: Mapped[str] = mapped_column(String(64))
    cloud_type: Mapped[str] = mapped_column(String(16))
    data_center_id: Mapped[str | None] = mapped_column(String(16), nullable=True)
    cost_per_hr: Mapped[Decimal | None] = mapped_column(Numeric(8, 4), nullable=True)
    # SHA-256 of the one-time token the pod's gate accepts; the token itself is returned once.
    gate_token_hash: Mapped[str] = mapped_column(String(64))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    last_heartbeat_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    stopped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    stop_reason: Mapped[str | None] = mapped_column(String(16), nullable=True)
    usd: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
