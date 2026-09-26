"""0097 creates the owner's drama requests table and gives each video a format.

``0001_initial`` builds a fresh database from the current models, so CI never sees a database
without them; this test takes them off a real PostgreSQL, runs the migration through a real
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
MIGRATION = "0097_video_drama_requests"
TABLE = "video_drama_requests"
PROJECTS = "video_projects"
FORMAT_CHECK = "ck_video_project_format"


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


def checks(connection: Connection, table: str) -> set[str]:
    return {str(check.get("name")) for check in sa.inspect(connection).get_check_constraints(table)}


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
    connection.execute(sa.text(f"ALTER TABLE {PROJECTS} DROP CONSTRAINT IF EXISTS {FORMAT_CHECK}"))
    connection.execute(sa.text(f"ALTER TABLE {PROJECTS} DROP COLUMN IF EXISTS format"))
    assert TABLE not in tables(connection)
    assert "format" not in columns(connection, PROJECTS)

    run(connection, "upgrade")
    assert TABLE in tables(connection)
    inspector = sa.inspect(connection)
    assert {
        "premise",
        "source_guide",
        "style_preset",
        "target_minutes",
        "status",
        "slug",
        "created_by_user_id",
        "started_by_token_id",
        "started_at",
        "cancelled_at",
    } <= columns(connection, TABLE)
    assert {index["name"] for index in inspector.get_indexes(TABLE)} >= {
        "ix_video_drama_requests_status_created"
    }
    assert checks(connection, TABLE) >= {
        "ck_video_drama_request_status",
        "ck_video_drama_request_style",
    }
    assert "format" in columns(connection, PROJECTS)
    assert FORMAT_CHECK in checks(connection, PROJECTS)
    # An older row reads as a slides video.
    connection.execute(
        sa.text(
            f"INSERT INTO {PROJECTS} (id, slug, title, stage, checklist, last_synced_at, "
            "created_at, updated_at) VALUES (gen_random_uuid(), 'older-video', 't', 'brief', "
            "'[]', now(), now(), now())"
        )
    )
    stored = connection.execute(
        sa.text(f"SELECT format FROM {PROJECTS} WHERE slug = 'older-video'")
    ).scalar()
    assert stored == "slides"
    with pytest.raises(sa.exc.DBAPIError):
        with connection.begin_nested():
            connection.execute(
                sa.text(f"UPDATE {PROJECTS} SET format = 'opera' WHERE slug = 'older-video'")
            )

    # Idempotent: a second upgrade finds everything and leaves it alone.
    run(connection, "upgrade")
    run(connection, "downgrade")
    assert TABLE not in tables(connection)
    assert "format" not in columns(connection, PROJECTS)


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_adds_the_requests_and_the_format_and_downgrade_removes_them() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
