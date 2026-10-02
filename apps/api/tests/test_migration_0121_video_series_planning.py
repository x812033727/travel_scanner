"""Exercise the old-table branch and SQL checks, not just create_all's current model."""

from __future__ import annotations

import importlib.util
import io
import os
from collections.abc import AsyncIterator
from pathlib import Path
from types import ModuleType
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
from app.models import VIDEO_CATEGORIES
from app.video_automation.models import (
    SERIES_CATEGORY_CHECK,
    SERIES_PLANNING_CHECK,
)

MIGRATION = "0121_video_series_planning"
POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


def load_migration() -> ModuleType:
    file = Path(__file__).resolve().parents[1] / "migrations" / "versions" / f"{MIGRATION}.py"
    spec = importlib.util.spec_from_file_location(f"migration_{MIGRATION}", file)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(connection: Connection, direction: str) -> None:
    with Operations.context(MigrationContext.configure(connection)):
        getattr(load_migration(), direction)()


def test_migration_and_model_contracts_match() -> None:
    migration = load_migration()
    assert len(migration.revision) <= 32
    assert migration.down_revision == "0120_video_dropped_request"
    assert migration.CATEGORIES == VIDEO_CATEGORIES
    # 0122 extends the live model. This historical migration must retain its own bounds.
    assert "planning_only = true AND target_minutes BETWEEN 21 AND 30" in migration.NUMBERS_CHECK
    assert migration.LEAD_CHECK == (
        "lead IN ('female', 'male', 'dual-male') OR (planning_only = true AND lead = 'ensemble')"
    )
    assert migration.CATEGORY_CHECK == SERIES_CATEGORY_CHECK
    assert migration.PLANNING_CHECK == SERIES_PLANNING_CHECK


@pytest.mark.parametrize("present", [False, True])
def test_upgrade_adds_only_missing_columns(present: bool, monkeypatch: pytest.MonkeyPatch) -> None:
    migration = load_migration()
    operations = Mock()
    columns = {"planning_only", "category", "planning_spec"} if present else set()
    checks = {migration.NUMBERS, migration.LEAD, migration.CATEGORY, migration.PLANNING}
    monkeypatch.setattr(migration, "op", operations)
    monkeypatch.setattr(migration, "_columns", lambda: columns)
    monkeypatch.setattr(migration, "_checks", lambda: checks)
    migration.upgrade()
    assert operations.add_column.call_count == (0 if present else 3)
    assert operations.drop_constraint.call_count == 4
    assert operations.create_check_constraint.call_count == 4


@pytest.mark.parametrize("direction", ["upgrade", "downgrade"])
def test_offline_sql_does_not_inspect(direction: str, monkeypatch: pytest.MonkeyPatch) -> None:
    migration = load_migration()
    monkeypatch.setattr(
        migration.sa, "inspect", lambda _connection: pytest.fail("must not inspect offline")
    )
    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": output}
    )
    with Operations.context(context):
        getattr(migration, direction)()
    sql = output.getvalue()
    assert "ck_video_drama_series_numbers" in sql and "ck_video_drama_series_lead" in sql
    if direction == "upgrade":
        assert "ADD COLUMN planning_only BOOLEAN DEFAULT 'false' NOT NULL" in sql
        assert "ADD COLUMN planning_spec JSON" in sql
        assert migration.PLANNING_CHECK in sql
    else:
        assert "RAISE EXCEPTION" in sql
        assert sql.index("RAISE EXCEPTION") < sql.index("DROP CONSTRAINT")


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def postgres_engine() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def _refused(connection: Connection, sql: str, values: dict[str, object]) -> bool:
    savepoint = connection.begin_nested()
    try:
        connection.execute(sa.text(sql), values)
    except IntegrityError:
        savepoint.rollback()
        return True
    savepoint.rollback()
    return False


def _exercise(connection: Connection) -> None:
    migration = load_migration()
    with connection.begin() as transaction:
        try:
            connection.execute(
                sa.text(
                    "CREATE TEMPORARY TABLE video_drama_series (id uuid PRIMARY KEY, "
                    "slug varchar(40) NOT NULL UNIQUE, kind varchar(12) NOT NULL DEFAULT 'series', "
                    "status varchar(12) NOT NULL DEFAULT 'active', "
                    "planned_episodes integer NOT NULL DEFAULT 120, "
                    "episodes_per_chapter integer NOT NULL DEFAULT 12, "
                    "target_minutes integer NOT NULL DEFAULT 8, "
                    "lead varchar(12) NOT NULL DEFAULT 'male', "
                    "hands_off boolean NOT NULL DEFAULT false, "
                    "compilation boolean NOT NULL DEFAULT false, "
                    "force_next boolean NOT NULL DEFAULT false, requested_chapter integer, "
                    f"CONSTRAINT {migration.NUMBERS} CHECK ({migration.OLD_NUMBERS_CHECK}), "
                    f"CONSTRAINT {migration.LEAD} CHECK ({migration.OLD_LEAD_CHECK})) "
                    "ON COMMIT DROP"
                )
            )
            connection.execute(
                sa.text("INSERT INTO video_drama_series(id, slug) VALUES (:id, 'kept')"),
                {"id": uuid4()},
            )
            run(connection, "upgrade")
            run(connection, "upgrade")
            ordinary = connection.execute(
                sa.text(
                    "SELECT planning_only, category, planning_spec, target_minutes, lead "
                    "FROM video_drama_series WHERE slug = 'kept'"
                )
            ).one()
            assert tuple(ordinary) == (False, None, None, 8, "male")
            connection.execute(
                sa.text(
                    "INSERT INTO video_drama_series(id, slug, planning_only, category, "
                    "planning_spec, "
                    "status, target_minutes, lead) VALUES (:id, 'anime-plan', true, 'anime', "
                    "CAST(:spec AS json), 'paused', 22, 'ensemble')"
                ),
                {"id": uuid4(), "spec": '{"story_minutes":22,"tone":"原創群像"}'},
            )
            for column, value in (
                ("planning_only", False),
                ("status", "active"),
                ("category", None),
                ("category", "drama"),
                ("kind", "story"),
                ("hands_off", True),
                ("compilation", True),
                ("force_next", True),
                ("requested_chapter", 1),
                ("target_minutes", 31),
                ("lead", "bogus"),
            ):
                assert _refused(
                    connection,
                    (f"UPDATE video_drama_series SET {column} = :value WHERE slug = 'anime-plan'"),
                    {"value": value},
                ), (column, value)
            for column, value in (
                ("target_minutes", 21),
                ("lead", "ensemble"),
                ("category", "bad"),
            ):
                assert _refused(
                    connection,
                    (f"UPDATE video_drama_series SET {column} = :value WHERE slug = 'kept'"),
                    {"value": value},
                )
            with pytest.raises(RuntimeError, match="must be preserved"):
                run(connection, "downgrade")
            assert (
                connection.scalar(
                    sa.text("SELECT count(*) FROM video_drama_series WHERE planning_only = true")
                )
                == 1
            )
            connection.execute(sa.text("DELETE FROM video_drama_series WHERE slug = 'anime-plan'"))
            run(connection, "downgrade")
            columns = {
                column["name"] for column in sa.inspect(connection).get_columns(migration.TABLE)
            }
            assert not {"planning_only", "category", "planning_spec"} & columns
            assert connection.execute(
                sa.text("SELECT target_minutes, lead FROM video_drama_series WHERE slug = 'kept'")
            ).one() == (8, "male")
            assert _refused(
                connection,
                ("UPDATE video_drama_series SET target_minutes = 22 WHERE slug = 'kept'"),
                {},
            )
        finally:
            transaction.rollback()


@POSTGRES
@pytest.mark.usefixtures("postgres_engine")
@pytest.mark.asyncio(loop_scope="module")
async def test_real_old_table_upgrade_checks_idempotency_and_downgrade() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(_exercise)
