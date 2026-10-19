"""Protect B18 v2 and five follow-on stories with separate USD 5 full-film ceilings.

Revision ID: 0133_story_followon_budget
Revises: 0132_video_pilot_budget

The existing B18 v2 account and every operation remain in place. Lowering its account
ceiling does not erase a prior hold or charge: the budget service refuses new dispatches
when retained exposure is above USD 5. The five new accounts are inserted independently.

Deploy the separate 0132 application compatibility release (#1521) and verify it
before this migration. Production runs migrations before switching API containers and
an application rollback does not downgrade the database.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import insert

revision: str = "0133_story_followon_budget"
down_revision: str | None = "0132_video_pilot_budget"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

ACCOUNT = "video_pilot_budgets"
CONSTRAINT = "ck_video_pilot_budget_limit"
B18_V2 = "story-conveyor-belt-sushi-v2"
FOLLOWONS = (
    "story-five-lego-legoland",
    "story-five-costco-hot-dog",
    "story-five-adidas-puma-brothers",
    "story-five-ajinomoto-chip-film",
    "story-five-pringles-vat-case",
)


def upgrade() -> None:
    # Replacing the same named constraint makes rerunning the upgrade bounded; the value
    # update and ON CONFLICT seeds do not touch operation rows or reset paid exposure.
    op.drop_constraint(CONSTRAINT, ACCOUNT, type_="check")
    op.create_check_constraint(CONSTRAINT, ACCOUNT, "limit_usd IN (5.000000, 25.000000)")

    account = sa.table(
        ACCOUNT,
        sa.column("slug", sa.String(length=80)),
        sa.column("limit_usd", sa.Numeric(12, 6)),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    op.execute(
        sa.update(account)
        .where(account.c.slug == B18_V2)
        .where(account.c.limit_usd == sa.literal(25))
        .values(limit_usd=sa.literal(5))
    )
    for slug in FOLLOWONS:
        op.execute(
            insert(account)
            .values(slug=slug, limit_usd=sa.literal(5), created_at=sa.func.now())
            .on_conflict_do_nothing(index_elements=["slug"])
        )


def downgrade() -> None:
    # Automatically expanding B18 back to USD 25 or dropping a follow-on account could
    # authorize more spend or erase the context of retained operations. Roll back only
    # the application code; a database reversal requires a separate reviewed plan.
    raise RuntimeError("The story budget ceiling cannot be downgraded automatically")
