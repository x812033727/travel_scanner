from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.user_schemas import (
    AdminActionResult,
    AdminErasureRequest,
    AdminReasonRequest,
    AdminRolesUpdate,
    AdminSuspensionRequest,
    AdminUsageAdjustment,
    AdminUsageAdjustmentResult,
    AdminUserDetail,
    AdminUserList,
    AdminUserUpdate,
)
from app.admin.users import (
    adjust_admin_user_usage,
    admin_user_detail,
    cancel_admin_erasure,
    list_admin_users,
    replace_admin_roles,
    resend_admin_verification,
    revoke_admin_user_sessions,
    schedule_admin_erasure,
    suspend_admin_user,
    unsuspend_admin_user,
    update_admin_user,
)
from app.auth.service import require_admin_step_up, require_capability
from app.db import get_session
from app.models import User

router = APIRouter(prefix="/admin/users", tags=["admin users"])
Session = Annotated[AsyncSession, Depends(get_session)]
UsersReader = Annotated[User, Depends(require_capability("users.read"))]
UsersManager = Annotated[User, Depends(require_capability("users.manage"))]
UsageManager = Annotated[User, Depends(require_capability("usage.manage"))]
RolesManager = Annotated[User, Depends(require_capability("roles.manage"))]
IdempotencyKey = Annotated[
    str,
    Header(alias="Idempotency-Key", min_length=8, max_length=120),
]


@router.get("", response_model=AdminUserList)
async def get_admin_users(
    user: UsersReader,
    session: Session,
    query: Annotated[str | None, Query(max_length=320)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    status: Annotated[
        Literal["active", "inactive", "suspended", "erasure_pending"] | None, Query()
    ] = None,
    role: Annotated[
        Literal[
            "viewer",
            "support",
            "content",
            "operations",
            "database_operator",
            "deployer",
            "owner",
        ]
        | None,
        Query(),
    ] = None,
    verified: Annotated[bool | None, Query()] = None,
    auth_method: Annotated[Literal["password", "google", "line", "apple"] | None, Query()] = None,
    registered_from: Annotated[datetime | None, Query()] = None,
    registered_to: Annotated[datetime | None, Query()] = None,
    activity: Annotated[Literal["has_activity", "no_activity"] | None, Query()] = None,
    sort: Annotated[
        Literal[
            "created_at",
            "last_login_at",
            "last_activity_at",
            "activity_count",
            "email",
            "updated_at",
            "remaining_uses",
        ],
        Query(),
    ] = "created_at",
    direction: Annotated[Literal["asc", "desc"], Query()] = "desc",
) -> AdminUserList:
    return await list_admin_users(
        session,
        user,
        query,
        page,
        limit,
        status=status,
        role=role,
        verified=verified,
        auth_method=auth_method,
        registered_from=registered_from,
        registered_to=registered_to,
        activity=activity,
        sort=sort,
        direction=direction,
    )


@router.get("/{user_id}", response_model=AdminUserDetail)
async def get_admin_user(user_id: UUID, user: UsersReader, session: Session) -> AdminUserDetail:
    return await admin_user_detail(session, user_id, user)


@router.put("/{user_id}", response_model=AdminUserDetail)
async def put_admin_user(
    user_id: UUID,
    payload: AdminUserUpdate,
    user: UsersManager,
    session: Session,
) -> AdminUserDetail:
    return await update_admin_user(session, user_id, payload, user)


@router.post("/{user_id}/usage-adjustments", response_model=AdminUsageAdjustmentResult)
async def post_admin_usage_adjustment(
    user_id: UUID,
    payload: AdminUsageAdjustment,
    user: UsageManager,
    session: Session,
    idempotency_key: IdempotencyKey,
) -> AdminUsageAdjustmentResult:
    return await adjust_admin_user_usage(session, user_id, payload, user, idempotency_key)


@router.patch("/{user_id}/roles", response_model=AdminActionResult)
async def patch_admin_user_roles(
    user_id: UUID,
    payload: AdminRolesUpdate,
    request: Request,
    user: RolesManager,
    session: Session,
    idempotency_key: IdempotencyKey,
) -> AdminActionResult:
    await require_admin_step_up(request, user, "users.roles")
    return await replace_admin_roles(session, user_id, payload, user, idempotency_key)


@router.post("/{user_id}/suspension", response_model=AdminActionResult)
async def post_admin_user_suspension(
    user_id: UUID,
    payload: AdminSuspensionRequest,
    request: Request,
    user: UsersManager,
    session: Session,
    idempotency_key: IdempotencyKey,
) -> AdminActionResult:
    if payload.suspended_until is None:
        await require_admin_step_up(request, user, "users.suspend_permanent")
    return await suspend_admin_user(session, user_id, payload, user, idempotency_key)


@router.delete("/{user_id}/suspension", response_model=AdminUserDetail)
async def delete_admin_user_suspension(
    user_id: UUID,
    payload: AdminReasonRequest,
    user: UsersManager,
    session: Session,
) -> AdminUserDetail:
    return await unsuspend_admin_user(session, user_id, payload, user)


@router.post("/{user_id}/sessions/revoke", response_model=AdminUserDetail)
async def post_admin_user_session_revocation(
    user_id: UUID,
    payload: AdminReasonRequest,
    user: UsersManager,
    session: Session,
) -> AdminUserDetail:
    return await revoke_admin_user_sessions(session, user_id, payload, user)


@router.post("/{user_id}/verification", response_model=AdminUserDetail, status_code=202)
async def post_admin_user_verification(
    user_id: UUID,
    user: UsersManager,
    session: Session,
) -> AdminUserDetail:
    return await resend_admin_verification(session, user_id, user)


@router.post("/{user_id}/erasure", response_model=AdminActionResult, status_code=202)
async def post_admin_user_erasure(
    user_id: UUID,
    payload: AdminErasureRequest,
    request: Request,
    user: UsersManager,
    session: Session,
    idempotency_key: IdempotencyKey,
) -> AdminActionResult:
    await require_admin_step_up(request, user, "users.erase")
    return await schedule_admin_erasure(session, user_id, payload, user, idempotency_key)


@router.delete("/{user_id}/erasure", response_model=AdminUserDetail)
async def delete_admin_user_erasure(
    user_id: UUID,
    payload: AdminReasonRequest,
    user: UsersManager,
    session: Session,
) -> AdminUserDetail:
    return await cancel_admin_erasure(session, user_id, payload, user)
