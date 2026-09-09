from __future__ import annotations

import asyncio
import math
from collections.abc import AsyncIterator, Collection
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from typing import Literal
from uuid import UUID
from weakref import WeakKeyDictionary

from sqlalchemy import and_, case, exists, false, func, literal, or_, select, text, true, union_all
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.selectable import Subquery

from app.admin.audit_safety import safe_audit_metadata
from app.admin.user_schemas import (
    AdminActionResult,
    AdminAuthIdentityItem,
    AdminErasureRequest,
    AdminErasureStatus,
    AdminReasonRequest,
    AdminRolesUpdate,
    AdminSuspensionRequest,
    AdminUsageAdjustment,
    AdminUsageAdjustmentResult,
    AdminUsageHistoryItem,
    AdminUserActivity,
    AdminUserAuditItem,
    AdminUserDetail,
    AdminUserList,
    AdminUserStats,
    AdminUserSummary,
    AdminUserUpdate,
)
from app.community.accounts import request_mail
from app.community.jobs import enqueue_jobs
from app.community.models import Comment, Job, Post
from app.config import get_settings
from app.db import escape_like
from app.infra import enforce_named_rate_limit
from app.models import (
    AccountErasureRequest,
    AdminAuditLog,
    AdminRoleAssignment,
    PriceAlert,
    SearchRequest,
    TripPlan,
    UsageAccount,
    UsageLedger,
    User,
    UserAuthIdentity,
)
from app.problems import AppError

LEGACY_ROLES = frozenset({"support", "content", "operations"})
ACTIVE_ERASURE_STATUSES = ("scheduled", "processing")
MAX_TIMED_SUSPENSION = timedelta(days=90)
OWNER_MUTATION_ADVISORY_LOCK_ID = 0x545341444D494E
_owner_fallback_locks: WeakKeyDictionary[asyncio.AbstractEventLoop, asyncio.Lock] = (
    WeakKeyDictionary()
)


def _aware(value: datetime | None) -> datetime | None:
    if value is None or value.tzinfo is not None:
        return value
    return value.replace(tzinfo=UTC)


def _owner_fallback_lock() -> asyncio.Lock:
    loop = asyncio.get_running_loop()
    lock = _owner_fallback_locks.get(loop)
    if lock is None:
        lock = asyncio.Lock()
        _owner_fallback_locks[loop] = lock
    return lock


@asynccontextmanager
async def _owner_mutation_guard(session: AsyncSession) -> AsyncIterator[None]:
    """Serialize mutations that can remove the platform's last usable owner.

    PostgreSQL holds the advisory lock until the surrounding transaction commits
    or rolls back. SQLite ignores ``FOR UPDATE`` and has no advisory locks, so
    tests and local development keep the whole service operation under one
    event-loop lock instead.
    """
    try:
        dialect = session.get_bind().dialect.name
    except (AttributeError, RuntimeError):
        dialect = ""
    if dialect == "postgresql":
        await session.execute(
            text("SELECT pg_advisory_xact_lock(:lock_id)"),
            {"lock_id": OWNER_MUTATION_ADVISORY_LOCK_ID},
        )
        yield
        return
    async with _owner_fallback_lock():
        yield


def _admin_source(user: User, roles: Collection[str] = ()) -> str:
    assigned = set(roles)
    if user.email.lower() in get_settings().admin_email_set:
        return "environment"
    if user.is_admin or assigned:
        return "database"
    return "none"


def _effective_admin(user: User, roles: Collection[str] = ()) -> bool:
    del user
    return bool(roles)


def _can_adjust_usage(user_id: UUID, actor: User) -> bool:
    return user_id != actor.id or actor.email.lower() in get_settings().admin_email_set


def _status(
    user: User, erasure: AccountErasureRequest | None
) -> Literal["active", "inactive", "suspended", "erasure_pending"]:
    if erasure is not None and erasure.status in ACTIVE_ERASURE_STATUSES:
        return "erasure_pending"
    if not user.is_active or user.deleted_at is not None:
        return "inactive"
    until = _aware(user.suspended_until)
    if user.suspended_at is not None and (until is None or until > datetime.now(UTC)):
        return "suspended"
    return "active"


def _summary(
    user: User,
    account: UsageAccount | None,
    actor: User,
    *,
    roles: Collection[str] = (),
    auth_methods: Collection[str] = (),
    erasure: AccountErasureRequest | None = None,
    activity: AdminUserActivity | None = None,
    last_activity_at: datetime | None = None,
) -> AdminUserSummary:
    remaining = account.remaining_uses if account else 0
    reserved = account.reserved_uses if account else 0
    return AdminUserSummary(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        is_admin=user.is_admin,
        effective_is_admin=_effective_admin(user, roles),
        admin_source=_admin_source(user, roles),
        is_self=user.id == actor.id,
        can_adjust_usage=_can_adjust_usage(user.id, actor),
        status=_status(user, erasure),
        admin_roles=sorted(set(roles)),
        auth_methods=sorted(set(auth_methods)),
        email_verified=user.email_verified_at is not None,
        last_login_at=user.last_login_at,
        last_activity_at=last_activity_at,
        activity=activity or AdminUserActivity(),
        suspended_at=user.suspended_at,
        suspended_until=user.suspended_until,
        suspension_reason=user.suspension_reason,
        erasure_status=erasure.status if erasure else None,
        remaining_uses=remaining,
        reserved_uses=reserved,
        available_uses=remaining - reserved,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def _audit_item(item: AdminAuditLog) -> AdminUserAuditItem:
    safe_metadata = safe_audit_metadata(dict(item.metadata_json or {}))
    return AdminUserAuditItem(
        id=item.id,
        action=item.action,
        actor_user_id=item.actor_user_id,
        metadata=safe_metadata if isinstance(safe_metadata, dict) else {},
        created_at=item.created_at,
    )


def _search_filter(query: str | None) -> ColumnElement[bool]:
    if not query or not query.strip():
        return true()
    return User.email.ilike(f"%{escape_like(query.strip())}%", escape="\\")


def _activity_summary_subquery() -> Subquery:
    """Aggregate all user-owned product activity once for list and detail views."""
    events = union_all(
        select(
            TripPlan.user_id.label("user_id"),
            literal("trip").label("kind"),
            TripPlan.updated_at.label("occurred_at"),
        ),
        select(
            SearchRequest.user_id.label("user_id"),
            literal("search").label("kind"),
            SearchRequest.updated_at.label("occurred_at"),
        ),
        select(
            PriceAlert.user_id.label("user_id"),
            literal("alert").label("kind"),
            PriceAlert.updated_at.label("occurred_at"),
        ),
        select(
            Post.author_id.label("user_id"),
            literal("post").label("kind"),
            Post.updated_at.label("occurred_at"),
        ),
        select(
            Comment.author_id.label("user_id"),
            literal("comment").label("kind"),
            Comment.updated_at.label("occurred_at"),
        ),
    ).subquery("admin_user_activity_events")
    return (
        select(
            events.c.user_id,
            func.sum(case((events.c.kind == "trip", 1), else_=0)).label("trips"),
            func.sum(case((events.c.kind == "search", 1), else_=0)).label("searches"),
            func.sum(case((events.c.kind == "alert", 1), else_=0)).label("alerts"),
            func.sum(case((events.c.kind == "post", 1), else_=0)).label("community_posts"),
            func.sum(case((events.c.kind == "comment", 1), else_=0)).label("community_comments"),
            func.count().label("activity_count"),
            func.max(events.c.occurred_at).label("last_activity_at"),
        )
        .group_by(events.c.user_id)
        .subquery("admin_user_activity")
    )


def _activity_model(
    trips: int | None,
    searches: int | None,
    alerts: int | None,
    community_posts: int | None,
    community_comments: int | None,
) -> AdminUserActivity:
    return AdminUserActivity(
        trips=int(trips or 0),
        searches=int(searches or 0),
        alerts=int(alerts or 0),
        community_posts=int(community_posts or 0),
        community_comments=int(community_comments or 0),
    )


def _list_filters(
    *,
    query: str | None,
    status: str | None,
    role: str | None,
    verified: bool | None,
    auth_method: str | None,
    registered_from: datetime | None,
    registered_to: datetime | None,
) -> list[ColumnElement[bool]]:
    now = datetime.now(UTC)
    conditions = [_search_filter(query)]
    active_erasure = exists(
        select(AccountErasureRequest.id).where(
            AccountErasureRequest.user_id == User.id,
            AccountErasureRequest.status.in_(ACTIVE_ERASURE_STATUSES),
        )
    )
    suspended = and_(
        User.suspended_at.is_not(None),
        or_(User.suspended_until.is_(None), User.suspended_until > now),
    )
    if status == "active":
        conditions += [
            User.is_active.is_(True),
            User.deleted_at.is_(None),
            ~suspended,
            ~active_erasure,
        ]
    elif status == "inactive":
        conditions += [
            ~active_erasure,
            or_(User.is_active.is_(False), User.deleted_at.is_not(None)),
        ]
    elif status == "suspended":
        conditions += [
            User.is_active.is_(True),
            User.deleted_at.is_(None),
            ~active_erasure,
            suspended,
        ]
    elif status == "erasure_pending":
        conditions.append(active_erasure)
    if role:
        any_assignment = exists(
            select(AdminRoleAssignment.id).where(AdminRoleAssignment.user_id == User.id)
        )
        assigned = exists(
            select(AdminRoleAssignment.id).where(
                AdminRoleAssignment.user_id == User.id,
                AdminRoleAssignment.role == role,
                or_(AdminRoleAssignment.expires_at.is_(None), AdminRoleAssignment.expires_at > now),
            )
        )
        role_conditions: list[ColumnElement[bool]] = [assigned]
        if role in LEGACY_ROLES:
            role_conditions.append(and_(User.is_admin.is_(True), ~any_assignment))
        if role == "owner" and get_settings().admin_email_set:
            role_conditions.append(func.lower(User.email).in_(get_settings().admin_email_set))
        conditions.append(or_(*role_conditions))
    if verified is not None:
        conditions.append(
            User.email_verified_at.is_not(None) if verified else User.email_verified_at.is_(None)
        )
    if auth_method == "password":
        conditions.append(User.password_hash.is_not(None))
    elif auth_method:
        conditions.append(
            exists(
                select(UserAuthIdentity.id).where(
                    UserAuthIdentity.user_id == User.id,
                    UserAuthIdentity.provider == auth_method,
                    UserAuthIdentity.revoked_at.is_(None),
                )
            )
        )
    if registered_from is not None:
        conditions.append(User.created_at >= registered_from)
    if registered_to is not None:
        conditions.append(User.created_at <= registered_to)
    return conditions


async def _metadata_for_users(
    session: AsyncSession, users: list[User]
) -> tuple[dict[UUID, set[str]], dict[UUID, set[str]], dict[UUID, AccountErasureRequest]]:
    if not users:
        return {}, {}, {}
    ids = [user.id for user in users]
    now = datetime.now(UTC)
    role_rows = list(
        (
            await session.scalars(
                select(AdminRoleAssignment).where(AdminRoleAssignment.user_id.in_(ids))
            )
        ).all()
    )
    all_role_users = {row.user_id for row in role_rows}
    role_map: dict[UUID, set[str]] = {user.id: set() for user in users}
    for role_row in role_rows:
        expires = _aware(role_row.expires_at)
        if expires is None or expires > now:
            role_map[role_row.user_id].add(role_row.role)
    env_owners = get_settings().admin_email_set
    for user in users:
        if user.email.lower() in env_owners:
            role_map[user.id].add("owner")
        if user.is_admin and user.id not in all_role_users:
            role_map[user.id].update(LEGACY_ROLES)
    identities = list(
        (
            await session.scalars(
                select(UserAuthIdentity).where(
                    UserAuthIdentity.user_id.in_(ids), UserAuthIdentity.revoked_at.is_(None)
                )
            )
        ).all()
    )
    method_map: dict[UUID, set[str]] = {
        user.id: ({"password"} if user.password_hash else set()) for user in users
    }
    for identity in identities:
        method_map[identity.user_id].add(identity.provider)
    erasure_rows = list(
        (
            await session.scalars(
                select(AccountErasureRequest)
                .where(
                    AccountErasureRequest.user_id.in_(ids),
                    AccountErasureRequest.status.in_(ACTIVE_ERASURE_STATUSES),
                )
                .order_by(AccountErasureRequest.created_at.desc())
            )
        ).all()
    )
    erasures: dict[UUID, AccountErasureRequest] = {}
    for erasure_row in erasure_rows:
        erasures.setdefault(erasure_row.user_id, erasure_row)
    return role_map, method_map, erasures


async def list_admin_users(
    session: AsyncSession,
    actor: User,
    query: str | None,
    page: int,
    limit: int,
    *,
    status: str | None = None,
    role: str | None = None,
    verified: bool | None = None,
    auth_method: str | None = None,
    registered_from: datetime | None = None,
    registered_to: datetime | None = None,
    activity: str | None = None,
    sort: str = "created_at",
    direction: str = "desc",
) -> AdminUserList:
    activity_summary = _activity_summary_subquery()
    activity_count = func.coalesce(activity_summary.c.activity_count, 0)
    filters = _list_filters(
        query=query,
        status=status,
        role=role,
        verified=verified,
        auth_method=auth_method,
        registered_from=registered_from,
        registered_to=registered_to,
    )
    if activity == "has_activity":
        filters.append(activity_count > 0)
    elif activity == "no_activity":
        filters.append(activity_count == 0)
    env_admins = sorted(get_settings().admin_email_set)
    now = datetime.now(UTC)
    any_role_assignment = exists(
        select(AdminRoleAssignment.id).where(AdminRoleAssignment.user_id == User.id)
    )
    active_role_assignment = exists(
        select(AdminRoleAssignment.id).where(
            AdminRoleAssignment.user_id == User.id,
            or_(AdminRoleAssignment.expires_at.is_(None), AdminRoleAssignment.expires_at > now),
        )
    )
    effective_admin = or_(
        and_(User.is_admin.is_(True), ~any_role_assignment),
        func.lower(User.email).in_(env_admins) if env_admins else false(),
        active_role_assignment,
    )
    suspended = and_(
        User.suspended_at.is_not(None),
        or_(User.suspended_until.is_(None), User.suspended_until > now),
    )
    erasure_pending = exists(
        select(AccountErasureRequest.id).where(
            AccountErasureRequest.user_id == User.id,
            AccountErasureRequest.status.in_(ACTIVE_ERASURE_STATUSES),
        )
    )
    visibly_suspended = and_(
        User.is_active.is_(True),
        User.deleted_at.is_(None),
        ~erasure_pending,
        suspended,
    )
    truly_active = and_(
        User.is_active.is_(True),
        User.deleted_at.is_(None),
        ~suspended,
        ~erasure_pending,
    )
    stats_query = select(
        func.count(User.id),
        func.count(User.id).filter(truly_active),
        func.count(User.id).filter(effective_admin),
        func.coalesce(func.sum(UsageAccount.remaining_uses - UsageAccount.reserved_uses), 0),
        func.count(User.id).filter(visibly_suspended),
        func.count(User.id).filter(erasure_pending),
    ).outerjoin(UsageAccount, UsageAccount.user_id == User.id)
    if activity is not None:
        stats_query = stats_query.outerjoin(activity_summary, activity_summary.c.user_id == User.id)
    stats_row = (await session.execute(stats_query.where(*filters))).one()
    total = int(stats_row[0])
    sort_column = {
        "created_at": User.created_at,
        "last_login_at": User.last_login_at,
        "email": User.email,
        "updated_at": User.updated_at,
        "remaining_uses": UsageAccount.remaining_uses,
        "last_activity_at": activity_summary.c.last_activity_at,
        "activity_count": activity_count,
    }.get(sort, User.created_at)
    ordering = sort_column.asc() if direction == "asc" else sort_column.desc()
    rows = (
        await session.execute(
            select(
                User,
                UsageAccount,
                activity_summary.c.trips,
                activity_summary.c.searches,
                activity_summary.c.alerts,
                activity_summary.c.community_posts,
                activity_summary.c.community_comments,
                activity_summary.c.last_activity_at,
            )
            .outerjoin(UsageAccount, UsageAccount.user_id == User.id)
            .outerjoin(activity_summary, activity_summary.c.user_id == User.id)
            .where(*filters)
            .order_by(
                ordering.nullslast(),
                User.id.asc() if direction == "asc" else User.id.desc(),
            )
            .offset((page - 1) * limit)
            .limit(limit)
        )
    ).all()
    users = [row[0] for row in rows]
    roles, methods, erasures = await _metadata_for_users(session, users)
    return AdminUserList(
        items=[
            _summary(
                row[0],
                row[1],
                actor,
                roles=roles[row[0].id],
                auth_methods=methods[row[0].id],
                erasure=erasures.get(row[0].id),
                activity=_activity_model(row[2], row[3], row[4], row[5], row[6]),
                last_activity_at=row[7],
            )
            for row in rows
        ],
        page=page,
        limit=limit,
        total=total,
        pages=max(1, math.ceil(total / limit)),
        stats=AdminUserStats(
            total=total,
            active=int(stats_row[1]),
            administrators=int(stats_row[2]),
            available_uses=int(stats_row[3]),
            suspended=int(stats_row[4]),
            erasure_pending=int(stats_row[5]),
        ),
    )


async def _user_and_account(
    session: AsyncSession,
    user_id: UUID,
    *,
    lock_user: bool = False,
    lock_account: bool = False,
) -> tuple[User, UsageAccount | None]:
    user_query = select(User).where(User.id == user_id)
    if lock_user:
        user_query = user_query.with_for_update()
    user = await session.scalar(user_query)
    if user is None:
        raise AppError(404, "admin_user_not_found", "找不到這個會員帳號")
    account_query = select(UsageAccount).where(UsageAccount.user_id == user_id)
    if lock_account:
        account_query = account_query.with_for_update()
    return user, await session.scalar(account_query)


async def admin_user_detail(session: AsyncSession, user_id: UUID, actor: User) -> AdminUserDetail:
    user, account = await _user_and_account(session, user_id)
    roles, methods, erasures = await _metadata_for_users(session, [user])
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
    identities = list(
        (
            await session.scalars(
                select(UserAuthIdentity)
                .where(UserAuthIdentity.user_id == user_id, UserAuthIdentity.revoked_at.is_(None))
                .order_by(UserAuthIdentity.created_at)
            )
        ).all()
    )
    activity_summary = _activity_summary_subquery()
    activity_row = (
        await session.execute(
            select(
                activity_summary.c.trips,
                activity_summary.c.searches,
                activity_summary.c.alerts,
                activity_summary.c.community_posts,
                activity_summary.c.community_comments,
                activity_summary.c.last_activity_at,
            ).where(activity_summary.c.user_id == user_id)
        )
    ).one_or_none()
    activity = (
        _activity_model(*activity_row[:5]) if activity_row is not None else AdminUserActivity()
    )
    last_activity_at = activity_row[5] if activity_row is not None else None
    erasure = erasures.get(user.id)
    summary = _summary(
        user,
        account,
        actor,
        roles=roles[user.id],
        auth_methods=methods[user.id],
        erasure=erasure,
        activity=activity,
        last_activity_at=last_activity_at,
    )
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
        admin_history=[_audit_item(item) for item in audits],
        auth_identities=[
            AdminAuthIdentityItem(
                provider=item.provider,
                email=item.provider_email,
                email_verified=item.email_verified,
                linked_at=item.created_at,
                last_login_at=item.last_login_at,
            )
            for item in identities
        ],
        erasure=(
            AdminErasureStatus(
                id=erasure.id,
                status=erasure.status,
                scheduled_for=erasure.scheduled_for,
                requested_at=erasure.created_at,
                cancelled_at=erasure.cancelled_at,
                completed_at=erasure.completed_at,
                reason=erasure.reason,
            )
            if erasure
            else None
        ),
    )


def _environment_designated(user: User) -> bool:
    settings = get_settings()
    return user.email.lower() in (
        settings.admin_email_set
        | settings.deploy_admin_email_set
        | settings.database_admin_email_set
    )


async def update_admin_user(
    session: AsyncSession, user_id: UUID, payload: AdminUserUpdate, actor: User
) -> AdminUserDetail:
    user, _ = await _user_and_account(session, user_id, lock_user=True)
    if _environment_designated(user) and (payload.is_admin is False or payload.is_active is False):
        raise AppError(
            409, "admin_environment_override", "此帳號由主機環境授權，請先從主機環境設定移除"
        )
    if payload.is_admin is not None:
        raise AppError(
            409,
            "admin_role_endpoint_required",
            "管理員角色只能透過角色設定流程變更",
        )
    if payload.is_active is False:
        raise AppError(
            409,
            "admin_suspension_endpoint_required",
            "停用帳號請使用具備原因與重新驗證的停權流程",
        )
    if user.deleted_at is not None:
        raise AppError(409, "admin_deleted_user", "已清除個資的帳號不可重新啟用")
    changed: dict[str, bool] = {}
    if payload.is_active is not None and payload.is_active != user.is_active:
        user.is_active = payload.is_active
        user.auth_version = (user.auth_version or 1) + 1
        changed["is_active"] = payload.is_active
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
        raise AppError(409, "admin_self_usage_adjustment", "不可調整目前登入管理員自己的使用次數")
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
                409, "admin_adjustment_key_reused", "Idempotency-Key 已用於不同的次數調整"
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
        metadata_json={"actor_user_id": str(actor.id)},
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
    ledger_id, balance_after = ledger.id, account.remaining_uses
    await session.commit()
    return AdminUsageAdjustmentResult(
        user=await admin_user_detail(session, user.id, actor),
        ledger_id=ledger_id,
        change=payload.change,
        balance_after=balance_after,
        replayed=False,
    )


async def _idempotency_replay(
    session: AsyncSession,
    *,
    action: str,
    target: str,
    actor: User,
    key: str,
    fingerprint: str,
) -> bool:
    rows = list(
        (
            await session.scalars(
                select(AdminAuditLog)
                .where(
                    AdminAuditLog.actor_user_id == actor.id,
                    AdminAuditLog.action == action,
                    AdminAuditLog.target == target,
                )
                .order_by(AdminAuditLog.created_at.desc())
            )
        ).all()
    )
    for row in rows:
        if row.metadata_json.get("idempotency_key") != key:
            continue
        if row.metadata_json.get("fingerprint") != fingerprint:
            raise AppError(409, "admin_idempotency_key_reused", "Idempotency-Key 已用於不同操作")
        return True
    return False


async def _active_roles(session: AsyncSession, user: User) -> set[str]:
    now = datetime.now(UTC)
    rows = list(
        (
            await session.scalars(
                select(AdminRoleAssignment)
                .where(AdminRoleAssignment.user_id == user.id)
                .with_for_update()
            )
        ).all()
    )
    roles: set[str] = set()
    for row in rows:
        expires = _aware(row.expires_at)
        if expires is None or expires > now:
            roles.add(row.role)
    if user.email.lower() in get_settings().admin_email_set:
        roles.add("owner")
    if user.is_admin and not rows:
        roles.update(LEGACY_ROLES)
    return roles


async def _ensure_not_last_owner(session: AsyncSession, target: User) -> None:
    if "owner" not in await _active_roles(session, target):
        return
    now = datetime.now(UTC)
    active_erasure = exists(
        select(AccountErasureRequest.id).where(
            AccountErasureRequest.user_id == User.id,
            AccountErasureRequest.status.in_(ACTIVE_ERASURE_STATUSES),
        )
    )
    other_env_emails = get_settings().admin_email_set - {target.email.lower()}
    if other_env_emails:
        active_environment_owner = await session.scalar(
            select(User.id)
            .where(
                func.lower(User.email).in_(other_env_emails),
                User.is_active.is_(True),
                User.deleted_at.is_(None),
                ~active_erasure,
                or_(
                    User.suspended_at.is_(None),
                    and_(User.suspended_until.is_not(None), User.suspended_until <= now),
                ),
            )
            .with_for_update()
            .limit(1)
        )
        if active_environment_owner is not None:
            return
    other = await session.scalar(
        select(AdminRoleAssignment.id)
        .join(User, User.id == AdminRoleAssignment.user_id)
        .where(
            AdminRoleAssignment.user_id != target.id,
            AdminRoleAssignment.role == "owner",
            User.is_active.is_(True),
            User.deleted_at.is_(None),
            ~active_erasure,
            or_(
                User.suspended_at.is_(None),
                and_(User.suspended_until.is_not(None), User.suspended_until <= now),
            ),
            # A temporary owner cannot be the durable recovery path for the
            # account being changed. Otherwise both safeguards can disappear
            # as soon as this assignment expires without another mutation.
            AdminRoleAssignment.expires_at.is_(None),
        )
        .with_for_update()
        .limit(1)
    )
    if other is None:
        raise AppError(409, "admin_last_owner", "至少必須保留一位可用的 owner")


async def replace_admin_roles(
    session: AsyncSession,
    user_id: UUID,
    payload: AdminRolesUpdate,
    actor: User,
    idempotency_key: str,
) -> AdminActionResult:
    async with _owner_mutation_guard(session):
        return await _replace_admin_roles_serialized(
            session, user_id, payload, actor, idempotency_key
        )


async def _replace_admin_roles_serialized(
    session: AsyncSession,
    user_id: UUID,
    payload: AdminRolesUpdate,
    actor: User,
    idempotency_key: str,
) -> AdminActionResult:
    user, _ = await _user_and_account(session, user_id, lock_user=True)
    expires_at = _aware(payload.expires_at)
    if expires_at is not None and expires_at <= datetime.now(UTC):
        raise AppError(422, "admin_role_expiry_invalid", "角色到期時間必須晚於現在")
    if expires_at is not None and "owner" in payload.roles:
        raise AppError(422, "admin_owner_expiry_unsupported", "owner 角色不可設定到期時間")
    expected = f"ROLES {user.email}"
    if payload.confirmation != expected:
        raise AppError(409, "admin_confirmation_mismatch", f"請輸入 {expected}")
    if user.id == actor.id:
        raise AppError(409, "admin_self_role_change", "不可變更目前登入帳號自己的角色")
    if user.email.lower() in get_settings().admin_email_set:
        raise AppError(409, "admin_environment_override", "環境 owner 的角色不可由後台變更")
    current_roles, requested = await _active_roles(session, user), set(payload.roles)
    if "owner" in current_roles and "owner" not in requested:
        await _ensure_not_last_owner(session, user)
    fingerprint = "|".join(sorted(requested)) + f"|{expires_at}|{payload.reason}"
    if await _idempotency_replay(
        session,
        action="user_roles_updated",
        target=f"user:{user.id}",
        actor=actor,
        key=idempotency_key,
        fingerprint=fingerprint,
    ):
        return AdminActionResult(
            user=await admin_user_detail(session, user.id, actor), replayed=True
        )
    assignments = list(
        (
            await session.scalars(
                select(AdminRoleAssignment).where(AdminRoleAssignment.user_id == user.id)
            )
        ).all()
    )
    by_role = {item.role: item for item in assignments}
    for item in assignments:
        if item.role not in requested:
            await session.delete(item)
    for role in requested:
        existing_assignment = by_role.get(role)
        if existing_assignment is None:
            session.add(
                AdminRoleAssignment(
                    user_id=user.id,
                    role=role,
                    granted_by_user_id=actor.id,
                    source="manual",
                    expires_at=expires_at,
                )
            )
        else:
            existing_assignment.granted_by_user_id = actor.id
            existing_assignment.source = "manual"
            existing_assignment.expires_at = expires_at
    user.is_admin = bool(requested)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="user_roles_updated",
            target=f"user:{user.id}",
            metadata_json={
                "email": user.email,
                "roles": sorted(requested),
                "expires_at": expires_at.isoformat() if expires_at else None,
                "reason": payload.reason,
                "idempotency_key": idempotency_key,
                "fingerprint": fingerprint,
            },
        )
    )
    await session.commit()
    return AdminActionResult(user=await admin_user_detail(session, user.id, actor))


async def suspend_admin_user(
    session: AsyncSession,
    user_id: UUID,
    payload: AdminSuspensionRequest,
    actor: User,
    idempotency_key: str,
) -> AdminActionResult:
    async with _owner_mutation_guard(session):
        return await _suspend_admin_user_serialized(
            session, user_id, payload, actor, idempotency_key
        )


async def _suspend_admin_user_serialized(
    session: AsyncSession,
    user_id: UUID,
    payload: AdminSuspensionRequest,
    actor: User,
    idempotency_key: str,
) -> AdminActionResult:
    user, _ = await _user_and_account(session, user_id, lock_user=True)
    if user.id == actor.id:
        raise AppError(409, "admin_self_suspension", "不可停權目前登入的管理員帳號")
    if _environment_designated(user):
        raise AppError(409, "admin_environment_override", "主機環境指定帳號不可由後台停權")
    now = datetime.now(UTC)
    until = _aware(payload.suspended_until)
    if until is not None and until <= now:
        raise AppError(422, "admin_suspension_time_invalid", "停權結束時間必須晚於現在")
    if until is not None and until > now + MAX_TIMED_SUSPENSION:
        raise AppError(
            422,
            "admin_suspension_time_too_far",
            "限時停權最多可設定 90 天；更長期間請使用需再次驗證的永久停權",
        )
    if until is None and payload.confirmation != f"SUSPEND {user.email}":
        raise AppError(409, "admin_confirmation_mismatch", f"請輸入 SUSPEND {user.email}")
    await _ensure_not_last_owner(session, user)
    fingerprint = f"{until}|{payload.reason}"
    if await _idempotency_replay(
        session,
        action="user_suspended",
        target=f"user:{user.id}",
        actor=actor,
        key=idempotency_key,
        fingerprint=fingerprint,
    ):
        return AdminActionResult(
            user=await admin_user_detail(session, user.id, actor), replayed=True
        )
    user.suspended_at = now
    user.suspended_until = until
    user.suspension_reason = payload.reason
    user.auth_version = (user.auth_version or 1) + 1
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="user_suspended",
            target=f"user:{user.id}",
            metadata_json={
                "email": user.email,
                "until": until.isoformat() if until else None,
                "reason": payload.reason,
                "idempotency_key": idempotency_key,
                "fingerprint": fingerprint,
            },
        )
    )
    await session.commit()
    return AdminActionResult(user=await admin_user_detail(session, user.id, actor))


async def unsuspend_admin_user(
    session: AsyncSession, user_id: UUID, payload: AdminReasonRequest, actor: User
) -> AdminUserDetail:
    user, _ = await _user_and_account(session, user_id, lock_user=True)
    user.suspended_at = user.suspended_until = None
    user.suspension_reason = None
    user.auth_version = (user.auth_version or 1) + 1
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="user_suspension_removed",
            target=f"user:{user.id}",
            metadata_json={"email": user.email, "reason": payload.reason},
        )
    )
    await session.commit()
    return await admin_user_detail(session, user.id, actor)


async def revoke_admin_user_sessions(
    session: AsyncSession, user_id: UUID, payload: AdminReasonRequest, actor: User
) -> AdminUserDetail:
    user, _ = await _user_and_account(session, user_id, lock_user=True)
    user.auth_version = (user.auth_version or 1) + 1
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="user_sessions_revoked",
            target=f"user:{user.id}",
            metadata_json={"email": user.email, "reason": payload.reason},
        )
    )
    await session.commit()
    return await admin_user_detail(session, user.id, actor)


async def resend_admin_verification(
    session: AsyncSession, user_id: UUID, actor: User
) -> AdminUserDetail:
    user, _ = await _user_and_account(session, user_id, lock_user=True)
    await enforce_named_rate_limit(
        "admin-verification-user", str(user.id), limit=3, window_seconds=3_600
    )
    if not user.is_active or user.deleted_at is not None:
        raise AppError(409, "admin_user_inactive", "停用或已清除的帳號不能重寄驗證信")
    active_erasure = await session.scalar(
        select(AccountErasureRequest.id)
        .where(
            AccountErasureRequest.user_id == user.id,
            AccountErasureRequest.status.in_(ACTIVE_ERASURE_STATUSES),
        )
        .with_for_update()
    )
    if active_erasure is not None:
        raise AppError(409, "admin_erasure_in_progress", "個資清除期間不能重寄驗證信")
    mail_created = user.email_verified_at is None
    if user.email_verified_at is None:
        await request_mail(
            session,
            user,
            "verify",
            user.preferred_locale,
            commit=False,
            enqueue=False,
        )
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="user_verification_resent",
            target=f"user:{user.id}",
            metadata_json={
                "email": user.email,
                "already_verified": user.email_verified_at is not None,
            },
        )
    )
    await session.commit()
    if mail_created:
        enqueue_jobs()
    return await admin_user_detail(session, user.id, actor)


async def schedule_admin_erasure(
    session: AsyncSession,
    user_id: UUID,
    payload: AdminErasureRequest,
    actor: User,
    idempotency_key: str,
) -> AdminActionResult:
    async with _owner_mutation_guard(session):
        return await _schedule_admin_erasure_serialized(
            session, user_id, payload, actor, idempotency_key
        )


async def _schedule_admin_erasure_serialized(
    session: AsyncSession,
    user_id: UUID,
    payload: AdminErasureRequest,
    actor: User,
    idempotency_key: str,
) -> AdminActionResult:
    user, _ = await _user_and_account(session, user_id, lock_user=True)
    expected = f"ERASE {user.email}"
    if payload.confirmation != expected:
        raise AppError(409, "admin_confirmation_mismatch", f"請輸入 {expected}")
    if user.id == actor.id:
        raise AppError(409, "admin_self_erasure", "不可清除目前登入的管理員帳號")
    if _environment_designated(user):
        raise AppError(409, "admin_environment_override", "主機環境指定帳號不可由後台清除")
    await _ensure_not_last_owner(session, user)
    existing_request = await session.scalar(
        select(AccountErasureRequest).where(
            AccountErasureRequest.requested_by_user_id == actor.id,
            AccountErasureRequest.idempotency_key == idempotency_key,
        )
    )
    if existing_request is not None:
        if existing_request.user_id != user.id or existing_request.reason != payload.reason:
            raise AppError(
                409,
                "admin_idempotency_key_reused",
                "Idempotency-Key 已用於不同操作",
            )
        return AdminActionResult(
            user=await admin_user_detail(session, user.id, actor), replayed=True
        )
    if await _idempotency_replay(
        session,
        action="user_erasure_scheduled",
        target=f"user:{user.id}",
        actor=actor,
        key=idempotency_key,
        fingerprint=payload.reason,
    ):
        return AdminActionResult(
            user=await admin_user_detail(session, user.id, actor), replayed=True
        )
    active = await session.scalar(
        select(AccountErasureRequest).where(
            AccountErasureRequest.user_id == user.id,
            AccountErasureRequest.status.in_(ACTIVE_ERASURE_STATUSES),
        )
    )
    if active is not None:
        raise AppError(409, "admin_erasure_exists", "這個帳號已有待執行的個資清除")
    scheduled_for = datetime.now(UTC) + timedelta(hours=24)
    session.add(
        AccountErasureRequest(
            user_id=user.id,
            requested_by_user_id=actor.id,
            idempotency_key=idempotency_key,
            status="scheduled",
            reason=payload.reason,
            scheduled_for=scheduled_for,
        )
    )
    session.add(Job(kind="admin_erase_account", user_id=user.id, available_at=scheduled_for))
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="user_erasure_scheduled",
            target=f"user:{user.id}",
            metadata_json={
                "email": user.email,
                "scheduled_for": scheduled_for.isoformat(),
                "reason": payload.reason,
                "idempotency_key": idempotency_key,
                "fingerprint": payload.reason,
            },
        )
    )
    await session.commit()
    enqueue_jobs()
    return AdminActionResult(user=await admin_user_detail(session, user.id, actor))


async def cancel_admin_erasure(
    session: AsyncSession, user_id: UUID, payload: AdminReasonRequest, actor: User
) -> AdminUserDetail:
    # The worker claims a due Job before it locks User and AccountErasureRequest.
    # Claim every matching pending job in the same order first, or cancellation
    # can hold User while waiting for the worker's Job lock and deadlock with the
    # worker waiting for that User lock.
    jobs = list(
        (
            await session.scalars(
                select(Job)
                .where(
                    Job.user_id == user_id,
                    Job.kind == "admin_erase_account",
                    Job.status == "pending",
                )
                .order_by(Job.created_at, Job.id)
                .with_for_update()
            )
        ).all()
    )
    user, _ = await _user_and_account(session, user_id, lock_user=True)
    erasure = await session.scalar(
        select(AccountErasureRequest)
        .where(
            AccountErasureRequest.user_id == user.id,
            AccountErasureRequest.status == "scheduled",
        )
        .with_for_update()
    )
    if erasure is None:
        raise AppError(409, "admin_erasure_not_scheduled", "這個帳號沒有可取消的個資清除")
    erasure.status = "cancelled"
    erasure.cancelled_at = datetime.now(UTC)
    for job in jobs:
        job.status = "completed"
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="user_erasure_cancelled",
            target=f"user:{user.id}",
            metadata_json={"email": user.email, "reason": payload.reason},
        )
    )
    await session.commit()
    return await admin_user_detail(session, user.id, actor)
