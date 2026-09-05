"""Bulk Google Place ID matching for seeded food merchants, driven from ``python -m app.cli``.

Merchants are seeded deliberately unpublishable: no Place ID, no coordinates,
``map_match_status='unverified'``, ``review_status='pending'``, ``is_active=False``. This
module fills in only the first of those, so an administrator opens each row with a
candidate already attached instead of searching for it by hand.

It writes **only** ``google_place_id``. It never writes coordinates and never advances
``map_match_status``: publication additionally requires a durable non-Google coordinate
source, and Google's Places coordinates are licensed for comparison rather than storage.
Deciding that a Place ID is the right *branch* of a chain stays a human judgement.

Korea is skipped outright. ``has_exact_map_identity`` demands a
``map.naver.com/p/entry/place/…`` URL for KR merchants, and nothing in this repository can
produce one, so a Place ID there would add noise without moving a row closer to publishable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.hotspots.places import automatic_refresh_allowed
from app.locations.google_match import preview_google_place_match
from app.models import AdminAuditLog, FoodMerchant

SKIPPED_COUNTRIES = frozenset({"KR"})


@dataclass(frozen=True)
class MerchantMatchReport:
    slug: str
    name: str
    outcome: str
    place_id: str | None = None
    candidate: dict[str, Any] | None = None


async def unmatched_merchants(
    session: AsyncSession,
    *,
    destination_ids: tuple[str, ...] = (),
    limit: int | None = None,
) -> list[FoodMerchant]:
    """Merchants with no Place ID that an administrator could still publish."""

    query = (
        select(FoodMerchant)
        .where(
            FoodMerchant.google_place_id.is_(None),
            FoodMerchant.review_status != "rejected",
            FoodMerchant.country_code.notin_(tuple(SKIPPED_COUNTRIES)),
        )
        .order_by(FoodMerchant.destination_id, FoodMerchant.display_order, FoodMerchant.name)
    )
    if destination_ids:
        query = query.where(
            FoodMerchant.destination_id.in_([item.casefold() for item in destination_ids])
        )
    if limit:
        query = query.limit(limit)
    return list((await session.scalars(query)).all())


def search_query(merchant: FoodMerchant) -> str:
    """Name plus the endonym plus the city, which is what disambiguates a chain branch."""

    parts = [merchant.name]
    if merchant.local_name and merchant.local_name != merchant.name:
        parts.append(merchant.local_name)
    if merchant.address:
        parts.append(merchant.address)
    else:
        parts.append(merchant.destination_id.replace("-", " "))
    return " ".join(part for part in parts if part).strip()


async def match_merchant_places(
    session: AsyncSession,
    redis: Redis,
    settings: Settings,
    merchants: list[FoodMerchant],
    *,
    apply: bool = False,
) -> list[MerchantMatchReport]:
    """Attach a Place ID to each merchant, committing after each row.

    Stops at the first row the Google usage guard refuses, so a long batch cannot push
    the month past the free tier.
    """

    reports: list[MerchantMatchReport] = []
    for merchant in merchants:
        slug, name = merchant.slug, merchant.name
        if merchant.google_place_id:
            reports.append(MerchantMatchReport(slug, name, "already_matched"))
            continue
        if not await automatic_refresh_allowed(redis, settings):
            reports.append(MerchantMatchReport(slug, name, "usage_guard"))
            break
        try:
            preview = await preview_google_place_match(
                session,
                redis,
                query=search_query(merchant),
                country_code=merchant.country_code,
            )
        except Exception as exc:  # one bad row must not stop the batch
            await session.rollback()
            reports.append(
                MerchantMatchReport(slug, name, "failed", None, {"error": type(exc).__name__})
            )
            continue
        if not preview.get("configured"):
            reports.append(MerchantMatchReport(slug, name, "not_configured"))
            break
        candidates = preview.get("candidates") or []
        if not candidates:
            reports.append(MerchantMatchReport(slug, name, "no_candidate"))
            continue
        candidate = dict(candidates[0])
        place_id = str(candidate.get("place_id") or "")
        if not place_id:
            reports.append(MerchantMatchReport(slug, name, "no_candidate"))
            continue
        # google_place_id is UNIQUE: assigning one another row owns aborts the whole
        # transaction, so check before writing rather than catching the IntegrityError.
        owner = await session.scalar(
            select(FoodMerchant.slug).where(
                FoodMerchant.google_place_id == place_id, FoodMerchant.id != merchant.id
            )
        )
        if owner is not None:
            taken = {**candidate, "owner": owner}
            reports.append(MerchantMatchReport(slug, name, "duplicate", place_id, taken))
            continue
        if not apply:
            reports.append(MerchantMatchReport(slug, name, "would_match", place_id, candidate))
            continue
        merchant.google_place_id = place_id
        session.add(
            AdminAuditLog(
                actor_user_id=None,
                action="food_merchant.cli_place_matched",
                target=f"food_merchant:{merchant.id}",
                metadata_json={
                    "source": "cli",
                    "slug": slug,
                    "place_id": place_id,
                    "candidate_name": candidate.get("name"),
                },
            )
        )
        await session.commit()
        reports.append(MerchantMatchReport(slug, name, "matched", place_id, candidate))
    return reports


def summarize(reports: list[MerchantMatchReport]) -> dict[str, Any]:
    outcomes: dict[str, int] = {}
    for report in reports:
        outcomes[report.outcome] = outcomes.get(report.outcome, 0) + 1
    return {
        "processed": len(reports),
        "outcomes": outcomes,
        "rows": [
            {
                "slug": report.slug,
                "name": report.name,
                "outcome": report.outcome,
                "place_id": report.place_id,
                "candidate": (report.candidate or {}).get("name"),
                "address": (report.candidate or {}).get("address"),
            }
            for report in reports
        ],
    }
