from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated, Any, Literal, cast
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.alerts.monitoring import automatic_monitoring_supported, monitor_identity
from app.auth.service import CurrentUser
from app.db import get_session
from app.models import (
    FlightOfferRecord,
    HotelOfferRecord,
    PriceAlert,
    SearchRequest,
    TripPlan,
)
from app.problems import AppError
from app.trips.router import limit_for

router = APIRouter(prefix="/alerts", tags=["alerts"])
Session = Annotated[AsyncSession, Depends(get_session)]
ResourceType = Literal["flight", "hotel", "trip"]


class AlertCreate(BaseModel):
    resource_type: ResourceType
    resource_id: UUID
    target_price: Decimal | None = Field(default=None, gt=0)


class AlertPatch(BaseModel):
    target_price: Decimal | None = Field(default=None, gt=0)
    active: bool | None = None


class AlertResponse(BaseModel):
    id: UUID
    resource_type: ResourceType
    resource_id: UUID
    target_price: Decimal | None
    currency: str
    active: bool
    created_at: datetime
    updated_at: datetime
    title: str
    subtitle: str | None
    current_price: Decimal | None
    price_updated_at: datetime | None
    source_mode: str | None
    monitoring_mode: str
    monitoring_status: str
    last_checked_at: datetime | None
    next_check_at: datetime | None


@dataclass(frozen=True)
class ResourceSnapshot:
    title: str
    subtitle: str | None
    current_price: Decimal | None
    currency: str
    price_updated_at: datetime | None
    source_mode: str | None
    provider: str | None
    monitoring_mode: str
    monitor_key: dict[str, Any]


def _text(data: dict[str, Any], key: str, fallback: str = "") -> str:
    value = data.get(key)
    return value.strip() if isinstance(value, str) and value.strip() else fallback


def _data_timestamp(data: dict[str, Any], fallback: datetime) -> datetime:
    for key in ("last_verified_at", "retrieved_at"):
        value = data.get(key)
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                pass
    return fallback


async def resource_snapshot(
    session: AsyncSession,
    user_id: UUID,
    resource_type: ResourceType,
    resource_id: UUID,
) -> ResourceSnapshot | None:
    if resource_type == "trip":
        trip = await session.scalar(
            select(TripPlan).where(TripPlan.id == resource_id, TripPlan.user_id == user_id)
        )
        if trip is None:
            return None
        return ResourceSnapshot(
            title=trip.name,
            subtitle=trip.destination_name,
            current_price=trip.total_price if trip.total_price > 0 else None,
            currency=trip.currency,
            price_updated_at=trip.updated_at,
            source_mode="saved_trip",
            provider=None,
            monitoring_mode="manual_only",
            monitor_key={},
        )

    if resource_type == "flight":
        record = await session.scalar(
            select(FlightOfferRecord)
            .join(SearchRequest, FlightOfferRecord.search_id == SearchRequest.id)
            .where(
                FlightOfferRecord.public_offer_id == resource_id,
                SearchRequest.user_id == user_id,
            )
            .order_by(FlightOfferRecord.updated_at.desc())
            .limit(1)
        )
    else:
        record = await session.scalar(
            select(HotelOfferRecord)
            .join(SearchRequest, HotelOfferRecord.search_id == SearchRequest.id)
            .where(
                HotelOfferRecord.public_offer_id == resource_id,
                SearchRequest.user_id == user_id,
            )
            .order_by(HotelOfferRecord.updated_at.desc())
            .limit(1)
        )
    if record is None:
        return None
    data = record.data or {}
    if resource_type == "flight":
        title = _text(data, "marketing_airline", _text(data, "airline", "航班價格"))
        origin = _text(data, "origin")
        destination = _text(data, "destination")
        subtitle = f"{origin} → {destination}" if origin and destination else None
    else:
        title = _text(data, "hotel_name", "住宿價格")
        subtitle = _text(data, "address") or None
    return ResourceSnapshot(
        title=title,
        subtitle=subtitle,
        current_price=record.total_price,
        currency=record.currency,
        price_updated_at=_data_timestamp(data, record.updated_at),
        source_mode=_text(data, "source_mode") or None,
        provider=record.provider,
        monitoring_mode=(
            "automatic"
            if automatic_monitoring_supported(resource_type, record.provider)
            else "manual_only"
        ),
        monitor_key=monitor_identity(resource_type, data),
    )


def serialize(alert: PriceAlert, snapshot: ResourceSnapshot | None) -> AlertResponse:
    missing = ResourceSnapshot(
        title="來源已不存在",
        subtitle="這筆通知仍可刪除，但目前無法取得原始項目。",
        current_price=None,
        currency=alert.currency,
        price_updated_at=None,
        source_mode=None,
        provider=alert.provider,
        monitoring_mode=alert.monitoring_mode,
        monitor_key=alert.monitor_key,
    )
    value = snapshot or missing
    return AlertResponse(
        id=alert.id,
        resource_type=cast(ResourceType, alert.resource_type),
        resource_id=alert.resource_id,
        target_price=alert.target_price,
        currency=alert.currency,
        active=alert.active,
        created_at=alert.created_at,
        updated_at=alert.updated_at,
        title=value.title,
        subtitle=value.subtitle,
        current_price=(
            alert.last_observed_price
            if alert.last_observed_price is not None
            else value.current_price
        ),
        price_updated_at=alert.last_checked_at or value.price_updated_at,
        source_mode=value.source_mode,
        monitoring_mode=alert.monitoring_mode,
        monitoring_status=alert.monitoring_status,
        last_checked_at=alert.last_checked_at,
        next_check_at=alert.next_check_at,
    )


async def owned_alert(session: AsyncSession, user_id: UUID, alert_id: UUID) -> PriceAlert:
    alert = await session.scalar(
        select(PriceAlert).where(PriceAlert.id == alert_id, PriceAlert.user_id == user_id)
    )
    if alert is None:
        raise AppError(404, "alert_not_found", "找不到這筆價格通知")
    return alert


@router.post("", response_model=AlertResponse, status_code=201)
async def create_alert(
    payload: AlertCreate, user: CurrentUser, session: Session
) -> AlertResponse:
    snapshot = await resource_snapshot(session, user.id, payload.resource_type, payload.resource_id)
    if snapshot is None:
        raise AppError(404, "alert_resource_not_found", "找不到可追蹤的價格項目")
    existing = await session.scalar(
        select(PriceAlert).where(
            PriceAlert.user_id == user.id,
            PriceAlert.resource_type == payload.resource_type,
            PriceAlert.resource_id == payload.resource_id,
        )
    )
    if existing is not None:
        raise AppError(409, "alert_exists", "這個項目已經建立價格通知")
    count = await session.scalar(
        select(func.count())
        .select_from(PriceAlert)
        .where(PriceAlert.user_id == user.id, PriceAlert.active.is_(True))
    )
    if int(count or 0) >= await limit_for(session, user.id, "price_alerts"):
        raise AppError(403, "alert_limit_reached", "已達 20 筆價格通知上限")
    alert = PriceAlert(
        user_id=user.id,
        resource_type=payload.resource_type,
        resource_id=payload.resource_id,
        target_price=payload.target_price,
        currency=snapshot.currency,
        provider=snapshot.provider,
        monitoring_mode=snapshot.monitoring_mode,
        monitoring_status=(
            "scheduled" if snapshot.monitoring_mode == "automatic" else "manual_only"
        ),
        monitor_key=snapshot.monitor_key,
        baseline_price=snapshot.current_price,
        last_observed_price=snapshot.current_price,
        next_check_at=(datetime.now(UTC) if snapshot.monitoring_mode == "automatic" else None),
    )
    session.add(alert)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise AppError(409, "alert_exists", "這個項目已經建立價格通知") from exc
    await session.refresh(alert)
    return serialize(alert, snapshot)


@router.get("", response_model=list[AlertResponse])
async def list_alerts(user: CurrentUser, session: Session) -> list[AlertResponse]:
    alerts = list(
        (
            await session.scalars(
                select(PriceAlert)
                .where(PriceAlert.user_id == user.id)
                .order_by(PriceAlert.created_at.desc())
            )
        ).all()
    )
    return [
        serialize(
            alert,
            await resource_snapshot(
                session,
                user.id,
                cast(ResourceType, alert.resource_type),
                alert.resource_id,
            ),
        )
        for alert in alerts
    ]


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: UUID, user: CurrentUser, session: Session) -> AlertResponse:
    alert = await owned_alert(session, user.id, alert_id)
    snapshot = await resource_snapshot(
        session, user.id, cast(ResourceType, alert.resource_type), alert.resource_id
    )
    return serialize(alert, snapshot)


@router.patch("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: UUID, payload: AlertPatch, user: CurrentUser, session: Session
) -> AlertResponse:
    if not payload.model_fields_set:
        raise AppError(422, "alert_update_empty", "請至少修改一個價格通知欄位")
    alert = await owned_alert(session, user.id, alert_id)
    if "target_price" in payload.model_fields_set:
        alert.target_price = payload.target_price
        alert.armed = True
        if alert.active and alert.monitoring_mode == "automatic":
            alert.next_check_at = datetime.now(UTC)
    if "active" in payload.model_fields_set and payload.active is not None:
        if payload.active and not alert.active:
            count = await session.scalar(
                select(func.count())
                .select_from(PriceAlert)
                .where(PriceAlert.user_id == user.id, PriceAlert.active.is_(True))
            )
            if int(count or 0) >= await limit_for(session, user.id, "price_alerts"):
                raise AppError(403, "alert_limit_reached", "已達 20 筆價格通知上限")
        alert.active = payload.active
        if alert.active and alert.monitoring_mode == "automatic":
            alert.monitoring_status = "scheduled"
            alert.next_check_at = datetime.now(UTC)
        elif not alert.active and alert.monitoring_mode == "automatic":
            alert.monitoring_status = "paused"
            alert.next_check_at = None
    await session.commit()
    await session.refresh(alert)
    snapshot = await resource_snapshot(
        session, user.id, cast(ResourceType, alert.resource_type), alert.resource_id
    )
    return serialize(alert, snapshot)


@router.delete("/{alert_id}", status_code=204)
async def delete_alert(alert_id: UUID, user: CurrentUser, session: Session) -> None:
    alert = await owned_alert(session, user.id, alert_id)
    await session.delete(alert)
    await session.commit()
