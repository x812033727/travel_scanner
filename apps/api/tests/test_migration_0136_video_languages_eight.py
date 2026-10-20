"""0136 pre-ticks all eight languages in the settings row's two default lists.

``0001_initial`` builds a fresh database from the current models, whose defaults are already the
eight, so the rewrite only matters in production, where the row stores ``["en", "ja", "ko"]``.
The PostgreSQL test plants the old lists, runs the migration through a real alembic context and
checks both directions inside one rolled back transaction, the way
``test_migration_0128_video_languages_four`` does. The offline test reads the SQL the migration
would write to a file.
"""

from __future__ import annotations

import importlib.util
import io
import os
from collections.abc import AsyncIterator, Callable
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import Connection

from app.db import engine
from app.video_automation.models import (
    DEFAULT_CAPTION_LOCALES,
    DEFAULT_DRAMA,
    VideoAutomationSettings,
)
from app.video_automation.schemas import CAPTION_LOCALES
from app.video_reviews.schemas import DUB_LOCALES, IMPORTED_DUB_LOCALES
from tests.test_migration_sql_dialect import offenders_in

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0136_video_languages_eight"
AUTOMATION = "video_automation_settings"
EIGHT = ["en", "ja", "ko", "es", "pt", "id", "vi", "th"]
POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


def load_migration() -> ModuleType:
    path = VERSIONS / f"{MIGRATION}.py"
    spec = importlib.util.spec_from_file_location(f"migration_{MIGRATION}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(connection: Connection, direction: str) -> None:
    context = MigrationContext.configure(connection)
    with Operations.context(context):
        getattr(load_migration(), direction)()


def offline_sql(direction: str) -> str:
    buffer = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": buffer}
    )
    with Operations.context(context):
        getattr(load_migration(), direction)()
    return buffer.getvalue()


def test_the_migration_writes_what_the_models_and_schemas_now_default_to() -> None:
    migration = load_migration()
    assert migration.revision == MIGRATION
    assert migration.down_revision == "0135_video_backup"
    assert len(migration.revision) <= 32
    assert list(migration.EIGHT) == EIGHT == DEFAULT_CAPTION_LOCALES
    assert list(migration.EIGHT) == list(CAPTION_LOCALES) == list(DUB_LOCALES)
    assert DEFAULT_DRAMA["drama_caption_locales"] == EIGHT
    assert migration.FIVE == IMPORTED_DUB_LOCALES
    server_default = VideoAutomationSettings.__table__.c.drama_caption_locales.server_default
    assert server_default is not None
    assert str(cast(Any, server_default).arg) == f"'{migration.EIGHT_JSON}'"


def test_offline_sql_writes_the_eight_and_restores_with_json_functions_only() -> None:
    upgrade = offline_sql("upgrade")
    eight = '\'["en", "ja", "ko", "es", "pt", "id", "vi", "th"]\'::json'
    assert f"UPDATE {AUTOMATION} SET caption_locales = {eight}, " in upgrade
    assert f"drama_caption_locales = {eight}" in upgrade
    assert "ALTER COLUMN drama_caption_locales SET DEFAULT" in upgrade
    downgrade = offline_sql("downgrade")
    for column in ("caption_locales", "drama_caption_locales"):
        assert f"UPDATE {AUTOMATION} SET {column} = COALESCE(" in downgrade, column
    assert "ALTER COLUMN drama_caption_locales SET DEFAULT '[]'" in downgrade
    for sql in (upgrade, downgrade):
        assert "::jsonb" not in sql and "jsonb_" not in sql
    assert not offenders_in([(f"{MIGRATION}.py", (VERSIONS / f"{MIGRATION}.py").read_text())])


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def dispose_engine_after_module() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def in_a_rolled_back_transaction(
    exercise: Callable[[Connection], None],
) -> Callable[[Connection], None]:
    def runner(connection: Connection) -> None:
        transaction = connection.begin()
        try:
            exercise(connection)
        finally:
            transaction.rollback()

    return runner


def _lists(connection: Connection) -> tuple[Any, Any]:
    captions, drama = connection.execute(
        sa.text(f"SELECT caption_locales, drama_caption_locales FROM {AUTOMATION} WHERE id = 1")
    ).one()
    return captions, drama


def _plant(connection: Connection, captions: str, drama: str) -> None:
    connection.execute(
        sa.text(
            f"UPDATE {AUTOMATION} SET caption_locales = :captions, "
            "drama_caption_locales = :drama WHERE id = 1"
        ),
        {"captions": captions, "drama": drama},
    )


def _exercise(connection: Connection) -> None:
    table = cast(sa.Table, VideoAutomationSettings.__table__)
    present = connection.execute(sa.text(f"SELECT count(*) FROM {AUTOMATION} WHERE id = 1"))
    if not present.scalar():
        # The model's defaults fill a fresh row; the transaction rolls it back.
        connection.execute(sa.insert(table).values(id=1))
    _plant(connection, '["en", "ja", "ko"]', "[]")

    run(connection, "upgrade")
    assert _lists(connection) == (EIGHT, EIGHT)
    # Idempotent: a second upgrade writes the same lists.
    run(connection, "upgrade")
    assert _lists(connection) == (EIGHT, EIGHT)

    run(connection, "downgrade")
    assert _lists(connection) == (["en", "ja", "ko"], ["en", "ja", "ko"])
    # The downgrade keeps the other languages in their order, leaves a list without the five
    # alone, and leaves a list of only the five empty, not NULL.
    _plant(connection, '["th", "ko", "es", "en"]', '["vi", "pt"]')
    run(connection, "downgrade")
    assert _lists(connection) == (["ko", "en"], [])
    run(connection, "downgrade")
    assert _lists(connection) == (["ko", "en"], [])


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_pre_ticks_the_eight_and_downgrade_drops_the_five(
    dispose_engine_after_module: None,
) -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
