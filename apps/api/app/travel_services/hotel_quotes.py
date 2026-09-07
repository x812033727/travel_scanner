"""Provider-neutral, on-demand quote contract. No live adapters or price persistence in v1."""

import asyncio
import hashlib
from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any, Literal, Protocol, cast

from pydantic import Field, model_validator

from app.i18n import Locale
from app.models import HotelBookingOption, TravelServiceProduct
from app.travel_services.hotel_options import ready_option
from app.travel_services.schemas import CatalogConfig, HotelProvider, HotelQuotePolicy, StrictModel


class RoomOccupancy(StrictModel):
    adults: int = Field(ge=1, le=10)
    children_ages: list[int] = Field(default_factory=list, max_length=10)

    @model_validator(mode="after")
    def ages(self) -> "RoomOccupancy":
        if any(age < 0 or age > 17 for age in self.children_ages):
            raise ValueError("Child ages must be between 0 and 17")
        return self


class HotelQuoteRequest(StrictModel):
    check_in: date
    check_out: date
    rooms: list[RoomOccupancy] = Field(min_length=1, max_length=10)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    booker_country: str = Field(pattern=r"^[A-Z]{2}$")

    @model_validator(mode="after")
    def dates(self) -> "HotelQuoteRequest":
        if not 1 <= (self.check_out - self.check_in).days <= 365:
            raise ValueError("Invalid stay dates")
        return self


class HotelQuote(StrictModel):
    provider: HotelProvider
    property_id: str
    rate_id: str
    stay: HotelQuoteRequest
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    total: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    taxes: Decimal | None = Field(default=None, ge=0, max_digits=14, decimal_places=2)
    pay_at_property: Decimal | None = Field(default=None, ge=0, max_digits=14, decimal_places=2)
    mandatory_charges_complete: bool = False
    public_rate: bool = True
    room_name: str = Field(max_length=255)
    # Provider-approved, locale-appropriate factual terms, never an AI-written guarantee.
    bed_description: str | None = Field(default=None, max_length=500)
    meal_description: str | None = Field(default=None, max_length=500)
    cancellation_description: str | None = Field(default=None, max_length=1000)
    payment_description: str | None = Field(default=None, max_length=1000)
    # Requires reviewed cross-platform room identity; never populate from name similarity.
    room_match_key: str | None = None
    bed_key: str | None = None
    meal_key: str | None = None
    cancellation_key: str | None = None
    payment_key: str | None = None
    retrieved_at: datetime
    expires_at: datetime

    @model_validator(mode="after")
    def timestamps(self) -> "HotelQuote":
        if any(
            amount is not None and amount > self.total
            for amount in (self.taxes, self.pay_at_property)
        ):
            raise ValueError("Total must include all stated taxes and at-property charges")
        if (
            not self.retrieved_at.tzinfo
            or not self.expires_at.tzinfo
            or self.expires_at <= self.retrieved_at
        ):
            raise ValueError("Bounded timezone-aware quote validity required")
        return self


class HotelQuoteAdapter(Protocol):
    async def search(
        self, property_id: str, query: HotelQuoteRequest, locale: Locale
    ) -> list[HotelQuote]: ...


# Adding an adapter is an explicit integration/review change, not a credentials-only switch.
ADAPTERS: dict[str, HotelQuoteAdapter] = {}


def comparable_key(
    quote: HotelQuote, query: HotelQuoteRequest, now: datetime
) -> tuple[str, ...] | None:
    terms = (
        quote.room_match_key,
        quote.bed_key,
        quote.meal_key,
        quote.cancellation_key,
        quote.payment_key,
    )
    if (
        quote.stay != query
        or quote.currency != query.currency
        or not quote.public_rate
        or not quote.mandatory_charges_complete
        or quote.taxes is None
        or quote.pay_at_property is None
        or not quote.retrieved_at <= now < quote.expires_at
        or not all(terms)
    ):
        return None
    return tuple(str(term) for term in terms)


def rank_quotes(
    quotes: list[HotelQuote], query: HotelQuoteRequest, now: datetime
) -> list[dict[str, Any]]:
    current = [q for q in quotes if q.stay == query and q.retrieved_at <= now < q.expires_at]
    groups: dict[tuple[str, ...], list[HotelQuote]] = {}
    for quote in current:
        key = comparable_key(quote, query, now)
        if key:
            groups.setdefault(key, []).append(quote)
    result = []
    for quote in current:
        key = comparable_key(quote, query, now)
        peers = groups.get(key, []) if key else []
        eligible = len({q.provider for q in peers}) >= 2
        result.append(
            {
                **quote.model_dump(mode="json"),
                "comparable": eligible,
                "comparison_group": hashlib.sha256(repr(key).encode()).hexdigest()
                if eligible
                else None,
                "lowest_in_group": eligible and quote.total == min(q.total for q in peers),
            }
        )
    # Do not pretend unmatched rates belong to one price ranking.
    return sorted(
        result,
        key=lambda q: (
            not q["comparable"],
            q.get("room_match_key") or "",
            Decimal(q["total"]) if q["comparable"] else Decimal(0),
            q["provider"],
        ),
    )


async def reserve_calls(redis: Any, provider: str, policy: HotelQuotePolicy) -> bool:
    now = datetime.now(UTC)
    for suffix, limit, ttl in (
        (now.strftime("%Y-%m-%d"), policy.daily_limit, 172800),
        (now.strftime("%Y-%m-%dT%H:%M"), policy.per_minute_limit, 120),
    ):
        key = f"hotel-quotes:calls:{provider}:{suffix}"
        async with redis.pipeline(transaction=True) as pipe:
            pipe.incr(key)
            pipe.expire(key, ttl, nx=True)
            values = await pipe.execute()
        if int(values[0]) > limit:
            return False
    return True


async def search_quotes(
    product: TravelServiceProduct,
    query: HotelQuoteRequest,
    locale: Locale,
    config: CatalogConfig,
    redis: Any,
) -> dict[str, Any]:
    now = datetime.now(UTC)
    options = [
        o
        for o in product.hotel_options
        if ready_option(product, o, config, now) and o.provider != "official"
    ]

    async def fetch(option: HotelBookingOption) -> tuple[dict[str, str], list[HotelQuote]]:
        policy = config.hotel_quote_policies.get(cast(HotelProvider, option.provider))
        adapter = ADAPTERS.get(option.provider)
        state = {"provider": option.provider, "status": "not_configured"}
        if not policy or not policy.enabled or not adapter or not option.property_id:
            return state, []
        try:
            if not await reserve_calls(redis, option.provider, policy):
                return {**state, "status": "quota_exceeded"}, []
            async with asyncio.timeout(policy.timeout_seconds):
                quotes = [
                    HotelQuote.model_validate(q)
                    for q in await adapter.search(option.property_id, query, locale)
                ]
            if any(
                q.provider != option.provider
                or q.property_id != option.property_id
                or q.stay != query
                for q in quotes
            ):
                raise ValueError("Provider returned mismatched identity or search conditions")
            return {**state, "status": "available" if quotes else "no_availability"}, quotes
        except TimeoutError:
            return {**state, "status": "timeout"}, []
        except Exception:
            # Never leak credentials/provider payloads or block the other providers.
            return {**state, "status": "unavailable"}, []

    responses = await asyncio.gather(*(fetch(o) for o in options))
    states = [state for state, _ in responses]
    quotes = rank_quotes([q for _, quotes in responses for q in quotes], query, datetime.now(UTC))
    errors = {"timeout", "unavailable", "quota_exceeded"}
    status: Literal["available", "partial", "not_configured", "no_availability", "unavailable"]
    if any(s["status"] in errors for s in states):
        status = "partial" if quotes else "unavailable"
    elif quotes:
        status = "available"
    elif any(s["status"] in ("available", "no_availability") for s in states):
        status = "no_availability"
    else:
        status = "not_configured"
    return {"status": status, "providers": states, "quotes": quotes, "cached": False}
