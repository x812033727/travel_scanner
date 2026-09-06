"""Run migration 0047 against a real PostgreSQL, the way the migrate container does.

Follows ``test_migration_dead_branches.py``: plant rows in the old shape through the
ORM, run the migration's ``upgrade()`` under a real alembic context, check what it
wrote, and roll the whole transaction back so the shared database is untouched.
"""

import importlib.util
import json
import os
from collections.abc import AsyncIterator, Callable
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session

from app.admin.service import decrypt_secrets, encrypt_secrets
from app.db import engine
from app.models import ProviderConfig

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

MIGRATION = "0047_ai_vendor_settings"
VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
PROVIDERS = ("ai_vendors", "ai_planner", "gemini_guides")


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


def clear_rows(session: Session) -> None:
    session.execute(sa.delete(ProviderConfig).where(ProviderConfig.provider.in_(PROVIDERS)))
    session.flush()


def plant_old_rows(session: Session) -> None:
    clear_rows(session)
    session.add(
        ProviderConfig(
            provider="ai_planner",
            enabled=False,
            config={"ai_planner_mode": "auto", "openai_api_base_url": "https://api.openai.com/v1"},
            secret_config_encrypted=encrypt_secrets(
                {"openai_api_key": "sk-planner", "minimax_api_key": "mm-planner"}
            ),
            last_test_status="success",
            last_test_message="openai / gpt 結構化行程驗證成功",
        )
    )
    session.add(
        ProviderConfig(
            provider="gemini_guides",
            enabled=True,
            config={
                "hotspot_guide_gemini_model": "gemini-3.8-flash",
                "hotspot_guide_gemini_base_url": "https://generativelanguage.googleapis.com",
            },
            secret_config_encrypted=encrypt_secrets({"hotspot_guide_gemini_api_key": "g-key"}),
        )
    )
    session.flush()


def read_rows(connection: Connection) -> dict[str, dict[str, Any]]:
    rows = connection.execute(
        sa.text(
            "SELECT provider, enabled, config::text, secret_config_encrypted, last_test_status"
            " FROM provider_configs WHERE provider IN ('ai_vendors', 'ai_planner', 'gemini_guides')"
        )
    ).all()
    return {
        row[0]: {
            "enabled": row[1],
            "config": json.loads(row[2]),
            "secrets": decrypt_secrets(row[3]),
            "last_test_status": row[4],
        }
        for row in rows
    }


def _exercise_upgrade(connection: Connection) -> None:
    plant_old_rows(Session(bind=connection))

    run(connection, "upgrade")

    rows = read_rows(connection)
    assert rows["ai_vendors"] == {
        "enabled": True,
        "config": {
            "openai_api_base_url": "https://api.openai.com/v1",
            "hotspot_guide_gemini_base_url": "https://generativelanguage.googleapis.com",
        },
        "secrets": {
            "openai_api_key": "sk-planner",
            "minimax_api_key": "mm-planner",
            "hotspot_guide_gemini_api_key": "g-key",
        },
        "last_test_status": None,
    }
    assert rows["ai_planner"] == {
        "enabled": False,
        "config": {"ai_planner_mode": "auto"},
        "secrets": {},
        "last_test_status": None,
    }
    assert rows["gemini_guides"]["config"] == {"hotspot_guide_gemini_model": "gemini-3.8-flash"}
    assert rows["gemini_guides"]["secrets"] == {}

    # Idempotent: a second run finds nothing left to move and changes nothing.
    run(connection, "upgrade")
    assert read_rows(connection) == rows


def _exercise_gemini_only(connection: Connection) -> None:
    session = Session(bind=connection)
    clear_rows(session)
    session.add(
        ProviderConfig(
            provider="gemini_guides",
            enabled=True,
            config={"hotspot_guide_gemini_model": "gemini-3.8-flash"},
            secret_config_encrypted=encrypt_secrets({"hotspot_guide_gemini_api_key": "g-only"}),
        )
    )
    session.flush()

    run(connection, "upgrade")

    rows = read_rows(connection)
    assert rows["ai_vendors"]["secrets"] == {"hotspot_guide_gemini_api_key": "g-only"}
    assert rows["ai_vendors"]["config"] == {}
    assert "ai_planner" not in rows


def _exercise_nothing_to_move(connection: Connection) -> None:
    clear_rows(Session(bind=connection))

    run(connection, "upgrade")

    assert "ai_vendors" not in read_rows(connection)


def _exercise_downgrade(connection: Connection) -> None:
    plant_old_rows(Session(bind=connection))
    run(connection, "upgrade")

    run(connection, "downgrade")

    rows = read_rows(connection)
    assert "ai_vendors" not in rows
    assert rows["ai_planner"]["config"] == {
        "ai_planner_mode": "auto",
        "openai_api_base_url": "https://api.openai.com/v1",
    }
    assert rows["ai_planner"]["secrets"] == {
        "openai_api_key": "sk-planner",
        "minimax_api_key": "mm-planner",
    }
    assert rows["gemini_guides"]["secrets"] == {"hotspot_guide_gemini_api_key": "g-key"}


@pytest.mark.asyncio(loop_scope="module")
async def test_0045_moves_keys_and_base_urls_onto_ai_vendors() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_upgrade))


@pytest.mark.asyncio(loop_scope="module")
async def test_0045_handles_a_gemini_only_install() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_gemini_only))


@pytest.mark.asyncio(loop_scope="module")
async def test_0045_leaves_an_environment_only_install_alone() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_nothing_to_move))


@pytest.mark.asyncio(loop_scope="module")
async def test_0045_downgrade_puts_the_fields_back() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(in_a_rolled_back_transaction(_exercise_downgrade))
