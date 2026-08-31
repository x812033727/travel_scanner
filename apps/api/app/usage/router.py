import base64
import binascii
from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.db import get_session
from app.models import UsageLedger, UsagePackage
from app.problems import AppError
from app.usage.service import COMMON_LIMITS, get_usage_account

router = APIRouter(tags=["usage"])
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


@router.get("/usage")
async def usage(user: CurrentUser, session: Session) -> dict[str, Any]:
    account = await get_usage_account(session, user.id)
    return {
        "remaining_uses": account.remaining_uses,
        "reserved_uses": account.reserved_uses,
        "available_uses": account.remaining_uses - account.reserved_uses,
        "limits": COMMON_LIMITS,
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
