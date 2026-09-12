from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.parser import ParsedTripRequest, ParseTripRequest, SupportedDestination
from app.ai.trip_parser import parser_for_request
from app.db import get_session
from app.destinations.catalog import SEARCHABLE_DESTINATIONS
from app.infra import client_ip

router = APIRouter(prefix="/ai", tags=["ai"])
Session = Annotated[AsyncSession, Depends(get_session)]

# Enough to show the shape of what is covered without turning the refusal into a
# catalogue. The full list is on /destinations.
_SUGGESTION_LIMIT = 6


def _suggestions() -> list[SupportedDestination]:
    return [
        SupportedDestination(
            code=profile.code, city=profile.city, country_label=profile.country_label
        )
        for profile in SEARCHABLE_DESTINATIONS[:_SUGGESTION_LIMIT]
    ]


@router.post("/parse-trip", response_model=ParsedTripRequest)
async def parse_trip(
    request: Request, payload: ParseTripRequest, session: Session
) -> ParsedTripRequest:
    # Provider keys live in the admin DB, so the roster is per-request. The
    # helper never raises: an anonymous caller over the LLM ceiling, or a
    # database that is down, still gets the rules parse.
    parser = await parser_for_request(session, client_ip(request))
    parsed = await parser.parse(payload.text)
    # Filled here rather than in each parser, so the two cannot answer differently.
    if parsed.destination_supported is False:
        parsed = parsed.model_copy(update={"supported_destinations": _suggestions()})
    return parsed
