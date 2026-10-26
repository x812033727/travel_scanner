"""Keep the C11 UCC remake account migration identical to the reviewed rollback contract."""

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
    C11_REMAKE_SLUG,
    C_SERIES_PILOT_LIMITS_USD,
    PILOT_LIMITS_USD,
    REMAKE_PILOT_LIMITS_USD,
    UNRECONCILED_STORY_SLUGS,
)
from app.video_budget.service import is_preproduction_held

REVISION = "0140_c11_ucc_remake_budget"
PRIOR_REVISION = "0139_c20_zippo_pilot_budget"
SLUG = "story-everyday-ucc-c11-remake-20261025"
# The same bytes the 0139 rollback image's integration test pinned (#1870).
REVIEWED_SOURCE_SHA256 = "b6a8707dc220819ccfae8f54ca9c90a790d0eb1cea448f7f030da93fe94583f6"
MIGRATION_FILE = Path(__file__).resolve().parents[1] / "migrations" / "versions" / f"{REVISION}.py"
API_ROOT = MIGRATION_FILE.parents[2]


def _migration() -> ModuleType:
    spec = importlib.util.spec_from_file_location("c11_remake_budget_0140", MIGRATION_FILE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_0140_matches_reviewed_0139_rollback_contract() -> None:
    source = MIGRATION_FILE.read_bytes().replace(b"\r\n", b"\n")
    assert hashlib.sha256(source).hexdigest() == REVIEWED_SOURCE_SHA256

    migration = _migration()
    assert migration.revision == REVISION
    assert migration.down_revision == PRIOR_REVISION
    assert len(migration.revision) <= 32
    assert migration.SLUG == SLUG == C11_REMAKE_SLUG
    assert migration.OWNERSHIP == "video_pilot_budget_0140_owned"
    assert migration.PRIOR_LIMITS == {
        **PILOT_LIMITS_USD,
        **C_SERIES_PILOT_LIMITS_USD,
        C20_PILOT_SLUG: 25,
    }
    assert set(migration.HISTORICAL) == UNRECONCILED_STORY_SLUGS
    # The owner activated this film with the account (2026-10-26).
    assert REMAKE_PILOT_LIMITS_USD == {SLUG: 25}
    assert not is_preproduction_held(SLUG)


def test_0140_refuses_offline_mutation_and_destructive_downgrade() -> None:
    migration = _migration()
    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": output}
    )
    with Operations.context(context):
        with pytest.raises(RuntimeError, match="online C11 remake account verification"):
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


def _refused_at_0139(url: URL) -> None:
    assert _alembic(url, "upgrade", REVISION).returncode != 0
    assert asyncio.run(_fetch(url, "SELECT version_num FROM alembic_version")) == [
        (PRIOR_REVISION,)
    ]
    assert asyncio.run(_fetch(url, "SELECT to_regclass('video_pilot_budget_0140_owned')")) == [
        (None,)
    ]


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="local PostgreSQL required")
def test_real_0140_rejects_conflicts_and_downgrade_preserves_account() -> None:
    base = _disposable_url()
    name = f"test_c11_0140_{uuid4().hex[:16]}"
    isolated = base.set(database=name)
    asyncio.run(_execute(base, f'CREATE DATABASE "{name}"', autocommit=True))
    try:
        upgraded_0139 = _alembic(isolated, "upgrade", PRIOR_REVISION)
        assert upgraded_0139.returncode == 0, upgraded_0139.stderr[-2000:]
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
        assert len(accounts_before) == 17
        assert len(holds_before) == 4

        # An account that predates the migration is not proof of a new ledger.
        asyncio.run(
            _execute(
                isolated,
                f"INSERT INTO video_pilot_budgets(slug, limit_usd) VALUES ('{SLUG}', 25)",
            )
        )
        _refused_at_0139(isolated)
        asyncio.run(_execute(isolated, f"DELETE FROM video_pilot_budgets WHERE slug = '{SLUG}'"))

        asyncio.run(
            _execute(
                isolated,
                "UPDATE video_pilot_budget_operations SET status = 'reserved' "
                "WHERE slug = 'story-everyday-moleskine-c03' "
                "AND operation_id = 'pre-ledger-history'",
            )
        )
        _refused_at_0139(isolated)
        asyncio.run(
            _execute(
                isolated,
                "UPDATE video_pilot_budget_operations SET status = 'uncertain' "
                "WHERE slug = 'story-everyday-moleskine-c03' "
                "AND operation_id = 'pre-ledger-history'",
            )
        )

        asyncio.run(
            _execute(
                isolated,
                "UPDATE video_pilot_budget_0139_owned "
                "SET account_created_at = account_created_at + interval '1 second'",
            )
        )
        _refused_at_0139(isolated)
        asyncio.run(
            _execute(
                isolated,
                "UPDATE video_pilot_budget_0139_owned SET account_created_at = "
                "(SELECT created_at FROM video_pilot_budgets "
                f"WHERE slug = '{C20_PILOT_SLUG}')",
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
                    f"WHERE slug <> '{SLUG}' ORDER BY slug",
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
        account = asyncio.run(
            _fetch(
                isolated,
                "SELECT slug, limit_usd, created_at FROM video_pilot_budgets "
                f"WHERE slug = '{SLUG}'",
            )
        )
        owner = asyncio.run(
            _fetch(
                isolated,
                "SELECT slug, account_created, account_created_at "
                "FROM video_pilot_budget_0140_owned",
            )
        )
        assert len(account) == 1 and len(owner) == 1
        assert account[0][0] == owner[0][0] == SLUG
        assert str(account[0][1]) == "25.000000"
        assert owner[0][1] is True and owner[0][2] == account[0][2]
        assert asyncio.run(
            _fetch(
                isolated,
                f"SELECT count(*) FROM video_pilot_budget_operations WHERE slug = '{SLUG}'",
            )
        ) == [(0,)]

        assert _alembic(isolated, "downgrade", PRIOR_REVISION).returncode != 0
        assert asyncio.run(_fetch(isolated, "SELECT version_num FROM alembic_version")) == [
            (REVISION,)
        ]
        assert asyncio.run(_fetch(isolated, "SELECT slug FROM video_pilot_budget_0140_owned")) == [
            (SLUG,)
        ]
    finally:
        asyncio.run(
            _execute(base, f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)', autocommit=True)
        )
