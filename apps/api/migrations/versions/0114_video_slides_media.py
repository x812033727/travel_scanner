"""Illustrated slides: the pictures' switch, image model, cap, storyboard rule and media names.

Revision ID: 0114_video_slides_media
Revises: 0113_video_flat_explainer

The settings row gains the illustrated slides' fields (docs/videos/ILLUSTRATED.md): the switch
that lets a slides video draw pictures (``slides_media_enabled``, off), its own image model
(``slides_image_model``, gemini-3.1-flash-image; NULL follows the drama's), its per-video cap
(``slides_max_usd_per_video``, US$20), whether its storyboard approves itself from the judge's
scores (``slides_auto_approve_storyboard``, on: the owner decided that on 2026-09-29), and the
owner's licensed music file and sound-effect set the worker gives every new video
(``slides_music_track``, ``slides_sfx_set``, NULL until the owner names them).

0001 builds a fresh database from the current models, so every column is added only when it is
missing, and the cap's check only when it is not there.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0114_video_slides_media"
down_revision: str | None = "0113_video_flat_explainer"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SETTINGS = "video_automation_settings"
USD_CHECK = ("ck_video_slides_usd", "slides_max_usd_per_video BETWEEN 0 AND 10000")
# (name, type, nullable, server default or None)
COLUMNS: tuple[tuple[str, sa.types.TypeEngine[object], bool, str | None], ...] = (
    ("slides_media_enabled", sa.Boolean(), False, "false"),
    ("slides_image_model", sa.String(128), True, "'gemini-3.1-flash-image'"),
    ("slides_max_usd_per_video", sa.Integer(), False, "20"),
    ("slides_auto_approve_storyboard", sa.Boolean(), False, "true"),
    ("slides_music_track", sa.String(80), True, None),
    ("slides_sfx_set", sa.String(64), True, None),
)


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


def upgrade() -> None:
    present = _columns(SETTINGS)
    for name, kind, nullable, default in COLUMNS:
        if name in present:
            continue
        op.add_column(
            SETTINGS,
            sa.Column(
                name,
                kind,
                nullable=nullable,
                server_default=sa.text(default) if default is not None else None,
            ),
        )
    if USD_CHECK[0] not in _checks(SETTINGS):
        op.create_check_constraint(USD_CHECK[0], SETTINGS, USD_CHECK[1])


def downgrade() -> None:
    if _offline() or USD_CHECK[0] in _checks(SETTINGS):
        op.drop_constraint(USD_CHECK[0], SETTINGS, type_="check")
    present = _columns(SETTINGS)
    for name, _kind, _nullable, _default in reversed(COLUMNS):
        if _offline() or name in present:
            op.drop_column(SETTINGS, name)
