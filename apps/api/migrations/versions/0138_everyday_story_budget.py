"""Open USD 25 full-film accounts for the owner-approved everyday-object story pilots.

Revision ID: 0138_everyday_story_budget
Revises: 0137_video_manga_tier

C03-C06 called TTS, transcription and Jev before they had accounts, and Google's shared
project bill cannot attribute those calls to one film. Each of them starts with one
``uncertain`` operation holding the whole USD 25, so no fresh balance appears: an operator
settles that hold against provider evidence with ``app.video_budget.reconcile_cli``
(RECONCILE.md). C07, C10 and C15 made no paid call before this and open with the full
USD 25. Rerunning the upgrade never resets an account or a hold that was already settled.
"""

from collections.abc import Sequence
from decimal import Decimal

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID, insert

revision: str = "0138_everyday_story_budget"
down_revision: str | None = "0137_video_manga_tier"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LIMIT_USD = Decimal("25.000000")
HISTORICAL_HOLD = "pre-ledger-history"
UNRECONCILED = (
    "story-everyday-moleskine-c03",
    "story-everyday-bubble-wrap-c04",
    "story-everyday-kincho-c05",
    "story-everyday-play-doh-c06",
)
FRESH = (
    "story-everyday-dr-martens-c07",
    "story-everyday-oxo-c10",
    "story-everyday-frixion-c15",
)


def upgrade() -> None:
    account = sa.table(
        "video_pilot_budgets",
        sa.column("slug", sa.String(length=80)),
        sa.column("limit_usd", sa.Numeric(12, 6)),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    operation = sa.table(
        "video_pilot_budget_operations",
        sa.column("id", UUID(as_uuid=True)),
        sa.column("slug", sa.String(length=80)),
        sa.column("operation_id", sa.String(length=160)),
        sa.column("category", sa.String(length=40)),
        sa.column("provider", sa.String(length=40)),
        sa.column("model", sa.String(length=128)),
        sa.column("max_usd", sa.Numeric(12, 6)),
        sa.column("status", sa.String(length=12)),
        sa.column("attempts", sa.Integer()),
        sa.column("created_at", sa.DateTime(timezone=True)),
        sa.column("updated_at", sa.DateTime(timezone=True)),
    )
    # A typed bind: PostgreSQL refuses a VARCHAR parameter for the numeric columns.
    limit = sa.literal(LIMIT_USD, sa.Numeric(12, 6))
    for slug in UNRECONCILED + FRESH:
        op.execute(
            insert(account)
            .values(slug=slug, limit_usd=limit, created_at=sa.func.now())
            .on_conflict_do_nothing(index_elements=["slug"])
        )
    for slug in UNRECONCILED:
        # The unique (slug, operation_id) pair keeps a settled hold from being reopened.
        op.execute(
            insert(operation)
            .values(
                id=sa.func.gen_random_uuid(),
                slug=slug,
                operation_id=HISTORICAL_HOLD,
                category="historical",
                provider="unattributed",
                model="pre-ledger",
                max_usd=limit,
                status="uncertain",
                attempts=1,
                created_at=sa.func.now(),
                updated_at=sa.func.now(),
            )
            .on_conflict_do_nothing(index_elements=["slug", "operation_id"])
        )


def downgrade() -> None:
    # Dropping an account or its historical hold would erase retained exposure.
    raise RuntimeError("The everyday story budget accounts cannot be downgraded automatically")
