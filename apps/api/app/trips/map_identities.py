"""Trip-local identities: independent of canonical position and route duration."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlencode

from app.locations.map_identity import normalize_map_identities
from app.models import TripPlanItem
from app.trips.routing import RoutePoint, infer_place_provider

GOOGLE_ID = re.compile(r"^[A-Za-z0-9_-]{1,255}$")
NAVER_EXACT = re.compile(r"^https://map\.naver\.com/(?:p|v5)/entry/place/[0-9]+/?$")


def trip_map_identities(item: TripPlanItem) -> dict[str, dict[str, Any]]:
    data = item.data or {}
    raw = normalize_map_identities(data.get("map_identities"))
    result: dict[str, dict[str, Any]] = {}
    if isinstance(raw, dict):
        for provider in ("google_places", "naver_maps"):
            identity = raw.get(provider)
            if not isinstance(identity, dict) or identity.get("provider") != provider:
                continue
            place_id, url = identity.get("place_id"), identity.get("map_url")
            if provider == "google_places":
                if not isinstance(place_id, str) or not GOOGLE_ID.fullmatch(place_id):
                    continue
                url = f"https://www.google.com/maps/search/?api=1&query=place&query_place_id={place_id}"
            elif not isinstance(url, str) or not NAVER_EXACT.fullmatch(url):
                continue  # A NAVER Local hash/search URL is not an exact identity.
            result[provider] = {
                "provider": provider,
                "place_id": place_id,
                "map_url": url,
                "status": identity.get("status", "unverified"),
                "verified_at": identity.get("verified_at"),
            }
    # A genuinely legacy row can retain its hand-picked Google identity. New or
    # changed client rows explicitly receive an empty metadata key from the server,
    # which must not be upgraded by client-controlled compatibility fields.
    if (
        "map_identities" not in data
        and "google_places" not in result
        and item.location_source == "confirmed"
        and (
            infer_place_provider(item.location_source, data) == "google_places"
            and item.provider_place_id
            and GOOGLE_ID.fullmatch(item.provider_place_id)
        )
    ):
        place_id = item.provider_place_id
        result["google_places"] = {
            "provider": "google_places",
            "place_id": place_id,
            "map_url": f"https://www.google.com/maps/search/?api=1&query=place&query_place_id={place_id}",
            "status": "verified",
            "verified_at": None,
        }
    return result


def item_route_point(item: TripPlanItem) -> RoutePoint | None:
    if item.latitude is None or item.longitude is None:
        return None
    if not (-90 <= float(item.latitude) <= 90 and -180 <= float(item.longitude) <= 180):
        return None
    identities = trip_map_identities(item)
    google = identities.get("google_places", {})
    naver = identities.get("naver_maps", {})
    return RoutePoint(
        item_id=item.id,
        name=item.location_name or item.title or item.item_type,
        latitude=float(item.latitude),
        longitude=float(item.longitude),
        provider_place_id=item.provider_place_id,
        place_provider=infer_place_provider(item.location_source, item.data),
        google_place_id=google.get("place_id") if google.get("status") == "verified" else None,
        naver_map_url=naver.get("map_url") if naver.get("status") == "verified" else None,
    )


def location_map_links(item: TripPlanItem) -> list[dict[str, Any]]:
    """Safe exact links plus an explicitly labelled Google coordinate reference."""
    identities = trip_map_identities(item)
    links = [
        {
            "provider": "naver" if provider == "naver_maps" else "google",
            "url": identity["map_url"],
            "position_only": False,
        }
        for provider, identity in identities.items()
        if identity.get("status") == "verified" and identity.get("map_url")
    ]
    if not any(link["provider"] == "google" for link in links):
        # Coordinate links also describe unsaved draft items, which have no UUID
        # yet. A routable persisted RoutePoint is not required for this display.
        latitude = float(item.latitude) if item.latitude is not None else None
        longitude = float(item.longitude) if item.longitude is not None else None
        if (
            latitude is not None
            and longitude is not None
            and -90 <= latitude <= 90
            and -180 <= longitude <= 180
        ):
            query = urlencode({"api": 1, "query": f"{latitude:.7f},{longitude:.7f}"})
            links.append(
                {
                    "provider": "google",
                    "url": f"https://www.google.com/maps/search/?{query}",
                    "position_only": True,
                }
            )
    return links
