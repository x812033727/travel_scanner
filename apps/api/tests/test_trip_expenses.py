"""The ledger's arithmetic and seeding, without a database.

The endpoints are exercised against real Postgres in
tests/test_integration_postgres_redis.py; what matters here is that the sums
are exact, that seeding is idempotent, and that nothing in an unknown currency
sneaks into a total.
"""

from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.main import app
from app.models import TripExpense, TripPlan
from app.trips.expenses import MAX_EXPENSES, cost_summary, seed_rows
from app.trips.router import TripExpensePatchRequest, TripExpenseRequest

DAY_ONE = date(2026, 11, 10)
DAY_TWO = date(2026, 11, 11)


def _trip(**overrides: object) -> TripPlan:
    fields: dict[str, object] = {
        "id": uuid4(),
        "user_id": uuid4(),
        "name": "東京五日",
        "mode": "manual",
        "total_price": Decimal("48200"),
        "currency": "TWD",
        "data": {},
        "version": 3,
        "start_date": DAY_ONE,
        "end_date": DAY_TWO,
        "timezone": "Asia/Tokyo",
        "route_preference": "FEWER_TRANSFERS",
        "budget_amount": None,
        "cost_currency": "TWD",
    }
    fields.update(overrides)
    return TripPlan(**fields)


def _row(day: date, amount: str, category: str = "food", position: int = 0) -> TripExpense:
    return TripExpense(
        id=uuid4(),
        trip_plan_id=uuid4(),
        day_date=day,
        label="午餐",
        amount=Decimal(amount),
        category=category,
        source="manual",
        position=position,
        created_at=datetime(2026, 11, 10, 9, position, tzinfo=UTC),
    )


def test_expense_routes_are_published() -> None:
    paths = app.openapi()["paths"]
    assert "post" in paths["/api/v1/trips/{trip_id}/expenses"]
    assert "post" in paths["/api/v1/trips/{trip_id}/expenses/seed"]
    assert "patch" in paths["/api/v1/trips/{trip_id}/expenses/{expense_id}"]
    assert "delete" in paths["/api/v1/trips/{trip_id}/expenses/{expense_id}"]


def test_totals_are_exact_and_split_by_day_and_category() -> None:
    # 0.1 + 0.2 in floats is 0.30000000000000004; a ledger must not do that.
    summary = cost_summary(
        _trip(budget_amount=Decimal("1000.00")),
        [
            _row(DAY_ONE, "0.10", "food"),
            _row(DAY_ONE, "0.20", "transport", position=1),
            _row(DAY_TWO, "250.55", "lodging"),
        ],
    )

    assert summary["total"] == "250.85"
    assert summary["by_day"] == {"2026-11-10": "0.30", "2026-11-11": "250.55"}
    assert summary["by_category"]["food"] == "0.10"
    assert summary["difference"] == "749.15"
    assert summary["currency"] == "TWD"


def test_an_overspend_reads_as_a_negative_difference() -> None:
    summary = cost_summary(_trip(budget_amount=Decimal("100")), [_row(DAY_ONE, "180")])
    # A bare absolute value would leave the traveller guessing which way.
    assert summary["difference"] == "-80"


def test_a_ledger_without_a_budget_reports_no_difference() -> None:
    summary = cost_summary(_trip(), [_row(DAY_ONE, "180")])
    assert summary["budget"] is None
    assert summary["difference"] is None
    assert summary["total"] == "180"


def test_seeding_takes_known_prices_and_never_repeats_one() -> None:
    trip = _trip(
        data={
            "total_cost": {
                "components": [
                    {"category": "flight_base", "label": "機票票價", "amount": "21800"},
                    {"category": "hotel", "label": "住宿", "amount": "19400"},
                    {"category": "local_transport", "label": "當地交通估算", "amount": "4200"},
                    # Not in the seedable map: skipped rather than guessed.
                    {"category": "mystery_fee", "label": "未知", "amount": "999"},
                ]
            }
        }
    )

    seeds = seed_rows(trip, existing_keys=set(), day=DAY_ONE)
    keys = {seed["source_key"] for seed in seeds}

    assert keys == {"total_cost:flight_base", "total_cost:hotel", "total_cost:local_transport"}
    assert {seed["category"] for seed in seeds} == {"flight", "lodging", "transport"}
    # Pressing the button again adds nothing.
    assert seed_rows(trip, existing_keys=keys, day=DAY_ONE) == []


def test_seeding_skips_amounts_that_are_not_real_money() -> None:
    trip = _trip(
        data={
            "total_cost": {
                "components": [
                    {"category": "flight_base", "label": "機票", "amount": "0"},
                    {"category": "hotel", "label": "住宿", "amount": None},
                    {"category": "baggage", "label": "行李", "amount": "not-a-number"},
                    {"category": "activities", "label": "活動", "amount": "-50"},
                ]
            }
        }
    )
    assert seed_rows(trip, existing_keys=set(), day=DAY_ONE) == []


def test_a_ledger_line_is_trimmed_and_cannot_be_blank_or_negative() -> None:
    assert TripExpenseRequest(
        version=1, day_date=DAY_ONE, label="  一蘭拉麵  ", amount=Decimal("980")
    ).label == "一蘭拉麵"
    with pytest.raises(ValidationError):
        TripExpenseRequest(version=1, day_date=DAY_ONE, label="   ", amount=Decimal("980"))
    with pytest.raises(ValidationError):
        TripExpenseRequest(version=1, day_date=DAY_ONE, label="退款", amount=Decimal("-1"))
    with pytest.raises(ValidationError):
        TripExpenseRequest(
            version=1, day_date=DAY_ONE, label="午餐", amount=Decimal("1"), category="bribe"
        )


def test_an_edit_must_change_something_and_carry_a_version() -> None:
    with pytest.raises(ValidationError):
        TripExpensePatchRequest(version=1)
    with pytest.raises(ValidationError):
        TripExpensePatchRequest(amount=Decimal("10"))  # type: ignore[call-arg]
    assert TripExpensePatchRequest(version=2, amount=Decimal("10")).amount == Decimal("10")


def test_the_ledger_cap_is_a_real_number() -> None:
    assert MAX_EXPENSES == 200
