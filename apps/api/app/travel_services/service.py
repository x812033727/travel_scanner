from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.hotspots.areas import city_areas
from app.hotspots.cities import CITY_BY_DESTINATION_ID
from app.hotspots.discovery import haversine_km
from app.models import (
    DestinationAffiliateOffer,
    TravelServiceBrand,
    TravelServiceConfig,
    TravelServiceOffer,
    TravelServiceProduct,
    TripPlan,
    TripPlanItem,
)
from app.problems import AppError
from app.restaurants.editorial import validate_editorial_url
from app.travel_services.channels import (
    channel_context,
    channel_for,
    channel_project,
    klook_product_target,
    validate_offer_target,
)
from app.travel_services.registry import BRANDS, affiliate_target
from app.travel_services.schemas import CITIES, KINDS, CatalogConfig, Facts, HotelLink, ProductInput
from app.trips.stay_areas import evidence_items, extension_destination_ids, score_stay_areas


def fail(code: str, status: int = 422) -> AppError:
    return AppError(status, code, code)


def fingerprint(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


async def catalog_config(session: AsyncSession) -> tuple[CatalogConfig, int]:
    row = await session.get(TravelServiceConfig, 1)
    return (CatalogConfig.model_validate(row.data), row.version) if row else (CatalogConfig(), 0)


def enabled(config: CatalogConfig, city: str, kind: str, *, public: bool = False) -> bool:
    return (
        (not public or config.public_enabled)
        and city in config.enabled_destinations
        and kind in config.enabled_kinds
    )


def product_enabled(config: CatalogConfig, product: TravelServiceProduct) -> bool:
    if product.kind != "esim":
        return enabled(config, product.destination_id, product.kind)
    coverage = product.facts.get("country_codes", [])
    return any(enabled(config, city, "esim") and CITIES[city][0] in coverage for city in CITIES)


def require_product_review(data: ProductInput) -> None:
    facts = data.facts
    try:
        validate_editorial_url(data.source_url)
        if facts.coordinate_source_url:
            validate_editorial_url(facts.coordinate_source_url)
    except AppError as exc:
        raise fail("service_source_required") from exc
    if facts.latitude is not None and not facts.coordinate_source_url:
        raise fail("service_source_required")
    if data.kind == "hotel":
        if (
            facts.latitude is None
            or facts.longitude is None
            or not facts.map_verified
            or not facts.coordinate_source_url
        ):
            raise fail("service_identity_required")
        if CITIES[data.destination_id][0] == "KR":
            if not re.fullmatch(
                r"https://map\.naver\.com/(?:p|v5)/entry/place/\d+/?(?:\?.*)?",
                facts.naver_map_url or "",
            ):
                raise fail("service_identity_required")
        elif not facts.google_place_id:
            raise fail("service_identity_required")
        center = CITIES[data.destination_id][2]
        if haversine_km(*center, facts.latitude, facts.longitude) > 55:
            raise fail("service_destination_mismatch")
        area = next(
            (a for a in city_areas(CITIES[data.destination_id][1]) if a.code == facts.area_code),
            None,
        )
        if not area or haversine_km(*center, area.latitude, area.longitude) > 25:
            raise fail("service_area_required")
        if (
            haversine_km(area.latitude, area.longitude, facts.latitude, facts.longitude)
            > area.radius_km
        ):
            raise fail("service_area_required")
    if data.kind == "transfer" and (
        facts.airport not in CITIES[data.destination_id][3] or not facts.direction
    ):
        raise fail("service_airport_required")
    if data.kind == "esim" and not facts.country_codes:
        raise fail("service_coverage_required")


def product_input(product: TravelServiceProduct) -> ProductInput:
    from app.travel_services.hotel_options import legacy_links

    return ProductInput(
        source_key=product.source_key,
        kind=product.kind,
        destination_id=product.destination_id,
        title=product.title,
        names_json=product.names_json,
        source_url=product.source_url,
        facts={
            **product.facts,
            "hotel_links": [link.model_dump() for link in legacy_links(product)],
        },
    )


def fresh_price(facts: Facts, now: datetime) -> bool:
    return bool(
        facts.currency
        and facts.reference_price is not None
        and facts.price_checked_at
        and now - timedelta(hours=48) <= facts.price_checked_at <= now
    )


def ready_brand(brand: TravelServiceBrand, settings: Settings, now: datetime) -> bool:
    channel = channel_for(brand)
    return bool(
        brand.code in BRANDS
        and brand.project_id == channel_project(settings, channel)
        and brand.enabled
        and brand.approval == "approved"
        and brand.verified_at
        and now - timedelta(days=30) <= brand.verified_at <= now
        and (
            channel == "travelpayouts" and settings.travelpayouts_enabled
            or channel == "klook_direct" and brand.code == "klook" and settings.klook_enabled
        )
    )


def link_context(settings: Settings, channel: str = "travelpayouts") -> str:
    return channel_context(settings, channel)


def ready_offer(
    offer: TravelServiceOffer,
    brand: TravelServiceBrand,
    product: TravelServiceProduct,
    settings: Settings,
    now: datetime,
) -> bool:
    if not (
        product.status == "approved"
        and offer.status == "approved"
        and offer.verified_at
        and now - timedelta(days=30) <= offer.verified_at <= now
        and (not offer.expires_at or offer.expires_at > now)
        and ready_brand(brand, settings, now)
        and product.kind in BRANDS[brand.code].kinds
    ):
        return False
    try:
        validate_offer_target(brand, offer.target_url, offer.static_url)
        if channel_for(brand) == "klook_direct":
            if offer.scope == "product":
                klook_product_target(offer.target_url, product.kind)
            return offer.verification_context == link_context(settings, "klook_direct")
        if offer.static_url:
            affiliate_target(offer.static_url)
            return bool(
                settings.travelpayouts_marker
                and offer.verification_context == link_context(settings)
            )
    except ValueError:
        return False
    return bool(
        BRANDS[brand.code].api_supported
        and settings.travelpayouts_api_token
        and settings.travelpayouts_marker
        and settings.travelpayouts_project_id
    )


def ready_destination_offer(
    offer: DestinationAffiliateOffer,
    brand: TravelServiceBrand,
    settings: Settings,
    now: datetime,
) -> bool:
    if not (
        offer.status == "approved"
        and offer.verified_at
        and now - timedelta(days=30) <= offer.verified_at <= now
        and (not offer.expires_at or offer.expires_at > now)
        and ready_brand(brand, settings, now)
        and offer.module in BRANDS[brand.code].supported_modules
        and offer.verification_context == link_context(settings, channel_for(brand))
    ):
        return False
    try:
        validate_offer_target(brand, offer.target_url, offer.static_url)
        if channel_for(brand) == "klook_direct":
            return True
        if offer.static_url:
            affiliate_target(offer.static_url)
            return bool(settings.travelpayouts_marker)
    except (KeyError, ValueError):
        return False
    return bool(
        BRANDS[brand.code].api_supported
        and settings.travelpayouts_api_token
        and settings.travelpayouts_marker
        and settings.travelpayouts_project_id
    )


def public_product(product: TravelServiceProduct, locale: str, now: datetime) -> dict[str, Any]:
    from app.hotspots.maps import build_map_links
    from app.locations.map_identity import catalog_country_code, catalog_map_identities

    facts = Facts.model_validate(product.facts)
    # A stale or missing reference is unknown, never free or a quote.
    if product.kind == "hotel" or not fresh_price(facts, now):
        facts = facts.model_copy(
            update={"reference_price": None, "currency": None, "price_checked_at": None}
        )
    return {
        "id": str(product.id),
        "kind": product.kind,
        "destination_id": product.destination_id,
        "title": product.names_json.get(locale) or product.title,
        # Link URLs and review evidence stay server-side; clickout resolves saved identity.
        "facts": {
            **facts.model_dump(mode="json", exclude={"hotel_links", "map_identities"}),
            "map_identities": catalog_map_identities(product),
        },
        "map_identities": catalog_map_identities(product),
        "map_links": build_map_links(
            name=product.title, local_name=None, city_name=product.destination_id,
            country_code=catalog_country_code(product),
            latitude=facts.latitude, longitude=facts.longitude,
            google_place_id=facts.google_place_id, naver_map_url=facts.naver_map_url,
            map_match_status="verified" if facts.map_verified else "unverified",
            map_identities=catalog_map_identities(product),
        ) if product.kind == "hotel" else [],
        "source_url": product.source_url,
        "verified_at": product.verified_at,
        "distance_km": None,
        "reason": "destination_match",
        "offers": [],
        "direct_links": [],
    }


def ready_hotel_links(
    product: TravelServiceProduct, config: CatalogConfig, now: datetime
) -> list[HotelLink]:
    if not (
        config.direct_hotel_links_enabled
        and product_enabled(config, product)
        and product.kind == "hotel"
        and product.status == "approved"
        and product.verified_at
        and now - timedelta(days=30) <= product.verified_at <= now
    ):
        return []
    from app.travel_services.hotel_options import ready_option

    return [
        HotelLink(provider=o.provider, url=o.url, evidence_url=o.evidence_url)
        for o in product.hotel_options
        if ready_option(product, o, config, now) and o.url and o.evidence_url
    ]


def trip_destinations(trip: TripPlan, rows: list[TripPlanItem]) -> list[str]:
    tagged = {
        str(row.data.get("destination_id"))
        for row in rows
        if not row.is_skipped and row.data.get("destination_id") in CITIES
    }
    name = " ".join(
        str(value or "") for value in (trip.destination_name, trip.data.get("destination_city"))
    ).lower()
    if trip.data.get("destination_id") in CITIES:
        tagged.add(str(trip.data["destination_id"]))
    aliases = {
        "tokyo": ("tokyo", "東京", "东京", "도쿄"),
        "osaka": ("osaka", "大阪", "오사카"),
        "kyoto": ("kyoto", "京都", "교토"),
        "seoul": ("seoul", "首爾", "首尔", "서울"),
        "busan": ("busan", "釜山", "부산"),
        "taipei": ("taipei", "台北", "臺北", "타이베이"),
    }
    tagged.update(city for city, names in aliases.items() if any(word in name for word in names))
    return [city for city in CITIES if city in tagged]


def trip_countries(trip: TripPlan, rows: list[TripPlanItem]) -> list[str]:
    countries = {CITIES[city][0] for city in trip_destinations(trip, rows)}
    destinations = {str(r.data.get("destination_id")) for r in rows if not r.is_skipped}
    destinations.update(extension_destination_ids(trip, None))
    for destination in destinations:
        if destination in CITY_BY_DESTINATION_ID:
            countries.add(CITY_BY_DESTINATION_ID[destination].country_code)
    return sorted(countries)


def rank_products(
    products: list[dict[str, Any]],
    *,
    city: str,
    rows: list[TripPlanItem] | None = None,
    trip: TripPlan | None = None,
    center: tuple[float, float] | None = None,
    radius: int | None = None,
    area: str | None = None,
    facilities: list[str] | None = None,
    airport: str | None = None,
    direction: str | None = None,
    passengers: int | None = None,
    language: str | None = None,
    countries: list[str] | None = None,
    days: int | None = None,
) -> list[dict[str, Any]]:
    evidence, _ = evidence_items(
        rows or [], CITIES[city][1], extension_destination_ids(trip, None) if trip else ()
    )
    # A shared KIX gateway must not make a Kyoto attraction vote for an Osaka hotel.
    evidence = [
        e for e in evidence if haversine_km(*CITIES[city][2], e.latitude, e.longitude) <= 25
    ]
    ranked: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
    area_center = next(
        ((a.latitude, a.longitude) for a in city_areas(CITIES[city][1]) if a.code == area), None
    )
    for product in products:
        if product["destination_id"] != city and product["kind"] != "esim":
            continue
        facts, kind = product["facts"], product["kind"]
        score: tuple[Any, ...] = (0, product["title"], product["id"])
        if kind == "hotel":
            if (
                area
                and facts["area_code"] != area
                or facilities
                and not set(facilities) <= set(facts["facilities"])
            ):
                continue
            if facts["latitude"] is None or facts["longitude"] is None:
                continue
            lat, lng = facts["latitude"], facts["longitude"]
            nearby = haversine_km(*(center or area_center or CITIES[city][2]), lat, lng)
            if radius and nearby > radius:
                continue
            total_weight = sum(e.weight for e in evidence)
            distance = (
                sum(haversine_km(e.latitude, e.longitude, lat, lng) * e.weight for e in evidence)
                / total_weight
                if total_weight
                else nearby
            )
            product = {
                **product,
                "distance_km": round(distance, 2),
                "reason": "trip_distance" if total_weight else "center_distance",
            }
            score = (distance, product["title"], product["id"])
        elif kind == "transfer":
            if (
                airport
                and facts["airport"] != airport
                or direction
                and facts["direction"] != direction
            ):
                continue
            if passengers and facts["passengers"] is not None and facts["passengers"] < passengers:
                continue
            product = {**product, "reason": "airport_match"}
            score = (facts["passengers"] is None, product["title"], product["id"])
        elif kind == "tour":
            if language and language not in facts["languages"]:
                continue
            matched = len(
                set(facts["attraction_ids"]) & {str(r.data.get("hotspot_id")) for r in rows or []}
            )
            score = (-matched, product["title"], product["id"])
        elif kind == "esim":
            if not set(countries or [CITIES[city][0]]) <= set(facts["country_codes"]):
                continue
            if days and (facts["validity_days"] is None or facts["validity_days"] < days):
                continue
            product = {**product, "reason": "coverage_match"}
            # Do not compare prices across currencies or unequal packages.
            score = (
                facts["validity_days"] is None,
                facts["validity_days"] or 999,
                -(facts["data_gb"] or 0),
                facts["currency"] or "ZZZ",
                facts["reference_price"] is None,
                facts["reference_price"] if facts["reference_price"] is not None else 0,
                product["title"],
                product["id"],
            )
        ranked.append((score, product))
    return [
        product
        for _, product in sorted(ranked, key=lambda pair: (KINDS.index(pair[1]["kind"]), pair[0]))
    ]


async def recommendations(
    session: AsyncSession,
    settings: Settings,
    locale: str,
    *,
    city: str,
    public: bool = True,
    trip: TripPlan | None = None,
    rows: list[TripPlanItem] | None = None,
    tracking_allowed: bool = True,
    **filters: Any,
) -> dict[str, Any]:
    if city not in CITIES:
        raise fail("service_destination_mismatch", 404)
    config, _ = await catalog_config(session)
    kinds = [kind for kind in KINDS if enabled(config, city, kind, public=public)]
    now = datetime.now(UTC)
    products = list(
        await session.scalars(
            select(TravelServiceProduct).where(
                or_(
                    TravelServiceProduct.destination_id == city, TravelServiceProduct.kind == "esim"
                ),
                TravelServiceProduct.kind.in_(kinds),
                TravelServiceProduct.status == "approved",
            )
        )
    )
    offers: dict[str, list[dict[str, Any]]] = {}
    hotel_targets: dict[str, set[tuple[str, str]]] = {}
    for offer, brand in (
        await session.execute(
            select(TravelServiceOffer, TravelServiceBrand)
            .join(TravelServiceBrand, TravelServiceBrand.id == TravelServiceOffer.brand_id)
            .where(TravelServiceOffer.product_id.in_([p.id for p in products]))
        )
    ).all():
        product = next(p for p in products if p.id == offer.product_id)
        if ready_offer(offer, brand, product, settings, now):
            if offer.scope == "product":
                hotel_targets.setdefault(str(product.id), set()).add((brand.code, offer.target_url))
            offers.setdefault(str(product.id), []).append(
                {
                    "id": str(offer.id),
                    "brand": brand.code,
                    "brand_name": BRANDS[brand.code].name,
                    "scope": offer.scope,
                }
            )
    results = rank_products(
        [public_product(p, locale, now) for p in products],
        city=city,
        trip=trip,
        rows=rows,
        **filters,
    )
    for result_product in results:
        result_product["offers"] = offers.get(result_product["id"], [])
        product = next(p for p in products if str(p.id) == result_product["id"])
        from app.travel_services.hotel_options import public_options

        result_product["booking_options"] = (
            await public_options(
                session, product, config, settings, now, hotel_targets.get(str(product.id), set()),
                tracking_allowed=tracking_allowed,
            )
            if product.kind == "hotel"
            else []
        )
        result_product["direct_links"] = [
            {
                "provider": link.provider,
                "name": BRANDS[link.provider].name if link.provider != "official" else None,
            }
            for link in ready_hotel_links(product, config, now)
        ]
    evidence, _ = evidence_items(rows or [], CITIES[city][1])
    areas = score_stay_areas(CITIES[city][1], evidence)
    local_areas = {
        a.code: a
        for a in city_areas(CITIES[city][1])
        if haversine_km(*CITIES[city][2], a.latitude, a.longitude) <= 25
    }
    scored = {a.area.code: a for a in areas.areas}
    return {
        "enabled": bool(kinds),
        "enabled_kinds": kinds,
        "destination_id": city,
        "items": results[:120],
        "total": len(results),
        "areas": [
            {
                "code": code,
                "names": a.names,
                "score": scored[code].score if code in scored else None,
            }
            for code, a in local_areas.items()
        ],
        "price_mode": "external",
        "ranking": "context_not_commission",
    }
