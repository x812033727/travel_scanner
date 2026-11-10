"""Bounded advisory checks. Publication evidence and articles are never refreshed here."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ValidationError
from sqlalchemy import func, or_, select, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.selectable import Subquery

from app.guides.models import GuideArticle
from app.news_automation.fetch import SafeNewsFetcher
from app.news_automation.models import (
    NewsAutomationSettings,
    NewsCandidate,
    NewsEvidence,
    NewsPipelineRun,
)
from app.news_automation.validation import revalidate_evidence

STAGE = "freshness-check"
COVERAGE_DAYS = 90
INTERVAL_DAYS = 7
MAX_CANDIDATES = 20
MAX_EVIDENCE = 4
CHECK_SECONDS = 25
BATCH_SECONDS = 540
FreshnessStatus = Literal["unchanged", "changed", "unverified", "pending"]
FreshnessView = Literal["all", "due", "changed"]


class CheckResult(BaseModel):
    status: FreshnessStatus
    checked_sources: int = 0
    total_sources: int = 0
    changed_sources: int = 0
    unavailable_sources: int = 0


class FreshnessItem(BaseModel):
    candidate_id: UUID
    title: str
    published_at: datetime | None
    checked_at: datetime | None
    status: FreshnessStatus
    review_due: bool
    validity_expired: bool
    result: CheckResult | None


class FreshnessReport(BaseModel):
    enabled: bool
    coverage_days: int = COVERAGE_DAYS
    interval_days: int = INTERVAL_DAYS
    daily_limit: int = MAX_CANDIDATES
    eligible_count: int
    due_count: int
    total_count: int
    page: int
    pages: int
    items: list[FreshnessItem]


def _snapshot(row: NewsEvidence) -> NewsEvidence:
    # Transient objects, never added to the session: revalidation's retrieved_at/etag
    # updates must not change publication provenance or extend excerpt retention.
    return NewsEvidence(
        id=row.id,
        candidate_id=row.candidate_id,
        role=row.role,
        is_first_party=row.is_first_party,
        url=row.url,
        title=row.title,
        retrieved_at=row.retrieved_at,
        source_date=row.source_date,
        etag=row.etag,
        last_modified=row.last_modified,
        content_hash=row.content_hash,
        body_hash=row.body_hash,
        excerpt=row.excerpt,
    )


async def check_evidence(
    session: AsyncSession, evidence: list[NewsEvidence], fetcher: SafeNewsFetcher
) -> CheckResult:
    selected = evidence[:MAX_EVIDENCE]
    if not selected:
        return CheckResult(status="unverified")
    try:
        async with asyncio.timeout(CHECK_SECONDS):
            _, reasons = await revalidate_evidence(
                session, [_snapshot(row) for row in selected], fetcher=fetcher
            )
    except TimeoutError:
        return CheckResult(status="unverified", total_sources=len(evidence))
    changed = sum(f"source_content_changed:{row.url}" in reasons for row in selected)
    unavailable = len(reasons) - changed
    status: FreshnessStatus = "unchanged"
    if changed:
        status = "changed"
    elif unavailable or len(selected) < len(evidence):
        status = "unverified"
    return CheckResult(
        status=status,
        checked_sources=len(selected),
        total_sources=len(evidence),
        changed_sources=changed,
        unavailable_sources=unavailable,
    )


def _latest(now: datetime) -> Subquery:
    return (
        select(NewsPipelineRun.candidate_id, func.max(NewsPipelineRun.started_at).label("checked"))
        .join(NewsCandidate, NewsCandidate.id == NewsPipelineRun.candidate_id)
        .where(NewsPipelineRun.stage == STAGE, *_coverage(now))
        .group_by(NewsPipelineRun.candidate_id)
        .subquery()
    )


def _coverage(now: datetime) -> tuple[ColumnElement[bool], ...]:
    return (
        NewsCandidate.status == "published",
        NewsCandidate.guide_article_id.is_not(None),
        NewsCandidate.published_at >= now - timedelta(days=COVERAGE_DAYS),
    )


async def _reserve_check(
    session: AsyncSession,
    candidate_id: UUID,
    now: datetime | None = None,
    *,
    clock: Callable[[], datetime] | None = None,
) -> UUID | None:
    # Serialize only the small quota reservation, never network I/O. Queue deliveries
    # and concurrent workers share the same hard daily cap, including failed attempts.
    await session.execute(text("SELECT pg_advisory_xact_lock(184729, 11010)"))
    now = now or (clock() if clock is not None else datetime.now(UTC))
    last_attempt = await session.scalar(
        select(func.max(NewsPipelineRun.started_at)).where(
            NewsPipelineRun.candidate_id == candidate_id,
            NewsPipelineRun.stage == STAGE,
        )
    )
    if last_attempt is not None and last_attempt >= now - timedelta(days=INTERVAL_DAYS):
        await session.commit()
        return None
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    used = int(
        await session.scalar(
            select(func.count())
            .select_from(NewsPipelineRun)
            .where(
                NewsPipelineRun.stage == STAGE,
                NewsPipelineRun.started_at >= day_start,
                NewsPipelineRun.started_at < day_start + timedelta(days=1),
            )
        )
        or 0
    )
    if used >= MAX_CANDIDATES:
        await session.commit()
        return None
    run_id = await session.scalar(
        insert(NewsPipelineRun)
        .values(
            candidate_id=candidate_id,
            stage=STAGE,
            status="running",
            attempt=1,
            idempotency_key=f"{STAGE}:{candidate_id}:{now.date().isoformat()}",
            metadata_json={},
            started_at=now,
        )
        .on_conflict_do_nothing(index_elements=["idempotency_key"])
        .returning(NewsPipelineRun.id)
    )
    await session.commit()
    return run_id


async def run_checks(
    session: AsyncSession,
    fetcher: SafeNewsFetcher,
    *,
    now: datetime | None = None,
    clock: Callable[[], datetime] | None = None,
) -> int:
    now = now or datetime.now(UTC)
    settings = await session.get(NewsAutomationSettings, 1)
    if settings is None or not settings.enabled:
        return 0
    latest = _latest(now)
    candidates = list(
        await session.scalars(
            select(NewsCandidate)
            .outerjoin(latest, latest.c.candidate_id == NewsCandidate.id)
            .where(
                *_coverage(now),
                or_(
                    latest.c.checked.is_(None),
                    latest.c.checked < now - timedelta(days=INTERVAL_DAYS),
                ),
            )
            .order_by(
                latest.c.checked.asc().nulls_first(), NewsCandidate.published_at, NewsCandidate.id
            )
            .limit(MAX_CANDIDATES)
        )
    )
    deadline = time.monotonic() + BATCH_SECONDS
    completed = 0
    for candidate in candidates:
        if time.monotonic() + CHECK_SECONDS > deadline:
            break
        # The database guards duplicate queue deliveries; a killed run remains visible
        # as unverified instead of automatically trying the same candidate again today.
        run_id = await _reserve_check(session, candidate.id, clock=clock)
        if run_id is None:
            continue
        run = await session.get(NewsPipelineRun, run_id)
        assert run is not None
        evidence = list(
            await session.scalars(
                select(NewsEvidence)
                .where(NewsEvidence.candidate_id == candidate.id)
                .order_by(NewsEvidence.is_first_party.desc(), NewsEvidence.id)
            )
        )
        try:
            result = await check_evidence(session, evidence, fetcher)
        except Exception:
            # Do not persist fetched content, headers, credentials or exception text.
            run.status = "failed"
            run.error_code = "freshness_check_failed"
            run.metadata_json = CheckResult(status="unverified").model_dump()
            run.finished_at = datetime.now(UTC)
            await session.commit()
            raise
        run.status = "succeeded"
        run.metadata_json = result.model_dump()
        run.finished_at = datetime.now(UTC)
        await session.commit()
        completed += 1
    return completed


async def report(
    session: AsyncSession,
    *,
    now: datetime | None = None,
    view: FreshnessView = "all",
    page: int = 1,
) -> FreshnessReport:
    now = now or datetime.now(UTC)
    settings = await session.get(NewsAutomationSettings, 1)
    latest = _latest(now)
    due = or_(latest.c.checked.is_(None), latest.c.checked < now - timedelta(days=INTERVAL_DAYS))
    base = select(NewsCandidate).where(*_coverage(now))
    eligible_count = int(
        await session.scalar(select(func.count()).select_from(base.subquery())) or 0
    )
    due_count = int(
        await session.scalar(
            select(func.count())
            .select_from(NewsCandidate)
            .outerjoin(latest, latest.c.candidate_id == NewsCandidate.id)
            .where(*_coverage(now), due)
        )
        or 0
    )
    # Filter before pagination, so overdue rows cannot disappear behind recent results.
    query = (
        select(NewsCandidate, NewsPipelineRun, GuideArticle.valid_until)
        .outerjoin(latest, latest.c.candidate_id == NewsCandidate.id)
        .outerjoin(
            NewsPipelineRun,
            (NewsPipelineRun.candidate_id == NewsCandidate.id)
            & (NewsPipelineRun.stage == STAGE)
            & (NewsPipelineRun.started_at == latest.c.checked),
        )
        .join(GuideArticle, GuideArticle.id == NewsCandidate.guide_article_id)
        .where(*_coverage(now))
    )
    if view == "due":
        query = query.where(due)
    elif view == "changed":
        query = query.where(NewsPipelineRun.metadata_json["status"].as_string() == "changed")
    total_count = int(await session.scalar(select(func.count()).select_from(query.subquery())) or 0)
    rows = (
        await session.execute(
            query.order_by(
                (NewsPipelineRun.metadata_json["status"].as_string() == "changed")
                .desc()
                .nulls_last(),
                latest.c.checked.desc().nulls_last(),
                NewsCandidate.published_at.desc(),
                NewsCandidate.id,
            )
            .limit(25)
            .offset((page - 1) * 25)
        )
    ).all()
    items = []
    for candidate, run, valid_until in rows:
        try:
            result = (
                CheckResult.model_validate(run.metadata_json) if run and run.metadata_json else None
            )
        except ValidationError:
            result = CheckResult(status="unverified")
        checked_at = run.started_at if run else None
        items.append(
            FreshnessItem(
                candidate_id=candidate.id,
                title=candidate.source_title,
                published_at=candidate.published_at,
                checked_at=checked_at,
                status=result.status if result else "unverified" if run else "pending",
                review_due=checked_at is None or checked_at < now - timedelta(days=INTERVAL_DAYS),
                validity_expired=valid_until is not None and valid_until < now.date(),
                result=result,
            )
        )
    return FreshnessReport(
        enabled=bool(settings and settings.enabled),
        eligible_count=eligible_count,
        due_count=due_count,
        total_count=total_count,
        page=page,
        pages=max(1, (total_count + 24) // 25),
        items=items,
    )
