import asyncio
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import Annotated, Any, cast
from urllib.parse import urlparse
from uuid import UUID

from fastapi import APIRouter, Depends, Header
from fastapi.responses import RedirectResponse, StreamingResponse
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
    FlightOfferRecord,
    ProviderRequest,
    ProviderResponse,
    SearchJob,
    SearchRequest,
    UsageReservation,
)
from app.problems import AppError
from app.providers.registry import (
    build_flight_provider,
    provider_status_for_modules,
)
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
        raise AppError(404, "search_not_found", "Search was not found")
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
        raise AppError(404, "search_not_found", "Search was not found")

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
        raise AppError(404, "offer_not_found", "Offer was not found")
    search = await session.get(SearchRequest, record.search_id)
    assert search is not None
    provider = build_flight_provider(get_redis(), provider_name=record.provider)
    if provider is None:
        raise AppError(503, "provider_unavailable", "The original flight provider is unavailable")
    offer = FlightOffer.model_validate(record.data)
    try:
        try:
            original_query = SearchCreate.model_validate(search.request_json)
        except ValueError:
            original_query = None
        result = await provider.refresh_offer(offer, original_query)
    except ConnectionError as exc:
        raise AppError(503, "provider_unavailable", str(exc)) from exc
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
        raise AppError(404, "offer_not_found", "Offer was not found")
    offer = FlightOffer.model_validate(record.data)
    if not offer.clickout_available or offer.expires_at <= datetime.now(UTC):
        raise AppError(409, "offer_expired", "Offer must be refreshed before booking")
    provider = build_flight_provider(get_redis(), provider_name=record.provider)
    if provider is None:
        raise AppError(503, "provider_unavailable", "The original flight provider is unavailable")
    target = await provider.clickout(offer)
    parsed = urlparse(target or "")
    if parsed.scheme != "https" or not parsed.netloc:
        raise AppError(409, "clickout_unavailable", "A secure booking link is unavailable")
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
    await session.commit()
    return RedirectResponse(target, status_code=303)
