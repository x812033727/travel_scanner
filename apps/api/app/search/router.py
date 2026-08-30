import asyncio
from collections.abc import AsyncIterator
from decimal import Decimal
from typing import Annotated, Any, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Header
from fastapi.responses import StreamingResponse
from redis import Redis as SyncRedis
from rq import Queue
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.config import get_settings
from app.db import get_session
from app.infra import enforce_rate_limit, get_redis
from app.models import SearchJob, SearchRequest
from app.problems import AppError
from app.providers.registry import provider_status
from app.search.events import stream_key
from app.search.orchestrator import refresh_saved_offer
from app.search.schemas import SearchCreate
from app.usage.service import release_reservation, reserve_credits, search_operation_cost

router = APIRouter(tags=["search"])
Session = Annotated[AsyncSession, Depends(get_session)]


@router.post("/searches", status_code=202)
async def create_search(
    payload: SearchCreate,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    status = provider_status()
    if status.status != "ready":
        raise AppError(503, "provider_not_configured", status.message)
    await enforce_rate_limit(user.id)
    payload_json = payload.model_dump(mode="json")
    operation, cost = search_operation_cost(payload_json)
    reservation, created = await reserve_credits(session, user.id, idempotency_key, operation, cost)
    if not created and reservation.resource_id:
        existing = await session.get(SearchRequest, reservation.resource_id)
        if existing:
            return {
                "search_id": str(existing.id),
                "status": existing.status,
                "progress": existing.progress,
                "credits_charged": reservation.credits,
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
        await release_reservation(session, reservation)
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
        "credits_charged": cost,
    }


@router.get("/searches/{search_id}")
async def get_search(search_id: UUID, user: CurrentUser, session: Session) -> dict[str, Any]:
    search = await session.scalar(
        select(SearchRequest).where(SearchRequest.id == search_id, SearchRequest.user_id == user.id)
    )
    if search is None:
        raise AppError(404, "search_not_found", "Search was not found")
    return {
        "search_id": str(search.id),
        "status": search.status,
        "progress": search.progress,
        "request": search.request_json,
        "result": search.result_json,
        "warnings": search.warnings_json,
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
    searches = list(
        (await session.scalars(select(SearchRequest).where(SearchRequest.user_id == user.id))).all()
    )
    for search in searches:
        modules = search.result_json.get("modules", {})
        for offers in modules.values():
            for offer in offers:
                if offer.get("id") == str(offer_id):
                    value = offer.get("total_price", offer.get("price", 0))
                    return refresh_saved_offer(offer_id, Decimal(str(value)))
    raise AppError(404, "offer_not_found", "Offer was not found")
