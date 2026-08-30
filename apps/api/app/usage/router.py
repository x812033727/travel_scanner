from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.db import get_session
from app.models import Plan, PlanEntitlement, Subscription

router = APIRouter(tags=["plans"])
Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("/plans")
async def list_plans(session: Session) -> list[dict[str, Any]]:
    plans = list((await session.scalars(select(Plan).order_by(Plan.price_twd))).all())
    result: list[dict[str, Any]] = []
    for plan in plans:
        entitlements = list(
            (
                await session.scalars(
                    select(PlanEntitlement).where(PlanEntitlement.plan_id == plan.id)
                )
            ).all()
        )
        result.append(
            {
                "code": plan.code,
                "name": plan.name,
                "monthly_credits": plan.monthly_credits,
                "price_twd": plan.price_twd,
                "entitlements": {item.key: item.value for item in entitlements},
            }
        )
    return result


@router.get("/usage")
async def usage(user: CurrentUser, session: Session) -> dict[str, Any]:
    row = (
        await session.execute(
            select(Subscription, Plan)
            .join(Plan, Subscription.plan_id == Plan.id)
            .where(Subscription.user_id == user.id)
        )
    ).one()
    subscription, plan = row
    return {
        "plan": plan.code,
        "credits_remaining": subscription.credit_balance,
        "monthly_credits": plan.monthly_credits,
        "period_start": subscription.period_start,
        "period_end": subscription.period_end,
    }
