"""A long drama series: the series, its documents and its episodes (docs/videos/SERIES.md).

Revision ID: 0099_video_drama_series
Revises: 0098_video_stage_instructions

``video_drama_series`` is one long series the owner planned on /admin/videos; ``video_drama_docs``
holds its setting book, its whole-series outline and each chapter's detailed outline, one row per
version, with the owner's decision; ``video_drama_episodes`` is the episode table, one row per
planned episode, linked to the video the worker made of it. A request gains ``series_id`` and
``episode_number`` so an episode still travels through the request queue; a project gains
``series_slug`` and ``episode_number`` so the drama tab lists a series' episodes; the review gate
check gains ``script`` (an episode's screenplay, read before any image or clip is paid for); the
settings row gains the series knobs; the stage prompt table is keyed by a ``variant`` too, so a
series document's prompt does not overwrite an episode's.

0001 builds a fresh database from the current models, so every object is added only when it is
missing. The gate check is replaced rather than left alone, as 0095 did. The downgrade drops the
tables and the columns; it refuses while any script review exists, since the narrow gate check
cannot hold them.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0099_video_drama_series"
down_revision: str | None = "0098_video_stage_instructions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SETTINGS = "video_automation_settings"
REQUESTS = "video_drama_requests"
PROJECTS = "video_projects"
REVIEWS = "video_reviews"
PROMPTS = "video_stage_prompts"
SERIES = "video_drama_series"
DOCS = "video_drama_docs"
EPISODES = "video_drama_episodes"
GATE_CHECK = "ck_video_review_gate"
OLD_GATES = "gate IN ('outline', 'look', 'storyboard', 'audio', 'final', 'publish')"
NEW_GATES = "gate IN ('outline', 'script', 'look', 'storyboard', 'audio', 'final', 'publish')"
PRESETS = "'cinematic-3d', 'anime-2d', 'ink-wash', 'custom'"
SETTINGS_COLUMNS: tuple[tuple[str, sa.types.TypeEngine[object], str], ...] = (
    ("series_max_in_flight", sa.Integer(), "1"),
    ("series_script_gate", sa.Boolean(), "true"),
    ("series_auto_continue", sa.Boolean(), "true"),
    ("series_chapter_ahead", sa.Integer(), "2"),
    ("series_doc_rewrites", sa.Integer(), "2"),
    ("series_episodes_per_month", sa.Integer(), "30"),
)
SETTINGS_CHECK = (
    "ck_video_drama_series",
    "series_max_in_flight BETWEEN 1 AND 2 AND series_chapter_ahead BETWEEN 0 AND 10 "
    "AND series_doc_rewrites BETWEEN 0 AND 5 AND series_episodes_per_month BETWEEN 0 AND 500",
)


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _tables() -> set[str]:
    return set() if _offline() else set(sa.inspect(op.get_bind()).get_table_names())


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


def _indexes(table: str) -> set[str]:
    if _offline():
        return set()
    return {str(index.get("name")) for index in sa.inspect(op.get_bind()).get_indexes(table)}


def _create_series() -> None:
    op.create_table(
        SERIES,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("slug", sa.String(40), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("premise", sa.Text(), nullable=False),
        sa.Column("aspects", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("tone", sa.String(40), nullable=False, server_default="dual-male-leads-subtext"),
        sa.Column("style_preset", sa.String(40), nullable=False, server_default="cinematic-3d"),
        sa.Column("target_minutes", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("planned_episodes", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("episodes_per_chapter", sa.Integer(), nullable=False, server_default="10"),
        sa.Column("open_ended", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("status", sa.String(12), nullable=False, server_default="setting"),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("requested_chapter", sa.Integer(), nullable=True),
        sa.Column("force_next", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "created_by_user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", name="fk_video_drama_series_user", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("slug", name="uq_video_drama_series_slug"),
        sa.CheckConstraint(
            "status IN ('setting', 'outline', 'active', 'paused', 'finished')",
            name="ck_video_drama_series_status",
        ),
        sa.CheckConstraint(
            "planned_episodes BETWEEN 1 AND 500 AND episodes_per_chapter BETWEEN 4 AND 20 "
            "AND target_minutes BETWEEN 1 AND 8",
            name="ck_video_drama_series_numbers",
        ),
        sa.CheckConstraint(f"style_preset IN ({PRESETS})", name="ck_video_drama_series_style"),
    )


def _create_docs() -> None:
    op.create_table(
        DOCS,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "series_id",
            sa.Uuid(),
            sa.ForeignKey(f"{SERIES}.id", name="fk_video_drama_docs_series", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("kind", sa.String(12), nullable=False),
        sa.Column("chapter_number", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("body_md", sa.Text(), nullable=False),
        sa.Column("body_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("status", sa.String(12), nullable=False, server_default="review"),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "decided_by_user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", name="fk_video_drama_docs_user", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "series_id", "kind", "chapter_number", "version", name="uq_video_drama_doc_version"
        ),
        sa.CheckConstraint(
            "kind IN ('setting', 'outline', 'chapter')", name="ck_video_drama_doc_kind"
        ),
        sa.CheckConstraint(
            "status IN ('generating', 'review', 'approved', 'rejected')",
            name="ck_video_drama_doc_status",
        ),
        sa.CheckConstraint(
            "version >= 1 AND chapter_number >= 0", name="ck_video_drama_doc_numbers"
        ),
    )


def _create_episodes() -> None:
    op.create_table(
        EPISODES,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "series_id",
            sa.Uuid(),
            sa.ForeignKey(
                f"{SERIES}.id", name="fk_video_drama_episodes_series", ondelete="CASCADE"
            ),
            nullable=False,
        ),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("chapter_number", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("logline", sa.Text(), nullable=False, server_default=""),
        sa.Column("beats", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("status", sa.String(12), nullable=False, server_default="planned"),
        sa.Column("slug", sa.String(80), nullable=True),
        sa.Column(
            "request_id",
            sa.Uuid(),
            sa.ForeignKey(
                f"{REQUESTS}.id", name="fk_video_drama_episodes_request", ondelete="SET NULL"
            ),
            nullable=True,
        ),
        sa.Column("recap", sa.Text(), nullable=True),
        sa.Column("state_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("series_id", "number", name="uq_video_drama_episode_number"),
        sa.UniqueConstraint("slug", name="uq_video_drama_episode_slug"),
        sa.CheckConstraint(
            "status IN ('planned', 'ready', 'queued', 'started', 'done', 'skipped')",
            name="ck_video_drama_episode_status",
        ),
        sa.CheckConstraint(
            "number >= 1 AND chapter_number >= 1", name="ck_video_drama_episode_numbers"
        ),
    )


def upgrade() -> None:
    tables = _tables()
    if SERIES not in tables:
        _create_series()
    if DOCS not in tables:
        _create_docs()
    if EPISODES not in tables:
        _create_episodes()

    requests = _columns(REQUESTS)
    if "series_id" not in requests:
        op.add_column(
            REQUESTS,
            sa.Column(
                "series_id",
                sa.Uuid(),
                sa.ForeignKey(
                    f"{SERIES}.id", name="fk_video_drama_requests_series", ondelete="SET NULL"
                ),
                nullable=True,
            ),
        )
    if "episode_number" not in requests:
        op.add_column(REQUESTS, sa.Column("episode_number", sa.Integer(), nullable=True))

    projects = _columns(PROJECTS)
    if "series_slug" not in projects:
        op.add_column(PROJECTS, sa.Column("series_slug", sa.String(40), nullable=True))
    if "episode_number" not in projects:
        op.add_column(PROJECTS, sa.Column("episode_number", sa.Integer(), nullable=True))
    if "ix_video_projects_series_slug" not in _indexes(PROJECTS):
        op.create_index("ix_video_projects_series_slug", PROJECTS, ["series_slug"])

    settings = _columns(SETTINGS)
    for name, kind, default in SETTINGS_COLUMNS:
        if name not in settings:
            op.add_column(
                SETTINGS, sa.Column(name, kind, nullable=False, server_default=sa.text(default))
            )
    if SETTINGS_CHECK[0] not in _checks(SETTINGS):
        op.create_check_constraint(SETTINGS_CHECK[0], SETTINGS, SETTINGS_CHECK[1])

    if "variant" not in _columns(PROMPTS):
        op.add_column(
            PROMPTS, sa.Column("variant", sa.String(32), nullable=False, server_default="")
        )
        op.drop_constraint("video_stage_prompts_pkey", PROMPTS, type_="primary")
        op.create_primary_key("video_stage_prompts_pkey", PROMPTS, ["stage", "format", "variant"])

    # The gate check is replaced rather than left alone: a fresh database (0001) already has
    # the wide one under this name, an older one has the narrow one.
    if _offline() or GATE_CHECK in _checks(REVIEWS):
        op.drop_constraint(GATE_CHECK, REVIEWS, type_="check")
    op.create_check_constraint(GATE_CHECK, REVIEWS, NEW_GATES)


def downgrade() -> None:
    if not _offline():
        held = (
            op.get_bind()
            .execute(sa.text(f"SELECT count(*) FROM {REVIEWS} WHERE gate = 'script'"))
            .scalar()
        )
        if held:
            raise RuntimeError(
                f"{held} script reviews exist; the narrow gate check cannot hold them"
            )
    op.drop_constraint(GATE_CHECK, REVIEWS, type_="check")
    op.create_check_constraint(GATE_CHECK, REVIEWS, OLD_GATES)
    if _offline() or "variant" in _columns(PROMPTS):
        op.drop_constraint("video_stage_prompts_pkey", PROMPTS, type_="primary")
        op.drop_column(PROMPTS, "variant")
        op.create_primary_key("video_stage_prompts_pkey", PROMPTS, ["stage", "format"])
    if _offline() or SETTINGS_CHECK[0] in _checks(SETTINGS):
        op.drop_constraint(SETTINGS_CHECK[0], SETTINGS, type_="check")
    settings = _columns(SETTINGS)
    for name, _kind, _default in reversed(SETTINGS_COLUMNS):
        if _offline() or name in settings:
            op.drop_column(SETTINGS, name)
    if _offline() or "ix_video_projects_series_slug" in _indexes(PROJECTS):
        op.drop_index("ix_video_projects_series_slug", table_name=PROJECTS)
    projects = _columns(PROJECTS)
    for name in ("episode_number", "series_slug"):
        if _offline() or name in projects:
            op.drop_column(PROJECTS, name)
    tables = _tables()
    if _offline() or EPISODES in tables:
        op.drop_table(EPISODES)
    requests = _columns(REQUESTS)
    for name in ("episode_number", "series_id"):
        if _offline() or name in requests:
            op.drop_column(REQUESTS, name)
    if _offline() or DOCS in tables:
        op.drop_table(DOCS)
    if _offline() or SERIES in tables:
        op.drop_table(SERIES)
