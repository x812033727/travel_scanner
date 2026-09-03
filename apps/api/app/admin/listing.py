"""Shared helpers for admin list endpoints: fixed country order and localized names."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from sqlalchemy import ColumnElement, case
from sqlalchemy.orm import InstrumentedAttribute

from app.destinations.catalog import DESTINATIONS
from app.foods.catalog import COUNTRY_NAMES
from app.i18n import Locale

COUNTRY_ORDER: tuple[str, ...] = tuple(COUNTRY_NAMES)
COUNTRY_RANK: dict[str, int] = {code: index for index, code in enumerate(COUNTRY_ORDER)}
DESTINATION_ROLE_RANK: dict[str, int] = {"primary": 0, "secondary": 1, "extension": 2}
DESTINATION_RANK: dict[str, int] = {
    item.id: DESTINATION_ROLE_RANK[item.role] for item in DESTINATIONS
}
HOTSPOT_CATEGORY_ORDER: tuple[str, ...] = (
    "culture",
    "food",
    "nature",
    "beach",
    "family",
    "viewpoint",
    "shopping",
    "nightlife",
)
FOOD_KIND_ORDER: tuple[str, ...] = ("main", "noodle_soup", "street_food", "dessert", "drink")


def country_rank(column: InstrumentedAttribute[str]) -> ColumnElement[int]:
    """Sort rows by the catalog's country order in the database, unknown countries last.

    Sorting on the server keeps every country contiguous across pages, which the admin
    lists rely on to render one section header per country.
    """
    return case(COUNTRY_RANK, value=column, else_=len(COUNTRY_RANK))


def destination_rank(column: InstrumentedAttribute[str]) -> ColumnElement[int]:
    """Within a country, list primary cities first, then secondary, then cross-city extensions."""
    return case(DESTINATION_RANK, value=column, else_=len(DESTINATION_ROLE_RANK))


def country_name_for(code: str, locale: Locale, fallback: str | None = None) -> str:
    names = COUNTRY_NAMES.get(code)
    if names is None:
        return fallback or code
    return names.get(locale) or names["en"]


def ranked(rows: Iterable[Any], attr: str, order: tuple[str, ...]) -> list[Any]:
    """Order facet rows by a fixed code order; codes outside it go last, alphabetically."""
    rank = {code: index for index, code in enumerate(order)}
    return sorted(
        rows,
        key=lambda row: (rank.get(getattr(row, attr), len(rank)), getattr(row, attr)),
    )
