from __future__ import annotations

from typing import Any, cast

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.places.google import GoogleTravelService


async def preview_google_place_match(
    session: AsyncSession,
    redis: Redis,
    *,
    query: str,
    country_code: str,
    latitude: float | None = None,
    longitude: float | None = None,
) -> dict[str, Any]:
    """Return a transient candidate without turning Places coordinates into catalog data."""

    settings = await load_runtime_settings(session)
    service = GoogleTravelService(redis, settings, locale="zh-TW")
    if not service.configured:
        return {
            "configured": False,
            "candidates": [],
            "reason": "google_places_not_configured",
            "message": "Google Places 金鑰未設定，請手動輸入已驗證的 Place ID 與永久座標來源。",
        }
    place = await service.search_place(
        query,
        latitude,
        longitude,
        detailed=False,
        region_code=country_code,
    )
    if not place:
        return {"configured": True, "candidates": [], "reason": "no_unique_candidate"}
    display = cast(dict[str, Any], place.get("displayName") or {})
    location = cast(dict[str, Any], place.get("location") or {})
    return {
        "configured": True,
        "candidates": [
            {
                "place_id": place.get("id"),
                "name": display.get("text"),
                "address": place.get("formattedAddress"),
                "google_maps_url": place.get("googleMapsUri"),
                "temporary_match_coordinates": {
                    "latitude": location.get("latitude"),
                    "longitude": location.get("longitude"),
                    "expires_in_days": 30,
                    "usage": "comparison_only",
                },
                "suggested_status": "unverified",
            }
        ],
        "reason": "manual_confirmation_required",
    }
