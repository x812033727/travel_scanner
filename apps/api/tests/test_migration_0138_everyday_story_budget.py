"""0138 must seed held film accounts without losing old or later budget evidence."""

from __future__ import annotations

import asyncio
import importlib.util
import io
import os
import subprocess
import sys
from collections.abc import Callable
from decimal import Decimal
from pathlib import Path
from types import ModuleType
from uuid import uuid4

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import URL, Connection, make_url
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import get_settings
from app.db import engine
from app.migration_guard import C20_PILOT_SLUG, _verify_reviewed_0138
from app.video_budget.models import (
    ACTIVATED_STORY_SLUGS,
    C_SERIES_PILOT_LIMITS_USD,
    PILOT_LIMITS_USD,
    VideoPilotBudget,
    VideoPilotBudgetOperation,
)
from app.video_budget.service import is_preproduction_held

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "migrations"
    / "versions"
    / "0138_everyday_story_budget.py"
)
API_ROOT = SOURCE.parents[2]
POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


def load_migration() -> ModuleType:
    spec = importlib.util.spec_from_file_location("migration_0138_everyday_story_budget", SOURCE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(connection: Connection, direction: str) -> None:
    with Operations.context(MigrationContext.configure(connection)):
        getattr(load_migration(), direction)()


def _prepare_0137(connection: Connection) -> None:
    migration = load_migration()
    # API shards start at the current head. Reconstruct the older 0137 account
    # inventory within this test transaction before exercising the 0138 migration.
    c20_ownership = "video_pilot_budget_0139_owned"
    if sa.inspect(connection).has_table(c20_ownership):
        c20_owner = connection.execute(
            sa.text(f"SELECT slug, account_created FROM {c20_ownership}")
        ).all()
        assert c20_owner == [(C20_PILOT_SLUG, True)]
        connection.execute(sa.text(f"DROP TABLE {c20_ownership}"))
        connection.execute(
            sa.delete(VideoPilotBudgetOperation).where(
                VideoPilotBudgetOperation.slug == C20_PILOT_SLUG
            )
        )
        connection.execute(
            sa.delete(VideoPilotBudget).where(VideoPilotBudget.slug == C20_PILOT_SLUG)
        )
    if sa.inspect(connection).has_table(migration.OWNERSHIP):
        connection.execute(sa.text(f"DROP TABLE {migration.OWNERSHIP}"))
    connection.execute(
        sa.delete(VideoPilotBudgetOperation).where(
            VideoPilotBudgetOperation.slug.in_(migration.PILOTS)
        )
    )
    connection.execute(
        sa.delete(VideoPilotBudget).where(VideoPilotBudget.slug.in_(migration.PILOTS))
    )


def _limits(connection: Connection) -> dict[str, Decimal]:
    return {
        slug: limit
        for slug, limit in connection.execute(
            sa.select(VideoPilotBudget.slug, VideoPilotBudget.limit_usd)
        ).all()
    }


def _hold(connection: Connection, slug: str) -> sa.RowMapping | None:
    return (
        connection.execute(
            sa.select(VideoPilotBudgetOperation.__table__).where(
                VideoPilotBudgetOperation.slug == slug,
                VideoPilotBudgetOperation.operation_id == "pre-ledger-history",
            )
        )
        .mappings()
        .one_or_none()
    )


def _owner(connection: Connection, slug: str) -> sa.RowMapping:
    owned = load_migration()._ownership()
    return connection.execute(sa.select(owned).where(owned.c.slug == slug)).mappings().one()


def _insert_account(connection: Connection, slug: str, limit: str = "25.000000") -> None:
    connection.execute(
        sa.insert(VideoPilotBudget).values(
            slug=slug, limit_usd=Decimal(limit), created_at=sa.func.now()
        )
    )


def _insert_operation(
    connection: Connection,
    slug: str,
    operation_id: str,
    *,
    model: str = "unattributed",
    status: str = "uncertain",
    actual_usd: Decimal | None = None,
    receipt_ref: str | None = None,
) -> None:
    connection.execute(
        sa.insert(VideoPilotBudgetOperation).values(
            id=uuid4(),
            slug=slug,
            operation_id=operation_id,
            category="historical" if operation_id == "pre-ledger-history" else "speech",
            provider="unattributed" if operation_id == "pre-ledger-history" else "gemini",
            model=model,
            max_usd=Decimal("25.000000") if operation_id == "pre-ledger-history" else Decimal("1"),
            actual_usd=actual_usd,
            status=status,
            attempts=1,
            receipt_ref=receipt_ref,
            release_reason=None,
            created_at=sa.func.now(),
            updated_at=sa.func.now(),
        )
    )


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def dispose_engine_after_module() -> None:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


async def _in_rolled_back_transaction(exercise: Callable[[Connection], None]) -> None:
    async with engine.connect() as connection:
        transaction = await connection.begin()
        try:
            await connection.run_sync(exercise)
        finally:
            await transaction.rollback()


def test_revision_and_held_contract_match_the_0137_compatibility_image() -> None:
    migration = load_migration()
    assert migration.revision == "0138_story_everyday_budget"
    assert migration.down_revision == "0137_video_manga_tier"
    assert len(migration.revision) <= 32
    assert migration.PRIOR_LIMITS == PILOT_LIMITS_USD
    assert set(migration.PILOTS) == set(C_SERIES_PILOT_LIMITS_USD)
    assert all(C_SERIES_PILOT_LIMITS_USD[slug] == migration.LIMIT for slug in migration.PILOTS)
    # C03 was activated by the owner on 2026-10-24 (models.ACTIVATED_STORY_SLUGS);
    # the migration still seeds its account and full-ceiling hold unchanged.
    assert all(
        is_preproduction_held(slug) != (slug in ACTIVATED_STORY_SLUGS)
        for slug in migration.PILOTS
    )
    assert ACTIVATED_STORY_SLUGS <= set(migration.HISTORICAL)
    assert migration.HISTORICAL_ID == "pre-ledger-history"


def test_offline_mode_refuses_unverified_account_mutation() -> None:
    migration = load_migration()
    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": output}
    )
    with Operations.context(context):
        with pytest.raises(RuntimeError, match="online account and provenance verification"):
            migration.upgrade()
        with pytest.raises(RuntimeError, match="online account and provenance verification"):
            migration.downgrade()
    assert output.getvalue() == ""


def _isolated_base_url() -> URL:
    url = make_url(get_settings().database_url)
    assert url.drivername == "postgresql+asyncpg"
    # Creating and dropping a database must never target production or another remote host.
    assert url.host in {"localhost", "127.0.0.1", "::1"}
    assert url.database
    return url


async def _database_ddl(url: URL, statement: str) -> None:
    disposable_engine = create_async_engine(url, isolation_level="AUTOCOMMIT")
    try:
        async with disposable_engine.connect() as connection:
            await connection.execute(sa.text(statement))
    finally:
        await disposable_engine.dispose()


async def _isolated_fetch(url: URL, statement: str) -> list[tuple[object, ...]]:
    disposable_engine = create_async_engine(url)
    try:
        async with disposable_engine.connect() as connection:
            result = await connection.execute(sa.text(statement))
            return [tuple(row) for row in result.all()]
    finally:
        await disposable_engine.dispose()


def _isolated_version(url: URL) -> list[tuple[object, ...]]:
    return asyncio.run(_isolated_fetch(url, "SELECT version_num FROM alembic_version"))


def _isolated_limits(url: URL) -> dict[str, Decimal]:
    rows = asyncio.run(_isolated_fetch(url, "SELECT slug, limit_usd FROM video_pilot_budgets"))
    return {str(slug): Decimal(str(limit)) for slug, limit in rows}


async def _seed_unrelated_operation(url: URL, operation_id: str) -> None:
    disposable_engine = create_async_engine(url)
    try:
        async with disposable_engine.begin() as connection:
            await connection.execute(
                sa.insert(VideoPilotBudgetOperation).values(
                    id=uuid4(),
                    slug="story-rolling-suitcase",
                    operation_id=operation_id,
                    category="speech",
                    provider="gemini",
                    model="test-model",
                    max_usd=Decimal("1.000000"),
                    actual_usd=Decimal("0.250000"),
                    status="settled",
                    attempts=1,
                    receipt_ref="0138-isolated-test",
                    created_at=sa.func.now(),
                    updated_at=sa.func.now(),
                )
            )
    finally:
        await disposable_engine.dispose()


def _alembic_on_isolated_database(url: URL, direction: str, revision: str) -> None:
    environment = {
        **os.environ,
        "DATABASE_URL": url.render_as_string(hide_password=False),
    }
    result = subprocess.run(
        [sys.executable, "-m", "alembic", direction, revision],
        cwd=API_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, (
        f"Alembic {direction} {revision} failed in disposable database: "
        f"stdout={result.stdout[-2000:]} stderr={result.stderr[-2000:]}"
    )


@POSTGRES
@pytest.mark.skipif(os.getenv("CI") != "true", reason="disposable CI PostgreSQL only")
def test_real_alembic_upgrade_and_downgrade_use_only_a_disposable_database() -> None:
    migration = load_migration()
    base = _isolated_base_url()
    database = f"test_c0138_{uuid4().hex[:16]}"
    isolated = base.set(database=database)
    asyncio.run(_database_ddl(base, f'CREATE DATABASE "{database}"'))
    try:
        _alembic_on_isolated_database(isolated, "upgrade", migration.down_revision)
        assert _isolated_version(isolated) == [(migration.down_revision,)]
        prior_accounts = _isolated_limits(isolated)
        assert prior_accounts == migration.PRIOR_LIMITS
        unrelated_operation = f"0138-disposable-{uuid4()}"
        asyncio.run(_seed_unrelated_operation(isolated, unrelated_operation))
        before_operation = asyncio.run(
            _isolated_fetch(
                isolated,
                "SELECT id, slug, operation_id, actual_usd, status "
                "FROM video_pilot_budget_operations "
                "WHERE slug = 'story-rolling-suitcase'",
            )
        )
        assert len(before_operation) == 1

        _alembic_on_isolated_database(isolated, "upgrade", migration.revision)
        assert _isolated_version(isolated) == [(migration.revision,)]
        accounts = _isolated_limits(isolated)
        assert accounts == {**prior_accounts, **dict.fromkeys(migration.PILOTS, migration.LIMIT)}
        holds = asyncio.run(
            _isolated_fetch(
                isolated,
                "SELECT slug, operation_id, category, provider, model, max_usd, status "
                "FROM video_pilot_budget_operations "
                "WHERE operation_id = 'pre-ledger-history' ORDER BY slug",
            )
        )
        assert holds == [
            (
                slug,
                "pre-ledger-history",
                "historical",
                "unattributed",
                "unattributed",
                migration.LIMIT,
                "uncertain",
            )
            for slug in sorted(migration.HISTORICAL)
        ]
        assert len(
            asyncio.run(_isolated_fetch(isolated, f"SELECT slug FROM {migration.OWNERSHIP}"))
        ) == len(migration.PILOTS)

        _alembic_on_isolated_database(isolated, "downgrade", migration.down_revision)
        assert _isolated_version(isolated) == [(migration.down_revision,)]
        assert _isolated_limits(isolated) == prior_accounts
        assert (
            asyncio.run(
                _isolated_fetch(
                    isolated,
                    "SELECT id, slug, operation_id, actual_usd, status "
                    "FROM video_pilot_budget_operations "
                    "WHERE slug = 'story-rolling-suitcase'",
                )
            )
            == before_operation
        )
        assert asyncio.run(
            _isolated_fetch(isolated, "SELECT to_regclass('video_pilot_budget_0138_owned')")
        ) == [(None,)]
    finally:
        asyncio.run(_database_ddl(base, f'DROP DATABASE IF EXISTS "{database}" WITH (FORCE)'))


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_repeat_and_downgrade_preserve_other_ledger_rows(
    dispose_engine_after_module: None,
) -> None:
    migration = load_migration()

    def exercise(connection: Connection) -> None:
        _prepare_0137(connection)
        before = _limits(connection)
        assert before == migration.PRIOR_LIMITS
        unrelated = "story-rolling-suitcase"
        operation_id = f"0138-unrelated-{uuid4()}"
        _insert_operation(connection, unrelated, operation_id)

        run(connection, "upgrade")
        first_ids = {slug: _hold(connection, slug)["id"] for slug in migration.HISTORICAL}
        first_created = {
            slug: _owner(connection, slug)["account_created_at"] for slug in migration.PILOTS
        }
        run(connection, "upgrade")
        assert _limits(connection) == {**before, **dict.fromkeys(migration.PILOTS, migration.LIMIT)}
        assert all(_owner(connection, slug)["account_created"] for slug in migration.PILOTS)
        assert all(_owner(connection, slug)["hold_created"] for slug in migration.HISTORICAL)
        for slug in migration.HISTORICAL:
            hold = _hold(connection, slug)
            assert hold is not None
            assert (hold["id"], hold["status"], hold["max_usd"], hold["model"]) == (
                first_ids[slug],
                "uncertain",
                migration.LIMIT,
                "unattributed",
            )
        assert all(
            _owner(connection, slug)["account_created_at"] == first_created[slug]
            for slug in migration.PILOTS
        )
        assert all(_hold(connection, slug) is None for slug in migration.NEW_PILOTS)

        run(connection, "downgrade")
        assert _limits(connection) == before
        assert not sa.inspect(connection).has_table(migration.OWNERSHIP)
        assert (
            connection.execute(
                sa.select(sa.func.count())
                .select_from(VideoPilotBudgetOperation)
                .where(
                    VideoPilotBudgetOperation.slug == unrelated,
                    VideoPilotBudgetOperation.operation_id == operation_id,
                )
            ).scalar_one()
            == 1
        )

    await _in_rolled_back_transaction(exercise)


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
async def test_real_upgrade_matches_previous_image_rollback_readback(
    dispose_engine_after_module: None,
) -> None:
    async with engine.connect() as connection:
        transaction = await connection.begin()
        try:
            await connection.run_sync(_prepare_0137)
            await connection.run_sync(lambda sync: run(sync, "upgrade"))
            await _verify_reviewed_0138(connection)
        finally:
            await transaction.rollback()


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
async def test_preexisting_matching_rows_survive_repeat_and_targeted_downgrade(
    dispose_engine_after_module: None,
) -> None:
    migration = load_migration()

    def exercise(connection: Connection) -> None:
        _prepare_0137(connection)
        c03, c07 = migration.HISTORICAL[0], migration.NEW_PILOTS[0]
        _insert_account(connection, c03)
        _insert_operation(
            connection,
            c03,
            "pre-ledger-history",
            status="settled",
            actual_usd=Decimal("1.5"),
            receipt_ref="bill:0138-prior",
        )
        _insert_account(connection, c07)
        before_hold = _hold(connection, c03)
        before_account = connection.execute(
            sa.select(VideoPilotBudget.created_at).where(VideoPilotBudget.slug == c07)
        ).scalar_one()

        run(connection, "upgrade")
        run(connection, "upgrade")
        assert not _owner(connection, c03)["account_created"]
        assert not _owner(connection, c03)["hold_created"]
        assert not _owner(connection, c07)["account_created"]
        run(connection, "downgrade")
        assert _hold(connection, c03) == before_hold
        assert (
            connection.execute(
                sa.select(VideoPilotBudget.created_at).where(VideoPilotBudget.slug == c07)
            ).scalar_one()
            == before_account
        )
        assert set(_limits(connection)) == set(migration.PRIOR_LIMITS) | {c03, c07}

    await _in_rolled_back_transaction(exercise)


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
@pytest.mark.parametrize("conflict", ["account", "historical-model"])
async def test_upgrade_rejects_conflicting_preexisting_rows(
    dispose_engine_after_module: None, conflict: str
) -> None:
    migration = load_migration()

    def exercise(connection: Connection) -> None:
        _prepare_0137(connection)
        if conflict == "account":
            _insert_account(connection, migration.NEW_PILOTS[0], "5.000000")
            message = "conflicts with USD 25"
        else:
            _insert_account(connection, migration.HISTORICAL[0])
            _insert_operation(
                connection, migration.HISTORICAL[0], "pre-ledger-history", model="pre-ledger"
            )
            message = "historical hold"
        with pytest.raises(RuntimeError, match=message):
            run(connection, "upgrade")
        # Alembic rolls the whole failed upgrade transaction back. Before that
        # rollback, the conflicting original row has not been overwritten.
        if conflict == "account":
            assert _limits(connection)[migration.NEW_PILOTS[0]] == Decimal("5")
        else:
            assert _hold(connection, migration.HISTORICAL[0])["model"] == "pre-ledger"

    await _in_rolled_back_transaction(exercise)


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
@pytest.mark.parametrize(
    "change", ["settled-hold", "later-operation", "preexisting-account-later-operation"]
)
async def test_downgrade_refuses_to_erase_reconciled_or_later_operations(
    dispose_engine_after_module: None, change: str
) -> None:
    migration = load_migration()

    def exercise(connection: Connection) -> None:
        _prepare_0137(connection)
        if change == "preexisting-account-later-operation":
            _insert_account(connection, migration.HISTORICAL[0])
        run(connection, "upgrade")
        if change == "settled-hold":
            connection.execute(
                sa.update(VideoPilotBudgetOperation)
                .where(
                    VideoPilotBudgetOperation.slug == migration.HISTORICAL[0],
                    VideoPilotBudgetOperation.operation_id == "pre-ledger-history",
                )
                .values(status="settled", actual_usd=Decimal("1.5"), receipt_ref="bill:0138")
            )
            message = "was reconciled"
        else:
            slug = (
                migration.HISTORICAL[0]
                if change == "preexisting-account-later-operation"
                else migration.NEW_PILOTS[0]
            )
            _insert_operation(connection, slug, "later-call")
            message = "has later operations"
        with pytest.raises(RuntimeError, match=message):
            run(connection, "downgrade")
        assert sa.inspect(connection).has_table(migration.OWNERSHIP)
        assert set(migration.PILOTS).issubset(_limits(connection))

    await _in_rolled_back_transaction(exercise)
