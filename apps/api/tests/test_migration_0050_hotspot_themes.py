"""Run migration 0050 against a real PostgreSQL, the way the migrate container does.

Follows ``test_migration_0047_ai_vendors.py``: drive ``upgrade()``/``downgrade()`` under
a real alembic operations context inside one transaction, check the schema it leaves,
and roll everything back so the shared database is untouched. The CI database has
already run ``alembic upgrade head`` (and 0001's ``create_all``), so the tables exist
when the test starts; the round trip proves the guards, the downgrade and a fresh
upgrade all agree.
"""

import importlib.util
import os
from collections.abc import AsyncIterator, Callable
from pathlib import Path
from types import ModuleType

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import Connection

from app.db import engine

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

MIGRATION = "0050_hotspot_themes_intros"
VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
TABLES = ("hotspot_themes", "hotspot_theme_links", "hotspot_intros", "hotspot_intro_runs")


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


def in_a_rolled_back_transaction(
    exercise: Callable[[Connection], None],
) -> Callable[[Connection], None]:
    def wrapped(connection: Connection) -> None:
        transaction = connection.begin()
        try:
            exercise(connection)
        finally:
            transaction.rollback()

    return wrapped


def tables_present(connection: Connection) -> set[str]:
    inspector = sa.inspect(connection)
    inspector.clear_cache()
    return {table for table in TABLES if inspector.has_table(table)}


def _insert_theme(connection: Connection, slug: str, kind: str, source: str = "seed") -> None:
    connection.execute(
        sa.text(
            "INSERT INTO hotspot_themes"
            " (id, slug, kind, names_json, months_json, display_order, is_active, source,"
            "  created_at, updated_at)"
            " VALUES (gen_random_uuid(), :slug, :kind, '{}', '[]', 1, true, :source,"
            "  now(), now())"
        ),
        {"slug": slug, "kind": kind, "source": source},
    )


def _exercise_round_trip(connection: Connection) -> None:
    assert tables_present(connection) == set(TABLES)

    # On a database that already has the tables the upgrade is a no-op, not an error.
    run(connection, "upgrade")
    assert tables_present(connection) == set(TABLES)

    run(connection, "downgrade")
    assert tables_present(connection) == set()

    run(connection, "upgrade")
    assert tables_present(connection) == set(TABLES)
    inspector = sa.inspect(connection)
    inspector.clear_cache()

    theme_columns = {column["name"] for column in inspector.get_columns("hotspot_themes")}
    assert {
        "id",
        "slug",
        "kind",
        "names_json",
        "months_json",
        "display_order",
        "is_active",
        "source",
        "created_at",
        "updated_at",
    } <= theme_columns
    link_columns = {column["name"] for column in inspector.get_columns("hotspot_theme_links")}
    assert {"hotspot_id", "theme_id", "months_json", "source", "note", "is_active"} <= link_columns
    intro_columns = {column["name"] for column in inspector.get_columns("hotspot_intros")}
    assert {
        "hotspot_id",
        "locale",
        "body",
        "review_status",
        "review_reason",
        "source",
        "ai_provider",
        "ai_model",
        "generated_at",
        "reviewed_at",
        "reviewed_by_user_id",
        "metadata_json",
    } <= intro_columns
    run_columns = {column["name"] for column in inspector.get_columns("hotspot_intro_runs")}
    assert {"idempotency_key", "requested_locales", "provider", "model", "force", "status"} <= (
        run_columns
    )

    checks = {
        table: {check["name"] for check in inspector.get_check_constraints(table)}
        for table in TABLES
    }
    assert {"ck_hotspot_theme_kind", "ck_hotspot_theme_source"} <= checks["hotspot_themes"]
    assert "ck_hotspot_theme_link_source" in checks["hotspot_theme_links"]
    assert {
        "ck_hotspot_intro_locale",
        "ck_hotspot_intro_review_status",
        "ck_hotspot_intro_source",
    } <= checks["hotspot_intros"]
    assert {"ck_hotspot_intro_run_provider", "ck_hotspot_intro_run_status"} <= checks[
        "hotspot_intro_runs"
    ]

    uniques = {
        table: {item["name"] for item in inspector.get_unique_constraints(table)}
        for table in TABLES
    }
    assert "uq_hotspot_theme_link" in uniques["hotspot_theme_links"]
    assert "uq_hotspot_intro_locale" in uniques["hotspot_intros"]
    assert "uq_hotspot_intro_run_idempotency" in uniques["hotspot_intro_runs"]

    indexes = {table: {item["name"] for item in inspector.get_indexes(table)} for table in TABLES}
    assert {"ix_hotspot_themes_slug", "ix_hotspot_themes_kind_active"} <= indexes["hotspot_themes"]
    assert {"ix_hotspot_theme_links_hotspot_id", "ix_hotspot_theme_links_theme_id"} <= indexes[
        "hotspot_theme_links"
    ]
    assert "ix_hotspot_intros_status_locale" in indexes["hotspot_intros"]

    foreign_keys = {
        (fk["referred_table"], fk["options"].get("ondelete"))
        for fk in inspector.get_foreign_keys("hotspot_theme_links")
    }
    assert foreign_keys == {("travel_hotspots", "CASCADE"), ("hotspot_themes", "CASCADE")}
    intro_keys = {
        (fk["referred_table"], fk["options"].get("ondelete"))
        for fk in inspector.get_foreign_keys("hotspot_intros")
    }
    assert intro_keys == {("travel_hotspots", "CASCADE"), ("users", "SET NULL")}

    # The vocabularies are enforced by the database, not only by the application.
    with connection.begin_nested():
        _insert_theme(connection, "sakura", "season")
    with pytest.raises(sa.exc.IntegrityError):
        with connection.begin_nested():
            _insert_theme(connection, "bogus-kind", "festival")
    with pytest.raises(sa.exc.IntegrityError):
        with connection.begin_nested():
            _insert_theme(connection, "bogus-source", "shop", source="import")
    with pytest.raises(sa.exc.IntegrityError):
        with connection.begin_nested():
            _insert_theme(connection, "sakura", "season")

    # Running the upgrade once more still finds everything in place.
    run(connection, "upgrade")
    assert tables_present(connection) == set(TABLES)


@pytest.mark.asyncio(loop_scope="module")
async def test_0050_round_trips_and_enforces_its_vocabularies() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_round_trip))
