import hashlib
import re
from datetime import UTC, date, datetime, timedelta
from typing import Annotated, Any
from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, model_validator
from redis.exceptions import RedisError
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.ai.parser import MockAITripParser
from app.auth.service import CurrentUser
from app.db import get_session
from app.destinations.catalog import DESTINATIONS
from app.infra import client_ip, enforce_named_rate_limit, get_redis
from app.places.google import GoogleTravelService
from app.problems import AppError
from app.providers.usage_meter import record_google_maps_request
from app.search.schemas import PropertyType, Travelers, TripPace

router = APIRouter(prefix="/destinations", tags=["destinations"])
public_router = APIRouter(prefix="/places", tags=["places"])
Session = Annotated[AsyncSession, Depends(get_session)]
PHOTO_NAME_PATTERN = re.compile(r"^places/[A-Za-z0-9._~-]{1,255}/photos/[A-Za-z0-9._~-]{1,512}$")
GOOGLE_PLACES_USER_LIMIT = 120
GOOGLE_PLACES_USER_WINDOW_SECONDS = 600


def _safe_photo_uri(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    parsed = urlparse(value)
    try:
        port = parsed.port
    except ValueError:
        return None
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or port not in (None, 443)
    ):
        return None
    return value


@public_router.get("/autocomplete")
async def autocomplete_places(
    user: CurrentUser,
    session: Session,
    q: str,
    session_token: str | None = None,
    country_codes: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
) -> list[dict[str, Any]]:
    _ = user
    if len(q.strip()) < 2 or len(q) > 120:
        raise AppError(422, "invalid_place_query", "地點關鍵字須為 2 至 120 個字元")
    if session_token is not None and not 8 <= len(session_token) <= 36:
        raise AppError(422, "invalid_session_token", "地點搜尋工作階段代碼格式錯誤")
    if (latitude is None) != (longitude is None):
        raise AppError(422, "invalid_place_bias", "地點搜尋中心必須同時包含經緯度")
    if latitude is not None and not -90 <= latitude <= 90:
        raise AppError(422, "invalid_place_bias", "地點搜尋緯度格式錯誤")
    if longitude is not None and not -180 <= longitude <= 180:
        raise AppError(422, "invalid_place_bias", "地點搜尋經度格式錯誤")
    codes = [code.strip().lower() for code in (country_codes or "").split(",") if code.strip()]
    allowed_codes = {"jp", "kr", "th"}
    if len(codes) > 3 or any(code not in allowed_codes for code in codes):
        raise AppError(422, "invalid_place_regions", "地點搜尋目前支援日本、韓國與泰國")
    service = GoogleTravelService(get_redis(), await load_runtime_settings(session))
    if not service.configured:
        raise AppError(503, "google_maps_not_configured", "Google Maps 地點搜尋尚未啟用")
    await enforce_named_rate_limit(
        "google-places-user",
        str(user.id),
        limit=GOOGLE_PLACES_USER_LIMIT,
        window_seconds=GOOGLE_PLACES_USER_WINDOW_SECONDS,
    )
    return await service.autocomplete(q, session_token, codes, latitude, longitude)


@public_router.get("/{provider}/{place_id}")
async def get_place_details(
    provider: str,
    place_id: str,
    user: CurrentUser,
    session: Session,
    session_token: str | None = None,
) -> dict[str, Any]:
    _ = user
    if provider != "google_places":
        raise AppError(404, "place_provider_not_found", "不支援的地點來源")
    if session_token is not None and not 8 <= len(session_token) <= 36:
        raise AppError(422, "invalid_session_token", "地點搜尋工作階段代碼格式錯誤")
    service = GoogleTravelService(get_redis(), await load_runtime_settings(session))
    if not service.configured:
        raise AppError(503, "google_maps_not_configured", "Google Maps 地點搜尋尚未啟用")
    await enforce_named_rate_limit(
        "google-places-user",
        str(user.id),
        limit=GOOGLE_PLACES_USER_LIMIT,
        window_seconds=GOOGLE_PLACES_USER_WINDOW_SECONDS,
    )
    result = await service.place_details(place_id, session_token)
    if not result:
        raise AppError(404, "place_not_found", "找不到這個地點")
    return result


@public_router.get("/photo")
async def place_photo(name: str, request: Request, session: Session) -> RedirectResponse:
    settings = await load_runtime_settings(session)
    if not settings.google_maps_api_key or not PHOTO_NAME_PATTERN.fullmatch(name):
        raise AppError(404, "photo_not_found", "目前沒有可用的地點照片")
    redis = get_redis()
    cache_key = f"places:photo-uri:{hashlib.sha256(name.encode()).hexdigest()}"
    try:
        cached = _safe_photo_uri(await redis.get(cache_key))
    except RedisError:
        cached = None
    if cached:
        return RedirectResponse(cached, status_code=302)
    await enforce_named_rate_limit(
        "places-photo-ip",
        client_ip(request),
        limit=settings.place_photo_ip_limit,
        window_seconds=settings.place_photo_window_seconds,
    )
    url = f"https://places.googleapis.com/v1/{name}/media"
    try:
        async with httpx.AsyncClient(timeout=settings.provider_timeout_seconds) as client:
            response = await client.get(
                url,
                params={
                    "maxWidthPx": 960,
                    "skipHttpRedirect": "true",
                    "key": settings.google_maps_api_key,
                },
            )
    except httpx.HTTPError as exc:
        raise AppError(503, "photo_provider_unavailable", "地點照片服務暫時無法使用") from exc
    finally:
        await record_google_maps_request(redis, "places_photo")
    if response.status_code >= 400:
        raise AppError(404, "photo_not_found", "目前沒有可用的地點照片")
    try:
        photo_uri = _safe_photo_uri(response.json().get("photoUri"))
    except (TypeError, ValueError):
        photo_uri = None
    if not photo_uri:
        raise AppError(404, "photo_not_found", "目前沒有可用的地點照片")
    try:
        await redis.setex(cache_key, settings.place_photo_cache_ttl_seconds, photo_uri)
    except RedisError:
        pass
    return RedirectResponse(photo_uri, status_code=302)


class DiscoveryRequest(BaseModel):
    origin: str = Field(min_length=3, max_length=3)
    destination_region: str | None = "Japan"
    month: str | None = None
    budget_twd: int | None = None
    top_n: int = Field(default=3, ge=1, le=10)
    travel_window: "TravelWindow | None" = None
    trip_length_range: "TripLengthRange | None" = None
    destination_countries: list[str] = Field(default_factory=list, max_length=3)
    destination_codes: list[str] = Field(default_factory=list, max_length=13)
    travelers: Travelers = Field(default_factory=Travelers)
    lodging_preferences: "LodgingPreferences" = Field(default_factory=lambda: LodgingPreferences())
    interests: list[str] = Field(default_factory=list, max_length=10)
    pace: TripPace = TripPace.BALANCED
    notes: str | None = Field(default=None, max_length=1000)


class TravelWindow(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_window(self) -> "TravelWindow":
        if self.end_date <= self.start_date:
            raise ValueError("travel window end must be after start")
        if (self.end_date - self.start_date).days > 180:
            raise ValueError("travel window cannot exceed 180 days")
        return self


class TripLengthRange(BaseModel):
    min_days: int = Field(ge=2, le=21)
    max_days: int = Field(ge=2, le=21)

    @model_validator(mode="after")
    def validate_length(self) -> "TripLengthRange":
        if self.max_days < self.min_days:
            raise ValueError("maximum trip length cannot be shorter than minimum")
        return self


class LodgingPreferences(BaseModel):
    accepted_property_types: list[PropertyType] = Field(default_factory=list, max_length=5)
    nightly_price_min_twd: int | None = Field(default=None, ge=0)
    nightly_price_max_twd: int | None = Field(default=None, ge=1)
    min_star_rating: int | None = Field(default=None, ge=1, le=5)
    min_review_score: float | None = Field(default=None, ge=0, le=10)
    min_review_count: int | None = Field(default=None, ge=0)
    preferred_areas: list[str] = Field(default_factory=list, max_length=10)
    max_station_walk_minutes: int | None = Field(default=None, ge=0, le=120)
    breakfast_required: bool | None = None
    refundable_required: bool | None = None

    @model_validator(mode="after")
    def validate_price(self) -> "LodgingPreferences":
        if (
            self.nightly_price_min_twd is not None
            and self.nightly_price_max_twd is not None
            and self.nightly_price_min_twd > self.nightly_price_max_twd
        ):
            raise ValueError("minimum nightly price cannot exceed maximum")
        return self


DiscoveryRequest.model_rebuild()


_COUNTRIES = {
    "JP": "Japan",
    "KR": "South Korea",
    "TH": "Thailand",
}
_RECOMMENDED_DAYS = {
    "FUK": (3, 5),
    "PUS": (4, 5),
    "KIX": (5, 7),
    "CTS": (5, 7),
    "HKT": (5, 7),
    "KBV": (4, 6),
}


def _estimate(
    profile: Any, departure: date, days: int, payload: DiscoveryRequest
) -> dict[str, Any]:
    travelers = payload.travelers.adults + payload.travelers.children
    seasonal = 1.18 if departure.month in {1, 4, 7, 8, 12} else 1.0
    weekday = 0.94 if departure.weekday() in {1, 2, 3} else 1.04
    flight = round(profile.estimated_flight_twd * max(1, travelers) * seasonal * weekday)
    nightly = round((profile.estimated_flight_twd * 0.43 + 900) / 100) * 100
    lodging = nightly * max(1, days - 1) * payload.travelers.rooms
    daily = 1800 * days * max(1, travelers)
    total = flight + lodging + daily
    matched_interests = [item for item in payload.interests if item in profile.suggestions]
    score = 72 + min(18, len(matched_interests) * 6)
    if payload.budget_twd:
        score += (
            8 if total <= payload.budget_twd else max(-20, -((total - payload.budget_twd) // 3000))
        )
    prefs = payload.lodging_preferences
    relaxed: list[str] = []
    if prefs.nightly_price_min_twd is not None and nightly < prefs.nightly_price_min_twd:
        relaxed.append("住宿每晚最低價格")
        score -= 4
    if prefs.nightly_price_max_twd is not None and nightly > prefs.nightly_price_max_twd:
        relaxed.append("住宿每晚最高價格")
        score -= 10
    if PropertyType.VACATION_RENTAL in prefs.accepted_property_types:
        relaxed.append("公寓／民宿需在正式搜尋確認供應量")
    return {
        "departure_date": departure,
        "return_date": departure + timedelta(days=days),
        "trip_length_days": days,
        "estimated_flight_twd": flight,
        "estimated_lodging_twd": lodging,
        "estimated_total_twd": total,
        "score": max(0, min(100, int(score))),
        "matched_interests": matched_interests,
        "relaxed_preferences": relaxed,
    }


@router.post("/discover")
async def discover(payload: DiscoveryRequest) -> dict[str, Any]:
    if payload.notes:
        parsed = await MockAITripParser().parse(payload.notes)
        lodging = payload.lodging_preferences
        lodging = lodging.model_copy(
            update={
                "nightly_price_max_twd": (
                    lodging.nightly_price_max_twd or parsed.hotel_max_nightly_twd
                ),
                "min_star_rating": lodging.min_star_rating or parsed.hotel_min_rating,
                "max_station_walk_minutes": (
                    lodging.max_station_walk_minutes or parsed.max_station_walk_minutes
                ),
                "breakfast_required": (
                    lodging.breakfast_required
                    if lodging.breakfast_required is not None
                    else (True if parsed.breakfast_required else None)
                ),
                "refundable_required": (
                    lodging.refundable_required
                    if lodging.refundable_required is not None
                    else (True if parsed.refundable_required else None)
                ),
            }
        )
        payload = payload.model_copy(
            update={
                "interests": payload.interests or parsed.interests,
                "lodging_preferences": lodging,
                "budget_twd": payload.budget_twd or parsed.budget_twd,
                "pace": payload.pace if payload.pace != TripPace.BALANCED else parsed.pace,
            }
        )
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
    selected_countries = {
        _COUNTRIES[item.upper()]
        for item in payload.destination_countries
        if item.upper() in _COUNTRIES
    }
    if not selected_countries and payload.destination_region:
        region = region_aliases.get(payload.destination_region.casefold())
        if region is None:
            raise AppError(422, "unsupported_region", "目前目的地探索支援日本、韓國與泰國")
        selected_countries = {region}
    if not selected_countries:
        selected_countries = set(_COUNTRIES.values())
    selected_codes = {item.upper() for item in payload.destination_codes}
    profiles = [
        item
        for item in DESTINATIONS
        if item.country in selected_countries
        and (not selected_codes or item.code in selected_codes)
    ]
    if not profiles:
        raise AppError(422, "unsupported_destination", "選取的國家或城市目前沒有支援資料")

    if payload.travel_window or payload.trip_length_range or payload.destination_countries:
        today = datetime.now(UTC).date()
        window = payload.travel_window or TravelWindow(
            start_date=today + timedelta(days=30), end_date=today + timedelta(days=180)
        )
        recommendations: list[dict[str, Any]] = []
        for profile in profiles:
            recommended = _RECOMMENDED_DAYS.get(profile.code, (4, 6))
            lengths = payload.trip_length_range or TripLengthRange(
                min_days=recommended[0], max_days=recommended[1]
            )
            best: dict[str, Any] | None = None
            current = window.start_date
            while current + timedelta(days=lengths.min_days) <= window.end_date:
                for days in range(lengths.min_days, lengths.max_days + 1):
                    if current + timedelta(days=days) > window.end_date:
                        continue
                    estimate = _estimate(profile, current, days, payload)
                    if best is None or (estimate["score"], -estimate["estimated_total_twd"]) > (
                        best["score"],
                        -best["estimated_total_twd"],
                    ):
                        best = estimate
                current += timedelta(days=1)
            if best is None:
                continue
            recommendations.append(
                {
                    "candidate_id": (
                        f"{profile.code}:{best['departure_date']}:{best['trip_length_days']}"
                    ),
                    "city": profile.city,
                    "airport": profile.code,
                    "country": profile.country_label,
                    "country_code": next(
                        code for code, name in _COUNTRIES.items() if name == profile.country
                    ),
                    "timezone": profile.timezone,
                    "local_currency": profile.currency,
                    "areas": list(profile.areas),
                    "reason": profile.reason,
                    "source": "curated_estimate",
                    **best,
                }
            )
        recommendations.sort(
            key=lambda item: (-item["score"], item["estimated_total_twd"], item["airport"])
        )
        return {
            "origin": payload.origin.upper(),
            "source": "curated_estimate",
            "recommendations": recommendations[: payload.top_n],
            "assumptions": [
                "推薦階段使用估算資料，不是即時最低價",
                "選定方案後才會執行完整搜尋與扣點",
            ],
        }

    region = next(iter(selected_countries))
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
