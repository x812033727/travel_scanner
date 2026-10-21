"""Seed independent USD 25 full-film accounts for the October brand-story batch.

Revision ID: 0137_brand_story_batch_budget
Revises: 0136_video_languages_eight

The application registers these five slugs before their accounts are usable, so a
missing account refuses every paid dispatch. The existing budget constraint already
allows USD 25. Retain accounts and operation receipts on rollback; an application
rollback after any story starts must keep its worker stopped until the guarded code
is restored.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import insert

revision: str = "0137_brand_story_batch_budget"
down_revision: str | None = "0136_video_languages_eight"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

ACCOUNT = "video_pilot_budgets"
BRAND_STORIES = (
    "story-new-20261020-muji-no-brand",
    "story-new-20261020-ikea-flatpack",
    "story-new-20261020-garmin-after-smartphones",
    "story-new-20261020-uniqlo-everyday-clothes",
    "story-new-20261020-giant-own-name",
)


def upgrade() -> None:
    account = sa.table(
        ACCOUNT,
        sa.column("slug", sa.String(length=80)),
        sa.column("limit_usd", sa.Numeric(12, 6)),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    for slug in BRAND_STORIES:
        op.execute(
            insert(account)
            .values(slug=slug, limit_usd=sa.literal(25), created_at=sa.func.now())
            .on_conflict_do_nothing(index_elements=["slug"])
        )


def downgrade() -> None:
    raise RuntimeError("Brand-story budget accounts and receipts cannot be removed automatically")
