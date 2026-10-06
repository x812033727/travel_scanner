"""0125 adds the news review judge: its settings, a candidate's verdict and the assessment type.

The guard and offline SQL tests run without a database, as in
``test_migration_0124_video_review_subject``. The PostgreSQL test takes the columns off a
real database and narrows the assessment check again, runs the migration through a real
alembic context, and checks both directions inside one rolled back transaction, the way
``test_migration_0094_news_final_editor`` does.
"""

from __future__ import annotations

import importlib.util
import io
import os
from collections.abc import AsyncIterator, Callable
from pathlib import Path
from types import ModuleType
from typing import cast
from unittest.mock import Mock
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import Table
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session

from app.db import Base, engine
from app.news_automation.models import (
    NewsAssessment,
    NewsAutomationSettings,
    NewsCandidate,
    NewsSource,
)

POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0125_news_review_judge"
SETTINGS = "news_automation_settings"
CANDIDATES = "news_candidates"
ASSESSMENTS = "news_assessments"
PROVIDER_CHECK = "ck_news_judge_provider"
DECISION_CHECK = "ck_news_candidate_judge_decision"
TYPE_CHECK = "ck_news_assessment_type"
SETTINGS_COLUMNS = {"judge_enabled", "judge_provider", "judge_model"}
CANDIDATE_COLUMNS = {"judge_decision", "judge_hold"}
# The check 0084 created, which 0125 widens and its downgrade puts back.
OLD_TYPE_CHECK = "assessment_type IN ('duplicate','verification','locale_review','jev','human')"


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


def declared_checks(model: type[Base]) -> dict[str, str]:
    return {
        str(constraint.name): str(constraint.sqltext)
        for constraint in cast(Table, model.__table__).constraints
        if isinstance(constraint, sa.CheckConstraint)
    }


def test_the_migration_writes_the_checks_the_models_declare() -> None:
    migration = load_migration()
    assert declared_checks(NewsAutomationSettings)[PROVIDER_CHECK] == migration.PROVIDERS
    assert declared_checks(NewsCandidate)[DECISION_CHECK] == migration.DECISIONS
    widened = migration._type_check((*migration.TYPES, migration.NEW_TYPE))
    assert declared_checks(NewsAssessment)[TYPE_CHECK] == widened
    assert migration._type_check(migration.TYPES).replace(", ", ",") == OLD_TYPE_CHECK


def test_a_database_that_already_has_the_judge_is_left_alone(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    migration = load_migration()
    operations = Mock()
    widened = migration._type_check((*migration.TYPES, migration.NEW_TYPE))
    monkeypatch.setattr(migration, "op", operations)
    monkeypatch.setattr(migration, "_offline", lambda: False)
    monkeypatch.setattr(migration, "_columns", lambda _table: SETTINGS_COLUMNS | CANDIDATE_COLUMNS)
    monkeypatch.setattr(migration, "_existing_type_check", lambda _assumed: widened)
    migration.upgrade()
    assert operations.mock_calls == []


@pytest.mark.parametrize("direction", ["upgrade", "downgrade"])
def test_offline_sql_does_not_inspect_a_database(
    direction: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    migration = load_migration()
    monkeypatch.setattr(
        migration.sa,
        "inspect",
        lambda _connection: pytest.fail("offline SQL must not inspect a database"),
    )
    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": output}
    )
    with Operations.context(context):
        getattr(migration, direction)()
    sql = output.getvalue()
    rewritten = sql.index(f"ADD CONSTRAINT {TYPE_CHECK} CHECK (assessment_type IN ('duplicate', ")
    if direction == "upgrade":
        for statement in (
            f"ALTER TABLE {SETTINGS} ADD COLUMN judge_enabled BOOLEAN DEFAULT false NOT NULL;",
            f"ALTER TABLE {SETTINGS} ADD COLUMN judge_provider VARCHAR(16) "
            "DEFAULT 'anthropic' NOT NULL;",
            f"ALTER TABLE {SETTINGS} ADD CONSTRAINT {PROVIDER_CHECK} CHECK (judge_provider IN ",
            f"ALTER TABLE {SETTINGS} ADD COLUMN judge_model VARCHAR(128);",
            f"UPDATE {SETTINGS} SET judge_model=",
            f"ALTER TABLE {CANDIDATES} ADD COLUMN judge_decision VARCHAR(16);",
            f"ALTER TABLE {CANDIDATES} ADD CONSTRAINT {DECISION_CHECK} CHECK (judge_decision IS ",
            f"ALTER TABLE {CANDIDATES} ADD COLUMN judge_hold VARCHAR(64);",
            f"ALTER TABLE {ASSESSMENTS} DROP CONSTRAINT {TYPE_CHECK};",
        ):
            assert statement in sql
        assert sql[rewritten:].count("'judge'") == 1
    else:
        # The judge's rows go before the check that would refuse them comes back.
        deleted = sql.index(f"DELETE FROM {ASSESSMENTS} WHERE assessment_type = 'judge';")
        assert deleted < sql.index(f"DROP CONSTRAINT {TYPE_CHECK};") < rewritten
        assert "'judge'" not in sql[rewritten:]
        for name in (PROVIDER_CHECK, DECISION_CHECK):
            assert f"DROP CONSTRAINT {name};" in sql
        for column in SETTINGS_COLUMNS:
            assert f"ALTER TABLE {SETTINGS} DROP COLUMN {column};" in sql
        for column in CANDIDATE_COLUMNS:
            assert f"ALTER TABLE {CANDIDATES} DROP COLUMN {column};" in sql


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def postgres_engine() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def columns(connection: Connection, table: str) -> set[str]:
    return {column["name"] for column in sa.inspect(connection).get_columns(table)}


def checks(connection: Connection, table: str) -> dict[str, str]:
    return {
        str(check.get("name")): str(check.get("sqltext") or "")
        for check in sa.inspect(connection).get_check_constraints(table)
    }


def plant_candidate(session: Session) -> UUID:
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
        error_code="news_zh_draft_ready",
    )
    session.add(candidate)
    session.flush()
    return candidate.id


def plant_assessment(connection: Connection, candidate_id: UUID, assessment_type: str) -> UUID:
    session = Session(bind=connection)
    row = NewsAssessment(
        candidate_id=candidate_id,
        assessment_type=assessment_type,
        verdict="manual",
        prompt_version="news-v1",
    )
    session.add(row)
    session.flush()
    session.close()
    return row.id


def assessments_of(connection: Connection, candidate_id: UUID) -> set[str]:
    rows = connection.execute(
        sa.text(f"SELECT id FROM {ASSESSMENTS} WHERE candidate_id = :id"), {"id": candidate_id}
    )
    return {str(row[0]) for row in rows}


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
    # The rows go in first: the models name the new columns, which are about to be dropped.
    session = Session(bind=connection)
    if session.get(NewsAutomationSettings, 1) is None:
        session.add(NewsAutomationSettings(id=1))
        session.flush()
    candidate_id = plant_candidate(session)
    session.close()
    earlier = plant_assessment(connection, candidate_id, "jev")
    connection.execute(sa.text(f"ALTER TABLE {SETTINGS} DROP CONSTRAINT {PROVIDER_CHECK}"))
    for column in sorted(SETTINGS_COLUMNS):
        connection.execute(sa.text(f"ALTER TABLE {SETTINGS} DROP COLUMN {column}"))
    connection.execute(sa.text(f"ALTER TABLE {CANDIDATES} DROP CONSTRAINT {DECISION_CHECK}"))
    for column in sorted(CANDIDATE_COLUMNS):
        connection.execute(sa.text(f"ALTER TABLE {CANDIDATES} DROP COLUMN {column}"))
    connection.execute(sa.text(f"ALTER TABLE {ASSESSMENTS} DROP CONSTRAINT {TYPE_CHECK}"))
    connection.execute(
        sa.text(f"ALTER TABLE {ASSESSMENTS} ADD CONSTRAINT {TYPE_CHECK} CHECK ({OLD_TYPE_CHECK})")
    )

    run(connection, "upgrade")
    assert SETTINGS_COLUMNS <= columns(connection, SETTINGS)
    assert CANDIDATE_COLUMNS <= columns(connection, CANDIDATES)
    assert PROVIDER_CHECK in checks(connection, SETTINGS)
    assert DECISION_CHECK in checks(connection, CANDIDATES)
    assert "judge" in checks(connection, ASSESSMENTS)[TYPE_CHECK]
    settings = connection.execute(
        sa.text(f"SELECT judge_enabled, judge_provider, judge_model FROM {SETTINGS} WHERE id = 1")
    ).one()
    assert tuple(settings) == (False, "anthropic", "claude-opus-5-5")
    answered = sa.text(f"SELECT judge_decision, judge_hold FROM {CANDIDATES} WHERE id = :id")
    assert tuple(connection.execute(answered, {"id": candidate_id}).one()) == (None, None)

    # The new values are accepted, and the checks refuse anything else.
    answer = sa.text(
        f"UPDATE {CANDIDATES} SET judge_decision = :decision, judge_hold = error_code "
        "WHERE id = :id"
    )
    connection.execute(answer, {"decision": "manual", "id": candidate_id})
    with pytest.raises(sa.exc.IntegrityError), connection.begin_nested():
        connection.execute(answer, {"decision": "rewrite", "id": candidate_id})
    with pytest.raises(sa.exc.IntegrityError), connection.begin_nested():
        connection.execute(sa.text(f"UPDATE {SETTINGS} SET judge_provider = 'nobody'"))
    judged = plant_assessment(connection, candidate_id, "judge")
    assert assessments_of(connection, candidate_id) == {str(earlier), str(judged)}

    # Idempotent: a second upgrade finds the columns and the wider check and changes nothing.
    run(connection, "upgrade")
    assert "judge" in checks(connection, ASSESSMENTS)[TYPE_CHECK]
    assert tuple(connection.execute(answered, {"id": candidate_id}).one()) == (
        "manual",
        "news_zh_draft_ready",
    )

    run(connection, "downgrade")
    assert not SETTINGS_COLUMNS & columns(connection, SETTINGS)
    assert not CANDIDATE_COLUMNS & columns(connection, CANDIDATES)
    assert PROVIDER_CHECK not in checks(connection, SETTINGS)
    assert DECISION_CHECK not in checks(connection, CANDIDATES)
    assert "judge" not in checks(connection, ASSESSMENTS)[TYPE_CHECK]
    # Only the judge's assessment went with it, and the narrowed check is back in force.
    assert assessments_of(connection, candidate_id) == {str(earlier)}
    with pytest.raises(sa.exc.IntegrityError), connection.begin_nested():
        connection.execute(
            sa.text(f"UPDATE {ASSESSMENTS} SET assessment_type = 'judge' WHERE id = :id"),
            {"id": earlier},
        )


@POSTGRES
@pytest.mark.usefixtures("postgres_engine")
@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_adds_the_judge_with_its_defaults_and_downgrade_removes_it() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise))
