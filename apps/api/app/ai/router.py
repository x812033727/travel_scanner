from fastapi import APIRouter

from app.ai.parser import MockAITripParser, ParsedTripRequest, ParseTripRequest

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/parse-trip", response_model=ParsedTripRequest)
async def parse_trip(payload: ParseTripRequest) -> ParsedTripRequest:
    return await MockAITripParser().parse(payload.text)
