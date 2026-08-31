from typing import Literal

from pydantic import BaseModel
from redis.asyncio import Redis

from app.config import Settings, get_settings
from app.providers.amadeus import AmadeusProvider
from app.providers.base import FlightProvider, TravelProvider
from app.providers.mock import MockProvider
from app.providers.skyscanner import SkyscannerProvider


class ProviderStatus(BaseModel):
    provider: str
    mode: Literal["live", "test", "mock", "disabled"]
    status: Literal["ready", "not_configured", "disabled"]
    modules: list[str]
    message: str


def _travel_provider_status(config: Settings) -> ProviderStatus:
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


def flight_provider_status(settings: Settings | None = None) -> ProviderStatus:
    config = settings or get_settings()
    requested = config.flight_provider_mode.lower()
    if requested == "auto":
        if config.skyscanner_configured:
            requested = "skyscanner"
        elif config.amadeus_configured:
            requested = "amadeus"
        elif config.travel_provider_mode.lower() == "mock":
            requested = "mock"
        else:
            requested = config.travel_provider_mode.lower()
    if requested == "skyscanner":
        if not config.skyscanner_configured:
            return ProviderStatus(
                provider="skyscanner",
                mode="disabled",
                status="not_configured",
                modules=["flight"],
                message="航班即時比價尚未啟用：缺少 Skyscanner API key。",
            )
        return ProviderStatus(
            provider="skyscanner",
            mode="live",
            status="ready",
            modules=["flight"],
            message="Skyscanner 即時航班比價已啟用。",
        )
    if requested in {"amadeus", "live"}:
        status = _travel_provider_status(
            config.model_copy(update={"travel_provider_mode": "amadeus"})
        )
        status.modules = ["flight"]
        return status
    if requested == "mock" and not config.production:
        return ProviderStatus(
            provider="mock",
            mode="mock",
            status="ready",
            modules=["flight"],
            message="開發環境正在使用模擬航班資料。",
        )
    return ProviderStatus(
        provider="none",
        mode="disabled",
        status="disabled",
        modules=["flight"],
        message="正式環境沒有可用的航班供應商。",
    )


def provider_status(settings: Settings | None = None) -> ProviderStatus:
    config = settings or get_settings()
    flight = flight_provider_status(config)
    if config.flight_provider_mode.lower() != "auto" or flight.provider == "skyscanner":
        return flight
    return _travel_provider_status(config)


def provider_status_for_modules(
    modules: list[str], settings: Settings | None = None
) -> ProviderStatus:
    config = settings or get_settings()
    statuses = []
    if "flight" in modules:
        statuses.append(flight_provider_status(config))
    if any(module in {"hotel", "activities", "transport"} for module in modules):
        statuses.append(_travel_provider_status(config))
    ready = next((item for item in statuses if item.status == "ready"), None)
    return ready or (statuses[0] if statuses else provider_status(config))


def build_flight_provider(
    redis: Redis, settings: Settings | None = None, provider_name: str | None = None
) -> FlightProvider | None:
    config = settings or get_settings()
    if provider_name == "skyscanner":
        return SkyscannerProvider(redis, config) if config.skyscanner_configured else None
    if provider_name == "amadeus":
        return AmadeusProvider(redis, config) if config.amadeus_configured else None
    if provider_name == "mock":
        return MockProvider() if not config.production else None
    status = flight_provider_status(config)
    if status.status != "ready":
        return None
    if status.provider == "skyscanner":
        return SkyscannerProvider(redis, config)
    if status.provider == "amadeus":
        return AmadeusProvider(redis, config)
    return MockProvider()


def build_provider(redis: Redis, settings: Settings | None = None) -> TravelProvider | None:
    config = settings or get_settings()
    status = _travel_provider_status(config)
    if status.status != "ready":
        return None
    if status.provider == "amadeus":
        return AmadeusProvider(redis, config)
    return MockProvider()


def build_module_providers(
    redis: Redis, settings: Settings | None = None
) -> dict[str, object | None]:
    config = settings or get_settings()
    travel = build_provider(redis, config)
    return {
        "flight": build_flight_provider(redis, config),
        "hotel": travel,
        "activities": travel,
        "transport": travel,
    }
