import asyncio
import os
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

import asyncpg
import pytest
from sqlalchemy.engine import make_url

from app.config import get_settings

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_MIGRATION_TESTS") != "1",
    reason="requires PostgreSQL database-creation privileges",
)

LEGACY_SCHEMA = """
CREATE TABLE users (
  id uuid PRIMARY KEY, email varchar(320) UNIQUE NOT NULL, password_hash varchar(255) NOT NULL,
  is_active boolean NOT NULL, created_at timestamptz NOT NULL, updated_at timestamptz NOT NULL
);
CREATE TABLE plans (
  id uuid PRIMARY KEY, code varchar(32) UNIQUE NOT NULL, name varchar(100) NOT NULL,
  monthly_credits integer NOT NULL, price_twd integer NOT NULL,
  created_at timestamptz NOT NULL, updated_at timestamptz NOT NULL
);
CREATE TABLE subscriptions (
  id uuid PRIMARY KEY, user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  plan_id uuid NOT NULL REFERENCES plans(id), status varchar(32) NOT NULL,
  credit_balance integer NOT NULL, period_start date NOT NULL, period_end date NOT NULL,
  created_at timestamptz NOT NULL, updated_at timestamptz NOT NULL,
  CONSTRAINT uq_subscription_user UNIQUE (user_id)
);
CREATE TABLE usage_ledger (
  id uuid PRIMARY KEY, user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  subscription_id uuid NOT NULL REFERENCES subscriptions(id), entry_type varchar(32) NOT NULL,
  amount integer NOT NULL, balance_after integer NOT NULL, reference varchar(255) NOT NULL,
  metadata_json json NOT NULL, created_at timestamptz NOT NULL,
  CONSTRAINT uq_ledger_user_reference_type UNIQUE (user_id, reference, entry_type)
);
CREATE INDEX ix_usage_ledger_user_id ON usage_ledger(user_id);
CREATE INDEX ix_usage_ledger_subscription_id ON usage_ledger(subscription_id);
CREATE INDEX ix_usage_ledger_reference ON usage_ledger(reference);
CREATE TABLE usage_reservations (
  id uuid PRIMARY KEY, user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  subscription_id uuid NOT NULL REFERENCES subscriptions(id), idempotency_key varchar(255) NOT NULL,
  operation varchar(64) NOT NULL, credits integer NOT NULL, status varchar(32) NOT NULL,
  resource_id uuid NULL, created_at timestamptz NOT NULL, updated_at timestamptz NOT NULL,
  CONSTRAINT uq_usage_idempotency UNIQUE (user_id, idempotency_key)
);
"""


def connection_kwargs(database: str) -> dict[str, object]:
    url = make_url(get_settings().database_url)
    return {
        "host": url.host or "127.0.0.1",
        "port": url.port or 5432,
        "user": url.username,
        "password": url.password,
        "database": database,
    }


@pytest.mark.asyncio
async def test_legacy_balance_migrates_one_to_one_and_ledger_is_immutable() -> None:
    database = f"travel_scanner_migration_test_{uuid4().hex[:12]}"
    admin = await asyncpg.connect(**connection_kwargs("postgres"))
    try:
        await admin.execute(f'CREATE DATABASE "{database}"')
        legacy = await asyncpg.connect(**connection_kwargs(database))
        try:
            await legacy.execute(LEGACY_SCHEMA)
            user_id, plan_id, account_id = uuid4(), uuid4(), uuid4()
            await legacy.execute(
                "INSERT INTO users VALUES ($1, 'legacy@example.com', 'hash', true, now(), now())",
                user_id,
            )
            await legacy.execute(
                "INSERT INTO plans VALUES ($1, 'FREE', 'Free', 10, 0, now(), now())",
                plan_id,
            )
            await legacy.execute(
                "INSERT INTO subscriptions VALUES "
                "($1, $2, $3, 'active', 7, current_date, current_date + 30, now(), now())",
                account_id,
                user_id,
                plan_id,
            )
            await legacy.execute(
                "INSERT INTO usage_ledger VALUES "
                "($1, $2, $3, 'debit', -3, 7, 'legacy-use', '{}', now())",
                uuid4(),
                user_id,
                account_id,
            )
        finally:
            await legacy.close()

        settings_url = make_url(get_settings().database_url).set(database=database)
        environment = {**os.environ, "DATABASE_URL": settings_url.render_as_string(False)}
        api_root = Path(__file__).parents[1]
        for command in (
            [sys.executable, "-m", "alembic", "stamp", "0002_itinerary_sharing"],
            [sys.executable, "-m", "alembic", "upgrade", "head"],
        ):
            await asyncio.to_thread(
                subprocess.run,
                command,
                cwd=api_root,
                env=environment,
                check=True,
                capture_output=True,
                text=True,
            )

        migrated = await asyncpg.connect(**connection_kwargs(database))
        try:
            account = await migrated.fetchrow(
                "SELECT remaining_uses, reserved_uses FROM usage_accounts"
            )
            assert dict(account) == {"remaining_uses": 7, "reserved_uses": 0}
            old = await migrated.fetchrow(
                "SELECT status, unit FROM usage_ledger WHERE reference = 'legacy-use'"
            )
            assert dict(old) == {"status": "charged", "unit": "legacy_credit"}
            conversion = await migrated.fetchrow(
                "SELECT status, balance_after FROM usage_ledger WHERE entry_type = 'migration'"
            )
            assert dict(conversion) == {"status": "migrated", "balance_after": 7}
            operation_costs = await migrated.fetch(
                "SELECT operation, uses FROM usage_operation_costs ORDER BY operation"
            )
            costs_by_operation = {row["operation"]: row["uses"] for row in operation_costs}
            assert len(costs_by_operation) == 13
            # 0039 seeds refinement free; every other operation keeps the 1-use default.
            assert costs_by_operation["ai_itinerary_refine"] == 0
            assert {
                uses
                for operation, uses in costs_by_operation.items()
                if operation != "ai_itinerary_refine"
            } == {1}
            fallback_package = await migrated.fetchrow(
                "SELECT localized_names, display_order, is_featured "
                "FROM usage_packages WHERE code = 'FREE'"
            )
            assert fallback_package is not None
            assert fallback_package["localized_names"] == {
                locale: "Free" for locale in ("zh-TW", "zh-CN", "en", "ja", "ko")
            }
            assert fallback_package["display_order"] == 100
            assert fallback_package["is_featured"] is False
            with pytest.raises(asyncpg.RaiseError, match="append-only"):
                await migrated.execute("DELETE FROM usage_ledger WHERE reference = 'legacy-use'")
        finally:
            await migrated.close()
    finally:
        await admin.execute(
            "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = $1", database
        )
        await admin.execute(f'DROP DATABASE IF EXISTS "{database}"')
        await admin.close()
