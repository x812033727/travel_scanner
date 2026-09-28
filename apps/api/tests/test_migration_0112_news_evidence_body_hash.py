"""0112 adds ``body_hash`` to news evidence and news candidates.

``0001_initial`` builds a fresh database from the current models, so CI never sees a database
without the columns. This test plants a candidate and its evidence, takes the columns and the
index off a real PostgreSQL, runs the migration through a real alembic context, and checks both
directions inside one rolled back transaction, the way
``test_migration_0088_news_needs_redraft_status`` does. Stored rows must come through with no
body hash, so revalidation keeps comparing them by ``content_hash``.
"""

from __future__ import annotations

import importlib.util
import os
from collections.abc import AsyncIterator, Callable
from pathlib import Path
from types import ModuleType
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session

from app.db import engine
from app.news_automation.models import NewsCandidate, NewsEvidence, NewsSource

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0112_news_evidence_body_hash"
EVIDENCE = "news_evidence"
CANDIDATES = "news_candidates"
INDEX = "ix_news_candidates_body_hash"


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


def indexes(connection: Connection, table: str) -> set[str]:
    return {str(index.get("name")) for index in sa.inspect(connection).get_indexes(table)}


def plant(session: Session) -> tuple[UUID, UUID]:
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
        status="manual_review",
        canonical_url=f"https://{marker}.example/story",
        source_title="Migration candidate",
        normalized_title=f"migration candidate {marker}",
        content_hash=marker * 2,
        idempotency_key=marker * 2,
    )
    session.add(candidate)
    session.flush()
    evidence = NewsEvidence(
        candidate_id=candidate.id,
        role="evidence",
        url=f"https://{marker}.example/story",
        title="Migration evidence",
        content_hash=marker * 2,
        excerpt="Stored before the body hash existed.",
    )
    session.add(evidence)
    session.flush()
    return candidate.id, evidence.id


def body_hash(connection: Connection, table: str, row_id: UUID) -> object:
    return connection.execute(
        sa.text(f"SELECT body_hash FROM {table} WHERE id = :id"), {"id": row_id}
    ).scalar()


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
    candidate_id, evidence_id = plant(Session(bind=connection))
    connection.execute(sa.text(f"DROP INDEX IF EXISTS {INDEX}"))
    for table in (EVIDENCE, CANDIDATES):
        connection.execute(sa.text(f"ALTER TABLE {table} DROP COLUMN IF EXISTS body_hash"))
        assert "body_hash" not in columns(connection, table)

    run(connection, "upgrade")
    assert "body_hash" in columns(connection, EVIDENCE)
    assert "body_hash" in columns(connection, CANDIDATES)
    assert INDEX in indexes(connection, CANDIDATES)
    # Stored rows have no body hash: revalidation compares them by content_hash.
    assert body_hash(connection, EVIDENCE, evidence_id) is None
    assert body_hash(connection, CANDIDATES, candidate_id) is None
    value = "body-v1:" + "a" * 64
    connection.execute(
        sa.text(f"UPDATE {EVIDENCE} SET body_hash = :value WHERE id = :id"),
        {"value": value, "id": evidence_id},
    )
    # Idempotent: a second upgrade finds everything and changes nothing.
    run(connection, "upgrade")
    assert body_hash(connection, EVIDENCE, evidence_id) == value

    run(connection, "downgrade")
    assert "body_hash" not in columns(connection, EVIDENCE)
    assert "body_hash" not in columns(connection, CANDIDATES)
    assert INDEX not in indexes(connection, CANDIDATES)
    assert connection.execute(
        sa.text(f"SELECT count(*) FROM {EVIDENCE} WHERE id = :id"), {"id": evidence_id}
    ).scalar() == 1
    run(connection, "downgrade")
    run(connection, "upgrade")
    assert "body_hash" in columns(connection, EVIDENCE)


@pytest.mark.asyncio(loop_scope="module")
async def test_0112_adds_the_body_hash_columns_and_comes_back_off() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
