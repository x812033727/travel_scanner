"""Affiliate click report: which partner, surface, module and destination get clicks.

Reads only the append-only ``affiliate_clicks`` ledger, never a provider API, so it
counts redirects and cannot claim a booking or a commission. Modelled on
``app.analytics.discovery``: a handful of grouped counts over indexed columns, small
enough to run against sqlite in a unit test.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import ColumnElement, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.affiliates.sub_id import is_catalog_sub_id
from app.analytics.schemas import AnalyticsRange
from app.analytics.service import _range_bounds
from app.models import AffiliateClick

LIMIT = 10
UNKNOWN = "unknown"
# (report key, column). The nullable columns are coalesced: rows written before the
# surface started recording its placement, or before brands existed, count as unknown
# rather than vanishing from the totals.
DIMENSIONS: tuple[tuple[str, Any], ...] = (
    ("by_partner", AffiliateClick.partner),
    ("by_module", AffiliateClick.module),
    ("by_placement", AffiliateClick.placement),
    ("by_destination", AffiliateClick.destination_id),
    ("by_brand", AffiliateClick.brand),
    ("by_target_host", AffiliateClick.target_host),
)


async def _count(session: AsyncSession, *where: ColumnElement[bool]) -> int:
    return int(
        await session.scalar(select(func.count()).select_from(AffiliateClick).where(*where)) or 0
    )


async def affiliate_report(
    session: AsyncSession, value: AnalyticsRange, now: datetime | None = None
) -> dict[str, Any]:
    now = now or datetime.now(UTC)
    start, end, _ = _range_bounds(value, now)
    # Inclusive end, like the dashboard and discovery metrics: `end` is "now".
    window = (AffiliateClick.created_at >= start, AffiliateClick.created_at <= end)
    total = await _count(session, *window)
    previous_total = await _count(
        session,
        AffiliateClick.created_at >= start - (end - start),
        AffiliateClick.created_at < start,
    )
    report: dict[str, Any] = {
        "range": value,
        "timezone": "Asia/Taipei",
        "from": start.isoformat(),
        "to": end.isoformat(),
        "total": total,
        "previous_total": previous_total,
        "change": (
            round((total - previous_total) * 100 / previous_total, 1) if previous_total else None
        ),
    }
    for name, column in DIMENSIONS:
        key = func.coalesce(column, UNKNOWN)
        rows = await session.execute(
            select(key, func.count())
            .select_from(AffiliateClick)
            .where(*window)
            .group_by(key)
            .order_by(func.count().desc(), key)
            .limit(LIMIT)
        )
        report[name] = [{"key": str(label), "value": int(count)} for label, count in rows]
    # sub_id rows written before 2026-09-12 could carry a member-derived pseudonym. Only
    # values shaped like our catalog labels are echoed; everything else folds into one
    # bucket so the report never becomes a second place an identifier is displayed.
    rows = await session.execute(
        select(AffiliateClick.sub_id, func.count())
        .where(*window)
        .group_by(AffiliateClick.sub_id)
        .order_by(func.count().desc(), AffiliateClick.sub_id)
        .limit(LIMIT * 5)
    )
    ranked: list[dict[str, Any]] = []
    unknown = 0
    for sub_id, count in rows:
        if is_catalog_sub_id(str(sub_id)) and len(ranked) < LIMIT:
            ranked.append({"key": str(sub_id), "value": int(count)})
        elif not is_catalog_sub_id(str(sub_id)):
            unknown += int(count)
    if unknown:
        ranked.append({"key": UNKNOWN, "value": unknown})
    report["top_sub_ids"] = ranked
    return report
