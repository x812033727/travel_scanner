import json
import re
from datetime import UTC, date, datetime, timedelta
from typing import Any, cast

import httpx
from redis.asyncio import Redis

from app.config import Settings, get_settings


def _ident(value: object) -> str:
    return str(value or "").replace(" ", "").upper()


def _iata(value: object) -> str:
    if isinstance(value, dict):
        return str(value.get("code_iata") or value.get("code") or "").upper()
    return str(value or "").upper()


def _local_date(value: object) -> date | None:
    if not isinstance(value, str) or len(value) < 10:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


class FlightAwareProvider:
    name = "flightaware"

    def __init__(
        self,
        redis: Redis,
        settings: Settings | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.redis = redis
        self.settings = settings or get_settings()
        self.client = client

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        key = self.settings.flightaware_api_key
        if not key:
            raise ConnectionError("FlightAware API key is not configured")
        try:
            if self.client is not None:
                response = await self.client.get(
                    f"{self.settings.flightaware_base_url}{path}",
                    params=params,
                    headers={"x-apikey": key, "Accept": "application/json"},
                )
            else:
                async with httpx.AsyncClient(
                    timeout=self.settings.provider_timeout_seconds
                ) as client:
                    response = await client.get(
                        f"{self.settings.flightaware_base_url}{path}",
                        params=params,
                        headers={"x-apikey": key, "Accept": "application/json"},
                    )
        except httpx.HTTPError as exc:
            raise ConnectionError(f"FlightAware request failed: {exc}") from exc
        if response.status_code == 429:
            raise ConnectionError("FlightAware rate_limited (429)")
        if response.status_code >= 400:
            raise ConnectionError(f"FlightAware request failed ({response.status_code})")
        return cast(dict[str, Any], response.json())

    @staticmethod
    def _matches(
        row: dict[str, Any],
        departure_date: date,
        *,
        ident: str | None = None,
        origin: str | None = None,
        destination: str | None = None,
    ) -> bool:
        row_ident = _ident(row.get("ident_iata") or row.get("ident_icao") or row.get("ident"))
        row_origin = _iata(row.get("origin"))
        row_destination = _iata(row.get("destination"))
        row_date = _local_date(
            row.get("scheduled_out")
            or row.get("scheduled_off")
            or row.get("estimated_out")
            or row.get("filed_departure_time")
        )
        if row_date != departure_date:
            return False
        if ident and row_ident != _ident(ident):
            return False
        if origin and row_origin != origin.upper():
            return False
        return not destination or row_destination == destination.upper()

    @staticmethod
    def _normalize(row: dict[str, Any], *, schedule_only: bool) -> dict[str, Any]:
        return {
            "provider": "flightaware",
            "fa_flight_id": row.get("fa_flight_id"),
            "ident": row.get("ident_iata") or row.get("ident_icao") or row.get("ident"),
            "origin": _iata(row.get("origin")),
            "destination": _iata(row.get("destination")),
            "status": "schedule_verified" if schedule_only else str(row.get("status") or "unknown"),
            "schedule_only": schedule_only,
            "cancelled": bool(row.get("cancelled")),
            "diverted": bool(row.get("diverted")),
            "departure_delay_seconds": row.get("departure_delay"),
            "arrival_delay_seconds": row.get("arrival_delay"),
            "departure_terminal": cast(dict[str, Any], row.get("origin", {})).get("terminal"),
            "departure_gate": cast(dict[str, Any], row.get("origin", {})).get("gate"),
            "arrival_terminal": cast(dict[str, Any], row.get("destination", {})).get("terminal"),
            "arrival_gate": cast(dict[str, Any], row.get("destination", {})).get("gate"),
            "scheduled_out": row.get("scheduled_out"),
            "estimated_out": row.get("estimated_out"),
            "actual_out": row.get("actual_out"),
            "scheduled_off": row.get("scheduled_off"),
            "estimated_off": row.get("estimated_off"),
            "actual_off": row.get("actual_off"),
            "scheduled_on": row.get("scheduled_on"),
            "estimated_on": row.get("estimated_on"),
            "actual_on": row.get("actual_on"),
            "scheduled_in": row.get("scheduled_in"),
            "estimated_in": row.get("estimated_in"),
            "actual_in": row.get("actual_in"),
            "updated_at": datetime.now(UTC).isoformat(),
            "attribution": "FlightAware",
        }

    async def lookup(
        self,
        departure_date: date,
        *,
        ident: str | None = None,
        origin: str | None = None,
        destination: str | None = None,
    ) -> tuple[list[dict[str, Any]], bool]:
        cache_key = (
            "provider:flightaware:lookup:"
            f"{_ident(ident)}:{(origin or '').upper()}:"
            f"{(destination or '').upper()}:{departure_date}"
        )
        cached = await self.redis.get(cache_key)
        if cached:
            value = json.loads(cached.decode() if isinstance(cached, bytes) else str(cached))
            return cast(list[dict[str, Any]], value), True
        near_departure = departure_date <= datetime.now(UTC).date() + timedelta(days=2)
        if near_departure and ident:
            payload = await self._get(
                f"/flights/{_ident(ident)}",
                {
                    "start": departure_date.isoformat(),
                    "end": (departure_date + timedelta(days=1)).isoformat(),
                },
            )
            rows = payload.get("flights", [])
            schedule_only = False
        else:
            schedule_end = (departure_date + timedelta(days=1)).isoformat()
            parsed_ident = re.fullmatch(r"([A-Z0-9]{2,3})(\d{1,4}[A-Z]?)", _ident(ident))
            payload = await self._get(
                f"/schedules/{departure_date.isoformat()}/{schedule_end}",
                {
                    **({"origin": origin.upper()} if origin else {}),
                    **({"destination": destination.upper()} if destination else {}),
                    **({"airline": parsed_ident.group(1)} if parsed_ident else {}),
                    **({"flight_number": parsed_ident.group(2)} if parsed_ident else {}),
                },
            )
            rows = payload.get("scheduled", payload.get("flights", []))
            schedule_only = True
        matches = [
            self._normalize(row, schedule_only=schedule_only)
            for row in rows
            if isinstance(row, dict)
            and self._matches(
                row,
                departure_date,
                ident=ident,
                origin=origin,
                destination=destination,
            )
        ]
        await self.redis.set(
            cache_key,
            json.dumps(matches, default=str),
            ex=self.settings.flightaware_cache_ttl_seconds,
        )
        return matches, False

    async def track(self, fa_flight_id: str) -> tuple[dict[str, Any], bool]:
        cache_key = f"provider:flightaware:track:{fa_flight_id}"
        cached = await self.redis.get(cache_key)
        if cached:
            return json.loads(cached.decode() if isinstance(cached, bytes) else str(cached)), True
        payload = await self._get(f"/flights/{fa_flight_id}/track")
        result = {
            "fa_flight_id": fa_flight_id,
            "positions": payload.get("positions", []),
            "links": payload.get("links", {}),
            "retrieved_at": datetime.now(UTC).isoformat(),
            "attribution": "FlightAware",
        }
        await self.redis.set(
            cache_key,
            json.dumps(result, default=str),
            ex=self.settings.flightaware_track_cache_ttl_seconds,
        )
        return result, False
