"""A brand-story series: its kind, its length, a daily count, an image model and a shared look.

Revision ID: 0111_video_story_series
Revises: 0109_video_shorts

A brand story (docs/videos/STORY.md) is an episode of a drama series of ``kind = 'story'``: the
series has no documents, its episodes are the stories of a planned backlog imported ready to
make, and each runs 12 to 15 minutes. So:

- ``ck_video_drama_series_kind`` admits ``story``;
- ``ck_video_drama_series_numbers`` lets ``target_minutes`` be 1 to 20 (the API still holds the
  other kinds to 8);
- ``video_drama_series`` gains ``episodes_per_day`` (how many episodes may start on one
  Asia/Taipei calendar day; NULL is no daily limit, otherwise 1 to 12 under
  ``ck_video_drama_series_per_day``), ``image_model`` (NULL follows the settings tab) and
  ``look`` (JSON: the style, the negative prompt and the motion every story of the series
  shares, since a story series has no setting book to keep them in; NULL for the other kinds).

The number skips 0109 and 0110 on purpose. Two open pull requests add a 0109 on top of 0108 as
well, #898 (``0109_video_shorts``) and #904 (``0109_video_flat_explainer``), and whichever of
them merges second takes the next number. ``down_revision`` names the head main had when this
branch was last pushed: when the pull request leaves draft, set it again to the head main has
then, and the number too if a merged migration took it (skill backend-conventions, "編號會撞").

The columns are added only when missing and the checks replaced whatever their text, so the
upgrade may run again. The downgrade refuses while a story series, or any series longer than 8
minutes, exists: the narrower checks cannot hold those rows, and fitting the owner's rows to
them is not a downgrade's call (0073 and 0107 refuse the same way).
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0111_video_story_series"
down_revision: str | None = "0109_video_shorts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SERIES = "video_drama_series"
KIND_CHECK = "ck_video_drama_series_kind"
OLD_KINDS = "kind IN ('series', 'one-off')"
NEW_KINDS = "kind IN ('series', 'one-off', 'story')"
NUMBERS_CHECK = "ck_video_drama_series_numbers"
OLD_NUMBERS = (
    "planned_episodes BETWEEN 1 AND 500 AND episodes_per_chapter BETWEEN 1 AND 20 "
    "AND target_minutes BETWEEN 1 AND 8"
)
NEW_NUMBERS = (
    "planned_episodes BETWEEN 1 AND 500 AND episodes_per_chapter BETWEEN 1 AND 20 "
    "AND target_minutes BETWEEN 1 AND 20"
)
PER_DAY_CHECK = "ck_video_drama_series_per_day"
PER_DAY = "episodes_per_day IS NULL OR episodes_per_day BETWEEN 1 AND 12"
NEW_COLUMNS = ("episodes_per_day", "image_model", "look")


def _new_columns() -> list[sa.Column[object]]:
    # A Column belongs to one table, so each run builds its own.
    return [
        sa.Column("episodes_per_day", sa.Integer(), nullable=True),
        sa.Column("image_model", sa.String(128), nullable=True),
        sa.Column("look", sa.JSON(), nullable=True),
    ]


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _columns(table: str) -> set[str]:
    return (
        set() if _offline() else {c["name"] for c in sa.inspect(op.get_bind()).get_columns(table)}
    )


def _checks(table: str) -> dict[str, str]:
    if _offline():
        return {}
    return {
        str(check.get("name")): str(check.get("sqltext"))
        for check in sa.inspect(op.get_bind()).get_check_constraints(table)
    }


def _replace_check(name: str, table: str, condition: str) -> None:
    # PostgreSQL stores a BETWEEN as two comparisons, so the text cannot be compared: a check
    # that exists is dropped and written again (0107 does the same).
    if _offline() or name in _checks(table):
        op.drop_constraint(name, table, type_="check")
    op.create_check_constraint(name, table, condition)


def upgrade() -> None:
    present = _columns(SERIES)
    for column in _new_columns():
        if column.name not in present:
            op.add_column(SERIES, column)
    _replace_check(KIND_CHECK, SERIES, NEW_KINDS)
    _replace_check(NUMBERS_CHECK, SERIES, NEW_NUMBERS)
    if PER_DAY_CHECK not in _checks(SERIES):
        op.create_check_constraint(PER_DAY_CHECK, SERIES, PER_DAY)


def downgrade() -> None:
    if not _offline():
        bind = op.get_bind()
        stories = bind.execute(
            sa.text(f"SELECT count(*) FROM {SERIES} WHERE kind = 'story'")
        ).scalar()
        longer = bind.execute(
            sa.text(f"SELECT count(*) FROM {SERIES} WHERE target_minutes > 8")
        ).scalar()
        if stories or longer:
            raise RuntimeError(
                f"{stories} story series and {longer} series longer than 8 minutes exist; the "
                "checks of 0108 cannot hold them. Remove or change those rows by hand first "
                "(withdrawing a series on /admin/videos removes it with its episodes), or stay "
                "on this revision"
            )
    if _offline() or PER_DAY_CHECK in _checks(SERIES):
        op.drop_constraint(PER_DAY_CHECK, SERIES, type_="check")
    _replace_check(NUMBERS_CHECK, SERIES, OLD_NUMBERS)
    _replace_check(KIND_CHECK, SERIES, OLD_KINDS)
    present = _columns(SERIES)
    for name in reversed(NEW_COLUMNS):
        if _offline() or name in present:
            op.drop_column(SERIES, name)
