"""Per-video dub languages, and the dubs review gate (docs/videos/DUBS.md).

Revision ID: 0100_video_dub_locales
Revises: 0099_video_drama_series

Every video is made in Traditional Chinese; afterwards the owner ticks, on /admin/videos, which of
en, ja, ko and zh-CN to dub it in (``video_projects.dub_locales``, empty by default), and the
worker makes only those tracks. It submits them as one ``dubs`` review, which the owner approves
once the tracks are uploaded in YouTube Studio, so ``ck_video_review_gate`` admits ``dubs``.

0001 builds a fresh database from the current models, so the column is added only when missing
and the gate check is replaced under its name, as 0095 and 0099 did ('script' stays in
both sets). The downgrade refuses while a dubs
review exists: the narrow check could not hold it.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0100_video_dub_locales"
down_revision: str | None = "0099_video_drama_series"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

PROJECTS = "video_projects"
COLUMN = "dub_locales"
REVIEWS = "video_reviews"
GATE_CHECK = "ck_video_review_gate"
OLD_GATES = "gate IN ('outline', 'script', 'look', 'storyboard', 'audio', 'final', 'publish')"
NEW_GATES = (
    "gate IN ('outline', 'script', 'look', 'storyboard', 'audio', 'final', 'publish', 'dubs')"
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
    if COLUMN not in _columns(PROJECTS):
        op.add_column(
            PROJECTS,
            sa.Column(COLUMN, sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        )
    # The gate check is replaced rather than left alone: a fresh database (0001) already has
    # the wide one under this name, an older one has the narrow one.
    if _offline() or GATE_CHECK in _checks(REVIEWS):
        op.drop_constraint(GATE_CHECK, REVIEWS, type_="check")
    op.create_check_constraint(GATE_CHECK, REVIEWS, NEW_GATES)


def downgrade() -> None:
    if not _offline():
        held = (
            op.get_bind()
            .execute(sa.text(f"SELECT count(*) FROM {REVIEWS} WHERE gate = 'dubs'"))
            .scalar()
        )
        if held:
            raise RuntimeError(f"{held} dubs reviews exist; the narrow gate check cannot hold them")
    op.drop_constraint(GATE_CHECK, REVIEWS, type_="check")
    op.create_check_constraint(GATE_CHECK, REVIEWS, OLD_GATES)
    if _offline() or COLUMN in _columns(PROJECTS):
        op.drop_column(PROJECTS, COLUMN)
