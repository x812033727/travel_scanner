"""Keep separate decisions when a Short's evidence changes for the same final MP4.

Revision ID: 0115_video_review_revision
Revises: 0114_video_slides_media

The content hash continues to identify the real reviewed file. A nonnegative revision
distinguishes decisions about new QA evidence without overwriting earlier decisions.
Existing rows receive revision zero from the default; their hashes and payloads stay intact.
0001 creates tables from the current models, so columns and constraints are inspected before
changing them. Old application code can still insert rows through the server default.

Application deployment rollback does not downgrade the database. An explicit downgrade
refuses when several revisions share the old identity: preserving review history takes
precedence over restoring the old unique constraint. No review is deleted or rewritten.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0115_video_review_revision"
down_revision: str | None = "0114_video_slides_media"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

REVIEWS = "video_reviews"
OLD_UNIQUE = "uq_video_review_content"
NEW_UNIQUE = "uq_video_review_content_revision"
REVISION_CHECK = "ck_video_review_revision"
CONTENT_IDENTITY = ("project_id", "gate", "content_sha256")
DUPLICATES = (
    f"SELECT 1 FROM {REVIEWS} GROUP BY project_id, gate, content_sha256 HAVING count(*) > 1 LIMIT 1"
)
DOWNGRADE_REFUSAL = "multiple review revisions exist; downgrade would discard review history"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _columns() -> set[str]:
    if _offline():
        return set()
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(REVIEWS)}


def _checks() -> set[str]:
    if _offline():
        return set()
    return {
        str(check.get("name")) for check in sa.inspect(op.get_bind()).get_check_constraints(REVIEWS)
    }


def _uniques() -> set[str]:
    if _offline():
        return set()
    return {
        str(constraint.get("name"))
        for constraint in sa.inspect(op.get_bind()).get_unique_constraints(REVIEWS)
    }


def upgrade() -> None:
    if "revision" not in _columns():
        op.add_column(
            REVIEWS,
            sa.Column("revision", sa.Integer(), nullable=False, server_default=sa.text("0")),
        )
    if REVISION_CHECK not in _checks():
        op.create_check_constraint(REVISION_CHECK, REVIEWS, "revision >= 0")
    unique_names = _uniques()
    if NEW_UNIQUE not in unique_names:
        op.create_unique_constraint(NEW_UNIQUE, REVIEWS, [*CONTENT_IDENTITY, "revision"])
    if _offline() or OLD_UNIQUE in unique_names:
        op.drop_constraint(OLD_UNIQUE, REVIEWS, type_="unique")


def downgrade() -> None:
    if _offline():
        # Offline SQL must still refuse at execution time, before any destructive DDL.
        op.execute(
            f"DO $$ BEGIN IF EXISTS ({DUPLICATES}) THEN "
            f"RAISE EXCEPTION '{DOWNGRADE_REFUSAL}'; END IF; END; $$"
        )
    elif op.get_bind().execute(sa.text(DUPLICATES)).scalar() is not None:
        raise RuntimeError(DOWNGRADE_REFUSAL)
    unique_names = _uniques()
    # Restore the stricter constraint first. It also catches an intervening insert before
    # either the revision constraint or column can be removed.
    if OLD_UNIQUE not in unique_names:
        op.create_unique_constraint(OLD_UNIQUE, REVIEWS, list(CONTENT_IDENTITY))
    if _offline() or NEW_UNIQUE in unique_names:
        op.drop_constraint(NEW_UNIQUE, REVIEWS, type_="unique")
    if _offline() or REVISION_CHECK in _checks():
        op.drop_constraint(REVISION_CHECK, REVIEWS, type_="check")
    if _offline() or "revision" in _columns():
        op.drop_column(REVIEWS, "revision")
