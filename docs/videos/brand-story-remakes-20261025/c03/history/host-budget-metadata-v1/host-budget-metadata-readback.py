#!/usr/bin/env python3
"""Host/API-container-only C03 metadata probe; never grants paid admission.

No command-line inputs, account creation, ORM flush, provider call or reconciliation.
SQL data queries are SELECTs with fixed slug parameters. SET TRANSACTION and SHOW
only establish and verify the transaction's read-only/repeatable-read protection.
Run through the adjacent reviewed shell wrapper on the already connected host.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import platform
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

OLD_SLUG = "story-everyday-moleskine-c03"
NEW_SLUG = "story-everyday-moleskine-c03-remake-20261025"
SLUGS = (OLD_SLUG, NEW_SLUG)
BASELINE_COMMIT = "8c338dfc264dedaf200e4e50da816631285c207a"
BASELINE_HASHES = {
    "models": "8eaad7c3c125ee206d2896f4fa31e8e05e4e4af6d7b038801566b2646485d98e",
    "service": "1b3043b58f2811e8a2176bb210c34cb7b0ef26928c79f7c7bf51fcb4aaf4cecf",
    "db": "5fa7d7036175ab6a891408982d2eac27b8dfcebefc5791c2e04db15f82584997",
    "schema": "9deef8ae92447bde10916d7383c62a939d7153587ae5458715b9a15df313f9a2",
}
HISTORY_OPERATION = "pre-ledger-history"
HISTORY_RECEIPT = "owner-decision-20261024-c03-full-ceiling"
MICRO = Decimal("0.000001")
ZERO = Decimal("0")
EXPECTED_CAP = Decimal("25")
REQUIRED_COLUMNS = {
    "video_pilot_budgets": {"slug": "character varying", "limit_usd": "numeric"},
    "video_pilot_budget_operations": {
        "slug": "character varying", "operation_id": "character varying",
        "status": "character varying", "max_usd": "numeric",
        "actual_usd": "numeric", "receipt_ref": "character varying",
    },
}

ACCOUNT_SQL = """
SELECT slug, limit_usd FROM public.video_pilot_budgets
WHERE slug IN (:old_slug, :new_slug)
"""
AGGREGATE_SQL = """
SELECT slug, status,
       CASE WHEN operation_id = :history_operation THEN 1 ELSE 0 END AS preledger,
       CASE WHEN slug = :old_slug AND :recognize_history
                 AND operation_id = :history_operation AND status = :settled_status
                 AND receipt_ref = :history_receipt AND actual_usd = max_usd
            THEN 1 ELSE 0 END AS owner_closed,
       count(*) AS operation_count,
       coalesce(sum(max_usd), 0) AS ceiling_usd,
       coalesce(sum(actual_usd), 0) AS actual_usd,
       sum(CASE WHEN status = :settled_status AND actual_usd IS NULL THEN 1 ELSE 0 END)
           AS missing_actual_count,
       sum(CASE WHEN max_usd <= 0 OR actual_usd < 0 THEN 1 ELSE 0 END)
           AS invalid_amount_count,
       sum(CASE WHEN status = :settled_status AND actual_usd > max_usd THEN 1 ELSE 0 END)
           AS overrun_count
FROM public.video_pilot_budget_operations
WHERE slug IN (:old_slug, :new_slug)
GROUP BY slug, status, preledger, owner_closed
"""
COLUMNS_SQL = """
SELECT table_name, column_name, data_type FROM information_schema.columns
WHERE table_schema = :schema_name AND table_name IN (:account_table, :operation_table)
"""


def amount(value: Any) -> Decimal:
    result = value if isinstance(value, Decimal) else Decimal(str(value))
    if not result.is_finite():
        raise ValueError("invalid_amount")
    return result


def money(value: Decimal) -> str:
    return format(value.quantize(MICRO), "f")


def file_hash(module: Any) -> str:
    return hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()


def unknown_account(slug: str, registry: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "slug": slug, "account_exists": None, "metadata_status": "UNKNOWN",
        "cap_usd": None, "settled_usd": None, "reserved_usd": None,
        "uncertain_usd": None, "uncertain_operations": None, "available_usd": None,
        "registry": registry, "paid_dispatch_readiness": "NOT_READY",
        "admissible_available_usd": None, "reason_codes": [reason],
    }


def summarize_account(
    slug: str, account: dict[str, Any] | None, groups: list[dict[str, Any]],
    registry: dict[str, Any], history_semantics_verified: bool,
) -> dict[str, Any]:
    """Pure arithmetic over bounded aggregates; never uses the native summary guard."""
    result = unknown_account(slug, registry, "account_missing")
    result["account_exists"] = account is not None
    if account is None:
        result["metadata_status"] = "NOT_READY"
        return result
    try:
        cap = amount(account["limit_usd"])
        if cap <= ZERO:
            raise ValueError("invalid_cap")
        gross_settled = ZERO
        reserved = ZERO
        reserved_only = ZERO
        uncertain = ZERO
        closed = ZERO
        history_uncertain = ZERO
        history_uncertain_count = 0
        uncertain_count = 0
        operation_count = 0
        overrun_count = 0
        invalid = False
        for group in groups:
            if group["slug"] != slug:
                continue
            count = int(group["operation_count"])
            ceiling = amount(group["ceiling_usd"])
            actual = amount(group["actual_usd"])
            status = group["status"]
            operation_count += count
            invalid = invalid or (
                count < 0 or ceiling < ZERO or actual < ZERO
                or status not in {"reserved", "uncertain", "settled", "released"}
                or int(group["missing_actual_count"]) != 0
                or int(group["invalid_amount_count"]) != 0
            )
            overrun_count += int(group["overrun_count"])
            if status in {"reserved", "uncertain"}:
                reserved += ceiling
            if status == "reserved":
                reserved_only += ceiling
            if status == "uncertain":
                uncertain += ceiling
                uncertain_count += count
                if slug == OLD_SLUG and bool(group["preledger"]):
                    history_uncertain += ceiling
                    history_uncertain_count += count
            if status == "settled":
                gross_settled += actual
                if bool(group["owner_closed"]) and history_semantics_verified:
                    closed += actual
        if invalid or closed > gross_settled:
            raise ValueError("invalid_ledger")
        settled = gross_settled - closed
        available = cap - settled - reserved
        reasons = ["probe_does_not_authorize_provider_dispatch"]
        if registry["preproduction_held"] is not False:
            reasons.append("api_preproduction_held_or_unknown")
        if registry["registered_cap_usd"] != money(EXPECTED_CAP):
            reasons.append("exact_slug_not_registered_at_usd25")
        if cap != EXPECTED_CAP or registry["registered_cap_usd"] != money(cap):
            reasons.append("db_cap_does_not_match_reviewed_exact_slug_usd25")
        if not history_semantics_verified:
            reasons.append("deployed_budget_semantics_not_bound_to_reviewed_source")
        if available < ZERO or overrun_count:
            reasons.append("ledger_overrun")
        result.update({
            "metadata_status": "READ_ONLY_METADATA_OBTAINED",
            "cap_usd": money(cap), "settled_usd": money(settled),
            "settled_including_closed_history_usd": money(gross_settled),
            "reserved_usd": money(reserved), "reserved_only_usd": money(reserved_only),
            "uncertain_usd": money(uncertain), "uncertain_operations": uncertain_count,
            "historical_closed_usd": money(closed),
            "old_preledger_uncertain_usd": money(history_uncertain),
            "old_preledger_uncertain_operations": history_uncertain_count,
            "operation_count": operation_count, "overrun_operations": overrun_count,
            "available_usd": money(available),
            "available_calculation": (
                "stored_cap_minus_settled_excluding_exact_owner_closed_history_minus_reserved_including_uncertain"
                if history_semantics_verified else
                "conservative_stored_cap_minus_all_settled_minus_reserved_including_uncertain"
            ),
            "available_is_payment_authority": False,
            "admissible_available_usd": "0.000000" if len(reasons) > 1 else None,
            "paid_dispatch_readiness": "NOT_READY", "reason_codes": reasons,
        })
        return result
    except (ValueError, KeyError, TypeError, InvalidOperation, OverflowError):
        result = unknown_account(slug, registry, "invalid_or_incomplete_ledger_aggregate")
        result["account_exists"] = True
        return result


async def read_metadata() -> dict[str, Any]:
    # Imports remain inside the caught boundary. Settings/DSN and exception messages
    # are never serialized. app.db creates an engine but this probe uses no ORM session.
    from sqlalchemy import text
    from app import db, schema
    from app.video_budget import models, service

    source_hashes = {
        "models": file_hash(models), "service": file_hash(service),
        "db": file_hash(db), "schema": file_hash(schema),
    }
    semantics_verified = all(source_hashes[k] == BASELINE_HASHES[k] for k in BASELINE_HASHES)
    registries = {}
    for slug in SLUGS:
        declared = models.PILOT_LIMITS_USD.get(slug, models.C_SERIES_PILOT_LIMITS_USD.get(slug))
        registries[slug] = {
            "registered_cap_usd": money(amount(declared)) if declared is not None else None,
            "activated_exact_slug": slug in models.ACTIVATED_STORY_SLUGS,
            "preproduction_held": bool(service.is_preproduction_held(slug)),
        }
    output = {
        "probe": "c03-fixed-slug-budget-metadata-v1", "result": "NOT_READY",
        "production_authorized": False, "baseline_commit": BASELINE_COMMIT,
        "python_version": platform.python_version(), "source_sha256": source_hashes,
        "reviewed_budget_semantics_match": semantics_verified,
        "transaction": {"read_only": None, "isolation": None, "verified": False},
        "schema": {"current_revisions": [], "expected_revision": None, "compatible": False},
        "accounts": [unknown_account(s, registries[s], "metadata_not_read") for s in SLUGS],
    }
    if db.engine.dialect.name != "postgresql":
        output["reason_code"] = "unsupported_database_backend"
        return output
    expected_revision = schema.expected_schema_revision()
    output["schema"]["expected_revision"] = expected_revision
    params = {
        "old_slug": OLD_SLUG, "new_slug": NEW_SLUG,
        "history_operation": HISTORY_OPERATION, "history_receipt": HISTORY_RECEIPT,
        "settled_status": "settled",
        "recognize_history": semantics_verified and OLD_SLUG in models.ACTIVATED_STORY_SLUGS,
    }
    try:
        async with db.engine.connect() as connection:
            async with connection.begin() as transaction:
                await connection.execute(text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY"))
                read_only = (await connection.execute(text("SHOW transaction_read_only"))).scalar_one()
                isolation = (await connection.execute(text("SHOW transaction_isolation"))).scalar_one()
                verified = read_only == "on" and isolation == "repeatable read"
                output["transaction"] = {"read_only": read_only, "isolation": isolation, "verified": verified}
                if not verified:
                    output["reason_code"] = "read_only_transaction_not_verified"
                    await transaction.rollback()
                    return output
                revisions = (await connection.execute(text("SELECT version_num FROM public.alembic_version"))).scalars().all()
                # Revision identifiers are code metadata, never arbitrary DB text in output.
                valid_revisions = [r for r in revisions if isinstance(r, str) and r.replace("_", "").isalnum() and len(r) <= 100]
                compatible = len(revisions) == 1 and len(valid_revisions) == 1 and schema.schema_is_current(revisions[0])
                output["schema"].update({"current_revisions": valid_revisions, "compatible": bool(compatible)})
                columns = (await connection.execute(text(COLUMNS_SQL), {
                    "schema_name": "public", "account_table": "video_pilot_budgets",
                    "operation_table": "video_pilot_budget_operations",
                })).mappings().all()
                found = {(r["table_name"], r["column_name"]): r["data_type"] for r in columns}
                columns_match = all(found.get((table, column)) == kind for table, entries in REQUIRED_COLUMNS.items() for column, kind in entries.items())
                output["schema"]["required_columns_match"] = columns_match
                if not compatible or not columns_match:
                    output["accounts"] = [unknown_account(s, registries[s], "schema_not_compatible") for s in SLUGS]
                    output["reason_code"] = "schema_not_compatible"
                    await transaction.rollback()
                    return output
                accounts = (await connection.execute(text(ACCOUNT_SQL), params)).mappings().all()
                groups = (await connection.execute(text(AGGREGATE_SQL), params)).mappings().all()
                by_slug = {row["slug"]: dict(row) for row in accounts}
                output["accounts"] = [summarize_account(s, by_slug.get(s), groups, registries[s], semantics_verified) for s in SLUGS]
                await transaction.rollback()
        return output
    finally:
        await db.engine.dispose()


def main() -> int:
    try:
        output = asyncio.run(asyncio.wait_for(read_metadata(), timeout=45))
        complete = output["transaction"]["verified"] and output["schema"]["compatible"]
        complete = complete and all(a["metadata_status"] == "READ_ONLY_METADATA_OBTAINED" for a in output["accounts"])
        code = 3 if complete else 4
    except BaseException:
        # Do not serialize exception strings, traceback, DSN, request or provider state.
        output = {"probe": "c03-fixed-slug-budget-metadata-v1", "result": "UNKNOWN",
                  "production_authorized": False, "reason_code": "probe_unavailable_or_interrupted"}
        code = 4
    print(json.dumps(output, ensure_ascii=True, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
