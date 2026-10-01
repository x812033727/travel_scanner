"""The Studio uploader connection, owned by the video settings card.

ProviderConfig supplies existing encrypted storage; this private provider is deliberately
absent from the generic provider editor. No Google credential or desktop password is stored.
Each caller passes its session and retains one Config for the entire remote operation.
"""

from __future__ import annotations

import hashlib
import ipaddress
import os
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, cast
from urllib.parse import urlsplit, urlunsplit

from pydantic import BaseModel, ConfigDict, Field, SecretStr
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import decrypt_secrets, encrypt_secrets
from app.models import AdminAuditLog, ProviderConfig, User
from app.video_youtube.errors import Refused

if TYPE_CHECKING:
    from app.video_youtube.vps import Config

PROVIDER = "video_vps_uploader"
CHANNEL = re.compile(r"^UC[A-Za-z0-9_-]{22}$")
PRIVATE_NETWORKS = tuple(
    ipaddress.ip_network(value)
    for value in (
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
        "127.0.0.0/8",
        "::1/128",
        "fc00::/7",
    )
)
PRIVATE_HOSTS = {"localhost", "mokaair-studio-uploader"}
DEFAULT_DESKTOP = "http://127.0.0.1:6080/vnc.html"


class SettingsIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_updated_at: datetime | None
    enabled: bool | None = None
    url: str | None = Field(default=None, max_length=500)
    channel_id: str | None = Field(default=None, max_length=64)
    desktop_url: str | None = Field(default=None, max_length=500)
    secret: SecretStr | None = None


class SettingsView(BaseModel):
    enabled: bool
    url: str
    channel_id: str
    desktop_url: str
    secret_set: bool
    configured: bool
    source: Literal["database", "environment", "none"]
    updated_at: datetime | None
    last_test_status: str | None = None
    last_test_message: str | None = None
    last_tested_at: datetime | None = None
    browser_status: str | None = None
    active_jobs: int | None = None


def _url(value: str, *, desktop: bool = False) -> str:
    value = value.strip()
    if not value:
        return ""
    try:
        parsed = urlsplit(value)
        hostname, port = parsed.hostname, parsed.port
        if (
            parsed.scheme not in {"http", "https"}
            or not hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
            or (not desktop and parsed.path not in ("", "/"))
            or any(character.isspace() or ord(character) < 32 for character in value)
            or "\\" in value
            or port == 0
        ):
            raise ValueError
        try:
            address = ipaddress.ip_address(hostname)
        except ValueError:
            address = None
            if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?", hostname):
                raise ValueError from None
        if address is not None and (
            address.is_link_local
            or address.is_multicast
            or address.is_unspecified
            or address.is_reserved
            and not address.is_loopback
        ):
            raise ValueError
        # A private RPC is intentional; public plaintext and metadata endpoints are not.
        private = hostname.lower() in PRIVATE_HOSTS or (
            address is not None and any(address in network for network in PRIVATE_NETWORKS)
        )
        if parsed.scheme == "http" and not private:
            raise ValueError
        if hostname.lower() in {"metadata.google.internal", "metadata.goog"}:
            raise ValueError
        host = f"[{hostname.lower()}]" if ":" in hostname else hostname.lower()
        default_port = 443 if parsed.scheme == "https" else 80
        authority = host if port in (None, default_port) else f"{host}:{port}"
        return urlunsplit((parsed.scheme, authority, parsed.path if desktop else "", "", ""))
    except ValueError:
        raise Refused(
            422, "vps_url_invalid", "請使用安全的 VPS 網址；服務網址不能含路徑、帳密或查詢參數"
        ) from None


def rpc_url(value: str) -> str:
    return _url(value)


def _stamp(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


async def _row(session: AsyncSession, *, lock: bool = False) -> ProviderConfig | None:
    with session.no_autoflush:
        if lock and session.get_bind().dialect.name == "postgresql":
            # Serialize the first save too, and hold configuration through a job creation.
            key = int.from_bytes(
                hashlib.sha256(f"provider-settings:{PROVIDER}".encode()).digest()[:8], signed=True
            )
            await session.execute(select(func.pg_advisory_xact_lock(key)))
        statement = select(ProviderConfig).where(ProviderConfig.provider == PROVIDER)
        if lock:
            statement = statement.with_for_update().execution_options(populate_existing=True)
        return cast(ProviderConfig | None, await session.scalar(statement))


def _values(row: ProviderConfig | None) -> tuple[dict[str, Any], str, str]:
    if row is not None and not row.config.get("inherit_environment"):
        return (
            {**row.config, "enabled": row.enabled},
            decrypt_secrets(row.secret_config_encrypted).get("secret", ""),
            "database",
        )
    # A test-only row can retain diagnostics without making environment fallback sticky.
    url = os.getenv("MOKAAIR_VPS_UPLOADER_URL", "").rstrip("/")
    try:
        secret = (
            Path(os.environ["MOKAAIR_VPS_UPLOADER_SECRET_FILE"]).read_text().strip() if url else ""
        )
    except (KeyError, OSError):
        # Show an incomplete legacy configuration on the card. Operational resolution and
        # connection changes still fail closed when the old service cannot be verified.
        secret = ""
    return (
        {
            "enabled": bool(url),
            "url": url,
            "channel_id": os.getenv("MOKAAIR_VPS_UPLOADER_CHANNEL_ID", ""),
            "desktop_url": os.getenv("MOKAAIR_VPS_UPLOADER_DESKTOP_URL", DEFAULT_DESKTOP),
        },
        secret,
        "environment" if url else "none",
    )


def _config(values: dict[str, Any], secret: str) -> Config | None:
    from app.video_youtube.vps import Config

    if not values.get("enabled"):
        return None
    url = rpc_url(str(values.get("url") or ""))
    channel = str(values.get("channel_id") or "")
    if (
        not url
        or not CHANNEL.fullmatch(channel)
        or not 32 <= len(secret) <= 2048
        or any(character.isspace() for character in secret)
    ):
        raise Refused(503, "vps_not_configured", "VPS 上傳服務尚未完成設定")
    return Config(url, secret, channel)


async def resolve(session: AsyncSession, *, lock: bool = False) -> Config | None:
    values, secret, _source = _values(await _row(session, lock=lock))
    return _config(values, secret)


def _view(row: ProviderConfig | None) -> SettingsView:
    values, secret, source = _values(row)
    try:
        configured = _config({**values, "enabled": True}, secret) is not None
    except Refused:
        configured = False
    # Invalid legacy URLs can contain credentials or executable schemes. Do not echo them
    # into a text field or an "open desktop" link, even when reporting incomplete setup.
    safe_urls = {}
    for field in ("url", "desktop_url"):
        try:
            safe_urls[field] = _url(str(values.get(field) or ""), desktop=field == "desktop_url")
        except Refused:
            safe_urls[field] = ""
    return SettingsView(
        enabled=bool(values.get("enabled")),
        url=safe_urls["url"],
        channel_id=str(values.get("channel_id") or ""),
        desktop_url=safe_urls["desktop_url"],
        secret_set=bool(secret),
        configured=configured,
        source=source,
        updated_at=_stamp(row.updated_at) if row else None,
        last_test_status=row.last_test_status if row else None,
        last_test_message=row.last_test_message if row else None,
        last_tested_at=_stamp(row.last_tested_at) if row else None,
    )


async def view(session: AsyncSession) -> SettingsView:
    return _view(await _row(session))


async def probe(settings: Config, *, require_channel_match: bool = True) -> dict[str, Any]:
    from app.video_youtube import vps

    result = await vps.remote("GET", "/status", settings=settings)
    reported_channel = result.get("channel_id")
    if not isinstance(reported_channel, str) or not CHANNEL.fullmatch(reported_channel):
        raise Refused(409, "vps_status_invalid", "VPS 未回報有效的頻道設定，請先核對服務")
    if require_channel_match and reported_channel != settings.channel:
        raise Refused(409, "vps_channel_mismatch", "VPS 設定的頻道與網站不同，請先核對")
    active = result.get("active_jobs")
    return {
        "browser_status": result.get("browser")
        if result.get("browser") in ("idle", "working", "stopped")
        else None,
        "active_jobs": active if type(active) is int and active >= 0 else None,
    }


def _audit(session: AsyncSession, user: User, action: str, **values: Any) -> None:
    session.add(
        AdminAuditLog(actor_user_id=user.id, action=action, target=PROVIDER, metadata_json=values)
    )


async def save(session: AsyncSession, user: User, payload: SettingsIn) -> SettingsView:
    row = await _row(session, lock=True)
    if _stamp(payload.expected_updated_at) != (_stamp(row.updated_at) if row else None):
        raise Refused(409, "vps_settings_conflict", "設定已被其他管理員更新，請重新載入後再儲存")
    current, old_secret, _source = _values(row)
    values = {key: current.get(key) for key in ("enabled", "url", "channel_id", "desktop_url")}
    for field in ("url", "channel_id", "desktop_url"):
        if field in payload.model_fields_set:
            values[field] = (getattr(payload, field) or "").strip()
    if payload.enabled is not None:
        values["enabled"] = payload.enabled
    values["url"] = rpc_url(str(values.get("url") or ""))
    values["desktop_url"] = _url(str(values.get("desktop_url") or ""), desktop=True)
    if values["channel_id"] and not CHANNEL.fullmatch(values["channel_id"]):
        raise Refused(422, "vps_channel_invalid", "請填入有效的 YouTube 頻道 ID")
    supplied = payload.secret.get_secret_value().strip() if payload.secret is not None else ""
    if supplied and (
        not 32 <= len(supplied) <= 2048 or any(character.isspace() for character in supplied)
    ):
        raise Refused(422, "vps_secret_invalid", "服務密鑰須為 32 至 2048 個非空白字元")
    if values["url"] != rpc_url(str(current.get("url") or "")) and old_secret and not supplied:
        raise Refused(422, "vps_secret_required", "更換服務網址時，請重新填入該服務的密鑰")
    secret = supplied or old_secret
    _config(values, secret)
    old = _config(current, old_secret)
    if old is not None and (
        not values["enabled"]
        or values["url"] != old.url
        or values["channel_id"] != old.channel
        or secret != old.secret
    ):
        # An empty authenticated queue permits correcting a mistyped channel ID.
        # Connection tests still require the configured and reported channels to match.
        if (await probe(old, require_channel_match=False))["active_jobs"] != 0:
            raise Refused(
                409, "vps_settings_busy", "原 VPS 尚有未完成工作或無法確認佇列，請先處理原工作"
            )
    if row is None:
        row = ProviderConfig(provider=PROVIDER, priority=100, config={})
        session.add(row)
    row.config = {key: values[key] for key in ("url", "channel_id", "desktop_url")}
    row.enabled = bool(values["enabled"])
    row.secret_config_encrypted = encrypt_secrets({"secret": secret}) if secret else None
    row.updated_by_user_id = user.id
    moment = datetime.now(UTC)
    previous = _stamp(row.updated_at)
    row.updated_at = max(moment, previous + timedelta(microseconds=1)) if previous else moment
    row.last_tested_at = row.last_test_status = row.last_test_message = None
    _audit(
        session,
        user,
        "video_vps_settings_updated",
        fields=sorted(payload.model_fields_set - {"expected_updated_at"}),
    )
    await session.commit()
    return _view(row)


async def test_connection(session: AsyncSession, user: User) -> SettingsView:
    row = await _row(session, lock=True)
    values, secret, _source = _values(row)
    details: dict[str, Any] = {}
    try:
        settings = _config(values, secret)
        if settings is None:
            raise Refused(409, "vps_not_configured", "請先啟用並儲存 VPS 上傳服務設定")
        details = await probe(settings)
        status, message = "success", "服務連線成功且頻道設定相符；Google 登入請到遠端桌面確認"
    except Refused as error:
        status, message = "failed", error.detail
    if row is None:
        row = ProviderConfig(
            provider=PROVIDER, enabled=True, priority=100, config={"inherit_environment": True}
        )
        session.add(row)
    row.last_tested_at = datetime.now(UTC)
    row.last_test_status, row.last_test_message = status, message
    _audit(session, user, "video_vps_connection_tested", status=status)
    await session.commit()
    return _view(row).model_copy(update=details)
