from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import Request
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.admin import user_router
from app.admin import users as admin_users
from app.admin.user_schemas import (
    AdminReasonRequest,
    AdminSuspensionRequest,
    AdminUsageAdjustment,
    AdminUserDetail,
    AdminUserUpdate,
)
from app.admin.users import _can_adjust_usage, adjusted_usage_balance
from app.auth.service import create_admin_step_up_token, current_user
from app.config import get_settings
from app.db import Base
from app.main import app
from app.models import AccountErasureRequest, AdminAuditLog, AdminRoleAssignment, UsageAccount, User
from app.problems import AppError


def test_user_detail_audit_history_redacts_secrets_embedded_in_values() -> None:
    item = AdminAuditLog(
        id=uuid4(),
        actor_user_id=None,
        action="legacy_failure",
        target="user:test",
        metadata_json={
            "detail": "password=hunter2; Authorization: Bearer exposed-value",
            "connection": "redis://service:redis-secret@redis/0",
            "opaque": ("eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.signature0123456789"),
        },
        created_at=datetime.now(UTC),
    )

    metadata = admin_users._audit_item(item).metadata  # noqa: SLF001

    assert metadata == {
        "detail": "password=***; Authorization: ***",
        "connection": "redis://service:***@redis/0",
        "opaque": "***",
    }


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
@pytest.mark.parametrize(("initial", "updated"), [(False, True)])
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
async def test_legacy_update_cannot_bypass_permanent_suspension_step_up(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = User(
        id=uuid4(),
        email="target@example.com",
        password_hash="unused",
        is_active=True,
        is_admin=False,
    )
    session = AsyncMock(spec=AsyncSession)
    monkeypatch.setattr(admin_users, "_user_and_account", AsyncMock(return_value=(target, None)))
    with pytest.raises(AppError) as caught:
        await admin_users.update_admin_user(
            session,
            target.id,
            AdminUserUpdate(is_active=False),
            User(email="admin@example.com", password_hash="unused", is_admin=True),
        )
    assert caught.value.code == "admin_suspension_endpoint_required"
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_legacy_update_cannot_promote_or_demote_an_administrator(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = User(
        id=uuid4(),
        email="target@example.com",
        password_hash="unused",
        is_active=True,
        is_admin=False,
    )
    session = AsyncMock(spec=AsyncSession)
    monkeypatch.setattr(admin_users, "_user_and_account", AsyncMock(return_value=(target, None)))

    with pytest.raises(AppError) as caught:
        await admin_users.update_admin_user(
            session,
            target.id,
            AdminUserUpdate(is_admin=True),
            User(email="support@example.com", password_hash="unused", is_admin=True),
        )

    assert caught.value.code == "admin_role_endpoint_required"
    assert target.is_admin is False
    session.commit.assert_not_awaited()


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
    monkeypatch.setattr(admin_users, "_user_and_account", AsyncMock(return_value=(target, None)))

    with pytest.raises(AppError) as caught:
        await admin_users.update_admin_user(session, target.id, payload, actor)

    assert caught.value.code == "admin_environment_override"
    assert target.is_active is True
    assert target.is_admin is True
    assert target.auth_version == 3
    session.commit.assert_not_awaited()


@pytest_asyncio.fixture
async def suspension_db(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> AsyncIterator[tuple[async_sessionmaker[AsyncSession], User, User]]:
    """Persist mutations locally without replacing the role/guard/write code."""
    engine = create_async_engine(f"sqlite+aiosqlite:///{(tmp_path / 'suspension.db').as_posix()}")
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda connection: Base.metadata.create_all(
                connection,
                tables=[
                    User.__table__,
                    UsageAccount.__table__,
                    AdminRoleAssignment.__table__,
                    AccountErasureRequest.__table__,
                    AdminAuditLog.__table__,
                ],
            )
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    actor = User(id=uuid4(), email="support@example.com", auth_version=3)
    target = User(id=uuid4(), email="target@example.com", auth_version=7)
    backup_owner = User(id=uuid4(), email="backup-owner@example.com")
    async with factory() as session:
        session.add_all([actor, target, backup_owner])
        await session.flush()
        session.add_all(
            [
                AdminRoleAssignment(user_id=actor.id, role="support"),
                AdminRoleAssignment(user_id=backup_owner.id, role="owner"),
            ]
        )
        await session.commit()
    # Detail rendering queries unrelated trip/community tables; keep the real
    # service authorization, last-owner check, idempotency and persisted writes.
    monkeypatch.setattr(
        admin_users, "admin_user_detail", AsyncMock(return_value=Mock(spec=AdminUserDetail))
    )
    try:
        yield factory, actor, target
    finally:
        await engine.dispose()


def _suspension_request(actor: User, credential: str = "missing") -> Request:
    headers: list[tuple[bytes, bytes]] = []
    if credential != "missing":
        scope = "users.roles" if credential == "wrong_scope" else "users.suspend_permanent"
        token, _ = create_admin_step_up_token(actor, [scope])
        if credential == "invalid":
            token = "invalid-token"
        headers.append((b"cookie", f"admin_step_up={token}".encode()))
    return Request(
        {"type": "http", "method": "POST", "path": "/admin/users/suspension", "headers": headers}
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("role", ["owner", "deployer", "database_operator"])
@pytest.mark.parametrize("credential", ["missing", "wrong_scope", "invalid", "valid"])
async def test_timed_privileged_suspension_requires_scoped_step_up(
    suspension_db: tuple[async_sessionmaker[AsyncSession], User, User],
    role: str,
    credential: str,
) -> None:
    factory, actor, target = suspension_db
    until = datetime.now(UTC) + timedelta(days=30)
    async with factory() as setup:
        setup.add(AdminRoleAssignment(user_id=target.id, role=role))
        await setup.commit()
    async with factory() as session:

        async def suspend() -> None:
            await user_router.post_admin_user_suspension(
                target.id,
                AdminSuspensionRequest(reason="security regression", suspended_until=until),
                _suspension_request(actor, credential),
                actor,
                session,
                "timed-privileged-test",
            )

        if credential == "valid":
            await suspend()
        else:
            with pytest.raises(AppError) as caught:
                await suspend()
            assert (caught.value.status, caught.value.code) == {
                "missing": (401, "admin_step_up_required"),
                "wrong_scope": (403, "admin_step_up_scope_required"),
                "invalid": (401, "admin_step_up_invalid"),
            }[credential]
            assert not session.dirty and not session.new
            await session.rollback()
    async with factory() as check:
        persisted = await check.get(User, target.id)
        assert persisted is not None
        assert persisted.auth_version == (8 if credential == "valid" else 7)
        assert (persisted.suspended_at is not None) == (credential == "valid")
        if credential == "valid":
            assert persisted.suspended_until is not None
            assert persisted.suspended_until.replace(tzinfo=UTC) == until
        audits = list((await check.scalars(select(AdminAuditLog))).all())
        assert [audit.action for audit in audits] == (
            ["user_suspended"] if credential == "valid" else []
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("role", ["owner", "deployer", "database_operator"])
async def test_timed_privileged_service_refuses_missing_verifier(
    suspension_db: tuple[async_sessionmaker[AsyncSession], User, User], role: str
) -> None:
    factory, actor, target = suspension_db
    async with factory() as session:
        session.add(AdminRoleAssignment(user_id=target.id, role=role))
        await session.commit()
        with pytest.raises(AppError) as caught:
            await admin_users.suspend_admin_user(
                session,
                target.id,
                AdminSuspensionRequest(
                    reason="no route verifier",
                    suspended_until=datetime.now(UTC) + timedelta(days=30),
                ),
                actor,
                "missing-verifier-test",
            )
        assert caught.value.code == "admin_step_up_required"
        assert not session.dirty and not session.new
        assert await session.scalar(select(func.count()).select_from(AdminAuditLog)) == 0
        persisted = await session.get(User, target.id)
        assert persisted is not None and persisted.auth_version == 7
        assert persisted.suspended_at is None


@pytest.mark.asyncio
@pytest.mark.parametrize("role", [None, "support", "owner", "deployer", "database_operator"])
async def test_ordinary_and_expired_role_timed_suspension_needs_no_step_up(
    suspension_db: tuple[async_sessionmaker[AsyncSession], User, User],
    monkeypatch: pytest.MonkeyPatch,
    role: str | None,
) -> None:
    factory, actor, target = suspension_db
    verifier = AsyncMock(side_effect=AssertionError("ordinary member must not require step-up"))
    monkeypatch.setattr(user_router, "require_admin_step_up", verifier)
    async with factory() as session:
        if role is not None:
            session.add(
                AdminRoleAssignment(
                    user_id=target.id,
                    role=role,
                    expires_at=None if role == "support" else datetime.now(UTC) - timedelta(days=1),
                )
            )
            await session.commit()
        await user_router.post_admin_user_suspension(
            target.id,
            AdminSuspensionRequest(
                reason="ordinary member flow",
                suspended_until=datetime.now(UTC) + timedelta(days=30),
            ),
            _suspension_request(actor),
            actor,
            session,
            "ordinary-member-test",
        )
        verifier.assert_not_awaited()
        persisted = await session.get(User, target.id)
        assert persisted is not None and persisted.auth_version == 8
        assert persisted.suspended_until is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "setting", ["admin_emails", "deploy_admin_emails", "database_admin_emails"]
)
@pytest.mark.parametrize("action", ["unsuspend", "revoke"])
async def test_environment_session_and_suspension_guards_do_not_mutate(
    suspension_db: tuple[async_sessionmaker[AsyncSession], User, User],
    monkeypatch: pytest.MonkeyPatch,
    setting: str,
    action: str,
) -> None:
    factory, actor, target = suspension_db
    monkeypatch.setattr(get_settings(), setting, target.email.upper())
    since = datetime.now(UTC) - timedelta(days=1)
    until = datetime.now(UTC) + timedelta(days=1)
    async with factory() as setup:
        persisted = await setup.get(User, target.id)
        assert persisted is not None
        persisted.suspended_at, persisted.suspended_until = since, until
        persisted.suspension_reason = "existing suspension"
        # A database assignment must not mask the environment protection.
        setup.add(AdminRoleAssignment(user_id=target.id, role="support"))
        await setup.commit()
    method = (
        admin_users.unsuspend_admin_user
        if action == "unsuspend"
        else admin_users.revoke_admin_user_sessions
    )
    async with factory() as session:
        with pytest.raises(AppError) as caught:
            await method(session, target.id, AdminReasonRequest(reason="guard regression"), actor)
        assert (caught.value.status, caught.value.code) == (409, "admin_environment_override")
        assert not session.dirty and not session.new
    async with factory() as check:
        persisted = await check.get(User, target.id)
        assert persisted is not None and persisted.auth_version == 7
        assert persisted.suspended_at is not None and persisted.suspended_until is not None
        assert persisted.suspended_at.replace(tzinfo=UTC) == since
        assert persisted.suspended_until.replace(tzinfo=UTC) == until
        assert persisted.suspension_reason == "existing suspension"
        assert await check.scalar(select(func.count()).select_from(AdminAuditLog)) == 0


@pytest.mark.asyncio
async def test_self_session_revocation_does_not_mutate(
    suspension_db: tuple[async_sessionmaker[AsyncSession], User, User],
) -> None:
    factory, actor, _ = suspension_db
    async with factory() as session:
        with pytest.raises(AppError) as caught:
            await admin_users.revoke_admin_user_sessions(
                session, actor.id, AdminReasonRequest(reason="self revocation"), actor
            )
        assert (caught.value.status, caught.value.code) == (409, "admin_self_action")
        assert not session.dirty and not session.new
        persisted = await session.get(User, actor.id)
        assert persisted is not None and persisted.auth_version == 3
        assert await session.scalar(select(func.count()).select_from(AdminAuditLog)) == 0


@pytest.mark.asyncio
async def test_suspension_refreshes_preloaded_target_auth_version(
    suspension_db: tuple[async_sessionmaker[AsyncSession], User, User],
) -> None:
    factory, actor, target = suspension_db
    async with factory() as session:
        stale = await session.get(User, target.id)
        assert stale is not None and stale.auth_version == 7
        async with factory() as other:
            await other.execute(update(User).where(User.id == target.id).values(auth_version=11))
            await other.commit()
        await user_router.post_admin_user_suspension(
            target.id,
            AdminSuspensionRequest(
                reason="fresh version regression",
                suspended_until=datetime.now(UTC) + timedelta(days=30),
            ),
            _suspension_request(actor),
            actor,
            session,
            "fresh-target-version",
        )
    async with factory() as check:
        persisted = await check.get(User, target.id)
        assert persisted is not None and persisted.auth_version == 12
