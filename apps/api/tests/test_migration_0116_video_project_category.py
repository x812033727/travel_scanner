"""0116 adds the video category, its constraint, and files the rows two rules can name.

Guard and offline SQL tests run without a database. The PostgreSQL test creates a temporary
pre-0116 video_projects table, shadowing the shared table in its own connection, so it
exercises the real ALTER, the backfill and the constraint without touching shared rows.
"""

from __future__ import annotations

import importlib.util
import io
import os
from collections.abc import AsyncIterator
from pathlib import Path
from types import ModuleType, SimpleNamespace
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

MIGRATION = "0116_video_project_category"
PROJECTS = "video_projects"
CATEGORY_CHECK = "ck_video_project_category"
POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


def load_migration(name: str = MIGRATION) -> ModuleType:
    file = Path(__file__).resolve().parents[1] / "migrations" / "versions" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"migration_{name}", file)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(connection: Connection, direction: str) -> None:
    with Operations.context(MigrationContext.configure(connection)):
        getattr(load_migration(), direction)()


def test_the_migration_lists_the_categories_0119_widens() -> None:
    migration = load_migration()
    later = load_migration("0119_video_category_anime")
    assert migration.CATEGORIES == later.OLD_CATEGORIES
    assert migration.CHECK_TEXT == later.OLD_CHECK_TEXT
    assert len(migration.revision) <= 32


def test_current_model_shape_needs_no_schema_changes(monkeypatch: pytest.MonkeyPatch) -> None:
    migration = load_migration()
    operations = Mock()
    monkeypatch.setattr(migration, "op", operations)
    monkeypatch.setattr(migration, "_offline", lambda: False)
    monkeypatch.setattr(migration, "_columns", lambda: {"category"})
    monkeypatch.setattr(migration, "_checks", lambda: {CATEGORY_CHECK})
    migration.upgrade()
    assert operations.mock_calls == []


def test_a_missing_constraint_is_added_without_refiling_the_rows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    migration = load_migration()
    operations = Mock()
    monkeypatch.setattr(migration, "op", operations)
    monkeypatch.setattr(migration, "_offline", lambda: False)
    monkeypatch.setattr(migration, "_columns", lambda: {"category"})
    monkeypatch.setattr(migration, "_checks", lambda: set())
    migration.upgrade()
    operations.create_check_constraint.assert_called_once_with(
        CATEGORY_CHECK, PROJECTS, migration.CHECK_TEXT
    )
    operations.add_column.assert_not_called()
    operations.execute.assert_not_called()


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
    if direction == "upgrade":
        assert f"ALTER TABLE {PROJECTS} ADD COLUMN category VARCHAR(16)" in sql
        assert f"ADD CONSTRAINT {CATEGORY_CHECK} CHECK ({migration.CHECK_TEXT})" in sql
        assert sql.count(f"UPDATE {PROJECTS} SET category=") == 4
        assert f"SET category='story' WHERE {PROJECTS}.category IS NULL" in sql
        assert "IN (SELECT video_drama_series.slug" in sql and "kind = 'story'" in sql
        assert f"SET category='drama' WHERE {PROJECTS}.category IS NULL" in sql
        assert f"SET category='ai-news' WHERE {PROJECTS}.category IS NULL" in sql
        assert f"substr({PROJECTS}.source_guide, 1, 8) = 'ai-news-'" in sql
        assert f"substr({PROJECTS}.slug, 1, 8) = 'ai-term-'" in sql
        assert sql.index("category='story'") < sql.index("category='drama'"), "stories first"
        assert "%(" not in sql, "the constants are rendered inline, not as bind parameters"
        assert sql.index("ADD CONSTRAINT") < sql.index("UPDATE"), "the rows are filed under it"
    else:
        assert f"DROP CONSTRAINT {CATEGORY_CHECK}" in sql
        assert f"ALTER TABLE {PROJECTS} DROP COLUMN category" in sql
        assert sql.index("DROP CONSTRAINT") < sql.index("DROP COLUMN")


def test_offline_mode_uses_the_operations_context(monkeypatch: pytest.MonkeyPatch) -> None:
    migration = load_migration()
    monkeypatch.setattr(migration.op, "get_context", lambda: SimpleNamespace(as_sql=True))
    assert migration._offline() is True


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def postgres_engine() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def _checks(connection: Connection) -> set[str]:
    return {str(c["name"]) for c in sa.inspect(connection).get_check_constraints(PROJECTS)}


def _exercise(connection: Connection) -> None:
    with connection.begin() as transaction:
        try:
            connection.execute(
                sa.text(
                    f"CREATE TEMPORARY TABLE {PROJECTS} ("
                    "id uuid PRIMARY KEY, slug varchar(80) NOT NULL UNIQUE, "
                    "title varchar(200) NOT NULL, format varchar(8) NOT NULL DEFAULT 'slides', "
                    "shorts_line varchar(8), series_slug varchar(40), source_guide varchar(120)) "
                    "ON COMMIT DROP"
                )
            )
            # Shadows the shared series table too: one brand-story series the story rule reads.
            connection.execute(
                sa.text(
                    "CREATE TEMPORARY TABLE video_drama_series (slug varchar(40) PRIMARY KEY, "
                    "kind varchar(12) NOT NULL) ON COMMIT DROP"
                )
            )
            connection.execute(
                sa.text(
                    "INSERT INTO video_drama_series (slug, kind) VALUES "
                    "('brand-stories', 'story'), ('wenjian', 'series')"
                )
            )
            rows = {
                "ai-term-token": "ai-terms",
                "gemini-student-offer": "ai-news",
                "ai-model-choice": None,
                "brellco-umbrellas": "story",
                "wenjian-ep-01": "drama",
                "wenjian-ep-01-short-1": None,
            }
            connection.execute(
                sa.text(
                    f"INSERT INTO {PROJECTS} "
                    "(id, slug, title, format, shorts_line, series_slug, source_guide) VALUES "
                    "(:a, 'ai-term-token', 'Token', 'slides', NULL, NULL, NULL), "
                    "(:b, 'gemini-student-offer', '學生方案', 'slides', NULL, NULL, "
                    "'ai-news-gemini-student-offer-20260820'), "
                    "(:c, 'ai-model-choice', 'AI 模型怎麼挑', 'slides', NULL, NULL, "
                    "'ai-model-choice-guide'), "
                    "(:d, 'brellco-umbrellas', '折疊傘', 'drama', NULL, 'brand-stories', NULL), "
                    "(:e, 'wenjian-ep-01', '問劍 第一集', 'drama', NULL, 'wenjian', NULL), "
                    "(:f, 'wenjian-ep-01-short-1', '問劍 短片', 'drama', 'drama', 'wenjian', NULL)"
                ),
                {key: uuid4() for key in "abcdef"},
            )
            run(connection, "upgrade")
            run(connection, "upgrade")
            filed = {
                str(slug): category
                for slug, category in connection.execute(
                    sa.text(f"SELECT slug, category FROM {PROJECTS}")
                ).all()
            }
            assert filed == rows, "the four rules file four rows; a Short and a plain tutorial wait"
            assert CATEGORY_CHECK in _checks(connection)
            with pytest.raises(IntegrityError):
                with connection.begin_nested():
                    connection.execute(
                        sa.text(
                            f"INSERT INTO {PROJECTS} (id, slug, title, category) "
                            "VALUES (:id, 'bogus', 'b', 'bogus')"
                        ),
                        {"id": uuid4()},
                    )
            connection.execute(
                sa.text(
                    f"UPDATE {PROJECTS} SET category = 'tutorial' WHERE slug = 'ai-model-choice'"
                )
            )
            run(connection, "upgrade")
            assert (
                connection.execute(
                    sa.text(f"SELECT category FROM {PROJECTS} WHERE slug = 'ai-model-choice'")
                ).scalar()
                == "tutorial"
            ), "a category the owner set survives another run"
            run(connection, "downgrade")
            assert "category" not in {
                column["name"] for column in sa.inspect(connection).get_columns(PROJECTS)
            }
            assert CATEGORY_CHECK not in _checks(connection)
        finally:
            transaction.rollback()


@POSTGRES
@pytest.mark.usefixtures("postgres_engine")
@pytest.mark.asyncio(loop_scope="module")
async def test_postgresql_backfill_constraint_and_downgrade() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(_exercise)
