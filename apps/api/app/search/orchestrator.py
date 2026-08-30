import asyncio
import time
from datetime import datetime
from decimal import Decimal
from typing import Any, cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra import get_redis
from app.models import (
    ActivityOfferRecord,
    FlightOfferRecord,
    HotelOfferRecord,
    ProviderRequest,
    ProviderResponse,
    SearchJob,
    SearchRequest,
    TransportOfferRecord,
    UsageReservation,
)
from app.providers.mock import MockProvider
from app.providers.runner import ProviderRunner, ProviderUnavailableError
from app.providers.schemas import ActivityOffer, FlightOffer, HotelOffer, Offer, TransportOffer
from app.search.events import publish_event
from app.search.schemas import SearchCreate
from app.usage.service import commit_reservation

MODULE_PROGRESS = {"flight": 25, "hotel": 45, "activities": 62, "transport": 78}


async def persist_offers(
    session: AsyncSession, search_id: UUID, module: str, offers: list[Offer]
) -> None:
    for offer in offers:
        data = offer.model_dump(mode="json")
        if isinstance(offer, FlightOffer):
            session.add(
                FlightOfferRecord(
                    search_id=search_id,
                    provider=offer.provider,
                    provider_offer_id=offer.provider_offer_id,
                    data=data,
                    total_price=offer.total_price,
                    currency=offer.currency,
                    expires_at=offer.expires_at,
                )
            )
        elif isinstance(offer, HotelOffer):
            session.add(
                HotelOfferRecord(
                    search_id=search_id,
                    provider=offer.provider,
                    provider_offer_id=offer.provider_offer_id,
                    data=data,
                    total_price=offer.total_price,
                    currency=offer.currency,
                    expires_at=offer.expires_at,
                )
            )
        elif isinstance(offer, ActivityOffer):
            session.add(
                ActivityOfferRecord(
                    search_id=search_id,
                    provider=offer.provider,
                    provider_offer_id=offer.provider_offer_id,
                    data=data,
                    price=offer.price,
                    currency=offer.currency,
                    expires_at=offer.expires_at,
                )
            )
        elif isinstance(offer, TransportOffer):
            session.add(
                TransportOfferRecord(
                    search_id=search_id,
                    provider=offer.provider,
                    provider_offer_id=offer.provider_offer_id,
                    data=data,
                    price=offer.price,
                    currency=offer.currency,
                    expires_at=offer.expires_at,
                )
            )


async def run_module(
    provider: MockProvider, runner: ProviderRunner, module: str, query: SearchCreate
) -> list[Offer]:
    if module == "flight":
        return cast(
            list[Offer],
            await runner.run(provider.name, module, lambda: provider.search_flights(query)),
        )
    if module == "hotel":
        return cast(
            list[Offer],
            await runner.run(provider.name, module, lambda: provider.search_hotels(query)),
        )
    if module == "activities":
        return cast(
            list[Offer],
            await runner.run(provider.name, module, lambda: provider.search_activities(query)),
        )
    if module == "transport":
        return cast(
            list[Offer],
            await runner.run(provider.name, module, lambda: provider.search_transport(query)),
        )
    return []


async def orchestrate_search(session: AsyncSession, search_id: UUID) -> None:
    redis = get_redis()
    search = await session.get(SearchRequest, search_id)
    if search is None:
        return
    job = await session.scalar(select(SearchJob).where(SearchJob.search_id == search_id))
    reservation = await session.scalar(
        select(UsageReservation).where(UsageReservation.resource_id == search_id)
    )
    if reservation is not None and reservation.status == "reserved":
        await commit_reservation(session, reservation, search_id)
    if job:
        job.status = "running"
    await session.commit()
    await publish_event(redis, search_id, "search.created", 0, {"status": "processing"})
    query = SearchCreate.model_validate(search.request_json)
    provider, runner = MockProvider(), ProviderRunner(redis)
    results: dict[str, list[dict[str, Any]]] = {}
    warnings: list[str] = []

    async def collect(module: str) -> tuple[str, list[Offer], str | None]:
        started = time.perf_counter()
        provider_request = ProviderRequest(
            search_id=search_id, provider=provider.name, module=module
        )
        session.add(provider_request)
        await session.flush()
        try:
            offers = await run_module(provider, runner, module, query)
            provider_request.status = "completed"
            provider_request.latency_ms = int((time.perf_counter() - started) * 1000)
            session.add(
                ProviderResponse(
                    provider_request_id=provider_request.id,
                    payload={"count": len(offers), "is_mock": True},
                )
            )
            await persist_offers(session, search_id, module, offers)
            await session.commit()
            return module, offers, None
        except ProviderUnavailableError as exc:
            provider_request.status = "failed"
            provider_request.error = str(exc)
            await session.commit()
            return module, [], str(exc)

    tasks = [asyncio.create_task(collect(str(module))) for module in query.modules]
    for completed in asyncio.as_completed(tasks):
        module, offers, error = await completed
        progress = MODULE_PROGRESS[module]
        if error:
            warnings.append(error)
        else:
            serialized = [offer.model_dump(mode="json") for offer in offers]
            results[module] = serialized
            await publish_event(
                redis,
                search_id,
                "module.results",
                progress,
                {"module": module, "offers": serialized},
            )
        await publish_event(
            redis,
            search_id,
            "provider.completed",
            progress,
            {"module": module, "status": "failed" if error else "completed"},
        )
        search.progress = progress
        search.result_json = {"modules": results}
        search.warnings_json = warnings
        await session.commit()

    search.status = "completed" if results else "failed"
    search.progress = 100
    search.result_json = {"modules": results, "plans": []}
    search.warnings_json = warnings
    if job:
        job.status = search.status
    await session.commit()
    terminal = "search.completed" if results else "search.failed"
    await publish_event(
        redis, search_id, terminal, 100, {"status": search.status, "warnings": warnings}
    )


def refresh_saved_offer(offer_id: UUID, old_price: Decimal) -> dict[str, Any]:
    available = offer_id.int % 17 != 0
    delta = Decimal((offer_id.int % 7) - 3) * Decimal(50)
    new_price = max(Decimal(0), old_price + delta) if available else old_price
    return {
        "offer_id": str(offer_id),
        "old_price": old_price,
        "new_price": new_price,
        "price_change": new_price - old_price,
        "still_available": available,
        "refreshed_at": datetime.now().astimezone(),
    }
