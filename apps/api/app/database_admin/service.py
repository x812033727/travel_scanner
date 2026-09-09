import re
from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.audit_safety import safe_audit_metadata
from app.config import get_settings
from app.database_admin.agent import DatabaseAgentClient
from app.database_admin.schemas import (
    AgentDatabaseJob,
    AgentDatabaseOverview,
    AgentVerifiedBackup,
    DatabaseConnections,
    DatabaseOperationList,
    DatabaseOperationType,
    DatabaseOperationView,
    DatabaseOverview,
    DatabaseSchemaSnapshot,
    DatabaseTableList,
    DatabaseTableSnapshot,
    PostgreSQLSnapshot,
)
from app.models import (
    ACTIVE_DATABASE_OPERATION_STATUSES,
    ACTIVE_DEPLOYMENT_STATUSES,
    AdminAuditLog,
    DatabaseOperationRun,
    DeploymentRun,
    User,
)
from app.problems import AppError
from app.schema import expected_schema_revision


def _safe_text(value: str | None, limit: int = 500) -> str | None:
    if value is None:
        return None
    redacted = safe_audit_metadata(value)
    cleaned = " ".join(str(redacted).replace("\x00", "").split())
    return cleaned[:limit] or None


def _operation_has_verified_backup(operation: DatabaseOperationRun) -> bool:
    return bool(
        operation.operation_type == "backup"
        and operation.status == "succeeded"
        and operation.backup_name
        and operation.checksum_sha256
        and re.fullmatch(r"[0-9a-f]{64}", operation.checksum_sha256)
        and operation.size_bytes
        and operation.size_bytes > 0
        and operation.schema_revision
        and operation.release_sha
        and re.fullmatch(r"[0-9a-f]{40}", operation.release_sha)
    )


def _agent_job_has_verified_backup(job: AgentDatabaseJob) -> bool:
    return bool(
        job.action == "backup"
        and job.status == "succeeded"
        and job.backup_name
        and job.checksum_sha256
        and re.fullmatch(r"[0-9a-f]{64}", job.checksum_sha256)
        and job.size_bytes
        and job.size_bytes > 0
        and job.schema_revision
        and job.release_sha
        and re.fullmatch(r"[0-9a-f]{40}", job.release_sha)
    )


async def _terminalize_operation_failure(
    session: AsyncSession,
    operation: DatabaseOperationRun,
    *,
    failure_code: str,
    failure_detail: str | None,
) -> DatabaseOperationRun:
    expected_agent_job_id = operation.agent_job_id
    operation, can_reconcile = await _lock_reconcilable_operation(
        session,
        operation,
        expected_agent_job_id=expected_agent_job_id,
    )
    if not can_reconcile:
        return operation
    operation.status = "failed"
    operation.failure_code = _safe_text(failure_code, 64)
    operation.failure_detail = _safe_text(failure_detail)
    operation.finished_at = datetime.now(UTC)
    metadata = dict(operation.metadata_json or {})
    if not metadata.get("terminal_audited"):
        metadata["terminal_audited"] = True
        session.add(
            AdminAuditLog(
                actor_user_id=operation.requested_by_user_id,
                action="database.operation.failed",
                target=str(operation.id),
                metadata_json={
                    "operation_type": operation.operation_type,
                    "result": "failed",
                    "failure_code": operation.failure_code,
                },
            )
        )
    operation.metadata_json = metadata
    await session.commit()
    return operation


async def _lock_reconcilable_operation(
    session: AsyncSession,
    operation: DatabaseOperationRun,
    *,
    expected_agent_job_id: str | None,
) -> tuple[DatabaseOperationRun, bool]:
    current = await session.scalar(
        select(DatabaseOperationRun)
        .where(DatabaseOperationRun.id == operation.id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if current is None:
        return operation, False
    metadata = current.metadata_json or {}
    return current, bool(
        current.status in ACTIVE_DATABASE_OPERATION_STATUSES
        and current.agent_job_id == expected_agent_job_id
        and not metadata.get("terminal_audited")
    )


async def _operation_view(
    session: AsyncSession, operation: DatabaseOperationRun
) -> DatabaseOperationView:
    requester = (
        await session.get(User, operation.requested_by_user_id)
        if operation.requested_by_user_id
        else None
    )
    raw_events = (operation.metadata_json or {}).get("events", [])
    return DatabaseOperationView(
        id=operation.id,
        requested_by_email=requester.email if requester else None,
        operation_type=operation.operation_type,
        status=operation.status,
        agent_job_id=operation.agent_job_id,
        backup_name=operation.backup_name,
        checksum_sha256=operation.checksum_sha256,
        size_bytes=operation.size_bytes,
        schema_revision=operation.schema_revision,
        release_sha=operation.release_sha,
        failure_code=operation.failure_code,
        failure_detail=operation.failure_detail,
        started_at=operation.started_at,
        finished_at=operation.finished_at,
        created_at=operation.created_at,
        updated_at=operation.updated_at,
        events=raw_events if isinstance(raw_events, list) else [],
        source="manual",
        verified=_operation_has_verified_backup(operation),
    )


async def _agent_backup_view(
    session: AsyncSession, backup: AgentVerifiedBackup
) -> DatabaseOperationView | None:
    if backup.source_job_id is None:
        # A deployment backup is attached to its immutable job id immediately
        # after verification. Do not invent an id for an incomplete catalog row.
        return None
    requester: User | None = None
    if backup.source == "manual":
        operation = await session.get(DatabaseOperationRun, backup.source_job_id)
        if operation and operation.requested_by_user_id:
            requester = await session.get(User, operation.requested_by_user_id)
    else:
        deployment = await session.get(DeploymentRun, backup.source_job_id)
        if deployment and deployment.requested_by_user_id:
            requester = await session.get(User, deployment.requested_by_user_id)
    return DatabaseOperationView(
        id=backup.source_job_id,
        requested_by_email=requester.email if requester else None,
        operation_type="backup",
        status="succeeded",
        agent_job_id=str(backup.source_job_id),
        backup_name=backup.backup_name,
        checksum_sha256=backup.checksum_sha256,
        size_bytes=backup.size_bytes,
        schema_revision=backup.schema_revision,
        release_sha=backup.release_sha,
        started_at=backup.verified_at,
        finished_at=backup.verified_at,
        created_at=backup.verified_at,
        updated_at=backup.verified_at,
        source=backup.source,
        verified=True,
    )


async def _database_backup_catalog(
    session: AsyncSession,
    agent: AgentDatabaseOverview,
    *,
    limit: int,
) -> list[DatabaseOperationView]:
    operations = list(
        (
            await session.scalars(
                select(DatabaseOperationRun)
                .where(DatabaseOperationRun.operation_type == "backup")
                .order_by(DatabaseOperationRun.created_at.desc())
                .limit(limit)
            )
        ).all()
    )
    for operation in operations:
        if operation.status in ACTIVE_DATABASE_OPERATION_STATUSES and agent.connected:
            try:
                await _reconcile(session, operation)
            except AppError as exc:
                if exc.code != "database_agent_unavailable":
                    raise

    # Keep failed/in-progress attempts for diagnosis, but a terminal success is
    # visible only when checksum, size, schema and release prove verification.
    merged: dict[tuple[str, UUID], DatabaseOperationView] = {}
    for operation in operations:
        if operation.status == "succeeded" and not _operation_has_verified_backup(operation):
            continue
        merged[("manual", operation.id)] = await _operation_view(session, operation)

    live_keys: set[tuple[str, UUID]] = set()
    for backup in sorted(agent.backups, key=lambda item: item.verified_at, reverse=True):
        if backup.source_job_id is None:
            continue
        key = (backup.source, backup.source_job_id)
        if key in live_keys:
            continue
        view = await _agent_backup_view(session, backup)
        if view is not None:
            merged[key] = view
            live_keys.add(key)

    return sorted(
        merged.values(),
        key=lambda item: item.finished_at or item.updated_at,
        reverse=True,
    )[:limit]


async def _reconcile(
    session: AsyncSession, operation: DatabaseOperationRun
) -> DatabaseOperationRun:
    if (
        not operation.agent_job_id
        or operation.status not in ACTIVE_DATABASE_OPERATION_STATUSES
    ):
        return operation
    expected_agent_job_id = operation.agent_job_id
    try:
        job = await DatabaseAgentClient().job(expected_agent_job_id)
    except AppError as exc:
        if exc.code != "database_operation_not_found":
            raise
        return await _terminalize_operation_failure(
            session,
            operation,
            failure_code="database_agent_lost_job",
            failure_detail="資料庫維運代理恢復連線後找不到這筆工作",
        )

    if (
        operation.operation_type == "backup"
        and job.status == "succeeded"
        and not _agent_job_has_verified_backup(job)
    ):
        return await _terminalize_operation_failure(
            session,
            operation,
            failure_code="database_backup_verification_missing",
            failure_detail="維運代理未提供完整的備份驗證資料",
        )

    operation, can_reconcile = await _lock_reconcilable_operation(
        session,
        operation,
        expected_agent_job_id=expected_agent_job_id,
    )
    if not can_reconcile:
        return operation

    previous_status = operation.status
    operation.status = job.status
    operation.backup_name = _safe_text(job.backup_name, 255)
    operation.checksum_sha256 = _safe_text(job.checksum_sha256, 64)
    operation.size_bytes = job.size_bytes
    operation.schema_revision = _safe_text(job.schema_revision, 64)
    operation.release_sha = _safe_text(job.release_sha, 40)
    operation.failure_code = _safe_text(job.failure_code, 64)
    operation.failure_detail = _safe_text(job.failure_detail)
    operation.started_at = job.started_at
    operation.finished_at = job.finished_at
    metadata = dict(operation.metadata_json or {})
    metadata["events"] = [event.model_dump(mode="json") for event in job.events]
    terminal = job.status not in ACTIVE_DATABASE_OPERATION_STATUSES
    if terminal and not metadata.get("terminal_audited"):
        metadata["terminal_audited"] = True
        session.add(
            AdminAuditLog(
                actor_user_id=operation.requested_by_user_id,
                action=(
                    "database.operation.succeeded"
                    if job.status == "succeeded"
                    else "database.operation.failed"
                ),
                target=str(operation.id),
                metadata_json={
                    "operation_type": operation.operation_type,
                    "status": job.status,
                    "backup_name": operation.backup_name,
                    "size_bytes": operation.size_bytes,
                    "schema_revision": operation.schema_revision,
                    "release_sha": operation.release_sha,
                },
            )
        )
    operation.metadata_json = metadata
    if previous_status != operation.status or job.events:
        await session.commit()
    return operation


async def _agent_overview() -> AgentDatabaseOverview:
    try:
        return await DatabaseAgentClient().overview()
    except AppError as exc:
        if exc.code != "database_agent_unavailable":
            raise
        return AgentDatabaseOverview(connected=False, available=False)


async def database_overview(session: AsyncSession) -> DatabaseOverview:
    agent = await _agent_overview()
    active = await session.scalar(
        select(DatabaseOperationRun)
        .where(DatabaseOperationRun.status.in_(ACTIVE_DATABASE_OPERATION_STATUSES))
        .order_by(DatabaseOperationRun.created_at.desc())
        .limit(1)
    )
    if active is not None:
        try:
            active = await _reconcile(session, active)
        except AppError as exc:
            if exc.code != "database_agent_unavailable":
                raise
    backup_catalog = await _database_backup_catalog(session, agent, limit=50)
    last_backup = next((item for item in backup_catalog if item.verified), None)
    settings = get_settings()
    maintenance_enabled = bool(
        getattr(settings, "admin_database_maintenance_enabled", False)
    )
    try:
        # Operational statistics are optional. Keep their permission/runtime
        # failure inside a savepoint so PostgreSQL does not poison the request
        # transaction before we serialize an active maintenance operation.
        async with session.begin_nested():
            row = (
                await session.execute(
                    text(
                        """
                    SELECT
                      current_setting('server_version') AS version,
                      pg_database_size(current_database())::bigint AS database_size_bytes,
                      current_setting('max_connections')::int AS maximum,
                      (SELECT count(*)::int FROM pg_stat_activity
                        WHERE datname=current_database() AND state='active'
                          AND pid <> pg_backend_pid()) AS active,
                      (SELECT count(*)::int FROM pg_stat_activity
                        WHERE datname=current_database() AND state='idle') AS idle,
                      (SELECT count(*)::int FROM pg_stat_activity
                        WHERE datname=current_database() AND state='active'
                          AND wait_event IS NOT NULL) AS waiting,
                      (SELECT count(*)::int FROM pg_stat_activity
                        WHERE datname=current_database() AND xact_start IS NOT NULL
                          AND xact_start < now() - interval '5 minutes'
                          AND pid <> pg_backend_pid()) AS long_transactions,
                      (SELECT count(*)::int FROM pg_stat_activity
                        WHERE datname=current_database() AND wait_event_type='Lock') AS lock_waits,
                      (SELECT CASE WHEN blks_hit + blks_read = 0 THEN NULL
                         ELSE round(100.0 * blks_hit / (blks_hit + blks_read), 2) END
                       FROM pg_stat_database WHERE datname=current_database()) AS cache_hit_ratio,
                      (SELECT version_num FROM alembic_version LIMIT 1) AS current_revision
                        """
                    )
                )
            ).mappings().one()
    except SQLAlchemyError:
        return DatabaseOverview(
            status="unavailable",
            checked_at=datetime.now(UTC),
            agent=agent,
            maintenance_enabled=maintenance_enabled,
            last_backup=last_backup,
            active_operation=(await _operation_view(session, active)) if active else None,
            unavailable_reason="無法讀取 PostgreSQL 營運統計",
        )
    expected = expected_schema_revision()
    current = str(row["current_revision"]) if row["current_revision"] else None
    return DatabaseOverview(
        status="ok",
        checked_at=datetime.now(UTC),
        postgres=PostgreSQLSnapshot(
            version=str(row["version"]),
            database_size_bytes=int(row["database_size_bytes"]),
            connections=DatabaseConnections(
                active=int(row["active"]),
                idle=int(row["idle"]),
                waiting=int(row["waiting"]),
                maximum=int(row["maximum"]),
            ),
            long_transactions=int(row["long_transactions"]),
            lock_waits=int(row["lock_waits"]),
            cache_hit_ratio=(
                float(row["cache_hit_ratio"])
                if row["cache_hit_ratio"] is not None
                else None
            ),
        ),
        schema_info=DatabaseSchemaSnapshot(
            current_revision=current,
            expected_revision=expected,
            is_current=current == expected,
        ),
        agent=agent,
        maintenance_enabled=maintenance_enabled,
        last_backup=last_backup,
        active_operation=(
            await _operation_view(session, active)
            if active and active.status in ACTIVE_DATABASE_OPERATION_STATUSES
            else None
        ),
    )


async def database_tables(session: AsyncSession) -> DatabaseTableList:
    try:
        rows = (
            await session.execute(
                text(
                    """
                    SELECT
                      relname AS name,
                      COALESCE(n_live_tup, 0)::bigint AS estimated_rows,
                      pg_relation_size(relid)::bigint AS data_bytes,
                      pg_indexes_size(relid)::bigint AS index_bytes,
                      pg_total_relation_size(relid)::bigint AS total_bytes,
                      COALESCE(n_dead_tup, 0)::bigint AS dead_rows,
                      last_vacuum, last_autovacuum, last_analyze, last_autoanalyze
                    FROM pg_stat_user_tables
                    WHERE schemaname = 'public'
                    ORDER BY pg_total_relation_size(relid) DESC, relname ASC
                    """
                )
            )
        ).mappings().all()
    except SQLAlchemyError as exc:
        raise AppError(
            503, "database_statistics_unavailable", "目前無法讀取資料表統計"
        ) from exc
    return DatabaseTableList(
        items=[
            DatabaseTableSnapshot(
                name=str(row["name"]),
                estimated_rows=int(row["estimated_rows"]),
                data_bytes=int(row["data_bytes"]),
                index_bytes=int(row["index_bytes"]),
                total_bytes=int(row["total_bytes"]),
                dead_rows=int(row["dead_rows"]),
                last_vacuum=row["last_vacuum"],
                last_autovacuum=row["last_autovacuum"],
                last_analyze=row["last_analyze"],
                last_autoanalyze=row["last_autoanalyze"],
            )
            for row in rows
        ]
    )


async def list_database_operations(
    session: AsyncSession,
    *,
    operation_type: DatabaseOperationType | None = None,
    limit: int = 50,
) -> DatabaseOperationList:
    if operation_type == "backup":
        agent = await _agent_overview()
        return DatabaseOperationList(
            items=await _database_backup_catalog(session, agent, limit=limit)
        )
    statement = select(DatabaseOperationRun).order_by(
        DatabaseOperationRun.created_at.desc()
    )
    if operation_type:
        statement = statement.where(
            DatabaseOperationRun.operation_type == operation_type
        )
    operations = list((await session.scalars(statement.limit(limit))).all())
    for operation in operations:
        if operation.status in ACTIVE_DATABASE_OPERATION_STATUSES:
            try:
                await _reconcile(session, operation)
            except AppError as exc:
                if exc.code != "database_agent_unavailable":
                    raise
    return DatabaseOperationList(
        items=[await _operation_view(session, operation) for operation in operations]
    )


async def database_operation_detail(
    session: AsyncSession, operation_id: UUID
) -> DatabaseOperationView:
    operation = await session.get(DatabaseOperationRun, operation_id)
    if operation is None:
        raise AppError(404, "database_operation_not_found", "找不到這筆資料庫工作")
    if operation.status in ACTIVE_DATABASE_OPERATION_STATUSES:
        try:
            operation = await _reconcile(session, operation)
        except AppError as exc:
            if exc.code != "database_agent_unavailable":
                raise
    return await _operation_view(session, operation)


async def create_database_operation(
    session: AsyncSession,
    actor: User,
    operation_type: DatabaseOperationType,
    confirmation: str,
    idempotency_key: str,
) -> DatabaseOperationView:
    replay = await session.scalar(
        select(DatabaseOperationRun).where(
            DatabaseOperationRun.requested_by_user_id == actor.id,
            DatabaseOperationRun.idempotency_key == idempotency_key,
        )
    )
    if replay is not None:
        if replay.operation_type != operation_type:
            raise AppError(
                409,
                "idempotency_key_reused",
                "這個 Idempotency-Key 已用於另一種資料庫操作",
            )
        return await _operation_view(session, replay)

    settings = get_settings()
    if not bool(getattr(settings, "admin_database_maintenance_enabled", False)):
        raise AppError(503, "database_maintenance_disabled", "資料庫維護功能目前未啟用")
    expected_confirmation = "BACKUP" if operation_type == "backup" else "ANALYZE"
    if confirmation != expected_confirmation:
        raise AppError(422, "database_confirmation_invalid", "資料庫操作確認文字不正確")
    if await session.scalar(
        select(DatabaseOperationRun.id).where(
            DatabaseOperationRun.status.in_(ACTIVE_DATABASE_OPERATION_STATUSES)
        )
    ):
        raise AppError(409, "database_operation_in_progress", "目前已有資料庫工作正在執行")
    if await session.scalar(
        select(DeploymentRun.id).where(
            DeploymentRun.status.in_(ACTIVE_DEPLOYMENT_STATUSES)
        )
    ):
        raise AppError(409, "database_operation_in_progress", "部署期間不能執行資料庫維護")
    agent = await DatabaseAgentClient().overview()
    if not agent.available:
        raise AppError(503, "database_agent_unavailable", "資料庫維運代理尚未就緒")

    operation = DatabaseOperationRun(
        id=uuid4(),
        requested_by_user_id=actor.id,
        idempotency_key=idempotency_key,
        operation_type=operation_type,
        status="queued",
        metadata_json={},
    )
    operation.agent_job_id = str(operation.id)
    session.add(operation)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="database.operation.requested",
            target=str(operation.id),
            metadata_json={"operation_type": operation_type},
        )
    )
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        concurrent_replay = await session.scalar(
            select(DatabaseOperationRun).where(
                DatabaseOperationRun.requested_by_user_id == actor.id,
                DatabaseOperationRun.idempotency_key == idempotency_key,
            )
        )
        if concurrent_replay is not None:
            if concurrent_replay.operation_type != operation_type:
                raise AppError(
                    409,
                    "idempotency_key_reused",
                    "這個 Idempotency-Key 已用於另一種資料庫操作",
                ) from exc
            return await _operation_view(session, concurrent_replay)
        raise AppError(
            409, "database_operation_in_progress", "目前已有系統維運工作正在執行"
        ) from exc

    try:
        created = await DatabaseAgentClient().create(str(operation.id), operation_type)
    except AppError as exc:
        if exc.code == "database_agent_unavailable":
            operation, can_reconcile = await _lock_reconcilable_operation(
                session,
                operation,
                expected_agent_job_id=str(operation.id),
            )
            if can_reconcile:
                operation.failure_code = "database_agent_ack_pending"
                operation.failure_detail = "尚未收到維運代理確認；恢復連線後可重新同步"
                await session.commit()
            raise
        await _terminalize_operation_failure(
            session,
            operation,
            failure_code=exc.code,
            failure_detail=exc.detail,
        )
        raise
    if created.job_id != str(operation.id):
        await _terminalize_operation_failure(
            session,
            operation,
            failure_code="database_agent_invalid_response",
            failure_detail="資料庫維運代理回傳了不相符的工作識別碼",
        )
        raise AppError(502, "database_agent_invalid_response", "資料庫工作識別碼不正確")
    # A very small database can finish before the agent's 202 response is read. Keep
    # the API record active long enough to fetch the authoritative job payload; copying
    # only the terminal status here would permanently lose checksum/size/schema data.
    operation, can_reconcile = await _lock_reconcilable_operation(
        session,
        operation,
        expected_agent_job_id=str(operation.id),
    )
    if not can_reconcile:
        return await _operation_view(session, operation)
    operation.status = (
        created.status
        if created.status in ACTIVE_DATABASE_OPERATION_STATUSES
        else "running"
    )
    await session.commit()
    if created.status not in ACTIVE_DATABASE_OPERATION_STATUSES:
        operation = await _reconcile(session, operation)
    return await _operation_view(session, operation)
