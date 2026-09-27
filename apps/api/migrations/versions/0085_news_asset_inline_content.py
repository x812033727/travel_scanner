"""Keep news images in the row on hosts without object storage.

Revision ID: 0085_news_asset_inline_content
Revises: 0084_ai_news_automation
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0085_news_asset_inline_content"
down_revision: str | None = "0084_ai_news_automation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("news_assets", sa.Column("content", sa.LargeBinary(), nullable=True))


def downgrade() -> None:
    op.drop_column("news_assets", "content")
