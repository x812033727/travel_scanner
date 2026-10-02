"""0120 cancels the drama requests still started for a video the owner dropped.

The offline SQL test runs without a database. The PostgreSQL test creates temporary
video_projects and video_drama_requests tables holding only the columns the backfill reads and
writes, shadowing the shared tables in its own connection, so it runs the real statement without
touching shared rows and without the NOT NULL columns whose defaults live only in Python.
"""

from __future__ import annotations

import importlib.util
import io
import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Any
from uuid import uuid4

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import Connection

from app.db import engine

MIGRATION = "0120_video_dropped_request"
REQUESTS = "video_drama_requests"
PROJECTS = "video_projects"
POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)
SEEDED = datetime(2026, 9, 1, tzinfo=UTC)
DROPPED = datetime(2026, 9, 20, 8, 30, tzinfo=UTC)
EARLIER = datetime(2026, 9, 10, tzinfo=UTC)


def load_migration() -> ModuleType:
    file = Path(__file__).resolve().parents[1] / "migrations" / "versions" / f"{MIGRATION}.py"
    spec = importlib.util.spec_from_file_location(f"migration_{MIGRATION}", file)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(connection: Connection, direction: str) -> None:
    with Operations.context(MigrationContext.configure(connection)):
        getattr(load_migration(), direction)()


def test_the_revision_follows_0119() -> None:
    migration = load_migration()
    assert migration.revision == MIGRATION
    assert migration.down_revision == "0119_video_category_anime"
    assert len(migration.revision) <= 32


def test_offline_sql_is_the_one_backfill_and_the_downgrade_is_empty() -> None:
    migration = load_migration()
    sql = {}
    for direction in ("upgrade", "downgrade"):
        output = io.StringIO()
        context = MigrationContext.configure(
            dialect_name="postgresql", opts={"as_sql": True, "output_buffer": output}
        )
        with Operations.context(context):
            getattr(migration, direction)()
        sql[direction] = output.getvalue()
    assert migration.BACKFILL in sql["upgrade"]
    assert "r.status = 'started' AND p.dropped_at IS NOT NULL" in sql["upgrade"]
    assert sql["downgrade"].strip() == ""


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def postgres_engine() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def _project(connection: Connection, slug: str, dropped_at: datetime | None) -> None:
    connection.execute(
        sa.text(f"INSERT INTO {PROJECTS} (id, slug, dropped_at) VALUES (:id, :slug, :dropped)"),
        {"id": uuid4(), "slug": slug, "dropped": dropped_at},
    )


def _request(
    connection: Connection,
    name: str,
    status: str,
    slug: str | None,
    cancelled_at: datetime | None = None,
) -> None:
    connection.execute(
        sa.text(
            f"INSERT INTO {REQUESTS} (id, name, slug, status, updated_at, cancelled_at) "
            "VALUES (:id, :name, :slug, :status, :updated, :cancelled)"
        ),
        {
            "id": uuid4(),
            "name": name,
            "slug": slug,
            "status": status,
            "updated": SEEDED,
            "cancelled": cancelled_at,
        },
    )


def _rows(connection: Connection) -> dict[str, dict[str, Any]]:
    result = connection.execute(
        sa.text(f"SELECT name, status, updated_at, cancelled_at FROM {REQUESTS}")
    )
    return {row.name: dict(row._mapping) for row in result}


def _exercise(connection: Connection) -> None:
    with connection.begin() as transaction:
        try:
            connection.execute(
                sa.text(
                    f"CREATE TEMPORARY TABLE {PROJECTS} (id uuid PRIMARY KEY, "
                    "slug varchar(80) NOT NULL UNIQUE, dropped_at timestamptz) ON COMMIT DROP"
                )
            )
            connection.execute(
                sa.text(
                    f"CREATE TEMPORARY TABLE {REQUESTS} (id uuid PRIMARY KEY, "
                    "name varchar(40) NOT NULL, slug varchar(80) UNIQUE, "
                    "status varchar(12) NOT NULL, updated_at timestamptz NOT NULL, "
                    "cancelled_at timestamptz) ON COMMIT DROP"
                )
            )
            _project(connection, "gone", DROPPED)
            _project(connection, "gone-done", DROPPED)
            _project(connection, "gone-cancelled", DROPPED)
            _project(connection, "alive", None)
            _request(connection, "started-dropped", "started", "gone")
            _request(connection, "done-dropped", "done", "gone-done")
            _request(connection, "cancelled-dropped", "cancelled", "gone-cancelled", EARLIER)
            _request(connection, "started-alive", "started", "alive")
            _request(connection, "started-no-project", "started", "nowhere")
            _request(connection, "queued", "queued", None)
            before = _rows(connection)

            run(connection, "upgrade")
            after = _rows(connection)
            cancelled = after.pop("started-dropped")
            assert cancelled["status"] == "cancelled"
            assert cancelled["cancelled_at"] == DROPPED, "cancelled when the video was dropped"
            assert cancelled["updated_at"] > SEEDED
            del before["started-dropped"]
            assert after == before, "every other request is left as it was"

            once = _rows(connection)
            run(connection, "upgrade")
            assert _rows(connection) == once, "a second run changes nothing"

            run(connection, "downgrade")
            assert _rows(connection) == once, "the downgrade changes nothing"
        finally:
            transaction.rollback()


@POSTGRES
@pytest.mark.usefixtures("postgres_engine")
@pytest.mark.asyncio(loop_scope="module")
async def test_postgresql_backfill_cancels_only_started_requests_of_dropped_videos() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(_exercise)
