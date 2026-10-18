"""The cute-cartoon and cute-mystery style presets for the explainer route.

Revision ID: 0130_video_cute_presets
Revises: 0128_video_languages_four

The illustrated explainer (0113's ``flat-explainer``: narrator only, every shot a still) becomes
a family of three. ``cute-cartoon`` is So That's Why redrawn as a cute cartoon and
``cute-mystery`` is the history-and-curiosity series (docs/videos/history-curiosity/); both are
picked wherever a style preset is picked, so the three checks that list the presets are
recreated with them, under the same names. No row is rewritten. The downgrade refuses while any
row still uses either name, since the old checks cannot hold that row.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0130_video_cute_presets"
down_revision: str | None = "0128_video_languages_four"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

OLD_PRESETS = ("cinematic-3d", "anime-2d", "ink-wash", "flat-explainer", "custom")
NEW_PRESETS = (
    "cinematic-3d", "anime-2d", "ink-wash", "flat-explainer", "cute-cartoon", "cute-mystery",
    "custom",
)
CUTE_PRESETS = ("cute-cartoon", "cute-mystery")
# (table, check name): every place a style preset is stored.
CHECKS: tuple[tuple[str, str], ...] = (
    ("video_automation_settings", "ck_video_drama_preset"),
    ("video_drama_requests", "ck_video_drama_request_style"),
    ("video_drama_series", "ck_video_drama_series_style"),
)


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _checks(table: str) -> set[str]:
    if _offline():
        return set()
    return {
        str(check.get("name")) for check in sa.inspect(op.get_bind()).get_check_constraints(table)
    }


def _text(presets: Sequence[str]) -> str:
    return "style_preset IN ({})".format(", ".join(f"'{preset}'" for preset in presets))


def _replace(presets: Sequence[str]) -> None:
    for table, name in CHECKS:
        if _offline() or name in _checks(table):
            op.drop_constraint(name, table, type_="check")
        op.create_check_constraint(name, table, _text(presets))


def upgrade() -> None:
    _replace(NEW_PRESETS)


def downgrade() -> None:
    if not _offline():
        bind = op.get_bind()
        for table, _name in CHECKS:
            used = bind.execute(
                sa.text(
                    f"SELECT count(*) FROM {table} WHERE style_preset IN (:cartoon, :mystery)"
                ),
                {"cartoon": CUTE_PRESETS[0], "mystery": CUTE_PRESETS[1]},
            ).scalar()
            if used:
                raise RuntimeError(
                    f"{used} rows of {table} use the cute-cartoon or cute-mystery preset; "
                    "change them to another preset first"
                )
    _replace(OLD_PRESETS)
