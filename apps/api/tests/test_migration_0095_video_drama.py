"""0095 adds the drama settings columns and the look/storyboard review gates.

``0001_initial`` builds a fresh database from the current models, so CI never sees the tables
in their older shape; this test takes the columns and constraints off a real PostgreSQL, runs
the migration through a real alembic context, and checks both directions inside one rolled
back transaction, the way ``test_migration_0094_news_final_editor`` does. The downgrade must
refuse while a look review exists, and go through once it is gone.
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
from app.video_automation.models import VideoAutomationSettings

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0095_video_drama"
SETTINGS = "video_automation_settings"
REVIEWS = "video_reviews"
GATE_CHECK = "ck_video_review_gate"
OLD_GATES = "gate IN ('outline', 'audio', 'final', 'publish')"


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


def _older_shape(connection: Connection, module: ModuleType) -> None:
    for name, _condition in module.CHECKS:
        connection.execute(sa.text(f"ALTER TABLE {SETTINGS} DROP CONSTRAINT IF EXISTS {name}"))
    for name, _kind, _default in module.COLUMNS:
        connection.execute(sa.text(f"ALTER TABLE {SETTINGS} DROP COLUMN IF EXISTS {name}"))
    connection.execute(sa.text(f"ALTER TABLE {REVIEWS} DROP CONSTRAINT IF EXISTS {GATE_CHECK}"))
    connection.execute(sa.text(f"ALTER TABLE {REVIEWS} DROP COLUMN IF EXISTS subject"))
    connection.execute(
        sa.text(f"ALTER TABLE {REVIEWS} ADD CONSTRAINT {GATE_CHECK} CHECK ({OLD_GATES})")
    )


def _exercise(connection: Connection) -> None:
    module = load_migration()
    session = Session(bind=connection)
    if session.get(VideoAutomationSettings, 1) is None:
        session.add(VideoAutomationSettings(id=1))
        session.flush()
    session.close()
    _older_shape(connection, module)
    drama_columns = {name for name, _kind, _default in module.COLUMNS}
    check_names = {name for name, _condition in module.CHECKS}
    assert not drama_columns & columns(connection, SETTINGS)
    assert "subject" not in columns(connection, REVIEWS)

    run(connection, "upgrade")
    assert drama_columns <= columns(connection, SETTINGS)
    assert check_names <= set(checks(connection, SETTINGS))
    assert "subject" in columns(connection, REVIEWS)
    assert "'look'" in checks(connection, REVIEWS)[GATE_CHECK]
    row = connection.execute(
        sa.text(
            "SELECT drama_enabled, image_model, clip_model, clip_resolution, "
            f"monthly_clip_seconds_budget, style_preset, character_voice_pool FROM {SETTINGS} "
            "WHERE id = 1"
        )
    ).one()
    assert tuple(row)[:6] == (
        False,
        "gemini-3-pro-image",
        "gemini-omni-1.1-flash",
        "1080p",
        3000,
        "cinematic-3d",
    )
    assert row[6] == []
    # Idempotent: a second upgrade finds everything and leaves it alone.
    run(connection, "upgrade")
    assert "'storyboard'" in checks(connection, REVIEWS)[GATE_CHECK]

    # A look review blocks the downgrade; once it is gone the older shape comes back.
    session = Session(bind=connection)
    project = VideoProject(slug="mig-0095-drama", title="t", stage="look")
    session.add(project)
    session.flush()
    review = VideoReview(
        project_id=project.id,
        gate="look",
        subject="jingwei",
        content_sha256="a" * 64,
        summary="s",
        payload={},
        files=[],
        status="pending",
    )
    session.add(review)
    session.flush()
    with pytest.raises(RuntimeError, match="look or storyboard"):
        run(connection, "downgrade")
    session.delete(review)
    session.flush()
    run(connection, "downgrade")
    assert not drama_columns & columns(connection, SETTINGS)
    assert not check_names & set(checks(connection, SETTINGS))
    assert "subject" not in columns(connection, REVIEWS)
    assert "'look'" not in checks(connection, REVIEWS)[GATE_CHECK]
    session.close()


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_adds_the_drama_settings_and_gates_and_downgrade_removes_them() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
