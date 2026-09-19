"""Find approved guides that introduce a place in another country, and reject them.

Standard discovery used to search an attraction's bare name, so Hanoi's 玉山祠 collected
the tourism bureau's page about Taiwan's 玉山 and Sapporo's 圓山公園 collected Taipei's
圓山; a scorer that read only the title approved them. The search and the review were
fixed on 2026-09-16 (``guide_search_query`` adds the city and the country,
``guide_review`` reads ``foreign_place`` before any score), but the rows those searches
had already approved stayed public: 52 of them were found through the public discovery
window alone on 2026-09-13, and that window shows at most 100 rows per source in one
locale, so nobody has read the whole ``approved`` table.

This module reads it. Every selected row goes through the same ``foreign_place`` call
the review uses, with the attraction's localized name, aliases and search terms as its
own terms, and a row that names another country and never this attraction is a
finding. ``run`` lists the findings; with an actor it rejects them through exactly the
fields the admin endpoint writes (``review_status``, ``review_reason``, ``reviewed_at``,
``reviewed_by_user_id``) and records one ``hotspot_guides_reviewed`` audit entry, so the
admin panel shows who did it and why.

The rule is not a judgement, so two lists travel with a run: ids to skip (a Hội An
article that merely lists 日本橋 was flagged on 2026-09-13 and kept), and ids to reject
although the rule cannot see them (a 三芝 淺水灣 video under Hong Kong's 淺水灣: the
attraction's own name is the other place's name too). Carry both forward; the review of
2026-09-12 lost a row exactly because a skip list was not.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.hotspots.ai_search import _localized_context
from app.hotspots.guides import foreign_place
from app.i18n import LOCALES
from app.models import AdminAuditLog, HotspotGuide, TravelHotspot

SOURCE = "guides-foreign-place-scan"
#: The reason written on a row an admin named explicitly; the rule's own findings carry
#: the country they are really about.
DEFAULT_REASON = "地點不符：內容是另一個國家的景點"


@dataclass(frozen=True)
class Finding:
    guide_id: UUID
    hotspot_id: UUID
    hotspot_name: str
    city: str
    country: str
    destination_id: str
    locale: str
    content_type: str
    status: str
    title: str
    url: str
    elsewhere: str

    @property
    def reason(self) -> str:
        # The wording ``guide_review._decide`` writes, so both paths read alike in the panel.
        return f"地點不符：內容講的是{self.elsewhere}，這個景點在{self.city}（{self.country}）"

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["guide_id"] = str(self.guide_id)
        data["hotspot_id"] = str(self.hotspot_id)
        data["reason"] = self.reason
        return data


@dataclass
class ScanReport:
    scanned: int = 0
    findings: list[Finding] = field(default_factory=list)
    #: Rows named with ``--reject-id`` that exist and are not rejected yet: (id, status, title).
    named: list[tuple[UUID, str, str]] = field(default_factory=list)
    already_rejected: list[UUID] = field(default_factory=list)
    missing: list[UUID] = field(default_factory=list)
    skipped: int = 0
    applied: bool = False
    rejected: int = 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "scanned": self.scanned,
            "findings": [finding.as_dict() for finding in self.findings],
            "named": [
                {"guide_id": str(guide_id), "status": status, "title": title}
                for guide_id, status, title in self.named
            ],
            "already_rejected": [str(guide_id) for guide_id in self.already_rejected],
            "missing": [str(guide_id) for guide_id in self.missing],
            "skipped": self.skipped,
            "applied": self.applied,
            "rejected": self.rejected,
        }


def guides_statement(
    *,
    statuses: Sequence[str] | None = ("approved",),
    locales: Sequence[str] = (),
    ids: Iterable[UUID] | None = None,
) -> Select[tuple[HotspotGuide, TravelHotspot]]:
    statement = select(HotspotGuide, TravelHotspot).join(
        TravelHotspot, TravelHotspot.id == HotspotGuide.hotspot_id
    )
    if statuses:
        statement = statement.where(HotspotGuide.review_status.in_(tuple(statuses)))
    if locales:
        statement = statement.where(HotspotGuide.locale.in_(tuple(locales)))
    if ids is not None:
        statement = statement.where(HotspotGuide.id.in_(tuple(ids)))
    return statement.order_by(TravelHotspot.name, HotspotGuide.locale, HotspotGuide.title)


async def _rows(
    session: AsyncSession, statement: Select[tuple[HotspotGuide, TravelHotspot]]
) -> list[tuple[HotspotGuide, TravelHotspot]]:
    return [(guide, hotspot) for guide, hotspot in (await session.execute(statement)).all()]


async def _own_terms(
    session: AsyncSession,
    hotspot: TravelHotspot,
    locale: str,
    cache: dict[tuple[UUID, str], list[str]],
) -> list[str]:
    """The names this attraction is searched with in ``locale``: the same list the review uses."""
    key = (hotspot.id, locale)
    if key not in cache:
        terms: list[Any] = [hotspot.name]
        if locale in LOCALES:
            context = await _localized_context(session, hotspot, locale)
            terms = [context["name"], *(context["aliases"] or []), *(context["search_terms"] or [])]
        cache[key] = [str(term) for term in terms if term]
    return cache[key]


async def scan_guides(
    session: AsyncSession,
    *,
    statuses: Sequence[str] = ("approved",),
    locales: Sequence[str] = (),
    skip: Iterable[UUID] = (),
    limit: int | None = None,
) -> ScanReport:
    """Read the selected rows and list the ones that are about another country."""
    report = ScanReport()
    skipped_ids = set(skip)
    rows = await _rows(session, guides_statement(statuses=statuses, locales=locales))
    if limit is not None:
        rows = rows[:limit]
    report.scanned = len(rows)
    cache: dict[tuple[UUID, str], list[str]] = {}
    for guide, hotspot in rows:
        if guide.id in skipped_ids:
            report.skipped += 1
            continue
        terms = await _own_terms(session, hotspot, guide.locale, cache)
        elsewhere = foreign_place(f"{guide.title} {guide.summary or ''}", hotspot, own_terms=terms)
        if not elsewhere:
            continue
        report.findings.append(
            Finding(
                guide_id=guide.id,
                hotspot_id=hotspot.id,
                hotspot_name=hotspot.name,
                city=hotspot.city_name,
                country=hotspot.country_name,
                destination_id=hotspot.destination_id,
                locale=guide.locale,
                content_type=guide.content_type,
                status=guide.review_status,
                title=guide.title,
                url=guide.canonical_url,
                elsewhere=elsewhere,
            )
        )
    return report


def reject_guides(
    decisions: Iterable[tuple[HotspotGuide, str]], *, actor_id: UUID, now: datetime | None = None
) -> AdminAuditLog:
    """Reject each ``(row, reason)`` the way the admin endpoint does; returns the audit entry.

    The caller adds the entry to the session and commits, so a dry run never touches this.
    """
    moment = now or datetime.now(UTC)
    ids: list[str] = []
    for guide, reason in decisions:
        guide.review_status = "rejected"
        guide.review_reason = reason
        guide.reviewed_at = moment
        guide.reviewed_by_user_id = actor_id
        ids.append(str(guide.id))
    return AdminAuditLog(
        actor_user_id=actor_id,
        action="hotspot_guides_reviewed",
        target=f"hotspot-guides:{len(ids)}",
        metadata_json={"action": "reject", "ids": ids, "locale": None, "source": SOURCE},
    )


async def run(
    session: AsyncSession,
    *,
    statuses: Sequence[str] = ("approved",),
    locales: Sequence[str] = (),
    skip: Iterable[UUID] = (),
    reject: Iterable[UUID] = (),
    limit: int | None = None,
    actor_id: UUID | None = None,
    reason: str = DEFAULT_REASON,
) -> ScanReport:
    """Scan, add the explicitly named rows, and reject everything when ``actor_id`` is given.

    Without an actor nothing is written and nothing is committed.
    """
    report = await scan_guides(session, statuses=statuses, locales=locales, skip=skip, limit=limit)
    wanted = list(dict.fromkeys(reject))
    named_rows: list[HotspotGuide] = []
    if wanted:
        found = {
            guide.id: guide
            for guide, _hotspot in await _rows(session, guides_statement(statuses=None, ids=wanted))
        }
        flagged = {finding.guide_id for finding in report.findings}
        for guide_id in wanted:
            guide = found.get(guide_id)
            if guide is None:
                report.missing.append(guide_id)
            elif guide.review_status == "rejected":
                report.already_rejected.append(guide_id)
            elif guide_id not in flagged:
                named_rows.append(guide)
                report.named.append((guide.id, guide.review_status, guide.title))
    if actor_id is None:
        return report
    by_id = (
        {
            guide.id: guide
            for guide, _hotspot in await _rows(
                session,
                guides_statement(
                    statuses=None, ids=[finding.guide_id for finding in report.findings]
                ),
            )
        }
        if report.findings
        else {}
    )
    decisions: list[tuple[HotspotGuide, str]] = [
        (by_id[finding.guide_id], finding.reason)
        for finding in report.findings
        if finding.guide_id in by_id
    ]
    decisions.extend((guide, reason) for guide in named_rows)
    if decisions:
        session.add(reject_guides(decisions, actor_id=actor_id))
        await session.commit()
    report.applied = True
    report.rejected = len(decisions)
    return report
