"""A binge series: genre, hands-off gates, visual tier and the compilation (docs/videos/BINGE.md).

Revision ID: 0103_video_binge_series
Revises: 0102_video_youtube_sync

``video_drama_series`` gains the genre preset the planner writes from, who leads, whether the
series is hands-off (its documents, screenplays, sheets and storyboards are decided by the
checks), whether its episodes are compiled into one long video, the compilation length the
owner asked for, the visual tier (how many shots may be image-to-video clips), and the
compilation video's slug with when it started and finished. The settings row's series check
is recreated so up to six episodes may be in the making at once.

0001 builds a fresh database from the current models, so every column and check is added only
when it is missing. The settings check is replaced rather than left alone, as 0099 created it
with the narrower bound. The downgrade refuses while any settings row keeps more than two
episodes in flight or any series is hands-off or compiled, since the old columns and bound
cannot hold them.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0103_video_binge_series"
down_revision: str | None = "0102_video_youtube_sync"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SETTINGS = "video_automation_settings"
SERIES = "video_drama_series"
SETTINGS_CHECK = (
    "ck_video_drama_series",
    "series_max_in_flight BETWEEN 1 AND 6 AND series_chapter_ahead BETWEEN 0 AND 10 "
    "AND series_doc_rewrites BETWEEN 0 AND 5 AND series_episodes_per_month BETWEEN 0 AND 500",
)
OLD_SETTINGS_CHECK = (
    "series_max_in_flight BETWEEN 1 AND 2 AND series_chapter_ahead BETWEEN 0 AND 10 "
    "AND series_doc_rewrites BETWEEN 0 AND 5 AND series_episodes_per_month BETWEEN 0 AND 500"
)
SERIES_COLUMNS: tuple[tuple[str, sa.types.TypeEngine[object], str | None], ...] = (
    ("genre", sa.String(32), "'xianxia-bonds'"),
    ("lead", sa.String(12), "'dual-male'"),
    ("hands_off", sa.Boolean(), "false"),
    ("compilation", sa.Boolean(), "false"),
    ("visual_tier", sa.String(8), "'clips'"),
    ("total_minutes", sa.Integer(), None),
    ("compilation_slug", sa.String(80), None),
    ("compilation_started_at", sa.DateTime(timezone=True), None),
    ("compilation_finished_at", sa.DateTime(timezone=True), None),
)
SERIES_CHECKS: tuple[tuple[str, str], ...] = (
    (
        "ck_video_drama_series_genre",
        "genre IN ('xianxia-bonds', 'rebirth-revenge', 'system-game', 'urban-return', "
        "'empress-rise', 'custom')",
    ),
    ("ck_video_drama_series_lead", "lead IN ('female', 'male', 'dual-male')"),
    ("ck_video_drama_series_tier", "visual_tier IN ('clips', 'hybrid', 'stills')"),
    (
        "ck_video_drama_series_total_minutes",
        "total_minutes IS NULL OR total_minutes BETWEEN 30 AND 480",
    ),
)
COMPILATION_UNIQUE = "uq_video_drama_series_compilation_slug"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _columns(table: str) -> set[str]:
    if _offline():
        return set()
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(table)}


def _checks(table: str) -> set[str]:
    if _offline():
        return set()
    return {
        str(check.get("name")) for check in sa.inspect(op.get_bind()).get_check_constraints(table)
    }


def _uniques(table: str) -> set[str]:
    if _offline():
        return set()
    return {
        str(unique.get("name"))
        for unique in sa.inspect(op.get_bind()).get_unique_constraints(table)
    }


def upgrade() -> None:
    columns = _columns(SERIES)
    for name, kind, default in SERIES_COLUMNS:
        if name in columns:
            continue
        if default is None:
            op.add_column(SERIES, sa.Column(name, kind, nullable=True))
        else:
            op.add_column(
                SERIES, sa.Column(name, kind, nullable=False, server_default=sa.text(default))
            )
    checks = _checks(SERIES)
    for name, text in SERIES_CHECKS:
        if name not in checks:
            op.create_check_constraint(name, SERIES, text)
    if COMPILATION_UNIQUE not in _uniques(SERIES):
        op.create_unique_constraint(COMPILATION_UNIQUE, SERIES, ["compilation_slug"])
    # The settings check is replaced: a fresh database (0001) already has the wide one under
    # this name, an older one has the narrow one from 0099.
    if _offline() or SETTINGS_CHECK[0] in _checks(SETTINGS):
        op.drop_constraint(SETTINGS_CHECK[0], SETTINGS, type_="check")
    op.create_check_constraint(SETTINGS_CHECK[0], SETTINGS, SETTINGS_CHECK[1])


def downgrade() -> None:
    if not _offline():
        bind = op.get_bind()
        wide = bind.execute(
            sa.text(f"SELECT count(*) FROM {SETTINGS} WHERE series_max_in_flight > 2")
        ).scalar()
        if wide:
            raise RuntimeError("a settings row keeps more than two episodes in flight")
        held = bind.execute(
            sa.text(f"SELECT count(*) FROM {SERIES} WHERE hands_off OR compilation")
        ).scalar()
        if held:
            raise RuntimeError(
                f"{held} hands-off or compiled series exist; the old columns cannot hold them"
            )
    if _offline() or SETTINGS_CHECK[0] in _checks(SETTINGS):
        op.drop_constraint(SETTINGS_CHECK[0], SETTINGS, type_="check")
    op.create_check_constraint(SETTINGS_CHECK[0], SETTINGS, OLD_SETTINGS_CHECK)
    if _offline() or COMPILATION_UNIQUE in _uniques(SERIES):
        op.drop_constraint(COMPILATION_UNIQUE, SERIES, type_="unique")
    checks = _checks(SERIES)
    for name, _text in reversed(SERIES_CHECKS):
        if _offline() or name in checks:
            op.drop_constraint(name, SERIES, type_="check")
    columns = _columns(SERIES)
    for name, _kind, _default in reversed(SERIES_COLUMNS):
        if _offline() or name in columns:
            op.drop_column(SERIES, name)
