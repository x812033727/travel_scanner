"""0119 rebuilds the video category check so it takes anime.

Guard and offline SQL tests run without a database. The PostgreSQL test creates a temporary
video_projects table with 0116's check, shadowing the shared table in its own connection, so
it exercises the real rebuild and downgrade without touching shared rows.
"""

from __future__ import annotations

import importlib.util
import io
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
from sqlalchemy.exc import IntegrityError

from app.db import engine
from app.models import VIDEO_CATEGORIES, VIDEO_CATEGORY_CHECK

MIGRATION = "0119_video_category_anime"
PROJECTS = "video_projects"
CATEGORY_CHECK = "ck_video_project_category"
POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


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


def test_the_migration_lists_the_same_categories_as_the_model() -> None:
    migration = load_migration()
    assert migration.CATEGORIES == VIDEO_CATEGORIES
    assert migration.CHECK_TEXT == VIDEO_CATEGORY_CHECK
    assert set(migration.CATEGORIES) - set(migration.OLD_CATEGORIES) == {"anime"}
    assert len(migration.revision) <= 32


@pytest.mark.parametrize("found", [set(), {CATEGORY_CHECK}])
def test_upgrade_drops_the_check_only_when_it_is_there(
    found: set[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    migration = load_migration()
    operations = Mock()
    monkeypatch.setattr(migration, "op", operations)
    monkeypatch.setattr(migration, "_offline", lambda: False)
    monkeypatch.setattr(migration, "_checks", lambda: found)
    migration.upgrade()
    assert operations.drop_constraint.called == bool(found)
    operations.create_check_constraint.assert_called_once_with(
        CATEGORY_CHECK, PROJECTS, migration.CHECK_TEXT
    )


@pytest.mark.parametrize("direction", ["upgrade", "downgrade"])
def test_offline_sql_does_not_inspect_a_database(
    direction: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    migration = load_migration()
    monkeypatch.setattr(
        migration.sa,
        "inspect",
        lambda _connection: pytest.fail("offline SQL must not inspect a database"),
    )
    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": output}
    )
    with Operations.context(context):
        getattr(migration, direction)()
    sql = output.getvalue()
    assert f"DROP CONSTRAINT {CATEGORY_CHECK}" in sql
    assert sql.index("DROP CONSTRAINT") < sql.index("ADD CONSTRAINT")
    if direction == "upgrade":
        assert f"ADD CONSTRAINT {CATEGORY_CHECK} CHECK ({migration.CHECK_TEXT})" in sql
    else:
        assert f"UPDATE {PROJECTS} SET category = NULL WHERE category = 'anime'" in sql
        assert f"ADD CONSTRAINT {CATEGORY_CHECK} CHECK ({migration.OLD_CHECK_TEXT})" in sql
        assert sql.index("UPDATE") < sql.index("ADD CONSTRAINT"), "unfiled before it narrows"


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def postgres_engine() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def _refused(connection: Connection, slug: str, category: str) -> bool:
    savepoint = connection.begin_nested()
    try:
        connection.execute(
            sa.text(f"INSERT INTO {PROJECTS} (id, slug, category) VALUES (:id, :slug, :category)"),
            {"id": uuid4(), "slug": slug, "category": category},
        )
    except IntegrityError:
        savepoint.rollback()
        return True
    savepoint.rollback()
    return False


def _exercise(connection: Connection) -> None:
    migration = load_migration()
    with connection.begin() as transaction:
        try:
            connection.execute(
                sa.text(
                    f"CREATE TEMPORARY TABLE {PROJECTS} (id uuid PRIMARY KEY, "
                    "slug varchar(80) NOT NULL UNIQUE, category varchar(16), "
                    f"CONSTRAINT {CATEGORY_CHECK} CHECK ({migration.OLD_CHECK_TEXT})) "
                    "ON COMMIT DROP"
                )
            )
            connection.execute(
                sa.text(
                    f"INSERT INTO {PROJECTS} (id, slug, category) VALUES (:id, 'kept', 'drama')"
                ),
                {"id": uuid4()},
            )
            assert _refused(connection, "too-early", "anime")

            run(connection, "upgrade")
            run(connection, "upgrade")
            connection.execute(
                sa.text(
                    f"INSERT INTO {PROJECTS} (id, slug, category) VALUES (:id, 'toon', 'anime')"
                ),
                {"id": uuid4()},
            )
            assert _refused(connection, "bogus", "bogus")

            run(connection, "downgrade")
            filed = dict(
                connection.execute(sa.text(f"SELECT slug, category FROM {PROJECTS}")).all()
            )
            assert filed == {"kept": "drama", "toon": None}, "only the anime video is unfiled"
            assert _refused(connection, "after-down", "anime")
        finally:
            transaction.rollback()


@POSTGRES
@pytest.mark.usefixtures("postgres_engine")
@pytest.mark.asyncio(loop_scope="module")
async def test_postgresql_rebuild_and_downgrade() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(_exercise)
