from typing import Protocol
from uuid import UUID

from app.providers.schemas import (
    ActivityOffer,
    FlightOffer,
    HotelOffer,
    OfferRefreshResult,
    TransportOffer,
)
from app.search.schemas import SearchCreate


class FlightProvider(Protocol):
    name: str

    async def search_flights(self, query: SearchCreate) -> list[FlightOffer]: ...
    async def refresh_offer(self, offer_id: UUID) -> OfferRefreshResult: ...
    async def get_offer_details(self, offer_id: UUID) -> FlightOffer | None: ...


class HotelProvider(Protocol):
    name: str

    async def search_hotels(self, query: SearchCreate) -> list[HotelOffer]: ...
    async def refresh_offer(self, offer_id: UUID) -> OfferRefreshResult: ...
    async def get_hotel_details(self, hotel_id: str) -> dict[str, str]: ...


class ActivityProvider(Protocol):
    name: str

    async def search_activities(self, query: SearchCreate) -> list[ActivityOffer]: ...


class TransportProvider(Protocol):
    name: str

    async def search_transport(self, query: SearchCreate) -> list[TransportOffer]: ...
