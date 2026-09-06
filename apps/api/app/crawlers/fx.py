import asyncio
import json
import time
from collections.abc import Callable
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from typing import cast

import httpx
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import Settings
from app.crawlers.schemas import FxRateSnapshot

RateParser = Callable[[object, str, str], tuple[Decimal, date]]


class FxRateError(Exception):
    pass


class FxRateProvider:
    def __init__(
        self,
        settings: Settings,
        redis: Redis,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.settings = settings
        self.redis = redis
        self.transport = transport
        self._memory_cache: dict[str, tuple[float, str]] = {}
        self._redis_available = True

    async def _get(self, key: str) -> str | None:
        if not self._redis_available:
            cached = self._memory_cache.get(key)
            if cached is None:
                return None
            expires_at, value = cached
            if expires_at <= time.monotonic():
                self._memory_cache.pop(key, None)
                return None
            return value
        try:
            value = await asyncio.wait_for(
                self.redis.get(key),
                timeout=self.settings.airline_crawler_cache_backend_timeout_seconds,
            )
            return cast(str | None, value)
        except (TimeoutError, RedisError, OSError):
            self._redis_available = False
            return await self._get(key)

    async def _set(self, key: str, value: str, ttl: int) -> None:
        self._memory_cache[key] = (time.monotonic() + ttl, value)
        if not self._redis_available:
            return
        try:
            await asyncio.wait_for(
                self.redis.set(key, value, ex=ttl),
                timeout=self.settings.airline_crawler_cache_backend_timeout_seconds,
            )
        except (TimeoutError, RedisError, OSError):
            self._redis_available = False

    @staticmethod
    def _deserialize(value: str, *, stale: bool) -> FxRateSnapshot:
        snapshot = FxRateSnapshot.model_validate_json(value)
        return snapshot.model_copy(update={"is_stale": stale})

    @staticmethod
    def _parse_currency_api(payload: object, base: str, quote: str) -> tuple[Decimal, date]:
        """``{"date": "2026-09-05", "jpy": {"twd": 0.2028, ...}}`` from Currency-api."""
        if not isinstance(payload, dict):
            raise FxRateError("匯率服務回應格式錯誤")
        table = payload.get(base.lower())
        if not isinstance(table, dict) or quote.lower() not in table:
            raise FxRateError("匯率服務未提供這組幣別")
        rate = Decimal(str(table[quote.lower()]))
        if rate <= 0:
            raise FxRateError("匯率服務未提供有效匯率")
        return rate, date.fromisoformat(str(payload["date"]))

    @staticmethod
    def _parse_frankfurter(payload: object, base: str, quote: str) -> tuple[Decimal, date]:
        """``[{"date", "base", "quote", "rate"}]`` (or a single object) from Frankfurter v2."""
        if isinstance(payload, list):
            payload = next(
                (
                    item
                    for item in payload
                    if isinstance(item, dict)
                    and str(item.get("base", "")).upper() == base
                    and str(item.get("quote", "")).upper() == quote
                ),
                None,
            )
        if not isinstance(payload, dict):
            raise FxRateError("匯率服務回應格式錯誤")
        rate = Decimal(str(payload["rate"]))
        if str(payload.get("base", "")).upper() != base:
            raise FxRateError("匯率服務回傳的基準幣別不符")
        if str(payload.get("quote", "")).upper() != quote or rate <= 0:
            raise FxRateError(f"匯率服務未提供有效 {quote} 匯率")
        return rate, date.fromisoformat(str(payload["date"]))

    def _sources(self, base: str, quote: str) -> list[tuple[str, RateParser]]:
        """Currency-api on its two CDNs first (daily, 300+ currencies), then Frankfurter."""
        file_name = f"currencies/{base.lower()}.min.json"
        return [
            (
                f"{self.settings.fx_currency_api_base_url.rstrip('/')}/{file_name}",
                self._parse_currency_api,
            ),
            (
                f"{self.settings.fx_currency_api_fallback_url.rstrip('/')}/{file_name}",
                self._parse_currency_api,
            ),
            (
                f"{self.settings.fx_rate_base_url.rstrip('/')}/rates?base={base}&quotes={quote}",
                self._parse_frankfurter,
            ),
        ]

    async def _fetch(self, base: str, quote: str) -> FxRateSnapshot:
        timeout = httpx.Timeout(self.settings.fx_rate_timeout_seconds)
        async with httpx.AsyncClient(timeout=timeout, transport=self.transport) as client:
            for source_url, parse in self._sources(base, quote):
                try:
                    response = await client.get(source_url, headers={"Accept": "application/json"})
                    response.raise_for_status()
                    rate, as_of = parse(response.json(), base, quote)
                except (
                    httpx.HTTPError,
                    FxRateError,
                    KeyError,
                    ValueError,
                    InvalidOperation,
                    json.JSONDecodeError,
                ):
                    continue
                return FxRateSnapshot(
                    base_currency=base,
                    quote_currency=quote,
                    rate=rate,
                    as_of=as_of,
                    source_url=source_url,
                )
        raise FxRateError(f"目前無法取得 {quote} 估算匯率")

    async def rate(self, base_currency: str, quote_currency: str) -> FxRateSnapshot:
        """One unit of ``base_currency`` in ``quote_currency``, cached for a day."""
        base = base_currency.upper()
        quote = quote_currency.upper()
        if base == quote:
            return FxRateSnapshot(
                base_currency=base,
                quote_currency=quote,
                rate=Decimal("1"),
                as_of=datetime.now(UTC).date(),
                source_url="internal://identity-rate",
            )

        fresh_key = f"fx:rates:{base}:{quote}:fresh"
        stale_key = f"fx:rates:{base}:{quote}:stale"
        cached = await self._get(fresh_key)
        if cached is not None:
            return self._deserialize(cached, stale=False)

        try:
            snapshot = await self._fetch(base, quote)
        except FxRateError:
            stale = await self._get(stale_key)
            if stale is not None:
                return self._deserialize(stale, stale=True)
            raise

        serialized = snapshot.model_dump_json()
        await self._set(fresh_key, serialized, self.settings.fx_rate_cache_ttl_seconds)
        await self._set(stale_key, serialized, self.settings.fx_rate_stale_ttl_seconds)
        return snapshot

    async def rate_to_twd(self, currency: str) -> FxRateSnapshot:
        return await self.rate(currency, "TWD")
