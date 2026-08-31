import math
import re
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any, cast
from uuid import NAMESPACE_URL, UUID, uuid5

import httpx
from redis.asyncio import Redis

from app.config import Settings, get_settings
from app.providers.schemas import (
    ActionKind,
    ActivityOffer,
    FlightOffer,
    FlightSegment,
    HotelOffer,
    OfferRefreshResult,
    SourceMode,
    TransportOffer,
)
from app.search.schemas import SearchCreate, TripType

CITY_CODE_OVERRIDES = {
    "NRT": "TYO",
    "HND": "TYO",
    "KIX": "OSA",
    "ITM": "OSA",
    "UKB": "OSA",
    "ICN": "SEL",
    "GMP": "SEL",
    "DMK": "BKK",
}


def stable_offer_id(kind: str, provider_id: str) -> UUID:
    return uuid5(NAMESPACE_URL, f"travel-scanner:amadeus:{kind}:{provider_id}")


def decimal_value(value: object, default: str = "0") -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return Decimal(default)


def parse_datetime(value: object, fallback: datetime | None = None) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=UTC)
    if isinstance(value, str) and value:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
    return fallback or datetime.now(UTC)


def duration_minutes(value: object, default: int = 120) -> int:
    if isinstance(value, int | float):
        return max(1, int(value))
    if not isinstance(value, str):
        return default
    match = re.fullmatch(r"P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?", value)
    if not match:
        return default
    days, hours, minutes = (int(part or 0) for part in match.groups())
    return max(1, days * 1440 + hours * 60 + minutes)


class AmadeusProvider:
    name = "amadeus"

    def __init__(
        self,
        redis: Redis,
        settings: Settings | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.redis = redis
        self.settings = settings or get_settings()
        self.client = client
        self._offers: dict[UUID, FlightOffer | HotelOffer] = {}

    @property
    def source_mode(self) -> SourceMode:
        return (
            SourceMode.LIVE
            if self.settings.amadeus_env.lower() == "production"
            else SourceMode.TEST
        )

    async def _send(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        try:
            if self.client is not None:
                return await self.client.request(method, url, **kwargs)
            async with httpx.AsyncClient(timeout=self.settings.provider_timeout_seconds) as client:
                return await client.request(method, url, **kwargs)
        except httpx.HTTPError as exc:
            raise ConnectionError(f"Amadeus request failed: {exc}") from exc

    async def _token(self) -> str:
        cached = await self.redis.get("provider:amadeus:oauth-token")
        if cached:
            return cached.decode() if isinstance(cached, bytes) else str(cached)
        if not self.settings.amadeus_configured:
            raise ConnectionError("Amadeus credentials are not configured")
        response = await self._send(
            "POST",
            f"{self.settings.amadeus_base_url}/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.settings.amadeus_client_id,
                "client_secret": self.settings.amadeus_client_secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if response.status_code >= 400:
            raise ConnectionError(f"Amadeus authentication failed ({response.status_code})")
        payload = cast(dict[str, Any], response.json())
        token = str(payload.get("access_token") or "")
        if not token:
            raise ConnectionError("Amadeus authentication returned no access token")
        ttl = max(30, int(payload.get("expires_in") or 1800) - 60)
        await self.redis.set("provider:amadeus:oauth-token", token, ex=ttl)
        return token

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        token = await self._token()
        response = await self._send(
            method,
            f"{self.settings.amadeus_base_url}{path}",
            params=params,
            json=json,
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        )
        if response.status_code == 401:
            await self.redis.delete("provider:amadeus:oauth-token")
        if response.status_code >= 400:
            raise ConnectionError(f"Amadeus {path} failed ({response.status_code})")
        return cast(dict[str, Any], response.json())

    @staticmethod
    def _route(query: SearchCreate) -> tuple[str, str, date, date]:
        if query.legs:
            first = query.legs[0]
            returning = query.return_date or first.departure_date + timedelta(days=5)
            return first.origin.upper(), first.destination.upper(), first.departure_date, returning
        departure = query.departure_date or datetime.now(UTC).date()
        returning = query.return_date or departure + timedelta(days=5)
        return (
            (query.origin or "TPE").upper(),
            (query.destination or "NRT").upper(),
            departure,
            returning,
        )

    async def search_flights(self, query: SearchCreate) -> list[FlightOffer]:
        origin, destination, departure, returning = self._route(query)
        if query.trip_type == TripType.MULTI_CITY:
            travelers = [
                {"id": str(index + 1), "travelerType": "ADULT"}
                for index in range(query.travelers.adults)
            ]
            travelers.extend(
                {"id": str(len(travelers) + 1), "travelerType": "CHILD"}
                for _ in range(query.travelers.children)
            )
            payload = await self._request(
                "POST",
                "/v2/shopping/flight-offers",
                json={
                    "currencyCode": query.currency,
                    "originDestinations": [
                        {
                            "id": str(index + 1),
                            "originLocationCode": leg.origin.upper(),
                            "destinationLocationCode": leg.destination.upper(),
                            "departureDateTimeRange": {"date": leg.departure_date.isoformat()},
                        }
                        for index, leg in enumerate(query.legs)
                    ],
                    "travelers": travelers,
                    "sources": ["GDS"],
                    "searchCriteria": {
                        "maxFlightOffers": 12,
                        "flightFilters": {
                            "cabinRestrictions": [
                                {
                                    "cabin": query.cabin_class.value.upper(),
                                    "coverage": "MOST_SEGMENTS",
                                    "originDestinationIds": [
                                        str(index + 1) for index in range(len(query.legs))
                                    ],
                                }
                            ]
                        },
                    },
                },
            )
        else:
            params: dict[str, Any] = {
                "originLocationCode": origin,
                "destinationLocationCode": destination,
                "departureDate": departure.isoformat(),
                "adults": query.travelers.adults,
                "children": query.travelers.children,
                "currencyCode": query.currency,
                "travelClass": query.cabin_class.value.upper(),
                "max": 12,
            }
            if query.trip_type == TripType.ROUND_TRIP:
                params["returnDate"] = returning.isoformat()
            payload = await self._request("GET", "/v2/shopping/flight-offers", params=params)
        carriers = cast(dict[str, str], payload.get("dictionaries", {}).get("carriers", {}))
        now = datetime.now(UTC)
        offers: list[FlightOffer] = []
        for row in cast(list[dict[str, Any]], payload.get("data", [])):
            itineraries = cast(list[dict[str, Any]], row.get("itineraries", []))
            if not itineraries:
                continue
            flat_segments: list[FlightSegment] = []
            raw_segments: list[dict[str, Any]] = []
            for itinerary in itineraries:
                for segment in cast(list[dict[str, Any]], itinerary.get("segments", [])):
                    departure_data = cast(dict[str, Any], segment.get("departure", {}))
                    arrival_data = cast(dict[str, Any], segment.get("arrival", {}))
                    carrier = str(segment.get("carrierCode") or "")
                    flat_segments.append(
                        FlightSegment(
                            origin=str(departure_data.get("iataCode") or origin),
                            destination=str(arrival_data.get("iataCode") or destination),
                            departure_time=parse_datetime(departure_data.get("at")),
                            arrival_time=parse_datetime(arrival_data.get("at")),
                            airline=carriers.get(carrier, carrier),
                            flight_number=f"{carrier}{segment.get('number') or ''}",
                        )
                    )
                    raw_segments.append(segment)
            if not flat_segments:
                continue
            price = cast(dict[str, Any], row.get("price", {}))
            total = decimal_value(price.get("grandTotal") or price.get("total"))
            base = decimal_value(price.get("base"))
            taxes = max(Decimal(0), total - base)
            provider_id = str(row.get("id") or len(offers))
            offer_id = stable_offer_id("flight", provider_id)
            first_itinerary = itineraries[0]
            outbound = cast(list[dict[str, Any]], first_itinerary.get("segments", []))
            returning_segments = (
                cast(list[dict[str, Any]], itineraries[1].get("segments", []))
                if query.trip_type == TripType.ROUND_TRIP and len(itineraries) > 1
                else []
            )
            outbound_end = (
                len(outbound) - 1
                if query.trip_type == TripType.ROUND_TRIP
                else len(flat_segments) - 1
            )
            first_segment = raw_segments[0]
            carrier = str(first_segment.get("carrierCode") or "")
            offer = FlightOffer(
                id=offer_id,
                provider=self.name,
                provider_offer_id=provider_id,
                currency=str(price.get("currency") or query.currency),
                retrieved_at=now,
                expires_at=now + timedelta(minutes=10),
                source_mode=self.source_mode,
                is_mock=False,
                is_bookable=True,
                action_kind=ActionKind.RECHECK,
                origin=flat_segments[0].origin,
                destination=flat_segments[outbound_end].destination,
                departure_time=flat_segments[0].departure_time,
                arrival_time=flat_segments[outbound_end].arrival_time,
                return_departure_time=(
                    parse_datetime(returning_segments[0].get("departure", {}).get("at"))
                    if returning_segments
                    else None
                ),
                return_arrival_time=(
                    parse_datetime(returning_segments[-1].get("arrival", {}).get("at"))
                    if returning_segments
                    else None
                ),
                duration_minutes=sum(
                    duration_minutes(item.get("duration")) for item in itineraries
                ),
                segments=flat_segments,
                stops=sum(
                    max(0, len(cast(list[Any], item.get("segments", []))) - 1)
                    for item in itineraries
                ),
                airline=carriers.get(carrier, carrier),
                flight_number=f"{carrier}{first_segment.get('number') or ''}",
                cabin_class=query.cabin_class.value,
                base_price=base,
                taxes=taxes,
                fees=Decimal(0),
                baggage_price=Decimal(0),
                total_price=total,
                carry_on=True,
                checked_baggage_kg=0,
                refundable=bool(row.get("pricingOptions", {}).get("refundableFare")),
                changeable=not bool(row.get("instantTicketingRequired")),
                marketing_airline=carriers.get(carrier, carrier),
                operating_airlines=list(
                    dict.fromkeys(segment.airline for segment in flat_segments)
                ),
                last_verified_at=now,
                clickout_available=False,
                arrival_day_offset=(
                    flat_segments[outbound_end].arrival_time.date()
                    - flat_segments[0].departure_time.date()
                ).days,
            )
            self._offers[offer_id] = offer
            offers.append(offer)
        return offers

    async def _hotel_catalog(self, destination: str) -> list[dict[str, Any]]:
        city_code = CITY_CODE_OVERRIDES.get(destination, destination)
        payload = await self._request(
            "GET",
            "/v1/reference-data/locations/hotels/by-city",
            params={"cityCode": city_code, "radius": 20, "radiusUnit": "KM"},
        )
        return cast(list[dict[str, Any]], payload.get("data", []))[:20]

    async def search_hotels(self, query: SearchCreate) -> list[HotelOffer]:
        _, destination, check_in, check_out = self._route(query)
        catalog = await self._hotel_catalog(destination)
        hotel_ids = [str(item.get("hotelId")) for item in catalog if item.get("hotelId")]
        if not hotel_ids:
            return []
        catalog_by_id = {str(item.get("hotelId")): item for item in catalog}
        payload = await self._request(
            "GET",
            "/v3/shopping/hotel-offers",
            params={
                "hotelIds": ",".join(hotel_ids),
                "adults": query.travelers.adults,
                "roomQuantity": query.travelers.rooms,
                "checkInDate": check_in.isoformat(),
                "checkOutDate": check_out.isoformat(),
                "currency": query.currency,
                "bestRateOnly": "true",
            },
        )
        now = datetime.now(UTC)
        nights = max(1, (check_out - check_in).days)
        offers: list[HotelOffer] = []
        for row in cast(list[dict[str, Any]], payload.get("data", [])):
            hotel = cast(dict[str, Any], row.get("hotel", {}))
            hotel_id = str(hotel.get("hotelId") or "")
            reference = catalog_by_id.get(hotel_id, {})
            geo = cast(
                dict[str, Any],
                hotel if hotel.get("latitude") else reference.get("geoCode", {}),
            )
            for raw_offer in cast(list[dict[str, Any]], row.get("offers", []))[:2]:
                price = cast(dict[str, Any], raw_offer.get("price", {}))
                raw_total = decimal_value(price.get("total"))
                raw_base = decimal_value(price.get("base"), str(raw_total))
                total = raw_total * query.travelers.rooms
                base = raw_base * query.travelers.rooms
                provider_id = str(raw_offer.get("id") or f"{hotel_id}-{len(offers)}")
                offer_id = stable_offer_id("hotel", provider_id)
                policies = cast(dict[str, Any], raw_offer.get("policies", {}))
                cancellations = cast(list[dict[str, Any]], policies.get("cancellations", []))
                cancellation_text = "; ".join(
                    str(item.get("description", {}).get("text") or item.get("deadline") or "")
                    for item in cancellations
                    if item
                )
                room = cast(dict[str, Any], raw_offer.get("room", {}))
                description = str(room.get("description", {}).get("text") or "標準客房")
                board_type = str(raw_offer.get("boardType") or "")
                address = reference.get("address", {})
                if isinstance(address, dict):
                    address_text = " ".join(str(item) for item in address.get("lines", []))
                else:
                    address_text = str(address or "")
                latitude = float(geo.get("latitude") or 0)
                longitude = float(geo.get("longitude") or 0)
                offer = HotelOffer(
                    id=offer_id,
                    provider=self.name,
                    provider_offer_id=provider_id,
                    currency=str(price.get("currency") or query.currency),
                    retrieved_at=now,
                    expires_at=now + timedelta(minutes=10),
                    source_mode=self.source_mode,
                    is_mock=False,
                    is_bookable=True,
                    action_kind=ActionKind.RECHECK,
                    cancellation_policy=cancellation_text or None,
                    hotel_id=hotel_id,
                    hotel_name=str(hotel.get("name") or reference.get("name") or hotel_id),
                    latitude=latitude,
                    longitude=longitude,
                    rating=float(reference.get("rating") or hotel.get("rating") or 0),
                    room_type=description[:240],
                    check_in=parse_datetime(f"{check_in.isoformat()}T15:00:00+00:00"),
                    check_out=parse_datetime(f"{check_out.isoformat()}T11:00:00+00:00"),
                    nights=nights,
                    base_price=base,
                    taxes=max(Decimal(0), total - base),
                    fees=Decimal(0),
                    total_price=total,
                    nightly_price=(total / nights).quantize(Decimal("0.01")),
                    breakfast_included="BREAKFAST" in board_type.upper(),
                    refundable="NON_REFUNDABLE" not in cancellation_text.upper(),
                    station_walk_minutes=15,
                    address=address_text or None,
                    amenities=[str(value) for value in reference.get("amenities", [])],
                )
                self._offers[offer_id] = offer
                offers.append(offer)
        return offers

    async def _city_center(self, destination: str) -> tuple[float, float]:
        payload = await self._request(
            "GET",
            "/v1/reference-data/locations",
            params={"subType": "CITY,AIRPORT", "keyword": destination, "page[limit]": 1},
        )
        rows = cast(list[dict[str, Any]], payload.get("data", []))
        geo = cast(dict[str, Any], rows[0].get("geoCode", {})) if rows else {}
        return float(geo.get("latitude") or 0), float(geo.get("longitude") or 0)

    async def search_activities(self, query: SearchCreate) -> list[ActivityOffer]:
        _, destination, _, _ = self._route(query)
        latitude, longitude = await self._city_center(destination)
        if math.isclose(latitude, 0) and math.isclose(longitude, 0):
            return []
        payload = await self._request(
            "GET",
            "/v1/shopping/activities",
            params={"latitude": latitude, "longitude": longitude, "radius": 20},
        )
        now = datetime.now(UTC)
        offers: list[ActivityOffer] = []
        for row in cast(list[dict[str, Any]], payload.get("data", []))[:12]:
            provider_id = str(row.get("id") or len(offers))
            price = cast(dict[str, Any], row.get("price", {}))
            geo = cast(dict[str, Any], row.get("geoCode", {}))
            pictures = [str(value) for value in cast(list[Any], row.get("pictures", []))]
            booking_url = str(row.get("bookingLink") or "") or None
            offers.append(
                ActivityOffer(
                    id=stable_offer_id("activity", provider_id),
                    provider=self.name,
                    provider_offer_id=provider_id,
                    currency=str(price.get("currencyCode") or query.currency),
                    booking_url=booking_url,
                    retrieved_at=now,
                    expires_at=now + timedelta(hours=1),
                    source_mode=self.source_mode,
                    is_mock=False,
                    is_bookable=booking_url is not None,
                    action_kind=ActionKind.DEEP_LINK if booking_url else ActionKind.RECHECK,
                    images=pictures,
                    title=str(row.get("name") or "在地活動"),
                    city=destination,
                    latitude=float(geo.get("latitude") or latitude),
                    longitude=float(geo.get("longitude") or longitude),
                    duration_minutes=duration_minutes(row.get("minimumDuration")),
                    price=decimal_value(price.get("amount")),
                    rating=float(row.get("rating") or 0),
                    category="experience",
                    description=str(row.get("shortDescription") or "") or None,
                )
            )
        return offers

    async def search_transport(self, query: SearchCreate) -> list[TransportOffer]:
        _, destination, departure, _ = self._route(query)
        latitude, longitude = await self._city_center(destination)
        payload = await self._request(
            "POST",
            "/v1/shopping/transfer-offers",
            json={
                "startLocationCode": destination,
                "endGeoCode": {"latitude": latitude, "longitude": longitude},
                "startDateTime": f"{departure.isoformat()}T12:00:00",
                "passengers": query.travelers.adults + query.travelers.children,
            },
        )
        now = datetime.now(UTC)
        offers: list[TransportOffer] = []
        for row in cast(list[dict[str, Any]], payload.get("data", []))[:8]:
            provider_id = str(row.get("id") or len(offers))
            quotation = cast(dict[str, Any], row.get("quotation", {}))
            start = cast(dict[str, Any], row.get("start", {}))
            end = cast(dict[str, Any], row.get("end", {}))
            departure_time = parse_datetime(start.get("dateTime"), now)
            minutes = duration_minutes(row.get("duration"), 60)
            booking_url = str(row.get("bookingLink") or "") or None
            vehicle = cast(dict[str, Any], row.get("vehicle", {}))
            offers.append(
                TransportOffer(
                    id=stable_offer_id("transport", provider_id),
                    provider=self.name,
                    provider_offer_id=provider_id,
                    currency=str(quotation.get("currencyCode") or query.currency),
                    booking_url=booking_url,
                    retrieved_at=now,
                    expires_at=now + timedelta(minutes=15),
                    source_mode=self.source_mode,
                    is_mock=False,
                    is_bookable=booking_url is not None,
                    action_kind=ActionKind.DEEP_LINK if booking_url else ActionKind.RECHECK,
                    origin=str(start.get("name") or destination),
                    destination=str(end.get("name") or "市區"),
                    transport_type=str(
                        vehicle.get("description") or row.get("transferType") or "接送"
                    ),
                    departure_time=departure_time,
                    arrival_time=departure_time + timedelta(minutes=minutes),
                    duration_minutes=minutes,
                    price=decimal_value(quotation.get("monetaryAmount")),
                    convenience_score=88,
                )
            )
        return offers

    async def refresh_offer(
        self, offer: FlightOffer, query: SearchCreate | None = None
    ) -> OfferRefreshResult:
        price = offer.total_price
        refreshed = None
        if query is not None:
            candidates = await self.search_flights(query)
            refreshed = next(
                (
                    item
                    for item in candidates
                    if item.flight_number == offer.flight_number
                    and item.departure_time == offer.departure_time
                ),
                None,
            )
        new_price = refreshed.total_price if refreshed else price
        return OfferRefreshResult(
            offer_id=offer.id,
            old_price=price,
            new_price=new_price,
            price_change=new_price - price,
            still_available=refreshed is not None,
            refreshed_at=datetime.now(UTC),
            offer=refreshed,
        )

    async def clickout(self, offer: FlightOffer) -> str | None:
        return None

    async def get_offer_details(self, offer_id: UUID) -> FlightOffer | None:
        offer = self._offers.get(offer_id)
        return offer if isinstance(offer, FlightOffer) else None

    async def get_hotel_details(self, hotel_id: str) -> dict[str, str]:
        return {"hotel_id": hotel_id, "source": self.name}
