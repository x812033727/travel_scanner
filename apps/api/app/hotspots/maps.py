from __future__ import annotations

from decimal import Decimal
from typing import Any
from urllib.parse import urlencode

from app.locations.map_identity import verified_google_place_id

# Naver URLs that identify exactly one place; shared with the SQL publication filter.
EXACT_NAVER_PLACE_PREFIXES: tuple[str, ...] = (
    "https://map.naver.com/p/entry/place/",
    "https://map.naver.com/v5/entry/place/",
)


def is_exact_naver_map_url(url: str | None) -> bool:
    return bool(url and url.startswith(EXACT_NAVER_PLACE_PREFIXES))


def has_exact_map_identity(
    country_code: str,
    google_place_id: str | None,
    naver_map_url: str | None,
) -> bool:
    if country_code.upper() == "KR":
        return is_exact_naver_map_url(naver_map_url)
    return bool(google_place_id and google_place_id.strip())


def build_map_links(
    *,
    name: str,
    local_name: str | None,
    city_name: str,
    country_code: str,
    latitude: Decimal | float | None,
    longitude: Decimal | float | None,
    google_place_id: str | None = None,
    naver_map_url: str | None = None,
    map_match_status: str = "unverified",
    map_identities: dict[str, Any] | None = None,
) -> list[dict[str, str | bool]]:
    """Build only reviewed provider links that identify one exact POI."""

    _ = latitude, longitude
    if map_match_status != "verified":
        return []
    if country_code.upper() == "KR":
        if not is_exact_naver_map_url(naver_map_url):
            return []
        links: list[dict[str, str | bool]] = [
            {
                "provider": "naver",
                "label": "Naver Map",
                "url": str(naver_map_url),
                "primary": True,
            }
        ]
        if google_place_id and verified_google_place_id(map_identities, google_place_id):
            query = " ".join(item for item in (local_name or name, city_name) if item)
            params = {"api": "1", "query": query, "query_place_id": google_place_id}
            links.append({
                "provider": "google", "label": "Google Maps",
                "url": f"https://www.google.com/maps/search/?{urlencode(params)}",
                "primary": False,
            })
        return links
    if not google_place_id:
        return []

    google_query = " ".join(item for item in (local_name or name, city_name) if item).strip()
    google_params = {"api": "1", "query": google_query}
    google_params["query_place_id"] = google_place_id
    google_url = f"https://www.google.com/maps/search/?{urlencode(google_params)}"

    google: dict[str, str | bool] = {
        "provider": "google",
        "label": "Google Maps",
        "url": google_url,
        "primary": True,
    }
    return [google]
