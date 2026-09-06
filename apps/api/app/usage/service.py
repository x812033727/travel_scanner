from typing import Any, Literal
from uuid import UUID, uuid4

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    AdminAuditLog,
    UsageAccount,
    UsageLedger,
    UsageOperationCost,
    UsagePackage,
    UsageReservation,
    User,
)
from app.problems import AppError
from app.usage.schemas import (
    SUPPORTED_LOCALES,
    AdminUsagePackageView,
    OperationCostsUpdate,
    PublicUsagePackageView,
    UsageCatalog,
    UsageOperationCostView,
    UsagePackageInput,
    UsageSettingsAuditView,
    UsageSettingsSnapshot,
    UsageStatus,
)

USAGE_OPERATIONS = (
    "travel_search",
    "flexible_flight_search",
    "flight_hotel_search",
    "full_trip_search",
    "multi_city_search",
    "public_airline_fare_search",
    "back_to_back_fare_search",
    "live_back_to_back_fare_search",
    "flight_status_lookup",
    "ai_itinerary_generation",
    # Re-planning an existing trip from the intent bar. Seeded at 0 uses by
    # migration 0039 so refinement ships free and its price stays an admin
    # dial rather than a deploy.
    "ai_itinerary_refine",
    "itinerary_optimization",
    "price_reoptimization",
)

PACKAGE_DEFAULTS: dict[str, dict[str, Any]] = {
    "TRIAL_3": {
        "name": "註冊體驗",
        "localized_names": {
            "zh-TW": "註冊體驗",
            "zh-CN": "注册体验",
            "en": "Registration trial",
            "ja": "登録トライアル",
            "ko": "가입 체험",
        },
        "uses": 3,
        "price_twd": 0,
        "display_order": 0,
        "is_featured": False,
        "purchasable": False,
    },
    "PACK_10": {
        "name": "輕量 10 次包",
        "localized_names": {
            "zh-TW": "輕量包",
            "zh-CN": "轻量包",
            "en": "Light pack",
            "ja": "ライトパック",
            "ko": "라이트 팩",
        },
        "uses": 10,
        "price_twd": 199,
        "display_order": 10,
        "is_featured": False,
        "purchasable": False,
    },
    "PACK_30": {
        "name": "常用 30 次包",
        "localized_names": {
            "zh-TW": "常用包",
            "zh-CN": "常用包",
            "en": "Standard pack",
            "ja": "スタンダードパック",
            "ko": "스탠다드 팩",
        },
        "uses": 30,
        "price_twd": 499,
        "display_order": 20,
        "is_featured": True,
        "purchasable": False,
    },
    "PACK_100": {
        "name": "大量 100 次包",
        "localized_names": {
            "zh-TW": "大量包",
            "zh-CN": "大容量包",
            "en": "Bulk pack",
            "ja": "大容量パック",
            "ko": "대용량 팩",
        },
        "uses": 100,
        "price_twd": 1299,
        "display_order": 30,
        "is_featured": False,
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
            package = UsagePackage(
                code=code,
                name=str(defaults["name"]),
                localized_names=dict(defaults["localized_names"]),
                uses=int(defaults["uses"]),
                price_twd=int(defaults["price_twd"]),
                display_order=int(defaults["display_order"]),
                is_active=True,
                is_featured=bool(defaults["is_featured"]),
                purchasable=bool(defaults["purchasable"]),
            )
            session.add(package)
    await session.flush()


async def effective_operation_cost(session: AsyncSession, operation: str) -> int:
    if operation not in USAGE_OPERATIONS:
        return 1
    row = await session.get(UsageOperationCost, operation)
    return row.uses if row is not None else 1


async def operation_costs(session: AsyncSession) -> tuple[dict[str, int], set[str]]:
    rows = list((await session.scalars(select(UsageOperationCost))).all())
    stored = {row.operation: row.uses for row in rows if row.operation in USAGE_OPERATIONS}
    return ({operation: stored.get(operation, 1) for operation in USAGE_OPERATIONS}, set(stored))


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
            summary=f"註冊贈送 {trial.uses} 次",
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
        raise AppError(409, "usage_account_missing", "找不到可用次數帳戶")
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
        if existing.resource_id is None:
            raise AppError(
                409,
                "idempotency_result_unavailable",
                "This Idempotency-Key has no replayable result; use a new key",
            )
        return existing, False
    uses = await effective_operation_cost(session, operation)
    if account.remaining_uses - account.reserved_uses < uses:
        raise AppError(402, "insufficient_uses", "可用次數不足，請前往方案頁查看次數包")
    account.reserved_uses += uses
    reservation = UsageReservation(
        user_id=user_id,
        account_id=account.id,
        idempotency_key=idempotency_key,
        operation=operation,
        summary=summary[:255],
        uses=uses,
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
        raise AppError(409, "usage_balance_invalid", "保留次數的帳務狀態不正確")
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
        raise AppError(409, "usage_balance_invalid", "保留次數的帳務狀態不正確")
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
        raise AppError(404, "usage_package_not_found", "找不到這個次數包")
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


def _package_names(package: UsagePackage) -> dict[str, str]:
    stored = package.localized_names or {}
    return {locale: str(stored.get(locale) or package.name) for locale in SUPPORTED_LOCALES}


def _admin_package_view(package: UsagePackage) -> AdminUsagePackageView:
    return AdminUsagePackageView(
        id=package.id,
        code=package.code,
        localized_names=_package_names(package),
        uses=package.uses,
        price_twd=package.price_twd,
        display_order=package.display_order,
        is_active=package.is_active,
        is_featured=package.is_featured,
    )


async def usage_settings_snapshot(session: AsyncSession) -> UsageSettingsSnapshot:
    await seed_usage_packages(session)
    packages = list(
        (
            await session.scalars(
                select(UsagePackage).order_by(UsagePackage.display_order, UsagePackage.price_twd)
            )
        ).all()
    )
    trial = next(package for package in packages if package.code == "TRIAL_3")
    costs, stored = await operation_costs(session)
    audit_actions = (
        "usage_operation_costs_updated",
        "usage_package_created",
        "usage_package_updated",
        "usage_package_archived",
        "registration_trial_updated",
    )
    audit_rows = list(
        (
            await session.scalars(
                select(AdminAuditLog)
                .where(AdminAuditLog.action.in_(audit_actions))
                .order_by(AdminAuditLog.created_at.desc())
                .limit(50)
            )
        ).all()
    )
    return UsageSettingsSnapshot(
        trial_uses=trial.uses,
        packages=[_admin_package_view(package) for package in packages if package is not trial],
        operation_costs=[
            UsageOperationCostView(
                operation=operation,
                uses=costs[operation],
                source="database" if operation in stored else "default",
            )
            for operation in USAGE_OPERATIONS
        ],
        audit=[
            UsageSettingsAuditView(
                id=row.id,
                actor_user_id=row.actor_user_id,
                action=row.action,
                target=row.target,
                metadata=row.metadata_json,
                created_at=row.created_at,
            )
            for row in audit_rows
        ],
    )


async def update_trial_uses(
    session: AsyncSession, uses: int, actor: User
) -> UsageSettingsSnapshot:
    await seed_usage_packages(session)
    trial = await session.scalar(
        select(UsagePackage).where(UsagePackage.code == "TRIAL_3").with_for_update()
    )
    if trial is None:
        raise RuntimeError("TRIAL_3 package seed failed")
    before = trial.uses
    trial.uses = uses
    trial.is_active = True
    trial.is_featured = False
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="registration_trial_updated",
            target=trial.code,
            metadata_json={"before": {"uses": before}, "after": {"uses": uses}},
        )
    )
    await session.commit()
    return await usage_settings_snapshot(session)


async def update_operation_costs(
    session: AsyncSession, payload: OperationCostsUpdate, actor: User
) -> UsageSettingsSnapshot:
    unknown = sorted(set(payload.costs) - set(USAGE_OPERATIONS))
    if unknown:
        raise AppError(422, "usage_operation_unknown", f"未知的計次操作：{', '.join(unknown)}")
    before: dict[str, int] = {}
    after: dict[str, int] = {}
    for operation, uses in payload.costs.items():
        row = await session.scalar(
            select(UsageOperationCost)
            .where(UsageOperationCost.operation == operation)
            .with_for_update()
        )
        before[operation] = row.uses if row is not None else 1
        if row is None:
            row = UsageOperationCost(operation=operation, uses=uses)
            session.add(row)
        row.uses = uses
        row.updated_by_user_id = actor.id
        after[operation] = uses
    changed = {key: value for key, value in after.items() if before[key] != value}
    if changed:
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action="usage_operation_costs_updated",
                target="usage_operation_costs",
                metadata_json={
                    "before": {key: before[key] for key in changed},
                    "after": changed,
                },
            )
        )
    await session.commit()
    return await usage_settings_snapshot(session)


async def _clear_featured_packages(session: AsyncSession, except_id: UUID | None = None) -> None:
    statement = update(UsagePackage).where(UsagePackage.is_featured.is_(True))
    if except_id is not None:
        statement = statement.where(UsagePackage.id != except_id)
    await session.execute(statement.values(is_featured=False))


async def create_usage_package(
    session: AsyncSession, payload: UsagePackageInput, actor: User
) -> UsageSettingsSnapshot:
    if payload.is_featured and payload.is_active:
        await _clear_featured_packages(session)
    package = UsagePackage(
        code=f"PACK_{uuid4().hex[:12].upper()}",
        name=payload.localized_names["zh-TW"],
        localized_names=payload.localized_names,
        uses=payload.uses,
        price_twd=payload.price_twd,
        display_order=payload.display_order,
        is_active=payload.is_active,
        is_featured=payload.is_featured and payload.is_active,
        purchasable=False,
    )
    session.add(package)
    await session.flush()
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="usage_package_created",
            target=package.code,
            metadata_json={"after": _admin_package_view(package).model_dump(mode="json")},
        )
    )
    await session.commit()
    return await usage_settings_snapshot(session)


async def update_usage_package(
    session: AsyncSession, package_id: UUID, payload: UsagePackageInput, actor: User
) -> UsageSettingsSnapshot:
    package = await session.scalar(
        select(UsagePackage).where(UsagePackage.id == package_id).with_for_update()
    )
    if package is None or package.code == "TRIAL_3":
        raise AppError(404, "usage_package_not_found", "找不到這個次數包")
    before = _admin_package_view(package).model_dump(mode="json")
    if payload.is_featured and payload.is_active:
        await _clear_featured_packages(session, package.id)
    package.name = payload.localized_names["zh-TW"]
    package.localized_names = payload.localized_names
    package.uses = payload.uses
    package.price_twd = payload.price_twd
    package.display_order = payload.display_order
    package.is_active = payload.is_active
    package.is_featured = payload.is_featured and payload.is_active
    after = _admin_package_view(package).model_dump(mode="json")
    action = (
        "usage_package_archived"
        if before["is_active"] and not package.is_active
        else "usage_package_updated"
    )
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action=action,
            target=package.code,
            metadata_json={"before": before, "after": after},
        )
    )
    await session.commit()
    return await usage_settings_snapshot(session)


async def public_usage_catalog(session: AsyncSession, locale: str) -> UsageCatalog:
    await seed_usage_packages(session)
    packages = list(
        (
            await session.scalars(
                select(UsagePackage)
                .where(
                    UsagePackage.code != "TRIAL_3",
                    UsagePackage.is_active.is_(True),
                )
                .order_by(UsagePackage.display_order, UsagePackage.price_twd)
            )
        ).all()
    )
    trial = await session.scalar(select(UsagePackage).where(UsagePackage.code == "TRIAL_3"))
    if trial is None:
        raise RuntimeError("TRIAL_3 package seed failed")
    costs, _ = await operation_costs(session)
    return UsageCatalog(
        trial_uses=trial.uses,
        packages=[
            PublicUsagePackageView(
                code=package.code,
                name=_package_names(package)[locale],
                uses=package.uses,
                price_twd=package.price_twd,
                display_order=package.display_order,
                is_featured=package.is_featured,
                purchasable=False,
            )
            for package in packages
        ],
        operation_costs=costs,
    )
