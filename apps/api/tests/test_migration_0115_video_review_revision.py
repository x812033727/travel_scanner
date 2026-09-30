"""0115 preserves review history while adding a revision to the content identity.

Guard and offline SQL tests run without a database. The PostgreSQL test creates a
temporary legacy-shaped review table, shadowing the shared table in its own connection,
so it exercises the real ALTER statements and defaults without touching shared rows.
"""

from __future__ import annotations

import importlib.util
import io
import os
from collections.abc import AsyncIterator
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError

from app.db import engine

MIGRATION = "0115_video_review_revision"
REVIEWS = "video_reviews"
OLD_UNIQUE = "uq_video_review_content"
NEW_UNIQUE = "uq_video_review_content_revision"
REVISION_CHECK = "ck_video_review_revision"
POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


def load_migration() -> ModuleType:
    file = Path(__file__).resolve().parents[1] / "migrations" / "versions" / f"{MIGRATION}.py"
    spec = importlib.util.spec_from_file_location(f"migration_{MIGRATION}", file)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(connection: Connection, direction: str) -> None:
    with Operations.context(MigrationContext.configure(connection)):
        getattr(load_migration(), direction)()


def test_current_model_shape_needs_no_schema_changes(monkeypatch: pytest.MonkeyPatch) -> None:
    migration = load_migration()
    operations = Mock()
    monkeypatch.setattr(migration, "op", operations)
    monkeypatch.setattr(migration, "_offline", lambda: False)
    monkeypatch.setattr(migration, "_columns", lambda: {"revision"})
    monkeypatch.setattr(migration, "_checks", lambda: {REVISION_CHECK})
    monkeypatch.setattr(migration, "_uniques", lambda: {NEW_UNIQUE})
    migration.upgrade()
    assert operations.mock_calls == []


def test_legacy_constraint_is_removed_even_if_new_shape_already_exists(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    migration = load_migration()
    operations = Mock()
    monkeypatch.setattr(migration, "op", operations)
    monkeypatch.setattr(migration, "_offline", lambda: False)
    monkeypatch.setattr(migration, "_columns", lambda: {"revision"})
    monkeypatch.setattr(migration, "_checks", lambda: {REVISION_CHECK})
    monkeypatch.setattr(migration, "_uniques", lambda: {OLD_UNIQUE, NEW_UNIQUE})
    migration.upgrade()
    operations.drop_constraint.assert_called_once_with(OLD_UNIQUE, REVIEWS, type_="unique")
    operations.add_column.assert_not_called()
    operations.create_unique_constraint.assert_not_called()
    operations.create_check_constraint.assert_not_called()


def test_downgrade_refuses_duplicate_identities_before_any_schema_change(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    migration = load_migration()
    operations = Mock()
    operations.get_bind.return_value.execute.return_value.scalar.return_value = 1
    monkeypatch.setattr(migration, "op", operations)
    monkeypatch.setattr(migration, "_offline", lambda: False)
    with pytest.raises(RuntimeError, match="multiple review revisions exist"):
        migration.downgrade()
    operations.create_unique_constraint.assert_not_called()
    operations.drop_constraint.assert_not_called()
    operations.drop_column.assert_not_called()


@pytest.mark.parametrize("direction", ["upgrade", "downgrade"])
def test_offline_sql_does_not_inspect_a_database(
    direction: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    migration = load_migration()
    monkeypatch.setattr(
        migration.sa,
        "inspect",
        lambda _connection: pytest.fail("offline SQL must not inspect a database"),
    )
    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": output}
    )
    with Operations.context(context):
        getattr(migration, direction)()
    sql = output.getvalue()
    if direction == "upgrade":
        assert "ADD COLUMN revision INTEGER DEFAULT 0 NOT NULL" in sql
        assert f"ADD CONSTRAINT {REVISION_CHECK} CHECK (revision >= 0)" in sql
        assert "UNIQUE (project_id, gate, content_sha256, revision)" in sql
        assert f"DROP CONSTRAINT {OLD_UNIQUE}" in sql
    else:
        assert "HAVING count(*) > 1 LIMIT 1" in sql
        assert "RAISE EXCEPTION 'multiple review revisions exist" in sql
        assert sql.index("RAISE EXCEPTION") < sql.index(f"ADD CONSTRAINT {OLD_UNIQUE}")
        assert sql.index(f"ADD CONSTRAINT {OLD_UNIQUE}") < sql.index("DROP COLUMN revision")
        assert f"DROP CONSTRAINT {NEW_UNIQUE}" in sql


def test_offline_mode_uses_the_operations_context(monkeypatch: pytest.MonkeyPatch) -> None:
    migration = load_migration()
    monkeypatch.setattr(migration.op, "get_context", lambda: SimpleNamespace(as_sql=True))
    assert migration._offline() is True


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def postgres_engine() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def _exercise(connection: Connection) -> None:
    with connection.begin() as transaction:
        try:
            connection.execute(
                sa.text(
                    f"CREATE TEMPORARY TABLE {REVIEWS} ("
                    "id uuid PRIMARY KEY, project_id uuid NOT NULL, gate varchar(20) NOT NULL, "
                    "content_sha256 varchar(64) NOT NULL, summary varchar(500) NOT NULL, "
                    "payload json NOT NULL, status varchar(20) NOT NULL, decided_at timestamptz, "
                    f"CONSTRAINT {OLD_UNIQUE} UNIQUE (project_id, gate, content_sha256)) "
                    "ON COMMIT DROP"
                )
            )
            ids = {"id": uuid4(), "project_id": uuid4(), "sha": "a" * 64}
            connection.execute(
                sa.text(
                    f"INSERT INTO {REVIEWS} "
                    "(id, project_id, gate, content_sha256, summary, payload, status, decided_at) "
                    "VALUES (:id, :project_id, 'final', :sha, 'owner decision', "
                    "'{\"qa\": {\"ok\": false}}', 'approved', '2026-09-30T00:00:00Z')"
                ),
                ids,
            )
            before = connection.execute(
                sa.text(f"SELECT summary, payload::text, status, decided_at FROM {REVIEWS}")
            ).one()
            run(connection, "upgrade")
            run(connection, "upgrade")
            columns = {
                column["name"]: column for column in sa.inspect(connection).get_columns(REVIEWS)
            }
            assert columns["revision"]["nullable"] is False
            assert str(columns["revision"]["default"]) == "0"
            assert connection.execute(sa.text(f"SELECT revision FROM {REVIEWS}")).scalar() == 0
            assert (
                connection.execute(
                    sa.text(f"SELECT summary, payload::text, status, decided_at FROM {REVIEWS}")
                ).one()
                == before
            )
            uniques = {
                constraint["name"]
                for constraint in sa.inspect(connection).get_unique_constraints(REVIEWS)
            }
            assert NEW_UNIQUE in uniques and OLD_UNIQUE not in uniques

            insert = sa.text(
                f"INSERT INTO {REVIEWS} "
                "(id, project_id, gate, content_sha256, summary, payload, status, revision) "
                "VALUES (:id, :project_id, 'final', :sha, 'renewed', '{}', 'pending', :revision)"
            )
            for invalid in (0, -1):
                with pytest.raises(IntegrityError):
                    with connection.begin_nested():
                        connection.execute(insert, {**ids, "id": uuid4(), "revision": invalid})
            connection.execute(insert, {**ids, "id": uuid4(), "revision": 1})
            with pytest.raises(RuntimeError, match="multiple review revisions exist"):
                run(connection, "downgrade")
            assert connection.execute(
                sa.text(f"SELECT revision FROM {REVIEWS} ORDER BY revision")
            ).scalars().all() == [0, 1]

            # Only the fixture's added revision is removed to exercise the safe reverse path.
            connection.execute(sa.text(f"DELETE FROM {REVIEWS} WHERE revision = 1"))
            run(connection, "downgrade")
            assert "revision" not in {
                column["name"] for column in sa.inspect(connection).get_columns(REVIEWS)
            }
            assert OLD_UNIQUE in {
                constraint["name"]
                for constraint in sa.inspect(connection).get_unique_constraints(REVIEWS)
            }
            assert (
                connection.execute(
                    sa.text(f"SELECT summary, payload::text, status, decided_at FROM {REVIEWS}")
                ).one()
                == before
            )
        finally:
            transaction.rollback()


@POSTGRES
@pytest.mark.usefixtures("postgres_engine")
@pytest.mark.asyncio(loop_scope="module")
async def test_postgresql_legacy_rows_defaults_history_and_downgrade() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(_exercise)
