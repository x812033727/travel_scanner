"""The trip expense ledger: totals, and seeding it from what is already known.

Kept out of the router so the arithmetic can be tested without a database. Two
rules shape everything here:

* One currency per trip. Per-row currencies would make a daily total
  meaningless without live conversion, and the only converter in this codebase
  (`FxRateProvider.rate_to_twd`) can convert *to* TWD and nothing else.
* Totals are summed in Python over the rows the payload already carries, not
  with a SQL aggregate. The rows have to be fetched anyway to render the
  ledger, `Decimal` addition is exact, and a `GROUP BY` would only add a second
  round trip to zip back together.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

from app.models import TripExpense, TripPlan

EXPENSE_CATEGORIES = (
    "flight",
    "lodging",
    "transport",
    "food",
    "activity",
    "shopping",
    "other",
)
# A ledger someone types by hand; well past any realistic trip, and small
# enough that summing and serialising it stays trivial.
MAX_EXPENSES = 200

# Which ledger category each known price component belongs to. Anything not
# listed here is not seeded at all rather than guessed into "other".
_SEEDABLE: dict[str, str] = {
    "flight_base": "flight",
    "flight_tax": "flight",
    "flight_fee": "flight",
    "baggage": "flight",
    "hotel": "lodging",
    "hotel_tax": "lodging",
    "hotel_fee": "lodging",
    "activities": "activity",
    "airport_transport": "transport",
    "local_transport": "transport",
}


def _decimal(value: object) -> Decimal | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
    return amount if amount.is_finite() and amount >= 0 else None


def serialize_expense(row: TripExpense) -> dict[str, Any]:
    return {
        "id": str(row.id),
        "day_date": row.day_date.isoformat(),
        "label": row.label,
        "amount": str(row.amount),
        "category": row.category,
        "source": row.source,
        "source_key": row.source_key,
        "position": row.position,
    }


def cost_summary(trip: TripPlan, rows: Iterable[TripExpense]) -> dict[str, Any]:
    """The ledger as the planner renders it: rows, per-day totals, the total.

    `difference` is budget minus spend, so a negative number is an overspend —
    the planner shows the sign rather than a bare absolute value.
    """
    ordered = sorted(rows, key=lambda row: (row.day_date, row.position, row.created_at))
    by_day: dict[str, Decimal] = {}
    by_category: dict[str, Decimal] = {}
    total = Decimal("0")
    for row in ordered:
        day = row.day_date.isoformat()
        by_day[day] = by_day.get(day, Decimal("0")) + row.amount
        by_category[row.category] = by_category.get(row.category, Decimal("0")) + row.amount
        total += row.amount
    budget = trip.budget_amount
    return {
        "currency": trip.cost_currency or "TWD",
        "budget": str(budget) if budget is not None else None,
        "total": str(total),
        "difference": str(budget - total) if budget is not None else None,
        "by_day": {day: str(amount) for day, amount in sorted(by_day.items())},
        "by_category": {name: str(amount) for name, amount in sorted(by_category.items())},
        "items": [serialize_expense(row) for row in ordered],
    }


def seed_rows(
    trip: TripPlan,
    *,
    existing_keys: set[str],
    day: date,
) -> list[dict[str, Any]]:
    """Ledger lines derivable from what the trip already knows.

    Sources: the price search's `total_cost.components`, and the saved lodging's
    price snapshot. Everything lands on one day (`day`) because these are
    whole-trip figures, not things that happened on an afternoon — the
    traveller can move them.

    Deliberately NOT seeded: `trip_route_segments.fare`, which is stored in the
    provider's own currency and never converted. Adding it would silently
    corrupt the total.
    """
    seeds: list[dict[str, Any]] = []

    def add(key: str, label: str, amount: Decimal | None, category: str) -> None:
        if amount is None or amount <= 0 or key in existing_keys:
            return
        if any(seed["source_key"] == key for seed in seeds):
            return
        seeds.append(
            {
                "source_key": key,
                "label": label[:120],
                "amount": amount,
                "category": category,
                "day_date": day,
            }
        )

    data = trip.data if isinstance(trip.data, Mapping) else {}
    total_cost = data.get("total_cost")
    if isinstance(total_cost, Mapping):
        components = total_cost.get("components")
        if isinstance(components, list):
            for component in components:
                if not isinstance(component, Mapping):
                    continue
                category_key = str(component.get("category") or "")
                ledger_category = _SEEDABLE.get(category_key)
                if ledger_category is None:
                    continue
                add(
                    f"total_cost:{category_key}",
                    str(component.get("label") or category_key),
                    _decimal(component.get("amount")),
                    ledger_category,
                )

    lodging = data.get("primary_lodging")
    if isinstance(lodging, Mapping):
        snapshot = lodging.get("price_snapshot")
        if isinstance(snapshot, Mapping):
            add(
                "primary_lodging:price_snapshot",
                str(lodging.get("name") or "住宿"),
                _decimal(snapshot.get("amount") or snapshot.get("total")),
                "lodging",
            )

    return seeds
