"""Exact reviewed OTA links only; no network calls, prices, or auto link rewriting.

Protocol: https://dev.stay22.com/docs/allez/parameters
The supplied target is encoded once as an opaque `link`, never appended to or
rewritten in the stored hotel identity. Account tracking needs live verification.
"""

from __future__ import annotations

import re
from datetime import UTC, date, datetime
from typing import Literal, get_args
from urllib.parse import quote, unquote, urlencode, urlsplit

from app.i18n import LOCALES, Locale
from app.models import HotelBookingOption
from app.travel_services.schemas import (
    SERVICE_DESTINATION_IDS,
    STAY22_PROVIDERS,
    CatalogConfig,
    HotelBookingContext,
    HotelLink,
    Stay22Config,
)

BookingPlacement = Literal["destination", "hotspot", "trip", "stay", "checklist", "discovery"]
# The HTTP boundary and campaign builder share this finite set: a new public
# entry point must not pass one check and then fail after the user clicks.
BOOKING_PLACEMENTS = frozenset(get_args(BookingPlacement))
BookingChannel = Literal["existing", "stay22", "direct"]

# Deliberately narrower than generic reviewed links: Allez must get a property,
# never a destination page, a nested redirect, or another user's search context.
_PROPERTY_PATHS = {
    "booking": re.compile(r"^/hotel/[a-z]{2}/[^/]+/?$", re.I),
    "agoda": re.compile(r"^(?:/[a-z]{2}(?:-[a-z]{2})?)?/[^/]+/hotel/[^/]+\.html/?$", re.I),
    "expedia": re.compile(r"^/[^/]+\.h[0-9]+\.Hotel-Information/?$", re.I),
}


def validate_stay22_target(provider: str, target: str) -> str:
    """Return a safe canonical property URL or fail closed, without network I/O."""
    if provider not in STAY22_PROVIDERS:
        raise ValueError("Stay22 provider is not enabled for exact hotel links")
    link = HotelLink(provider=provider, url=target, evidence_url=target)
    parsed = urlsplit(link.url)
    # Allow no opaque query fields, including currently unknown occupancy or
    # tracking aliases. Editors can re-review a clean canonical URL instead.
    if parsed.query or urlsplit(target).fragment:
        raise ValueError("Stay22 requires a clean property URL without query or fragment")
    decoded_path = unquote(unquote(parsed.path))
    if (
        any(ord(char) < 33 for char in decoded_path)
        or any(char in decoded_path for char in ("\\", "?", "#", ";", "%"))
        or "//" in decoded_path
        or any(part in (".", "..") for part in decoded_path.split("/"))
        or not _PROPERTY_PATHS[provider].fullmatch(decoded_path)
    ):
        raise ValueError("A canonical exact hotel property page is required")
    return link.url


def validate_booking_context(
    context: HotelBookingContext, *, today: date | None = None
) -> HotelBookingContext:
    """Revalidate at click time; never invent dates or silently shorten a stay."""
    validated = HotelBookingContext.model_validate(context.model_dump())
    if validated.check_in and validated.check_in < (today or datetime.now(UTC).date()):
        raise ValueError("Check-in cannot be in the past")
    return validated


def stay22_eligible(
    option: HotelBookingOption, config: CatalogConfig, *, tracking_allowed: bool = True
) -> bool:
    """Channel capability only: callers must also verify product/option review."""
    if not (
        tracking_allowed
        and config.stay22.enabled
        and option.provider in config.stay22.enabled_providers
        and option.url
    ):
        return False
    try:
        validate_stay22_target(option.provider, option.url)
    except ValueError:
        return False
    return True


def booking_channel(
    option: HotelBookingOption,
    config: CatalogConfig,
    *,
    has_offer: bool,
    tracking_allowed: bool = True,
) -> BookingChannel | None:
    """Choose once before execution; a failed existing channel is not Stay22 consent."""
    if has_offer:
        return "existing"
    if stay22_eligible(option, config, tracking_allowed=tracking_allowed):
        return "stay22"
    return "direct" if config.direct_hotel_links_enabled else None


def build_stay22_url(
    provider: str,
    target: str,
    config: Stay22Config,
    *,
    context: HotelBookingContext | None = None,
    destination_id: str,
    locale: Locale = "zh-TW",
    placement: BookingPlacement = "destination",
    today: date | None = None,
) -> str:
    """Build the fixed provider endpoint only following an explicit user click."""
    if not config.enabled or provider not in config.enabled_providers:
        raise ValueError("Stay22 is disabled for this provider")
    if (
        destination_id not in SERVICE_DESTINATION_IDS
        or locale not in LOCALES
        or placement not in BOOKING_PLACEMENTS
    ):
        raise ValueError("Only public destination, locale and placement labels are permitted")
    target = validate_stay22_target(provider, target)
    # Stay22 splits '-' into multiple campaign labels; '_' preserves one label.
    campaign = "_".join(("mokaair", destination_id, provider, locale, placement)).replace("-", "_")
    params = {
        "aid": config.aid,
        "link": target,
        "campaign": campaign,
        "lang": locale,
        "currency": "TWD",
    }
    if context is not None:
        context = validate_booking_context(context, today=today)
        if context.check_in and context.check_out:
            params["checkin"] = context.check_in.isoformat()
            params["checkout"] = context.check_out.isoformat()
        if context.adults is not None:
            params["adults"] = str(context.adults)
        if context.children is not None:
            params["children"] = str(context.children)
    # rooms and children_ages are UI context only: neither is a documented Allez
    # field, and no per-user identifiers are ever sent as attribution.
    return f"https://www.stay22.com/allez/{provider}?{urlencode(params, quote_via=quote)}"
