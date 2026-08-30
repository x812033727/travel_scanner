import asyncio
import hashlib
import json
import time
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from typing import Any, cast
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser
from uuid import NAMESPACE_URL, uuid5

import httpx
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import Settings
from app.crawlers.schemas import (
    AirlineCode,
    AirlineCrawlerSource,
    AirlineFareSearch,
    AirlineFareSearchResponse,
    CabinClass,
    PublicFareQuote,
    SourceState,
)

CITY_SLUGS = {
    "TPE": "taipei",
    "TSA": "taipei",
    "TYO": "tokyo",
    "NRT": "tokyo",
    "HND": "tokyo",
    "OSA": "osaka",
    "KIX": "osaka",
    "FUK": "fukuoka",
    "CTS": "sapporo",
    "OKA": "okinawa",
    "SEL": "seoul",
    "ICN": "seoul",
    "BKK": "bangkok",
    "SIN": "singapore",
    "LAX": "los-angeles",
    "SFO": "san-francisco",
}

AIRPORT_GROUPS = {
    "TPE": {"TPE", "TSA"},
    "TYO": {"NRT", "HND"},
    "OSA": {"KIX", "ITM"},
    "SEL": {"ICN", "GMP"},
}


class CrawlerError(Exception):
    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(detail)


class CrawlerPolicyError(CrawlerError):
    pass


class _NextDataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._capturing = False
        self._parts: list[str] = []
        self.documents: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "script" and attributes.get("id") == "__NEXT_DATA__":
            self._capturing = True
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._capturing:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._capturing:
            self.documents.append("".join(self._parts))
            self._capturing = False
            self._parts = []


def _fare_lists(value: object) -> Iterator[list[dict[str, Any]]]:
    if isinstance(value, dict):
        mapping = cast(dict[str, object], value)
        for key, child in mapping.items():
            if key == "fares" and isinstance(child, list):
                rows = [cast(dict[str, Any], row) for row in child if isinstance(row, dict)]
                if rows:
                    yield rows
            yield from _fare_lists(child)
    elif isinstance(value, list):
        for child in cast(list[object], value):
            yield from _fare_lists(child)


def _parse_date(value: object) -> date | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _parse_cabin(value: object) -> CabinClass | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip().upper().replace("-", "_").replace(" ", "_")
    if "PREMIUM" in normalized and "ECONOMY" in normalized:
        return CabinClass.PREMIUM_ECONOMY
    if "BUSINESS" in normalized:
        return CabinClass.BUSINESS
    if "FIRST" in normalized:
        return CabinClass.FIRST
    if "ECONOMY" in normalized:
        return CabinClass.ECONOMY
    return None


def _airport_matches(requested: str, actual: str) -> bool:
    return actual in AIRPORT_GROUPS.get(requested, {requested})


def _date_matches(actual: date | None, requested: date | None, flex_days: int) -> bool:
    if requested is None:
        return True
    return actual is not None and abs((actual - requested).days) <= flex_days


def _last_seen(row: dict[str, Any]) -> str | None:
    raw = row.get("priceLastSeen")
    if not isinstance(raw, dict):
        return None
    value, unit = raw.get("value"), raw.get("unit")
    if value is None or not isinstance(unit, str):
        return None
    return f"{value} {unit} ago"


def parse_public_fares(
    html: str,
    *,
    airline_code: AirlineCode,
    airline_name: str,
    source_url: str,
    query: AirlineFareSearch,
) -> list[PublicFareQuote]:
    parser = _NextDataParser()
    parser.feed(html)
    if not parser.documents:
        raise CrawlerError("page_format_changed", "找不到公開票價頁的結構化資料")

    rows: list[dict[str, Any]] = []
    for document in parser.documents:
        try:
            payload: object = json.loads(document)
        except json.JSONDecodeError:
            continue
        for fares in _fare_lists(payload):
            rows.extend(fares)

    retrieved_at = datetime.now(UTC)
    quotes: dict[str, PublicFareQuote] = {}
    for row in rows:
        origin = str(row.get("originAirportCode", "")).upper()
        destination = str(row.get("destinationAirportCode", "")).upper()
        departure = _parse_date(row.get("departureDate"))
        returning = _parse_date(row.get("returnDate"))
        cabin = _parse_cabin(row.get("farenetTravelClass") or row.get("formattedTravelClass"))
        if not _airport_matches(query.origin, origin):
            continue
        if not _airport_matches(query.destination, destination):
            continue
        if cabin != query.cabin_class:
            continue
        if not _date_matches(departure, query.departure_date, query.flex_days):
            continue
        if not _date_matches(returning, query.return_date, query.flex_days):
            continue
        if departure is None:
            continue
        try:
            total_price = Decimal(str(row["totalPrice"]))
        except (KeyError, InvalidOperation):
            continue
        currency = str(row.get("currencyCode", "")).upper()
        if not currency:
            continue
        trip_type = str(row.get("flightType", "ROUND_TRIP")).lower()
        identity = ":".join(
            (
                airline_code,
                origin,
                destination,
                departure.isoformat(),
                returning.isoformat() if returning else "",
                cabin,
                currency,
                str(total_price),
            )
        )
        quotes[identity] = PublicFareQuote(
            id=uuid5(NAMESPACE_URL, f"travel-scanner:public-fare:{identity}"),
            airline_code=airline_code,
            airline_name=airline_name,
            origin=origin,
            destination=destination,
            departure_date=departure,
            return_date=returning,
            trip_type=trip_type,
            cabin_class=cabin,
            total_price=total_price,
            currency=currency,
            price_last_seen=_last_seen(row),
            source_url=source_url,
            retrieved_at=retrieved_at,
        )

    def sort_key(quote: PublicFareQuote) -> tuple[int, Decimal, date]:
        distance = (
            abs((quote.departure_date - query.departure_date).days) if query.departure_date else 0
        )
        return distance, quote.total_price, quote.departure_date

    return sorted(quotes.values(), key=sort_key)[: query.limit_per_airline]


class PublicFareAdapter:
    code: AirlineCode
    name: str
    host: str
    base_path: str
    enabled = True
    disabled_reason = ""

    def fare_url(self, query: AirlineFareSearch) -> str:
        origin_slug = CITY_SLUGS.get(query.origin)
        destination_slug = CITY_SLUGS.get(query.destination)
        if origin_slug is None or destination_slug is None:
            raise CrawlerError(
                "unsupported_route",
                f"公開票價頁目前不支援 {query.origin}-{query.destination} 的城市 slug",
            )
        return (
            f"https://{self.host}{self.base_path}/flights-from-{origin_slug}-to-{destination_slug}"
        )

    def parse(self, html: str, source_url: str, query: AirlineFareSearch) -> list[PublicFareQuote]:
        return parse_public_fares(
            html,
            airline_code=self.code,
            airline_name=self.name,
            source_url=source_url,
            query=query,
        )


class ChinaAirlinesFareAdapter(PublicFareAdapter):
    code = AirlineCode.CHINA_AIRLINES
    name = "中華航空"
    host = "flights.china-airlines.com"
    base_path = "/en-tw"


class EvaAirFareAdapter(PublicFareAdapter):
    code = AirlineCode.EVA_AIR
    name = "長榮航空"
    host = "flights.evaair.com"
    base_path = "/en-tw"
    enabled = False
    disabled_reason = "票價子網域的 robots.txt 回覆 403；依 fail-closed 政策暫停抓取"


class StarluxFareAdapter(PublicFareAdapter):
    code = AirlineCode.STARLUX
    name = "星宇航空"
    host = "www.starlux-airlines.com"
    base_path = "/flights/en-tw"


ADAPTERS: dict[AirlineCode, PublicFareAdapter] = {
    AirlineCode.CHINA_AIRLINES: ChinaAirlinesFareAdapter(),
    AirlineCode.EVA_AIR: EvaAirFareAdapter(),
    AirlineCode.STARLUX: StarluxFareAdapter(),
}


@dataclass(frozen=True)
class FetchResult:
    content: str
    cache_hit: bool


class _MemoryFallbackCache:
    def __init__(self) -> None:
        self._values: dict[str, tuple[float, str]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> str | None:
        async with self._lock:
            item = self._values.get(key)
            if item is None:
                return None
            expires_at, value = item
            if expires_at <= time.monotonic():
                self._values.pop(key, None)
                return None
            return value

    async def set(self, key: str, value: str, *, ttl: int, only_if_missing: bool = False) -> bool:
        async with self._lock:
            existing = self._values.get(key)
            if only_if_missing and existing and existing[0] > time.monotonic():
                return False
            self._values[key] = (time.monotonic() + ttl, value)
            return True


_memory_cache = _MemoryFallbackCache()


class RobotsAwareFetcher:
    def __init__(self, settings: Settings, redis: Redis) -> None:
        self.settings = settings
        self.redis = redis
        self._redis_available = True

    async def _get_cached(self, key: str) -> str | None:
        if not self._redis_available:
            return await _memory_cache.get(key)
        try:
            value = await asyncio.wait_for(
                self.redis.get(key),
                timeout=self.settings.airline_crawler_cache_backend_timeout_seconds,
            )
            return cast(str | None, value)
        except (TimeoutError, RedisError, OSError):
            self._redis_available = False
            return await _memory_cache.get(key)

    async def _set_cached(
        self, key: str, value: str, *, ttl: int, only_if_missing: bool = False
    ) -> bool:
        if not self._redis_available:
            return await _memory_cache.set(key, value, ttl=ttl, only_if_missing=only_if_missing)
        try:
            result = await asyncio.wait_for(
                self.redis.set(key, value, ex=ttl, nx=only_if_missing),
                timeout=self.settings.airline_crawler_cache_backend_timeout_seconds,
            )
            return bool(result)
        except (TimeoutError, RedisError, OSError):
            self._redis_available = False
            return await _memory_cache.set(key, value, ttl=ttl, only_if_missing=only_if_missing)

    async def _request(self, client: httpx.AsyncClient, url: str) -> str:
        last_error: Exception | None = None
        for attempt in range(2):
            try:
                async with client.stream("GET", url) as response:
                    if response.status_code >= 500 and attempt == 0:
                        await response.aread()
                        await asyncio.sleep(0.25)
                        continue
                    if response.status_code != 200:
                        raise CrawlerError(
                            "source_http_error",
                            f"來源 {urlsplit(url).hostname} 回覆 HTTP {response.status_code}",
                        )
                    content_length = response.headers.get("content-length")
                    if (
                        content_length
                        and int(content_length) > self.settings.airline_crawler_max_bytes
                    ):
                        raise CrawlerError("source_too_large", "來源頁面超過允許大小")
                    body = bytearray()
                    async for chunk in response.aiter_bytes():
                        body.extend(chunk)
                        if len(body) > self.settings.airline_crawler_max_bytes:
                            raise CrawlerError("source_too_large", "來源頁面超過允許大小")
                    return body.decode(response.encoding or "utf-8", errors="replace")
            except (httpx.TimeoutException, httpx.TransportError) as exc:
                last_error = exc
                if attempt == 0:
                    await asyncio.sleep(0.25)
                    continue
        raise CrawlerError("source_unavailable", "來源暫時無法連線") from last_error

    async def _robots_allows(self, client: httpx.AsyncClient, url: str) -> None:
        parsed = urlsplit(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        key = f"crawler:robots:{parsed.netloc}"
        body = await self._get_cached(key)
        if body is None:
            try:
                body = await self._request(client, robots_url)
            except CrawlerError as exc:
                raise CrawlerPolicyError(
                    "robots_unavailable",
                    f"無法確認 {parsed.netloc} 的 robots.txt，依 fail-closed 政策不抓取",
                ) from exc
            await self._set_cached(key, body, ttl=86_400)
        parser = RobotFileParser(robots_url)
        parser.parse(body.splitlines())
        if not parser.can_fetch(self.settings.airline_crawler_agent_token, url):
            raise CrawlerPolicyError("robots_disallowed", "robots.txt 不允許抓取此頁")

    async def fetch(self, client: httpx.AsyncClient, url: str) -> FetchResult:
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.hostname not in {
            adapter.host for adapter in ADAPTERS.values()
        }:
            raise CrawlerPolicyError("source_not_allowed", "來源 URL 不在航空公司白名單")
        digest = hashlib.sha256(url.encode()).hexdigest()
        page_key = f"crawler:page:{digest}"
        cached = await self._get_cached(page_key)
        if cached is not None:
            return FetchResult(cached, cache_hit=True)
        await self._robots_allows(client, url)
        throttle_key = f"crawler:throttle:{parsed.hostname}"
        acquired = await self._set_cached(
            throttle_key,
            "1",
            ttl=self.settings.airline_crawler_min_interval_seconds,
            only_if_missing=True,
        )
        if not acquired:
            raise CrawlerError("source_throttled", "同一來源請求過於頻繁，請稍後再試")
        content = await self._request(client, url)
        await self._set_cached(
            page_key, content, ttl=self.settings.airline_crawler_cache_ttl_seconds
        )
        return FetchResult(content, cache_hit=False)


class AirlineFareCrawlerService:
    def __init__(self, settings: Settings, redis: Redis) -> None:
        self.settings = settings
        self.fetcher = RobotsAwareFetcher(settings, redis)

    @staticmethod
    def status() -> list[AirlineCrawlerSource]:
        sources: list[AirlineCrawlerSource] = []
        for adapter in ADAPTERS.values():
            sources.append(
                AirlineCrawlerSource(
                    airline_code=adapter.code,
                    airline_name=adapter.name,
                    host=adapter.host,
                    state=SourceState.READY if adapter.enabled else SourceState.DISABLED,
                    policy="runtime_robots_check_fail_closed",
                    detail=(
                        "公開近期票價頁；每次快取失效後重新檢查 robots.txt"
                        if adapter.enabled
                        else adapter.disabled_reason
                    ),
                )
            )
        return sources

    async def _search_site(
        self,
        client: httpx.AsyncClient,
        adapter: PublicFareAdapter,
        query: AirlineFareSearch,
    ) -> tuple[list[PublicFareQuote], AirlineCrawlerSource, str | None]:
        if not adapter.enabled:
            source = AirlineCrawlerSource(
                airline_code=adapter.code,
                airline_name=adapter.name,
                host=adapter.host,
                state=SourceState.DISABLED,
                policy="runtime_robots_check_fail_closed",
                detail=adapter.disabled_reason,
            )
            return [], source, f"{adapter.name}：{adapter.disabled_reason}"
        try:
            url = adapter.fare_url(query)
            fetched = await self.fetcher.fetch(client, url)
            quotes = adapter.parse(fetched.content, url, query)
            detail = "讀取公開近期票價成功"
            warning = None
            if not quotes:
                detail = "來源正常，但指定日期或艙等沒有公開快取票價"
                warning = f"{adapter.name}：{detail}"
            source = AirlineCrawlerSource(
                airline_code=adapter.code,
                airline_name=adapter.name,
                host=adapter.host,
                state=SourceState.SUCCESS,
                policy="robots_allowed",
                detail=detail,
                quote_count=len(quotes),
                cache_hit=fetched.cache_hit,
            )
            return quotes, source, warning
        except CrawlerPolicyError as exc:
            source = AirlineCrawlerSource(
                airline_code=adapter.code,
                airline_name=adapter.name,
                host=adapter.host,
                state=SourceState.BLOCKED,
                policy="fail_closed",
                detail=exc.detail,
            )
            return [], source, f"{adapter.name}：{exc.detail}"
        except CrawlerError as exc:
            source = AirlineCrawlerSource(
                airline_code=adapter.code,
                airline_name=adapter.name,
                host=adapter.host,
                state=SourceState.FAILED,
                policy="robots_checked",
                detail=exc.detail,
            )
            return [], source, f"{adapter.name}：{exc.detail}"

    async def search(self, query: AirlineFareSearch) -> AirlineFareSearchResponse:
        timeout = httpx.Timeout(self.settings.airline_crawler_timeout_seconds)
        headers = {
            "User-Agent": self.settings.airline_crawler_user_agent,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
        }
        async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
            tasks = [self._search_site(client, ADAPTERS[code], query) for code in query.airlines]
            results = await asyncio.gather(*tasks)
        quotes = [quote for result, _, _ in results for quote in result]
        sources = [source for _, source, _ in results]
        warnings = [warning for _, _, warning in results if warning]
        quotes.sort(key=lambda quote: (quote.total_price, quote.departure_date))
        return AirlineFareSearchResponse(quotes=quotes, sources=sources, warnings=warnings)
