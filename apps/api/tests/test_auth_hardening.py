from collections.abc import AsyncIterator, Iterator
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import fakeredis.aioredis
import jwt
import pytest
from httpx import ASGITransport, AsyncClient
from redis.exceptions import RedisError
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Route

import app.auth.router as auth_router
import app.auth.service as auth_service
from app.auth.service import (
    create_access_token,
    current_user,
    decode_access_token_claims,
    hash_password,
    is_reserved_admin_email,
)
from app.config import get_settings
from app.db import escape_like, get_session
from app.main import app
from app.middleware import RequestBodyLimitMiddleware
from app.models import ProviderConfig, User
from app.problems import AppError, app_error_handler


class GuardedSession:
    def __init__(self) -> None:
        self.mutated = False

    def add(self, _value: object) -> None:
        self.mutated = True


@pytest.fixture
def guarded_session() -> GuardedSession:
    return GuardedSession()


@pytest.fixture
def session_override(guarded_session: GuardedSession) -> Iterator[None]:
    async def provide_session() -> AsyncIterator[GuardedSession]:
        yield guarded_session

    app.dependency_overrides[get_session] = provide_session
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def open_registration(monkeypatch: pytest.MonkeyPatch) -> None:
    async def allow_rate_limit(*_args: object, **_kwargs: object) -> None:
        return None

    async def enabled(_session: object) -> bool:
        return True

    monkeypatch.setattr(auth_router, "enforce_named_rate_limit", allow_rate_limit)
    monkeypatch.setattr(auth_router, "effective_registration_enabled", enabled)


def make_user() -> User:
    return User(
        id=uuid4(),
        email="member@example.com",
        password_hash=hash_password("correct-password-1"),
        is_active=True,
        is_admin=False,
        auth_version=1,
    )


def test_reserved_admin_email_detection_is_case_insensitive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "admin_emails", "Owner@Example.com")
    monkeypatch.setattr(settings, "deploy_admin_emails", "deploy@example.com")
    assert is_reserved_admin_email("owner@example.com") is True
    assert is_reserved_admin_email("  OWNER@EXAMPLE.COM ") is True
    assert is_reserved_admin_email("deploy@example.com") is True
    assert is_reserved_admin_email("member@example.com") is False


@pytest.mark.asyncio
@pytest.mark.parametrize("setting", ["admin_emails", "deploy_admin_emails"])
async def test_reserved_admin_email_cannot_self_register(
    setting: str,
    monkeypatch: pytest.MonkeyPatch,
    guarded_session: GuardedSession,
    session_override: None,
    open_registration: None,
) -> None:
    monkeypatch.setattr(get_settings(), setting, "Owner@Example.com")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "owner@example.com", "password": "strong-password-123"},
        )

    assert response.status_code == 403
    assert response.json()["code"] == "admin_email_reserved"
    assert "set-cookie" not in response.headers
    assert not guarded_session.mutated


@pytest.mark.asyncio
async def test_reserved_admin_email_is_localized_for_other_locales(
    monkeypatch: pytest.MonkeyPatch,
    session_override: None,
    open_registration: None,
) -> None:
    monkeypatch.setattr(get_settings(), "admin_emails", "owner@example.com")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "owner@example.com", "password": "strong-password-123"},
            headers={"X-Travel-Locale": "en"},
        )
    assert response.status_code == 403
    assert "administrator" in response.json()["detail"]


@pytest.mark.asyncio
async def test_logout_revokes_the_presented_token(monkeypatch: pytest.MonkeyPatch) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(auth_service, "get_redis", lambda: redis)
    user = make_user()
    session = AsyncMock()
    session.scalars.return_value.all = Mock(return_value=[])
    session.get.return_value = user
    token = create_access_token(user.id, user.auth_version)
    assert (
        await current_user(session, Response(), authorization=f"Bearer {token}", travel_access=None)
        is user
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 204
    assert 'travel_access=""' in response.headers["set-cookie"]

    with pytest.raises(AppError) as caught:
        await current_user(session, Response(), authorization=f"Bearer {token}", travel_access=None)
    assert caught.value.code == "invalid_token"
    with pytest.raises(AppError):
        await current_user(session, Response(), authorization=None, travel_access=token)
    claims = decode_access_token_claims(token)
    # The deny entry covers the whole sign-in (until the absolute cap), not just the
    # presented copy: renewals share this jti but keep minting later expiries.
    ttl = await redis.ttl(f"auth:revoked:{claims.token_id}")
    cap_seconds = get_settings().session_absolute_max_days * 86_400
    assert get_settings().access_token_expire_minutes * 60 < ttl <= cap_seconds + 1
    await redis.aclose()


def aged_token(user: User, *, issued_ago: timedelta, session_age: timedelta) -> str:
    """Mint a token as if it had been issued earlier, without waiting."""
    settings = get_settings()
    now = datetime.now(UTC)
    issued = now - issued_ago
    return jwt.encode(
        {
            "sub": str(user.id),
            "ver": user.auth_version,
            "iss": auth_service.ISSUER,
            "aud": auth_service.AUDIENCE,
            "jti": str(uuid4()),
            "iat": issued,
            "nbf": issued,
            "exp": issued + timedelta(minutes=settings.access_token_expire_minutes),
            "sid_iat": int((now - session_age).timestamp()),
        },
        settings.app_secret_key,
        algorithm=auth_service.ALGORITHM,
    )


@pytest.mark.asyncio
async def test_cookie_session_slides_forward_after_half_its_lifetime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(auth_service, "get_redis", lambda: redis)
    user = make_user()
    session = AsyncMock()
    session.scalars.return_value.all = Mock(return_value=[])
    session.get.return_value = user
    lifetime = timedelta(minutes=get_settings().access_token_expire_minutes)

    fresh = Response()
    await current_user(
        session,
        fresh,
        authorization=None,
        travel_access=aged_token(user, issued_ago=lifetime * 0.2, session_age=lifetime * 0.2),
    )
    assert "set-cookie" not in fresh.headers

    stale = aged_token(user, issued_ago=lifetime * 0.7, session_age=timedelta(days=2))
    renewed = Response()
    await current_user(session, renewed, authorization=None, travel_access=stale)
    cookie = renewed.headers["set-cookie"]
    assert cookie.startswith("travel_access=") and "HttpOnly" in cookie
    new_token = cookie.split("travel_access=", 1)[1].split(";", 1)[0]
    new_claims = decode_access_token_claims(new_token)
    old_claims = decode_access_token_claims(stale)
    assert new_claims.expires_at > old_claims.expires_at
    assert new_claims.session_started_at == old_claims.session_started_at
    # One id for the whole sign-in. A fresh id per renewal let a copied cookie renew into
    # a chain of its own, and signing out - which denylists only the id it was handed -
    # could not reach it.
    assert new_claims.token_id == old_claims.token_id

    bearer = Response()
    await current_user(session, bearer, authorization=f"Bearer {stale}", travel_access=None)
    assert "set-cookie" not in bearer.headers

    expired_session = aged_token(
        user,
        issued_ago=lifetime * 0.7,
        session_age=timedelta(days=get_settings().session_absolute_max_days + 1),
    )
    # Past the absolute cap the token is refused outright, not merely left unrenewed:
    # one minted just before the cap would otherwise stay usable for its whole lifetime.
    with pytest.raises(AppError) as expired:
        await current_user(session, Response(), authorization=None, travel_access=expired_session)
    assert expired.value.status == 401
    await redis.aclose()


@pytest.mark.asyncio
async def test_signing_out_ends_a_session_that_has_already_been_renewed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The property the shared id exists for: renewal must not outlive a sign-out."""
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(auth_service, "get_redis", lambda: redis)
    user = make_user()
    session = AsyncMock()
    session.scalars.return_value.all = Mock(return_value=[])
    session.get.return_value = user
    lifetime = timedelta(minutes=get_settings().access_token_expire_minutes)

    original = aged_token(user, issued_ago=lifetime * 0.7, session_age=lifetime * 0.7)
    response = Response()
    await current_user(session, response, authorization=None, travel_access=original)
    renewed = response.headers["set-cookie"].split("travel_access=", 1)[1].split(";", 1)[0]

    # Signing out with either copy has to invalidate both, because they are one session.
    await auth_service.revoke_access_token(decode_access_token_claims(original))

    for token in (original, renewed):
        with pytest.raises(AppError) as refused:
            await current_user(session, Response(), authorization=None, travel_access=token)
        assert refused.value.status == 401
    await redis.aclose()


@pytest.mark.asyncio
async def test_logout_denylist_outlives_every_renewed_sibling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Revoking with an early copy must still cover siblings renewed after it.

    Renewal keeps one jti but mints later expiries. Keying the deny TTL to the
    presented copy's exp let a sibling renewed later come back to life once the
    entry aged out — and renew itself for the rest of the absolute cap, while every
    later logout denylists a different, fresh jti.
    """
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(auth_service, "get_redis", lambda: redis)
    user = make_user()
    session = AsyncMock()
    session.scalars.return_value.all = Mock(return_value=[])
    session.get.return_value = user
    settings = get_settings()
    lifetime = timedelta(minutes=settings.access_token_expire_minutes)

    original = aged_token(user, issued_ago=lifetime * 0.7, session_age=timedelta(days=2))
    response = Response()
    await current_user(session, response, authorization=None, travel_access=original)
    sibling = response.headers["set-cookie"].split("travel_access=", 1)[1].split(";", 1)[0]
    original_claims = decode_access_token_claims(original)
    sibling_claims = decode_access_token_claims(sibling)
    assert sibling_claims.expires_at > original_claims.expires_at

    await auth_service.revoke_access_token(original_claims)

    ttl = await redis.ttl(f"auth:revoked:{original_claims.token_id}")
    now = datetime.now(UTC)
    sibling_remaining = (sibling_claims.expires_at - now).total_seconds()
    cap_remaining = (
        original_claims.session_started_at
        + timedelta(days=settings.session_absolute_max_days)
        - now
    ).total_seconds()
    assert ttl > sibling_remaining
    assert ttl >= cap_remaining - 5
    for token in (original, sibling):
        with pytest.raises(AppError) as refused:
            await current_user(session, Response(), authorization=None, travel_access=token)
        assert refused.value.status == 401
    await redis.aclose()


@pytest.mark.asyncio
async def test_logout_without_a_valid_token_still_clears_the_cookie(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(auth_service, "get_redis", lambda: redis)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        anonymous = await client.post("/api/v1/auth/logout")
        client.cookies.set("travel_access", "not-a-jwt")
        garbage = await client.post("/api/v1/auth/logout")
    assert anonymous.status_code == 204
    assert garbage.status_code == 204
    assert 'travel_access=""' in garbage.headers["set-cookie"]
    assert await redis.keys("auth:revoked:*") == []
    await redis.aclose()


@pytest.mark.asyncio
async def test_revocation_check_fails_closed_when_redis_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class BrokenRedis:
        async def exists(self, *_args: object) -> int:
            raise RedisError("redis is down")

    monkeypatch.setattr(auth_service, "get_redis", lambda: BrokenRedis())
    user = make_user()
    session = AsyncMock()
    session.scalars.return_value.all = Mock(return_value=[])
    session.get.return_value = user
    token = create_access_token(user.id, user.auth_version)
    with pytest.raises(AppError) as caught:
        await current_user(session, Response(), authorization=f"Bearer {token}", travel_access=None)
    assert caught.value.status == 503
    assert caught.value.code == "session_check_unavailable"


def test_runtime_settings_change_the_lifetime_of_new_tokens() -> None:
    """The lifetime comes from the settings handed in, which the routes load from the
    administrator's runtime overrides; the environment value is only the fallback."""
    base = get_settings()
    shorter = base.model_copy(update={"access_token_expire_minutes": 15})
    claims = decode_access_token_claims(create_access_token(uuid4(), settings=shorter))
    assert claims.expires_at - claims.issued_at == timedelta(minutes=15)
    default = decode_access_token_claims(create_access_token(uuid4()))
    assert default.expires_at - default.issued_at == timedelta(
        minutes=base.access_token_expire_minutes
    )


@pytest.mark.asyncio
async def test_a_renewal_mints_with_the_lifetime_the_administrator_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The end-to-end check the first attempt at this setting never had: a stored runtime
    override, a cookie due for renewal, and the renewed token carrying the new lifetime."""
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(auth_service, "get_redis", lambda: redis)
    user = make_user()
    session = AsyncMock()
    session.get.return_value = user
    row = ProviderConfig(
        provider="runtime",
        enabled=True,
        config={"access_token_expire_minutes": 15, "session_absolute_max_days": 3},
        secret_config_encrypted=None,
    )
    session.scalars.return_value.all = Mock(return_value=[row])
    lifetime = timedelta(minutes=get_settings().access_token_expire_minutes)

    renewed = Response()
    await current_user(
        session,
        renewed,
        authorization=None,
        travel_access=aged_token(user, issued_ago=lifetime * 0.7, session_age=timedelta(days=1)),
    )
    new_token = renewed.headers["set-cookie"].split("travel_access=", 1)[1].split(";", 1)[0]
    new_claims = decode_access_token_claims(new_token)
    assert new_claims.expires_at - new_claims.issued_at == timedelta(minutes=15)
    assert "Max-Age=900" in renewed.headers["set-cookie"]

    # The absolute cap is the administrator's too: three days, not the environment's.
    with pytest.raises(AppError) as expired:
        await current_user(
            session,
            Response(),
            authorization=None,
            travel_access=aged_token(
                user, issued_ago=lifetime * 0.2, session_age=timedelta(days=4)
            ),
        )
    assert expired.value.code == "session_expired"
    await redis.aclose()


def test_escape_like_neutralizes_pattern_metacharacters() -> None:
    assert escape_like("50%_off\\") == "50\\%\\_off\\\\"
    assert escape_like("plain text") == "plain text"


def limited_app(max_bytes: int) -> Starlette:
    async def echo(request: Request) -> PlainTextResponse:
        body = await request.body()
        return PlainTextResponse(str(len(body)))

    application = Starlette(routes=[Route("/echo", echo, methods=["POST"])])
    application.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    application.add_middleware(RequestBodyLimitMiddleware, max_bytes=max_bytes)
    return application


@pytest.mark.asyncio
async def test_request_body_limit_rejects_declared_and_streamed_oversized_bodies() -> None:
    application = limited_app(100)
    transport = ASGITransport(app=application)

    async def chunks() -> AsyncIterator[bytes]:
        for _ in range(3):
            yield b"x" * 60

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        declared = await client.post("/echo", content=b"x" * 200)
        streamed = await client.post("/echo", content=chunks())
        accepted = await client.post("/echo", content=b"x" * 100)
        negative = await client.post("/echo", content=b"", headers={"Content-Length": "-1"})

    assert declared.status_code == 413
    assert declared.json()["code"] == "request_too_large"
    assert streamed.status_code == 413
    assert streamed.json()["code"] == "request_too_large"
    assert accepted.status_code == 200
    assert accepted.text == "100"
    assert negative.status_code == 400
    assert negative.json()["code"] == "invalid_content_length"


def test_api_installs_the_request_body_limit() -> None:
    assert any(item.cls is RequestBodyLimitMiddleware for item in app.user_middleware)
    assert get_settings().api_max_request_bytes == 5_242_880
