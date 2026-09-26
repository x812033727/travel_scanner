"""The channel stance and the hands-off switches (docs/videos/HANDS-OFF.md).

Revision ID: 0100_video_hands_off
Revises: 0099_video_drama_series

The settings row gains ``channel_stance`` (what this channel believes, the only source the
planner writes the owner's viewpoint from) and three switches: ``auto_pick_outline`` (Jev
chooses the outline; no effect while the stance is blank), ``auto_approve_final`` (the final cut
and the upload confirmation approve themselves when the automatic quality check passes) and
``auto_pick_look`` (a drama character's sheet is picked by the judge's score). A project gains
``youtube_publish_at``, the time the owner chose on the "ready to upload" list, and its
``youtube_video_id`` is held to YouTube's eleven characters.

0001 builds a fresh database from the current models, so every column is added only when it is
missing. The id check is created NOT VALID: rows written before it are not re-read, new writes
are held to it.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0100_video_hands_off"
down_revision: str | None = "0099_video_drama_series"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SETTINGS = "video_automation_settings"
PROJECTS = "video_projects"
ID_CHECK = (
    "ck_video_project_youtube_id",
    "youtube_video_id IS NULL OR length(youtube_video_id) = 11",
)
SETTINGS_COLUMNS: tuple[tuple[str, sa.types.TypeEngine[object], str], ...] = (
    ("channel_stance", sa.Text(), "''"),
    ("auto_pick_outline", sa.Boolean(), "true"),
    ("auto_approve_final", sa.Boolean(), "true"),
    ("auto_pick_look", sa.Boolean(), "false"),
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
    settings = _columns(SETTINGS)
    for name, kind, default in SETTINGS_COLUMNS:
        if name not in settings:
            op.add_column(
                SETTINGS, sa.Column(name, kind, nullable=False, server_default=sa.text(default))
            )
    if "youtube_publish_at" not in _columns(PROJECTS):
        op.add_column(
            PROJECTS, sa.Column("youtube_publish_at", sa.DateTime(timezone=True), nullable=True)
        )
    if ID_CHECK[0] not in _checks(PROJECTS):
        op.create_check_constraint(ID_CHECK[0], PROJECTS, ID_CHECK[1], postgresql_not_valid=True)


def downgrade() -> None:
    if _offline() or ID_CHECK[0] in _checks(PROJECTS):
        op.drop_constraint(ID_CHECK[0], PROJECTS, type_="check")
    if _offline() or "youtube_publish_at" in _columns(PROJECTS):
        op.drop_column(PROJECTS, "youtube_publish_at")
    settings = _columns(SETTINGS)
    for name, _kind, _default in reversed(SETTINGS_COLUMNS):
        if _offline() or name in settings:
            op.drop_column(SETTINGS, name)
