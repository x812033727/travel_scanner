"""Run the backfill branches that CI otherwise never executes.

``0001_initial`` builds the schema from the *current* models, so a fresh CI database
already has every column a later migration adds. Every branch written as
``if "x" not in columns:`` is therefore skipped in CI, and its SQL runs for the first
time in production. That is how ``0042_trip_notes`` shipped a jsonb-only operator
against a json column, failed the migrate container and rolled a deploy back on
2026-09-06 with eight green checks behind it.

Each test here puts a real PostgreSQL back into the shape the migration expects to
find (drops the column or table it adds), plants rows in the old shape through the
ORM first, runs that one migration's ``upgrade()`` through a real alembic context and
checks what the backfill wrote. Everything happens inside one transaction that is
rolled back at the end, so the database the other integration tests share is exactly
as it was.

The rule for the next migration: every ``if ... not in columns`` / ``not in tables``
branch that executes SQL beyond creating an empty column or table gets a case in this
file. Restoring the old shape is a ``DROP COLUMN`` or ``DROP TABLE``; if the branch
reads existing rows, plant one row that should change, one that should be left alone
and one at the boundary. Without such a case the branch is untested until the deploy.
"""

import importlib.util
import os
from collections.abc import AsyncIterator, Callable
from decimal import Decimal
from pathlib import Path
from types import ModuleType
from typing import Any
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool

from app.config import get_settings
from app.db import engine
from app.models import FoodMerchant, FoodMerchantSource, TravelHotspot, TripPlan, User

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def load_migration(name: str) -> ModuleType:
    """Import one migration file by name, the way alembic would."""
    path = VERSIONS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"migration_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_upgrade(connection: Connection, name: str) -> None:
    """Execute one migration's upgrade() on this connection, inside its transaction.

    ``alembic.op`` is a proxy that only works while an Operations context is
    active; this is the same wiring ``alembic upgrade`` sets up, minus the version
    table bookkeeping, so the migration runs exactly the SQL it would run in the
    migrate container.
    """
    context = MigrationContext.configure(connection)
    with Operations.context(context):
        load_migration(name).upgrade()


def plant_trip(session: Session, data: dict[str, Any]) -> UUID:
    user = User(email=f"dead-branch-{uuid4()}@example.com", password_hash=None, is_active=True)
    session.add(user)
    session.flush()
    trip = TripPlan(
        user_id=user.id,
        name="舊形狀的行程",
        mode="manual",
        total_price=Decimal("0"),
        currency="TWD",
        data=data,
        timezone="Asia/Tokyo",
    )
    session.add(trip)
    session.flush()
    return trip.id


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


def _exercise_0042(connection: Connection) -> None:
    session = Session(bind=connection)
    kept = plant_trip(session, {"notes": "  帶泳衣，週三看煙火  "})
    blank = plant_trip(session, {"notes": "   "})
    absent = plant_trip(session, {"preferences": {}})
    session.flush()

    # The shape a production database had before 0042 ran.
    connection.execute(sa.text("DROP TABLE trip_day_notes"))
    connection.execute(sa.text("ALTER TABLE trip_plans DROP COLUMN notes"))

    run_upgrade(connection, "0042_trip_notes")

    notes = dict(
        connection.execute(
            sa.text("SELECT id, notes FROM trip_plans WHERE id IN (:kept, :blank, :absent)"),
            {"kept": kept, "blank": blank, "absent": absent},
        ).all()
    )
    assert notes[kept] == "  帶泳衣，週三看煙火  "
    assert notes[blank] is None
    assert notes[absent] is None
    assert "trip_day_notes" in sa.inspect(connection).get_table_names()


def _exercise_0043(connection: Connection) -> None:
    session = Session(bind=connection)
    priced = plant_trip(session, {"preferences": {"budget_twd": "42000"}})
    fractional = plant_trip(session, {"preferences": {"budget_twd": "1234.50"}})
    prose = plant_trip(session, {"preferences": {"budget_twd": "about 40k"}})
    unset = plant_trip(session, {"preferences": {}})
    session.flush()

    connection.execute(sa.text("DROP TABLE trip_expenses"))
    connection.execute(
        sa.text("ALTER TABLE trip_plans DROP COLUMN budget_amount, DROP COLUMN cost_currency")
    )

    run_upgrade(connection, "0043_trip_expenses")

    rows = {
        row.id: (row.budget_amount, row.cost_currency)
        for row in connection.execute(
            sa.text(
                "SELECT id, budget_amount, cost_currency FROM trip_plans "
                "WHERE id IN (:priced, :fractional, :prose, :unset)"
            ),
            {"priced": priced, "fractional": fractional, "prose": prose, "unset": unset},
        ).all()
    }
    assert rows[priced] == (Decimal("42000.00"), "TWD")
    assert rows[fractional] == (Decimal("1234.50"), "TWD")
    assert rows[prose] == (None, "TWD")
    assert rows[unset] == (None, "TWD")
    assert "trip_expenses" in sa.inspect(connection).get_table_names()


@pytest.mark.asyncio(loop_scope="module")
async def test_0042_moves_the_brief_from_data_into_the_notes_column() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_0042))


@pytest.mark.asyncio(loop_scope="module")
async def test_0043_seeds_the_budget_from_the_search_preferences() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_0043))


def _plant_hotspot(session: Session, slug: str, review_status: str) -> None:
    session.add(
        TravelHotspot(
            slug=slug,
            name=slug,
            city_code="ICN",
            city_name="Seoul",
            country_code="KR",
            country_name="South Korea",
            category="culture",
            search_text=slug,
            review_status=review_status,
            is_active=False,
        )
    )
    session.flush()


def _drop_review_status_check(connection: Connection) -> None:
    # The model now declares the constraint, so a fresh database already has it and
    # a quoted value could not even be planted; a pre-0044 production did not.
    connection.execute(
        sa.text("ALTER TABLE travel_hotspots DROP CONSTRAINT ck_travel_hotspot_review_status")
    )


def _exercise_0044(connection: Connection) -> None:
    _drop_review_status_check(connection)
    session = Session(bind=connection)
    _plant_hotspot(session, "dead-branch-quoted", "'approved'")
    _plant_hotspot(session, "dead-branch-quoted-pending", "'pending'")
    _plant_hotspot(session, "dead-branch-fine", "rejected")

    run_upgrade(connection, "0044_repair_quoted_review_status")

    statuses = dict(
        connection.execute(
            sa.text(
                "SELECT slug, review_status FROM travel_hotspots WHERE slug LIKE 'dead-branch-%'"
            )
        ).all()
    )
    assert statuses == {
        "dead-branch-quoted": "approved",
        "dead-branch-quoted-pending": "pending",
        "dead-branch-fine": "rejected",
    }
    checks = {c["name"] for c in sa.inspect(connection).get_check_constraints("travel_hotspots")}
    assert "ck_travel_hotspot_review_status" in checks


def _exercise_0044_refuses_a_value_it_cannot_read(connection: Connection) -> None:
    _drop_review_status_check(connection)
    session = Session(bind=connection)
    _plant_hotspot(session, "dead-branch-odd", "'weird'")
    # The quotes are stripped only into the valid set; anything else stays as it is,
    # and then the constraint refuses to be created over it. A deploy stops here
    # instead of carrying an unreadable value forward under a CHECK that lies.
    with pytest.raises(sa.exc.DBAPIError):
        run_upgrade(connection, "0044_repair_quoted_review_status")


@pytest.mark.asyncio(loop_scope="module")
async def test_0044_strips_the_quotes_and_adds_the_check() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_0044))


@pytest.mark.asyncio(loop_scope="module")
async def test_0044_refuses_a_status_outside_the_vocabulary() -> None:
    # The failed CREATE CONSTRAINT leaves the DBAPI connection in a state the shared
    # pool would hand to the next test as closed; use a one-connection engine and
    # throw it away.
    isolated = create_async_engine(get_settings().database_url, poolclass=NullPool)
    try:
        async with isolated.connect() as connection:
            await connection.run_sync(
                in_a_rolled_back_transaction(_exercise_0044_refuses_a_value_it_cannot_read)
            )
    finally:
        await isolated.dispose()


def _exercise_0045(connection: Connection) -> None:
    for table, constraint in (
        ("travel_foods", "ck_travel_food_source"),
        ("food_localizations", "ck_food_localization_source"),
    ):
        connection.execute(sa.text(f"ALTER TABLE {table} DROP CONSTRAINT {constraint}"))
        connection.execute(sa.text(f"ALTER TABLE {table} DROP COLUMN source"))
    food_id = uuid4()
    connection.execute(
        sa.text(
            "INSERT INTO travel_foods (id, slug, country_code, local_name, romanized_name, "
            "food_kind, meal_types, ingredient_tags, dietary_notes, search_text, source_urls, "
            "review_status, is_active, display_order, created_at, updated_at) VALUES "
            "(:id, :slug, 'JP', '寿司', 'sushi', 'main', '[]', '[]', '[]', 'sushi', '[]', "
            "'approved', true, 1, now(), now())"
        ),
        {"id": food_id, "slug": f"dead-branch-{food_id.hex[:8]}"},
    )
    connection.execute(
        sa.text(
            "INSERT INTO food_localizations (id, food_id, locale, name, summary, created_at, "
            "updated_at) VALUES (:id, :food_id, 'en', 'Sushi', 'Sushi.', now(), now())"
        ),
        {"id": uuid4(), "food_id": food_id},
    )

    run_upgrade(connection, "0045_food_seed_ownership")

    # Every row that existed before the column is the seed's: see the migration docstring
    # for why that is a measurement, not an assumption.
    dish_source = sa.text("SELECT source FROM travel_foods WHERE id = :id")
    assert connection.scalar(dish_source, {"id": food_id}) == "seed"
    assert (
        connection.scalar(
            sa.text("SELECT source FROM food_localizations WHERE food_id = :id"), {"id": food_id}
        )
        == "seed"
    )
    inspector = sa.inspect(connection)
    assert "ck_travel_food_source" in {
        c["name"] for c in inspector.get_check_constraints("travel_foods")
    }
    assert "ck_food_localization_source" in {
        c["name"] for c in inspector.get_check_constraints("food_localizations")
    }


def _exercise_0046(connection: Connection) -> None:
    connection.execute(sa.text("DROP TABLE hotspot_guide_backfill_attempts"))
    run_upgrade(connection, "0046_guide_backfill_attempts")
    inspector = sa.inspect(connection)
    assert "hotspot_guide_backfill_attempts" in set(inspector.get_table_names())
    assert {c["name"] for c in inspector.get_columns("hotspot_guide_backfill_attempts")} == {
        "id",
        "hotspot_id",
        "locale",
        "outcome",
        "created_count",
        "attempted_at",
    }
    assert "uq_hotspot_guide_backfill_attempt" in {
        c["name"] for c in inspector.get_unique_constraints("hotspot_guide_backfill_attempts")
    }


@pytest.mark.asyncio(loop_scope="module")
async def test_0045_marks_every_existing_dish_and_localization_as_the_seeds() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_0045))


@pytest.mark.asyncio(loop_scope="module")
async def test_0046_creates_the_backfill_attempt_ledger() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_0046))


def _plant_merchant_source(
    session: Session, merchant: FoodMerchant, url: str, *, scope: str = "merchant_website"
) -> UUID:
    source = FoodMerchantSource(
        merchant_id=merchant.id,
        source_type="merchant_official" if scope == "merchant_website" else "official_tourism",
        source_scope=scope,
        source_title="planted",
        source_url=url,
        claims_json=["display_name"],
    )
    session.add(source)
    session.flush()
    return source.id


def _exercise_0047(connection: Connection) -> None:
    session = Session(bind=connection)
    merchant = FoodMerchant(
        slug=f"dead-branch-{uuid4()}",
        destination_id="tainan",
        country_code="TW",
        name="Hanlin Tea Room",
        local_name="翰林茶館",
        official_website_url="https://www.hanlin-tea.com.tw/",
    )
    session.add(merchant)
    session.flush()
    dead = _plant_merchant_source(session, merchant, "https://www.hanlin-tea.com.tw/")
    pdf = _plant_merchant_source(
        session,
        merchant,
        "https://www.visitsingapore.com/content/dam/desktop/global/deals/hk/Singapore_Food_Guide_PDF.pdf",
        scope="merchant_listing",
    )
    kept = _plant_merchant_source(session, merchant, "https://example.com/still-alive")
    session.flush()

    run_upgrade(connection, "0047_repair_merchant_citations")

    rows = {
        row.id: row
        for row in connection.execute(
            sa.text(
                "SELECT id, source_url, source_type, source_scope, claims_json::text AS claims"
                " FROM food_merchant_sources WHERE merchant_id = :merchant"
            ),
            {"merchant": merchant.id},
        ).all()
    }
    assert pdf not in rows
    assert rows[dead].source_url == "https://www.twtainan.net/zh-tw/shop/consume/2236/"
    assert rows[dead].source_type == "official_tourism"
    assert rows[dead].source_scope == "merchant_listing"
    assert '"address"' in rows[dead].claims
    assert rows[kept].source_url == "https://example.com/still-alive"
    assert (
        connection.scalar(
            sa.text("SELECT official_website_url FROM food_merchants WHERE id = :id"),
            {"id": merchant.id},
        )
        is None
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_0047_rewrites_the_dead_citations_and_drops_the_pdf() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_0047))


@pytest.mark.asyncio(loop_scope="module")
async def test_the_rollback_left_the_shared_schema_intact() -> None:
    """The other integration modules run against the same database afterwards."""
    async with engine.connect() as connection:
        columns = await connection.run_sync(
            lambda sync: {c["name"] for c in sa.inspect(sync).get_columns("trip_plans")}
        )
        tables = await connection.run_sync(lambda sync: set(sa.inspect(sync).get_table_names()))
        food_columns = await connection.run_sync(
            lambda sync: {c["name"] for c in sa.inspect(sync).get_columns("food_localizations")}
        )
        checks = await connection.run_sync(
            lambda sync: {
                c["name"] for c in sa.inspect(sync).get_check_constraints("travel_hotspots")
            }
        )
    assert {"notes", "budget_amount", "cost_currency"} <= columns
    assert {"trip_day_notes", "trip_expenses", "hotspot_guide_backfill_attempts"} <= tables
    assert "ck_travel_hotspot_review_status" in checks
    assert "source" in food_columns
