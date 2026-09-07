from __future__ import annotations

from datetime import date, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import JSON, CheckConstraint, Date, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.community.models import Timestamped
from app.db import Base


class PetPlace(Timestamped, Base):
    __tablename__ = "pet_places"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','approved','rejected','disabled')", name="ck_pet_place_status"
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    identity_key: Mapped[str | None] = mapped_column(String(200), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(160))
    names: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    kind: Mapped[str] = mapped_column(String(20), index=True)
    country: Mapped[str] = mapped_column(String(2), index=True)
    destination: Mapped[str] = mapped_column(String(160), index=True)
    address: Mapped[str] = mapped_column(String(400), default="")
    official_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    latitude: Mapped[float | None] = mapped_column(nullable=True)
    longitude: Mapped[float | None] = mapped_column(nullable=True)
    coordinate_source_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    status: Mapped[str] = mapped_column(String(16), default="pending", index=True)
    policies: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    source_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    verified_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    disputed: Mapped[bool] = mapped_column(default=False)
    version: Mapped[int] = mapped_column(default=1)


class PlaceReference(Base):
    __tablename__ = "pet_place_references"
    __table_args__ = (UniqueConstraint("kind", "target", name="uq_pet_place_reference"),)
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    place_id: Mapped[UUID] = mapped_column(ForeignKey("pet_places.id"), index=True)
    kind: Mapped[str] = mapped_column(String(20))
    target: Mapped[str] = mapped_column(String(160))


class PetReport(Timestamped, Base):
    __tablename__ = "pet_reports"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    place_id: Mapped[UUID] = mapped_column(ForeignKey("pet_places.id"), index=True)
    reporter_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    body: Mapped[str] = mapped_column(String(2000))
    source_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    visited_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    media_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    proposed_policies: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(16), default="pending", index=True)


class PetHistory(Timestamped, Base):
    __tablename__ = "pet_policy_history"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    place_id: Mapped[UUID] = mapped_column(ForeignKey("pet_places.id"), index=True)
    actor_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    before: Mapped[dict[str, Any]] = mapped_column(JSON)
    after: Mapped[dict[str, Any]] = mapped_column(JSON)
    reason: Mapped[str] = mapped_column(String(1000))
