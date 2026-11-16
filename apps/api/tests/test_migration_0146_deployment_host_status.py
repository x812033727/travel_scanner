"""The host timer status table's DDL agrees with the model, offline and against PostgreSQL."""

from __future__ import annotations

import importlib.util
import io
import os
from pathlib import Path
from types import ModuleType
from typing import cast

import pytest
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config import get_settings
from app.deployments.models import DeploymentHostStatus

MIGRATION = "0146_deployment_host_status"
POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)
TABLE = "deployment_host_status"


def load_migration() -> ModuleType:
    path = Path(__file__).resolve().parents[1] / "migrations" / "versions" / f"{MIGRATION}.py"
    spec = importlib.util.spec_from_file_location(f"migration_{MIGRATION}", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _offline_sql() -> str:
    buffer = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": buffer}
    )
    with Operations.context(context):
        load_migration().upgrade()
    return buffer.getvalue()


def test_model_and_migration_agree() -> None:
    migration = load_migration()
    assert migration.revision == MIGRATION
    assert len(migration.revision) <= 32
    assert migration.down_revision == "0145_video_youtube_reports"
    sql = _offline_sql()
    table = cast(sa.Table, DeploymentHostStatus.__table__)
    assert f"CREATE TABLE {table.name} (" in sql
    for column in table.columns:
        assert f"    {column.name} " in sql, f"{table.name}.{column.name} is missing"
    for constraint in table.constraints:
        if constraint.name and isinstance(constraint.name, str):
            assert constraint.name in sql, f"{constraint.name} is not in the migration"


@POSTGRES
async def test_upgrade_and_downgrade_are_idempotent() -> None:
    # Its own engine, disposed here: the shared app engine would keep pooled connections bound
    # to this test's event loop, and the next module-scoped test in the shard would inherit them.
    engine = create_async_engine(get_settings().database_url)
    try:
        await _upgrade_and_downgrade(engine)
    finally:
        await engine.dispose()


async def _upgrade_and_downgrade(engine: AsyncEngine) -> None:
    migration = load_migration()

    def run(connection: sa.Connection, direction: str) -> None:
        with Operations.context(MigrationContext.configure(connection)):
            getattr(migration, direction)()

    async with engine.begin() as connection:
        await connection.run_sync(run, "upgrade")
        await connection.run_sync(run, "upgrade")
        tables = await connection.run_sync(lambda sync: sa.inspect(sync).get_table_names())
        assert TABLE in tables
        await connection.run_sync(run, "downgrade")
        await connection.run_sync(run, "downgrade")
        tables = await connection.run_sync(lambda sync: sa.inspect(sync).get_table_names())
        assert TABLE not in tables
        await connection.run_sync(run, "upgrade")
