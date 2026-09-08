import json
from datetime import UTC, datetime
from typing import Annotated, Any, cast
from urllib.parse import urlparse
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.affiliates.registry import (
    AFFILIATE_PARTNERS,
    PARTNERS_BY_CODE,
    partner_configured,
    partner_enabled,
    partners_for_module,
)
from app.affiliates.schemas import (
    AffiliateModule,
    AffiliateOption,
    AffiliateOptionsResponse,
    AffiliatePartnerStatus,
    DestinationAffiliateOption,
    DestinationAffiliateOptionsResponse,
)
from app.affiliates.service import (
    AffiliateContext,
    TravelpayoutsLinkClient,
    allowed_hosts,
    partner_supports_module,
    resolve_partner_target,
    token_payload,
    validate_target_url,
)
from app.auth.service import CurrentUser, OptionalCurrentUser
from app.db import get_session
from app.destinations.catalog import destination_for_code, destination_for_id, match_destination
from app.i18n import Locale, active_locale
from app.infra import client_ip, enforce_named_rate_limit, get_redis
from app.models import (
    AffiliateClick,
    DestinationAffiliateOffer,
    SearchRequest,
    TravelServiceBrand,
    TripPlan,
)
from app.problems import AppError
from app.travel_services.registry import BRANDS, affiliate_click_target
from app.travel_services.service import catalog_config, ready_destination_offer

router = APIRouter(prefix="/affiliates", tags=["affiliate partners"])
Session = Annotated[AsyncSession, Depends(get_session)]
DISCLOSURE = "透過合作連結預訂，本站可能獲得分潤，價格不因此增加。"
DISCLOSURES: dict[Locale, str] = {
    "en": "We may earn a commission from partner links at no extra cost to you.",
    "ja": "提携リンクから予約された場合、追加料金なしで当サイトに報酬が支払われることがあります。",
    "ko": "제휴 링크로 예약하면 추가 비용 없이 당사에 수수료가 지급될 수 있습니다.",
    "zh-TW": DISCLOSURE,
    "zh-CN": "通过合作链接预订，本站可能获得佣金，价格不会因此增加。",
}


def _destination_id(value: str | None, fallback: str) -> str | None:
    profile = (
        destination_for_id(value)
        or destination_for_code(value)
        or match_destination(fallback)
    )
    return profile.id if profile else None


async def _ready_destination_offers(
    session: AsyncSession,
    settings: Any,
    destination_id: str,
    module: AffiliateModule,
) -> list[tuple[DestinationAffiliateOffer, TravelServiceBrand]]:
    config, _ = await catalog_config(session)
    if not config.public_enabled or destination_id not in config.enabled_destinations:
        return []
    now = datetime.now(UTC)
    rows = list(
        (
            await session.execute(
                select(DestinationAffiliateOffer, TravelServiceBrand)
                .join(
                    TravelServiceBrand,
                    TravelServiceBrand.id == DestinationAffiliateOffer.brand_id,
                )
                .where(
                    DestinationAffiliateOffer.destination_id == destination_id,
                    DestinationAffiliateOffer.module == module,
                )
                .order_by(TravelServiceBrand.code, DestinationAffiliateOffer.id)
            )
        ).tuples().all()
    )
    return [row for row in rows if ready_destination_offer(*row, settings, now)]


def _destination_option(
    offer: DestinationAffiliateOffer,
    brand: TravelServiceBrand,
    locale: Locale,
    *,
    token: str | None = None,
) -> DestinationAffiliateOption:
    definition = BRANDS[brand.code]
    cta = _localized_cta(definition.name, locale)
    suffix = f"?token={token}" if token else ""
    return DestinationAffiliateOption(
        id=str(offer.id),
        brand=brand.code,
        display_name=definition.name,
        destination_id=offer.destination_id,
        module=cast(AffiliateModule, offer.module),
        cta=cta,
        clickout_url=f"/api/travel/affiliates/destination-offers/{offer.id}/clickout{suffix}",
    )


def _localized_cta(name: str, locale: Locale) -> str:
    if locale == "ja":
        return f"{name}で見る"
    if locale == "ko":
        return f"{name}에서 보기"
    if locale == "en":
        return f"View on {name}"
    return f"{'到' if locale == 'zh-TW' else '前往'} {name} 查看"


@router.get("/status", response_model=list[AffiliatePartnerStatus])
async def affiliate_status(session: Session) -> list[AffiliatePartnerStatus]:
    settings = await load_runtime_settings(session)
    return [
        AffiliatePartnerStatus(
            code=partner.code,
            display_name=partner.display_name,
            enabled=partner_enabled(partner, settings),
            configured=partner_configured(partner, settings),
            available=partner_enabled(partner, settings) and partner_configured(partner, settings),
            modules=list(partner.modules),
            capabilities=list(partner.capabilities),
        )
        for partner in AFFILIATE_PARTNERS
    ]


async def _owned_context(
    session: AsyncSession,
    user_id: UUID,
    module: AffiliateModule,
    search_id: UUID | None,
    trip_id: UUID | None,
) -> tuple[AffiliateContext, str | None, str | None, str | None]:
    if (search_id is None) == (trip_id is None):
        raise AppError(422, "affiliate_source_invalid", "請指定搜尋或已儲存旅程")
    if search_id is not None:
        search = await session.scalar(
            select(SearchRequest).where(
                SearchRequest.id == search_id,
                SearchRequest.user_id == user_id,
            )
        )
        if search is None:
            raise AppError(404, "search_not_found", "找不到這次搜尋")
        payload = search.request_json
        destination = str(payload.get("destination") or "旅遊目的地")[:128]
        source = str(search.id)
        context = AffiliateContext(
            module=module,
            destination=destination,
            departure_date=cast(str | None, payload.get("departure_date")),
            return_date=cast(str | None, payload.get("return_date")),
            sub_id="",
        )
        return (
            context,
            source,
            None,
            _destination_id(
                str(payload.get("destination_id") or payload.get("destination_code") or "")
                or None,
                destination,
            ),
        )
    trip = await session.scalar(
        select(TripPlan).where(TripPlan.id == trip_id, TripPlan.user_id == user_id)
    )
    if trip is None:
        raise AppError(404, "trip_not_found", "找不到這個旅程")
    source = str(trip.id)
    destination = (trip.destination_name or "旅遊目的地")[:128]
    return (
        AffiliateContext(
            module=module,
            destination=destination,
            departure_date=trip.start_date.isoformat() if trip.start_date else None,
            return_date=trip.end_date.isoformat() if trip.end_date else None,
            sub_id="",
        ),
        None,
        source,
        _destination_id(str(trip.data.get("destination_id") or "") or None, destination),
    )


@router.get(
    "/destination-offers",
    response_model=DestinationAffiliateOptionsResponse,
)
async def destination_affiliate_options(
    destination_id: str,
    module: AffiliateModule,
    session: Session,
    response: Response,
) -> DestinationAffiliateOptionsResponse:
    response.headers["Cache-Control"] = "no-store"
    profile = destination_for_id(destination_id)
    if not profile:
        raise AppError(404, "affiliate_destination_not_found", "找不到目的地")
    settings = await load_runtime_settings(session)
    locale = active_locale()
    rows = await _ready_destination_offers(session, settings, profile.id, module)
    return DestinationAffiliateOptionsResponse(
        destination_id=profile.id,
        module=module,
        disclosure=DISCLOSURES[locale],
        options=[_destination_option(offer, brand, locale) for offer, brand in rows],
    )


@router.post("/destination-offers/{offer_id}/clickout", status_code=303)
async def destination_affiliate_clickout(
    offer_id: UUID,
    request: Request,
    session: Session,
    user: OptionalCurrentUser,
    token: str | None = None,
) -> RedirectResponse:
    await enforce_named_rate_limit(
        "destination-affiliate-clickout",
        str(user.id) if user else client_ip(request),
        limit=120,
        window_seconds=60,
    )
    result = (
        await session.execute(
            select(DestinationAffiliateOffer, TravelServiceBrand)
            .join(TravelServiceBrand, TravelServiceBrand.id == DestinationAffiliateOffer.brand_id)
            .where(DestinationAffiliateOffer.id == offer_id)
        )
    ).first()
    settings = await load_runtime_settings(session)
    if not result:
        raise AppError(404, "affiliate_offer_not_found", "找不到合作方案")
    offer, brand = result
    if not ready_destination_offer(offer, brand, settings, datetime.now(UTC)):
        raise AppError(404, "affiliate_offer_not_found", "找不到合作方案")
    redis = get_redis()
    source_search_id = source_trip_id = None
    if token:
        raw = await redis.get(f"affiliate:destination-clickout:{token}")
        if not raw:
            raise AppError(409, "affiliate_link_expired", "合作連結已過期，請重新整理")
        try:
            payload = cast(dict[str, Any], json.loads(str(raw)))
        except (json.JSONDecodeError, TypeError) as exc:
            raise AppError(409, "affiliate_link_invalid", "合作連結無效") from exc
        if (
            not user
            or payload.get("user_id") != str(user.id)
            or payload.get("offer_id") != str(offer.id)
        ):
            raise AppError(404, "affiliate_link_not_found", "找不到合作連結")
        source_search_id = payload.get("search_id")
        source_trip_id = payload.get("trip_id")
        await redis.delete(f"affiliate:destination-clickout:{token}")
    locale = active_locale()
    sub_id = f"dst_{offer.module}_{offer.destination_id}_{locale}"
    try:
        target = offer.static_url or await TravelpayoutsLinkClient(redis, settings).create(
            offer.target_url,
            sub_id,
            cache_context=(
                f"destination:{brand.id}:{brand.version}:{offer.id}:{offer.version}:{locale}"
            ),
        )
        target = affiliate_click_target(brand.code, target)
    except (ConnectionError, ValueError) as exc:
        raise AppError(503, "affiliate_link_unavailable", "合作連結暫時無法使用") from exc
    session.add(
        AffiliateClick(
            user_id=user.id if user else None,
            search_id=UUID(source_search_id) if source_search_id else None,
            trip_id=UUID(source_trip_id) if source_trip_id else None,
            offer_id=offer.id,
            partner="travelpayouts",
            brand=brand.code,
            service_type=None,
            placement="destination",
            destination_id=offer.destination_id,
            module=offer.module,
            sub_id=sub_id[:64],
            destination_summary=offer.destination_id,
            target_host=(urlparse(target).hostname or "")[:255],
            status="redirected",
        )
    )
    await session.commit()
    return RedirectResponse(
        target,
        status_code=303,
        headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"},
    )


@router.get("/options", response_model=AffiliateOptionsResponse)
async def affiliate_options(
    module: AffiliateModule,
    user: CurrentUser,
    session: Session,
    search_id: UUID | None = None,
    trip_id: UUID | None = None,
) -> AffiliateOptionsResponse:
    base_context, source_search_id, source_trip_id, destination_id = await _owned_context(
        session, user.id, module, search_id, trip_id
    )
    settings = await load_runtime_settings(session)
    redis = get_redis()
    source = source_search_id or source_trip_id or "unknown"
    options: list[AffiliateOption] = []
    branded_codes: set[str] = set()
    if destination_id:
        for offer, brand in await _ready_destination_offers(
            session, settings, destination_id, module
        ):
            token = uuid4().hex
            await redis.set(
                f"affiliate:destination-clickout:{token}",
                json.dumps(
                    {
                        "offer_id": str(offer.id),
                        "user_id": str(user.id),
                        "search_id": source_search_id,
                        "trip_id": source_trip_id,
                    }
                ),
                ex=settings.affiliate_clickout_token_ttl_seconds,
            )
            localized = _destination_option(offer, brand, active_locale(), token=token)
            options.append(
                AffiliateOption(
                    partner=brand.code,
                    display_name=localized.display_name,
                    module=module,
                    cta=localized.cta,
                    clickout_url=localized.clickout_url,
                )
            )
            branded_codes.add(brand.code)
    for partner in partners_for_module(module):
        if partner.code in branded_codes or (partner.code == "travelpayouts" and branded_codes):
            continue
        if not partner_supports_module(partner, module, settings):
            continue
        sub_id = uuid5(
            NAMESPACE_URL,
            f"travel-scanner:affiliate:{user.id}:{source}:{partner.code}:{module}",
        ).hex
        context = AffiliateContext(
            module=base_context.module,
            destination=base_context.destination,
            departure_date=base_context.departure_date,
            return_date=base_context.return_date,
            sub_id=sub_id,
        )
        try:
            target = await resolve_partner_target(partner, context, settings, redis)
        except (ConnectionError, ValueError):
            continue
        token = uuid4().hex
        await redis.set(
            f"affiliate:clickout:{token}",
            token_payload(
                target=target,
                user_id=str(user.id),
                partner=partner.code,
                module=module,
                sub_id=sub_id,
                destination=context.destination,
                search_id=source_search_id,
                trip_id=source_trip_id,
            ),
            ex=settings.affiliate_clickout_token_ttl_seconds,
        )
        options.append(
            AffiliateOption(
                partner=partner.code,
                display_name=partner.display_name,
                module=module,
                cta=_localized_cta(partner.display_name, active_locale()),
                clickout_url=f"/api/travel/affiliates/{partner.code}/clickout?token={token}",
            )
        )
    return AffiliateOptionsResponse(
        module=module,
        disclosure=DISCLOSURES[active_locale()],
        options=options,
    )


@router.post("/{partner}/clickout", status_code=303)
async def affiliate_clickout(
    partner: str,
    token: str,
    user: CurrentUser,
    session: Session,
) -> RedirectResponse:
    definition = PARTNERS_BY_CODE.get(partner)
    if definition is None:
        raise AppError(404, "affiliate_partner_not_found", "找不到合作平台")
    redis = get_redis()
    raw = await redis.get(f"affiliate:clickout:{token}")
    if not raw:
        raise AppError(409, "affiliate_link_expired", "合作連結已過期，請重新整理")
    try:
        payload = cast(dict[str, Any], json.loads(str(raw)))
    except (json.JSONDecodeError, TypeError) as exc:
        raise AppError(409, "affiliate_link_invalid", "合作連結無效") from exc
    if payload.get("user_id") != str(user.id) or payload.get("partner") != partner:
        raise AppError(404, "affiliate_link_not_found", "找不到合作連結")
    settings = await load_runtime_settings(session)
    try:
        target = validate_target_url(
            str(payload.get("target") or ""), allowed_hosts(settings, definition)
        )
    except ValueError as exc:
        raise AppError(409, "affiliate_link_invalid", "合作連結無效") from exc
    await redis.delete(f"affiliate:clickout:{token}")
    session.add(
        AffiliateClick(
            user_id=user.id,
            search_id=UUID(payload["search_id"]) if payload.get("search_id") else None,
            trip_id=UUID(payload["trip_id"]) if payload.get("trip_id") else None,
            partner=partner,
            module=str(payload.get("module") or "unknown"),
            sub_id=str(payload.get("sub_id") or "")[:64],
            destination_summary=str(payload.get("destination") or "旅遊目的地")[:128],
            target_host=(urlparse(target).hostname or "")[:255],
            status="redirected",
        )
    )
    await session.commit()
    return RedirectResponse(target, status_code=303)
