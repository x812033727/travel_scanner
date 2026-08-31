from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import CurrentUser
from app.db import get_session
from app.infra import enforce_rate_limit, get_redis
from app.models import FlightOfferRecord, SearchRequest, UsageReservation
from app.problems import AppError
from app.providers.live_back_to_back import (
    LiveBackToBackResponse,
    LiveBackToBackSearch,
    LiveBackToBackService,
)
from app.providers.registry import build_flight_provider, flight_provider_status
from app.usage.service import commit_reservation, release_reservation, reserve_use, usage_status

router = APIRouter(prefix="/flights", tags=["flights"])
Session = Annotated[AsyncSession, Depends(get_session)]


@router.post("/back-to-back", response_model=LiveBackToBackResponse)
async def compare_live_back_to_back(
    payload: LiveBackToBackSearch,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> LiveBackToBackResponse:
    if idempotency_key is None or not 8 <= len(idempotency_key) <= 255:
        raise AppError(422, "idempotency_key_required", "Idempotency-Key is required")
    settings = await load_runtime_settings(session)
    status = flight_provider_status(settings)
    if status.status != "ready":
        raise AppError(503, "provider_not_configured", status.message)
    await enforce_rate_limit(user.id)
    summary = (
        f"即時倒買比較 {payload.origin} → {payload.first_destination}／"
        f"{payload.second_destination} · {payload.first_trip.departure_date}"
    )
    reservation, created = await reserve_use(
        session,
        user.id,
        idempotency_key,
        "live_back_to_back_fare_search",
        summary,
    )
    if not created and reservation.resource_id:
        existing = await session.get(SearchRequest, reservation.resource_id)
        if existing and existing.result_json:
            replay = LiveBackToBackResponse.model_validate(existing.result_json)
            return replay.model_copy(update={"usage": usage_status(reservation)})
    search = SearchRequest(
        user_id=user.id,
        operation="live_back_to_back_fare_search",
        request_json=payload.model_dump(mode="json"),
    )
    session.add(search)
    await session.flush()
    reservation.resource_id = search.id
    await session.commit()
    try:
        provider = build_flight_provider(get_redis(), settings)
        if provider is None:
            raise AppError(503, "provider_not_configured", status.message)
        result = await LiveBackToBackService(provider).search(payload)
        usable = any(
            item.conventional is not None or item.back_to_back is not None
            for item in result.comparisons
        )
        search.status = "completed" if usable else "failed"
        search.progress = 100
        search.result_json = result.model_dump(mode="json")
        unique_offers = {
            component.offer.id: component.offer
            for comparison in result.comparisons
            for strategy in (comparison.conventional, comparison.back_to_back)
            if strategy is not None
            for component in strategy.components
        }
        for offer in unique_offers.values():
            session.add(
                FlightOfferRecord(
                    search_id=search.id,
                    provider=offer.provider,
                    provider_offer_id=offer.provider_offer_id,
                    data=offer.model_dump(mode="json"),
                    total_price=offer.total_price,
                    currency=offer.currency,
                    expires_at=offer.expires_at,
                )
            )
        if usable:
            await commit_reservation(session, reservation, search.id)
        else:
            await release_reservation(session, reservation, "no_comparable_fares")
        await session.commit()
        return result.model_copy(update={"usage": usage_status(reservation)})
    except Exception:
        await session.rollback()
        failed_search = await session.get(SearchRequest, search.id)
        if failed_search is not None:
            failed_search.status = "failed"
            failed_search.progress = 100
        reloaded = await session.get(UsageReservation, reservation.id)
        if reloaded is not None:
            await release_reservation(session, reloaded, "provider_error")
            await session.commit()
        raise
