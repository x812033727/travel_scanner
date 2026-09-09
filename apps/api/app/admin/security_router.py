from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.user_schemas import AdminStepUpRequest, AdminStepUpResponse
from app.auth.service import (
    STEP_UP_SCOPE_CAPABILITY,
    STEP_UP_TTL_SECONDS,
    AdminUser,
    cached_admin_capabilities,
    create_admin_step_up_token,
    set_admin_step_up_cookie,
    verify_password,
)
from app.db import get_session
from app.infra import enforce_named_rate_limit
from app.models import AdminAuditLog
from app.problems import AppError

router = APIRouter(prefix="/admin", tags=["admin security"])
Session = Annotated[AsyncSession, Depends(get_session)]


async def _record_step_up(
    session: AsyncSession,
    user: AdminUser,
    scopes: list[str],
    *,
    result: str,
    code: str | None = None,
) -> None:
    metadata: dict[str, object] = {"result": result, "scopes": sorted(scopes)}
    if code:
        metadata["code"] = code
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action=f"admin_step_up_{result}",
            target=f"user:{user.id}",
            metadata_json=metadata,
        )
    )
    await session.commit()


@router.post("/step-up", response_model=AdminStepUpResponse)
async def step_up(
    payload: AdminStepUpRequest,
    request: Request,
    response: Response,
    user: AdminUser,
    session: Session,
) -> AdminStepUpResponse:
    del request  # The account-scoped limiter intentionally does not trust proxy IP headers.
    await enforce_named_rate_limit(
        "admin-step-up-user",
        str(user.id),
        limit=5,
        window_seconds=3_600,
    )
    if not user.password_hash:
        await _record_step_up(
            session,
            user,
            list(payload.scopes),
            result="failed",
            code="admin_password_not_set",
        )
        raise AppError(
            409,
            "admin_password_not_set",
            "這個管理員只使用第三方登入，請先透過帳號安全流程設定本機密碼",
        )
    if not verify_password(payload.password, user.password_hash):
        await _record_step_up(
            session,
            user,
            list(payload.scopes),
            result="failed",
            code="invalid_credentials",
        )
        raise AppError(401, "invalid_credentials", "目前密碼不正確")
    capabilities = cached_admin_capabilities(user)
    missing = [
        scope for scope in payload.scopes if STEP_UP_SCOPE_CAPABILITY[scope] not in capabilities
    ]
    if missing:
        await _record_step_up(
            session,
            user,
            list(payload.scopes),
            result="failed",
            code="admin_capability_required",
        )
        raise AppError(403, "admin_capability_required", "目前管理員角色沒有這項操作權限")
    token, expires_at = create_admin_step_up_token(user, payload.scopes)
    await _record_step_up(session, user, list(payload.scopes), result="succeeded")
    set_admin_step_up_cookie(response, token)
    response.headers["Cache-Control"] = "no-store"
    return AdminStepUpResponse(
        scopes=payload.scopes,
        expires_at=expires_at,
        expires_in=STEP_UP_TTL_SECONDS,
    )
