import hashlib
import json
from unittest.mock import AsyncMock
from urllib.parse import parse_qs, urlparse
from uuid import uuid4

import fakeredis.aioredis
import pytest

from app.auth.oauth import (
    OAuthProfile,
    exchange_oauth,
    provider_status,
    revoke_identity,
    start_oauth,
)
from app.auth.schemas import OAuthStartRequest
from app.config import Settings, get_settings
from app.models import User, UserAuthIdentity
from app.problems import AppError


def oauth_settings() -> Settings:
    return Settings(
        _env_file=None,
        next_public_site_url="https://mokaair.com",
        auth_google_enabled=True,
        auth_google_client_id="google-client",
        auth_google_client_secret="google-secret",
        auth_line_enabled=True,
        auth_line_channel_id="line-channel",
        auth_line_channel_secret="line-secret",
    )


def test_provider_status_requires_both_enablement_and_credentials() -> None:
    status = provider_status(oauth_settings())
    assert status == {"google": True, "line": True, "apple": False}


@pytest.mark.asyncio
async def test_google_start_uses_pkce_and_one_time_server_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = oauth_settings()

    async def runtime_settings(_session: object) -> Settings:
        return settings

    monkeypatch.setattr("app.auth.oauth.load_runtime_settings", runtime_settings)
    monkeypatch.setattr("app.auth.oauth.get_redis", lambda: redis)
    result = await start_oauth(
        AsyncMock(),
        OAuthStartRequest(
            locale="ja",
            next_path="//evil.example/path",
            browser_binding="binding_abcdefghijklmnopqrstuvwxyz123456",
        ),
        "google",
        None,
    )
    query = parse_qs(urlparse(result.authorization_url).query)
    assert query["redirect_uri"] == ["https://mokaair.com/api/auth/oauth/google/callback"]
    assert query["scope"] == ["openid email"]
    assert query["code_challenge_method"] == ["S256"]
    flow = json.loads(await redis.get(f"oauth-flow:{result.flow_id}"))
    assert flow["locale"] == "ja"
    assert flow["next"] == "/"
    assert flow["binding"] != "binding_abcdefghijklmnopqrstuvwxyz123456"


@pytest.mark.asyncio
async def test_exchange_consumes_state_even_when_browser_binding_is_wrong(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr("app.auth.oauth.get_redis", lambda: redis)
    await redis.set(
        "oauth-flow:abcdefghijklmnopqrstuvwxyz123456",
        json.dumps(
            {
                "provider": "google",
                "state": "state_abcdefghijklmnopqrstuvwxyz123456",
                "binding": "not-the-browser-hash",
            }
        ),
    )
    with pytest.raises(AppError) as raised:
        await exchange_oauth(
            AsyncMock(),
            "google",
            flow_id="abcdefghijklmnopqrstuvwxyz123456",
            state="state_abcdefghijklmnopqrstuvwxyz123456",
            code="code",
            browser_binding="binding_abcdefghijklmnopqrstuvwxyz123456",
            current_user=None,
        )
    assert raised.value.code == "oauth_state_invalid"
    assert await redis.get("oauth-flow:abcdefghijklmnopqrstuvwxyz123456") is None


@pytest.mark.asyncio
async def test_matching_provider_email_never_auto_merges_existing_account(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    binding = "binding_abcdefghijklmnopqrstuvwxyz123456"
    flow_id = "flow_id_abcdefghijklmnopqrstuvwxyz123456"
    state = "state_abcdefghijklmnopqrstuvwxyz123456"
    await redis.set(
        f"oauth-flow:{flow_id}",
        json.dumps(
            {
                "provider": "google",
                "intent": "login",
                "state": state,
                "binding": hashlib.sha256(binding.encode()).hexdigest(),
                "nonce": "nonce",
                "verifier": "verifier",
                "locale": "en",
                "next": "/account",
            }
        ),
    )

    async def runtime_settings(_session: object) -> Settings:
        return oauth_settings()

    async def profile(*_args: object, **_kwargs: object) -> OAuthProfile:
        return OAuthProfile("google-subject", "member@example.com", True)

    async def existing_user(_session: object, _email: str) -> User:
        return User(email="member@example.com", password_hash="hash")

    session = AsyncMock()
    session.scalar.return_value = None
    monkeypatch.setattr("app.auth.oauth.get_redis", lambda: redis)
    monkeypatch.setattr("app.auth.oauth.load_runtime_settings", runtime_settings)
    monkeypatch.setattr("app.auth.oauth.exchange_profile", profile)
    monkeypatch.setattr("app.auth.oauth.find_user_by_email", existing_user)

    with pytest.raises(AppError) as raised:
        await exchange_oauth(
            session,
            "google",
            flow_id=flow_id,
            state=state,
            code="code",
            browser_binding=binding,
            current_user=None,
        )
    assert raised.value.code == "oauth_account_exists"
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_social_only_user_cannot_disconnect_last_identity() -> None:
    user = User(
        id=uuid4(),
        email="social@example.com",
        password_hash=None,
        auth_version=1,
    )
    identity = UserAuthIdentity(
        id=uuid4(), user_id=user.id, provider="line", subject="line-subject"
    )
    session = AsyncMock()
    session.get.return_value = identity
    session.scalar.return_value = 1
    with pytest.raises(AppError) as raised:
        await revoke_identity(session, user, identity.id)
    assert raised.value.code == "oauth_last_method"
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_reserved_admin_email_cannot_be_claimed_through_oauth(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Same rule as password registration: a reserved administrator address must never
    be creatable by whoever controls it at a provider (API-01 covered only /register)."""
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    binding = "binding_abcdefghijklmnopqrstuvwxyz123456"
    flow_id = "flow_id_abcdefghijklmnopqrstuvwxyz123456"
    state = "state_abcdefghijklmnopqrstuvwxyz123456"
    await redis.set(
        f"oauth-flow:{flow_id}",
        json.dumps(
            {
                "provider": "google",
                "intent": "login",
                "state": state,
                "binding": hashlib.sha256(binding.encode()).hexdigest(),
                "nonce": "nonce",
                "verifier": "verifier",
                "locale": "en",
                "next": "/account",
            }
        ),
    )

    async def runtime_settings(_session: object) -> Settings:
        return oauth_settings()

    async def profile(*_args: object, **_kwargs: object) -> OAuthProfile:
        return OAuthProfile("google-subject", "owner@example.com", True)

    async def nobody(_session: object, _email: str) -> None:
        return None

    async def registration_open(_session: object) -> bool:
        return True

    monkeypatch.setattr(get_settings(), "admin_emails", "Owner@Example.com")
    session = AsyncMock()
    session.scalar.return_value = None
    monkeypatch.setattr("app.auth.oauth.get_redis", lambda: redis)
    monkeypatch.setattr("app.auth.oauth.load_runtime_settings", runtime_settings)
    monkeypatch.setattr("app.auth.oauth.exchange_profile", profile)
    monkeypatch.setattr("app.auth.oauth.find_user_by_email", nobody)
    monkeypatch.setattr("app.auth.oauth.effective_registration_enabled", registration_open)

    with pytest.raises(AppError) as raised:
        await exchange_oauth(
            session,
            "google",
            flow_id=flow_id,
            state=state,
            code="code",
            browser_binding=binding,
            current_user=None,
        )
    assert raised.value.code == "admin_email_reserved"
    session.commit.assert_not_awaited()
