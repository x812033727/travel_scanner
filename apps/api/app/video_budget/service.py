"""A fail-closed, per-slug full-film dollar gate shared by paid story dispatches.

``reserve`` commits its hold before the caller talks to a vendor. All mutations lock the
pilot's account row, so concurrent stages cannot each spend the same remaining dollars.
Callers must check ``dispatch_allowed``: a repeated reserved, uncertain, or settled operation
is never sent again. An automatically released, proven-unbilled operation may be retried;
operator-released operation IDs remain closed with their evidence.

The passed AsyncSession is committed by mutations. Call from a dedicated or otherwise clean
session; do not mix unrelated uncommitted changes into the reservation transaction.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_CEILING, Decimal, InvalidOperation

from sqlalchemy import Connection, inspect, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.problems import AppError
from app.video_budget.models import (
    FOLLOWON_LIMIT_USD,
    PILOT_LIMIT_USD,
    PILOT_LIMITS_USD,
    PILOT_SLUGS,
    VideoPilotBudget,
    VideoPilotBudgetOperation,
    utcnow,
)
from app.video_budget.prices import price_window_current

MICRO_USD = Decimal("0.000001")
ACTIVE_STATUSES = frozenset(("reserved", "uncertain"))
OPERATOR_NO_CHARGE_PREFIX = "operator-no-charge evidence="
B18_V2_SLUG = "story-conveyor-belt-sushi-v2"
B18_V2_LIMIT_USD = FOLLOWON_LIMIT_USD
A01_ADMISSION_SLUG = "story-rolling-suitcase-v2"


class BudgetError(AppError):
    """The normal API problem format, with a pilot-specific code."""


@dataclass(frozen=True)
class Reservation:
    slug: str
    operation_id: str
    max_usd: Decimal
    status: str
    created: bool
    dispatch_allowed: bool
    attempts: int


@dataclass(frozen=True)
class BudgetSummary:
    slug: str
    limit_usd: Decimal
    reserved_usd: Decimal
    settled_usd: Decimal
    remaining_usd: Decimal
    uncertain_operations: int
    settled_operations: int
    released_operations: int
    overrun_operations: int
    total_over_limit: bool
    over_limit_usd: Decimal


def is_pilot(slug: str | None) -> bool:
    return slug in PILOT_SLUGS


def _amount(value: Decimal | None, *, allow_zero: bool, code: str) -> Decimal:
    if not isinstance(value, Decimal) or not value.is_finite():
        raise BudgetError(503, code, "試作影片的供應商價格尚未核定，不能送出付費請求")
    try:
        rounded = value.quantize(MICRO_USD, rounding=ROUND_CEILING)
    except InvalidOperation as error:
        raise BudgetError(503, code, "試作影片的供應商價格無法安全計算") from error
    if rounded < 0 or (rounded == 0 and not allow_zero):
        raise BudgetError(503, code, "試作影片的付費請求沒有有效的價格上限")
    return rounded


def _label(value: str, *, name: str, length: int) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > length:
        raise BudgetError(422, "video_budget_invalid_operation", f"{name} 缺漏或長度無效")
    return value


def _account_limit_is_valid(slug: str, limit_usd: Decimal) -> bool:
    if slug == B18_V2_SLUG:
        return limit_usd in (PILOT_LIMIT_USD, B18_V2_LIMIT_USD)
    return limit_usd == PILOT_LIMITS_USD.get(slug)


async def _locked_account(session: AsyncSession, slug: str) -> VideoPilotBudget:
    account = await session.scalar(
        select(VideoPilotBudget)
        .where(VideoPilotBudget.slug == slug)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if account is None:
        raise BudgetError(503, "video_budget_missing_account", "試作影片的費用帳戶尚未就緒")
    if not _account_limit_is_valid(slug, account.limit_usd):
        raise BudgetError(503, "video_budget_invalid_account", "試作影片的費用帳戶上限不符")
    return account


def _has_admission_column(connection: Connection) -> bool:
    """Probe the current transaction's schema; this image runs on 0133 or 0134."""
    return "admission_token" in {
        column["name"] for column in inspect(connection).get_columns("video_pilot_budgets")
    }


async def _admission_held_locked(session: AsyncSession, account: VideoPilotBudget) -> bool:
    """Read the optional 0134 token while holding this account row FOR UPDATE.

    The 0133 model intentionally does not map the new column. On a 0133 database
    the probe returns False; on 0134, the raw token read uses the very same
    session and transaction. Do not cache column presence across a deploy.
    """
    if account.slug != A01_ADMISSION_SLUG:
        return False
    connection = await session.connection()
    if not await connection.run_sync(_has_admission_column):
        return False
    token = await session.scalar(
        text("SELECT admission_token FROM video_pilot_budgets WHERE slug=:slug"),
        {"slug": account.slug},
    )
    return token is not None


async def assert_a01_admission_open(session: AsyncSession, *, slug: str) -> None:
    """Join the durable text-stage dispatch transaction before its marker.

    The caller commits its dispatch marker under this same budget-row lock.
    """
    if slug != A01_ADMISSION_SLUG:
        return
    account = await _locked_account(session, slug)
    if await _admission_held_locked(session, account):
        raise BudgetError(409, "video_budget_admission_held", "A01 來源匯入期間不會派送寫稿工作")


async def _operation(
    session: AsyncSession, slug: str, operation_id: str
) -> VideoPilotBudgetOperation:
    operation = await session.scalar(
        select(VideoPilotBudgetOperation).where(
            VideoPilotBudgetOperation.slug == slug,
            VideoPilotBudgetOperation.operation_id == operation_id,
        )
    )
    if operation is None:
        raise BudgetError(404, "video_budget_operation_missing", "找不到這筆付費操作預留")
    return operation


async def _totals(session: AsyncSession, slug: str) -> tuple[Decimal, Decimal, int, int, int, int]:
    rows = (
        await session.scalars(
            select(VideoPilotBudgetOperation).where(VideoPilotBudgetOperation.slug == slug)
        )
    ).all()
    reserved = sum((row.max_usd for row in rows if row.status in ACTIVE_STATUSES), Decimal("0"))
    settled = sum(
        (row.actual_usd or Decimal("0") for row in rows if row.status == "settled"),
        Decimal("0"),
    )
    uncertain = sum(row.status == "uncertain" for row in rows)
    settled_count = sum(row.status == "settled" for row in rows)
    released = sum(row.status == "released" for row in rows)
    overruns = sum(
        row.status == "settled" and row.actual_usd is not None and row.actual_usd > row.max_usd
        for row in rows
    )
    return reserved, settled, uncertain, settled_count, released, overruns


async def reserve(
    session: AsyncSession,
    *,
    slug: str,
    operation_id: str,
    category: str,
    provider: str,
    model: str,
    max_usd: Decimal | None,
) -> Reservation | None:
    """Persist a conservative hold and return permission for exactly one vendor dispatch.

    An unknown or expired published price blocks the pilot. Another video gets ``None`` and
    follows its existing budgets unchanged. The same ID may dispatch again only after an
    automatic, proven-unbilled release. An operator no-charge release is terminal so its
    evidence remains durable; a later attempt needs a new operation ID.
    """
    if not is_pilot(slug):
        return None
    operation_id = _label(operation_id, name="operation_id", length=160)
    category = _label(category, name="category", length=40)
    provider = _label(provider, name="provider", length=40)
    model = _label(model, name="model", length=128)
    ceiling = _amount(max_usd, allow_zero=False, code="video_budget_price_unknown")
    if not price_window_current():
        raise BudgetError(
            503, "video_budget_price_expired", "試作影片供應商價格期限已過，須先重新核價"
        )

    try:
        account = await _locked_account(session, slug)
        if await _admission_held_locked(session, account):
            raise BudgetError(
                409, "video_budget_admission_held", "A01 來源匯入期間不會預留付費操作"
            )
        existing = await session.scalar(
            select(VideoPilotBudgetOperation).where(
                VideoPilotBudgetOperation.slug == slug,
                VideoPilotBudgetOperation.operation_id == operation_id,
            )
        )
        if existing is not None:
            if (existing.category, existing.provider, existing.model, existing.max_usd) != (
                category,
                provider,
                model,
                ceiling,
            ):
                raise BudgetError(
                    409,
                    "video_budget_operation_conflict",
                    "同一操作 ID 的供應商、模型或價格上限與既有預留不同",
                )
            if existing.status != "released":
                result = Reservation(
                    slug,
                    operation_id,
                    existing.max_usd,
                    existing.status,
                    False,
                    False,
                    existing.attempts,
                )
                await session.commit()
                return result
            if (existing.release_reason or "").startswith(OPERATOR_NO_CHARGE_PREFIX):
                raise BudgetError(
                    409,
                    "video_budget_operator_reconciled",
                    "人工核對未收費的操作 ID 已封存；新的付費嘗試須使用新的操作 ID",
                )

        # The compatibility release runs before 0133. Old USD 25 B18 v2 rows
        # remain readable and reconcilable, but cannot authorize a new dispatch.
        if slug == B18_V2_SLUG and account.limit_usd != B18_V2_LIMIT_USD:
            raise BudgetError(503, "video_budget_missing_account", "B18 v2 的 5 美元帳戶尚未就緒")

        reserved, settled, _, _, _, overruns = await _totals(session, slug)
        if overruns:
            raise BudgetError(
                503,
                "video_budget_overrun_hold",
                "本片有費用超過預留上限，須先人工核對，已停止後續付費操作",
            )
        if reserved + settled + ceiling > account.limit_usd:
            raise BudgetError(
                429,
                "video_budget_exhausted",
                f"這次付費請求會超過本片 {account.limit_usd:g} 美元總上限，已停止送出",
            )
        if existing is None:
            existing = VideoPilotBudgetOperation(
                slug=slug,
                operation_id=operation_id,
                category=category,
                provider=provider,
                model=model,
                max_usd=ceiling,
                status="reserved",
                attempts=1,
            )
            session.add(existing)
            created = True
        else:
            existing.status = "reserved"
            existing.attempts += 1
            existing.release_reason = None
            existing.updated_at = utcnow()
            created = False
        attempts = existing.attempts
        await session.commit()
        return Reservation(slug, operation_id, ceiling, "reserved", created, True, attempts)
    except Exception:
        await session.rollback()
        raise


async def settle(
    session: AsyncSession,
    *,
    slug: str,
    operation_id: str,
    actual_usd: Decimal,
    receipt_ref: str | None = None,
) -> None:
    """Replace the hold with documented actual cost, including an unexpected overrun.

    An over-ceiling vendor receipt is recorded before raising: hiding a known charge behind an
    old, smaller reservation would make the remaining budget falsely optimistic.
    """
    if not is_pilot(slug):
        return
    actual = _amount(actual_usd, allow_zero=True, code="video_budget_actual_unknown")
    if receipt_ref is not None:
        receipt_ref = _label(receipt_ref, name="receipt_ref", length=255)
    try:
        await _locked_account(session, slug)
        operation = await _operation(session, slug, operation_id)
        overrun = actual > operation.max_usd
        if operation.status == "settled":
            if operation.actual_usd != actual:
                raise BudgetError(
                    409, "video_budget_operation_conflict", "同一操作 ID 的實際費用不一致"
                )
        elif operation.status == "released" and not (
            (operation.release_reason or "").startswith(OPERATOR_NO_CHARGE_PREFIX)
            and receipt_ref is not None
        ):
            raise BudgetError(409, "video_budget_operation_conflict", "已證實未收費的操作不能結算")
        else:
            operation.actual_usd = actual
            operation.status = "settled"
            operation.updated_at = utcnow()
        if receipt_ref is not None:
            if operation.receipt_ref is not None and operation.receipt_ref != receipt_ref:
                raise BudgetError(409, "video_budget_operation_conflict", "收費憑證與既有記錄不同")
            operation.receipt_ref = receipt_ref
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    if overrun:
        raise BudgetError(
            503,
            "video_budget_actual_exceeds_reservation",
            "供應商實際費用超過已預留上限，須人工核對並停止後續付費操作",
        )


async def mark_uncertain(session: AsyncSession, *, slug: str, operation_id: str) -> None:
    """Keep the full hold when the vendor may have received a request."""
    if not is_pilot(slug):
        return
    try:
        await _locked_account(session, slug)
        operation = await _operation(session, slug, operation_id)
        if operation.status == "reserved":
            operation.status = "uncertain"
            operation.updated_at = utcnow()
        await session.commit()
    except Exception:
        await session.rollback()
        raise


async def release(session: AsyncSession, *, slug: str, operation_id: str, reason: str) -> None:
    """Release only after the caller has positive evidence the vendor charged nothing."""
    if not is_pilot(slug):
        return
    reason = _label(reason, name="release_reason", length=255)
    try:
        await _locked_account(session, slug)
        operation = await _operation(session, slug, operation_id)
        if operation.status == "settled":
            raise BudgetError(409, "video_budget_operation_conflict", "已結算的費用不能釋放")
        if operation.status != "released":
            operation.status = "released"
            operation.release_reason = reason
            operation.updated_at = utcnow()
        await session.commit()
    except Exception:
        await session.rollback()
        raise


async def summary(session: AsyncSession, slug: str) -> BudgetSummary | None:
    """Read the aggregate ledger for a pilot without exposing account credentials."""
    if not is_pilot(slug):
        return None
    account = await session.scalar(select(VideoPilotBudget).where(VideoPilotBudget.slug == slug))
    if account is None:
        raise BudgetError(503, "video_budget_missing_account", "試作影片的費用帳戶尚未就緒")
    if not _account_limit_is_valid(slug, account.limit_usd):
        raise BudgetError(503, "video_budget_invalid_account", "試作影片的費用帳戶上限不符")
    reserved, settled, uncertain, settled_count, released, overruns = await _totals(session, slug)
    # Show the intended ceiling even before 0133 lowers B18's persisted row.
    # This is a read-only transitional state; reserve stays held at USD 25.
    effective_limit = PILOT_LIMITS_USD[slug]
    remaining = effective_limit - reserved - settled
    return BudgetSummary(
        slug=slug,
        limit_usd=effective_limit,
        reserved_usd=reserved,
        settled_usd=settled,
        remaining_usd=remaining,
        uncertain_operations=uncertain,
        settled_operations=settled_count,
        released_operations=released,
        overrun_operations=overruns,
        total_over_limit=remaining < 0,
        over_limit_usd=max(-remaining, Decimal("0.000000")),
    )
