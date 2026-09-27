"""0103 gives each video its language choice and admits the languages gate.

``0001_initial`` builds a fresh database from the current models, so CI never sees a video
without ``locales``, and the copy the migration makes (the dub languages ticked before become
whole languages; a video on YouTube, or with dubs ticked, counts as decided) never runs there.
This test seeds videos the way the site had them, takes the columns and the wide gate check off a
real PostgreSQL, runs the migration through a real alembic context, and checks both directions
inside one rolled back transaction, the way ``test_migration_0101_video_dub_locales`` does.
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

from app.db import engine
from app.models import VideoProject, VideoReview

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0103_video_locales"
PROJECTS = "video_projects"
REVIEWS = "video_reviews"
GATE_CHECK = "ck_video_review_gate"
OLD_GATES = (
    "gate IN ('outline', 'script', 'look', 'storyboard', 'audio', 'final', 'publish', 'dubs')"
)
WHOLE = {"metadata": True, "captions": True, "dub": True}


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
    for name in ("locales_decided_at", "locales"):
        connection.execute(sa.text(f"ALTER TABLE {PROJECTS} DROP COLUMN IF EXISTS {name}"))
    connection.execute(sa.text(f"ALTER TABLE {REVIEWS} DROP CONSTRAINT IF EXISTS {GATE_CHECK}"))
    connection.execute(
        sa.text(f"ALTER TABLE {REVIEWS} ADD CONSTRAINT {GATE_CHECK} CHECK ({OLD_GATES})")
    )


def _row(connection: Connection, slug: str) -> sa.Row[tuple[object, ...]]:
    return connection.execute(
        sa.text(f"SELECT locales, locales_decided_at FROM {PROJECTS} WHERE slug = :slug"),
        {"slug": slug},
    ).one()


def _exercise(connection: Connection) -> None:
    # Three videos as the site had them: one with dub languages ticked, one already on YouTube
    # without any, one still in the making. The first two count as decided, the third waits.
    session = Session(bind=connection)
    dubbed = VideoProject(
        slug="mig-0103-dubbed", title="t", stage="final", dub_locales=["en", "ko"]
    )
    published = VideoProject(
        slug="mig-0103-published", title="t", stage="done", youtube_video_id="dQw4w9WgXcQ"
    )
    making = VideoProject(slug="mig-0103-making", title="t", stage="script")
    session.add_all([dubbed, published, making])
    session.flush()
    _older_shape(connection)
    assert not {"locales", "locales_decided_at"} & columns(connection, PROJECTS)
    assert "'languages'" not in checks(connection, REVIEWS)[GATE_CHECK]

    run(connection, "upgrade")
    assert {"locales", "locales_decided_at"} <= columns(connection, PROJECTS)
    assert "'languages'" in checks(connection, REVIEWS)[GATE_CHECK]
    locales, decided = _row(connection, "mig-0103-dubbed")
    assert locales == {"en": WHOLE, "ko": WHOLE}, "a ticked dub language becomes a whole language"
    assert decided is not None
    locales, decided = _row(connection, "mig-0103-published")
    assert locales == {} and decided is not None, "on YouTube: decided, nothing added"
    locales, decided = _row(connection, "mig-0103-making")
    assert locales == {} and decided is None, "still in the making: the owner decides"

    # Idempotent: a second upgrade finds everything, copies nothing and marks nothing.
    connection.execute(
        sa.text(
            f"UPDATE {PROJECTS} SET locales = '{{}}', locales_decided_at = NULL "
            "WHERE slug = 'mig-0103-dubbed'"
        )
    )
    run(connection, "upgrade")
    locales, decided = _row(connection, "mig-0103-dubbed")
    assert locales == {} and decided is None
    assert "'languages'" in checks(connection, REVIEWS)[GATE_CHECK]
    assert "'dubs'" in checks(connection, REVIEWS)[GATE_CHECK]

    # A languages review blocks the downgrade; once it is gone the older shape comes back.
    review = VideoReview(
        project_id=making.id,
        gate="languages",
        content_sha256="a" * 64,
        summary="s",
        payload={},
        files=[],
        status="pending",
    )
    session.add(review)
    session.flush()
    with pytest.raises(RuntimeError, match="languages reviews exist"):
        run(connection, "downgrade")
    session.delete(review)
    session.flush()
    run(connection, "downgrade")
    assert not {"locales", "locales_decided_at"} & columns(connection, PROJECTS)
    assert "'languages'" not in checks(connection, REVIEWS)[GATE_CHECK]
    kept = connection.execute(
        sa.text(f"SELECT dub_locales FROM {PROJECTS} WHERE slug = 'mig-0103-dubbed'")
    ).scalar()
    assert kept == ["en", "ko"], "the older column is never touched"
    session.close()


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_adds_the_language_choice_from_the_dubs_and_downgrade_removes_it() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
