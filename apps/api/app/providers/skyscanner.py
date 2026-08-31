import asyncio
import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any, cast
from urllib.parse import urlparse
from uuid import NAMESPACE_URL, uuid5

import httpx
from redis.asyncio import Redis

from app.config import Settings, get_settings
from app.providers.base import FlightSearchBatch, FlightSearchState
from app.providers.schemas import (
    ActionKind,
    FlightOffer,
    FlightSegment,
    OfferRefreshResult,
    SourceMode,
)
from app.search.schemas import SearchCreate, TripType

SKYSCANNER_ATTRIBUTION_URL = "https://www.skyscanner.net"


def _items(value: object) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        return [cast(dict[str, Any], item) for item in value.values() if isinstance(item, dict)]
    if isinstance(value, list):
        return [cast(dict[str, Any], item) for item in value if isinstance(item, dict)]
    return []


def _indexed(value: object) -> dict[str, dict[str, Any]]:
    if isinstance(value, dict):
        return {
            str(key): cast(dict[str, Any], item)
            for key, item in value.items()
            if isinstance(item, dict)
        }
    return {
        str(item.get("id")): item
        for item in _items(value)
        if item.get("id") is not None
    }


def _decimal(value: object) -> Decimal:
    try:
        return Decimal(str(value or "0"))
    except (InvalidOperation, TypeError, ValueError):
        return Decimal(0)


def _money(value: object) -> Decimal:
    if not isinstance(value, dict):
        return _decimal(value)
    amount = _decimal(value.get("amount"))
    unit = str(value.get("unit") or "").upper()
    if "MICRO" in unit:
        return amount / Decimal(1_000_000)
    if "MILLI" in unit:
        return amount / Decimal(1_000)
    return amount


def _datetime(value: object) -> datetime:
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
    if isinstance(value, dict):
        data = cast(dict[str, Any], value)
        return datetime(
            int(data.get("year") or 1970),
            int(data.get("month") or 1),
            int(data.get("day") or 1),
            int(data.get("hour") or 0),
            int(data.get("minute") or 0),
            int(data.get("second") or 0),
            tzinfo=UTC,
        )
    return datetime.now(UTC)


def _https_url(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    parsed = urlparse(value)
    return value if parsed.scheme == "https" and parsed.netloc else None


def _deep_link(option: dict[str, Any]) -> str | None:
    direct = _https_url(option.get("deepLink") or option.get("deeplink"))
    if direct:
        return direct
    for item in _items(option.get("items")):
        link = _https_url(item.get("deepLink") or item.get("deeplink"))
        if link:
            return link
    return None


class SkyscannerProvider:
    name = "skyscanner"

    def __init__(
        self,
        redis: Redis,
        settings: Settings | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.redis = redis
        self.settings = settings or get_settings()
        self.client = client

    async def _send(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.settings.skyscanner_api_key:
            raise ConnectionError("Skyscanner API key is not configured")
        try:
            if self.client is not None:
                response = await self.client.post(
                    f"{self.settings.skyscanner_base_url}{path}",
                    json=payload,
                    headers={"x-api-key": self.settings.skyscanner_api_key},
                )
            else:
                async with httpx.AsyncClient(
                    timeout=self.settings.provider_timeout_seconds
                ) as client:
                    response = await client.post(
                        f"{self.settings.skyscanner_base_url}{path}",
                        json=payload,
                        headers={"x-api-key": self.settings.skyscanner_api_key},
                    )
        except httpx.HTTPError as exc:
            raise ConnectionError(f"Skyscanner request failed: {exc}") from exc
        if response.status_code == 429:
            raise ConnectionError("Skyscanner rate_limited (429)")
        if response.status_code >= 400:
            raise ConnectionError(f"Skyscanner request failed ({response.status_code})")
        return cast(dict[str, Any], response.json())

    def _query(self, query: SearchCreate) -> dict[str, Any]:
        if query.trip_type == TripType.MULTI_CITY:
            legs = query.legs
        else:
            assert query.origin and query.destination and query.departure_date
            from app.search.schemas import TripLeg

            legs = [
                TripLeg(
                    origin=query.origin,
                    destination=query.destination,
                    departure_date=query.departure_date,
                )
            ]
            if query.trip_type == TripType.ROUND_TRIP and query.return_date:
                legs.append(
                    TripLeg(
                        origin=query.destination,
                        destination=query.origin,
                        departure_date=query.return_date,
                    )
                )
        children = query.travelers.children_ages or [10] * query.travelers.children
        return {
            "market": self.settings.skyscanner_market,
            "locale": query.locale or self.settings.skyscanner_locale,
            "currency": query.currency or self.settings.skyscanner_currency,
            "queryLegs": [
                {
                    "originPlaceId": {"iata": leg.origin.upper()},
                    "destinationPlaceId": {"iata": leg.destination.upper()},
                    "date": {
                        "year": leg.departure_date.year,
                        "month": leg.departure_date.month,
                        "day": leg.departure_date.day,
                    },
                }
                for leg in legs
            ],
            "adults": query.travelers.adults,
            "childrenAges": children,
            "cabinClass": f"CABIN_CLASS_{query.cabin_class.value.upper()}",
        }

    @staticmethod
    def _state(payload: dict[str, Any]) -> FlightSearchState:
        status = str(
            payload.get("status")
            or cast(dict[str, Any], payload.get("content", {})).get("status")
            or ""
        ).upper()
        return (
            FlightSearchState.COMPLETE
            if status in {"RESULT_STATUS_COMPLETE", "COMPLETE"}
            else FlightSearchState.INCOMPLETE
        )

    async def _offers(
        self,
        payload: dict[str, Any],
        session_id: str,
        *,
        estimate: bool = False,
        cabin_class: str = "economy",
    ) -> list[FlightOffer]:
        content = cast(dict[str, Any], payload.get("content", payload))
        results = cast(dict[str, Any], content.get("results", content))
        itineraries = _items(results.get("itineraries"))
        legs = _indexed(results.get("legs"))
        segments = _indexed(results.get("segments"))
        places = _indexed(results.get("places"))
        carriers = _indexed(results.get("carriers"))
        agents = _indexed(results.get("agents"))
        now = datetime.now(UTC)
        normalized: list[FlightOffer] = []
        for itinerary in itineraries:
            itinerary_id = str(itinerary.get("id") or len(normalized))
            itinerary_legs = [legs.get(str(value), {}) for value in itinerary.get("legIds", [])]
            if not itinerary_legs and itinerary.get("legs"):
                itinerary_legs = _items(itinerary.get("legs"))
            if not itinerary_legs:
                continue
            options = _items(itinerary.get("pricingOptions")) or [{}]
            for option_index, option in enumerate(options[:3]):
                price = _money(option.get("price") or itinerary.get("price"))
                if price <= 0:
                    continue
                flat_segments: list[FlightSegment] = []
                marketing_names: list[str] = []
                operating_names: list[str] = []
                for leg in itinerary_legs:
                    raw_segments = [
                        segments.get(str(value), {}) for value in leg.get("segmentIds", [])
                    ]
                    if not raw_segments and leg.get("segments"):
                        raw_segments = _items(leg.get("segments"))
                    for segment in raw_segments:
                        marketing_id = str(
                            segment.get("marketingCarrierId")
                            or next(iter(leg.get("marketingCarrierIds", [])), "")
                        )
                        operating_id = str(segment.get("operatingCarrierId") or marketing_id)
                        marketing = carriers.get(marketing_id, {})
                        operating = carriers.get(operating_id, marketing)
                        marketing_name = str(
                            marketing.get("name") or marketing.get("iata") or marketing_id
                        )
                        operating_name = str(
                            operating.get("name") or operating.get("iata") or operating_id
                        )
                        marketing_names.append(marketing_name)
                        operating_names.append(operating_name)
                        origin_id = str(
                            segment.get("originPlaceId") or leg.get("originPlaceId") or ""
                        )
                        destination_id = str(
                            segment.get("destinationPlaceId") or leg.get("destinationPlaceId") or ""
                        )
                        origin_place = places.get(origin_id, {})
                        destination_place = places.get(destination_id, {})
                        flight_number = str(
                            segment.get("marketingFlightNumber")
                            or segment.get("flightNumber")
                            or ""
                        )
                        iata = str(marketing.get("iata") or "")
                        flat_segments.append(
                            FlightSegment(
                                origin=str(origin_place.get("iata") or origin_id),
                                destination=str(destination_place.get("iata") or destination_id),
                                departure_time=_datetime(
                                    segment.get("departureDateTime") or leg.get("departureDateTime")
                                ),
                                arrival_time=_datetime(
                                    segment.get("arrivalDateTime") or leg.get("arrivalDateTime")
                                ),
                                airline=marketing_name,
                                flight_number=f"{iata}{flight_number}",
                            )
                        )
                if not flat_segments:
                    first_leg, last_leg = itinerary_legs[0], itinerary_legs[-1]
                    origin_id = str(first_leg.get("originPlaceId") or "")
                    destination_id = str(last_leg.get("destinationPlaceId") or "")
                    flat_segments = [
                        FlightSegment(
                            origin=str(places.get(origin_id, {}).get("iata") or origin_id),
                            destination=str(
                                places.get(destination_id, {}).get("iata") or destination_id
                            ),
                            departure_time=_datetime(first_leg.get("departureDateTime")),
                            arrival_time=_datetime(last_leg.get("arrivalDateTime")),
                            airline="航空公司待確認",
                            flight_number="",
                        )
                    ]
                agent_ids = option.get("agentIds", [])
                if not agent_ids:
                    agent_ids = [item.get("agentId") for item in _items(option.get("items"))]
                agent = agents.get(str(next(iter(agent_ids), "")), {})
                link = None if estimate else _deep_link(option)
                provider_id = f"{itinerary_id}:{option.get('id') or option_index}"
                offer_id = uuid5(NAMESPACE_URL, f"travel-scanner:skyscanner:{provider_id}")
                departure = flat_segments[0].departure_time
                arrival = flat_segments[-1].arrival_time
                duration = sum(int(item.get("durationInMinutes") or 0) for item in itinerary_legs)
                stops = sum(int(item.get("stopCount") or 0) for item in itinerary_legs)
                primary = next((value for value in marketing_names if value), "航空公司待確認")
                offer = FlightOffer(
                    id=offer_id,
                    provider=self.name,
                    provider_offer_id=provider_id,
                    currency=self.settings.skyscanner_currency,
                    booking_url=None,
                    retrieved_at=now,
                    expires_at=now + timedelta(minutes=10),
                    source_mode=SourceMode.ESTIMATE if estimate else SourceMode.LIVE,
                    is_mock=False,
                    is_bookable=bool(link),
                    action_kind=ActionKind.NONE if estimate else ActionKind.DEEP_LINK,
                    attributions=["Skyscanner"],
                    attribution_urls=[SKYSCANNER_ATTRIBUTION_URL],
                    origin=flat_segments[0].origin,
                    destination=flat_segments[-1].destination,
                    departure_time=departure,
                    arrival_time=arrival,
                    duration_minutes=max(1, duration),
                    segments=flat_segments,
                    airline=primary,
                    flight_number=flat_segments[0].flight_number,
                    cabin_class=cabin_class,
                    base_price=price,
                    taxes=Decimal(0),
                    fees=Decimal(0),
                    baggage_price=Decimal(0),
                    total_price=price,
                    carry_on=False,
                    checked_baggage_kg=0,
                    refundable=False,
                    changeable=False,
                    stops=stops,
                    marketing_airline=primary,
                    operating_airlines=list(dict.fromkeys(operating_names)),
                    selling_agent=str(agent.get("name") or "") or None,
                    last_verified_at=now,
                    clickout_available=bool(link),
                    arrival_day_offset=(arrival.date() - departure.date()).days,
                )
                normalized.append(offer)
                await self.redis.set(
                    f"provider:skyscanner:offer:{offer.id}",
                    json.dumps(
                        {
                            "session_id": session_id,
                            "provider_offer_id": provider_id,
                            "clickout": link,
                        }
                    ),
                    ex=600,
                )
        unique = {offer.provider_offer_id: offer for offer in normalized}
        return sorted(unique.values(), key=lambda item: (item.total_price, item.provider_offer_id))

    async def start_search(self, query: SearchCreate) -> FlightSearchBatch:
        indicative = query.flexible_dates
        path = (
            "/apiservices/v3/flights/indicative/search"
            if indicative
            else "/apiservices/v3/flights/live/search/create"
        )
        payload = await self._send(path, {"query": self._query(query)})
        session_id = str(
            payload.get("sessionToken") or f"indicative-{datetime.now(UTC).timestamp()}"
        )
        await self.redis.set(
            f"provider:skyscanner:session:{session_id}",
            json.dumps({"cabin_class": query.cabin_class.value}),
            ex=600,
        )
        state = FlightSearchState.COMPLETE if indicative else self._state(payload)
        return FlightSearchBatch(
            session_id,
            await self._offers(
                payload,
                session_id,
                estimate=indicative,
                cabin_class=query.cabin_class.value,
            ),
            state,
        )

    async def poll_search(self, session_id: str) -> FlightSearchBatch:
        payload = await self._send(
            f"/apiservices/v3/flights/live/search/poll/{session_id}", {}
        )
        raw = await self.redis.get(f"provider:skyscanner:session:{session_id}")
        metadata = json.loads(raw.decode() if isinstance(raw, bytes) else str(raw)) if raw else {}
        return FlightSearchBatch(
            session_id,
            await self._offers(
                payload,
                session_id,
                cabin_class=str(metadata.get("cabin_class") or "economy"),
            ),
            self._state(payload),
        )

    async def search_flights(self, query: SearchCreate) -> list[FlightOffer]:
        first = await self.start_search(query)
        offers = {offer.provider_offer_id: offer for offer in first.offers}
        current = first
        for _ in range(self.settings.skyscanner_poll_attempts):
            if current.state == FlightSearchState.COMPLETE:
                break
            await asyncio.sleep(self.settings.skyscanner_poll_interval_seconds)
            current = await self.poll_search(first.session_id)
            offers.update({offer.provider_offer_id: offer for offer in current.offers})
        return sorted(offers.values(), key=lambda item: (item.total_price, item.provider_offer_id))

    async def refresh_offer(
        self, offer: FlightOffer, query: SearchCreate | None = None
    ) -> OfferRefreshResult:
        old_price = offer.total_price
        raw = await self.redis.get(f"provider:skyscanner:offer:{offer.id}")
        if not raw:
            return OfferRefreshResult(
                offer_id=offer.id,
                old_price=old_price,
                new_price=old_price,
                price_change=Decimal(0),
                still_available=False,
                refreshed_at=datetime.now(UTC),
            )
        meta = json.loads(raw.decode() if isinstance(raw, bytes) else str(raw))
        batch = await self.poll_search(str(meta["session_id"]))
        refreshed = next(
            (
                item
                for item in batch.offers
                if item.provider_offer_id == offer.provider_offer_id
            ),
            None,
        )
        return OfferRefreshResult(
            offer_id=offer.id,
            old_price=old_price,
            new_price=refreshed.total_price if refreshed else old_price,
            price_change=(refreshed.total_price - old_price) if refreshed else Decimal(0),
            still_available=refreshed is not None,
            refreshed_at=datetime.now(UTC),
            offer=refreshed,
        )

    async def clickout(self, offer: FlightOffer) -> str | None:
        raw = await self.redis.get(f"provider:skyscanner:offer:{offer.id}")
        if not raw:
            return None
        meta = json.loads(raw.decode() if isinstance(raw, bytes) else str(raw))
        return _https_url(meta.get("clickout"))

    async def get_offer_details(self, offer_id: object) -> FlightOffer | None:
        return None
