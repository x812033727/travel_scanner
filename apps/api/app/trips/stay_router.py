"""Stay-area recommendation, per-area hotel comparison, selection and partner click-outs."""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Annotated, Any, cast
from urllib.parse import urlparse
from uuid import NAMESPACE_URL, UUID, uuid5

from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.affiliates.registry import PARTNERS_BY_CODE
from app.affiliates.router import DISCLOSURE
from app.affiliates.service import (
    AffiliateContext,
    _with_query,
    allowed_hosts,
    partner_supports_module,
    resolve_partner_target,
    validate_target_url,
)
from app.auth.service import CurrentUser
from app.config import Settings
from app.crawlers.fx import FxRateProvider
from app.db import get_session
from app.destinations.catalog import DestinationProfile
from app.hotspots.areas import HotspotArea, area_name, resolve_area
from app.i18n import Locale, current_locale
from app.infra import enforce_named_rate_limit, get_redis
from app.models import AffiliateClick, SearchRequest, TripPlan, TripPlanItem
from app.problems import AppError
from app.providers.registry import build_hotel_provider, hotel_provider_status
from app.providers.runner import ProviderRunner, ProviderUnavailableError
from app.providers.schemas import HotelOffer, SourceMode
from app.search.schemas import SearchCreate
from app.trips.router import (
    hydrate_legacy_items,
    load_items,
    owned_trip,
    persist_system_schedule_change,
)
from app.trips.schedule import primary_lodging, sync_primary_lodging
from app.trips.stay_areas import (
    STAY_PARTNER_ORDER,
    StayDates,
    area_offers_cache_key,
    area_summary,
    booking_deep_link,
    evidence_items,
    extension_destination_ids,
    find_area,
    hotel_payload,
    normalize_offers,
    offers_cache_ttl,
    rank_area_offers,
    score_stay_areas,
    split_area_offers,
    stay_dates,
    stay_partner_options,
    stay_search_query,
    trim_offer,
    trip_city,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/trips/{trip_id}/stay-areas", tags=["trips"])
Session = Annotated[AsyncSession, Depends(get_session)]
RequestLocale = Annotated[Locale, Depends(current_locale)]
AreaCode = Annotated[str, Path(pattern=r"^[a-z0-9-]{1,32}$")]
STAY_AREAS_USER_LIMIT = 120
STAY_HOTELS_USER_LIMIT = 60
STAY_PROVIDER_TRIP_LIMIT = 20
STAY_SELECT_USER_LIMIT = 10
STAY_CLICKOUT_USER_LIMIT = 120
STAY_WINDOW_SECONDS = 3_600
LODGING_WARNING = "主要飯店已更新，請重新計算每日來回路線。"


class StayHotelSelectRequest(BaseModel):
    version: int = Field(ge=1)
    provider: str = Field(min_length=1, max_length=32)
    hotel_id: str = Field(min_length=1, max_length=64)


@dataclass
class StayContext:
    trip: TripPlan
    rows: list[TripPlanItem]
    search_json: dict[str, Any] | None
    profile: DestinationProfile | None
    city_code: str | None
    settings: Settings

    @property
    def destination_label(self) -> str:
        if self.trip.destination_name:
            return self.trip.destination_name
        if self.profile is not None:
            return self.profile.city
        return self.city_code or "旅遊目的地"


@dataclass
class AreaSearch:
    status: str
    provider: str | None = None
    offers: list[HotelOffer] | None = None
    retrieved_at: datetime | None = None
    expires_at: datetime | None = None
    cached: bool = False
    message: str | None = None
    is_fallback: bool = False

    @property
    def rows(self) -> list[HotelOffer]:
        return self.offers or []


async def _load_context(session: AsyncSession, user_id: UUID, trip_id: UUID) -> StayContext:
    trip = await owned_trip(session, user_id, trip_id)
    rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    search_json: dict[str, Any] | None = None
    if trip.search_id is not None:
        search = await session.get(SearchRequest, trip.search_id)
        if search is not None and isinstance(search.request_json, dict):
            search_json = search.request_json
    profile, city_code = trip_city(trip, search_json)
    return StayContext(
        trip=trip,
        rows=rows,
        search_json=search_json,
        profile=profile,
        city_code=city_code,
        settings=await load_runtime_settings(session),
    )


def _require_area(context: StayContext, area_code: str) -> HotspotArea:
    if context.city_code is None:
        raise AppError(422, "unsupported_destination", "目前不支援這個目的地的住宿熱區")
    area = find_area(context.city_code, area_code)
    if area is None:
        raise AppError(422, "unsupported_area", "這個目的地沒有這個區域")
    return area


def _pricing_availability(settings: Settings) -> dict[str, Any]:
    status = hotel_provider_status(settings)
    return {
        "available": status.available,
        "provider": status.selected_provider if status.available else None,
        "mode": status.mode,
        "message": None if status.available else status.message,
    }


@router.get("")
async def stay_areas(
    trip_id: UUID, user: CurrentUser, session: Session, locale: RequestLocale
) -> dict[str, Any]:
    await enforce_named_rate_limit(
        "trip-stay-areas-user",
        str(user.id),
        limit=STAY_AREAS_USER_LIMIT,
        window_seconds=STAY_WINDOW_SECONDS,
    )
    context = await _load_context(session, user.id, trip_id)
    trip = context.trip
    payload: dict[str, Any] = {
        "trip_id": str(trip.id),
        "version": trip.version,
        "destination_name": context.destination_label,
        "city_code": context.city_code,
        "pricing": _pricing_availability(context.settings),
        "current_lodging_area_code": None,
        "located_item_count": 0,
        "unassigned_item_count": 0,
        "excluded_extension": {},
        "warnings": [],
        "areas": [],
    }
    if context.city_code is None:
        return {**payload, "status": "unsupported"}
    lodging = primary_lodging(trip, context.rows)
    current_area = (
        resolve_area(context.city_code, lodging.get("latitude"), lodging.get("longitude"))
        if lodging
        else None
    )
    items, excluded = evidence_items(
        context.rows,
        context.city_code,
        extension_destination_ids(trip, context.search_json),
    )
    recommendation = score_stay_areas(
        context.city_code,
        items,
        excluded_extension=excluded,
        current_lodging_area=current_area,
    )
    return {
        **payload,
        "status": recommendation.status,
        "current_lodging_area_code": current_area.code if current_area else None,
        "located_item_count": recommendation.located_item_count,
        "unassigned_item_count": recommendation.unassigned_item_count,
        "excluded_extension": recommendation.excluded_extension,
        "warnings": recommendation.warnings,
        "areas": [area_summary(score, locale) for score in recommendation.areas],
    }


def _serialize_search(search: AreaSearch) -> str:
    return json.dumps(
        {
            "status": search.status,
            "provider": search.provider,
            "retrieved_at": search.retrieved_at.isoformat() if search.retrieved_at else None,
            "expires_at": search.expires_at.isoformat() if search.expires_at else None,
            "is_fallback": search.is_fallback,
            "offers": [offer.model_dump(mode="json") for offer in search.rows],
        }
    )


def _deserialize_search(raw: str) -> AreaSearch:
    data = cast(dict[str, Any], json.loads(raw))
    return AreaSearch(
        status=str(data.get("status") or "empty"),
        provider=data.get("provider"),
        offers=[HotelOffer.model_validate(item) for item in data.get("offers", [])],
        retrieved_at=(
            datetime.fromisoformat(data["retrieved_at"]) if data.get("retrieved_at") else None
        ),
        expires_at=datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None,
        cached=True,
        is_fallback=bool(data.get("is_fallback")),
    )


async def _search_area(
    context: StayContext,
    area: HotspotArea,
    query: SearchCreate,
    *,
    refresh: bool = False,
) -> AreaSearch:
    settings = context.settings
    status = hotel_provider_status(settings)
    redis = get_redis()
    provider = build_hotel_provider(redis, settings)
    if provider is None:
        return AreaSearch("not_configured", message=status.message)
    environment = str(getattr(provider, "source_mode", SourceMode.MOCK))
    key = area_offers_cache_key(
        provider.name, environment, context.city_code or "", area.code, query
    )
    if refresh:
        await redis.delete(key)
    else:
        cached = await redis.get(key)
        if cached:
            return _deserialize_search(str(cached))
    await enforce_named_rate_limit(
        "trip-stay-hotels-provider-trip",
        str(context.trip.id),
        limit=STAY_PROVIDER_TRIP_LIMIT,
        window_seconds=STAY_WINDOW_SECONDS,
    )
    runner = ProviderRunner(redis, settings)
    timeout = settings.hotel_area_search_timeout_seconds
    started = time.monotonic()
    is_fallback = False
    selected = provider
    try:
        offers = await runner.run(
            provider.name,
            "hotel",
            lambda: provider.search_hotels_near(
                query,
                latitude=area.latitude,
                longitude=area.longitude,
                radius_km=area.radius_km,
            ),
            timeout_seconds=timeout,
        )
    except ProviderUnavailableError as exc:
        fallback = (
            build_hotel_provider(redis, settings, provider_name=status.fallback_provider)
            if status.fallback_provider
            else None
        )
        if fallback is None:
            failure = "timeout" if isinstance(exc.__cause__, TimeoutError) else "unavailable"
            logger.warning(
                "stay_area_hotels provider=%s area=%s status=%s", provider.name, area.code, failure
            )
            return AreaSearch(failure, provider=provider.name, message=str(exc))
        try:
            offers = await runner.run(
                fallback.name,
                "hotel",
                lambda: fallback.search_hotels_near(
                    query,
                    latitude=area.latitude,
                    longitude=area.longitude,
                    radius_km=area.radius_km,
                ),
                timeout_seconds=timeout,
            )
        except ProviderUnavailableError as fallback_exc:
            return AreaSearch("unavailable", provider=provider.name, message=str(fallback_exc))
        is_fallback, selected = True, fallback
    now = datetime.now(UTC)
    normalized = await normalize_offers(offers, FxRateProvider(settings, redis))
    rows = [
        trim_offer(offer.model_copy(update={"is_fallback": True}) if is_fallback else offer)
        for offer in normalized
    ]
    result = AreaSearch(
        status=str(rows[0].source_mode) if rows else "empty",
        provider=selected.name,
        offers=rows,
        retrieved_at=now,
        expires_at=min((offer.expires_at for offer in rows), default=None),
        is_fallback=is_fallback,
    )
    await redis.set(key, _serialize_search(result), ex=offers_cache_ttl(rows, now))
    logger.info(
        "stay_area_hotels trip=%s city=%s area=%s provider=%s status=%s offers=%d latency_ms=%d",
        context.trip.id,
        context.city_code,
        area.code,
        selected.name,
        result.status,
        len(rows),
        int((time.monotonic() - started) * 1000),
    )
    return result


async def _cached_offer(
    context: StayContext,
    area: HotspotArea,
    query: SearchCreate,
    provider: str | None,
    hotel_id: str,
) -> HotelOffer | None:
    def find(search: AreaSearch) -> HotelOffer | None:
        return next(
            (
                offer
                for offer in search.rows
                if offer.hotel_id == hotel_id and (provider is None or offer.provider == provider)
            ),
            None,
        )

    search = await _search_area(context, area, query)
    offer = find(search)
    if offer is None and search.cached:
        # The member may be acting on a comparison older than the cache entry.
        offer = find(await _search_area(context, area, query, refresh=True))
    return offer


@router.get("/{area_code}/hotels")
async def stay_area_hotels(
    trip_id: UUID,
    area_code: AreaCode,
    user: CurrentUser,
    session: Session,
    locale: RequestLocale,
    refresh: bool = False,
) -> dict[str, Any]:
    await enforce_named_rate_limit(
        "trip-stay-hotels-user",
        str(user.id),
        limit=STAY_HOTELS_USER_LIMIT,
        window_seconds=STAY_WINDOW_SECONDS,
    )
    context = await _load_context(session, user.id, trip_id)
    trip, settings = context.trip, context.settings
    area = _require_area(context, area_code)
    area_label = area_name(area, locale)
    dates = stay_dates(trip)
    lodging = primary_lodging(trip, context.rows) or {}
    payload: dict[str, Any] = {
        "trip_id": str(trip.id),
        "version": trip.version,
        "destination_name": context.destination_label,
        "area": {
            "code": area.code,
            "name": area_label,
            "latitude": area.latitude,
            "longitude": area.longitude,
            "radius_km": area.radius_km,
        },
        "check_in": dates.check_in.isoformat() if dates.check_in else None,
        "check_out": dates.check_out.isoformat() if dates.check_out else None,
        "nights": dates.nights,
        "date_notes": list(dates.notes),
        "warnings": [],
        "filters": {"applied": {}, "relaxed": [], "excluded_by_hard_filter": 0},
        "hotels": [],
        "nearby": [],
        "area_partners": stay_partner_options(settings, area_label, None),
        "disclosure": DISCLOSURE,
    }
    if dates.status != "ready":
        return {
            **payload,
            "travelers": None,
            "pricing": {"status": dates.status, "provider": None, "message": None},
        }
    query = stay_search_query(
        trip, cast(str, context.city_code), context.search_json, dates, locale
    )
    travelers = query.travelers
    warnings: list[str] = []
    if travelers.children and not travelers.children_ages:
        warnings.append("children_ages_missing")
    search = await _search_area(context, area, query, refresh=refresh)
    in_area, nearby = split_area_offers(area, search.rows)
    ranked = rank_area_offers(in_area, query.preferences, travelers)
    current_hotel_id = str(lodging.get("hotel_id") or "")
    current_provider = str(lodging.get("provider") or "")

    def is_current(offer: HotelOffer) -> bool:
        return bool(current_hotel_id) and (
            offer.hotel_id == current_hotel_id and offer.provider == current_provider
        )

    preference_keys = {"breakfast_required", "refundable_required", "accepted_property_types"}
    applied = {
        key: value
        for key, value in query.preferences.model_dump(mode="json").items()
        if (key.startswith("hotel_") or key in preference_keys) and value not in (None, False, [])
    }
    return {
        **payload,
        "travelers": {
            "adults": travelers.adults,
            "children": travelers.children,
            "rooms": travelers.rooms,
        },
        "warnings": warnings,
        "pricing": {
            "status": search.status,
            "provider": search.provider,
            "message": search.message,
            "retrieved_at": search.retrieved_at.isoformat() if search.retrieved_at else None,
            "expires_at": search.expires_at.isoformat() if search.expires_at else None,
            "cached": search.cached,
            "is_fallback": search.is_fallback,
        },
        "filters": {
            "applied": applied,
            "relaxed": [
                {"code": constraint.code, "label": constraint.label}
                for constraint in ranked.filters.relaxed
            ],
            "excluded_by_hard_filter": ranked.filters.excluded_by_hard_filter,
        },
        "hotels": [
            hotel_payload(
                candidate,
                gaps=ranked.filters.gaps.get(candidate.offer.id, []),
                is_current_lodging=is_current(candidate.offer),
                partners=stay_partner_options(settings, area_label, candidate.offer),
            )
            for candidate in ranked.hotels
        ],
        "nearby": [
            hotel_payload(
                candidate,
                gaps=[],
                is_current_lodging=is_current(candidate.offer),
                partners=stay_partner_options(settings, area_label, candidate.offer),
            )
            for candidate in nearby
        ],
    }


@router.post("/{area_code}/select")
async def select_stay_hotel(
    trip_id: UUID,
    area_code: AreaCode,
    payload: StayHotelSelectRequest,
    user: CurrentUser,
    session: Session,
    locale: RequestLocale,
) -> dict[str, Any]:
    await enforce_named_rate_limit(
        "trip-stay-select-user",
        str(user.id),
        limit=STAY_SELECT_USER_LIMIT,
        window_seconds=STAY_WINDOW_SECONDS,
    )
    context = await _load_context(session, user.id, trip_id)
    trip = context.trip
    area = _require_area(context, area_code)
    dates = stay_dates(trip)
    if dates.status != "ready":
        raise AppError(422, "trip_dates_required", "請先設定旅程日期，才能依日期選擇飯店")
    query = stay_search_query(
        trip, cast(str, context.city_code), context.search_json, dates, locale
    )
    offer = await _cached_offer(context, area, query, payload.provider, payload.hotel_id)
    if offer is None:
        raise AppError(409, "hotel_offer_expired", "這筆報價已過期，請重新整理飯店比價後再選擇")
    lodging = {
        "name": offer.hotel_name,
        "location_name": offer.address or offer.hotel_name,
        "provider_place_id": None,
        "latitude": offer.latitude,
        "longitude": offer.longitude,
        "location_source": "provider",
        "offer_id": str(offer.id),
        "provider": offer.provider,
        "hotel_id": offer.hotel_id,
        "area_code": area.code,
        "selection_source": "user",
        "selected_at": datetime.now(UTC).isoformat(),
        "price_snapshot": {
            "nightly_price": str(offer.nightly_price or offer.total_price / max(1, offer.nights)),
            "total_price": str(offer.total_price),
            "currency": offer.currency,
            "nights": offer.nights,
            "retrieved_at": offer.retrieved_at.isoformat(),
            "expires_at": offer.expires_at.isoformat(),
        },
    }
    changed_rows = sync_primary_lodging(trip, context.rows, lodging)
    return await persist_system_schedule_change(
        session,
        trip,
        user.id,
        payload.version,
        context.rows,
        warning=LODGING_WARNING,
        changed_item_ids=changed_rows,
    )


@router.post("/{area_code}/clickout", status_code=303)
async def stay_area_clickout(
    trip_id: UUID,
    area_code: AreaCode,
    partner: str,
    user: CurrentUser,
    session: Session,
    locale: RequestLocale,
    hotel_id: Annotated[str | None, Query(max_length=64)] = None,
) -> RedirectResponse:
    await enforce_named_rate_limit(
        "trip-stay-clickout-user",
        str(user.id),
        limit=STAY_CLICKOUT_USER_LIMIT,
        window_seconds=STAY_WINDOW_SECONDS,
    )
    if partner not in STAY_PARTNER_ORDER:
        raise AppError(404, "affiliate_partner_not_found", "找不到合作平台")
    definition = PARTNERS_BY_CODE[partner]
    context = await _load_context(session, user.id, trip_id)
    trip, settings = context.trip, context.settings
    area = _require_area(context, area_code)
    area_label = area_name(area, locale)
    dates = stay_dates(trip)
    offer: HotelOffer | None = None
    if hotel_id and dates.status == "ready":
        query = stay_search_query(
            trip, cast(str, context.city_code), context.search_json, dates, locale
        )
        offer = await _cached_offer(context, area, query, None, hotel_id)
    sub_id = uuid5(
        NAMESPACE_URL,
        f"travel-scanner:affiliate:{user.id}:{trip.id}:{partner}:hotel:{area.code}",
    ).hex
    affiliate_context = AffiliateContext(
        module="hotel",
        destination=context.destination_label,
        departure_date=dates.check_in.isoformat() if dates.check_in else None,
        return_date=dates.check_out.isoformat() if dates.check_out else None,
        sub_id=sub_id,
        area=area_label,
        hotel_name=offer.hotel_name if offer else None,
    )
    redis = get_redis()
    try:
        deep_link = booking_deep_link(offer) if partner == "booking" else None
        if deep_link is not None:
            target = validate_target_url(
                _with_query(deep_link, "aid", settings.booking_demand_effective_affiliate_id),
                {"booking.com"} | allowed_hosts(settings, definition),
            )
        else:
            if not partner_supports_module(definition, "hotel", settings):
                raise AppError(404, "affiliate_partner_not_found", "找不到合作平台")
            target = await resolve_partner_target(definition, affiliate_context, settings, redis)
    except (ConnectionError, ValueError) as exc:
        raise AppError(409, "affiliate_link_invalid", "合作連結無效") from exc
    session.add(
        AffiliateClick(
            user_id=user.id,
            search_id=None,
            trip_id=trip.id,
            offer_id=offer.id if offer else None,
            partner=partner,
            module="hotel",
            sub_id=sub_id[:64],
            destination_summary=f"{context.destination_label}／{area_label}"[:128],
            target_host=(urlparse(target).hostname or "")[:255],
            status="redirected",
        )
    )
    await session.commit()
    return RedirectResponse(target, status_code=303)


__all__ = ["StayDates", "router"]
