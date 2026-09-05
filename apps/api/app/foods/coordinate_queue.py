"""Batch queue that turns Google-corroborated merchant locations into admin-verified ones.

The catalogue refuses provider coordinates as a durable source — a Places result may be
cached for at most thirty days, so ``google_places`` can never satisfy the publication
gate. What a provider result CAN do is stand next to the merchant we imported so a human
can compare the two. This module renders that comparison a page at a time and, on
approval, records the human's judgement as ``admin_verified`` with the public Google Maps
page as the auditable source URL.

The approve path never trusts coordinates from the browser: it re-resolves the merchant
server-side (a Redis-cached repeat of the query the queue page just ran, so no extra
quota) and refuses to write when Google no longer returns the place the admin looked at.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, cast
from uuid import UUID

from redis.exceptions import RedisError
from sqlalchemy import Select, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.hotspots.candidates import NAME_THRESHOLD, name_score
from app.hotspots.discovery import haversine_km
from app.hotspots.maps import has_exact_map_identity, is_exact_naver_map_url
from app.locations.coordinates import (
    DURABLE_COORDINATE_SOURCES,
    has_durable_coordinates,
    valid_coordinate_pair,
)
from app.models import FoodMerchant
from app.places.google import GoogleTravelService

# A merchant that already has coordinates counts as agreeing with Google only when the
# two positions are this close — the same drift bound the hotspot pipeline uses.
MAX_DRIFT_KM = 1.0
# The provider cache only stores answers Google actually gave, so a merchant it cannot
# resolve would re-bill a Pro search on every page render while sitting in the queue
# forever. Remember the emptiness ourselves for a day instead.
NO_RESULT_TTL_SECONDS = 86_400


def _no_result_key(merchant_id: UUID) -> str:
    return f"foods:coordinate_queue:no_result:{merchant_id}"


async def resolve_merchant(
    google: GoogleTravelService, merchant: FoodMerchant
) -> CandidateMatch | None:
    """One negative-cached Google lookup; both the queue page and approval go through it."""
    key = _no_result_key(merchant.id)
    try:
        if await google.redis.exists(key):
            return None
    except RedisError:
        pass  # the negative cache is an optimisation, never a gate
    place = await google.search_place(
        merchant_search_query(merchant),
        float(merchant.latitude) if merchant.latitude is not None else None,
        float(merchant.longitude) if merchant.longitude is not None else None,
        detailed=False,
        region_code=merchant.country_code,
    )
    match = extract_match(place) if place else None
    if match is None:
        try:
            await google.redis.set(key, "1", ex=NO_RESULT_TTL_SECONDS)
        except RedisError:
            pass
    return match


@dataclass(frozen=True)
class CandidateMatch:
    place_id: str
    name: str
    address: str | None
    google_maps_url: str | None
    latitude: float
    longitude: float


@dataclass(frozen=True)
class QueueSignals:
    name_score: float
    distance_km: float | None
    place_id_taken: bool
    verdict: str  # "agree" | "check"


def merchant_search_query(merchant: FoodMerchant) -> str:
    """The same query shape the corroboration dry-run used, so cache entries are shared."""
    parts = (merchant.local_name or merchant.name, merchant.address, merchant.destination_id)
    return " ".join(part for part in parts if part)


def extract_match(place: dict[str, Any]) -> CandidateMatch | None:
    place_id = str(place.get("id") or "")
    location = cast(dict[str, Any], place.get("location") or {})
    latitude, longitude = location.get("latitude"), location.get("longitude")
    if not place_id or latitude is None or longitude is None:
        return None
    if len(place_id) > 255:
        # Would overflow the column; treat as unusable rather than truncate an id.
        return None
    display = cast(dict[str, Any], place.get("displayName") or {})
    maps_url = str(place.get("googleMapsUri") or "")
    if len(maps_url) > 2048:
        maps_url = ""  # fall back to the place-id URL, which always fits
    return CandidateMatch(
        place_id=place_id,
        name=str(display.get("text") or ""),
        address=cast(str | None, place.get("formattedAddress")),
        google_maps_url=maps_url if maps_url.startswith("https://") else None,
        latitude=float(latitude),
        longitude=float(longitude),
    )


def judge(merchant: FoodMerchant, match: CandidateMatch, *, place_id_taken: bool) -> QueueSignals:
    score = max(
        name_score(merchant.name, match.name),
        name_score(merchant.local_name or "", match.name),
    )
    distance: float | None = None
    if merchant.latitude is not None and merchant.longitude is not None:
        distance = round(
            haversine_km(
                float(merchant.latitude), float(merchant.longitude), match.latitude, match.longitude
            ),
            3,
        )
    agree = (
        score >= NAME_THRESHOLD
        and not place_id_taken
        and (distance is None or distance <= MAX_DRIFT_KM)
    )
    return QueueSignals(
        name_score=round(score, 2),
        distance_km=distance,
        place_id_taken=place_id_taken,
        verdict="agree" if agree else "check",
    )


def lacks_durable_coordinates_clause() -> Any:
    # Mirrors is_durable_coordinate_source: the publication gate also demands an https
    # source URL, so a row with a durable type but no citable URL still belongs here.
    return or_(
        FoodMerchant.latitude.is_(None),
        FoodMerchant.coordinate_source_type.is_(None),
        FoodMerchant.coordinate_source_type.not_in(sorted(DURABLE_COORDINATE_SOURCES)),
        FoodMerchant.coordinate_source_url.is_(None),
        FoodMerchant.coordinate_source_url.not_like("https://%"),
    )


def coordinate_queue_statement() -> Select[tuple[FoodMerchant]]:
    return (
        select(FoodMerchant)
        .where(
            FoodMerchant.review_status.not_in(("rejected", "disabled")),
            # An admin who marked a match ambiguous or disabled made a deliberate call;
            # batch approval must not quietly overturn it.
            FoodMerchant.map_match_status.not_in(("ambiguous", "disabled")),
            lacks_durable_coordinates_clause(),
        )
        .order_by(
            FoodMerchant.country_code,
            FoodMerchant.destination_id,
            FoodMerchant.name,
            # Unique tiebreaker so pagination never skips or repeats rows when
            # several merchants share a name.
            FoodMerchant.id,
        )
    )


async def taken_place_ids(session: AsyncSession, place_ids: list[str]) -> dict[str, UUID]:
    """place_id -> merchant that already owns it, for conflict flags."""
    if not place_ids:
        return {}
    rows = await session.execute(
        select(FoodMerchant.google_place_id, FoodMerchant.id).where(
            FoodMerchant.google_place_id.in_(place_ids)
        )
    )
    return {str(place_id): merchant_id for place_id, merchant_id in rows if place_id}


async def resolve_queue_page(
    session: AsyncSession,
    google: GoogleTravelService,
    merchants: list[FoodMerchant],
) -> list[dict[str, Any]]:
    matches: list[tuple[FoodMerchant, CandidateMatch | None]] = []
    for merchant in merchants:
        matches.append((merchant, await resolve_merchant(google, merchant)))

    owners = await taken_place_ids(
        session, [match.place_id for _, match in matches if match is not None]
    )
    items: list[dict[str, Any]] = []
    for merchant, match in matches:
        entry: dict[str, Any] = {
            "merchant": {
                "id": str(merchant.id),
                "slug": merchant.slug,
                "name": merchant.name,
                "local_name": merchant.local_name,
                "address": merchant.address,
                "destination_id": merchant.destination_id,
                "country_code": merchant.country_code,
                "latitude": float(merchant.latitude) if merchant.latitude is not None else None,
                "longitude": float(merchant.longitude) if merchant.longitude is not None else None,
                "map_match_status": merchant.map_match_status,
                "review_status": merchant.review_status,
                # The gate demands an exact Naver place page, not just any Naver link.
                "needs_naver_url": merchant.country_code.upper() == "KR"
                and not is_exact_naver_map_url(merchant.naver_map_url),
            },
        }
        if match is None:
            entry["candidate"] = None
            entry["signals"] = {"verdict": "no_result"}
        else:
            taken_by = owners.get(match.place_id)
            taken = taken_by is not None and taken_by != merchant.id
            signals = judge(merchant, match, place_id_taken=taken)
            entry["candidate"] = {
                "place_id": match.place_id,
                "name": match.name,
                "address": match.address,
                "google_maps_url": match.google_maps_url,
                "latitude": match.latitude,
                "longitude": match.longitude,
            }
            entry["signals"] = {
                "verdict": signals.verdict,
                "name_score": signals.name_score,
                "distance_km": signals.distance_km,
                "place_id_taken": signals.place_id_taken,
            }
        items.append(entry)
    return items


async def queue_total(session: AsyncSession) -> int:
    return int(
        await session.scalar(
            select(func.count()).select_from(coordinate_queue_statement().subquery())
        )
        or 0
    )


async def apply_approval(
    session: AsyncSession,
    google: GoogleTravelService,
    merchant: FoodMerchant,
    *,
    expected_place_id: str,
    actor_id: UUID,
    now: datetime | None = None,
) -> str:
    """Re-resolve one merchant and write the admin's verdict. Returns an outcome tag."""
    if merchant.review_status in ("rejected", "disabled") or merchant.map_match_status in (
        "ambiguous",
        "disabled",
    ):
        # The queue never lists these; a stale browser tab could still submit one.
        return "not_eligible"
    if has_durable_coordinates(
        merchant.latitude,
        merchant.longitude,
        merchant.coordinate_source_type,
        merchant.coordinate_source_url,
    ):
        return "already_durable"
    match = await resolve_merchant(google, merchant)
    if match is None:
        return "no_result"
    if not valid_coordinate_pair(match.latitude, match.longitude):
        return "no_result"
    if match.place_id != expected_place_id:
        # Google now resolves the query to a different place than the one the admin saw;
        # writing anyway would verify a location no human looked at.
        return "candidate_changed"
    owners = await taken_place_ids(session, [match.place_id])
    taken_by = owners.get(match.place_id)
    if taken_by is not None and taken_by != merchant.id:
        return "place_id_taken"

    moment = now or datetime.now(UTC)
    merchant.latitude = match.latitude  # type: ignore[assignment]
    merchant.longitude = match.longitude  # type: ignore[assignment]
    merchant.google_place_id = match.place_id
    merchant.coordinate_source_type = "admin_verified"
    merchant.coordinate_source_url = match.google_maps_url or (
        f"https://www.google.com/maps/place/?q=place_id:{match.place_id}"
    )
    merchant.coordinate_verified_at = moment
    if has_exact_map_identity(
        merchant.country_code, merchant.google_place_id, merchant.naver_map_url
    ):
        merchant.map_match_status = "verified"
        merchant.verified_at = moment
        merchant.verified_by_user_id = actor_id
        return "verified"
    # KR without a Naver page: the coordinates are now durable but publication still
    # waits on the exact-map-identity requirement.
    return "coordinates_saved"
