"""0107 turns every queued one-off request into a one-episode series with a story bible to plan.

``0001_initial`` builds a fresh database from the current models, so CI never sees a series
without ``kind`` or the narrow checks, and the conversion (a queued request becomes a
``one-off`` series with its episode 1 planned and the request pointing at it) never runs there.
This test seeds requests the way the site had them, takes the column and the wide checks off a
real PostgreSQL, runs the migration through a real alembic context, and checks both directions
inside one rolled back transaction, the way ``test_migration_0106_video_locales`` does.
"""

from __future__ import annotations

import importlib.util
import os
from collections.abc import AsyncIterator, Callable
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

import app.models  # noqa: F401  (registers every table, so the request's foreign keys resolve)
from app.db import engine
from app.video_automation.models import VideoDramaRequest

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0107_video_one_off_series"
SERIES = "video_drama_series"
DOCS = "video_drama_docs"
EPISODES = "video_drama_episodes"
REQUESTS = "video_drama_requests"
OLD_NUMBERS = (
    "planned_episodes BETWEEN 1 AND 500 AND episodes_per_chapter BETWEEN 4 AND 20 "
    "AND target_minutes BETWEEN 1 AND 8"
)
OLD_DOC_KINDS = "kind IN ('setting', 'outline', 'chapter')"


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
    connection.execute(sa.text(f"ALTER TABLE {SERIES} DROP COLUMN IF EXISTS kind"))
    connection.execute(
        sa.text(f"ALTER TABLE {SERIES} DROP CONSTRAINT IF EXISTS ck_video_drama_series_numbers")
    )
    connection.execute(
        sa.text(
            f"ALTER TABLE {SERIES} ADD CONSTRAINT ck_video_drama_series_numbers "
            f"CHECK ({OLD_NUMBERS})"
        )
    )
    connection.execute(
        sa.text(f"ALTER TABLE {DOCS} DROP CONSTRAINT IF EXISTS ck_video_drama_doc_kind")
    )
    connection.execute(
        sa.text(
            f"ALTER TABLE {DOCS} ADD CONSTRAINT ck_video_drama_doc_kind CHECK ({OLD_DOC_KINDS})"
        )
    )


def _series_of(connection: Connection, request_id: object) -> sa.Row[tuple[object, ...]] | None:
    return connection.execute(
        sa.text(
            f"SELECT slug, kind, title, premise, style_preset, target_minutes, planned_episodes, "
            f"episodes_per_chapter, open_ended, status, note FROM {SERIES} WHERE id = :id"
        ),
        {"id": request_id},
    ).one_or_none()


def _request(connection: Connection, request_id: object) -> sa.Row[tuple[object, ...]]:
    return connection.execute(
        sa.text(f"SELECT status, series_id, episode_number FROM {REQUESTS} WHERE id = :id"),
        {"id": request_id},
    ).one()


def _count(connection: Connection, table: str, where: str = "true") -> int:
    return int(
        connection.execute(sa.text(f"SELECT count(*) FROM {table} WHERE {where}")).scalar() or 0
    )


def _exercise(connection: Connection) -> None:
    # Three requests as the site had them: one queued (the owner's next one-off), one the
    # worker already started under a slug, one withdrawn. Only the queued one becomes a series.
    session = Session(bind=connection)
    queued = VideoDramaRequest(
        id=uuid4(),
        premise="精衛填海：炎帝最小的女兒在東海溺水。",
        title="精衛",
        style_preset="ink-wash",
        target_minutes=2,
        note="慢一點",
        status="queued",
    )
    untitled = VideoDramaRequest(id=uuid4(), premise="夸父逐日", status="queued")
    started = VideoDramaRequest(
        id=uuid4(), premise="p", status="started", slug=f"mig-0105-{uuid4().hex[:8]}"
    )
    cancelled = VideoDramaRequest(id=uuid4(), premise="p", status="cancelled")
    session.add_all([queued, untitled, started, cancelled])
    session.flush()
    _older_shape(connection)
    assert "kind" not in columns(connection, SERIES)
    assert (
        "episodes_per_chapter >= 4" in checks(connection, SERIES)["ck_video_drama_series_numbers"]
    )
    assert "'bible'" not in checks(connection, DOCS)["ck_video_drama_doc_kind"]
    series_before = _count(connection, SERIES)

    run(connection, "upgrade")
    assert "kind" in columns(connection, SERIES)
    assert (
        "episodes_per_chapter >= 1" in checks(connection, SERIES)["ck_video_drama_series_numbers"]
    )
    assert "'bible'" in checks(connection, DOCS)["ck_video_drama_doc_kind"]
    assert "'one-off'" in checks(connection, SERIES)["ck_video_drama_series_kind"]
    assert _count(connection, SERIES) == series_before + 2, "one series per queued request"

    made = _series_of(connection, queued.id)
    assert made is not None
    slug, kind, title, premise, preset, minutes, planned, per_chapter, open_ended, status, note = (
        made
    )
    assert slug == f"one-off-{queued.id.hex[:8]}" and kind == "one-off"
    assert (title, premise, preset, minutes) == ("精衛", queued.premise, "ink-wash", 2)
    assert (planned, per_chapter, open_ended, status, note) == (1, 1, False, "setting", "慢一點")
    episode = connection.execute(
        sa.text(
            f"SELECT number, chapter_number, status, title FROM {EPISODES} WHERE series_id = :id"
        ),
        {"id": queued.id},
    ).one()
    assert tuple(episode) == (1, 1, "planned", "精衛"), "episode 1 waits for the bible"
    assert tuple(_request(connection, queued.id)) == ("queued", queued.id, 1)
    untitled_series = _series_of(connection, untitled.id)
    assert untitled_series is not None and untitled_series[2] == "夸父逐日", (
        "a request without a title is named by its premise"
    )
    assert _series_of(connection, started.id) is None, "a started request walks the old road"
    assert tuple(_request(connection, started.id)) == ("started", None, None)
    assert _series_of(connection, cancelled.id) is None

    # Idempotent: a second upgrade finds the requests already pointing at their series.
    run(connection, "upgrade")
    assert _count(connection, SERIES) == series_before + 2
    assert _count(connection, EPISODES, f"series_id = '{queued.id}'") == 1

    # The one-offs block the downgrade; once they are gone the older shape comes back.
    with pytest.raises(RuntimeError, match="one-off series"):
        run(connection, "downgrade")
    for row in (queued, untitled):
        connection.execute(
            sa.text(
                f"UPDATE {REQUESTS} SET series_id = NULL, episode_number = NULL WHERE id = :id"
            ),
            {"id": row.id},
        )
        connection.execute(sa.text(f"DELETE FROM {SERIES} WHERE id = :id"), {"id": row.id})
    run(connection, "downgrade")
    assert "kind" not in columns(connection, SERIES)
    assert (
        "episodes_per_chapter >= 4" in checks(connection, SERIES)["ck_video_drama_series_numbers"]
    )
    assert "'bible'" not in checks(connection, DOCS)["ck_video_drama_doc_kind"]
    assert "ck_video_drama_series_kind" not in checks(connection, SERIES)
    assert tuple(_request(connection, queued.id)) == ("queued", None, None)
    session.close()


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_turns_queued_requests_into_one_off_series_and_downgrade_removes_it() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
