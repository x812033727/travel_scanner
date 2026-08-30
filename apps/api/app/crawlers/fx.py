import asyncio
import json
import time
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from typing import cast

import httpx
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import Settings
from app.crawlers.schemas import FxRateSnapshot


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

    async def _fetch(self, currency: str) -> FxRateSnapshot:
        source_url = (
            f"{self.settings.fx_rate_base_url.rstrip('/')}/rates"
            f"?base={currency}&quotes=TWD"
        )
        timeout = httpx.Timeout(self.settings.fx_rate_timeout_seconds)
        try:
            async with httpx.AsyncClient(timeout=timeout, transport=self.transport) as client:
                response = await client.get(source_url, headers={"Accept": "application/json"})
                response.raise_for_status()
                payload = response.json()
            if not isinstance(payload, dict):
                raise FxRateError("匯率服務回應格式錯誤")
            rate = Decimal(str(payload["rate"]))
            as_of = date.fromisoformat(str(payload["date"]))
            if str(payload.get("base", "")).upper() != currency:
                raise FxRateError("匯率服務回傳的基準幣別不符")
            if str(payload.get("quote", "")).upper() != "TWD" or rate <= 0:
                raise FxRateError("匯率服務未提供有效 TWD 匯率")
        except (
            httpx.HTTPError,
            KeyError,
            ValueError,
            InvalidOperation,
            json.JSONDecodeError,
        ) as exc:
            raise FxRateError("目前無法取得 TWD 估算匯率") from exc
        return FxRateSnapshot(
            base_currency=currency,
            rate=rate,
            as_of=as_of,
            source_url=source_url,
        )

    async def rate_to_twd(self, currency: str) -> FxRateSnapshot:
        normalized = currency.upper()
        if normalized == "TWD":
            return FxRateSnapshot(
                base_currency="TWD",
                rate=Decimal("1"),
                as_of=datetime.now(UTC).date(),
                source_url="internal://identity-rate",
            )

        fresh_key = f"fx:frankfurter:{normalized}:TWD:fresh"
        stale_key = f"fx:frankfurter:{normalized}:TWD:stale"
        cached = await self._get(fresh_key)
        if cached is not None:
            return self._deserialize(cached, stale=False)

        try:
            snapshot = await self._fetch(normalized)
        except FxRateError:
            stale = await self._get(stale_key)
            if stale is not None:
                return self._deserialize(stale, stale=True)
            raise

        serialized = snapshot.model_dump_json()
        await self._set(fresh_key, serialized, self.settings.fx_rate_cache_ttl_seconds)
        await self._set(stale_key, serialized, self.settings.fx_rate_stale_ttl_seconds)
        return snapshot
