from __future__ import annotations

import base64
import hashlib
import json
import logging
import re
import time
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime, timedelta
from typing import Any, cast
from urllib.parse import urlparse
from uuid import uuid4
from zoneinfo import ZoneInfo

import httpx
from cryptography.fernet import Fernet, InvalidToken
from pydantic import ValidationError
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.schemas import (
    AdminAuditView,
    ProviderSettingsSnapshot,
    ProviderSettingsUpdate,
    ProviderSettingsView,
    ProviderTestResult,
    ProviderUsageView,
    PublicRuntimeConfig,
    SecretState,
    SiteVisibility,
)
from app.ai.itinerary import AIItineraryPlanner, AIItineraryRequest
from app.config import (
    OFFICIAL_PROVIDER_HOSTS,
    Settings,
    get_settings,
    official_provider_url_ok,
)
from app.models import AdminAuditLog, ProviderConfig, ProviderRequest, User
from app.places.google import GoogleTravelService
from app.places.naver import NaverPlaceService
from app.problems import AppError
from app.providers.amadeus import AmadeusProvider
from app.providers.booking import BOOKING_API_HOSTS, BookingHotelProvider
from app.providers.duffel import DuffelProvider
from app.providers.flightaware import FlightAwareProvider
from app.providers.google_travel_impact import GoogleTravelImpactProvider
from app.providers.skyscanner import SkyscannerProvider
from app.providers.usage_meter import (
    ekispert_usage_snapshot,
    google_maps_usage_snapshot,
    naver_maps_usage_snapshot,
    navitime_usage_snapshot,
    odsay_usage_snapshot,
    youtube_usage_snapshot,
)
from app.search.schemas import SearchCreate, SearchModule, SearchPreferences, Travelers
from app.trips.routing import (
    EkispertRouteProvider,
    GoogleRouteProvider,
    NaverDirectionsProvider,
    NavitimeRouteProvider,
    OdsayRouteProvider,
    RoutePoint,
)
from app.weather.google import GoogleWeatherService

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProviderDefinition:
    label: str
    description: str
    config_fields: tuple[str, ...]
    secret_fields: tuple[str, ...]
    enabled_field: str | None = None


SITE_VISIBILITY_FIELDS = (
    "hotspots_enabled",
    "trips_enabled",
    "alerts_enabled",
    "flight_status_enabled",
    "airline_fares_enabled",
    "pricing_enabled",
)


PROVIDER_DEFINITIONS: dict[str, ProviderDefinition] = {
    "google_login": ProviderDefinition(
        "Google 登入",
        "使用 Google OpenID Connect 登入；callback 固定由正式網站網域產生。",
        ("auth_google_client_id", "auth_oauth_flow_ttl_seconds", "auth_oauth_ip_limit"),
        ("auth_google_client_secret",),
        "auth_google_enabled",
    ),
    "line_login": ProviderDefinition(
        "LINE 登入",
        "使用 LINE Login v2.1 與已核准的 Email scope 登入。",
        ("auth_line_channel_id",),
        ("auth_line_channel_secret",),
        "auth_line_enabled",
    ),
    "apple_login": ProviderDefinition(
        "Apple 登入",
        "使用 Sign in with Apple；Private Key 僅在伺服器端加密保存。",
        ("auth_apple_services_id", "auth_apple_team_id", "auth_apple_key_id"),
        ("auth_apple_private_key",),
        "auth_apple_enabled",
    ),
    "analytics": ProviderDefinition(
        "流量分析與 GA4",
        "第一方隱私分析與選配的 GA4 cookieless 事件；不保存原始 IP 或長期訪客 ID。",
        (
            "ga4_enabled",
            "ga4_measurement_id",
            "analytics_trust_country_header",
            "analytics_event_ip_limit",
            "analytics_event_session_limit",
            "analytics_retention_days",
            "analytics_rollup_retention_months",
        ),
        (),
        "analytics_enabled",
    ),
    "runtime": ProviderDefinition(
        "執行模式與保護設定",
        "控制公開註冊、即時／測試供應商選擇、逾時與重試斷路器。",
        (
            "registration_enabled",
            "travel_provider_mode",
            "flight_provider_mode",
            "flight_search_strategy",
            "flight_min_result_count",
            "hotel_provider_mode",
            "provider_timeout_seconds",
            "provider_failure_threshold",
            "provider_circuit_seconds",
        ),
        (),
    ),
    "layout": ProviderDefinition(
        "前台版面管理",
        "控制公開前台功能入口與頁面是否顯示；不會停用底層 API 或刪除資料。",
        SITE_VISIBILITY_FIELDS,
        (),
    ),
    "ai_planner": ProviderDefinition(
        "AI 行程規劃",
        "由後台選擇 OpenAI／ChatGPT、Claude、MiniMax 或內建備援，金鑰只在伺服器端加密保存。",
        (
            "ai_planner_mode",
            "ai_planner_priority",
            "ai_planner_timeout_seconds",
            "ai_planner_total_timeout_seconds",
            "ai_planner_max_output_tokens",
            "openai_api_base_url",
            "openai_model",
            "anthropic_api_base_url",
            "anthropic_model",
            "minimax_api_base_url",
            "minimax_model",
        ),
        ("openai_api_key", "anthropic_api_key", "minimax_api_key"),
        "ai_planner_enabled",
    ),
    "ai_guide_search": ProviderDefinition(
        "AI 景點介紹搜尋",
        "由 MiniMax、OpenAI 或 Claude 規劃與評選多語搜尋；網址只接受 Brave 與 YouTube。",
        (
            "hotspot_guide_ai_default_provider",
            "hotspot_guide_ai_timeout_seconds",
            "hotspot_guide_ai_max_output_tokens",
            "hotspot_guide_ai_daily_run_limit",
            "hotspot_guide_ai_daily_call_budget",
        ),
        (),
        "hotspot_guide_ai_search_enabled",
    ),
    "google_maps": ProviderDefinition(
        "Google Maps",
        "Google Places 地點搜尋、Routes 路線（日本大眾運輸除外）、Weather 天氣與瀏覽器地圖。",
        (
            "route_cache_ttl_seconds",
            "weather_cache_ttl_seconds",
            "google_maps_javascript_enabled",
            "google_maps_essentials_free_limit",
            "google_maps_pro_free_limit",
            "google_maps_enterprise_free_limit",
            "restaurant_scan_enabled",
            "restaurant_aggregate_monthly_budget",
            "restaurant_nearby_monthly_budget",
            "restaurant_details_monthly_budget",
            "restaurant_scan_refresh_days",
            "restaurant_scan_max_depth",
            "restaurant_scan_batch_call_limit",
            "restaurant_location_cache_days",
        ),
        ("google_maps_api_key", "next_public_google_maps_browser_key"),
    ),
    "naver_maps": ProviderDefinition(
        "NAVER Maps",
        "韓國地點搜尋、地址解析、Dynamic Map 與汽車路線；大眾運輸維持外部導航。",
        (
            "route_cache_ttl_seconds",
            "naver_place_cache_ttl_seconds",
            "naver_maps_monthly_request_limit",
        ),
        ("naver_maps_client_id", "naver_maps_client_secret"),
    ),
    "youtube_guides": ProviderDefinition(
        "YouTube 景點介紹",
        "依景點與目前語系探索 YouTube 影片；候選必須經管理員核准才公開。",
        (
            "hotspot_guide_youtube_daily_search_budget",
            "hotspot_guide_youtube_search_daily_free_limit",
            "hotspot_guide_youtube_core_daily_free_limit",
            "hotspot_guide_refresh_days",
        ),
        ("hotspot_guide_youtube_api_key",),
        "hotspot_guide_youtube_enabled",
    ),
    "brave_guides": ProviderDefinition(
        "Brave 多語文章搜尋",
        "依景點與目前語系探索公開旅遊文章；只保存搜尋結果允許的摘要資料。",
        ("hotspot_guide_brave_daily_search_budget", "hotspot_guide_refresh_days"),
        ("hotspot_guide_brave_api_key",),
        "hotspot_guide_brave_enabled",
    ),
    "gemini_guides": ProviderDefinition(
        "Gemini 多語文章搜尋",
        "以 Google 搜尋接地尋找各語系旅遊文章；連結只取自來源標註，不採用模型寫出的網址。",
        (
            "hotspot_guide_gemini_base_url",
            "hotspot_guide_gemini_model",
            "hotspot_guide_gemini_timeout_seconds",
            "hotspot_guide_gemini_daily_search_budget",
        ),
        ("hotspot_guide_gemini_api_key",),
        "hotspot_guide_gemini_enabled",
    ),
    "amadeus": ProviderDefinition(
        "Amadeus",
        "航班、飯店、活動與機場接送；可切換 Self-Service test 或 production。",
        ("amadeus_env",),
        ("amadeus_client_id", "amadeus_client_secret"),
    ),
    "skyscanner": ProviderDefinition(
        "Skyscanner",
        "合作夥伴即時航班搜尋與彈性日期結果。",
        (
            "skyscanner_base_url",
            "skyscanner_market",
            "skyscanner_locale",
            "skyscanner_currency",
            "skyscanner_poll_attempts",
            "skyscanner_poll_interval_seconds",
        ),
        ("skyscanner_api_key",),
    ),
    "duffel": ProviderDefinition(
        "Duffel",
        "Offer Request 即時票價與 Get Offer 官方重新驗價；第一版不站內開票。",
        ("duffel_env", "duffel_base_url", "duffel_supplier_timeout_ms"),
        ("duffel_access_token",),
    ),
    "flightaware": ProviderDefinition(
        "FlightAware AeroAPI",
        "航班班表、延誤、取消、航廈、登機門與按需航跡；不提供票價。",
        (
            "flightaware_base_url",
            "flightaware_enrich_offer_limit",
            "flightaware_cache_ttl_seconds",
            "flightaware_track_cache_ttl_seconds",
        ),
        ("flightaware_api_key",),
    ),
    "google_travel_impact": ProviderDefinition(
        "Google Travel Impact Model",
        "以 Google 官方統一模型計算每位旅客碳排，不擷取 Google Flights 價格。",
        ("google_travel_impact_base_url", "travel_impact_cache_ttl_seconds"),
        ("google_travel_impact_api_key",),
    ),
    "navitime": ProviderDefinition(
        "NAVITIME",
        "日本大眾運輸班次；Google Routes API 不提供日本交通資料。"
        "可使用 RapidAPI 的 NAVITIME Route(totalnavi) 金鑰，或直接契約的 Client ID 與金鑰，"
        "並補充班次時刻、票價、月台、出口及建議車廂資訊。",
        ("navitime_api_base_url", "navitime_monthly_request_limit"),
        ("navitime_client_id", "navitime_api_key"),
    ),
    "ekispert": ProviderDefinition(
        "Ekispert（駅すぱあと）",
        "日本大眾運輸路線。預設使用平均等待時間的 plain 模式以控制成本；"
        "只有合約已開通時刻表查詢時，才切換為 departure 模式。",
        (
            "ekispert_api_base_url",
            "ekispert_search_type",
            "ekispert_monthly_request_limit",
        ),
        ("ekispert_api_key",),
    ),
    "odsay": ProviderDefinition(
        "ODsay",
        "韓國大眾運輸多路線。伺服器端必須使用綁定正式主機固定 IP 的 Server Key；"
        "單次查詢直接回傳多個方案，不額外呼叫圖形 API。",
        ("odsay_api_base_url", "odsay_language", "odsay_daily_request_limit"),
        ("odsay_api_key",),
    ),
    "travelpayouts": ProviderDefinition(
        "Travelpayouts Affiliate",
        "航班、住宿、活動、交通與 eSIM 合作連結；可透過 Partner Links API 產生追蹤網址。",
        (
            "travelpayouts_api_base_url",
            "travelpayouts_marker",
            "travelpayouts_project_id",
            "travelpayouts_static_url_template",
            "travelpayouts_flight_target_url",
            "travelpayouts_hotel_target_url",
            "travelpayouts_activities_target_url",
            "travelpayouts_transport_target_url",
            "travelpayouts_connectivity_target_url",
            "travelpayouts_allowed_hosts",
        ),
        ("travelpayouts_api_token",),
        "travelpayouts_enabled",
    ),
    "kkday": ProviderDefinition(
        "KKday KKpartners",
        "活動、票券與接送合作連結；商品 API 需由 KKday 個別核准。",
        ("kkday_cid", "kkday_affiliate_url_template", "kkday_allowed_hosts", "kkday_api_base_url"),
        ("kkday_api_key",),
        "kkday_enabled",
    ),
    "klook": ProviderDefinition(
        "Klook Affiliate",
        "活動、票券與交通合作連結；API 或 data feed 需由 Klook 個別核准。",
        ("klook_affiliate_url_template", "klook_allowed_hosts", "klook_api_base_url"),
        ("klook_api_key",),
        "klook_enabled",
    ),
    "airalo": ProviderDefinition(
        "Airalo Affiliate",
        "eSIM Affiliate 導流，不使用會建立訂單的 Partner Reseller API。",
        ("airalo_affiliate_url_template", "airalo_allowed_hosts"),
        (),
        "airalo_enabled",
    ),
    "trip_com": ProviderDefinition(
        "Trip.com Affiliate",
        "航班、住宿、活動與交通合作連結；完整保留後台產生的追蹤參數。",
        ("trip_com_affiliate_url_template", "trip_com_allowed_hosts"),
        (),
        "trip_com_enabled",
    ),
    "agoda": ProviderDefinition(
        "Agoda Affiliate",
        "住宿 CID 導流；Affiliate API 僅在取得正式憑證後使用。",
        ("agoda_cid", "agoda_affiliate_url_template", "agoda_allowed_hosts", "agoda_api_base_url"),
        ("agoda_api_key",),
        "agoda_enabled",
    ),
    "booking": ProviderDefinition(
        "Booking.com Affiliate",
        "住宿 affiliate ID 與合作連結導流；即時飯店查價在獨立 Demand API 區塊設定。",
        (
            "booking_affiliate_id",
            "booking_affiliate_url_template",
            "booking_allowed_hosts",
        ),
        (),
        "booking_enabled",
    ),
    "booking_demand": ProviderDefinition(
        "Booking.com Demand API",
        "飯店即時查價與 Search and Redirect；不建立站內訂單或處理付款。",
        (
            "booking_demand_env",
            "booking_demand_api_base_url",
            "booking_demand_affiliate_id",
            "booking_booker_country",
            "booking_language",
            "booking_location_cache_ttl_seconds",
        ),
        ("booking_demand_api_token",),
        "booking_demand_enabled",
    ),
    "skyscanner_affiliate": ProviderDefinition(
        "Skyscanner Affiliate",
        "Impact Affiliate 文字連結；不會重複包裝 Travel API 已回傳的 clickout。",
        ("skyscanner_affiliate_url_template", "skyscanner_affiliate_allowed_hosts"),
        (),
        "skyscanner_affiliate_enabled",
    ),
}


def _default_provider_enabled(provider: str) -> bool:
    enabled_field = PROVIDER_DEFINITIONS[provider].enabled_field
    return bool(getattr(get_settings(), enabled_field)) if enabled_field else True


def _fernet(settings: Settings | None = None) -> Fernet:
    config = settings or get_settings()
    raw = config.settings_encryption_key or config.app_secret_key
    key = base64.urlsafe_b64encode(hashlib.sha256(raw.encode()).digest())
    return Fernet(key)


def encrypt_secrets(values: dict[str, str], settings: Settings | None = None) -> str | None:
    if not values:
        return None
    payload = json.dumps(values, ensure_ascii=False, sort_keys=True).encode()
    return _fernet(settings).encrypt(payload).decode()


def decrypt_secrets(value: str | None, settings: Settings | None = None) -> dict[str, str]:
    if not value:
        return {}
    try:
        payload = json.loads(_fernet(settings).decrypt(value.encode()))
    except (InvalidToken, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AppError(
            500,
            "provider_secrets_unreadable",
            "供應商金鑰無法解密，請確認 SETTINGS_ENCRYPTION_KEY 未被變更",
        ) from exc
    if not isinstance(payload, dict) or any(
        not isinstance(key, str) or not isinstance(item, str) for key, item in payload.items()
    ):
        raise AppError(500, "provider_secrets_invalid", "供應商金鑰資料格式錯誤")
    return cast(dict[str, str], payload)


def masked_secret(value: str | None) -> str | None:
    if not value:
        return None
    if len(value) <= 8:
        return "•" * len(value)
    return f"{'•' * 8}{value[-4:]}"


async def provider_rows(session: AsyncSession) -> list[ProviderConfig]:
    return list((await session.scalars(select(ProviderConfig))).all())


def apply_runtime_overrides(base: Settings, rows: list[ProviderConfig]) -> Settings:
    updates: dict[str, Any] = {}
    for row in rows:
        definition = PROVIDER_DEFINITIONS.get(row.provider)
        if definition is None:
            continue
        for field in definition.config_fields:
            if field in row.config:
                updates[field] = row.config[field]
        if definition.enabled_field:
            updates[definition.enabled_field] = row.enabled
        if not row.enabled and row.provider != "runtime":
            updates.update({field: None for field in definition.secret_fields})
            continue
        stored_secrets = decrypt_secrets(row.secret_config_encrypted, base)
        for field in definition.secret_fields:
            if field in stored_secrets:
                updates[field] = stored_secrets[field]
    for field in [name for name in updates if name in OFFICIAL_PROVIDER_HOSTS]:
        stored_url = updates[field]
        if (
            isinstance(stored_url, str)
            and stored_url
            and not official_provider_url_ok(field, stored_url)
        ):
            logger.warning(
                "Ignoring stored %s because it does not use an official provider host", field
            )
            del updates[field]
    try:
        return Settings.model_validate({**base.model_dump(), **updates})
    except ValidationError as exc:
        raise AppError(500, "provider_settings_invalid", "後台供應商設定格式錯誤") from exc


async def load_runtime_settings(session: AsyncSession) -> Settings:
    return apply_runtime_overrides(get_settings(), await provider_rows(session))


async def effective_registration_enabled(session: AsyncSession) -> bool:
    row = await session.scalar(select(ProviderConfig).where(ProviderConfig.provider == "runtime"))
    if row is None:
        return get_settings().registration_enabled
    return apply_runtime_overrides(get_settings(), [row]).registration_enabled


def _site_visibility(settings: Settings) -> SiteVisibility:
    return SiteVisibility(
        **{field: bool(getattr(settings, field)) for field in SITE_VISIBILITY_FIELDS}
    )


async def effective_site_visibility(session: AsyncSession) -> SiteVisibility:
    row = await session.scalar(select(ProviderConfig).where(ProviderConfig.provider == "layout"))
    base = get_settings()
    return _site_visibility(base if row is None else apply_runtime_overrides(base, [row]))


def _configured(provider: str, settings: Settings) -> tuple[bool, str, str]:
    if provider in {"google_login", "line_login", "apple_login"}:
        from app.auth.oauth import provider_enabled

        oauth_provider = {
            "google_login": "google",
            "line_login": "line",
            "apple_login": "apple",
        }[provider]
        configured = provider_enabled(cast(Any, oauth_provider), settings)
        callback = (
            f"{settings.next_public_site_url.rstrip('/')}/api/auth/oauth/{oauth_provider}/callback"
        )
        return (
            configured,
            "ready" if configured else "not_configured",
            f"設定完整；Callback：{callback}"
            if configured
            else f"缺少必要憑證；Callback：{callback}",
        )
    if provider == "analytics":
        ga4_configured = bool(settings.ga4_measurement_id)
        configured = bool(settings.analytics_enabled) and (
            not settings.ga4_enabled or ga4_configured
        )
        message = "第一方分析已啟用" if settings.analytics_enabled else "第一方分析尚未啟用"
        if settings.ga4_enabled:
            message += "；GA4 已設定" if ga4_configured else "；GA4 缺少 Measurement ID"
        else:
            message += "；GA4 未啟用"
        return configured, "ready" if configured else "not_configured", message
    if provider == "runtime":
        from app.providers.registry import flight_provider_status, hotel_provider_status

        flight = flight_provider_status(settings)
        hotel = hotel_provider_status(settings)
        return (
            True,
            "ready",
            (
                f"目前航空：{flight.selected_provider}（{flight.status}）；"
                f"飯店：{hotel.selected_provider}（{hotel.status}）"
            ),
        )
    if provider == "layout":
        visible = sum(bool(getattr(settings, field)) for field in SITE_VISIBILITY_FIELDS)
        message = f"目前開放 {visible}／{len(SITE_VISIBILITY_FIELDS)} 個前台模組"
        return True, "ready", message
    if provider == "ai_planner":
        configured_names = [
            label
            for value, label in (
                (settings.openai_api_key, "OpenAI"),
                (settings.anthropic_api_key, "Claude"),
                (settings.minimax_api_key, "MiniMax"),
            )
            if value
        ]
        if settings.ai_planner_mode in {"fallback", "disabled"}:
            return True, "ready", "目前使用內建備援草稿"
        configured = bool(configured_names)
        return (
            configured,
            "ready" if configured else "not_configured",
            f"已設定：{'、'.join(configured_names)}"
            if configured
            else "尚未設定真實 AI 金鑰，建立行程時會使用內建備援",
        )
    if provider == "ai_guide_search":
        selected = settings.hotspot_guide_ai_default_provider
        key = {
            "openai": settings.openai_api_key,
            "anthropic": settings.anthropic_api_key,
            "minimax": settings.minimax_api_key,
        }[selected]
        sources = bool(
            settings.hotspot_guide_brave_enabled
            and settings.hotspot_guide_brave_api_key
            or settings.hotspot_guide_youtube_enabled
            and settings.hotspot_guide_youtube_api_key
        )
        configured = bool(key and sources)
        return (
            configured,
            "ready" if configured else "not_configured",
            f"預設 {selected}；Brave／YouTube 受控搜尋已可用"
            if configured
            else f"預設 {selected}；請設定對應 AI 金鑰與至少一個搜尋來源",
        )
    if provider == "google_maps":
        configured = bool(settings.google_maps_api_key)
        browser = bool(settings.next_public_google_maps_browser_key)
        browser_enabled = browser and settings.google_maps_javascript_enabled
        message = (
            "Places、Routes 與 Weather 已設定；瀏覽器地圖已明確啟用"
            if configured and browser_enabled
            else "Places、Routes 與 Weather 已設定；瀏覽器地圖安全閘門關閉"
            if configured and browser
            else "Places、Routes 與 Weather 已設定；瀏覽器地圖 Key 尚未設定"
            if configured
            else "缺少伺服器 Google Maps API key"
        )
        return configured, "ready" if configured else "not_configured", message
    if provider == "naver_maps":
        configured = settings.naver_maps_configured
        return (
            configured,
            "ready" if configured else "not_configured",
            "NAVER 憑證已設定；請再以正式網站來源驗證 Dynamic Map"
            if configured
            else "缺少 NAVER Cloud Client ID 或 Client Secret",
        )
    if provider == "youtube_guides":
        configured = bool(settings.hotspot_guide_youtube_api_key)
        return (
            configured,
            "ready" if configured else "not_configured",
            "YouTube Data API 已設定" if configured else "缺少 YouTube Data API key",
        )
    if provider == "brave_guides":
        configured = bool(settings.hotspot_guide_brave_api_key)
        return (
            configured,
            "ready" if configured else "not_configured",
            "Brave Search API 已設定" if configured else "缺少 Brave Search API key",
        )
    if provider == "gemini_guides":
        configured = bool(settings.hotspot_guide_gemini_api_key)
        return (
            configured,
            "ready" if configured else "not_configured",
            "Gemini API 已設定" if configured else "缺少 Gemini API key",
        )
    if provider == "amadeus":
        return (
            settings.amadeus_configured,
            "ready" if settings.amadeus_configured else "not_configured",
            "Amadeus 憑證已設定" if settings.amadeus_configured else "缺少 Client ID 或 Secret",
        )
    if provider == "skyscanner":
        return (
            settings.skyscanner_configured,
            "ready" if settings.skyscanner_configured else "not_configured",
            "Skyscanner API key 已設定"
            if settings.skyscanner_configured
            else "缺少 Skyscanner API key",
        )
    if provider == "duffel":
        configured = settings.duffel_configured and not (
            settings.production and settings.duffel_env.lower() != "live"
        )
        return (
            configured,
            "ready" if configured else "not_configured",
            f"Duffel {settings.duffel_env} 已設定"
            if configured
            else "缺少 Duffel token，或正式環境仍使用 test",
        )
    if provider == "flightaware":
        return (
            settings.flightaware_configured,
            "ready" if settings.flightaware_configured else "not_configured",
            "FlightAware AeroAPI 已設定"
            if settings.flightaware_configured
            else "缺少 FlightAware API key",
        )
    if provider == "google_travel_impact":
        return (
            settings.google_travel_impact_configured,
            "ready" if settings.google_travel_impact_configured else "not_configured",
            "Google Travel Impact Model 已設定"
            if settings.google_travel_impact_configured
            else "缺少 Google Travel Impact API key",
        )
    if provider == "ekispert":
        configured = settings.ekispert_configured
        mode = "時刻表" if settings.ekispert_search_type == "departure" else "平均等待時間"
        return (
            configured,
            "ready" if configured else "not_configured",
            f"Ekispert 憑證已設定（{mode}模式）" if configured else "缺少 Ekispert API key",
        )
    if provider == "odsay":
        configured = settings.odsay_configured
        return (
            configured,
            "ready" if configured else "not_configured",
            "ODsay Server Key 已設定；請確認已綁定正式主機固定 IP"
            if configured
            else "缺少 ODsay Server Key",
        )
    if provider == "booking_demand":
        configured = settings.booking_demand_configured
        return (
            configured,
            "ready" if configured else "not_configured",
            (
                f"Booking.com Demand API {settings.booking_demand_env} 飯店查價已設定"
                if configured
                else "請啟用並設定 Demand Affiliate ID 與 Bearer Token"
            ),
        )
    affiliate_codes = {
        "travelpayouts": "travelpayouts",
        "kkday": "kkday",
        "klook": "klook",
        "airalo": "airalo",
        "trip_com": "trip_com",
        "agoda": "agoda",
        "booking": "booking",
        "skyscanner_affiliate": "skyscanner",
    }
    if provider in affiliate_codes:
        from app.affiliates.registry import PARTNERS_BY_CODE, partner_configured

        partner = PARTNERS_BY_CODE[affiliate_codes[provider]]
        configured = partner_configured(partner, settings)
        return (
            configured,
            "ready" if configured else "not_configured",
            f"{partner.display_name} 合作連結已設定"
            if configured
            else "缺少安全合作連結或必要憑證",
        )
    configured = settings.navitime_configured
    if configured:
        gateway = "RapidAPI" if settings.navitime_rapidapi else "直接契約"
        detail = f"NAVITIME 憑證已設定（{gateway}）"
    else:
        detail = "缺少 API Base URL 或 API key；直接契約另需 Client ID"
    return (configured, "ready" if configured else "not_configured", detail)


def _field_sources(
    definition: ProviderDefinition,
    row: ProviderConfig | None,
    base: Settings,
) -> tuple[dict[str, str], dict[str, SecretState]]:
    config_sources = {
        field: "database" if row is not None and field in row.config else "environment"
        for field in definition.config_fields
    }
    stored = decrypt_secrets(row.secret_config_encrypted, base) if row else {}
    secret_states: dict[str, SecretState] = {}
    for field in definition.secret_fields:
        database_value = stored.get(field)
        environment_value = cast(str | None, getattr(base, field))
        effective = database_value or environment_value
        source = "database" if database_value else "environment" if environment_value else "none"
        if row is not None and not row.enabled:
            effective, source = None, "disabled"
        secret_states[field] = SecretState(
            configured=bool(effective), masked=masked_secret(effective), source=source
        )
    return config_sources, secret_states


def _production_test_required(provider: str, settings: Settings) -> bool:
    if provider == "amadeus":
        return settings.amadeus_env.lower() == "production"
    if provider == "booking_demand":
        return settings.booking_demand_env.lower() == "production"
    if provider == "duffel":
        return settings.duffel_env.lower() == "live"
    return provider in {
        "skyscanner",
        "flightaware",
        "google_travel_impact",
        "naver_maps",
        "ekispert",
        "odsay",
    }


async def settings_snapshot(
    session: AsyncSession, redis: Redis | None = None
) -> ProviderSettingsSnapshot:
    base = get_settings()
    rows = await provider_rows(session)
    by_provider = {row.provider: row for row in rows}
    effective = apply_runtime_overrides(base, rows)
    google_usage = (
        await google_maps_usage_snapshot(
            redis,
            essentials_free_limit=effective.google_maps_essentials_free_limit,
            pro_free_limit=effective.google_maps_pro_free_limit,
            enterprise_free_limit=effective.google_maps_enterprise_free_limit,
        )
        if redis is not None
        else None
    )
    naver_usage = (
        await naver_maps_usage_snapshot(
            redis,
            monthly_limit=effective.naver_maps_monthly_request_limit,
        )
        if redis is not None
        else None
    )
    navitime_usage = (
        await navitime_usage_snapshot(
            redis,
            monthly_limit=effective.navitime_monthly_request_limit,
        )
        if redis is not None
        else None
    )
    ekispert_usage = (
        await ekispert_usage_snapshot(
            redis,
            monthly_limit=effective.ekispert_monthly_request_limit,
        )
        if redis is not None
        else None
    )
    odsay_usage = (
        await odsay_usage_snapshot(
            redis,
            daily_limit=effective.odsay_daily_request_limit,
        )
        if redis is not None
        else None
    )
    youtube_usage = (
        await youtube_usage_snapshot(
            redis,
            search_daily_free_limit=effective.hotspot_guide_youtube_search_daily_free_limit,
            core_daily_free_limit=effective.hotspot_guide_youtube_core_daily_free_limit,
        )
        if redis is not None
        else None
    )
    recent_requests = list(
        (
            await session.scalars(
                select(ProviderRequest).where(
                    ProviderRequest.created_at >= datetime.now(UTC) - timedelta(hours=24)
                )
            )
        ).all()
    )
    providers: list[ProviderSettingsView] = []
    for provider, definition in PROVIDER_DEFINITIONS.items():
        row = by_provider.get(provider)
        enabled = (
            row.enabled
            if row is not None
            else bool(getattr(base, definition.enabled_field))
            if definition.enabled_field
            else True
        )
        configured, status, message = _configured(provider, effective)
        if not enabled and provider != "runtime":
            configured, status, message = False, "disabled", "已由管理後台停用"
        elif configured and row is not None and row.last_test_status == "failed":
            configured, status = False, "error"
            message = f"最近一次連線測試失敗：{row.last_test_message or '請重新測試'}"
        elif (
            configured
            and _production_test_required(provider, effective)
            and (row is None or row.last_test_status != "success")
        ):
            configured, status = False, "test_required"
            message = "Production 憑證已設定，必須通過連線測試後才標示為可用"
        config_sources, secret_states = _field_sources(definition, row, base)
        providers.append(
            ProviderSettingsView(
                provider=provider,
                label=definition.label,
                description=definition.description,
                enabled=enabled,
                configured=configured,
                status=status,
                status_message=message,
                config={
                    field: cast(Any, getattr(effective, field))
                    for field in definition.config_fields
                },
                config_sources=config_sources,
                secrets=secret_states,
                last_tested_at=row.last_tested_at if row else None,
                last_test_status=row.last_test_status if row else None,
                last_test_message=row.last_test_message if row else None,
                updated_at=row.updated_at if row else None,
                usage=(
                    ProviderUsageView(**asdict(google_usage))
                    if provider == "google_maps" and google_usage is not None
                    else ProviderUsageView(**asdict(naver_usage))
                    if provider == "naver_maps" and naver_usage is not None
                    else ProviderUsageView(**asdict(navitime_usage))
                    if provider == "navitime" and navitime_usage is not None
                    else ProviderUsageView(**asdict(ekispert_usage))
                    if provider == "ekispert" and ekispert_usage is not None
                    else ProviderUsageView(**asdict(odsay_usage))
                    if provider == "odsay" and odsay_usage is not None
                    else ProviderUsageView(**asdict(youtube_usage))
                    if provider == "youtube_guides" and youtube_usage is not None
                    else None
                ),
                requests_24h=sum(
                    1 for request in recent_requests if provider in request.provider.split(",")
                ),
                errors_24h=sum(
                    1
                    for request in recent_requests
                    if provider in request.provider.split(",") and request.status == "failed"
                ),
                last_error_at=max(
                    (
                        request.created_at
                        for request in recent_requests
                        if provider in request.provider.split(",") and request.status == "failed"
                    ),
                    default=None,
                ),
            )
        )
    audit_rows = list(
        (
            await session.scalars(
                select(AdminAuditLog)
                .where(
                    AdminAuditLog.action.in_(
                        [
                            "provider_settings_updated",
                            "provider_connection_tested",
                            "system_settings_updated",
                            "layout_settings_updated",
                        ]
                    )
                )
                .order_by(AdminAuditLog.created_at.desc())
                .limit(20)
            )
        ).all()
    )
    audit = [
        AdminAuditView(
            id=row.id,
            actor_user_id=row.actor_user_id,
            action=row.action,
            target=row.target,
            metadata=row.metadata_json,
            created_at=row.created_at,
        )
        for row in audit_rows
    ]
    return ProviderSettingsSnapshot(
        providers=providers,
        audit=audit,
        encryption_source=(
            "SETTINGS_ENCRYPTION_KEY" if base.settings_encryption_key else "APP_SECRET_KEY"
        ),
    )


def _validate_provider_values(
    provider: str,
    current_config: dict[str, Any],
    payload: ProviderSettingsUpdate,
) -> dict[str, Any]:
    definition = PROVIDER_DEFINITIONS[provider]
    unknown_config = set(payload.config) - set(definition.config_fields)
    unknown_secrets = set(payload.secrets) - set(definition.secret_fields)
    if unknown_config or unknown_secrets:
        names = ", ".join(sorted(unknown_config | unknown_secrets))
        raise AppError(422, "provider_setting_unknown", f"不支援的設定欄位：{names}")
    merged = dict(current_config)
    for field, value in payload.config.items():
        if value is None:
            merged.pop(field, None)
        else:
            merged[field] = value
    boolean_fields = {
        "registration_enabled",
        "ga4_enabled",
        "analytics_trust_country_header",
        "google_maps_javascript_enabled",
        *SITE_VISIBILITY_FIELDS,
    }
    for field in boolean_fields:
        if field in merged and not isinstance(merged[field], bool):
            raise AppError(
                422,
                "provider_setting_invalid",
                f"{field} 必須是布林值",
            )
    if "ga4_measurement_id" in merged:
        measurement_id = str(merged["ga4_measurement_id"] or "").strip().upper()
        if measurement_id and not re.fullmatch(r"G-[A-Z0-9]{4,16}", measurement_id):
            raise AppError(
                422,
                "provider_setting_invalid",
                "ga4_measurement_id 必須是有效的 G-... Measurement ID",
            )
        merged["ga4_measurement_id"] = measurement_id
    modes = {
        "travel_provider_mode": {"mock", "amadeus", "live", "disabled"},
        "flight_provider_mode": {"auto", "skyscanner", "duffel", "amadeus", "mock", "disabled"},
        "flight_search_strategy": {"hybrid", "single"},
        "hotel_provider_mode": {"auto", "booking", "amadeus", "mock", "disabled"},
        "amadeus_env": {"test", "production"},
        "duffel_env": {"test", "live"},
        "booking_demand_env": {"sandbox", "production"},
        "ai_planner_mode": {
            "auto",
            "openai",
            "anthropic",
            "minimax",
            "fallback",
            "disabled",
        },
        "hotspot_guide_ai_default_provider": {"openai", "anthropic", "minimax"},
    }
    for field, allowed in modes.items():
        if field in merged and str(merged[field]).lower() not in allowed:
            raise AppError(422, "provider_setting_invalid", f"{field} 的選項不正確")
    url_fields = {
        field for field in merged if field.endswith("_url") or field.endswith("_url_template")
    }
    for field in url_fields:
        if field in merged:
            value = str(merged[field])
            if not value:
                continue
            parsed = urlparse(value)
            if parsed.scheme != "https" or not parsed.netloc:
                raise AppError(422, "provider_setting_invalid", f"{field} 必須是 HTTPS URL")
    for field in (item for item in merged if item.endswith("_allowed_hosts")):
        hosts = [item.strip() for item in str(merged[field]).split(",") if item.strip()]
        if not hosts or any(
            "/" in host or ":" in host or "@" in host or "*" in host or "." not in host
            for host in hosts
        ):
            raise AppError(
                422,
                "provider_setting_invalid",
                f"{field} 必須是逗號分隔的完整網域，不可包含協定、路徑或萬用字元",
            )
    for field, allowed_hosts in OFFICIAL_PROVIDER_HOSTS.items():
        pinned_value = merged.get(field)
        if pinned_value and not official_provider_url_ok(field, str(pinned_value)):
            raise AppError(
                422,
                "provider_setting_invalid",
                f"{field} 必須使用官方 API 網域（{', '.join(sorted(allowed_hosts))}）",
            )
    if "ai_planner_priority" in merged:
        priority = [item.strip().lower() for item in str(merged["ai_planner_priority"]).split(",")]
        if (
            not priority
            or len(priority) != len(set(priority))
            or any(item not in {"openai", "anthropic", "minimax"} for item in priority)
        ):
            raise AppError(
                422,
                "provider_setting_invalid",
                "AI 備援順序只能使用不重複的 openai、anthropic、minimax",
            )
    if "skyscanner_market" in merged:
        merged["skyscanner_market"] = str(merged["skyscanner_market"]).upper()
    if "skyscanner_currency" in merged:
        merged["skyscanner_currency"] = str(merged["skyscanner_currency"]).upper()
    if "booking_demand_env" in merged:
        environment = str(merged["booking_demand_env"]).lower()
        merged["booking_demand_env"] = environment
        official_urls = {
            "sandbox": "https://demandapi-sandbox.booking.com/3.1",
            "production": "https://demandapi.booking.com/3.1",
        }
        current_url = str(merged.get("booking_demand_api_base_url") or "")
        if not current_url or (urlparse(current_url).hostname or "").lower() in BOOKING_API_HOSTS:
            merged["booking_demand_api_base_url"] = official_urls[environment]
    if "booking_demand_api_base_url" in merged:
        booking_url = urlparse(str(merged["booking_demand_api_base_url"]))
        booking_environment = str(
            merged.get("booking_demand_env", get_settings().booking_demand_env)
        ).lower()
        expected_host = {
            "sandbox": "demandapi-sandbox.booking.com",
            "production": "demandapi.booking.com",
        }.get(booking_environment)
        if (
            (booking_url.hostname or "").lower() not in BOOKING_API_HOSTS
            or (expected_host is not None and booking_url.hostname != expected_host)
            or booking_url.path.rstrip("/") != "/3.1"
        ):
            raise AppError(
                422,
                "provider_setting_invalid",
                "Booking Demand API 必須使用官方 v3.1 sandbox 或 production URL",
            )
    for field in ("booking_booker_country", "booking_language"):
        if field in merged:
            merged[field] = str(merged[field]).lower()
    if "booking_booker_country" in merged and not re.fullmatch(
        r"[a-z]{2}", str(merged["booking_booker_country"])
    ):
        raise AppError(422, "provider_setting_invalid", "Booker country 必須是兩碼國家代碼")
    try:
        Settings.model_validate({**get_settings().model_dump(), **merged})
    except ValidationError as exc:
        raise AppError(422, "provider_setting_invalid", "設定數值超出允許範圍") from exc
    return merged


async def update_provider_settings(
    session: AsyncSession,
    provider: str,
    payload: ProviderSettingsUpdate,
    actor: User,
    redis: Redis,
) -> ProviderSettingsSnapshot:
    if provider not in PROVIDER_DEFINITIONS:
        raise AppError(404, "provider_setting_not_found", "找不到這個供應商設定")
    row = await session.scalar(select(ProviderConfig).where(ProviderConfig.provider == provider))
    if row is None:
        row = ProviderConfig(
            provider=provider,
            enabled=_default_provider_enabled(provider),
            priority=100,
            config={},
        )
        session.add(row)
    previous_config = dict(row.config or {})
    row.config = _validate_provider_values(provider, previous_config, payload)
    stored = _merge_secret_values(decrypt_secrets(row.secret_config_encrypted), payload.secrets)
    row.secret_config_encrypted = encrypt_secrets(stored)
    if provider in {"runtime", "layout"}:
        row.enabled = True
    elif payload.enabled is not None:
        row.enabled = payload.enabled
    row.updated_by_user_id = actor.id
    row.last_test_status = None
    row.last_test_message = None
    audit_metadata: dict[str, object] = {
        "config_fields": sorted(payload.config),
    }
    if provider == "runtime":
        missing = object()
        audit_metadata["config_fields"] = sorted(
            field
            for field in payload.config
            if previous_config.get(field, missing) != row.config.get(field, missing)
        )
        audit_action = "system_settings_updated"
        audit_metadata["registration_enabled"] = apply_runtime_overrides(
            get_settings(), [row]
        ).registration_enabled
    elif provider == "layout":
        missing = object()
        audit_metadata["config_fields"] = sorted(
            field
            for field in payload.config
            if previous_config.get(field, missing) != row.config.get(field, missing)
        )
        audit_action = "layout_settings_updated"
        audit_metadata["visibility"] = _site_visibility(
            apply_runtime_overrides(get_settings(), [row])
        ).model_dump()
    else:
        audit_action = "provider_settings_updated"
        audit_metadata.update(
            {
                "enabled": row.enabled,
                "secret_fields": sorted(payload.secrets),
            }
        )
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action=audit_action,
            target=provider,
            metadata_json=audit_metadata,
        )
    )
    await session.commit()
    if provider == "amadeus":
        await redis.delete("provider:amadeus:oauth-token")
    return await settings_snapshot(session, redis)


def _merge_secret_values(current: dict[str, str], updates: dict[str, str | None]) -> dict[str, str]:
    merged = dict(current)
    for field, value in updates.items():
        if value is None:
            merged.pop(field, None)
            continue
        cleaned = value.strip()
        if not cleaned:
            continue
        if len(cleaned) > 2048:
            raise AppError(422, "provider_secret_invalid", f"{field} 金鑰格式不正確")
        merged[field] = cleaned
    return merged


async def _test_google(settings: Settings, redis: Redis) -> str:
    service = GoogleTravelService(redis, settings)
    places = await service.autocomplete("台北車站", None, ["tw"])
    if not places:
        raise ConnectionError("Places API 未回傳結果，請檢查 API 啟用狀態與金鑰限制")
    route_test_time = datetime.now(ZoneInfo("Asia/Taipei")) + timedelta(days=1)
    while route_test_time.weekday() >= 5:
        route_test_time += timedelta(days=1)
    route_test_time = route_test_time.replace(hour=10, minute=0, second=0, microsecond=0)
    routes = await GoogleRouteProvider(settings, None, redis).probe(
        RoutePoint(
            item_id=uuid4(),
            name="台北車站",
            latitude=25.0478,
            longitude=121.5170,
        ),
        RoutePoint(
            item_id=uuid4(),
            name="台北 101",
            latitude=25.0330,
            longitude=121.5654,
        ),
        route_test_time,
    )
    if not routes.reachable:
        details = routes.error_code or "UNKNOWN_ERROR"
        if routes.status_code is not None:
            details = f"HTTP {routes.status_code} / {details}"
        raise ConnectionError(f"Places 可用，但 Routes API 連線失敗（{details}）")
    route_message = (
        "Routes API 可連線（日本大眾運輸使用 Ekispert 或 NAVITIME）"
        if routes.route_available
        else "Routes API 可連線；非日本測試路線目前無可用班次"
        "（日本大眾運輸使用 Ekispert 或 NAVITIME）"
    )
    weather_message = "Weather API 連線成功"
    try:
        weather = await GoogleWeatherService(redis, settings).lookup(
            latitude=35.6812,
            longitude=139.7671,
            location_name="東京車站",
        )
        if weather.current is None and not weather.days:
            weather_message = "Weather API 未回傳資料（不影響地圖與路線）"
    except AppError as exc:
        logger.info(
            "google_weather_connection_test_partial",
            extra={"reason_code": exc.code},
        )
        weather_message = f"Weather API 暫時不可用（{exc.code}；不影響地圖與路線）"
    except Exception:
        logger.warning(
            "google_weather_connection_test_failed",
            extra={"reason_code": "weather_connection_failed"},
            exc_info=True,
        )
        weather_message = "Weather API 暫時不可用（不影響地圖與路線）"
    return f"Google Places、{route_message}；{weather_message}"


async def _test_naver(settings: Settings, redis: Redis) -> str:
    places = await NaverPlaceService(redis, settings).autocomplete("景福宮", "connection-test")
    if not places:
        raise ConnectionError("NAVER Local Search／Geocoding 未回傳韓國地點")
    segment = await NaverDirectionsProvider(settings, None, redis).compute(
        RoutePoint(
            item_id=uuid4(),
            name="景福宮",
            latitude=37.5796,
            longitude=126.9770,
            place_provider="naver_local",
        ),
        RoutePoint(
            item_id=uuid4(),
            name="北村韓屋村",
            latitude=37.5826,
            longitude=126.9830,
            place_provider="naver_local",
        ),
        None,
        "FASTEST",
        "drive",
    )
    if segment is None:
        raise ConnectionError("NAVER Directions 未回傳首爾汽車路線")
    return "NAVER 韓國地點搜尋與汽車路線驗證成功；Dynamic Map 仍需由已授權網站來源載入確認"


async def _test_provider(provider: str, settings: Settings, redis: Redis) -> str:
    if provider in {"google_login", "line_login", "apple_login"}:
        from app.auth.oauth import APPLE_JWKS, GOOGLE_JWKS, apple_client_secret

        if provider == "apple_login":
            _ = apple_client_secret(settings)
            url = APPLE_JWKS
        elif provider == "google_login":
            url = GOOGLE_JWKS
        else:
            url = "https://access.line.me/.well-known/openid-configuration"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            _ = response.json()
        return "官方 OpenID metadata 可連線；完整憑證會在實際互動登入時驗證"
    if provider == "ai_planner":
        request = AIItineraryRequest(
            destination_name="東京",
            start_date=date.today() + timedelta(days=45),
            end_date=date.today() + timedelta(days=45),
            timezone="Asia/Tokyo",
            route_preference="FEWER_TRANSFERS",
            travelers=Travelers(adults=1),
            preferences=SearchPreferences(interests=["culture"]),
            notes="連線測試",
        )
        result = await AIItineraryPlanner(settings).generate(request)
        if result.planning.provider == "catalog":
            raise ConnectionError("沒有任何真實 AI 供應商成功回傳結構化行程")
        return f"{result.planning.provider} / {result.planning.model} 結構化行程驗證成功"
    if provider == "ai_guide_search":
        from app.hotspots.ai_search import test_research_provider

        selected, model = await test_research_provider(settings)
        return f"{selected} / {model} AI 景點搜尋結構化輸出驗證成功"
    if provider == "google_maps":
        return await _test_google(settings, redis)
    if provider == "naver_maps":
        return await _test_naver(settings, redis)
    if provider == "youtube_guides":
        from app.hotspots.guides import YouTubeGuideProvider

        if not settings.hotspot_guide_youtube_api_key:
            raise ConnectionError("缺少 YouTube Data API key")
        youtube_client = YouTubeGuideProvider(settings.hotspot_guide_youtube_api_key, redis=redis)
        try:
            await youtube_client.search("Tokyo travel guide", "en", 1)
        finally:
            await youtube_client.close()
        return "YouTube 景點影片搜尋成功"
    if provider == "brave_guides":
        from app.hotspots.guides import BraveGuideProvider

        if not settings.hotspot_guide_brave_api_key:
            raise ConnectionError("缺少 Brave Search API key")
        brave_client = BraveGuideProvider(settings.hotspot_guide_brave_api_key)
        try:
            await brave_client.search("Tokyo travel guide", "en", 1)
        finally:
            await brave_client.close()
        return "Brave 多語文章搜尋成功"
    if provider == "gemini_guides":
        from app.hotspots.guides import GeminiGuideProvider

        if not settings.hotspot_guide_gemini_api_key:
            raise ConnectionError("缺少 Gemini API key")
        gemini_client = GeminiGuideProvider(
            settings.hotspot_guide_gemini_api_key,
            settings.hotspot_guide_gemini_base_url,
            settings.hotspot_guide_gemini_model,
            settings.hotspot_guide_gemini_timeout_seconds,
        )
        try:
            await gemini_client.search("Tokyo Senso-ji travel blog", "en", 1)
        finally:
            await gemini_client.close()
        return f"Gemini 多語文章搜尋成功（{settings.hotspot_guide_gemini_model}）"
    if provider == "amadeus":
        await AmadeusProvider(redis, settings)._token()
        return f"Amadeus {settings.amadeus_env} OAuth 驗證成功"
    if provider == "skyscanner":
        query = SearchCreate(
            origin="TPE",
            destination="NRT",
            departure_date=date.today() + timedelta(days=45),
            return_date=date.today() + timedelta(days=49),
            modules=[SearchModule.FLIGHT],
        )
        await SkyscannerProvider(redis, settings).start_search(query)
        return "Skyscanner Live Flights 驗證成功"
    if provider == "duffel":
        query = SearchCreate(
            origin="TPE",
            destination="NRT",
            departure_date=date.today() + timedelta(days=45),
            return_date=date.today() + timedelta(days=49),
            modules=[SearchModule.FLIGHT],
        )
        await DuffelProvider(redis, settings).search_flights(query)
        return f"Duffel {settings.duffel_env} Offer Request 驗證成功"
    if provider == "flightaware":
        await FlightAwareProvider(redis, settings).lookup(
            date.today() + timedelta(days=10), origin="TPE", destination="NRT"
        )
        return "FlightAware AeroAPI 班表查詢成功"
    if provider == "google_travel_impact":
        await GoogleTravelImpactProvider(redis, settings)._compute(
            [
                {
                    "origin": "TPE",
                    "destination": "NRT",
                    "operatingCarrierCode": "BR",
                    "flightNumber": 198,
                    "departureDate": {
                        "year": (date.today() + timedelta(days=45)).year,
                        "month": (date.today() + timedelta(days=45)).month,
                        "day": (date.today() + timedelta(days=45)).day,
                    },
                }
            ]
        )
        return "Google Travel Impact Model 驗證成功"
    if provider == "booking_demand":
        await BookingHotelProvider(redis, settings).probe()
        return f"Booking.com Demand API {settings.booking_demand_env} 驗證成功"
    if provider == "ekispert":
        ekispert_probe = await EkispertRouteProvider(settings, None, redis).probe(
            RoutePoint(item_id=uuid4(), name="東京", latitude=35.6812, longitude=139.7671),
            RoutePoint(item_id=uuid4(), name="淺草", latitude=35.7148, longitude=139.7967),
        )
        if not ekispert_probe.reachable:
            details = ekispert_probe.error_code or "UNKNOWN_ERROR"
            if ekispert_probe.status_code is not None:
                details = f"HTTP {ekispert_probe.status_code} / {details}"
            raise ConnectionError(f"Ekispert 連線失敗（{details}）")
        if not ekispert_probe.route_available:
            raise ConnectionError("Ekispert 可連線，但未回傳東京→淺草的測試路線")
        return "Ekispert 日本大眾運輸路線驗證成功"
    if provider == "odsay":
        odsay_probe = await OdsayRouteProvider(settings, None, redis).probe(
            RoutePoint(item_id=uuid4(), name="首爾站", latitude=37.5547, longitude=126.9707),
            RoutePoint(item_id=uuid4(), name="景福宮", latitude=37.5796, longitude=126.9770),
        )
        if not odsay_probe.reachable:
            details = odsay_probe.error_code or "UNKNOWN_ERROR"
            if odsay_probe.status_code is not None:
                details = f"HTTP {odsay_probe.status_code} / {details}"
            raise ConnectionError(f"ODsay 連線失敗（{details}）")
        if not odsay_probe.route_available:
            raise ConnectionError("ODsay 可連線，但未回傳首爾站→景福宮的測試路線")
        return "ODsay 韓國大眾運輸路線驗證成功"
    if provider == "navitime":
        gateway = "RapidAPI" if settings.navitime_rapidapi else "直接契約"
        navitime_probe = await NavitimeRouteProvider(settings, None, redis).probe(
            RoutePoint(item_id=uuid4(), name="東京", latitude=35.6812, longitude=139.7671),
            RoutePoint(item_id=uuid4(), name="淺草", latitude=35.7148, longitude=139.7967),
        )
        if not navitime_probe.reachable:
            details = navitime_probe.error_code or "UNKNOWN_ERROR"
            if navitime_probe.status_code is not None:
                details = f"HTTP {navitime_probe.status_code} / {details}"
            raise ConnectionError(f"NAVITIME（{gateway}）連線失敗（{details}）")
        if not navitime_probe.route_available:
            raise ConnectionError(f"NAVITIME（{gateway}）可連線，但未回傳東京→淺草的測試路線")
        return f"NAVITIME（{gateway}）路線驗證成功"
    affiliate_codes = {
        "travelpayouts": "travelpayouts",
        "kkday": "kkday",
        "klook": "klook",
        "airalo": "airalo",
        "trip_com": "trip_com",
        "agoda": "agoda",
        "booking": "booking",
        "skyscanner_affiliate": "skyscanner",
    }
    if provider in affiliate_codes:
        from app.affiliates.registry import PARTNERS_BY_CODE
        from app.affiliates.service import AffiliateContext, resolve_partner_target

        partner = PARTNERS_BY_CODE[affiliate_codes[provider]]
        module = partner.modules[0]
        await resolve_partner_target(
            partner,
            AffiliateContext(
                module=module,
                destination="東京",
                departure_date=(date.today() + timedelta(days=45)).isoformat(),
                return_date=(date.today() + timedelta(days=49)).isoformat(),
                sub_id="connection-test",
            ),
            settings,
            redis,
        )
        return f"{partner.display_name} 合作連結驗證成功"
    return "執行模式設定不需要外部連線測試"


def _safe_test_message(provider: str, message: str, settings: Settings) -> str:
    definition = PROVIDER_DEFINITIONS[provider]
    sanitized = message
    for field in definition.secret_fields:
        value = cast(str | None, getattr(settings, field))
        if value:
            sanitized = sanitized.replace(value, "***")
    return sanitized[:500] or "連線測試失敗"


async def test_provider_connection(
    session: AsyncSession,
    provider: str,
    actor: User,
    redis: Redis,
) -> ProviderTestResult:
    if provider not in PROVIDER_DEFINITIONS:
        raise AppError(404, "provider_setting_not_found", "找不到這個供應商設定")
    row = await session.scalar(select(ProviderConfig).where(ProviderConfig.provider == provider))
    if row is None:
        row = ProviderConfig(
            provider=provider,
            enabled=_default_provider_enabled(provider),
            priority=100,
            config={},
        )
        session.add(row)
    settings = await load_runtime_settings(session)
    started = time.perf_counter()
    tested_at = datetime.now(UTC)
    try:
        message = await _test_provider(provider, settings, redis)
        status = "success"
    except Exception as exc:
        status = "failed"
        message = _safe_test_message(provider, str(exc), settings)
    latency_ms = round((time.perf_counter() - started) * 1000)
    row.last_tested_at = tested_at
    row.last_test_status = status
    row.last_test_message = message
    row.updated_by_user_id = actor.id
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="provider_connection_tested",
            target=provider,
            metadata_json={"status": status, "latency_ms": latency_ms},
        )
    )
    await session.commit()
    return ProviderTestResult(
        provider=provider,
        status=status,
        message=message,
        tested_at=tested_at,
        latency_ms=latency_ms,
    )


async def public_runtime_config(session: AsyncSession) -> PublicRuntimeConfig:
    settings = await load_runtime_settings(session)
    google_browser_map_enabled = bool(
        settings.next_public_google_maps_browser_key and settings.google_maps_javascript_enabled
    )
    return PublicRuntimeConfig(
        # The browser key is public by design, but the kill switch should still stop
        # handing it out: with the JavaScript/embed surfaces off nothing needs it.
        google_maps_browser_key=(
            settings.next_public_google_maps_browser_key if google_browser_map_enabled else None
        ),
        google_maps_enabled=bool(settings.google_maps_api_key),
        google_routes_enabled=bool(settings.google_maps_api_key),
        google_places_enabled=bool(settings.google_maps_api_key),
        google_maps_embed_enabled=google_browser_map_enabled,
        google_maps_javascript_enabled=google_browser_map_enabled,
        navitime_enabled=settings.navitime_configured,
        ekispert_enabled=settings.ekispert_configured,
        odsay_enabled=settings.odsay_configured,
        naver_maps_browser_client_id=settings.naver_maps_client_id,
        naver_maps_enabled=settings.naver_maps_configured,
        naver_places_enabled=settings.naver_maps_configured,
        naver_directions_enabled=settings.naver_maps_configured,
        naver_dynamic_map_enabled=bool(settings.naver_maps_client_id),
    )
