from __future__ import annotations

import math
from uuid import UUID

from sqlalchemy import false, func, or_, select, true
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement

from app.admin.user_schemas import (
    AdminUsageAdjustment,
    AdminUsageAdjustmentResult,
    AdminUsageHistoryItem,
    AdminUserAuditItem,
    AdminUserDetail,
    AdminUserList,
    AdminUserStats,
    AdminUserSummary,
    AdminUserUpdate,
)
from app.config import get_settings
from app.db import escape_like
from app.models import AdminAuditLog, UsageAccount, UsageLedger, User
from app.problems import AppError


def _admin_source(user: User) -> str:
    if user.is_admin:
        return "database"
    if user.email.lower() in get_settings().admin_email_set:
        return "environment"
    return "none"


def _effective_admin(user: User) -> bool:
    return _admin_source(user) != "none"


def _can_adjust_usage(user_id: UUID, actor: User) -> bool:
    return user_id != actor.id or actor.email.lower() in get_settings().admin_email_set


def _summary(user: User, account: UsageAccount | None, actor: User) -> AdminUserSummary:
    remaining = account.remaining_uses if account else 0
    reserved = account.reserved_uses if account else 0
    return AdminUserSummary(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        is_admin=user.is_admin,
        effective_is_admin=_effective_admin(user),
        admin_source=_admin_source(user),
        is_self=user.id == actor.id,
        can_adjust_usage=_can_adjust_usage(user.id, actor),
        remaining_uses=remaining,
        reserved_uses=reserved,
        available_uses=remaining - reserved,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def _search_filter(query: str | None) -> ColumnElement[bool]:
    if not query or not query.strip():
        return true()
    return User.email.ilike(f"%{escape_like(query.strip())}%", escape="\\")


async def list_admin_users(
    session: AsyncSession,
    actor: User,
    query: str | None,
    page: int,
    limit: int,
) -> AdminUserList:
    search_filter = _search_filter(query)
    env_admins = sorted(get_settings().admin_email_set)
    effective_admin = or_(
        User.is_admin.is_(True),
        func.lower(User.email).in_(env_admins) if env_admins else false(),
    )
    stats_row = (
        await session.execute(
            select(
                func.count(User.id),
                func.count(User.id).filter(User.is_active.is_(True)),
                func.count(User.id).filter(effective_admin),
                func.coalesce(
                    func.sum(UsageAccount.remaining_uses - UsageAccount.reserved_uses), 0
                ),
            )
            .outerjoin(UsageAccount, UsageAccount.user_id == User.id)
            .where(search_filter)
        )
    ).one()
    total = int(stats_row[0])
    rows = (
        await session.execute(
            select(User, UsageAccount)
            .outerjoin(UsageAccount, UsageAccount.user_id == User.id)
            .where(search_filter)
            .order_by(User.created_at.desc(), User.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )
    ).all()
    return AdminUserList(
        items=[_summary(user, account, actor) for user, account in rows],
        page=page,
        limit=limit,
        total=total,
        pages=max(1, math.ceil(total / limit)),
        stats=AdminUserStats(
            total=total,
            active=int(stats_row[1]),
            administrators=int(stats_row[2]),
            available_uses=int(stats_row[3]),
        ),
    )


async def _user_and_account(
    session: AsyncSession, user_id: UUID, *, lock_account: bool = False
) -> tuple[User, UsageAccount | None]:
    user = await session.get(User, user_id)
    if user is None:
        raise AppError(404, "admin_user_not_found", "找不到這個會員帳號")
    statement = select(UsageAccount).where(UsageAccount.user_id == user_id)
    if lock_account:
        statement = statement.with_for_update()
    account = await session.scalar(statement)
    return user, account


async def admin_user_detail(session: AsyncSession, user_id: UUID, actor: User) -> AdminUserDetail:
    user, account = await _user_and_account(session, user_id)
    ledger = list(
        (
            await session.scalars(
                select(UsageLedger)
                .where(UsageLedger.user_id == user_id)
                .order_by(UsageLedger.created_at.desc(), UsageLedger.id.desc())
                .limit(20)
            )
        ).all()
    )
    audits = list(
        (
            await session.scalars(
                select(AdminAuditLog)
                .where(AdminAuditLog.target == f"user:{user_id}")
                .order_by(AdminAuditLog.created_at.desc(), AdminAuditLog.id.desc())
                .limit(20)
            )
        ).all()
    )
    summary = _summary(user, account, actor)
    return AdminUserDetail(
        **summary.model_dump(),
        usage_history=[
            AdminUsageHistoryItem(
                id=item.id,
                occurred_at=item.created_at,
                entry_type=item.entry_type,
                status=item.status,
                change=item.amount,
                balance_after=item.balance_after,
                summary=item.summary,
                reference=item.reference,
            )
            for item in ledger
        ],
        admin_history=[
            AdminUserAuditItem(
                id=item.id,
                action=item.action,
                actor_user_id=item.actor_user_id,
                metadata=item.metadata_json,
                created_at=item.created_at,
            )
            for item in audits
        ],
    )


async def update_admin_user(
    session: AsyncSession,
    user_id: UUID,
    payload: AdminUserUpdate,
    actor: User,
) -> AdminUserDetail:
    user, _ = await _user_and_account(session, user_id)
    if user.id == actor.id and payload.is_active is False:
        raise AppError(409, "admin_self_deactivation", "不可停用目前登入的管理員帳號")
    if user.id == actor.id and payload.is_admin is False:
        raise AppError(409, "admin_self_demotion", "不可移除目前登入帳號的管理員權限")
    settings = get_settings()
    environment_designated = (
        user.email.lower() in settings.admin_email_set
        or user.email.lower() in settings.deploy_admin_email_set
    )
    # Suspension would bump auth_version and sign the account out, so it locks out an
    # environment-designated administrator just as effectively as demotion does; both
    # must go through the host environment first.
    if environment_designated and (payload.is_admin is False or payload.is_active is False):
        raise AppError(
            409,
            "admin_environment_override",
            "此帳號由 ADMIN_EMAILS 授權，請先從主機環境設定移除",
        )
    changed: dict[str, bool] = {}
    if payload.is_active is not None and payload.is_active != user.is_active:
        user.is_active = payload.is_active
        user.auth_version = (user.auth_version or 1) + 1
        changed["is_active"] = payload.is_active
    if payload.is_admin is not None and payload.is_admin != user.is_admin:
        user.is_admin = payload.is_admin
        changed["is_admin"] = payload.is_admin
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="user_account_updated",
            target=f"user:{user.id}",
            metadata_json={"changed": changed, "email": user.email},
        )
    )
    await session.commit()
    return await admin_user_detail(session, user.id, actor)


def adjusted_usage_balance(account: UsageAccount, change: int) -> int:
    balance = account.remaining_uses + change
    if balance < account.reserved_uses:
        raise AppError(
            409,
            "admin_usage_below_reserved",
            f"調整後不得低於目前保留的 {account.reserved_uses} 次",
        )
    return balance


async def adjust_admin_user_usage(
    session: AsyncSession,
    user_id: UUID,
    payload: AdminUsageAdjustment,
    actor: User,
    idempotency_key: str,
) -> AdminUsageAdjustmentResult:
    if not _can_adjust_usage(user_id, actor):
        raise AppError(
            409,
            "admin_self_usage_adjustment",
            "不可調整目前登入管理員自己的使用次數",
        )
    reference = f"admin-adjustment:{actor.id}:{idempotency_key}"
    user, account = await _user_and_account(session, user_id, lock_account=True)
    if account is None:
        raise AppError(409, "usage_account_missing", "此會員尚未建立次數帳戶")
    existing = await session.scalar(
        select(UsageLedger).where(
            UsageLedger.user_id == user_id,
            UsageLedger.entry_type == "admin_adjustment",
            UsageLedger.reference == reference,
        )
    )
    if existing is not None:
        if existing.amount != payload.change or existing.summary != payload.reason:
            raise AppError(
                409,
                "admin_adjustment_key_reused",
                "Idempotency-Key 已用於不同的次數調整",
            )
        return AdminUsageAdjustmentResult(
            user=await admin_user_detail(session, user_id, actor),
            ledger_id=existing.id,
            change=existing.amount,
            balance_after=existing.balance_after,
            replayed=True,
        )
    account.remaining_uses = adjusted_usage_balance(account, payload.change)
    ledger = UsageLedger(
        user_id=user.id,
        account_id=account.id,
        entry_type="admin_adjustment",
        status="granted" if payload.change > 0 else "charged",
        amount=payload.change,
        balance_after=account.remaining_uses,
        reference=reference,
        operation="admin_usage_adjustment",
        summary=payload.reason,
        unit="use",
        metadata_json={"actor_user_id": str(actor.id), "actor_email": actor.email},
    )
    session.add(ledger)
    await session.flush()
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="user_usage_adjusted",
            target=f"user:{user.id}",
            metadata_json={
                "email": user.email,
                "change": payload.change,
                "balance_after": account.remaining_uses,
                "reason": payload.reason,
                "ledger_id": str(ledger.id),
            },
        )
    )
    ledger_id = ledger.id
    balance_after = account.remaining_uses
    await session.commit()
    return AdminUsageAdjustmentResult(
        user=await admin_user_detail(session, user.id, actor),
        ledger_id=ledger_id,
        change=payload.change,
        balance_after=balance_after,
        replayed=False,
    )
