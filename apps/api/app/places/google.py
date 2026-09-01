import asyncio
import hashlib
import json
from datetime import timedelta
from typing import Any, cast
from urllib.parse import quote

import httpx
from redis.asyncio import Redis

from app.config import Settings, get_settings
from app.i18n import Locale, normalize_locale
from app.providers.schemas import ActivityOffer, HotelOffer
from app.providers.usage_meter import record_google_maps_request
from app.trips.itinerary import ItineraryDay

# Places API (New) bills a request at the highest SKU tier its field mask touches.
# places.rating, places.userRatingCount and places.regularOpeningHours are Enterprise
# fields (1,000 free calls/month); everything below them is Pro (5,000 free/month).
# Callers that only need to place a pin ask for LOCATE_FIELD_MASK and stay on Pro.
LOCATE_FIELD_MASK = (
    "places.id,places.displayName,places.formattedAddress,places.location,places.googleMapsUri"
)
DETAIL_FIELD_MASK = (
    "places.id,places.formattedAddress,places.location,places.rating,"
    "places.userRatingCount,places.photos,places.attributions,"
    "places.regularOpeningHours,places.displayName,places.googleMapsUri"
)


class GoogleTravelService:
    text_search_url = "https://places.googleapis.com/v1/places:searchText"
    autocomplete_url = "https://places.googleapis.com/v1/places:autocomplete"
    place_details_url = "https://places.googleapis.com/v1/places"
    routes_url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    def __init__(
        self,
        redis: Redis,
        settings: Settings | None = None,
        client: httpx.AsyncClient | None = None,
        locale: Locale | str = "zh-TW",
    ) -> None:
        self.redis = redis
        self.settings = settings or get_settings()
        self.client = client
        self.locale = normalize_locale(locale)

    @property
    def configured(self) -> bool:
        return bool(self.settings.google_maps_api_key)

    async def _post(
        self,
        url: str,
        *,
        json_data: dict[str, Any],
        field_mask: str,
        operation: str,
    ) -> dict[str, Any]:
        if not self.settings.google_maps_api_key:
            return {}
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.settings.google_maps_api_key,
            "X-Goog-FieldMask": field_mask,
        }
        try:
            if self.client is not None:
                response = await self.client.post(url, json=json_data, headers=headers)
            else:
                async with httpx.AsyncClient(
                    timeout=self.settings.provider_timeout_seconds
                ) as client:
                    response = await client.post(url, json=json_data, headers=headers)
            response.raise_for_status()
            return cast(dict[str, Any], response.json())
        except httpx.HTTPError:
            return {}
        finally:
            await record_google_maps_request(self.redis, operation)

    async def _get(
        self,
        url: str,
        *,
        field_mask: str,
        operation: str,
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        if not self.settings.google_maps_api_key:
            return {}
        headers = {
            "X-Goog-Api-Key": self.settings.google_maps_api_key,
            "X-Goog-FieldMask": field_mask,
        }
        try:
            if self.client is not None:
                response = await self.client.get(url, headers=headers, params=params)
            else:
                async with httpx.AsyncClient(
                    timeout=self.settings.provider_timeout_seconds
                ) as client:
                    response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return cast(dict[str, Any], response.json())
        except httpx.HTTPError:
            return {}
        finally:
            await record_google_maps_request(self.redis, operation)

    async def autocomplete(
        self,
        query: str,
        session_token: str | None = None,
        country_codes: list[str] | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> list[dict[str, Any]]:
        if not self.configured or len(query.strip()) < 2:
            return []
        body: dict[str, Any] = {"input": query.strip(), "languageCode": self.locale}
        if session_token:
            body["sessionToken"] = session_token
        if country_codes:
            body["includedRegionCodes"] = [code.lower() for code in country_codes]
            if len(country_codes) == 1:
                body["regionCode"] = country_codes[0].lower()
        if latitude is not None and longitude is not None:
            location = {"latitude": latitude, "longitude": longitude}
            body["origin"] = location
            body["locationBias"] = {"circle": {"center": location, "radius": 50_000.0}}
        payload = await self._post(
            self.autocomplete_url,
            json_data=body,
            field_mask=(
                "suggestions.placePrediction.placeId,suggestions.placePrediction.text,"
                "suggestions.placePrediction.structuredFormat,"
                "suggestions.placePrediction.distanceMeters"
            ),
            operation="places_autocomplete",
        )
        results: list[dict[str, Any]] = []
        for suggestion in cast(list[dict[str, Any]], payload.get("suggestions", [])):
            prediction = cast(dict[str, Any], suggestion.get("placePrediction") or {})
            text = cast(dict[str, Any], prediction.get("text") or {})
            structured = cast(dict[str, Any], prediction.get("structuredFormat") or {})
            main_text = cast(dict[str, Any], structured.get("mainText") or {})
            secondary_text = cast(dict[str, Any], structured.get("secondaryText") or {})
            if prediction.get("placeId"):
                results.append(
                    {
                        "provider": "google_places",
                        "place_id": prediction["placeId"],
                        "name": main_text.get("text") or text.get("text") or query,
                        "address": secondary_text.get("text"),
                        "distance_meters": prediction.get("distanceMeters"),
                        "attribution": "Google Maps",
                    }
                )
        return results

    async def place_details(
        self, place_id: str, session_token: str | None = None
    ) -> dict[str, Any]:
        params: dict[str, str] = {"languageCode": self.locale}
        if session_token:
            params["sessionToken"] = session_token
        payload = await self._get(
            f"{self.place_details_url}/{quote(place_id, safe='')}",
            field_mask=(
                "id,displayName,formattedAddress,location,googleMapsUri,"
                "regularOpeningHours,entrances"
            ),
            operation="place_details",
            params=params,
        )
        if not payload:
            return {}
        display = cast(dict[str, Any], payload.get("displayName") or {})
        location = cast(dict[str, Any], payload.get("location") or {})
        regular = cast(dict[str, Any], payload.get("regularOpeningHours") or {})
        return {
            "provider": "google_places",
            "place_id": payload.get("id") or place_id,
            "name": display.get("text") or payload.get("formattedAddress") or place_id,
            "address": payload.get("formattedAddress"),
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "google_maps_url": payload.get("googleMapsUri"),
            "opening_hours": regular.get("weekdayDescriptions", []),
            "entrances": payload.get("entrances", []),
            "attribution": "Google Maps",
        }

    async def search_place(
        self,
        name: str,
        latitude: float | None,
        longitude: float | None,
        *,
        detailed: bool = True,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        """Text Search for a place.

        detailed=False drops the Enterprise-tier fields (rating, review count, opening
        hours, photos) so the call bills as Pro. Use it wherever the caller only needs
        coordinates and a display name.
        """
        if not self.configured:
            return {}
        variant = "detail" if detailed else "locate"
        raw_key = (
            f"{variant}:{self.locale}:{region_code or '-'}:{name}:{latitude}:{longitude}"
        ).encode()
        key = f"places:google:{hashlib.sha256(raw_key).hexdigest()}"
        cached = await self.redis.get(key)
        if cached:
            value = cached.decode() if isinstance(cached, bytes) else str(cached)
            return cast(dict[str, Any], json.loads(value))
        body: dict[str, Any] = {"textQuery": name, "languageCode": self.locale, "pageSize": 1}
        if region_code:
            body["regionCode"] = region_code.upper()
        if latitude is not None and longitude is not None and (latitude or longitude):
            body["locationBias"] = {
                "circle": {
                    "center": {"latitude": latitude, "longitude": longitude},
                    "radius": 5000,
                }
            }
        payload = await self._post(
            self.text_search_url,
            json_data=body,
            field_mask=DETAIL_FIELD_MASK if detailed else LOCATE_FIELD_MASK,
            operation="places_text_search" if detailed else "places_text_search_locate",
        )
        places = cast(list[dict[str, Any]], payload.get("places", []))
        result = places[0] if places else {}
        if result:
            await self.redis.set(
                key,
                json.dumps(result, ensure_ascii=False),
                ex=self.settings.reference_cache_ttl_seconds,
            )
        return result

    @staticmethod
    def _photos(place: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
        photos = cast(list[dict[str, Any]], place.get("photos", []))[:3]
        urls = [
            f"/api/travel/places/photo?name={quote(str(photo.get('name') or ''))}"
            for photo in photos
            if photo.get("name")
        ]
        attributions: list[str] = []
        attribution_urls: list[str] = []
        for photo in photos:
            for attribution in cast(list[dict[str, Any]], photo.get("authorAttributions", [])):
                label = str(attribution.get("displayName") or "Google Maps contributor")
                if label not in attributions:
                    attributions.append(label)
                    attribution_urls.append(str(attribution.get("uri") or ""))
        return urls, attributions, attribution_urls

    async def enrich_hotel(self, offer: HotelOffer) -> HotelOffer:
        place = await self.search_place(offer.hotel_name, offer.latitude, offer.longitude)
        if not place:
            return offer
        location = cast(dict[str, Any], place.get("location", {}))
        images, attributions, attribution_urls = self._photos(place)
        return offer.model_copy(
            update={
                "address": place.get("formattedAddress") or offer.address,
                "latitude": float(location.get("latitude") or offer.latitude),
                "longitude": float(location.get("longitude") or offer.longitude),
                "review_score": place.get("rating"),
                "review_count": place.get("userRatingCount"),
                "images": images or offer.images,
                "attributions": attributions or offer.attributions,
                "attribution_urls": attribution_urls or offer.attribution_urls,
            }
        )

    async def enrich_activity(self, offer: ActivityOffer) -> ActivityOffer:
        place = await self.search_place(offer.title, offer.latitude, offer.longitude)
        if not place:
            return offer
        location = cast(dict[str, Any], place.get("location", {}))
        regular = cast(dict[str, Any], place.get("regularOpeningHours", {}))
        images, attributions, attribution_urls = self._photos(place)
        return offer.model_copy(
            update={
                "address": place.get("formattedAddress") or offer.address,
                "latitude": float(location.get("latitude") or offer.latitude),
                "longitude": float(location.get("longitude") or offer.longitude),
                "rating": float(place.get("rating") or offer.rating),
                "opening_hours": regular.get("weekdayDescriptions", offer.opening_hours),
                "images": images or offer.images,
                "attributions": attributions or offer.attributions,
                "attribution_urls": attribution_urls or offer.attribution_urls,
            }
        )

    async def enrich_hotels(self, offers: list[HotelOffer]) -> list[HotelOffer]:
        enriched = await asyncio.gather(*(self.enrich_hotel(item) for item in offers[:6]))
        return [*enriched, *offers[6:]]

    async def enrich_activities(self, offers: list[ActivityOffer]) -> list[ActivityOffer]:
        enriched = await asyncio.gather(*(self.enrich_activity(item) for item in offers[:8]))
        return [*enriched, *offers[8:]]

    async def enrich_itinerary(self, itinerary: list[ItineraryDay]) -> list[ItineraryDay]:
        """Resolve suggested places, then replace generic travel buffers with Routes estimates."""
        for day in itinerary:
            for item in day.items:
                if item.item_type not in {"suggestion", "meal"}:
                    continue
                place = await self.search_place(
                    f"{item.title} {item.location_name or ''}", item.latitude, item.longitude
                )
                if not place:
                    item.data = {**item.data, "places_status": "unavailable"}
                    continue
                location = cast(dict[str, Any], place.get("location", {}))
                regular = cast(dict[str, Any], place.get("regularOpeningHours", {}))
                display = cast(dict[str, Any], place.get("displayName", {}))
                _, attributions, attribution_urls = self._photos(place)
                item.location_name = str(
                    display.get("text") or place.get("formattedAddress") or item.location_name
                )
                item.latitude = float(location.get("latitude") or 0) or item.latitude
                item.longitude = float(location.get("longitude") or 0) or item.longitude
                item.provider_place_id = str(place.get("id") or "") or None
                item.location_source = "google_places"
                item.is_estimated = False
                item.data = {
                    **item.data,
                    "places_status": "resolved",
                    "needs_place_confirmation": False,
                    "opening_hours": regular.get("weekdayDescriptions", []),
                    "google_maps_url": place.get("googleMapsUri"),
                    "attributions": attributions,
                    "attribution_urls": attribution_urls,
                }

            for index, item in enumerate(day.items):
                if item.item_type != "travel":
                    continue
                previous = next(
                    (
                        row
                        for row in reversed(day.items[:index])
                        if row.latitude is not None and row.longitude is not None
                    ),
                    None,
                )
                following = next(
                    (
                        row
                        for row in day.items[index + 1 :]
                        if row.latitude is not None and row.longitude is not None
                    ),
                    None,
                )
                if previous is None or following is None:
                    item.data = {**item.data, "routes_status": "unavailable"}
                    continue
                previous_latitude = previous.latitude
                previous_longitude = previous.longitude
                following_latitude = following.latitude
                following_longitude = following.longitude
                if (
                    previous_latitude is None
                    or previous_longitude is None
                    or following_latitude is None
                    or following_longitude is None
                ):
                    item.data = {**item.data, "routes_status": "unavailable"}
                    continue
                minutes = await self.route_minutes(
                    (previous_latitude, previous_longitude),
                    (following_latitude, following_longitude),
                )
                if minutes is None:
                    item.data = {**item.data, "routes_status": "unavailable"}
                    continue
                item.start_time = previous.end_time or item.start_time
                if item.start_time is not None:
                    item.end_time = item.start_time + timedelta(minutes=minutes)
                item.data = {
                    **item.data,
                    "source_mode": "estimate",
                    "routes_status": "resolved",
                    "provider": "google_routes",
                    "minutes": minutes,
                }
        return itinerary

    async def route_minutes(
        self,
        origin: tuple[float, float],
        destination: tuple[float, float],
    ) -> int | None:
        payload = await self._post(
            self.routes_url,
            json_data={
                "origin": {"location": {"latLng": {"latitude": origin[0], "longitude": origin[1]}}},
                "destination": {
                    "location": {
                        "latLng": {
                            "latitude": destination[0],
                            "longitude": destination[1],
                        }
                    }
                },
                "travelMode": "TRANSIT",
                "languageCode": self.locale,
            },
            field_mask="routes.duration",
            operation="routes",
        )
        routes = cast(list[dict[str, Any]], payload.get("routes", []))
        if not routes:
            return None
        raw = str(routes[0].get("duration") or "")
        if not raw.endswith("s"):
            return None
        try:
            return max(1, round(float(raw[:-1]) / 60))
        except ValueError:
            return None
