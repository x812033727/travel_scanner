"""Host-only pilot budget reconciliation. Defaults to read-only inspection.

Run inside the API container, after deployment. Never use a timeout, failed job, or absent
Redis lock as proof of no charge. Match the exact provider billing/task record first; use an
opaque evidence reference, not a secret or signed URL. For a live media job, stop the media
worker/API dispatch path and confirm quiescence before ``--worker-stopped``. All actions are
dry runs until ``--apply`` and require the inspected status to prevent stale writes.

Examples::

    python -m app.video_budget.reconcile_cli --slug story-rolling-suitcase-v2
    python -m app.video_budget.reconcile_cli --slug story-rolling-suitcase-v2 \
        --operation-id OP --action settle --expected-status uncertain \
        --actual-usd 0.042 --evidence-ref invoice-2026-10-row-7
    python -m app.video_budget.reconcile_cli --slug story-rolling-suitcase-v2 \
        --operation-id OP --action release --expected-status uncertain \
        --no-charge-reason "vendor confirms no task or invoice" \
        --evidence-ref vendor-support-case-123

Repeat the exact command with ``--apply`` only after reviewing the dry-run result. A no-charge
operation ID is closed permanently; a reconciled media job gets a fresh ID on a later retry.
If a later invoice disproves no-charge evidence, settle the closed operation with that invoice.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from decimal import Decimal, InvalidOperation
from typing import Any
from uuid import UUID

from redis.asyncio import Redis

from app.config import get_settings
from app.db import SessionFactory
from app.video_budget import recovery, service


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--slug", required=True)
    command.add_argument("--operation-id")
    command.add_argument("--action", choices=("settle", "release"))
    command.add_argument("--expected-status", choices=("reserved", "uncertain", "released"))
    command.add_argument("--actual-usd")
    command.add_argument("--no-charge-reason")
    command.add_argument("--evidence-ref")
    command.add_argument("--worker-stopped", action="store_true")
    command.add_argument("--apply", action="store_true")
    return command


async def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.action is None:
        if (
            args.apply or args.expected_status or args.actual_usd or args.no_charge_reason
            or args.evidence_ref or args.worker_stopped
        ):
            raise service.BudgetError(
                422, "video_budget_invalid_action", "先指定 settle 或 release"
            )
        async with SessionFactory() as session:
            return await recovery.inspect(session, slug=args.slug, operation_id=args.operation_id)
    if not args.operation_id or not args.expected_status or not args.evidence_ref:
        raise service.BudgetError(
            422, "video_budget_invalid_action", "對帳須指定操作 ID、預期狀態與證據編號"
        )
    if args.action == "settle":
        if args.actual_usd is None:
            raise service.BudgetError(422, "video_budget_invalid_action", "settle 缺少實際美元金額")
        try:
            actual = Decimal(args.actual_usd)
        except InvalidOperation as error:
            raise service.BudgetError(
                422, "video_budget_invalid_action", "實際美元金額無效"
            ) from error
    else:
        actual = None

    async with Redis.from_url(get_settings().redis_url, socket_timeout=5) as redis:

        async def locked(job_id: UUID) -> bool:
            return bool(await redis.exists(f"video-media:lock:{job_id}"))

        async with SessionFactory() as session:
            return await recovery.reconcile(
                session,
                slug=args.slug,
                operation_id=args.operation_id,
                action=args.action,
                evidence_ref=args.evidence_ref,
                expected_status=args.expected_status,
                apply=args.apply,
                actual_usd=actual,
                no_charge_reason=args.no_charge_reason,
                worker_stopped=args.worker_stopped,
                lock_probe=locked,
            )


def main() -> int:
    args = parser().parse_args()
    try:
        result: dict[str, Any] = asyncio.run(run(args))
    except service.BudgetError as error:
        # settle() records an overrun before raising; show a separate readback command
        # rather than implying the failed process rolled back that known vendor charge.
        print(json.dumps({"error": error.code, "detail": error.detail}, ensure_ascii=False))
        return 3
    except Exception as error:
        # Redis and DB failures must fail closed and keep the hold; do not auto-retry.
        print(
            json.dumps(
                {"error": "video_budget_reconcile_unavailable", "detail": type(error).__name__}
            )
        )
        return 4
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
