from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast
from urllib.parse import quote

import httpx
from redis.asyncio import Redis

from app.config import Settings
from app.i18n import Locale, normalize_locale
from app.providers.usage_meter import record_google_maps_request, reserve_google_maps_request

DINING_PLACE_TYPES = (
    "restaurant",
    "cafe",
    "coffee_shop",
    "bakery",
    "dessert_shop",
    "ice_cream_shop",
    "food_court",
    "meal_delivery",
    "meal_takeaway",
    "bar",
    "pub",
    "night_club",
)

NEARBY_FIELD_MASK = (
    "places.id,places.displayName,places.formattedAddress,places.location,"
    "places.rating,places.userRatingCount,places.regularOpeningHours,"
    "places.currentOpeningHours,places.websiteUri,places.googleMapsUri,"
    "places.plusCode,places.primaryType,places.businessStatus"
)

DETAIL_FIELD_MASK = (
    "id,displayName,formattedAddress,location,rating,userRatingCount,"
    "regularOpeningHours,currentOpeningHours,websiteUri,googleMapsUri,"
    "plusCode,primaryType,businessStatus,movedPlaceId"
)


class RestaurantProviderError(RuntimeError):
    code = "restaurant_provider_error"


class RestaurantQuotaExceeded(RestaurantProviderError):
    code = "restaurant_google_budget_exhausted"


class RestaurantProviderNotConfigured(RestaurantProviderError):
    code = "restaurant_google_not_configured"


@dataclass(frozen=True)
class RestaurantAggregateResult:
    count: int
    place_ids: tuple[str, ...]


@dataclass(frozen=True)
class RestaurantSnapshot:
    place_id: str
    name: str
    address: str | None
    latitude: float | None
    longitude: float | None
    rating: float | None
    review_count: int | None
    opening_hours: tuple[str, ...]
    open_now: bool | None
    official_website_url: str | None
    google_maps_url: str | None
    plus_code: str | None
    primary_type: str | None
    business_status: str | None

    @property
    def qualified(self) -> bool:
        return (
            self.rating is not None
            and self.rating >= 3.8
            and self.review_count is not None
            and self.review_count >= 1_000
            and self.business_status != "CLOSED_PERMANENTLY"
        )


@dataclass(frozen=True)
class RestaurantIdentityResult:
    status: str
    place_id: str | None
    moved_place_id: str | None = None


def _snapshot(payload: dict[str, Any]) -> RestaurantSnapshot | None:
    place_id = str(payload.get("id") or "").strip()
    if not place_id:
        return None
    display_name = cast(dict[str, Any], payload.get("displayName") or {})
    location = cast(dict[str, Any], payload.get("location") or {})
    regular = cast(dict[str, Any], payload.get("regularOpeningHours") or {})
    current = cast(dict[str, Any], payload.get("currentOpeningHours") or {})
    plus_code = cast(dict[str, Any], payload.get("plusCode") or {})
    rating = payload.get("rating")
    review_count = payload.get("userRatingCount")
    return RestaurantSnapshot(
        place_id=place_id,
        name=str(display_name.get("text") or payload.get("formattedAddress") or place_id),
        address=str(payload["formattedAddress"]) if payload.get("formattedAddress") else None,
        latitude=float(location["latitude"]) if location.get("latitude") is not None else None,
        longitude=float(location["longitude"]) if location.get("longitude") is not None else None,
        rating=float(rating) if rating is not None else None,
        review_count=int(review_count) if review_count is not None else None,
        opening_hours=tuple(str(item) for item in regular.get("weekdayDescriptions", [])),
        open_now=bool(current["openNow"]) if current.get("openNow") is not None else None,
        official_website_url=str(payload["websiteUri"]) if payload.get("websiteUri") else None,
        google_maps_url=str(payload["googleMapsUri"]) if payload.get("googleMapsUri") else None,
        plus_code=str(plus_code.get("compoundCode") or plus_code.get("globalCode") or "") or None,
        primary_type=str(payload["primaryType"]) if payload.get("primaryType") else None,
        business_status=str(payload["businessStatus"]) if payload.get("businessStatus") else None,
    )


class GoogleRestaurantProvider:
    nearby_url = "https://places.googleapis.com/v1/places:searchNearby"
    text_search_url = "https://places.googleapis.com/v1/places:searchText"
    details_url = "https://places.googleapis.com/v1/places"
    aggregate_url = "https://areainsights.googleapis.com/v1:computeInsights"

    def __init__(
        self,
        redis: Redis,
        settings: Settings,
        *,
        locale: Locale | str = "zh-TW",
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.redis = redis
        self.settings = settings
        self.locale = normalize_locale(locale)
        self.client = client

    def _headers(self, field_mask: str | None = None) -> dict[str, str]:
        if not self.settings.google_maps_api_key:
            raise RestaurantProviderNotConfigured("Google restaurant discovery is not configured")
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.settings.google_maps_api_key,
        }
        if field_mask:
            headers["X-Goog-FieldMask"] = field_mask
        return headers

    async def _post(
        self,
        url: str,
        body: dict[str, Any],
        *,
        operation: str,
        budget: int,
        field_mask: str | None = None,
    ) -> dict[str, Any]:
        headers = self._headers(field_mask)
        if not await reserve_google_maps_request(self.redis, operation, budget):
            raise RestaurantQuotaExceeded(operation)
        try:
            if self.client is not None:
                response = await self.client.post(url, json=body, headers=headers)
            else:
                async with httpx.AsyncClient(
                    timeout=self.settings.provider_timeout_seconds
                ) as client:
                    response = await client.post(url, json=body, headers=headers)
            response.raise_for_status()
            return cast(dict[str, Any], response.json())
        except httpx.HTTPError as exc:
            raise RestaurantProviderError(f"{operation} failed") from exc

    async def nearby(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int,
        *,
        limit: int = 20,
    ) -> list[RestaurantSnapshot]:
        payload = await self._post(
            self.nearby_url,
            {
                "includedTypes": list(DINING_PLACE_TYPES),
                "maxResultCount": min(20, max(1, limit)),
                "rankPreference": "POPULARITY",
                "languageCode": self.locale,
                "locationRestriction": {
                    "circle": {
                        "center": {"latitude": latitude, "longitude": longitude},
                        "radius": float(radius_meters),
                    }
                },
            },
            operation="places_nearby_restaurants",
            budget=min(
                self.settings.restaurant_nearby_monthly_budget,
                self.settings.google_maps_enterprise_free_limit,
            ),
            field_mask=NEARBY_FIELD_MASK,
        )
        return [
            snapshot
            for item in cast(list[dict[str, Any]], payload.get("places", []))
            if (snapshot := _snapshot(item)) is not None
        ]

    async def details(self, place_id: str) -> RestaurantSnapshot | None:
        headers = self._headers(DETAIL_FIELD_MASK)
        if not await reserve_google_maps_request(
            self.redis,
            "place_details_restaurant",
            min(
                self.settings.restaurant_details_monthly_budget,
                self.settings.google_maps_enterprise_free_limit,
            ),
            shared_operations=("place_details", "place_details_restaurant"),
            shared_monthly_budget=min(
                self.settings.restaurant_details_monthly_budget,
                self.settings.google_maps_enterprise_free_limit,
            ),
        ):
            raise RestaurantQuotaExceeded("place_details_restaurant")
        try:
            url = f"{self.details_url}/{quote(place_id, safe='')}"
            params = {"languageCode": self.locale}
            if self.client is not None:
                response = await self.client.get(url, params=params, headers=headers)
            else:
                async with httpx.AsyncClient(
                    timeout=self.settings.provider_timeout_seconds
                ) as client:
                    response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return _snapshot(cast(dict[str, Any], response.json()))
        except httpx.HTTPError as exc:
            raise RestaurantProviderError("place_details_restaurant failed") from exc

    async def aggregate(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int,
    ) -> RestaurantAggregateResult:
        if not self.settings.restaurant_scan_enabled:
            raise RestaurantProviderNotConfigured("Google restaurant automation is paused")
        payload = await self._post(
            self.aggregate_url,
            {
                "insights": ["INSIGHT_COUNT", "INSIGHT_PLACES"],
                "filter": {
                    "locationFilter": {
                        "circle": {
                            "latLng": {"latitude": latitude, "longitude": longitude},
                            "radius": radius_meters,
                        }
                    },
                    "typeFilter": {"includedTypes": list(DINING_PLACE_TYPES)},
                    "operatingStatus": ["OPERATING_STATUS_OPERATIONAL"],
                    "ratingFilter": {"minRating": 3.8, "maxRating": 5.0},
                },
            },
            operation="places_aggregate_restaurants",
            budget=min(
                self.settings.restaurant_aggregate_monthly_budget,
                self.settings.google_maps_pro_free_limit,
            ),
        )
        place_ids = tuple(
            value.removeprefix("places/")
            for item in cast(list[dict[str, Any]], payload.get("placeInsights", []))
            if (value := str(item.get("place") or ""))
        )
        return RestaurantAggregateResult(count=int(payload.get("count") or 0), place_ids=place_ids)

    async def search_ids_only(
        self,
        query: str,
        *,
        latitude: float | None = None,
        longitude: float | None = None,
        limit: int = 5,
    ) -> tuple[str, ...]:
        """Resolve text to Place IDs without requesting provider display fields."""

        body: dict[str, Any] = {
            "textQuery": query,
            "languageCode": self.locale,
            "pageSize": min(10, max(1, limit)),
        }
        if latitude is not None and longitude is not None:
            body["locationBias"] = {
                "circle": {
                    "center": {"latitude": latitude, "longitude": longitude},
                    "radius": 10_000.0,
                }
            }
        headers = self._headers("places.id")
        await record_google_maps_request(self.redis, "places_text_search_ids_only")
        try:
            if self.client is not None:
                response = await self.client.post(self.text_search_url, json=body, headers=headers)
            else:
                async with httpx.AsyncClient(
                    timeout=self.settings.provider_timeout_seconds
                ) as client:
                    response = await client.post(self.text_search_url, json=body, headers=headers)
            response.raise_for_status()
            payload = cast(dict[str, Any], response.json())
        except httpx.HTTPError as exc:
            raise RestaurantProviderError("places_text_search_ids_only failed") from exc
        return tuple(
            place_id
            for item in cast(list[dict[str, Any]], payload.get("places", []))
            if (place_id := str(item.get("id") or "").strip())
        )

    async def refresh_identity(self, place_id: str) -> RestaurantIdentityResult:
        """Check a durable Place ID with the IDs-only field mask."""

        headers = self._headers("id,movedPlaceId")
        await record_google_maps_request(self.redis, "place_id_refresh")
        try:
            url = f"{self.details_url}/{quote(place_id, safe='')}"
            if self.client is not None:
                response = await self.client.get(url, headers=headers)
            else:
                async with httpx.AsyncClient(
                    timeout=self.settings.provider_timeout_seconds
                ) as client:
                    response = await client.get(url, headers=headers)
            if response.status_code == 404:
                return RestaurantIdentityResult("not_found", None)
            response.raise_for_status()
            payload = cast(dict[str, Any], response.json())
        except httpx.HTTPError as exc:
            raise RestaurantProviderError("place_id_refresh failed") from exc
        refreshed = str(payload.get("id") or "").strip() or None
        moved = str(payload.get("movedPlaceId") or "").strip() or None
        return RestaurantIdentityResult(
            "moved" if moved else "active",
            refreshed,
            moved,
        )
