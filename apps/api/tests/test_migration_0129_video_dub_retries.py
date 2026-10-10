"""Exercise the 0129 column migration: offline everywhere, and on a real PostgreSQL schema.

0001 creates a fresh schema from the current models, so the PostgreSQL part removes the column
first to exercise the upgrade branch that production takes.
"""

from __future__ import annotations

import importlib.util
import io
import os
from collections.abc import AsyncIterator
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import Connection

from app.db import engine
from app.models import VideoProject

MIGRATION = "0129_video_dub_retries"
PATH = Path(__file__).resolve().parents[1] / "migrations" / "versions" / f"{MIGRATION}.py"
TABLE = "video_projects"
COLUMN = "dub_retries"
POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


def load_migration() -> ModuleType:
    spec = importlib.util.spec_from_file_location(f"migration_{MIGRATION}", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(connection: Connection, direction: str) -> None:
    context = MigrationContext.configure(connection)
    with Operations.context(context):
        getattr(load_migration(), direction)()


def columns(connection: Connection) -> dict[str, Any]:
    return {item["name"]: item for item in sa.inspect(connection).get_columns(TABLE)}


def test_the_revision_follows_0128_and_fits_the_id_column() -> None:
    migration = load_migration()
    assert migration.revision == MIGRATION
    assert migration.down_revision == "0128_video_languages_four"
    assert len(migration.revision) <= 32, "alembic_version.version_num is 32 characters"
    assert (migration.TABLE, migration.COLUMN) == (TABLE, COLUMN)
    # A fresh database (0001) builds the column from the model: the two must agree.
    column = cast(sa.Table, VideoProject.__table__).c[COLUMN]
    assert isinstance(column.type, sa.JSON) and not column.nullable
    assert column.server_default is not None
    assert str(cast(sa.DefaultClause, column.server_default).arg) == "'{}'"


@pytest.mark.parametrize("direction", ["upgrade", "downgrade"])
def test_offline_sql_adds_one_json_column_without_inspecting(
    direction: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    migration = load_migration()
    monkeypatch.setattr(
        migration.sa, "inspect", lambda _connection: pytest.fail("offline inspection")
    )
    buffer = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": buffer}
    )
    with Operations.context(context):
        getattr(migration, direction)()
    statements = [line.strip() for line in buffer.getvalue().splitlines() if line.strip()]
    if direction == "upgrade":
        assert statements == [
            "ALTER TABLE video_projects ADD COLUMN dub_retries JSON DEFAULT '{}' NOT NULL;"
        ], "one additive column, json and not jsonb, no backfill"
    else:
        assert statements == ["ALTER TABLE video_projects DROP COLUMN dub_retries;"]


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def postgres_engine() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def exercise(connection: Connection) -> None:
    transaction = connection.begin()
    try:
        connection.execute(sa.text(f"ALTER TABLE {TABLE} DROP COLUMN IF EXISTS {COLUMN}"))
        before = columns(connection)
        assert COLUMN not in before
        run(connection, "upgrade")
        added = columns(connection)[COLUMN]
        assert isinstance(added["type"], sa.JSON) and not added["nullable"]
        assert "'{}'" in str(added["default"])
        # The rows that were there read as "no request" without a backfill.
        assert (
            connection.execute(
                sa.text(f"SELECT count(*) FROM {TABLE} WHERE {COLUMN}::text <> '{{}}'")
            ).scalar_one()
            == 0
        )
        run(connection, "upgrade")
        assert set(columns(connection)) == set(before) | {COLUMN}, "a second run adds nothing"
        run(connection, "downgrade")
        assert set(columns(connection)) == set(before)
        run(connection, "downgrade")
        assert set(columns(connection)) == set(before), "a second downgrade is a no-op"
    finally:
        transaction.rollback()


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_twice_then_downgrade_leaves_the_table_as_it_was(
    postgres_engine: None,
) -> None:
    async with engine.connect() as connection:
        await connection.run_sync(exercise)
