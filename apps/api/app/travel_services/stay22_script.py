"""Public, minimal inputs for the isolated Stay22 script document.

This module never wraps links, resolves affiliate offers, records a booking,
or reads a user's trip. Loading the SDK belongs only to the public document;
private application pages retain their existing server-side clickout flow.
"""

from datetime import datetime
from typing import Any
from urllib.parse import urlsplit

from app.models import TravelServiceProduct
from app.problems import AppError
from app.travel_services.hotel_options import ready_option, safe_click_target
from app.travel_services.registry import BRANDS
from app.travel_services.schemas import HOTEL_PROVIDERS, CatalogConfig
from app.travel_services.stay22 import validate_stay22_target


def script_config(config: CatalogConfig, *, tracking_allowed: bool) -> dict[str, Any]:
    enabled = bool(
        tracking_allowed
        and config.public_enabled
        # Original anchors remain the truthful fallback when a browser blocks
        # the SDK. Script mode must not bypass the ordinary-link policy.
        and config.direct_hotel_links_enabled
        and "hotel" in config.enabled_kinds
        and config.stay22.enabled
        and config.stay22.integration_mode == "script"
        and config.stay22.lma_id
    )
    return {
        "enabled": enabled,
        "integration_mode": config.stay22.integration_mode,
        "lma_id": config.stay22.lma_id if enabled else None,
    }


async def script_options(
    product: TravelServiceProduct,
    config: CatalogConfig,
    now: datetime,
    *,
    locale: str,
) -> dict[str, Any]:
    options: list[dict[str, str]] = []
    ordered = sorted(
        product.hotel_options,
        key=lambda row: (
            HOTEL_PROVIDERS.index(row.provider)
            if row.provider in HOTEL_PROVIDERS else len(HOTEL_PROVIDERS)
        ),
    )
    for option in ordered:
        if not ready_option(product, option, config, now):
            continue
        try:
            # A script-visible URL must contain no stored dates, occupancy,
            # affiliate identifiers or other opaque personal query values.
            if not option.url or urlsplit(option.url).query or urlsplit(option.url).fragment:
                continue
            if option.provider in ("booking", "agoda", "expedia"):
                validate_stay22_target(option.provider, option.url)
            url = await safe_click_target(option)
        except (AppError, ValueError, TimeoutError, OSError):
            # One unsafe/unavailable platform must not expose its target or
            # suppress the hotel's other independently reviewed platforms.
            continue
        options.append({
            "id": str(option.id),
            "provider": option.provider,
            "name": (
                "Official website"
                if option.provider == "official"
                else BRANDS[option.provider].name
            ),
            "url": url,
        })
    return {
        "title": product.names_json.get(locale) or product.title,
        "destination_id": product.destination_id,
        "options": options,
    }
