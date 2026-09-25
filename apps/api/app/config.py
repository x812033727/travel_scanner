import hashlib
import hmac
from functools import lru_cache
from typing import Literal
from urllib.parse import urlparse

from pydantic import Field, field_validator
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
    "jev_api_base_url": frozenset({"api.typesafe.ai"}),
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
    # A placeholder, and the one value production refuses by name:
    # `validate_deployment_security` rejects it and anything under 32 characters.
    app_secret_key: str = "development-secret-change-me-please-32"  # noqa: S105
    settings_encryption_key: str | None = None
    admin_emails: str = ""
    community_enabled: bool = False
    discovery_enabled: bool = False
    community_s3_endpoint: str | None = None
    community_s3_public_endpoint: str | None = None
    community_s3_region: str = "us-east-1"
    community_s3_bucket: str = "mokaair-community"
    community_s3_access_key: str | None = None
    community_s3_secret_key: str | None = None
    community_smtp_host: str | None = None
    community_smtp_port: int = Field(default=587, ge=1, le=65535)
    community_smtp_starttls: bool = True
    community_smtp_username: str | None = None
    community_smtp_password: str | None = None
    community_mail_from: str = ""
    deployments_enabled: bool = False
    deploy_admin_emails: str = ""
    database_admin_emails: str = ""
    admin_database_maintenance_enabled: bool = False
    deploy_agent_socket: str = "/run/travel-scanner-deployer/deployer.sock"
    deploy_agent_hmac_key: str | None = None
    deploy_agent_timeout_seconds: float = Field(default=10.0, gt=0, le=30)
    deploy_cooldown_seconds: int = Field(default=300, ge=0, le=3_600)
    # /admin/ai-accounts: the host agent in ops/ai-accounts signs root's Claude Code and
    # Codex CLIs in to subscription accounts. The socket path is fixed by its systemd unit.
    ai_accounts_enabled: bool = False
    ai_accounts_agent_socket: str = "/run/mokaair-ai-accounts/agent.sock"
    ai_accounts_agent_hmac_key: str | None = None
    # Starting a login runs a CLI on the host; the web proxy allows 30 s for these routes.
    ai_accounts_agent_timeout_seconds: float = Field(default=25.0, gt=0, le=28)
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
    # Administrator overrides of the web UI copy are read on every page render, so each
    # locale's payload is cached in Redis. Every write deletes the cache; this TTL only
    # bounds how long a stale copy survives a missed invalidation.
    ui_text_cache_ttl_seconds: int = Field(default=300, ge=5, le=86_400)
    provider_timeout_seconds: float = 3.0
    provider_failure_threshold: int = 3
    provider_circuit_seconds: int = 60
    # A stay-area hotel search is up to three sequential Booking round trips, so it
    # gets its own budget instead of the per-module search timeout.
    hotel_area_search_timeout_seconds: float = Field(default=8.0, gt=0, le=30)
    rate_limit_per_minute: int = Field(default=120, ge=1)
    api_max_request_bytes: int = Field(default=5_242_880, ge=65_536, le=52_428_800)
    # The public catalogue is meant to be read, including by search engines, so this
    # bounds how fast one source may read it rather than deciding who may. It ships in
    # "observe" -- counted and logged, never refused -- because the number that stops a
    # scraper and the number that stops an office behind one NAT address are not known
    # to be far apart until real traffic has been measured. Move to "enforce" on
    # evidence, not on principle.
    public_read_rate_limit_mode: Literal["off", "observe", "enforce"] = "observe"
    public_read_ip_limit: int = Field(default=180, ge=10, le=100_000)
    public_read_ip_window_seconds: int = Field(default=60, ge=10, le=3_600)
    # The second window catches what the first cannot: a crawler polite enough to stay
    # under the per-minute burst all day still empties the catalogue.
    public_read_ip_hour_limit: int = Field(default=2_400, ge=60, le=1_000_000)
    analytics_enabled: bool = False
    ga4_enabled: bool = False
    ga4_measurement_id: str | None = None
    analytics_trust_country_header: bool = False
    analytics_event_ip_limit: int = Field(default=120, ge=10, le=10_000)
    analytics_event_session_limit: int = Field(default=60, ge=10, le=10_000)
    analytics_retention_days: int = Field(default=90, ge=30, le=365)
    analytics_rollup_retention_months: int = Field(default=25, ge=13, le=60)
    analytics_scheduler_interval_seconds: int = Field(default=3_600, ge=300, le=86_400)
    # Display advertising on article pages. Off until the owner has an approved AdSense
    # account and has filled both IDs in: the public endpoint reports "off" unless every
    # one of these is set and valid, so a half-filled card never reaches a reader.
    adsense_enabled: bool = False
    adsense_publisher_id: str | None = None
    adsense_slot_id: str | None = None
    # True asserts that a Google-certified consent message is published in the AdSense back
    # office. It is the owner stating a fact about that account; the code derives behaviour
    # from it — without it the loader forces non-personalised ads, because personalised ads
    # in the EEA, the UK or Switzerland require a certified CMP.
    adsense_cmp_enabled: bool = False
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
    # Proof that a forwarded address came from our own BFF rather than from something else
    # that can reach this API. Nothing at the network layer can tell those apart: neither
    # Compose file declares `networks:`, so every container shares one bridge with addresses
    # that change on each restart, and "the Compose subnet" is precisely the set we would be
    # trying to exclude. Empty means the address is believed on `trust_proxy_client_ip`
    # alone -- the previous behaviour, kept as the default because a token set on the API but
    # not on the web container would collapse every visitor into one rate-limit bucket, which
    # is an outage rather than a defence.
    internal_proxy_token: str = ""
    ai_planner_enabled: bool = True
    ai_planner_mode: str = "auto"
    ai_planner_priority: str = "openai,anthropic,minimax,gemini"
    ai_planner_timeout_seconds: float = Field(default=15.0, gt=0, le=60)
    ai_planner_total_timeout_seconds: float = Field(default=35.0, gt=0, le=120)
    ai_planner_max_output_tokens: int = Field(default=12_000, ge=1_000, le=32_000)
    # One account's share of the planner's provider bill. Spent, planning falls back to the
    # reviewed catalogue rather than refusing: the itinerary still arrives, it just stops
    # costing per call, and the traveller is told which of the two happened.
    #
    # Counted per attempt on the roster and never refunded, which is the part that bounds a
    # caller who can provoke a failure. The fair-use limiters beside it do give their slot
    # back on a real outage, and should -- but a budget that can be handed back is not a
    # ceiling. Deliberately looser than any of them, so it binds an abuser and not a
    # traveller having an intense afternoon.
    ai_planner_user_budget: int = Field(default=40, ge=1, le=1_000)
    # Per address as well, because an account costs nothing to mint: /auth/register hands
    # back a token immediately, and AUTH_REGISTER_IP_LIMIT lets thirty through an hour. Per
    # account alone, that is thirty times the budget above from one machine. Set well clear
    # of the per-account number so a household, an office or a carrier NAT never meets it.
    ai_planner_ip_budget: int = Field(default=120, ge=1, le=10_000)
    ai_planner_user_budget_window_seconds: int = Field(default=3_600, ge=60, le=86_400)
    openai_api_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-6-sol"
    openai_api_key: str | None = None
    anthropic_api_base_url: str = "https://api.anthropic.com/v1"
    anthropic_model: str = "claude-sonnet-5"
    anthropic_api_key: str | None = None
    minimax_api_base_url: str = "https://api.minimaxi.com/v1"
    minimax_model: str = "MiniMax-M3"
    # Gemini shares the key and base URL of the article search (hotspot_guide_gemini_*);
    # this is the model the planner and the trip parser use.
    gemini_model: str = "gemini-3.8-flash"
    minimax_api_key: str | None = None
    # Jev is TypeSafe's System One model. It decides -- choice, score, noul -- and never
    # generates text, so it is not an AI_PLANNER_PRIORITY vendor and never a planner
    # fallback; it lives here only because its key belongs on the same encrypted card.
    jev_api_base_url: str = "https://api.typesafe.ai/v1"
    # The vendor ships the `jev-latest` alias and then tells you to pin a version in
    # production. Every other model id in this file is pinned; so is this one.
    jev_model: str = "jev-1.13.0"
    jev_api_key: str | None = None
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
    klook_affiliate_id: str | None = Field(default=None, pattern=r"^[1-9][0-9]{0,19}$")
    klook_affiliate_url_template: str | None = None
    klook_allowed_hosts: str = "klook.com,www.klook.com"
    klook_api_base_url: str | None = None
    klook_api_key: str | None = None

    @field_validator("klook_affiliate_id", mode="before")
    @classmethod
    def empty_klook_aid(cls, value: object) -> object:
        return None if value == "" else value

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
    # Redis cache for provider route results, shared across trips; see
    # RouteService._cache_time_key for how departure times are bucketed.
    route_cache_ttl_seconds: int = Field(default=86_400, ge=60, le=86_400)
    # How long an applied provider route stays valid in trip_route_segments before the
    # planner shows it as stale. Manual routes never expire, and itinerary edits delete
    # the affected pairs directly, so this only guards against very old timetables.
    route_segment_ttl_seconds: int = Field(default=30 * 86_400, ge=3_600, le=180 * 86_400)
    weather_cache_ttl_seconds: int = Field(default=900, ge=300, le=3_600)
    # Trip weather: MET Norway is free for commercial use (CC BY 4.0) and only asks for
    # an identifying User-Agent; Google Weather stays available as the fallback.
    weather_provider: Literal["met_norway", "google"] = "met_norway"
    met_norway_base_url: str = "https://api.met.no"
    met_norway_user_agent: str = "Mokaair/1.0 (+https://mokaair.com)"
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
    airline_crawler_agent_token: str = "TravelScannerBot"  # noqa: S105 -- a User-Agent string
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
    # Flash-tier models refuse "list these sources" prompts on the grounded path, but
    # handle the schema-bound candidate list fine, and gemini-2.5-pro is closed to new
    # keys. Admin-changeable per install.
    hotspot_guide_gemini_model: str = "gemini-3.8-flash"
    hotspot_guide_gemini_timeout_seconds: float = Field(default=45.0, gt=0, le=120)
    hotspot_guide_gemini_daily_search_budget: int = Field(default=30, ge=1, le=1000)
    # Independent of the shared daily budget: this ceiling applies to the
    # cumulative provider calls within one catalog review run, including retries.
    catalog_review_max_calls: int = Field(default=80, ge=1, le=1000)

    @field_validator("catalog_review_max_calls", mode="before")
    @classmethod
    def catalog_review_calls_integer(cls, value: object) -> object:
        # Environment values arrive as strings, but booleans and floats must
        # never be coerced into a spending limit.
        if isinstance(value, str):
            value = value.strip()
            if value.isascii() and value.isdigit():
                return value
        elif isinstance(value, int) and not isinstance(value, bool):
            return value
        raise ValueError("catalog_review_max_calls must be an integer")

    hotspot_guide_refresh_days: int = Field(default=7, ge=1, le=30)
    hotspot_guide_ai_search_enabled: bool = True
    hotspot_guide_ai_default_provider: Literal["minimax", "openai", "anthropic", "gemini"] = (
        "minimax"
    )
    # Per-vendor model for AI guide search; empty means the planner's <vendor>_model.
    hotspot_guide_ai_openai_model: str | None = None
    hotspot_guide_ai_anthropic_model: str | None = None
    hotspot_guide_ai_minimax_model: str | None = None
    hotspot_guide_ai_gemini_model: str | None = None
    hotspot_guide_ai_timeout_seconds: float = Field(default=90.0, gt=0, le=120)
    hotspot_guide_ai_max_output_tokens: int = Field(default=16_000, ge=1_000, le=32_000)
    hotspot_guide_ai_daily_run_limit: int = Field(default=10, ge=1, le=100)
    hotspot_guide_ai_daily_call_budget: int = Field(default=60, ge=1, le=500)
    # Writing a first-party introduction is a different job from searching for
    # somebody else's article, so it gets its own vendor, model and budget.
    hotspot_intro_ai_enabled: bool = True
    hotspot_intro_ai_default_provider: Literal["minimax", "openai", "anthropic", "gemini"] = (
        "minimax"
    )
    hotspot_intro_ai_openai_model: str | None = None
    hotspot_intro_ai_anthropic_model: str | None = None
    hotspot_intro_ai_minimax_model: str | None = None
    hotspot_intro_ai_gemini_model: str | None = None
    hotspot_intro_ai_timeout_seconds: float = Field(default=90.0, gt=0, le=120)
    hotspot_intro_ai_max_output_tokens: int = Field(default=8_000, ge=1_000, le=32_000)
    hotspot_intro_ai_daily_run_limit: int = Field(default=20, ge=1, le=200)
    hotspot_intro_ai_daily_call_budget: int = Field(default=200, ge=1, le=2_000)
    # Jev decision budgets. A System One call returns no prose, so a slow one is a
    # signal rather than a long answer being written: 20s, not the planner's 90.
    jev_timeout_seconds: float = Field(default=20.0, gt=0, le=60)
    jev_daily_call_budget: int = Field(default=200, ge=1, le=5_000)
    # The vendor caps a request at 64k tokens, and state plus the longest single
    # question at 32k. These sit under both, so a batch splits on our own estimate
    # instead of on a 422 from the far side.
    jev_max_state_tokens: int = Field(default=24_000, ge=1_000, le=32_000)
    jev_max_request_tokens: int = Field(default=56_000, ge=2_000, le=64_000)
    # The vendor's own example thresholds, and placeholders until shadow-mode numbers
    # from our own data replace them. Above `act` the answer may be acted on; between
    # the two it is flagged for review; below `flag` nothing happens.
    jev_act_confidence: float = Field(default=0.9, ge=0, le=1)
    jev_flag_confidence: float = Field(default=0.5, ge=0, le=1)
    # TypeSafe says accuracy is best in English and asks you to validate on your own
    # Traditional Chinese data before setting automation thresholds. This product is
    # five-language, so that warning is a default-closed switch rather than a
    # paragraph in a README: while it is off, a confident answer about non-English
    # state is downgraded from "act" to "confirm" instead of acting on its own.
    jev_cjk_autopilot_enabled: bool = False
    # The first Jev consumer, shipped measuring rather than deciding. "shadow" asks Jev
    # the same question the guide assessor is already answering and records both, while
    # the existing relevance threshold still decides every accept. An "enforce" value
    # belongs here later; the enum exists now so adding it is not a type change. Same
    # reasoning as public_read_rate_limit_mode: move on evidence, not on principle.
    jev_shadow_guide_assessment: Literal["off", "shadow"] = "off"
    # Azure AI Speech narrates the YouTube videos the local pipeline in tools/video builds
    # (docs/videos/DESIGN.md). The key stays on this server: the pipeline sends sentences to
    # POST /api/v1/video/speech with a video tool token and gets audio back. The endpoint host
    # is built from the region, which is why the region is pattern-checked and no base URL is
    # stored.
    azure_speech_region: str | None = Field(default=None, pattern=r"^[a-z][a-z0-9]{1,31}$")
    azure_speech_key: str | None = None

    @field_validator("azure_speech_region", mode="before")
    @classmethod
    def empty_azure_speech_region(cls, value: object) -> object:
        # An empty AZURE_SPEECH_REGION= (as in .env.example) means "not set", not a bad region.
        if isinstance(value, str):
            return value.strip().lower() or None
        return value

    # Voices the pipeline may ask for: Taiwan Mandarin, and the multilingual voices that can
    # speak it through <lang xml:lang="zh-TW">.
    azure_speech_voices: str = (
        "zh-TW-HsiaoChenNeural,zh-TW-YunJheNeural,zh-TW-HsiaoYuNeural,"
        "en-US-AvaMultilingualNeural,en-US-AndrewMultilingualNeural,"
        "en-US-BrianMultilingualNeural,en-US-EmmaMultilingualNeural"
    )
    # Billable characters per UTC month; Azure counts a Chinese character twice and bills the
    # SSML markup too. 0 counts without blocking. The default stays under the free tier's
    # 500,000 so a month of videos cannot turn into a bill.
    azure_speech_monthly_character_limit: int = Field(default=450_000, ge=0, le=100_000_000)
    azure_speech_timeout_seconds: float = Field(default=90.0, ge=5, le=280)
    # Gemini narration uses the site's Gemini key (hotspot_guide_gemini_*). Its month counts
    # the text characters sent: 300,000 is about a hundred 10-minute videos, roughly US$13 at
    # the 2026 price of gemini-3.8-flash-tts.
    video_speech_gemini_monthly_character_limit: int = Field(
        default=300_000, ge=0, le=100_000_000
    )
    video_speech_gemini_timeout_seconds: float = Field(default=150.0, ge=5, le=280)
    # Previews the owner reviews on /admin/videos: a 720p cut, the narration, the contact sheet.
    # Production has no object storage, so they live in a volume on the host
    # (docker-compose.prod.yml) and are served to admins only.
    video_review_dir: str = "/var/lib/mokaair/video-reviews"
    video_review_max_file_bytes: int = Field(default=400_000_000, ge=1_000_000, le=4_000_000_000)
    video_review_max_total_bytes: int = Field(
        default=20_000_000_000, ge=10_000_000, le=500_000_000_000
    )
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
    # Currency-api (github.com/fawazahmed0/currency-api) publishes daily rates for 300+
    # currencies as static JSON on two CDNs; Frankfurter (ECB) is the last resort.
    fx_currency_api_base_url: str = (
        "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1"
    )
    fx_currency_api_fallback_url: str = "https://latest.currency-api.pages.dev/v1"
    fx_rate_base_url: str = "https://api.frankfurter.dev/v2"
    fx_rate_timeout_seconds: float = Field(default=3.0, gt=0, le=10)
    fx_rate_cache_ttl_seconds: int = Field(default=86_400, ge=300, le=86_400)
    fx_rate_stale_ttl_seconds: int = Field(default=604_800, ge=86_400, le=2_592_000)

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.api_cors_origins.split(",") if origin.strip()]

    @property
    def analytics_hash_key(self) -> bytes:
        """The key that pseudonymises analytics visitors, derived so it is not the signing key.

        Analytics used ``app_secret_key`` directly, which quietly coupled two things that
        need to move at different speeds. ``app_secret_key`` signs every access token and
        every admin step-up token, so it is the secret you most want to be able to rotate on
        an hour's notice — and doing that also re-keyed every ``visitor_day_hash`` and
        ``session_hash``, so returning visitors read as new and sessions split at the
        boundary, with nothing in the dashboard saying why. Paying for an emergency rotation
        in silently corrupted analytics is how a rotation gets postponed.

        Derived from ``settings_encryption_key``, which in production is required, at least
        32 characters, and different from ``app_secret_key`` (``validate_deployment_security``).
        Outside production that setting is optional, so the signing key is the fallback:
        development has one secret and no continuity to protect.

        One HMAC is the whole derivation, and that is enough here rather than a shortcut.
        HKDF's extract step exists to condense a non-uniform input and its expand step to
        produce more than one hash length of output; the input is already a high-entropy
        random secret and the output is a single 256-bit MAC key, so neither step applies.
        The label pins the purpose: the same secret used for anything else cannot land on
        this key by accident, and ``:v1`` is where a deliberate re-key would announce itself.
        """
        secret = self.settings_encryption_key or self.app_secret_key
        return hmac.new(secret.encode(), b"mokaair:analytics-hash-key:v1", hashlib.sha256).digest()

    @property
    def admin_email_set(self) -> set[str]:
        return {email.strip().lower() for email in self.admin_emails.split(",") if email.strip()}

    @property
    def deploy_admin_email_set(self) -> set[str]:
        return {
            email.strip().lower() for email in self.deploy_admin_emails.split(",") if email.strip()
        }

    @property
    def database_admin_email_set(self) -> set[str]:
        return {
            email.strip().lower()
            for email in self.database_admin_emails.split(",")
            if email.strip()
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
    def database_maintenance_configured(self) -> bool:
        return bool(
            self.admin_database_maintenance_enabled
            and self.database_admin_email_set
            and self.deploy_agent_hmac_key
            and len(self.deploy_agent_hmac_key) >= 32
            and self.deploy_agent_socket.startswith("/")
        )

    @property
    def ai_accounts_configured(self) -> bool:
        return bool(
            self.ai_accounts_enabled
            and self.ai_accounts_agent_hmac_key
            and len(self.ai_accounts_agent_hmac_key) >= 32
            and self.ai_accounts_agent_socket.startswith("/")
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
    def jev_configured(self) -> bool:
        return bool(self.jev_api_key and self.jev_api_base_url)

    @property
    def azure_speech_configured(self) -> bool:
        return bool(self.azure_speech_key and self.azure_speech_region)

    @property
    def azure_speech_voice_list(self) -> tuple[str, ...]:
        voices = (voice.strip() for voice in self.azure_speech_voices.split(","))
        return tuple(voice for voice in voices if voice)

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
        if not database.password or database.password == "travel":  # noqa: S105 -- refuses it
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
            if self.deploy_agent_socket != "/run/travel-scanner-deployer/deployer.sock":
                errors.append(
                    "DEPLOY_AGENT_SOCKET must use the systemd-managed "
                    "/run/travel-scanner-deployer/deployer.sock path"
                )
        if self.admin_database_maintenance_enabled:
            if not self.database_admin_email_set:
                errors.append("DATABASE_ADMIN_EMAILS must contain at least one email")
            if not self.deploy_agent_hmac_key or len(self.deploy_agent_hmac_key) < 32:
                errors.append("DEPLOY_AGENT_HMAC_KEY must be set to at least 32 characters")
            if self.deploy_agent_socket != "/run/travel-scanner-deployer/deployer.sock":
                errors.append(
                    "DEPLOY_AGENT_SOCKET must use the systemd-managed "
                    "/run/travel-scanner-deployer/deployer.sock path"
                )
        if self.ai_accounts_enabled:
            if not self.ai_accounts_agent_hmac_key or len(self.ai_accounts_agent_hmac_key) < 32:
                errors.append("AI_ACCOUNTS_AGENT_HMAC_KEY must be set to at least 32 characters")
            if self.ai_accounts_agent_socket != "/run/mokaair-ai-accounts/agent.sock":
                errors.append(
                    "AI_ACCOUNTS_AGENT_SOCKET must use the systemd-managed "
                    "/run/mokaair-ai-accounts/agent.sock path"
                )
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
            "JEV_API_BASE_URL": (self.jev_api_key, "jev_api_base_url"),
            "TRAVELPAYOUTS_API_BASE_URL": (
                self.travelpayouts_api_token if self.travelpayouts_enabled else None,
                "travelpayouts_api_base_url",
            ),
            "HOTSPOT_GUIDE_GEMINI_BASE_URL": (
                self.hotspot_guide_gemini_api_key,
                "hotspot_guide_gemini_base_url",
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
