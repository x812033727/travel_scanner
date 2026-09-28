"""Each video's languages, and the languages review gate (docs/videos/LANGUAGES.md).

Revision ID: 0106_video_locales
Revises: 0105_video_split_settings

Every video is made in Traditional Chinese; after its final cut the owner chooses, on
/admin/videos, which of en, ja, ko and zh-CN to add and what of each: the title and description,
the captions, a dub track. ``video_projects.locales`` holds that choice ({"en": {"metadata":
true, "captions": true, "dub": false}}, only the languages chosen) and ``locales_decided_at``
when the owner first saved it, "only Traditional Chinese" included; the worker makes only what
was chosen and submits it as one ``languages`` review, so ``ck_video_review_gate`` admits
``languages``.

``dub_locales`` (0101) was the dub part of the same choice: it is copied into ``locales`` with
all three parts on, and a video that is on YouTube already, or had dub languages ticked, counts as
decided, so only videos still in the making wait for the owner. The column stays, unread.

0001 builds a fresh database from the current models, so the columns are added only when
missing, the copy runs only then, and the gate check is replaced under its name, as 0101 did.
The downgrade refuses while a languages review exists: the narrow check could not hold it.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0106_video_locales"
down_revision: str | None = "0105_video_split_settings"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

PROJECTS = "video_projects"
REVIEWS = "video_reviews"
GATE_CHECK = "ck_video_review_gate"
OLD_GATES = (
    "gate IN ('outline', 'script', 'look', 'storyboard', 'audio', 'final', 'publish', 'dubs')"
)
NEW_GATES = (
    "gate IN ('outline', 'script', 'look', 'storyboard', 'audio', 'final', 'publish', 'dubs', "
    "'languages')"
)
# The dub part of the choice, as it was ticked, becomes a whole language: descriptions, captions
# and the dub. json functions only: the column is json, not jsonb.
COPY_DUBS = (
    f"UPDATE {PROJECTS} SET locales = ("
    'SELECT json_object_agg(value, \'{"metadata": true, "captions": true, "dub": true}\'::json) '
    "FROM json_array_elements_text(dub_locales)) "
    "WHERE dub_locales::text <> '[]'"
)
MARK_DECIDED = (
    f"UPDATE {PROJECTS} SET locales_decided_at = now() "
    "WHERE locales_decided_at IS NULL "
    "AND (youtube_video_id IS NOT NULL OR dub_locales::text <> '[]')"
)


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _columns(table: str) -> set[str]:
    return (
        set() if _offline() else {c["name"] for c in sa.inspect(op.get_bind()).get_columns(table)}
    )


def _checks(table: str) -> set[str]:
    if _offline():
        return set()
    return {
        str(check.get("name")) for check in sa.inspect(op.get_bind()).get_check_constraints(table)
    }


def upgrade() -> None:
    existing = _columns(PROJECTS)
    added = False
    if "locales" not in existing:
        op.add_column(
            PROJECTS,
            sa.Column("locales", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        )
        added = True
    if "locales_decided_at" not in existing:
        op.add_column(
            PROJECTS, sa.Column("locales_decided_at", sa.DateTime(timezone=True), nullable=True)
        )
        added = True
    if added:
        op.execute(COPY_DUBS)
        op.execute(MARK_DECIDED)
    # The gate check is replaced rather than left alone: a fresh database (0001) already has
    # the wide one under this name, an older one has the narrow one.
    if _offline() or GATE_CHECK in _checks(REVIEWS):
        op.drop_constraint(GATE_CHECK, REVIEWS, type_="check")
    op.create_check_constraint(GATE_CHECK, REVIEWS, NEW_GATES)


def downgrade() -> None:
    if not _offline():
        held = (
            op.get_bind()
            .execute(sa.text(f"SELECT count(*) FROM {REVIEWS} WHERE gate = 'languages'"))
            .scalar()
        )
        if held:
            raise RuntimeError(
                f"{held} languages reviews exist; the narrow gate check cannot hold them"
            )
    op.drop_constraint(GATE_CHECK, REVIEWS, type_="check")
    op.create_check_constraint(GATE_CHECK, REVIEWS, OLD_GATES)
    existing = _columns(PROJECTS)
    for name in ("locales_decided_at", "locales"):
        if _offline() or name in existing:
            op.drop_column(PROJECTS, name)
