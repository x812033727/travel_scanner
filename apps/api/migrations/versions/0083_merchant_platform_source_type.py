"""Let a merchant source be the shop's own reservation-platform page or its linked social account.

Revision ID: 0083_merchant_platform_source_type
Revises: 0082_travel_food_subtopics

``food_merchant_sources.source_type`` has admitted ``official_tourism``, ``merchant_official``
and ``michelin_licensed`` since 0026. On 2026-09-23 the owner added a weaker tier,
``merchant_platform``: the page a shop registered itself on a reservation platform
(CatchTable), or the social account that page's own "website" field points to. It is
shown separately on the public card and only the CatchTable converter and the admin form
may write it; the enrichment proposals still refuse platform hosts.

0001 still calls the current ``Base.metadata.create_all``, so a fresh database already has
the widened constraint and there is nothing to drop; the step inspects first, through the
operations context so the migration tests can drive it, and offline SQL runs unguarded.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0083_merchant_platform_source_type"
down_revision: str | None = "0082_travel_food_subtopics"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "food_merchant_sources"
CONSTRAINT = "ck_food_merchant_source_type"
NEW_TYPE = "merchant_platform"
WITH_PLATFORM = (
    "source_type IN ('official_tourism', 'merchant_official', 'michelin_licensed', "
    "'merchant_platform')"
)
WITHOUT_PLATFORM = "source_type IN ('official_tourism', 'merchant_official', 'michelin_licensed')"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _existing_check() -> str | None:
    """The constraint's current text, or None when the table has none by that name."""
    if _offline():
        return WITHOUT_PLATFORM
    checks = sa.inspect(op.get_bind()).get_check_constraints(TABLE)
    for check in checks:
        if check.get("name") == CONSTRAINT:
            return str(check.get("sqltext") or "")
    return None


def upgrade() -> None:
    current = _existing_check()
    if current is not None and NEW_TYPE in current:
        return
    if current is not None:
        op.drop_constraint(CONSTRAINT, TABLE, type_="check")
    op.create_check_constraint(CONSTRAINT, TABLE, WITH_PLATFORM)


def downgrade() -> None:
    current = _existing_check()
    if current is None or NEW_TYPE not in current:
        return
    if not _offline():
        remaining = (
            op.get_bind()
            .execute(sa.text(f"SELECT count(*) FROM {TABLE} WHERE source_type = '{NEW_TYPE}'"))
            .scalar()
        )
        if remaining:
            raise RuntimeError(
                f"{remaining} merchant_platform sources exist; delete or retype them before "
                "narrowing ck_food_merchant_source_type"
            )
    op.drop_constraint(CONSTRAINT, TABLE, type_="check")
    op.create_check_constraint(CONSTRAINT, TABLE, WITHOUT_PLATFORM)
