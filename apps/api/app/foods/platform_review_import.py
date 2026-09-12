"""Apply a committed review file of reservation-platform outcomes to food merchants.

The admin editor records one platform review at a time through
``PUT /admin/foods/merchants/{id}/platform-link``. A catalog-wide research pass produces
hundreds of them, so this applies a reviewed JSON file with the editor's own validation
(``MerchantPlatformLinkPayload``), the same branch-identity guard and one audit entry per
written row. It writes platform rows only: merchant facts, coordinates, sources, relations
and approval are never touched.

A batch never overwrites an administrator's review. It may replace a row nobody reviewed —
the seed's conservative ``ambiguous`` audit, or an earlier batch — and otherwise only a row
whose ``checked_at`` still equals the ``expected_checked_at`` the record was researched
against, the optimistic check the admin editor itself uses.
"""

from __future__ import annotations

import sys
from collections import Counter
from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from pathlib import Path
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, ValidationError
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionFactory
from app.foods.admin_router import MerchantPlatformLinkPayload
from app.foods.platform_links import platform_url_identity
from app.models import AdminAuditLog, FoodMerchant, FoodMerchantPlatformLink

DATA_DIR = Path(__file__).resolve().parent / "data" / "platform_reviews"
DEFAULT_REVIEW_FILE = DATA_DIR / "2026-09-11-public-merchants.json"
AUDIT_ACTION = "food_merchant.cli_platform_link_reviewed"
WRITES = frozenset({"created", "updated"})
WOULD_WRITE = frozenset({"would_create", "would_update"})


class ReviewFileError(ValueError):
    """The review file cannot be applied as a whole; nothing was written."""


class ReviewEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: str = Field(min_length=8, max_length=2048)
    role: str = Field(min_length=2, max_length=64)
    observation: str = Field(min_length=2, max_length=1000)


class PlatformReviewRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    merchant_id: UUID
    slug: str = Field(min_length=1, max_length=160)
    provider: str = Field(min_length=2, max_length=32)
    status: Literal["verified", "not_found", "ambiguous", "disabled"]
    canonical_url: str | None = Field(default=None, max_length=2048)
    localized_urls: dict[str, str] = Field(default_factory=dict)
    review_note: str = Field(min_length=1, max_length=1000)
    expected_checked_at: datetime | None = None
    evidence: list[ReviewEvidence] = Field(default_factory=list)
    # Context for whoever reads the file; never written to the database.
    name: str | None = None
    country_code: str | None = None
    booking_observation: str | None = None


class PlatformReviewBatch(BaseModel):
    schema_version: Literal[1]
    batch_id: str = Field(min_length=3, max_length=120)
    researched_at: datetime
    records: list[PlatformReviewRecord]


@dataclass(frozen=True)
class RecordOutcome:
    slug: str
    provider: str
    status: str
    action: str
    detail: str | None = None


def load_review_file(path: Path) -> PlatformReviewBatch:
    """Parse and validate the whole file, so a bad record stops the batch before any write."""

    try:
        batch = PlatformReviewBatch.model_validate_json(path.read_text(encoding="utf-8"))
    except ValidationError as exc:
        raise ReviewFileError(f"{path.name}: {exc}") from exc
    problems: list[str] = []
    if batch.researched_at.tzinfo is None:
        problems.append("researched_at must include a timezone")
    slugs: dict[UUID, str] = {}
    pairs: set[tuple[UUID, str]] = set()
    branches: dict[tuple[str, str], UUID] = {}
    for index, record in enumerate(batch.records):
        label = f"records[{index}] {record.slug}/{record.provider}"
        try:
            payload = MerchantPlatformLinkPayload(
                provider=record.provider,
                status=record.status,
                canonical_url=record.canonical_url,
                localized_urls=record.localized_urls,
                review_note=record.review_note,
            )
        except ValidationError as exc:
            problems.append(f"{label}: " + "; ".join(str(err["msg"]) for err in exc.errors()))
            continue
        record.canonical_url = payload.canonical_url
        record.localized_urls = payload.localized_urls
        if record.status in {"verified", "disabled"} and not record.evidence:
            problems.append(f"{label}: a {record.status} outcome needs evidence")
        if record.expected_checked_at is not None and record.expected_checked_at.tzinfo is None:
            problems.append(f"{label}: expected_checked_at must include a timezone")
        if slugs.setdefault(record.merchant_id, record.slug) != record.slug:
            problems.append(f"{label}: the merchant id appears under two slugs")
        if (record.merchant_id, record.provider) in pairs:
            problems.append(f"{label}: the merchant and provider appear twice")
        pairs.add((record.merchant_id, record.provider))
        if record.canonical_url:
            branch = (record.provider, platform_url_identity(record.provider, record.canonical_url))
            if branches.setdefault(branch, record.merchant_id) != record.merchant_id:
                problems.append(f"{label}: the branch page is also assigned to another merchant")
    if problems:
        raise ReviewFileError(f"{path.name}: " + " | ".join(problems))
    return batch


def _aware(value: datetime) -> datetime:
    # SQLite drops timezone metadata; PostgreSQL keeps the timestamp's instant.
    return value if value.tzinfo is not None else value.replace(tzinfo=UTC)


async def _branch_owner(
    session: AsyncSession, merchant_id: UUID, provider: str, identity: str
) -> UUID | None:
    if session.get_bind().dialect.name == "postgresql":
        # The admin editor takes this same lock, so a batch write and an editor save of one
        # branch serialize instead of both passing the check below.
        lock_key = int.from_bytes(
            sha256(f"reservation:{provider}:{identity}".encode()).digest()[:8], signed=True
        )
        await session.execute(select(func.pg_advisory_xact_lock(lock_key)))
    links = await session.scalars(
        select(FoodMerchantPlatformLink).where(
            FoodMerchantPlatformLink.provider == provider,
            FoodMerchantPlatformLink.merchant_id != merchant_id,
            FoodMerchantPlatformLink.canonical_url.is_not(None),
        )
    )
    for link in links.all():
        if link.canonical_url is None:
            continue
        try:
            if platform_url_identity(provider, link.canonical_url) == identity:
                return link.merchant_id
        except ValueError:
            continue
    return None


async def _review_one(
    session: AsyncSession,
    batch: PlatformReviewBatch,
    record: PlatformReviewRecord,
    *,
    apply: bool,
) -> RecordOutcome:
    def outcome(action: str, detail: str | None = None) -> RecordOutcome:
        return RecordOutcome(record.slug, record.provider, record.status, action, detail)

    merchant = await session.scalar(
        select(FoodMerchant).where(FoodMerchant.id == record.merchant_id)
        .with_for_update().execution_options(populate_existing=True)
    )
    if merchant is None:
        return outcome("skipped_missing_merchant")
    if merchant.slug != record.slug:
        return outcome("skipped_slug_mismatch", merchant.slug)
    row = await session.scalar(
        select(FoodMerchantPlatformLink).where(
            FoodMerchantPlatformLink.merchant_id == merchant.id,
            FoodMerchantPlatformLink.provider == record.provider,
        ).with_for_update().execution_options(populate_existing=True)
    )
    previous: dict[str, Any] | None = None
    if row is not None:
        checked_at = _aware(row.checked_at)
        if record.expected_checked_at is not None:
            if checked_at != record.expected_checked_at:
                return outcome("skipped_changed_since_research", checked_at.isoformat())
        elif row.checked_by_user_id is not None:
            return outcome("skipped_admin_reviewed", checked_at.isoformat())
        current = (row.status, row.canonical_url, row.localized_urls_json or {}, row.review_note)
        wanted = (record.status, record.canonical_url, record.localized_urls, record.review_note)
        if current == wanted:
            return outcome("unchanged")
        previous = {
            "status": row.status,
            "canonical_url": row.canonical_url,
            "checked_at": checked_at.isoformat(),
        }
    elif record.expected_checked_at is not None:
        return outcome("skipped_changed_since_research", "the reviewed row no longer exists")
    if record.canonical_url:
        identity = platform_url_identity(record.provider, record.canonical_url)
        owner = await _branch_owner(session, merchant.id, record.provider, identity)
        if owner is not None:
            return outcome("skipped_branch_conflict", str(owner))
    if not apply:
        return outcome("would_update" if previous else "would_create")
    now = datetime.now(UTC)
    if row is None:
        row = FoodMerchantPlatformLink(
            merchant_id=merchant.id, provider=record.provider, status=record.status, checked_at=now
        )
        session.add(row)
    else:
        now = max(now, _aware(row.checked_at) + timedelta(microseconds=1))
    row.status = record.status
    row.canonical_url = record.canonical_url
    row.localized_urls_json = dict(record.localized_urls)
    row.review_note = record.review_note
    row.checked_at = now
    row.checked_by_user_id = None
    session.add(
        AdminAuditLog(
            actor_user_id=None,
            action=AUDIT_ACTION,
            target=f"food_merchant:{merchant.id}",
            metadata_json={
                "source": "cli",
                "batch_id": batch.batch_id,
                "slug": record.slug,
                "provider": record.provider,
                "status": record.status,
                "canonical_url": record.canonical_url,
                "localized_locales": sorted(record.localized_urls),
                "previous": previous,
                "evidence_urls": [item.url for item in record.evidence[:5]],
            },
        )
    )
    return outcome("updated" if previous else "created")


async def apply_platform_reviews(
    session: AsyncSession,
    batch: PlatformReviewBatch,
    *,
    apply: bool,
    limit: int | None = None,
    progress: Callable[[str], None] | None = None,
) -> list[RecordOutcome]:
    """Review each record in its own transaction, so one conflict never blocks the rest."""

    outcomes: list[RecordOutcome] = []
    for record in batch.records[:limit]:
        try:
            result = await _review_one(session, batch, record, apply=apply)
            if result.action in WRITES:
                await session.commit()
            else:
                # Ends the read transaction and releases the row locks this record took.
                await session.rollback()
        except IntegrityError:
            await session.rollback()
            result = RecordOutcome(
                record.slug, record.provider, record.status,
                "skipped_branch_conflict", "database constraint",
            )
        outcomes.append(result)
        if progress:
            progress(f"{record.slug} {record.provider}: {result.action}")
    return outcomes


def summarize(
    batch: PlatformReviewBatch, outcomes: list[RecordOutcome], *, apply: bool
) -> dict[str, Any]:
    actions = Counter(item.action for item in outcomes)
    statuses = Counter(item.status for item in outcomes if item.action in WRITES | WOULD_WRITE)
    return {
        "batch_id": batch.batch_id,
        "applied": apply,
        "records": len(outcomes),
        "actions": dict(sorted(actions.items())),
        "statuses": dict(sorted(statuses.items())),
        "skipped": [asdict(item) for item in outcomes if item.action.startswith("skipped")],
    }


async def apply_food_platform_reviews(
    path: Path, *, apply: bool, limit: int | None = None
) -> dict[str, Any]:
    batch = load_review_file(path)
    async with SessionFactory() as session:
        outcomes = await apply_platform_reviews(
            session,
            batch,
            apply=apply,
            limit=limit,
            progress=lambda line: print(line, file=sys.stderr, flush=True),
        )
    return summarize(batch, outcomes, apply=apply)
