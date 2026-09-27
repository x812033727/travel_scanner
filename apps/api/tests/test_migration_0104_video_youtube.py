"""0104 adds the connected YouTube channel and each video's last sync record.

``0001_initial`` builds a fresh database from the current models, so CI never sees a database
without them. This test takes the table and the column off a real PostgreSQL, runs the
migration through a real alembic context, and checks both directions inside one rolled back
transaction, the way ``test_migration_0103_video_locales`` does.
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

import app.models  # noqa: F401 -- the metadata every table hangs on
from app.db import engine

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0104_video_youtube"
PROJECTS = "video_projects"
CHANNEL = "video_youtube_channel"
CHANNEL_COLUMNS = {
    "id",
    "channel_id",
    "channel_title",
    "refresh_token_encrypted",
    "scope",
    "connected_by_user_id",
    "connected_at",
    "created_at",
    "updated_at",
}


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


def columns(connection: Connection, table: str) -> set[str]:
    return {column["name"] for column in sa.inspect(connection).get_columns(table)}


def tables(connection: Connection) -> set[str]:
    return set(sa.inspect(connection).get_table_names())


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


def _older_shape(connection: Connection) -> None:
    connection.execute(sa.text(f"ALTER TABLE {PROJECTS} DROP COLUMN IF EXISTS youtube_sync"))
    connection.execute(sa.text(f"DROP TABLE IF EXISTS {CHANNEL}"))


def _exercise(connection: Connection) -> None:
    _older_shape(connection)
    assert "youtube_sync" not in columns(connection, PROJECTS)
    assert CHANNEL not in tables(connection)

    run(connection, "upgrade")
    assert "youtube_sync" in columns(connection, PROJECTS)
    assert CHANNEL_COLUMNS <= columns(connection, CHANNEL)
    connection.execute(
        sa.text(
            f"INSERT INTO {CHANNEL} (id, channel_title, refresh_token_encrypted, scope, "
            "connected_at, created_at, updated_at) VALUES (gen_random_uuid(), 'Mokaair', 'x', "
            "'youtube.force-ssl', now(), now(), now())"
        )
    )
    # Idempotent: a second upgrade finds everything and changes nothing.
    run(connection, "upgrade")
    assert connection.execute(sa.text(f"SELECT count(*) FROM {CHANNEL}")).scalar() == 1

    run(connection, "downgrade")
    assert "youtube_sync" not in columns(connection, PROJECTS)
    assert CHANNEL not in tables(connection)
    run(connection, "upgrade")
    assert CHANNEL in tables(connection)


@pytest.mark.asyncio(loop_scope="module")
async def test_0104_adds_the_channel_and_the_sync_record_and_comes_back_off() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
