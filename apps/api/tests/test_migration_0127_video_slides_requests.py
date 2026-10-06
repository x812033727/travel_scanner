"""Exercise the slides-request DDL both offline and against an existing PostgreSQL schema."""

from __future__ import annotations

import importlib.util
import io
import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Any, cast
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
from app.video_automation.models import VideoSlidesRequest

MIGRATION = "0127_video_slides_requests"
TABLE = "video_slides_requests"
NOW = datetime(2026, 10, 5, 8, 0, tzinfo=UTC)
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
    table = cast(sa.Table, VideoSlidesRequest.__table__)
    checks = {
        str(item.sqltext) for item in table.constraints if isinstance(item, sa.CheckConstraint)
    }
    assert migration.STATUS_CHECK in checks
    uniques = {item.name for item in table.constraints if isinstance(item, sa.UniqueConstraint)}
    assert "uq_video_slides_requests_slug" in uniques, "a fresh database names it as 0127 does"
    assert migration.INDEX in {index.name for index in table.indexes}
    assert migration.revision == MIGRATION
    assert migration.down_revision == "0126_ai_income_topic"
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
        assert "CREATE TABLE video_slides_requests" in sql
        assert "source_guide VARCHAR(120) NOT NULL" in sql
        assert "ON DELETE SET NULL" in sql
        assert "fk_video_slides_requests_user" in sql and "fk_video_slides_requests_token" in sql
        assert "UNIQUE (slug)" in sql
        assert "ix_video_slides_requests_status_created" in sql
        assert "ALTER TABLE" not in sql, "no existing table changes"
    else:
        assert "DROP INDEX ix_video_slides_requests_status_created" in sql
        assert "DROP TABLE video_slides_requests" in sql


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def postgres_engine() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def _values(**changes: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "id": uuid4(),
        "source_guide": "ai-freelance-getting-started",
        "status": "queued",
        "created_at": NOW,
        "updated_at": NOW,
    }
    values.update(changes)
    return values


def exercise(connection: Connection) -> None:
    transaction = connection.begin()
    try:
        connection.execute(sa.text(f"DROP TABLE IF EXISTS {TABLE}"))
        run(connection, "upgrade")
        run(connection, "upgrade")
        with Session(bind=connection) as session:
            token = VideoToolToken(
                id=uuid4(), name="migration", token_hash=uuid4().hex, token_prefix="mkv_test"
            )
            session.add(token)
            session.flush()
            token_id = token.id
        connection.execute(sa.insert(VideoSlidesRequest).values(**_values(note="不給投資建議")))
        connection.execute(
            sa.insert(VideoSlidesRequest).values(
                **_values(
                    status="started",
                    slug="slides-1a2b3c4d",
                    started_by_token_id=token_id,
                    started_at=NOW,
                )
            )
        )
        assert connection.execute(sa.text(f"SELECT count(*) FROM {TABLE}")).scalar_one() == 2
        for values in (
            _values(status="dropped"),
            _values(source_guide=None),
            _values(slug="slides-1a2b3c4d"),
        ):
            with connection.begin_nested() as savepoint:
                with pytest.raises(IntegrityError):
                    connection.execute(sa.insert(VideoSlidesRequest).values(**values))
                savepoint.rollback()
        run(connection, "downgrade")
        assert TABLE not in sa.inspect(connection).get_table_names()
    finally:
        transaction.rollback()


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
async def test_real_upgrade_idempotence_constraints_and_downgrade(postgres_engine) -> None:
    async with engine.connect() as connection:
        await connection.run_sync(exercise)
