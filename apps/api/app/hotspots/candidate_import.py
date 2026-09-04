"""Persist resolved candidates, or explain why a row was left alone.

Rows are keyed by Wikidata id and share the ``wikidata-<qid>`` slug the Wikimedia
collector already uses, so a place found by both routes converges on one row instead of
becoming a duplicate.

``google_place_id`` carries a unique constraint. Assigning one that another hotspot
already owns aborts the whole transaction, so a taken id is reported rather than written
- the same reason the place matcher parks that case for a human.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.hotspots.areas import resolve_area_code
from app.hotspots.candidates import CandidateResolution
from app.hotspots.cities import CITY_BY_CODE
from app.models import TravelHotspot

# Rows this pipeline writes, so they can be told apart from curated seeds and from the
# Wikimedia collector's own finds when auditing where a hotspot came from.
CANDIDATE_ORIGIN = "candidate_import"


async def _place_id_owner(
    session: AsyncSession, place_id: str, hotspot_id: Any | None
) -> Any | None:
    statement = select(TravelHotspot.id).where(TravelHotspot.google_place_id == place_id)
    if hotspot_id is not None:
        statement = statement.where(TravelHotspot.id != hotspot_id)
    return await session.scalar(statement)


async def persist_resolutions(
    session: AsyncSession,
    resolutions: list[CandidateResolution],
    *,
    now: datetime,
    apply: bool = False,
) -> dict[str, int]:
    counts: dict[str, int] = {}

    def tally(key: str) -> None:
        counts[key] = counts.get(key, 0) + 1

    for resolution in resolutions:
        if resolution.lane == "rejected" or resolution.article is None:
            tally(f"skipped:{resolution.reason}")
            continue
        city = CITY_BY_CODE.get(resolution.candidate.city_code)
        if city is None:
            tally("skipped:unknown_city_code")
            continue

        article = resolution.article
        hotspot = await session.scalar(
            select(TravelHotspot).where(TravelHotspot.wikidata_item_id == article.qid)
        )
        if hotspot is not None and hotspot.review_status in {"rejected", "disabled"}:
            tally("skipped:previously_rejected")
            continue
        if hotspot is not None and hotspot.map_match_status == "verified":
            tally("skipped:already_verified")
            continue

        place_id = resolution.google_place_id
        if place_id and await _place_id_owner(session, place_id, getattr(hotspot, "id", None)):
            # Another hotspot already owns this place; writing it would abort the batch.
            tally("skipped:place_id_taken")
            continue

        created = hotspot is None
        if not apply:
            tally(f"would_{'create' if created else 'update'}:{resolution.lane}")
            continue

        if hotspot is None:
            hotspot = TravelHotspot(
                slug=f"wikidata-{article.qid.lower()}",
                wikidata_item_id=article.qid,
                discovered_at=now,
            )
            session.add(hotspot)
        hotspot.name = resolution.candidate.name
        hotspot.destination_id = city.id
        hotspot.city_code = city.code
        hotspot.city_name = city.name
        hotspot.country_code = city.country_code
        hotspot.country_name = city.country_name
        hotspot.category = resolution.category
        hotspot.search_text = f"{resolution.candidate.name} {article.title} {city.name}".casefold()
        hotspot.latitude = Decimal(str(article.latitude))
        hotspot.longitude = Decimal(str(article.longitude))
        hotspot.area_code = resolve_area_code(city.code, article.latitude, article.longitude)
        # The point comes from the article, so the article is what gets cited.
        hotspot.coordinate_source_type = "curated"
        hotspot.coordinate_source_url = article.article_url
        hotspot.coordinate_verified_at = now
        hotspot.wikipedia_project = article.wikipedia_project
        hotspot.wikipedia_title = article.title
        hotspot.google_place_id = place_id
        hotspot.origin = CANDIDATE_ORIGIN
        hotspot.last_seen_at = now
        if resolution.lane == "confirmed":
            hotspot.review_status = "approved"
            hotspot.review_reason = None
            hotspot.map_match_status = "verified"
            hotspot.map_verified_at = now
        else:
            hotspot.review_status = "pending"
            hotspot.review_reason = resolution.reason
            hotspot.map_match_status = "unverified"
            hotspot.map_verified_at = None
        tally(f"{'created' if created else 'updated'}:{resolution.lane}")

    if apply:
        await session.commit()
    return counts
