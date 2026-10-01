"""0117 adds the Shorts' topic library, assets and reports, and widens two prompt checks.

``0001_initial`` builds a fresh database from ``app.models``, which does not hold the video
tables, so their migrations create them; this test still takes the new tables, the new
settings columns and the wide checks off a real PostgreSQL, so every branch of the upgrade
runs, and checks both directions inside one rolled back transaction, the way
``test_migration_0109_video_shorts`` does. The rebuilt checks must keep every value they
took before.
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
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import engine
from app.video_shorts.models import VideoShortsSettings

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0117_video_shorts_topics"
SETTINGS = "video_shorts_settings"
PROMPTS = "video_stage_prompts"
TABLES = ("video_shorts_reports", "video_shorts_assets", "video_shorts_topics")
COLUMNS = {"max_per_month", "last_plan_at", "last_brief_at"}
MONTH_CHECK = "ck_video_shorts_settings_month"
STAGE_CHECK = "ck_video_stage_prompt_stage"
FORMAT_CHECK = "ck_video_stage_prompt_format"
OLD_STAGES = ("planner", "writer", "verifier", "listener", "translator", "caption_reviewer")
OLD_FORMATS = ("slides", "drama")
PROMPT = (
    f"INSERT INTO {PROMPTS} (stage, format, variant, slug, instructions, sent_at) "
    "VALUES (:stage, :format, :variant, 'mig-0117', 'prompt', now())"
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


def checks(connection: Connection, table: str) -> dict[str, str]:
    return {
        str(check.get("name")): str(check.get("sqltext"))
        for check in sa.inspect(connection).get_check_constraints(table)
    }


def tables(connection: Connection) -> set[str]:
    return set(sa.inspect(connection).get_table_names())


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


def _refused(connection: Connection, statement: str, **values: object) -> bool:
    """Whether the database refuses the statement; the transaction goes on either way."""
    savepoint = connection.begin_nested()
    try:
        connection.execute(sa.text(statement), values)
    except IntegrityError:
        savepoint.rollback()
        return True
    savepoint.rollback()
    return False


def _older_shape(connection: Connection) -> None:
    for table in TABLES:
        connection.execute(sa.text(f"DROP TABLE IF EXISTS {table}"))
    connection.execute(sa.text(f"ALTER TABLE {SETTINGS} DROP CONSTRAINT IF EXISTS {MONTH_CHECK}"))
    for name in sorted(COLUMNS):
        connection.execute(sa.text(f"ALTER TABLE {SETTINGS} DROP COLUMN IF EXISTS {name}"))
    connection.execute(
        sa.text(f"DELETE FROM {PROMPTS} WHERE stage = 'subject' OR format = 'shorts'")
    )
    for name, column, values in (
        (STAGE_CHECK, "stage", OLD_STAGES),
        (FORMAT_CHECK, "format", OLD_FORMATS),
    ):
        listed = ", ".join(f"'{value}'" for value in values)
        connection.execute(sa.text(f"ALTER TABLE {PROMPTS} DROP CONSTRAINT IF EXISTS {name}"))
        connection.execute(
            sa.text(f"ALTER TABLE {PROMPTS} ADD CONSTRAINT {name} CHECK ({column} IN ({listed}))")
        )


def _exercise(connection: Connection) -> None:
    session = Session(bind=connection)
    if session.get(VideoShortsSettings, 1) is None:
        session.add(VideoShortsSettings(id=1))
        session.flush()
    _older_shape(connection)
    assert not COLUMNS & columns(connection, SETTINGS)
    assert not set(TABLES) & tables(connection)
    for stage in OLD_STAGES:
        connection.execute(sa.text(PROMPT), {"stage": stage, "format": "drama", "variant": "old"})
    assert _refused(connection, PROMPT, stage="subject", format="slides", variant="a")
    assert _refused(connection, PROMPT, stage="writer", format="shorts", variant="b")

    run(connection, "upgrade")
    assert set(TABLES) <= tables(connection)
    assert COLUMNS <= columns(connection, SETTINGS)
    assert MONTH_CHECK in checks(connection, SETTINGS)
    month = connection.execute(sa.text(f"SELECT max_per_month FROM {SETTINGS} WHERE id = 1"))
    assert month.scalar() == 60, "the row that was there takes the default cap"
    found = checks(connection, PROMPTS)
    for value in (*OLD_STAGES, "subject"):
        assert f"'{value}'" in found[STAGE_CHECK], value
    for value in (*OLD_FORMATS, "shorts"):
        assert f"'{value}'" in found[FORMAT_CHECK], value
    kept = connection.execute(
        sa.text(f"SELECT count(*) FROM {PROMPTS} WHERE slug = 'mig-0117' AND variant = 'old'")
    )
    assert kept.scalar() == len(OLD_STAGES), "every prompt that was there stays"
    connection.execute(sa.text(PROMPT), {"stage": "subject", "format": "shorts", "variant": "a"})
    connection.execute(sa.text(PROMPT), {"stage": "writer", "format": "shorts", "variant": "lab"})
    assert _refused(connection, PROMPT, stage="narrator", format="shorts", variant="c")
    assert _refused(connection, PROMPT, stage="writer", format="reels", variant="d")
    assert _refused(connection, f"UPDATE {SETTINGS} SET max_per_month = 401 WHERE id = 1")
    topic = (
        "INSERT INTO video_shorts_topics (id, slug, line, title, status, brief, origin, "
        "assets_needed, created_at, updated_at) VALUES (gen_random_uuid(), :slug, 'lab', 't', "
        ":status, '{}', 'campaign', '[]', now(), now())"
    )
    connection.execute(sa.text(topic), {"slug": "mig-0117-topic", "status": "ready"})
    assert _refused(connection, topic, slug="mig-0117-topic", status="idea"), "one slug"
    assert _refused(connection, topic, slug="mig-0117-other", status="someday")

    # Idempotent: a second upgrade finds everything and leaves the rows alone.
    run(connection, "upgrade")
    assert connection.execute(sa.text("SELECT count(*) FROM video_shorts_topics")).scalar() == 1

    # Down: the prompts kept under the new values go, the rest stay, the narrow checks return.
    run(connection, "downgrade")
    assert not set(TABLES) & tables(connection)
    assert not COLUMNS & columns(connection, SETTINGS)
    left = connection.execute(sa.text(f"SELECT count(*) FROM {PROMPTS} WHERE slug = 'mig-0117'"))
    assert left.scalar() == len(OLD_STAGES)
    found = checks(connection, PROMPTS)
    assert "'subject'" not in found[STAGE_CHECK] and "'shorts'" not in found[FORMAT_CHECK]
    assert _refused(connection, PROMPT, stage="subject", format="shorts", variant="e")

    # And up again from there, as the host would.
    run(connection, "upgrade")
    assert set(TABLES) <= tables(connection) and COLUMNS <= columns(connection, SETTINGS)
    session.close()


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_adds_the_library_and_keeps_every_prompt_value() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
