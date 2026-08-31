from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.auth.service import (
    CurrentUser,
    create_access_token,
    find_user_by_email,
    hash_password,
    is_admin_user,
    verify_password,
)
from app.config import get_settings
from app.db import get_session
from app.models import User
from app.problems import AppError
from app.usage.service import create_usage_account

router = APIRouter(prefix="/auth", tags=["auth"])
Session = Annotated[AsyncSession, Depends(get_session)]


async def user_response(session: AsyncSession, user: User) -> UserResponse:
    _ = session
    return UserResponse(id=user.id, email=user.email, is_admin=is_admin_user(user))


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


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(payload: RegisterRequest, response: Response, session: Session) -> TokenResponse:
    if await find_user_by_email(session, str(payload.email)):
        raise AppError(409, "email_exists", "這個 Email 已經註冊")
    user = User(email=str(payload.email).lower(), password_hash=hash_password(payload.password))
    session.add(user)
    await session.flush()
    await create_usage_account(session, user)
    await session.commit()
    token = create_access_token(user.id)
    set_auth_cookie(response, token)
    return TokenResponse(access_token=token, user=await user_response(session, user))


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, response: Response, session: Session) -> TokenResponse:
    user = await find_user_by_email(session, str(payload.email))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise AppError(401, "invalid_credentials", "Email 或密碼不正確")
    token = create_access_token(user.id)
    set_auth_cookie(response, token)
    return TokenResponse(access_token=token, user=await user_response(session, user))


@router.post("/logout", status_code=204)
async def logout(response: Response) -> None:
    response.delete_cookie("travel_access", path="/")


@router.get("/me", response_model=UserResponse)
async def me(user: CurrentUser, session: Session) -> UserResponse:
    return await user_response(session, user)


@router.post("/change-password", status_code=204)
async def change_password(
    payload: ChangePasswordRequest, user: CurrentUser, session: Session
) -> None:
    if not verify_password(payload.current_password, user.password_hash):
        raise AppError(401, "invalid_credentials", "目前密碼不正確")
    user.password_hash = hash_password(payload.new_password)
    await session.commit()
