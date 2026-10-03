"""Exercise additive old-schema upgrade and real JSON CHECK enforcement on PostgreSQL."""

from __future__ import annotations

import importlib.util
import io
import json
import os
from collections.abc import AsyncIterator
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock
from uuid import uuid4

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import Connection
from sqlalchemy.exc import DBAPIError

from app.db import engine
from app.video_automation.models import (
    SERIES_ANIME_POLICY_CHECK,
    SERIES_ANIME_RUNTIME_CHECK,
    SERIES_LEAD_CHECK,
    SERIES_NUMBERS_CHECK,
)

MIGRATION = "0122_video_anime_production_policy"
RUNTIME = {
    "body_target_seconds": 1320,
    "op_ed_budget_seconds": 180,
    "broadcast_slot_seconds": 1800,
    "slot_reserve_seconds": 300,
}
POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


def load_migration() -> ModuleType:
    file = Path(__file__).resolve().parents[1] / "migrations" / "versions" / f"{MIGRATION}.py"
    spec = importlib.util.spec_from_file_location(f"migration_{MIGRATION}", file)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(connection: Connection, direction: str) -> None:
    with Operations.context(MigrationContext.configure(connection)):
        getattr(load_migration(), direction)()


def test_model_checks_match_pinned_migration() -> None:
    migration = load_migration()
    assert len(migration.revision) <= 32
    assert migration.down_revision == "0121_video_series_planning"
    assert migration.NUMBERS_CHECK == SERIES_NUMBERS_CHECK
    assert migration.LEAD_CHECK == SERIES_LEAD_CHECK
    assert migration.POLICY_CHECK == SERIES_ANIME_POLICY_CHECK
    assert migration.RUNTIME_CHECK == SERIES_ANIME_RUNTIME_CHECK


@pytest.mark.parametrize("present", [False, True])
def test_upgrade_adds_only_missing_columns(present: bool, monkeypatch: pytest.MonkeyPatch) -> None:
    migration = load_migration()
    operations = Mock()
    monkeypatch.setattr(migration, "op", operations)
    monkeypatch.setattr(
        migration, "_columns", lambda: {"production_policy", "runtime_spec"} if present else set()
    )
    monkeypatch.setattr(
        migration,
        "_checks",
        lambda: {migration.NUMBERS, migration.LEAD, migration.POLICY, migration.RUNTIME},
    )
    migration.upgrade()
    assert operations.add_column.call_count == (0 if present else 2)
    assert operations.drop_constraint.call_count == 4
    assert operations.create_check_constraint.call_count == 4


@pytest.mark.parametrize("direction", ["upgrade", "downgrade"])
def test_offline_sql_never_inspects(direction: str, monkeypatch: pytest.MonkeyPatch) -> None:
    migration = load_migration()
    monkeypatch.setattr(
        migration.sa, "inspect", lambda _connection: pytest.fail("offline must not inspect")
    )
    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": output}
    )
    with Operations.context(context):
        getattr(migration, direction)()
    sql = output.getvalue()
    if direction == "upgrade":
        assert "ADD COLUMN runtime_spec JSON" in sql
        assert "ADD COLUMN production_policy VARCHAR(32)" in sql
        assert migration.RUNTIME_CHECK in sql.replace("%%", "%")
    else:
        assert sql.index("RAISE EXCEPTION") < sql.index("DROP CONSTRAINT")


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def postgres_engine() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def refused(connection: Connection, sql: str, values: dict[str, object]) -> bool:
    savepoint = connection.begin_nested()
    try:
        connection.execute(sa.text(sql), values)
    except DBAPIError:
        savepoint.rollback()
        return True
    savepoint.rollback()
    return False


def exercise(connection: Connection) -> None:
    migration = load_migration()
    transaction = connection.begin()
    try:
        connection.execute(
            sa.text(
                "CREATE TEMPORARY TABLE video_drama_series (id uuid PRIMARY KEY, "
                "slug varchar(40) NOT NULL UNIQUE, kind varchar(12) NOT NULL DEFAULT 'series', "
                "status varchar(12) NOT NULL DEFAULT 'active', "
                "planned_episodes integer NOT NULL DEFAULT 120, "
                "episodes_per_chapter integer NOT NULL DEFAULT 12, "
                "target_minutes integer NOT NULL DEFAULT 8, "
                "lead varchar(12) NOT NULL DEFAULT 'male', "
                "planning_only boolean NOT NULL DEFAULT false, category varchar(24), "
                "planning_spec json, style_preset varchar(24) NOT NULL DEFAULT 'cinematic-3d', "
                "genre varchar(32) NOT NULL DEFAULT 'custom', total_minutes integer, "
                "hands_off boolean NOT NULL DEFAULT false, "
                "compilation boolean NOT NULL DEFAULT false, "
                "force_next boolean NOT NULL DEFAULT false, requested_chapter integer, "
                f"CONSTRAINT {migration.NUMBERS} CHECK ({migration.OLD_NUMBERS_CHECK}), "
                f"CONSTRAINT {migration.LEAD} CHECK ({migration.OLD_LEAD_CHECK}), "
                "CONSTRAINT ck_video_drama_series_planning CHECK (planning_only = false OR "
                "(kind='series' AND category='anime' AND status='paused' AND hands_off=false "
                "AND compilation=false AND force_next=false AND requested_chapter IS NULL))) "
                "ON COMMIT DROP"
            )
        )
        connection.execute(
            sa.text("INSERT INTO video_drama_series(id, slug) VALUES (:id, 'ordinary')"),
            {"id": uuid4()},
        )
        connection.execute(
            sa.text(
                "INSERT INTO video_drama_series(id, slug, planning_only, category, status, "
                "target_minutes, lead, planning_spec) VALUES (:id, 'locked-plan', true, 'anime', "
                "'paused', 22, 'ensemble', CAST(:planning AS json))"
            ),
            {"id": uuid4(), "planning": '{"original":true}'},
        )
        run(connection, "upgrade")
        run(connection, "upgrade")
        assert connection.execute(
            sa.text(
                "SELECT production_policy, runtime_spec, target_minutes, lead "
                "FROM video_drama_series WHERE slug='ordinary'"
            )
        ).one() == (None, None, 8, "male")
        assert connection.execute(
            sa.text(
                "SELECT planning_only, production_policy, target_minutes, lead, planning_spec "
                "FROM video_drama_series WHERE slug='locked-plan'"
            )
        ).one() == (True, None, 22, "ensemble", {"original": True})
        connection.execute(
            sa.text(
                "INSERT INTO video_drama_series(id, slug, production_policy, runtime_spec, "
                "category, style_preset, target_minutes, lead, status) VALUES (:id, 'long-anime', "
                "'long-anime-v1', CAST(:runtime AS json), 'anime', 'anime-2d', "
                "22, 'ensemble', 'paused')"
            ),
            {"id": uuid4(), "runtime": json.dumps(RUNTIME)},
        )
        for column, value in (
            ("production_policy", None),
            ("production_policy", "fake"),
            ("category", None),
            ("category", "drama"),
            ("kind", "one-off"),
            ("genre", "custom-other"),
            ("style_preset", "cinematic-3d"),
            ("lead", "male"),
            ("hands_off", True),
            ("compilation", True),
            ("total_minutes", 120),
            ("planning_only", True),
            ("target_minutes", 21),
            ("target_minutes", 31),
        ):
            assert refused(
                connection,
                f"UPDATE video_drama_series SET {column}=:value WHERE slug='long-anime'",
                {"value": value},
            ), (column, value)
        for column, value in (("target_minutes", 22), ("lead", "ensemble")):
            assert refused(
                connection,
                f"UPDATE video_drama_series SET {column}=:value WHERE slug='ordinary'",
                {"value": value},
            )
        bad_runtimes: list[object] = [
            None,
            {},
            [],
            {**RUNTIME, "body_target_seconds": "1320"},
            {**RUNTIME, "body_target_seconds": 1320.0},
            {**RUNTIME, "body_target_seconds": True},
            {**RUNTIME, "body_target_seconds": 1321},
            {**RUNTIME, "op_ed_budget_seconds": 301},
            {**RUNTIME, "slot_reserve_seconds": 901},
            {**RUNTIME, "broadcast_slot_seconds": 1799},
        ]
        for runtime in bad_runtimes:
            assert refused(
                connection,
                "UPDATE video_drama_series SET runtime_spec=CAST(:value AS json) "
                "WHERE slug='long-anime'",
                {"value": json.dumps(runtime)},
            ), runtime
        with pytest.raises(RuntimeError, match="must be preserved"):
            run(connection, "downgrade")
        connection.execute(sa.text("DELETE FROM video_drama_series WHERE slug='long-anime'"))
        run(connection, "downgrade")
        columns = {column["name"] for column in sa.inspect(connection).get_columns(migration.TABLE)}
        assert not {"production_policy", "runtime_spec"} & columns
        assert connection.execute(
            sa.text(
                "SELECT planning_only, target_minutes, lead FROM video_drama_series WHERE "
                "slug='locked-plan'"
            )
        ).one() == (True, 22, "ensemble")
        assert refused(
            connection, "UPDATE video_drama_series SET target_minutes=22 WHERE slug='ordinary'", {}
        )
    finally:
        transaction.rollback()


@POSTGRES
@pytest.mark.usefixtures("postgres_engine")
@pytest.mark.asyncio(loop_scope="module")
async def test_real_old_schema_checks_and_safe_downgrade() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(exercise)
