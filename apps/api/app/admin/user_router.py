from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.user_schemas import (
    AdminUsageAdjustment,
    AdminUsageAdjustmentResult,
    AdminUserDetail,
    AdminUserList,
    AdminUserUpdate,
)
from app.admin.users import (
    adjust_admin_user_usage,
    admin_user_detail,
    list_admin_users,
    update_admin_user,
)
from app.auth.service import AdminUser
from app.db import get_session

router = APIRouter(prefix="/admin/users", tags=["admin users"])
Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=AdminUserList)
async def get_admin_users(
    user: AdminUser,
    session: Session,
    query: Annotated[str | None, Query(max_length=320)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> AdminUserList:
    return await list_admin_users(session, user, query, page, limit)


@router.get("/{user_id}", response_model=AdminUserDetail)
async def get_admin_user(user_id: UUID, user: AdminUser, session: Session) -> AdminUserDetail:
    return await admin_user_detail(session, user_id, user)


@router.put("/{user_id}", response_model=AdminUserDetail)
async def put_admin_user(
    user_id: UUID,
    payload: AdminUserUpdate,
    user: AdminUser,
    session: Session,
) -> AdminUserDetail:
    return await update_admin_user(session, user_id, payload, user)


@router.post("/{user_id}/usage-adjustments", response_model=AdminUsageAdjustmentResult)
async def post_admin_usage_adjustment(
    user_id: UUID,
    payload: AdminUsageAdjustment,
    user: AdminUser,
    session: Session,
    idempotency_key: Annotated[
        str,
        Header(alias="Idempotency-Key", min_length=8, max_length=120),
    ],
) -> AdminUsageAdjustmentResult:
    return await adjust_admin_user_usage(session, user_id, payload, user, idempotency_key)
