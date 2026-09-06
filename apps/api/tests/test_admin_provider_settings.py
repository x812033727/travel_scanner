import logging
from datetime import datetime
from typing import Any

import fakeredis.aioredis
import pytest
from httpx import ASGITransport, AsyncClient

import app.admin.service as admin_service
from app.admin.schemas import ProviderSettingsUpdate
from app.admin.service import (
    _default_provider_enabled,
    _merge_secret_values,
    _safe_test_message,
    _test_google,
    _validate_provider_values,
    apply_runtime_overrides,
    decrypt_secrets,
    effective_registration_enabled,
    effective_site_visibility,
    encrypt_secrets,
    public_runtime_config,
    settings_snapshot,
    update_provider_settings,
)
from app.auth.service import current_user
from app.config import Settings
from app.main import app
from app.models import AdminAuditLog, ProviderConfig, User
from app.problems import AppError
from app.providers.usage_meter import record_google_maps_request, record_youtube_request
from app.trips.routing import GoogleRoutesProbeResult, NavitimeProbeResult, RoutePoint


class ScalarRows:
    def __init__(self, rows: list[Any]) -> None:
        self.rows = rows

    def all(self) -> list[Any]:
        return self.rows


class SnapshotSession:
    def __init__(self, providers: list[ProviderConfig]) -> None:
        self.providers = providers
        self.calls = 0

    async def scalars(self, _statement: object) -> ScalarRows:
        self.calls += 1
        return ScalarRows(self.providers if self.calls == 1 else [])


class RegistrationSession:
    def __init__(self, row: ProviderConfig | None) -> None:
        self.row = row

    async def scalar(self, _statement: object) -> ProviderConfig | None:
        return self.row


class UpdateSession:
    def __init__(self) -> None:
        self.added: list[object] = []
        self.committed = False

    async def scalar(self, _statement: object) -> None:
        return None

    def add(self, value: object) -> None:
        self.added.append(value)

    async def commit(self) -> None:
        self.committed = True


def test_provider_secrets_are_encrypted_and_round_trip() -> None:
    settings = Settings(
        app_secret_key="test-app-secret-at-least-thirty-two-characters",
        settings_encryption_key="dedicated-settings-key",
    )
    encrypted = encrypt_secrets({"google_maps_api_key": "server-secret-key"}, settings)
    assert encrypted is not None
    assert "server-secret-key" not in encrypted
    assert decrypt_secrets(encrypted, settings) == {"google_maps_api_key": "server-secret-key"}


def test_blank_secret_keeps_existing_value_and_null_clears_it() -> None:
    assert _merge_secret_values({"token": "original"}, {"token": "   "}) == {"token": "original"}
    assert _merge_secret_values({"token": "original"}, {"token": None}) == {}


def test_new_affiliate_provider_rows_default_to_disabled() -> None:
    assert not _default_provider_enabled("travelpayouts")
    assert not _default_provider_enabled("booking")
    assert not _default_provider_enabled("booking_demand")
    assert _default_provider_enabled("google_maps")


def test_the_runtime_row_carries_the_session_lifetimes() -> None:
    """Both fields are administrator-editable; the auth routes read them through
    load_runtime_settings, so a stored value must survive the override step."""
    base = Settings(app_secret_key="test-app-secret-at-least-thirty-two-characters")
    row = ProviderConfig(
        provider="runtime",
        enabled=True,
        config={"access_token_expire_minutes": 720, "session_absolute_max_days": 7},
        secret_config_encrypted=None,
    )
    effective = apply_runtime_overrides(base, [row])
    assert effective.access_token_expire_minutes == 720
    assert effective.session_absolute_max_days == 7


def test_database_provider_settings_override_environment_and_can_disable_provider() -> None:
    base = Settings(
        app_secret_key="test-app-secret-at-least-thirty-two-characters",
        google_maps_api_key="environment-key",
        route_cache_ttl_seconds=900,
    )
    row = ProviderConfig(
        provider="google_maps",
        enabled=True,
        config={"route_cache_ttl_seconds": 1800},
        secret_config_encrypted=encrypt_secrets({"google_maps_api_key": "database-key"}, base),
    )
    effective = apply_runtime_overrides(base, [row])
    assert effective.google_maps_api_key == "database-key"
    assert effective.route_cache_ttl_seconds == 1800

    row.enabled = False
    disabled = apply_runtime_overrides(base, [row])
    assert disabled.google_maps_api_key is None


def test_connection_failure_message_redacts_provider_secrets() -> None:
    settings = Settings(google_maps_api_key="secret-google-key")
    message = _safe_test_message(
        "google_maps",
        "request with secret-google-key was rejected",
        settings,
    )
    assert message == "request with *** was rejected"


def test_runtime_accepts_independent_hotel_provider_mode() -> None:
    validated = _validate_provider_values(
        "runtime",
        {},
        admin_service.ProviderSettingsUpdate(
            config={
                "travel_provider_mode": "amadeus",
                "flight_provider_mode": "auto",
                "hotel_provider_mode": "booking",
            }
        ),
    )

    assert validated["hotel_provider_mode"] == "booking"


def test_registration_defaults_to_open() -> None:
    assert Settings.model_construct().registration_enabled is True


def test_site_visibility_defaults_to_open() -> None:
    settings = Settings.model_construct()
    assert settings.hotspots_enabled is True
    assert settings.trips_enabled is True
    assert settings.alerts_enabled is True
    assert settings.flight_status_enabled is True
    assert settings.airline_fares_enabled is True
    assert settings.pricing_enabled is True


def test_registration_setting_rejects_non_boolean_values() -> None:
    with pytest.raises(AppError, match="registration_enabled 必須是布林值"):
        _validate_provider_values(
            "runtime",
            {},
            ProviderSettingsUpdate(config={"registration_enabled": 0}),
        )


def test_google_browser_map_safety_gate_rejects_non_boolean_values() -> None:
    with pytest.raises(AppError, match="google_maps_javascript_enabled 必須是布林值"):
        _validate_provider_values(
            "google_maps",
            {},
            ProviderSettingsUpdate(config={"google_maps_javascript_enabled": 1}),
        )


def test_layout_settings_reject_non_boolean_values() -> None:
    with pytest.raises(AppError, match="trips_enabled 必須是布林值"):
        _validate_provider_values(
            "layout",
            {},
            ProviderSettingsUpdate(config={"trips_enabled": 1}),
        )


@pytest.mark.asyncio
async def test_registration_database_value_overrides_environment_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        admin_service,
        "get_settings",
        lambda: Settings(registration_enabled=False),
    )
    assert not await effective_registration_enabled(RegistrationSession(None))  # type: ignore[arg-type]

    row = ProviderConfig(
        provider="runtime",
        enabled=True,
        config={"registration_enabled": True},
    )
    assert await effective_registration_enabled(RegistrationSession(row))  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_layout_database_values_override_environment_defaults(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        admin_service,
        "get_settings",
        lambda: Settings(trips_enabled=False, pricing_enabled=True),
    )
    environment = await effective_site_visibility(RegistrationSession(None))  # type: ignore[arg-type]
    assert environment.trips_enabled is False
    assert environment.pricing_enabled is True

    row = ProviderConfig(
        provider="layout",
        enabled=True,
        config={"trips_enabled": True, "pricing_enabled": False},
    )
    database = await effective_site_visibility(RegistrationSession(row))  # type: ignore[arg-type]
    assert database.trips_enabled is True
    assert database.pricing_enabled is False

    snapshot = await settings_snapshot(SnapshotSession([row]))  # type: ignore[arg-type]
    layout = next(item for item in snapshot.providers if item.provider == "layout")
    assert layout.config["trips_enabled"] is True
    assert layout.config["pricing_enabled"] is False
    assert layout.config_sources["trips_enabled"] == "database"
    assert layout.config_sources["alerts_enabled"] == "environment"


@pytest.mark.asyncio
async def test_runtime_update_uses_system_audit_without_sensitive_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected_snapshot = object()

    async def fake_snapshot(*_args: object) -> object:
        return expected_snapshot

    monkeypatch.setattr(admin_service, "settings_snapshot", fake_snapshot)
    session = UpdateSession()
    actor = User(
        id=admin_service.uuid4(),
        email="admin@example.com",
        password_hash="unused",
        is_admin=True,
    )

    result = await update_provider_settings(
        session,  # type: ignore[arg-type]
        "runtime",
        ProviderSettingsUpdate(
            config={"registration_enabled": False, "provider_timeout_seconds": 8}
        ),
        actor,
        object(),  # type: ignore[arg-type]
    )

    assert result is expected_snapshot
    assert session.committed
    row = next(item for item in session.added if isinstance(item, ProviderConfig))
    audit = next(item for item in session.added if isinstance(item, AdminAuditLog))
    assert row.config["registration_enabled"] is False
    assert audit.action == "system_settings_updated"
    assert audit.actor_user_id == actor.id
    assert audit.target == "runtime"
    assert audit.metadata_json == {
        "config_fields": ["provider_timeout_seconds", "registration_enabled"],
        "registration_enabled": False,
    }


@pytest.mark.asyncio
async def test_layout_update_records_changed_fields_and_effective_visibility(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected_snapshot = object()

    async def fake_snapshot(*_args: object) -> object:
        return expected_snapshot

    monkeypatch.setattr(admin_service, "settings_snapshot", fake_snapshot)
    session = UpdateSession()
    actor = User(
        id=admin_service.uuid4(),
        email="admin@example.com",
        password_hash="unused",
        is_admin=True,
    )

    result = await update_provider_settings(
        session,  # type: ignore[arg-type]
        "layout",
        ProviderSettingsUpdate(
            enabled=False,
            config={"trips_enabled": False, "pricing_enabled": True},
        ),
        actor,
        object(),  # type: ignore[arg-type]
    )

    assert result is expected_snapshot
    row = next(item for item in session.added if isinstance(item, ProviderConfig))
    audit = next(item for item in session.added if isinstance(item, AdminAuditLog))
    assert row.enabled is True
    assert audit.action == "layout_settings_updated"
    assert audit.target == "layout"
    assert audit.metadata_json == {
        "config_fields": ["pricing_enabled", "trips_enabled"],
        "visibility": {
            "hotspots_enabled": True,
            "trips_enabled": False,
            "alerts_enabled": True,
            "flight_status_enabled": True,
            "airline_fares_enabled": True,
            "pricing_enabled": True,
        },
    }


def test_booking_demand_environment_uses_only_official_v31_url() -> None:
    validated = _validate_provider_values(
        "booking_demand",
        {},
        admin_service.ProviderSettingsUpdate(
            config={
                "booking_demand_env": "production",
                "booking_demand_api_base_url": "https://demandapi-sandbox.booking.com/3.1",
                "booking_demand_affiliate_id": "12345",
                "booking_booker_country": "TW",
                "booking_language": "ZH-TW",
            }
        ),
    )
    assert validated["booking_demand_api_base_url"] == "https://demandapi.booking.com/3.1"
    assert validated["booking_booker_country"] == "tw"
    assert validated["booking_language"] == "zh-tw"

    with pytest.raises(AppError, match="Booking Demand API"):
        _validate_provider_values(
            "booking_demand",
            {},
            admin_service.ProviderSettingsUpdate(
                config={"booking_demand_api_base_url": "https://example.com/3.1"}
            ),
        )
    with pytest.raises(AppError, match="Booking Demand API"):
        _validate_provider_values(
            "booking_demand",
            {},
            admin_service.ProviderSettingsUpdate(
                config={"booking_demand_api_base_url": "https://demandapi.booking.com/3.1"}
            ),
        )


@pytest.mark.asyncio
async def test_google_connection_accepts_reachable_empty_route(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed_points: list[RoutePoint] = []

    class PlacesStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def autocomplete(self, *_args: object) -> list[dict[str, Any]]:
            return [{"place_id": "unstable-first-prediction"}]

    class RoutesStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def probe(
            self,
            origin: RoutePoint,
            destination: RoutePoint,
            _departure_time: datetime | None = None,
        ) -> GoogleRoutesProbeResult:
            observed_points.extend([origin, destination])
            return GoogleRoutesProbeResult(True, False, status_code=200)

    class WeatherStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def lookup(self, **_kwargs: object) -> object:
            return type("Weather", (), {"current": object(), "days": []})()

    monkeypatch.setattr(admin_service, "GoogleTravelService", PlacesStub)
    monkeypatch.setattr(admin_service, "GoogleRouteProvider", RoutesStub)
    monkeypatch.setattr(admin_service, "GoogleWeatherService", WeatherStub)

    message = await _test_google(Settings(google_maps_api_key="key"), object())  # type: ignore[arg-type]

    assert message == (
        "Google Places、Routes API 可連線；非日本測試路線目前無可用班次"
        "（日本大眾運輸使用 Ekispert 或 NAVITIME）；Weather API 連線成功"
    )
    assert observed_points[0].provider_place_id is None
    assert observed_points[0].latitude == 25.0478


@pytest.mark.asyncio
async def test_google_connection_reports_routes_http_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class PlacesStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def autocomplete(self, *_args: object) -> list[dict[str, Any]]:
            return [{"place_id": "tokyo"}]

    class RoutesStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def probe(
            self,
            _origin: RoutePoint,
            _destination: RoutePoint,
            _departure_time: datetime | None = None,
        ) -> GoogleRoutesProbeResult:
            return GoogleRoutesProbeResult(
                False,
                False,
                status_code=403,
                error_code="PERMISSION_DENIED",
            )

    monkeypatch.setattr(admin_service, "GoogleTravelService", PlacesStub)
    monkeypatch.setattr(admin_service, "GoogleRouteProvider", RoutesStub)

    with pytest.raises(
        ConnectionError,
        match=r"Routes API 連線失敗（HTTP 403 / PERMISSION_DENIED）",
    ):
        await _test_google(Settings(google_maps_api_key="key"), object())  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_google_connection_keeps_places_and_routes_ready_when_weather_is_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class PlacesStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def autocomplete(self, *_args: object) -> list[dict[str, Any]]:
            return [{"place_id": "tokyo"}]

    class RoutesStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def probe(
            self,
            _origin: RoutePoint,
            _destination: RoutePoint,
            _departure_time: datetime | None = None,
        ) -> GoogleRoutesProbeResult:
            return GoogleRoutesProbeResult(True, True, status_code=200)

    class WeatherStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def lookup(self, **_kwargs: object) -> object:
            raise AppError(503, "weather_api_not_enabled", "Weather API 尚未啟用")

    monkeypatch.setattr(admin_service, "GoogleTravelService", PlacesStub)
    monkeypatch.setattr(admin_service, "GoogleRouteProvider", RoutesStub)
    monkeypatch.setattr(admin_service, "GoogleWeatherService", WeatherStub)

    message = await _test_google(Settings(google_maps_api_key="key"), object())  # type: ignore[arg-type]

    assert "Routes API 可連線" in message
    assert "weather_api_not_enabled" in message
    assert "不影響地圖與路線" in message


@pytest.mark.asyncio
async def test_admin_snapshot_never_returns_plaintext_secret() -> None:
    base = Settings()
    secret = "google-key-that-must-not-leak"
    row = ProviderConfig(
        provider="google_maps",
        enabled=True,
        config={},
        secret_config_encrypted=encrypt_secrets({"google_maps_api_key": secret}, base),
    )
    snapshot = await settings_snapshot(SnapshotSession([row]))  # type: ignore[arg-type]
    payload = snapshot.model_dump_json()
    assert secret not in payload
    google = next(item for item in snapshot.providers if item.provider == "google_maps")
    assert google.secrets["google_maps_api_key"].masked == "••••••••leak"
    assert google.secrets["google_maps_api_key"].source == "database"


@pytest.mark.asyncio
async def test_admin_snapshot_lists_google_monthly_free_usage_by_sku() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    await record_google_maps_request(redis, "weather_current")
    await record_google_maps_request(redis, "weather_daily_forecast")
    row = ProviderConfig(
        provider="google_maps",
        enabled=True,
        config={
            "google_maps_essentials_free_limit": 100,
            "google_maps_enterprise_free_limit": 10,
        },
    )

    snapshot = await settings_snapshot(
        SnapshotSession([row]),  # type: ignore[arg-type]
        redis,
    )

    google = next(item for item in snapshot.providers if item.provider == "google_maps")
    assert google.usage is not None
    assert google.usage.used == 2
    weather = next(item for item in google.usage.sku_usage if item.sku == "weather_usage")
    assert weather.used == 2
    assert weather.free_limit == 100
    assert weather.free_remaining == 98
    assert len(google.usage.monthly_history) == 6
    await redis.aclose()


@pytest.mark.asyncio
async def test_admin_snapshot_lists_youtube_daily_allowance_and_usage() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    await record_youtube_request(redis, "search_list")
    await record_youtube_request(redis, "videos_list")
    row = ProviderConfig(
        provider="youtube_guides",
        enabled=True,
        config={
            "hotspot_guide_youtube_search_daily_free_limit": 50,
            "hotspot_guide_youtube_core_daily_free_limit": 500,
        },
    )

    snapshot = await settings_snapshot(
        SnapshotSession([row]),  # type: ignore[arg-type]
        redis,
    )

    youtube = next(item for item in snapshot.providers if item.provider == "youtube_guides")
    assert youtube.usage is not None
    assert youtube.usage.period_kind == "day"
    assert youtube.usage.used == 2
    search = next(item for item in youtube.usage.sku_usage if item.sku == "search_queries")
    core = next(item for item in youtube.usage.sku_usage if item.sku == "core_api_units")
    assert search.free_limit == 50
    assert search.free_remaining == 49
    assert core.free_limit == 500
    assert core.free_remaining == 499
    await redis.aclose()


@pytest.mark.asyncio
async def test_production_booking_is_not_marked_available_until_connection_test_passes() -> None:
    base = Settings()
    row = ProviderConfig(
        provider="booking_demand",
        enabled=True,
        config={
            "booking_demand_env": "production",
            "booking_demand_api_base_url": "https://demandapi.booking.com/3.1",
            "booking_demand_affiliate_id": "12345",
        },
        secret_config_encrypted=encrypt_secrets(
            {"booking_demand_api_token": "booking-production-secret"}, base
        ),
    )
    pending = await settings_snapshot(SnapshotSession([row]))  # type: ignore[arg-type]
    booking = next(item for item in pending.providers if item.provider == "booking_demand")
    assert booking.configured is False
    assert booking.status == "test_required"

    row.last_test_status = "success"
    ready = await settings_snapshot(SnapshotSession([row]))  # type: ignore[arg-type]
    booking = next(item for item in ready.providers if item.provider == "booking_demand")
    assert booking.configured is True
    assert booking.status == "ready"
    assert "booking-production-secret" not in ready.model_dump_json()


@pytest.mark.asyncio
async def test_ai_vendor_secrets_are_masked_and_shared_by_the_ai_features() -> None:
    base = Settings()
    secrets = {
        "openai_api_key": "openai-secret-ending-1234",
        "anthropic_api_key": "anthropic-secret-ending-5678",
    }
    vendors_row = ProviderConfig(
        provider="ai_vendors",
        enabled=True,
        config={},
        secret_config_encrypted=encrypt_secrets(secrets, base),
    )
    planner_row = ProviderConfig(
        provider="ai_planner", enabled=True, config={"ai_planner_mode": "auto"}
    )
    session = SnapshotSession([vendors_row, planner_row])
    snapshot = await settings_snapshot(session)  # type: ignore[arg-type]
    payload = snapshot.model_dump_json()
    assert all(secret not in payload for secret in secrets.values())
    vendors = next(item for item in snapshot.providers if item.provider == "ai_vendors")
    assert vendors.configured is True
    assert vendors.secrets["openai_api_key"].masked == "••••••••1234"
    assert vendors.secrets["anthropic_api_key"].source == "database"
    assert "MiniMax" in vendors.status_message and "Gemini" in vendors.status_message
    planner = next(item for item in snapshot.providers if item.provider == "ai_planner")
    assert planner.configured is True
    assert planner.secrets == {}
    assert "openai_api_base_url" not in planner.config
    search = next(item for item in snapshot.providers if item.provider == "ai_guide_search")
    assert search.secrets == {}


@pytest.mark.asyncio
async def test_snapshot_exposes_model_catalog_options() -> None:
    snapshot = await settings_snapshot(SnapshotSession([]))  # type: ignore[arg-type]
    by_provider = {item.provider: item for item in snapshot.providers}
    planner = by_provider["ai_planner"]
    assert set(planner.field_options) == {
        "openai_model",
        "anthropic_model",
        "minimax_model",
        "gemini_model",
    }
    assert "gemini-3.8-flash" in [
        option.value for option in planner.field_options["gemini_model"]
    ]
    assert Settings().openai_model in [
        option.value for option in planner.field_options["openai_model"]
    ]
    assert set(by_provider["ai_guide_search"].field_options) == {
        "hotspot_guide_ai_openai_model",
        "hotspot_guide_ai_anthropic_model",
        "hotspot_guide_ai_minimax_model",
        "hotspot_guide_ai_gemini_model",
    }
    gemini = by_provider["gemini_guides"].field_options["hotspot_guide_gemini_model"]
    assert "gemini-3.8-flash" in [option.value for option in gemini]
    assert all(option.label for option in gemini)
    assert by_provider["ai_vendors"].field_options == {}
    assert by_provider["google_maps"].field_options == {}


def test_ai_vendors_rejects_non_official_base_url_and_planner_rejects_moved_fields() -> None:
    with pytest.raises(AppError) as host_error:
        _validate_provider_values(
            "ai_vendors",
            {},
            ProviderSettingsUpdate(config={"openai_api_base_url": "https://attacker.example/v1"}),
        )
    assert getattr(host_error.value, "code", None) == "provider_setting_invalid"

    with pytest.raises(AppError) as moved_config:
        _validate_provider_values(
            "ai_planner",
            {},
            ProviderSettingsUpdate(config={"openai_api_base_url": "https://api.openai.com/v1"}),
        )
    assert getattr(moved_config.value, "code", None) == "provider_setting_unknown"

    with pytest.raises(AppError) as moved_secret:
        _validate_provider_values(
            "ai_planner", {}, ProviderSettingsUpdate(secrets={"openai_api_key": "sk-new"})
        )
    assert getattr(moved_secret.value, "code", None) == "provider_setting_unknown"

    with pytest.raises(AppError) as priority_error:
        _validate_provider_values(
            "ai_planner",
            {},
            ProviderSettingsUpdate(config={"ai_planner_priority": "openai,openai"}),
        )
    assert getattr(priority_error.value, "code", None) == "provider_setting_invalid"


def test_gemini_is_a_valid_planner_and_guide_search_choice() -> None:
    validated = _validate_provider_values(
        "ai_planner",
        {},
        ProviderSettingsUpdate(
            config={
                "ai_planner_mode": "gemini",
                "ai_planner_priority": "gemini,openai,anthropic,minimax",
                "gemini_model": " gemini-3.5-flash ",
            }
        ),
    )
    assert validated["ai_planner_mode"] == "gemini"
    assert validated["gemini_model"] == "gemini-3.5-flash"
    search = _validate_provider_values(
        "ai_guide_search",
        {},
        ProviderSettingsUpdate(
            config={
                "hotspot_guide_ai_default_provider": "gemini",
                "hotspot_guide_ai_gemini_model": "",
            }
        ),
    )
    assert search["hotspot_guide_ai_default_provider"] == "gemini"
    assert "hotspot_guide_ai_gemini_model" not in search


def test_ai_card_status_reports_gemini_through_the_shared_guide_key() -> None:
    from app.admin.service import _configured

    settings = Settings(
        ai_planner_mode="auto",
        ai_planner_priority="gemini,openai",
        openai_api_key="sk-test",
        anthropic_api_key=None,
        minimax_api_key=None,
        hotspot_guide_gemini_api_key="g-key",
        gemini_model="gemini-3.8-flash",
        hotspot_guide_ai_default_provider="gemini",
        hotspot_guide_ai_gemini_model=None,
        hotspot_guide_brave_enabled=True,
        hotspot_guide_brave_api_key="brave-key",
    )
    configured, status, message = _configured("ai_planner", settings)
    assert (configured, status) == (True, "ready")
    assert message == f"自動備援：Gemini（gemini-3.8-flash） → OpenAI（{settings.openai_model}）"

    pinned = settings.model_copy(update={"ai_planner_mode": "gemini"})
    assert _configured("ai_planner", pinned) == (True, "ready", "指定 Gemini（gemini-3.8-flash）")
    unkeyed = pinned.model_copy(update={"hotspot_guide_gemini_api_key": None})
    assert _configured("ai_planner", unkeyed)[:2] == (False, "not_configured")

    search_ok, search_status, search_message = _configured("ai_guide_search", settings)
    assert (search_ok, search_status) == (True, "ready")
    assert search_message.startswith("預設 gemini（gemini-3.8-flash）")
    assert _configured("ai_guide_search", unkeyed)[:2] == (False, "not_configured")


def test_model_fields_accept_catalog_or_custom_ids_and_reject_path_characters() -> None:
    validated = _validate_provider_values(
        "ai_planner",
        {},
        ProviderSettingsUpdate(
            config={
                "openai_model": " gpt-5.6-terra ",
                "anthropic_model": "ft:claude-sonnet-5:org:x",
            }
        ),
    )
    assert validated["openai_model"] == "gpt-5.6-terra"
    assert validated["anthropic_model"] == "ft:claude-sonnet-5:org:x"

    for bad in ("gpt/../admin", "a" * 129, "model name", ""):
        with pytest.raises(AppError) as error:
            _validate_provider_values(
                "ai_planner", {}, ProviderSettingsUpdate(config={"openai_model": bad})
            )
        assert getattr(error.value, "code", None) == "provider_setting_invalid", bad

    current = {"hotspot_guide_ai_openai_model": "gpt-5.6-terra"}
    cleared = _validate_provider_values(
        "ai_guide_search",
        current,
        ProviderSettingsUpdate(config={"hotspot_guide_ai_openai_model": "  "}),
    )
    assert "hotspot_guide_ai_openai_model" not in cleared
    removed = _validate_provider_values(
        "ai_guide_search",
        current,
        ProviderSettingsUpdate(config={"hotspot_guide_ai_openai_model": None}),
    )
    assert "hotspot_guide_ai_openai_model" not in removed


def test_ai_vendors_row_never_disables_its_secrets() -> None:
    base = Settings()
    row = ProviderConfig(
        provider="ai_vendors",
        enabled=False,
        config={},
        secret_config_encrypted=encrypt_secrets({"minimax_api_key": "mm-key"}, base),
    )
    assert apply_runtime_overrides(base, [row]).minimax_api_key == "mm-key"


@pytest.mark.asyncio
async def test_updating_ai_vendors_keeps_the_row_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    expected_snapshot = object()

    async def fake_snapshot(*_args: object) -> object:
        return expected_snapshot

    monkeypatch.setattr(admin_service, "settings_snapshot", fake_snapshot)
    session = UpdateSession()
    actor = User(
        id=admin_service.uuid4(),
        email="admin@example.com",
        password_hash="unused",
        is_admin=True,
    )

    result = await update_provider_settings(
        session,  # type: ignore[arg-type]
        "ai_vendors",
        ProviderSettingsUpdate(enabled=False, secrets={"openai_api_key": "sk-new"}),
        actor,
        object(),  # type: ignore[arg-type]
    )

    assert result is expected_snapshot
    row = next(item for item in session.added if isinstance(item, ProviderConfig))
    audit = next(item for item in session.added if isinstance(item, AdminAuditLog))
    assert row.enabled is True
    assert "sk-new" not in (row.secret_config_encrypted or "")
    assert decrypt_secrets(row.secret_config_encrypted) == {"openai_api_key": "sk-new"}
    assert audit.action == "provider_settings_updated"
    assert audit.target == "ai_vendors"
    assert audit.metadata_json["secret_fields"] == ["openai_api_key"]


def test_disabling_the_planner_keeps_the_guide_search_keys() -> None:
    from app.hotspots.ai_search import configured_research_providers

    base = Settings()
    vendors = ProviderConfig(
        provider="ai_vendors",
        enabled=True,
        config={},
        secret_config_encrypted=encrypt_secrets({"openai_api_key": "sk-shared"}, base),
    )
    planner = ProviderConfig(provider="ai_planner", enabled=False, config={})
    effective = apply_runtime_overrides(base, [vendors, planner])
    assert effective.openai_api_key == "sk-shared"
    assert effective.ai_planner_enabled is False
    assert configured_research_providers(effective)["openai"] is True


@pytest.mark.asyncio
async def test_legacy_planner_row_is_flagged_until_migrated(
    caplog: pytest.LogCaptureFixture,
) -> None:
    base = Settings()
    row = ProviderConfig(
        provider="ai_planner",
        enabled=True,
        config={"openai_api_base_url": "https://api.openai.com/v1"},
        secret_config_encrypted=encrypt_secrets({"openai_api_key": "sk-legacy"}, base),
    )
    with caplog.at_level(logging.WARNING):
        snapshot = await settings_snapshot(SnapshotSession([row]))  # type: ignore[arg-type]
    planner = next(item for item in snapshot.providers if item.provider == "ai_planner")
    assert "migration 0047" in planner.status_message
    assert "openai_api_base_url" in planner.status_message
    assert "openai_api_key" in planner.status_message
    assert "sk-legacy" not in snapshot.model_dump_json()
    assert any("moved AI vendor fields" in record.getMessage() for record in caplog.records)


def test_feature_test_messages_redact_vendor_secrets() -> None:
    settings = Settings(
        openai_api_key="secret-openai-key", hotspot_guide_gemini_api_key="secret-gemini-key"
    )
    for provider in ("ai_planner", "ai_guide_search", "gemini_guides", "ai_vendors"):
        message = _safe_test_message(
            provider, "secret-openai-key and secret-gemini-key leaked", settings
        )
        assert "secret-openai-key" not in message, provider
        assert "secret-gemini-key" not in message, provider


@pytest.mark.asyncio
async def test_ai_vendors_connection_test_probes_each_configured_vendor() -> None:
    import httpx

    seen: list[tuple[str, str, dict[str, str]]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append((request.url.host, request.url.path, dict(request.headers)))
        if request.url.host == "api.openai.com":
            return httpx.Response(200, json={"data": [{"id": "gpt-5.6-terra"}]})
        if request.url.host == "api.anthropic.com":
            return httpx.Response(200, json={"data": [{"id": "claude-opus-5"}]})
        if request.url.host == "api.minimaxi.com":
            return httpx.Response(404, json={"error": "not found"})
        return httpx.Response(200, json={"models": [{"name": "models/gemini-3.8-flash"}]})

    settings = Settings(
        openai_api_key="sk-openai",
        anthropic_api_key="sk-anthropic",
        minimax_api_key="sk-minimax",
        hotspot_guide_gemini_api_key="g-key",
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        message = await admin_service._test_ai_vendors(settings, client)
    assert "OpenAI ✓（gpt-5.6-terra）" in message
    assert "金鑰有效，模型清單未列出 claude-sonnet-5" in message
    assert "MiniMax 已設定" in message
    assert "Gemini ✓（gemini-3.8-flash）" in message
    assert "sk-openai" not in message
    assert {(host, path) for host, path, _ in seen} == {
        ("api.openai.com", "/v1/models"),
        ("api.anthropic.com", "/v1/models"),
        ("api.minimaxi.com", "/v1/models"),
        ("generativelanguage.googleapis.com", "/v1beta/models"),
    }
    anthropic_headers = next(headers for host, _, headers in seen if host == "api.anthropic.com")
    assert anthropic_headers["anthropic-version"] == "2023-06-01"
    assert anthropic_headers["x-api-key"] == "sk-anthropic"

    def unauthorized(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"error": "bad key"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(unauthorized)) as client:
        with pytest.raises(ConnectionError) as error:
            await admin_service._test_ai_vendors(Settings(openai_api_key="sk-openai"), client)
    assert "OpenAI 驗證失敗（HTTP 401）" in str(error.value)

    nothing = Settings(
        openai_api_key=None,
        anthropic_api_key=None,
        minimax_api_key=None,
        hotspot_guide_gemini_api_key=None,
    )
    with pytest.raises(ConnectionError):
        await admin_service._test_ai_vendors(nothing, None)


def test_hotspot_guides_status_reports_its_own_sources() -> None:
    from app.admin.service import _configured

    nothing = Settings(
        hotspot_guide_youtube_api_key=None,
        hotspot_guide_brave_api_key=None,
        hotspot_guide_gemini_api_key=None,
    )
    configured, status, message = _configured("hotspot_guides", nothing)
    assert configured is False and status == "not_configured"
    assert "NAVITIME" not in message
    ready, status, message = _configured(
        "hotspot_guides",
        Settings(hotspot_guide_youtube_enabled=True, hotspot_guide_youtube_api_key="yt-key"),
    )
    assert ready is True and status == "ready"
    assert "YouTube" in message


@pytest.mark.asyncio
async def test_admin_api_rejects_regular_user() -> None:
    user = User(
        email="member@example.com",
        password_hash="unused",
        is_active=True,
        is_admin=False,
    )
    app.dependency_overrides[current_user] = lambda: user
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v1/admin/provider-settings")
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 403
    assert response.json()["code"] == "admin_required"


@pytest.mark.asyncio
async def test_public_runtime_keeps_browser_map_disabled_until_explicitly_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def runtime(_session: object) -> Settings:
        return Settings(
            google_maps_api_key="server-key",
            next_public_google_maps_browser_key="browser-key",
        )

    monkeypatch.setattr(admin_service, "load_runtime_settings", runtime)
    result = await public_runtime_config(object())  # type: ignore[arg-type]
    assert result.google_routes_enabled is True
    assert result.google_places_enabled is True
    assert result.google_maps_embed_enabled is False
    assert result.google_maps_javascript_enabled is False
    # With the safety gate off, the browser key stays home too: nothing may load a map.
    assert result.google_maps_browser_key is None
    assert result.navitime_enabled is False
    assert result.ekispert_enabled is False
    assert result.odsay_enabled is False
    assert result.naver_maps_enabled is False
    assert result.naver_maps_browser_client_id is None


@pytest.mark.asyncio
async def test_public_runtime_enables_browser_map_only_with_key_and_safety_gate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def runtime(_session: object) -> Settings:
        return Settings(
            next_public_google_maps_browser_key="browser-key",
            google_maps_javascript_enabled=True,
        )

    monkeypatch.setattr(admin_service, "load_runtime_settings", runtime)
    result = await public_runtime_config(object())  # type: ignore[arg-type]
    assert result.google_maps_embed_enabled is True
    assert result.google_maps_javascript_enabled is True
    assert result.google_maps_browser_key == "browser-key"


@pytest.mark.asyncio
async def test_public_runtime_does_not_enable_browser_map_without_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def runtime(_session: object) -> Settings:
        return Settings(google_maps_javascript_enabled=True)

    monkeypatch.setattr(admin_service, "load_runtime_settings", runtime)
    result = await public_runtime_config(object())  # type: ignore[arg-type]
    assert result.google_maps_embed_enabled is False
    assert result.google_maps_javascript_enabled is False


@pytest.mark.asyncio
async def test_public_runtime_exposes_naver_browser_capabilities_but_not_secret(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def runtime(_session: object) -> Settings:
        return Settings(
            naver_maps_client_id="public-browser-id",
            naver_maps_client_secret="never-expose-this-secret",
        )

    monkeypatch.setattr(admin_service, "load_runtime_settings", runtime)
    result = await public_runtime_config(object())  # type: ignore[arg-type]
    payload = result.model_dump(mode="json")
    assert payload["naver_maps_browser_client_id"] == "public-browser-id"
    assert payload["naver_maps_enabled"] is True
    assert payload["naver_places_enabled"] is True
    assert payload["naver_directions_enabled"] is True
    assert payload["naver_dynamic_map_enabled"] is True
    assert "never-expose-this-secret" not in str(payload)
    assert "naver_maps_client_secret" not in payload


@pytest.mark.asyncio
async def test_public_runtime_exposes_transit_provider_capabilities_without_keys(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def runtime(_session: object) -> Settings:
        return Settings(ekispert_api_key="japan-secret", odsay_api_key="korea-secret")

    monkeypatch.setattr(admin_service, "load_runtime_settings", runtime)
    payload = (await public_runtime_config(object())).model_dump(mode="json")  # type: ignore[arg-type]
    assert payload["ekispert_enabled"] is True
    assert payload["odsay_enabled"] is True
    assert "japan-secret" not in str(payload)
    assert "korea-secret" not in str(payload)


@pytest.mark.parametrize(
    ("provider", "field", "value"),
    [
        ("flightaware", "flightaware_base_url", "https://attacker.example/aeroapi"),
        ("skyscanner", "skyscanner_base_url", "https://partners.api.skyscanner.net.evil.example"),
        ("duffel", "duffel_base_url", "http://api.duffel.com"),
        ("google_travel_impact", "google_travel_impact_base_url", "https://attacker.example/v1"),
        ("ekispert", "ekispert_api_base_url", "https://api.ekispert.jp.evil.example"),
        ("odsay", "odsay_api_base_url", "http://api.odsay.com/v1/api"),
        ("travelpayouts", "travelpayouts_api_base_url", "https://attacker.example"),
    ],
)
def test_credentialed_provider_base_urls_must_stay_on_official_hosts(
    provider: str, field: str, value: str
) -> None:
    with pytest.raises(AppError) as error:
        _validate_provider_values(provider, {}, ProviderSettingsUpdate(config={field: value}))
    assert error.value.code == "provider_setting_invalid"


def test_official_provider_base_urls_are_accepted() -> None:
    validated = _validate_provider_values(
        "flightaware",
        {},
        ProviderSettingsUpdate(
            config={"flightaware_base_url": "https://aeroapi.flightaware.com/aeroapi"}
        ),
    )
    assert validated["flightaware_base_url"] == "https://aeroapi.flightaware.com/aeroapi"


def test_stored_provider_base_url_on_unofficial_host_is_ignored_when_read() -> None:
    base = Settings(
        app_secret_key="test-app-secret-at-least-thirty-two-characters",
        flightaware_api_key="environment-key",
    )
    row = ProviderConfig(
        provider="flightaware",
        enabled=True,
        config={
            "flightaware_base_url": "https://attacker.example/aeroapi",
            "flightaware_enrich_offer_limit": 3,
        },
    )
    effective = apply_runtime_overrides(base, [row])
    assert effective.flightaware_base_url == base.flightaware_base_url
    assert effective.flightaware_enrich_offer_limit == 3


@pytest.mark.asyncio
async def test_navitime_connection_reports_gateway_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class NavitimeStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def probe(
            self,
            _origin: RoutePoint,
            _destination: RoutePoint,
            _departure_time: datetime | None = None,
        ) -> NavitimeProbeResult:
            return NavitimeProbeResult(
                False,
                False,
                status_code=403,
                error_code="You are not subscribed to this API.",
            )

    monkeypatch.setattr(admin_service, "NavitimeRouteProvider", NavitimeStub)
    settings = Settings(
        navitime_api_base_url="https://navitime-route-totalnavi.p.rapidapi.com",
        navitime_api_key="key",
    )

    with pytest.raises(
        ConnectionError,
        match=r"NAVITIME（RapidAPI）連線失敗（HTTP 403 / You are not subscribed to this API.）",
    ):
        await admin_service._test_provider("navitime", settings, object())  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_navitime_connection_succeeds_through_rapidapi(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: list[RoutePoint] = []

    class NavitimeStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def probe(
            self,
            origin: RoutePoint,
            destination: RoutePoint,
            _departure_time: datetime | None = None,
        ) -> NavitimeProbeResult:
            observed.extend([origin, destination])
            return NavitimeProbeResult(True, True, status_code=200)

    monkeypatch.setattr(admin_service, "NavitimeRouteProvider", NavitimeStub)
    settings = Settings(
        navitime_api_base_url="https://navitime-route-totalnavi.p.rapidapi.com",
        navitime_api_key="key",
    )

    message = await admin_service._test_provider("navitime", settings, object())  # type: ignore[arg-type]

    assert message == "NAVITIME（RapidAPI）路線驗證成功"
    assert [item.name for item in observed] == ["東京", "淺草"]
    assert admin_service._configured("navitime", settings)[2] == "NAVITIME 憑證已設定（RapidAPI）"
    assert admin_service._configured("navitime", Settings())[2] == (
        "缺少 API Base URL 或 API key；直接契約另需 Client ID"
    )
