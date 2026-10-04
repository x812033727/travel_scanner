"""Exercise durable receipt DDL both offline and against an existing PostgreSQL schema."""

from __future__ import annotations

import importlib.util
import io
import os
from collections.abc import AsyncIterator
from pathlib import Path
from types import ModuleType
from typing import cast
from uuid import uuid4

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import engine
from app.models import VideoToolToken
from app.video_automation.models import VideoStageJob

MIGRATION = "0123_video_stage_jobs"
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


def run(connection: Connection, direction: str) -> None:
    with Operations.context(MigrationContext.configure(connection)):
        getattr(load_migration(), direction)()


def test_model_and_migration_constraints_match() -> None:
    migration = load_migration()
    checks = {
        str(item.sqltext)
        for item in cast(sa.Table, VideoStageJob.__table__).constraints
        if isinstance(item, sa.CheckConstraint)
    }
    assert migration.STATUS_CHECK in checks and migration.RESULT_CHECK in checks
    assert migration.down_revision == "0122_video_anime_production"
    assert len(migration.revision) <= 32


@pytest.mark.parametrize("direction", ["upgrade", "downgrade"])
def test_offline_sql_is_additive_and_never_inspects(direction: str, monkeypatch) -> None:
    migration = load_migration()
    monkeypatch.setattr(
        migration.sa, "inspect", lambda _connection: pytest.fail("offline inspection")
    )
    buffer = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": buffer}
    )
    with Operations.context(context):
        getattr(migration, direction)()
    sql = buffer.getvalue()
    if direction == "upgrade":
        assert "CREATE TABLE video_stage_jobs" in sql
        assert "result_json JSON" in sql
        assert "FOREIGN KEY(token_id) REFERENCES video_tool_tokens (id) ON DELETE SET NULL" in sql
        assert "UNIQUE (token_id, request_key)" in sql
        assert "ix_video_stage_jobs_status_created" in sql
    else:
        assert "DROP TABLE video_stage_jobs" in sql


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def postgres_engine() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def exercise(connection: Connection) -> None:
    transaction = connection.begin()
    try:
        connection.execute(sa.text("DROP TABLE IF EXISTS video_stage_jobs"))
        run(connection, "upgrade")
        run(connection, "upgrade")
        with Session(bind=connection) as session:
            token = VideoToolToken(
                id=uuid4(), name="migration", token_hash=uuid4().hex, token_prefix="mkv_test"
            )
            session.add(token)
            session.flush()
            key = uuid4()
            job = VideoStageJob(
                id=uuid4(),
                token_id=token.id,
                request_key=key,
                request_hash="a" * 64,
                input_hash="b" * 64,
                request_json={"slug": "writer"},
                provider="anthropic",
                model="writer",
                status="queued",
            )
            session.add(job)
            session.flush()
            assert (
                connection.execute(
                    sa.text("SELECT result_json FROM video_stage_jobs WHERE id=:id"), {"id": job.id}
                ).scalar_one()
                is None
            )
            for values in (
                {"status": "invented"},
                {"status": "succeeded"},
                {"result_json": {"text": "must be successful"}},
            ):
                with connection.begin_nested() as savepoint:
                    with pytest.raises(IntegrityError):
                        connection.execute(
                            sa.update(VideoStageJob)
                            .where(VideoStageJob.id == job.id)
                            .values(**values)
                        )
                    savepoint.rollback()
            with connection.begin_nested() as savepoint:
                with pytest.raises(IntegrityError):
                    connection.execute(
                        sa.insert(VideoStageJob).values(
                            id=uuid4(),
                            token_id=token.id,
                            request_key=key,
                            request_hash="a" * 64,
                            input_hash="b" * 64,
                            request_json={},
                            provider="anthropic",
                            model="writer",
                            status="queued",
                        )
                    )
                savepoint.rollback()
            connection.execute(
                sa.update(VideoStageJob)
                .where(VideoStageJob.id == job.id)
                .values(status="succeeded", result_json={"text": "exact"})
            )
            assert (
                connection.execute(
                    sa.text("SELECT result_json ->> 'text' FROM video_stage_jobs WHERE id=:id"),
                    {"id": job.id},
                ).scalar_one()
                == "exact"
            )
        run(connection, "downgrade")
        assert "video_stage_jobs" not in sa.inspect(connection).get_table_names()
    finally:
        transaction.rollback()


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
async def test_real_upgrade_idempotence_constraints_and_downgrade(postgres_engine) -> None:
    async with engine.connect() as connection:
        await connection.run_sync(exercise)
