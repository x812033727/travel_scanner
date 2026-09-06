"""Let a guide AI search record a Gemini run.

Revision ID: 0051_guide_run_gemini
Revises: 0050_hotspot_themes_intros

``hotspot_guide_ai_search_runs`` has carried the same three providers since 0021, while the
setting that chooses one, its request payload and ``AIProviderName`` all grew a fourth. An
administrator who picked Gemini got a 500 from the INSERT rather than a queued run.

0001 still calls the current ``Base.metadata.create_all``, so a fresh database already has
the widened constraint and there is nothing to drop; the step inspects first, through the
operations context so the migration tests can drive it, and offline SQL runs unguarded.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0051_guide_run_gemini"
down_revision: str | None = "0050_hotspot_themes_intros"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "hotspot_guide_ai_search_runs"
CONSTRAINT = "ck_hotspot_guide_ai_search_provider"
WITH_GEMINI = "provider IN ('minimax', 'openai', 'anthropic', 'gemini')"
WITHOUT_GEMINI = "provider IN ('minimax', 'openai', 'anthropic')"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _existing_check() -> str | None:
    """The constraint's current text, or None when the table has none by that name."""
    if _offline():
        return WITHOUT_GEMINI
    checks = sa.inspect(op.get_bind()).get_check_constraints(TABLE)
    for check in checks:
        if check.get("name") == CONSTRAINT:
            return str(check.get("sqltext") or "")
    return None


def upgrade() -> None:
    current = _existing_check()
    if current is not None and "gemini" in current:
        return
    if current is not None:
        op.drop_constraint(CONSTRAINT, TABLE, type_="check")
    op.create_check_constraint(CONSTRAINT, TABLE, WITH_GEMINI)


def downgrade() -> None:
    current = _existing_check()
    if current is None or "gemini" not in current:
        return
    op.drop_constraint(CONSTRAINT, TABLE, type_="check")
    op.create_check_constraint(CONSTRAINT, TABLE, WITHOUT_GEMINI)
