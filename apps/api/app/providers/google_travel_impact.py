import json
import re
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, cast

import httpx
from redis.asyncio import Redis

from app.config import Settings, get_settings
from app.providers.schemas import FlightOffer, FlightSegment


class GoogleTravelImpactProvider:
    name = "google_tim"

    def __init__(
        self,
        redis: Redis,
        settings: Settings | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.redis = redis
        self.settings = settings or get_settings()
        self.client = client

    @staticmethod
    def _flight(segment: FlightSegment) -> dict[str, Any] | None:
        match = re.fullmatch(r"([A-Z0-9]{2,3})(\d{1,4}[A-Z]?)", segment.flight_number.upper())
        if not match:
            return None
        carrier, number = match.groups()
        numeric = re.match(r"\d+", number)
        if numeric is None:
            return None
        departure = segment.departure_time.date()
        return {
            "origin": segment.origin.upper(),
            "destination": segment.destination.upper(),
            "operatingCarrierCode": carrier,
            "flightNumber": int(numeric.group()),
            "departureDate": {
                "year": departure.year,
                "month": departure.month,
                "day": departure.day,
            },
        }

    async def _compute(self, flights: list[dict[str, Any]]) -> dict[str, Any]:
        key = self.settings.google_travel_impact_api_key
        if not key:
            raise ConnectionError("Google Travel Impact API key is not configured")
        try:
            if self.client is not None:
                response = await self.client.post(
                    f"{self.settings.google_travel_impact_base_url}/flights:computeFlightEmissions",
                    params={"key": key},
                    json={"flights": flights},
                )
            else:
                async with httpx.AsyncClient(
                    timeout=self.settings.provider_timeout_seconds
                ) as client:
                    response = await client.post(
                        f"{self.settings.google_travel_impact_base_url}/flights:computeFlightEmissions",
                        params={"key": key},
                        json={"flights": flights},
                    )
        except httpx.HTTPError as exc:
            raise ConnectionError(f"Google Travel Impact request failed: {exc}") from exc
        if response.status_code >= 400:
            raise ConnectionError(f"Google Travel Impact request failed ({response.status_code})")
        return cast(dict[str, Any], response.json())

    async def enrich(self, offers: list[FlightOffer]) -> list[FlightOffer]:
        if not offers or not self.settings.google_travel_impact_configured:
            return offers
        unique: dict[str, dict[str, Any]] = {}
        for offer in offers:
            for segment in offer.segments:
                flight = self._flight(segment)
                if flight:
                    unique[json.dumps(flight, sort_keys=True)] = flight
        if not unique:
            return offers
        keys = list(unique)
        cached_values: dict[str, dict[str, Any] | None] = {}
        missing: list[str] = []
        for value in keys:
            cache_key = f"provider:google-tim:{value}"
            cached = await self.redis.get(cache_key)
            if cached:
                cached_values[value] = json.loads(
                    cached.decode() if isinstance(cached, bytes) else str(cached)
                )
            else:
                missing.append(value)
        if missing:
            payload = await self._compute([unique[value] for value in missing])
            rows = payload.get("flightEmissions", [])
            model_version = payload.get("modelVersion")
            rows_by_flight = {
                json.dumps(row.get("flight"), sort_keys=True): row
                for row in rows
                if isinstance(row, dict) and isinstance(row.get("flight"), dict)
            }
            for index, value in enumerate(missing):
                row = rows_by_flight.get(value)
                if row is None:
                    row = (
                        rows[index]
                        if index < len(rows) and isinstance(rows[index], dict)
                        else None
                    )
                if row is not None and model_version and "modelVersion" not in row:
                    row = {
                        **row,
                        "modelVersion": (
                            json.dumps(model_version, sort_keys=True)
                            if isinstance(model_version, dict)
                            else str(model_version)
                        ),
                    }
                cached_values[value] = row
                await self.redis.set(
                    f"provider:google-tim:{value}",
                    json.dumps(row),
                    ex=self.settings.travel_impact_cache_ttl_seconds,
                )
        now = datetime.now(UTC)
        enriched: list[FlightOffer] = []
        cabin_fields = {
            "economy": "economy",
            "premium_economy": "premiumEconomy",
            "business": "business",
            "first": "first",
        }
        for offer in offers:
            grams = 0
            versions: list[str] = []
            complete = True
            for segment in offer.segments:
                flight = self._flight(segment)
                row = cached_values.get(json.dumps(flight, sort_keys=True)) if flight else None
                emissions = cast(dict[str, Any], row.get("emissionsGramsPerPax", {})) if row else {}
                emissions_value = emissions.get(cabin_fields.get(offer.cabin_class, "economy"))
                if emissions_value is None:
                    complete = False
                    break
                grams += int(emissions_value)
                version = row.get("modelVersion") if row else None
                if version:
                    versions.append(str(version))
            if complete and grams > 0:
                offer = offer.model_copy(
                    update={
                        "emissions_kg_per_pax": (Decimal(grams) / Decimal(1000)).quantize(
                            Decimal("0.01")
                        ),
                        "emissions_cabin": offer.cabin_class,
                        "emissions_source": "google_tim",
                        "emissions_model_version": ",".join(dict.fromkeys(versions)) or None,
                        "emissions_retrieved_at": now,
                    }
                )
            enriched.append(offer)
        return enriched
