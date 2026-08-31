from __future__ import annotations

import base64
import hashlib
import json
import time
from dataclasses import dataclass
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
    PublicRuntimeConfig,
    SecretState,
)
from app.config import Settings, get_settings
from app.models import AdminAuditLog, ProviderConfig, User
from app.places.google import GoogleTravelService
from app.problems import AppError
from app.providers.amadeus import AmadeusProvider
from app.providers.skyscanner import SkyscannerProvider
from app.search.schemas import SearchCreate
from app.trips.routing import (
    GoogleRouteProvider,
    NavitimeRouteProvider,
    RoutePoint,
)


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
            "provider_timeout_seconds",
            "provider_failure_threshold",
            "provider_circuit_seconds",
        ),
        (),
    ),
    "google_maps": ProviderDefinition(
        "Google Maps",
        "Google Places 地點搜尋、Routes 大眾運輸路線與瀏覽器 Embed 地圖。",
        ("route_cache_ttl_seconds",),
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
        "住宿 affiliate ID 導流，並預留 Demand API sandbox／production 設定。",
        (
            "booking_affiliate_id",
            "booking_affiliate_url_template",
            "booking_allowed_hosts",
            "booking_demand_api_base_url",
        ),
        ("booking_demand_api_token",),
        "booking_enabled",
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
        return True, "ready", "執行模式設定已套用"
    if provider == "google_maps":
        configured = bool(settings.google_maps_api_key)
        browser = bool(settings.next_public_google_maps_browser_key)
        message = (
            "Places 與 Routes 已設定；Embed 地圖已設定"
            if configured and browser
            else "Places 與 Routes 已設定；Embed 地圖尚未設定"
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


async def settings_snapshot(session: AsyncSession) -> ProviderSettingsSnapshot:
    base = get_settings()
    rows = await provider_rows(session)
    by_provider = {row.provider: row for row in rows}
    effective = apply_runtime_overrides(base, rows)
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
        "flight_provider_mode": {"auto", "skyscanner", "amadeus", "mock", "disabled"},
        "amadeus_env": {"test", "production"},
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
    if "skyscanner_market" in merged:
        merged["skyscanner_market"] = str(merged["skyscanner_market"]).upper()
    if "skyscanner_currency" in merged:
        merged["skyscanner_currency"] = str(merged["skyscanner_currency"]).upper()
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
    stored = decrypt_secrets(row.secret_config_encrypted)
    for field, value in payload.secrets.items():
        if value is None:
            stored.pop(field, None)
            continue
        cleaned = value.strip()
        if not cleaned or len(cleaned) > 2048:
            raise AppError(422, "provider_secret_invalid", f"{field} 金鑰格式不正確")
        stored[field] = cleaned
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
    return await settings_snapshot(session)


async def _test_google(settings: Settings, redis: Redis) -> str:
    service = GoogleTravelService(redis, settings)
    places = await service.autocomplete("東京車站", None, ["jp"])
    if not places:
        raise ConnectionError("Places API 未回傳結果，請檢查 API 啟用狀態與金鑰限制")
    routes = await GoogleRouteProvider(settings).probe(
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
    if not routes.route_available:
        return "Google Places 與 Routes API 連線成功；測試路線目前無可用班次"
    return "Google Places 與 Routes 連線成功"


async def _test_provider(provider: str, settings: Settings, redis: Redis) -> str:
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
            modules=["flight"],
        )
        await SkyscannerProvider(redis, settings).start_search(query)
        return "Skyscanner Live Flights 驗證成功"
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
