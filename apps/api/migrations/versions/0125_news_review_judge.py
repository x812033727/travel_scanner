"""The news review judge: a model that decides the review queue and the redraft list.

Revision ID: 0125_news_review_judge
Revises: 0124_video_review_subject

The owner decided on 2026-10-06 that a story waiting in the review queue or the redraft list
is decided by an AI judge from what the admin detail page shows, and that the owner picks its
model. The settings row gains the switch, off until the owner turns it on, and the judge's
vendor and model; the model takes Claude Opus 5.5 whether or not anyone saved it: the column
is new, so nothing was chosen yet. A candidate records the judge's latest answer and the hold
it answered, and ``judge`` joins the assessment types.

Every step inspects first, as 0094 and 0088 do, so a database that already has a column or
the wider check is left alone; offline SQL runs unguarded.

Application deployment rollback does not downgrade the database, so each new column is
nullable or has a server default and the older code can still write its rows. An explicit
downgrade deletes the judge's assessments before it narrows the check: they explain the
candidate columns that are dropped with them, and the older code has no use for either.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0125_news_review_judge"
down_revision: str | None = "0124_video_review_subject"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SETTINGS = "news_automation_settings"
CANDIDATES = "news_candidates"
ASSESSMENTS = "news_assessments"
PROVIDER_CHECK = "ck_news_judge_provider"
DECISION_CHECK = "ck_news_candidate_judge_decision"
TYPE_CHECK = "ck_news_assessment_type"
DEFAULT_PROVIDER = "anthropic"
DEFAULT_MODEL = "claude-opus-5-5"
PROVIDERS = "judge_provider IN ('openai','anthropic','minimax','gemini')"
DECISIONS = "judge_decision IS NULL OR judge_decision IN ('publish','reject','manual','duplicate')"
NEW_TYPE = "judge"
TYPES = ("duplicate", "verification", "locale_review", "jev", "human")


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _columns(table: str) -> set[str]:
    if _offline():
        return set()
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(table)}


def _type_check(types: Sequence[str]) -> str:
    return "assessment_type IN (" + ", ".join(f"'{name}'" for name in types) + ")"


def _existing_type_check(assumed: Sequence[str]) -> str | None:
    # Offline SQL cannot look, so it takes the shape the direction starts from.
    if _offline():
        return _type_check(assumed)
    for check in sa.inspect(op.get_bind()).get_check_constraints(ASSESSMENTS):
        if check.get("name") == TYPE_CHECK:
            return str(check.get("sqltext") or "")
    return None


def upgrade() -> None:
    settings = _columns(SETTINGS)
    if "judge_enabled" not in settings:
        op.add_column(
            SETTINGS,
            sa.Column(
                "judge_enabled", sa.Boolean(), nullable=False, server_default=sa.text("false")
            ),
        )
    if "judge_provider" not in settings:
        op.add_column(
            SETTINGS,
            sa.Column(
                "judge_provider",
                sa.String(16),
                nullable=False,
                server_default=sa.text(f"'{DEFAULT_PROVIDER}'"),
            ),
        )
        op.create_check_constraint(PROVIDER_CHECK, SETTINGS, PROVIDERS)
    if "judge_model" not in settings:
        op.add_column(SETTINGS, sa.Column("judge_model", sa.String(128), nullable=True))
        row = sa.table(SETTINGS, sa.column("judge_model", sa.String(128)))
        op.execute(row.update().values(judge_model=DEFAULT_MODEL))

    candidates = _columns(CANDIDATES)
    if "judge_decision" not in candidates:
        op.add_column(CANDIDATES, sa.Column("judge_decision", sa.String(16), nullable=True))
        op.create_check_constraint(DECISION_CHECK, CANDIDATES, DECISIONS)
    if "judge_hold" not in candidates:
        op.add_column(CANDIDATES, sa.Column("judge_hold", sa.String(64), nullable=True))

    current = _existing_type_check(TYPES)
    if current is None or NEW_TYPE not in current:
        if current is not None:
            op.drop_constraint(TYPE_CHECK, ASSESSMENTS, type_="check")
        op.create_check_constraint(TYPE_CHECK, ASSESSMENTS, _type_check((*TYPES, NEW_TYPE)))


def downgrade() -> None:
    op.execute(f"DELETE FROM {ASSESSMENTS} WHERE assessment_type = '{NEW_TYPE}'")
    current = _existing_type_check((*TYPES, NEW_TYPE))
    if current is not None and NEW_TYPE in current:
        op.drop_constraint(TYPE_CHECK, ASSESSMENTS, type_="check")
        op.create_check_constraint(TYPE_CHECK, ASSESSMENTS, _type_check(TYPES))
    op.drop_constraint(DECISION_CHECK, CANDIDATES, type_="check")
    op.drop_column(CANDIDATES, "judge_hold")
    op.drop_column(CANDIDATES, "judge_decision")
    op.drop_constraint(PROVIDER_CHECK, SETTINGS, type_="check")
    op.drop_column(SETTINGS, "judge_model")
    op.drop_column(SETTINGS, "judge_provider")
    op.drop_column(SETTINGS, "judge_enabled")
