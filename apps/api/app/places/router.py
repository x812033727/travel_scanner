from typing import Any

import httpx
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from app.auth.service import CurrentUser
from app.config import get_settings
from app.destinations.catalog import DESTINATIONS
from app.problems import AppError

router = APIRouter(prefix="/destinations", tags=["destinations"])
public_router = APIRouter(prefix="/places", tags=["places"])


@public_router.get("/photo")
async def place_photo(name: str) -> RedirectResponse:
    settings = get_settings()
    if not settings.google_maps_api_key or not name.startswith("places/"):
        raise AppError(404, "photo_not_found", "Place photo is unavailable")
    url = f"https://places.googleapis.com/v1/{name}/media"
    async with httpx.AsyncClient(timeout=settings.provider_timeout_seconds) as client:
        response = await client.get(
            url,
            params={
                "maxWidthPx": 960,
                "skipHttpRedirect": "true",
                "key": settings.google_maps_api_key,
            },
        )
    if response.status_code >= 400:
        raise AppError(404, "photo_not_found", "Place photo is unavailable")
    photo_uri = response.json().get("photoUri")
    if not photo_uri:
        raise AppError(404, "photo_not_found", "Place photo is unavailable")
    return RedirectResponse(str(photo_uri), status_code=302)


class DiscoveryRequest(BaseModel):
    origin: str = Field(min_length=3, max_length=3)
    destination_region: str = "Japan"
    month: str | None = None
    budget_twd: int | None = None
    top_n: int = Field(default=3, ge=1, le=10)


@router.post("/discover")
async def discover(payload: DiscoveryRequest, user: CurrentUser) -> dict[str, Any]:
    _ = user
    region_aliases = {
        "japan": "Japan",
        "日本": "Japan",
        "south korea": "South Korea",
        "korea": "South Korea",
        "韓國": "South Korea",
        "南韓": "South Korea",
        "thailand": "Thailand",
        "泰國": "Thailand",
    }
    region = region_aliases.get(payload.destination_region.casefold())
    if region is None:
        raise AppError(422, "unsupported_region", "目前目的地探索支援日本、韓國與泰國")
    profiles = [item for item in DESTINATIONS if item.country == region]
    candidates = [
        {
            "city": item.city,
            "airport": item.code,
            "country": item.country_label,
            "timezone": item.timezone,
            "local_currency": item.currency,
            "areas": item.areas,
            "estimated_flight_twd": item.estimated_flight_twd,
            "within_budget_estimate": (
                payload.budget_twd is None or item.estimated_flight_twd <= payload.budget_twd * 0.45
            ),
            "reason": item.reason,
        }
        for item in sorted(profiles, key=lambda item: item.estimated_flight_twd)
    ]
    return {
        "origin": payload.origin.upper(),
        "region": region,
        "source": "curated_estimate",
        "candidates": candidates[: payload.top_n],
        "next_step": "選定城市後再執行即時機票、住宿、活動與接送搜尋",
    }
