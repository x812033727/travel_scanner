from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.parser import ParsedTripRequest, ParseTripRequest
from app.ai.trip_parser import parser_for_request
from app.db import get_session
from app.infra import client_ip

router = APIRouter(prefix="/ai", tags=["ai"])
Session = Annotated[AsyncSession, Depends(get_session)]


@router.post("/parse-trip", response_model=ParsedTripRequest)
async def parse_trip(
    request: Request, payload: ParseTripRequest, session: Session
) -> ParsedTripRequest:
    # Provider keys live in the admin DB, so the roster is per-request. The
    # helper never raises: an anonymous caller over the LLM ceiling, or a
    # database that is down, still gets the rules parse.
    parser = await parser_for_request(session, client_ip(request))
    return await parser.parse(payload.text)
