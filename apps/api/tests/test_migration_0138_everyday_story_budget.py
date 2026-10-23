"""Everyday story accounts open without a fresh balance for films with unrecorded history."""

from __future__ import annotations

import importlib.util
import io
import os
from decimal import Decimal
from pathlib import Path
from types import ModuleType

import pytest
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations

from app.db import engine
from app.video_budget.models import (
    EVERYDAY_PILOT_SLUGS,
    HISTORICAL_HOLD_OPERATION_ID,
    PILOT_LIMIT_USD,
    UNRECONCILED_STORY_SLUGS,
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
SOURCE = VERSIONS / "0138_everyday_story_budget.py"


def load_migration(source: Path = SOURCE) -> ModuleType:
    spec = importlib.util.spec_from_file_location(source.stem, source)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_migration_matches_the_application_account_set() -> None:
    migration = load_migration()
    assert migration.down_revision == "0137_video_manga_tier"
    assert len(migration.revision) <= 32
    assert set(migration.UNRECONCILED) == UNRECONCILED_STORY_SLUGS
    assert set(migration.UNRECONCILED + migration.FRESH) == EVERYDAY_PILOT_SLUGS
    assert migration.HISTORICAL_HOLD == HISTORICAL_HOLD_OPERATION_ID
    assert Decimal(migration.LIMIT_USD) == PILOT_LIMIT_USD


def test_offline_sql_only_inserts_accounts_and_holds() -> None:
    migration = load_migration()
    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": output}
    )
    with Operations.context(context):
        migration.upgrade()
    sql = output.getvalue()
    assert sql.count("INSERT INTO video_pilot_budgets") == len(EVERYDAY_PILOT_SLUGS)
    assert sql.count("INSERT INTO video_pilot_budget_operations") == len(
        UNRECONCILED_STORY_SLUGS
    )
    assert sql.count("ON CONFLICT") == len(EVERYDAY_PILOT_SLUGS) + len(UNRECONCILED_STORY_SLUGS)
    for statement in ("UPDATE ", "DELETE ", "DROP "):
        assert statement not in sql


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.asyncio
async def test_real_upgrade_holds_history_and_never_reopens_a_settled_hold() -> None:
    migration = load_migration()
    earlier = [
        load_migration(VERSIONS / name)
        for name in ("0132_video_pilot_budget.py", "0133_story_followon_budget.py")
    ]
    c05 = "story-everyday-kincho-c05"

    def exercise(connection: sa.Connection) -> None:
        transaction = connection.begin()
        try:
            connection.execute(sa.text("DROP TABLE IF EXISTS video_pilot_budget_operations"))
            connection.execute(sa.text("DROP TABLE IF EXISTS video_pilot_budgets"))
            with Operations.context(MigrationContext.configure(connection)):
                for step in earlier:
                    step.upgrade()
                migration.upgrade()
            # An operator settles C05's hold; a repeated upgrade must leave it settled.
            connection.execute(
                sa.text(
                    "UPDATE video_pilot_budget_operations SET status='settled', "
                    "actual_usd=1.250000, receipt_ref='invoice-test' "
                    "WHERE slug=:slug AND operation_id=:op"
                ),
                {"slug": c05, "op": HISTORICAL_HOLD_OPERATION_ID},
            )
            with Operations.context(MigrationContext.configure(connection)):
                migration.upgrade()
                with pytest.raises(RuntimeError, match="cannot be downgraded"):
                    migration.downgrade()

            limits = dict(
                connection.execute(
                    sa.text("SELECT slug, limit_usd FROM video_pilot_budgets")
                ).all()
            )
            assert all(limits[slug] == PILOT_LIMIT_USD for slug in EVERYDAY_PILOT_SLUGS)
            assert limits["story-five-lego-legoland"] == Decimal("5.000000")
            holds = connection.execute(
                sa.text(
                    "SELECT slug, operation_id, category, max_usd, actual_usd, status "
                    "FROM video_pilot_budget_operations "
                    "WHERE slug LIKE 'story-everyday-%' ORDER BY slug"
                )
            ).all()
            assert {row.slug for row in holds} == UNRECONCILED_STORY_SLUGS
            for row in holds:
                assert (row.operation_id, row.category, row.max_usd) == (
                    HISTORICAL_HOLD_OPERATION_ID,
                    "historical",
                    PILOT_LIMIT_USD,
                )
                expected = ("settled", Decimal("1.250000")) if row.slug == c05 else (
                    "uncertain",
                    None,
                )
                assert (row.status, row.actual_usd) == expected
        finally:
            transaction.rollback()

    try:
        async with engine.connect() as connection:
            await connection.run_sync(exercise)
    finally:
        # Asyncpg connections in the shared engine cannot cross pytest's event loops.
        await engine.dispose()
