from decimal import Decimal
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.db import get_session
from app.models import PriceAlert
from app.problems import AppError
from app.trips.router import limit_for

router = APIRouter(prefix="/alerts", tags=["alerts"])
Session = Annotated[AsyncSession, Depends(get_session)]


class AlertCreate(BaseModel):
    resource_type: str
    resource_id: UUID
    target_price: Decimal | None = None


def serialize(alert: PriceAlert) -> dict[str, Any]:
    return {
        "id": str(alert.id),
        "resource_type": alert.resource_type,
        "resource_id": str(alert.resource_id),
        "target_price": alert.target_price,
        "currency": alert.currency,
        "active": alert.active,
        "created_at": alert.created_at,
    }


@router.post("", status_code=201)
async def create_alert(payload: AlertCreate, user: CurrentUser, session: Session) -> dict[str, Any]:
    if payload.resource_type not in {"flight", "hotel", "trip"}:
        raise AppError(422, "invalid_alert_type", "Alert type must be flight, hotel, or trip")
    count = await session.scalar(
        select(func.count())
        .select_from(PriceAlert)
        .where(PriceAlert.user_id == user.id, PriceAlert.active.is_(True))
    )
    if int(count or 0) >= await limit_for(session, user.id, "price_alerts"):
        raise AppError(
            403, "alert_limit_reached", "已達所有會員共用的 20 筆價格通知上限"
        )
    alert = PriceAlert(user_id=user.id, **payload.model_dump())
    session.add(alert)
    await session.commit()
    await session.refresh(alert)
    return serialize(alert)


@router.get("")
async def list_alerts(user: CurrentUser, session: Session) -> list[dict[str, Any]]:
    alerts = list(
        (
            await session.scalars(
                select(PriceAlert)
                .where(PriceAlert.user_id == user.id)
                .order_by(PriceAlert.created_at.desc())
            )
        ).all()
    )
    return [serialize(alert) for alert in alerts]


@router.get("/{alert_id}")
async def get_alert(alert_id: UUID, user: CurrentUser, session: Session) -> dict[str, Any]:
    alert = await session.scalar(
        select(PriceAlert).where(PriceAlert.id == alert_id, PriceAlert.user_id == user.id)
    )
    if alert is None:
        raise AppError(404, "alert_not_found", "Price alert was not found")
    return serialize(alert)


@router.delete("/{alert_id}", status_code=204)
async def delete_alert(alert_id: UUID, user: CurrentUser, session: Session) -> None:
    alert = await session.scalar(
        select(PriceAlert).where(PriceAlert.id == alert_id, PriceAlert.user_id == user.id)
    )
    if alert is None:
        raise AppError(404, "alert_not_found", "Price alert was not found")
    await session.delete(alert)
    await session.commit()
