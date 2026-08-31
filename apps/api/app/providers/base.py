from enum import StrEnum
from typing import Protocol
from uuid import UUID

from app.providers.schemas import (
    ActivityOffer,
    FlightDateOption,
    FlightOffer,
    HotelOffer,
    OfferRefreshResult,
    TransportOffer,
)
from app.search.schemas import SearchCreate


class FlightSearchState(StrEnum):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
    PARTIAL = "partial"
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"


class FlightSearchBatch:
    def __init__(
        self,
        session_id: str,
        offers: list[FlightOffer],
        state: FlightSearchState,
        warnings: list[str] | None = None,
    ) -> None:
        self.session_id = session_id
        self.offers = offers
        self.state = state
        self.warnings = warnings or []


class FlightProvider(Protocol):
    name: str

    async def search_flights(self, query: SearchCreate) -> list[FlightOffer]: ...
    async def refresh_offer(
        self, offer: FlightOffer, query: SearchCreate | None = None
    ) -> OfferRefreshResult: ...
    async def clickout(self, offer: FlightOffer) -> str | None: ...
    async def get_offer_details(self, offer_id: UUID) -> FlightOffer | None: ...


class FlexibleFlightProvider(Protocol):
    async def search_flexible_dates(
        self, query: SearchCreate, flex_days: int
    ) -> list[FlightDateOption]: ...


class HotelProvider(Protocol):
    name: str

    async def search_hotels(self, query: SearchCreate) -> list[HotelOffer]: ...
    async def get_hotel_details(self, hotel_id: str) -> dict[str, str]: ...


class ActivityProvider(Protocol):
    name: str

    async def search_activities(self, query: SearchCreate) -> list[ActivityOffer]: ...


class TransportProvider(Protocol):
    name: str

    async def search_transport(self, query: SearchCreate) -> list[TransportOffer]: ...


class TravelProvider(
    FlightProvider,
    HotelProvider,
    ActivityProvider,
    TransportProvider,
    Protocol,
):
    """Provider capable of serving every module in a complete trip search."""
