import asyncio

import fakeredis.aioredis
import pytest

from app.providers.mock import MockProvider
from app.providers.runner import ProviderRunner, ProviderUnavailableError


@pytest.mark.asyncio
async def test_provider_timeout_isolated(monkeypatch: pytest.MonkeyPatch) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    runner = ProviderRunner(redis)
    monkeypatch.setattr(runner.settings, "provider_timeout_seconds", 0.01)
    provider = MockProvider(latency=0.1)

    async def slow_call() -> list[object]:
        await asyncio.sleep(provider.latency)
        return []

    with pytest.raises(ProviderUnavailableError):
        await runner.run("mock", "flight", slow_call)
