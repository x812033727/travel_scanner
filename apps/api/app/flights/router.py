from datetime import UTC, datetime, timedelta
from typing import Annotated, Any
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Header
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import CurrentUser
from app.db import get_session
from app.flights.schemas import FlightStatusLookupCreate
from app.infra import get_redis
from app.models import FlightStatusLookup, UsageReservation
from app.problems import AppError
from app.providers.flightaware import FlightAwareProvider
from app.usage.service import (
    commit_reservation,
    release_reservation,
    reserve_use,
    usage_status,
)

router = APIRouter(prefix="/flights", tags=["flight-status"])
Session = Annotated[AsyncSession, Depends(get_session)]


def _response(row: FlightStatusLookup, reservation: UsageReservation | None) -> dict[str, Any]:
    return {
        "id": str(row.id),
        "provider": row.provider,
        "query": row.query_json,
        "items": row.result_json.get("items", []),
        "cache_hit": row.cache_hit,
        "expires_at": row.expires_at,
        "usage": usage_status(reservation).model_dump() if reservation else None,
    }


@router.post("/status-lookups", status_code=201)
async def create_status_lookup(
    payload: FlightStatusLookupCreate,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    settings = await load_runtime_settings(session)
    if not settings.flightaware_configured:
        raise AppError(503, "flightaware_not_configured", "FlightAware 航班動態尚未啟用")
    await session.execute(
        delete(FlightStatusLookup).where(
            FlightStatusLookup.expires_at <= datetime.now(UTC)
        )
    )
    query = payload.model_dump(mode="json", exclude_none=True)
    reservation, created = await reserve_use(
        session,
        user.id,
        idempotency_key,
        "flight_status_lookup",
        (
            f"航班動態 {payload.ident or f'{payload.origin}-{payload.destination}'}"
            f" · {payload.departure_date}"
        ),
    )
    if not created and reservation.resource_id:
        existing = await session.get(FlightStatusLookup, reservation.resource_id)
        if existing and existing.user_id == user.id:
            return _response(existing, reservation)
    try:
        items, cache_hit = await FlightAwareProvider(get_redis(), settings).lookup(
            payload.departure_date,
            ident=payload.ident,
            origin=payload.origin,
            destination=payload.destination,
        )
    except ConnectionError as exc:
        await release_reservation(session, reservation, "provider_failure")
        await session.commit()
        raise AppError(503, "flightaware_unavailable", str(exc)) from exc
    normalized = [{**item, "item_id": str(uuid4())} for item in items]
    row = FlightStatusLookup(
        user_id=user.id,
        reservation_id=reservation.id,
        query_json=query,
        result_json={"items": normalized},
        cache_hit=cache_hit,
        expires_at=datetime.now(UTC) + timedelta(hours=settings.flight_status_retention_hours),
    )
    session.add(row)
    await session.flush()
    reservation.resource_id = row.id
    if items and not cache_hit:
        await commit_reservation(session, reservation, row.id)
    else:
        await release_reservation(
            session, reservation, "cache_hit" if cache_hit else "empty_result"
        )
    await session.commit()
    return _response(row, reservation)


async def _owned_lookup(
    lookup_id: UUID, user: CurrentUser, session: AsyncSession
) -> FlightStatusLookup:
    row = await session.scalar(
        select(FlightStatusLookup).where(
            FlightStatusLookup.id == lookup_id, FlightStatusLookup.user_id == user.id
        )
    )
    if row is None:
        raise AppError(404, "flight_status_lookup_not_found", "找不到這筆航班動態查詢")
    if row.expires_at <= datetime.now(UTC):
        raise AppError(410, "flight_status_lookup_expired", "這筆航班動態查詢已到期")
    return row


@router.get("/status-lookups/{lookup_id}")
async def get_status_lookup(lookup_id: UUID, user: CurrentUser, session: Session) -> dict[str, Any]:
    row = await _owned_lookup(lookup_id, user, session)
    reservation = (
        await session.get(UsageReservation, row.reservation_id) if row.reservation_id else None
    )
    return _response(row, reservation)


@router.get("/status-lookups/{lookup_id}/items/{item_id}/track")
async def get_flight_track(
    lookup_id: UUID, item_id: UUID, user: CurrentUser, session: Session
) -> dict[str, Any]:
    row = await _owned_lookup(lookup_id, user, session)
    item = next(
        (
            value
            for value in row.result_json.get("items", [])
            if value.get("item_id") == str(item_id)
        ),
        None,
    )
    if item is None:
        raise AppError(404, "flight_status_item_not_found", "找不到這個航班項目")
    fa_flight_id = item.get("fa_flight_id")
    if not fa_flight_id or item.get("schedule_only"):
        raise AppError(409, "flight_track_unavailable", "班表資料尚無可用的實際航跡")
    settings = await load_runtime_settings(session)
    try:
        track, cache_hit = await FlightAwareProvider(get_redis(), settings).track(str(fa_flight_id))
    except ConnectionError as exc:
        raise AppError(503, "flightaware_unavailable", str(exc)) from exc
    return {**track, "cache_hit": cache_hit}
