from typing import Literal

from pydantic import BaseModel, Field
from redis.asyncio import Redis

from app.config import Settings, get_settings
from app.providers.amadeus import AmadeusProvider
from app.providers.base import FlightProvider, HotelProvider, TravelProvider
from app.providers.booking import BookingHotelProvider
from app.providers.duffel import DuffelProvider
from app.providers.mock import MockProvider
from app.providers.skyscanner import SkyscannerProvider

ProviderMode = Literal["live", "test", "mock", "disabled"]
ProviderReadiness = Literal["ready", "not_configured", "disabled"]


class ModuleProviderStatus(BaseModel):
    selected_provider: str
    mode: ProviderMode
    status: ProviderReadiness
    available: bool
    configured: bool
    fallback_provider: str | None = None
    environment: str
    message: str
    candidate_providers: list[str] = Field(default_factory=list)
    strategy: str | None = None

    @property
    def provider(self) -> str:
        """Compatibility alias for existing internal callers."""
        return self.selected_provider


class ProviderStatus(BaseModel):
    provider: str
    mode: ProviderMode
    status: ProviderReadiness
    modules: list[str]
    message: str
    module_statuses: dict[str, ModuleProviderStatus] = Field(default_factory=dict)


def _status(
    provider: str,
    *,
    configured: bool,
    mode: ProviderMode,
    environment: str,
    ready_message: str,
    missing_message: str,
    fallback_provider: str | None = None,
    disabled: bool = False,
) -> ModuleProviderStatus:
    status: ProviderReadiness = (
        "disabled" if disabled else "ready" if configured else "not_configured"
    )
    return ModuleProviderStatus(
        selected_provider=provider if not disabled else "none",
        mode=mode if configured and not disabled else "disabled",
        status=status,
        available=configured and not disabled,
        configured=configured,
        fallback_provider=fallback_provider if configured and not disabled else None,
        environment=environment,
        message=ready_message if configured and not disabled else missing_message,
    )


def _amadeus_status(config: Settings, module: str) -> ModuleProviderStatus:
    labels = {
        "flight": "Amadeus 航班查價",
        "hotel": "Amadeus 飯店查價",
        "activities": "Amadeus 活動搜尋",
        "transport": "Amadeus 接送搜尋",
    }
    label = labels[module]
    configured = config.amadeus_configured and not (
        config.production and config.amadeus_env.lower() != "production"
    )
    return _status(
        "amadeus",
        configured=configured,
        mode="live" if config.amadeus_env.lower() == "production" else "test",
        environment=config.amadeus_env.lower(),
        ready_message=f"{label}已啟用。",
        missing_message=f"{label}尚未啟用：缺少 Client ID 或 Secret。",
    )


def _mock_status(config: Settings, module: str) -> ModuleProviderStatus:
    allowed = not config.production
    return _status(
        "mock",
        configured=allowed,
        mode="mock",
        environment="development",
        ready_message=f"{module} 正在使用明確標示的模擬資料。",
        missing_message="正式環境禁止使用模擬報價。",
        disabled=not allowed,
    )


def flight_provider_status(settings: Settings | None = None) -> ModuleProviderStatus:
    config = settings or get_settings()
    requested = config.flight_provider_mode.lower()
    if requested == "auto":
        candidates = []
        if config.skyscanner_configured:
            candidates.append("skyscanner")
        if config.duffel_configured and not (
            config.production and config.duffel_env.lower() != "live"
        ):
            candidates.append("duffel")
        if config.amadeus_configured and not (
            config.production and config.amadeus_env.lower() != "production"
        ):
            candidates.append("amadeus")
        if candidates:
            requested = candidates[0]
        elif config.travel_provider_mode.lower() == "mock" and not config.production:
            requested, candidates = "mock", ["mock"]
        else:
            requested, candidates = "disabled", []
    else:
        candidates = [requested] if requested != "disabled" else []
    if requested == "skyscanner":
        result = _status(
            "skyscanner",
            configured=config.skyscanner_configured,
            mode="live",
            environment="production",
            ready_message="Skyscanner 即時航班比價已啟用。",
            missing_message="航班即時比價尚未啟用：缺少 Skyscanner API key。",
            fallback_provider=candidates[1] if len(candidates) > 1 else None,
        )
        result.candidate_providers = candidates
        result.strategy = config.flight_search_strategy
        return result
    if requested == "duffel":
        configured = config.duffel_configured and not (
            config.production and config.duffel_env.lower() != "live"
        )
        result = _status(
            "duffel",
            configured=configured,
            mode="live" if config.duffel_env.lower() == "live" else "test",
            environment=config.duffel_env.lower(),
            ready_message="Duffel 航班報價已啟用。",
            missing_message="Duffel 尚未啟用，或正式環境仍設定為 test。",
            fallback_provider=candidates[1] if len(candidates) > 1 else None,
        )
        result.candidate_providers = candidates
        result.strategy = config.flight_search_strategy
        return result
    if requested in {"amadeus", "live"}:
        result = _amadeus_status(config, "flight")
        result.candidate_providers = candidates
        result.strategy = config.flight_search_strategy
        return result
    if requested == "mock":
        return _mock_status(config, "flight")
    return _status(
        "none",
        configured=False,
        mode="disabled",
        environment=config.app_env,
        ready_message="",
        missing_message="目前沒有可用的航班查價供應商。",
        disabled=True,
    )


def hotel_provider_status(settings: Settings | None = None) -> ModuleProviderStatus:
    config = settings or get_settings()
    requested = config.hotel_provider_mode.lower()
    if requested == "auto":
        if config.booking_demand_configured:
            requested = "booking"
        elif config.amadeus_configured:
            requested = "amadeus"
        elif config.travel_provider_mode.lower() == "mock" and not config.production:
            requested = "mock"
        else:
            requested = "disabled"
    if requested == "booking":
        return _status(
            "booking",
            configured=config.booking_demand_configured,
            mode="live" if config.booking_demand_env.lower() == "production" else "test",
            environment=config.booking_demand_env.lower(),
            ready_message="Booking.com Demand API 飯店查價已啟用。",
            missing_message=(
                "Booking.com 飯店查價尚未啟用：請確認 Demand API 已啟用、"
                "Affiliate ID 與 Bearer Token 均已設定。"
            ),
            fallback_provider="amadeus" if config.amadeus_configured else None,
        )
    if requested in {"amadeus", "live"}:
        return _amadeus_status(config, "hotel")
    if requested == "mock":
        return _mock_status(config, "hotel")
    return _status(
        "none",
        configured=False,
        mode="disabled",
        environment=config.app_env,
        ready_message="",
        missing_message="目前沒有可用的飯店查價供應商。",
        disabled=True,
    )


def travel_module_status(module: str, settings: Settings | None = None) -> ModuleProviderStatus:
    config = settings or get_settings()
    requested = config.travel_provider_mode.lower()
    if requested in {"live", "amadeus"}:
        return _amadeus_status(config, module)
    if requested == "mock":
        return _mock_status(config, module)
    return _status(
        "none",
        configured=False,
        mode="disabled",
        environment=config.app_env,
        ready_message="",
        missing_message=f"目前沒有可用的 {module} 供應商。",
        disabled=True,
    )


def module_provider_statuses(
    settings: Settings | None = None,
) -> dict[str, ModuleProviderStatus]:
    config = settings or get_settings()
    return {
        "flight": flight_provider_status(config),
        "hotel": hotel_provider_status(config),
        "activities": travel_module_status("activities", config),
        "transport": travel_module_status("transport", config),
    }


def provider_status(settings: Settings | None = None) -> ProviderStatus:
    config = settings or get_settings()
    statuses = module_provider_statuses(config)
    ready = [module for module, status in statuses.items() if status.available]
    explicit_flight = config.flight_provider_mode.lower() != "auto"
    primary = (
        statuses["flight"]
        if statuses["flight"].available or explicit_flight
        else next((status for status in statuses.values() if status.available), statuses["flight"])
    )
    if explicit_flight and not primary.available:
        return ProviderStatus(
            provider=primary.selected_provider,
            mode=primary.mode,
            status=primary.status,
            modules=ready,
            message=primary.message,
            module_statuses=statuses,
        )
    if ready:
        summary = "、".join(f"{module}={statuses[module].selected_provider}" for module in ready)
        message = f"可用即時資料模組：{summary}。"
        overall: ProviderReadiness = "ready"
    else:
        message = "；".join(dict.fromkeys(status.message for status in statuses.values()))
        overall = (
            "not_configured"
            if any(status.status == "not_configured" for status in statuses.values())
            else "disabled"
        )
    return ProviderStatus(
        provider=primary.selected_provider,
        mode=primary.mode,
        status=overall,
        modules=ready,
        message=message,
        module_statuses=statuses,
    )


def provider_status_for_modules(
    modules: list[str], settings: Settings | None = None
) -> ProviderStatus:
    aggregate = provider_status(settings)
    requested = [module for module in modules if module in aggregate.module_statuses]
    statuses = [aggregate.module_statuses[module] for module in requested]
    ready_modules = [module for module in requested if aggregate.module_statuses[module].available]
    if ready_modules:
        primary = aggregate.module_statuses[ready_modules[0]]
        aggregate.provider = primary.selected_provider
        aggregate.mode = primary.mode
        aggregate.status = "ready"
        aggregate.modules = ready_modules
        aggregate.message = "、".join(
            f"{module}={aggregate.module_statuses[module].selected_provider}"
            for module in ready_modules
        )
        return aggregate
    aggregate.modules = []
    aggregate.status = (
        "not_configured"
        if any(item.status == "not_configured" for item in statuses)
        else "disabled"
    )
    aggregate.message = "；".join(dict.fromkeys(item.message for item in statuses))
    return aggregate


def build_flight_provider(
    redis: Redis, settings: Settings | None = None, provider_name: str | None = None
) -> FlightProvider | None:
    config = settings or get_settings()
    selected = provider_name or flight_provider_status(config).selected_provider
    if selected == "skyscanner":
        return SkyscannerProvider(redis, config) if config.skyscanner_configured else None
    if selected == "duffel":
        if config.production and config.duffel_env.lower() != "live":
            return None
        return DuffelProvider(redis, config) if config.duffel_configured else None
    if selected == "amadeus":
        if config.production and config.amadeus_env.lower() != "production":
            return None
        return AmadeusProvider(redis, config) if config.amadeus_configured else None
    if selected == "mock":
        return MockProvider() if not config.production else None
    return None


def build_hotel_provider(
    redis: Redis, settings: Settings | None = None, provider_name: str | None = None
) -> HotelProvider | None:
    config = settings or get_settings()
    selected = provider_name or hotel_provider_status(config).selected_provider
    if selected == "booking":
        return BookingHotelProvider(redis, config) if config.booking_demand_configured else None
    if selected == "amadeus":
        return AmadeusProvider(redis, config) if config.amadeus_configured else None
    if selected == "mock":
        return MockProvider() if not config.production else None
    return None


def build_provider(redis: Redis, settings: Settings | None = None) -> TravelProvider | None:
    config = settings or get_settings()
    status = travel_module_status("activities", config)
    if not status.available:
        return None
    if status.selected_provider == "amadeus":
        return AmadeusProvider(redis, config)
    return MockProvider()


def build_module_provider_candidates(
    redis: Redis, settings: Settings | None = None
) -> dict[str, list[object]]:
    config = settings or get_settings()
    flight = build_flight_provider(redis, config)
    hotel = build_hotel_provider(redis, config)
    travel = build_provider(redis, config)
    candidates: dict[str, list[object]] = {
        "flight": [flight] if flight else [],
        "hotel": [hotel] if hotel else [],
        "activities": [travel] if travel else [],
        "transport": [travel] if travel else [],
    }
    if config.flight_provider_mode.lower() == "auto":
        candidates["flight"] = []
        if config.skyscanner_configured:
            candidates["flight"].append(SkyscannerProvider(redis, config))
        if config.duffel_configured and not (
            config.production and config.duffel_env.lower() != "live"
        ):
            candidates["flight"].append(DuffelProvider(redis, config))
        if config.amadeus_configured and not (
            config.production and config.amadeus_env.lower() != "production"
        ):
            candidates["flight"].append(AmadeusProvider(redis, config))
        if (
            not candidates["flight"]
            and config.travel_provider_mode == "mock"
            and not config.production
        ):
            candidates["flight"].append(MockProvider())
    for module in ("flight", "hotel"):
        primary = candidates[module][0] if candidates[module] else None
        if (
            primary is not None
            and getattr(primary, "name", None) != "amadeus"
            and config.amadeus_configured
            and not (config.production and config.amadeus_env.lower() != "production")
            and not any(getattr(item, "name", None) == "amadeus" for item in candidates[module])
        ):
            candidates[module].append(AmadeusProvider(redis, config))
    return candidates


def build_module_providers(
    redis: Redis, settings: Settings | None = None
) -> dict[str, object | None]:
    return {
        module: candidates[0] if candidates else None
        for module, candidates in build_module_provider_candidates(redis, settings).items()
    }
