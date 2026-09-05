from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin import users as admin_users
from app.admin.user_schemas import AdminUsageAdjustment, AdminUserUpdate
from app.admin.users import _can_adjust_usage, adjusted_usage_balance
from app.auth.service import current_user
from app.config import get_settings
from app.main import app
from app.models import UsageAccount, User
from app.problems import AppError


def test_usage_adjustment_preserves_reserved_balance() -> None:
    account = UsageAccount(
        user_id=uuid4(),
        remaining_uses=5,
        reserved_uses=2,
    )
    assert adjusted_usage_balance(account, 3) == 8
    assert adjusted_usage_balance(account, -3) == 2
    with pytest.raises(AppError) as caught:
        adjusted_usage_balance(account, -4)
    assert caught.value.code == "admin_usage_below_reserved"


def test_only_environment_admin_can_adjust_own_usage(monkeypatch: pytest.MonkeyPatch) -> None:
    environment_admin = User(
        id=uuid4(),
        email="environment-admin@example.com",
        password_hash="unused",
        is_active=True,
        is_admin=False,
    )
    database_admin = User(
        id=uuid4(),
        email="database-admin@example.com",
        password_hash="unused",
        is_active=True,
        is_admin=True,
    )
    monkeypatch.setattr(get_settings(), "admin_emails", environment_admin.email.upper())

    assert _can_adjust_usage(environment_admin.id, environment_admin) is True
    environment_admin.is_admin = True
    assert _can_adjust_usage(environment_admin.id, environment_admin) is True
    assert _can_adjust_usage(database_admin.id, database_admin) is False
    assert _can_adjust_usage(environment_admin.id, database_admin) is True


def test_admin_user_payloads_require_meaningful_changes() -> None:
    assert AdminUsageAdjustment(change=5, reason="  客服補償  ").reason == "客服補償"
    with pytest.raises(ValidationError):
        AdminUsageAdjustment(change=0, reason="客服補償")
    with pytest.raises(ValidationError):
        AdminUsageAdjustment(change=1, reason="   ")
    with pytest.raises(ValidationError):
        AdminUserUpdate()


@pytest.mark.asyncio
@pytest.mark.parametrize(("initial", "updated"), [(True, False), (False, True)])
async def test_changing_account_active_state_revokes_existing_sessions(
    monkeypatch: pytest.MonkeyPatch, initial: bool, updated: bool
) -> None:
    user = User(
        id=uuid4(),
        email="target@example.com",
        password_hash="unused",
        is_active=initial,
        is_admin=False,
        auth_version=7,
    )
    actor = User(
        id=uuid4(),
        email="admin@example.com",
        password_hash="unused",
        is_active=True,
        is_admin=True,
    )
    session = AsyncMock(spec=AsyncSession)
    detail = object()
    monkeypatch.setattr(
        admin_users,
        "_user_and_account",
        AsyncMock(return_value=(user, None)),
    )
    monkeypatch.setattr(
        admin_users,
        "admin_user_detail",
        AsyncMock(return_value=detail),
    )

    result = await admin_users.update_admin_user(
        session,
        user.id,
        AdminUserUpdate(is_active=updated),
        actor,
    )

    assert result is detail
    assert user.is_active is updated
    assert user.auth_version == 8
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_admin_user_api_rejects_regular_user() -> None:
    user = User(
        email="member@example.com",
        password_hash="unused",
        is_active=True,
        is_admin=False,
    )
    app.dependency_overrides[current_user] = lambda: user
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v1/admin/users")
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 403
    assert response.json()["code"] == "admin_required"


@pytest.mark.asyncio
@pytest.mark.parametrize("setting", ["admin_emails", "deploy_admin_emails"])
@pytest.mark.parametrize(
    "payload",
    [AdminUserUpdate(is_active=False), AdminUserUpdate(is_admin=False)],
    ids=["suspend", "demote"],
)
async def test_environment_designated_admin_cannot_be_suspended_or_demoted(
    monkeypatch: pytest.MonkeyPatch, setting: str, payload: AdminUserUpdate
) -> None:
    """Suspension bumps auth_version and signs the account out, so it locks out an
    ADMIN_EMAILS / DEPLOY_ADMIN_EMAILS administrator as effectively as demotion."""
    monkeypatch.setattr(get_settings(), setting, "Owner@Example.com")
    target = User(
        id=uuid4(),
        email="owner@example.com",
        password_hash="unused",
        is_active=True,
        is_admin=True,
        auth_version=3,
    )
    actor = User(
        id=uuid4(),
        email="other-admin@example.com",
        password_hash="unused",
        is_active=True,
        is_admin=True,
    )
    session = AsyncMock(spec=AsyncSession)
    monkeypatch.setattr(
        admin_users, "_user_and_account", AsyncMock(return_value=(target, None))
    )

    with pytest.raises(AppError) as caught:
        await admin_users.update_admin_user(session, target.id, payload, actor)

    assert caught.value.code == "admin_environment_override"
    assert target.is_active is True
    assert target.is_admin is True
    assert target.auth_version == 3
    session.commit.assert_not_awaited()
