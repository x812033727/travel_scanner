"""Exercise the 0104 column migration on a real PostgreSQL schema.

0001 creates a fresh schema from current models, so CI must remove the columns first to
exercise the upgrade branch that production uses.
"""

from __future__ import annotations

import importlib.util
import os
from collections.abc import AsyncIterator
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
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)

MIGRATION = "0104_video_retry_request"
PATH = Path(__file__).resolve().parents[1] / "migrations" / "versions" / f"{MIGRATION}.py"
COLUMNS = {"retry_request_id", "retry_acknowledged_id"}


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def load_migration() -> ModuleType:
    spec = importlib.util.spec_from_file_location(f"migration_{MIGRATION}", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(connection: Connection, direction: str) -> None:
    context = MigrationContext.configure(connection)
    with Operations.context(context):
        getattr(load_migration(), direction)()


def columns(connection: Connection) -> set[str]:
    return {item["name"] for item in sa.inspect(connection).get_columns("video_projects")}


def exercise(connection: Connection) -> None:
    transaction = connection.begin()
    try:
        for name in COLUMNS:
            connection.execute(sa.text(f"ALTER TABLE video_projects DROP COLUMN IF EXISTS {name}"))
        assert not COLUMNS & columns(connection)
        run(connection, "upgrade")
        assert COLUMNS <= columns(connection)
        run(connection, "upgrade")
        run(connection, "downgrade")
        assert not COLUMNS & columns(connection)
    finally:
        transaction.rollback()


@pytest.mark.asyncio(loop_scope="module")
async def test_retry_columns_upgrade_idempotently_and_downgrade() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(exercise)
