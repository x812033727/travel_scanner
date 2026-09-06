import base64
import binascii
from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AdminUser, CurrentUser
from app.db import get_session
from app.models import PriceAlert, TripPlan, UsageLedger, UsagePackage
from app.problems import AppError
from app.usage.schemas import (
    OperationCostsUpdate,
    TrialSettingsUpdate,
    UsageCatalog,
    UsagePackageInput,
    UsageSettingsSnapshot,
)
from app.usage.service import (
    COMMON_LIMITS,
    create_usage_package,
    get_usage_account,
    public_usage_catalog,
    update_operation_costs,
    update_trial_uses,
    update_usage_package,
    usage_settings_snapshot,
)

router = APIRouter(tags=["usage"])
admin_router = APIRouter(prefix="/admin/usage-settings", tags=["admin usage settings"])
Session = Annotated[AsyncSession, Depends(get_session)]
HistoryKind = Literal["all", "charged", "granted", "released"]


def encode_cursor(created_at: datetime, ledger_id: UUID) -> str:
    raw = f"{created_at.isoformat()}|{ledger_id}".encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def decode_cursor(cursor: str) -> tuple[datetime, UUID]:
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        created_at, ledger_id = base64.urlsafe_b64decode(padded).decode().split("|", 1)
        parsed_at = datetime.fromisoformat(created_at)
        if parsed_at.tzinfo is None:
            raise ValueError("cursor timestamp must include a timezone")
        return parsed_at, UUID(ledger_id)
    except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
        raise AppError(422, "invalid_usage_cursor", "使用紀錄游標格式不正確") from exc


@router.get("/plans")
async def list_plans(session: Session) -> list[dict[str, Any]]:
    packages = list(
        (
            await session.scalars(
                select(UsagePackage)
                .where(UsagePackage.is_active.is_(True))
                .order_by(UsagePackage.price_twd, UsagePackage.uses)
            )
        ).all()
    )
    return [
        {
            "code": package.code,
            "name": package.name,
            "uses": package.uses,
            "price_twd": package.price_twd,
            "expires": False,
            "purchasable": package.purchasable,
        }
        for package in packages
    ]


@router.get("/usage-catalog", response_model=UsageCatalog)
async def usage_catalog(
    response: Response,
    session: Session,
    locale: Literal["zh-TW", "zh-CN", "en", "ja", "ko"] = "zh-TW",
) -> UsageCatalog:
    response.headers["Cache-Control"] = "no-store"
    return await public_usage_catalog(session, locale)


@admin_router.get("", response_model=UsageSettingsSnapshot)
async def get_usage_settings(user: AdminUser, session: Session) -> UsageSettingsSnapshot:
    _ = user
    return await usage_settings_snapshot(session)


@admin_router.put("/trial", response_model=UsageSettingsSnapshot)
async def put_trial_settings(
    payload: TrialSettingsUpdate, user: AdminUser, session: Session
) -> UsageSettingsSnapshot:
    return await update_trial_uses(session, payload.uses, user)


@admin_router.put("/operation-costs", response_model=UsageSettingsSnapshot)
async def put_operation_costs(
    payload: OperationCostsUpdate, user: AdminUser, session: Session
) -> UsageSettingsSnapshot:
    return await update_operation_costs(session, payload, user)


@admin_router.post("/packages", response_model=UsageSettingsSnapshot, status_code=201)
async def post_usage_package(
    payload: UsagePackageInput, user: AdminUser, session: Session
) -> UsageSettingsSnapshot:
    return await create_usage_package(session, payload, user)


@admin_router.put("/packages/{package_id}", response_model=UsageSettingsSnapshot)
async def put_usage_package(
    package_id: UUID,
    payload: UsagePackageInput,
    user: AdminUser,
    session: Session,
) -> UsageSettingsSnapshot:
    return await update_usage_package(session, package_id, payload, user)


@router.get("/usage")
async def usage(user: CurrentUser, session: Session) -> dict[str, Any]:
    account = await get_usage_account(session, user.id)
    # The limits alone never told a member how close they were; the counts use the
    # same predicates the create endpoints enforce (every trip, active alerts only).
    trip_count = await session.scalar(
        select(func.count()).select_from(TripPlan).where(TripPlan.user_id == user.id)
    )
    alert_count = await session.scalar(
        select(func.count())
        .select_from(PriceAlert)
        .where(PriceAlert.user_id == user.id, PriceAlert.active.is_(True))
    )
    return {
        "remaining_uses": account.remaining_uses,
        "reserved_uses": account.reserved_uses,
        "available_uses": account.remaining_uses - account.reserved_uses,
        "limits": COMMON_LIMITS,
        "counts": {
            "saved_trips": int(trip_count or 0),
            "price_alerts": int(alert_count or 0),
        },
    }


@router.get("/usage/history")
async def usage_history(
    user: CurrentUser,
    session: Session,
    cursor: str | None = None,
    kind: HistoryKind = "all",
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> dict[str, Any]:
    statement = select(UsageLedger).where(UsageLedger.user_id == user.id)
    if kind != "all":
        statement = statement.where(UsageLedger.status == kind)
    if cursor:
        created_at, ledger_id = decode_cursor(cursor)
        statement = statement.where(
            or_(
                UsageLedger.created_at < created_at,
                and_(UsageLedger.created_at == created_at, UsageLedger.id < ledger_id),
            )
        )
    rows = list(
        (
            await session.scalars(
                statement.order_by(UsageLedger.created_at.desc(), UsageLedger.id.desc()).limit(
                    limit + 1
                )
            )
        ).all()
    )
    page, has_more = rows[:limit], len(rows) > limit
    items = [
        {
            "id": str(item.id),
            "occurred_at": item.created_at,
            "type": item.entry_type,
            "status": item.status,
            "operation": item.operation,
            "summary": item.summary,
            "change": item.amount,
            "balance_after": item.balance_after,
            "reference": item.reference,
            "resource_id": str(item.resource_id) if item.resource_id else None,
            "unit": item.unit,
            "is_legacy": item.unit == "legacy_credit",
        }
        for item in page
    ]
    next_cursor = encode_cursor(page[-1].created_at, page[-1].id) if has_more and page else None
    return {"items": items, "next_cursor": next_cursor}
