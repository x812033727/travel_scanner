"""The language panel pre-ticks titles and captions in all eight languages a video may add.

Revision ID: 0136_video_languages_eight
Revises: 0135_video_backup

On 2026-10-20 the owner let the video worker make titles, descriptions and captions in es, pt,
id, vi and th as well as en, ja and ko, for every category
(tasks/open/2026-10-19-worker-video-languages-five.md), and chose that the settings tab's
language defaults pre-tick titles and captions in all eight, for the tutorials
(``video_automation_settings.caption_locales``, 0090) and the drama (``drama_caption_locales``,
0105) alike. Dubs are never pre-ticked; these lists carry no dub. The settings row already
stores its lists (``["en", "ja", "ko"]`` and the drama's own), so the new code default alone
would never reach it: this writes the eight, in the page's order, into every settings row, and
the drama column's server default follows the model. Writing the same list again changes
nothing, so a re-run is harmless. The owner may untick any language on the settings tab
afterwards. Nothing else is touched: a video's own choice (``video_projects.locales``) stays as
the owner saved it.

The columns are json, not jsonb, so the downgrade drops the five with
``json_array_elements_text`` and ``json_agg`` rather than the ``-`` operator
(tests/test_migration_sql_dialect.py), keeping the other languages in their order; only rows
that hold one of the five are touched. A video's saved choice of the five is left alone: the
previous release reads it, and only refuses a new save of it on a video that was not imported.
"""

import json
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0136_video_languages_eight"
down_revision: str | None = "0135_video_backup"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_automation_settings"
COLUMNS = ("caption_locales", "drama_caption_locales")
EIGHT = ("en", "ja", "ko", "es", "pt", "id", "vi", "th")
FIVE = EIGHT[3:]
EIGHT_JSON = json.dumps(list(EIGHT))
PREVIOUS_DRAMA_DEFAULT = "'[]'"
_FIVE_SQL = ", ".join(f"'{locale}'" for locale in FIVE)

UPGRADE = f"UPDATE {TABLE} SET " + ", ".join(
    f"{column} = '{EIGHT_JSON}'::json" for column in COLUMNS
)


def drop_the_five(column: str) -> str:
    """A json array of strings without es, pt, id, vi and th, in its order; [] when empty."""
    return (
        f"UPDATE {TABLE} SET {column} = COALESCE("
        "(SELECT json_agg(item.value ORDER BY item.ord) "
        f"FROM json_array_elements_text({column}) WITH ORDINALITY AS item(value, ord) "
        f"WHERE item.value NOT IN ({_FIVE_SQL})), '[]'::json) "
        f"WHERE json_typeof({column}) = 'array' AND EXISTS ("
        f"SELECT 1 FROM json_array_elements_text({column}) AS found(value) "
        f"WHERE found.value IN ({_FIVE_SQL}))"
    )


DOWNGRADE = tuple(drop_the_five(column) for column in COLUMNS)


def upgrade() -> None:
    op.execute(UPGRADE)
    op.alter_column(
        TABLE,
        "drama_caption_locales",
        existing_type=sa.JSON(),
        server_default=sa.text(f"'{EIGHT_JSON}'"),
    )


def downgrade() -> None:
    op.alter_column(
        TABLE,
        "drama_caption_locales",
        existing_type=sa.JSON(),
        server_default=sa.text(PREVIOUS_DRAMA_DEFAULT),
    )
    for statement in DOWNGRADE:
        op.execute(statement)
