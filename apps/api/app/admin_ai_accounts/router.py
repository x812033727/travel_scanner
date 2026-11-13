from typing import Annotated, Any, Literal

from fastapi import APIRouter, Depends, Query, Request, Response, status
from fastapi import Path as PathParam
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin_ai_accounts import colab_leases, service
from app.admin_ai_accounts.schemas import (
    HOLDER_PATTERN,
    AiAccountsOverview,
    AiDefaultRequest,
    AiDefaults,
    AiLoginCodeRequest,
    AiLoginSession,
    AiLogoutResult,
    ColabAccounts,
    ColabCredentials,
    ColabLease,
    ColabLeaseRequest,
    ColabReleaseRequest,
    ColabReleaseResult,
    Slot,
    Tool,
)
from app.auth.service import require_capability
from app.db import get_session
from app.infra import client_ip, enforce_named_rate_limit
from app.models import AdminAuditLog, User, VideoToolToken
from app.problems import AppError
from app.video_speech.admin_api import video_tool

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


@router.post("/colab/{slot}/lease/break", response_model=ColabReleaseResult)
async def post_break_colab_lease(slot: Slot, user: Owner, session: Session) -> ColabReleaseResult:
    """The owner ends an agent's lease on a Colab account, e.g. one a crashed agent left.

    The agent's next renewal takes it again if the account is still free, so this is for an
    agent that is gone; the audit row names whose lease it was.
    """
    broken = await colab_leases.break_lease(slot)
    if broken is not None:
        await service.audit(
            session,
            user,
            "ai_account.colab_lease_broken",
            f"ai-account:colab-{slot}",
            {"holder": broken.holder, "token": broken.token},
        )
    return ColabReleaseResult(slot=slot, released=broken is not None)


# What a paired cloud session calls with its video tool token, through the web route
# apps/web/app/api/video/colab-credentials (nginx exposes only the web app). No browser session
# reaches it: the dependency takes a bearer token and nothing else.
colab_tool_router = APIRouter(prefix="/video/colab-credentials", tags=["video tool"])
CREDENTIAL_FETCHES_PER_HOUR = 30


@colab_tool_router.get("", response_model=ColabCredentials)
async def get_colab_credentials(
    session: Session,
    response: Response,
    token: Annotated[VideoToolToken, Depends(video_tool)],
    slot: Slot | Literal["default"] = "default",
    holder: Annotated[str | None, Query(pattern=HOLDER_PATTERN)] = None,
) -> ColabCredentials:
    """The Colab CLI token file of one account the owner signed in on /admin/ai-accounts.

    Only a video tool token the owner marked for Colab gets it (`colab_access`: a pairing that
    asked for Colab and was allowed, or the box on the admin card). Every fetch is audited
    against the token; the credentials themselves are never logged. An account another agent
    leased (`/video/colab-accounts/{slot}/lease`) is refused with 409 `colab_account_leased`
    unless `holder` names that lease's holder, so two agents never run on one account.
    """
    response.headers["Cache-Control"] = "no-store"
    _require_colab(token)
    await enforce_named_rate_limit(
        "video_tool_colab_credentials",
        str(token.id),
        limit=CREDENTIAL_FETCHES_PER_HOUR,
        window_seconds=3_600,
    )
    credentials = await service.agent_client().colab_credentials(slot)
    lease = await colab_leases.current(credentials.slot)
    if lease is not None and lease.holder != holder:
        raise colab_leases.leased_by_other(credentials.slot, lease, holder)
    metadata: dict[str, str] = {"token": token.token_prefix, "requested_slot": slot}
    if holder:
        metadata["holder"] = holder
    session.add(
        AdminAuditLog(
            actor_user_id=token.created_by_user_id,
            action="ai_account.colab_credentials_fetched",
            target=f"ai-account:colab-{credentials.slot}",
            metadata_json=metadata,
        )
    )
    await session.commit()
    return credentials


def _require_colab(token: VideoToolToken) -> None:
    if not token.colab_access:
        raise AppError(
            403,
            "video_tool_token_no_colab",
            "這組影片工具權杖沒有 Colab 帳號權限；重新配對時要求 Colab，或在後台建立時勾選",
        )


# Several agents, one Colab account each: they read the accounts with their balances and who
# holds them, lease one (or let `auto` pick the free one with the most compute units left),
# renew it while they work and give it back. Same token rules as the credentials route.
colab_accounts_router = APIRouter(prefix="/video/colab-accounts", tags=["video tool"])
ACCOUNT_READS_PER_HOUR = 240
LEASE_CHANGES_PER_HOUR = 120
LeaseSlot = Slot | Literal["auto"]


async def _colab_accounts() -> ColabAccounts:
    overview = await service.agent_client().overview()
    leases = await colab_leases.all_leases()
    return colab_leases.accounts_view(overview.slots, overview.defaults, leases)


async def _audit_lease(
    session: AsyncSession, token: VideoToolToken, action: str, slot: Slot, metadata: dict[str, Any]
) -> None:
    session.add(
        AdminAuditLog(
            actor_user_id=token.created_by_user_id,
            action=action,
            target=f"ai-account:colab-{slot}",
            metadata_json={"token": token.token_prefix, **metadata},
        )
    )
    await session.commit()


@colab_accounts_router.get("", response_model=ColabAccounts)
async def get_colab_accounts(
    response: Response, token: Annotated[VideoToolToken, Depends(video_tool)]
) -> ColabAccounts:
    """Every Colab account: signed in or not, compute units, and who leases it. No secrets."""
    response.headers["Cache-Control"] = "no-store"
    _require_colab(token)
    await enforce_named_rate_limit(
        "video_tool_colab_accounts",
        str(token.id),
        limit=ACCOUNT_READS_PER_HOUR,
        window_seconds=3_600,
    )
    return await _colab_accounts()


@colab_accounts_router.post("/{slot}/lease", response_model=ColabLease)
async def post_colab_lease(
    slot: LeaseSlot,
    payload: ColabLeaseRequest,
    session: Session,
    response: Response,
    token: Annotated[VideoToolToken, Depends(video_tool)],
) -> ColabLease:
    """Lease one account to `holder`, or renew the lease it holds.

    `auto` takes the free signed-in account with the most compute units (the one this holder
    already leases, if any). 409 `colab_account_leased` names who holds a taken account,
    `colab_not_signed_in` an empty slot, `colab_no_free_account` an `auto` that found none.
    """
    response.headers["Cache-Control"] = "no-store"
    _require_colab(token)
    await enforce_named_rate_limit(
        "video_tool_colab_leases",
        str(token.id),
        limit=LEASE_CHANGES_PER_HOUR,
        window_seconds=3_600,
    )
    accounts = await _colab_accounts()
    ttl = payload.ttl_minutes * 60
    if slot == "auto":
        order = colab_leases.pick_order(accounts, payload.holder, payload.min_balance)
    else:
        view = next((item for item in accounts.accounts if item.slot == slot), None)
        if view is None or not view.signed_in:
            raise AppError(
                409,
                "colab_not_signed_in",
                f"Colab 帳號 {slot.upper()} 還沒在後台登入；先在 /admin/ai-accounts 登入",
            )
        order = [slot]
    for candidate in order:
        try:
            lease, new = await colab_leases.acquire(
                candidate, payload.holder, token.token_prefix, ttl
            )
        except AppError as exc:
            # Another agent took it between the read and now: `auto` tries the next one.
            if slot == "auto" and exc.code == "colab_account_leased":
                continue
            raise
        await _audit_lease(
            session,
            token,
            "ai_account.colab_leased" if new else "ai_account.colab_lease_renewed",
            candidate,
            {"holder": payload.holder, "requested_slot": slot, "expires_at": lease.expires_at},
        )
        return lease
    busy = ", ".join(
        f"{item.slot.upper()}={item.lease.holder}" for item in accounts.accounts if item.lease
    )
    raise AppError(
        409,
        "colab_no_free_account",
        "沒有空著、已登入"
        + ("、餘額夠" if payload.min_balance is not None else "")
        + f"的 Colab 帳號（使用中：{busy or '無'}）；等別人 release，或在後台登入更多帳號",
    )


@colab_accounts_router.post("/{slot}/lease/release", response_model=ColabReleaseResult)
async def post_colab_release(
    slot: Slot,
    payload: ColabReleaseRequest,
    session: Session,
    response: Response,
    token: Annotated[VideoToolToken, Depends(video_tool)],
) -> ColabReleaseResult:
    """Give the account back. Only its holder can; a lease already gone says `released: false`."""
    response.headers["Cache-Control"] = "no-store"
    _require_colab(token)
    await enforce_named_rate_limit(
        "video_tool_colab_leases",
        str(token.id),
        limit=LEASE_CHANGES_PER_HOUR,
        window_seconds=3_600,
    )
    released = await colab_leases.release(slot, payload.holder)
    if released:
        await _audit_lease(
            session, token, "ai_account.colab_lease_released", slot, {"holder": payload.holder}
        )
    return ColabReleaseResult(slot=slot, released=released)
