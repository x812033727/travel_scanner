"""0114 adds the illustrated slides' settings (docs/videos/ILLUSTRATED.md) to the settings row.

``0001_initial`` builds a fresh database from the current models, so CI never sees a database
without them; this test takes them off a real PostgreSQL, runs the migration through a real
alembic context, and checks both directions inside one rolled back transaction, the way
``test_migration_0100_video_hands_off`` does.
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
MIGRATION = "0114_video_slides_media"
SETTINGS = "video_automation_settings"
USD_CHECK = "ck_video_slides_usd"
COLUMNS = (
    "slides_media_enabled",
    "slides_image_model",
    "slides_max_usd_per_video",
    "slides_auto_approve_storyboard",
    "slides_music_track",
    "slides_sfx_set",
)


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
    connection.execute(sa.text(f"ALTER TABLE {SETTINGS} DROP CONSTRAINT IF EXISTS {USD_CHECK}"))
    for name in COLUMNS:
        connection.execute(sa.text(f"ALTER TABLE {SETTINGS} DROP COLUMN IF EXISTS {name}"))
    assert not set(COLUMNS) & columns(connection, SETTINGS)
    assert USD_CHECK not in checks(connection, SETTINGS)

    run(connection, "upgrade")
    assert set(COLUMNS) <= columns(connection, SETTINGS)
    assert USD_CHECK in checks(connection, SETTINGS)
    # An existing settings row reads the defaults: pictures off, Flash, US$20, the storyboard
    # approving itself, no music file or effect set named yet.
    found = {
        column["name"]: column
        for column in sa.inspect(connection).get_columns(SETTINGS)
        if column["name"] in COLUMNS
    }
    assert str(found["slides_media_enabled"]["default"]) == "false"
    assert "gemini-3.1-flash-image" in str(found["slides_image_model"]["default"])
    assert str(found["slides_max_usd_per_video"]["default"]) == "20"
    assert str(found["slides_auto_approve_storyboard"]["default"]) == "true"
    for name in ("slides_music_track", "slides_sfx_set"):
        assert found[name]["default"] is None and found[name]["nullable"]

    # Idempotent: a second upgrade finds everything and leaves it alone.
    run(connection, "upgrade")
    run(connection, "downgrade")
    assert not set(COLUMNS) & columns(connection, SETTINGS)
    assert USD_CHECK not in checks(connection, SETTINGS)


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_adds_the_slides_media_settings_and_downgrade_removes_them() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
