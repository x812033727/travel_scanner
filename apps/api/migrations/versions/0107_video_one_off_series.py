"""A one-off drama is a series of one episode with a story bible (docs/videos/DRAMA-FLOW.md §二).

Revision ID: 0107_video_one_off_series
Revises: 0106_video_locales

The owner's one-off dramas used to travel as bare requests: the planner wrote a brief, the owner
picked an outline on a card, and there was no screenplay gate. Now a one-off is a
``video_drama_series`` row of ``kind = 'one-off'`` with one episode and one document, the story
bible, and from there it walks the same road as an episode of a long series. So:

- ``video_drama_series.kind`` (``series`` | ``one-off``), and ``ck_video_drama_series_numbers``
  lets ``episodes_per_chapter`` be 1;
- ``ck_video_drama_doc_kind`` admits ``bible``;
- every request still queued and not yet an episode becomes a one-off series
  (``one-off-<first 8 of the request id>``, the request's title or premise, style, length and
  note), with its episode 1 planned and the request row pointing at it (``series_id``,
  ``episode_number = 1``); the worker starts it through the series path once the bible is
  approved. A request already started walks the old road to its end and is left alone.

0001 builds a fresh database from the current models, so the column and the checks are added or
replaced only when they are missing or narrow. The downgrade refuses while a one-off series or a
bible document exists, since the narrow checks cannot hold them.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0107_video_one_off_series"
down_revision: str | None = "0106_video_locales"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SERIES = "video_drama_series"
DOCS = "video_drama_docs"
EPISODES = "video_drama_episodes"
REQUESTS = "video_drama_requests"
KIND_CHECK = "ck_video_drama_series_kind"
NUMBERS_CHECK = "ck_video_drama_series_numbers"
OLD_NUMBERS = (
    "planned_episodes BETWEEN 1 AND 500 AND episodes_per_chapter BETWEEN 4 AND 20 "
    "AND target_minutes BETWEEN 1 AND 8"
)
NEW_NUMBERS = (
    "planned_episodes BETWEEN 1 AND 500 AND episodes_per_chapter BETWEEN 1 AND 20 "
    "AND target_minutes BETWEEN 1 AND 8"
)
DOC_KIND_CHECK = "ck_video_drama_doc_kind"
OLD_DOC_KINDS = "kind IN ('setting', 'outline', 'chapter')"
NEW_DOC_KINDS = "kind IN ('setting', 'outline', 'chapter', 'bible')"

# Every queued request that is not an episode yet becomes a one-off series with its episode 1
# planned; the request keeps its row and points at the series. Three statements, all keyed by
# the request id, so a second run finds nothing left to convert.
CONVERT_SERIES = f"""
INSERT INTO {SERIES} (
    id, slug, kind, title, premise, aspects, tone, style_preset, target_minutes,
    planned_episodes, episodes_per_chapter, open_ended, status, note, force_next,
    created_by_user_id, created_at, updated_at
)
SELECT
    r.id, 'one-off-' || left(replace(r.id::text, '-', ''), 8), 'one-off',
    left(coalesce(r.title, r.premise), 200), r.premise, '[]', 'dual-male-leads-subtext',
    r.style_preset, r.target_minutes, 1, 1, false, 'setting', r.note, false,
    r.created_by_user_id, r.created_at, r.updated_at
FROM {REQUESTS} r
WHERE r.status = 'queued' AND r.series_id IS NULL
"""
CONVERT_EPISODES = f"""
INSERT INTO {EPISODES} (
    id, series_id, number, chapter_number, title, logline, beats, status, state_json,
    created_at, updated_at
)
SELECT gen_random_uuid(), r.id, 1, 1, left(coalesce(r.title, r.premise), 200), '', '{{}}',
    'planned', '{{}}', r.created_at, r.updated_at
FROM {REQUESTS} r
WHERE r.status = 'queued' AND r.series_id IS NULL
"""
CONVERT_REQUESTS = f"""
UPDATE {REQUESTS} SET series_id = id, episode_number = 1
WHERE status = 'queued' AND series_id IS NULL
"""


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
    if _offline() or name in _checks(table):
        op.drop_constraint(name, table, type_="check")
    op.create_check_constraint(name, table, condition)


def upgrade() -> None:
    if "kind" not in _columns(SERIES):
        op.add_column(
            SERIES, sa.Column("kind", sa.String(12), nullable=False, server_default="series")
        )
    if KIND_CHECK not in _checks(SERIES):
        op.create_check_constraint(KIND_CHECK, SERIES, "kind IN ('series', 'one-off')")
    # The checks are replaced rather than left alone, as 0099 did with the gate check: a fresh
    # database (0001) already has the wide ones under these names, an older one has the narrow
    # ones, and PostgreSQL stores a BETWEEN as two comparisons, so the text cannot be compared.
    _replace_check(NUMBERS_CHECK, SERIES, NEW_NUMBERS)
    _replace_check(DOC_KIND_CHECK, DOCS, NEW_DOC_KINDS)
    if not _offline():
        # The rows already carry series_id once converted, so this runs to nothing again.
        bind = op.get_bind()
        bind.execute(sa.text(CONVERT_SERIES))
        bind.execute(sa.text(CONVERT_EPISODES))
        bind.execute(sa.text(CONVERT_REQUESTS))


def downgrade() -> None:
    if not _offline():
        bind = op.get_bind()
        one_offs = bind.execute(
            sa.text(f"SELECT count(*) FROM {SERIES} WHERE kind = 'one-off'")
        ).scalar()
        bibles = bind.execute(sa.text(f"SELECT count(*) FROM {DOCS} WHERE kind = 'bible'")).scalar()
        if one_offs or bibles:
            raise RuntimeError(
                f"{one_offs} one-off series and {bibles} bible documents exist; "
                "the narrow checks cannot hold them"
            )
    _replace_check(DOC_KIND_CHECK, DOCS, OLD_DOC_KINDS)
    _replace_check(NUMBERS_CHECK, SERIES, OLD_NUMBERS)
    if _offline() or KIND_CHECK in _checks(SERIES):
        op.drop_constraint(KIND_CHECK, SERIES, type_="check")
    if _offline() or "kind" in _columns(SERIES):
        op.drop_column(SERIES, "kind")
