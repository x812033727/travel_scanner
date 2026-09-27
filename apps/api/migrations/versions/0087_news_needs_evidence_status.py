"""Keep news candidates that stopped at the evidence gate out of manual review.

Revision ID: 0087_news_needs_evidence_status
Revises: 0086_video_tool_tokens

A candidate without evidence from two websites (one first-party) stops before any model
call. Until now it went to ``manual_review``, where on 2026-09-24 it made up 83 of 147
rows an editor could not act on. It gets its own status, ``needs_evidence``, and the rows
already waiting are moved there.

0001 builds a fresh database from the current models, which already carry the widened
constraint, so the step inspects first (as 0083 does) and offline SQL runs unguarded.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0087_news_needs_evidence_status"
down_revision: str | None = "0086_video_tool_tokens"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "news_candidates"
CONSTRAINT = "ck_news_candidate_status"
NEW_STATUS = "needs_evidence"
STATUSES = (
    "discovered",
    "drafting",
    "verifying",
    "locale_review",
    "jev_review",
    "shadow_review",
    "manual_review",
    "published",
    "duplicate",
    "rejected",
    "failed",
)


def _check(statuses: Sequence[str]) -> str:
    return "status IN (" + ", ".join(f"'{status}'" for status in statuses) + ")"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _existing_check() -> str | None:
    if _offline():
        return _check(STATUSES)
    for check in sa.inspect(op.get_bind()).get_check_constraints(TABLE):
        if check.get("name") == CONSTRAINT:
            return str(check.get("sqltext") or "")
    return None


def upgrade() -> None:
    current = _existing_check()
    if current is None or NEW_STATUS not in current:
        if current is not None:
            op.drop_constraint(CONSTRAINT, TABLE, type_="check")
        op.create_check_constraint(CONSTRAINT, TABLE, _check((*STATUSES, NEW_STATUS)))
    op.execute(
        f"UPDATE {TABLE} SET status = '{NEW_STATUS}' "
        "WHERE status = 'manual_review' AND error_code = 'news_evidence_insufficient'"
    )


def downgrade() -> None:
    op.execute(f"UPDATE {TABLE} SET status = 'manual_review' WHERE status = '{NEW_STATUS}'")
    current = _existing_check()
    if current is not None and NEW_STATUS in current:
        op.drop_constraint(CONSTRAINT, TABLE, type_="check")
        op.create_check_constraint(CONSTRAINT, TABLE, _check(STATUSES))
