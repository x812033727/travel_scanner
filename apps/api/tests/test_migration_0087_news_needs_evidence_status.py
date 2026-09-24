"""0087 adds ``needs_evidence`` to ``ck_news_candidate_status`` and moves the rows.

``0001_initial`` builds a fresh database from the current models, so CI never sees the
old constraint; this test puts a real PostgreSQL back into that shape, runs the migration
through a real alembic context, and checks both directions inside one rolled back
transaction, the way ``test_migration_0083_merchant_platform_source`` does.
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
from app.news_automation.models import NewsCandidate, NewsSource

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0087_news_needs_evidence_status"
TABLE = "news_candidates"
CONSTRAINT = "ck_news_candidate_status"
OLD_CHECK = (
    "status IN ('discovered','drafting','verifying','locale_review','jev_review',"
    "'shadow_review','manual_review','published','duplicate','rejected','failed')"
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


def check_text(connection: Connection) -> str:
    for check in sa.inspect(connection).get_check_constraints(TABLE):
        if check.get("name") == CONSTRAINT:
            return str(check.get("sqltext") or "")
    return ""


def plant(session: Session, status: str, error_code: str | None) -> NewsCandidate:
    marker = uuid4().hex
    source = NewsSource(
        name=f"Migration {marker}",
        url=f"https://{marker}.example/feed",
        format="rss",
        role="evidence",
        vertical="ai",
    )
    session.add(source)
    session.flush()
    candidate = NewsCandidate(
        source_id=source.id,
        vertical="ai",
        status=status,
        canonical_url=f"https://{marker}.example/story",
        source_title="Migration candidate",
        normalized_title=f"migration candidate {marker}",
        content_hash=marker * 2,
        idempotency_key=marker * 2,
        error_code=error_code,
    )
    session.add(candidate)
    session.flush()
    return candidate


def status_of(connection: Connection, candidate: NewsCandidate) -> str:
    return str(
        connection.execute(
            sa.text(f"SELECT status FROM {TABLE} WHERE id = :id"), {"id": candidate.id}
        ).scalar()
    )


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


def _exercise(connection: Connection) -> None:
    connection.execute(sa.text(f"ALTER TABLE {TABLE} DROP CONSTRAINT {CONSTRAINT}"))
    connection.execute(
        sa.text(f"ALTER TABLE {TABLE} ADD CONSTRAINT {CONSTRAINT} CHECK ({OLD_CHECK})")
    )
    session = Session(bind=connection)
    stopped = plant(session, "manual_review", "news_evidence_insufficient")
    reviewed = plant(session, "manual_review", "news_verification_failed")

    run(connection, "upgrade")
    assert "needs_evidence" in check_text(connection)
    assert status_of(connection, stopped) == "needs_evidence"
    assert status_of(connection, reviewed) == "manual_review"
    # Idempotent: a second upgrade leaves the widened constraint alone.
    run(connection, "upgrade")
    assert "needs_evidence" in check_text(connection)

    run(connection, "downgrade")
    assert "needs_evidence" not in check_text(connection)
    assert status_of(connection, stopped) == "manual_review"
    run(connection, "downgrade")


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_moves_evidence_gate_rows_and_downgrade_restores_them() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
