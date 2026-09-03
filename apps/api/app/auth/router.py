from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Cookie, Depends, Header, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import effective_registration_enabled, load_runtime_settings
from app.auth.jobs import enqueue_provider_revocation
from app.auth.oauth import (
    active_identities,
    attempt_provider_revocation,
    exchange_oauth,
    provider_status,
    revoke_identity,
    start_oauth,
)
from app.auth.schemas import (
    AuthIdentityResponse,
    ChangePasswordRequest,
    LoginRequest,
    OAuthExchangeRequest,
    OAuthExchangeResponse,
    OAuthProvider,
    OAuthProvidersResponse,
    OAuthStartRequest,
    OAuthStartResponse,
    RegisterRequest,
    RegistrationStatus,
    TokenResponse,
    UserPreferencesUpdate,
    UserResponse,
)
from app.auth.service import (
    DUMMY_PASSWORD_HASH,
    CurrentUser,
    OptionalCurrentUser,
    can_deploy_user,
    create_access_token,
    decode_access_token_claims,
    find_user_by_email,
    hash_password,
    is_admin_user,
    is_reserved_admin_email,
    revoke_access_token,
    set_auth_cookie,
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
    identities = await active_identities(session, user.id)
    methods = (["password"] if user.password_hash else []) + [item.provider for item in identities]
    return UserResponse(
        id=user.id,
        email=user.email,
        is_admin=is_admin_user(user),
        can_deploy=can_deploy_user(user),
        preferred_locale=normalize_locale(user.preferred_locale),
        has_password=bool(user.password_hash),
        auth_methods=methods,
        identity_count=len(identities),
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
    if is_reserved_admin_email(str(payload.email)):
        raise AppError(
            403,
            "admin_email_reserved",
            "這個 Email 已保留給系統管理員，請由主機管理員以 CLI 建立帳號",
        )
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
        user.password_hash if user is not None and user.password_hash else DUMMY_PASSWORD_HASH,
    )
    if user is None or not password_valid:
        raise AppError(401, "invalid_credentials", "Email 或密碼不正確")
    await clear_named_rate_limit("auth-login-account", email)
    token = create_access_token(user.id, user.auth_version)
    set_auth_cookie(response, token)
    return token_response(token, await user_response(session, user))


@router.post("/logout", status_code=204)
async def logout(
    response: Response,
    authorization: Annotated[str | None, Header()] = None,
    travel_access: Annotated[str | None, Cookie()] = None,
) -> None:
    token = travel_access
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:]
    if token:
        try:
            claims = decode_access_token_claims(token)
        except AppError:
            claims = None
        if claims is not None:
            await revoke_access_token(claims)
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
    if not user.password_hash:
        raise AppError(409, "password_not_set", "這個帳號尚未設定密碼")
    if not verify_password(payload.current_password, user.password_hash):
        raise AppError(401, "invalid_credentials", "目前密碼不正確")
    user.password_hash = hash_password(payload.new_password)
    user.auth_version = (user.auth_version or 1) + 1
    await session.commit()
    token = create_access_token(user.id, user.auth_version)
    set_auth_cookie(response, token)
    return token_response(token, await user_response(session, user))


@router.get("/oauth/providers", response_model=OAuthProvidersResponse)
async def oauth_providers(session: Session) -> OAuthProvidersResponse:
    return OAuthProvidersResponse(providers=provider_status(await load_runtime_settings(session)))


@router.post("/oauth/{provider}/start", response_model=OAuthStartResponse)
async def oauth_start(
    provider: OAuthProvider,
    payload: OAuthStartRequest,
    request: Request,
    user: OptionalCurrentUser,
    session: Session,
) -> OAuthStartResponse:
    settings = await load_runtime_settings(session)
    await enforce_named_rate_limit(
        "auth-oauth-start-ip",
        client_ip(request),
        limit=settings.auth_oauth_ip_limit,
        window_seconds=3_600,
    )
    return await start_oauth(session, payload, provider, user)


@router.post("/oauth/{provider}/exchange", response_model=OAuthExchangeResponse)
async def oauth_exchange(
    provider: OAuthProvider,
    payload: OAuthExchangeRequest,
    user: OptionalCurrentUser,
    session: Session,
) -> OAuthExchangeResponse:
    result = await exchange_oauth(
        session,
        provider,
        flow_id=payload.flow_id,
        state=payload.state,
        code=payload.code,
        browser_binding=payload.browser_binding,
        current_user=user,
    )
    token = create_access_token(result.user.id, result.user.auth_version)
    response = token_response(token, await user_response(session, result.user))
    return OAuthExchangeResponse(**response.model_dump(), new_account=result.created)


@router.get("/identities", response_model=list[AuthIdentityResponse])
async def list_identities(user: CurrentUser, session: Session) -> list[AuthIdentityResponse]:
    return [
        AuthIdentityResponse(
            id=item.id,
            provider=item.provider,
            email=item.provider_email,
            linked_at=item.created_at,
            last_login_at=item.last_login_at,
        )
        for item in await active_identities(session, user.id)
    ]


@router.delete("/identities/{identity_id}", response_model=TokenResponse)
async def unlink_identity(
    identity_id: UUID,
    user: CurrentUser,
    session: Session,
) -> TokenResponse:
    identity = await revoke_identity(session, user, identity_id)
    if not await attempt_provider_revocation(session, identity):
        enqueue_provider_revocation(identity.id)
    token = create_access_token(user.id, user.auth_version)
    return token_response(token, await user_response(session, user))
