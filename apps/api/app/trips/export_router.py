"""Calendar export for a saved trip."""

from __future__ import annotations

import re
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.db import get_session
from app.i18n import Locale, current_locale
from app.trips.ics import trip_calendar
from app.trips.route_planner import load_route_segments, segment_from_record
from app.trips.router import hydrate_legacy_items, load_items, owned_trip

router = APIRouter(prefix="/trips", tags=["trips"])
Session = Annotated[AsyncSession, Depends(get_session)]


def filename_for(name: str, trip_id: UUID) -> str:
    """An ASCII filename clients can save; the readable name rides in filename*."""
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-").lower()
    return f"{slug or 'trip'}-{str(trip_id)[:8]}.ics"


@router.get("/{trip_id}/export.ics")
async def export_trip_calendar(
    trip_id: UUID,
    user: CurrentUser,
    session: Session,
    locale: Annotated[Locale, Depends(current_locale)],
) -> Response:
    trip = await owned_trip(session, user.id, trip_id)
    items = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    segments = [
        segment_from_record(record) for record in await load_route_segments(session, trip.id)
    ]
    body = trip_calendar(trip, items, segments, locale=locale)
    ascii_name = filename_for(trip.name, trip.id)
    return Response(
        content=body,
        media_type="text/calendar; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{ascii_name}"',
            "Cache-Control": "no-store",
        },
    )
