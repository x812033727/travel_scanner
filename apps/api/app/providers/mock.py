import asyncio
import hashlib
import random
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import NAMESPACE_URL, UUID, uuid5

from app.providers.schemas import (
    ActivityOffer,
    FlightOffer,
    FlightSegment,
    HotelOffer,
    OfferRefreshResult,
    TransportOffer,
)
from app.search.schemas import SearchCreate

CITY_DATA = {
    "TYO": ("東京", 35.6762, 139.6503),
    "NRT": ("東京", 35.6762, 139.6503),
    "HND": ("東京", 35.6762, 139.6503),
    "OSA": ("大阪", 34.6937, 135.5023),
    "KIX": ("大阪", 34.6937, 135.5023),
    "FUK": ("福岡", 33.5904, 130.4017),
    "CTS": ("札幌", 43.0618, 141.3545),
    "OKA": ("沖繩", 26.2124, 127.6809),
    "NGO": ("名古屋", 35.1815, 136.9066),
    "ICN": ("首爾", 37.5665, 126.9780),
    "PUS": ("釜山", 35.1796, 129.0756),
    "CJU": ("濟州", 33.4996, 126.5312),
    "BKK": ("曼谷", 13.7563, 100.5018),
    "CNX": ("清邁", 18.7883, 98.9853),
    "HKT": ("普吉", 7.8804, 98.3923),
    "KBV": ("喀比", 8.0863, 98.9063),
}


def query_seed(query: SearchCreate, module: str) -> int:
    digest = hashlib.sha256(f"{query.model_dump_json()}:{module}".encode()).hexdigest()
    return int(digest[:16], 16)


def stable_id(value: str) -> UUID:
    return uuid5(NAMESPACE_URL, f"travel-scanner:{value}")


def route(query: SearchCreate) -> tuple[str, str, datetime, datetime]:
    if query.legs:
        leg = query.legs[0]
        origin, destination, departure = leg.origin, leg.destination, leg.departure_date
    else:
        origin, destination = query.origin or "TPE", query.destination or "NRT"
        departure = query.departure_date or datetime.now(UTC).date()
    returning = query.return_date or departure + timedelta(days=5)
    return (
        origin.upper(),
        destination.upper(),
        datetime.combine(departure, datetime.min.time(), tzinfo=UTC),
        datetime.combine(returning, datetime.min.time(), tzinfo=UTC),
    )


class MockProvider:
    name = "mock"

    def __init__(self, latency: float = 0, fail_modules: set[str] | None = None) -> None:
        self.latency = latency
        self.fail_modules = fail_modules or set()
        self._offers: dict[UUID, FlightOffer | HotelOffer] = {}

    async def _wait(self, module: str) -> None:
        if self.latency:
            await asyncio.sleep(self.latency)
        if module in self.fail_modules:
            raise ConnectionError(f"mock {module} failure")

    async def search_flights(self, query: SearchCreate) -> list[FlightOffer]:
        await self._wait("flight")
        rng = random.Random(query_seed(query, "flight"))
        origin, destination, departure, _ = route(query)
        now = datetime.now(UTC)
        airlines = [("星宇航空", "JX"), ("中華航空", "CI"), ("長榮航空", "BR"), ("樂桃航空", "MM")]
        offers: list[FlightOffer] = []
        for index, (airline, code) in enumerate(airlines):
            depart_at = departure.replace(hour=[7, 10, 14, 23][index]) + timedelta(
                minutes=rng.randrange(0, 3) * 10
            )
            duration = 175 + rng.randrange(-15, 25)
            base, taxes = Decimal(6200 + index * 850 + rng.randrange(0, 500)), Decimal(1850)
            fees, baggage = Decimal(350 if index == 3 else 0), Decimal(950 if index == 3 else 0)
            offer_id = stable_id(f"flight:{query_seed(query, 'flight')}:{index}")
            arrival = depart_at + timedelta(minutes=duration)
            offer = FlightOffer(
                id=offer_id,
                provider=self.name,
                provider_offer_id=f"MF-{offer_id.hex[:12]}",
                booking_url="https://example.invalid/mock-booking",
                retrieved_at=now,
                expires_at=now + timedelta(minutes=5),
                origin=origin,
                destination=destination,
                departure_time=depart_at,
                arrival_time=arrival,
                duration_minutes=duration,
                segments=[
                    FlightSegment(
                        origin=origin,
                        destination=destination,
                        departure_time=depart_at,
                        arrival_time=arrival,
                        airline=airline,
                        flight_number=f"{code}{100 + index * 17}",
                    )
                ],
                airline=airline,
                flight_number=f"{code}{100 + index * 17}",
                base_price=base,
                taxes=taxes,
                fees=fees,
                baggage_price=baggage,
                total_price=base + taxes + fees + baggage,
                carry_on=True,
                checked_baggage_kg=0 if index == 3 else 23,
                refundable=index in (1, 2),
                changeable=index != 3,
            )
            offers.append(offer)
            self._offers[offer_id] = offer
        return offers

    async def search_hotels(self, query: SearchCreate) -> list[HotelOffer]:
        await self._wait("hotel")
        rng = random.Random(query_seed(query, "hotel"))
        _, destination, check_in, check_out = route(query)
        city, latitude, longitude = CITY_DATA.get(destination, (destination, 35.0, 139.0))
        now, nights = datetime.now(UTC), max(1, (check_out.date() - check_in.date()).days)
        names = [
            f"{city}中央旅店",
            f"{city}站前花園飯店",
            f"{city}河畔設計酒店",
            f"{city}都會舒適飯店",
        ]
        offers: list[HotelOffer] = []
        for index, name in enumerate(names):
            base = Decimal(2500 + index * 720 + rng.randrange(0, 300)) * nights
            taxes, fees = (
                (base * Decimal("0.1")).quantize(Decimal("1")),
                Decimal(0 if index < 2 else 500),
            )
            offer_id = stable_id(f"hotel:{query_seed(query, 'hotel')}:{index}")
            offer = HotelOffer(
                id=offer_id,
                provider=self.name,
                provider_offer_id=f"MH-{offer_id.hex[:12]}",
                booking_url="https://example.invalid/mock-booking",
                retrieved_at=now,
                expires_at=now + timedelta(minutes=5),
                hotel_id=f"mock-hotel-{index}",
                hotel_name=name,
                latitude=latitude + index * 0.004,
                longitude=longitude - index * 0.003,
                rating=3.8 + index * 0.35,
                room_type="標準雙人房" if index < 2 else "豪華雙人房",
                check_in=check_in.replace(hour=15),
                check_out=check_out.replace(hour=11),
                nights=nights,
                base_price=base,
                taxes=taxes,
                fees=fees,
                total_price=base + taxes + fees,
                breakfast_included=index > 0,
                refundable=index != 0,
                station_walk_minutes=[11, 5, 8, 3][index],
                nightly_price=((base + taxes + fees) / nights).quantize(Decimal("0.01")),
            )
            offers.append(offer)
            self._offers[offer_id] = offer
        return offers

    async def search_activities(self, query: SearchCreate) -> list[ActivityOffer]:
        await self._wait("activities")
        _, destination, _, _ = route(query)
        city, latitude, longitude = CITY_DATA.get(destination, (destination, 35.0, 139.0))
        now = datetime.now(UTC)
        rows = [
            ("在地美食散步", "food", 1280),
            ("城市精華一日遊", "culture", 2200),
            ("購物街導覽", "shopping", 880),
        ]
        return [
            ActivityOffer(
                id=stable_id(f"activity:{query_seed(query, 'activities')}:{index}"),
                provider=self.name,
                provider_offer_id=f"MA-{index}-{destination}",
                booking_url="https://example.invalid/mock-booking",
                retrieved_at=now,
                expires_at=now + timedelta(minutes=5),
                title=f"{city}{title}",
                city=city,
                latitude=latitude + index * 0.002,
                longitude=longitude + index * 0.002,
                duration_minutes=[180, 420, 120][index],
                price=Decimal(price),
                rating=4.5 + index * 0.1,
                category=category,
            )
            for index, (title, category, price) in enumerate(rows)
        ]

    async def search_transport(self, query: SearchCreate) -> list[TransportOffer]:
        await self._wait("transport")
        _, destination, departure, _ = route(query)
        city = CITY_DATA.get(destination, (destination, 0, 0))[0]
        now = datetime.now(UTC)
        rows = [("機場快線", 45, 420, 92), ("機場巴士", 75, 300, 74), ("共乘接送", 55, 1280, 96)]
        return [
            TransportOffer(
                id=stable_id(f"transport:{query_seed(query, 'transport')}:{index}"),
                provider=self.name,
                provider_offer_id=f"MT-{index}-{destination}",
                booking_url="https://example.invalid/mock-booking",
                retrieved_at=now,
                expires_at=now + timedelta(minutes=5),
                origin=f"{destination} 機場",
                destination=f"{city}市區",
                transport_type=kind,
                departure_time=departure.replace(hour=12 + index),
                arrival_time=departure.replace(hour=12 + index) + timedelta(minutes=minutes),
                duration_minutes=minutes,
                price=Decimal(price),
                convenience_score=score,
            )
            for index, (kind, minutes, price, score) in enumerate(rows)
        ]

    async def refresh_offer(self, offer_id: UUID) -> OfferRefreshResult:
        await self._wait("refresh")
        offer = self._offers.get(offer_id)
        old_price = Decimal(0) if offer is None else offer.total_price
        available = offer is not None and offer_id.int % 17 != 0
        delta = Decimal((offer_id.int % 7) - 3) * Decimal(50)
        new_price = max(Decimal(0), old_price + delta) if available else old_price
        return OfferRefreshResult(
            offer_id=offer_id,
            old_price=old_price,
            new_price=new_price,
            price_change=new_price - old_price,
            still_available=available,
            refreshed_at=datetime.now(UTC),
        )

    async def get_offer_details(self, offer_id: UUID) -> FlightOffer | None:
        offer = self._offers.get(offer_id)
        return offer if isinstance(offer, FlightOffer) else None

    async def get_hotel_details(self, hotel_id: str) -> dict[str, str]:
        return {"hotel_id": hotel_id, "source": "mock"}
