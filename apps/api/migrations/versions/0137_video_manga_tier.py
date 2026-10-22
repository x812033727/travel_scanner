"""The manga visual tier: every shot a still under a camera move, no clip bought.

Revision ID: 0137_video_manga_tier
Revises: 0136_video_languages_eight

On 2026-10-22 the owner asked for the motion-comic format of the 漫画解说 channels (a narrator
reads the story over a new anime still every few seconds) drawn with MiniMax image-01
(tasks/open/2026-10-22-manga-image-01.md, docs/videos/BINGE.md §畫面等級). The lowest tier so far,
``stills``, still buys one clip in ten, so ``video_drama_series.visual_tier`` takes a fourth
value, ``manga``, whose clip share is zero. Only the check constraint changes: the column, its
default and every stored row stay as they are.

``0001_initial`` builds a fresh database from the current models, which already carry the wide
check under this name, so the constraint is dropped by name when it exists and created again in
its wide form either way; a production database holds the narrow one from 0103. The downgrade
refuses while a manga series exists, since the narrow check could not hold its row.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0137_video_manga_tier"
down_revision: str | None = "0136_video_languages_eight"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SERIES = "video_drama_series"
CHECK = "ck_video_drama_series_tier"
WIDE = "visual_tier IN ('clips', 'hybrid', 'stills', 'manga')"
NARROW = "visual_tier IN ('clips', 'hybrid', 'stills')"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _checks(table: str) -> set[str]:
    if _offline():
        return set()
    return {
        str(check.get("name")) for check in sa.inspect(op.get_bind()).get_check_constraints(table)
    }


def upgrade() -> None:
    if _offline() or CHECK in _checks(SERIES):
        op.drop_constraint(CHECK, SERIES, type_="check")
    op.create_check_constraint(CHECK, SERIES, WIDE)


def downgrade() -> None:
    if not _offline():
        held = (
            op.get_bind()
            .execute(sa.text(f"SELECT count(*) FROM {SERIES} WHERE visual_tier = 'manga'"))
            .scalar()
        )
        if held:
            raise RuntimeError(f"{held} manga series exist; the narrow tier check cannot hold them")
    if _offline() or CHECK in _checks(SERIES):
        op.drop_constraint(CHECK, SERIES, type_="check")
    op.create_check_constraint(CHECK, SERIES, NARROW)
