"""0111 lets a drama series be a brand-story series (docs/videos/STORY.md).

The upgrade widens ``ck_video_drama_series_kind`` to ``story`` and ``ck_video_drama_series_numbers``
to 20 minutes, and adds ``episodes_per_day`` (with ``ck_video_drama_series_per_day``),
``image_model`` and ``look``. The downgrade refuses while a story series, or a series longer than
8 minutes, exists, and once they are gone puts the narrow checks back and drops the columns.

This test takes a real PostgreSQL back to the shape the series table had before 0111 (as 0108
left it; 0109 does not touch it): the columns gone, the narrow checks back. It seeds a series
the way the site has them, runs the migration through a real alembic context both ways, and
checks it all inside one rolled back transaction, the way
``test_migration_0107_video_one_off_series`` does.
"""

from __future__ import annotations

import importlib.util
import os
from collections.abc import AsyncIterator, Callable
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from uuid import uuid4

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session

import app.models  # noqa: F401  (registers the users table the series' foreign key names)
from app.db import engine
from app.video_automation.models import VideoDramaSeries

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0111_video_story_series"
SERIES = "video_drama_series"
OLD_KINDS = "kind IN ('series', 'one-off')"
OLD_NUMBERS = (
    "planned_episodes BETWEEN 1 AND 500 AND episodes_per_chapter BETWEEN 1 AND 20 "
    "AND target_minutes BETWEEN 1 AND 8"
)
NEW_COLUMNS = {"episodes_per_day", "image_model", "look"}
WHEN = datetime(2026, 9, 28, 9, 0, tzinfo=UTC)


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


def columns(connection: Connection) -> set[str]:
    return {column["name"] for column in sa.inspect(connection).get_columns(SERIES)}


def checks(connection: Connection) -> dict[str, str]:
    return {
        str(check.get("name")): str(check.get("sqltext"))
        for check in sa.inspect(connection).get_check_constraints(SERIES)
    }


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
    connection.execute(
        sa.text(f"ALTER TABLE {SERIES} DROP CONSTRAINT IF EXISTS ck_video_drama_series_per_day")
    )
    for name in NEW_COLUMNS:
        connection.execute(sa.text(f"ALTER TABLE {SERIES} DROP COLUMN IF EXISTS {name}"))
    for name, condition in (
        ("ck_video_drama_series_kind", OLD_KINDS),
        ("ck_video_drama_series_numbers", OLD_NUMBERS),
    ):
        connection.execute(sa.text(f"ALTER TABLE {SERIES} DROP CONSTRAINT IF EXISTS {name}"))
        connection.execute(
            sa.text(f"ALTER TABLE {SERIES} ADD CONSTRAINT {name} CHECK ({condition})")
        )


def _insert_series(connection: Connection, *, new_columns: bool = True, **values: object) -> None:
    row: dict[str, object] = {
        "id": uuid4(),
        "slug": f"mig-0111-{uuid4().hex[:8]}",
        "kind": "story",
        "title": "品牌故事",
        "premise": "p",
        "target_minutes": 13,
        "status": "active",
        "hands_off": True,
        "visual_tier": "stills",
        "episodes_per_day": 2,
        "image_model": "gemini-3.1-flash-image",
        "look": '{"style": "flat 2D cartoon", "negative": "text, logo"}',
        "created_at": WHEN,
        "updated_at": WHEN,
    }
    row.update(values)
    if not new_columns:
        row = {name: value for name, value in row.items() if name not in NEW_COLUMNS}
    names = ", ".join(row)
    params = ", ".join(f"CAST(:{name} AS json)" if name == "look" else f":{name}" for name in row)
    connection.execute(sa.text(f"INSERT INTO {SERIES} ({names}) VALUES ({params})"), row)


def _refused(connection: Connection, *, new_columns: bool = True, **values: object) -> bool:
    """Whether the checks refuse this row; a savepoint keeps the transaction usable."""
    savepoint = connection.begin_nested()
    try:
        _insert_series(connection, new_columns=new_columns, **values)
    except sa.exc.IntegrityError:
        savepoint.rollback()
        return True
    savepoint.rollback()
    return False


def _count(connection: Connection, where: str) -> int:
    return int(
        connection.execute(sa.text(f"SELECT count(*) FROM {SERIES} WHERE {where}")).scalar() or 0
    )


def _exercise(connection: Connection) -> None:
    # A long series as the site has it, made before 0111; it must come through both ways.
    session = Session(bind=connection)
    classic = VideoDramaSeries(
        id=uuid4(),
        slug=f"mig-0111-{uuid4().hex[:8]}",
        kind="series",
        title="問劍",
        premise="兩個少年",
        target_minutes=3,
        status="active",
        created_at=WHEN,
        updated_at=WHEN,
    )
    session.add(classic)
    session.flush()
    _older_shape(connection)
    assert not NEW_COLUMNS & columns(connection)
    assert "'story'" not in checks(connection)["ck_video_drama_series_kind"]
    assert "target_minutes <= 8" in checks(connection)["ck_video_drama_series_numbers"]
    assert _refused(connection, new_columns=False), "the older checks refuse a story"
    assert _refused(connection, new_columns=False, kind="series"), "and 13 minutes"
    assert not _refused(connection, new_columns=False, kind="series", target_minutes=8)

    run(connection, "upgrade")
    assert NEW_COLUMNS <= columns(connection)
    found = checks(connection)
    assert "'story'" in found["ck_video_drama_series_kind"]
    assert "target_minutes <= 20" in found["ck_video_drama_series_numbers"]
    assert "ck_video_drama_series_per_day" in found
    _insert_series(connection, slug="mig-0111-story")
    assert not _refused(connection, episodes_per_day=None, target_minutes=20, look=None)
    assert _refused(connection, episodes_per_day=13), "a day holds 1 to 12 stories"
    assert _refused(connection, episodes_per_day=0)
    assert _refused(connection, target_minutes=21)
    assert _refused(connection, kind="movie")
    old = connection.execute(
        sa.text(f"SELECT kind, episodes_per_day, image_model, look FROM {SERIES} WHERE id = :id"),
        {"id": classic.id},
    ).one()
    assert tuple(old) == ("series", None, None, None), "an older series gets no story values"

    # Idempotent: a second upgrade finds the columns and puts the same checks back.
    run(connection, "upgrade")
    assert NEW_COLUMNS <= columns(connection)
    assert "ck_video_drama_series_per_day" in checks(connection)

    # The story blocks the downgrade, and so does a series longer than 8 minutes; the message
    # counts the whole table, which other tests share.
    def blocked() -> str:
        stories = _count(connection, "kind = 'story'")
        longer = _count(connection, "target_minutes > 8")
        return f"{stories} story series and {longer} series longer than 8 minutes exist"

    assert _count(connection, "kind = 'story'") >= 1
    with pytest.raises(RuntimeError, match=blocked()):
        run(connection, "downgrade")
    connection.execute(sa.text(f"DELETE FROM {SERIES} WHERE slug = 'mig-0111-story'"))
    connection.execute(
        sa.text(f"UPDATE {SERIES} SET target_minutes = 9 WHERE id = :id"), {"id": classic.id}
    )
    assert _count(connection, "target_minutes > 8") >= 1
    with pytest.raises(RuntimeError, match=blocked()):
        run(connection, "downgrade")
    connection.execute(
        sa.text(f"UPDATE {SERIES} SET target_minutes = 3 WHERE id = :id"), {"id": classic.id}
    )
    run(connection, "downgrade")
    assert not NEW_COLUMNS & columns(connection)
    found = checks(connection)
    assert "'story'" not in found["ck_video_drama_series_kind"]
    assert "target_minutes <= 8" in found["ck_video_drama_series_numbers"]
    assert "ck_video_drama_series_per_day" not in found
    assert _count(connection, f"id = '{classic.id}'") == 1, "the long series is untouched"
    session.close()


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_lets_a_series_be_a_story_and_downgrade_refuses_while_one_exists() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
