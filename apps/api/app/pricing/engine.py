from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel

from app.providers.schemas import ActivityOffer, FlightOffer, HotelOffer, TransportOffer


class Confidence(StrEnum):
    CONFIRMED = "confirmed"
    ESTIMATED = "estimated"


class PriceComponent(BaseModel):
    category: str
    label: str
    amount: Decimal
    currency: str = "TWD"
    confidence: Confidence


class TotalCost(BaseModel):
    confirmed_cost: Decimal
    estimated_cost: Decimal
    total_cost: Decimal
    currency: str = "TWD"
    components: list[PriceComponent]


class TotalCostEngine:
    def calculate(
        self,
        flight: FlightOffer | None,
        hotel: HotelOffer | None,
        activity: ActivityOffer | None,
        transport: TransportOffer | None,
        travelers: int,
    ) -> TotalCost:
        parts: list[PriceComponent] = []

        def add(category: str, label: str, amount: Decimal, confidence: Confidence) -> None:
            if amount:
                parts.append(
                    PriceComponent(
                        category=category, label=label, amount=amount, confidence=confidence
                    )
                )

        people = Decimal(travelers)
        if flight:
            add("flight_base", "機票票價", flight.base_price * people, Confidence.CONFIRMED)
            add("flight_tax", "機票稅金", flight.taxes * people, Confidence.CONFIRMED)
            add("flight_fee", "航空附加費", flight.fees * people, Confidence.CONFIRMED)
            add("baggage", "托運行李", flight.baggage_price * people, Confidence.CONFIRMED)
        if hotel:
            add("hotel", "住宿", hotel.base_price, Confidence.CONFIRMED)
            add("hotel_tax", "住宿稅金", hotel.taxes, Confidence.CONFIRMED)
            add("hotel_fee", "住宿附加費", hotel.fees, Confidence.CONFIRMED)
        if activity:
            add("activities", "活動體驗", activity.price * people, Confidence.CONFIRMED)
        if transport:
            add("airport_transport", "機場交通", transport.price * people, Confidence.CONFIRMED)
        nights = hotel.nights if hotel else 5
        add(
            "local_transport",
            "當地交通估算",
            Decimal(nights * travelers * 300),
            Confidence.ESTIMATED,
        )
        confirmed = sum(
            (p.amount for p in parts if p.confidence == Confidence.CONFIRMED), Decimal(0)
        )
        estimated = sum(
            (p.amount for p in parts if p.confidence == Confidence.ESTIMATED), Decimal(0)
        )
        return TotalCost(
            confirmed_cost=confirmed,
            estimated_cost=estimated,
            total_cost=confirmed + estimated,
            components=parts,
        )
