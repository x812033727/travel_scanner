from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Annotated, cast
from uuid import UUID, uuid4

import jwt
from fastapi import Cookie, Depends, Header, Response
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from redis.exceptions import RedisError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db import get_session
from app.infra import get_redis
from app.models import User
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


def create_access_token(
    user_id: UUID,
    auth_version: int = 1,
    *,
    session_started_at: datetime | None = None,
    token_id: str | None = None,
) -> str:
    settings = get_settings()
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


def session_past_absolute_cap(claims: AccessTokenClaims, now: datetime | None = None) -> bool:
    """Whether this sign-in is older than the absolute cap, regardless of renewals.

    Checked when a token is presented, not only when one is renewed: a token minted just
    before the cap was reached would otherwise stay valid for its full lifetime past it.
    """
    moment = now or datetime.now(UTC)
    limit = timedelta(days=get_settings().session_absolute_max_days)
    return moment - claims.session_started_at >= limit


def should_renew_session(claims: AccessTokenClaims, now: datetime | None = None) -> bool:
    settings = get_settings()
    moment = now or datetime.now(UTC)
    lifetime = timedelta(minutes=settings.access_token_expire_minutes)
    if moment - claims.issued_at < lifetime * SESSION_RENEWAL_FRACTION:
        return False
    return moment - claims.session_started_at < timedelta(days=settings.session_absolute_max_days)


def set_auth_cookie(response: Response, token: str) -> None:
    settings = get_settings()
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
    """Deny-list one token id until the moment it would have expired anyway."""
    remaining = int((claims.expires_at - datetime.now(UTC)).total_seconds()) + 1
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


async def _authenticate(session: AsyncSession, token: str) -> tuple[User, AccessTokenClaims]:
    claims = decode_access_token_claims(token)
    user = await session.get(User, claims.user_id)
    if user is None or not user.is_active or user.auth_version != claims.auth_version:
        raise AppError(401, "invalid_user", "這個帳號目前無法使用")
    if session_past_absolute_cap(claims):
        raise AppError(401, "session_expired", "登入已逾期,請重新登入")
    await ensure_token_not_revoked(claims)
    return user, claims


def _renew_cookie_session(
    response: Response, user: User, claims: AccessTokenClaims, *, from_cookie: bool
) -> None:
    """Slide a cookie session forward; bearer clients manage their own tokens."""
    if not from_cookie or not should_renew_session(claims):
        return
    set_auth_cookie(
        response,
        create_access_token(
            user.id,
            user.auth_version,
            session_started_at=claims.session_started_at,
            # Carry the id forward so the sign-in keeps one revocation handle.
            token_id=claims.token_id,
        ),
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
    user, claims = await _authenticate(session, token)
    _renew_cookie_session(response, user, claims, from_cookie=not authorization)
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
    user, claims = await _authenticate(session, token)
    _renew_cookie_session(response, user, claims, from_cookie=not authorization)
    return user


OptionalCurrentUser = Annotated[User | None, Depends(optional_current_user)]


def is_admin_user(user: User) -> bool:
    return user.is_admin or user.email.lower() in get_settings().admin_email_set


def is_reserved_admin_email(email: str) -> bool:
    """True when public self-registration must not be allowed to claim this address."""
    settings = get_settings()
    normalized = email.strip().lower()
    return normalized in settings.admin_email_set or normalized in settings.deploy_admin_email_set


async def require_admin(user: CurrentUser) -> User:
    if not is_admin_user(user):
        raise AppError(403, "admin_required", "此功能僅限系統管理員使用")
    return user


AdminUser = Annotated[User, Depends(require_admin)]


def can_deploy_user(user: User) -> bool:
    settings = get_settings()
    return bool(
        settings.deployments_configured
        and is_admin_user(user)
        and user.email.lower() in settings.deploy_admin_email_set
    )


async def require_deploy_admin(user: CurrentUser) -> User:
    if not can_deploy_user(user):
        raise AppError(403, "deployment_admin_required", "此功能僅限部署管理員使用")
    return user


DeployAdminUser = Annotated[User, Depends(require_deploy_admin)]


async def find_user_by_email(session: AsyncSession, email: str) -> User | None:
    return cast(User | None, await session.scalar(select(User).where(User.email == email.lower())))
