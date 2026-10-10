"""0128 takes zh-CN out of every video's language choice and the three default lists.

``0001_initial`` builds a fresh database from the current models, and nothing in CI writes
zh-CN into a video's languages any more, so the rewrite only runs for real in production. The
PostgreSQL test plants a choice with zh-CN, one without, an empty one and the three default
lists, runs the migration through a real alembic context and checks what changed and what was
left alone, inside one rolled back transaction, the way ``test_migration_0106_video_locales``
does. The offline test reads the SQL the migration would write to a file.
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
from sqlalchemy.orm import Session

from app.db import engine
from app.models import VideoProject
from app.video_automation.models import DEFAULT_CAPTION_LOCALES, VideoAutomationSettings
from app.video_reviews.schemas import DUB_LOCALES, RETIRED_LOCALES
from app.video_shorts.models import VideoShortsSettings
from app.video_shorts.schemas import SHORTS_LOCALES
from tests.test_migration_sql_dialect import offenders_in

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0128_video_languages_four"
PROJECTS = "video_projects"
AUTOMATION = "video_automation_settings"
SHORTS = "video_shorts_settings"
WHOLE = {"metadata": True, "captions": True, "dub": True}
CAPTIONS = {"metadata": False, "captions": True, "dub": False}
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


def test_the_migration_retires_the_language_the_schemas_no_longer_admit() -> None:
    migration = load_migration()
    assert migration.revision == MIGRATION
    assert migration.down_revision == "0127_video_slides_requests"
    assert len(migration.revision) <= 32
    assert RETIRED_LOCALES == {migration.RETIRED}
    assert migration.RETIRED not in DUB_LOCALES
    assert migration.RETIRED not in DEFAULT_CAPTION_LOCALES
    assert migration.RETIRED not in SHORTS_LOCALES


def test_offline_sql_rewrites_the_four_json_columns_with_json_functions_only() -> None:
    migration = load_migration()
    buffer = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": buffer}
    )
    with Operations.context(context):
        migration.upgrade()
    sql = buffer.getvalue()
    for table, column in (
        (PROJECTS, "locales"),
        (AUTOMATION, "caption_locales"),
        (AUTOMATION, "drama_caption_locales"),
        (SHORTS, "locales"),
    ):
        assert f"UPDATE {table} SET {column} = COALESCE(" in sql, (table, column)
    assert sql.count("'zh-CN'") == 8, "each statement names the language once to drop, once to find"
    assert "::jsonb" not in sql and "jsonb_" not in sql
    assert not offenders_in([(f"{MIGRATION}.py", (VERSIONS / f"{MIGRATION}.py").read_text())])
    buffer = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": buffer}
    )
    with Operations.context(context):
        migration.downgrade()
    assert "UPDATE" not in buffer.getvalue(), "the downgrade restores nothing"


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


def _locales(connection: Connection, slug: str) -> Any:
    return connection.execute(
        sa.text(f"SELECT locales FROM {PROJECTS} WHERE slug = :slug"), {"slug": slug}
    ).scalar_one()


def _lists(connection: Connection) -> tuple[Any, Any, Any]:
    captions, drama = connection.execute(
        sa.text(f"SELECT caption_locales, drama_caption_locales FROM {AUTOMATION} WHERE id = 1")
    ).one()
    shorts = connection.execute(sa.text(f"SELECT locales FROM {SHORTS} WHERE id = 1")).scalar_one()
    return captions, drama, shorts


def _ensure_singleton(connection: Connection, table: sa.Table) -> None:
    present = connection.execute(sa.text(f"SELECT count(*) FROM {table.name} WHERE id = 1"))
    if not present.scalar():
        # The model's defaults fill a fresh row; the transaction rolls it back.
        connection.execute(sa.insert(table).values(id=1))


def _exercise(connection: Connection) -> None:
    session = Session(bind=connection)
    session.add_all(
        [
            VideoProject(
                slug="mig-0128-mixed",
                title="t",
                stage="final",
                locales={"en": WHOLE, "zh-CN": CAPTIONS, "ko": CAPTIONS},
            ),
            VideoProject(
                slug="mig-0128-only", title="t", stage="final", locales={"zh-CN": WHOLE}
            ),
            VideoProject(slug="mig-0128-kept", title="t", stage="final", locales={"ja": WHOLE}),
            VideoProject(slug="mig-0128-empty", title="t", stage="final", locales={}),
        ]
    )
    session.flush()
    _ensure_singleton(connection, cast(sa.Table, VideoAutomationSettings.__table__))
    _ensure_singleton(connection, cast(sa.Table, VideoShortsSettings.__table__))
    connection.execute(
        sa.text(
            f"UPDATE {AUTOMATION} SET caption_locales = :captions, "
            "drama_caption_locales = :drama WHERE id = 1"
        ),
        {"captions": '["en", "ja", "ko", "zh-CN"]', "drama": '["zh-CN"]'},
    )
    connection.execute(
        sa.text(f"UPDATE {SHORTS} SET locales = :locales WHERE id = 1"),
        {"locales": '["zh-CN", "en"]'},
    )

    run(connection, "upgrade")
    assert _locales(connection, "mig-0128-mixed") == {"en": WHOLE, "ko": CAPTIONS}, (
        "the other languages keep their parts"
    )
    assert _locales(connection, "mig-0128-only") == {}, "a choice of zh-CN alone is {} not NULL"
    assert _locales(connection, "mig-0128-kept") == {"ja": WHOLE}
    assert _locales(connection, "mig-0128-empty") == {}
    assert _lists(connection) == (["en", "ja", "ko"], [], ["en"])

    # Idempotent: a second upgrade finds nothing to drop.
    run(connection, "upgrade")
    assert _locales(connection, "mig-0128-mixed") == {"en": WHOLE, "ko": CAPTIONS}
    assert _lists(connection) == (["en", "ja", "ko"], [], ["en"])
    run(connection, "downgrade")
    assert _locales(connection, "mig-0128-mixed") == {"en": WHOLE, "ko": CAPTIONS}, (
        "the downgrade restores nothing"
    )
    session.close()


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_drops_zh_cn_from_choices_and_defaults_and_is_idempotent(
    dispose_engine_after_module: None,
) -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
