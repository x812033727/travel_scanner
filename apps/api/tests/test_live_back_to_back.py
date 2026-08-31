from datetime import date

import pytest

from app.providers.live_back_to_back import (
    LiveBackToBackSearch,
    LiveBackToBackService,
    LiveComparisonMode,
    LiveTripDates,
)
from app.providers.mock import MockProvider
from app.providers.schemas import FlightOffer, OfferRefreshResult
from app.search.schemas import SearchCreate, TripType


class RecordingFlightProvider:
    name = "recording"

    def __init__(self, fail_multi_city: bool = False) -> None:
        self.mock = MockProvider()
        self.queries: list[SearchCreate] = []
        self.fail_multi_city = fail_multi_city

    async def search_flights(self, query: SearchCreate) -> list[FlightOffer]:
        self.queries.append(query)
        if self.fail_multi_city and query.trip_type == TripType.MULTI_CITY:
            raise ConnectionError("middle ticket unavailable")
        return await self.mock.search_flights(query)

    async def refresh_offer(
        self, offer: FlightOffer, query: SearchCreate | None = None
    ) -> OfferRefreshResult:
        return await self.mock.refresh_offer(offer, query)

    async def clickout(self, offer: FlightOffer) -> str | None:
        return None

    async def get_offer_details(self, offer_id: object) -> FlightOffer | None:
        return None


def request() -> LiveBackToBackSearch:
    return LiveBackToBackSearch(
        origin="TPE",
        first_destination="NRT",
        second_destination="KIX",
        first_trip=LiveTripDates(
            departure_date=date(2026, 10, 10), return_date=date(2026, 10, 15)
        ),
        second_trip=LiveTripDates(
            departure_date=date(2027, 3, 10), return_date=date(2027, 3, 15)
        ),
    )


@pytest.mark.asyncio
async def test_live_back_to_back_expands_five_real_ticket_shapes() -> None:
    provider = RecordingFlightProvider()
    result = await LiveBackToBackService(provider).search(request())

    assert len(provider.queries) == 5
    middle = next(query for query in provider.queries if query.trip_type == TripType.MULTI_CITY)
    assert [(leg.origin, leg.destination) for leg in middle.legs] == [
        ("NRT", "TPE"),
        ("TPE", "KIX"),
    ]
    mixed = next(
        item for item in result.comparisons if item.mode == LiveComparisonMode.MIXED_AIRLINES
    )
    same = next(
        item for item in result.comparisons if item.mode == LiveComparisonMode.SAME_AIRLINE
    )
    assert mixed.conventional is not None and mixed.back_to_back is not None
    assert same.conventional is not None and same.back_to_back is not None
    assert len(mixed.back_to_back.components) == 3


@pytest.mark.asyncio
async def test_live_back_to_back_does_not_invent_missing_middle_ticket() -> None:
    result = await LiveBackToBackService(RecordingFlightProvider(True)).search(request())

    assert result.comparisons[0].conventional is not None
    assert result.comparisons[0].back_to_back is None
    assert result.comparisons[0].verdict == "comparison_unavailable"
    assert any("middle_two_segment" in warning for warning in result.warnings)
