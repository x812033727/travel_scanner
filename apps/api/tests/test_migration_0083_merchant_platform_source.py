"""0083 widens ``ck_food_merchant_source_type`` and refuses to narrow it over live rows.

``0001_initial`` builds a fresh database from the current models, so CI never sees the
old three-value constraint; this test puts a real PostgreSQL back into that shape, runs the
migration through a real alembic context, and checks both directions inside one rolled
back transaction, the way ``test_migration_0073_catalog_run_mode`` does.
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
from app.models import FoodMerchant, FoodMerchantSource

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
MIGRATION = "0083_merchant_platform_source"
TABLE = "food_merchant_sources"
CONSTRAINT = "ck_food_merchant_source_type"
OLD_CHECK = "source_type IN ('official_tourism', 'merchant_official', 'michelin_licensed')"


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


def plant_merchant(session: Session) -> FoodMerchant:
    number = uuid4().int % 1_000_000
    merchant = FoodMerchant(
        id=UUID(int=uuid4().int),
        slug=f"seoul-migration-0083-{number}",
        destination_id="seoul",
        country_code="KR",
        name=f"Migration {number}",
        local_name=f"마이그레이션 {number}",
        names_json={},
        address=None,
        google_place_id=None,
        review_status="pending",
        map_match_status="unverified",
        is_active=False,
        display_order=100,
    )
    session.add(merchant)
    session.flush()
    return merchant


def plant_source(session: Session, merchant: FoodMerchant, source_type: str) -> None:
    session.add(
        FoodMerchantSource(
            merchant_id=merchant.id,
            source_type=source_type,
            source_scope="merchant_listing",
            source_title="CatchTable shop page",
            source_url=f"https://www.catchtable.net/shop/migration-{uuid4().hex[:8]}",
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
    merchant = plant_merchant(session)
    with pytest.raises(sa.exc.IntegrityError), session.begin_nested():
        plant_source(session, merchant, "merchant_platform")

    run_upgrade(connection)
    assert "merchant_platform" in check_text(connection)
    plant_source(session, merchant, "merchant_platform")
    with pytest.raises(sa.exc.IntegrityError), session.begin_nested():
        plant_source(session, merchant, "tripadvisor")

    # Idempotent: a second upgrade finds the widened constraint and leaves it alone.
    run_upgrade(connection)
    assert "merchant_platform" in check_text(connection)


def _exercise_downgrade(connection: Connection) -> None:
    run_upgrade(connection)
    session = Session(bind=connection)
    merchant = plant_merchant(session)
    plant_source(session, merchant, "merchant_platform")
    with pytest.raises(RuntimeError, match="merchant_platform sources exist"):
        run_downgrade(connection)
    assert "merchant_platform" in check_text(connection)

    connection.execute(sa.text(f"DELETE FROM {TABLE} WHERE source_type = 'merchant_platform'"))
    run_downgrade(connection)
    assert "merchant_platform" not in check_text(connection)
    with pytest.raises(sa.exc.IntegrityError), session.begin_nested():
        plant_source(session, merchant, "merchant_platform")
    # And a second downgrade is a no-op on the already narrowed constraint.
    run_downgrade(connection)
    assert "merchant_platform" not in check_text(connection)


@pytest.mark.asyncio(loop_scope="module")
async def test_upgrade_widens_the_constraint_and_is_idempotent() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_upgrade))


@pytest.mark.asyncio(loop_scope="module")
async def test_downgrade_refuses_over_live_rows_then_narrows() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_downgrade))
