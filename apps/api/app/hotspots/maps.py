from __future__ import annotations

from decimal import Decimal
from urllib.parse import quote, urlencode


def build_map_links(
    *,
    name: str,
    local_name: str | None,
    city_name: str,
    country_code: str,
    latitude: Decimal | float | None,
    longitude: Decimal | float | None,
    google_place_id: str | None = None,
) -> list[dict[str, str | bool]]:
    """Build keyless map search links without persisting provider results."""

    google_query = f"{name} {city_name}"
    if latitude is not None and longitude is not None:
        google_query = f"{float(latitude):.6f},{float(longitude):.6f}"
    google_params = {"api": "1", "query": google_query}
    if google_place_id:
        google_params["query_place_id"] = google_place_id
    google_url = f"https://www.google.com/maps/search/?{urlencode(google_params)}"

    google: dict[str, str | bool] = {
        "provider": "google",
        "label": "Google Maps",
        "url": google_url,
        "primary": country_code.upper() != "KR",
    }
    if country_code.upper() != "KR":
        return [google]

    naver_query = local_name or name
    naver: dict[str, str | bool] = {
        "provider": "naver",
        "label": "Naver Map",
        "url": f"https://map.naver.com/p/search/{quote(naver_query, safe='')}",
        "primary": True,
    }
    return [naver, google]
