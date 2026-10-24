"""Run normal migrations, except for reviewed application rollback states.

The 0132 application can serve the additive 0133 story-budget schema, but its
Alembic directory cannot resolve that newer revision. Compose recreates `migrate`
before starting the API on rollback, so the exception must live in that command.
The 0137 C-series compatibility image likewise accepts only the reviewed 0138
budget schema after reading back its held accounts and historical operations.
The 0138 image accepts only the additive 0139 C20 account contract, with the
same historical holds and a matching C20 ownership record. Paid admission
remains held in that image.
The 0139 image accepts only the additive 0140 C08 account contract after
checking both new account ownership records. Paid admission remains held.
This module never stamps or downgrades a database.
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
from app.video_budget.models import (
    C_SERIES_PILOT_LIMITS_USD,
    C_SERIES_PRE_LEDGER_OPERATION_ID,
    PILOT_LIMITS_USD,
    UNRECONCILED_STORY_SLUGS,
    VideoPilotBudget,
    VideoPilotBudgetOperation,
)

ROLLBACK_IMAGE_HEAD = "0132_video_pilot_budget"
REVIEWED_FUTURE_REVISION = "0133_story_followon_budget"
C_SERIES_ROLLBACK_IMAGE_HEAD = "0137_video_manga_tier"
C_SERIES_REVIEWED_FUTURE_REVISION = "0138_story_everyday_budget"
C20_ROLLBACK_IMAGE_HEAD = "0138_story_everyday_budget"
C20_REVIEWED_FUTURE_REVISION = "0139_c20_zippo_pilot_budget"
C20_PILOT_SLUG = "story-everyday-zippo-c20-short-v8"
C20_PILOT_LIMIT_USD = Decimal("25.000000")
C08_ROLLBACK_IMAGE_HEAD = "0139_c20_zippo_pilot_budget"
C08_REVIEWED_FUTURE_REVISION = "0140_c08_kikkoman_pilot_budget"
C08_PILOT_SLUG = "story-everyday-kikkoman-c08-short-v8"
C08_PILOT_LIMIT_USD = Decimal("25.000000")
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
    if expected == ROLLBACK_IMAGE_HEAD and current == REVIEWED_FUTURE_REVISION:
        return MigrationState(current, expected, "rollback-compatible")
    if expected == C_SERIES_ROLLBACK_IMAGE_HEAD and current == C_SERIES_REVIEWED_FUTURE_REVISION:
        return MigrationState(current, expected, "rollback-compatible")
    if expected == C20_ROLLBACK_IMAGE_HEAD and current == C20_REVIEWED_FUTURE_REVISION:
        return MigrationState(current, expected, "rollback-compatible")
    if expected == C08_ROLLBACK_IMAGE_HEAD and current == C08_REVIEWED_FUTURE_REVISION:
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
    raise MigrationGuardError("reviewed budget constraint catalog has an invalid char field")


async def _revisions(connection: AsyncConnection) -> tuple[str, ...]:
    has_version_table = await connection.run_sync(
        lambda sync_connection: inspect(sync_connection).has_table("alembic_version")
    )
    if not has_version_table:
        return ()
    result = await connection.execute(text("SELECT version_num FROM alembic_version"))
    return tuple(result.scalars())


async def _verify_reviewed_budget_schema(
    connection: AsyncConnection, *, expected_accounts: dict[str, Decimal], revision: str
) -> None:
    """Read back the exact budget accounts and shared schema before skipping Alembic."""
    rows = await connection.execute(
        select(VideoPilotBudget.slug, VideoPilotBudget.limit_usd, VideoPilotBudget.created_at)
    )
    accounts = rows.all()
    actual = {slug: Decimal(limit) for slug, limit, _created_at in accounts}
    if len(accounts) != len(expected_accounts) or actual != expected_accounts:
        raise MigrationGuardError(f"reviewed {revision} budget accounts or limits do not match")

    # Every column used by either rollback image's budget service must remain.
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
            raise MigrationGuardError(
                f"reviewed {revision} constraint {key[1]} is missing or invalid"
            )
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
            raise MigrationGuardError(f"reviewed {revision} constraint {key[1]} changed")
    foreign_key = actual_constraints[
        ("video_pilot_budget_operations", "video_pilot_budget_operations_slug_fkey")
    ]
    if foreign_key[2] != "r" or foreign_key[3] is not True:
        raise MigrationGuardError(f"reviewed {revision} operation foreign key changed")
    foreign_key_definition = re.sub(r"\s+", "", foreign_key[4].lower())
    if foreign_key_definition not in {
        "foreignkey(slug)referencesvideo_pilot_budgets(slug)ondeleterestrict",
        "foreignkey(slug)referencespublic.video_pilot_budgets(slug)ondeleterestrict",
    }:
        raise MigrationGuardError(f"reviewed {revision} operation foreign key definition changed")

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
        raise MigrationGuardError(f"reviewed {revision} operation slug index is missing")


async def _verify_reviewed_0133(connection: AsyncConnection) -> None:
    """Read back the nine-account 0133 contract before skipping Alembic."""
    await _verify_reviewed_budget_schema(
        connection, expected_accounts=PILOT_LIMITS_USD, revision="0133"
    )


async def _verify_reviewed_0138(connection: AsyncConnection) -> None:
    """Verify seven held accounts and the four preserved pre-ledger exposure rows."""
    await _verify_reviewed_budget_schema(
        connection,
        expected_accounts={**PILOT_LIMITS_USD, **C_SERIES_PILOT_LIMITS_USD},
        revision="0138",
    )
    await _verify_c_series_holds(connection, revision="0138")


async def _verify_c_series_holds(connection: AsyncConnection, *, revision: str) -> None:
    # Verify the four indispensable baseline holds. Other operations may appear
    # after a later evidence-backed settlement or activation; the rollback app
    # still counts them in summaries and refuses every C-series paid admission.
    rows = await connection.execute(
        select(
            VideoPilotBudgetOperation.slug,
            VideoPilotBudgetOperation.operation_id,
            VideoPilotBudgetOperation.category,
            VideoPilotBudgetOperation.provider,
            VideoPilotBudgetOperation.model,
            VideoPilotBudgetOperation.max_usd,
            VideoPilotBudgetOperation.actual_usd,
            VideoPilotBudgetOperation.status,
            VideoPilotBudgetOperation.attempts,
            VideoPilotBudgetOperation.receipt_ref,
            VideoPilotBudgetOperation.release_reason,
        ).where(
            VideoPilotBudgetOperation.slug.in_(UNRECONCILED_STORY_SLUGS),
            VideoPilotBudgetOperation.operation_id == C_SERIES_PRE_LEDGER_OPERATION_ID,
        )
    )
    historic = rows.all()
    if (
        len(historic) != len(UNRECONCILED_STORY_SLUGS)
        or {row[0] for row in historic} != UNRECONCILED_STORY_SLUGS
    ):
        raise MigrationGuardError(f"reviewed {revision} pre-ledger holds are missing")
    for (
        _slug,
        operation_id,
        category,
        provider,
        model,
        maximum,
        actual,
        status,
        attempts,
        receipt,
        release_reason,
    ) in historic:
        try:
            maximum_matches = Decimal(maximum) == Decimal("25.000000")
        except (TypeError, ValueError):
            maximum_matches = False
        if (
            operation_id != C_SERIES_PRE_LEDGER_OPERATION_ID
            or category != "historical"
            or provider != "unattributed"
            or model != "unattributed"
            or not maximum_matches
            or attempts != 1
        ):
            raise MigrationGuardError(f"reviewed {revision} pre-ledger hold identity changed")
        if status == "uncertain":
            valid = actual is None and release_reason is None
        elif status == "settled":
            valid = actual is not None and receipt is not None
        elif status == "released":
            valid = (
                actual is None
                and isinstance(release_reason, str)
                and bool(
                    re.fullmatch(
                        r"operator-no-charge evidence=[A-Za-z0-9][A-Za-z0-9._:/#-]{0,159}; \S.*",
                        release_reason,
                    )
                )
            )
        else:
            valid = False
        if not valid:
            raise MigrationGuardError(f"reviewed {revision} pre-ledger hold outcome is invalid")


async def _verify_reviewed_0139(connection: AsyncConnection) -> None:
    """Accept only C20's held USD 25 account on the reviewed 0139 revision."""
    await _verify_reviewed_budget_schema(
        connection,
        expected_accounts={
            **PILOT_LIMITS_USD,
            **C_SERIES_PILOT_LIMITS_USD,
            C20_PILOT_SLUG: C20_PILOT_LIMIT_USD,
        },
        revision="0139",
    )
    await _verify_c_series_holds(connection, revision="0139")
    await _verify_c20_ownership(connection)


async def _verify_c20_ownership(connection: AsyncConnection) -> None:
    # The later migration must record that it created this exact account. A
    # matching row that predated 0139 is not proof of a new per-film ledger.
    rows = await connection.execute(
        text("SELECT slug, account_created, account_created_at FROM video_pilot_budget_0139_owned")
    )
    owners = rows.all()
    if len(owners) != 1 or owners[0][0] != C20_PILOT_SLUG or owners[0][1] is not True:
        raise MigrationGuardError("reviewed 0139 C20 ownership record is invalid")
    account = await connection.execute(
        select(VideoPilotBudget.created_at).where(VideoPilotBudget.slug == C20_PILOT_SLUG)
    )
    if owners[0][2] is None or owners[0][2] != account.scalar_one():
        raise MigrationGuardError("reviewed 0139 C20 ownership timestamp changed")
    constraints = await connection.execute(
        text(
            "SELECT con.contype, con.convalidated, pg_get_constraintdef(con.oid) "
            "FROM pg_constraint AS con "
            "WHERE con.conrelid = 'video_pilot_budget_0139_owned'::regclass "
            "AND con.conname = 'video_pilot_budget_0139_owned_pkey'"
        )
    )
    primary_keys = constraints.all()
    if (
        len(primary_keys) != 1
        or _pg_char(primary_keys[0][0]) != "p"
        or primary_keys[0][1] is not True
        or _canonical_check(primary_keys[0][2]).upper() != "PRIMARYKEYSLUG"
    ):
        raise MigrationGuardError("reviewed 0139 C20 ownership primary key changed")


async def _verify_reviewed_0140(connection: AsyncConnection) -> None:
    """Accept only the held C08 account added after reviewed C20 0139."""
    await _verify_reviewed_budget_schema(
        connection,
        expected_accounts={
            **PILOT_LIMITS_USD,
            **C_SERIES_PILOT_LIMITS_USD,
            C20_PILOT_SLUG: C20_PILOT_LIMIT_USD,
            C08_PILOT_SLUG: C08_PILOT_LIMIT_USD,
        },
        revision="0140",
    )
    await _verify_c_series_holds(connection, revision="0140")
    await _verify_c20_ownership(connection)
    rows = await connection.execute(
        text("SELECT slug, account_created, account_created_at FROM video_pilot_budget_0140_owned")
    )
    owners = rows.all()
    if len(owners) != 1 or owners[0][0] != C08_PILOT_SLUG or owners[0][1] is not True:
        raise MigrationGuardError("reviewed 0140 C08 ownership record is invalid")
    account = await connection.execute(
        select(VideoPilotBudget.created_at).where(VideoPilotBudget.slug == C08_PILOT_SLUG)
    )
    if owners[0][2] is None or owners[0][2] != account.scalar_one():
        raise MigrationGuardError("reviewed 0140 C08 ownership timestamp changed")
    constraints = await connection.execute(
        text(
            "SELECT con.contype, con.convalidated, pg_get_constraintdef(con.oid) "
            "FROM pg_constraint AS con "
            "WHERE con.conrelid = 'video_pilot_budget_0140_owned'::regclass "
            "AND con.conname = 'video_pilot_budget_0140_owned_pkey'"
        )
    )
    primary_keys = constraints.all()
    if (
        len(primary_keys) != 1
        or _pg_char(primary_keys[0][0]) != "p"
        or primary_keys[0][1] is not True
        or _canonical_check(primary_keys[0][2]).upper() != "PRIMARYKEYSLUG"
    ):
        raise MigrationGuardError("reviewed 0140 C08 ownership primary key changed")


async def read_state() -> MigrationState:
    expected = expected_schema_revision()
    known = {revision.revision for revision in migration_revisions()}
    engine = create_async_engine(get_settings().database_url, poolclass=NullPool)
    try:
        async with engine.connect() as connection:
            state = classify_revisions(await _revisions(connection), expected, known)
            if state.state == "rollback-compatible":
                if state.current == REVIEWED_FUTURE_REVISION:
                    await _verify_reviewed_0133(connection)
                elif state.current == C_SERIES_REVIEWED_FUTURE_REVISION:
                    await _verify_reviewed_0138(connection)
                elif state.current == C20_REVIEWED_FUTURE_REVISION:
                    await _verify_reviewed_0139(connection)
                elif state.current == C08_REVIEWED_FUTURE_REVISION:
                    await _verify_reviewed_0140(connection)
                else:
                    raise MigrationGuardError("unreviewed rollback revision")
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
