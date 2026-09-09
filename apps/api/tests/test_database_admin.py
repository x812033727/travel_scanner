import asyncio
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Literal, cast
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
import sqlalchemy as sa
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.admin.operations_service import list_audit_logs
from app.auth.service import create_admin_step_up_token, current_user
from app.config import get_settings
from app.database_admin import service as database_service
from app.database_admin.agent import DatabaseAgentClient
from app.database_admin.router import router
from app.database_admin.schemas import (
    AgentDatabaseCreateResponse,
    AgentDatabaseJob,
    AgentDatabaseOverview,
    AgentVerifiedBackup,
    DatabaseOperationView,
    DatabaseOverview,
)
from app.database_admin.service import (
    _database_backup_catalog,
    _lock_reconcilable_operation,
    _reconcile,
    _terminalize_operation_failure,
    create_database_operation,
    database_overview,
    database_tables,
)
from app.db import Base, get_session
from app.models import AdminAuditLog, DatabaseOperationRun, DeploymentRun, User
from app.problems import AppError, app_error_handler


class MappingResult:
    def __init__(
        self,
        *,
        one: dict[str, Any] | None = None,
        all: list[dict[str, Any]] | None = None,
    ):
        self._one = one
        self._all = all or []

    def mappings(self) -> "MappingResult":
        return self

    def one(self) -> dict[str, Any]:
        assert self._one is not None
        return self._one

    def all(self) -> list[dict[str, Any]]:
        return self._all


@pytest.mark.asyncio
async def test_database_overview_maps_one_fixed_postgres_snapshot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = AsyncMock(spec=AsyncSession)
    session.scalar.return_value = None
    scalar_rows = Mock()
    scalar_rows.all.return_value = []
    session.scalars.return_value = scalar_rows
    session.execute.return_value = MappingResult(
        one={
            "version": "17.6",
            "database_size_bytes": 10_000,
            "maximum": 100,
            "active": 2,
            "idle": 4,
            "waiting": 1,
            "long_transactions": 0,
            "lock_waits": 1,
            "cache_hit_ratio": 99.95,
            "current_revision": "0068_admin_operations_center",
        }
    )
    monkeypatch.setattr(
        DatabaseAgentClient,
        "overview",
        AsyncMock(
            return_value=AgentDatabaseOverview(
                connected=True,
                available=True,
                release_sha="a" * 40,
            )
        ),
    )

    snapshot = await database_overview(cast(AsyncSession, session))

    assert snapshot.status == "ok"
    assert snapshot.postgres is not None
    assert snapshot.postgres.connections.waiting == 1
    assert snapshot.postgres.cache_hit_ratio == 99.95
    assert snapshot.schema_info is not None and snapshot.schema_info.is_current is True
    assert snapshot.model_dump(by_alias=True)["schema"]["current_revision"] == (
        "0068_admin_operations_center"
    )
    sql = str(session.execute.await_args.args[0])
    assert "pg_stat_activity" in sql
    assert "pg_stat_database" in sql


@pytest.mark.asyncio
async def test_database_overview_recovers_from_optional_metrics_failure_with_active_operation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    engine = create_async_engine(f"sqlite+aiosqlite:///{(tmp_path / 'overview.db').as_posix()}")
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync_connection: Base.metadata.create_all(
                sync_connection,
                tables=[User.__table__, DatabaseOperationRun.__table__],
            )
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    requester = User(id=uuid4(), email="database-operator@example.com", password_hash="unused")
    operation = DatabaseOperationRun(
        id=uuid4(),
        requested_by_user_id=requester.id,
        idempotency_key="active-analyze",
        operation_type="analyze",
        status="queued",
        metadata_json={},
    )
    async with factory() as session:
        session.add_all([requester, operation])
        await session.commit()
    monkeypatch.setattr(
        DatabaseAgentClient,
        "overview",
        AsyncMock(return_value=AgentDatabaseOverview(connected=False, available=False)),
    )

    try:
        async with factory() as session:
            snapshot = await database_overview(session)
        assert snapshot.status == "unavailable"
        assert snapshot.active_operation is not None
        assert snapshot.active_operation.id == operation.id
        assert snapshot.active_operation.requested_by_email == requester.email
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_backup_catalog_includes_verified_deployment_backup() -> None:
    verified_at = datetime.now(UTC)
    deployment_id = uuid4()
    requester = User(id=uuid4(), email="deployer@example.com", password_hash="unused")
    deployment = DeploymentRun(
        id=deployment_id,
        requested_by_user_id=requester.id,
        idempotency_key="deployment-catalog-test",
        status="succeeded",
        stage="succeeded",
        target_sha="b" * 40,
        backup_name="deployment.dump",
        metadata_json={},
        created_at=verified_at,
        updated_at=verified_at,
    )
    manual = DatabaseOperationRun(
        id=uuid4(),
        requested_by_user_id=None,
        idempotency_key="manual-catalog-test",
        operation_type="backup",
        status="succeeded",
        backup_name="manual.dump",
        checksum_sha256="c" * 64,
        size_bytes=2048,
        schema_revision="0068_admin_operations_center",
        release_sha="a" * 40,
        finished_at=verified_at - timedelta(minutes=1),
        metadata_json={},
        created_at=verified_at - timedelta(minutes=1),
        updated_at=verified_at - timedelta(minutes=1),
    )
    agent = AgentDatabaseOverview(
        connected=True,
        available=True,
        backups=[
            AgentVerifiedBackup(
                backup_name="deployment.dump",
                checksum_sha256="a" * 64,
                size_bytes=4096,
                schema_revision="0068_admin_operations_center",
                release_sha="b" * 40,
                source="deployment",
                source_job_id=deployment_id,
                verified_at=verified_at,
            ),
            AgentVerifiedBackup(
                backup_name="deployment-retry-older.dump",
                checksum_sha256="d" * 64,
                size_bytes=1024,
                schema_revision="0068_admin_operations_center",
                release_sha="b" * 40,
                source="deployment",
                source_job_id=deployment_id,
                verified_at=verified_at - timedelta(minutes=2),
            ),
        ],
    )
    session = AsyncMock(spec=AsyncSession)
    scalar_rows = Mock()
    scalar_rows.all.return_value = [manual]
    session.scalars.return_value = scalar_rows
    session.get.side_effect = [deployment, requester]

    items = await _database_backup_catalog(
        cast(AsyncSession, session), agent, limit=50
    )

    assert len(items) == 2
    assert items[0].id == deployment_id
    assert items[0].source == "deployment"
    assert items[0].verified is True
    assert items[0].requested_by_email == "deployer@example.com"
    assert items[0].checksum_sha256 == "a" * 64
    assert items[1].source == "manual"
    assert items[1].verified is True


@pytest.mark.asyncio
async def test_backup_catalog_does_not_claim_unproven_success() -> None:
    observed = datetime.now(UTC)
    unproven = DatabaseOperationRun(
        id=uuid4(),
        requested_by_user_id=None,
        idempotency_key="legacy-unproven-success",
        operation_type="backup",
        status="succeeded",
        backup_name="unproven.dump",
        metadata_json={},
        created_at=observed,
        updated_at=observed,
    )
    session = AsyncMock(spec=AsyncSession)
    scalar_rows = Mock()
    scalar_rows.all.return_value = [unproven]
    session.scalars.return_value = scalar_rows

    items = await _database_backup_catalog(
        cast(AsyncSession, session),
        AgentDatabaseOverview(connected=False, available=False),
        limit=50,
    )

    assert items == []


@pytest.mark.asyncio
async def test_database_overview_reports_actual_latest_verified_backup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = datetime.now(UTC)
    older = operation_view()
    older.status = "succeeded"
    older.verified = True
    older.finished_at = now - timedelta(days=1)
    latest = operation_view()
    latest.status = "succeeded"
    latest.verified = True
    latest.source = "deployment"
    latest.finished_at = now
    session = AsyncMock(spec=AsyncSession)
    session.scalar.return_value = None
    session.execute.return_value = MappingResult(
        one={
            "version": "17.6",
            "database_size_bytes": 10_000,
            "maximum": 100,
            "active": 1,
            "idle": 1,
            "waiting": 0,
            "long_transactions": 0,
            "lock_waits": 0,
            "cache_hit_ratio": 99.9,
            "current_revision": "0068_admin_operations_center",
        }
    )
    monkeypatch.setattr(
        database_service,
        "_agent_overview",
        AsyncMock(
            return_value=AgentDatabaseOverview(connected=True, available=True)
        ),
    )
    monkeypatch.setattr(
        database_service,
        "_database_backup_catalog",
        AsyncMock(return_value=[latest, older]),
    )

    result = await database_overview(cast(AsyncSession, session))

    assert result.last_backup is not None
    assert result.last_backup.id == latest.id
    assert result.last_backup.source == "deployment"
    assert result.last_backup.verified is True


@pytest.mark.asyncio
async def test_database_table_statistics_are_public_schema_metadata_only() -> None:
    observed = datetime.now(UTC)
    session = AsyncMock(spec=AsyncSession)
    session.execute.return_value = MappingResult(
        all=[
            {
                "name": "users",
                "estimated_rows": 42,
                "data_bytes": 2048,
                "index_bytes": 1024,
                "total_bytes": 3072,
                "dead_rows": 3,
                "last_vacuum": None,
                "last_autovacuum": observed,
                "last_analyze": None,
                "last_autoanalyze": observed,
            }
        ]
    )

    result = await database_tables(cast(AsyncSession, session))

    assert result.items[0].name == "users"
    assert result.items[0].total_bytes == 3072
    sql = str(session.execute.await_args.args[0])
    assert "pg_stat_user_tables" in sql
    assert "schemaname = 'public'" in sql
    assert "SELECT *" not in sql.upper()


def operation_view(
    operation_type: Literal["backup", "analyze"] = "backup",
) -> DatabaseOperationView:
    now = datetime.now(UTC)
    return DatabaseOperationView(
        id=uuid4(),
        requested_by_email="database@example.com",
        operation_type=operation_type,
        status="queued",
        agent_job_id=str(uuid4()),
        created_at=now,
        updated_at=now,
    )


@pytest.mark.asyncio
async def test_idempotent_database_operation_replays_before_agent_or_feature_checks() -> None:
    now = datetime.now(UTC)
    actor = User(
        id=uuid4(),
        email="database@example.com",
        password_hash="unused",
    )
    replay = DatabaseOperationRun(
        id=uuid4(),
        requested_by_user_id=actor.id,
        idempotency_key="same-request-key",
        operation_type="backup",
        status="succeeded",
        agent_job_id=str(uuid4()),
        backup_name="verified.dump",
        checksum_sha256="a" * 64,
        size_bytes=123,
        schema_revision="0068_admin_operations_center",
        release_sha="b" * 40,
        metadata_json={},
        created_at=now,
        updated_at=now,
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.return_value = replay
    session.get.return_value = actor

    result = await create_database_operation(
        cast(AsyncSession, session),
        actor,
        "backup",
        "BACKUP",
        "same-request-key",
    )

    assert result.id == replay.id
    assert result.backup_name == "verified.dump"
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_database_idempotency_race_rejects_a_different_operation_type(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "admin_database_maintenance_enabled", True)
    actor = User(id=uuid4(), email="database@example.com", password_hash="unused")
    concurrent = DatabaseOperationRun(
        id=uuid4(),
        requested_by_user_id=actor.id,
        idempotency_key="cross-type-race",
        operation_type="backup",
        status="queued",
        metadata_json={},
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.side_effect = [None, None, None, concurrent]
    session.commit.side_effect = IntegrityError("INSERT", {}, Exception("unique"))
    monkeypatch.setattr(
        DatabaseAgentClient,
        "overview",
        AsyncMock(return_value=AgentDatabaseOverview(connected=True, available=True)),
    )

    with pytest.raises(AppError) as caught:
        await create_database_operation(
            cast(AsyncSession, session),
            actor,
            "analyze",
            "ANALYZE",
            "cross-type-race",
        )

    assert caught.value.code == "idempotency_key_reused"
    session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_database_operation_reports_agent_unavailable_without_queueing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = get_settings()
    original = settings.admin_database_maintenance_enabled
    settings.admin_database_maintenance_enabled = True
    actor = User(id=uuid4(), email="database@example.com", password_hash="unused")
    session = AsyncMock(spec=AsyncSession)
    session.scalar.side_effect = [None, None, None]
    monkeypatch.setattr(
        DatabaseAgentClient,
        "overview",
        AsyncMock(
            side_effect=AppError(
                503, "database_agent_unavailable", "agent unavailable"
            )
        ),
    )
    try:
        with pytest.raises(AppError) as caught:
            await create_database_operation(
                cast(AsyncSession, session),
                actor,
                "backup",
                "BACKUP",
                "unavailable-request",
            )
    finally:
        settings.admin_database_maintenance_enabled = original
    assert caught.value.code == "database_agent_unavailable"
    session.add.assert_not_called()


@pytest.mark.asyncio
async def test_database_job_id_mismatch_terminalizes_the_active_operation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "admin_database_maintenance_enabled", True)
    actor = User(id=uuid4(), email="database@example.com", password_hash="unused")
    session = AsyncMock(spec=AsyncSession)

    def scalar_result(_statement: Any) -> DatabaseOperationRun | None:
        if session.scalar.await_count <= 3:
            return None
        return next(
            call.args[0]
            for call in session.add.call_args_list
            if isinstance(call.args[0], DatabaseOperationRun)
        )

    session.scalar.side_effect = scalar_result
    monkeypatch.setattr(
        DatabaseAgentClient,
        "overview",
        AsyncMock(return_value=AgentDatabaseOverview(connected=True, available=True)),
    )
    monkeypatch.setattr(
        DatabaseAgentClient,
        "create",
        AsyncMock(
            return_value=AgentDatabaseCreateResponse(job_id=str(uuid4()), status="running")
        ),
    )

    with pytest.raises(AppError) as caught:
        await create_database_operation(
            cast(AsyncSession, session),
            actor,
            "backup",
            "BACKUP",
            "database-invalid-agent-job",
        )

    operation = next(
        call.args[0]
        for call in session.add.call_args_list
        if isinstance(call.args[0], DatabaseOperationRun)
    )
    audits = [
        call.args[0]
        for call in session.add.call_args_list
        if isinstance(call.args[0], AdminAuditLog)
    ]
    assert caught.value.code == "database_agent_invalid_response"
    assert operation.status == "failed"
    assert operation.failure_code == "database_agent_invalid_response"
    assert operation.finished_at is not None
    assert operation.metadata_json.get("terminal_audited") is True
    assert any(
        audit.action == "database.operation.failed"
        and audit.metadata_json.get("failure_code") == "database_agent_invalid_response"
        for audit in audits
    )
    assert session.commit.await_count == 2


@pytest.mark.asyncio
async def test_stale_create_ack_does_not_regress_a_terminal_operation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "admin_database_maintenance_enabled", True)
    actor = User(id=uuid4(), email="database@example.com", password_hash="unused")
    now = datetime.now(UTC)
    session = AsyncMock(spec=AsyncSession)

    def scalar_result(_statement: Any) -> DatabaseOperationRun | None:
        if session.scalar.await_count <= 3:
            return None
        operation = next(
            call.args[0]
            for call in session.add.call_args_list
            if isinstance(call.args[0], DatabaseOperationRun)
        )
        operation.status = "succeeded"
        operation.metadata_json = {"terminal_audited": True}
        operation.created_at = now
        operation.updated_at = now
        return operation

    async def create_job(
        _client: DatabaseAgentClient, run_id: str, _action: str
    ) -> AgentDatabaseCreateResponse:
        return AgentDatabaseCreateResponse(job_id=run_id, status="running")

    session.scalar.side_effect = scalar_result
    session.get.return_value = actor
    monkeypatch.setattr(
        DatabaseAgentClient,
        "overview",
        AsyncMock(return_value=AgentDatabaseOverview(connected=True, available=True)),
    )
    monkeypatch.setattr(DatabaseAgentClient, "create", create_job)

    result = await create_database_operation(
        cast(AsyncSession, session),
        actor,
        "analyze",
        "ANALYZE",
        "stale-create-ack",
    )

    assert result.status == "succeeded"
    assert session.commit.await_count == 1
    lock_statement = session.scalar.await_args.args[0]
    assert lock_statement._for_update_arg is not None  # noqa: SLF001
    assert lock_statement.get_execution_options()["populate_existing"] is True


@pytest.mark.asyncio
async def test_agent_cannot_report_backup_success_without_verification_proof(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = datetime.now(UTC)
    operation = DatabaseOperationRun(
        id=uuid4(),
        requested_by_user_id=None,
        idempotency_key="agent-missing-proof",
        operation_type="backup",
        status="running",
        agent_job_id=str(uuid4()),
        metadata_json={},
        created_at=now,
        updated_at=now,
    )
    monkeypatch.setattr(
        DatabaseAgentClient,
        "job",
        AsyncMock(
            return_value=AgentDatabaseJob(
                job_id=operation.agent_job_id,
                action="backup",
                status="succeeded",
                backup_name="claimed-but-unverified.dump",
                created_at=now,
            )
        ),
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.return_value = operation

    result = await _reconcile(cast(AsyncSession, session), operation)

    assert result.status == "failed"
    assert result.failure_code == "database_backup_verification_missing"
    assert result.finished_at is not None
    assert any(
        isinstance(call.args[0], AdminAuditLog)
        and call.args[0].action == "database.operation.failed"
        for call in session.add.call_args_list
    )


@pytest.mark.asyncio
async def test_missing_agent_job_terminalizes_the_locked_current_snapshot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    operation = DatabaseOperationRun(
        id=uuid4(),
        requested_by_user_id=None,
        idempotency_key="agent-lost-job",
        operation_type="analyze",
        status="running",
        agent_job_id=str(uuid4()),
        metadata_json={},
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.return_value = operation
    monkeypatch.setattr(
        DatabaseAgentClient,
        "job",
        AsyncMock(
            side_effect=AppError(
                404, "database_operation_not_found", "agent no longer has the job"
            )
        ),
    )

    result = await _reconcile(cast(AsyncSession, session), operation)

    assert result.status == "failed"
    assert result.failure_code == "database_agent_lost_job"
    assert result.metadata_json.get("terminal_audited") is True
    audit = next(
        call.args[0]
        for call in session.add.call_args_list
        if isinstance(call.args[0], AdminAuditLog)
    )
    assert audit.action == "database.operation.failed"
    assert session.scalar.await_args.args[0]._for_update_arg is not None  # noqa: SLF001


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status", "job_matches", "terminal_audited", "expected"),
    [
        ("running", True, False, True),
        ("succeeded", True, True, False),
        ("running", False, False, False),
        ("running", True, True, False),
    ],
)
async def test_reconcile_lock_rechecks_the_current_database_snapshot(
    status: str,
    job_matches: bool,
    terminal_audited: bool,
    expected: bool,
) -> None:
    operation_id = uuid4()
    expected_job_id = str(operation_id)
    stale = DatabaseOperationRun(
        id=operation_id,
        requested_by_user_id=None,
        idempotency_key="stale-reconcile",
        operation_type="analyze",
        status="running",
        agent_job_id=expected_job_id,
        metadata_json={},
    )
    current = DatabaseOperationRun(
        id=operation_id,
        requested_by_user_id=None,
        idempotency_key="current-reconcile",
        operation_type="analyze",
        status=status,
        agent_job_id=expected_job_id if job_matches else str(uuid4()),
        metadata_json={"terminal_audited": terminal_audited},
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.return_value = current

    locked, can_reconcile = await _lock_reconcilable_operation(
        cast(AsyncSession, session),
        stale,
        expected_agent_job_id=expected_job_id,
    )

    assert locked is current
    assert can_reconcile is expected
    statement = session.scalar.await_args.args[0]
    assert statement._for_update_arg is not None  # noqa: SLF001
    assert statement.get_execution_options()["populate_existing"] is True


@pytest.mark.asyncio
async def test_reconcile_calls_the_agent_before_locking_and_does_not_regress_terminal_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = datetime.now(UTC)
    operation_id = uuid4()
    job_id = str(operation_id)
    stale = DatabaseOperationRun(
        id=operation_id,
        requested_by_user_id=None,
        idempotency_key="stale-terminal-reconcile",
        operation_type="analyze",
        status="running",
        agent_job_id=job_id,
        metadata_json={},
    )
    current = DatabaseOperationRun(
        id=operation_id,
        requested_by_user_id=None,
        idempotency_key="current-terminal-reconcile",
        operation_type="analyze",
        status="succeeded",
        agent_job_id=job_id,
        metadata_json={"terminal_audited": True},
    )
    order: list[str] = []

    async def agent_job(_client: DatabaseAgentClient, _job_id: str) -> AgentDatabaseJob:
        order.append("agent")
        return AgentDatabaseJob(
            job_id=job_id,
            action="analyze",
            status="failed",
            failure_code="stale-agent-result",
            created_at=now,
        )

    session = AsyncMock(spec=AsyncSession)

    async def locked_row(_statement: Any) -> DatabaseOperationRun:
        order.append("lock")
        return current

    session.scalar.side_effect = locked_row
    monkeypatch.setattr(DatabaseAgentClient, "job", agent_job)

    result = await _reconcile(cast(AsyncSession, session), stale)

    assert order == ["agent", "lock"]
    assert result is current
    assert result.status == "succeeded"
    session.add.assert_not_called()
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_failure_terminalizer_does_not_overwrite_a_locked_terminal_operation() -> None:
    operation_id = uuid4()
    job_id = str(operation_id)
    stale = DatabaseOperationRun(
        id=operation_id,
        requested_by_user_id=None,
        idempotency_key="stale-failure-terminalizer",
        operation_type="analyze",
        status="running",
        agent_job_id=job_id,
        metadata_json={},
    )
    current = DatabaseOperationRun(
        id=operation_id,
        requested_by_user_id=None,
        idempotency_key="current-failure-terminalizer",
        operation_type="analyze",
        status="succeeded",
        agent_job_id=job_id,
        metadata_json={"terminal_audited": True},
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.return_value = current

    result = await _terminalize_operation_failure(
        cast(AsyncSession, session),
        stale,
        failure_code="stale-failure",
        failure_detail="must not replace the committed result",
    )

    assert result is current
    assert result.status == "succeeded"
    session.add.assert_not_called()
    session.commit.assert_not_awaited()


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.asyncio
async def test_postgresql_concurrent_reconcile_records_one_terminal_audit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    schema = "database_reconcile_" + uuid4().hex
    administrator = create_async_engine(get_settings().database_url)
    engine = create_async_engine(
        get_settings().database_url,
        connect_args={"server_settings": {"search_path": schema}},
    )
    operation_id = uuid4()
    now = datetime.now(UTC)
    job = AgentDatabaseJob(
        job_id=str(operation_id),
        action="backup",
        status="succeeded",
        backup_name="concurrent.dump",
        checksum_sha256="a" * 64,
        size_bytes=4096,
        schema_revision="0068_admin_operations_center",
        release_sha="b" * 40,
        started_at=now,
        finished_at=now,
        created_at=now,
    )
    agent_call_count = 0
    both_agent_calls = asyncio.Event()

    async def terminal_job(_client: DatabaseAgentClient, job_id: str) -> AgentDatabaseJob:
        nonlocal agent_call_count
        assert job_id == str(operation_id)
        agent_call_count += 1
        if agent_call_count == 2:
            both_agent_calls.set()
        try:
            await asyncio.wait_for(both_agent_calls.wait(), timeout=0.25)
        except TimeoutError:
            pass
        return job

    monkeypatch.setattr(DatabaseAgentClient, "job", terminal_job)

    try:
        async with administrator.begin() as connection:
            await connection.execute(sa.text(f'CREATE SCHEMA "{schema}"'))
        async with engine.begin() as connection:
            await connection.run_sync(
                lambda sync_connection: Base.metadata.create_all(
                    sync_connection,
                    tables=[
                        User.__table__,
                        AdminAuditLog.__table__,
                        DatabaseOperationRun.__table__,
                    ],
                )
            )
        factory = async_sessionmaker(engine, expire_on_commit=False)
        async with factory() as session:
            session.add(
                DatabaseOperationRun(
                    id=operation_id,
                    requested_by_user_id=None,
                    idempotency_key=f"concurrent-terminal-{operation_id}",
                    operation_type="backup",
                    status="running",
                    agent_job_id=str(operation_id),
                    metadata_json={},
                    created_at=now,
                    updated_at=now,
                )
            )
            await session.commit()

        loaded_count = 0
        both_loaded = asyncio.Event()
        loaded_guard = asyncio.Lock()

        async def reconcile_once() -> DatabaseOperationRun:
            nonlocal loaded_count
            async with factory() as session:
                operation = await session.get(DatabaseOperationRun, operation_id)
                assert operation is not None
                async with loaded_guard:
                    loaded_count += 1
                    if loaded_count == 2:
                        both_loaded.set()
                await asyncio.wait_for(both_loaded.wait(), timeout=5)
                return await _reconcile(session, operation)

        results = await asyncio.wait_for(
            asyncio.gather(reconcile_once(), reconcile_once()), timeout=10
        )

        assert [result.status for result in results] == ["succeeded", "succeeded"]
        assert agent_call_count == 2
        async with factory() as session:
            operation = await session.get(DatabaseOperationRun, operation_id)
            audit_count = await session.scalar(
                sa.select(sa.func.count())
                .select_from(AdminAuditLog)
                .where(
                    AdminAuditLog.target == str(operation_id),
                    AdminAuditLog.action.in_(
                        ["database.operation.succeeded", "database.operation.failed"]
                    ),
                )
            )
        assert operation is not None
        assert operation.status == "succeeded"
        assert operation.metadata_json.get("terminal_audited") is True
        assert audit_count == 1
    finally:
        await engine.dispose()
        async with administrator.begin() as connection:
            await connection.execute(sa.text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
        await administrator.dispose()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status", "code"),
    [
        (401, "database_agent_unauthorized"),
        (409, "database_agent_busy"),
        (502, "database_agent_rejected"),
    ],
)
async def test_database_agent_rejections_are_terminal_failed_and_auditable(
    monkeypatch: pytest.MonkeyPatch,
    status: int,
    code: str,
) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "admin_database_maintenance_enabled", True)
    actor = User(id=uuid4(), email="database@example.com", password_hash="unused")
    session = AsyncMock(spec=AsyncSession)

    def scalar_result(_statement: Any) -> DatabaseOperationRun | None:
        if session.scalar.await_count <= 3:
            return None
        return next(
            call.args[0]
            for call in session.add.call_args_list
            if isinstance(call.args[0], DatabaseOperationRun)
        )

    session.scalar.side_effect = scalar_result
    monkeypatch.setattr(
        DatabaseAgentClient,
        "overview",
        AsyncMock(return_value=AgentDatabaseOverview(connected=True, available=True)),
    )
    monkeypatch.setattr(
        DatabaseAgentClient,
        "create",
        AsyncMock(side_effect=AppError(status, code, "agent rejected password=private")),
    )

    with pytest.raises(AppError) as caught:
        await create_database_operation(
            cast(AsyncSession, session),
            actor,
            "analyze",
            "ANALYZE",
            f"agent-rejected-{status}",
        )

    operation = next(
        call.args[0]
        for call in session.add.call_args_list
        if isinstance(call.args[0], DatabaseOperationRun)
    )
    audit = next(
        call.args[0]
        for call in session.add.call_args_list
        if isinstance(call.args[0], AdminAuditLog)
        and call.args[0].action == "database.operation.failed"
    )
    audit.id = uuid4()
    assert caught.value.code == code
    assert operation.status == "failed"
    assert operation.failure_code == code
    assert operation.failure_detail == "agent rejected password=***"
    assert operation.finished_at is not None
    assert operation.metadata_json.get("terminal_audited") is True
    assert audit.metadata_json["result"] == "failed"
    assert session.commit.await_count == 2

    audit.created_at = datetime.now(UTC)
    audit_session = AsyncMock(spec=AsyncSession)
    audit_session.scalar.return_value = 1
    rows = Mock()
    rows.all.return_value = [(audit, actor.email)]
    audit_session.execute.return_value = rows
    page = await list_audit_logs(
        cast(AsyncSession, audit_session),
        actor=None,
        action=None,
        target=None,
        result="failed",
        date_from=None,
        date_to=None,
        page=1,
        limit=20,
    )
    assert len(page.items) == 1
    assert page.items[0].result == "failed"


@pytest.mark.asyncio
async def test_database_router_enforces_capability_allowlist_and_step_up(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import app.database_admin.router as database_router

    settings = get_settings()
    original = (
        settings.admin_database_maintenance_enabled,
        settings.database_admin_emails,
    )
    settings.admin_database_maintenance_enabled = True
    settings.database_admin_emails = "database@example.com"
    session = AsyncMock(spec=AsyncSession)
    user_holder = {
        "user": User(
            id=uuid4(),
            email="database@example.com",
            password_hash="unused",
            auth_version=0,
        )
    }
    user_holder["user"]._admin_roles_cache = frozenset(  # type: ignore[attr-defined]
        {"database_operator"}
    )

    async def override_user() -> User:
        return user_holder["user"]

    async def override_session() -> Any:
        yield session

    application = FastAPI()
    application.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    application.include_router(router, prefix="/api/v1")
    application.dependency_overrides[current_user] = override_user
    application.dependency_overrides[get_session] = override_session
    snapshot = DatabaseOverview(
        status="unavailable",
        checked_at=datetime.now(UTC),
        agent=AgentDatabaseOverview(connected=False, available=False),
        maintenance_enabled=True,
        unavailable_reason="fixture",
    )
    overview_mock = AsyncMock(return_value=snapshot)
    create_mock = AsyncMock(return_value=operation_view())
    monkeypatch.setattr(database_router, "database_overview", overview_mock)
    monkeypatch.setattr(database_router, "create_database_operation", create_mock)
    monkeypatch.setattr(database_router, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(
        database_router, "effective_admin_roles", AsyncMock(return_value={"database_operator"})
    )

    try:
        async with AsyncClient(
            transport=ASGITransport(app=application), base_url="http://test"
        ) as client:
            readable = await client.get("/api/v1/admin/database/overview")
            assert readable.status_code == 200
            assert readable.json()["status"] == "unavailable"

            no_step_up = await client.post(
                "/api/v1/admin/database/backups",
                headers={"Idempotency-Key": "backup-without-stepup"},
                json={"confirmation": "BACKUP"},
            )
            assert no_step_up.status_code == 401
            assert no_step_up.json()["code"] == "admin_step_up_required"

            token, _ = create_admin_step_up_token(
                user_holder["user"], ["database.backup"]
            )
            client.cookies.set("admin_step_up", token, path="/api/v1/admin")
            accepted = await client.post(
                "/api/v1/admin/database/backups",
                headers={"Idempotency-Key": "backup-with-stepup"},
                json={"confirmation": "BACKUP"},
            )
            assert accepted.status_code == 202
            create_mock.assert_awaited_once()

            settings.database_admin_emails = "someone-else@example.com"
            rejected = await client.post(
                "/api/v1/admin/database/backups",
                headers={"Idempotency-Key": "backup-not-allowlisted"},
                json={"confirmation": "BACKUP"},
            )
            assert rejected.status_code == 403
            assert rejected.json()["code"] == "database_operator_required"

            support = User(
                id=uuid4(), email="support@example.com", password_hash="unused"
            )
            support._admin_roles_cache = frozenset({"support"})  # type: ignore[attr-defined]
            user_holder["user"] = support
            forbidden_read = await client.get("/api/v1/admin/database/overview")
            assert forbidden_read.status_code == 403
            assert forbidden_read.json()["code"] == "admin_capability_required"
    finally:
        (
            settings.admin_database_maintenance_enabled,
            settings.database_admin_emails,
        ) = original
