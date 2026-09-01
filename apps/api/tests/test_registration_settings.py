from collections.abc import AsyncIterator, Iterator

import pytest
from httpx import ASGITransport, AsyncClient

import app.auth.router as auth_router
from app.db import get_session
from app.main import app


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


@pytest.mark.asyncio
async def test_registration_status_is_public_and_not_cached(
    monkeypatch: pytest.MonkeyPatch,
    session_override: None,
) -> None:
    async def enabled(_session: object) -> bool:
        return True

    monkeypatch.setattr(auth_router, "effective_registration_enabled", enabled)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/auth/registration-status")

    assert response.status_code == 200
    assert response.json() == {"registration_enabled": True}
    assert response.headers["cache-control"] == "no-store"


@pytest.mark.asyncio
@pytest.mark.parametrize("email", ["member@example.com", "environment-admin@example.com"])
async def test_closed_registration_fails_before_any_account_or_cookie_side_effect(
    email: str,
    monkeypatch: pytest.MonkeyPatch,
    guarded_session: GuardedSession,
    session_override: None,
) -> None:
    async def allow_rate_limit(*_args: object, **_kwargs: object) -> None:
        return None

    async def disabled(_session: object) -> bool:
        return False

    monkeypatch.setattr(auth_router, "enforce_named_rate_limit", allow_rate_limit)
    monkeypatch.setattr(auth_router, "effective_registration_enabled", disabled)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "strong-password-123"},
        )

    assert response.status_code == 403
    assert response.json()["code"] == "registration_closed"
    assert "set-cookie" not in response.headers
    assert not guarded_session.mutated
