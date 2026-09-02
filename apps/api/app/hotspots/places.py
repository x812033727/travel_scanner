from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from difflib import SequenceMatcher
from math import asin, cos, radians, sin, sqrt
from typing import Any, Literal, cast
from urllib.parse import urlparse
from uuid import UUID, uuid4

import httpx
from redis.asyncio import Redis
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.hotspots.guides import canonical_external_url
from app.hotspots.maps import build_map_links
from app.locations.coordinates import has_durable_coordinates
from app.models import HotspotPlaceEnrichmentRun, HotspotPlaceProfile, TravelHotspot
from app.places.google import GoogleTravelService
from app.problems import AppError
from app.providers.usage_meter import google_maps_usage_snapshot

PUBLIC_HOTSPOT_STATUSES = ("approved", "auto_approved")
BLOCKED_WEBSITE_HOSTS = {
    "airbnb.com",
    "agoda.com",
    "booking.com",
    "ctrip.com",
    "expedia.com",
    "facebook.com",
    "getyourguide.com",
    "google.com",
    "hotels.com",
    "instagram.com",
    "kkday.com",
    "klook.com",
    "linkedin.com",
    "maps.app.goo.gl",
    "tiktok.com",
    "trip.com",
    "tripadvisor.com",
    "traveloka.com",
    "twitter.com",
    "viator.com",
    "weibo.com",
    "x.com",
    "yelp.com",
    "youtube.com",
}
RunMode = Literal["missing_or_expired", "force"]


@dataclass(frozen=True)
class PlaceCandidateMatch:
    candidate: dict[str, Any] | None
    confidence: float
    auto_approved: bool
    evidence: dict[str, Any]


def _normalized_text(value: str | None) -> str:
    normalized = unicodedata.normalize("NFKC", value or "").casefold()
    return "".join(character for character in normalized if character.isalnum())


def _haversine_km(
    latitude_a: float | None,
    longitude_a: float | None,
    latitude_b: float | None,
    longitude_b: float | None,
) -> float | None:
    if None in (latitude_a, longitude_a, latitude_b, longitude_b):
        return None
    lat_a, lon_a, lat_b, lon_b = map(
        radians,
        cast(tuple[float, float, float, float], (latitude_a, longitude_a, latitude_b, longitude_b)),
    )
    delta_latitude = lat_b - lat_a
    delta_longitude = lon_b - lon_a
    value = sin(delta_latitude / 2) ** 2 + cos(lat_a) * cos(lat_b) * sin(
        delta_longitude / 2
    ) ** 2
    return round(6371.0088 * 2 * asin(sqrt(value)), 3)


def choose_place_candidate(
    hotspot: TravelHotspot, candidates: list[dict[str, Any]]
) -> PlaceCandidateMatch:
    aliases = [hotspot.name, str(hotspot.metadata_json.get("local_name") or "")]
    aliases.extend(str(item) for item in hotspot.metadata_json.get("aliases", []))
    normalized_aliases = {_normalized_text(item) for item in aliases if _normalized_text(item)}
    expected_city = _normalized_text(hotspot.city_name)
    expected_country = _normalized_text(hotspot.country_name)
    latitude = float(hotspot.latitude) if hotspot.latitude is not None else None
    longitude = float(hotspot.longitude) if hotspot.longitude is not None else None
    scored: list[tuple[float, dict[str, Any], dict[str, Any]]] = []

    for candidate in candidates:
        candidate_name = _normalized_text(str(candidate.get("name") or ""))
        address = _normalized_text(str(candidate.get("address") or ""))
        exact_name = candidate_name in normalized_aliases
        similarity = max(
            (SequenceMatcher(None, candidate_name, alias).ratio() for alias in normalized_aliases),
            default=0.0,
        )
        candidate_country_code = str(candidate.get("country_code") or "").upper()
        country_match = candidate_country_code == hotspot.country_code or bool(
            expected_country and expected_country in address
        )
        city_match = bool(expected_city and expected_city in address)
        distance_km = _haversine_km(
            latitude,
            longitude,
            _optional_float(candidate.get("latitude")),
            _optional_float(candidate.get("longitude")),
        )
        has_reference_coordinates = latitude is not None and longitude is not None
        exact_with_location = exact_name and country_match and (
            (distance_km is not None and distance_km <= 5.0)
            or (not has_reference_coordinates and city_match)
        )
        fuzzy_with_location = (
            similarity >= 0.90
            and country_match
            and city_match
            and distance_km is not None
            and distance_km <= 1.5
        )
        auto_approved = exact_with_location or fuzzy_with_location
        confidence = min(
            0.999,
            similarity * 0.70
            + (0.12 if country_match else 0)
            + (0.08 if city_match else 0)
            + (0.09 if distance_km is not None and distance_km <= 1.5 else 0),
        )
        evidence = {
            "exact_name": exact_name,
            "name_similarity": round(similarity, 4),
            "country_match": country_match,
            "city_match": city_match,
            "distance_km": distance_km,
            "auto_approved": auto_approved,
        }
        scored.append((confidence, candidate, evidence))

    if not scored:
        return PlaceCandidateMatch(None, 0.0, False, {"reason": "no_candidates"})
    confidence, candidate, evidence = max(scored, key=lambda item: item[0])
    return PlaceCandidateMatch(candidate, confidence, bool(evidence["auto_approved"]), evidence)


def _optional_float(value: object) -> float | None:
    if value is None:
        return None
    try:
        return float(cast(Any, value))
    except (TypeError, ValueError):
        return None


def canonical_official_website(value: str) -> str:
    try:
        canonical = canonical_external_url(value)
    except (AppError, ValueError) as exc:
        raise AppError(
            422,
            "hotspot_official_website_invalid",
            "官方網站必須是公開 HTTPS URL",
        ) from exc
    hostname = (urlparse(canonical).hostname or "").casefold()
    if any(
        hostname == blocked or hostname.endswith(f".{blocked}")
        for blocked in BLOCKED_WEBSITE_HOSTS
    ):
        raise AppError(422, "hotspot_official_website_not_official", "這個網址不是可核准的官方網站")
    return canonical


def _safe_provider_website(value: object) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return canonical_official_website(value)
    except AppError:
        return None


def _safe_google_maps_uri(value: object) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        canonical = canonical_external_url(value)
    except (AppError, ValueError):
        return None
    hostname = (urlparse(canonical).hostname or "").casefold()
    return canonical if hostname == "google.com" or hostname.endswith(".google.com") else None


def _normalized_attributions(value: object) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    normalized: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        provider = item.get("provider")
        if not isinstance(provider, str) or not provider.strip():
            continue
        attribution = {"provider": provider.strip()[:255]}
        provider_uri = item.get("providerUri")
        if isinstance(provider_uri, str):
            try:
                attribution["providerUri"] = canonical_external_url(provider_uri)
            except (AppError, ValueError):
                pass
        normalized.append(attribution)
    return normalized


def _decimal(value: object) -> Decimal | None:
    number = _optional_float(value)
    return Decimal(str(number)) if number is not None else None


def _profile_for(
    hotspot: TravelHotspot, profile: HotspotPlaceProfile | None
) -> HotspotPlaceProfile:
    if profile is not None:
        return profile
    return HotspotPlaceProfile(
        hotspot_id=hotspot.id,
        place_id_source="legacy" if hotspot.google_place_id else "none",
        match_status="approved" if hotspot.google_place_id else "unmatched",
    )


async def enrich_hotspot_place(
    session: AsyncSession,
    redis: Redis,
    settings: Settings,
    hotspot: TravelHotspot,
    *,
    now: datetime | None = None,
    client: httpx.AsyncClient | None = None,
) -> tuple[str, int]:
    observed_at = now or datetime.now(UTC)
    profile = await session.scalar(
        select(HotspotPlaceProfile).where(HotspotPlaceProfile.hotspot_id == hotspot.id)
    )
    profile = _profile_for(hotspot, profile)
    session.add(profile)
    rejected_provider_website = profile.website_review_status == "rejected"
    had_current_cache = bool(
        profile.provider_expires_at
        and profile.provider_expires_at > observed_at
        and profile.match_status in {"approved", "auto_approved"}
    )
    google = GoogleTravelService(redis, settings, client, locale="zh-TW")
    calls = 0
    place_id = hotspot.google_place_id

    if not place_id:
        local_name = str(hotspot.metadata_json.get("local_name") or "").strip()
        query = " ".join(
            part for part in (hotspot.name, local_name, hotspot.city_name) if part
        )
        candidates = await google.search_place_candidates(
            query,
            float(hotspot.latitude) if hotspot.latitude is not None else None,
            float(hotspot.longitude) if hotspot.longitude is not None else None,
            region_code=hotspot.country_code,
            limit=3,
        )
        calls += 1
        match = choose_place_candidate(hotspot, candidates)
        profile.match_confidence = Decimal(str(round(match.confidence, 4)))
        profile.match_evidence_json = match.evidence
        if match.candidate is None:
            profile.match_status = "unmatched"
            _clear_candidate(profile)
            return "unmatched", calls
        profile.provider_fetched_at = observed_at
        profile.provider_refresh_after = observed_at + timedelta(
            days=settings.hotspot_place_refresh_after_days
        )
        profile.provider_expires_at = observed_at + timedelta(
            days=settings.hotspot_place_cache_days
        )
        _set_candidate(profile, match.candidate)
        if not match.auto_approved:
            profile.match_status = "pending"
            return "pending", calls
        place_id = str(match.candidate["place_id"])
        hotspot.google_place_id = place_id
        if hotspot.country_code.upper() != "KR":
            hotspot.map_match_status = "verified"
            hotspot.map_verified_at = observed_at
        profile.place_id_source = "automatic"
        profile.match_status = "auto_approved"

    details = await google.place_details(place_id)
    calls += 1
    if not details:
        if not had_current_cache:
            profile.match_status = "failed"
        profile.match_evidence_json = {
            **(profile.match_evidence_json or {}),
            "details_error": "provider_unavailable_or_place_not_found",
        }
        return "failed", calls

    if profile.place_id_source == "none":
        profile.place_id_source = "legacy"
    if profile.match_status not in {"approved", "auto_approved"}:
        profile.match_status = (
            "approved" if profile.place_id_source != "automatic" else "auto_approved"
        )
    _clear_candidate(profile)
    profile.google_maps_uri = _safe_google_maps_uri(details.get("google_maps_url"))
    profile.formatted_address = cast(str | None, details.get("address"))
    profile.google_latitude = _decimal(details.get("latitude"))
    profile.google_longitude = _decimal(details.get("longitude"))
    profile.opening_hours_json = cast(
        dict[str, Any], details.get("opening_hours_structured") or {}
    )
    profile.provider_website_uri = cast(str | None, details.get("website_url"))
    profile.provider_locale = cast(str | None, details.get("data_locale")) or "zh-TW"
    profile.provider_attributions_json = _normalized_attributions(details.get("attributions"))
    if profile.manual_official_website_url:
        profile.website_review_status = "approved"
    elif rejected_provider_website:
        profile.website_review_status = "rejected"
    elif profile.provider_website_uri:
        profile.website_review_status = (
            "auto_approved" if _safe_provider_website(profile.provider_website_uri) else "pending"
        )
    else:
        profile.website_review_status = "none"
    profile.provider_fetched_at = observed_at
    profile.provider_refresh_after = observed_at + timedelta(
        days=settings.hotspot_place_refresh_after_days
    )
    profile.provider_expires_at = observed_at + timedelta(days=settings.hotspot_place_cache_days)
    return "published", calls


def _set_candidate(profile: HotspotPlaceProfile, candidate: dict[str, Any]) -> None:
    profile.candidate_place_id = cast(str | None, candidate.get("place_id"))
    profile.candidate_name = cast(str | None, candidate.get("name"))
    profile.candidate_address = cast(str | None, candidate.get("address"))
    profile.candidate_latitude = _decimal(candidate.get("latitude"))
    profile.candidate_longitude = _decimal(candidate.get("longitude"))


def _clear_candidate(profile: HotspotPlaceProfile) -> None:
    profile.candidate_place_id = None
    profile.candidate_name = None
    profile.candidate_address = None
    profile.candidate_latitude = None
    profile.candidate_longitude = None


def _current(profile: HotspotPlaceProfile | None, now: datetime) -> bool:
    return bool(profile and profile.provider_expires_at and profile.provider_expires_at > now)


def _exact_map_links(hotspot: TravelHotspot) -> list[dict[str, str | bool]]:
    return build_map_links(
        name=hotspot.name,
        local_name=cast(str | None, hotspot.metadata_json.get("local_name")),
        city_name=hotspot.city_name,
        country_code=hotspot.country_code,
        latitude=hotspot.latitude,
        longitude=hotspot.longitude,
        google_place_id=hotspot.google_place_id,
        naver_map_url=hotspot.naver_map_url,
        map_match_status=hotspot.map_match_status,
    )


def _map_url(hotspot: TravelHotspot) -> str | None:
    return next(
        (
            str(item["url"])
            for item in _exact_map_links(hotspot)
            if item["provider"] == "google"
        ),
        None,
    )


def place_status(
    profile: HotspotPlaceProfile | None,
    *,
    configured: bool,
    now: datetime,
) -> Literal["ready", "pending_review", "stale", "unavailable"]:
    if profile and (
        profile.match_status == "pending" or profile.website_review_status == "pending"
    ):
        return "pending_review"
    if _current(profile, now) and profile and profile.match_status in {"approved", "auto_approved"}:
        return "ready"
    if profile and profile.provider_expires_at is not None and profile.provider_expires_at <= now:
        return "stale"
    return "unavailable"


def place_summary_payload(
    hotspot: TravelHotspot,
    profile: HotspotPlaceProfile | None,
    *,
    configured: bool,
    now: datetime | None = None,
) -> dict[str, Any]:
    observed_at = now or datetime.now(UTC)
    current = bool(
        _current(profile, observed_at)
        and profile
        and profile.match_status in {"approved", "auto_approved"}
    )
    provider_website = (
        _safe_provider_website(profile.provider_website_uri)
        if current and profile and profile.website_review_status in {"approved", "auto_approved"}
        else None
    )
    official_website = (
        profile.manual_official_website_url if profile else None
    ) or provider_website
    return {
        "status": place_status(profile, configured=configured, now=observed_at),
        "google_maps_url": _map_url(hotspot),
        "map_links": _exact_map_links(hotspot),
        "official_website_url": official_website,
        "official_website_verified": bool(profile and profile.manual_official_website_url),
        "has_details": bool(
            current and profile and profile.match_status in {"approved", "auto_approved"}
        ),
        "updated_at": profile.provider_fetched_at if current and profile else None,
    }


def place_detail_payload(
    hotspot: TravelHotspot,
    profile: HotspotPlaceProfile | None,
    *,
    configured: bool,
    now: datetime | None = None,
) -> dict[str, Any]:
    observed_at = now or datetime.now(UTC)
    current = bool(
        _current(profile, observed_at)
        and profile
        and profile.match_status in {"approved", "auto_approved"}
    )
    summary = place_summary_payload(
        hotspot, profile, configured=configured, now=observed_at
    )
    durable_coordinates = has_durable_coordinates(
        hotspot.latitude,
        hotspot.longitude,
        hotspot.coordinate_source_type,
        hotspot.coordinate_source_url,
    )
    latitude: float | None = None
    longitude: float | None = None
    if durable_coordinates and hotspot.latitude is not None and hotspot.longitude is not None:
        latitude = float(hotspot.latitude)
        longitude = float(hotspot.longitude)
    coordinate_source = hotspot.coordinate_source_type if durable_coordinates else None
    website_source = None
    if profile and profile.manual_official_website_url:
        website_source = "manual_review"
    elif summary["official_website_url"]:
        website_source = "google_places_cache"
    return {
        "hotspot_id": str(hotspot.id),
        "hotspot_name": hotspot.name,
        **summary,
        "address": profile.formatted_address if current and profile else None,
        "coordinates": {
            "latitude": latitude,
            "longitude": longitude,
            "source": coordinate_source,
        },
        "opening_hours": profile.opening_hours_json if current and profile else {},
        "data_locale": profile.provider_locale if current and profile else None,
        "fetched_at": profile.provider_fetched_at if current and profile else None,
        "expires_at": profile.provider_expires_at if current and profile else None,
        "attribution": {
            "provider": "Google Maps" if current else None,
            "provider_url": "https://maps.google.com/" if current else None,
            "third_party": profile.provider_attributions_json if current and profile else [],
        },
        "field_sources": {
            "google_maps_url": (
                "google_place_id" if summary["google_maps_url"] else None
            ),
            "official_website_url": website_source,
            "address": (
                "google_places_cache"
                if current and profile and profile.formatted_address
                else None
            ),
            "coordinates": coordinate_source,
            "opening_hours": (
                "google_places_cache"
                if current and profile and profile.opening_hours_json
                else None
            ),
        },
    }


async def enrichment_targets(
    session: AsyncSession,
    *,
    mode: RunMode,
    country_code: str | None = None,
    hotspot_ids: list[UUID] | None = None,
    now: datetime | None = None,
) -> list[TravelHotspot]:
    observed_at = now or datetime.now(UTC)
    query = (
        select(TravelHotspot)
        .outerjoin(HotspotPlaceProfile, HotspotPlaceProfile.hotspot_id == TravelHotspot.id)
        .where(
            TravelHotspot.is_active.is_(True),
            TravelHotspot.review_status.in_(PUBLIC_HOTSPOT_STATUSES),
        )
    )
    if country_code:
        query = query.where(TravelHotspot.country_code == country_code.upper())
    if hotspot_ids:
        query = query.where(TravelHotspot.id.in_(hotspot_ids))
    if mode == "missing_or_expired":
        query = query.where(
            or_(
                HotspotPlaceProfile.id.is_(None),
                and_(
                    HotspotPlaceProfile.match_status != "rejected",
                    or_(
                        HotspotPlaceProfile.provider_expires_at.is_(None),
                        HotspotPlaceProfile.provider_expires_at <= observed_at,
                        HotspotPlaceProfile.match_status.in_(("unmatched", "failed")),
                    ),
                ),
            )
        )
    return list(
        (
            await session.scalars(
                query.order_by(TravelHotspot.country_code, TravelHotspot.name)
            )
        ).all()
    )


def run_payload(run: HotspotPlaceEnrichmentRun) -> dict[str, Any]:
    progress = round(run.processed_count / run.total_count * 100) if run.total_count else 100
    return {
        "run_id": str(run.id),
        "status": run.status,
        "mode": run.mode,
        "scope": run.scope_json,
        "progress": progress,
        "counts": {
            "total": run.total_count,
            "processed": run.processed_count,
            "published": run.published_count,
            "pending": run.pending_count,
            "unmatched": run.unmatched_count,
            "failed": run.failed_count,
        },
        "usage": {
            "estimated_google_calls": run.estimated_google_calls,
            "actual_google_calls": run.actual_google_calls,
        },
        "current": run.progress_json,
        "errors": run.error_json,
        "created_at": run.created_at,
        "started_at": run.started_at,
        "completed_at": run.completed_at,
    }


async def automatic_refresh_allowed(redis: Redis, settings: Settings) -> bool:
    usage = await google_maps_usage_snapshot(
        redis,
        essentials_free_limit=settings.google_maps_essentials_free_limit,
        pro_free_limit=settings.google_maps_pro_free_limit,
        enterprise_free_limit=settings.google_maps_enterprise_free_limit,
    )
    if not usage.available:
        return False
    relevant = {
        item.sku: item
        for item in usage.sku_usage
        if item.sku in {"place_details_enterprise", "text_search_pro"}
    }
    return all(item.percentage < 90 for item in relevant.values())


async def due_refresh_targets(
    session: AsyncSession, settings: Settings, *, now: datetime | None = None
) -> list[TravelHotspot]:
    observed_at = now or datetime.now(UTC)
    return list(
        (
            await session.scalars(
                select(TravelHotspot)
                .join(HotspotPlaceProfile, HotspotPlaceProfile.hotspot_id == TravelHotspot.id)
                .where(
                    TravelHotspot.is_active.is_(True),
                    TravelHotspot.review_status.in_(PUBLIC_HOTSPOT_STATUSES),
                    HotspotPlaceProfile.match_status.in_(("approved", "auto_approved")),
                    HotspotPlaceProfile.provider_refresh_after.is_not(None),
                    HotspotPlaceProfile.provider_refresh_after <= observed_at,
                )
                .order_by(HotspotPlaceProfile.provider_refresh_after)
                .limit(settings.hotspot_place_refresh_batch_size)
            )
        ).all()
    )


async def purge_expired_place_content(
    session: AsyncSession, *, now: datetime | None = None
) -> int:
    """Remove expired Google-derived content while retaining stable/manual identity."""
    observed_at = now or datetime.now(UTC)
    profiles = list(
        (
            await session.scalars(
                select(HotspotPlaceProfile).where(
                    HotspotPlaceProfile.provider_expires_at.is_not(None),
                    HotspotPlaceProfile.provider_expires_at <= observed_at,
                )
            )
        ).all()
    )
    for profile in profiles:
        profile.google_maps_uri = None
        profile.formatted_address = None
        profile.google_latitude = None
        profile.google_longitude = None
        profile.opening_hours_json = {}
        profile.provider_website_uri = None
        profile.provider_locale = None
        profile.provider_attributions_json = []
        if (
            not profile.manual_official_website_url
            and profile.website_review_status != "rejected"
        ):
            profile.website_review_status = "none"
        if profile.match_status == "pending":
            profile.match_status = "unmatched"
            _clear_candidate(profile)
    if profiles:
        await session.commit()
    return len(profiles)


async def create_system_refresh_run(
    session: AsyncSession,
    targets: list[TravelHotspot],
    *,
    now: datetime | None = None,
) -> HotspotPlaceEnrichmentRun | None:
    if not targets:
        return None
    observed_at = now or datetime.now(UTC)
    ids = [str(item.id) for item in targets]
    idempotency_key = f"automatic:{observed_at:%Y-%m-%dT%H}:{ids[0]}"
    existing = await session.scalar(
        select(HotspotPlaceEnrichmentRun).where(
            HotspotPlaceEnrichmentRun.actor_user_id.is_(None),
            HotspotPlaceEnrichmentRun.idempotency_key == idempotency_key,
        )
    )
    if existing:
        return existing
    run = HotspotPlaceEnrichmentRun(
        id=uuid4(),
        actor_user_id=None,
        idempotency_key=idempotency_key,
        mode="force",
        scope_json={"type": "automatic_refresh", "hotspot_ids": ids},
        status="queued",
        total_count=len(targets),
        estimated_google_calls=len(targets),
        result_json={"processed_ids": []},
    )
    session.add(run)
    await session.commit()
    return run


async def profile_overview(
    session: AsyncSession, redis: Redis, settings: Settings
) -> dict[str, Any]:
    total = int(
        await session.scalar(
            select(func.count(TravelHotspot.id)).where(
                TravelHotspot.is_active.is_(True),
                TravelHotspot.review_status.in_(PUBLIC_HOTSPOT_STATUSES),
            )
        )
        or 0
    )
    missing_place_ids = int(
        await session.scalar(
            select(func.count(TravelHotspot.id)).where(
                TravelHotspot.is_active.is_(True),
                TravelHotspot.review_status.in_(PUBLIC_HOTSPOT_STATUSES),
                TravelHotspot.google_place_id.is_(None),
            )
        )
        or 0
    )
    now = datetime.now(UTC)
    counts = {
        status: int(
            await session.scalar(
                select(func.count(HotspotPlaceProfile.id))
                .join(TravelHotspot, TravelHotspot.id == HotspotPlaceProfile.hotspot_id)
                .where(
                    TravelHotspot.is_active.is_(True),
                    TravelHotspot.review_status.in_(PUBLIC_HOTSPOT_STATUSES),
                    HotspotPlaceProfile.match_status == status
                )
            )
            or 0
        )
        for status in ("pending", "unmatched", "failed")
    }
    ready = int(
        await session.scalar(
            select(func.count(HotspotPlaceProfile.id))
            .join(TravelHotspot, TravelHotspot.id == HotspotPlaceProfile.hotspot_id)
            .where(
                TravelHotspot.is_active.is_(True),
                TravelHotspot.review_status.in_(PUBLIC_HOTSPOT_STATUSES),
                HotspotPlaceProfile.match_status.in_(("approved", "auto_approved")),
                HotspotPlaceProfile.website_review_status != "pending",
                HotspotPlaceProfile.provider_expires_at > now,
            )
        )
        or 0
    )
    website_pending = int(
        await session.scalar(
            select(func.count(HotspotPlaceProfile.id))
            .join(TravelHotspot, TravelHotspot.id == HotspotPlaceProfile.hotspot_id)
            .where(
                TravelHotspot.is_active.is_(True),
                TravelHotspot.review_status.in_(PUBLIC_HOTSPOT_STATUSES),
                HotspotPlaceProfile.match_status != "pending",
                HotspotPlaceProfile.website_review_status == "pending",
            )
        )
        or 0
    )
    expired = int(
        await session.scalar(
            select(func.count(HotspotPlaceProfile.id))
            .join(TravelHotspot, TravelHotspot.id == HotspotPlaceProfile.hotspot_id)
            .where(
                TravelHotspot.is_active.is_(True),
                TravelHotspot.review_status.in_(PUBLIC_HOTSPOT_STATUSES),
                HotspotPlaceProfile.provider_expires_at.is_not(None),
                HotspotPlaceProfile.provider_expires_at <= now,
            )
        )
        or 0
    )
    usage = await google_maps_usage_snapshot(
        redis,
        essentials_free_limit=settings.google_maps_essentials_free_limit,
        pro_free_limit=settings.google_maps_pro_free_limit,
        enterprise_free_limit=settings.google_maps_enterprise_free_limit,
    )
    return {
        "configured": bool(
            settings.google_maps_api_key and settings.hotspot_place_enrichment_enabled
        ),
        "total": total,
        "missing_place_ids": missing_place_ids,
        "ready": ready,
        "pending": counts["pending"] + website_pending,
        "unmatched": counts["unmatched"],
        "failed": counts["failed"],
        "expired": expired,
        "usage": {
            "period": usage.period,
            "used": usage.used,
            "free_remaining": usage.free_remaining,
            "available": usage.available,
            "sku_usage": [
                {
                    "sku": item.sku,
                    "used": item.used,
                    "free_limit": item.free_limit,
                    "percentage": item.percentage,
                }
                for item in usage.sku_usage
            ],
        },
    }
