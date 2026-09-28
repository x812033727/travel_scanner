"""0109 lets a video be a Short and creates the Shorts' own tables.

``0001_initial`` builds a fresh database from the current models, so CI never sees
``video_projects`` without the Shorts columns or with the narrow format check, and the
branches that add them never run there. This test takes the columns, the checks and the four
tables off a real PostgreSQL, runs the migration through a real alembic context, and checks
both directions inside one rolled back transaction, the way
``test_migration_0106_video_locales`` does.
"""

from __future__ import annotations

import importlib.util
import os
from collections.abc import AsyncIterator, Callable
from datetime import UTC, datetime
from decimal import Decimal
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
from app.models import VideoProject

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0109_video_shorts"
PROJECTS = "video_projects"
TABLES = (
    "video_shorts_costs",
    "video_shorts_metrics",
    "video_shorts_slots",
    "video_shorts_settings",
)
COLUMNS = {"shorts_line", "shorts_series", "source_slug", "youtube_removed_at"}
SHORT = "mig-0109-tutorial"
FORMAT_CHECK = "ck_video_project_format"
LINE_CHECK = "ck_video_project_shorts_line"
SLOT = (
    "INSERT INTO video_shorts_slots (id, starts_at, phase, project_slug, status, created_at, "
    "updated_at) VALUES (gen_random_uuid(), :starts_at, 1, :slug, :status, now(), now())"
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


def _older_shape(connection: Connection) -> None:
    for table in TABLES:
        connection.execute(sa.text(f"DROP TABLE IF EXISTS {table}"))
    for name in (LINE_CHECK, FORMAT_CHECK):
        connection.execute(sa.text(f"ALTER TABLE {PROJECTS} DROP CONSTRAINT IF EXISTS {name}"))
    for name in sorted(COLUMNS):
        connection.execute(sa.text(f"ALTER TABLE {PROJECTS} DROP COLUMN IF EXISTS {name}"))
    connection.execute(
        sa.text(
            f"ALTER TABLE {PROJECTS} ADD CONSTRAINT {FORMAT_CHECK} "
            "CHECK (format IN ('slides', 'drama'))"
        )
    )


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


def _exercise(connection: Connection) -> None:
    session = Session(bind=connection)
    tutorial = VideoProject(slug="mig-0109-tutorial", title="t", stage="final")
    drama = VideoProject(slug="mig-0109-drama", title="t", stage="final", format="drama")
    session.add_all([tutorial, drama])
    session.flush()
    _older_shape(connection)
    assert not COLUMNS & columns(connection, PROJECTS)
    assert not set(TABLES) & tables(connection)
    assert "'shorts'" not in checks(connection, PROJECTS)[FORMAT_CHECK]

    run(connection, "upgrade")
    assert COLUMNS <= columns(connection, PROJECTS)
    assert set(TABLES) <= tables(connection)
    found = checks(connection, PROJECTS)
    assert "'shorts'" in found[FORMAT_CHECK] and "'drama'" in found[FORMAT_CHECK]
    assert "'lab'" in found[LINE_CHECK]
    kept = connection.execute(
        sa.text(
            f"SELECT slug, format, shorts_line FROM {PROJECTS} "
            "WHERE slug LIKE 'mig-0109-%' ORDER BY slug"
        )
    ).all()
    assert [tuple(row) for row in kept] == [
        ("mig-0109-drama", "drama", None),
        ("mig-0109-tutorial", "slides", None),
    ], "the videos that were there are not Shorts"

    # What the new shape takes and refuses.
    connection.execute(
        sa.text(
            f"UPDATE {PROJECTS} SET format = 'shorts', shorts_line = 'lab', "
            "shorts_series = 'daily' WHERE slug = 'mig-0109-tutorial'"
        )
    )
    assert _refused(
        connection, f"UPDATE {PROJECTS} SET shorts_line = 'travel' WHERE slug = 'mig-0109-drama'"
    )
    assert _refused(
        connection, f"UPDATE {PROJECTS} SET format = 'reels' WHERE slug = 'mig-0109-drama'"
    )
    # asyncpg takes a moment as a datetime and an amount as a Decimal, never as text.
    first = {"starts_at": datetime(2026, 10, 5, 11, 30, tzinfo=UTC), "slug": SHORT}
    second = {"starts_at": datetime(2026, 10, 6, 11, 30, tzinfo=UTC), "slug": SHORT}
    connection.execute(sa.text(SLOT), {**first, "status": "missed"})
    connection.execute(sa.text(SLOT), {**second, "status": "assigned"})
    third = {"starts_at": datetime(2026, 10, 7, 11, 30, tzinfo=UTC), "slug": SHORT}
    assert _refused(connection, SLOT, **third, status="locked"), "a Short holds one slot"
    assert _refused(connection, SLOT, **{**second, "slug": "another", "status": "open"}), (
        "one slot a time"
    )
    assert _refused(connection, SLOT, **{**third, "slug": None, "status": "sometime"})
    ledger = (
        "INSERT INTO video_shorts_costs (id, occurred_at, category, amount, currency, "
        "amount_ntd, status, source, created_at, updated_at) VALUES (gen_random_uuid(), now(), "
        "'tool', :amount, 'TWD', :amount, :status, 'manual', now(), now())"
    )
    assert _refused(connection, ledger, amount=None, status="confirmed"), "no amount, not confirmed"
    assert _refused(connection, ledger, amount=Decimal(0), status="unknown"), (
        "an unknown is not a zero"
    )
    connection.execute(sa.text(ledger), {"amount": Decimal(0), "status": "confirmed"})
    connection.execute(sa.text(ledger), {"amount": None, "status": "unknown"})

    # Idempotent: a second upgrade finds everything and leaves the rows alone.
    run(connection, "upgrade")
    assert connection.execute(sa.text("SELECT count(*) FROM video_shorts_slots")).scalar() == 2
    assert connection.execute(sa.text("SELECT count(*) FROM video_shorts_costs")).scalar() == 2
    assert "'shorts'" in checks(connection, PROJECTS)[FORMAT_CHECK]

    # A Short blocks the downgrade: by its format, and by its line alone (a vertical drama).
    with pytest.raises(RuntimeError, match="1 videos are Shorts"):
        run(connection, "downgrade")
    connection.execute(
        sa.text(
            f"UPDATE {PROJECTS} SET format = 'drama', shorts_line = 'drama' "
            "WHERE slug = 'mig-0109-tutorial'"
        )
    )
    with pytest.raises(RuntimeError, match="1 videos are Shorts"):
        run(connection, "downgrade")
    connection.execute(
        sa.text(f"UPDATE {PROJECTS} SET shorts_line = NULL WHERE slug = 'mig-0109-tutorial'")
    )
    run(connection, "downgrade")
    assert not COLUMNS & columns(connection, PROJECTS)
    assert not set(TABLES) & tables(connection)
    found = checks(connection, PROJECTS)
    assert "'shorts'" not in found[FORMAT_CHECK] and LINE_CHECK not in found

    # And up again from there, as the host would.
    run(connection, "upgrade")
    assert COLUMNS <= columns(connection, PROJECTS) and set(TABLES) <= tables(connection)
    session.close()


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_makes_room_for_shorts_and_downgrade_refuses_while_one_exists() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
