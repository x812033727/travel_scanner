from __future__ import annotations

import base64
import hashlib
import hmac
import inspect
import json
import secrets
from collections.abc import Awaitable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, cast
from urllib.parse import urlencode

import httpx
import jwt
from cryptography.fernet import Fernet, InvalidToken
from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import effective_registration_enabled, load_runtime_settings
from app.auth.schemas import OAuthProvider, OAuthStartRequest, OAuthStartResponse
from app.auth.service import find_user_by_email
from app.config import Settings
from app.i18n import normalize_locale
from app.infra import get_redis
from app.models import User, UserAuthIdentity
from app.problems import AppError
from app.usage.service import create_usage_account

GOOGLE_AUTHORIZE = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN = "https://oauth2.googleapis.com/token"
GOOGLE_JWKS = "https://www.googleapis.com/oauth2/v3/certs"
LINE_AUTHORIZE = "https://access.line.me/oauth2/v2.1/authorize"
LINE_TOKEN = "https://api.line.me/oauth2/v2.1/token"
LINE_VERIFY = "https://api.line.me/oauth2/v2.1/verify"
APPLE_AUTHORIZE = "https://appleid.apple.com/auth/authorize"
APPLE_TOKEN = "https://appleid.apple.com/auth/token"
APPLE_REVOKE = "https://appleid.apple.com/auth/revoke"
APPLE_JWKS = "https://appleid.apple.com/auth/keys"


@dataclass(frozen=True)
class OAuthProfile:
    subject: str
    email: str | None
    email_verified: bool
    refresh_token: str | None = None


@dataclass(frozen=True)
class OAuthResult:
    user: User
    identity: UserAuthIdentity
    created: bool


def provider_enabled(provider: OAuthProvider, settings: Settings) -> bool:
    values = {
        "google": bool(
            settings.auth_google_enabled
            and settings.auth_google_client_id
            and settings.auth_google_client_secret
        ),
        "line": bool(
            settings.auth_line_enabled
            and settings.auth_line_channel_id
            and settings.auth_line_channel_secret
        ),
        "apple": bool(
            settings.auth_apple_enabled
            and settings.auth_apple_services_id
            and settings.auth_apple_team_id
            and settings.auth_apple_key_id
            and settings.auth_apple_private_key
        ),
    }
    return values[provider]


def provider_status(settings: Settings) -> dict[OAuthProvider, bool]:
    providers: tuple[OAuthProvider, ...] = ("google", "line", "apple")
    return {provider: provider_enabled(provider, settings) for provider in providers}


def callback_url(settings: Settings, provider: OAuthProvider) -> str:
    return f"{settings.next_public_site_url.rstrip('/')}/api/auth/oauth/{provider}/callback"


def _safe_next(value: str) -> str:
    value = value.strip()
    if not value.startswith("/") or value.startswith("//") or "\\" in value:
        return "/"
    return value


def _challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()


async def start_oauth(
    session: AsyncSession,
    payload: OAuthStartRequest,
    provider: OAuthProvider,
    current_user: User | None,
) -> OAuthStartResponse:
    settings = await load_runtime_settings(session)
    if not provider_enabled(provider, settings):
        raise AppError(503, "oauth_provider_unavailable", "這個登入方式尚未設定")
    if payload.intent == "link" and current_user is None:
        raise AppError(401, "authentication_required", "請先登入再連結其他帳號")

    flow_id = secrets.token_urlsafe(32)
    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)
    record = {
        "provider": provider,
        "intent": payload.intent,
        "locale": normalize_locale(payload.locale),
        "next": _safe_next(payload.next_path),
        "binding": hashlib.sha256(payload.browser_binding.encode()).hexdigest(),
        "state": state,
        "nonce": nonce,
        "verifier": verifier,
        "user_id": str(current_user.id) if current_user else None,
        "auth_version": current_user.auth_version if current_user else None,
    }
    try:
        await get_redis().set(
            f"oauth-flow:{flow_id}",
            json.dumps(record),
            ex=settings.auth_oauth_flow_ttl_seconds,
        )
    except RedisError as exc:
        raise AppError(503, "oauth_state_unavailable", "登入驗證服務暫時無法使用") from exc

    common = {
        "response_type": "code",
        "redirect_uri": callback_url(settings, provider),
        "state": state,
        "nonce": nonce,
    }
    if provider == "google":
        params = {
            **common,
            "client_id": cast(str, settings.auth_google_client_id),
            "scope": "openid email",
            "code_challenge": _challenge(verifier),
            "code_challenge_method": "S256",
        }
        authorization_url = f"{GOOGLE_AUTHORIZE}?{urlencode(params)}"
    elif provider == "line":
        params = {
            **common,
            "client_id": cast(str, settings.auth_line_channel_id),
            "scope": "openid email",
            "code_challenge": _challenge(verifier),
            "code_challenge_method": "S256",
        }
        authorization_url = f"{LINE_AUTHORIZE}?{urlencode(params)}"
    else:
        params = {
            **common,
            "client_id": cast(str, settings.auth_apple_services_id),
            "scope": "email",
            "response_mode": "form_post",
        }
        authorization_url = f"{APPLE_AUTHORIZE}?{urlencode(params)}"
    return OAuthStartResponse(
        authorization_url=authorization_url,
        flow_id=flow_id,
        state=state,
        expires_in=settings.auth_oauth_flow_ttl_seconds,
    )


async def _jwks(
    redis: Redis, client: httpx.AsyncClient, provider: str, url: str
) -> dict[str, Any]:
    cache_key = f"oauth-jwks:{provider}"
    cached = await redis.get(cache_key)
    if cached:
        try:
            return cast(dict[str, Any], json.loads(cached))
        except json.JSONDecodeError:
            pass
    response = await client.get(url)
    response.raise_for_status()
    result = cast(dict[str, Any], response.json())
    await redis.set(cache_key, json.dumps(result), ex=21_600)
    return result


async def _verify_jwt(
    redis: Redis,
    client: httpx.AsyncClient,
    token: str,
    *,
    provider: str,
    jwks_url: str,
    audience: str,
    issuers: tuple[str, ...],
    nonce: str,
) -> dict[str, Any]:
    header = jwt.get_unverified_header(token)
    keys = (await _jwks(redis, client, provider, jwks_url)).get("keys", [])
    key_data = next((item for item in keys if item.get("kid") == header.get("kid")), None)
    if not key_data:
        raise AppError(401, "oauth_token_invalid", "登入身份驗證失敗")
    claims: dict[str, Any] = jwt.decode(
        token,
        jwt.PyJWK.from_dict(key_data).key,
        algorithms=["RS256"],
        audience=audience,
        issuer=issuers,
        options={"require": ["sub", "iss", "aud", "iat", "exp"]},
    )
    if not hmac.compare_digest(str(claims.get("nonce", "")), nonce):
        raise AppError(401, "oauth_nonce_invalid", "登入驗證已失效，請重新操作")
    return claims


def apple_client_secret(settings: Settings) -> str:
    now = datetime.now(UTC)
    private_key = cast(str, settings.auth_apple_private_key).replace("\\n", "\n")
    return jwt.encode(
        {
            "iss": settings.auth_apple_team_id,
            "iat": now,
            "exp": now + timedelta(minutes=5),
            "aud": "https://appleid.apple.com",
            "sub": settings.auth_apple_services_id,
        },
        private_key,
        algorithm="ES256",
        headers={"kid": settings.auth_apple_key_id},
    )


def _verified(value: object) -> bool:
    return value is True or str(value).lower() == "true"


async def exchange_profile(
    settings: Settings,
    redis: Redis,
    provider: OAuthProvider,
    code: str,
    nonce: str,
    verifier: str,
) -> OAuthProfile:
    redirect_uri = callback_url(settings, provider)
    async with httpx.AsyncClient(timeout=12.0) as client:
        if provider == "google":
            response = await client.post(
                GOOGLE_TOKEN,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri,
                    "client_id": settings.auth_google_client_id,
                    "client_secret": settings.auth_google_client_secret,
                    "code_verifier": verifier,
                },
            )
            response.raise_for_status()
            claims = await _verify_jwt(
                redis,
                client,
                response.json()["id_token"],
                provider="google",
                jwks_url=GOOGLE_JWKS,
                audience=cast(str, settings.auth_google_client_id),
                issuers=("https://accounts.google.com", "accounts.google.com"),
                nonce=nonce,
            )
            return OAuthProfile(
                subject=str(claims["sub"]),
                email=str(claims["email"]).lower() if claims.get("email") else None,
                email_verified=_verified(claims.get("email_verified")),
            )
        if provider == "line":
            response = await client.post(
                LINE_TOKEN,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri,
                    "client_id": settings.auth_line_channel_id,
                    "client_secret": settings.auth_line_channel_secret,
                    "code_verifier": verifier,
                },
            )
            response.raise_for_status()
            verify = await client.post(
                LINE_VERIFY,
                data={
                    "id_token": response.json()["id_token"],
                    "client_id": settings.auth_line_channel_id,
                    "nonce": nonce,
                },
            )
            verify.raise_for_status()
            claims = verify.json()
            return OAuthProfile(
                subject=str(claims["sub"]),
                email=str(claims["email"]).lower() if claims.get("email") else None,
                email_verified=bool(claims.get("email")),
            )

        response = await client.post(
            APPLE_TOKEN,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": settings.auth_apple_services_id,
                "client_secret": apple_client_secret(settings),
            },
        )
        response.raise_for_status()
        token_data = response.json()
        claims = await _verify_jwt(
            redis,
            client,
            token_data["id_token"],
            provider="apple",
            jwks_url=APPLE_JWKS,
            audience=cast(str, settings.auth_apple_services_id),
            issuers=("https://appleid.apple.com",),
            nonce=nonce,
        )
        return OAuthProfile(
            subject=str(claims["sub"]),
            email=str(claims["email"]).lower() if claims.get("email") else None,
            email_verified=_verified(claims.get("email_verified")),
            refresh_token=token_data.get("refresh_token"),
        )


def _fernet(settings: Settings) -> Fernet:
    raw = settings.settings_encryption_key or settings.app_secret_key
    return Fernet(base64.urlsafe_b64encode(hashlib.sha256(raw.encode()).digest()))


def encrypt_refresh_token(token: str | None, settings: Settings) -> str | None:
    return _fernet(settings).encrypt(token.encode()).decode() if token else None


def decrypt_refresh_token(identity: UserAuthIdentity, settings: Settings) -> str | None:
    if not identity.refresh_token_encrypted:
        return None
    try:
        return _fernet(settings).decrypt(identity.refresh_token_encrypted.encode()).decode()
    except (InvalidToken, UnicodeDecodeError) as exc:
        raise AppError(500, "oauth_secret_unreadable", "登入憑證無法解密") from exc


async def exchange_oauth(
    session: AsyncSession,
    provider: OAuthProvider,
    *,
    flow_id: str,
    state: str,
    code: str,
    browser_binding: str,
    current_user: User | None,
) -> OAuthResult:
    redis = get_redis()
    try:
        raw = await redis.getdel(f"oauth-flow:{flow_id}")
    except RedisError as exc:
        raise AppError(503, "oauth_state_unavailable", "登入驗證服務暫時無法使用") from exc
    if not raw:
        raise AppError(401, "oauth_state_invalid", "登入驗證已失效，請重新操作")
    try:
        flow = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AppError(401, "oauth_state_invalid", "登入驗證已失效，請重新操作") from exc
    binding = hashlib.sha256(browser_binding.encode()).hexdigest()
    if (
        flow.get("provider") != provider
        or not hmac.compare_digest(str(flow.get("state", "")), state)
        or not hmac.compare_digest(str(flow.get("binding", "")), binding)
    ):
        raise AppError(401, "oauth_state_invalid", "登入驗證已失效，請重新操作")
    if flow.get("intent") == "link" and (
        current_user is None
        or str(current_user.id) != flow.get("user_id")
        or current_user.auth_version != flow.get("auth_version")
    ):
        raise AppError(401, "oauth_link_session_invalid", "帳號連結工作階段已失效")

    settings = await load_runtime_settings(session)
    if not provider_enabled(provider, settings):
        raise AppError(503, "oauth_provider_unavailable", "這個登入方式目前無法使用")
    try:
        profile = await exchange_profile(
            settings, redis, provider, code, str(flow["nonce"]), str(flow["verifier"])
        )
    except AppError:
        raise
    except (httpx.HTTPError, jwt.PyJWTError, KeyError, TypeError, ValueError) as exc:
        raise AppError(401, "oauth_token_invalid", "登入身份驗證失敗") from exc

    identity = await session.scalar(
        select(UserAuthIdentity).where(
            UserAuthIdentity.provider == provider,
            UserAuthIdentity.subject == profile.subject,
        )
    )
    created = False
    if flow.get("intent") == "link":
        assert current_user is not None
        if identity and identity.user_id != current_user.id:
            raise AppError(409, "oauth_identity_conflict", "這個登入帳號已連結其他會員")
        if identity is None:
            identity = UserAuthIdentity(
                user_id=current_user.id, provider=provider, subject=profile.subject
            )
            session.add(identity)
        identity.revoked_at = None
        identity.revocation_pending = False
        user = current_user
    elif identity is not None:
        if identity.revoked_at is not None:
            raise AppError(409, "oauth_identity_revoked", "此登入方式已解除，請登入後重新連結")
        loaded_user = await session.get(User, identity.user_id)
        if loaded_user is None or not loaded_user.is_active:
            raise AppError(401, "invalid_user", "這個帳號目前無法使用")
        user = loaded_user
    else:
        if not profile.email or not profile.email_verified:
            raise AppError(422, "oauth_email_required", "首次建立帳號需要已驗證的 Email")
        if await find_user_by_email(session, profile.email):
            raise AppError(
                409,
                "oauth_account_exists",
                "此 Email 已有會員，請先用原方式登入後再連結",
            )
        if not await effective_registration_enabled(session):
            raise AppError(403, "registration_closed", "目前暫停開放新帳號註冊")
        user = User(
            email=profile.email,
            password_hash=None,
            preferred_locale=normalize_locale(flow.get("locale")),
        )
        session.add(user)
        await session.flush()
        await create_usage_account(session, user)
        identity = UserAuthIdentity(
            user_id=user.id, provider=provider, subject=profile.subject
        )
        session.add(identity)
        created = True

    identity.provider_email = profile.email
    identity.email_verified = profile.email_verified
    identity.last_login_at = datetime.now(UTC)
    if provider == "apple" and profile.refresh_token:
        identity.refresh_token_encrypted = encrypt_refresh_token(profile.refresh_token, settings)
    await session.commit()
    return OAuthResult(user=user, identity=identity, created=created)


async def active_identities(session: AsyncSession, user_id: Any) -> list[UserAuthIdentity]:
    rows = (
        await session.scalars(
            select(UserAuthIdentity)
            .where(
                UserAuthIdentity.user_id == user_id,
                UserAuthIdentity.revoked_at.is_(None),
            )
            .order_by(UserAuthIdentity.created_at)
        )
    ).all()
    if inspect.isawaitable(rows):
        rows = await cast(Awaitable[list[UserAuthIdentity]], rows)
    return list(rows)


async def revoke_identity(
    session: AsyncSession, user: User, identity_id: Any
) -> UserAuthIdentity:
    identity = await session.get(UserAuthIdentity, identity_id)
    if identity is None or identity.user_id != user.id or identity.revoked_at is not None:
        raise AppError(404, "oauth_identity_not_found", "找不到這個登入方式")
    identity_count = await session.scalar(
        select(func.count(UserAuthIdentity.id)).where(
            UserAuthIdentity.user_id == user.id,
            UserAuthIdentity.revoked_at.is_(None),
        )
    )
    if not user.password_hash and int(identity_count or 0) <= 1:
        raise AppError(409, "oauth_last_method", "至少需要保留一種可用的登入方式")
    identity.revoked_at = datetime.now(UTC)
    identity.revocation_pending = bool(
        identity.provider == "apple" and identity.refresh_token_encrypted
    )
    user.auth_version = (user.auth_version or 1) + 1
    await session.commit()
    return identity


async def attempt_provider_revocation(
    session: AsyncSession, identity: UserAuthIdentity
) -> bool:
    if not identity.revocation_pending or identity.provider != "apple":
        return True
    settings = await load_runtime_settings(session)
    token = decrypt_refresh_token(identity, settings)
    if not token or not provider_enabled("apple", settings):
        return False
    try:
        async with httpx.AsyncClient(timeout=12.0) as client:
            response = await client.post(
                APPLE_REVOKE,
                data={
                    "client_id": settings.auth_apple_services_id,
                    "client_secret": apple_client_secret(settings),
                    "token": token,
                    "token_type_hint": "refresh_token",
                },
            )
            response.raise_for_status()
    except (httpx.HTTPError, jwt.PyJWTError, ValueError):
        return False
    identity.revocation_pending = False
    identity.refresh_token_encrypted = None
    await session.commit()
    return True
