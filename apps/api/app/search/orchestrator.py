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
from app.optimization.engine import TripOptimizer
from app.places.google import GoogleTravelService
from app.providers.base import TravelProvider
from app.providers.registry import build_provider, provider_status
from app.providers.runner import ProviderRunner, ProviderUnavailableError
from app.providers.schemas import ActivityOffer, FlightOffer, HotelOffer, Offer, TransportOffer
from app.search.events import publish_event
from app.search.schemas import SearchCreate
from app.usage.service import commit_reservation, release_reservation, usage_status

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
    provider: TravelProvider, runner: ProviderRunner, module: str, query: SearchCreate
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
    if job:
        job.status = "running"
    await session.commit()
    await publish_event(redis, search_id, "search.created", 0, {"status": "processing"})
    query = SearchCreate.model_validate(search.request_json)
    provider, runner = build_provider(redis), ProviderRunner(redis)
    place_service = GoogleTravelService(redis)
    status = provider_status()
    if provider is None:
        search.status = "failed"
        search.progress = 100
        search.warnings_json = [status.message]
        if job:
            job.status = "failed"
            job.error = status.message
        if reservation is not None:
            await release_reservation(session, reservation, "provider_unavailable")
        await session.commit()
        await publish_event(
            redis,
            search_id,
            "search.failed",
            100,
            {
                "status": "failed",
                "warnings": [status.message],
                "usage": usage_status(reservation).model_dump() if reservation else None,
            },
        )
        return
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
            if module == "hotel" and place_service.configured:
                hotels = [item for item in offers if isinstance(item, HotelOffer)]
                offers = cast(list[Offer], await place_service.enrich_hotels(hotels))
            elif module == "activities" and place_service.configured:
                activities = [item for item in offers if isinstance(item, ActivityOffer)]
                offers = cast(list[Offer], await place_service.enrich_activities(activities))
            provider_request.status = "completed"
            provider_request.latency_ms = int((time.perf_counter() - started) * 1000)
            session.add(
                ProviderResponse(
                    provider_request_id=provider_request.id,
                    payload={"count": len(offers), "mode": status.mode},
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

    plans: list[dict[str, Any]] = []
    if any(results.values()):
        flights = [FlightOffer.model_validate(item) for item in results.get("flight", [])]
        hotels = [HotelOffer.model_validate(item) for item in results.get("hotel", [])]
        activities = [ActivityOffer.model_validate(item) for item in results.get("activities", [])]
        transports = [TransportOffer.model_validate(item) for item in results.get("transport", [])]
        optimized = TripOptimizer().optimize(query, flights, hotels, activities, transports)
        if place_service.configured:
            await asyncio.gather(
                *(place_service.enrich_itinerary(plan.itinerary) for plan in optimized)
            )
        plans = [plan.model_dump(mode="json") for plan in optimized]
        await publish_event(redis, search_id, "optimization.completed", 90, {"plans": plans})
    has_usable_result = any(results.values()) or bool(plans)
    search.status = "completed" if has_usable_result else "failed"
    search.progress = 100
    search.result_json = {"modules": results, "plans": plans}
    search.warnings_json = warnings
    if job:
        job.status = search.status
    if reservation is not None:
        if has_usable_result:
            await commit_reservation(session, reservation, search_id)
        else:
            await release_reservation(session, reservation, "no_usable_result")
    await session.commit()
    terminal = "search.completed" if has_usable_result else "search.failed"
    await publish_event(
        redis,
        search_id,
        terminal,
        100,
        {
            "status": search.status,
            "warnings": warnings,
            "usage": usage_status(reservation).model_dump() if reservation else None,
        },
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
