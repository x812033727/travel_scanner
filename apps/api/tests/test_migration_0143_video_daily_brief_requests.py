"""Exercise the daily brief DDL both offline and against an existing PostgreSQL schema."""

from __future__ import annotations

import importlib.util
import io
import json
import os
from collections.abc import AsyncIterator
from datetime import UTC, date, datetime
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

from app.db import engine
from app.video_automation.models import (
    DAILY_BRIEF_CHECK,
    DEFAULT_DAILY_BRIEF_LOCALES,
    VideoAutomationSettings,
    VideoDailyBriefRequest,
)

MIGRATION = "0143_video_daily_brief_requests"
TABLE = "video_daily_brief_requests"
SETTINGS = "video_automation_settings"
COLUMNS = (
    "daily_brief_enabled",
    "daily_brief_hour",
    "daily_brief_min_stories",
    "daily_brief_locales",
)
NOW = datetime(2026, 10, 29, 1, 0, tzinfo=UTC)
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


def test_model_and_migration_agree() -> None:
    migration = load_migration()
    table = cast(sa.Table, VideoDailyBriefRequest.__table__)
    checks = {
        str(item.sqltext) for item in table.constraints if isinstance(item, sa.CheckConstraint)
    }
    assert migration.STATUS_CHECK in checks
    uniques = {item.name for item in table.constraints if isinstance(item, sa.UniqueConstraint)}
    assert {
        "uq_video_daily_brief_requests_news_date",
        "uq_video_daily_brief_requests_slug",
    } <= uniques, "a fresh database names them as 0143 does"
    assert migration.INDEX in {index.name for index in table.indexes}
    settings = cast(sa.Table, VideoAutomationSettings.__table__)
    named = {
        item.name: str(item.sqltext)
        for item in settings.constraints
        if isinstance(item, sa.CheckConstraint)
    }
    assert named[migration.SETTINGS_CHECK_NAME] == migration.SETTINGS_CHECK == DAILY_BRIEF_CHECK
    assert json.loads(migration.DEFAULT_LOCALES) == DEFAULT_DAILY_BRIEF_LOCALES
    assert set(COLUMNS) <= set(settings.columns.keys())
    assert migration.revision == "0143_video_daily_briefs"
    assert migration.down_revision == "0142_video_tool_token_colab"
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
        assert "CREATE TABLE video_daily_brief_requests" in sql
        assert "news_date DATE NOT NULL" in sql and "source_guides JSON NOT NULL" in sql
        assert "fk_video_daily_brief_requests_token" in sql and "ON DELETE SET NULL" in sql
        assert "UNIQUE (news_date)" in sql and "UNIQUE (slug)" in sql
        assert "ix_video_daily_brief_requests_status_date" in sql
        for column in COLUMNS:
            assert f"ADD COLUMN {column}" in sql
        assert "daily_brief_hour INTEGER DEFAULT '9' NOT NULL" in sql
        assert "ADD CONSTRAINT ck_video_daily_brief CHECK" in sql
        assert "jsonb" not in sql.lower()
    else:
        assert "DROP CONSTRAINT ck_video_daily_brief" in sql
        for column in COLUMNS:
            assert f"DROP COLUMN {column}" in sql
        assert "DROP TABLE video_daily_brief_requests" in sql


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def postgres_engine() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def _values(**changes: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "id": uuid4(),
        "news_date": date(2026, 10, 28),
        "slug": "daily-ai-20261028",
        "source_guides": ["ai-news-a", "tech-news-b"],
        "status": "queued",
        "created_at": NOW,
        "updated_at": NOW,
    }
    values.update(changes)
    return values


def _settings_columns(connection: Connection) -> set[str]:
    return {column["name"] for column in sa.inspect(connection).get_columns(SETTINGS)}


def exercise(connection: Connection) -> None:
    transaction = connection.begin()
    try:
        # The shape before 0143: no table, no columns, no check.
        connection.execute(sa.text(f"DROP TABLE IF EXISTS {TABLE}"))
        connection.execute(
            sa.text(f"ALTER TABLE {SETTINGS} DROP CONSTRAINT IF EXISTS ck_video_daily_brief")
        )
        for column in COLUMNS:
            connection.execute(sa.text(f"ALTER TABLE {SETTINGS} DROP COLUMN IF EXISTS {column}"))
        connection.execute(sa.text(f"DELETE FROM {SETTINGS}"))
        run(connection, "upgrade")
        run(connection, "upgrade")
        assert set(COLUMNS) <= _settings_columns(connection)
        # An existing settings row reads the defaults the previous release never wrote.
        connection.execute(sa.insert(VideoAutomationSettings).values(id=1))
        connection.execute(
            sa.text(
                f"UPDATE {SETTINGS} SET daily_brief_enabled = DEFAULT, daily_brief_hour = DEFAULT,"
                " daily_brief_min_stories = DEFAULT, daily_brief_locales = DEFAULT"
            )
        )
        enabled, hour, minimum, locales = connection.execute(
            sa.text(
                "SELECT daily_brief_enabled, daily_brief_hour, daily_brief_min_stories,"
                f" daily_brief_locales FROM {SETTINGS}"
            )
        ).one()
        assert (enabled, hour, minimum) == (False, 9, 5)
        assert locales == DEFAULT_DAILY_BRIEF_LOCALES
        for bad in ("daily_brief_hour = 24", "daily_brief_min_stories = 0"):
            with connection.begin_nested() as savepoint:
                with pytest.raises(IntegrityError):
                    connection.execute(sa.text(f"UPDATE {SETTINGS} SET {bad}"))
                savepoint.rollback()
        connection.execute(sa.insert(VideoDailyBriefRequest).values(**_values()))
        for values in (
            _values(status="dropped", news_date=date(2026, 10, 27), slug="daily-ai-20261027"),
            _values(slug="daily-ai-other"),
            _values(news_date=date(2026, 10, 26)),
        ):
            with connection.begin_nested() as savepoint:
                with pytest.raises(IntegrityError):
                    connection.execute(sa.insert(VideoDailyBriefRequest).values(**values))
                savepoint.rollback()
        run(connection, "downgrade")
        assert TABLE not in sa.inspect(connection).get_table_names()
        assert not set(COLUMNS) & _settings_columns(connection)
        run(connection, "downgrade")
    finally:
        transaction.rollback()


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
async def test_real_upgrade_idempotence_constraints_and_downgrade(postgres_engine) -> None:
    async with engine.connect() as connection:
        await connection.run_sync(exercise)
