"""Seed the ai_itinerary_refine operation cost at zero uses.

Revision ID: 0040_ai_itinerary_refine
Revises: 0039_repair_dead_food_sources
"""

from collections.abc import Sequence
from datetime import UTC, datetime

import sqlalchemy as sa
from alembic import op

revision: str = "0041_ai_itinerary_refine"
down_revision: str | None = "0040_localized_names"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

OPERATION = "ai_itinerary_refine"

# usage_operation_costs.operation is a plain String(64) primary key — the only
# CHECK on the table is `uses >= 0 AND uses <= 100`, which 0 satisfies. Adding
# an operation therefore needs a seed row, not DDL. Without the row,
# effective_operation_cost falls back to 1 and refinement would silently charge.


def upgrade() -> None:
    costs = sa.table(
        "usage_operation_costs",
        sa.column("operation", sa.String()),
        sa.column("uses", sa.Integer()),
        sa.column("created_at", sa.DateTime(timezone=True)),
        sa.column("updated_at", sa.DateTime(timezone=True)),
    )
    connection = op.get_bind()
    existing = connection.execute(
        sa.select(costs.c.operation).where(costs.c.operation == OPERATION)
    ).first()
    if existing is not None:
        return
    now = datetime.now(UTC)
    connection.execute(
        costs.insert().values(operation=OPERATION, uses=0, created_at=now, updated_at=now)
    )


def downgrade() -> None:
    costs = sa.table(
        "usage_operation_costs",
        sa.column("operation", sa.String()),
    )
    op.get_bind().execute(costs.delete().where(costs.c.operation == OPERATION))
