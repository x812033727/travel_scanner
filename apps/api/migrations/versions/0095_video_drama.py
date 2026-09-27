"""The AI drama route's settings and review gates (docs/videos/DRAMA.md).

Revision ID: 0095_video_drama
Revises: 0094_news_final_editor

``video_automation_settings`` gains the media settings of the drama format: which image, clip
and music models, the clip resolution and length, budgets, the judge threshold, the style
preset and the character voice pool. Every column has a server default, so the one existing
row keeps working and the budgets start where the owner asked on 2026-09-26 (wide open, to be
lowered after the pilot). ``video_reviews`` gains ``subject`` (one look review per character)
and its gate check admits ``look`` and ``storyboard``.

0001 builds a fresh database from the current models, so each column and constraint is added
only when missing. The downgrade refuses while a look or storyboard review exists: dropping the
subject and the wider check would orphan the owner's decisions.
"""

import json
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0095_video_drama"
down_revision: str | None = "0094_news_final_editor"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SETTINGS = "video_automation_settings"
REVIEWS = "video_reviews"
GATE_CHECK = "ck_video_review_gate"
OLD_GATES = "gate IN ('outline', 'audio', 'final', 'publish')"
NEW_GATES = "gate IN ('outline', 'look', 'storyboard', 'audio', 'final', 'publish')"
TOPIC_SCOPE = json.dumps(["山海經", "民間傳說", "原創玄幻"], ensure_ascii=True)

# Column name, type, server default. The defaults mirror DEFAULT_DRAMA in
# app/video_automation/models.py; the model catalog is app/video_media/catalog.py.
COLUMNS: tuple[tuple[str, sa.types.TypeEngine[object], str], ...] = (
    ("drama_enabled", sa.Boolean(), "false"),
    ("image_provider", sa.String(16), "'gemini'"),
    ("image_model", sa.String(128), "'gemini-3-pro-image'"),
    ("clip_provider", sa.String(16), "'gemini'"),
    ("clip_model", sa.String(128), "'gemini-omni-1.1-flash'"),
    ("music_provider", sa.String(16), "'gemini'"),
    ("music_model", sa.String(128), "'lyria-3.5'"),
    ("clip_resolution", sa.String(8), "'1080p'"),
    ("clip_seconds_default", sa.Integer(), "8"),
    ("clip_native_audio", sa.Boolean(), "false"),
    ("drama_aspect", sa.String(8), "'16:9'"),
    ("max_clips_per_video", sa.Integer(), "40"),
    ("max_retakes_per_shot", sa.Integer(), "2"),
    ("monthly_clip_seconds_budget", sa.Integer(), "3000"),
    ("monthly_images_budget", sa.Integer(), "1500"),
    ("monthly_judge_calls_budget", sa.Integer(), "3000"),
    ("monthly_music_budget", sa.Integer(), "60"),
    ("max_usd_per_video", sa.Integer(), "200"),
    ("judge_min_score", sa.Integer(), "7"),
    ("auto_approve_storyboard", sa.Boolean(), "false"),
    ("character_voice_pool", sa.JSON(), "'[]'"),
    ("music_enabled", sa.Boolean(), "true"),
    ("subtitle_burn_in", sa.Boolean(), "true"),
    ("style_preset", sa.String(40), "'cinematic-3d'"),
    ("drama_topic_scope", sa.JSON(), f"'{TOPIC_SCOPE}'"),
)

CHECKS: tuple[tuple[str, str], ...] = (
    (
        "ck_video_drama_providers",
        "image_provider IN ('gemini', 'minimax') AND clip_provider IN ('gemini', 'minimax') "
        "AND music_provider IN ('gemini', 'minimax')",
    ),
    ("ck_video_drama_resolution", "clip_resolution IN ('720p', '768p', '1080p', '2k', '4k')"),
    ("ck_video_drama_aspect", "drama_aspect IN ('16:9', '9:16')"),
    ("ck_video_drama_seconds", "clip_seconds_default BETWEEN 4 AND 10"),
    ("ck_video_drama_clips", "max_clips_per_video BETWEEN 1 AND 120"),
    ("ck_video_drama_retakes", "max_retakes_per_shot BETWEEN 0 AND 5"),
    (
        "ck_video_drama_budgets",
        "monthly_clip_seconds_budget BETWEEN 0 AND 100000 "
        "AND monthly_images_budget BETWEEN 0 AND 100000 "
        "AND monthly_judge_calls_budget BETWEEN 0 AND 100000 "
        "AND monthly_music_budget BETWEEN 0 AND 100000",
    ),
    ("ck_video_drama_usd", "max_usd_per_video BETWEEN 0 AND 10000"),
    ("ck_video_drama_judge", "judge_min_score BETWEEN 0 AND 10"),
    (
        "ck_video_drama_preset",
        "style_preset IN ('cinematic-3d', 'anime-2d', 'ink-wash', 'custom')",
    ),
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
    existing = _columns(SETTINGS)
    for name, kind, default in COLUMNS:
        if name not in existing:
            op.add_column(
                SETTINGS, sa.Column(name, kind, nullable=False, server_default=sa.text(default))
            )
    present = _checks(SETTINGS)
    for name, condition in CHECKS:
        if name not in present:
            op.create_check_constraint(name, SETTINGS, condition)

    if "subject" not in _columns(REVIEWS):
        op.add_column(REVIEWS, sa.Column("subject", sa.String(40), nullable=True))
    # The gate check is replaced rather than left alone: a fresh database (0001) already has
    # the wide one under this name, an older one has the narrow one.
    if _offline() or GATE_CHECK in _checks(REVIEWS):
        op.drop_constraint(GATE_CHECK, REVIEWS, type_="check")
    op.create_check_constraint(GATE_CHECK, REVIEWS, NEW_GATES)


def downgrade() -> None:
    if not _offline():
        held = (
            op.get_bind()
            .execute(
                sa.text(f"SELECT count(*) FROM {REVIEWS} WHERE gate IN ('look', 'storyboard')")
            )
            .scalar()
        )
        if held:
            raise RuntimeError(
                f"{held} look or storyboard reviews exist; the narrow gate check cannot hold them"
            )
    op.drop_constraint(GATE_CHECK, REVIEWS, type_="check")
    op.create_check_constraint(GATE_CHECK, REVIEWS, OLD_GATES)
    op.drop_column(REVIEWS, "subject")
    for name, _condition in reversed(CHECKS):
        op.drop_constraint(name, SETTINGS, type_="check")
    for name, _kind, _default in reversed(COLUMNS):
        op.drop_column(SETTINGS, name)
