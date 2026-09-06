from __future__ import annotations

import math
from decimal import Decimal
from typing import Literal

DURABLE_COORDINATE_SOURCES = frozenset(
    {"curated", "wikidata", "official_tourism", "merchant_official", "admin_verified"}
)
# A point Google gave us is good enough for one traveller's own stop: they pasted the
# link, they will see the pin, and a wrong one costs them a walk. It is never good
# enough for the catalogue, where one wrong pin is served to everybody and outlives
# whoever added it.
TRIP_ONLY_COORDINATE_SOURCES = frozenset({"google_places", "user_paste"})


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


def is_durable_coordinate_source(
    source_type: str | None,
    source_url: str | None,
    *,
    scope: Literal["catalog", "trip"] = "catalog",
) -> bool:
    """Whether a coordinate may be kept without anyone checking it again.

    ``catalog`` is the strict rule: a hotspot or merchant row is shown to everyone,
    so only a source a human vouched for counts. ``trip`` also accepts the point a
    traveller's own pasted link carried, which is theirs alone.
    """
    allowed = DURABLE_COORDINATE_SOURCES
    if scope == "trip":
        allowed = allowed | TRIP_ONLY_COORDINATE_SOURCES
    return bool(
        source_type in allowed
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
