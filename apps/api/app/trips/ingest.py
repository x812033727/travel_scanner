"""Turning what a traveller pasted into candidates for a trip.

Each line is one place: a Google Maps link (short or long), a bare Place ID, or a name
somebody typed. Links are expanded and read by ``resolve_maps_input``, which already
knows the fifteen Google hosts and refuses everything else, so a paste cannot make the
server fetch an arbitrary address.

Nothing here spends a Places request. A resolved Place ID is looked up in our own hotspot
catalogue: a match brings the catalogue's names, coordinates and depth score with it, and
a miss is kept as the traveller's own text so they can still drop it into a day. Asking
Google to identify the rest would cost a paid lookup per line pasted.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.hotspots.service import load_hotspot_names
from app.localized_names import item_names
from app.models import TravelHotspot, TripPlaceCandidate
from app.problems import AppError
from app.restaurants.imports import resolve_maps_input

# One paste, not a data import: enough for a day's worth of links, small enough that the
# short-URL expansions behind it stay a handful of requests.
MAX_LINES_PER_PASTE = 30
# Per member per day, counted in Redis. Short-URL expansion is cheap but it is still an
# outbound request per line, and the inbox is a waiting list, not a database.
DAILY_PLACE_LIMIT = 100


@dataclass(frozen=True)
class ParsedLine:
    raw: str
    place_id: str | None
    maps_url: str | None
    query: str | None
    source: str


def split_lines(text: str) -> list[str]:
    """One place per line, blank lines dropped, order kept."""
    seen: set[str] = set()
    lines: list[str] = []
    for raw in text.replace("\r\n", "\n").split("\n"):
        line = raw.strip()
        if not line or line in seen:
            continue
        seen.add(line)
        lines.append(line)
    return lines


async def parse_line(line: str, *, client: httpx.AsyncClient | None = None) -> ParsedLine:
    """Read one pasted line without deciding anything about it."""
    if line.startswith("https://"):
        resolution = await resolve_maps_input(line, client=client)
        return ParsedLine(
            raw=line,
            place_id=resolution.place_id,
            maps_url=resolution.expanded_url,
            query=resolution.suggested_query,
            source="maps_url",
        )
    # A bare Place ID resolves without a network call; anything else is a name.
    try:
        resolution = await resolve_maps_input(line, client=client)
    except AppError:
        return ParsedLine(raw=line, place_id=None, maps_url=None, query=line, source="text")
    return ParsedLine(
        raw=line,
        place_id=resolution.place_id,
        maps_url=resolution.expanded_url,
        query=resolution.suggested_query,
        source="place_id",
    )


async def hotspots_by_place_id(
    session: AsyncSession, place_ids: list[str]
) -> dict[str, TravelHotspot]:
    if not place_ids:
        return {}
    rows = list(
        (
            await session.scalars(
                select(TravelHotspot).where(TravelHotspot.google_place_id.in_(place_ids))
            )
        ).all()
    )
    return {row.google_place_id: row for row in rows if row.google_place_id}


async def catalogue_names(
    session: AsyncSession, hotspots: list[TravelHotspot]
) -> dict[UUID, dict[str, str]]:
    """Five-locale names for the hotspots a paste matched."""
    return await load_hotspot_names(session, hotspots)


def candidate_from(
    trip_id: UUID,
    parsed: ParsedLine,
    hotspot: TravelHotspot | None,
    names: dict[str, str] | None = None,
) -> TripPlaceCandidate:
    """A row for the inbox: the catalogue's record when we have one, the paste when we do not."""
    if hotspot is not None:
        return TripPlaceCandidate(
            trip_plan_id=trip_id,
            hotspot_id=hotspot.id,
            raw_input=parsed.raw,
            source=parsed.source,
            title=hotspot.name,
            location_name=hotspot.city_name,
            google_place_id=parsed.place_id,
            maps_url=parsed.maps_url,
            latitude=hotspot.latitude,
            longitude=hotspot.longitude,
            names_json=item_names(title=names) if names else {},
            data={
                "matched": "hotspot",
                "hotspot_slug": hotspot.slug,
                "city_code": hotspot.city_code,
                "category": hotspot.category,
                "depth_score": float(hotspot.depth_score) if hotspot.depth_score else None,
            },
        )
    title = (parsed.query or parsed.raw).strip()[:255]
    return TripPlaceCandidate(
        trip_plan_id=trip_id,
        hotspot_id=None,
        raw_input=parsed.raw,
        source=parsed.source,
        title=title or parsed.raw[:255],
        location_name=None,
        google_place_id=parsed.place_id,
        maps_url=parsed.maps_url,
        latitude=None,
        longitude=None,
        names_json={},
        data={"matched": "none"},
    )


def serialize_candidate(candidate: TripPlaceCandidate) -> dict[str, object]:
    return {
        "id": str(candidate.id),
        "status": candidate.status,
        "source": candidate.source,
        "raw_input": candidate.raw_input,
        "title": candidate.title,
        "location_name": candidate.location_name,
        "google_place_id": candidate.google_place_id,
        "maps_url": candidate.maps_url,
        "latitude": float(candidate.latitude) if candidate.latitude is not None else None,
        "longitude": float(candidate.longitude) if candidate.longitude is not None else None,
        "hotspot_id": str(candidate.hotspot_id) if candidate.hotspot_id else None,
        "names": candidate.names_json or {},
        "data": candidate.data or {},
        "created_at": candidate.created_at.isoformat() if candidate.created_at else None,
    }
