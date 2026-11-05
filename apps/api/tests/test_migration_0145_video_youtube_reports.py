"""The channel reports' DDL agrees with the models, offline and against PostgreSQL."""

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
from app.video_youtube.models import (
    VideoYoutubeReport,
    VideoYoutubeReportJob,
    VideoYoutubeReportState,
)

MIGRATION = "0145_video_youtube_reports"
POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)
TABLES = ("video_youtube_report_jobs", "video_youtube_reports", "video_youtube_report_state")


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
    assert migration.down_revision == "0144_video_runpod_sessions"
    sql = _offline_sql()
    for model in (VideoYoutubeReportJob, VideoYoutubeReport, VideoYoutubeReportState):
        table = cast(sa.Table, model.__table__)
        assert f"CREATE TABLE {table.name} (" in sql
        for column in table.columns:
            assert f"    {column.name} " in sql, f"{table.name}.{column.name} is missing"
        for constraint in table.constraints:
            if constraint.name and isinstance(constraint.name, str):
                assert constraint.name in sql, f"{constraint.name} is not in the migration"
        for index in table.indexes:
            assert f"CREATE INDEX {index.name}" in sql
    assert "ON DELETE CASCADE" in sql


@POSTGRES
async def test_upgrade_and_downgrade_are_idempotent() -> None:
    migration = load_migration()

    def run(connection: sa.Connection, direction: str) -> None:
        with Operations.context(MigrationContext.configure(connection)):
            getattr(migration, direction)()

    async with engine.begin() as connection:
        await connection.run_sync(run, "upgrade")
        await connection.run_sync(run, "upgrade")
        tables = await connection.run_sync(lambda sync: sa.inspect(sync).get_table_names())
        assert set(TABLES) <= set(tables)
        await connection.run_sync(run, "downgrade")
        await connection.run_sync(run, "downgrade")
        tables = await connection.run_sync(lambda sync: sa.inspect(sync).get_table_names())
        assert not set(TABLES) & set(tables)
        await connection.run_sync(run, "upgrade")
