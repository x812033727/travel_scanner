"""More than one linked channel: the DDL agrees with the models, offline and against PostgreSQL."""

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
from app.models import VideoProject, VideoYoutubeConnection
from app.video_youtube.models import VideoYoutubeReportState

MIGRATION = "0147_video_youtube_channels"
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


def _offline(direction: str) -> str:
    buffer = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": buffer}
    )
    with Operations.context(context):
        getattr(load_migration(), direction)()
    return buffer.getvalue()


def _names(model: type) -> set[str]:
    table = cast(sa.Table, model.__table__)  # type: ignore[attr-defined]
    return {str(item.name) for item in table.constraints if isinstance(item.name, str)}


def test_model_and_migration_agree() -> None:
    migration = load_migration()
    assert migration.revision == MIGRATION
    assert len(migration.revision) <= 32
    assert migration.down_revision == "0146_deployment_host_status"
    sql = _offline("upgrade")
    assert "DROP CONSTRAINT ck_video_youtube_connection_single" in sql
    assert "DROP CONSTRAINT ck_video_youtube_report_state_single" in sql
    assert "ADD COLUMN key VARCHAR(32) DEFAULT 'default' NOT NULL" in sql
    assert "ADD COLUMN label VARCHAR(80)" in sql
    assert "ADD COLUMN youtube_channel_key VARCHAR(32)" in sql
    assert "ADD COLUMN channel_id VARCHAR(64)" in sql
    for name in ("uq_video_youtube_connections_key", "uq_video_youtube_report_state_channel_id"):
        assert name in sql
    assert "uq_video_youtube_connections_key" in _names(VideoYoutubeConnection)
    assert "uq_video_youtube_report_state_channel_id" in _names(VideoYoutubeReportState)
    assert "ck_video_youtube_connection_single" not in _names(VideoYoutubeConnection)
    assert "ck_video_youtube_report_state_single" not in _names(VideoYoutubeReportState)
    columns = cast(sa.Table, VideoProject.__table__).columns
    assert columns["youtube_channel_key"].nullable
    assert "jsonb" not in sql.lower()


def test_the_downgrade_goes_back_to_one_row() -> None:
    sql = _offline("downgrade")
    assert "DELETE FROM video_youtube_connections WHERE id <> 1" in sql
    assert "ck_video_youtube_connection_single CHECK (id = 1)" in sql
    assert "ck_video_youtube_report_state_single CHECK (id = 1)" in sql


@POSTGRES
async def test_upgrade_and_downgrade_are_idempotent_and_keep_the_linked_channel() -> None:
    migration = load_migration()

    def run(connection: sa.Connection, direction: str) -> None:
        with Operations.context(MigrationContext.configure(connection)):
            getattr(migration, direction)()

    async with engine.begin() as connection:
        await connection.run_sync(run, "downgrade")
        await connection.run_sync(run, "downgrade")
        await connection.execute(sa.text("DELETE FROM video_youtube_connections"))
        await connection.execute(
            sa.text(
                "INSERT INTO video_youtube_connections (id, channel_id, audited, created_at, "
                "updated_at) VALUES (1, 'UCbefore', false, now(), now())"
            )
        )
        await connection.run_sync(run, "upgrade")
        await connection.run_sync(run, "upgrade")
        key = await connection.scalar(
            sa.text("SELECT key FROM video_youtube_connections WHERE id = 1")
        )
        assert key == "default"
        await connection.execute(
            sa.text(
                "INSERT INTO video_youtube_connections (key, audited, created_at, updated_at) "
                "VALUES ('theater', false, now(), now())"
            )
        )
        await connection.run_sync(run, "downgrade")
        left = await connection.scalar(sa.text("SELECT count(*) FROM video_youtube_connections"))
        assert left == 1
        await connection.run_sync(run, "upgrade")
        await connection.execute(sa.text("DELETE FROM video_youtube_connections"))
