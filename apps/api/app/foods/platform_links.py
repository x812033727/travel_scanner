"""Reviewed reservation platforms and strict merchant-specific link serialization."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit

from app.models import FoodMerchantPlatformLink

SITE_LOCALES = ("zh-TW", "zh-CN", "en", "ja", "ko")
PLATFORM_STATUSES = frozenset({"verified", "not_found", "ambiguous", "disabled"})


@dataclass(frozen=True)
class PlatformDefinition:
    provider: str
    label: str
    hosts: tuple[str, ...]
    default_language: str


# Country defaults remain a seed/backward-compatibility hint, never an allowlist.
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
        "hungry_hub", "Hungry Hub",
        ("hungryhub.com", "www.hungryhub.com", "web.hungryhub.com"), "en",
    ),
    "VN": PlatformDefinition("pasgo", "PasGo", ("pasgo.vn", "www.pasgo.vn"), "vi"),
}
PLATFORMS_BY_PROVIDER = {item.provider: item for item in PLATFORMS_BY_COUNTRY.values()}
PLATFORMS_BY_PROVIDER.update({
    item.provider: item for item in (
        PlatformDefinition("inline", "inline", ("inline.app",), ""),
        PlatformDefinition("maifood", "Maifood", ("reservation.maifood.com.tw",), ""),
        PlatformDefinition(
            "sevenrooms", "SevenRooms", ("sevenrooms.com", "www.sevenrooms.com"), ""
        ),
        PlatformDefinition("ikyu", "一休", ("restaurant.ikyu.com",), ""),
        PlatformDefinition(
            "myconcierge", "My Concierge Japan",
            ("myconciergejapan.com", "www.myconciergejapan.com"), "",
        ),
    )
})

_LANGUAGES = {
    "en": "en", "ja": "ja", "ko": "ko", "th": "th", "vi": "vi",
    "zh-tw": "zh-TW", "zh-hk": "zh-TW", "zh-hant": "zh-TW",
    "zh-cn": "zh-CN", "zh-hans": "zh-CN",
}
_LOCALE = "(?:" + "|".join(_LANGUAGES) + ")"
_SLUG = r"[A-Za-z0-9][A-Za-z0-9_-]*"
# Catchtable venue IDs may contain literal dots, but never empty dot segments.
_CATCHTABLE_SLUG = r"[A-Za-z0-9][A-Za-z0-9_-]*(?:\.[A-Za-z0-9][A-Za-z0-9_-]*)*"
_INLINE_ID = r"[A-Za-z0-9_-]+"
_RESERVED = frozenset({
    "search", "ranking", "rankings", "discovery", "explore", "restaurants",
    "list_of_restaurants", "booking", "reserve", "reservations", "shops",
    "restaurant", "branches",
})


def expected_platform(country_code: str) -> PlatformDefinition:
    try:
        return PLATFORMS_BY_COUNTRY[country_code.upper()]
    except KeyError as exc:
        raise ValueError("unsupported merchant country") from exc


def available_platforms() -> list[dict[str, str]]:
    return [
        {"provider": provider, "label": PLATFORMS_BY_PROVIDER[provider].label}
        for provider in sorted(PLATFORMS_BY_PROVIDER)
    ]


def normalize_platform_url(url: str) -> str:
    # Check before urlsplit: parsers silently discard some control characters.
    if not url or len(url) > 2048 or re.search(r"[\x00-\x20\x7f-\x9f\\]", url):
        raise ValueError("reservation URL contains unsafe characters")
    if re.search(r"%(?:2f|5c|2e|25|[01][0-9a-f]|7f)", url, re.IGNORECASE):
        raise ValueError("reservation URL contains unsafe encoded characters")
    if re.search(r"%(?![0-9a-f]{2})", url, re.IGNORECASE):
        raise ValueError("reservation URL contains invalid encoding")
    parts = urlsplit(url)
    if parts.scheme.lower() != "https" or not parts.hostname:
        raise ValueError("reservation URL must be an HTTPS URL")
    if parts.netloc.lower() != parts.hostname.lower() or "#" in url:
        raise ValueError("reservation URL cannot contain credentials, a port or a fragment")
    if "//" in parts.path or ("?" in url and not parts.query):
        raise ValueError("reservation URL contains an invalid path")
    path = parts.path.removesuffix("/") or "/"
    decoded = unquote(path, errors="strict")
    if any(segment in {".", "..", ""} for segment in decoded.split("/")[1:]):
        raise ValueError("reservation URL contains an invalid path")
    if re.search(r"[\x00-\x20\x7f-\x9f\\]", decoded):
        raise ValueError("reservation URL contains unsafe characters")
    return urlunsplit(("https", parts.netloc.lower(), path, parts.query, ""))


def _merchant_identity(provider: str, path: str) -> str:
    """Return the branch identifier, excluding known locale and route aliases."""
    optional_locale = rf"(?:{_LOCALE}/)?"
    patterns: dict[str, tuple[str, ...]] = {
        "tablecheck": (
            rf"/{optional_locale}shops/(?P<id>{_SLUG})/reserve",
            rf"/{_LOCALE}/(?P<id>{_SLUG})/reserve/(?:message|landing)",
        ),
        "catchtable_global": (
            rf"/{optional_locale}(?:shop|restaurant|restaurants)/(?P<id>{_CATCHTABLE_SLUG})",
        ),
        "eztable": (rf"/{optional_locale}(?:restaurant|restaurants)/(?P<id>{_SLUG})",),
        "chope": (
            rf"/{optional_locale}(?P<region>[a-z]+(?:-[a-z]+)*-restaurants)"
            rf"/restaurant/(?P<id>{_SLUG})",
        ),
        "openrice": (
            rf"/{_LOCALE}/(?P<region>[a-z][a-z-]*)/[pr]-[^/]+-(?P<id>[pr][0-9]+)",
        ),
        "hungry_hub": (rf"/{optional_locale}restaurants/(?P<id>{_SLUG})(?:/web)?",),
        "pasgo": (rf"/nha-hang/(?P<id>{_SLUG})",),
        "inline": (rf"/booking/(?P<id>{_INLINE_ID}:{_INLINE_ID}/{_INLINE_ID})",),
        "maifood": (rf"/(?P<brand>{_SLUG})/(?P<id>{_SLUG})",),
        "sevenrooms": (
            rf"/reservations/(?P<id>{_SLUG})",
            rf"/explore/(?P<id>{_SLUG})/reservations/create/search",
        ),
        "ikyu": (r"/(?P<id>[0-9]+)",),
        "myconcierge": (rf"/{optional_locale}restaurants/(?P<id>{_SLUG})",),
    }
    for pattern in patterns.get(provider, ()):
        match = re.fullmatch(pattern, path, flags=re.IGNORECASE | re.ASCII)
        if match:
            identifier = match["id"]
            if identifier.lower() in _RESERVED:
                break
            if provider == "inline" and identifier.split("/")[-1].lower() in _RESERVED:
                break
            brand = match.groupdict().get("brand")
            if brand:
                if brand.lower() in _RESERVED:
                    break
                return f"{brand}/{identifier}"
            region = match.groupdict().get("region")
            if provider == "openrice":
                if any(not (char.isalnum() or char in "_-") for char in path.split("/")[-1]):
                    break
                identifier = identifier.lower()
            return f"{region.lower()}/{identifier}" if region else identifier
    raise ValueError("reservation URL is not a recognized merchant-specific page")


def validate_platform_url(provider: str, url: str) -> str:
    """Accept only explicit merchant routes; never fetch or guess a redirect."""
    definition = PLATFORMS_BY_PROVIDER.get(provider)
    if definition is None:
        raise ValueError("unsupported reservation platform")
    normalized = normalize_platform_url(url)
    parts = urlsplit(normalized)
    if parts.hostname not in definition.hosts:
        raise ValueError("reservation URL host does not match provider")
    _merchant_identity(provider, unquote(parts.path, errors="strict"))
    query = ""
    if parts.query:
        pairs = parse_qsl(parts.query, keep_blank_values=True, strict_parsing=True)
        if (
            provider != "inline" or len(pairs) != 1 or pairs[0][0] != "language"
            or pairs[0][1].lower() not in _LANGUAGES
            or parts.query != f"language={pairs[0][1]}"
        ):
            raise ValueError("reservation URL contains unsupported query parameters")
        query = urlencode(pairs)
    return urlunsplit(("https", parts.netloc, parts.path, query, ""))


def platform_url_identity(provider: str, url: str) -> str:
    parts = urlsplit(validate_platform_url(provider, url))
    return _merchant_identity(provider, unquote(parts.path, errors="strict"))


def platform_url_language(provider: str, url: str) -> str:
    parts = urlsplit(validate_platform_url(provider, url))
    if provider == "inline":
        language = dict(parse_qsl(parts.query)).get("language", "")
    elif provider in {
        "tablecheck", "catchtable_global", "eztable", "chope", "openrice",
        "hungry_hub", "myconcierge",
    }:
        language = unquote(parts.path, errors="strict").split("/")[1]
    else:
        language = ""
    return _LANGUAGES.get(language.lower(), "")


def validate_localized_platform_urls(
    provider: str, canonical_url: str | None, localized_urls: dict[str, str]
) -> dict[str, str]:
    if not localized_urls:
        return {}
    if not canonical_url:
        raise ValueError("localized URLs require a canonical merchant URL")
    identity = platform_url_identity(provider, canonical_url)
    result = {}
    for locale, url in localized_urls.items():
        if locale not in SITE_LOCALES:
            raise ValueError("unsupported reservation URL locale")
        normalized = validate_platform_url(provider, url)
        if platform_url_identity(provider, normalized) != identity:
            raise ValueError("localized URL identifies a different merchant or branch")
        language = platform_url_language(provider, normalized)
        if language and language != locale:
            raise ValueError("localized URL language does not match its locale")
        result[locale] = normalized
    return result


def serialize_reservation_link(
    row: FoodMerchantPlatformLink,
    *,
    country_code: str,
    locale: str,
) -> dict[str, str] | None:
    definition = PLATFORMS_BY_PROVIDER.get(row.provider)
    if row.status != "verified" or definition is None or not row.canonical_url:
        return None
    try:
        canonical = validate_platform_url(row.provider, row.canonical_url)
    except (ValueError, TypeError):
        return None
    # Legacy bad localized metadata cannot hide an otherwise valid canonical page.
    selected_url = canonical
    localized = row.localized_urls_json or {}
    requested_locale = locale if locale in SITE_LOCALES else "en"
    if localized.get(requested_locale):
        try:
            selected_url = validate_localized_platform_urls(
                row.provider, canonical, {requested_locale: localized[requested_locale]}
            )[requested_locale]
        except (ValueError, TypeError):
            pass
    return {
        "provider": definition.provider,
        "label": definition.label,
        "url": selected_url,
        "verified_at": _isoformat(row.checked_at),
        "language_code": platform_url_language(row.provider, selected_url),
    }


def _isoformat(value: datetime) -> str:
    return value.isoformat()
