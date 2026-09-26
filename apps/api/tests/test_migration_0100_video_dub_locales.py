"""0100 adds ``video_projects.dub_locales`` and the ``dubs`` review gate.

``0001_initial`` builds a fresh database from the current models, so CI never sees the tables in
their older shape; this test takes the column and the wide gate check off a real PostgreSQL, runs
the migration through a real alembic context, and checks both directions inside one rolled back
transaction, the way ``test_migration_0095_video_drama`` does. The downgrade must refuse while a
dubs review exists, and go through once it is gone.
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
MIGRATION = "0100_video_dub_locales"
PROJECTS = "video_projects"
REVIEWS = "video_reviews"
GATE_CHECK = "ck_video_review_gate"
OLD_GATES = "gate IN ('outline', 'script', 'look', 'storyboard', 'audio', 'final', 'publish')"


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
    connection.execute(sa.text(f"ALTER TABLE {PROJECTS} DROP COLUMN IF EXISTS dub_locales"))
    connection.execute(sa.text(f"ALTER TABLE {REVIEWS} DROP CONSTRAINT IF EXISTS {GATE_CHECK}"))
    connection.execute(
        sa.text(f"ALTER TABLE {REVIEWS} ADD CONSTRAINT {GATE_CHECK} CHECK ({OLD_GATES})")
    )


def _exercise(connection: Connection) -> None:
    # A video from before the column existed: it must come out with no dub languages.
    session = Session(bind=connection)
    project = VideoProject(slug="mig-0100-dubs", title="t", stage="final")
    session.add(project)
    session.flush()
    _older_shape(connection)
    assert "dub_locales" not in columns(connection, PROJECTS)
    assert "'dubs'" not in checks(connection, REVIEWS)[GATE_CHECK]

    run(connection, "upgrade")
    assert "dub_locales" in columns(connection, PROJECTS)
    assert "'dubs'" in checks(connection, REVIEWS)[GATE_CHECK]
    stored = connection.execute(
        sa.text(f"SELECT dub_locales FROM {PROJECTS} WHERE slug = 'mig-0100-dubs'")
    ).scalar()
    assert stored == []
    # Idempotent: a second upgrade finds everything and leaves it alone.
    run(connection, "upgrade")
    assert "'dubs'" in checks(connection, REVIEWS)[GATE_CHECK]
    assert "'publish'" in checks(connection, REVIEWS)[GATE_CHECK]

    # A dubs review blocks the downgrade; once it is gone the older shape comes back.
    review = VideoReview(
        project_id=project.id,
        gate="dubs",
        content_sha256="a" * 64,
        summary="s",
        payload={},
        files=[],
        status="pending",
    )
    session.add(review)
    session.flush()
    with pytest.raises(RuntimeError, match="dubs reviews exist"):
        run(connection, "downgrade")
    session.delete(review)
    session.flush()
    run(connection, "downgrade")
    assert "dub_locales" not in columns(connection, PROJECTS)
    assert "'dubs'" not in checks(connection, REVIEWS)[GATE_CHECK]
    session.close()


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_adds_the_dub_languages_and_gate_and_downgrade_removes_them() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
