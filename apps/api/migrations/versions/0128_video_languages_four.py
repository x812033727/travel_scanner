"""A video's languages are four: zh-CN leaves the video pipeline (docs/videos/LANGUAGES.md).

Revision ID: 0128_video_languages_four
Revises: 0127_video_slides_requests

The owner decided on 2026-10-09 that a YouTube video is narrated in zh-TW and may add en, ja
and ko, nothing else; the site keeps its five locales, the videos do not. The API's language
literals narrow to those three with this release, so a stored ``zh-CN`` would no longer read:
``video_projects.locales`` (the owner's choice per video, 0106) loses its ``"zh-CN"`` key, and
the three default lists, ``video_automation_settings.caption_locales`` (0090),
``video_automation_settings.drama_caption_locales`` (0105) and ``video_shorts_settings.locales``
(0109), lose their ``"zh-CN"`` element. The columns are json, not jsonb, so the rewrite is
done with ``json_each`` / ``json_array_elements_text`` and the aggregates rather than the ``-``
operator (tests/test_migration_sql_dialect.py). Only rows that hold the key or element are
touched, so a re-run changes nothing. ``video_projects.dub_locales`` (0101) is legacy and
unread since 0106; it is left alone. An approved languages batch that named zh-CN stays as it
is: the API ignores that language when it reads the batch, so the other languages keep syncing.

The downgrade is a no-op: which rows named zh-CN is not recorded, and the previous release read
rows without it just as well.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0128_video_languages_four"
down_revision: str | None = "0127_video_slides_requests"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

RETIRED = "zh-CN"
PROJECTS = "video_projects"
AUTOMATION_SETTINGS = "video_automation_settings"
SHORTS_SETTINGS = "video_shorts_settings"
# A json object without the retired key; an object left empty is {} rather than NULL.
DROP_PROJECT_KEY = (
    f"UPDATE {PROJECTS} SET locales = COALESCE("
    "(SELECT json_object_agg(entry.key, entry.value) FROM json_each(locales) AS entry "
    f"WHERE entry.key <> '{RETIRED}'), '{{}}'::json) "
    "WHERE json_typeof(locales) = 'object' AND EXISTS ("
    f"SELECT 1 FROM json_object_keys(locales) AS found WHERE found = '{RETIRED}')"
)


def drop_list_element(table: str, column: str) -> str:
    """A json array of strings without the retired element; an array left empty is []."""
    return (
        f"UPDATE {table} SET {column} = COALESCE("
        f"(SELECT json_agg(item.value) FROM json_array_elements_text({column}) AS item "
        f"WHERE item.value <> '{RETIRED}'), '[]'::json) "
        f"WHERE json_typeof({column}) = 'array' AND EXISTS ("
        f"SELECT 1 FROM json_array_elements_text({column}) AS item WHERE item.value = '{RETIRED}')"
    )


STATEMENTS = (
    DROP_PROJECT_KEY,
    drop_list_element(AUTOMATION_SETTINGS, "caption_locales"),
    drop_list_element(AUTOMATION_SETTINGS, "drama_caption_locales"),
    drop_list_element(SHORTS_SETTINGS, "locales"),
)


def upgrade() -> None:
    for statement in STATEMENTS:
        op.execute(statement)


def downgrade() -> None:
    # Nothing to restore: the rows that named zh-CN are not recorded, and the previous release
    # read a choice or a default list without it just as well.
    return
