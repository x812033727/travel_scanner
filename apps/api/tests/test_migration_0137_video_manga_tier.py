"""0137 widens ``ck_video_drama_series_tier`` to the four tiers, ``manga`` included.

``0001_initial`` builds a fresh database from the current models, whose check already names the
four, so the migration matters in production, where 0103 left the narrow one. The offline test
reads the SQL the migration would write to a file; the PostgreSQL test plants the narrow check,
runs both directions through a real alembic context inside one rolled back transaction, and
reads the constraint's definition back each time.
"""

from __future__ import annotations

import importlib.util
import io
import os
from collections.abc import AsyncIterator, Callable
from pathlib import Path
from types import ModuleType

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import Connection

from app.db import engine
from app.video_automation.models import VISUAL_TIERS
from app.video_automation.schemas import DramaRequestIn, SeriesIn
from tests.test_migration_sql_dialect import offenders_in

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0137_video_manga_tier"
SERIES = "video_drama_series"
CHECK = "ck_video_drama_series_tier"
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


def test_the_migration_names_the_tiers_the_models_and_schemas_know() -> None:
    migration = load_migration()
    assert migration.revision == MIGRATION
    assert migration.down_revision == "0136_video_languages_eight"
    assert len(migration.revision) <= 32
    assert VISUAL_TIERS == ("clips", "hybrid", "stills", "manga")
    assert migration.WIDE == "visual_tier IN ('clips', 'hybrid', 'stills', 'manga')"
    assert migration.NARROW == "visual_tier IN ('clips', 'hybrid', 'stills')"
    # The schemas accept the fourth tier on both forms; the one-off keeps its old default.
    assert SeriesIn(premise="p", visual_tier="manga").visual_tier == "manga"
    assert DramaRequestIn(premise="p", visual_tier="manga").visual_tier == "manga"
    assert DramaRequestIn(premise="p").visual_tier == "clips"


def test_offline_sql_replaces_the_check_in_both_directions() -> None:
    upgrade = offline_sql("upgrade")
    assert f"ALTER TABLE {SERIES} DROP CONSTRAINT {CHECK}" in upgrade
    assert f"ADD CONSTRAINT {CHECK} CHECK ({load_migration().WIDE})" in upgrade
    downgrade = offline_sql("downgrade")
    assert f"ALTER TABLE {SERIES} DROP CONSTRAINT {CHECK}" in downgrade
    assert f"ADD CONSTRAINT {CHECK} CHECK ({load_migration().NARROW})" in downgrade
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


def _definition(connection: Connection) -> str:
    return str(
        connection.execute(
            sa.text("SELECT pg_get_constraintdef(oid) FROM pg_constraint WHERE conname = :name"),
            {"name": CHECK},
        ).scalar_one()
    )


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_widens_the_check_and_downgrade_narrows_it_again(
    dispose_engine_after_module: None,
) -> None:
    migration = load_migration()

    @in_a_rolled_back_transaction
    def exercise(connection: Connection) -> None:
        # Production's shape: the narrow check from 0103.
        connection.execute(sa.text(f"ALTER TABLE {SERIES} DROP CONSTRAINT {CHECK}"))
        connection.execute(
            sa.text(f"ALTER TABLE {SERIES} ADD CONSTRAINT {CHECK} CHECK ({migration.NARROW})")
        )
        assert "manga" not in _definition(connection)
        run(connection, "upgrade")
        assert "manga" in _definition(connection)
        run(connection, "downgrade")
        assert "manga" not in _definition(connection)
        # The fresh-database shape (0001 already wide): the upgrade is harmless there too.
        run(connection, "upgrade")
        run(connection, "upgrade")
        assert "manga" in _definition(connection)

    async with engine.connect() as connection:
        await connection.run_sync(exercise)
