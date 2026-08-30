from typing import Any, Literal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UsageAccount, UsageLedger, UsagePackage, UsageReservation, User
from app.problems import AppError
from app.usage.schemas import UsageStatus

PACKAGE_DEFAULTS: dict[str, dict[str, Any]] = {
    "TRIAL_3": {
        "name": "註冊體驗",
        "uses": 3,
        "price_twd": 0,
        "purchasable": False,
    },
    "PACK_10": {
        "name": "輕量 10 次包",
        "uses": 10,
        "price_twd": 199,
        "purchasable": False,
    },
    "PACK_30": {
        "name": "常用 30 次包",
        "uses": 30,
        "price_twd": 499,
        "purchasable": False,
    },
    "PACK_100": {
        "name": "大量 100 次包",
        "uses": 100,
        "price_twd": 1299,
        "purchasable": False,
    },
}

COMMON_LIMITS = {"saved_trips": 20, "price_alerts": 20}


def search_operation(payload: dict[str, Any]) -> str:
    if payload.get("trip_type") == "multi_city":
        return "multi_city_search"
    modules = set(payload.get("modules", []))
    if payload.get("preferences", {}).get("optimization_mode") and len(modules) >= 3:
        return "full_trip_search"
    if modules == {"flight", "hotel"}:
        return "flight_hotel_search"
    if payload.get("flexible_dates") and "flight" in modules:
        return "flexible_flight_search"
    return "travel_search"


def search_summary(payload: dict[str, Any]) -> str:
    if payload.get("trip_type") == "multi_city":
        legs = payload.get("legs", [])
        if legs:
            first = legs[0]
            last = legs[-1]
            route = f"{first.get('origin', '—')} → {last.get('destination', '—')}"
            return f"多城市旅程 {route} · {first.get('departure_date', '日期未定')}"[:255]
        return "多城市旅程查詢"
    origin = payload.get("origin", "—")
    destination = payload.get("destination", "—")
    departure = payload.get("departure_date", "日期未定")
    returning = payload.get("return_date")
    date_text = f"{departure}–{returning}" if returning else str(departure)
    return f"旅程查詢 {origin} → {destination} · {date_text}"[:255]


async def seed_usage_packages(session: AsyncSession) -> None:
    for code, defaults in PACKAGE_DEFAULTS.items():
        package = await session.scalar(select(UsagePackage).where(UsagePackage.code == code))
        if package is None:
            package = UsagePackage(code=code, name=str(defaults["name"]), uses=0)
            session.add(package)
        package.name = str(defaults["name"])
        package.uses = int(defaults["uses"])
        package.price_twd = int(defaults["price_twd"])
        package.is_active = True
        package.purchasable = bool(defaults["purchasable"])
    await session.flush()


async def create_usage_account(session: AsyncSession, user: User) -> UsageAccount:
    await seed_usage_packages(session)
    trial = await session.scalar(
        select(UsagePackage).where(UsagePackage.code == "TRIAL_3")
    )
    if trial is None:
        raise RuntimeError("TRIAL_3 package seed failed")
    account = UsageAccount(user_id=user.id, remaining_uses=trial.uses, reserved_uses=0)
    session.add(account)
    await session.flush()
    session.add(
        UsageLedger(
            user_id=user.id,
            account_id=account.id,
            package_id=trial.id,
            entry_type="grant",
            status="granted",
            amount=trial.uses,
            balance_after=trial.uses,
            reference=f"trial:{user.id}",
            operation="trial_registration",
            summary="註冊贈送 3 次",
            unit="use",
            metadata_json={"package": trial.code},
        )
    )
    return account


async def get_usage_account(
    session: AsyncSession, user_id: UUID, lock: bool = False
) -> UsageAccount:
    statement = select(UsageAccount).where(UsageAccount.user_id == user_id)
    if lock:
        statement = statement.with_for_update()
    account = await session.scalar(statement)
    if account is None:
        raise AppError(409, "usage_account_missing", "No usage account was found")
    return account


async def reserve_use(
    session: AsyncSession,
    user_id: UUID,
    idempotency_key: str,
    operation: str,
    summary: str,
) -> tuple[UsageReservation, bool]:
    account = await get_usage_account(session, user_id, lock=True)
    existing = await session.scalar(
        select(UsageReservation).where(
            UsageReservation.user_id == user_id,
            UsageReservation.idempotency_key == idempotency_key,
        )
    )
    if existing is not None:
        if existing.operation != operation:
            raise AppError(
                409,
                "idempotency_key_reused",
                "Idempotency-Key has already been used for another operation",
            )
        return existing, False
    if account.remaining_uses - account.reserved_uses < 1:
        raise AppError(402, "insufficient_uses", "可用次數不足，請前往方案頁查看次數包")
    account.reserved_uses += 1
    reservation = UsageReservation(
        user_id=user_id,
        account_id=account.id,
        idempotency_key=idempotency_key,
        operation=operation,
        summary=summary[:255],
        uses=1,
    )
    session.add(reservation)
    await session.flush()
    return reservation, True


async def commit_reservation(
    session: AsyncSession, reservation: UsageReservation, resource_id: UUID | None = None
) -> None:
    current = await session.scalar(
        select(UsageReservation)
        .where(UsageReservation.id == reservation.id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if current is None or current.status != "reserved":
        return
    account = await get_usage_account(session, current.user_id, lock=True)
    if account.reserved_uses < current.uses or account.remaining_uses < current.uses:
        raise AppError(409, "usage_balance_invalid", "The reserved usage balance is invalid")
    account.reserved_uses -= current.uses
    account.remaining_uses -= current.uses
    current.status = "committed"
    if resource_id is not None:
        current.resource_id = resource_id
    session.add(
        UsageLedger(
            user_id=current.user_id,
            account_id=account.id,
            entry_type="use",
            status="charged",
            amount=-current.uses,
            balance_after=account.remaining_uses,
            reference=str(current.id),
            operation=current.operation,
            summary=current.summary,
            resource_id=current.resource_id,
            unit="use",
            metadata_json={},
        )
    )


async def release_reservation(
    session: AsyncSession, reservation: UsageReservation, reason: str = "no_usable_result"
) -> None:
    current = await session.scalar(
        select(UsageReservation)
        .where(UsageReservation.id == reservation.id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if current is None or current.status != "reserved":
        return
    account = await get_usage_account(session, current.user_id, lock=True)
    if account.reserved_uses < current.uses:
        raise AppError(409, "usage_balance_invalid", "The reserved usage balance is invalid")
    account.reserved_uses -= current.uses
    current.status = "released"
    session.add(
        UsageLedger(
            user_id=current.user_id,
            account_id=account.id,
            entry_type="use",
            status="released",
            amount=0,
            balance_after=account.remaining_uses,
            reference=str(current.id),
            operation=current.operation,
            summary=current.summary,
            resource_id=current.resource_id,
            unit="use",
            metadata_json={"reason": reason},
        )
    )


def usage_status(reservation: UsageReservation) -> UsageStatus:
    status: Literal["reserved", "charged", "released"]
    if reservation.status == "reserved":
        status = "reserved"
    elif reservation.status == "committed":
        status = "charged"
    else:
        status = "released"
    return UsageStatus(status=status, uses=reservation.uses, reference=str(reservation.id))


async def grant_package(
    session: AsyncSession,
    user_id: UUID,
    package_code: str,
    external_reference: str,
) -> tuple[UsageLedger, bool]:
    external_reference = external_reference.strip()
    if not external_reference or len(external_reference) > 200:
        raise AppError(
            422,
            "invalid_external_reference",
            "External reference must contain between 1 and 200 characters",
        )
    await seed_usage_packages(session)
    package = await session.scalar(
        select(UsagePackage).where(
            UsagePackage.code == package_code.upper(), UsagePackage.is_active.is_(True)
        )
    )
    if package is None or package.code == "TRIAL_3":
        raise AppError(404, "usage_package_not_found", "Usage package was not found")
    reference = f"package:{external_reference}"
    existing = await session.scalar(
        select(UsageLedger).where(
            UsageLedger.reference == reference,
            UsageLedger.entry_type == "package_grant",
        )
    )
    if existing is not None:
        return existing, False
    account = await get_usage_account(session, user_id, lock=True)
    account.remaining_uses += package.uses
    ledger = UsageLedger(
        user_id=user_id,
        account_id=account.id,
        package_id=package.id,
        entry_type="package_grant",
        status="granted",
        amount=package.uses,
        balance_after=account.remaining_uses,
        reference=reference,
        operation="manual_package_grant",
        summary=f"{package.name}加值",
        unit="use",
        metadata_json={"package": package.code, "source": "cli"},
    )
    session.add(ledger)
    await session.flush()
    return ledger, True
