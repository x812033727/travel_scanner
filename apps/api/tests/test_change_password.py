from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.auth.service import current_user, hash_password, verify_password
from app.db import get_session
from app.main import app
from app.models import User


def make_user(password: str) -> User:
    return User(email="member@example.com", password_hash=hash_password(password))


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
    assert response.status_code == 204
    session.commit.assert_awaited_once()
    assert verify_password("brand-new-password-1", user.password_hash)
    assert not verify_password("correct-password-1", user.password_hash)
