from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import JSON, Boolean, CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class DiscoveryPreference(Base):
    __tablename__ = "discovery_preferences"
    __table_args__ = (CheckConstraint("version >= 1", name="ck_discovery_preference_version"),)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    version: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    destinations: Mapped[list[str]] = mapped_column(JSON, default=list)
    topics: Mapped[list[str]] = mapped_column(JSON, default=list)
    include_saved: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    include_following: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )


class DiscoveryDismissal(Base):
    __tablename__ = "discovery_dismissals"
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    content_key: Mapped[str] = mapped_column(String(64), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
