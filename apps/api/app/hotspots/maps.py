from __future__ import annotations

from decimal import Decimal
from urllib.parse import urlencode


def is_exact_naver_map_url(url: str | None) -> bool:
    return bool(
        url
        and (
            url.startswith("https://map.naver.com/p/entry/place/")
            or url.startswith("https://map.naver.com/v5/entry/place/")
        )
    )


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
) -> list[dict[str, str | bool]]:
    """Build only reviewed provider links that identify one exact POI."""

    _ = latitude, longitude
    if map_match_status != "verified":
        return []
    if country_code.upper() == "KR":
        if not is_exact_naver_map_url(naver_map_url):
            return []
        return [
            {
                "provider": "naver",
                "label": "Naver Map",
                "url": str(naver_map_url),
                "primary": True,
            }
        ]
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
