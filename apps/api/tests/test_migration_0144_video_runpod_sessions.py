"""The RunPod sessions DDL agrees with the model, offline and against PostgreSQL."""

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
from app.models import VideoToolToken
from app.video_runpod.models import STOP_REASONS, VideoRunpodSession

MIGRATION = "0144_video_runpod_sessions"
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


def test_model_and_migration_agree() -> None:
    migration = load_migration()
    assert migration.revision == MIGRATION
    assert migration.down_revision == "0143_video_daily_briefs"
    assert migration.STOP_REASONS == "(" + ", ".join(f"'{item}'" for item in STOP_REASONS) + ")"
    table = cast(sa.Table, VideoRunpodSession.__table__)
    checks = {
        item.name: str(item.sqltext)
        for item in table.constraints
        if isinstance(item, sa.CheckConstraint)
    }
    assert migration.STOP_REASONS in checks["ck_video_runpod_sessions_stop_reason"]
    assert (
        checks["ck_video_runpod_sessions_stopped"] == "(stopped_at IS NULL) = (stop_reason IS NULL)"
    )
    assert {index.name for index in table.indexes} == {
        "ix_video_runpod_sessions_started_at",
        "ix_video_runpod_sessions_token_id",
    }
    assert "runpod_access" in cast(sa.Table, VideoToolToken.__table__).columns


def test_offline_sql_adds_the_flag_and_the_table() -> None:
    buffer = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": buffer}
    )
    with Operations.context(context):
        load_migration().upgrade()
    sql = buffer.getvalue()
    assert (
        "ALTER TABLE video_tool_tokens ADD COLUMN runpod_access BOOLEAN DEFAULT false NOT NULL"
        in sql
    )
    assert "CREATE TABLE video_runpod_sessions" in sql


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
        assert "video_runpod_sessions" in tables
        await connection.run_sync(run, "downgrade")
        await connection.run_sync(run, "downgrade")
        await connection.run_sync(run, "upgrade")
