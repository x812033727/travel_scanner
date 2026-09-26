"""0100 adds the channel stance, the hands-off switches and the publish time.

``0001_initial`` builds a fresh database from the current models, so CI never sees a database
without them; this test takes them off a real PostgreSQL, runs the migration through a real
alembic context, and checks both directions inside one rolled back transaction, the way
``test_migration_0097_video_drama_requests`` does.
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
MIGRATION = "0100_video_hands_off"
SETTINGS = "video_automation_settings"
PROJECTS = "video_projects"
ID_CHECK = "ck_video_project_youtube_id"
SETTINGS_COLUMNS = ("channel_stance", "auto_pick_outline", "auto_approve_final", "auto_pick_look")


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
    connection.execute(sa.text(f"ALTER TABLE {PROJECTS} DROP CONSTRAINT IF EXISTS {ID_CHECK}"))
    connection.execute(sa.text(f"ALTER TABLE {PROJECTS} DROP COLUMN IF EXISTS youtube_publish_at"))
    for name in SETTINGS_COLUMNS:
        connection.execute(sa.text(f"ALTER TABLE {SETTINGS} DROP COLUMN IF EXISTS {name}"))
    assert not set(SETTINGS_COLUMNS) & columns(connection, SETTINGS)
    assert "youtube_publish_at" not in columns(connection, PROJECTS)
    assert ID_CHECK not in checks(connection, PROJECTS)

    run(connection, "upgrade")
    assert set(SETTINGS_COLUMNS) <= columns(connection, SETTINGS)
    assert "youtube_publish_at" in columns(connection, PROJECTS)
    assert ID_CHECK in checks(connection, PROJECTS)
    # An existing settings row reads the defaults: a blank stance, the switches on, the look off.
    # (The older columns have no server defaults, so a bare INSERT cannot make a row here; the
    # server defaults the migration set are what an existing row would read.)
    defaults = {
        column["name"]: str(column["default"])
        for column in sa.inspect(connection).get_columns(SETTINGS)
        if column["name"] in SETTINGS_COLUMNS
    }
    assert defaults["channel_stance"] in ("''::text", "''")
    assert defaults["auto_pick_outline"] == "true"
    assert defaults["auto_approve_final"] == "true"
    assert defaults["auto_pick_look"] == "false"
    # A YouTube id is eleven characters; the check holds new writes to it.
    connection.execute(
        sa.text(
            f"INSERT INTO {PROJECTS} (id, slug, title, stage, checklist, last_synced_at, "
            "created_at, updated_at, youtube_video_id) VALUES (gen_random_uuid(), 'eleven-chars', "
            "'t', 'done', '[]', now(), now(), now(), 'dQw4w9WgXcQ')"
        )
    )
    with pytest.raises(sa.exc.DBAPIError):
        with connection.begin_nested():
            connection.execute(
                sa.text(
                    f"UPDATE {PROJECTS} SET youtube_video_id = 'short' WHERE slug = 'eleven-chars'"
                )
            )

    # Idempotent: a second upgrade finds everything and leaves it alone.
    run(connection, "upgrade")
    run(connection, "downgrade")
    assert not set(SETTINGS_COLUMNS) & columns(connection, SETTINGS)
    assert "youtube_publish_at" not in columns(connection, PROJECTS)
    assert ID_CHECK not in checks(connection, PROJECTS)


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_adds_stance_switches_and_publish_time_and_downgrade_removes_them() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
