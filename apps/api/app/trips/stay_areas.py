"""Stay-area recommendation and per-area hotel comparison for a saved trip.

The recommendation reads only the trip's own located items: every item votes for
the catalog area (``app.hotspots.areas``) that contains it, weighted down for meals
and auto-matched coordinates, and the city's areas are scored on how much of the
itinerary they hold, how many days touch them and how central they sit to
everything. Hotel offers for a chosen area come from the provider's coordinate
search, are normalised to TWD, filtered with the member's lodging preferences and
sorted by nightly price. Nothing here touches the database or Redis.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Any, Literal, cast
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from app.affiliates.registry import PARTNERS_BY_CODE
from app.affiliates.service import partner_supports_module
from app.config import Settings
from app.crawlers.fx import FxRateError, FxRateProvider
from app.destinations.catalog import DestinationProfile, destination_for_code, match_destination
from app.hotspots.areas import HotspotArea, area_by_code, area_name, city_areas, resolve_area
from app.hotspots.cities import CITY_BY_DESTINATION_ID
from app.hotspots.discovery import haversine_km
from app.i18n import Locale
from app.models import TripPlan, TripPlanItem
from app.optimization.hotel_filters import (
    HotelFilterResult,
    filter_hotels_with_relaxation,
    nightly_price,
)
from app.providers.schemas import HotelOffer
from app.search.schemas import SearchCreate, SearchModule, SearchPreferences, Travelers, TripType
from app.trips.schedule import active_route_rows

STAY_AREA_MAX = 4
STAY_AREA_MIN = 2
STAY_HOTEL_LIMIT = 12
NEARBY_LIMIT = 5
MIN_AREA_HOTELS = 3
URBAN_RADIUS_KM = 3.0
DAY_TRIP_RADIUS_KM = 5.0
MAX_STAY_NIGHTS = 14
MIN_EVIDENCE_WEIGHT = 1.5
OFFER_CACHE_MIN_TTL_SECONDS = 60
OFFER_CACHE_MAX_TTL_SECONDS = 600
# Owner's monetisation order for the stay flow; the search page keeps the registry order.
STAY_PARTNER_ORDER: tuple[str, ...] = ("agoda", "booking", "trip_com", "travelpayouts")
LODGING_ROLES = frozenset({"hotel_start", "hotel_end"})
LODGING_ITEM_TYPES = frozenset({"hotel", "hotel_anchor"})

StayAreaStatus = Literal["recommended", "low_evidence", "no_evidence", "unsupported"]
StayDateStatus = Literal["ready", "dates_missing", "dates_past"]
PartnerLinkKind = Literal["deep_link", "hotel_search", "area_search"]


def trip_timezone(trip: TripPlan) -> ZoneInfo:
    try:
        return ZoneInfo(trip.timezone or "UTC")
    except ZoneInfoNotFoundError:
        return ZoneInfo("UTC")


def trip_city(
    trip: TripPlan, search_json: dict[str, Any] | None
) -> tuple[DestinationProfile | None, str | None]:
    """Map a trip to the hotspot city whose area catalog can host its stay."""
    profile: DestinationProfile | None = None
    if search_json:
        profile = destination_for_code(str(search_json.get("destination") or ""))
    if profile is None and trip.destination_name:
        profile = match_destination(trip.destination_name)
    if profile is None:
        destination_city = trip.data.get("destination_city")
        if isinstance(destination_city, str) and destination_city:
            profile = match_destination(destination_city)
    if profile is None:
        return None, None
    city = CITY_BY_DESTINATION_ID.get(profile.id)
    city_code = city.code if city is not None else profile.code
    if not city_areas(city_code):
        return profile, None
    return profile, city_code


def extension_destination_ids(
    trip: TripPlan, search_json: dict[str, Any] | None
) -> tuple[str, ...]:
    source = (search_json or {}).get("preferences") or trip.data.get("preferences") or {}
    raw = source.get("extension_destination_ids") if isinstance(source, dict) else None
    return tuple(str(item) for item in raw or [] if item)


@dataclass(frozen=True)
class EvidenceItem:
    latitude: float
    longitude: float
    weight: float
    dwell_minutes: int
    day_date: date | None
    title: str
    area: HotspotArea | None


def _row_weight(row: TripPlanItem) -> float:
    weight = 0.5 if row.system_role in {"lunch", "dinner"} else 1.0
    source = str(row.location_source or "")
    if (
        row.is_estimated
        or source.endswith("_auto")
        or row.data.get("needs_place_confirmation") is True
    ):
        weight *= 0.6
    return weight


def _extension_owner(
    row: TripPlanItem,
    latitude: float,
    longitude: float,
    extension_ids: tuple[str, ...],
) -> str | None:
    tagged = row.data.get("destination_id")
    if isinstance(tagged, str) and tagged in extension_ids:
        return tagged
    for destination_id in extension_ids:
        city = CITY_BY_DESTINATION_ID.get(destination_id)
        if city is not None and resolve_area(city.code, latitude, longitude) is not None:
            return destination_id
    return None


def evidence_items(
    rows: list[TripPlanItem],
    city_code: str,
    extension_ids: tuple[str, ...] = (),
) -> tuple[list[EvidenceItem], dict[str, int]]:
    """Located itinerary rows that should vote for a stay area, minus the lodging itself."""
    items: list[EvidenceItem] = []
    excluded: dict[str, int] = {}
    for row in active_route_rows(rows):
        if row.system_role in LODGING_ROLES or row.item_type in LODGING_ITEM_TYPES:
            continue
        if row.latitude is None or row.longitude is None:
            continue
        latitude, longitude = float(row.latitude), float(row.longitude)
        if abs(latitude) < 1e-4 and abs(longitude) < 1e-4:
            continue
        owner = _extension_owner(row, latitude, longitude, extension_ids)
        if owner is not None:
            excluded[owner] = excluded.get(owner, 0) + 1
            continue
        items.append(
            EvidenceItem(
                latitude=latitude,
                longitude=longitude,
                weight=_row_weight(row),
                dwell_minutes=max(30, min(240, row.duration_minutes or 60)),
                day_date=row.day_date,
                title=(row.title or row.location_name or "").strip(),
                area=resolve_area(city_code, latitude, longitude),
            )
        )
    return items, excluded


@dataclass(frozen=True)
class StayAreaScore:
    area: HotspotArea
    score: float
    item_count: int
    dwell_minutes: int
    day_count: int
    sample_titles: tuple[str, ...]
    reasons: tuple[str, ...]

    @property
    def is_day_trip(self) -> bool:
        return self.area.radius_km > DAY_TRIP_RADIUS_KM


@dataclass(frozen=True)
class StayAreaRecommendation:
    status: StayAreaStatus
    areas: list[StayAreaScore]
    located_item_count: int
    unassigned_item_count: int
    excluded_extension: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


@dataclass
class _AreaStats:
    weight: float = 0.0
    count: int = 0
    dwell_minutes: float = 0.0
    days: set[date] = field(default_factory=set)
    titles: list[str] = field(default_factory=list)


def _urban_factor(area: HotspotArea) -> float:
    if area.radius_km <= URBAN_RADIUS_KM:
        return 1.0
    if area.radius_km <= DAY_TRIP_RADIUS_KM:
        return 0.8
    return 0.5


def _centrality(area: HotspotArea, items: list[EvidenceItem], total_weight: float) -> float:
    if total_weight <= 0:
        return 0.0
    return (
        sum(
            item.weight
            / (1 + haversine_km(area.latitude, area.longitude, item.latitude, item.longitude) / 3)
            for item in items
        )
        / total_weight
    )


def _hub_area(city_code: str, items: list[EvidenceItem], total_weight: float) -> HotspotArea | None:
    if total_weight <= 0:
        return None
    latitude = sum(item.latitude * item.weight for item in items) / total_weight
    longitude = sum(item.longitude * item.weight for item in items) / total_weight
    hub = resolve_area(city_code, latitude, longitude)
    if hub is not None:
        return hub
    nearest: tuple[float, HotspotArea] | None = None
    for area in city_areas(city_code):
        if area.radius_km > URBAN_RADIUS_KM:
            continue
        distance = haversine_km(latitude, longitude, area.latitude, area.longitude)
        if distance <= 3 and (nearest is None or distance < nearest[0]):
            nearest = (distance, area)
    return nearest[1] if nearest else None


def _default_areas(city_code: str) -> list[HotspotArea]:
    areas = city_areas(city_code)
    urban = [area for area in areas if area.radius_km <= URBAN_RADIUS_KM]
    return list(urban[:3] or areas[:3])


def score_stay_areas(
    city_code: str,
    items: list[EvidenceItem],
    *,
    excluded_extension: dict[str, int] | None = None,
    current_lodging_area: HotspotArea | None = None,
) -> StayAreaRecommendation:
    excluded = dict(excluded_extension or {})
    warnings: list[str] = []
    excluded_count = sum(excluded.values())
    if excluded_count and excluded_count >= 0.4 * (len(items) + excluded_count):
        warnings.append("consider_second_stay")
    total_weight = sum(item.weight for item in items)
    if total_weight <= 0:
        defaults = [
            StayAreaScore(
                area=area,
                score=0.0,
                item_count=0,
                dwell_minutes=0,
                day_count=0,
                sample_titles=(),
                reasons=(
                    "destination_default",
                    *(("current_lodging",) if area is current_lodging_area else ()),
                ),
            )
            for area in _default_areas(city_code)
        ]
        return StayAreaRecommendation("no_evidence", defaults, 0, 0, excluded, warnings)

    areas = city_areas(city_code)
    catalog_index = {area.code: index for index, area in enumerate(areas)}
    stats: dict[str, _AreaStats] = {}
    unassigned = 0
    for item in items:
        if item.area is None:
            unassigned += 1
            continue
        entry = stats.setdefault(item.area.code, _AreaStats())
        entry.weight += item.weight
        entry.count += 1
        entry.dwell_minutes += item.dwell_minutes * item.weight
        if item.day_date is not None:
            entry.days.add(item.day_date)
        if item.title and len(entry.titles) < 3 and item.title not in entry.titles:
            entry.titles.append(item.title)
    days_with_evidence = len({item.day_date for item in items if item.day_date is not None})
    max_weight = max((entry.weight for entry in stats.values()), default=0.0)
    max_dwell = max((entry.dwell_minutes for entry in stats.values()), default=0.0)
    max_days = max((len(entry.days) for entry in stats.values()), default=0)
    hub = _hub_area(city_code, items, total_weight)

    def scored(area: HotspotArea, *, is_fill: bool = False) -> StayAreaScore:
        entry = stats.get(area.code)
        items_term = entry.weight / max_weight if entry and max_weight else 0.0
        dwell_term = entry.dwell_minutes / max_dwell if entry and max_dwell else 0.0
        cover_term = len(entry.days) / max(1, days_with_evidence) if entry else 0.0
        score = _urban_factor(area) * (
            0.5 * items_term
            + 0.15 * dwell_term
            + 0.15 * cover_term
            + 0.2 * _centrality(area, items, total_weight)
        )
        reasons: list[str] = []
        if entry and entry.weight == max_weight:
            reasons.append("most_items")
        if entry and max_days >= 2 and len(entry.days) == max_days:
            reasons.append("most_days")
        if area is hub or is_fill:
            reasons.append("central")
        if area.radius_km > DAY_TRIP_RADIUS_KM:
            reasons.append("day_trip_zone")
        if area is current_lodging_area:
            reasons.append("current_lodging")
        return StayAreaScore(
            area=area,
            score=score,
            item_count=entry.count if entry else 0,
            dwell_minutes=int(round(entry.dwell_minutes)) if entry else 0,
            day_count=len(entry.days) if entry else 0,
            sample_titles=tuple(entry.titles) if entry else (),
            reasons=tuple(reasons),
        )

    def order_key(score: StayAreaScore) -> tuple[float, int, int, float, int]:
        return (
            -round(score.score, 3),
            -score.item_count,
            -score.day_count,
            score.area.radius_km,
            catalog_index.get(score.area.code, len(catalog_index)),
        )

    candidate_codes = set(stats)
    if hub is not None:
        candidate_codes.add(hub.code)
    ranked = sorted(
        (scored(area) for area in areas if area.code in candidate_codes), key=order_key
    )[:STAY_AREA_MAX]
    if len(ranked) < STAY_AREA_MIN:
        chosen = {score.area.code for score in ranked}
        fills = sorted(
            (scored(area, is_fill=True) for area in areas if area.code not in chosen),
            key=order_key,
        )
        ranked.extend(fills[: STAY_AREA_MIN - len(ranked)])
    status: StayAreaStatus = (
        "recommended" if total_weight >= MIN_EVIDENCE_WEIGHT else "low_evidence"
    )
    return StayAreaRecommendation(
        status=status,
        areas=ranked,
        located_item_count=len(items),
        unassigned_item_count=unassigned,
        excluded_extension=excluded,
        warnings=warnings,
    )


def area_summary(score: StayAreaScore, locale: Locale) -> dict[str, Any]:
    return {
        "code": score.area.code,
        "name": area_name(score.area, locale),
        "latitude": score.area.latitude,
        "longitude": score.area.longitude,
        "radius_km": score.area.radius_km,
        "is_day_trip": score.is_day_trip,
        "score": round(score.score, 3),
        "item_count": score.item_count,
        "dwell_minutes": score.dwell_minutes,
        "day_count": score.day_count,
        "sample_titles": list(score.sample_titles),
        "reasons": list(score.reasons),
    }


@dataclass(frozen=True)
class StayDates:
    status: StayDateStatus
    check_in: date | None = None
    check_out: date | None = None
    nights: int = 0
    notes: tuple[str, ...] = ()


def stay_dates(trip: TripPlan, today: date | None = None) -> StayDates:
    """Check-in/out for pricing: never in the past, at most MAX_STAY_NIGHTS nights."""
    if trip.start_date is None or trip.end_date is None:
        return StayDates("dates_missing")
    current = today or datetime.now(trip_timezone(trip)).date()
    if trip.end_date < current:
        return StayDates("dates_past", trip.start_date, trip.end_date)
    notes: list[str] = []
    check_in = trip.start_date
    if check_in < current:
        check_in = current
        notes.append("checkin_moved_to_today")
    nights = (trip.end_date - check_in).days
    if nights <= 0:
        nights = 1
        notes.append("assumed_one_night")
    if nights > MAX_STAY_NIGHTS:
        nights = MAX_STAY_NIGHTS
        notes.append("stay_truncated")
    return StayDates("ready", check_in, check_in + timedelta(days=nights), nights, tuple(notes))


def stay_search_query(
    trip: TripPlan,
    city_code: str,
    search_json: dict[str, Any] | None,
    dates: StayDates,
    locale: Locale,
) -> SearchCreate:
    if search_json:
        base = SearchCreate.model_validate(search_json)
        travelers, preferences, origin = base.travelers, base.preferences, base.origin
    else:
        travelers = Travelers.model_validate(cast(dict[str, Any], trip.data.get("travelers") or {}))
        preferences = SearchPreferences.model_validate(
            cast(dict[str, Any], trip.data.get("preferences") or {})
        )
        origin = None
    return SearchCreate(
        trip_type=TripType.ROUND_TRIP,
        # Hotel providers never read the origin, but the schema validator requires one.
        origin=origin or "TPE",
        destination=city_code,
        departure_date=dates.check_in,
        return_date=dates.check_out,
        travelers=travelers,
        # The area is chosen geographically here, and extension ids would trip the
        # trip-length validation for short stays.
        preferences=preferences.model_copy(
            update={
                "extension_destination_ids": [],
                "preferred_areas": [],
                "preferred_area": None,
            }
        ),
        modules=[SearchModule.HOTEL],
        currency="TWD",
        locale=locale,
    )


def area_offers_cache_key(
    provider_name: str,
    environment: str,
    city_code: str,
    area_code: str,
    query: SearchCreate,
) -> str:
    digest = hashlib.sha256(
        json.dumps(
            {
                "check_in": query.departure_date.isoformat() if query.departure_date else None,
                "check_out": query.return_date.isoformat() if query.return_date else None,
                "adults": query.travelers.adults,
                "children_ages": query.travelers.children_ages,
                "rooms": query.travelers.rooms,
                "currency": query.currency,
                "locale": query.locale,
            },
            sort_keys=True,
        ).encode()
    ).hexdigest()[:24]
    return f"stay:hotels:{provider_name}:{environment}:{city_code}:{area_code}:{digest}"


def offers_cache_ttl(offers: list[HotelOffer], now: datetime) -> int:
    if not offers:
        return OFFER_CACHE_MIN_TTL_SECONDS
    remaining = (min(offer.expires_at for offer in offers) - now).total_seconds()
    return int(max(OFFER_CACHE_MIN_TTL_SECONDS, min(OFFER_CACHE_MAX_TTL_SECONDS, remaining)))


def trim_offer(offer: HotelOffer) -> HotelOffer:
    """Drop bulk that the comparison never shows so cached areas stay small."""
    return offer.model_copy(update={"images": offer.images[:1], "amenities": offer.amenities[:6]})


def _twd(value: Decimal, rate: Decimal) -> Decimal:
    return (value * rate).quantize(Decimal("1"))


def dedupe_offers(offers: list[HotelOffer]) -> list[HotelOffer]:
    """One row per hotel (cheapest room), remembering how many rates were offered."""
    cheapest: dict[tuple[str, str], HotelOffer] = {}
    counts: dict[tuple[str, str], int] = {}
    for offer in offers:
        key = (offer.provider, offer.hotel_id)
        counts[key] = counts.get(key, 0) + 1
        current = cheapest.get(key)
        if current is None or nightly_price(offer) < nightly_price(current):
            cheapest[key] = offer
    return [
        offer.model_copy(update={"offer_count": counts[key]}) if counts[key] > 1 else offer
        for key, offer in cheapest.items()
    ]


async def normalize_offers(offers: list[HotelOffer], fx: FxRateProvider | None) -> list[HotelOffer]:
    """Drop unplaceable offers, convert foreign prices to TWD and collapse room rates."""
    located = [
        offer
        for offer in offers
        if not (abs(offer.latitude) < 1e-4 and abs(offer.longitude) < 1e-4)
    ]
    rates: dict[str, Decimal | None] = {}
    converted: list[HotelOffer] = []
    for offer in located:
        currency = offer.currency.upper()
        if currency == "TWD":
            converted.append(offer)
            continue
        if currency not in rates:
            rate: Decimal | None = None
            if fx is not None:
                try:
                    rate = (await fx.rate_to_twd(currency)).rate
                except FxRateError:
                    rate = None
            rates[currency] = rate
        rate = rates[currency]
        if rate is None:
            converted.append(offer.model_copy(update={"price_estimate_unavailable": True}))
            continue
        converted.append(
            offer.model_copy(
                update={
                    "currency": "TWD",
                    "base_price": _twd(offer.base_price, rate),
                    "taxes": _twd(offer.taxes, rate),
                    "fees": _twd(offer.fees, rate),
                    "total_price": _twd(offer.total_price, rate),
                    "nightly_price": _twd(nightly_price(offer), rate),
                    "original_currency": currency,
                    "original_total_price": offer.total_price,
                    "exchange_rate": rate,
                    "exchange_rate_retrieved_at": datetime.now(UTC),
                }
            )
        )
    return dedupe_offers(converted)


@dataclass(frozen=True)
class AreaOffer:
    offer: HotelOffer
    distance_km: float
    in_area: bool


def area_margin_km(area: HotspotArea) -> float:
    return max(0.5, 0.25 * area.radius_km)


def split_area_offers(
    area: HotspotArea, offers: list[HotelOffer]
) -> tuple[list[AreaOffer], list[AreaOffer]]:
    """Offers inside the area circle (plus a margin), and the nearest few when thin."""
    ranked = sorted(
        (
            (offer, haversine_km(area.latitude, area.longitude, offer.latitude, offer.longitude))
            for offer in offers
        ),
        key=lambda pair: pair[1],
    )
    limit = area.radius_km + area_margin_km(area)
    in_area = [
        AreaOffer(offer, round(distance, 1), True)
        for offer, distance in ranked
        if distance <= limit
    ]
    nearby: list[AreaOffer] = []
    if len(in_area) < MIN_AREA_HOTELS:
        nearby = [
            AreaOffer(offer, round(distance, 1), False)
            for offer, distance in ranked
            if distance > limit
        ][:NEARBY_LIMIT]
    return in_area, nearby


@dataclass(frozen=True)
class RankedHotels:
    hotels: list[AreaOffer]
    filters: HotelFilterResult


def rank_area_offers(
    candidates: list[AreaOffer], preferences: SearchPreferences, travelers: Travelers
) -> RankedHotels:
    filters = filter_hotels_with_relaxation(
        preferences,
        travelers.adults + travelers.children,
        [candidate.offer for candidate in candidates],
        include_area_constraint=False,
        # Live providers hard-code station walk minutes, so the constraint is noise.
        ignore_station_walk=True,
    )
    by_id = {candidate.offer.id: candidate for candidate in candidates}

    def sort_key(candidate: AreaOffer) -> tuple[bool, bool, Decimal, float, int]:
        offer = candidate.offer
        return (
            offer.price_estimate_unavailable,
            bool(filters.gaps.get(offer.id)),
            nightly_price(offer),
            -(offer.review_score or 0.0),
            -(offer.review_count or 0),
        )

    # Every hard match stays visible so the member can weigh a cheaper hotel against
    # the preference it misses; full matches lead and `relaxed` explains an empty top.
    ordered = sorted((by_id[offer_id] for offer_id in filters.gaps), key=sort_key)
    return RankedHotels(ordered[:STAY_HOTEL_LIMIT], filters)


def booking_deep_link(offer: HotelOffer | None) -> str | None:
    if offer is None or offer.provider != "booking":
        return None
    return offer.booking_url


def stay_partner_options(
    settings: Settings, area_label: str, hotel: HotelOffer | None
) -> list[dict[str, Any]]:
    """Partner buttons in the stay flow order; URLs are rendered at click time."""
    options: list[dict[str, Any]] = []
    for code in STAY_PARTNER_ORDER:
        partner = PARTNERS_BY_CODE[code]
        # A Booking Demand deep link is already the affiliate contract, so it does not
        # need the separate Booking affiliate template to be configured.
        deep_link = code == "booking" and booking_deep_link(hotel) is not None
        if not deep_link and not partner_supports_module(partner, "hotel", settings):
            continue
        kind: PartnerLinkKind = (
            "deep_link" if deep_link else "hotel_search" if hotel is not None else "area_search"
        )
        cta = {
            "deep_link": f"到 {partner.display_name} 預訂",
            "hotel_search": f"在 {partner.display_name} 搜尋此飯店",
            "area_search": f"到 {partner.display_name} 查看{area_label}住宿",
        }[kind]
        options.append(
            {
                "partner": code,
                "display_name": partner.display_name,
                "kind": kind,
                "cta": cta,
            }
        )
    return options


def hotel_payload(
    candidate: AreaOffer,
    *,
    gaps: list[str],
    is_current_lodging: bool,
    partners: list[dict[str, Any]],
) -> dict[str, Any]:
    payload = candidate.offer.model_dump(mode="json")
    payload.update(
        {
            "distance_km": candidate.distance_km,
            "in_area": candidate.in_area,
            "is_current_lodging": is_current_lodging,
            "preference_gaps": gaps,
            "partners": partners,
        }
    )
    return payload


def find_area(city_code: str | None, area_code: str) -> HotspotArea | None:
    return area_by_code(city_code, area_code)
