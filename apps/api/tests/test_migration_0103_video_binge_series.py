"""0103 adds the binge columns to ``video_drama_series`` and widens the in-flight bound.

``0001_initial`` builds a fresh database from the current models, so CI never sees the table in
its older shape; this test takes the columns and the checks off a real PostgreSQL, puts the
narrow settings check back, runs the migration through a real alembic context, and checks both
directions inside one rolled back transaction, the way ``test_migration_0101`` does. The
downgrade must refuse while a hands-off or compiled series exists, or while the settings keep
more than two episodes in flight, and go through once they are gone.
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
MIGRATION = "0103_video_binge_series"
SERIES = "video_drama_series"
SETTINGS = "video_automation_settings"
SETTINGS_CHECK = "ck_video_drama_series"
OLD_SETTINGS_CHECK = (
    "series_max_in_flight BETWEEN 1 AND 2 AND series_chapter_ahead BETWEEN 0 AND 10 "
    "AND series_doc_rewrites BETWEEN 0 AND 5 AND series_episodes_per_month BETWEEN 0 AND 500"
)
COLUMNS = (
    "genre",
    "lead",
    "hands_off",
    "compilation",
    "visual_tier",
    "total_minutes",
    "compilation_slug",
    "compilation_started_at",
    "compilation_finished_at",
)
CHECKS = (
    "ck_video_drama_series_genre",
    "ck_video_drama_series_lead",
    "ck_video_drama_series_tier",
    "ck_video_drama_series_total_minutes",
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


def checks(connection: Connection, table: str) -> dict[str, str]:
    return {
        str(check.get("name")): str(check.get("sqltext"))
        for check in sa.inspect(connection).get_check_constraints(table)
    }


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
    for name in CHECKS:
        connection.execute(sa.text(f"ALTER TABLE {SERIES} DROP CONSTRAINT IF EXISTS {name}"))
    connection.execute(
        sa.text(
            f"ALTER TABLE {SERIES} DROP CONSTRAINT IF EXISTS uq_video_drama_series_compilation_slug"
        )
    )
    for name in COLUMNS:
        connection.execute(sa.text(f"ALTER TABLE {SERIES} DROP COLUMN IF EXISTS {name}"))
    connection.execute(
        sa.text(f"ALTER TABLE {SETTINGS} DROP CONSTRAINT IF EXISTS {SETTINGS_CHECK}")
    )
    connection.execute(
        sa.text(
            f"ALTER TABLE {SETTINGS} ADD CONSTRAINT {SETTINGS_CHECK} CHECK ({OLD_SETTINGS_CHECK})"
        )
    )


def _exercise(connection: Connection) -> None:
    # A series from before the columns existed: it must come out as the classic series.
    connection.execute(
        sa.text(
            f"INSERT INTO {SERIES} (id, slug, title, premise, status, created_at, updated_at) "
            "VALUES (gen_random_uuid(), 'mig-0103', 't', 'p', 'active', now(), now())"
        )
    )
    _older_shape(connection)
    assert "genre" not in columns(connection, SERIES)
    assert "1 AND 2" in checks(connection, SETTINGS)[SETTINGS_CHECK]

    run(connection, "upgrade")
    assert set(COLUMNS) <= columns(connection, SERIES)
    assert set(CHECKS) <= set(checks(connection, SERIES))
    assert "1 AND 6" in checks(connection, SETTINGS)[SETTINGS_CHECK]
    row = connection.execute(
        sa.text(
            f"SELECT genre, lead, hands_off, compilation, visual_tier, total_minutes "
            f"FROM {SERIES} WHERE slug = 'mig-0103'"
        )
    ).one()
    assert tuple(row) == ("xianxia-bonds", "dual-male", False, False, "clips", None)
    # Idempotent: a second upgrade finds everything and leaves it alone.
    run(connection, "upgrade")
    assert "1 AND 6" in checks(connection, SETTINGS)[SETTINGS_CHECK]

    # A hands-off series blocks the downgrade; once it is classic again the old shape returns.
    connection.execute(
        sa.text(f"UPDATE {SERIES} SET hands_off = true, compilation = true WHERE slug = 'mig-0103'")
    )
    with pytest.raises(RuntimeError, match="hands-off or compiled"):
        run(connection, "downgrade")
    connection.execute(
        sa.text(
            f"UPDATE {SERIES} SET hands_off = false, compilation = false WHERE slug = 'mig-0103'"
        )
    )
    run(connection, "downgrade")
    assert "genre" not in columns(connection, SERIES)
    assert "1 AND 2" in checks(connection, SETTINGS)[SETTINGS_CHECK]


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_adds_the_binge_columns_and_downgrade_removes_them() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
