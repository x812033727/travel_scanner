"""0118 raises the slides route's length to at least eight minutes and narrows its check.

``0001_initial`` builds a fresh database from the current models, so CI never sees the old
check; the PostgreSQL test puts it back, stores a three-minute setting, and runs both directions
inside one rolled back transaction, the way ``test_migration_0113`` does.
"""

from __future__ import annotations

import importlib.util
import os
from collections.abc import AsyncIterator, Callable
from pathlib import Path
from types import ModuleType
from typing import cast

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import Connection

from app.db import engine
from app.video_automation.models import VideoAutomationSettings

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0118_video_min_8_minutes"
SETTINGS = "video_automation_settings"
CHECK = "ck_video_automation_minutes"
POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


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


def test_the_migration_writes_the_models_check() -> None:
    migration = load_migration()
    assert migration.revision == MIGRATION
    assert migration.down_revision == "0117_video_shorts_topics"
    assert len(migration.revision) <= 32
    checks = {
        constraint.name: str(constraint.sqltext)
        for constraint in cast(sa.Table, VideoAutomationSettings.__table__).constraints
        if isinstance(constraint, sa.CheckConstraint)
    }
    assert checks[CHECK] == migration.check_text(8)


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def dispose_engine_after_module() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


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


def _minutes(connection: Connection) -> tuple[int, int]:
    row = connection.execute(
        sa.text(f"SELECT target_minutes_min, target_minutes_max FROM {SETTINGS} WHERE id = 1")
    ).one()
    return int(row[0]), int(row[1])


def _set(connection: Connection, low: int, high: int) -> None:
    connection.execute(
        sa.text(
            f"UPDATE {SETTINGS} SET target_minutes_min = :low, target_minutes_max = :high "
            "WHERE id = 1"
        ),
        {"low": low, "high": high},
    )


def _exercise(connection: Connection) -> None:
    migration = load_migration()
    present = connection.execute(sa.text(f"SELECT count(*) FROM {SETTINGS} WHERE id = 1"))
    if not present.scalar():
        # The model's defaults fill a fresh row; the transaction rolls it back.
        connection.execute(
            sa.insert(cast(sa.Table, VideoAutomationSettings.__table__)).values(id=1)
        )
    connection.execute(sa.text(f"ALTER TABLE {SETTINGS} DROP CONSTRAINT IF EXISTS {CHECK}"))
    connection.execute(
        sa.text(f"ALTER TABLE {SETTINGS} ADD CONSTRAINT {CHECK} CHECK ({migration.check_text(3)})")
    )
    _set(connection, 3, 5)

    run(connection, "upgrade")
    assert _minutes(connection) == (8, 8)
    with pytest.raises(sa.exc.IntegrityError):
        with connection.begin_nested():
            _set(connection, 7, 12)
    # Idempotent: a second upgrade leaves the values and recreates the same check.
    run(connection, "upgrade")
    assert _minutes(connection) == (8, 8)

    run(connection, "downgrade")
    _set(connection, 3, 12)
    assert _minutes(connection) == (3, 12)


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_raises_short_settings_to_eight_and_downgrade_widens_the_check_again(
    dispose_engine_after_module: None,
) -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
