"""Validity boundary for the pilot's manually verified provider price ceilings.

The route-specific integrations supply conservative dollar ceilings to the ledger. Their
published 2026 rates are not automatically valid after the current pricing period; all pilot
dispatches stop until those ceilings have been checked and this date deliberately advanced.
"""

from datetime import date

PRICE_VALID_THROUGH = date(2026, 12, 31)


def price_window_current(today: date | None = None) -> bool:
    return (today or date.today()) <= PRICE_VALID_THROUGH
