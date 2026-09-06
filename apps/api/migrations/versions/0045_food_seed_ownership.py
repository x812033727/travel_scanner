"""Record who owns a dish row and each of its localizations: the seed catalog or an admin.

Revision ID: 0045_food_seed_ownership
Revises: 0044_repair_quoted_review_status

``seed-foods`` used to create a localization only when none existed, so a corrected
name in ``FOOD_SEEDS`` never reached a database that already had the row. The seeder
now reconciles the rows it owns and leaves rows an administrator edited alone; these
two columns are how it tells them apart, the way ``food_merchants.area_source``
already does for areas.

Every existing row is marked ``seed``. That is not a guess: on 2026-09-06 production
was compared against the catalog and all 400 localizations matched their seed text
exactly, as did every dish row apart from two ``search_text`` values that were stale
for the very reason this migration exists (a city was added to a dish after the row
was written). Timestamps could not have decided it: ``updated_at`` is assigned
separately from ``created_at`` on insert and differs by a microsecond on most rows.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0045_food_seed_ownership"
down_revision: str | None = "0044_repair_quoted_review_status"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLES: tuple[tuple[str, str], ...] = (
    ("travel_foods", "ck_travel_food_source"),
    ("food_localizations", "ck_food_localization_source"),
)


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    for table, constraint in TABLES:
        columns = {str(column["name"]) for column in inspector.get_columns(table)}
        if "source" not in columns:
            op.add_column(
                table,
                sa.Column("source", sa.String(length=16), nullable=False, server_default="seed"),
            )
        checks = {str(check["name"]) for check in inspector.get_check_constraints(table)}
        if constraint not in checks:
            op.create_check_constraint(constraint, table, "source IN ('seed', 'admin')")


def downgrade() -> None:
    for table, constraint in TABLES:
        op.drop_constraint(constraint, table, type_="check")
        op.drop_column(table, "source")
