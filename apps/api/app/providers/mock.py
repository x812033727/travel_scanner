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
from app.search.schemas import PropertyType, SearchCreate

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
        origin, destination, departure, returning = route(query)
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
            return_departure = returning.replace(hour=[8, 12, 15, 20][index])
            return_arrival = return_departure + timedelta(minutes=duration)
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
                        leg_index=0,
                        departure_timezone="UTC+08:00",
                        arrival_timezone="UTC+09:00",
                    ),
                    FlightSegment(
                        origin=destination,
                        destination=origin,
                        departure_time=return_departure,
                        arrival_time=return_arrival,
                        airline=airline,
                        flight_number=f"{code}{101 + index * 17}",
                        leg_index=1,
                        departure_timezone="UTC+09:00",
                        arrival_timezone="UTC+08:00",
                    ),
                ],
                airline=airline,
                flight_number=f"{code}{100 + index * 17}",
                cabin_class=query.cabin_class.value,
                base_price=base,
                taxes=taxes,
                fees=fees,
                baggage_price=baggage,
                total_price=base + taxes + fees + baggage,
                carry_on=True,
                checked_baggage_kg=0 if index == 3 else 23,
                refundable=index in (1, 2),
                changeable=index != 3,
                return_departure_time=return_departure,
                return_arrival_time=return_arrival,
                marketing_airline=airline,
                operating_airlines=[airline],
                baggage_summary=("含手提行李" if index == 3 else "含 23 kg 托運行李"),
                last_verified_at=now,
                arrival_day_offset=(arrival.date() - depart_at.date()).days,
            )
            offers.append(offer)
            self._offers[offer_id] = offer
        return offers

    async def search_hotels(self, query: SearchCreate) -> list[HotelOffer]:
        await self._wait("hotel")
        _, destination, check_in, check_out = route(query)
        city, latitude, longitude = CITY_DATA.get(destination, (destination, 35.0, 139.0))
        return self._hotel_offers(query, city, latitude, longitude, check_in, check_out)

    async def search_hotels_near(
        self, query: SearchCreate, *, latitude: float, longitude: float, radius_km: float
    ) -> list[HotelOffer]:
        await self._wait("hotel")
        _, destination, check_in, check_out = route(query)
        city = CITY_DATA.get(destination, (destination, 0.0, 0.0))[0]
        return self._hotel_offers(
            query,
            city,
            latitude,
            longitude,
            check_in,
            check_out,
            seed=f"near:{latitude:.3f}:{longitude:.3f}:{radius_km:.1f}",
            spread_deg=min(0.004, radius_km / 4 / 111),
        )

    def _hotel_offers(
        self,
        query: SearchCreate,
        city: str,
        latitude: float,
        longitude: float,
        check_in: datetime,
        check_out: datetime,
        *,
        seed: str = "",
        spread_deg: float = 0.004,
    ) -> list[HotelOffer]:
        query_hash = query_seed(query, "hotel")
        rng = random.Random(query_seed(query, f"hotel:{seed}") if seed else query_hash)
        seed_tag = hashlib.sha256(seed.encode()).hexdigest()[:6] if seed else ""
        now, nights = datetime.now(UTC), max(1, (check_out.date() - check_in.date()).days)
        names = [
            f"{city}中央旅店",
            f"{city}站前花園飯店",
            f"{city}河畔整套公寓",
            f"{city}都會整套民宿",
        ]
        offers: list[HotelOffer] = []
        for index, name in enumerate(names):
            base = Decimal(2500 + index * 720 + rng.randrange(0, 300)) * nights
            taxes, fees = (
                (base * Decimal("0.1")).quantize(Decimal("1")),
                Decimal(0 if index < 2 else 500),
            )
            offer_id = stable_id(
                f"hotel:{query_hash}:{seed}:{index}" if seed else f"hotel:{query_hash}:{index}"
            )
            offer = HotelOffer(
                id=offer_id,
                provider=self.name,
                provider_offer_id=f"MH-{offer_id.hex[:12]}",
                booking_url="https://example.invalid/mock-booking",
                retrieved_at=now,
                expires_at=now + timedelta(minutes=5),
                hotel_id=f"mock-hotel-{seed_tag}-{index}" if seed else f"mock-hotel-{index}",
                hotel_name=f"{name} {seed_tag}".strip(),
                latitude=latitude + index * spread_deg,
                longitude=longitude - index * spread_deg * 0.75,
                rating=[3, 4, 4, 5][index],
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
                address=f"{city}市旅遊核心區 {index + 1}-{index + 3}",
                amenities=[
                    ["Wi-Fi", "空調"],
                    ["Wi-Fi", "健身房", "行李寄存"],
                    ["Wi-Fi", "洗衣服務", "餐廳"],
                    ["Wi-Fi", "健身房", "行政酒廊", "機場接送"],
                ][index],
                review_score=[7.6, 8.4, 8.9, 9.3][index],
                review_count=[48, 320, 126, 680][index],
                distance_to_center_km=[2.8, 0.8, 1.6, 0.5][index],
                cancellation_policy=(
                    "不可退款" if index == 0 else "入住前 3 天可免費取消，之後收取首晚房費"
                ),
                property_type=(PropertyType.HOTEL if index < 2 else PropertyType.VACATION_RENTAL),
                max_guests=[2, 4, 4, 6][index],
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

    async def refresh_offer(
        self, offer: FlightOffer, query: SearchCreate | None = None
    ) -> OfferRefreshResult:
        await self._wait("refresh")
        old_price = offer.total_price
        available = offer.id.int % 17 != 0
        delta = Decimal((offer.id.int % 7) - 3) * Decimal(50)
        new_price = max(Decimal(0), old_price + delta) if available else old_price
        return OfferRefreshResult(
            offer_id=offer.id,
            old_price=old_price,
            new_price=new_price,
            price_change=new_price - old_price,
            still_available=available,
            refreshed_at=datetime.now(UTC),
        )

    async def clickout(self, offer: FlightOffer) -> str | None:
        return None

    async def get_offer_details(self, offer_id: UUID) -> FlightOffer | None:
        offer = self._offers.get(offer_id)
        return offer if isinstance(offer, FlightOffer) else None

    async def get_hotel_details(self, hotel_id: str) -> dict[str, str]:
        return {"hotel_id": hotel_id, "source": "mock"}
