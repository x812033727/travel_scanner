from __future__ import annotations

import json
import re
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any, cast
from urllib.parse import urlparse
from uuid import NAMESPACE_URL, UUID, uuid5

import httpx
from redis.asyncio import Redis

from app.config import Settings, get_settings
from app.destinations.catalog import DestinationProfile, destination_for_code
from app.providers.schemas import ActionKind, HotelOffer, SourceMode
from app.search.schemas import PropertyType, SearchCreate, SearchModule

BOOKING_API_HOSTS = {"demandapi.booking.com", "demandapi-sandbox.booking.com"}


def stable_booking_offer_id(provider_id: str) -> UUID:
    return uuid5(NAMESPACE_URL, f"travel-scanner:booking:hotel:{provider_id}")


def _decimal(value: object, default: str = "0") -> Decimal:
    if isinstance(value, dict):
        for key in ("booker", "accommodation", "value", "amount"):
            if key in value:
                return _decimal(value[key], default)
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return Decimal(default)


def _float(value: object, default: float = 0) -> float:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return default


def _int(value: object, default: int = 0) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return default


def _localized(value: object, language: str, default: str = "") -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        lowered = language.lower()
        for key in (lowered, lowered.replace("-", "_"), "en-gb", "en", "name", "text"):
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate.strip():
                return candidate.strip()
        for candidate in value.values():
            if isinstance(candidate, str) and candidate.strip():
                return candidate.strip()
    return default


def _normalized_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def _safe_booking_url(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not (host == "booking.com" or host.endswith(".booking.com")):
        return None
    return value


def _safe_booking_image_url(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower()
    allowed = (
        host == "booking.com"
        or host.endswith(".booking.com")
        or host == "bstatic.com"
        or host.endswith(".bstatic.com")
    )
    return value if parsed.scheme == "https" and allowed else None


def _address_text(value: object, language: str) -> str | None:
    if isinstance(value, str):
        return value.strip() or None
    if not isinstance(value, dict):
        return None
    parts: list[str] = []
    for key in ("address_line", "street", "city", "postal_code", "postcode"):
        text = _localized(value.get(key), language)
        if text and text not in parts:
            parts.append(text)
    return " ".join(parts) or None


def _policy_text(value: object) -> str | None:
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, list):
        list_parts = [text for item in value if (text := _policy_text(item))]
        return "；".join(dict.fromkeys(list_parts)) or None
    if isinstance(value, dict):
        parts: list[str] = []
        for key in ("description", "type", "free_cancellation_until", "deadline"):
            if key in value and (text := _policy_text(value[key])):
                parts.append(text)
        return "；".join(dict.fromkeys(parts)) or None
    return None


def _property_type(value: object) -> PropertyType:
    raw = str(value or "").casefold()
    if "serviced" in raw or "aparthotel" in raw:
        return PropertyType.SERVICED_APARTMENT
    if "apartment" in raw or "vacation" in raw or "villa" in raw:
        return PropertyType.VACATION_RENTAL
    if "guest" in raw or "hostel" in raw or "homestay" in raw:
        return PropertyType.GUESTHOUSE
    return PropertyType.HOTEL if raw else PropertyType.UNKNOWN


def _english_city_query(profile: DestinationProfile) -> str:
    for alias in profile.aliases:
        if len(alias) > 3 and alias.isascii() and alias.replace(" ", "").isalpha():
            return alias
    return profile.code


class BookingHotelProvider:
    name = "booking"

    def __init__(
        self,
        redis: Redis,
        settings: Settings | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.redis = redis
        self.settings = settings or get_settings()
        self.client = client

    @property
    def source_mode(self) -> SourceMode:
        return (
            SourceMode.LIVE
            if self.settings.booking_demand_env.lower() == "production"
            else SourceMode.TEST
        )

    @property
    def base_url(self) -> str:
        value = self.settings.booking_demand_api_base_url.rstrip("/")
        parsed = urlparse(value)
        if parsed.scheme != "https" or (parsed.hostname or "").lower() not in BOOKING_API_HOSTS:
            raise ConnectionError("Booking Demand API Base URL 必須使用官方 HTTPS 網域")
        return value

    async def _send(self, path: str, payload: dict[str, Any]) -> httpx.Response:
        affiliate_id = self.settings.booking_demand_effective_affiliate_id
        token = self.settings.booking_demand_api_token
        if not self.settings.booking_demand_enabled or not affiliate_id or not token:
            raise ConnectionError("Booking Demand API 憑證尚未設定或未啟用")
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Affiliate-Id": affiliate_id,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
            if self.client is not None:
                return await self.client.post(
                    f"{self.base_url}{path}", json=payload, headers=headers
                )
            async with httpx.AsyncClient(timeout=self.settings.provider_timeout_seconds) as client:
                return await client.post(f"{self.base_url}{path}", json=payload, headers=headers)
        except httpx.HTTPError as exc:
            raise ConnectionError(f"Booking Demand API 連線失敗：{exc.__class__.__name__}") from exc

    async def _request(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = await self._send(path, payload)
        if response.status_code >= 400:
            raise ConnectionError(f"Booking Demand API {path} 失敗（HTTP {response.status_code}）")
        try:
            data = response.json()
        except ValueError as exc:
            raise ConnectionError("Booking Demand API 回傳無法解析的資料") from exc
        return cast(dict[str, Any], data) if isinstance(data, dict) else {}

    def _destination_profile(self, query: SearchCreate) -> DestinationProfile | None:
        destination = query.destination or (query.legs[0].destination if query.legs else None)
        return destination_for_code(destination)

    async def _city_id(self, query: SearchCreate) -> int | None:
        profile = self._destination_profile(query)
        if profile is None:
            return None
        destination = (query.destination or profile.code).upper()
        cache_key = (
            f"provider:booking:location:{self.settings.booking_demand_env.lower()}:"
            f"{self.settings.booking_language.lower()}:{destination}"
        )
        cached = await self.redis.get(cache_key)
        if cached is not None:
            raw = cached.decode() if isinstance(cached, bytes) else str(cached)
            return _int(raw) if raw and raw != "none" else None
        query_name = _english_city_query(profile)
        payload = await self._request(
            "/common/locations/cities",
            {
                "airport": destination,
                "languages": [self.settings.booking_language.lower(), "en-gb"],
                "rows": 10,
            },
        )
        aliases = {
            _normalized_name(alias)
            for alias in profile.aliases
            if len(alias) > 3 and alias.isascii()
        }
        aliases.add(_normalized_name(query_name))
        selected: int | None = None
        for row in cast(list[dict[str, Any]], payload.get("data", [])):
            name = _localized(row.get("name"), self.settings.booking_language)
            if _normalized_name(name) not in aliases:
                continue
            raw_id = row.get("id")
            if not isinstance(raw_id, int | str):
                continue
            try:
                selected = int(raw_id)
            except (TypeError, ValueError):
                continue
            break
        await self.redis.set(
            cache_key,
            str(selected) if selected is not None else "none",
            ex=(
                self.settings.booking_location_cache_ttl_seconds
                if selected is not None
                else min(self.settings.booking_location_cache_ttl_seconds, 3600)
            ),
        )
        return selected

    @staticmethod
    def _dates(query: SearchCreate) -> tuple[date, date]:
        check_in = query.departure_date or query.legs[0].departure_date
        check_out = query.return_date or check_in + timedelta(days=1)
        return check_in, check_out

    async def search_hotels(self, query: SearchCreate) -> list[HotelOffer]:
        city_id = await self._city_id(query)
        if city_id is None:
            return []
        check_in, check_out = self._dates(query)
        guests: dict[str, Any] = {
            "number_of_adults": query.travelers.adults,
            "number_of_rooms": query.travelers.rooms,
        }
        if query.travelers.children_ages:
            guests["children"] = query.travelers.children_ages
        search = await self._request(
            "/accommodations/search",
            {
                "booker": {
                    "country": self.settings.booking_booker_country.lower(),
                    "platform": "desktop",
                },
                "checkin": check_in.isoformat(),
                "checkout": check_out.isoformat(),
                "city": city_id,
                "currency": query.currency,
                "extras": ["extra_charges", "products"],
                "guests": guests,
            },
        )
        rows = cast(list[dict[str, Any]], search.get("data", []))[:30]
        accommodation_ids = [row.get("id") for row in rows if row.get("id") is not None]
        if not accommodation_ids:
            return []
        details_payload = await self._request(
            "/accommodations/details",
            {
                "accommodations": accommodation_ids,
                "extras": ["description", "facilities", "photos"],
                "languages": [self.settings.booking_language.lower()],
            },
        )
        details = {
            str(row.get("id")): row
            for row in cast(list[dict[str, Any]], details_payload.get("data", []))
        }
        now = datetime.now(UTC)
        nights = max(1, (check_out - check_in).days)
        offers: list[HotelOffer] = []
        for row in rows:
            hotel_id = str(row.get("id") or "")
            detail = details.get(hotel_id, {})
            products = cast(list[dict[str, Any]], row.get("products", []))
            product = products[0] if products else {}
            price = cast(dict[str, Any], product.get("price") or row.get("price") or {})
            total = _decimal(price.get("total") or price.get("book") or price.get("display"))
            if total <= 0:
                continue
            base = _decimal(price.get("base"), str(total))
            currency_value = row.get("currency") or price.get("currency") or query.currency
            if isinstance(currency_value, dict):
                currency_value = currency_value.get("booker") or currency_value.get("accommodation")
            booking_url = _safe_booking_url(row.get("deep_link_url")) or _safe_booking_url(
                row.get("url")
            )
            provider_offer_id = str(product.get("id") or f"{hotel_id}:{check_in}:{check_out}")
            coordinates = cast(
                dict[str, Any],
                detail.get("coordinates") or detail.get("location") or {},
            )
            policies = cast(dict[str, Any], product.get("policies") or {})
            cancellation = _policy_text(policies.get("cancellation"))
            cancellation_folded = (cancellation or "").casefold().replace("-", "_")
            meal_plan = json.dumps(policies.get("meal_plan") or {}, ensure_ascii=False).casefold()
            review = cast(dict[str, Any], detail.get("review_score") or {})
            rating_value = detail.get("rating")
            if isinstance(rating_value, dict):
                rating_value = rating_value.get("stars") or rating_value.get("score")
            photos = cast(list[Any], detail.get("photos") or [])
            images = [
                url
                for photo in photos
                if (
                    url := _safe_booking_image_url(
                        photo.get("url") if isinstance(photo, dict) else photo
                    )
                )
            ]
            facilities = cast(list[Any], detail.get("facilities") or [])
            amenities = [
                _localized(item, self.settings.booking_language, str(item))
                for item in facilities[:20]
            ]
            property_raw = detail.get("type") or detail.get("accommodation_type")
            room = product.get("room")
            room_type = _localized(room, self.settings.booking_language, "供應商房型")
            offers.append(
                HotelOffer(
                    id=stable_booking_offer_id(provider_offer_id),
                    provider=self.name,
                    provider_offer_id=provider_offer_id,
                    currency=str(currency_value or query.currency).upper(),
                    booking_url=booking_url,
                    retrieved_at=now,
                    expires_at=now + timedelta(minutes=10),
                    source_mode=self.source_mode,
                    is_mock=False,
                    is_bookable=booking_url is not None,
                    action_kind=ActionKind.DEEP_LINK if booking_url else ActionKind.RECHECK,
                    images=images,
                    attributions=["Booking.com"],
                    attribution_urls=["https://www.booking.com/"],
                    cancellation_policy=cancellation,
                    hotel_id=hotel_id,
                    hotel_name=_localized(
                        detail.get("name"),
                        self.settings.booking_language,
                        f"Booking.com #{hotel_id}",
                    ),
                    latitude=_float(coordinates.get("latitude")),
                    longitude=_float(coordinates.get("longitude")),
                    rating=_float(rating_value),
                    room_type=room_type[:240],
                    check_in=datetime.combine(check_in, time(15), tzinfo=UTC),
                    check_out=datetime.combine(check_out, time(11), tzinfo=UTC),
                    nights=nights,
                    base_price=base,
                    taxes=max(Decimal(0), total - base),
                    fees=Decimal(0),
                    total_price=total,
                    breakfast_included="breakfast" in meal_plan and "not_included" not in meal_plan,
                    refundable=bool(cancellation)
                    and "non_refundable" not in cancellation_folded,
                    station_walk_minutes=0,
                    nightly_price=(total / nights).quantize(Decimal("0.01")),
                    address=_address_text(detail.get("address"), self.settings.booking_language),
                    amenities=[item for item in amenities if item],
                    review_score=_float(
                        review.get("score") or detail.get("review_score_value")
                    )
                    or None,
                    review_count=_int(
                        review.get("number_of_reviews") or detail.get("number_of_reviews")
                    )
                    or None,
                    property_type=_property_type(property_raw),
                    max_guests=_int(product.get("number_of_adults")) or None,
                )
            )
        return offers

    async def probe(self) -> None:
        query = SearchCreate(
            origin="TPE",
            destination="NRT",
            departure_date=date.today() + timedelta(days=45),
            return_date=date.today() + timedelta(days=47),
            modules=[SearchModule.HOTEL],
        )
        if await self._city_id(query) is None:
            raise ConnectionError("Booking Demand API 已回應，但無法對應東京城市資料")

    async def get_hotel_details(self, hotel_id: str) -> dict[str, str]:
        payload = await self._request(
            "/accommodations/details",
            {
                "accommodations": [int(hotel_id)],
                "extras": ["description"],
                "languages": [self.settings.booking_language.lower()],
            },
        )
        rows = cast(list[dict[str, Any]], payload.get("data", []))
        if not rows:
            return {}
        row = rows[0]
        return {
            "id": str(row.get("id") or hotel_id),
            "name": _localized(row.get("name"), self.settings.booking_language),
            "description": _localized(row.get("description"), self.settings.booking_language),
        }
