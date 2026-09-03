from collections.abc import AsyncIterator, Iterator
from unittest.mock import AsyncMock
from uuid import uuid4

import fakeredis.aioredis
import pytest
from httpx import ASGITransport, AsyncClient
from redis.exceptions import RedisError
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
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
from app.models import User
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
    session.get.return_value = user
    token = create_access_token(user.id, user.auth_version)
    assert await current_user(session, authorization=f"Bearer {token}", travel_access=None) is user

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 204
    assert 'travel_access=""' in response.headers["set-cookie"]

    with pytest.raises(AppError) as caught:
        await current_user(session, authorization=f"Bearer {token}", travel_access=None)
    assert caught.value.code == "invalid_token"
    with pytest.raises(AppError):
        await current_user(session, authorization=None, travel_access=token)
    claims = decode_access_token_claims(token)
    assert 0 < await redis.ttl(f"auth:revoked:{claims.token_id}") <= 3600
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
    session.get.return_value = user
    token = create_access_token(user.id, user.auth_version)
    with pytest.raises(AppError) as caught:
        await current_user(session, authorization=f"Bearer {token}", travel_access=None)
    assert caught.value.status == 503
    assert caught.value.code == "session_check_unavailable"


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
