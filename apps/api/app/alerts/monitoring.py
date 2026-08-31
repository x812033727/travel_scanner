from __future__ import annotations

from typing import Any, Literal

ResourceType = Literal["flight", "hotel", "trip"]
AUTOMATIC_FLIGHT_PROVIDERS = frozenset({"amadeus", "duffel", "mock"})
AUTOMATIC_HOTEL_PROVIDERS = frozenset({"amadeus", "booking", "mock"})


def automatic_monitoring_supported(resource_type: ResourceType, provider: str | None) -> bool:
    if resource_type == "flight":
        return provider in AUTOMATIC_FLIGHT_PROVIDERS
    if resource_type == "hotel":
        return provider in AUTOMATIC_HOTEL_PROVIDERS
    return False


def monitor_identity(resource_type: ResourceType, data: dict[str, Any]) -> dict[str, Any]:
    if resource_type == "flight":
        return {
            "itinerary_key": data.get("itinerary_key"),
            "segments": [
                {
                    "origin": item.get("origin"),
                    "destination": item.get("destination"),
                    "departure_time": item.get("departure_time"),
                    "flight_number": item.get("flight_number"),
                }
                for item in data.get("segments", [])
                if isinstance(item, dict)
            ],
            "cabin_class": data.get("cabin_class"),
        }
    if resource_type == "hotel":
        return {
            "hotel_id": data.get("hotel_id"),
            "check_in": data.get("check_in"),
            "check_out": data.get("check_out"),
            "refundable": bool(data.get("refundable")),
            "breakfast_included": bool(data.get("breakfast_included")),
        }
    return {}
