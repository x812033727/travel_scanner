"""0096 creates the media generation jobs table of the drama route.

``0001_initial`` builds a fresh database from the current models, so CI never sees a database
without the table; this test drops it on a real PostgreSQL, runs the migration through a real
alembic context, and checks both directions inside one rolled back transaction, the way
``test_migration_0094_news_final_editor`` does.
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
MIGRATION = "0096_video_media_jobs"
TABLE = "video_media_jobs"


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
    assert TABLE not in tables(connection)
    run(connection, "upgrade")
    assert TABLE in tables(connection)
    inspector = sa.inspect(connection)
    columns = {column["name"] for column in inspector.get_columns(TABLE)}
    assert {
        "slug",
        "kind",
        "request",
        "request_hash",
        "status",
        "usd_estimate",
        "file_sha256",
    } <= columns
    assert {index["name"] for index in inspector.get_indexes(TABLE)} >= {
        "ix_video_media_jobs_slug",
        "ix_video_media_jobs_created",
        "ix_video_media_jobs_status",
    }
    assert {str(check.get("name")) for check in inspector.get_check_constraints(TABLE)} >= {
        "ck_video_media_job_kind",
        "ck_video_media_job_status",
    }
    # Idempotent: a second upgrade finds the table and leaves it alone.
    run(connection, "upgrade")
    run(connection, "downgrade")
    assert TABLE not in tables(connection)


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_creates_the_jobs_table_and_downgrade_drops_it() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
