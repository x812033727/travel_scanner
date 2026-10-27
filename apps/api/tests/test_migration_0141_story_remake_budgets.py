"""Keep the six story-remake account migration identical to the reviewed rollback contract."""

from __future__ import annotations

import asyncio
import hashlib
import importlib.util
import io
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from uuid import uuid4

import pytest
import sqlalchemy as sa
from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import get_settings
from app.migration_guard import C20_PILOT_SLUG
from app.video_budget.models import (
    BATCH_REMAKE_SLUGS,
    C11_REMAKE_SLUG,
    C_SERIES_PILOT_LIMITS_USD,
    PILOT_LIMITS_USD,
    REMAKE_PILOT_LIMITS_USD,
    UNRECONCILED_STORY_SLUGS,
)
from app.video_budget.service import is_preproduction_held

REVISION = "0141_story_remake_budgets"
PRIOR_REVISION = "0140_c11_ucc_remake_budget"
# The same bytes the 0140 rollback image's integration test pinned (#1875).
REVIEWED_SOURCE_SHA256 = "0f6116145d815c4bb6cdc71237b5750c02baa1c4a7ad2140f841c92f534a5afb"
IN_BATCH = "(" + ", ".join(f"'{slug}'" for slug in BATCH_REMAKE_SLUGS) + ")"
MIGRATION_FILE = Path(__file__).resolve().parents[1] / "migrations" / "versions" / f"{REVISION}.py"
API_ROOT = MIGRATION_FILE.parents[2]


def _migration() -> ModuleType:
    spec = importlib.util.spec_from_file_location("story_remake_budgets_0141", MIGRATION_FILE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_0141_matches_reviewed_0140_rollback_contract() -> None:
    source = MIGRATION_FILE.read_bytes().replace(b"\r\n", b"\n")
    assert hashlib.sha256(source).hexdigest() == REVIEWED_SOURCE_SHA256

    migration = _migration()
    assert migration.revision == REVISION
    assert migration.down_revision == PRIOR_REVISION
    assert len(migration.revision) <= 32
    assert migration.SLUGS == BATCH_REMAKE_SLUGS
    assert migration.OWNERSHIP == "video_pilot_budget_0141_owned"
    assert migration.PRIOR_OWNERS == {
        "video_pilot_budget_0139_owned": C20_PILOT_SLUG,
        "video_pilot_budget_0140_owned": C11_REMAKE_SLUG,
    }
    assert migration.PRIOR_LIMITS == {
        **PILOT_LIMITS_USD,
        **C_SERIES_PILOT_LIMITS_USD,
        C20_PILOT_SLUG: 25,
        C11_REMAKE_SLUG: 25,
    }
    assert set(migration.HISTORICAL) == UNRECONCILED_STORY_SLUGS
    # The owner activated these films with their accounts (2026-10-26).
    assert all(REMAKE_PILOT_LIMITS_USD[slug] == 25 for slug in BATCH_REMAKE_SLUGS)
    assert not any(is_preproduction_held(slug) for slug in BATCH_REMAKE_SLUGS)


def test_0141_refuses_offline_mutation_and_destructive_downgrade() -> None:
    migration = _migration()
    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": output}
    )
    with Operations.context(context):
        with pytest.raises(RuntimeError, match="online remake account verification"):
            migration.upgrade()
        with pytest.raises(RuntimeError, match="cannot be erased automatically"):
            migration.downgrade()
    assert output.getvalue() == ""


def _disposable_url() -> URL:
    base = make_url(get_settings().database_url)
    assert base.drivername == "postgresql+asyncpg"
    assert base.host in {"localhost", "127.0.0.1", "::1"}
    assert base.database
    return base


async def _execute(url: URL, sql: str, *, autocommit: bool = False) -> None:
    engine = create_async_engine(url, isolation_level="AUTOCOMMIT" if autocommit else None)
    try:
        async with engine.begin() as connection:
            await connection.execute(sa.text(sql))
    finally:
        await engine.dispose()


async def _fetch(url: URL, sql: str) -> list[tuple[object, ...]]:
    engine = create_async_engine(url)
    try:
        async with engine.connect() as connection:
            result = await connection.execute(sa.text(sql))
            return [tuple(row) for row in result.all()]
    finally:
        await engine.dispose()


def _alembic(url: URL, direction: str, revision: str) -> subprocess.CompletedProcess[str]:
    environment = {**os.environ, "DATABASE_URL": url.render_as_string(hide_password=False)}
    return subprocess.run(
        [sys.executable, "-m", "alembic", direction, revision],
        cwd=API_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )


def _refused_at_0140(url: URL) -> None:
    assert _alembic(url, "upgrade", REVISION).returncode != 0
    assert asyncio.run(_fetch(url, "SELECT version_num FROM alembic_version")) == [
        (PRIOR_REVISION,)
    ]
    assert asyncio.run(_fetch(url, "SELECT to_regclass('video_pilot_budget_0141_owned')")) == [
        (None,)
    ]


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="local PostgreSQL required")
def test_real_0141_rejects_conflicts_and_downgrade_preserves_accounts() -> None:
    base = _disposable_url()
    name = f"test_remakes_0141_{uuid4().hex[:16]}"
    isolated = base.set(database=name)
    asyncio.run(_execute(base, f'CREATE DATABASE "{name}"', autocommit=True))
    try:
        upgraded_0140 = _alembic(isolated, "upgrade", PRIOR_REVISION)
        assert upgraded_0140.returncode == 0, upgraded_0140.stderr[-2000:]
        accounts_before = asyncio.run(
            _fetch(
                isolated,
                "SELECT slug, limit_usd, created_at FROM video_pilot_budgets ORDER BY slug",
            )
        )
        holds_before = asyncio.run(
            _fetch(
                isolated,
                "SELECT id, slug, status, max_usd FROM video_pilot_budget_operations "
                "WHERE operation_id = 'pre-ledger-history' ORDER BY slug",
            )
        )
        assert len(accounts_before) == 18
        assert len(holds_before) == 4

        # An account that predates the migration is not proof of a new ledger.
        slug = BATCH_REMAKE_SLUGS[3]
        asyncio.run(
            _execute(
                isolated,
                f"INSERT INTO video_pilot_budgets(slug, limit_usd) VALUES ('{slug}', 25)",
            )
        )
        _refused_at_0140(isolated)
        asyncio.run(_execute(isolated, f"DELETE FROM video_pilot_budgets WHERE slug = '{slug}'"))

        asyncio.run(
            _execute(
                isolated,
                "UPDATE video_pilot_budget_operations SET status = 'reserved' "
                "WHERE slug = 'story-everyday-moleskine-c03' "
                "AND operation_id = 'pre-ledger-history'",
            )
        )
        _refused_at_0140(isolated)
        asyncio.run(
            _execute(
                isolated,
                "UPDATE video_pilot_budget_operations SET status = 'uncertain' "
                "WHERE slug = 'story-everyday-moleskine-c03' "
                "AND operation_id = 'pre-ledger-history'",
            )
        )

        for table, owner in (
            ("video_pilot_budget_0139_owned", C20_PILOT_SLUG),
            ("video_pilot_budget_0140_owned", C11_REMAKE_SLUG),
        ):
            asyncio.run(
                _execute(
                    isolated,
                    f"UPDATE {table} "
                    "SET account_created_at = account_created_at + interval '1 second'",
                )
            )
            _refused_at_0140(isolated)
            asyncio.run(
                _execute(
                    isolated,
                    f"UPDATE {table} SET account_created_at = "
                    f"(SELECT created_at FROM video_pilot_budgets WHERE slug = '{owner}')",
                )
            )

        upgraded = _alembic(isolated, "upgrade", REVISION)
        assert upgraded.returncode == 0, upgraded.stderr[-2000:]
        assert asyncio.run(_fetch(isolated, "SELECT version_num FROM alembic_version")) == [
            (REVISION,)
        ]
        assert (
            asyncio.run(
                _fetch(
                    isolated,
                    "SELECT slug, limit_usd, created_at FROM video_pilot_budgets "
                    f"WHERE slug NOT IN {IN_BATCH} ORDER BY slug",
                )
            )
            == accounts_before
        )
        assert (
            asyncio.run(
                _fetch(
                    isolated,
                    "SELECT id, slug, status, max_usd FROM video_pilot_budget_operations "
                    "WHERE operation_id = 'pre-ledger-history' ORDER BY slug",
                )
            )
            == holds_before
        )
        accounts = asyncio.run(
            _fetch(
                isolated,
                "SELECT slug, limit_usd, created_at FROM video_pilot_budgets "
                f"WHERE slug IN {IN_BATCH} ORDER BY slug",
            )
        )
        owners = asyncio.run(
            _fetch(
                isolated,
                "SELECT slug, account_created, account_created_at "
                "FROM video_pilot_budget_0141_owned ORDER BY slug",
            )
        )
        assert [row[0] for row in accounts] == sorted(BATCH_REMAKE_SLUGS)
        assert [row[0] for row in owners] == sorted(BATCH_REMAKE_SLUGS)
        assert all(str(row[1]) == "25.000000" for row in accounts)
        assert all(
            owner[1] is True and owner[2] == account[2]
            for owner, account in zip(owners, accounts, strict=True)
        )
        assert asyncio.run(
            _fetch(
                isolated,
                f"SELECT count(*) FROM video_pilot_budget_operations WHERE slug IN {IN_BATCH}",
            )
        ) == [(0,)]

        assert _alembic(isolated, "downgrade", PRIOR_REVISION).returncode != 0
        assert asyncio.run(_fetch(isolated, "SELECT version_num FROM alembic_version")) == [
            (REVISION,)
        ]
        assert asyncio.run(
            _fetch(isolated, "SELECT slug FROM video_pilot_budget_0141_owned ORDER BY slug")
        ) == [(slug,) for slug in sorted(BATCH_REMAKE_SLUGS)]
    finally:
        asyncio.run(
            _execute(base, f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)', autocommit=True)
        )
