from datetime import UTC, datetime
from uuid import UUID

from app.config import Settings
from app.destinations.catalog import DESTINATIONS, match_destination
from app.destinations.localized import city_name
from app.hotspots.guides import canonical_external_url
from app.i18n import Locale
from app.problems import AppError


def require_enabled(settings: Settings) -> None:
    if not settings.discovery_enabled:
        raise AppError(503, "discovery_unavailable", "旅遊探索尚未開放")


def safe_source(value: str | None) -> str | None:
    if not value or any(ord(char) < 32 for char in value) or "\\" in value:
        return None
    try:
        return canonical_external_url(value)
    except (AppError, ValueError):
        return None


def aware(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=UTC)


def stamp(value: datetime | None) -> str | None:
    return aware(value).isoformat() if value else None


def destination_id(value: str) -> str:
    match = next((item for item in DESTINATIONS if item.id == value), None) or match_destination(
        value
    )
    return match.id if match else value.strip().lower()


def destination_payload(value: str, locale: Locale = "zh-TW") -> dict[str, str] | None:
    match = next((item for item in DESTINATIONS if item.id == value), None) or match_destination(
        value
    )
    if not match:
        return {"id": value, "name": value} if value else None
    return {"id": match.id, "name": city_name(match, locale)}


def catalog_destination_ids(values: list[str]) -> list[str]:
    """The service catalog splits the legacy Osaka/Kyoto destination into two."""
    result = set(values)
    if "osaka-kyoto" in result:
        result.update(("osaka", "kyoto"))
    return sorted(result)


def parse_key(value: str) -> tuple[str, UUID]:
    try:
        kind, identifier = value.split(":", 1)
        if kind not in {"hotspot", "food", "merchant", "hotel", "guide", "post"}:
            raise ValueError
        return kind, UUID(identifier)
    except (ValueError, AttributeError) as exc:
        raise AppError(422, "validation_error", "Invalid discovery reference") from exc
