"""Keep each character's look review apart when the characters share one manifest hash.

Revision ID: 0124_video_review_subject
Revises: 0123_video_stage_jobs

review-push binds every character's look review to the same characters/manifest.json, so
the reviews share project, gate and hash and differ only by subject. The old unique
constraint left the subject out, so the second character was handed the first one's review.
The identity becomes (project, gate, subject, hash, revision): one partial unique index for
the rows with a subject, and one for the rows without, since NULLs never collide in a unique
constraint and the gates without a subject must stay exactly as strict as before.

Every existing row already satisfies both indexes: the old constraint was stricter, so the
new indexes are created before it is dropped and no row is read, changed or deleted. 0001
builds tables from the current models (with both indexes) and 0115 then adds the old
constraint to that empty table, so it is dropped here whenever it exists.

Application deployment rollback does not downgrade the database. An explicit downgrade
refuses while two subjects share a hash: restoring the old constraint would need one of
their reviews to be deleted.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0124_video_review_subject"
down_revision: str | None = "0123_video_stage_jobs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

REVIEWS = "video_reviews"
OLD_UNIQUE = "uq_video_review_content_revision"
NO_SUBJECT = "uq_video_review_no_subject"
SUBJECT = "uq_video_review_subject"
OLD_IDENTITY = ("project_id", "gate", "content_sha256", "revision")
SUBJECT_IDENTITY = ("project_id", "gate", "subject", "content_sha256", "revision")
DUPLICATES = (
    f"SELECT 1 FROM {REVIEWS} GROUP BY {', '.join(OLD_IDENTITY)} HAVING count(*) > 1 LIMIT 1"
)
DOWNGRADE_REFUSAL = "several subjects share a review identity; downgrade would discard reviews"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _uniques() -> set[str]:
    if _offline():
        return set()
    return {
        str(constraint.get("name"))
        for constraint in sa.inspect(op.get_bind()).get_unique_constraints(REVIEWS)
    }


def _indexes() -> set[str]:
    if _offline():
        return set()
    return {str(index.get("name")) for index in sa.inspect(op.get_bind()).get_indexes(REVIEWS)}


def upgrade() -> None:
    indexes = _indexes()
    if NO_SUBJECT not in indexes:
        op.create_index(
            NO_SUBJECT,
            REVIEWS,
            list(OLD_IDENTITY),
            unique=True,
            postgresql_where=sa.text("subject IS NULL"),
            sqlite_where=sa.text("subject IS NULL"),
        )
    if SUBJECT not in indexes:
        op.create_index(
            SUBJECT,
            REVIEWS,
            list(SUBJECT_IDENTITY),
            unique=True,
            postgresql_where=sa.text("subject IS NOT NULL"),
            sqlite_where=sa.text("subject IS NOT NULL"),
        )
    if _offline() or OLD_UNIQUE in _uniques():
        op.drop_constraint(OLD_UNIQUE, REVIEWS, type_="unique")


def downgrade() -> None:
    if _offline():
        # Offline SQL must still refuse at execution time, before any schema change.
        op.execute(
            f"DO $$ BEGIN IF EXISTS ({DUPLICATES}) THEN "
            f"RAISE EXCEPTION '{DOWNGRADE_REFUSAL}'; END IF; END; $$"
        )
    elif op.get_bind().execute(sa.text(DUPLICATES)).scalar() is not None:
        raise RuntimeError(DOWNGRADE_REFUSAL)
    # Restore the stricter constraint first, so an insert in between cannot slip past both.
    if OLD_UNIQUE not in _uniques():
        op.create_unique_constraint(OLD_UNIQUE, REVIEWS, list(OLD_IDENTITY))
    indexes = _indexes()
    for name in (SUBJECT, NO_SUBJECT):
        if _offline() or name in indexes:
            op.drop_index(name, table_name=REVIEWS)
