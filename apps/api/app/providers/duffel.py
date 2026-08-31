import json
import re
from datetime import UTC, datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any, cast
from uuid import NAMESPACE_URL, UUID, uuid5

import httpx
from redis.asyncio import Redis

from app.config import Settings, get_settings
from app.crawlers.fx import FxRateError, FxRateProvider
from app.providers.flight_keys import itinerary_key_from_segments
from app.providers.schemas import (
    ActionKind,
    FlightOffer,
    FlightSegment,
    OfferRefreshResult,
    SourceMode,
)
from app.search.schemas import SearchCreate, TripLeg, TripType


def _decimal(value: object) -> Decimal:
    try:
        return Decimal(str(value or "0"))
    except (InvalidOperation, TypeError, ValueError):
        return Decimal(0)


def _datetime(value: object, fallback: datetime | None = None) -> datetime:
    if isinstance(value, str) and value:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
    return fallback or datetime.now(UTC)


def _duration(value: object) -> int:
    match = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?", str(value or ""))
    if not match:
        return 1
    hours, minutes = (int(part or 0) for part in match.groups())
    return max(1, hours * 60 + minutes)


def _carrier_name(segment: dict[str, Any], kind: str) -> str:
    carrier = cast(dict[str, Any], segment.get(f"{kind}_carrier", {}))
    return str(carrier.get("name") or carrier.get("iata_code") or "航空公司待確認")


class DuffelProvider:
    name = "duffel"

    def __init__(
        self,
        redis: Redis,
        settings: Settings | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.redis = redis
        self.settings = settings or get_settings()
        self.client = client

    @property
    def source_mode(self) -> SourceMode:
        return SourceMode.LIVE if self.settings.duffel_env.lower() == "live" else SourceMode.TEST

    async def _request(
        self, method: str, path: str, *, payload: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        token = self.settings.duffel_access_token
        if not token:
            raise ConnectionError("Duffel access token is not configured")
        if self.settings.production and self.settings.duffel_env.lower() != "live":
            raise ConnectionError("正式環境禁止使用 Duffel test 報價")
        headers = {
            "Authorization": f"Bearer {token}",
            "Duffel-Version": "v2",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
            if self.client is not None:
                response = await self.client.request(
                    method,
                    f"{self.settings.duffel_base_url}{path}",
                    json=payload,
                    headers=headers,
                )
            else:
                timeout = self.settings.duffel_supplier_timeout_ms / 1000
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.request(
                        method,
                        f"{self.settings.duffel_base_url}{path}",
                        json=payload,
                        headers=headers,
                    )
        except httpx.HTTPError as exc:
            raise ConnectionError(f"Duffel request failed: {exc}") from exc
        if response.status_code == 429:
            raise ConnectionError("Duffel rate_limited (429)")
        if response.status_code >= 400:
            raise ConnectionError(f"Duffel request failed ({response.status_code})")
        body = cast(dict[str, Any], response.json())
        return cast(dict[str, Any], body.get("data", body))

    @staticmethod
    def _legs(query: SearchCreate) -> list[TripLeg]:
        if query.trip_type == TripType.MULTI_CITY:
            return query.legs
        assert query.origin and query.destination and query.departure_date
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
        return legs

    def _payload(self, query: SearchCreate) -> dict[str, Any]:
        ages = query.travelers.children_ages or [10] * query.travelers.children
        passengers: list[dict[str, Any]] = [
            {"type": "adult"} for _ in range(query.travelers.adults)
        ]
        passengers.extend({"age": age} for age in ages)
        return {
            "data": {
                "slices": [
                    {
                        "origin": leg.origin.upper(),
                        "destination": leg.destination.upper(),
                        "departure_date": leg.departure_date.isoformat(),
                    }
                    for leg in self._legs(query)
                ],
                "passengers": passengers,
                "cabin_class": query.cabin_class.value,
                "return_offers": True,
                "supplier_timeout": self.settings.duffel_supplier_timeout_ms,
            }
        }

    async def _normalize(
        self, rows: list[dict[str, Any]], query: SearchCreate
    ) -> list[FlightOffer]:
        now = datetime.now(UTC)
        offers: list[FlightOffer] = []
        for row in rows:
            provider_id = str(row.get("id") or "")
            slices = [item for item in row.get("slices", []) if isinstance(item, dict)]
            if not provider_id or not slices:
                continue
            segments: list[FlightSegment] = []
            for leg_index, slice_data in enumerate(slices):
                for segment in slice_data.get("segments", []):
                    if not isinstance(segment, dict):
                        continue
                    origin = cast(dict[str, Any], segment.get("origin", {}))
                    destination = cast(dict[str, Any], segment.get("destination", {}))
                    marketing = cast(dict[str, Any], segment.get("marketing_carrier", {}))
                    number = str(segment.get("marketing_carrier_flight_number") or "")
                    iata = str(marketing.get("iata_code") or "")
                    segments.append(
                        FlightSegment(
                            origin=str(origin.get("iata_code") or ""),
                            destination=str(destination.get("iata_code") or ""),
                            departure_time=_datetime(segment.get("departing_at")),
                            arrival_time=_datetime(segment.get("arriving_at")),
                            airline=_carrier_name(segment, "marketing"),
                            flight_number=f"{iata}{number}",
                            leg_index=leg_index,
                            departure_timezone="供應商當地時間",
                            arrival_timezone="供應商當地時間",
                        )
                    )
            if not segments:
                continue
            original_currency = str(row.get("total_currency") or query.currency).upper()
            original_total = _decimal(row.get("total_amount"))
            original_base = _decimal(row.get("base_amount"))
            original_tax = _decimal(row.get("tax_amount"))
            rate = Decimal(1)
            rate_at = now
            display_currency = original_currency
            if original_currency != "TWD":
                try:
                    fx = await FxRateProvider(self.settings, self.redis).rate_to_twd(
                        original_currency
                    )
                    rate = fx.rate
                    rate_at = datetime.combine(fx.as_of, datetime.min.time(), tzinfo=UTC)
                    display_currency = "TWD"
                except FxRateError:
                    rate = Decimal(1)
            total = (original_total * rate).quantize(Decimal("0.01"))
            base = (original_base * rate).quantize(Decimal("0.01"))
            taxes = (original_tax * rate).quantize(Decimal("0.01"))
            if taxes <= 0:
                taxes = max(Decimal(0), total - base)
            conditions = cast(dict[str, Any], row.get("conditions", {}))
            change = cast(dict[str, Any], conditions.get("change_before_departure", {}))
            refund = cast(dict[str, Any], conditions.get("refund_before_departure", {}))
            expires = _datetime(row.get("expires_at"), now + timedelta(minutes=30))
            offer_id = uuid5(NAMESPACE_URL, f"travel-scanner:duffel:{provider_id}")
            first_leg = [item for item in segments if item.leg_index == 0]
            second_leg = [item for item in segments if item.leg_index == 1]
            baggage = row.get("baggages") or []
            checked = max(
                (
                    int(item.get("quantity") or 0) * 23
                    for item in baggage
                    if isinstance(item, dict) and item.get("type") == "checked"
                ),
                default=0,
            )
            offer = FlightOffer(
                id=offer_id,
                provider=self.name,
                provider_offer_id=provider_id,
                currency=display_currency,
                retrieved_at=now,
                expires_at=expires,
                source_mode=self.source_mode,
                is_mock=False,
                is_bookable=False,
                action_kind=ActionKind.RECHECK,
                attributions=["Duffel"],
                attribution_urls=["https://duffel.com"],
                itinerary_key=itinerary_key_from_segments(segments, query.cabin_class.value),
                origin=first_leg[0].origin,
                destination=first_leg[-1].destination,
                departure_time=first_leg[0].departure_time,
                arrival_time=first_leg[-1].arrival_time,
                duration_minutes=sum(_duration(item.get("duration")) for item in slices),
                segments=segments,
                airline=first_leg[0].airline,
                flight_number=first_leg[0].flight_number,
                cabin_class=str(row.get("cabin_class") or query.cabin_class.value),
                base_price=base,
                taxes=taxes,
                fees=max(Decimal(0), total - base - taxes),
                baggage_price=Decimal(0),
                total_price=total,
                carry_on=True,
                checked_baggage_kg=checked,
                refundable=bool(refund.get("allowed")),
                changeable=bool(change.get("allowed")),
                return_departure_time=second_leg[0].departure_time if second_leg else None,
                return_arrival_time=second_leg[-1].arrival_time if second_leg else None,
                stops=sum(max(0, len(item.get("segments", [])) - 1) for item in slices),
                marketing_airline=first_leg[0].airline,
                operating_airlines=list(
                    dict.fromkeys(
                        _carrier_name(segment, "operating")
                        for item in slices
                        for segment in item.get("segments", [])
                        if isinstance(segment, dict)
                    )
                ),
                fare_brand=str(row.get("fare_brand_name") or "") or None,
                baggage_summary=f"托運行李 {checked} kg" if checked else "請向外站確認行李額度",
                last_verified_at=now,
                clickout_available=False,
                arrival_day_offset=(
                    first_leg[-1].arrival_time.date() - first_leg[0].departure_time.date()
                ).days,
                original_currency=original_currency,
                original_total_price=original_total,
                exchange_rate=rate if display_currency == "TWD" else None,
                exchange_rate_retrieved_at=rate_at if display_currency == "TWD" else None,
                verification_method="duffel_get_offer",
            )
            await self.redis.set(
                f"provider:duffel:offer:{offer.id}",
                json.dumps(row, default=str),
                ex=max(60, int((expires - now).total_seconds())),
            )
            offers.append(offer)
        return sorted(offers, key=lambda item: (item.total_price, item.provider_offer_id))

    async def search_flights(self, query: SearchCreate) -> list[FlightOffer]:
        payload = await self._request("POST", "/air/offer_requests", payload=self._payload(query))
        rows = [item for item in payload.get("offers", []) if isinstance(item, dict)]
        return await self._normalize(rows, query)

    async def refresh_offer(
        self, offer: FlightOffer, query: SearchCreate | None = None
    ) -> OfferRefreshResult:
        row = await self._request("GET", f"/air/offers/{offer.provider_offer_id}")
        if query is None:
            return OfferRefreshResult(
                offer_id=offer.id,
                old_price=offer.total_price,
                new_price=offer.total_price,
                price_change=Decimal(0),
                still_available=False,
                refreshed_at=datetime.now(UTC),
            )
        refreshed = (await self._normalize([row], query))[0]
        refreshed = refreshed.model_copy(update={"id": offer.id})
        return OfferRefreshResult(
            offer_id=offer.id,
            old_price=offer.total_price,
            new_price=refreshed.total_price,
            price_change=refreshed.total_price - offer.total_price,
            still_available=refreshed.expires_at > datetime.now(UTC),
            refreshed_at=datetime.now(UTC),
            offer=refreshed,
        )

    async def clickout(self, offer: FlightOffer) -> str | None:
        return None

    async def get_offer_details(self, offer_id: UUID) -> FlightOffer | None:
        return None
