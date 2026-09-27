"""0106 adds the discussion thread on every series document and every screenplay.

``0001_initial`` builds a fresh database from the current models, so CI never sees a database
without the table. This test takes it off a real PostgreSQL, runs the migration through a real
alembic context, and checks both directions inside one rolled back transaction, the way
``test_migration_0104_video_youtube`` does.
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
MIGRATION = "0106_video_drama_messages"
MESSAGES = "video_drama_messages"
SERIES = "video_drama_series"
COLUMNS = {
    "id",
    "series_id",
    "subject",
    "author",
    "body_md",
    "refers_to",
    "answered_at",
    "created_at",
    "created_by_user_id",
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


def indexes(connection: Connection, table: str) -> set[str]:
    return {str(index.get("name")) for index in sa.inspect(connection).get_indexes(table)}


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
    connection.execute(sa.text(f"DROP TABLE IF EXISTS {MESSAGES}"))
    assert MESSAGES not in tables(connection)

    run(connection, "upgrade")
    assert COLUMNS <= columns(connection, MESSAGES)
    assert "ix_video_drama_messages_thread" in indexes(connection, MESSAGES)
    series_id = connection.execute(
        sa.text(
            f"INSERT INTO {SERIES} (id, slug, kind, title, premise, planned_episodes, "
            "episodes_per_chapter, created_at, updated_at) VALUES (gen_random_uuid(), "
            "'mig-0106', 'one-off', 't', 'p', 1, 1, now(), now()) RETURNING id"
        )
    ).scalar()
    connection.execute(
        sa.text(
            f"INSERT INTO {MESSAGES} (id, series_id, subject, author, body_md, refers_to, "
            "created_at) VALUES (gen_random_uuid(), :series, 'bible', 'owner', '第二幕？', 'v1', "
            "now())"
        ),
        {"series": series_id},
    )
    with pytest.raises(sa.exc.IntegrityError):
        with connection.begin_nested():
            connection.execute(
                sa.text(
                    f"INSERT INTO {MESSAGES} (id, series_id, subject, author, body_md, "
                    "created_at) VALUES (gen_random_uuid(), :series, 'bible', 'critic', 'x', "
                    "now())"
                ),
                {"series": series_id},
            )
    # Idempotent: a second upgrade finds everything and changes nothing.
    run(connection, "upgrade")
    assert connection.execute(sa.text(f"SELECT count(*) FROM {MESSAGES}")).scalar() == 1
    # The thread goes with its series.
    connection.execute(sa.text(f"DELETE FROM {SERIES} WHERE id = :id"), {"id": series_id})
    assert connection.execute(sa.text(f"SELECT count(*) FROM {MESSAGES}")).scalar() == 0

    run(connection, "downgrade")
    assert MESSAGES not in tables(connection)
    run(connection, "upgrade")
    assert MESSAGES in tables(connection)


@pytest.mark.asyncio(loop_scope="module")
async def test_0106_adds_the_thread_table_and_comes_back_off() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
