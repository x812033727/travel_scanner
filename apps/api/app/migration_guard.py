"""Run normal migrations, except for reviewed application rollback states.

The 0132 application can serve the additive 0133 story-budget schema, and the
0133 application can serve the additive 0134 A01 admission column. Neither
image's Alembic directory can resolve its successor. Compose recreates
`migrate` before starting the API on rollback, so the exceptions must live in
that command. This module never stamps or downgrades a database.
"""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Literal

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, select, text
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import get_settings
from app.schema import expected_schema_revision, migration_revisions
from app.video_budget.models import PILOT_LIMITS_USD, VideoPilotBudget

ROLLBACK_IMAGE_HEAD = "0132_video_pilot_budget"
REVIEWED_FUTURE_REVISION = "0133_story_followon_budget"
REVIEWED_ADMISSION_REVISION = "0134_a01_admission_fence"
State = Literal["exact", "upgrade", "rollback-compatible"]


class MigrationGuardError(RuntimeError):
    """A database state that this image must not start against."""


@dataclass(frozen=True)
class MigrationState:
    current: str | None
    expected: str
    state: State


def classify_revisions(
    revisions: tuple[str, ...], expected: str, known_revisions: set[str]
) -> MigrationState:
    if len(revisions) > 1:
        raise MigrationGuardError("database has multiple migration revisions")
    current = revisions[0] if revisions else None
    if current == expected:
        return MigrationState(current, expected, "exact")
    if (expected, current) in {
        (ROLLBACK_IMAGE_HEAD, REVIEWED_FUTURE_REVISION),
        (REVIEWED_FUTURE_REVISION, REVIEWED_ADMISSION_REVISION),
    }:
        return MigrationState(current, expected, "rollback-compatible")
    if current is None or current in known_revisions:
        return MigrationState(current, expected, "upgrade")
    raise MigrationGuardError(f"database revision {current} is unknown to image head {expected}")


def _canonical_check(definition: str) -> str:
    """Normalize PostgreSQL's display casts without weakening the expression."""

    def decimal_token(match: re.Match[str]) -> str:
        number = format(Decimal(match.group()), "f")
        return number.rstrip("0").rstrip(".") if "." in number else number

    expression = definition.lower()
    expression = re.sub(r"::(?:character varying|text|numeric)(?:\[\])?", "", expression)
    expression = re.sub(r"(?<![a-z_])\d+(?:\.\d+)?", decimal_token, expression)
    return re.sub(r"[\s()]", "", expression)


def _pg_char(value: str | bytes) -> str:
    """asyncpg returns PostgreSQL's internal char fields as single-byte values."""
    if isinstance(value, bytes):
        return value.decode("ascii")
    if isinstance(value, str):
        return value
    raise MigrationGuardError("reviewed 0133 constraint catalog has an invalid char field")


async def _revisions(connection: AsyncConnection) -> tuple[str, ...]:
    has_version_table = await connection.run_sync(
        lambda sync_connection: inspect(sync_connection).has_table("alembic_version")
    )
    if not has_version_table:
        return ()
    result = await connection.execute(text("SELECT version_num FROM alembic_version"))
    return tuple(result.scalars())


async def _verify_reviewed_0133(connection: AsyncConnection) -> None:
    """Read back the 0133 migration's budget effects before skipping Alembic."""
    rows = await connection.execute(
        select(VideoPilotBudget.slug, VideoPilotBudget.limit_usd, VideoPilotBudget.created_at)
    )
    accounts = rows.all()
    actual = {slug: Decimal(limit) for slug, limit, _created_at in accounts}
    if len(accounts) != len(PILOT_LIMITS_USD) or actual != PILOT_LIMITS_USD:
        raise MigrationGuardError("reviewed 0133 budget accounts or limits do not match")

    # Every column used by the 0132 budget service must still exist after rollback.
    await connection.execute(
        text(
            "SELECT id, slug, operation_id, category, provider, model, max_usd, "
            "actual_usd, status, attempts, receipt_ref, release_reason, created_at, updated_at "
            "FROM video_pilot_budget_operations LIMIT 0"
        )
    )
    constraints = await connection.execute(
        text(
            "SELECT rel.relname, con.conname, con.contype, con.convalidated, "
            "con.confdeltype, con.confrelid = 'video_pilot_budgets'::regclass, "
            "pg_get_constraintdef(con.oid) "
            "FROM pg_constraint AS con "
            "JOIN pg_class AS rel ON rel.oid = con.conrelid "
            "WHERE con.conrelid IN "
            "('video_pilot_budgets'::regclass, 'video_pilot_budget_operations'::regclass)"
        )
    )
    actual_constraints = {}
    for row in constraints.all():
        table, name, kind, validated, delete_action, references_account, definition = row
        actual_constraints[(table, name)] = (
            _pg_char(kind),
            validated,
            _pg_char(delete_action),
            references_account,
            definition,
        )
    expected_constraints = {
        ("video_pilot_budgets", "video_pilot_budgets_pkey"): "p",
        ("video_pilot_budgets", "ck_video_pilot_budget_limit"): "c",
        ("video_pilot_budget_operations", "video_pilot_budget_operations_pkey"): "p",
        ("video_pilot_budget_operations", "uq_video_pilot_budget_operation"): "u",
        ("video_pilot_budget_operations", "video_pilot_budget_operations_slug_fkey"): "f",
        ("video_pilot_budget_operations", "ck_video_pilot_budget_operation_status"): "c",
        ("video_pilot_budget_operations", "ck_video_pilot_budget_operation_max"): "c",
        ("video_pilot_budget_operations", "ck_video_pilot_budget_operation_actual"): "c",
    }
    for key, kind in expected_constraints.items():
        found = actual_constraints.get(key)
        if found is None or found[0] != kind or found[1] is not True:
            raise MigrationGuardError(f"reviewed 0133 constraint {key[1]} is missing or invalid")
    expected_definitions = {
        ("video_pilot_budgets", "video_pilot_budgets_pkey"): {"PRIMARYKEYslug"},
        ("video_pilot_budgets", "ck_video_pilot_budget_limit"): {
            "CHECKlimit_usd=ANYARRAY[5,25]",
            "CHECKlimit_usdIN5,25",
        },
        ("video_pilot_budget_operations", "video_pilot_budget_operations_pkey"): {"PRIMARYKEYid"},
        ("video_pilot_budget_operations", "uq_video_pilot_budget_operation"): {
            "UNIQUEslug,operation_id"
        },
        ("video_pilot_budget_operations", "ck_video_pilot_budget_operation_status"): {
            "CHECKstatus=ANYARRAY['reserved','uncertain','settled','released']",
            "CHECKstatusIN'reserved','uncertain','settled','released'",
        },
        ("video_pilot_budget_operations", "ck_video_pilot_budget_operation_max"): {
            "CHECKmax_usd>0"
        },
        ("video_pilot_budget_operations", "ck_video_pilot_budget_operation_actual"): {
            "CHECKactual_usdISNULLORactual_usd>=0",
            "CHECKactual_usd>=0ORactual_usdISNULL",
        },
    }
    for key, accepted in expected_definitions.items():
        if _canonical_check(actual_constraints[key][4]).upper() not in {
            definition.upper() for definition in accepted
        }:
            raise MigrationGuardError(f"reviewed 0133 constraint {key[1]} changed")
    foreign_key = actual_constraints[
        ("video_pilot_budget_operations", "video_pilot_budget_operations_slug_fkey")
    ]
    if foreign_key[2] != "r" or foreign_key[3] is not True:
        raise MigrationGuardError("reviewed 0133 operation foreign key changed")
    foreign_key_definition = re.sub(r"\s+", "", foreign_key[4].lower())
    if foreign_key_definition not in {
        "foreignkey(slug)referencesvideo_pilot_budgets(slug)ondeleterestrict",
        "foreignkey(slug)referencespublic.video_pilot_budgets(slug)ondeleterestrict",
    }:
        raise MigrationGuardError("reviewed 0133 operation foreign key definition changed")

    indexes = await connection.execute(
        text(
            "SELECT indexname, indexdef FROM pg_indexes "
            "WHERE schemaname = current_schema() "
            "AND tablename = 'video_pilot_budget_operations'"
        )
    )
    index = ""
    for name, definition in indexes.all():
        if name == "ix_video_pilot_budget_operations_slug":
            index = definition
    if re.sub(r"\s+", "", index.lower()) not in {
        "createindexix_video_pilot_budget_operations_slug"
        "onvideo_pilot_budget_operationsusingbtree(slug)",
        "createindexix_video_pilot_budget_operations_slug"
        "onpublic.video_pilot_budget_operationsusingbtree(slug)",
    }:
        raise MigrationGuardError("reviewed 0133 operation slug index is missing")


async def _verify_reviewed_0134(connection: AsyncConnection) -> None:
    """Require the additive UUID fence on top of the reviewed 0133 ledger."""
    await _verify_reviewed_0133(connection)
    result = await connection.execute(
        text(
            "SELECT att.atttypid = 'uuid'::regtype, NOT att.attnotnull, "
            "NOT att.atthasdef, att.attgenerated = ''::\"char\", "
            "att.attidentity = ''::\"char\" "
            "FROM pg_attribute AS att "
            "WHERE att.attrelid = 'video_pilot_budgets'::regclass "
            "AND att.attname = 'admission_token' AND NOT att.attisdropped"
        )
    )
    if list(result.all()) != [(True, True, True, True, True)]:
        raise MigrationGuardError("reviewed 0134 admission column is missing or changed")
    held = await connection.execute(
        text(
            "SELECT admission_token FROM video_pilot_budgets "
            "WHERE slug = 'story-rolling-suitcase-v2'"
        )
    )
    tokens = held.all()
    if len(tokens) != 1 or tokens[0][0] is not None:
        raise MigrationGuardError("reviewed 0134 A01 admission token is held or missing")


async def read_state() -> MigrationState:
    expected = expected_schema_revision()
    known = {revision.revision for revision in migration_revisions()}
    engine = create_async_engine(get_settings().database_url, poolclass=NullPool)
    try:
        async with engine.connect() as connection:
            state = classify_revisions(await _revisions(connection), expected, known)
            if state.state == "rollback-compatible":
                if state.current == REVIEWED_ADMISSION_REVISION:
                    await _verify_reviewed_0134(connection)
                else:
                    await _verify_reviewed_0133(connection)
            return state
    finally:
        await engine.dispose()


def _alembic_config() -> Config:
    api_root = Path(__file__).resolve().parents[1]
    config = Config(str(api_root / "alembic.ini"))
    config.set_main_option("script_location", str(api_root / "migrations"))
    return config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Guard the production migration and rollback")
    parser.add_argument("--status", action="store_true", help="read-only revision and ledger check")
    args = parser.parse_args(argv)
    try:
        state = asyncio.run(read_state())
        print(
            f"SCHEMA_STATUS state={state.state} current={state.current or 'none'} "
            f"expected={state.expected}"
        )
        if args.status:
            return 0 if state.state != "upgrade" else 1
        if state.state == "rollback-compatible":
            return 0
        command.upgrade(_alembic_config(), "head")
        return 0
    except MigrationGuardError as error:
        print(f"migration guard refused: {error}", file=sys.stderr)
        return 1
    except Exception as error:
        # A driver exception can contain connection credentials. Keep the full traceback
        # out of deploy logs; the exception type still distinguishes access from schema.
        print(f"migration guard failed: {type(error).__name__}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
