"""0088 adds ``needs_redraft`` to ``ck_news_candidate_status`` and moves the rows.

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
from app.guides.models import GuideArticle
from app.news_automation.models import NewsCandidate, NewsSource

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0088_news_needs_redraft_status"
TABLE = "news_candidates"
CONSTRAINT = "ck_news_candidate_status"
OLD_CHECK = (
    "status IN ('discovered','drafting','verifying','locale_review','jev_review',"
    "'shadow_review','manual_review','needs_evidence','published','duplicate','rejected',"
    "'failed')"
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


def plant(
    session: Session, status: str, error_code: str | None, *, with_article: bool = False
) -> NewsCandidate:
    marker = uuid4().hex
    article_id = None
    if with_article:
        article = GuideArticle(slug=f"ai-news-migration-{marker[:12]}", kind="life")
        session.add(article)
        session.flush()
        article_id = article.id
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
        guide_article_id=article_id,
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
    stopped = {
        code: plant(session, "manual_review", code)
        for code in (
            "news_claim_source_invalid",
            "news_event_date_invalid",
            "news_verification_failed",
            "news_locale_review_failed",
            "news_hard_checks_failed",
        )
    }
    # These have a five-locale article or a question only a person can answer.
    decided = [
        plant(session, "manual_review", "news_jev_manual"),
        plant(session, "manual_review", "news_duplicate_uncertain"),
        plant(session, "manual_review", "news_evidence_changed"),
        # A re-verified article the editor can still fix in the guide editor.
        plant(session, "manual_review", "news_verification_failed", with_article=True),
    ]
    failed = plant(session, "failed", "news_verification_failed")

    run(connection, "upgrade")
    assert "needs_redraft" in check_text(connection)
    assert {code: status_of(connection, row) for code, row in stopped.items()} == {
        code: "needs_redraft" for code in stopped
    }
    assert [status_of(connection, row) for row in decided] == ["manual_review"] * 4
    assert status_of(connection, failed) == "failed"
    # Idempotent: a second upgrade leaves the widened constraint alone.
    run(connection, "upgrade")
    assert "needs_redraft" in check_text(connection)

    run(connection, "downgrade")
    assert "needs_redraft" not in check_text(connection)
    assert {status_of(connection, row) for row in stopped.values()} == {"manual_review"}
    run(connection, "downgrade")


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_moves_stopped_before_draft_rows_and_downgrade_restores_them() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
