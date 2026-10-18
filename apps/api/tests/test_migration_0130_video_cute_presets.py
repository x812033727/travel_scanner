"""0130 adds ``cute-cartoon`` and ``cute-mystery`` to the three checks that list the presets.

``0001_initial`` builds a fresh database from the current models, so CI never sees the narrow
checks; this test puts the five-preset checks back on a real PostgreSQL, runs the migration
through a real alembic context, and checks both directions inside one rolled back transaction,
the way ``test_migration_0113_video_flat_explainer`` does. The downgrade must refuse while a
request still uses either preset, and go through once none does.
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
MIGRATION = "0130_video_cute_presets"
CHECKS = (
    ("video_automation_settings", "ck_video_drama_preset"),
    ("video_drama_requests", "ck_video_drama_request_style"),
    ("video_drama_series", "ck_video_drama_series_style"),
)
OLD_CHECK = "style_preset IN ('cinematic-3d', 'anime-2d', 'ink-wash', 'flat-explainer', 'custom')"
CUTE_PRESETS = ("cute-cartoon", "cute-mystery")
REQUESTS = "video_drama_requests"


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


def allows_cute(connection: Connection) -> dict[str, bool]:
    """Whether each table's preset check mentions both new presets, as PostgreSQL renders it."""
    found: dict[str, bool] = {}
    for table, name in CHECKS:
        texts = {
            str(check.get("name")): str(check.get("sqltext"))
            for check in sa.inspect(connection).get_check_constraints(table)
        }
        assert name in texts, (table, texts)
        assert "flat-explainer" in texts[name], (table, texts[name])
        mentioned = [preset in texts[name] for preset in CUTE_PRESETS]
        assert all(mentioned) or not any(mentioned), (table, texts[name])
        found[table] = all(mentioned)
    return found


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
    for table, name in CHECKS:
        connection.execute(sa.text(f"ALTER TABLE {table} DROP CONSTRAINT IF EXISTS {name}"))
        connection.execute(
            sa.text(f"ALTER TABLE {table} ADD CONSTRAINT {name} CHECK ({OLD_CHECK})")
        )


def _insert_request(connection: Connection, preset: str) -> None:
    connection.execute(
        sa.text(
            f"INSERT INTO {REQUESTS} "
            "(id, premise, style_preset, target_minutes, status, created_at, updated_at) "
            "VALUES (gen_random_uuid(), 'why thunder is late', :preset, 8, 'queued', now(), now())"
        ),
        {"preset": preset},
    )


def _exercise(connection: Connection) -> None:
    _older_shape(connection)
    assert not any(allows_cute(connection).values())
    for preset in CUTE_PRESETS:
        with pytest.raises(sa.exc.IntegrityError):
            with connection.begin_nested():
                _insert_request(connection, preset)
    # The explainer that was already there is unaffected in both shapes.
    _insert_request(connection, "flat-explainer")

    run(connection, "upgrade")
    assert all(allows_cute(connection).values())
    _insert_request(connection, "cute-cartoon")
    _insert_request(connection, "flat-explainer")
    # Idempotent: a second upgrade recreates the same checks.
    run(connection, "upgrade")
    assert all(allows_cute(connection).values())

    # One row in either preset is enough to refuse: the old checks cannot hold it.
    with pytest.raises(RuntimeError, match="use the cute-cartoon or cute-mystery preset"):
        run(connection, "downgrade")
    connection.execute(
        sa.text(
            f"UPDATE {REQUESTS} SET style_preset = 'custom' WHERE style_preset = 'cute-cartoon'"
        )
    )
    _insert_request(connection, "cute-mystery")
    with pytest.raises(RuntimeError, match="use the cute-cartoon or cute-mystery preset"):
        run(connection, "downgrade")
    connection.execute(
        sa.text(
            f"UPDATE {REQUESTS} SET style_preset = 'custom' "
            "WHERE style_preset IN ('cute-cartoon', 'cute-mystery')"
        )
    )
    run(connection, "downgrade")
    assert not any(allows_cute(connection).values())


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_allows_the_cute_presets_and_downgrade_refuses_while_one_is_used() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
