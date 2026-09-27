"""Keep news candidates that stopped before a five-locale article out of manual review.

Revision ID: 0088_news_needs_redraft_status
Revises: 0087_news_needs_evidence_status

A candidate the verifier, a locale review, the hard checks or the claim and date checks
stopped has no saved article: nothing an editor can publish or fix in the guide editor,
only a new draft or a rejection. On 2026-09-24 those made up most of the 66 rows in
manual review, burying the two a person could actually decide. They get their own status,
``needs_redraft``, and the rows already waiting are moved there.

0001 builds a fresh database from the current models, which already carry the widened
constraint, so the step inspects first (as 0087 does) and offline SQL runs unguarded.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0088_news_needs_redraft_status"
down_revision: str | None = "0087_news_needs_evidence_status"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "news_candidates"
CONSTRAINT = "ck_news_candidate_status"
NEW_STATUS = "needs_redraft"
STATUSES = (
    "discovered",
    "drafting",
    "verifying",
    "locale_review",
    "jev_review",
    "shadow_review",
    "manual_review",
    "needs_evidence",
    "published",
    "duplicate",
    "rejected",
    "failed",
)
# The pipeline stops that happen before the five-locale article is saved.
REDRAFT_CODES = (
    "news_claim_source_invalid",
    "news_event_date_invalid",
    "news_verification_failed",
    "news_locale_review_failed",
    "news_hard_checks_failed",
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
    codes = ", ".join(f"'{code}'" for code in REDRAFT_CODES)
    op.execute(
        f"UPDATE {TABLE} SET status = '{NEW_STATUS}' "
        f"WHERE status = 'manual_review' AND error_code IN ({codes}) "
        "AND guide_article_id IS NULL"
    )


def downgrade() -> None:
    op.execute(f"UPDATE {TABLE} SET status = 'manual_review' WHERE status = '{NEW_STATUS}'")
    current = _existing_check()
    if current is not None and NEW_STATUS in current:
        op.drop_constraint(CONSTRAINT, TABLE, type_="check")
        op.create_check_constraint(CONSTRAINT, TABLE, _check(STATUSES))
