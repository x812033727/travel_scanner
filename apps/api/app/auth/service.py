from collections.abc import Awaitable, Callable, Collection
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Annotated, cast
from uuid import UUID, uuid4

import jwt
from fastapi import Cookie, Depends, Header, Request, Response
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from redis.exceptions import RedisError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.db import get_session
from app.infra import get_redis
from app.models import AdminRoleAssignment, User
from app.problems import AppError

password_hash = PasswordHash.recommended()
ALGORITHM = "HS256"
ISSUER = "travel-scanner-api"
AUDIENCE = "travel-scanner"
DUMMY_PASSWORD_HASH = password_hash.hash("not-a-real-travel-scanner-password")
REVOKED_TOKEN_PREFIX = "auth:revoked:"
# Renew a cookie session once the presented token has used up this share of
# its lifetime, so an active user never sees the hourly logout.
SESSION_RENEWAL_FRACTION = 0.5
STEP_UP_ISSUER = "travel-scanner-admin"
STEP_UP_AUDIENCE = "travel-scanner-admin-step-up"
STEP_UP_COOKIE = "admin_step_up"
STEP_UP_TTL_SECONDS = 300

ADMIN_ROLE_CAPABILITIES: dict[str, frozenset[str]] = {
    "viewer": frozenset(
        {
            "admin.access",
            "dashboard.read",
            "content.read",
            "community.read",
            "users.read",
            "analytics.read",
            "settings.read",
            "audit.read",
        }
    ),
    "support": frozenset(
        {
            "admin.access",
            "dashboard.read",
            "community.read",
            "community.manage",
            "users.read",
            "users.manage",
            "usage.manage",
            "audit.read",
        }
    ),
    "content": frozenset(
        {
            "admin.access",
            "dashboard.read",
            "content.read",
            "content.manage",
            "community.read",
            "audit.read",
        }
    ),
    "operations": frozenset(
        {
            "admin.access",
            "dashboard.read",
            "analytics.read",
            "settings.read",
            "settings.manage",
            "audit.read",
        }
    ),
    "database_operator": frozenset(
        {"admin.access", "dashboard.read", "database.read", "database.maintain", "audit.read"}
    ),
    "deployer": frozenset(
        {"admin.access", "dashboard.read", "deploy.read", "deploy.execute", "audit.read"}
    ),
}
ALL_ADMIN_CAPABILITIES = frozenset().union(*ADMIN_ROLE_CAPABILITIES.values()) | frozenset(
    {"roles.manage"}
)
ADMIN_ROLE_CAPABILITIES["owner"] = ALL_ADMIN_CAPABILITIES

STEP_UP_SCOPE_CAPABILITY = {
    "users.roles": "roles.manage",
    "users.suspend_permanent": "users.manage",
    "users.erase": "users.manage",
    "database.backup": "database.maintain",
    "database.analyze": "database.maintain",
}


@dataclass(frozen=True)
class AccessTokenClaims:
    user_id: UUID
    auth_version: int
    token_id: str
    expires_at: datetime
    issued_at: datetime
    session_started_at: datetime


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


async def runtime_auth_settings(session: AsyncSession) -> Settings:
    """Settings with the administrator's overrides applied.

    The auth paths mint and judge tokens with these, so a lifetime changed on
    /admin/settings takes effect on the next sign-in or renewal without a redeploy.
    Imported lazily because ``app.admin.service`` imports this module.
    """
    from app.admin.service import load_runtime_settings

    return await load_runtime_settings(session)


def create_access_token(
    user_id: UUID,
    auth_version: int = 1,
    *,
    session_started_at: datetime | None = None,
    token_id: str | None = None,
    settings: Settings | None = None,
) -> str:
    settings = settings or get_settings()
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "ver": auth_version,
        "iss": ISSUER,
        "aud": AUDIENCE,
        # A renewal passes the presented token's id back in, so jti identifies the whole
        # sign-in rather than one token in it. Minting a fresh id on every renewal let a
        # copied cookie renew into a chain of its own that signing out could not reach:
        # logout denylists only the id it was handed, and does not raise auth_version.
        "jti": token_id or str(uuid4()),
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
        # Original sign-in time survives renewals so the absolute cap holds.
        "sid_iat": int((session_started_at or now).timestamp()),
    }
    return jwt.encode(payload, settings.app_secret_key, algorithm=ALGORITHM)


def session_past_absolute_cap(
    claims: AccessTokenClaims, now: datetime | None = None, *, settings: Settings | None = None
) -> bool:
    """Whether this sign-in is older than the absolute cap, regardless of renewals.

    Checked when a token is presented, not only when one is renewed: a token minted just
    before the cap was reached would otherwise stay valid for its full lifetime past it.
    """
    moment = now or datetime.now(UTC)
    limit = timedelta(days=(settings or get_settings()).session_absolute_max_days)
    return moment - claims.session_started_at >= limit


def should_renew_session(
    claims: AccessTokenClaims, now: datetime | None = None, *, settings: Settings | None = None
) -> bool:
    moment = now or datetime.now(UTC)
    # Measured against the lifetime this token was actually minted with, not the one
    # currently configured. Reading the config here meant raising the lifetime moved the
    # renewal point beyond the expiry of every token already issued, so a change that was
    # supposed to keep people signed in for longer signed all of them out instead.
    lifetime = claims.expires_at - claims.issued_at
    if moment - claims.issued_at < lifetime * SESSION_RENEWAL_FRACTION:
        return False
    limit = timedelta(days=(settings or get_settings()).session_absolute_max_days)
    return moment - claims.session_started_at < limit


def set_auth_cookie(response: Response, token: str, *, settings: Settings | None = None) -> None:
    settings = settings or get_settings()
    response.set_cookie(
        "travel_access",
        token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
        path="/",
    )


def decode_access_token_claims(token: str) -> AccessTokenClaims:
    try:
        payload = jwt.decode(
            token,
            get_settings().app_secret_key,
            algorithms=[ALGORITHM],
            audience=AUDIENCE,
            issuer=ISSUER,
            options={"require": ["sub", "ver", "iss", "aud", "jti", "iat", "nbf", "exp"]},
        )
        auth_version = int(payload["ver"])
        if auth_version < 1:
            raise ValueError("invalid auth version")
        token_id = str(payload["jti"])
        if not token_id:
            raise ValueError("invalid token id")
        expires_at = datetime.fromtimestamp(int(payload["exp"]), tz=UTC)
        issued_at = datetime.fromtimestamp(int(payload["iat"]), tz=UTC)
        # Tokens minted before sliding renewal carry no sid_iat; treat their
        # issue time as the session start.
        session_started_at = datetime.fromtimestamp(
            int(payload.get("sid_iat", payload["iat"])), tz=UTC
        )
        return AccessTokenClaims(
            UUID(payload["sub"]), auth_version, token_id, expires_at, issued_at, session_started_at
        )
    except (InvalidTokenError, KeyError, TypeError, ValueError, OverflowError, OSError) as exc:
        raise AppError(401, "invalid_token", "登入憑證無效或已過期") from exc


def decode_access_token(token: str) -> UUID:
    return decode_access_token_claims(token).user_id


def _revocation_key(token_id: str) -> str:
    return f"{REVOKED_TOKEN_PREFIX}{token_id}"


async def revoke_access_token(claims: AccessTokenClaims) -> None:
    """Deny-list the sign-in's token id until no token of that sign-in can still be valid.

    Renewal keeps one ``jti`` for the whole sign-in but keeps minting later expiries, so
    the entry has to outlive the latest possible sibling, not just the copy presented at
    logout. Every token of the sign-in is refused once past the absolute cap, so that
    moment bounds them all; keying the TTL to the presented ``exp`` alone let a sibling
    renewed after it outlive the deny entry and slide itself forward for the rest of the
    cap, unreachable by any later logout because those mint a fresh ``jti``.
    """
    now = datetime.now(UTC)
    cap = claims.session_started_at + timedelta(days=get_settings().session_absolute_max_days)
    remaining = int((max(claims.expires_at, cap) - now).total_seconds()) + 1
    if remaining <= 0:
        return
    try:
        await get_redis().set(_revocation_key(claims.token_id), "1", ex=remaining)
    except RedisError as exc:
        raise AppError(503, "session_check_unavailable", "登入狀態服務暫時無法使用") from exc


async def ensure_token_not_revoked(claims: AccessTokenClaims) -> None:
    try:
        revoked = await get_redis().exists(_revocation_key(claims.token_id))
    except RedisError as exc:
        raise AppError(503, "session_check_unavailable", "登入狀態服務暫時無法使用") from exc
    if revoked:
        raise AppError(401, "invalid_token", "登入憑證已登出，請重新登入")


def _presented_token(authorization: str | None, travel_access: str | None) -> str | None:
    if authorization and authorization.lower().startswith("bearer "):
        return authorization[7:]
    return travel_access


async def _authenticate(
    session: AsyncSession, token: str
) -> tuple[User, AccessTokenClaims, Settings]:
    claims = decode_access_token_claims(token)
    user = await session.get(User, claims.user_id)
    if user is None or not user.is_active or user.auth_version != claims.auth_version:
        raise AppError(401, "invalid_user", "這個帳號目前無法使用")
    if user_is_suspended(user):
        raise AppError(403, "account_suspended", "這個帳號目前已被停權")
    user.__dict__["_admin_roles_cache"] = frozenset(await effective_admin_roles(session, user))
    settings = await runtime_auth_settings(session)
    if session_past_absolute_cap(claims, settings=settings):
        raise AppError(401, "session_expired", "登入已逾期,請重新登入")
    await ensure_token_not_revoked(claims)
    return user, claims, settings


def _renew_cookie_session(
    response: Response,
    user: User,
    claims: AccessTokenClaims,
    *,
    from_cookie: bool,
    settings: Settings,
) -> None:
    """Slide a cookie session forward; bearer clients manage their own tokens."""
    if not from_cookie or not should_renew_session(claims, settings=settings):
        return
    set_auth_cookie(
        response,
        create_access_token(
            user.id,
            user.auth_version,
            session_started_at=claims.session_started_at,
            # Carry the id forward so the sign-in keeps one revocation handle.
            token_id=claims.token_id,
            settings=settings,
        ),
        settings=settings,
    )


async def current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    response: Response,
    authorization: Annotated[str | None, Header()] = None,
    travel_access: Annotated[str | None, Cookie()] = None,
) -> User:
    token = _presented_token(authorization, travel_access)
    if not token:
        raise AppError(401, "authentication_required", "請先登入再繼續")
    user, claims, settings = await _authenticate(session, token)
    _renew_cookie_session(response, user, claims, from_cookie=not authorization, settings=settings)
    return user


CurrentUser = Annotated[User, Depends(current_user)]


async def optional_current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    response: Response,
    authorization: Annotated[str | None, Header()] = None,
    travel_access: Annotated[str | None, Cookie()] = None,
) -> User | None:
    token = _presented_token(authorization, travel_access)
    if not token:
        return None
    user, claims, settings = await _authenticate(session, token)
    _renew_cookie_session(response, user, claims, from_cookie=not authorization, settings=settings)
    return user


OptionalCurrentUser = Annotated[User | None, Depends(optional_current_user)]


def is_admin_user(user: User) -> bool:
    cached = getattr(user, "_admin_roles_cache", None)
    if cached is not None:
        return bool(cached or user.email.lower() in get_settings().admin_email_set)
    return bool(user.is_admin or user.email.lower() in get_settings().admin_email_set)


def is_reserved_admin_email(email: str) -> bool:
    """True when public self-registration must not be allowed to claim this address."""
    settings = get_settings()
    normalized = email.strip().lower()
    return normalized in (
        settings.admin_email_set
        | settings.deploy_admin_email_set
        | settings.database_admin_email_set
    )


async def effective_admin_roles(session: AsyncSession, user: User) -> set[str]:
    """Return active persisted roles plus immutable environment/legacy compatibility."""
    roles: set[str] = set()
    email = user.email.lower()
    if email in get_settings().admin_email_set:
        roles.add("owner")
    now = datetime.now(UTC)
    if not hasattr(session, "scalars"):
        if user.is_admin:
            roles.update(("support", "content", "operations"))
        return roles
    assignments = [
        assignment
        for assignment in (
            await session.scalars(
                select(AdminRoleAssignment).where(AdminRoleAssignment.user_id == user.id)
            )
        ).all()
        if isinstance(assignment, AdminRoleAssignment)
    ]
    roles.update(
        assignment.role
        for assignment in assignments
        if assignment.expires_at is None
        or (
            assignment.expires_at.replace(tzinfo=UTC)
            if assignment.expires_at.tzinfo is None
            else assignment.expires_at
        )
        > now
    )
    # Before 0067 a database administrator only had users.is_admin. The migration
    # backfills role rows; this fallback keeps tests, fixtures, and a partially rolled
    # deployment usable until that write has happened once.
    if user.is_admin and not assignments:
        roles.update(("support", "content", "operations"))
    return roles


def capabilities_for_roles(roles: Collection[str]) -> set[str]:
    capabilities: set[str] = set()
    for role in roles:
        capabilities.update(ADMIN_ROLE_CAPABILITIES.get(role, frozenset()))
    return capabilities


async def effective_admin_capabilities(session: AsyncSession, user: User) -> set[str]:
    roles = await effective_admin_roles(session, user)
    user.__dict__["_admin_roles_cache"] = frozenset(roles)
    return capabilities_for_roles(roles)


def cached_admin_roles(user: User) -> set[str]:
    cached = getattr(user, "_admin_roles_cache", None)
    roles = set(cached or ())
    if user.email.lower() in get_settings().admin_email_set:
        roles.add("owner")
    if user.is_admin and cached is None:
        roles.update(("support", "content", "operations"))
    return roles


def cached_admin_capabilities(user: User) -> set[str]:
    return capabilities_for_roles(cached_admin_roles(user))


def _admin_path_capability(request: Request) -> str:
    path = request.url.path
    read = request.method in {"GET", "HEAD", "OPTIONS"}
    if "/admin/users" in path:
        if "/usage-adjustments" in path:
            return "usage.manage"
        return "users.read" if read else "users.manage"
    if "/admin/community" in path or "/admin/pet-friendly" in path:
        return "community.read" if read else "community.manage"
    if any(
        value in path
        for value in (
            "/admin/catalog-review",
            "/admin/hotspots",
            "/admin/foods",
            "/admin/hotels",
            "/admin/travel-services",
        )
    ):
        return "content.read" if read else "content.manage"
    if "/admin/analytics" in path or "/admin/discovery" in path:
        return "analytics.read"
    if "/admin/bootstrap" in path:
        return "admin.access"
    if "/admin/dashboard" in path:
        return "dashboard.read"
    if "/admin/step-up" in path:
        return "admin.access"
    if "/admin/audit" in path:
        return "audit.read"
    if "/admin/database" in path:
        return "database.read" if read else "database.maintain"
    if "/admin/deployments" in path:
        return "deploy.read" if read else "deploy.execute"
    if any(
        value in path
        for value in (
            "/admin/provider-settings",
            "/admin/usage-settings",
            "/admin/ui-text",
            "/admin/system-settings",
            "/admin/layout-settings",
            "/admin/partners",
            "/admin/affiliates",
        )
    ):
        return "settings.read" if read else "settings.manage"
    return "roles.manage"


async def require_admin(request: Request, user: CurrentUser) -> User:
    required = _admin_path_capability(request)
    if required not in cached_admin_capabilities(user):
        if not cached_admin_roles(user):
            raise AppError(403, "admin_required", "此功能僅限系統管理員使用")
        raise AppError(403, "admin_capability_required", "目前管理員角色沒有這項操作權限")
    return user


AdminUser = Annotated[User, Depends(require_admin)]


def require_capability(capability: str) -> Callable[..., Awaitable[User]]:
    async def dependency(user: CurrentUser) -> User:
        if capability not in cached_admin_capabilities(user):
            if not cached_admin_roles(user):
                raise AppError(403, "admin_required", "此功能僅限系統管理員使用")
            raise AppError(403, "admin_capability_required", "目前管理員角色沒有這項操作權限")
        return user

    return dependency


def can_deploy_user(user: User, *, roles: Collection[str] | None = None) -> bool:
    settings = get_settings()
    assigned = set(roles) if roles is not None else cached_admin_roles(user)
    return bool(
        settings.deployments_configured
        and user.email.lower() in settings.deploy_admin_email_set
        and ("owner" in assigned or "deployer" in assigned)
    )


def can_database_maintain_user(user: User, *, roles: Collection[str] | None = None) -> bool:
    settings = get_settings()
    assigned = set(roles) if roles is not None else cached_admin_roles(user)
    return bool(
        settings.database_maintenance_configured
        and user.email.lower() in settings.database_admin_email_set
        and ("owner" in assigned or "database_operator" in assigned)
    )


async def require_deploy_admin(user: CurrentUser) -> User:
    if not can_deploy_user(user):
        raise AppError(403, "deployment_admin_required", "此功能僅限部署管理員使用")
    return user


DeployAdminUser = Annotated[User, Depends(require_deploy_admin)]


def user_is_suspended(user: User, now: datetime | None = None) -> bool:
    if user.suspended_at is None:
        return False
    until = user.suspended_until
    if until is None:
        return True
    if until.tzinfo is None:
        until = until.replace(tzinfo=UTC)
    return until > (now or datetime.now(UTC))


def create_admin_step_up_token(
    user: User,
    scopes: Collection[str],
    *,
    settings: Settings | None = None,
) -> tuple[str, datetime]:
    settings = settings or get_settings()
    now = datetime.now(UTC)
    expires_at = now + timedelta(seconds=STEP_UP_TTL_SECONDS)
    token = jwt.encode(
        {
            "sub": str(user.id),
            "ver": user.auth_version,
            "scopes": sorted(set(scopes)),
            "iss": STEP_UP_ISSUER,
            "aud": STEP_UP_AUDIENCE,
            "iat": now,
            "nbf": now,
            "exp": expires_at,
        },
        settings.app_secret_key,
        algorithm=ALGORITHM,
    )
    return token, expires_at


def set_admin_step_up_cookie(
    response: Response, token: str, *, settings: Settings | None = None
) -> None:
    settings = settings or get_settings()
    response.set_cookie(
        STEP_UP_COOKIE,
        token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="strict",
        max_age=STEP_UP_TTL_SECONDS,
        path="/api/v1/admin",
    )


async def require_admin_step_up(
    request: Request,
    user: User,
    scope: str,
) -> None:
    token = request.cookies.get(STEP_UP_COOKIE)
    if not token:
        raise AppError(401, "admin_step_up_required", "請重新輸入密碼後再執行此操作")
    try:
        payload = jwt.decode(
            token,
            get_settings().app_secret_key,
            algorithms=[ALGORITHM],
            audience=STEP_UP_AUDIENCE,
            issuer=STEP_UP_ISSUER,
            options={"require": ["sub", "ver", "scopes", "iss", "aud", "iat", "nbf", "exp"]},
        )
        raw_scopes = payload["scopes"]
        if not isinstance(raw_scopes, list) or any(
            not isinstance(item, str) for item in raw_scopes
        ):
            raise ValueError("invalid step-up scopes")
        scopes = set(cast(list[str], raw_scopes))
        if UUID(str(payload["sub"])) != user.id or int(payload["ver"]) != user.auth_version:
            raise ValueError("step-up principal changed")
        if scope not in scopes:
            raise AppError(403, "admin_step_up_scope_required", "請重新驗證這項操作的權限")
    except AppError:
        raise
    except (InvalidTokenError, KeyError, TypeError, ValueError, OverflowError, OSError) as exc:
        raise AppError(401, "admin_step_up_invalid", "重新驗證已失效，請再輸入一次密碼") from exc


async def find_user_by_email(session: AsyncSession, email: str) -> User | None:
    return cast(User | None, await session.scalar(select(User).where(User.email == email.lower())))
