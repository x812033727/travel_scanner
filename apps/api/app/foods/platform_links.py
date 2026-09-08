"""Country-specific reservation platforms and strict public-link serialization."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlsplit, urlunsplit

from app.models import FoodMerchantPlatformLink

SITE_LOCALES = ("zh-TW", "zh-CN", "en", "ja", "ko")
PLATFORM_STATUSES = frozenset({"verified", "not_found", "ambiguous", "disabled"})


@dataclass(frozen=True)
class PlatformDefinition:
    provider: str
    label: str
    hosts: tuple[str, ...]
    default_language: str


PLATFORMS_BY_COUNTRY: dict[str, PlatformDefinition] = {
    "JP": PlatformDefinition(
        "tablecheck", "TableCheck", ("tablecheck.com", "www.tablecheck.com"), "en"
    ),
    "KR": PlatformDefinition(
        "catchtable_global", "Catchtable Global", ("catchtable.net", "www.catchtable.net"), "en"
    ),
    "TW": PlatformDefinition("eztable", "EZTABLE", ("eztable.com", "www.eztable.com"), "zh-TW"),
    "SG": PlatformDefinition("chope", "Chope", ("chope.co", "www.chope.co"), "en"),
    "HK": PlatformDefinition("openrice", "OpenRice", ("openrice.com", "www.openrice.com"), "en"),
    "TH": PlatformDefinition(
        "hungry_hub",
        "Hungry Hub",
        ("hungryhub.com", "www.hungryhub.com", "web.hungryhub.com"),
        "en",
    ),
    "VN": PlatformDefinition("pasgo", "PasGo", ("pasgo.vn", "www.pasgo.vn"), "vi"),
}
PLATFORMS_BY_PROVIDER = {item.provider: item for item in PLATFORMS_BY_COUNTRY.values()}


def expected_platform(country_code: str) -> PlatformDefinition:
    try:
        return PLATFORMS_BY_COUNTRY[country_code.upper()]
    except KeyError as exc:
        raise ValueError("unsupported merchant country") from exc


def normalize_platform_url(url: str) -> str:
    parts = urlsplit(url.strip())
    if parts.scheme.lower() != "https" or not parts.hostname:
        raise ValueError("reservation URL must be an HTTPS URL")
    path = parts.path.rstrip("/") or "/"
    return urlunsplit(("https", parts.netloc.lower(), path, "", ""))


def validate_platform_url(provider: str, url: str) -> str:
    """Reject home, discovery, ranking, list and search URLs.

    The remaining provider-specific patterns identify a restaurant or branch page.
    Redirect resolution is intentionally not performed; an administrator confirms the
    page before setting the row to ``verified``.
    """

    definition = PLATFORMS_BY_PROVIDER.get(provider)
    if definition is None:
        raise ValueError("unsupported reservation platform")
    normalized = normalize_platform_url(url)
    parts = urlsplit(normalized)
    if parts.hostname not in definition.hosts:
        raise ValueError("reservation URL host does not match provider")
    segments = [segment.lower() for segment in parts.path.split("/") if segment]
    if not segments:
        raise ValueError("reservation URL must identify a specific merchant")
    forbidden = {
        "search", "ranking", "rankings", "discovery", "explore", "restaurants",
        "list_of_restaurants",
    }
    if segments[-1] in forbidden:
        raise ValueError("reservation URL cannot be a search, list or discovery page")

    valid = False
    if provider == "tablecheck":
        valid = (
            "shops" in segments
            and "reserve" in segments
            and segments.index("shops") + 1 < len(segments)
        )
    elif provider == "catchtable_global":
        valid = (
            any(token in segments for token in ("shop", "restaurant", "restaurants"))
            and len(segments) >= 2
        )
    elif provider == "eztable":
        valid = (
            any(token in segments for token in ("restaurant", "restaurants"))
            and len(segments) >= 2
        )
    elif provider == "chope":
        valid = "restaurant" in segments and segments.index("restaurant") + 1 < len(segments)
    elif provider == "openrice":
        valid = any(
            segment.startswith(("p-", "r-"))
            and any(char.isdigit() for char in segment)
            for segment in segments
        )
    elif provider == "hungry_hub":
        valid = "restaurants" in segments and segments.index("restaurants") + 1 < len(segments)
    elif provider == "pasgo":
        valid = "nha-hang" in segments and segments.index("nha-hang") + 1 < len(segments)
    if not valid:
        raise ValueError("reservation URL is not a recognized merchant-specific page")
    return normalized


def serialize_reservation_link(
    row: FoodMerchantPlatformLink,
    *,
    country_code: str,
    locale: str,
) -> dict[str, str] | None:
    definition = expected_platform(country_code)
    if row.status != "verified" or row.provider != definition.provider or not row.canonical_url:
        return None
    localized = row.localized_urls_json or {}
    requested_locale = locale if locale in SITE_LOCALES else "en"
    selected_url = localized.get(requested_locale) or row.canonical_url
    try:
        selected_url = validate_platform_url(row.provider, selected_url)
    except ValueError:
        return None
    language = requested_locale if requested_locale in localized else definition.default_language
    return {
        "provider": definition.provider,
        "label": definition.label,
        "url": selected_url,
        "verified_at": _isoformat(row.checked_at),
        "language_code": language,
    }


def _isoformat(value: datetime) -> str:
    return value.isoformat()
