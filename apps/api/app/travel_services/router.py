from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated, Any, Literal
from urllib.parse import urlsplit
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

import httpx
from fastapi import APIRouter, Depends, Header, Query, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.affiliates.service import TravelpayoutsLinkClient
from app.auth.service import CurrentUser
from app.db import get_session
from app.hotspots.maps import build_map_links
from app.i18n import Locale, current_locale
from app.infra import enforce_named_rate_limit, get_redis
from app.models import (
    AffiliateClick,
    HotelBookingClick,
    TravelHotspot,
    TravelServiceBrand,
    TravelServiceOffer,
    TravelServiceProduct,
    TripPlan,
    TripPlanItem,
    TripServiceSelection,
)
from app.travel_services.hotel_quotes import HotelQuoteRequest, search_quotes
from app.travel_services.registry import affiliate_click_target
from app.travel_services.schemas import CITIES, Facts, Kind, SelectInput, SelectionStatus
from app.travel_services.service import (
    catalog_config,
    fail,
    fingerprint,
    product_enabled,
    product_input,
    ready_hotel_links,
    ready_offer,
    recommendations,
    require_product_review,
    trip_countries,
    trip_destinations,
)
from app.trips.itinerary import ItineraryItem
from app.trips.router import item_record, load_items, persist_system_schedule_change
from app.trips.schedule import canonicalize_positions, ensure_system_slots, sync_primary_lodging

router = APIRouter(tags=["travel services"])
Session = Annotated[AsyncSession, Depends(get_session)]
RequestLocale = Annotated[Locale, Depends(current_locale)]
OperationKey = Annotated[
    str,
    Header(alias="Idempotency-Key", min_length=8, max_length=128, pattern=r"^[A-Za-z0-9._:-]+$"),
]


async def locked_trip(session: AsyncSession, user_id: UUID, trip_id: UUID) -> TripPlan:
    trip = await session.scalar(
        select(TripPlan)
        .where(TripPlan.id == trip_id, TripPlan.user_id == user_id)
        .with_for_update()
    )
    if trip is None:
        raise fail("trip_not_found", 404)
    return trip


@router.get("/travel-services/config")
async def public_config(session: Session) -> dict[str, Any]:
    config, _ = await catalog_config(session)
    return config.model_dump(exclude={"airalo_feed_enabled", "hotel_quote_policies"})


@router.get("/travel-services")
async def public_services(
    session: Session,
    locale: RequestLocale,
    destination_id: Annotated[str, Query(max_length=64)],
    type: Kind | None = None,
    hotspot_id: UUID | None = None,
    radius_km: Literal[1, 3, 5] = 3,
    area: Annotated[str | None, Query(max_length=64)] = None,
    facility: Literal["wifi", "breakfast", "accessible", "family", "laundry"] | None = None,
    airport: Annotated[str | None, Query(pattern=r"^[A-Z]{3}$")] = None,
    direction: Literal["arrival", "departure", "roundtrip"] | None = None,
    passengers: Annotated[int | None, Query(ge=1, le=100)] = None,
    language: Locale | None = None,
    days: Annotated[int | None, Query(ge=1, le=365)] = None,
) -> dict[str, Any]:
    center = None
    if hotspot_id:
        hotspot = await session.scalar(
            select(TravelHotspot).where(
                TravelHotspot.id == hotspot_id,
                TravelHotspot.is_active.is_(True),
                TravelHotspot.review_status.in_(("approved", "auto_approved")),
            )
        )
        if (
            not hotspot
            or hotspot.latitude is None
            or hotspot.longitude is None
            or destination_id not in CITIES
        ):
            raise fail("service_destination_mismatch", 404)
        from app.hotspots.discovery import haversine_km

        center = (float(hotspot.latitude), float(hotspot.longitude))
        if haversine_km(*center, *CITIES[destination_id][2]) > 55:
            raise fail("service_destination_mismatch", 404)
    result = await recommendations(
        session,
        await load_runtime_settings(session),
        locale,
        city=destination_id,
        center=center,
        radius=radius_km if center else None,
        area=area,
        facilities=[facility] if facility else None,
        airport=airport,
        direction=direction,
        passengers=passengers,
        language=language,
        days=days,
    )
    if type:
        result["items"] = [p for p in result["items"] if p["kind"] == type]
    return result


@router.get("/trips/{trip_id}/travel-services")
async def trip_services(
    trip_id: UUID,
    user: CurrentUser,
    session: Session,
    locale: RequestLocale,
    destination_id: str | None = None,
    type: Kind | None = None,
    area: str | None = None,
    language: Locale | None = None,
    airport: str | None = None,
    direction: str | None = None,
    passengers: Annotated[int | None, Query(ge=1, le=100)] = None,
) -> dict[str, Any]:
    trip = await locked_trip(session, user.id, trip_id)
    rows = await load_items(session, trip_id)
    cities = trip_destinations(trip, rows)
    if destination_id and destination_id not in cities:
        raise fail("service_destination_mismatch")
    settings = await load_runtime_settings(session)
    days = (trip.end_date - trip.start_date).days + 1 if trip.start_date and trip.end_date else None
    results = [
        await recommendations(
            session,
            settings,
            locale,
            city=city,
            public=False,
            trip=trip,
            rows=rows,
            area=area,
            language=language,
            airport=airport,
            direction=direction,
            passengers=passengers,
            countries=trip_countries(trip, rows),
            days=days,
        )
        for city in ([destination_id] if destination_id else cities)
    ]
    selections = (
        await session.execute(
            select(TripServiceSelection, TravelServiceProduct)
            .join(TravelServiceProduct, TravelServiceProduct.id == TripServiceSelection.product_id)
            .where(TripServiceSelection.trip_id == trip_id)
        )
    ).all()
    return {
        "enabled": any(r["enabled"] for r in results),
        "destinations": cities,
        "enabled_kinds": sorted({kind for r in results for kind in r["enabled_kinds"]}),
        "items": list(
            {
                p["id"]: p for r in results for p in r["items"] if not type or p["kind"] == type
            }.values()
        ),
        "areas": [a for r in results for a in r["areas"]],
        "selections": [
            {
                "id": str(s.id),
                "product_id": str(s.product_id),
                "item_id": str(s.item_id) if s.item_id else None,
                "status": s.status,
                "kind": p.kind,
                "title": p.names_json.get(locale) or p.title,
                "available": p.status == "approved",
                "details": s.details,
            }
            for s, p in selections
        ],
        "version": trip.version,
        "start_date": trip.start_date,
        "end_date": trip.end_date,
        "timezone": trip.timezone,
    }


def validate_schedule(
    payload: SelectInput, trip: TripPlan, rows: list[TripPlanItem], facts: Facts
) -> None:
    if not payload.start_time or not payload.end_time:
        return
    zone = ZoneInfo(trip.timezone)
    start, end = payload.start_time.astimezone(zone), payload.end_time.astimezone(zone)
    if (
        not trip.start_date
        or not trip.end_date
        or not payload.day_date
        or not trip.start_date <= payload.day_date <= trip.end_date
    ):
        raise fail("service_dates_required")
    if start.date() != payload.day_date or end.date() != payload.day_date:
        raise fail("service_dates_required")
    if facts.available_start and (
        start.strftime("%H:%M") < facts.available_start
        or end.strftime("%H:%M") > str(facts.available_end)
    ):
        raise fail("service_time_conflict", 409)
    if facts.duration_minutes and (end - start).total_seconds() < facts.duration_minutes * 60:
        raise fail("service_time_conflict", 409)
    for row in rows:
        if row.is_skipped or row.day_date != payload.day_date:
            continue
        if row.start_time and row.end_time and row.start_time < end and start < row.end_time:
            raise fail("service_time_conflict", 409)


def protected_lodging_item(item: TripPlanItem) -> bool:
    # System anchors are locked to preserve their schedule, not their old hotel identity.
    # Updating their location never changes their date/time; custom locked stops stay intact.
    return bool(
        (item.locked or item.fixed_time)
        and not (
            item.system_role in {"hotel_start", "hotel_end"}
            and item.data.get("source_mode") == "system"
        )
    )


@router.post("/trips/{trip_id}/travel-services")
async def select_service(
    trip_id: UUID, payload: SelectInput, key: OperationKey, user: CurrentUser, session: Session
) -> dict[str, Any]:
    await enforce_named_rate_limit("service-select", str(user.id), limit=60, window_seconds=3600)
    trip = await locked_trip(session, user.id, trip_id)
    digest = fingerprint(payload.model_dump(exclude={"version"}))
    replay = await session.scalar(
        select(TripServiceSelection).where(
            TripServiceSelection.trip_id == trip_id, TripServiceSelection.idempotency_key == key
        )
    )
    if replay:
        if replay.request_hash != digest:
            raise fail("service_operation_conflict", 409)
        return {
            "id": str(replay.id),
            "version": trip.version,
            "status": replay.status,
            "replayed": True,
        }
    if trip.version != payload.version:
        raise fail("trip_version_conflict", 409)
    product = await session.get(TravelServiceProduct, payload.product_id)
    config, _ = await catalog_config(session)
    if not product or product.status != "approved" or not product_enabled(config, product):
        raise fail("service_unavailable", 404)
    rows = await load_items(session, trip.id)
    if not rows:
        # Hydrate inside this transaction; the legacy helper commits and releases our lock.
        for raw_day in trip.data.get("itinerary", []):
            for raw_item in raw_day.get("items", []):
                session.add(
                    item_record(
                        trip.id, ItineraryItem.model_validate(raw_item), preserve_source_id=False
                    )
                )
        await session.flush()
        rows = await load_items(session, trip.id)
    if product.kind != "esim" and product.destination_id not in trip_destinations(trip, rows):
        raise fail("service_destination_mismatch")
    existing = await session.scalar(
        select(TripServiceSelection).where(
            TripServiceSelection.trip_id == trip_id, TripServiceSelection.product_id == product.id
        )
    )
    if existing and product.kind != "hotel" and (existing.item_id or not payload.start_time):
        return {
            "id": str(existing.id),
            "version": trip.version,
            "status": existing.status,
            "replayed": True,
        }
    facts = Facts.model_validate(product.facts)
    require_product_review(product_input(product))
    if product.kind == "esim":
        required_countries = trip_countries(trip, rows)
        days = (
            (trip.end_date - trip.start_date).days + 1
            if trip.start_date and trip.end_date
            else None
        )
        if (
            not required_countries
            or not set(required_countries) <= set(facts.country_codes)
            or days
            and (facts.validity_days is None or facts.validity_days < days)
        ):
            raise fail("service_coverage_required")
    if product.kind == "esim" and payload.start_time:
        raise fail("service_dates_required")
    if product.kind == "transfer" and payload.start_time:
        if (
            not payload.passengers
            or not payload.flight_number
            or payload.airport != facts.airport
            or payload.direction != facts.direction
        ):
            raise fail("service_airport_required")
        if facts.passengers and payload.passengers > facts.passengers:
            raise fail("service_capacity_exceeded")
    selection = existing or TripServiceSelection(
        id=uuid4(),
        trip_id=trip_id,
        product_id=product.id,
        idempotency_key=key,
        request_hash=digest,
        status="planned",
        details=payload.model_dump(mode="json", exclude={"version", "product_id"}),
    )
    selection.idempotency_key = key
    selection.request_hash = digest
    selection.details = payload.model_dump(mode="json", exclude={"version", "product_id"})
    selection.status = "planned"
    changed: set[UUID] = set()
    if product.kind == "hotel":
        if not trip.start_date or not trip.end_date:
            raise fail("service_dates_required")
        protected_values = {
            r.id: {c.name: deepcopy(getattr(r, c.name)) for c in r.__table__.columns}
            for r in rows
            if protected_lodging_item(r)
        }
        ensure_system_slots(session, trip, rows)
        for row in rows:
            for name, value in protected_values.get(row.id, {}).items():
                setattr(row, name, value)
        protected = [r for r in rows if protected_lodging_item(r)]
        editable = [r for r in rows if r not in protected]
        lodging = {
            "name": product.title,
            "location_name": product.title,
            "provider_place_id": facts.google_place_id,
            "latitude": facts.latitude,
            "longitude": facts.longitude,
            "location_source": "manual",
            "coordinate_source_type": "admin_verified",
            "coordinate_source_url": facts.coordinate_source_url,
            "naver_map_url": facts.naver_map_url,
            "map_links": build_map_links(
                name=product.title,
                local_name=None,
                city_name=product.destination_id,
                country_code=CITIES[product.destination_id][0],
                latitude=facts.latitude,
                longitude=facts.longitude,
                google_place_id=facts.google_place_id,
                naver_map_url=facts.naver_map_url,
                map_match_status="verified",
            ),
            "catalog_product_id": str(product.id),
            "area_code": facts.area_code,
            "selection_source": "user",
            "selected_at": datetime.now(UTC).isoformat(),
        }
        changed = sync_primary_lodging(trip, editable, lodging)
        trip.data = {**trip.data, "prices_stale": True}
        for row in editable:
            if row.id in changed:
                row.coordinate_source_type = "admin_verified"
                row.coordinate_source_url = facts.coordinate_source_url
                row.coordinate_verified_at = product.verified_at
    elif payload.start_time and payload.end_time:
        if len(rows) >= 500:
            raise fail("service_capacity_exceeded")
        validate_schedule(payload, trip, rows, facts)
        item = TripPlanItem(
            id=uuid4(),
            trip_plan_id=trip_id,
            # Existing transport rows belong to logistics, not the day timeline.
            item_type="activity",
            title=product.title,
            names_json={"title": product.names_json},
            day_date=payload.day_date,
            start_time=payload.start_time,
            end_time=payload.end_time,
            fixed_time=True,
            locked=False,
            position=max((r.position for r in rows if r.day_date == payload.day_date), default=-1)
            + 1,
            location_name=facts.meeting_point,
            latitude=Decimal(str(facts.latitude)) if facts.latitude is not None else None,
            longitude=Decimal(str(facts.longitude)) if facts.longitude is not None else None,
            coordinate_source_type="admin_verified" if facts.coordinate_source_url else None,
            coordinate_source_url=facts.coordinate_source_url,
            coordinate_verified_at=product.verified_at,
            location_source="manual",
            duration_minutes=int((payload.end_time - payload.start_time).total_seconds() / 60),
            data={
                "service_product_id": str(product.id),
                "service_kind": product.kind,
                "destination_id": product.destination_id,
                "source_mode": "manual",
                "booking_status": "planned",
            },
            is_estimated=False,
            is_skipped=False,
        )
        session.add(item)
        selection.item_id = item.id
        rows.append(item)
        canonicalize_positions(rows)
        changed.add(item.id)
    session.add(selection)
    await session.flush()
    await persist_system_schedule_change(
        session,
        trip,
        user.id,
        payload.version,
        rows,
        warning="service_schedule_changed",
        changed_item_ids=changed,
    )
    return {
        "id": str(selection.id),
        "version": trip.version,
        "status": "planned",
        "replayed": False,
    }


@router.patch("/trips/{trip_id}/travel-services/{selection_id}")
async def selection_status(
    trip_id: UUID, selection_id: UUID, payload: SelectionStatus, user: CurrentUser, session: Session
) -> dict[str, Any]:
    trip = await locked_trip(session, user.id, trip_id)
    selection = await session.scalar(
        select(TripServiceSelection).where(
            TripServiceSelection.id == selection_id, TripServiceSelection.trip_id == trip_id
        )
    )
    if not selection:
        raise fail("service_unavailable", 404)
    if selection.status == payload.status:
        return {"version": trip.version, "status": selection.status}
    if trip.version != payload.version:
        raise fail("trip_version_conflict", 409)
    selection.status = payload.status
    # Booking is self-reported. Neither external clicks nor cancellation rewrites a schedule.
    trip.version += 1
    await session.commit()
    return {"version": trip.version, "status": selection.status}


@router.post("/travel-services/{product_id}/hotel-links/{provider}/clickout", status_code=303)
async def hotel_clickout(
    product_id: UUID, provider: str, session: Session, request: Request
) -> RedirectResponse:
    await enforce_named_rate_limit(
        "hotel-direct-clickout",
        request.headers.get("x-travel-client-ip")
        or (request.client.host if request.client else "unknown"),
        limit=30,
        window_seconds=60,
    )
    product = await session.get(TravelServiceProduct, product_id)
    config, _ = await catalog_config(session)
    if not product:
        raise fail("service_unavailable", 404)
    link = next(
        (
            link
            for link in ready_hotel_links(product, config, datetime.now(UTC))
            if link.provider == provider
        ),
        None,
    )
    if link is None:
        raise fail("service_unavailable", 404)
    from app.travel_services.hotel_options import safe_click_target

    option = next(o for o in product.hotel_options if o.provider == provider)
    await safe_click_target(option)
    # This is not a commission-bearing click, booking or trip mutation.
    return RedirectResponse(
        link.url,
        status_code=303,
        headers={
            "Cache-Control": "no-store",
            "Referrer-Policy": "no-referrer",
        },
    )


@router.post("/travel-services/{product_id}/booking-options/{option_id}/clickout", status_code=303)
async def booking_option_clickout(
    product_id: UUID,
    option_id: UUID,
    session: Session,
    request: Request,
    locale: RequestLocale,
    placement: Literal["destination", "hotspot", "trip", "stay", "checklist"] = "destination",
) -> RedirectResponse:
    from app.travel_services.hotel_options import matching_offer, ready_option, safe_click_target

    await enforce_named_rate_limit(
        "hotel-options",
        request.headers.get("x-travel-client-ip")
        or (request.client.host if request.client else "unknown"),
        limit=60,
        window_seconds=60,
    )
    product = await session.get(TravelServiceProduct, product_id)
    config, _ = await catalog_config(session)
    if not product:
        raise fail("service_unavailable", 404)
    option = next((o for o in product.hotel_options if o.id == option_id), None)
    now = datetime.now(UTC)
    if not option or not ready_option(product, option, config, now):
        raise fail("service_unavailable", 404)
    direct = await safe_click_target(option)
    settings = await load_runtime_settings(session)
    offer = await matching_offer(session, product, option, settings, now)
    target, mode, fallback = direct, "direct", False
    sub_id = f"svc_hotel_{product.destination_id}_{locale}_{placement}"
    if offer:
        brand = await session.get(TravelServiceBrand, offer.brand_id)
        assert brand is not None
        try:
            target = affiliate_click_target(
                brand.code,
                offer.static_url
                or await TravelpayoutsLinkClient(get_redis(), settings).create(
                    direct,
                    sub_id,
                    cache_context=(
                        f"hotel:{option.id}:{option.version}:{brand.id}:{brand.version}:"
                        f"{offer.id}:{offer.version}:{locale}"
                    ),
                )
            )
            mode = "affiliate"
        except (ConnectionError, ValueError, httpx.HTTPError, TimeoutError):
            fallback = True
    if mode == "direct" and not config.direct_hotel_links_enabled:
        raise fail("service_link_unavailable", 503)
    if mode == "affiliate":
        session.add(
            AffiliateClick(
                user_id=None,
                partner="travelpayouts",
                brand=option.provider,
                service_type="hotel",
                placement=placement,
                destination_id=product.destination_id,
                module="hotel",
                sub_id=sub_id,
                destination_summary=product.destination_id,
                target_host=urlsplit(target).hostname or "",
                status="redirected",
            )
        )
    session.add(
        HotelBookingClick(
            option_id=option.id,
            provider=option.provider,
            destination_id=product.destination_id,
            mode=mode,
            fallback=fallback,
            placement=placement,
        )
    )
    await session.commit()
    return RedirectResponse(
        target,
        status_code=303,
        headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"},
    )


@router.post("/travel-services/{product_id}/hotel-quotes")
async def hotel_quotes(
    product_id: UUID,
    payload: HotelQuoteRequest,
    session: Session,
    request: Request,
    locale: RequestLocale,
    response: Response,
) -> dict[str, Any]:
    response.headers["Cache-Control"] = "no-store"
    await enforce_named_rate_limit(
        "hotel-quotes",
        request.headers.get("x-travel-client-ip")
        or (request.client.host if request.client else "unknown"),
        limit=20,
        window_seconds=60,
    )
    product = await session.get(TravelServiceProduct, product_id)
    config, _ = await catalog_config(session)
    if (
        not product
        or product.kind != "hotel"
        or product.status != "approved"
        or not product_enabled(config, product)
    ):
        raise fail("service_unavailable", 404)
    country = CITIES[product.destination_id][0]
    zone = {"JP": "Asia/Tokyo", "KR": "Asia/Seoul", "TW": "Asia/Taipei"}[country]
    if payload.check_in < datetime.now(UTC).astimezone(ZoneInfo(zone)).date():
        raise fail("service_schedule_invalid")
    return await search_quotes(product, payload, locale, config, get_redis())


@router.post("/affiliates/offers/{offer_id}/clickout", status_code=303)
async def offer_clickout(
    offer_id: UUID,
    session: Session,
    locale: RequestLocale,
    request: Request,
    placement: Literal["destination", "hotspot", "trip", "stay", "checklist"] = "destination",
) -> RedirectResponse:
    # Both anonymous and signed-in clicks use a coarse placement code, never a user/trip id.
    await enforce_named_rate_limit(
        "service-clickout",
        request.headers.get("x-travel-client-ip")
        or (request.client.host if request.client else "unknown"),
        limit=120,
        window_seconds=60,
    )
    result = (
        await session.execute(
            select(TravelServiceOffer, TravelServiceBrand, TravelServiceProduct)
            .join(TravelServiceBrand, TravelServiceBrand.id == TravelServiceOffer.brand_id)
            .join(TravelServiceProduct, TravelServiceProduct.id == TravelServiceOffer.product_id)
            .where(TravelServiceOffer.id == offer_id)
        )
    ).first()
    settings = await load_runtime_settings(session)
    config, _ = await catalog_config(session)
    now = datetime.now(UTC)
    if not result:
        raise fail("service_unavailable", 404)
    offer, brand, product = result
    if not product_enabled(config, product) or not ready_offer(
        offer, brand, product, settings, now
    ):
        raise fail("service_unavailable", 404)
    sub_id = f"svc_{product.kind}_{product.destination_id}_{locale}_{placement}"
    try:
        target = offer.static_url or await TravelpayoutsLinkClient(get_redis(), settings).create(
            offer.target_url,
            sub_id,
            cache_context=f"{brand.id}:{brand.version}:{offer.id}:{offer.version}:{locale}",
        )
        target = affiliate_click_target(brand.code, target)
    except (ConnectionError, ValueError) as exc:
        raise fail("service_link_unavailable", 503) from exc
    session.add(
        AffiliateClick(
            user_id=None,
            partner="travelpayouts",
            brand=brand.code,
            service_type=product.kind,
            placement=placement,
            destination_id=product.destination_id,
            module={
                "tour": "activities",
                "transfer": "transport",
                "esim": "connectivity",
                "hotel": "hotel",
            }[product.kind],
            sub_id=sub_id[:64],
            destination_summary=product.destination_id,
            target_host=urlsplit(target).hostname or "",
            status="redirected",
        )
    )
    await session.commit()
    return RedirectResponse(
        target,
        status_code=303,
        headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"},
    )
