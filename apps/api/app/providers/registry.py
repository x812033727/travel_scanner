from typing import Literal

from pydantic import BaseModel
from redis.asyncio import Redis

from app.config import Settings, get_settings
from app.providers.amadeus import AmadeusProvider
from app.providers.base import TravelProvider
from app.providers.mock import MockProvider


class ProviderStatus(BaseModel):
    provider: str
    mode: Literal["live", "test", "mock", "disabled"]
    status: Literal["ready", "not_configured", "disabled"]
    modules: list[str]
    message: str


def provider_status(settings: Settings | None = None) -> ProviderStatus:
    config = settings or get_settings()
    requested = config.travel_provider_mode.lower()
    modules = ["flight", "hotel", "activities", "transport"]
    if requested in {"live", "amadeus"}:
        if not config.amadeus_configured:
            return ProviderStatus(
                provider="amadeus",
                mode="disabled",
                status="not_configured",
                modules=modules,
                message="即時資料服務尚未啟用：缺少 Amadeus API 憑證。",
            )
        return ProviderStatus(
            provider="amadeus",
            mode="live" if config.amadeus_env.lower() == "production" else "test",
            status="ready",
            modules=modules,
            message="Amadeus 即時旅遊資料已啟用。",
        )
    if requested == "mock" and not config.production:
        return ProviderStatus(
            provider="mock",
            mode="mock",
            status="ready",
            modules=modules,
            message="開發環境正在使用明確標示的模擬資料。",
        )
    return ProviderStatus(
        provider="none",
        mode="disabled",
        status="disabled",
        modules=modules,
        message="正式環境禁止使用模擬報價，請設定即時供應商。",
    )


def build_provider(redis: Redis, settings: Settings | None = None) -> TravelProvider | None:
    config = settings or get_settings()
    status = provider_status(config)
    if status.status != "ready":
        return None
    if status.provider == "amadeus":
        return AmadeusProvider(redis, config)
    return MockProvider()
