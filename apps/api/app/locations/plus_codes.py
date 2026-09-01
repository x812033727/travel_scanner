from __future__ import annotations

import math
from decimal import Decimal

from openlocationcode import openlocationcode  # type: ignore[import-untyped]

PLUS_CODE_LENGTH = 10
DURABLE_COORDINATE_SOURCES = frozenset(
    {"curated", "wikidata", "official_tourism", "merchant_official", "admin_verified"}
)


def plus_code_for_coordinates(
    latitude: Decimal | float,
    longitude: Decimal | float,
) -> str:
    """Return a full 10-character Open Location Code for a WGS84 point."""

    lat = float(latitude)
    lng = float(longitude)
    if not math.isfinite(lat) or not math.isfinite(lng):
        raise ValueError("coordinates must be finite")
    if not -90 <= lat <= 90:
        raise ValueError("latitude must be between -90 and 90")
    if not -180 <= lng <= 180:
        raise ValueError("longitude must be between -180 and 180")
    return str(openlocationcode.encode(lat, lng, PLUS_CODE_LENGTH))


def is_durable_coordinate_source(source_type: str | None, source_url: str | None) -> bool:
    return bool(
        source_type in DURABLE_COORDINATE_SOURCES
        and source_url
        and source_url.startswith("https://")
    )


def has_durable_coordinates(
    latitude: Decimal | float | None,
    longitude: Decimal | float | None,
    plus_code_global: str | None,
    source_type: str | None,
    source_url: str | None,
) -> bool:
    if latitude is None or longitude is None or not plus_code_global:
        return False
    if not is_durable_coordinate_source(source_type, source_url):
        return False
    try:
        return plus_code_for_coordinates(latitude, longitude) == plus_code_global
    except ValueError:
        return False
