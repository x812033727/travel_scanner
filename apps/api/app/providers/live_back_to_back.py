import asyncio
from datetime import UTC, date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, Field, model_validator

from app.providers.base import FlightProvider
from app.providers.schemas import FlightOffer
from app.search.schemas import (
    FlightCabinClass,
    SearchCreate,
    SearchModule,
    Travelers,
    TripLeg,
    TripType,
)
from app.usage.schemas import UsageStatus


class LiveTripDates(BaseModel):
    departure_date: date
    return_date: date

    @model_validator(mode="after")
    def ordered(self) -> Self:
        if self.return_date <= self.departure_date:
            raise ValueError("return_date must be after departure_date")
        return self


class LiveBackToBackSearch(BaseModel):
    origin: str = Field(default="TPE", min_length=3, max_length=3)
    first_destination: str = Field(min_length=3, max_length=3)
    second_destination: str = Field(min_length=3, max_length=3)
    first_trip: LiveTripDates
    second_trip: LiveTripDates
    travelers: Travelers = Field(default_factory=Travelers)
    cabin_class: FlightCabinClass = FlightCabinClass.ECONOMY
    currency: str = Field(default="TWD", min_length=3, max_length=3)
    locale: str = Field(default="zh-TW", max_length=16)

    @model_validator(mode="after")
    def validate_order(self) -> Self:
        self.origin = self.origin.upper()
        self.first_destination = self.first_destination.upper()
        self.second_destination = self.second_destination.upper()
        self.currency = self.currency.upper()
        if self.origin in {self.first_destination, self.second_destination}:
            raise ValueError("origin and destinations must differ")
        dates = (
            self.first_trip.departure_date,
            self.first_trip.return_date,
            self.second_trip.departure_date,
            self.second_trip.return_date,
        )
        if not all(left < right for left, right in zip(dates, dates[1:], strict=False)):
            raise ValueError(
                "dates must satisfy first departure < first return < "
                "second departure < second return"
            )
        return self


class LiveComparisonMode(StrEnum):
    MIXED_AIRLINES = "mixed_airlines"
    SAME_AIRLINE = "same_airline"


class LiveFareComponent(BaseModel):
    role: str
    offer: FlightOffer


class LiveFareStrategy(BaseModel):
    components: list[LiveFareComponent]
    total_price: Decimal
    currency: str


class LiveBackToBackComparison(BaseModel):
    mode: LiveComparisonMode
    conventional: LiveFareStrategy | None
    back_to_back: LiveFareStrategy | None
    savings: Decimal | None
    verdict: str
    detail: str


class LiveBackToBackResponse(BaseModel):
    queried_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    provider: str
    comparisons: list[LiveBackToBackComparison]
    warnings: list[str]
    usage: UsageStatus | None = None


class LiveBackToBackService:
    roles = (
        "conventional_first",
        "conventional_second",
        "head_one_way",
        "middle_two_segment",
        "tail_one_way",
    )

    def __init__(self, provider: FlightProvider) -> None:
        self.provider = provider

    @staticmethod
    def _request(
        payload: LiveBackToBackSearch,
        trip_type: TripType,
        legs: list[TripLeg],
    ) -> SearchCreate:
        first = legs[0]
        return SearchCreate(
            trip_type=trip_type,
            origin=first.origin if trip_type != TripType.MULTI_CITY else None,
            destination=first.destination if trip_type != TripType.MULTI_CITY else None,
            departure_date=first.departure_date if trip_type != TripType.MULTI_CITY else None,
            return_date=(legs[1].departure_date if trip_type == TripType.ROUND_TRIP else None),
            legs=legs if trip_type == TripType.MULTI_CITY else [],
            travelers=payload.travelers,
            modules=[SearchModule.FLIGHT],
            cabin_class=payload.cabin_class,
            currency=payload.currency,
            locale=payload.locale,
        )

    def _requests(self, payload: LiveBackToBackSearch) -> dict[str, SearchCreate]:
        origin = payload.origin
        first = payload.first_destination
        second = payload.second_destination
        return {
            "conventional_first": self._request(
                payload,
                TripType.ROUND_TRIP,
                [
                    TripLeg(
                        origin=origin,
                        destination=first,
                        departure_date=payload.first_trip.departure_date,
                    ),
                    TripLeg(
                        origin=first,
                        destination=origin,
                        departure_date=payload.first_trip.return_date,
                    ),
                ],
            ),
            "conventional_second": self._request(
                payload,
                TripType.ROUND_TRIP,
                [
                    TripLeg(
                        origin=origin,
                        destination=second,
                        departure_date=payload.second_trip.departure_date,
                    ),
                    TripLeg(
                        origin=second,
                        destination=origin,
                        departure_date=payload.second_trip.return_date,
                    ),
                ],
            ),
            "head_one_way": self._request(
                payload,
                TripType.ONE_WAY,
                [
                    TripLeg(
                        origin=origin,
                        destination=first,
                        departure_date=payload.first_trip.departure_date,
                    )
                ],
            ),
            "middle_two_segment": self._request(
                payload,
                TripType.MULTI_CITY,
                [
                    TripLeg(
                        origin=first,
                        destination=origin,
                        departure_date=payload.first_trip.return_date,
                    ),
                    TripLeg(
                        origin=origin,
                        destination=second,
                        departure_date=payload.second_trip.departure_date,
                    ),
                ],
            ),
            "tail_one_way": self._request(
                payload,
                TripType.ONE_WAY,
                [
                    TripLeg(
                        origin=second,
                        destination=origin,
                        departure_date=payload.second_trip.return_date,
                    )
                ],
            ),
        }

    @staticmethod
    def _carrier(offer: FlightOffer) -> str:
        return offer.marketing_airline or offer.airline

    @classmethod
    def _best(
        cls,
        roles: tuple[str, ...],
        candidates: dict[str, list[FlightOffer]],
        currency: str,
        *,
        same_airline: bool,
    ) -> LiveFareStrategy | None:
        available = {
            role: [offer for offer in candidates.get(role, []) if offer.currency == currency]
            for role in roles
        }
        if any(not available[role] for role in roles):
            return None
        if same_airline:
            carriers = set.intersection(
                *(set(cls._carrier(offer) for offer in available[role]) for role in roles)
            )
            choices = []
            for carrier in carriers:
                offers = [
                    min(
                        (offer for offer in available[role] if cls._carrier(offer) == carrier),
                        key=lambda item: (item.total_price, item.provider_offer_id),
                    )
                    for role in roles
                ]
                choices.append((sum((offer.total_price for offer in offers), Decimal(0)), offers))
            if not choices:
                return None
            _, selected = min(choices, key=lambda item: item[0])
        else:
            selected = [
                min(available[role], key=lambda item: (item.total_price, item.provider_offer_id))
                for role in roles
            ]
        return LiveFareStrategy(
            components=[
                LiveFareComponent(role=role, offer=offer)
                for role, offer in zip(roles, selected, strict=True)
            ],
            total_price=sum((offer.total_price for offer in selected), Decimal(0)),
            currency=currency,
        )

    async def search(self, payload: LiveBackToBackSearch) -> LiveBackToBackResponse:
        requests = self._requests(payload)
        results = await asyncio.gather(
            *(self.provider.search_flights(requests[role]) for role in self.roles),
            return_exceptions=True,
        )
        candidates: dict[str, list[FlightOffer]] = {}
        warnings: list[str] = []
        for role, result in zip(self.roles, results, strict=True):
            if isinstance(result, BaseException):
                candidates[role] = []
                warnings.append(f"{role}：{result}")
            else:
                candidates[role] = result
                if not result:
                    warnings.append(f"{role}：沒有可用即時票價")
        comparisons = []
        for mode in LiveComparisonMode:
            same = mode == LiveComparisonMode.SAME_AIRLINE
            conventional = self._best(
                ("conventional_first", "conventional_second"),
                candidates,
                payload.currency,
                same_airline=same,
            )
            reverse = self._best(
                ("head_one_way", "middle_two_segment", "tail_one_way"),
                candidates,
                payload.currency,
                same_airline=same,
            )
            savings = (
                conventional.total_price - reverse.total_price
                if conventional and reverse
                else None
            )
            verdict = (
                "back_to_back_cheaper"
                if savings is not None and savings > 0
                else "conventional_cheaper"
                if savings is not None and savings < 0
                else "same_price"
                if savings == 0
                else "comparison_unavailable"
            )
            comparisons.append(
                LiveBackToBackComparison(
                    mode=mode,
                    conventional=conventional,
                    back_to_back=reverse,
                    savings=savings,
                    verdict=verdict,
                    detail=(
                        "所有必要票價均來自同一次使用者主動即時比較。"
                        if savings is not None
                        else "缺少一張以上必要票價，不建立不完整方案。"
                    ),
                )
            )
        return LiveBackToBackResponse(
            provider=self.provider.name,
            comparisons=comparisons,
            warnings=warnings,
        )
