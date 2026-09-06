import asyncio
import logging
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import Annotated, Any, cast
from urllib.parse import urlparse
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Header
from fastapi.responses import RedirectResponse, StreamingResponse
from pydantic import ValidationError
from redis import Redis as SyncRedis
from rq import Queue
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import CurrentUser
from app.config import get_settings
from app.db import get_session
from app.infra import enforce_rate_limit, get_redis
from app.models import (
    AffiliateClick,
    FlightOfferRecord,
    ProviderRequest,
    ProviderResponse,
    SearchJob,
    SearchRequest,
    UsageReservation,
)
from app.problems import AppError
from app.providers.base import FlightProvider
from app.providers.flight_keys import ensure_itinerary_key
from app.providers.flightaware import FlightAwareProvider
from app.providers.registry import (
    build_flight_provider,
    build_module_provider_candidates,
    provider_status_for_modules,
)
from app.providers.runner import ProviderRunner, ProviderUnavailableError
from app.providers.schemas import FlightOffer
from app.search.events import stream_key
from app.search.schemas import SearchCreate
from app.usage.service import (
    release_reservation,
    reserve_use,
    search_operation,
    search_summary,
    usage_status,
)

router = APIRouter(tags=["search"])
Session = Annotated[AsyncSession, Depends(get_session)]
logger = logging.getLogger(__name__)


@router.post("/searches", status_code=202)
async def create_search(
    payload: SearchCreate,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    settings = await load_runtime_settings(session)
    status = provider_status_for_modules([str(module) for module in payload.modules], settings)
    if status.status != "ready":
        raise AppError(503, "provider_not_configured", status.message)
    await enforce_rate_limit(user.id)
    payload_json = payload.model_dump(mode="json")
    operation = search_operation(payload_json)
    reservation, created = await reserve_use(
        session, user.id, idempotency_key, operation, search_summary(payload_json)
    )
    if not created and reservation.resource_id:
        existing = await session.get(SearchRequest, reservation.resource_id)
        if existing:
            return {
                "search_id": str(existing.id),
                "status": existing.status,
                "progress": existing.progress,
                "usage": usage_status(reservation).model_dump(),
            }
    search = SearchRequest(user_id=user.id, operation=operation, request_json=payload_json)
    session.add(search)
    await session.flush()
    reservation.resource_id = search.id
    job = SearchJob(search_id=search.id)
    session.add(job)
    await session.commit()
    try:
        connection = SyncRedis.from_url(get_settings().redis_url)
        queued = Queue("search", connection=connection).enqueue(
            "app.search.tasks.run_search_job", str(search.id), job_timeout=120
        )
        job.queue_job_id = queued.id
        await session.commit()
    except Exception as exc:
        await release_reservation(session, reservation, "queue_unavailable")
        search.status = "failed"
        job.status = "failed"
        job.error = "Queue unavailable"
        await session.commit()
        raise AppError(
            503, "queue_unavailable", "The search queue is temporarily unavailable"
        ) from exc
    return {
        "search_id": str(search.id),
        "status": "processing",
        "progress": 0,
        "usage": usage_status(reservation).model_dump(),
    }


@router.get("/searches/{search_id}")
async def get_search(search_id: UUID, user: CurrentUser, session: Session) -> dict[str, Any]:
    search = await session.scalar(
        select(SearchRequest).where(SearchRequest.id == search_id, SearchRequest.user_id == user.id)
    )
    if search is None:
        raise AppError(404, "search_not_found", "找不到這次搜尋")
    reservation = await session.scalar(
        select(UsageReservation).where(UsageReservation.resource_id == search.id)
    )
    return {
        "search_id": str(search.id),
        "status": search.status,
        "progress": search.progress,
        "request": search.request_json,
        "result": search.result_json,
        "warnings": search.warnings_json,
        "usage": usage_status(reservation).model_dump() if reservation else None,
    }


@router.get("/searches/{search_id}/events")
async def search_events(
    search_id: UUID,
    user: CurrentUser,
    session: Session,
    last_event_id: Annotated[str | None, Header(alias="Last-Event-ID")] = None,
) -> StreamingResponse:
    owned = await session.scalar(
        select(SearchRequest.id).where(
            SearchRequest.id == search_id, SearchRequest.user_id == user.id
        )
    )
    if owned is None:
        raise AppError(404, "search_not_found", "找不到這次搜尋")

    async def generate() -> AsyncIterator[str]:
        redis, cursor = get_redis(), last_event_id or "0-0"
        idle = 0
        while idle < 30:
            batches = cast(
                list[Any], await redis.xread({stream_key(search_id): cursor}, count=20, block=15000)
            )
            if not batches:
                idle += 1
                yield ": keep-alive\n\n"
                continue
            idle = 0
            for _, entries in batches:
                for event_id, fields in entries:
                    cursor = str(event_id)
                    yield f"id: {cursor}\nevent: {fields['event']}\ndata: {fields['data']}\n\n"
                    if fields["event"] in ("search.completed", "search.failed"):
                        return
            await asyncio.sleep(0)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/offers/{offer_id}/refresh")
async def refresh_offer(offer_id: UUID, user: CurrentUser, session: Session) -> dict[str, Any]:
    records = list(
        (
            await session.scalars(
                select(FlightOfferRecord)
                .join(SearchRequest, SearchRequest.id == FlightOfferRecord.search_id)
                .where(SearchRequest.user_id == user.id)
            )
        ).all()
    )
    record = next((item for item in records if item.data.get("id") == str(offer_id)), None)
    if record is None:
        raise AppError(404, "offer_not_found", "找不到這筆報價")
    search = await session.get(SearchRequest, record.search_id)
    assert search is not None
    provider = build_flight_provider(
        get_redis(), await load_runtime_settings(session), provider_name=record.provider
    )
    if provider is None:
        raise AppError(503, "provider_unavailable", "原始航班供應商目前無法使用")
    offer = _stored_offer(record)
    try:
        try:
            original_query = SearchCreate.model_validate(search.request_json)
        except ValueError:
            original_query = None
        result = await provider.refresh_offer(offer, original_query)
    except ConnectionError as exc:
        logger.warning("Offer refresh failed for provider %s: %s", record.provider, exc)
        raise AppError(
            503, "provider_unavailable", "原始航班供應商目前無法回應，請稍後再試"
        ) from exc
    if result.offer is not None:
        updated = result.offer.model_copy(update={"id": offer.id})
        record.data = updated.model_dump(mode="json")
        record.total_price = updated.total_price
        record.currency = updated.currency
        record.expires_at = updated.expires_at
        modules = search.result_json.get("modules", {})
        modules["flight"] = [
            updated.model_dump(mode="json") if item.get("id") == str(offer_id) else item
            for item in modules.get("flight", [])
        ]
        search.result_json = {**search.result_json, "modules": modules}
    await session.commit()
    return result.model_dump(mode="json", exclude={"offer"})


async def _owned_search(search_id: UUID, user: CurrentUser, session: AsyncSession) -> SearchRequest:
    search = await session.scalar(
        select(SearchRequest).where(SearchRequest.id == search_id, SearchRequest.user_id == user.id)
    )
    if search is None:
        raise AppError(404, "search_not_found", "找不到這次搜尋")
    return search


def _stored_query(search: SearchRequest) -> SearchCreate:
    """The query a search was run with, or 409 if this row was never that kind of search.

    Two routers write ``SearchRequest.request_json`` and they write different shapes: this
    one stores a ``SearchCreate``, while the live back-to-back fare endpoint stores its own
    payload, which has no modules and no dates and so can never validate here. Ownership is
    the only thing ``_owned_search`` checks, so without this the mismatch reached a bare
    ``model_validate`` and left as a 500.
    """
    try:
        return SearchCreate.model_validate(search.request_json)
    except ValidationError as exc:
        raise AppError(
            409, "search_not_expandable", "這次搜尋不是可以再擴充航班來源的類型"
        ) from exc


def _stored_offers(search: SearchRequest) -> list[FlightOffer]:
    """The flight offers saved with a search, as a readable conflict when they no longer parse."""
    try:
        return [
            ensure_itinerary_key(FlightOffer.model_validate(item))
            for item in search.result_json.get("modules", {}).get("flight", [])
        ]
    except ValidationError as exc:
        raise AppError(
            409, "search_offers_unreadable", "這次搜尋存下來的航班報價已無法讀取"
        ) from exc


def _stored_offer(record: FlightOfferRecord) -> FlightOffer:
    """One saved offer. A row this service wrote itself, so failing to read it is a conflict."""
    try:
        return FlightOffer.model_validate(record.data)
    except ValidationError as exc:
        raise AppError(409, "offer_unreadable", "這筆報價已無法讀取") from exc


@router.post("/searches/{search_id}/flight-sources/expand")
async def expand_flight_sources(
    search_id: UUID,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    search = await _owned_search(search_id, user, session)
    query = _stored_query(search)
    redis = get_redis()
    replay_key = f"search:{search_id}:flight-expand:{idempotency_key}"
    if await redis.exists(replay_key):
        return {
            "search_id": str(search.id),
            "replayed": True,
            "offers": search.result_json.get("modules", {}).get("flight", []),
            "provider_statuses": search.result_json.get("provider_statuses", {}).get("flight", []),
        }
    settings = await load_runtime_settings(session)
    candidates = build_module_provider_candidates(redis, settings).get("flight", [])
    tried_rows = list(
        (
            await session.scalars(
                select(ProviderRequest).where(
                    ProviderRequest.search_id == search.id,
                    ProviderRequest.module == "flight",
                )
            )
        ).all()
    )
    tried = {name for row in tried_rows for name in row.provider.split(",") if name}
    existing = _stored_offers(search)
    by_source = {(item.provider, item.provider_offer_id): item for item in existing}
    attempts: list[dict[str, Any]] = list(
        search.result_json.get("provider_statuses", {}).get("flight", [])
    )
    runner = ProviderRunner(redis, settings)
    for provider in candidates:
        name = str(getattr(provider, "name", "unknown"))
        if name in tried:
            continue
        started = datetime.now(UTC)
        try:
            flight_provider = cast(FlightProvider, provider)

            async def fetch_offers(
                selected: FlightProvider = flight_provider,
            ) -> list[FlightOffer]:
                return await selected.search_flights(query)

            offers = await runner.run(name, "flight", fetch_offers)
            for offer in offers:
                normalized = ensure_itinerary_key(offer)
                by_source[(normalized.provider, normalized.provider_offer_id)] = normalized
                session.add(
                    FlightOfferRecord(
                        search_id=search.id,
                        provider=normalized.provider,
                        provider_offer_id=normalized.provider_offer_id,
                        public_offer_id=normalized.id,
                        data=normalized.model_dump(mode="json"),
                        total_price=normalized.total_price,
                        currency=normalized.currency,
                        expires_at=normalized.expires_at,
                    )
                )
            latency = int((datetime.now(UTC) - started).total_seconds() * 1000)
            attempts.append({"provider": name, "status": "completed", "count": len(offers)})
            session.add(
                ProviderRequest(
                    search_id=search.id,
                    provider=name,
                    module="flight",
                    status="completed",
                    latency_ms=latency,
                )
            )
        except ProviderUnavailableError as exc:
            latency = int((datetime.now(UTC) - started).total_seconds() * 1000)
            attempts.append({"provider": name, "status": "failed", "error": str(exc)})
            session.add(
                ProviderRequest(
                    search_id=search.id,
                    provider=name,
                    module="flight",
                    status="failed",
                    latency_ms=latency,
                    error=str(exc),
                )
            )
    modules = dict(search.result_json.get("modules", {}))
    modules["flight"] = [
        item.model_dump(mode="json")
        for item in sorted(by_source.values(), key=lambda value: value.total_price)
    ]
    provider_statuses = dict(search.result_json.get("provider_statuses", {}))
    provider_statuses["flight"] = attempts
    search.result_json = {
        **search.result_json,
        "modules": modules,
        "provider_statuses": provider_statuses,
    }
    await redis.set(replay_key, "1", ex=86_400)
    await session.commit()
    return {
        "search_id": str(search.id),
        "replayed": False,
        "offers": modules["flight"],
        "provider_statuses": attempts,
    }


@router.post("/searches/{search_id}/flight-statuses")
async def enrich_search_flight_statuses(
    search_id: UUID, user: CurrentUser, session: Session
) -> dict[str, Any]:
    search = await _owned_search(search_id, user, session)
    settings = await load_runtime_settings(session)
    if not settings.flightaware_configured:
        raise AppError(503, "flightaware_not_configured", "FlightAware 航班動態尚未啟用")
    offers = _stored_offers(search)
    groups: dict[str, FlightOffer] = {}
    for offer in sorted(offers, key=lambda value: value.total_price):
        groups.setdefault(offer.itinerary_key or str(offer.id), offer)
    provider = FlightAwareProvider(get_redis(), settings)
    statuses: dict[str, list[dict[str, Any]]] = {}
    segment_count = 0
    for key, offer in list(groups.items())[: settings.flightaware_enrich_offer_limit]:
        matched: list[dict[str, Any]] = []
        for segment in offer.segments:
            if segment_count >= 12:
                break
            segment_count += 1
            values, _ = await provider.lookup(
                segment.departure_time.date(),
                ident=segment.flight_number,
                origin=segment.origin,
                destination=segment.destination,
            )
            if len(values) == 1:
                matched.append(values[0])
        statuses[key] = matched
    enriched = [
        offer.model_copy(
            update={"status_details": statuses.get(offer.itinerary_key or str(offer.id), [])}
        )
        for offer in offers
    ]
    modules = dict(search.result_json.get("modules", {}))
    modules["flight"] = [item.model_dump(mode="json") for item in enriched]
    search.result_json = {**search.result_json, "modules": modules}
    await session.commit()
    return {"search_id": str(search.id), "offers": modules["flight"]}


@router.post("/offers/{offer_id}/clickout", status_code=303)
async def clickout_offer(offer_id: UUID, user: CurrentUser, session: Session) -> RedirectResponse:
    records = list(
        (
            await session.scalars(
                select(FlightOfferRecord)
                .join(SearchRequest, SearchRequest.id == FlightOfferRecord.search_id)
                .where(SearchRequest.user_id == user.id)
            )
        ).all()
    )
    record = next((item for item in records if item.data.get("id") == str(offer_id)), None)
    if record is None:
        raise AppError(404, "offer_not_found", "找不到這筆報價")
    offer = _stored_offer(record)
    if not offer.clickout_available or offer.expires_at <= datetime.now(UTC):
        raise AppError(409, "offer_expired", "報價已過期，前往訂票前請先重新驗價")
    provider = build_flight_provider(
        get_redis(), await load_runtime_settings(session), provider_name=record.provider
    )
    if provider is None:
        raise AppError(503, "provider_unavailable", "原始航班供應商目前無法使用")
    target = await provider.clickout(offer)
    parsed = urlparse(target or "")
    if parsed.scheme != "https" or not parsed.netloc:
        raise AppError(409, "clickout_unavailable", "目前沒有可用的安全訂票連結")
    assert target is not None
    request = ProviderRequest(
        search_id=record.search_id,
        provider=record.provider,
        module="flight_clickout",
        status="completed",
        latency_ms=0,
    )
    session.add(request)
    await session.flush()
    session.add(
        ProviderResponse(
            provider_request_id=request.id,
            payload={
                "offer_id": str(offer_id),
                "provider_offer_id": offer.provider_offer_id,
                "selling_agent": offer.selling_agent,
            },
        )
    )
    if record.provider == "skyscanner":
        session.add(
            AffiliateClick(
                user_id=user.id,
                search_id=record.search_id,
                offer_id=offer_id,
                partner="skyscanner",
                module="flight",
                sub_id=uuid4().hex,
                destination_summary=f"{offer.origin}-{offer.destination}"[:128],
                target_host=(parsed.hostname or "")[:255],
                status="redirected",
            )
        )
    await session.commit()
    return RedirectResponse(target, status_code=303)
