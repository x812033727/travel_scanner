"""0102 creates the linked YouTube channel's table and adds each video's sync columns.

``0001_initial`` builds a fresh database from the current models, so CI never sees a database
without them; this test takes them away on a real PostgreSQL, runs the migration through a real
alembic context, and checks both directions inside one rolled back transaction, the way
``test_migration_0096_video_media_jobs`` does.
"""

from __future__ import annotations

import importlib.util
import os
from collections.abc import AsyncIterator, Callable
from pathlib import Path
from types import ModuleType

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import Connection

from app.db import engine

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0102_video_youtube_sync"
TABLE = "video_youtube_connections"
PROJECTS = "video_projects"
PROJECT_COLUMNS = {"youtube_sync", "youtube_upload_session"}


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def load_migration() -> ModuleType:
    path = VERSIONS / f"{MIGRATION}.py"
    spec = importlib.util.spec_from_file_location(f"migration_{MIGRATION}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(connection: Connection, direction: str) -> None:
    context = MigrationContext.configure(connection)
    with Operations.context(context):
        getattr(load_migration(), direction)()


def tables(connection: Connection) -> set[str]:
    return set(sa.inspect(connection).get_table_names())


def columns(connection: Connection, table: str) -> set[str]:
    return {column["name"] for column in sa.inspect(connection).get_columns(table)}


def in_a_rolled_back_transaction(
    exercise: Callable[[Connection], None],
) -> Callable[[Connection], None]:
    def runner(connection: Connection) -> None:
        transaction = connection.begin()
        try:
            exercise(connection)
        finally:
            transaction.rollback()

    return runner


def _exercise(connection: Connection) -> None:
    connection.execute(sa.text(f"DROP TABLE IF EXISTS {TABLE}"))
    for name in PROJECT_COLUMNS:
        connection.execute(sa.text(f"ALTER TABLE {PROJECTS} DROP COLUMN IF EXISTS {name}"))
    assert TABLE not in tables(connection)
    assert not PROJECT_COLUMNS & columns(connection, PROJECTS)

    run(connection, "upgrade")
    assert TABLE in tables(connection)
    assert {
        "client_id",
        "secret_config_encrypted",
        "channel_id",
        "channel_title",
        "verified_at",
        "problem",
        "audited",
    } <= columns(connection, TABLE)
    assert PROJECT_COLUMNS <= columns(connection, PROJECTS)
    checks = {
        str(check.get("name")) for check in sa.inspect(connection).get_check_constraints(TABLE)
    }
    assert "ck_video_youtube_connection_single" in checks
    # The one row, with the audit switch off until the owner says otherwise.
    connection.execute(
        sa.text(f"INSERT INTO {TABLE} (id, created_at, updated_at) VALUES (1, now(), now())")
    )
    assert connection.execute(sa.text(f"SELECT audited FROM {TABLE}")).scalar() is False
    with pytest.raises(sa.exc.IntegrityError):
        with connection.begin_nested():
            connection.execute(
                sa.text(
                    f"INSERT INTO {TABLE} (id, created_at, updated_at) VALUES (2, now(), now())"
                )
            )
    # Idempotent: a second upgrade finds everything and leaves it alone.
    run(connection, "upgrade")

    run(connection, "downgrade")
    assert TABLE not in tables(connection)
    assert not PROJECT_COLUMNS & columns(connection, PROJECTS)


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_adds_the_channel_table_and_the_sync_columns_and_downgrade_removes_them() -> (
    None
):
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
