from functools import lru_cache
from typing import Literal
from urllib.parse import urlparse

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _is_explicit_https_origin(value: str) -> bool:
    parsed = urlparse(value)
    try:
        _ = parsed.port
    except ValueError:
        return False
    return bool(
        parsed.scheme == "https"
        and parsed.hostname
        and parsed.username is None
        and parsed.password is None
        and not parsed.path
        and not parsed.params
        and not parsed.query
        and not parsed.fragment
    )


def _host_allowed(hostname: str, allowed_hosts: set[str]) -> bool:
    """Match a host exactly, or by suffix for entries written as ``.example.com``."""
    return any(
        hostname == allowed or (allowed.startswith(".") and hostname.endswith(allowed))
        for allowed in allowed_hosts
    )


def _is_official_https_url(
    value: str,
    allowed_hosts: set[str],
    *,
    allow_query: bool = False,
) -> bool:
    parsed = urlparse(value)
    try:
        port = parsed.port
    except ValueError:
        return False
    return bool(
        parsed.scheme == "https"
        and _host_allowed((parsed.hostname or "").lower(), allowed_hosts)
        and parsed.username is None
        and parsed.password is None
        and port in (None, 443)
        and (allow_query or not parsed.query)
        and not parsed.fragment
    )


# Provider endpoints that carry a credential must stay on the vendor's official host, both
# when set from the environment and when edited from the administration panel.
OFFICIAL_PROVIDER_HOSTS: dict[str, frozenset[str]] = {
    "openai_api_base_url": frozenset({"api.openai.com"}),
    "anthropic_api_base_url": frozenset({"api.anthropic.com"}),
    "minimax_api_base_url": frozenset({"api.minimaxi.com", "api.minimax.io"}),
    "flightaware_base_url": frozenset({"aeroapi.flightaware.com"}),
    "skyscanner_base_url": frozenset({"partners.api.skyscanner.net"}),
    "duffel_base_url": frozenset({"api.duffel.com"}),
    "google_travel_impact_base_url": frozenset({"travelimpactmodel.googleapis.com"}),
    "travelpayouts_api_base_url": frozenset({"api.travelpayouts.com"}),
    "hotspot_guide_gemini_base_url": frozenset({"generativelanguage.googleapis.com"}),
    "line_api_base_url": frozenset({"api.line.me"}),
    # NAVITIME serves the same API 2.0 contract through its RapidAPI listing and, for
    # direct contracts, gateway hosts under its own domains.
    "navitime_api_base_url": frozenset(
        {"navitime-route-totalnavi.p.rapidapi.com", ".navitime.co.jp", ".navitime.biz"}
    ),
    "ekispert_api_base_url": frozenset({"api.ekispert.jp"}),
    "odsay_api_base_url": frozenset({"api.odsay.com"}),
}


def official_provider_url_ok(field: str, value: str | None) -> bool:
    """Return True unless ``field`` is host-pinned and ``value`` leaves the official host."""
    allowed = OFFICIAL_PROVIDER_HOSTS.get(field)
    if allowed is None or not value:
        return True
    return _is_official_https_url(value, set(allowed))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")

    app_env: str = "development"
    app_secret_key: str = "development-secret-change-me-please-32"
    settings_encryption_key: str | None = None
    admin_emails: str = ""
    deployments_enabled: bool = False
    deploy_admin_emails: str = ""
    deploy_agent_socket: str = "/run/travel-scanner-deployer/deployer.sock"
    deploy_agent_hmac_key: str | None = None
    deploy_agent_timeout_seconds: float = Field(default=10.0, gt=0, le=30)
    deploy_cooldown_seconds: int = Field(default=300, ge=0, le=3_600)
    database_url: str = "postgresql+asyncpg://travel:travel@localhost:5432/travel_scanner"
    redis_url: str = "redis://localhost:6379/0"
    api_cors_origins: str = "http://localhost:3000"
    access_token_expire_minutes: int = Field(default=60, ge=5, le=1440)
    # Cookie sessions renew on activity once past half their lifetime, but
    # never beyond this many days after the original sign-in.
    session_absolute_max_days: int = Field(default=30, ge=1, le=365)
    cookie_secure: bool = False
    offer_cache_ttl_seconds: int = 300
    reference_cache_ttl_seconds: int = 86_400
    provider_timeout_seconds: float = 3.0
    provider_failure_threshold: int = 3
    provider_circuit_seconds: int = 60
    # A stay-area hotel search is up to three sequential Booking round trips, so it
    # gets its own budget instead of the per-module search timeout.
    hotel_area_search_timeout_seconds: float = Field(default=8.0, gt=0, le=30)
    rate_limit_per_minute: int = Field(default=120, ge=1)
    api_max_request_bytes: int = Field(default=5_242_880, ge=65_536, le=52_428_800)
    analytics_enabled: bool = False
    ga4_enabled: bool = False
    ga4_measurement_id: str | None = None
    analytics_trust_country_header: bool = False
    analytics_event_ip_limit: int = Field(default=120, ge=10, le=10_000)
    analytics_event_session_limit: int = Field(default=60, ge=10, le=10_000)
    analytics_retention_days: int = Field(default=90, ge=30, le=365)
    analytics_rollup_retention_months: int = Field(default=25, ge=13, le=60)
    analytics_scheduler_interval_seconds: int = Field(default=3_600, ge=300, le=86_400)
    auth_login_account_limit: int = Field(default=10, ge=1, le=100)
    auth_login_ip_limit: int = Field(default=30, ge=1, le=1_000)
    auth_login_window_seconds: int = Field(default=900, ge=60, le=86_400)
    auth_register_ip_limit: int = Field(default=30, ge=1, le=1_000)
    auth_register_window_seconds: int = Field(default=3_600, ge=60, le=86_400)
    auth_oauth_flow_ttl_seconds: int = Field(default=600, ge=300, le=1_800)
    auth_oauth_ip_limit: int = Field(default=30, ge=1, le=1_000)
    auth_google_enabled: bool = False
    auth_google_client_id: str | None = None
    auth_google_client_secret: str | None = None
    auth_line_enabled: bool = False
    auth_line_channel_id: str | None = None
    auth_line_channel_secret: str | None = None
    auth_apple_enabled: bool = False
    auth_apple_services_id: str | None = None
    auth_apple_team_id: str | None = None
    auth_apple_key_id: str | None = None
    auth_apple_private_key: str | None = None
    registration_enabled: bool = True
    hotspots_enabled: bool = True
    trips_enabled: bool = True
    alerts_enabled: bool = True
    flight_status_enabled: bool = True
    airline_fares_enabled: bool = True
    pricing_enabled: bool = True
    trust_proxy_client_ip: bool = False
    ai_planner_enabled: bool = True
    ai_planner_mode: str = "auto"
    ai_planner_priority: str = "openai,anthropic,minimax"
    ai_planner_timeout_seconds: float = Field(default=15.0, gt=0, le=60)
    ai_planner_total_timeout_seconds: float = Field(default=35.0, gt=0, le=120)
    ai_planner_max_output_tokens: int = Field(default=12_000, ge=1_000, le=32_000)
    openai_api_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-5.6-terra"
    openai_api_key: str | None = None
    anthropic_api_base_url: str = "https://api.anthropic.com/v1"
    anthropic_model: str = "claude-sonnet-5"
    anthropic_api_key: str | None = None
    minimax_api_base_url: str = "https://api.minimaxi.com/v1"
    minimax_model: str = "MiniMax-M3"
    minimax_api_key: str | None = None
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
    travelpayouts_connectivity_target_url: str | None = None
    travelpayouts_allowed_hosts: str = "tp.st,travelpayouts.com,tp.media"
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
    google_maps_javascript_enabled: bool = False
    google_maps_monthly_request_limit: int = Field(default=10_000, ge=1, le=10_000_000)
    google_maps_essentials_free_limit: int = Field(default=10_000, ge=1, le=10_000_000)
    google_maps_pro_free_limit: int = Field(default=5_000, ge=1, le=10_000_000)
    google_maps_enterprise_free_limit: int = Field(default=1_000, ge=1, le=10_000_000)
    restaurant_scan_enabled: bool = True
    restaurant_aggregate_monthly_budget: int = Field(default=4_000, ge=1, le=10_000_000)
    restaurant_nearby_monthly_budget: int = Field(default=800, ge=1, le=10_000_000)
    restaurant_details_monthly_budget: int = Field(default=800, ge=1, le=10_000_000)
    restaurant_scan_refresh_days: int = Field(default=90, ge=7, le=365)
    restaurant_scan_max_depth: int = Field(default=7, ge=1, le=8)
    restaurant_scan_batch_call_limit: int = Field(default=50, ge=1, le=1_000)
    restaurant_location_cache_days: int = Field(default=30, ge=1, le=30)
    naver_maps_client_id: str | None = None
    naver_maps_client_secret: str | None = None
    naver_maps_monthly_request_limit: int = Field(default=0, ge=0, le=10_000_000)
    naver_place_cache_ttl_seconds: int = Field(default=900, ge=60, le=86_400)
    place_photo_ip_limit: int = Field(default=120, ge=1, le=10_000)
    place_photo_window_seconds: int = Field(default=60, ge=10, le=3_600)
    place_photo_cache_ttl_seconds: int = Field(default=3_600, ge=60, le=86_400)
    route_cache_ttl_seconds: int = Field(default=900, ge=60, le=86_400)
    weather_cache_ttl_seconds: int = Field(default=900, ge=300, le=3_600)
    navitime_api_base_url: str | None = None
    navitime_client_id: str | None = None
    navitime_api_key: str | None = None
    # Calendar-month cap on outbound NAVITIME requests; 0 counts without blocking.
    navitime_monthly_request_limit: int = Field(default=450, ge=0, le=10_000_000)
    ekispert_api_base_url: str = "https://api.ekispert.jp"
    ekispert_api_key: str | None = None
    # ``plain`` uses average waiting times and is available on the lower-cost plan.
    # ``departure`` requires an Ekispert contract with timetable search enabled.
    ekispert_search_type: Literal["plain", "departure"] = "plain"
    ekispert_monthly_request_limit: int = Field(default=450, ge=0, le=10_000_000)
    odsay_api_base_url: str = "https://api.odsay.com/v1/api"
    odsay_api_key: str | None = None
    # Standard contracts may only include Korean; multilingual output depends on the plan.
    odsay_language: Literal["0", "1", "2", "3", "4"] = "0"
    # The free Basic tier allows 30 calls/day; keep five calls for connection checks.
    odsay_daily_request_limit: int = Field(default=25, ge=0, le=10_000_000)
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
    hotspot_collection_enabled: bool = True
    hotspot_collection_interval_seconds: int = Field(default=21_600, ge=300, le=604_800)
    hotspot_guide_backfill_enabled: bool = False
    hotspot_guide_backfill_batch_size: int = Field(default=10, ge=1, le=100)
    hotspot_guide_backfill_locale: str = "zh-TW"
    hotspot_wikimedia_enabled: bool = True
    hotspot_wikimedia_user_agent: str = (
        "TravelScannerBot/0.1 (+https://github.com/x812033727/travel_scanner)"
    )
    hotspot_wikimedia_timeout_seconds: float = Field(default=10.0, gt=0, le=30)
    hotspot_wikimedia_max_retries: int = Field(default=3, ge=0, le=5)
    hotspot_wikimedia_retry_backoff_seconds: float = Field(default=1.0, gt=0, le=10)
    hotspot_discovery_enabled: bool = True
    hotspot_discovery_interval_seconds: int = Field(default=604_800, ge=86_400)
    hotspot_discovery_candidate_limit: int = Field(default=100, ge=20, le=100)
    hotspot_discovery_pageview_limit: int = Field(default=30, ge=10, le=50)
    hotspot_discovery_concurrency: int = Field(default=3, ge=1, le=3)
    hotspot_place_enrichment_enabled: bool = True
    hotspot_place_refresh_after_days: int = Field(default=21, ge=1, le=29)
    hotspot_place_cache_days: int = Field(default=30, ge=2, le=30)
    hotspot_place_refresh_batch_size: int = Field(default=20, ge=1, le=100)
    hotspot_guides_enabled: bool = True
    hotspot_guide_youtube_enabled: bool = True
    hotspot_guide_brave_enabled: bool = True
    hotspot_guide_youtube_api_key: str | None = None
    hotspot_guide_brave_api_key: str | None = None
    hotspot_guide_youtube_daily_search_budget: int = Field(default=80, ge=1, le=80)
    hotspot_guide_youtube_search_daily_free_limit: int = Field(default=100, ge=1, le=1_000_000)
    hotspot_guide_youtube_core_daily_free_limit: int = Field(default=10_000, ge=1, le=10_000_000)
    hotspot_guide_brave_daily_search_budget: int = Field(default=30, ge=1, le=1000)
    # Gemini finds articles through Google Search grounding. Grounding cannot be combined
    # with a response schema, so this provider takes URLs from grounding metadata only and
    # never from model text; scoring stays with the existing structured assessment step.
    hotspot_guide_gemini_enabled: bool = False
    hotspot_guide_gemini_api_key: str | None = None
    hotspot_guide_gemini_base_url: str = "https://generativelanguage.googleapis.com"
    # Flash-tier models refuse "list these sources" prompts outright; a Pro-tier model is
    # what actually returns grounded results. Admin-changeable if that shifts.
    hotspot_guide_gemini_model: str = "gemini-2.5-pro"
    hotspot_guide_gemini_timeout_seconds: float = Field(default=45.0, gt=0, le=120)
    hotspot_guide_gemini_daily_search_budget: int = Field(default=30, ge=1, le=1000)
    hotspot_guide_refresh_days: int = Field(default=7, ge=1, le=30)
    hotspot_guide_ai_search_enabled: bool = True
    hotspot_guide_ai_default_provider: Literal["minimax", "openai", "anthropic"] = "minimax"
    hotspot_guide_ai_timeout_seconds: float = Field(default=90.0, gt=0, le=120)
    hotspot_guide_ai_max_output_tokens: int = Field(default=16_000, ge=1_000, le=32_000)
    hotspot_guide_ai_daily_run_limit: int = Field(default=10, ge=1, le=100)
    hotspot_guide_ai_daily_call_budget: int = Field(default=60, ge=1, le=500)
    line_messaging_enabled: bool = False
    line_channel_secret: str | None = None
    line_channel_access_token: str | None = None
    line_official_account_id: str | None = None
    line_add_friend_url: str | None = None
    line_api_base_url: str = "https://api.line.me"
    line_webhook_max_body_bytes: int = Field(default=1_048_576, ge=1_024, le=5_242_880)
    price_alert_check_interval_seconds: int = Field(default=21_600, ge=3_600, le=86_400)
    price_alert_scheduler_poll_seconds: int = Field(default=60, ge=15, le=300)
    price_alert_delivery_max_attempts: int = Field(default=5, ge=1, le=10)
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
    def deploy_admin_email_set(self) -> set[str]:
        return {
            email.strip().lower() for email in self.deploy_admin_emails.split(",") if email.strip()
        }

    @property
    def deployments_configured(self) -> bool:
        return bool(
            self.deployments_enabled
            and self.deploy_admin_email_set
            and self.deploy_agent_hmac_key
            and len(self.deploy_agent_hmac_key) >= 32
            and self.deploy_agent_socket.startswith("/")
        )

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
    def navitime_rapidapi(self) -> bool:
        """True when the NAVITIME base URL points at the RapidAPI gateway."""
        host = (urlparse(self.navitime_api_base_url or "").hostname or "").lower()
        return host.endswith(".p.rapidapi.com")

    @property
    def navitime_configured(self) -> bool:
        # RapidAPI authenticates with the key alone; direct contracts also need the
        # client ID that forms part of the request path.
        if not (self.navitime_api_base_url and self.navitime_api_key):
            return False
        return self.navitime_rapidapi or bool(self.navitime_client_id)

    @property
    def ekispert_configured(self) -> bool:
        return bool(self.ekispert_api_key and self.ekispert_api_base_url)

    @property
    def odsay_configured(self) -> bool:
        return bool(self.odsay_api_key and self.odsay_api_base_url)

    @property
    def naver_maps_configured(self) -> bool:
        return bool(self.naver_maps_client_id and self.naver_maps_client_secret)

    @property
    def line_messaging_configured(self) -> bool:
        return bool(
            self.line_messaging_enabled
            and self.line_channel_secret
            and self.line_channel_access_token
            and self.line_official_account_id
        )

    def validate_deployment_security(self) -> None:
        if not self.production:
            return
        errors: list[str] = []
        insecure_app_secrets = {
            "development-secret-change-me-please-32",
            "replace-with-at-least-32-random-characters",
        }
        if len(self.app_secret_key) < 32 or self.app_secret_key in insecure_app_secrets:
            errors.append("APP_SECRET_KEY must be a unique random value of at least 32 characters")
        if not self.settings_encryption_key or len(self.settings_encryption_key) < 32:
            errors.append("SETTINGS_ENCRYPTION_KEY must be set to at least 32 characters")
        elif self.settings_encryption_key == self.app_secret_key:
            errors.append("SETTINGS_ENCRYPTION_KEY must differ from APP_SECRET_KEY")
        if not self.cookie_secure:
            errors.append("COOKIE_SECURE must be true")
        if not _is_explicit_https_origin(self.next_public_site_url):
            errors.append("NEXT_PUBLIC_SITE_URL must be an HTTPS origin")
        for origin in self.cors_origins:
            if origin == "*" or not _is_explicit_https_origin(origin):
                errors.append("API_CORS_ORIGINS must contain only explicit HTTPS origins")
                break
        database = urlparse(self.database_url)
        if not database.password or database.password == "travel":
            errors.append("DATABASE_URL must use a non-default password")
        redis = urlparse(self.redis_url)
        if not redis.password:
            errors.append("REDIS_URL must include a password")
        if self.line_messaging_enabled and not self.line_messaging_configured:
            errors.append(
                "LINE messaging requires LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN, "
                "and LINE_OFFICIAL_ACCOUNT_ID"
            )
        if self.deployments_enabled:
            if not self.deploy_admin_email_set:
                errors.append("DEPLOY_ADMIN_EMAILS must contain at least one email")
            if not self.deploy_agent_hmac_key or len(self.deploy_agent_hmac_key) < 32:
                errors.append("DEPLOY_AGENT_HMAC_KEY must be set to at least 32 characters")
            if not self.deploy_agent_socket.startswith("/"):
                errors.append("DEPLOY_AGENT_SOCKET must be an absolute Unix socket path")
        pinned_endpoints = {
            "OPENAI_API_BASE_URL": (self.openai_api_key, "openai_api_base_url"),
            "ANTHROPIC_API_BASE_URL": (self.anthropic_api_key, "anthropic_api_base_url"),
            "MINIMAX_API_BASE_URL": (self.minimax_api_key, "minimax_api_base_url"),
            "FLIGHTAWARE_BASE_URL": (self.flightaware_api_key, "flightaware_base_url"),
            "SKYSCANNER_BASE_URL": (self.skyscanner_api_key, "skyscanner_base_url"),
            "DUFFEL_BASE_URL": (self.duffel_access_token, "duffel_base_url"),
            "GOOGLE_TRAVEL_IMPACT_BASE_URL": (
                self.google_travel_impact_api_key,
                "google_travel_impact_base_url",
            ),
            "NAVITIME_API_BASE_URL": (self.navitime_api_key, "navitime_api_base_url"),
            "EKISPERT_API_BASE_URL": (self.ekispert_api_key, "ekispert_api_base_url"),
            "ODSAY_API_BASE_URL": (self.odsay_api_key, "odsay_api_base_url"),
            "TRAVELPAYOUTS_API_BASE_URL": (
                self.travelpayouts_api_token if self.travelpayouts_enabled else None,
                "travelpayouts_api_base_url",
            ),
        }
        for env_name, (credential, field) in pinned_endpoints.items():
            if credential and not official_provider_url_ok(field, getattr(self, field)):
                errors.append(f"{env_name} must use an official HTTPS API endpoint")
        if self.line_messaging_enabled and not _is_official_https_url(
            self.line_api_base_url, {"api.line.me"}
        ):
            errors.append("LINE_API_BASE_URL must use the official HTTPS API endpoint")
        if self.line_add_friend_url and not _is_official_https_url(
            self.line_add_friend_url,
            {"line.me", "www.line.me", "lin.ee"},
            allow_query=True,
        ):
            errors.append("LINE_ADD_FRIEND_URL must use an official LINE HTTPS domain")
        if errors:
            raise RuntimeError("Unsafe production configuration: " + "; ".join(errors))

    def validate_api_serving_security(self) -> None:
        """Checks that only matter for the HTTP API process, not for workers or the CLI."""
        errors: list[str] = []
        if any(origin == "*" for origin in self.cors_origins):
            errors.append(
                "API_CORS_ORIGINS must not contain '*' because credentials are allowed cross-origin"
            )
        if self.production and not self.trust_proxy_client_ip:
            errors.append(
                "TRUST_PROXY_CLIENT_IP must be true in production because the web BFF is the "
                "only API caller and per-client rate limits depend on the forwarded address"
            )
        if errors:
            raise RuntimeError("Unsafe API configuration: " + "; ".join(errors))


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.validate_deployment_security()
    return settings
