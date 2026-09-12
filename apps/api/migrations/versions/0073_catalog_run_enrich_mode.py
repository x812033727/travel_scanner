"""Let a catalog review run record the merchant enrichment mode.

Revision ID: 0073_catalog_run_enrich_mode
Revises: 0072_travel_guides

``catalog_review_runs.mode`` has allowed only ``review_pending`` and ``discover_new`` since
0054. The merchant enrichment mode (``enrich_merchants``: fill address, official website,
tourism listing, area and category of pending food merchants from independently fetched
pages) reuses the same run table, so the CHECK constraint must admit the third value or
the INSERT in ``create_run`` fails with a 500 instead of a queued run.

0001 still calls the current ``Base.metadata.create_all``, so a fresh database already has
the widened constraint and there is nothing to drop; the step inspects first, through the
operations context so the migration tests can drive it, and offline SQL runs unguarded.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0073_catalog_run_enrich_mode"
down_revision: str | None = "0072_travel_guides"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "catalog_review_runs"
CONSTRAINT = "ck_catalog_run_mode"
WITH_ENRICH = "mode IN ('review_pending', 'discover_new', 'enrich_merchants')"
WITHOUT_ENRICH = "mode IN ('review_pending', 'discover_new')"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _existing_check() -> str | None:
    """The constraint's current text, or None when the table has none by that name."""
    if _offline():
        return WITHOUT_ENRICH
    checks = sa.inspect(op.get_bind()).get_check_constraints(TABLE)
    for check in checks:
        if check.get("name") == CONSTRAINT:
            return str(check.get("sqltext") or "")
    return None


def upgrade() -> None:
    current = _existing_check()
    if current is not None and "enrich_merchants" in current:
        return
    if current is not None:
        op.drop_constraint(CONSTRAINT, TABLE, type_="check")
    op.create_check_constraint(CONSTRAINT, TABLE, WITH_ENRICH)


def downgrade() -> None:
    current = _existing_check()
    if current is None or "enrich_merchants" not in current:
        return
    if not _offline():
        remaining = (
            op.get_bind()
            .execute(sa.text(f"SELECT count(*) FROM {TABLE} WHERE mode = 'enrich_merchants'"))
            .scalar()
        )
        if remaining:
            raise RuntimeError(
                f"{remaining} enrich_merchants runs exist; delete or archive them before "
                "narrowing ck_catalog_run_mode"
            )
    op.drop_constraint(CONSTRAINT, TABLE, type_="check")
    op.create_check_constraint(CONSTRAINT, TABLE, WITHOUT_ENRICH)
