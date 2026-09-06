"""Repair three hotspots whose review_status is the literal string 'approved', quotes included.

Revision ID: 0044_repair_quoted_review_status
Revises: 0043_trip_expenses

On 2026-08-31 a script wrote ``'approved'`` — ten characters, single quotes included —
into ``travel_hotspots.review_status`` for the three ``retired-*`` rows, through a path
that did not validate the value. Nothing public reads them (all three are
``is_active = false``), but the value is outside the vocabulary every filter compares
against: those rows answer no query, appear in no admin count and quietly widen every
``GROUP BY review_status``.

The repair strips the quotes only when what is left is one of the four valid statuses,
so a value nobody recognises is left for a human rather than guessed at. The evidence
supports ``approved`` — that is what the string says once the quotes come off — while
``is_active`` is deliberately left alone: what the writer meant by the status is
legible, what they meant by retiring the rows is not.

The same migration then adds the CHECK constraint ``food_merchants`` already carries,
so the mistake cannot be repeated. On 2026-09-06 production held exactly
approved/pending/rejected/disabled plus the three quoted rows, so the constraint is
safe to add once the repair has run; a database with any other value fails here on
purpose instead of carrying it forward.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0044_repair_quoted_review_status"
down_revision: str | None = "0043_trip_expenses"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

CONSTRAINT = "ck_travel_hotspot_review_status"
VALID = "('pending', 'approved', 'rejected', 'disabled')"


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "travel_hotspots" not in set(inspector.get_table_names()):
        return
    bind.execute(
        sa.text(
            "UPDATE travel_hotspots"
            "   SET review_status = btrim(review_status, '''')"
            " WHERE review_status LIKE '''%'''"
            f"   AND btrim(review_status, '''') IN {VALID}"
        )
    )
    names = {check["name"] for check in inspector.get_check_constraints("travel_hotspots")}
    if CONSTRAINT not in names:
        op.create_check_constraint(CONSTRAINT, "travel_hotspots", f"review_status IN {VALID}")


def downgrade() -> None:
    # The repaired rows cannot be told apart from rows that were always valid, and there
    # is no reason to put the quotes back; only the constraint is undone.
    inspector = sa.inspect(op.get_bind())
    if "travel_hotspots" not in set(inspector.get_table_names()):
        return
    names = {check["name"] for check in inspector.get_check_constraints("travel_hotspots")}
    if CONSTRAINT in names:
        op.drop_constraint(CONSTRAINT, "travel_hotspots", type_="check")
