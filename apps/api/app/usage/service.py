from calendar import monthrange
from datetime import UTC, date, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Plan, PlanEntitlement, Subscription, UsageLedger, UsageReservation, User
from app.problems import AppError

PLAN_DEFAULTS: dict[str, dict[str, Any]] = {
    "FREE": {
        "name": "免費版",
        "credits": 20,
        "price_twd": 0,
        "entitlements": {"saved_trips": 1, "price_alerts": 1, "full_trip_trials": 1},
    },
    "PRO": {
        "name": "專業版",
        "credits": 200,
        "price_twd": 299,
        "entitlements": {"saved_trips": 20, "price_alerts": 20, "full_trip_trials": 200},
    },
}


def period_for(day: date) -> tuple[date, date]:
    start = day.replace(day=1)
    end = day.replace(day=monthrange(day.year, day.month)[1])
    return start, end


def search_operation_cost(payload: dict[str, Any]) -> tuple[str, int]:
    if payload.get("trip_type") == "multi_city":
        return "multi_city_optimization", 15
    modules = set(payload.get("modules", []))
    if payload.get("preferences", {}).get("optimization_mode") and len(modules) >= 3:
        return "full_trip_optimization", 10
    if modules == {"flight", "hotel"}:
        return "flight_hotel_search", 5
    if payload.get("flexible_dates") and "flight" in modules:
        return "flexible_flight_search", 4
    return "fixed_search", max(1, len(modules))


async def seed_plans(session: AsyncSession) -> None:
    for code, defaults in PLAN_DEFAULTS.items():
        plan = await session.scalar(select(Plan).where(Plan.code == code))
        if plan is None:
            plan = Plan(
                code=code,
                name=str(defaults["name"]),
                monthly_credits=int(defaults["credits"]),
                price_twd=int(defaults["price_twd"]),
            )
            session.add(plan)
            await session.flush()
            for key, value in dict(defaults["entitlements"]).items():
                session.add(PlanEntitlement(plan_id=plan.id, key=key, value=value))


async def create_free_subscription(session: AsyncSession, user: User) -> Subscription:
    await seed_plans(session)
    plan = await session.scalar(select(Plan).where(Plan.code == "FREE"))
    if plan is None:
        raise RuntimeError("FREE plan seed failed")
    start, end = period_for(datetime.now(UTC).date())
    subscription = Subscription(
        user_id=user.id,
        plan_id=plan.id,
        credit_balance=plan.monthly_credits,
        period_start=start,
        period_end=end,
    )
    session.add(subscription)
    await session.flush()
    session.add(
        UsageLedger(
            user_id=user.id,
            subscription_id=subscription.id,
            entry_type="grant",
            amount=plan.monthly_credits,
            balance_after=plan.monthly_credits,
            reference=f"monthly:{start.isoformat()}",
            metadata_json={"plan": plan.code},
        )
    )
    return subscription


async def get_subscription(
    session: AsyncSession, user_id: UUID, lock: bool = False
) -> Subscription:
    statement = select(Subscription).where(Subscription.user_id == user_id)
    if lock:
        statement = statement.with_for_update()
    subscription = await session.scalar(statement)
    if subscription is None:
        raise AppError(409, "subscription_missing", "No active subscription was found")
    return subscription


async def reserve_credits(
    session: AsyncSession,
    user_id: UUID,
    idempotency_key: str,
    operation: str,
    credits: int,
) -> tuple[UsageReservation, bool]:
    subscription = await get_subscription(session, user_id, lock=True)
    existing = await session.scalar(
        select(UsageReservation).where(
            UsageReservation.user_id == user_id,
            UsageReservation.idempotency_key == idempotency_key,
        )
    )
    if existing is not None:
        return existing, False
    if subscription.credit_balance < credits:
        raise AppError(402, "insufficient_credits", "There are not enough credits for this request")
    subscription.credit_balance -= credits
    reservation = UsageReservation(
        user_id=user_id,
        subscription_id=subscription.id,
        idempotency_key=idempotency_key,
        operation=operation,
        credits=credits,
    )
    session.add(reservation)
    await session.flush()
    session.add(
        UsageLedger(
            user_id=user_id,
            subscription_id=subscription.id,
            entry_type="debit",
            amount=-credits,
            balance_after=subscription.credit_balance,
            reference=str(reservation.id),
            metadata_json={"operation": operation, "idempotency_key": idempotency_key},
        )
    )
    return reservation, True


async def commit_reservation(
    session: AsyncSession, reservation: UsageReservation, resource_id: UUID
) -> None:
    reservation.status = "committed"
    reservation.resource_id = resource_id


async def release_reservation(session: AsyncSession, reservation: UsageReservation) -> None:
    if reservation.status != "reserved":
        return
    subscription = await get_subscription(session, reservation.user_id, lock=True)
    subscription.credit_balance += reservation.credits
    reservation.status = "released"
    session.add(
        UsageLedger(
            user_id=reservation.user_id,
            subscription_id=subscription.id,
            entry_type="refund",
            amount=reservation.credits,
            balance_after=subscription.credit_balance,
            reference=str(reservation.id),
            metadata_json={"operation": reservation.operation},
        )
    )
