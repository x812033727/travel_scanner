import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

from redis.asyncio import Redis

from app.config import Settings, get_settings

T = TypeVar("T")


class ProviderUnavailableError(RuntimeError):
    pass


class ProviderRunner:
    def __init__(self, redis: Redis, settings: Settings | None = None) -> None:
        self.redis = redis
        self.settings = settings or get_settings()

    async def run(
        self,
        provider: str,
        module: str,
        call: Callable[[], Awaitable[T]],
        *,
        timeout_seconds: float | None = None,
    ) -> T:
        circuit_key = f"provider:circuit:{provider}:{module}"
        if await self.redis.exists(circuit_key):
            raise ProviderUnavailableError(f"{provider}/{module} circuit is open")
        last_error: Exception | None = None
        for attempt in range(2):
            try:
                result = await asyncio.wait_for(
                    call(), timeout=timeout_seconds or self.settings.provider_timeout_seconds
                )
                await self.redis.delete(f"provider:failures:{provider}:{module}")
                return result
            except (TimeoutError, ConnectionError) as exc:
                last_error = exc
                if attempt == 0:
                    await asyncio.sleep(0.05)
        failure_key = f"provider:failures:{provider}:{module}"
        failures = await self.redis.incr(failure_key)
        await self.redis.expire(failure_key, self.settings.provider_circuit_seconds)
        if failures >= self.settings.provider_failure_threshold:
            await self.redis.set(circuit_key, "open", ex=self.settings.provider_circuit_seconds)
        raise ProviderUnavailableError(f"{provider}/{module} failed") from last_error
