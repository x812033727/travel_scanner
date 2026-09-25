"""The news final editor: a third model that checks each of the five locales before Jev.

Revision ID: 0094_news_final_editor
Revises: 0092_video_subscription_limit

The owner decided on 2026-09-25 that a final editor checks every translated locale against
the evidence before Jev makes the last call, and that it runs on Claude Opus 5.5 by default
(on the subscription accounts when the AI vendors card says so). The settings row takes that
default whether or not anyone saved it: the column is new, so nothing was chosen yet.

0001 builds a fresh database from the current models, so the columns are added only when
missing.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0094_news_final_editor"
down_revision: str | None = "0092_video_subscription_limit"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "news_automation_settings"
CONSTRAINT = "ck_news_editor_provider"
DEFAULT_PROVIDER = "anthropic"
DEFAULT_MODEL = "claude-opus-5-5"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def upgrade() -> None:
    columns = (
        set()
        if _offline()
        else {column["name"] for column in sa.inspect(op.get_bind()).get_columns(TABLE)}
    )
    if _offline() or "editor_provider" not in columns:
        op.add_column(
            TABLE,
            sa.Column(
                "editor_provider",
                sa.String(16),
                nullable=False,
                server_default=sa.text(f"'{DEFAULT_PROVIDER}'"),
            ),
        )
        op.create_check_constraint(
            CONSTRAINT, TABLE, "editor_provider IN ('openai','anthropic','minimax','gemini')"
        )
    if _offline() or "editor_model" not in columns:
        op.add_column(TABLE, sa.Column("editor_model", sa.String(128), nullable=True))
        settings = sa.table(TABLE, sa.column("editor_model", sa.String(128)))
        op.execute(settings.update().values(editor_model=DEFAULT_MODEL))


def downgrade() -> None:
    op.drop_constraint(CONSTRAINT, TABLE, type_="check")
    op.drop_column(TABLE, "editor_model")
    op.drop_column(TABLE, "editor_provider")
