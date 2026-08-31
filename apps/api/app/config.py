from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")

    app_env: str = "development"
    app_secret_key: str = "development-secret-change-me-please-32"
    settings_encryption_key: str | None = None
    admin_emails: str = ""
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
    flight_provider_mode: str = "auto"
    flight_search_strategy: str = "hybrid"
    flight_min_result_count: int = Field(default=12, ge=1, le=100)
    hotel_provider_mode: str = "auto"
    amadeus_client_id: str | None = None
    amadeus_client_secret: str | None = None
    amadeus_env: str = "test"
    skyscanner_api_key: str | None = None
    skyscanner_base_url: str = "https://partners.api.skyscanner.net"
    skyscanner_market: str = "TW"
    skyscanner_locale: str = "zh-TW"
    skyscanner_currency: str = "TWD"
    skyscanner_poll_attempts: int = Field(default=4, ge=1, le=10)
    skyscanner_poll_interval_seconds: float = Field(default=0.5, ge=0, le=5)
    duffel_access_token: str | None = None
    duffel_env: str = "test"
    duffel_base_url: str = "https://api.duffel.com"
    duffel_supplier_timeout_ms: int = Field(default=10_000, ge=2_000, le=60_000)
    flightaware_api_key: str | None = None
    flightaware_base_url: str = "https://aeroapi.flightaware.com/aeroapi"
    flightaware_enrich_offer_limit: int = Field(default=5, ge=0, le=20)
    flightaware_cache_ttl_seconds: int = Field(default=300, ge=60, le=3_600)
    flightaware_track_cache_ttl_seconds: int = Field(default=120, ge=30, le=900)
    google_travel_impact_api_key: str | None = None
    google_travel_impact_base_url: str = "https://travelimpactmodel.googleapis.com/v1"
    travel_impact_cache_ttl_seconds: int = Field(default=86_400, ge=300, le=604_800)
    flight_status_retention_hours: int = Field(default=24, ge=1, le=168)
    affiliate_link_cache_ttl_seconds: int = Field(default=86_400, ge=60, le=604_800)
    affiliate_clickout_token_ttl_seconds: int = Field(default=900, ge=60, le=3_600)
    travelpayouts_enabled: bool = False
    travelpayouts_api_base_url: str = "https://api.travelpayouts.com"
    travelpayouts_marker: str | None = None
    travelpayouts_project_id: str | None = None
    travelpayouts_api_token: str | None = None
    travelpayouts_static_url_template: str | None = None
    travelpayouts_flight_target_url: str | None = None
    travelpayouts_hotel_target_url: str | None = None
    travelpayouts_activities_target_url: str | None = None
    travelpayouts_transport_target_url: str | None = None
    travelpayouts_allowed_hosts: str = "tp.st,travelpayouts.com"
    kkday_enabled: bool = False
    kkday_cid: str | None = None
    kkday_affiliate_url_template: str | None = None
    kkday_allowed_hosts: str = "kkday.com,www.kkday.com"
    kkday_api_base_url: str | None = None
    kkday_api_key: str | None = None
    klook_enabled: bool = False
    klook_affiliate_url_template: str | None = None
    klook_allowed_hosts: str = "klook.com,www.klook.com"
    klook_api_base_url: str | None = None
    klook_api_key: str | None = None
    airalo_enabled: bool = False
    airalo_affiliate_url_template: str | None = None
    airalo_allowed_hosts: str = "airalo.com,www.airalo.com"
    trip_com_enabled: bool = False
    trip_com_affiliate_url_template: str | None = None
    trip_com_allowed_hosts: str = "trip.com,www.trip.com"
    agoda_enabled: bool = False
    agoda_cid: str | None = None
    agoda_affiliate_url_template: str | None = None
    agoda_allowed_hosts: str = "agoda.com,www.agoda.com"
    agoda_api_base_url: str | None = None
    agoda_api_key: str | None = None
    booking_enabled: bool = False
    booking_affiliate_id: str | None = None
    booking_affiliate_url_template: str | None = None
    booking_allowed_hosts: str = "booking.com,www.booking.com"
    booking_demand_api_base_url: str = "https://demandapi-sandbox.booking.com/3.1"
    booking_demand_enabled: bool = False
    booking_demand_env: str = "sandbox"
    booking_demand_affiliate_id: str | None = None
    booking_demand_api_token: str | None = None
    booking_booker_country: str = "tw"
    booking_language: str = "zh-tw"
    booking_location_cache_ttl_seconds: int = Field(default=2_592_000, ge=3_600, le=31_536_000)
    skyscanner_affiliate_enabled: bool = False
    skyscanner_affiliate_url_template: str | None = None
    skyscanner_affiliate_allowed_hosts: str = "skyscanner.net,www.skyscanner.net"
    google_maps_api_key: str | None = None
    next_public_google_maps_browser_key: str | None = None
    route_cache_ttl_seconds: int = Field(default=900, ge=60, le=86_400)
    navitime_api_base_url: str | None = None
    navitime_client_id: str | None = None
    navitime_api_key: str | None = None
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
    def admin_email_set(self) -> set[str]:
        return {email.strip().lower() for email in self.admin_emails.split(",") if email.strip()}

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
    def skyscanner_configured(self) -> bool:
        return bool(self.skyscanner_api_key)

    @property
    def duffel_configured(self) -> bool:
        return bool(self.duffel_access_token)

    @property
    def flightaware_configured(self) -> bool:
        return bool(self.flightaware_api_key)

    @property
    def google_travel_impact_configured(self) -> bool:
        return bool(self.google_travel_impact_api_key)

    @property
    def booking_demand_effective_affiliate_id(self) -> str | None:
        return self.booking_demand_affiliate_id or self.booking_affiliate_id

    @property
    def booking_demand_configured(self) -> bool:
        return bool(
            self.booking_demand_enabled
            and self.booking_demand_effective_affiliate_id
            and self.booking_demand_api_token
        )

    @property
    def production(self) -> bool:
        return self.app_env.lower() in {"production", "prod"}

    @property
    def navitime_configured(self) -> bool:
        return bool(
            self.navitime_api_base_url and self.navitime_client_id and self.navitime_api_key
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
