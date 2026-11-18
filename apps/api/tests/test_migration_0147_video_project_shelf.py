"""The show and topic columns' DDL agrees with the model, offline and against PostgreSQL."""

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

from app.db import engine
from app.models import VideoProject

MIGRATION = "0147_video_project_shelf"
POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


def load_migration() -> ModuleType:
    path = Path(__file__).resolve().parents[1] / "migrations" / "versions" / f"{MIGRATION}.py"
    spec = importlib.util.spec_from_file_location(f"migration_{MIGRATION}", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _offline_sql(direction: str = "upgrade") -> str:
    buffer = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": buffer}
    )
    with Operations.context(context):
        getattr(load_migration(), direction)()
    return buffer.getvalue()


def test_model_and_migration_agree() -> None:
    migration = load_migration()
    assert migration.revision == MIGRATION
    assert len(migration.revision) <= 32
    assert migration.down_revision == "0146_deployment_host_status"
    sql = _offline_sql()
    table = cast(sa.Table, VideoProject.__table__)
    for name in ("series_key", "topic"):
        column = table.c[name]
        assert column.nullable
        assert isinstance(column.type, sa.String)
        assert f"ADD COLUMN {name} VARCHAR({column.type.length})" in sql
    assert "CREATE INDEX ix_video_projects_series_key ON video_projects (series_key)" in sql
    assert {index.name for index in table.indexes} >= {"ix_video_projects_series_key"}
    down = _offline_sql("downgrade")
    assert "DROP INDEX ix_video_projects_series_key" in down
    assert "DROP COLUMN topic" in down and "DROP COLUMN series_key" in down


@POSTGRES
async def test_upgrade_and_downgrade_are_idempotent() -> None:
    migration = load_migration()

    def run(connection: sa.Connection, direction: str) -> None:
        with Operations.context(MigrationContext.configure(connection)):
            getattr(migration, direction)()

    def columns(sync: sa.Connection) -> set[str]:
        return {column["name"] for column in sa.inspect(sync).get_columns("video_projects")}

    async with engine.begin() as connection:
        await connection.run_sync(run, "upgrade")
        await connection.run_sync(run, "upgrade")
        assert {"series_key", "topic"} <= await connection.run_sync(columns)
        await connection.run_sync(run, "downgrade")
        await connection.run_sync(run, "downgrade")
        assert not {"series_key", "topic"} & await connection.run_sync(columns)
        await connection.run_sync(run, "upgrade")
    await engine.dispose()
