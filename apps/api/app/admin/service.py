from __future__ import annotations

import base64
import hashlib
import json
import re
import time
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime, timedelta
from typing import Any, cast
from urllib.parse import urlparse
from uuid import uuid4

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
)
from app.ai.itinerary import AIItineraryPlanner, AIItineraryRequest
from app.config import Settings, get_settings
from app.models import AdminAuditLog, ProviderConfig, ProviderRequest, User
from app.places.google import GoogleTravelService
from app.problems import AppError
from app.providers.amadeus import AmadeusProvider
from app.providers.booking import BOOKING_API_HOSTS, BookingHotelProvider
from app.providers.duffel import DuffelProvider
from app.providers.flightaware import FlightAwareProvider
from app.providers.google_travel_impact import GoogleTravelImpactProvider
from app.providers.skyscanner import SkyscannerProvider
from app.providers.usage_meter import google_maps_usage_snapshot
from app.search.schemas import SearchCreate, SearchModule, SearchPreferences, Travelers
from app.trips.routing import (
    GoogleRouteProvider,
    NavitimeRouteProvider,
    RoutePoint,
)
from app.weather.google import GoogleWeatherService


@dataclass(frozen=True)
class ProviderDefinition:
    label: str
    description: str
    config_fields: tuple[str, ...]
    secret_fields: tuple[str, ...]
    enabled_field: str | None = None


PROVIDER_DEFINITIONS: dict[str, ProviderDefinition] = {
    "runtime": ProviderDefinition(
        "執行模式與保護設定",
        "控制即時／測試供應商選擇、逾時、重試斷路器及每分鐘請求上限。",
        (
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
    "google_maps": ProviderDefinition(
        "Google Maps",
        "Google Places 地點搜尋、Routes 大眾運輸路線、Weather 天氣與瀏覽器 Embed 地圖。",
        (
            "route_cache_ttl_seconds",
            "weather_cache_ttl_seconds",
            "google_maps_essentials_free_limit",
            "google_maps_pro_free_limit",
            "google_maps_enterprise_free_limit",
        ),
        ("google_maps_api_key", "next_public_google_maps_browser_key"),
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
        "日本大眾運輸備援，補充月台、出口及建議車廂資訊。",
        ("navitime_api_base_url",),
        ("navitime_client_id", "navitime_api_key"),
    ),
    "travelpayouts": ProviderDefinition(
        "Travelpayouts Affiliate",
        "航班、住宿、活動與交通合作連結；可透過 Partner Links API 產生追蹤網址。",
        (
            "travelpayouts_api_base_url",
            "travelpayouts_marker",
            "travelpayouts_project_id",
            "travelpayouts_static_url_template",
            "travelpayouts_flight_target_url",
            "travelpayouts_hotel_target_url",
            "travelpayouts_activities_target_url",
            "travelpayouts_transport_target_url",
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
    try:
        return Settings.model_validate({**base.model_dump(), **updates})
    except ValidationError as exc:
        raise AppError(500, "provider_settings_invalid", "後台供應商設定格式錯誤") from exc


async def load_runtime_settings(session: AsyncSession) -> Settings:
    return apply_runtime_overrides(get_settings(), await provider_rows(session))


def _configured(provider: str, settings: Settings) -> tuple[bool, str, str]:
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
    if provider == "google_maps":
        configured = bool(settings.google_maps_api_key)
        browser = bool(settings.next_public_google_maps_browser_key)
        message = (
            "Places、Routes 與 Weather 已設定；Embed 地圖已設定"
            if configured and browser
            else "Places、Routes 與 Weather 已設定；Embed 地圖尚未設定"
            if configured
            else "缺少伺服器 Google Maps API key"
        )
        return configured, "ready" if configured else "not_configured", message
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
    return (
        configured,
        "ready" if configured else "not_configured",
        "NAVITIME 憑證已設定" if configured else "缺少 API URL、Client ID 或 API key",
    )


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
    return provider in {"skyscanner", "flightaware", "google_travel_impact"}


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
                    ProviderUsageView(
                        **asdict(google_usage),
                    )
                    if provider == "google_maps" and google_usage is not None
                    else None
                ),
                requests_24h=sum(
                    1
                    for request in recent_requests
                    if provider in request.provider.split(",")
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
                        if provider in request.provider.split(",")
                        and request.status == "failed"
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
                        ["provider_settings_updated", "provider_connection_tested"]
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
    if "travelpayouts_api_base_url" in merged:
        host = urlparse(str(merged["travelpayouts_api_base_url"])).hostname
        if host != "api.travelpayouts.com":
            raise AppError(
                422,
                "provider_setting_invalid",
                "Travelpayouts API Base URL 必須使用官方 api.travelpayouts.com",
            )
    official_ai_hosts = {
        "openai_api_base_url": {"api.openai.com"},
        "anthropic_api_base_url": {"api.anthropic.com"},
        "minimax_api_base_url": {"api.minimaxi.com", "api.minimax.io"},
    }
    for field, allowed_hosts in official_ai_hosts.items():
        if field in merged and urlparse(str(merged[field])).hostname not in allowed_hosts:
            raise AppError(
                422,
                "provider_setting_invalid",
                f"{field} 必須使用官方 API 網域",
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
    row.config = _validate_provider_values(provider, row.config or {}, payload)
    stored = _merge_secret_values(decrypt_secrets(row.secret_config_encrypted), payload.secrets)
    row.secret_config_encrypted = encrypt_secrets(stored)
    if payload.enabled is not None:
        row.enabled = payload.enabled
    row.updated_by_user_id = actor.id
    row.last_test_status = None
    row.last_test_message = None
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="provider_settings_updated",
            target=provider,
            metadata_json={
                "enabled": row.enabled,
                "config_fields": sorted(payload.config),
                "secret_fields": sorted(payload.secrets),
            },
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
    places = await service.autocomplete("東京車站", None, ["jp"])
    if not places:
        raise ConnectionError("Places API 未回傳結果，請檢查 API 啟用狀態與金鑰限制")
    routes = await GoogleRouteProvider(settings, None, redis).probe(
        RoutePoint(
            item_id=uuid4(),
            name="東京車站",
            latitude=35.6812,
            longitude=139.7671,
        ),
        RoutePoint(
            item_id=uuid4(),
            name="淺草寺",
            latitude=35.7148,
            longitude=139.7967,
        ),
    )
    if not routes.reachable:
        details = routes.error_code or "UNKNOWN_ERROR"
        if routes.status_code is not None:
            details = f"HTTP {routes.status_code} / {details}"
        raise ConnectionError(f"Places 可用，但 Routes API 連線失敗（{details}）")
    route_message = (
        "Routes API 可連線"
        if routes.route_available
        else "Routes API 可連線；測試路線目前無可用班次"
    )
    weather = await GoogleWeatherService(redis, settings).lookup(
        latitude=35.6812,
        longitude=139.7671,
        location_name="東京車站",
    )
    if weather.current is None and not weather.days:
        raise ConnectionError("Weather API 未回傳目前天氣或預報")
    return f"Google Places、{route_message}；Weather API 連線成功"


async def _test_provider(provider: str, settings: Settings, redis: Redis) -> str:
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
    if provider == "google_maps":
        return await _test_google(settings, redis)
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
    if provider == "navitime":
        segment = await NavitimeRouteProvider(settings).compute(
            RoutePoint(item_id=uuid4(), name="東京", latitude=35.6812, longitude=139.7671),
            RoutePoint(item_id=uuid4(), name="淺草", latitude=35.7148, longitude=139.7967),
            None,
            "FEWER_TRANSFERS",
        )
        if segment is None:
            raise ConnectionError("NAVITIME 未回傳測試路線")
        return "NAVITIME 路線驗證成功"
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
    return PublicRuntimeConfig(
        google_maps_browser_key=settings.next_public_google_maps_browser_key,
        google_maps_enabled=bool(settings.google_maps_api_key),
    )
