"""0104 gives the drama its own settings beside the tutorial's, copying the tutorial's values.

``0001_initial`` builds a fresh database from the current models, so CI never sees a settings
row without the drama columns, and the copy the migration makes (the standing instructions and
the two switches start from the tutorial's) never runs there. This test seeds a row the way the
site had it, takes the columns off a real PostgreSQL, runs the migration through a real alembic
context, and checks both directions inside one rolled back transaction, the way
``test_migration_0100_video_hands_off`` does.
"""

from __future__ import annotations

import importlib.util
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
from sqlalchemy.orm import Session

# app.models registers every table, among them users, the settings row's foreign key target;
# without it the ORM cannot build the INSERT that seeds the row.
import app.models  # noqa: F401
from app.db import engine
from app.video_automation.models import VideoAutomationSettings

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0104_video_split_settings"
SETTINGS = "video_automation_settings"
ROUNDS_CHECK = "ck_video_drama_rounds"
COLUMNS = (
    "drama_stage_models",
    "drama_stage_instructions",
    "drama_voice",
    "drama_caption_locales",
    "drama_auto_approve_audio",
    "drama_auto_approve_final",
    "drama_max_verify_rounds",
    "drama_max_retake_rounds",
)


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


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


def columns(connection: Connection, table: str) -> set[str]:
    return {column["name"] for column in sa.inspect(connection).get_columns(table)}


def checks(connection: Connection, table: str) -> set[str]:
    return {str(check.get("name")) for check in sa.inspect(connection).get_check_constraints(table)}


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


def _row(connection: Connection) -> sa.Row[tuple[object, ...]]:
    found = connection.execute(
        sa.text(
            f"SELECT drama_stage_models, drama_stage_instructions, drama_voice, "
            f"drama_caption_locales, drama_auto_approve_audio, drama_auto_approve_final, "
            f"drama_max_verify_rounds, drama_max_retake_rounds FROM {SETTINGS} WHERE id = 1"
        )
    ).one()
    return found


def _exercise(connection: Connection) -> None:
    # The row as the site had it before the split: the owner wrote a standing instruction and
    # turned the narration's automatic approval off, both of which the drama must inherit.
    connection.execute(sa.text(f"DELETE FROM {SETTINGS}"))
    with Session(bind=connection) as session:
        session.add(
            VideoAutomationSettings(
                id=1,
                stage_instructions={"writer": "結尾留懸念"},
                auto_approve_audio=False,
                auto_approve_final=True,
            )
        )
        session.flush()
    connection.execute(sa.text(f"ALTER TABLE {SETTINGS} DROP CONSTRAINT IF EXISTS {ROUNDS_CHECK}"))
    for name in COLUMNS:
        connection.execute(sa.text(f"ALTER TABLE {SETTINGS} DROP COLUMN IF EXISTS {name}"))
    assert not set(COLUMNS) & columns(connection, SETTINGS)
    assert ROUNDS_CHECK not in checks(connection, SETTINGS)

    run(connection, "upgrade")
    assert set(COLUMNS) <= columns(connection, SETTINGS)
    assert ROUNDS_CHECK in checks(connection, SETTINGS)
    (
        models,
        instructions,
        voice,
        locales,
        approve_audio,
        approve_final,
        verify_rounds,
        retake_rounds,
    ) = _row(connection)
    assert models is None and voice is None, "the drama follows the tutorial's until chosen"
    assert instructions == {"writer": "結尾留懸念"}, "copied from the tutorial's"
    assert (approve_audio, approve_final) == (False, True), "copied from the tutorial's"
    assert locales == [] and (verify_rounds, retake_rounds) == (3, 2)
    # The rounds are held to the same bounds as the tutorial's.
    with pytest.raises(sa.exc.DBAPIError):
        with connection.begin_nested():
            connection.execute(
                sa.text(f"UPDATE {SETTINGS} SET drama_max_verify_rounds = 6 WHERE id = 1")
            )

    # Idempotent: a second upgrade finds everything and copies nothing over what the owner
    # may have changed since.
    connection.execute(
        sa.text(
            f"UPDATE {SETTINGS} SET drama_stage_instructions = '{{}}', "
            "drama_auto_approve_audio = true"
        )
    )
    run(connection, "upgrade")
    _, instructions, _, _, approve_audio, _, _, _ = _row(connection)
    assert instructions == {} and approve_audio is True

    run(connection, "downgrade")
    assert not set(COLUMNS) & columns(connection, SETTINGS)
    assert ROUNDS_CHECK not in checks(connection, SETTINGS)
    kept = connection.execute(
        sa.text(f"SELECT stage_instructions, auto_approve_audio FROM {SETTINGS} WHERE id = 1")
    ).one()
    assert kept == ({"writer": "結尾留懸念"}, False), "the tutorial's columns are untouched"


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_adds_the_drama_columns_from_the_tutorial_and_downgrade_removes_them() -> (
    None
):
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
