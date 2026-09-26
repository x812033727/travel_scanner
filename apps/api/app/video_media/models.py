"""One generation the pipeline asked a vendor for: what was asked, where it stands, what it cost.

The API has no background process, so a job moves only when the tool polls it (``jobs.py``):
a row is written before the vendor is called, and every state change is committed, so a
restart between two polls loses nothing and a vendor call is never repeated for the same
request. The month's spend is the sum of ``usd_estimate`` over these rows.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

KINDS = ("image", "clip", "music")
STATUSES = ("queued", "submitted", "ready", "failed", "expired")
LIVE_STATUSES = ("queued", "submitted", "ready")
MAX_ATTEMPTS = 3


def utcnow() -> datetime:
    return datetime.now(UTC)


class VideoMediaJob(Base):
    __tablename__ = "video_media_jobs"
    __table_args__ = (
        UniqueConstraint("slug", "request_hash", name="uq_video_media_job_request"),
        CheckConstraint("kind IN ('image', 'clip', 'music')", name="ck_video_media_job_kind"),
        CheckConstraint(
            "status IN ('queued', 'submitted', 'ready', 'failed', 'expired')",
            name="ck_video_media_job_status",
        ),
        Index("ix_video_media_jobs_created", "created_at"),
        Index("ix_video_media_jobs_status", "status"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(80), index=True)
    kind: Mapped[str] = mapped_column(String(8))
    purpose: Mapped[str] = mapped_column(String(24))
    shot_id: Mapped[str | None] = mapped_column(String(60), nullable=True)
    provider: Mapped[str] = mapped_column(String(16))
    model: Mapped[str] = mapped_column(String(128))
    # The request as the vendor adapter needs it, minus the reference bytes (those are files
    # in the store, named in ``references``), so a queued job can be submitted after a restart.
    request: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    request_hash: Mapped[str] = mapped_column(String(64))
    idempotency_key: Mapped[str | None] = mapped_column(String(80), nullable=True)
    status: Mapped[str] = mapped_column(String(12), default="queued")
    attempts: Mapped[int] = mapped_column(Integer, default=1)
    vendor_ref: Mapped[str | None] = mapped_column(String(512), nullable=True)
    seconds: Mapped[int] = mapped_column(Integer, default=0)
    file_sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    file_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    content_type: Mapped[str | None] = mapped_column(String(32), nullable=True)
    usd_estimate: Mapped[Decimal] = mapped_column(Numeric(10, 4), default=Decimal("0"))
    error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error_detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    polls: Mapped[int] = mapped_column(Integer, default=0)
    token_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("video_tool_tokens.id", ondelete="SET NULL"), nullable=True
    )
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ready_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
