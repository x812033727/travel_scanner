from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi import Path as PathParam
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai_accounts import service
from app.ai_accounts.schemas import (
    AiAccountsOverview,
    AiDefaultRequest,
    AiDefaults,
    AiLoginCodeRequest,
    AiLoginSession,
    AiLogoutResult,
    Slot,
    Tool,
)
from app.auth.service import require_capability
from app.db import get_session
from app.infra import client_ip, enforce_named_rate_limit
from app.models import User

router = APIRouter(prefix="/admin/ai-accounts", tags=["admin ai accounts"])
Session = Annotated[AsyncSession, Depends(get_session)]
# Owner only, and said here rather than left to the fall-through in
# `_admin_path_capability`: signing root's CLIs in to an account is a host-level change,
# and a later "/admin/ai" rule there must not quietly widen who may do it.
Owner = Annotated[User, Depends(require_capability("roles.manage"))]
LoginId = Annotated[str, PathParam(pattern=r"^[0-9a-f]{32}$")]


async def _limit_logins(user: User, request: Request) -> None:
    await enforce_named_rate_limit(
        "ai-account-login", f"{user.id}:{client_ip(request)}", limit=20, window_seconds=3_600
    )


@router.get("", response_model=AiAccountsOverview)
async def get_ai_accounts(user: Owner, fresh: bool = False) -> AiAccountsOverview:
    _ = user
    return await service.overview(fresh=fresh)


@router.post(
    "/{tool}/{slot}/login", response_model=AiLoginSession, status_code=status.HTTP_201_CREATED
)
async def post_login(
    tool: Tool, slot: Slot, user: Owner, session: Session, request: Request
) -> AiLoginSession:
    client = service.agent_client()
    await _limit_logins(user, request)
    login = await client.start_login(tool, slot)
    await service.audit(
        session,
        user,
        "ai_account.login_started",
        f"ai-login:{login.id}",
        {"tool": tool, "slot": slot, "kind": login.kind},
    )
    return login


@router.get("/logins/{login_id}", response_model=AiLoginSession)
async def get_login(login_id: LoginId, user: Owner, session: Session) -> AiLoginSession:
    login = await service.agent_client().login(login_id)
    await service.audit_login_outcome(session, user, login)
    return login


@router.post(
    "/logins/{login_id}/code",
    response_model=AiLoginSession,
    status_code=status.HTTP_202_ACCEPTED,
)
async def post_login_code(
    login_id: LoginId, payload: AiLoginCodeRequest, user: Owner, request: Request
) -> AiLoginSession:
    client = service.agent_client()
    await _limit_logins(user, request)
    # Never logged or audited: the code is a one-time credential.
    return await client.submit_code(login_id, payload.code.strip())


@router.post("/logins/{login_id}/cancel", response_model=AiLoginSession)
async def post_login_cancel(login_id: LoginId, user: Owner, session: Session) -> AiLoginSession:
    login = await service.agent_client().cancel_login(login_id)
    await service.audit_login_outcome(session, user, login)
    return login


@router.post("/{tool}/{slot}/logout", response_model=AiLogoutResult)
async def post_logout(tool: Tool, slot: Slot, user: Owner, session: Session) -> AiLogoutResult:
    result = await service.agent_client().logout(tool, slot)
    await service.audit(
        session,
        user,
        "ai_account.logout",
        f"ai-account:{tool}-{slot}",
        {"tool": tool, "slot": slot},
    )
    return result


@router.put("/defaults/{tool}", response_model=AiDefaults)
async def put_default(
    tool: Tool, payload: AiDefaultRequest, user: Owner, session: Session
) -> AiDefaults:
    result = await service.agent_client().set_default(tool, payload.slot)
    await service.audit(
        session,
        user,
        "ai_account.default_changed",
        f"ai-account:{tool}",
        {"tool": tool, "slot": payload.slot},
    )
    return result
