from __future__ import annotations

import math
from decimal import Decimal

DURABLE_COORDINATE_SOURCES = frozenset(
    {"curated", "wikidata", "official_tourism", "merchant_official", "admin_verified"}
)


def valid_coordinate_pair(
    latitude: Decimal | float | None,
    longitude: Decimal | float | None,
) -> bool:
    if latitude is None or longitude is None:
        return False
    try:
        lat = float(latitude)
        lng = float(longitude)
    except (TypeError, ValueError):
        return False
    return (
        math.isfinite(lat)
        and math.isfinite(lng)
        and -90 <= lat <= 90
        and -180 <= lng <= 180
    )


def is_durable_coordinate_source(source_type: str | None, source_url: str | None) -> bool:
    return bool(
        source_type in DURABLE_COORDINATE_SOURCES
        and source_url
        and source_url.startswith("https://")
    )


def has_durable_coordinates(
    latitude: Decimal | float | None,
    longitude: Decimal | float | None,
    source_type: str | None,
    source_url: str | None,
) -> bool:
    return valid_coordinate_pair(latitude, longitude) and is_durable_coordinate_source(
        source_type, source_url
    )
