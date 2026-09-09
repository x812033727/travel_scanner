import asyncio
import importlib.util
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import asyncpg
import pytest
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import make_url

from app.config import get_settings


def _migration():
    path = Path(__file__).parents[1] / "migrations/versions/0068_admin_operations_center.py"
    spec = importlib.util.spec_from_file_location("admin_operations_migration", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _connection_kwargs(database: str) -> dict[str, object]:
    url = make_url(get_settings().database_url)
    return {
        "host": url.host or "127.0.0.1",
        "port": url.port or 5432,
        "user": url.username,
        "password": url.password,
        "database": database,
    }


async def _run_alembic(database: str, revision: str) -> None:
    database_url = make_url(get_settings().database_url).set(database=database)
    environment = {
        **os.environ,
        "DATABASE_URL": database_url.render_as_string(hide_password=False),
    }
    await asyncio.to_thread(
        subprocess.run,
        [sys.executable, "-m", "alembic", "upgrade", revision],
        cwd=Path(__file__).parents[1],
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )


def test_admin_operations_migration_backfills_legacy_roles_and_is_idempotent(
    monkeypatch,
) -> None:
    migration = _migration()
    monkeypatch.setattr(migration.context, "is_offline_mode", lambda: False)
    engine = sa.create_engine("sqlite://")
    legacy = sa.MetaData()
    users = sa.Table(
        "users",
        legacy,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
    )
    owner_id, member_id = uuid4(), uuid4()

    with engine.begin() as connection:
        legacy.create_all(connection)
        connection.execute(
            users.insert(),
            [
                {"id": owner_id, "email": "legacy@example.com", "is_admin": True},
                {"id": member_id, "email": "member@example.com", "is_admin": False},
            ],
        )
        with Operations.context(MigrationContext.configure(connection)):
            migration.upgrade()
            migration.upgrade()

            inspector = sa.inspect(connection)
            assert {
                "admin_role_assignments",
                "database_operation_runs",
                "account_erasure_requests",
            } <= set(inspector.get_table_names())
            assert {
                "last_login_at",
                "suspended_at",
                "suspended_until",
                "suspension_reason",
            } <= {column["name"] for column in inspector.get_columns("users")}

            roles = sa.Table("admin_role_assignments", sa.MetaData(), autoload_with=connection)
            assert set(
                connection.scalars(sa.select(roles.c.role).where(roles.c.user_id == owner_id))
            ) == {"support", "content", "operations"}
            assert (
                connection.scalar(
                    sa.select(sa.func.count())
                    .select_from(roles)
                    .where(roles.c.user_id == member_id)
                )
                == 0
            )

            now = datetime.now(UTC)
            connection.execute(
                sa.text(
                    """INSERT INTO database_operation_runs
                    (id, requested_by_user_id, idempotency_key, operation_type, status,
                     metadata_json, created_at, updated_at)
                    VALUES (:id, :user_id, :key, 'backup', 'queued', '{}', :now, :now)"""
                ),
                {
                    "id": uuid4().hex,
                    "user_id": owner_id.hex,
                    "key": "first-operation",
                    "now": now.isoformat(),
                },
            )
            # The active-operation index is global, not merely per requester.
            nested = connection.begin_nested()
            try:
                with pytest.raises(sa.exc.IntegrityError):
                    connection.execute(
                        sa.text(
                            """INSERT INTO database_operation_runs
                            (id, requested_by_user_id, idempotency_key, operation_type, status,
                             metadata_json, created_at, updated_at)
                            VALUES (:id, :user_id, :key, 'analyze', 'running', '{}', :now, :now)"""
                        ),
                        {
                            "id": uuid4().hex,
                            "user_id": member_id.hex,
                            "key": "second-operation",
                            "now": now.isoformat(),
                        },
                    )
            finally:
                nested.rollback()

            migration.downgrade()
            assert "admin_role_assignments" not in sa.inspect(connection).get_table_names()
    engine.dispose()


@pytest.mark.skipif(
    os.getenv("RUN_MIGRATION_TESTS") != "1",
    reason="requires PostgreSQL database-creation privileges",
)
@pytest.mark.asyncio
async def test_postgresql_seeded_0067_upgrade_scrubs_pii_and_installs_guards() -> None:
    """Exercise the real PostgreSQL-only privacy path from the previous revision."""

    database = f"travel_scanner_admin_ops_{uuid4().hex[:12]}"
    admin = await asyncpg.connect(**_connection_kwargs("postgres"))
    try:
        await admin.execute(f'CREATE DATABASE "{database}"')
        await _run_alembic(database, "0067_collection_inbox")

        legacy = await asyncpg.connect(**_connection_kwargs(database))
        owner_id, member_id = uuid4(), uuid4()
        account_id, ledger_id, click_id = uuid4(), uuid4(), uuid4()
        try:
            # 0001 intentionally creates from current metadata so a brand-new
            # database remains installable. Remove 0068's additive objects to
            # accurately reproduce a database that was already at 0067.
            await legacy.execute(
                """
                DROP TABLE IF EXISTS account_erasure_requests CASCADE;
                DROP TABLE IF EXISTS database_operation_runs CASCADE;
                DROP TABLE IF EXISTS admin_role_assignments CASCADE;
                ALTER TABLE users DROP COLUMN IF EXISTS suspension_reason;
                ALTER TABLE users DROP COLUMN IF EXISTS suspended_until;
                ALTER TABLE users DROP COLUMN IF EXISTS suspended_at;
                ALTER TABLE users DROP COLUMN IF EXISTS last_login_at;
                """
            )
            await legacy.executemany(
                """
                INSERT INTO users
                    (id, email, password_hash, is_active, is_admin, auth_version,
                     preferred_locale, preferred_currency, created_at, updated_at)
                VALUES ($1, $2, 'hash', true, $3, 1, 'zh-TW', 'TWD', now(), now())
                """,
                [
                    (owner_id, "legacy-admin@example.com", True),
                    (member_id, "legacy-member@example.com", False),
                ],
            )
            await legacy.execute(
                """
                INSERT INTO usage_accounts
                    (id, user_id, remaining_uses, reserved_uses, status, created_at, updated_at)
                VALUES ($1, $2, 3, 0, 'active', now(), now())
                """,
                account_id,
                owner_id,
            )
            await legacy.execute(
                """
                INSERT INTO usage_ledger
                    (id, user_id, account_id, package_id, entry_type, status, amount,
                     balance_after, reference, operation, summary, resource_id, unit,
                     metadata_json, created_at)
                VALUES
                    ($1, $2, $3, NULL, 'adjustment', 'adjusted', 3, 3,
                     'legacy-admin-adjustment', 'admin_adjustment', 'Legacy adjustment',
                     NULL, 'use', $4::json, now())
                """,
                ledger_id,
                owner_id,
                account_id,
                '{"actor_email":"operator@example.com","note":"preserve-me"}',
            )
            await legacy.execute(
                """
                INSERT INTO affiliate_clicks
                    (id, user_id, brand, service_type, placement, destination_id,
                     search_id, trip_id, offer_id, partner, module, sub_id,
                     destination_summary, target_host, status, created_at)
                VALUES
                    ($1, $2, 'partner-brand', 'hotel', 'trip', 'tokyo',
                     $3, $4, $5, 'partner', 'hotel', 'private-sub-id',
                     'Private Tokyo trip', 'booking.example', 'redirected', now())
                """,
                click_id,
                owner_id,
                uuid4(),
                uuid4(),
                uuid4(),
            )
        finally:
            await legacy.close()

        await _run_alembic(database, "head")

        migrated = await asyncpg.connect(**_connection_kwargs(database))
        try:
            roles = await migrated.fetch(
                """
                SELECT user_id, role, source, expires_at
                FROM admin_role_assignments
                ORDER BY user_id, role
                """
            )
            owner_roles = {
                row["role"]
                for row in roles
                if row["user_id"] == owner_id
                and row["source"] == "legacy_backfill"
                and row["expires_at"] is None
            }
            assert owner_roles == {"content", "operations", "support"}
            assert all(row["user_id"] != member_id for row in roles)

            assert await migrated.fetchval(
                """
                SELECT metadata_json::jsonb = '{"note":"preserve-me"}'::jsonb
                FROM usage_ledger WHERE id = $1
                """,
                ledger_id,
            )
            with pytest.raises(asyncpg.RaiseError, match="usage_ledger is append-only"):
                await migrated.execute(
                    "UPDATE usage_ledger SET metadata_json = '{}'::json WHERE id = $1",
                    ledger_id,
                )

            triggers = {
                row["table_name"]: row["trigger_name"]
                for row in await migrated.fetch(
                    """
                    SELECT relation.relname AS table_name, trigger.tgname AS trigger_name
                    FROM pg_trigger AS trigger
                    JOIN pg_class AS relation ON relation.oid = trigger.tgrelid
                    JOIN pg_namespace AS namespace ON namespace.oid = relation.relnamespace
                    WHERE namespace.nspname = 'public'
                      AND NOT trigger.tgisinternal
                      AND trigger.tgname IN (
                          'usage_ledger_append_only', 'affiliate_clicks_append_only'
                      )
                    """
                )
            }
            assert triggers == {
                "affiliate_clicks": "affiliate_clicks_append_only",
                "usage_ledger": "usage_ledger_append_only",
            }

            function = await migrated.fetchrow(
                """
                SELECT procedure.prosecdef,
                       has_function_privilege(current_user, procedure.oid, 'EXECUTE') AS executable,
                       NOT EXISTS (
                           SELECT 1
                           FROM aclexplode(
                               COALESCE(
                                   procedure.proacl,
                                   acldefault('f', procedure.proowner)
                               )
                           ) AS privilege
                           WHERE privilege.grantee = 0
                             AND privilege.privilege_type = 'EXECUTE'
                       ) AS public_revoked
                FROM pg_proc AS procedure
                JOIN pg_namespace AS namespace ON namespace.oid = procedure.pronamespace
                WHERE procedure.oid =
                    'public.anonymize_affiliate_clicks_for_user(uuid)'::regprocedure
                """
            )
            assert function is not None
            assert dict(function) == {
                "prosecdef": True,
                "executable": True,
                "public_revoked": True,
            }

            with pytest.raises(asyncpg.RaiseError, match="affiliate_clicks is append-only"):
                await migrated.execute(
                    "UPDATE affiliate_clicks SET status = 'failed' WHERE id = $1",
                    click_id,
                )
            assert (
                await migrated.fetchval(
                    "SELECT public.anonymize_affiliate_clicks_for_user($1)", owner_id
                )
                == 1
            )
            anonymized = await migrated.fetchrow(
                """
                SELECT user_id, search_id, trip_id, offer_id, sub_id,
                       destination_summary, brand, partner, status
                FROM affiliate_clicks WHERE id = $1
                """,
                click_id,
            )
            assert anonymized is not None
            assert dict(anonymized) == {
                "user_id": None,
                "search_id": None,
                "trip_id": None,
                "offer_id": None,
                "sub_id": "",
                "destination_summary": "",
                "brand": "partner-brand",
                "partner": "partner",
                "status": "redirected",
            }
            with pytest.raises(asyncpg.RaiseError, match="affiliate_clicks is append-only"):
                await migrated.execute("DELETE FROM affiliate_clicks WHERE id = $1", click_id)

            partial_indexes = {
                row["index_name"]: row["predicate"]
                for row in await migrated.fetch(
                    """
                    SELECT index_class.relname AS index_name,
                           pg_get_expr(index.indpred, index.indrelid) AS predicate
                    FROM pg_index AS index
                    JOIN pg_class AS index_class ON index_class.oid = index.indexrelid
                    JOIN pg_class AS table_class ON table_class.oid = index.indrelid
                    JOIN pg_namespace AS namespace ON namespace.oid = table_class.relnamespace
                    WHERE namespace.nspname = 'public'
                      AND index_class.relname IN (
                          'uq_database_operation_one_active',
                          'uq_account_erasure_one_active'
                      )
                      AND index.indisunique
                    """
                )
            }
            assert set(partial_indexes) == {
                "uq_database_operation_one_active",
                "uq_account_erasure_one_active",
            }
            assert "queued" in partial_indexes["uq_database_operation_one_active"]
            assert "scheduled" in partial_indexes["uq_account_erasure_one_active"]

            now = datetime.now(UTC)
            await migrated.execute(
                """
                INSERT INTO database_operation_runs
                    (id, requested_by_user_id, idempotency_key, operation_type,
                     status, metadata_json, created_at, updated_at)
                VALUES ($1, $2, 'active-backup', 'backup', 'queued', '{}'::json, $3, $3)
                """,
                uuid4(),
                owner_id,
                now,
            )
            with pytest.raises(asyncpg.UniqueViolationError):
                await migrated.execute(
                    """
                    INSERT INTO database_operation_runs
                        (id, requested_by_user_id, idempotency_key, operation_type,
                         status, metadata_json, created_at, updated_at)
                    VALUES ($1, $2, 'active-analyze', 'analyze', 'running',
                            '{}'::json, $3, $3)
                    """,
                    uuid4(),
                    member_id,
                    now,
                )

            await migrated.execute(
                """
                INSERT INTO account_erasure_requests
                    (id, user_id, requested_by_user_id, idempotency_key, status,
                     reason, scheduled_for, created_at, updated_at)
                VALUES ($1, $2, $2, 'active-erasure', 'scheduled',
                        'verified migration test', $3, $3, $3)
                """,
                uuid4(),
                owner_id,
                now,
            )
            with pytest.raises(asyncpg.UniqueViolationError):
                await migrated.execute(
                    """
                    INSERT INTO account_erasure_requests
                        (id, user_id, requested_by_user_id, idempotency_key, status,
                         reason, scheduled_for, created_at, updated_at)
                    VALUES ($1, $2, $3, 'second-active-erasure', 'processing',
                            'must conflict', $4, $4, $4)
                    """,
                    uuid4(),
                    owner_id,
                    member_id,
                    now,
                )
        finally:
            await migrated.close()
    finally:
        await admin.execute(
            "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = $1",
            database,
        )
        await admin.execute(f'DROP DATABASE IF EXISTS "{database}"')
        await admin.close()
