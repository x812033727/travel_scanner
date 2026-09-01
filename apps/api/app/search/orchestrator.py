import asyncio
import time
from typing import Any, cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.hotspots.service import load_planner_hotspots
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
    ActivityProvider,
    FlexibleFlightProvider,
    FlightProvider,
    FlightSearchState,
    HotelProvider,
    TransportProvider,
)
from app.providers.flight_keys import ensure_itinerary_key
from app.providers.flightaware import FlightAwareProvider
from app.providers.google_travel_impact import GoogleTravelImpactProvider
from app.providers.registry import (
    build_module_provider_candidates,
    provider_status,
)
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
                    public_offer_id=offer.id,
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
                    public_offer_id=offer.id,
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
    if module == "hotel":
        hotel_provider = cast(HotelProvider, provider)
        return cast(
            list[Offer],
            await runner.run(
                hotel_provider.name,
                module,
                lambda: hotel_provider.search_hotels(query),
            ),
        )
    if module == "activities":
        activity_provider = cast(ActivityProvider, provider)
        return cast(
            list[Offer],
            await runner.run(
                activity_provider.name,
                module,
                lambda: activity_provider.search_activities(query),
            ),
        )
    if module == "transport":
        transport_provider = cast(TransportProvider, provider)
        return cast(
            list[Offer],
            await runner.run(
                transport_provider.name,
                module,
                lambda: transport_provider.search_transport(query),
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
    providers = build_module_provider_candidates(redis, settings)
    runner = ProviderRunner(redis, settings)
    place_service = GoogleTravelService(redis, settings, locale=query.locale)
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
    provider_attempts: dict[str, list[dict[str, Any]]] = {}
    warnings: list[str] = []
    flex_warnings: list[str] = []
    flight_date_options: list[FlightDateOption] = []

    async def enrich_flights(offers: list[FlightOffer]) -> list[FlightOffer]:
        normalized = [ensure_itinerary_key(item) for item in offers]
        if settings.google_travel_impact_configured:
            try:
                normalized = await GoogleTravelImpactProvider(redis, settings).enrich(normalized)
            except ConnectionError:
                warnings.append("Google Travel Impact 碳排資料暫時無法取得。")
        if not settings.flightaware_configured or settings.flightaware_enrich_offer_limit == 0:
            return normalized
        groups: dict[str, FlightOffer] = {}
        for offer in sorted(normalized, key=lambda item: item.total_price):
            key = offer.itinerary_key or str(offer.id)
            groups.setdefault(key, offer)
        details: dict[str, list[dict[str, Any]]] = {}
        segment_count = 0
        provider = FlightAwareProvider(redis, settings)
        try:
            for key, offer in list(groups.items())[: settings.flightaware_enrich_offer_limit]:
                statuses: list[dict[str, Any]] = []
                for segment in offer.segments:
                    if segment_count >= 12:
                        break
                    segment_count += 1
                    matches, _ = await provider.lookup(
                        segment.departure_time.date(),
                        ident=segment.flight_number,
                        origin=segment.origin,
                        destination=segment.destination,
                    )
                    if len(matches) == 1:
                        statuses.append(matches[0])
                if statuses:
                    details[key] = statuses
        except ConnectionError:
            warnings.append("FlightAware 航班動態暫時無法取得，票價結果不受影響。")
        return [
            offer.model_copy(
                update={"status_details": details.get(offer.itinerary_key or str(offer.id), [])}
            )
            for offer in normalized
        ]

    async def collect(
        module: str,
    ) -> tuple[
        str,
        str,
        list[Offer],
        str | None,
        int,
        str,
        bool,
        list[tuple[str, int, str]],
    ]:
        nonlocal flight_date_options
        candidates = providers.get(module, [])
        if not candidates:
            module_message = status.module_statuses.get(module)
            return (
                module,
                "none",
                [],
                (
                    module_message.message
                    if module_message
                    else f"{module} provider is not configured"
                ),
                0,
                "failed",
                False,
                [],
            )
        failed_attempts: list[tuple[str, int, str]] = []
        accumulated_flights: dict[tuple[str, str], FlightOffer] = {}
        attempted_names: list[str] = []
        for candidate_index, provider in enumerate(candidates):
            started = time.perf_counter()
            provider_name = str(getattr(provider, "name", "unknown"))
            attempted_names.append(provider_name)
            try:
                completion = "complete"
                progressive = False
                if module == "flight" and hasattr(provider, "start_search"):
                    progressive = True
                    flight_provider = cast(FlightProvider, provider)
                    first = await runner.run(
                        provider_name,
                        module,
                        lambda selected=flight_provider: selected.start_search(query),  # type: ignore[misc]
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
                        session_id = first.session_id
                        current = await runner.run(
                            provider_name,
                            module,
                            lambda selected=flight_provider, token=session_id: selected.poll_search(  # type: ignore[misc]
                                token
                            ),
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
                if candidate_index > 0 and module != "flight":
                    offers = [offer.model_copy(update={"is_fallback": True}) for offer in offers]
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
                        current_option = FlightDateOption(
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
                        flexible.append(current_option)
                    flight_date_options = sorted(flexible, key=lambda item: item.shift_days)
                    if flight_date_options:
                        await publish_event(
                            redis,
                            search_id,
                            "flight.date_options",
                            24,
                            {
                                "options": [
                                    item.model_dump(mode="json") for item in flight_date_options
                                ]
                            },
                        )
                if module == "hotel" and place_service.configured:
                    hotels = [item for item in offers if isinstance(item, HotelOffer)]
                    offers = cast(list[Offer], await place_service.enrich_hotels(hotels))
                elif module == "activities" and place_service.configured:
                    activities = [item for item in offers if isinstance(item, ActivityOffer)]
                    offers = cast(list[Offer], await place_service.enrich_activities(activities))
                latency_ms = int((time.perf_counter() - started) * 1000)
                if module == "flight":
                    for item in offers:
                        if isinstance(item, FlightOffer):
                            normalized = ensure_itinerary_key(item)
                            accumulated_flights[
                                (normalized.provider, normalized.provider_offer_id)
                            ] = normalized
                    group_count = len(
                        {
                            item.itinerary_key or str(item.id)
                            for item in accumulated_flights.values()
                        }
                    )
                    should_continue = (
                        settings.flight_search_strategy.lower() == "hybrid"
                        and candidate_index + 1 < len(candidates)
                        and group_count < settings.flight_min_result_count
                    )
                    if should_continue:
                        await publish_event(
                            redis,
                            search_id,
                            "flight.source.completed",
                            24,
                            {
                                "provider": provider_name,
                                "offer_count": len(offers),
                                "itinerary_count": group_count,
                                "next_provider": str(
                                    getattr(candidates[candidate_index + 1], "name", "unknown")
                                ),
                            },
                        )
                        continue
                    flight_offers = await enrich_flights(list(accumulated_flights.values()))
                    offers = cast(list[Offer], flight_offers)
                    provider_name = ",".join(attempted_names)
                if candidate_index > 0 and module != "flight":
                    warnings.append(f"{module} 主要供應商暫時無法使用，已切換至 {provider_name}。")
                return (
                    module,
                    provider_name,
                    offers,
                    None,
                    latency_ms,
                    completion,
                    progressive,
                    failed_attempts,
                )
            except ProviderUnavailableError as exc:
                latency_ms = int((time.perf_counter() - started) * 1000)
                detail = str(exc)
                failed_attempts.append((provider_name, latency_ms, detail))
                if candidate_index + 1 < len(candidates):
                    continue
                if module == "flight" and accumulated_flights:
                    flight_offers = await enrich_flights(list(accumulated_flights.values()))
                    return (
                        module,
                        ",".join(attempted_names),
                        cast(list[Offer], flight_offers),
                        None,
                        latency_ms,
                        "partial",
                        False,
                        failed_attempts,
                    )
                completion = (
                    "rate_limited" if "429" in detail or "rate_limited" in detail else "failed"
                )
                return (
                    module,
                    provider_name,
                    [],
                    detail,
                    latency_ms,
                    completion,
                    False,
                    failed_attempts[:-1],
                )
        raise RuntimeError("provider candidate loop ended unexpectedly")

    tasks = [asyncio.create_task(collect(str(module))) for module in query.modules]
    for completed in asyncio.as_completed(tasks):
        (
            module,
            provider_name,
            offers,
            error,
            latency_ms,
            completion,
            progressive,
            failed_attempts,
        ) = await completed
        for failed_provider, failed_latency, failed_error in failed_attempts:
            session.add(
                ProviderRequest(
                    search_id=search_id,
                    provider=failed_provider,
                    module=module,
                    status="failed",
                    latency_ms=failed_latency,
                    error=failed_error,
                )
            )
        provider_attempts[module] = [
            {
                "provider": failed_provider,
                "status": "failed",
                "latency_ms": failed_latency,
                "error": failed_error,
            }
            for failed_provider, failed_latency, failed_error in failed_attempts
        ]
        if not error:
            for completed_provider in provider_name.split(","):
                provider_attempts[module].append(
                    {
                        "provider": completed_provider,
                        "status": "completed",
                        "count": sum(
                            1
                            for offer in offers
                            if getattr(offer, "provider", None) == completed_provider
                        ),
                    }
                )
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
            "provider_statuses": provider_attempts,
        }
        search.warnings_json = warnings
        await session.commit()

    plans: list[dict[str, Any]] = []
    if any(results.values()):
        flights = [FlightOffer.model_validate(item) for item in results.get("flight", [])]
        hotels = [HotelOffer.model_validate(item) for item in results.get("hotel", [])]
        activities = [ActivityOffer.model_validate(item) for item in results.get("activities", [])]
        transports = [TransportOffer.model_validate(item) for item in results.get("transport", [])]
        hotspots = (
            await load_planner_hotspots(
                session,
                city_code=query.destination,
                interests=query.preferences.interests,
                limit=12,
            )
            if "deep_travel" in query.preferences.interests and query.destination
            else []
        )
        optimized = TripOptimizer().optimize(
            query, flights, hotels, activities, transports, hotspots
        )
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
        "provider_statuses": provider_attempts,
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
