from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")

    app_env: str = "development"
    app_secret_key: str = "development-secret-change-me-please-32"
    database_url: str = "postgresql+asyncpg://travel:travel@localhost:5432/travel_scanner"
    redis_url: str = "redis://localhost:6379/0"
    api_cors_origins: str = "http://localhost:3000"
    access_token_expire_minutes: int = 60
    cookie_secure: bool = False
    offer_cache_ttl_seconds: int = 300
    reference_cache_ttl_seconds: int = 86_400
    provider_timeout_seconds: float = 3.0
    provider_failure_threshold: int = 3
    provider_circuit_seconds: int = 60
    rate_limit_per_minute: int = Field(default=120, ge=1)
    travel_provider_mode: str = "mock"
    amadeus_client_id: str | None = None
    amadeus_client_secret: str | None = None
    amadeus_env: str = "test"
    google_maps_api_key: str | None = None
    next_public_site_url: str = "http://localhost:3000"
    airline_crawler_user_agent: str = (
        "TravelScannerBot/0.1 (+https://github.com/x812033727/travel_scanner)"
    )
    airline_crawler_agent_token: str = "TravelScannerBot"
    airline_crawler_timeout_seconds: float = Field(default=10.0, gt=0, le=30)
    airline_crawler_cache_ttl_seconds: int = Field(default=1800, ge=60, le=86_400)
    airline_crawler_min_interval_seconds: int = Field(default=5, ge=1, le=60)
    airline_crawler_max_bytes: int = Field(default=2_500_000, ge=100_000, le=5_000_000)
    airline_crawler_cache_backend_timeout_seconds: float = Field(default=0.5, gt=0, le=5)
    fx_rate_base_url: str = "https://api.frankfurter.dev/v2"
    fx_rate_timeout_seconds: float = Field(default=3.0, gt=0, le=10)
    fx_rate_cache_ttl_seconds: int = Field(default=86_400, ge=300, le=86_400)
    fx_rate_stale_ttl_seconds: int = Field(default=604_800, ge=86_400, le=2_592_000)

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.api_cors_origins.split(",") if origin.strip()]

    @property
    def amadeus_base_url(self) -> str:
        return (
            "https://api.amadeus.com"
            if self.amadeus_env.lower() == "production"
            else "https://test.api.amadeus.com"
        )

    @property
    def amadeus_configured(self) -> bool:
        return bool(self.amadeus_client_id and self.amadeus_client_secret)

    @property
    def production(self) -> bool:
        return self.app_env.lower() in {"production", "prod"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
