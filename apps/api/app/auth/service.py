from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Annotated, cast
from uuid import UUID, uuid4

import jwt
from fastapi import Cookie, Depends, Header
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db import get_session
from app.models import User
from app.problems import AppError

password_hash = PasswordHash.recommended()
ALGORITHM = "HS256"
ISSUER = "travel-scanner-api"
AUDIENCE = "travel-scanner"
DUMMY_PASSWORD_HASH = password_hash.hash("not-a-real-travel-scanner-password")


@dataclass(frozen=True)
class AccessTokenClaims:
    user_id: UUID
    auth_version: int


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


def create_access_token(user_id: UUID, auth_version: int = 1) -> str:
    settings = get_settings()
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "ver": auth_version,
        "iss": ISSUER,
        "aud": AUDIENCE,
        "jti": str(uuid4()),
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.app_secret_key, algorithm=ALGORITHM)


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
        return AccessTokenClaims(UUID(payload["sub"]), auth_version)
    except (InvalidTokenError, KeyError, TypeError, ValueError) as exc:
        raise AppError(401, "invalid_token", "登入憑證無效或已過期") from exc


def decode_access_token(token: str) -> UUID:
    return decode_access_token_claims(token).user_id


async def current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    authorization: Annotated[str | None, Header()] = None,
    travel_access: Annotated[str | None, Cookie()] = None,
) -> User:
    token = travel_access
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:]
    if not token:
        raise AppError(401, "authentication_required", "請先登入再繼續")
    claims = decode_access_token_claims(token)
    user = await session.get(User, claims.user_id)
    if user is None or not user.is_active or user.auth_version != claims.auth_version:
        raise AppError(401, "invalid_user", "這個帳號目前無法使用")
    return user


CurrentUser = Annotated[User, Depends(current_user)]


async def optional_current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    authorization: Annotated[str | None, Header()] = None,
    travel_access: Annotated[str | None, Cookie()] = None,
) -> User | None:
    token = travel_access
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:]
    if not token:
        return None
    claims = decode_access_token_claims(token)
    user = await session.get(User, claims.user_id)
    if user is None or not user.is_active or user.auth_version != claims.auth_version:
        raise AppError(401, "invalid_user", "這個帳號目前無法使用")
    return user


OptionalCurrentUser = Annotated[User | None, Depends(optional_current_user)]


def is_admin_user(user: User) -> bool:
    return user.is_admin or user.email.lower() in get_settings().admin_email_set


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
