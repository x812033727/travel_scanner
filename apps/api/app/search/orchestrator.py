import asyncio
import time
from typing import Any, cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
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
from app.providers.base import (
    FlexibleFlightProvider,
    FlightProvider,
    FlightSearchState,
    TravelProvider,
)
from app.providers.registry import build_module_providers, provider_status
from app.providers.runner import ProviderRunner, ProviderUnavailableError
from app.providers.schemas import (
    ActivityOffer,
    FlightDateOption,
    FlightOffer,
    HotelOffer,
    Offer,
    TransportOffer,
)
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
    provider: object, runner: ProviderRunner, module: str, query: SearchCreate
) -> list[Offer]:
    if module == "flight":
        flight_provider = cast(FlightProvider, provider)
        return cast(
            list[Offer],
            await runner.run(
                flight_provider.name,
                module,
                lambda: flight_provider.search_flights(query),
            ),
        )
    travel_provider = cast(TravelProvider, provider)
    if module == "hotel":
        return cast(
            list[Offer],
            await runner.run(
                travel_provider.name,
                module,
                lambda: travel_provider.search_hotels(query),
            ),
        )
    if module == "activities":
        return cast(
            list[Offer],
            await runner.run(
                travel_provider.name,
                module,
                lambda: travel_provider.search_activities(query),
            ),
        )
    if module == "transport":
        return cast(
            list[Offer],
            await runner.run(
                travel_provider.name,
                module,
                lambda: travel_provider.search_transport(query),
            ),
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
    settings = await load_runtime_settings(session)
    providers = build_module_providers(redis, settings)
    runner = ProviderRunner(redis, settings)
    place_service = GoogleTravelService(redis, settings)
    status = provider_status(settings)
    if not any(providers.get(str(module)) for module in query.modules):
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
    flex_warnings: list[str] = []
    flight_date_options: list[FlightDateOption] = []

    async def collect(
        module: str,
    ) -> tuple[str, str, list[Offer], str | None, int, str, bool]:
        nonlocal flight_date_options
        started = time.perf_counter()
        provider = providers.get(module)
        if provider is None:
            return (
                module,
                "none",
                [],
                f"{module} provider is not configured",
                0,
                "failed",
                False,
            )
        try:
            provider_name = str(getattr(provider, "name", "unknown"))
            completion = "complete"
            progressive = False
            if module == "flight" and hasattr(provider, "start_search"):
                progressive = True
                flight_provider = cast(FlightProvider, provider)
                first = await runner.run(
                    provider_name,
                    module,
                    lambda: flight_provider.start_search(query),  # type: ignore[attr-defined]
                )
                collected = {item.provider_offer_id: item for item in first.offers}
                await publish_event(
                    redis,
                    search_id,
                    "module.results",
                    15,
                    {
                        "module": module,
                        "offers": [item.model_dump(mode="json") for item in first.offers],
                        "status": first.state.value,
                    },
                )
                current = first
                attempts = 0
                while (
                    current.state == FlightSearchState.INCOMPLETE
                    and attempts < settings.skyscanner_poll_attempts
                ):
                    await asyncio.sleep(settings.skyscanner_poll_interval_seconds)
                    current = await runner.run(
                        provider_name,
                        module,
                        lambda: flight_provider.poll_search(first.session_id),  # type: ignore[attr-defined]
                    )
                    collected.update({item.provider_offer_id: item for item in current.offers})
                    attempts += 1
                    await publish_event(
                        redis,
                        search_id,
                        "module.results",
                        min(24, 15 + attempts * 2),
                        {
                            "module": module,
                            "offers": [item.model_dump(mode="json") for item in current.offers],
                            "status": current.state.value,
                        },
                    )
                offers = cast(
                    list[Offer],
                    sorted(
                        collected.values(),
                        key=lambda item: (item.total_price, item.provider_offer_id),
                    ),
                )
                completion = (
                    "timeout"
                    if current.state == FlightSearchState.INCOMPLETE
                    else current.state.value
                )
            else:
                offers = await run_module(provider, runner, module, query)
            if module == "flight" and query.flex_days:
                flexible: list[FlightDateOption] = []
                if hasattr(provider, "search_flexible_dates"):
                    try:
                        flexible_provider = cast(FlexibleFlightProvider, provider)
                        flexible = await flexible_provider.search_flexible_dates(
                            query, query.flex_days
                        )
                    except (ConnectionError, ProviderUnavailableError):
                        flex_warnings.append("彈性日期估價暫時無法取得，原日期班次仍可使用。")
                else:
                    flex_warnings.append("目前航班供應商不支援彈性日期估價。")
                exact_flights = [item for item in offers if isinstance(item, FlightOffer)]
                if exact_flights and query.departure_date:
                    cheapest = min(exact_flights, key=lambda item: item.total_price)
                    current = FlightDateOption(
                        shift_days=0,
                        departure_date=query.departure_date,
                        return_date=query.return_date,
                        lowest_price=cheapest.total_price,
                        currency=cheapest.currency,
                        provider=cheapest.provider,
                        source_mode=cheapest.source_mode,
                        is_current=True,
                        offer_count=len(exact_flights),
                    )
                    flexible = [item for item in flexible if item.shift_days != 0]
                    flexible.append(current)
                flight_date_options = sorted(flexible, key=lambda item: item.shift_days)
                if flight_date_options:
                    await publish_event(
                        redis,
                        search_id,
                        "flight.date_options",
                        24,
                        {"options": [item.model_dump(mode="json") for item in flight_date_options]},
                    )
            if module == "hotel" and place_service.configured:
                hotels = [item for item in offers if isinstance(item, HotelOffer)]
                offers = cast(list[Offer], await place_service.enrich_hotels(hotels))
            elif module == "activities" and place_service.configured:
                activities = [item for item in offers if isinstance(item, ActivityOffer)]
                offers = cast(list[Offer], await place_service.enrich_activities(activities))
            latency_ms = int((time.perf_counter() - started) * 1000)
            return (
                module,
                provider_name,
                offers,
                None,
                latency_ms,
                completion,
                progressive,
            )
        except ProviderUnavailableError as exc:
            latency_ms = int((time.perf_counter() - started) * 1000)
            detail = str(exc)
            completion = "rate_limited" if "429" in detail or "rate_limited" in detail else "failed"
            return (
                module,
                str(getattr(provider, "name", "unknown")),
                [],
                detail,
                latency_ms,
                completion,
                False,
            )

    tasks = [asyncio.create_task(collect(str(module))) for module in query.modules]
    for completed in asyncio.as_completed(tasks):
        module, provider_name, offers, error, latency_ms, completion, progressive = await completed
        provider_request = ProviderRequest(
            search_id=search_id,
            provider=provider_name,
            module=module,
            status="failed" if error else "completed",
            latency_ms=latency_ms,
            error=error,
        )
        session.add(provider_request)
        await session.flush()
        progress = MODULE_PROGRESS[module]
        if error:
            warnings.append(error)
        else:
            session.add(
                ProviderResponse(
                    provider_request_id=provider_request.id,
                    payload={
                        "count": len(offers),
                        "mode": offers[0].source_mode.value if offers else status.mode,
                    },
                )
            )
            await persist_offers(session, search_id, module, offers)
            serialized = [offer.model_dump(mode="json") for offer in offers]
            results[module] = serialized
            if not progressive:
                await publish_event(
                    redis,
                    search_id,
                    "module.results",
                    progress,
                    {"module": module, "offers": serialized, "status": completion},
                )
        for warning in flex_warnings:
            if warning not in warnings:
                warnings.append(warning)
        await publish_event(
            redis,
            search_id,
            "provider.completed",
            progress,
            {"module": module, "status": completion if not error else completion},
        )
        search.progress = progress
        search.result_json = {
            "modules": results,
            "flight_date_options": [item.model_dump(mode="json") for item in flight_date_options],
        }
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
    has_usable_result = any(results.values()) or bool(plans) or bool(flight_date_options)
    search.status = "completed" if has_usable_result else "failed"
    search.progress = 100
    search.result_json = {
        "modules": results,
        "plans": plans,
        "flight_date_options": [item.model_dump(mode="json") for item in flight_date_options],
    }
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
