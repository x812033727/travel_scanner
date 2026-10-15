"""The pilot's durable dollar holds, idempotency, and migration contract."""

from __future__ import annotations

import asyncio
import importlib.util
import io
import os
from collections.abc import AsyncIterator
from decimal import Decimal
from functools import partial
from pathlib import Path

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import engine as postgres_engine
from app.problems import AppError
from app.video_budget import service
from app.video_budget.models import (
    PILOT_LIMIT_USD,
    PILOT_SLUGS,
    VideoPilotBudget,
    VideoPilotBudgetOperation,
)

SLUG = "story-rolling-suitcase"
OTHER_SLUG = "story-conveyor-belt-sushi"
V2_SLUG = "story-rolling-suitcase-v2"
OTHER_V2_SLUG = "story-conveyor-belt-sushi-v2"
MIGRATION_SOURCE = (
    Path(__file__).resolve().parents[1] / "migrations" / "versions" / "0132_video_pilot_budget.py"
)


@pytest_asyncio.fixture
async def sessions(tmp_path: Path) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    database = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'budget.db'}")
    async with database.begin() as connection:
        await connection.run_sync(
            lambda sync: VideoPilotBudget.metadata.create_all(
                sync, tables=[VideoPilotBudget.__table__, VideoPilotBudgetOperation.__table__]
            )
        )
        await connection.execute(
            sa.insert(VideoPilotBudget),
            [{"slug": slug, "limit_usd": PILOT_LIMIT_USD} for slug in PILOT_SLUGS],
        )
    yield async_sessionmaker(database, expire_on_commit=False)
    await database.dispose()


async def _reserve(
    sessions: async_sessionmaker[AsyncSession],
    operation_id: str,
    cost: str | None,
    *,
    slug: str = SLUG,
    category: str = "image",
) -> service.Reservation | None:
    async with sessions() as session:
        return await service.reserve(
            session,
            slug=slug,
            operation_id=operation_id,
            category=category,
            provider="minimax",
            model="image-01",
            max_usd=Decimal(cost) if cost is not None else None,
        )


async def _summary(
    sessions: async_sessionmaker[AsyncSession], slug: str = SLUG
) -> service.BudgetSummary | None:
    async with sessions() as session:
        return await service.summary(session, slug)


@pytest.mark.asyncio
async def test_cross_stage_reservations_hold_exactly_at_boundary(
    sessions: async_sessionmaker[AsyncSession],
) -> None:
    first = await _reserve(sessions, "picture-1", "10", category="image")
    second = await _reserve(sessions, "speech-1", "15", category="speech")
    assert first is not None and first.dispatch_allowed
    assert second is not None and second.dispatch_allowed
    view = await _summary(sessions)
    assert view is not None
    assert (view.reserved_usd, view.settled_usd, view.remaining_usd) == (
        Decimal("25"),
        Decimal("0"),
        Decimal("0"),
    )
    with pytest.raises(AppError) as refused:
        await _reserve(sessions, "picture-2", "0.000001")
    assert refused.value.code == "video_budget_exhausted"
    assert (await _summary(sessions, OTHER_SLUG)).remaining_usd == PILOT_LIMIT_USD  # type: ignore[union-attr]


@pytest.mark.asyncio
async def test_v2_remakes_have_independent_accounts_and_legacy_slugs_stay_protected(
    sessions: async_sessionmaker[AsyncSession],
) -> None:
    assert PILOT_SLUGS == {SLUG, OTHER_SLUG, V2_SLUG, OTHER_V2_SLUG}
    for slug in (SLUG, OTHER_SLUG, V2_SLUG, OTHER_V2_SLUG):
        hold = await _reserve(sessions, "full-film", "25", slug=slug)
        assert hold is not None and hold.dispatch_allowed
    for slug in PILOT_SLUGS:
        view = await _summary(sessions, slug)
        assert view is not None
        assert view.remaining_usd == 0
        assert view.reserved_usd == PILOT_LIMIT_USD


@pytest.mark.asyncio
async def test_retry_requires_a_proven_no_charge_release(
    sessions: async_sessionmaker[AsyncSession],
) -> None:
    first = await _reserve(sessions, "fixed-operation", "7")
    repeated = await _reserve(sessions, "fixed-operation", "7")
    assert first is not None and first.dispatch_allowed and first.attempts == 1
    assert repeated is not None and not repeated.dispatch_allowed
    with pytest.raises(AppError) as conflict:
        await _reserve(sessions, "fixed-operation", "8")
    assert conflict.value.code == "video_budget_operation_conflict"
    async with sessions() as session:
        await service.release(
            session,
            slug=SLUG,
            operation_id="fixed-operation",
            reason="provider rejected request before generation",
        )
    assert (await _summary(sessions)).remaining_usd == PILOT_LIMIT_USD  # type: ignore[union-attr]
    again = await _reserve(sessions, "fixed-operation", "7")
    assert again is not None and again.dispatch_allowed and again.attempts == 2
    async with sessions() as session:
        await service.settle(
            session,
            slug=SLUG,
            operation_id="fixed-operation",
            actual_usd=Decimal("6.2"),
            receipt_ref="vendor-receipt-1",
        )
    settled = await _reserve(sessions, "fixed-operation", "7")
    assert settled is not None and not settled.dispatch_allowed and settled.status == "settled"
    view = await _summary(sessions)
    assert view is not None
    assert (view.reserved_usd, view.settled_usd, view.remaining_usd) == (
        Decimal("0"),
        Decimal("6.2"),
        Decimal("18.8"),
    )


@pytest.mark.asyncio
async def test_timeout_hold_survives_and_can_be_reconciled(
    sessions: async_sessionmaker[AsyncSession],
) -> None:
    await _reserve(sessions, "transcribe-1", "20", category="transcription")
    async with sessions() as session:
        await service.mark_uncertain(session, slug=SLUG, operation_id="transcribe-1")
    duplicate = await _reserve(sessions, "transcribe-1", "20", category="transcription")
    assert duplicate is not None and duplicate.status == "uncertain"
    assert not duplicate.dispatch_allowed
    view = await _summary(sessions)
    assert view is not None and view.uncertain_operations == 1
    assert view.remaining_usd == Decimal("5")
    with pytest.raises(AppError) as refused:
        await _reserve(sessions, "other", "5.000001")
    assert refused.value.code == "video_budget_exhausted"
    async with sessions() as session:
        await service.settle(
            session, slug=SLUG, operation_id="transcribe-1", actual_usd=Decimal("1.25")
        )
    assert (await _summary(sessions)).remaining_usd == Decimal("23.75")  # type: ignore[union-attr]


@pytest.mark.asyncio
async def test_unknown_or_expired_prices_fail_closed_and_third_slug_is_unchanged(
    sessions: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch
) -> None:
    with pytest.raises(AppError) as unknown:
        await _reserve(sessions, "missing-price", None)
    assert unknown.value.code == "video_budget_price_unknown"
    with pytest.raises(AppError) as zero:
        await _reserve(sessions, "zero-price", "0")
    assert zero.value.code == "video_budget_price_unknown"
    with pytest.raises(AppError) as not_finite:
        await _reserve(sessions, "nan-price", "NaN")
    assert not_finite.value.code == "video_budget_price_unknown"
    monkeypatch.setattr(service, "price_window_current", lambda: False)
    with pytest.raises(AppError) as expired:
        await _reserve(sessions, "expired-price", "1")
    assert expired.value.code == "video_budget_price_expired"
    assert await _reserve(sessions, "other-video", None, slug="a-third-story") is None


@pytest.mark.asyncio
async def test_actual_over_reservation_is_recorded_and_stops_further_spending(
    sessions: async_sessionmaker[AsyncSession],
) -> None:
    await _reserve(sessions, "estimate", "2")
    async with sessions() as session:
        with pytest.raises(AppError) as overrun:
            await service.settle(
                session, slug=SLUG, operation_id="estimate", actual_usd=Decimal("2.000001")
            )
    assert overrun.value.code == "video_budget_actual_exceeds_reservation"
    view = await _summary(sessions)
    assert view is not None
    assert view.reserved_usd == 0
    assert view.settled_usd == Decimal("2.000001")
    assert view.remaining_usd == Decimal("22.999999")
    assert view.overrun_operations == 1
    with pytest.raises(AppError) as held:
        await _reserve(sessions, "after-overrun", "0.01")
    assert held.value.code == "video_budget_overrun_hold"


def test_migration_offline_sql_creates_both_tables_and_seeds_all_pilots() -> None:
    spec = importlib.util.spec_from_file_location("pilot_budget_migration", MIGRATION_SOURCE)
    assert spec is not None and spec.loader is not None
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    assert migration.down_revision == "0131_video_dub_retries"
    assert len(migration.revision) <= 32
    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": output}
    )
    with Operations.context(context):
        migration.upgrade()
    sql = output.getvalue()
    assert "CREATE TABLE video_pilot_budgets" in sql
    assert "CREATE TABLE video_pilot_budget_operations" in sql
    assert "ON CONFLICT (slug) DO NOTHING" in sql
    assert sql.count("INSERT INTO video_pilot_budgets") == 4


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.asyncio
async def test_migration_creates_and_seeds_accounts_on_existing_database() -> None:
    spec = importlib.util.spec_from_file_location("pilot_budget_migration_live", MIGRATION_SOURCE)
    assert spec is not None and spec.loader is not None
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)

    def exercise(connection: sa.Connection, precreated_without_default: bool) -> None:
        transaction = connection.begin()
        try:
            connection.execute(sa.text("DROP TABLE IF EXISTS video_pilot_budget_operations"))
            connection.execute(sa.text("DROP TABLE IF EXISTS video_pilot_budgets"))
            if precreated_without_default:
                # 0001_initial creates tables from today's ORM metadata before later
                # migrations run. Verify the seed also works with a NOT NULL column
                # whose older table definition has no database default.
                connection.execute(
                    sa.text(
                        "CREATE TABLE video_pilot_budgets ("
                        "slug VARCHAR(80) PRIMARY KEY, "
                        "limit_usd NUMERIC(12, 6) NOT NULL, "
                        "created_at TIMESTAMPTZ NOT NULL)"
                    )
                )
            with Operations.context(MigrationContext.configure(connection)):
                migration.upgrade()
                migration.upgrade()
                rows = connection.execute(
                    sa.text(
                        "SELECT slug, limit_usd, created_at "
                        "FROM video_pilot_budgets ORDER BY slug"
                    )
                ).all()
                assert [(row.slug, row.limit_usd) for row in rows] == [
                    ("story-conveyor-belt-sushi", Decimal("25.000000")),
                    ("story-conveyor-belt-sushi-v2", Decimal("25.000000")),
                    ("story-rolling-suitcase", Decimal("25.000000")),
                    ("story-rolling-suitcase-v2", Decimal("25.000000")),
                ]
                assert all(row.created_at is not None for row in rows)
                migration.downgrade()
            assert "video_pilot_budgets" not in sa.inspect(connection).get_table_names()
        finally:
            transaction.rollback()

    # Both database shapes must use the same async event loop for the pooled engine.
    try:
        for precreated_without_default in (False, True):
            async with postgres_engine.connect() as connection:
                await connection.run_sync(
                    partial(exercise, precreated_without_default=precreated_without_default)
                )
    finally:
        # pytest gives the next integration test another loop; pooled asyncpg
        # connections must not cross that loop boundary.
        await postgres_engine.dispose()


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.asyncio
async def test_postgres_row_lock_prevents_concurrent_over_reservation() -> None:
    """Two independent sessions race for the same $25 account; exactly one can hold $15."""
    slug = OTHER_SLUG
    async with postgres_engine.begin() as connection:
        await connection.execute(
            sa.delete(VideoPilotBudgetOperation).where(VideoPilotBudgetOperation.slug == slug)
        )
        await connection.execute(
            sa.text(
                "INSERT INTO video_pilot_budgets (slug, limit_usd) VALUES (:slug, 25) "
                "ON CONFLICT (slug) DO NOTHING"
            ),
            {"slug": slug},
        )

    async def contender(operation_id: str) -> bool:
        async with async_sessionmaker(postgres_engine, expire_on_commit=False)() as session:
            try:
                hold = await service.reserve(
                    session,
                    slug=slug,
                    operation_id=operation_id,
                    category="image",
                    provider="minimax",
                    model="image-01",
                    max_usd=Decimal("15"),
                )
                return bool(hold and hold.dispatch_allowed)
            except AppError as error:
                assert error.code == "video_budget_exhausted"
                return False

    try:
        results = await asyncio.gather(contender("race-a"), contender("race-b"))
        assert sorted(results) == [False, True]
        async with async_sessionmaker(postgres_engine)() as session:
            view = await service.summary(session, slug)
        assert view is not None and view.reserved_usd == Decimal("15")
    finally:
        try:
            async with postgres_engine.begin() as connection:
                await connection.execute(
                    sa.delete(VideoPilotBudgetOperation).where(
                        VideoPilotBudgetOperation.slug == slug
                    )
                )
        finally:
            await postgres_engine.dispose()
