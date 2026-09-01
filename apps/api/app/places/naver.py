from __future__ import annotations

import hashlib
import html
import json
import logging
import re
from typing import Any, cast
from urllib.parse import quote

import httpx
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import Settings, get_settings
from app.providers.usage_meter import record_naver_maps_request

logger = logging.getLogger(__name__)

TAG_PATTERN = re.compile(r"<[^>]+>")
LOCAL_SEARCH_URL = "https://naverapihub.apigw.ntruss.com/search/v1/local"
GEOCODE_URL = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"


def _clean_text(value: object) -> str:
    return " ".join(html.unescape(TAG_PATTERN.sub("", str(value or ""))).split())


def _coordinate(value: object, *, latitude: bool) -> float | None:
    try:
        number = float(str(value))
    except (TypeError, ValueError):
        return None
    limit = 90 if latitude else 180
    if abs(number) > limit:
        number /= 10_000_000
    if not -limit <= number <= limit:
        return None
    return number


def _in_korea(latitude: float, longitude: float) -> bool:
    return 32.0 <= latitude <= 39.8 and 124.0 <= longitude <= 132.0


class NaverPlaceService:
    """Korea-only place lookup backed by NAVER API HUB and NAVER geocoding."""

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
    def configured(self) -> bool:
        return self.settings.naver_maps_configured

    @property
    def headers(self) -> dict[str, str]:
        return {
            "X-NCP-APIGW-API-KEY-ID": self.settings.naver_maps_client_id or "",
            "X-NCP-APIGW-API-KEY": self.settings.naver_maps_client_secret or "",
            "Accept": "application/json",
        }

    async def _get(
        self,
        url: str,
        params: dict[str, str | int],
        operation: str,
    ) -> dict[str, Any]:
        if not self.configured:
            return {}
        try:
            if self.client is not None:
                response = await self.client.get(url, params=params, headers=self.headers)
            else:
                async with httpx.AsyncClient(
                    timeout=self.settings.provider_timeout_seconds
                ) as client:
                    response = await client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            payload = response.json()
            return cast(dict[str, Any], payload) if isinstance(payload, dict) else {}
        except httpx.HTTPStatusError as exc:
            logger.warning(
                "naver_places_http_error",
                extra={
                    "provider": "naver_maps",
                    "operation": operation,
                    "status_code": exc.response.status_code,
                    "reason_code": "rate_limited"
                    if exc.response.status_code == 429
                    else "provider_http_error",
                },
            )
            return {}
        except (httpx.HTTPError, ValueError):
            logger.warning(
                "naver_places_unavailable",
                extra={
                    "provider": "naver_maps",
                    "operation": operation,
                    "reason_code": "provider_unavailable",
                },
            )
            return {}
        finally:
            await record_naver_maps_request(self.redis, operation)

    @staticmethod
    def _place_id(name: str, address: str, latitude: float, longitude: float) -> str:
        raw = f"{name}|{address}|{latitude:.7f}|{longitude:.7f}".encode()
        return hashlib.sha256(raw).hexdigest()[:32]

    @staticmethod
    def _detail_key(place_id: str, session_token: str | None) -> str:
        session = hashlib.sha256((session_token or "anonymous").encode()).hexdigest()[:16]
        return f"places:naver:detail:{session}:{place_id}"

    async def _cache_place(
        self,
        result: dict[str, Any],
        session_token: str | None,
    ) -> None:
        try:
            await self.redis.set(
                self._detail_key(str(result["place_id"]), session_token),
                json.dumps(result, ensure_ascii=False),
                ex=self.settings.naver_place_cache_ttl_seconds,
            )
        except RedisError:
            return

    async def _local_results(
        self, query: str, session_token: str | None
    ) -> list[dict[str, Any]]:
        payload = await self._get(
            LOCAL_SEARCH_URL,
            {"query": query, "display": 5, "start": 1, "format": "json"},
            "local_search",
        )
        results: list[dict[str, Any]] = []
        for raw in cast(list[dict[str, Any]], payload.get("items") or []):
            latitude = _coordinate(raw.get("mapy"), latitude=True)
            longitude = _coordinate(raw.get("mapx"), latitude=False)
            name = _clean_text(raw.get("title"))
            address = _clean_text(raw.get("roadAddress") or raw.get("address"))
            if (
                not name
                or latitude is None
                or longitude is None
                or not _in_korea(latitude, longitude)
            ):
                continue
            place_id = self._place_id(name, address, latitude, longitude)
            result: dict[str, Any] = {
                "provider": "naver_local",
                "place_id": place_id,
                "name": name,
                "address": address or None,
                "latitude": latitude,
                "longitude": longitude,
                "distance_meters": None,
                "naver_maps_url": f"https://map.naver.com/p/search/{quote(name, safe='')}",
                "external_url": f"https://map.naver.com/p/search/{quote(name, safe='')}",
                "opening_hours": [],
                "attribution": "NAVER Maps",
            }
            await self._cache_place(result, session_token)
            results.append(result)
        return results

    async def _geocode_results(
        self, query: str, session_token: str | None
    ) -> list[dict[str, Any]]:
        payload = await self._get(
            GEOCODE_URL,
            {"query": query},
            "geocode",
        )
        results: list[dict[str, Any]] = []
        for raw in cast(list[dict[str, Any]], payload.get("addresses") or [])[:5]:
            latitude = _coordinate(raw.get("y"), latitude=True)
            longitude = _coordinate(raw.get("x"), latitude=False)
            address = _clean_text(raw.get("roadAddress") or raw.get("jibunAddress"))
            name = address or query
            if (
                latitude is None
                or longitude is None
                or not _in_korea(latitude, longitude)
            ):
                continue
            place_id = self._place_id(name, address, latitude, longitude)
            result: dict[str, Any] = {
                "provider": "naver_local",
                "place_id": place_id,
                "name": name,
                "address": address or None,
                "latitude": latitude,
                "longitude": longitude,
                "distance_meters": None,
                "naver_maps_url": f"https://map.naver.com/p/search/{quote(name, safe='')}",
                "external_url": f"https://map.naver.com/p/search/{quote(name, safe='')}",
                "opening_hours": [],
                "attribution": "NAVER Maps",
            }
            await self._cache_place(result, session_token)
            results.append(result)
        return results

    async def autocomplete(
        self, query: str, session_token: str | None = None
    ) -> list[dict[str, Any]]:
        if not self.configured or len(query.strip()) < 2:
            return []
        results = await self._local_results(query.strip(), session_token)
        return results or await self._geocode_results(query.strip(), session_token)

    async def place_details(
        self, place_id: str, session_token: str | None = None
    ) -> dict[str, Any]:
        try:
            cached = await self.redis.get(self._detail_key(place_id, session_token))
        except RedisError:
            return {}
        if not cached:
            return {}
        value = cached.decode() if isinstance(cached, bytes) else str(cached)
        try:
            return cast(dict[str, Any], json.loads(value))
        except json.JSONDecodeError:
            return {}

    async def search_place(self, query: str) -> dict[str, Any]:
        session_token = f"auto-{hashlib.sha256(query.encode()).hexdigest()[:24]}"
        results = await self.autocomplete(query, session_token)
        return results[0] if results else {}
