from typing import Any

import httpx
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from app.auth.service import CurrentUser
from app.config import get_settings
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
    japan = [
        {
            "city": "福岡",
            "airport": "FUK",
            "estimated_flight_twd": 7_200,
            "reason": "短程、機場離市區近",
        },
        {
            "city": "大阪",
            "airport": "KIX",
            "estimated_flight_twd": 8_600,
            "reason": "美食與購物選擇密集",
        },
        {
            "city": "東京",
            "airport": "NRT",
            "estimated_flight_twd": 9_400,
            "reason": "航班與住宿選擇最多",
        },
        {
            "city": "札幌",
            "airport": "CTS",
            "estimated_flight_twd": 11_800,
            "reason": "自然景觀與季節體驗",
        },
    ]
    candidates = japan if payload.destination_region.lower() in {"japan", "日本"} else japan[:2]
    return {
        "origin": payload.origin.upper(),
        "source": "mock_historical_estimate",
        "candidates": candidates[: payload.top_n],
        "next_step": "Run live mock search only for these candidates",
    }
