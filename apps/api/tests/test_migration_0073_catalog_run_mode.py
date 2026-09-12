"""0073 widens ``ck_catalog_run_mode`` and refuses to narrow it over live enrichment runs.

``0001_initial`` builds a fresh database from the current models, so CI never sees the
old two-value constraint; this test puts a real PostgreSQL back into that shape, runs the
migration through a real alembic context, and checks both directions inside one rolled
back transaction, the way ``test_migration_dead_branches`` does.
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

from app.db import engine
from app.models import CatalogReviewRun, User

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0073_catalog_run_enrich_mode"
TABLE = "catalog_review_runs"
CONSTRAINT = "ck_catalog_run_mode"
OLD_CHECK = "mode IN ('review_pending', 'discover_new')"


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def load_migration(name: str) -> ModuleType:
    path = VERSIONS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"migration_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_upgrade(connection: Connection) -> None:
    context = MigrationContext.configure(connection)
    with Operations.context(context):
        load_migration(MIGRATION).upgrade()


def run_downgrade(connection: Connection) -> None:
    context = MigrationContext.configure(connection)
    with Operations.context(context):
        load_migration(MIGRATION).downgrade()


def check_text(connection: Connection) -> str:
    for check in sa.inspect(connection).get_check_constraints(TABLE):
        if check.get("name") == CONSTRAINT:
            return str(check.get("sqltext") or "")
    return ""


def plant_run(session: Session, mode: str) -> None:
    user = User(
        email=f"migration-0073-{uuid4()}@example.com",
        password_hash=None,
        is_active=True,
        is_admin=True,
    )
    session.add(user)
    session.flush()
    session.add(
        CatalogReviewRun(
            id=uuid4(),
            actor_user_id=user.id,
            idempotency_key=uuid4().hex,
            request_hash="0" * 64,
            request_json={"mode": mode, "scope": "foods"},
            mode=mode,
            phase=mode,
            status="completed",
            model="fixture",
            version=1,
            usage_json={},
            result_json={},
        )
    )
    session.flush()


def restore_old_shape(connection: Connection) -> None:
    connection.execute(sa.text(f"ALTER TABLE {TABLE} DROP CONSTRAINT {CONSTRAINT}"))
    connection.execute(
        sa.text(f"ALTER TABLE {TABLE} ADD CONSTRAINT {CONSTRAINT} CHECK ({OLD_CHECK})")
    )


def in_a_rolled_back_transaction(
    exercise: Callable[[Connection], None],
) -> Callable[[Connection], None]:
    def run(connection: Connection) -> None:
        transaction = connection.begin()
        try:
            exercise(connection)
        finally:
            transaction.rollback()

    return run


def _exercise_upgrade(connection: Connection) -> None:
    restore_old_shape(connection)
    session = Session(bind=connection)
    with pytest.raises(sa.exc.IntegrityError), session.begin_nested():
        plant_run(session, "enrich_merchants")

    run_upgrade(connection)
    assert "enrich_merchants" in check_text(connection)
    plant_run(session, "enrich_merchants")
    with pytest.raises(sa.exc.IntegrityError), session.begin_nested():
        plant_run(session, "bogus")

    # Idempotent: a second upgrade finds the widened constraint and leaves it alone.
    run_upgrade(connection)
    assert "enrich_merchants" in check_text(connection)


def _exercise_downgrade(connection: Connection) -> None:
    session = Session(bind=connection)
    plant_run(session, "enrich_merchants")
    with pytest.raises(RuntimeError, match="enrich_merchants"):
        run_downgrade(connection)
    assert "enrich_merchants" in check_text(connection)

    connection.execute(sa.text(f"DELETE FROM {TABLE} WHERE mode = 'enrich_merchants'"))
    run_downgrade(connection)
    assert "enrich_merchants" not in check_text(connection)
    with pytest.raises(sa.exc.IntegrityError), session.begin_nested():
        plant_run(session, "enrich_merchants")
    run_upgrade(connection)
    assert "enrich_merchants" in check_text(connection)


async def test_0073_widens_the_mode_check_and_is_idempotent() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_upgrade))


async def test_0073_downgrade_refuses_while_enrichment_runs_exist() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_downgrade))
