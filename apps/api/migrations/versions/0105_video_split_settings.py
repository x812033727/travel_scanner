"""The drama's own settings, beside the tutorial's (docs/videos/DRAMA-FLOW.md §一).

Revision ID: 0105_video_split_settings
Revises: 0104_video_retry_request

The settings tab on /admin/videos splits into a tutorial, a drama and a shared part, each saved
on its own, so every value that may differ by format gets a drama column next to the tutorial's:
the stage models (NULL follows the tutorial's), the standing instructions, the narrator voice
(NULL follows the tutorial's), the language defaults, the automatic approval of the narration and
of the final cut, and the fact-check and retake rounds. The existing row keeps behaving as it
did: the standing instructions and the two switches are copied from the tutorial's columns the
moment the drama columns are created, so nothing changes on deploy until the owner edits the
drama part.

0001 builds a fresh database from the current models, so every column is added only when it is
missing, and the copy runs only for a column that was missing (a second upgrade copies nothing).
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0105_video_split_settings"
down_revision: str | None = "0104_video_retry_request"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SETTINGS = "video_automation_settings"
ROUNDS_CHECK = (
    "ck_video_drama_rounds",
    "drama_max_verify_rounds BETWEEN 1 AND 5 AND drama_max_retake_rounds BETWEEN 0 AND 5",
)
# (name, type, server default or None for a nullable column, the tutorial column it copies)
COLUMNS: tuple[tuple[str, sa.types.TypeEngine[object], str | None, str | None], ...] = (
    ("drama_stage_models", sa.JSON(), None, None),
    ("drama_stage_instructions", sa.JSON(), "'{}'", "stage_instructions"),
    ("drama_voice", sa.JSON(), None, None),
    ("drama_caption_locales", sa.JSON(), "'[]'", None),
    ("drama_auto_approve_audio", sa.Boolean(), "true", "auto_approve_audio"),
    ("drama_auto_approve_final", sa.Boolean(), "true", "auto_approve_final"),
    ("drama_max_verify_rounds", sa.Integer(), "3", None),
    ("drama_max_retake_rounds", sa.Integer(), "2", None),
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
    existing = _columns(SETTINGS)
    copies: list[str] = []
    for name, kind, default, source in COLUMNS:
        if name in existing:
            continue
        if default is None:
            op.add_column(SETTINGS, sa.Column(name, kind, nullable=True))
        else:
            op.add_column(
                SETTINGS, sa.Column(name, kind, nullable=False, server_default=sa.text(default))
            )
        if source is not None:
            copies.append(f"{name} = {source}")
    if copies:
        # The row that exists reads as before: the drama starts from the tutorial's values.
        op.execute(f"UPDATE {SETTINGS} SET {', '.join(copies)}")  # noqa: S608
    if ROUNDS_CHECK[0] not in _checks(SETTINGS):
        op.create_check_constraint(ROUNDS_CHECK[0], SETTINGS, ROUNDS_CHECK[1])


def downgrade() -> None:
    if _offline() or ROUNDS_CHECK[0] in _checks(SETTINGS):
        op.drop_constraint(ROUNDS_CHECK[0], SETTINGS, type_="check")
    existing = _columns(SETTINGS)
    for name, _kind, _default, _source in reversed(COLUMNS):
        if _offline() or name in existing:
            op.drop_column(SETTINGS, name)
