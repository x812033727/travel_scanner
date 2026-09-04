import json
from typing import Annotated, Any, cast
from urllib.parse import urlparse
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

from fastapi import APIRouter, Depends
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
)
from app.affiliates.service import (
    AffiliateContext,
    allowed_hosts,
    partner_supports_module,
    resolve_partner_target,
    token_payload,
    validate_target_url,
)
from app.auth.service import CurrentUser
from app.db import get_session
from app.infra import get_redis
from app.models import AffiliateClick, SearchRequest, TripPlan
from app.problems import AppError

router = APIRouter(prefix="/affiliates", tags=["affiliate partners"])
Session = Annotated[AsyncSession, Depends(get_session)]
DISCLOSURE = "透過合作連結預訂，本站可能獲得分潤，價格不因此增加。"


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
) -> tuple[AffiliateContext, str | None, str | None]:
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
        return context, source, None
    trip = await session.scalar(
        select(TripPlan).where(TripPlan.id == trip_id, TripPlan.user_id == user_id)
    )
    if trip is None:
        raise AppError(404, "trip_not_found", "找不到這個旅程")
    source = str(trip.id)
    return (
        AffiliateContext(
            module=module,
            destination=(trip.destination_name or "旅遊目的地")[:128],
            departure_date=trip.start_date.isoformat() if trip.start_date else None,
            return_date=trip.end_date.isoformat() if trip.end_date else None,
            sub_id="",
        ),
        None,
        source,
    )


@router.get("/options", response_model=AffiliateOptionsResponse)
async def affiliate_options(
    module: AffiliateModule,
    user: CurrentUser,
    session: Session,
    search_id: UUID | None = None,
    trip_id: UUID | None = None,
) -> AffiliateOptionsResponse:
    base_context, source_search_id, source_trip_id = await _owned_context(
        session, user.id, module, search_id, trip_id
    )
    settings = await load_runtime_settings(session)
    redis = get_redis()
    source = source_search_id or source_trip_id or "unknown"
    options: list[AffiliateOption] = []
    for partner in partners_for_module(module):
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
                cta=f"到 {partner.display_name} 查看",
                clickout_url=f"/api/travel/affiliates/{partner.code}/clickout?token={token}",
            )
        )
    return AffiliateOptionsResponse(module=module, disclosure=DISCLOSURE, options=options)


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
