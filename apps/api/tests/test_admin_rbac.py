import asyncio
import re
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from fastapi import Request, Response
from sqlalchemy import create_engine, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session

from app import cli as app_cli
from app.admin import security_router
from app.admin import users as admin_users
from app.admin.user_schemas import (
    AdminErasureRequest,
    AdminReasonRequest,
    AdminRolesUpdate,
    AdminStepUpRequest,
    AdminSuspensionRequest,
    AdminUsageAdjustment,
    AdminUserDetail,
)
from app.auth.service import (
    ADMIN_ROLE_CAPABILITIES,
    _admin_path_capability,
    can_database_maintain_user,
    can_deploy_user,
    create_admin_step_up_token,
    effective_admin_capabilities,
    is_admin_user,
    require_admin_step_up,
)
from app.community import accounts as community_accounts
from app.community import jobs as community_jobs
from app.community.models import Job
from app.config import get_settings
from app.db import Base
from app.models import (
    AccountErasureRequest,
    AdminAuditLog,
    AdminRoleAssignment,
    UsageAccount,
    UsageLedger,
    User,
)
from app.problems import AppError


def _request(cookie: str | None = None, *, path: str = "/", method: str = "POST") -> Request:
    headers = [] if cookie is None else [(b"cookie", cookie.encode())]
    return Request({"type": "http", "method": method, "path": path, "headers": headers})


def test_role_capability_matrix_does_not_overgrant_sensitive_operations() -> None:
    assert "community.manage" in ADMIN_ROLE_CAPABILITIES["support"]
    assert "community.manage" not in ADMIN_ROLE_CAPABILITIES["content"]
    assert "deploy.execute" not in ADMIN_ROLE_CAPABILITIES["operations"]
    assert "database.maintain" not in ADMIN_ROLE_CAPABILITIES["operations"]
    assert "roles.manage" in ADMIN_ROLE_CAPABILITIES["owner"]


def test_documented_role_capability_matrix_matches_runtime() -> None:
    document = (
        Path(__file__).resolve().parents[3] / "docs" / "admin-operations-center.md"
    ).read_text(encoding="utf-8")
    start = "<!-- admin-role-capabilities:start -->"
    end = "<!-- admin-role-capabilities:end -->"
    assert document.count(start) == 1
    assert document.count(end) == 1
    block = document.split(start, 1)[1].split(end, 1)[0]
    documented: dict[str, frozenset[str]] = {}
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        assert len(cells) == 2
        role_tokens = re.findall(r"`([^`]+)`", cells[0])
        assert len(role_tokens) == 1
        role = role_tokens[0]
        assert role not in documented
        documented[role] = frozenset(re.findall(r"`([^`]+)`", cells[1]))

    assert documented == {
        role: frozenset(capabilities) for role, capabilities in ADMIN_ROLE_CAPABILITIES.items()
    }


@pytest.mark.asyncio
async def test_step_up_records_safe_success_and_failure_audits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user = User(
        id=uuid4(),
        email="owner@example.com",
        password_hash="stored-hash",
        is_active=True,
        is_admin=True,
    )
    monkeypatch.setattr(get_settings(), "admin_emails", user.email)
    monkeypatch.setattr(security_router, "enforce_named_rate_limit", AsyncMock())

    rejected = AsyncMock(spec=AsyncSession)
    monkeypatch.setattr(security_router, "verify_password", Mock(return_value=False))
    with pytest.raises(AppError) as error:
        await security_router.step_up(
            AdminStepUpRequest(password="wrong-password", scopes=["users.roles"]),
            _request(path="/api/v1/admin/step-up"),
            Response(),
            user,
            rejected,
        )
    assert error.value.code == "invalid_credentials"
    rejected.commit.assert_awaited_once()
    failed_audit = rejected.add.call_args.args[0]
    assert isinstance(failed_audit, AdminAuditLog)
    assert failed_audit.action == "admin_step_up_failed"
    assert failed_audit.metadata_json == {
        "result": "failed",
        "scopes": ["users.roles"],
        "code": "invalid_credentials",
    }
    assert "password" not in str(failed_audit.metadata_json).lower()

    accepted = AsyncMock(spec=AsyncSession)
    monkeypatch.setattr(security_router, "verify_password", Mock(return_value=True))
    response = Response()
    result = await security_router.step_up(
        AdminStepUpRequest(password="correct-password", scopes=["users.roles"]),
        _request(path="/api/v1/admin/step-up"),
        response,
        user,
        accepted,
    )
    assert result.scopes == ["users.roles"]
    accepted.commit.assert_awaited_once()
    success_audit = accepted.add.call_args.args[0]
    assert isinstance(success_audit, AdminAuditLog)
    assert success_audit.action == "admin_step_up_succeeded"
    assert success_audit.metadata_json == {
        "result": "succeeded",
        "scopes": ["users.roles"],
    }
    assert "admin_step_up=" in response.headers["set-cookie"]


@pytest.mark.asyncio
async def test_request_mail_defaults_commit_and_enqueue_but_supports_deferred_admin_flow(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user = User(
        id=uuid4(),
        email="member@example.com",
        password_hash="unused",
        is_active=True,
        auth_version=1,
    )
    wake = Mock(return_value=True)
    monkeypatch.setattr(community_accounts, "smtp_ready", Mock(return_value=True))
    monkeypatch.setattr(community_jobs, "enqueue_jobs", wake)
    committed = AsyncMock(spec=AsyncSession)
    committed.scalar.return_value = user

    await community_accounts.request_mail(committed, user, "verify", "zh-TW")

    committed.commit.assert_awaited_once()
    wake.assert_called_once()

    deferred = AsyncMock(spec=AsyncSession)
    deferred.scalar.return_value = user
    await community_accounts.request_mail(
        deferred,
        user,
        "verify",
        "zh-TW",
        commit=False,
        enqueue=False,
    )
    deferred.commit.assert_not_awaited()
    wake.assert_called_once()


@pytest.mark.asyncio
async def test_postgresql_owner_guard_uses_transaction_advisory_lock() -> None:
    session = AsyncMock(spec=AsyncSession)
    bind = Mock()
    bind.dialect.name = "postgresql"
    session.get_bind.return_value = bind

    async with admin_users._owner_mutation_guard(session):
        pass

    session.execute.assert_awaited_once()
    statement, parameters = session.execute.await_args.args
    assert "pg_advisory_xact_lock" in str(statement)
    assert parameters == {"lock_id": admin_users.OWNER_MUTATION_ADVISORY_LOCK_ID}


@pytest.mark.asyncio
async def test_all_owner_removing_entrypoints_use_the_shared_guard(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    entered: list[str] = []

    @asynccontextmanager
    async def guard(_session: AsyncSession):
        entered.append("entered")
        yield

    expected = AdminUserDetail.model_construct()
    role_impl = AsyncMock(return_value=expected)
    suspension_impl = AsyncMock(return_value=expected)
    erasure_impl = AsyncMock(return_value=expected)
    monkeypatch.setattr(admin_users, "_owner_mutation_guard", guard)
    monkeypatch.setattr(admin_users, "_replace_admin_roles_serialized", role_impl)
    monkeypatch.setattr(admin_users, "_suspend_admin_user_serialized", suspension_impl)
    monkeypatch.setattr(admin_users, "_schedule_admin_erasure_serialized", erasure_impl)
    session = AsyncMock(spec=AsyncSession)
    actor = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    target_id = uuid4()

    await admin_users.replace_admin_roles(
        session,
        target_id,
        AdminRolesUpdate(roles=[], reason="角色調整", confirmation="unused"),
        actor,
        "roles-key",
    )
    await admin_users.suspend_admin_user(
        session,
        target_id,
        AdminSuspensionRequest(reason="永久停權", confirmation="unused"),
        actor,
        "suspension-key",
    )
    await admin_users.schedule_admin_erasure(
        session,
        target_id,
        AdminErasureRequest(reason="個資清除", confirmation="unused"),
        actor,
        "erasure-key",
    )

    assert entered == ["entered", "entered", "entered"]
    role_impl.assert_awaited_once()
    suspension_impl.assert_awaited_once()
    erasure_impl.assert_awaited_once()


@pytest.mark.asyncio
async def test_concurrent_owner_removals_leave_one_owner(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    engine = create_async_engine(f"sqlite+aiosqlite:///{(tmp_path / 'owners.db').as_posix()}")
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync_connection: Base.metadata.create_all(
                sync_connection,
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
    actor = User(id=uuid4(), email="actor@example.com", password_hash="unused")
    first = User(id=uuid4(), email="first-owner@example.com", password_hash="unused", is_admin=True)
    second = User(
        id=uuid4(), email="second-owner@example.com", password_hash="unused", is_admin=True
    )
    async with factory() as session:
        session.add_all([actor, first, second])
        await session.flush()
        session.add_all(
            [
                AdminRoleAssignment(user_id=first.id, role="owner", source="manual"),
                AdminRoleAssignment(user_id=second.id, role="owner", source="manual"),
            ]
        )
        await session.commit()
    monkeypatch.setattr(
        admin_users,
        "admin_user_detail",
        AsyncMock(return_value=Mock(spec=AdminUserDetail)),
    )

    async def remove_owner(target: User, key: str) -> object:
        async with factory() as session:
            return await admin_users.replace_admin_roles(
                session,
                target.id,
                AdminRolesUpdate(
                    roles=[],
                    reason="並行移除測試",
                    confirmation=f"ROLES {target.email}",
                ),
                actor,
                key,
            )

    results = await asyncio.gather(
        remove_owner(first, "remove-first"),
        remove_owner(second, "remove-second"),
        return_exceptions=True,
    )

    failures = [result for result in results if isinstance(result, AppError)]
    assert len(failures) == 1
    assert failures[0].code == "admin_last_owner"
    async with factory() as session:
        remaining = await session.scalar(
            select(func.count())
            .select_from(AdminRoleAssignment)
            .where(AdminRoleAssignment.role == "owner")
        )
        assert remaining == 1
    await engine.dispose()


@pytest.mark.asyncio
async def test_cli_legacy_revoke_preserves_explicit_privileged_roles(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    engine = create_async_engine(f"sqlite+aiosqlite:///{(tmp_path / 'cli-roles.db').as_posix()}")
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync_connection: Base.metadata.create_all(
                sync_connection,
                tables=[User.__table__, AdminRoleAssignment.__table__, AdminAuditLog.__table__],
            )
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    user = User(id=uuid4(), email="cli-owner@example.com", password_hash="unused", is_admin=True)
    async with factory() as session:
        session.add(user)
        await session.flush()
        session.add_all(
            [
                AdminRoleAssignment(user_id=user.id, role="owner", source="manual"),
                AdminRoleAssignment(user_id=user.id, role="database_operator", source="manual"),
                AdminRoleAssignment(user_id=user.id, role="support", source="legacy_backfill"),
                AdminRoleAssignment(user_id=user.id, role="content", source="legacy_backfill"),
                AdminRoleAssignment(user_id=user.id, role="operations", source="legacy_backfill"),
            ]
        )
        await session.commit()
    monkeypatch.setattr(app_cli, "SessionFactory", factory)
    monkeypatch.setattr(get_settings(), "admin_emails", "")

    try:
        await app_cli.set_admin(user.email, False)
        async with factory() as session:
            stored = await session.get(User, user.id)
            roles = set(
                (
                    await session.scalars(
                        select(AdminRoleAssignment.role).where(
                            AdminRoleAssignment.user_id == user.id
                        )
                    )
                ).all()
            )
            audit = await session.scalar(
                select(AdminAuditLog).where(AdminAuditLog.target == f"user:{user.id}")
            )
        assert stored is not None and stored.is_admin is True
        assert roles == {"owner", "database_operator"}
        assert audit is not None
        assert audit.metadata_json["roles_revoked"] == ["content", "operations", "support"]
    finally:
        await engine.dispose()


@pytest.mark.parametrize(
    ("method", "path", "capability"),
    [
        ("GET", "/api/v1/admin/dashboard", "dashboard.read"),
        ("GET", "/api/v1/admin/bootstrap", "admin.access"),
        ("GET", "/api/v1/admin/users", "users.read"),
        ("PUT", "/api/v1/admin/users/123", "users.manage"),
        ("POST", "/api/v1/admin/users/123/usage-adjustments", "usage.manage"),
        ("POST", "/api/v1/admin/catalog-review/runs", "content.manage"),
        ("GET", "/api/v1/admin/hotspots", "content.read"),
        ("PATCH", "/api/v1/admin/community/posts/123", "community.manage"),
        ("GET", "/api/v1/admin/analytics", "analytics.read"),
        ("PATCH", "/api/v1/admin/provider-settings", "settings.manage"),
        ("PATCH", "/api/v1/admin/system-settings", "settings.manage"),
        ("GET", "/api/v1/admin/layout-settings", "settings.read"),
        ("POST", "/api/v1/admin/partners", "settings.manage"),
        ("POST", "/api/v1/admin/database/backups", "database.maintain"),
        ("GET", "/api/v1/admin/deployments", "deploy.read"),
        ("POST", "/api/v1/admin/deployments", "deploy.execute"),
        ("POST", "/api/v1/admin/unknown-mutation", "roles.manage"),
        ("GET", "/api/v1/admin/unknown-read", "roles.manage"),
    ],
)
def test_existing_admin_paths_resolve_to_least_privilege_capability(
    method: str, path: str, capability: str
) -> None:
    assert _admin_path_capability(_request(path=path, method=method)) == capability


def test_status_filters_match_the_mutually_exclusive_response_status() -> None:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(
        engine,
        tables=[User.__table__, AccountErasureRequest.__table__],
    )
    now = datetime.now(UTC)
    users = {
        "active": User(email="active@example.com", password_hash="unused", is_active=True),
        "inactive": User(email="inactive@example.com", password_hash="unused", is_active=False),
        "suspended": User(
            email="suspended@example.com",
            password_hash="unused",
            is_active=True,
            suspended_at=now,
        ),
        "inactive_suspended": User(
            email="inactive-suspended@example.com",
            password_hash="unused",
            is_active=False,
            suspended_at=now,
        ),
        "erasure": User(
            email="erasure@example.com",
            password_hash="unused",
            is_active=False,
            suspended_at=now,
        ),
    }
    with Session(engine) as session:
        session.add_all(users.values())
        session.flush()
        session.add(
            AccountErasureRequest(
                user_id=users["erasure"].id,
                requested_by_user_id=None,
                idempotency_key="erasure-status-filter",
                status="scheduled",
                reason="狀態篩選測試",
                scheduled_for=now + timedelta(hours=24),
            )
        )
        session.commit()

        def matching(status: str) -> set[str]:
            filters = admin_users._list_filters(
                query=None,
                status=status,
                role=None,
                verified=None,
                auth_method=None,
                registered_from=None,
                registered_to=None,
            )
            return set(session.scalars(select(User.email).where(*filters)))

        assert matching("active") == {"active@example.com"}
        assert matching("inactive") == {
            "inactive@example.com",
            "inactive-suspended@example.com",
        }
        assert matching("suspended") == {"suspended@example.com"}
        assert matching("erasure_pending") == {"erasure@example.com"}
    engine.dispose()


def test_user_detail_audit_metadata_recursively_removes_secrets() -> None:
    item = AdminAuditLog(
        id=uuid4(),
        actor_user_id=None,
        action="legacy_provider_test",
        target="provider:legacy",
        metadata_json={
            "result": "ok",
            "access_token": "never expose",
            "nested": {
                "password_hash": "never expose either",
                "detail": "visible",
                "items": [{"client_secret": "hidden", "name": "kept"}],
            },
        },
        created_at=datetime.now(UTC),
    )
    value = admin_users._audit_item(item).metadata

    assert value == {
        "result": "ok",
        "nested": {"detail": "visible", "items": [{"name": "kept"}]},
    }


def test_deploy_and_database_mutations_require_role_allowlist_and_feature(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "deployments_enabled", True)
    monkeypatch.setattr(settings, "admin_database_maintenance_enabled", True)
    monkeypatch.setattr(settings, "deploy_agent_hmac_key", "x" * 32)
    monkeypatch.setattr(settings, "deploy_agent_socket", "/run/deployer.sock")
    monkeypatch.setattr(settings, "deploy_admin_emails", "operator@example.com")
    monkeypatch.setattr(settings, "database_admin_emails", "operator@example.com")
    user = User(email="operator@example.com", password_hash="unused", is_admin=True)

    assert can_deploy_user(user) is False
    assert can_deploy_user(user, roles={"deployer"}) is True
    assert can_database_maintain_user(user, roles={"operations"}) is False
    assert can_database_maintain_user(user, roles={"database_operator"}) is True


@pytest.mark.asyncio
async def test_step_up_is_bound_to_user_version_and_scope() -> None:
    user = User(
        id=uuid4(),
        email="owner@example.com",
        password_hash="unused",
        auth_version=4,
    )
    token, expires_at = create_admin_step_up_token(user, ["users.erase"])
    assert timedelta(seconds=295) <= expires_at - datetime.now(UTC) <= timedelta(seconds=300)
    await require_admin_step_up(_request(f"admin_step_up={token}"), user, "users.erase")
    with pytest.raises(AppError) as wrong_scope:
        await require_admin_step_up(_request(f"admin_step_up={token}"), user, "database.backup")
    assert wrong_scope.value.code == "admin_step_up_scope_required"
    user.auth_version += 1
    with pytest.raises(AppError) as stale:
        await require_admin_step_up(_request(f"admin_step_up={token}"), user, "users.erase")
    assert stale.value.code == "admin_step_up_invalid"


@pytest.mark.asyncio
async def test_expired_persisted_role_does_not_fall_back_to_legacy_is_admin() -> None:
    user = User(id=uuid4(), email="former-admin@example.com", password_hash="unused", is_admin=True)
    expired = AdminRoleAssignment(
        user_id=user.id,
        role="viewer",
        source="manual",
        expires_at=datetime.now(UTC) - timedelta(minutes=1),
    )
    session = AsyncMock(spec=AsyncSession)
    result = AsyncMock()
    result.all = Mock(return_value=[expired])
    session.scalars.return_value = result

    assert await effective_admin_capabilities(session, user) == set()
    assert is_admin_user(user) is False


@pytest.mark.asyncio
async def test_permanent_suspension_revokes_sessions_and_records_reason(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = User(id=uuid4(), email="support@example.com", password_hash="unused")
    target = User(
        id=uuid4(),
        email="member@example.com",
        password_hash="unused",
        auth_version=8,
        is_active=True,
    )
    session = AsyncMock(spec=AsyncSession)
    detail = AdminUserDetail.model_construct()
    monkeypatch.setattr(admin_users, "_user_and_account", AsyncMock(return_value=(target, None)))
    monkeypatch.setattr(admin_users, "_ensure_not_last_owner", AsyncMock())
    monkeypatch.setattr(admin_users, "_idempotency_replay", AsyncMock(return_value=False))
    monkeypatch.setattr(admin_users, "admin_user_detail", AsyncMock(return_value=detail))

    result = await admin_users.suspend_admin_user(
        session,
        target.id,
        AdminSuspensionRequest(reason="違反服務規範", confirmation=f"SUSPEND {target.email}"),
        actor,
        "suspend-key-123",
    )

    assert result.user is detail
    assert target.auth_version == 9
    assert target.suspended_at is not None
    assert target.suspended_until is None
    assert target.suspension_reason == "違反服務規範"
    assert any(
        isinstance(call.args[0], AdminAuditLog) and call.args[0].action == "user_suspended"
        for call in session.add.call_args_list
    )
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_timed_suspension_cannot_bypass_permanent_step_up_with_far_future_date(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = User(id=uuid4(), email="support@example.com", password_hash="unused")
    target = User(id=uuid4(), email="member@example.com", password_hash="unused")
    session = AsyncMock(spec=AsyncSession)
    monkeypatch.setattr(admin_users, "_user_and_account", AsyncMock(return_value=(target, None)))

    with pytest.raises(AppError) as caught:
        await admin_users.suspend_admin_user(
            session,
            target.id,
            AdminSuspensionRequest(
                reason="超長限時停權測試",
                suspended_until=datetime.now(UTC) + timedelta(days=91),
            ),
            actor,
            "far-future-suspension",
        )

    assert caught.value.code == "admin_suspension_time_too_far"
    assert target.suspended_at is None
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_admin_usage_ledger_does_not_duplicate_actor_email(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = User(id=uuid4(), email="support@example.com", password_hash="unused")
    target = User(id=uuid4(), email="member@example.com", password_hash="unused")
    account = UsageAccount(
        id=uuid4(),
        user_id=target.id,
        remaining_uses=5,
        reserved_uses=0,
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.return_value = None

    def assign_ledger_id(item: object) -> None:
        if isinstance(item, UsageLedger) and item.id is None:
            item.id = uuid4()

    session.add.side_effect = assign_ledger_id
    monkeypatch.setattr(
        admin_users,
        "_user_and_account",
        AsyncMock(return_value=(target, account)),
    )
    monkeypatch.setattr(
        admin_users,
        "admin_user_detail",
        AsyncMock(return_value=Mock(spec=AdminUserDetail)),
    )

    await admin_users.adjust_admin_user_usage(
        session,
        target.id,
        AdminUsageAdjustment(change=1, reason="客服補償"),
        actor,
        "usage-no-email",
    )

    ledger = next(
        call.args[0] for call in session.add.call_args_list if isinstance(call.args[0], UsageLedger)
    )
    assert ledger.metadata_json == {"actor_user_id": str(actor.id)}
    assert actor.email not in str(ledger.metadata_json)


@pytest.mark.asyncio
async def test_missing_environment_email_does_not_count_as_a_live_owner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "admin_emails", "missing-owner@example.com")
    target = User(id=uuid4(), email="db-owner@example.com", password_hash="unused")
    session = AsyncMock(spec=AsyncSession)
    session.scalar.side_effect = [None, None]
    monkeypatch.setattr(admin_users, "_active_roles", AsyncMock(return_value={"owner"}))

    with pytest.raises(AppError) as caught:
        await admin_users._ensure_not_last_owner(session, target)

    assert caught.value.code == "admin_last_owner"


@pytest.mark.asyncio
async def test_expiring_owner_does_not_count_as_a_durable_last_owner_recovery(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    engine = create_async_engine(f"sqlite+aiosqlite:///{(tmp_path / 'owner-expiry.db').as_posix()}")
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync_connection: Base.metadata.create_all(
                sync_connection,
                tables=[
                    User.__table__,
                    AdminRoleAssignment.__table__,
                    AccountErasureRequest.__table__,
                ],
            )
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    target = User(id=uuid4(), email="permanent-owner@example.com", password_hash="unused")
    temporary = User(id=uuid4(), email="temporary-owner@example.com", password_hash="unused")
    async with factory() as session:
        session.add_all([target, temporary])
        await session.flush()
        session.add_all(
            [
                AdminRoleAssignment(user_id=target.id, role="owner", source="manual"),
                AdminRoleAssignment(
                    user_id=temporary.id,
                    role="owner",
                    source="manual",
                    expires_at=datetime.now(UTC) + timedelta(hours=1),
                ),
            ]
        )
        await session.commit()
    monkeypatch.setattr(get_settings(), "admin_emails", "")

    try:
        async with factory() as session:
            with pytest.raises(AppError) as caught:
                await admin_users._ensure_not_last_owner(session, target)
        assert caught.value.code == "admin_last_owner"
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_owner_role_cannot_be_created_with_an_expiry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = User(id=uuid4(), email="actor@example.com", password_hash="unused")
    target = User(id=uuid4(), email="future-owner@example.com", password_hash="unused")
    session = AsyncMock(spec=AsyncSession)
    monkeypatch.setattr(
        admin_users,
        "_user_and_account",
        AsyncMock(return_value=(target, None)),
    )

    with pytest.raises(AppError) as caught:
        await admin_users._replace_admin_roles_serialized(
            session,
            target.id,
            AdminRolesUpdate(
                roles=["owner"],
                reason="臨時 owner 測試",
                confirmation=f"ROLES {target.email}",
                expires_at=datetime.now(UTC) + timedelta(hours=1),
            ),
            actor,
            "expiring-owner-key",
        )

    assert caught.value.code == "admin_owner_expiry_unsupported"
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_erasure_is_scheduled_for_24_hours_and_wakes_worker(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    target = User(id=uuid4(), email="member@example.com", password_hash="unused", is_active=True)
    session = AsyncMock(spec=AsyncSession)
    session.scalar.return_value = None
    detail = AdminUserDetail.model_construct()
    monkeypatch.setattr(admin_users, "_user_and_account", AsyncMock(return_value=(target, None)))
    monkeypatch.setattr(admin_users, "_ensure_not_last_owner", AsyncMock())
    monkeypatch.setattr(admin_users, "_idempotency_replay", AsyncMock(return_value=False))
    monkeypatch.setattr(admin_users, "admin_user_detail", AsyncMock(return_value=detail))
    wake = Mock(return_value=True)
    monkeypatch.setattr(admin_users, "enqueue_jobs", wake)
    before = datetime.now(UTC)

    result = await admin_users.schedule_admin_erasure(
        session,
        target.id,
        AdminErasureRequest(reason="會員提出合法清除要求", confirmation=f"ERASE {target.email}"),
        actor,
        "erasure-key-123",
    )

    assert result.user is detail
    added = [call.args[0] for call in session.add.call_args_list]
    erasure = next(item for item in added if isinstance(item, AccountErasureRequest))
    job = next(item for item in added if isinstance(item, Job))
    assert (
        timedelta(hours=23, minutes=59)
        < erasure.scheduled_for - before
        < timedelta(hours=24, seconds=1)
    )
    assert job.kind == "admin_erase_account"
    session.commit.assert_awaited_once()
    wake.assert_called_once()


@pytest.mark.asyncio
async def test_scheduled_erasure_worker_commits_barrier_and_queues_delayed_scrub(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = User(
        id=uuid4(),
        email="member@example.com",
        password_hash="unused",
        is_admin=True,
        last_login_at=datetime.now(UTC),
        suspended_at=datetime.now(UTC),
        suspension_reason="先前停權",
    )
    request = AccountErasureRequest(
        id=uuid4(),
        user_id=target.id,
        requested_by_user_id=uuid4(),
        idempotency_key="erasure-key-123",
        status="scheduled",
        reason="合法清除要求",
        scheduled_for=datetime.now(UTC) - timedelta(minutes=1),
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.side_effect = [target, request, None]
    erase = AsyncMock()
    monkeypatch.setattr(community_jobs, "erase_account", erase)
    monkeypatch.setattr(admin_users, "_environment_designated", Mock(return_value=False))
    monkeypatch.setattr(admin_users, "_ensure_not_last_owner", AsyncMock())

    await community_jobs.erase_scheduled_admin_account(session, target.id)

    assert target.is_active is False
    assert target.deleted_at is not None
    assert target.auth_version == 2
    assert target.is_admin is False
    assert target.last_login_at is None
    assert target.suspended_at is None
    assert target.suspended_until is None
    assert target.suspension_reason is None
    assert request.status == "processing"
    assert request.completed_at is None
    erase.assert_not_awaited()
    finalize = next(
        call.args[0]
        for call in session.add.call_args_list
        if isinstance(call.args[0], Job) and call.args[0].kind == "admin_erasure_finalize"
    )
    assert finalize.available_at >= target.deleted_at + timedelta(minutes=5)
    session.commit.assert_awaited_once()
    locked = [str(call.args[0]) for call in session.scalar.await_args_list[:2]]
    assert "FROM users" in locked[0] and "FOR UPDATE" in locked[0]
    assert "FROM account_erasure_requests" in locked[1] and "FOR UPDATE" in locked[1]


@pytest.mark.asyncio
async def test_admin_erasure_finalize_scrubs_then_records_deidentified_audit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = User(
        id=uuid4(),
        email="member@example.com",
        password_hash=None,
        is_active=False,
        deleted_at=datetime.now(UTC),
    )
    request = AccountErasureRequest(
        id=uuid4(),
        user_id=target.id,
        requested_by_user_id=uuid4(),
        idempotency_key="erasure-key-finalize",
        status="processing",
        reason="合法清除要求",
        scheduled_for=datetime.now(UTC) - timedelta(minutes=2),
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.side_effect = [target, request]
    session.get.return_value = None
    erase = AsyncMock()
    monkeypatch.setattr(community_jobs, "erase_account", erase)

    await community_jobs.finalize_admin_erasure(session, target.id)

    erase.assert_awaited_once_with(session, target.id)
    assert request.status == "completed"
    assert request.completed_at is not None
    audit = next(
        call.args[0]
        for call in session.add.call_args_list
        if isinstance(call.args[0], AdminAuditLog)
    )
    assert audit.target == "user:erased"
    assert str(target.id) not in str(audit.metadata_json)
    locked = [str(call.args[0]) for call in session.scalar.await_args_list]
    assert "FROM users" in locked[0] and "FOR UPDATE" in locked[0]
    assert "FROM account_erasure_requests" in locked[1] and "FOR UPDATE" in locked[1]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("job_kind", "request_status", "handler_name", "phase"),
    [
        ("admin_erase_account", "scheduled", "erase_scheduled_admin_account", "deactivate"),
        ("admin_erasure_finalize", "processing", "finalize_admin_erasure", "scrub"),
    ],
)
async def test_erasure_retry_exhaustion_records_terminal_failure_audit(
    monkeypatch: pytest.MonkeyPatch,
    job_kind: str,
    request_status: str,
    handler_name: str,
    phase: str,
) -> None:
    user_id = uuid4()
    row = Job(
        id=uuid4(),
        kind=job_kind,
        user_id=user_id,
        status="pending",
        attempts=4,
        available_at=datetime.now(UTC),
        created_at=datetime.now(UTC),
    )
    request = AccountErasureRequest(
        id=uuid4(),
        user_id=user_id,
        requested_by_user_id=uuid4(),
        idempotency_key=f"failure-{job_kind}",
        status=request_status,
        reason="清除要求",
        scheduled_for=datetime.now(UTC),
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.side_effect = [row, request, None]
    empty = Mock()
    empty.all.return_value = []
    session.scalars.return_value = empty

    @asynccontextmanager
    async def factory():
        yield session

    monkeypatch.setattr(community_jobs, "SessionFactory", factory)
    monkeypatch.setattr(
        community_jobs,
        handler_name,
        AsyncMock(side_effect=RuntimeError("provider token=private")),
    )

    await community_jobs.drain_jobs()

    assert row.status == "failed" and row.attempts == 5
    assert request.status == "failed"
    audit = next(
        call.args[0]
        for call in session.add.call_args_list
        if isinstance(call.args[0], AdminAuditLog) and call.args[0].action == "user_erasure_failed"
    )
    assert audit.metadata_json == {
        "result": "failed",
        "failure_code": "erasure_worker_failed",
        "phase": phase,
    }
    assert "private" not in str(audit.metadata_json)


@pytest.mark.asyncio
async def test_cancel_erasure_uses_the_same_user_then_request_lock_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    target = User(id=uuid4(), email="member@example.com", password_hash="unused")
    request = AccountErasureRequest(
        id=uuid4(),
        user_id=target.id,
        requested_by_user_id=actor.id,
        idempotency_key="erasure-key-cancel",
        status="scheduled",
        reason="合法清除要求",
        scheduled_for=datetime.now(UTC) + timedelta(hours=23),
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.side_effect = [target, None, request]
    scalar_rows = Mock()
    scalar_rows.all.return_value = []
    session.scalars.return_value = scalar_rows
    monkeypatch.setattr(
        admin_users,
        "admin_user_detail",
        AsyncMock(return_value=AdminUserDetail.model_construct()),
    )

    await admin_users.cancel_admin_erasure(
        session,
        target.id,
        AdminReasonRequest(reason="會員撤回清除要求"),
        actor,
    )

    statements = [str(call.args[0]) for call in session.scalar.await_args_list]
    assert "FROM users" in statements[0] and "FOR UPDATE" in statements[0]
    assert "FROM usage_accounts" in statements[1]
    assert "FROM account_erasure_requests" in statements[2] and "FOR UPDATE" in statements[2]
    assert request.status == "cancelled"


@pytest.mark.asyncio
async def test_admin_verification_resend_is_one_locked_transaction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = User(id=uuid4(), email="support@example.com", password_hash="unused")
    target = User(id=uuid4(), email="member@example.com", password_hash="unused", is_active=True)
    session = AsyncMock(spec=AsyncSession)
    session.scalar.side_effect = [target, None, None]
    send = AsyncMock()
    wake = Mock(return_value=True)
    monkeypatch.setattr(admin_users, "request_mail", send)
    monkeypatch.setattr(admin_users, "enqueue_jobs", wake)
    monkeypatch.setattr(admin_users, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(
        admin_users,
        "admin_user_detail",
        AsyncMock(return_value=Mock(spec=AdminUserDetail)),
    )

    await admin_users.resend_admin_verification(session, target.id, actor)

    send.assert_awaited_once_with(
        session,
        target,
        "verify",
        target.preferred_locale,
        commit=False,
        enqueue=False,
    )
    statements = [str(call.args[0]) for call in session.scalar.await_args_list]
    assert "FROM users" in statements[0] and "FOR UPDATE" in statements[0]
    assert "FROM account_erasure_requests" in statements[2] and "FOR UPDATE" in statements[2]
    session.commit.assert_awaited_once()
    wake.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("deleted", [False, True])
async def test_admin_verification_resend_rejects_inactive_or_deleted_accounts(
    monkeypatch: pytest.MonkeyPatch,
    deleted: bool,
) -> None:
    actor = User(id=uuid4(), email="support@example.com", password_hash="unused")
    target = User(
        id=uuid4(),
        email="member@example.com",
        password_hash="unused",
        is_active=deleted,
        deleted_at=datetime.now(UTC) if deleted else None,
    )
    if not deleted:
        target.is_active = False
    session = AsyncMock(spec=AsyncSession)
    session.scalar.side_effect = [target, None]
    send = AsyncMock()
    monkeypatch.setattr(admin_users, "request_mail", send)
    monkeypatch.setattr(admin_users, "enforce_named_rate_limit", AsyncMock())

    with pytest.raises(AppError) as caught:
        await admin_users.resend_admin_verification(session, target.id, actor)

    assert caught.value.code == "admin_user_inactive"
    send.assert_not_awaited()
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_account_erasure_removes_administrator_identity_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = User(
        id=uuid4(),
        email="former-owner@example.com",
        password_hash="unused",
        is_active=False,
        is_admin=True,
        deleted_at=datetime.now(UTC),
        last_login_at=datetime.now(UTC),
        suspended_at=datetime.now(UTC),
        suspension_reason="先前停權",
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.return_value = target
    scalar_rows = Mock()
    scalar_rows.all.return_value = []
    session.scalars.return_value = scalar_rows
    session.get.return_value = None
    monkeypatch.setattr("app.community.invitations.erase_creator_invitation", AsyncMock())
    monkeypatch.setattr("app.discovery.preferences.erase_preferences", AsyncMock())

    await community_jobs.erase_account(session, target.id)

    assert target.email.endswith("@deleted.invalid")
    assert target.password_hash is None
    assert target.is_admin is False
    assert target.last_login_at is None
    assert target.suspended_at is None
    assert target.suspended_until is None
    assert target.suspension_reason is None
    statements = [str(call.args[0]) for call in session.execute.await_args_list]
    assert any("DELETE FROM admin_role_assignments" in statement for statement in statements)


@pytest.mark.asyncio
async def test_scheduled_erasure_rechecks_environment_protection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = User(id=uuid4(), email="new-owner@example.com", password_hash="unused", is_active=True)
    request = AccountErasureRequest(
        id=uuid4(),
        user_id=target.id,
        requested_by_user_id=uuid4(),
        idempotency_key="erasure-key-456",
        status="scheduled",
        reason="先前提出的清除要求",
        scheduled_for=datetime.now(UTC) - timedelta(minutes=1),
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.side_effect = [target, request]
    erase = AsyncMock()
    monkeypatch.setattr(community_jobs, "erase_account", erase)
    monkeypatch.setattr(get_settings(), "admin_emails", target.email)

    await community_jobs.erase_scheduled_admin_account(session, target.id)

    assert request.status == "failed"
    assert request.failure_code == "erasure_protected_environment_admin"
    assert target.is_active is True
    erase.assert_not_awaited()


@pytest.mark.asyncio
async def test_scheduled_erasure_rechecks_last_owner_after_role_changes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = User(
        id=uuid4(),
        email="promoted-owner@example.com",
        password_hash="unused",
        is_active=True,
    )
    request = AccountErasureRequest(
        id=uuid4(),
        user_id=target.id,
        requested_by_user_id=uuid4(),
        idempotency_key="erasure-key-promoted-owner",
        status="scheduled",
        reason="先前提出的清除要求",
        scheduled_for=datetime.now(UTC) - timedelta(minutes=1),
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.side_effect = [target, request]
    erase = AsyncMock()
    monkeypatch.setattr(community_jobs, "erase_account", erase)
    monkeypatch.setattr(admin_users, "_environment_designated", Mock(return_value=False))
    monkeypatch.setattr(
        admin_users,
        "_ensure_not_last_owner",
        AsyncMock(side_effect=AppError(409, "admin_last_owner", "最後一位 owner")),
    )

    await community_jobs.erase_scheduled_admin_account(session, target.id)

    assert request.status == "failed"
    assert request.failure_code == "erasure_last_owner"
    assert target.is_active is True
    erase.assert_not_awaited()
