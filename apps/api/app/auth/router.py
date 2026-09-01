from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import effective_registration_enabled
from app.auth.schemas import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    RegistrationStatus,
    TokenResponse,
    UserPreferencesUpdate,
    UserResponse,
)
from app.auth.service import (
    DUMMY_PASSWORD_HASH,
    CurrentUser,
    can_deploy_user,
    create_access_token,
    find_user_by_email,
    hash_password,
    is_admin_user,
    verify_password,
)
from app.config import get_settings
from app.db import get_session
from app.i18n import normalize_locale
from app.infra import (
    clear_named_rate_limit,
    client_ip,
    enforce_named_rate_limit,
)
from app.models import User
from app.problems import AppError
from app.usage.service import create_usage_account

router = APIRouter(prefix="/auth", tags=["auth"])
Session = Annotated[AsyncSession, Depends(get_session)]


async def user_response(session: AsyncSession, user: User) -> UserResponse:
    _ = session
    return UserResponse(
        id=user.id,
        email=user.email,
        is_admin=is_admin_user(user),
        can_deploy=can_deploy_user(user),
        preferred_locale=normalize_locale(user.preferred_locale),
    )


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


def token_response(token: str, response_user: UserResponse) -> TokenResponse:
    return TokenResponse(
        access_token=token,
        expires_in=get_settings().access_token_expire_minutes * 60,
        user=response_user,
    )


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    payload: RegisterRequest,
    request: Request,
    response: Response,
    session: Session,
) -> TokenResponse:
    settings = get_settings()
    await enforce_named_rate_limit(
        "auth-register-ip",
        client_ip(request),
        limit=settings.auth_register_ip_limit,
        window_seconds=settings.auth_register_window_seconds,
    )
    if not await effective_registration_enabled(session):
        raise AppError(403, "registration_closed", "目前暫停開放新帳號註冊")
    if await find_user_by_email(session, str(payload.email)):
        raise AppError(409, "email_exists", "這個 Email 已經註冊")
    user = User(
        email=str(payload.email).lower(),
        password_hash=hash_password(payload.password),
        preferred_locale=payload.preferred_locale,
    )
    session.add(user)
    await session.flush()
    await create_usage_account(session, user)
    await session.commit()
    token = create_access_token(user.id, user.auth_version)
    set_auth_cookie(response, token)
    return token_response(token, await user_response(session, user))


@router.get("/registration-status", response_model=RegistrationStatus)
async def registration_status(response: Response, session: Session) -> RegistrationStatus:
    response.headers["Cache-Control"] = "no-store"
    return RegistrationStatus(
        registration_enabled=await effective_registration_enabled(session)
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    session: Session,
) -> TokenResponse:
    settings = get_settings()
    email = str(payload.email).lower()
    source = client_ip(request)
    await enforce_named_rate_limit(
        "auth-login-account",
        email,
        limit=settings.auth_login_account_limit,
        window_seconds=settings.auth_login_window_seconds,
    )
    await enforce_named_rate_limit(
        "auth-login-ip",
        source,
        limit=settings.auth_login_ip_limit,
        window_seconds=settings.auth_login_window_seconds,
    )
    user = await find_user_by_email(session, email)
    password_valid = verify_password(
        payload.password,
        user.password_hash if user is not None else DUMMY_PASSWORD_HASH,
    )
    if user is None or not password_valid:
        raise AppError(401, "invalid_credentials", "Email 或密碼不正確")
    await clear_named_rate_limit("auth-login-account", email)
    token = create_access_token(user.id, user.auth_version)
    set_auth_cookie(response, token)
    return token_response(token, await user_response(session, user))


@router.post("/logout", status_code=204)
async def logout(response: Response) -> None:
    response.delete_cookie("travel_access", path="/")


@router.get("/me", response_model=UserResponse)
async def me(user: CurrentUser, session: Session) -> UserResponse:
    return await user_response(session, user)


@router.patch("/me", response_model=UserResponse)
async def update_me(
    payload: UserPreferencesUpdate,
    user: CurrentUser,
    session: Session,
) -> UserResponse:
    user.preferred_locale = payload.preferred_locale
    await session.commit()
    return await user_response(session, user)


@router.post("/change-password", response_model=TokenResponse)
async def change_password(
    payload: ChangePasswordRequest,
    response: Response,
    user: CurrentUser,
    session: Session,
) -> TokenResponse:
    await enforce_named_rate_limit(
        "auth-password-change-user",
        str(user.id),
        limit=5,
        window_seconds=3_600,
    )
    if not verify_password(payload.current_password, user.password_hash):
        raise AppError(401, "invalid_credentials", "目前密碼不正確")
    user.password_hash = hash_password(payload.new_password)
    user.auth_version = (user.auth_version or 1) + 1
    await session.commit()
    token = create_access_token(user.id, user.auth_version)
    set_auth_cookie(response, token)
    return token_response(token, await user_response(session, user))
