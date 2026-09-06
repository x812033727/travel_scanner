"""Throwaway: a second head to prove the guard. Do not merge.

Revision ID: 0044_second_head
Revises: 0043_trip_expenses
"""

from collections.abc import Sequence

revision: str = "0044_second_head"
down_revision: str | None = "0043_trip_expenses"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
