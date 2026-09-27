"""0094 adds the news final editor's vendor and model, defaulting to Claude Opus 5.5.

``0001_initial`` builds a fresh database from the current models, so CI never sees the
table without the columns; this test takes them off a real PostgreSQL, runs the migration
through a real alembic context, and checks both directions inside one rolled back
transaction, the way ``test_migration_0088_news_needs_redraft_status`` does.
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
from sqlalchemy.orm import Session

from app.db import engine
from app.news_automation.models import NewsAutomationSettings

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0094_news_final_editor"
TABLE = "news_automation_settings"
CONSTRAINT = "ck_news_editor_provider"


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


def columns(connection: Connection) -> set[str]:
    return {column["name"] for column in sa.inspect(connection).get_columns(TABLE)}


def checks(connection: Connection) -> set[str]:
    return {str(check.get("name")) for check in sa.inspect(connection).get_check_constraints(TABLE)}


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
    session = Session(bind=connection)
    if session.get(NewsAutomationSettings, 1) is None:
        session.add(NewsAutomationSettings(id=1))
        session.flush()
    session.close()
    connection.execute(sa.text(f"ALTER TABLE {TABLE} DROP CONSTRAINT {CONSTRAINT}"))
    connection.execute(sa.text(f"ALTER TABLE {TABLE} DROP COLUMN editor_model"))
    connection.execute(sa.text(f"ALTER TABLE {TABLE} DROP COLUMN editor_provider"))

    run(connection, "upgrade")
    assert {"editor_provider", "editor_model"} <= columns(connection)
    assert CONSTRAINT in checks(connection)
    row = connection.execute(
        sa.text(f"SELECT editor_provider, editor_model FROM {TABLE} WHERE id = 1")
    ).one()
    assert tuple(row) == ("anthropic", "claude-opus-5-5")
    # Idempotent: a second upgrade finds the columns and leaves them alone.
    run(connection, "upgrade")
    assert CONSTRAINT in checks(connection)

    run(connection, "downgrade")
    assert not {"editor_provider", "editor_model"} & columns(connection)
    assert CONSTRAINT not in checks(connection)


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_adds_the_final_editor_with_its_default_and_downgrade_removes_it() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
