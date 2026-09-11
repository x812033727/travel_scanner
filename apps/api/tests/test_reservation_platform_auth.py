"""HTTP authorization checks without replacing current_user or require_admin.

Only test persistence/runtime dependencies are mocked. Tokens are ephemeral test
credentials and never leave ASGITransport; no production account is involved.
"""

from collections.abc import AsyncIterator
from datetime import UTC, datetime
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import fakeredis.aioredis
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

import app.auth.service as auth
from app.config import get_settings
from app.db import get_session
from app.foods.admin_router import router
from app.i18n import ERROR_DETAILS, LOCALES
from app.models import AdminRoleAssignment, User
from app.problems import AppError, app_error_handler


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("identity", "expected_status", "expected_code"),
    [
        ("anonymous", 401, "authentication_required"),
        ("member", 403, "admin_required"),
        ("viewer", 403, "admin_capability_required"),
        ("operations", 403, "admin_capability_required"),
        ("suspended", 403, "account_suspended"),
        ("revoked", 401, "invalid_token"),
        ("old_version", 401, "invalid_user"),
        ("content", 422, None),
    ],
)
async def test_platform_write_keeps_real_authentication_and_content_role(
    monkeypatch: pytest.MonkeyPatch,
    identity: str,
    expected_status: int,
    expected_code: str | None,
) -> None:
    api = FastAPI()
    api.include_router(router)
    api.add_exception_handler(AppError, app_error_handler)
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(auth, "get_redis", lambda: redis)
    monkeypatch.setattr(auth, "runtime_auth_settings", AsyncMock(return_value=get_settings()))
    user = User(
        id=uuid4(),
        email="reservation-auth@example.test",
        password_hash="unused-test-hash",
        is_active=True,
        is_admin=False,
        auth_version=1,
        suspended_at=datetime.now(UTC) if identity == "suspended" else None,
    )
    role = identity if identity in {"viewer", "operations", "content"} else "content"
    assignments = (
        []
        if identity == "member"
        else [AdminRoleAssignment(user_id=user.id, role=role, expires_at=None)]
    )
    session = AsyncMock()
    session.get.return_value = user
    session.scalars.return_value.all = Mock(return_value=assignments)

    async def provide_session() -> AsyncIterator[AsyncMock]:
        yield session

    api.dependency_overrides[get_session] = provide_session
    token = auth.create_access_token(user.id, auth_version=1)
    if identity == "old_version":
        user.auth_version = 2
    if identity == "revoked":
        await auth.revoke_access_token(auth.decode_access_token_claims(token))
    headers = {} if identity == "anonymous" else {"Authorization": f"Bearer {token}"}
    try:
        async with AsyncClient(transport=ASGITransport(app=api), base_url="http://test") as client:
            # Missing provider is intentional: an authorized content administrator
            # reaches schema validation; unauthorized callers are rejected first.
            result = await client.put(
                f"/admin/foods/merchants/{uuid4()}/platform-link",
                json={},
                headers=headers,
            )
        assert result.status_code == expected_status, result.text
        if expected_code:
            assert result.json()["code"] == expected_code
        session.commit.assert_not_awaited()
        session.execute.assert_not_awaited()
        session.add.assert_not_called()
    finally:
        await redis.aclose()


def test_platform_conflict_has_five_specific_translations() -> None:
    messages = [
        ERROR_DETAILS[locale]["reservation_platform_version_conflict"] for locale in LOCALES
    ]
    assert all(messages)
    assert len(set(messages)) == 5
