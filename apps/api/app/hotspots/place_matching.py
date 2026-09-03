"""Bulk Google Place ID matching for curated hotspots, driven from ``python -m app.cli``.

The admin UI runs the same enrichment through RQ; this module gives an operator a
synchronous path for a bounded set of hotspots (a freshly seeded destination, a slug
prefix) plus a way to promote a pending candidate without a browser session. Every
write still goes through ``enrich_hotspot_place`` so the Google usage meter, the
30-day cache policy and the Place-ID-only persistence rule live in one place.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

import httpx
from redis.asyncio import Redis
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.db import escape_like
from app.hotspots.places import (
    PUBLIC_HOTSPOT_STATUSES,
    automatic_refresh_allowed,
    enrich_hotspot_place,
)
from app.models import AdminAuditLog, HotspotPlaceProfile, TravelHotspot


@dataclass(frozen=True)
class MatchReport:
    slug: str
    name: str
    outcome: str
    calls: int = 0
    candidate: dict[str, Any] | None = None


async def missing_place_targets(
    session: AsyncSession,
    *,
    destination_ids: tuple[str, ...] = (),
    slug_prefix: str | None = None,
    limit: int | None = None,
) -> list[TravelHotspot]:
    """Public hotspots that still have no Google Place ID and were not rejected."""

    query = (
        select(TravelHotspot)
        .outerjoin(HotspotPlaceProfile, HotspotPlaceProfile.hotspot_id == TravelHotspot.id)
        .where(
            TravelHotspot.is_active.is_(True),
            TravelHotspot.review_status.in_(PUBLIC_HOTSPOT_STATUSES),
            TravelHotspot.google_place_id.is_(None),
            or_(
                HotspotPlaceProfile.id.is_(None),
                HotspotPlaceProfile.match_status != "rejected",
            ),
        )
        .order_by(TravelHotspot.destination_id, TravelHotspot.name)
    )
    if destination_ids:
        query = query.where(
            TravelHotspot.destination_id.in_([item.casefold() for item in destination_ids])
        )
    if slug_prefix:
        query = query.where(
            TravelHotspot.slug.like(f"{escape_like(slug_prefix.casefold())}%", escape="\\")
        )
    if limit:
        query = query.limit(limit)
    return list((await session.scalars(query)).all())


def candidate_payload(profile: HotspotPlaceProfile | None) -> dict[str, Any] | None:
    if profile is None or not profile.candidate_place_id:
        return None
    return {
        "place_id": profile.candidate_place_id,
        "name": profile.candidate_name,
        "address": profile.candidate_address,
        "confidence": (
            float(profile.match_confidence) if profile.match_confidence is not None else None
        ),
    }


async def _profile(session: AsyncSession, hotspot_id: UUID) -> HotspotPlaceProfile | None:
    profile: HotspotPlaceProfile | None = await session.scalar(
        select(HotspotPlaceProfile).where(HotspotPlaceProfile.hotspot_id == hotspot_id)
    )
    return profile


async def match_missing_places(
    session: AsyncSession,
    redis: Redis,
    settings: Settings,
    hotspots: list[TravelHotspot],
    *,
    now: datetime | None = None,
    client: httpx.AsyncClient | None = None,
) -> list[MatchReport]:
    """Run the automatic matcher over ``hotspots``, committing after each row.

    Stops at the first row the Google usage guard refuses so a long batch cannot push
    the month past the free tier; the remaining rows are simply not reported.
    """

    reports: list[MatchReport] = []
    for hotspot in hotspots:
        hotspot_id, slug, name = hotspot.id, hotspot.slug, hotspot.name
        if hotspot.google_place_id:
            reports.append(MatchReport(slug, name, "already_matched"))
            continue
        if not await automatic_refresh_allowed(redis, settings):
            reports.append(MatchReport(slug, name, "usage_guard"))
            break
        try:
            outcome, calls = await enrich_hotspot_place(
                session, redis, settings, hotspot, now=now, client=client
            )
        except Exception as exc:  # one bad row must not stop the batch
            await session.rollback()
            reports.append(MatchReport(slug, name, "failed", 0, {"error": type(exc).__name__}))
            continue
        await session.commit()
        candidate = None
        if outcome == "pending":
            candidate = candidate_payload(await _profile(session, hotspot_id))
        reports.append(MatchReport(slug, name, outcome, calls, candidate))
    return reports


async def approve_pending_candidate(
    session: AsyncSession,
    redis: Redis,
    settings: Settings,
    hotspot: TravelHotspot,
    *,
    now: datetime | None = None,
    client: httpx.AsyncClient | None = None,
) -> MatchReport:
    """Promote the stored candidate to the hotspot's Place ID, then fetch its details."""

    observed_at = now or datetime.now(UTC)
    hotspot_id, slug, name = hotspot.id, hotspot.slug, hotspot.name
    if hotspot.google_place_id:
        return MatchReport(slug, name, "already_matched")
    profile = await _profile(session, hotspot_id)
    candidate = candidate_payload(profile)
    if profile is None or candidate is None:
        return MatchReport(slug, name, "no_candidate")
    place_id = str(candidate["place_id"])
    owner = await session.scalar(
        select(TravelHotspot.id).where(
            TravelHotspot.google_place_id == place_id, TravelHotspot.id != hotspot_id
        )
    )
    if owner is not None:
        return MatchReport(slug, name, "duplicate", 0, {**candidate, "owner": str(owner)})
    hotspot.google_place_id = place_id
    if hotspot.country_code.upper() != "KR":
        hotspot.map_match_status = "verified"
        hotspot.map_verified_at = observed_at
    profile.place_id_source = "manual"
    profile.match_status = "approved"
    profile.reviewed_at = observed_at
    profile.review_reason = "cli_approved"
    session.add(
        AdminAuditLog(
            actor_user_id=None,
            action="hotspot_place_profile.cli_approved",
            target=f"hotspot:{hotspot_id}",
            metadata_json={
                "source": "cli",
                "slug": slug,
                "place_id": place_id,
                "candidate_name": candidate.get("name"),
            },
        )
    )
    outcome, calls = await enrich_hotspot_place(
        session, redis, settings, hotspot, now=observed_at, client=client
    )
    await session.commit()
    return MatchReport(slug, name, outcome, calls, candidate)
