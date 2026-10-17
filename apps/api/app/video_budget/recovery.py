"""Host-only readback and evidence-bound reconciliation of pilot budget operations.

Never infer a no-charge outcome from a timeout or a failed media job. An operator must
compare the provider's billing/task record with the exact operation, then supply an opaque
evidence reference. A no-charge release closes that operation ID permanently; a media job
may retry only with a new ID after its old attempt is marked reconciled.
"""

from __future__ import annotations

import re
from collections.abc import Awaitable, Callable
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.video_budget import service
from app.video_budget.models import VideoPilotBudgetOperation, utcnow
from app.video_media.models import VideoMediaJob

LockProbe = Callable[[UUID], Awaitable[bool]]
EVIDENCE_REF = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/#-]{0,159}\Z")
MEDIA_NO_CHARGE_CODE = "video_media_no_charge_reconciled"


def _evidence(value: str) -> str:
    if not EVIDENCE_REF.fullmatch(value):
        raise service.BudgetError(
            422,
            "video_budget_invalid_evidence",
            "證據編號須為 1–160 個英數與 ._:/#- 字元；請勿貼金鑰或帶參數網址",
        )
    return value


def _record(row: VideoPilotBudgetOperation, jobs: list[VideoMediaJob]) -> dict[str, Any]:
    return {
        "operation_id": row.operation_id,
        "status": row.status,
        "category": row.category,
        "provider": row.provider,
        "model": row.model,
        "max_usd": str(row.max_usd),
        "actual_usd": str(row.actual_usd) if row.actual_usd is not None else None,
        "attempts": row.attempts,
        "receipt_ref": row.receipt_ref,
        "release_reason": row.release_reason,
        "created_at": row.created_at.isoformat(),
        "updated_at": row.updated_at.isoformat(),
        "media_jobs": [
            {
                "id": str(job.id),
                "status": job.status,
                "kind": job.kind,
                "provider": job.provider,
                "model": job.model,
                "error_code": job.error_code,
                # Vendor task IDs help match a billing record. Never print a signed URL,
                # token-bearing query string, or arbitrary provider response.
                "vendor_ref": (
                    job.vendor_ref
                    if job.vendor_ref and EVIDENCE_REF.fullmatch(job.vendor_ref)
                    else None
                ),
                "vendor_ref_present": job.vendor_ref is not None,
                "submitted_at": job.submitted_at.isoformat() if job.submitted_at else None,
            }
            for job in jobs
        ],
    }


async def _rows(
    session: AsyncSession, slug: str, operation_id: str | None, *, lock: bool = False
) -> list[tuple[VideoPilotBudgetOperation, list[VideoMediaJob]]]:
    query = select(VideoPilotBudgetOperation).where(VideoPilotBudgetOperation.slug == slug)
    if operation_id is not None:
        query = query.where(VideoPilotBudgetOperation.operation_id == operation_id)
    if lock:
        query = query.with_for_update().execution_options(populate_existing=True)
    operations = (await session.scalars(query.order_by(VideoPilotBudgetOperation.created_at))).all()
    if operation_id is not None and not operations:
        raise service.BudgetError(404, "video_budget_operation_missing", "找不到這筆付費操作預留")
    job_query = select(VideoMediaJob).where(VideoMediaJob.slug == slug)
    if lock:
        job_query = job_query.with_for_update().execution_options(populate_existing=True)
    jobs = (await session.scalars(job_query)).all()
    by_operation: dict[str, list[VideoMediaJob]] = {row.operation_id: [] for row in operations}
    for job in jobs:
        linked_id = job.request.get("pilot_budget_operation_id") if job.request else None
        if isinstance(linked_id, str) and linked_id in by_operation:
            by_operation[linked_id].append(job)
    return [(row, by_operation[row.operation_id]) for row in operations]


async def inspect(
    session: AsyncSession, *, slug: str, operation_id: str | None = None
) -> dict[str, Any]:
    """Read the account, exact ledger rows and related media state without mutation."""
    if not service.is_pilot(slug):
        raise service.BudgetError(422, "video_budget_not_pilot", "請指定受預算保護的影片 slug")
    account = await service.summary(session, slug)
    assert account is not None
    rows = await _rows(session, slug, operation_id)
    return {
        "slug": slug,
        "limit_usd": str(account.limit_usd),
        "reserved_usd": str(account.reserved_usd),
        "settled_usd": str(account.settled_usd),
        "remaining_usd": str(account.remaining_usd),
        "total_over_limit": account.total_over_limit,
        "over_limit_usd": str(account.over_limit_usd),
        "uncertain_operations": account.uncertain_operations,
        "overrun_operations": account.overrun_operations,
        "operations": [_record(row, jobs) for row, jobs in rows],
    }


async def reconcile(
    session: AsyncSession,
    *,
    slug: str,
    operation_id: str,
    action: str,
    evidence_ref: str,
    expected_status: str,
    apply: bool = False,
    actual_usd: Decimal | None = None,
    no_charge_reason: str | None = None,
    worker_stopped: bool = False,
    lock_probe: LockProbe | None = None,
) -> dict[str, Any]:
    """Plan or apply one documented resolution; recheck all state under DB row locks.

    ``worker_stopped`` is an operator assertion, required for any live media job. Redis
    locks are additionally checked, but their absence alone cannot prove the worker stopped.
    """
    if not service.is_pilot(slug):
        raise service.BudgetError(422, "video_budget_not_pilot", "請指定受預算保護的影片 slug")
    if action not in {"settle", "release"}:
        raise service.BudgetError(422, "video_budget_invalid_action", "只支援 settle 或 release")
    evidence_ref = _evidence(evidence_ref)
    if expected_status not in {"reserved", "uncertain", "released"}:
        raise service.BudgetError(
            422, "video_budget_invalid_status", "預期狀態必須是有效的未結操作"
        )
    if action == "settle":
        if actual_usd is None or no_charge_reason is not None:
            raise service.BudgetError(
                422, "video_budget_invalid_action", "settle 須提供實際美元金額"
            )
        actual = service._amount(
            actual_usd, allow_zero=True, code="video_budget_actual_unknown"
        )
    else:
        if actual_usd is not None or not no_charge_reason or "\n" in no_charge_reason:
            raise service.BudgetError(
                422, "video_budget_invalid_action", "release 須提供未收費原因"
            )
        actual = None
        no_charge_reason = no_charge_reason.strip()
        if not no_charge_reason or len(no_charge_reason) > 80:
            raise service.BudgetError(422, "video_budget_invalid_action", "未收費原因須為 1–80 字")
        if len(f"{service.OPERATOR_NO_CHARGE_PREFIX}{evidence_ref}; {no_charge_reason}") > 255:
            raise service.BudgetError(422, "video_budget_invalid_evidence", "證據編號與原因過長")

    if apply:
        await service._locked_account(session, slug)
    rows = await _rows(session, slug, operation_id, lock=apply)
    row, jobs = rows[0]
    if row.status != expected_status:
        raise service.BudgetError(
            409, "video_budget_status_changed", "操作狀態已改變，請重新唯讀檢查"
        )
    if row.status == "released" and not (
        action == "settle"
        and (row.release_reason or "").startswith(service.OPERATOR_NO_CHARGE_PREFIX)
    ):
        raise service.BudgetError(409, "video_budget_operation_conflict", "這筆操作已釋放")
    live_media = any(job.status in {"queued", "submitted"} for job in jobs)
    if live_media and not worker_stopped:
        raise service.BudgetError(
            409, "video_budget_worker_active", "媒體工作仍可執行；先停用處理器再對帳"
        )
    if action == "release":
        if any(job.status == "ready" for job in jobs):
            raise service.BudgetError(
                409, "video_budget_media_ready", "媒體已有成品，不能當成未收費釋放"
            )
    if jobs and (action == "release" or live_media):
        if lock_probe is None:
            raise service.BudgetError(
                503, "video_budget_lock_unknown", "無法核對媒體工作鎖，不能釋放預留"
            )
        for job in jobs:
            if await lock_probe(job.id):
                raise service.BudgetError(
                    409, "video_budget_media_locked", "媒體工作鎖仍在，不能釋放預留"
                )

    result = {
        "apply": apply,
        "action": action,
        "evidence_ref": evidence_ref,
        "expected_status": expected_status,
        "operation": _record(row, jobs),
        "planned_actual_usd": str(actual) if actual is not None else None,
    }
    if not apply:
        return result
    if action == "settle":
        assert actual is not None
        await service.settle(
            session, slug=slug, operation_id=operation_id, actual_usd=actual,
            receipt_ref=evidence_ref,
        )
    else:
        assert no_charge_reason is not None
        reason = f"{service.OPERATOR_NO_CHARGE_PREFIX}{evidence_ref}; {no_charge_reason}"
        for job in jobs:
            job.status = "failed"
            job.error_code = MEDIA_NO_CHARGE_CODE
            job.error_detail = (
                "Operator verified provider did not charge this attempt; "
                "retry uses a new budget operation ID."
            )
            job.updated_at = utcnow()
        await service.release(session, slug=slug, operation_id=operation_id, reason=reason)
    result["operation"] = _record(row, jobs)
    return result
