from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from starlette.responses import Response

from app.auth.service import (
    create_access_token,
    current_user,
    decode_access_token_claims,
    hash_password,
    verify_password,
)
from app.db import get_session
from app.main import app
from app.models import User
from app.problems import AppError


@pytest.fixture(autouse=True)
def disable_password_change_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    async def allow(*_args: object, **_kwargs: object) -> None:
        return None

    monkeypatch.setattr("app.auth.router.enforce_named_rate_limit", allow)


def make_user(password: str) -> User:
    return User(
        id=uuid4(),
        email="member@example.com",
        password_hash=hash_password(password),
        auth_version=1,
    )


@pytest.mark.asyncio
async def test_change_password_requires_authentication() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/change-password",
            json={"current_password": "old-password-1", "new_password": "new-password-12"},
        )
    assert response.status_code == 401
    assert response.json()["code"] == "authentication_required"


@pytest.mark.asyncio
async def test_change_password_rejects_wrong_current_password() -> None:
    user = make_user("correct-password-1")
    session = AsyncMock()
    app.dependency_overrides[current_user] = lambda: user
    app.dependency_overrides[get_session] = lambda: session
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/change-password",
                json={"current_password": "wrong-password-1", "new_password": "new-password-12"},
            )
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 401
    assert response.json()["code"] == "invalid_credentials"
    session.commit.assert_not_awaited()
    assert verify_password("correct-password-1", user.password_hash)


@pytest.mark.asyncio
async def test_change_password_rejects_short_new_password() -> None:
    user = make_user("correct-password-1")
    app.dependency_overrides[current_user] = lambda: user
    app.dependency_overrides[get_session] = lambda: AsyncMock()
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/change-password",
                json={"current_password": "correct-password-1", "new_password": "short"},
            )
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_change_password_updates_the_stored_hash() -> None:
    user = make_user("correct-password-1")
    old_token = create_access_token(user.id, user.auth_version)
    session = AsyncMock()
    app.dependency_overrides[current_user] = lambda: user
    app.dependency_overrides[get_session] = lambda: session
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/change-password",
                json={
                    "current_password": "correct-password-1",
                    "new_password": "brand-new-password-1",
                },
            )
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200
    session.commit.assert_awaited_once()
    assert response.json()["expires_in"] == 3600
    new_token = response.json()["access_token"]
    assert decode_access_token_claims(old_token).auth_version == 1
    assert decode_access_token_claims(new_token).auth_version == 2

    session.get.return_value = user
    with pytest.raises(AppError) as caught:
        await current_user(
            session, Response(), authorization=f"Bearer {old_token}", travel_access=None
        )
    assert caught.value.code == "invalid_user"
    assert verify_password("brand-new-password-1", user.password_hash)
    assert not verify_password("correct-password-1", user.password_hash)
