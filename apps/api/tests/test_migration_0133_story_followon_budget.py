"""The six smaller story ceilings retain prior charges and create no shared pool."""

from __future__ import annotations

import importlib.util
import io
import os
from decimal import Decimal
from pathlib import Path
from types import ModuleType
from uuid import uuid4

import pytest
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations

from app.db import engine
from app.video_budget.models import VideoPilotBudgetOperation

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "migrations"
    / "versions"
    / "0133_story_followon_budget.py"
)
OLD_SOURCE = SOURCE.with_name("0132_video_pilot_budget.py")
B18_V2 = "story-conveyor-belt-sushi-v2"
FOLLOWONS = (
    "story-five-lego-legoland",
    "story-five-costco-hot-dog",
    "story-five-adidas-puma-brothers",
    "story-five-ajinomoto-chip-film",
    "story-five-pringles-vat-case",
)


def load_migration(source: Path = SOURCE) -> ModuleType:
    spec = importlib.util.spec_from_file_location(source.stem, source)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_offline_sql_changes_only_the_ceiling_and_exact_accounts() -> None:
    migration = load_migration()
    assert migration.down_revision == "0132_video_pilot_budget"
    assert len(migration.revision) <= 32
    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": output}
    )
    with Operations.context(context):
        migration.upgrade()
    sql = output.getvalue()
    assert "DROP CONSTRAINT ck_video_pilot_budget_limit" in sql
    assert "limit_usd IN (5.000000, 25.000000)" in sql
    assert "UPDATE video_pilot_budgets" in sql
    assert sql.count("INSERT INTO video_pilot_budgets") == len(FOLLOWONS)
    assert "DELETE FROM video_pilot_budget_operations" not in sql
    assert "DROP TABLE video_pilot_budget_operations" not in sql


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.asyncio
async def test_existing_b18_operations_survive_real_upgrade_and_repeat() -> None:
    migration = load_migration()
    old_migration = load_migration(OLD_SOURCE)

    def exercise(connection: sa.Connection) -> None:
        transaction = connection.begin()
        try:
            connection.execute(sa.text("DROP TABLE IF EXISTS video_pilot_budget_operations"))
            connection.execute(sa.text("DROP TABLE IF EXISTS video_pilot_budgets"))
            with Operations.context(MigrationContext.configure(connection)):
                old_migration.upgrade()

            for operation_id, status, maximum, actual in (
                ("already-settled", "settled", "2.000000", "1.500000"),
                ("still-uncertain", "uncertain", "2.000000", None),
            ):
                connection.execute(
                    sa.insert(VideoPilotBudgetOperation).values(
                        id=uuid4(), slug=B18_V2, operation_id=operation_id,
                        category="speech", provider="gemini", model="test-model",
                        max_usd=Decimal(maximum),
                        actual_usd=Decimal(actual) if actual is not None else None,
                        status=status, attempts=1,
                    )
                )
            with Operations.context(MigrationContext.configure(connection)):
                migration.upgrade()
                migration.upgrade()
                with pytest.raises(RuntimeError, match="cannot be downgraded"):
                    migration.downgrade()

            rows = connection.execute(
                sa.text("SELECT slug, limit_usd FROM video_pilot_budgets ORDER BY slug")
            ).all()
            limits = {row.slug: row.limit_usd for row in rows}
            assert limits[B18_V2] == Decimal("5.000000")
            assert all(limits[slug] == Decimal("5.000000") for slug in FOLLOWONS)
            assert limits["story-rolling-suitcase-v2"] == Decimal("25.000000")
            operations = connection.execute(
                sa.text(
                    "SELECT operation_id, status, max_usd, actual_usd "
                    "FROM video_pilot_budget_operations WHERE slug=:slug ORDER BY operation_id"
                ),
                {"slug": B18_V2},
            ).all()
            actual_rows = [
                (row.operation_id, row.status, row.max_usd, row.actual_usd)
                for row in operations
            ]
            assert actual_rows == [
                ("already-settled", "settled", Decimal("2.000000"), Decimal("1.500000")),
                ("still-uncertain", "uncertain", Decimal("2.000000"), None),
            ]
        finally:
            transaction.rollback()

    try:
        async with engine.connect() as connection:
            await connection.run_sync(exercise)
    finally:
        # Asyncpg connections in the shared engine cannot cross pytest's event loops.
        await engine.dispose()
