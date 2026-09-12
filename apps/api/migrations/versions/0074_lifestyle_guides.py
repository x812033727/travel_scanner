"""Lifestyle articles: a third article kind and a section on every topic.

Revision ID: 0074_lifestyle_guides
Revises: 0073_catalog_run_enrich_mode

``guide_articles.kind`` gains ``life`` and ``guide_topics`` gains ``section`` so the
lifestyle area (``/life``) reuses the article system instead of getting a second one. Both
changes rewrite a constraint rather than add a plain column, so each is guarded by what
the database actually has: ``0001_initial`` builds from the current models, so a fresh
database already carries the three-value CHECK and the column, while a database upgrading
from 0072 has neither. The seven lifestyle topics are seeded after the column exists (an
upgrading PostgreSQL would otherwise fail with ``column "section" does not exist``) under
0072's contract: only absent slugs are inserted and nothing an administrator changed is
touched.

Known limits. SQLite has no ALTER for constraints, so both rewrites go through
``batch_alter_table``, which rebuilds the table; under ``PRAGMA foreign_keys=ON`` the
referencing tables refuse that rebuild, which is why ``tests/test_guides_migration.py``
runs this file on an engine without the pragma. The migrate container runs before the API
starts, but a hand-ordered deploy that starts the new API first would see its first
lifestyle article rejected by the old CHECK at INSERT time -- the trap ``0055`` documents.

The downgrade never raises. It removes the seeded lifestyle topics (their article links
first: SQLite without the pragma does not cascade), drops the section CHECK before the
column (the SQLite rebuild would otherwise reflect a CHECK naming a column that is gone),
and restores the two-value kind CHECK only when no ``life`` row exists. A rollback that
deletes an editor's articles to fit a constraint is worse than one that keeps the wider
constraint.
"""

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from alembic import context, op
from sqlalchemy.engine import Connection
from sqlalchemy.engine.reflection import Inspector

revision: str = "0074_lifestyle_guides"
down_revision: str | None = "0073_catalog_run_enrich_mode"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

KIND_CHECK = "ck_guide_article_kind"
SECTION_CHECK = "ck_guide_topic_section"
# Each predicate stays on one line: SQLite reflection reads a CHECK back with a
# single-line regular expression, and a predicate it cannot read is one it cannot drop.
KIND_PREDICATE = "kind IN ('intel', 'howto', 'life')"
LEGACY_KIND_PREDICATE = "kind IN ('intel', 'howto')"
SECTION_PREDICATE = "section IN ('travel', 'life')"
LOCALES = ("en", "ja", "ko", "zh-TW", "zh-CN")

# slug, display_order, (en, ja, ko, zh-TW, zh-CN); display_order continues after 0072's 190.
LIFE_SEED_TOPICS: tuple[tuple[str, int, tuple[str, str, str, str, str]], ...] = (
    ("ai", 200, ("AI tools", "AIツール", "AI 도구", "AI 工具", "AI 工具")),
    ("tutorial", 210, ("Tutorials", "チュートリアル", "튜토리얼", "教學", "教程")),
    (
        "software",
        220,
        ("Apps & software", "アプリ・ソフト", "앱·소프트웨어", "軟體與 App", "软件与应用"),
    ),
    ("gadgets", 230, ("Gadgets", "ガジェット", "가젯", "3C 裝置", "3C 设备")),
    ("productivity", 240, ("Productivity", "仕事効率化", "생산성", "效率工作", "效率工作")),
    ("daily", 250, ("Everyday life", "暮らし", "일상", "生活雜記", "生活杂记")),
    ("misc", 260, ("Other", "その他", "기타", "其他", "其他")),
)
REMOVE_LIFE_LINKS = (
    "DELETE FROM guide_article_topics WHERE topic_id IN "
    "(SELECT id FROM guide_topics WHERE section = 'life' AND source = 'seed')"
)
REMOVE_LIFE_TOPICS = "DELETE FROM guide_topics WHERE section = 'life' AND source = 'seed'"


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    _widen_kind_check(inspector)
    _add_topic_section(inspector)
    # After the column exists, never before: an upgrading database has no ``section``
    # until the batch above runs, and the seed writes it.
    _seed_life_topics()


def _check_constraints(inspector: Inspector, table: str) -> dict[str, str]:
    return {
        str(row.get("name")): str(row.get("sqltext") or "")
        for row in inspector.get_check_constraints(table)
    }


def _widen_kind_check(inspector: Inspector | None) -> None:
    present = True
    if inspector is not None:
        checks = _check_constraints(inspector, "guide_articles")
        if "'life'" in checks.get(KIND_CHECK, ""):
            # 0001 built the table from the current model; PostgreSQL's constraint
            # definition still spells the literals out, so the same test reads there.
            return
        present = KIND_CHECK in checks
    with op.batch_alter_table("guide_articles") as batch:
        if present:
            batch.drop_constraint(KIND_CHECK, type_="check")
        batch.create_check_constraint(KIND_CHECK, KIND_PREDICATE)


def _add_topic_section(inspector: Inspector | None) -> None:
    if inspector is not None:
        columns = {column["name"] for column in inspector.get_columns("guide_topics")}
        if "section" in columns:
            return
    with op.batch_alter_table("guide_topics") as batch:
        batch.add_column(
            sa.Column("section", sa.String(16), nullable=False, server_default="travel")
        )
        batch.create_check_constraint(SECTION_CHECK, SECTION_PREDICATE)


def _seed_life_topics() -> None:
    """The lifestyle vocabulary, not any article: 0072's contract, with a section."""
    if context.is_offline_mode():
        return
    existing = set(op.get_bind().execute(sa.text("SELECT slug FROM guide_topics")).scalars())
    missing = [entry for entry in LIFE_SEED_TOPICS if entry[0] not in existing]
    if not missing:
        return
    now = datetime.now(UTC)
    op.bulk_insert(
        sa.table(
            "guide_topics",
            sa.column("id", sa.Uuid()),
            sa.column("slug", sa.String()),
            sa.column("names_json", sa.JSON()),
            sa.column("display_order", sa.Integer()),
            sa.column("is_active", sa.Boolean()),
            sa.column("source", sa.String()),
            sa.column("section", sa.String()),
            sa.column("created_at", sa.DateTime(timezone=True)),
            sa.column("updated_at", sa.DateTime(timezone=True)),
        ),
        [
            {
                "id": uuid4(),
                "slug": slug,
                "names_json": dict(zip(LOCALES, labels, strict=True)),
                "display_order": order,
                "is_active": True,
                "source": "seed",
                "section": "life",
                "created_at": now,
                "updated_at": now,
            }
            for slug, order, labels in missing
        ],
    )


def downgrade() -> None:
    if context.is_offline_mode():
        op.execute(REMOVE_LIFE_LINKS)
        op.execute(REMOVE_LIFE_TOPICS)
        with op.batch_alter_table("guide_topics") as batch:
            batch.drop_constraint(SECTION_CHECK, type_="check")
            batch.drop_column("section")
        with op.batch_alter_table("guide_articles") as batch:
            batch.drop_constraint(KIND_CHECK, type_="check")
            batch.create_check_constraint(KIND_CHECK, LEGACY_KIND_PREDICATE)
        return
    bind = op.get_bind()
    tables = set(sa.inspect(bind).get_table_names())
    if "guide_topics" in tables:
        _drop_topic_section(bind, "guide_article_topics" in tables)
    if "guide_articles" in tables:
        _narrow_kind_check(bind)


def _drop_topic_section(bind: Connection, has_links: bool) -> None:
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("guide_topics")}
    if "section" not in columns:
        return
    if has_links:
        bind.execute(sa.text(REMOVE_LIFE_LINKS))
    bind.execute(sa.text(REMOVE_LIFE_TOPICS))
    checks = _check_constraints(inspector, "guide_topics")
    with op.batch_alter_table("guide_topics") as batch:
        # The CHECK first. On SQLite the rebuild reflects every constraint the table has,
        # and one that names a column the new table lacks makes the CREATE TABLE fail.
        if SECTION_CHECK in checks:
            batch.drop_constraint(SECTION_CHECK, type_="check")
        batch.drop_column("section")


def _narrow_kind_check(bind: Connection) -> None:
    checks = _check_constraints(sa.inspect(bind), "guide_articles")
    if "'life'" not in checks.get(KIND_CHECK, ""):
        return
    life_rows = bind.scalar(sa.text("SELECT count(*) FROM guide_articles WHERE kind = 'life'"))
    if life_rows:
        # Keeping the wider CHECK is the honest rollback: the rows stay, the API that
        # comes back is the one that never wrote them, and nothing was destroyed.
        return
    with op.batch_alter_table("guide_articles") as batch:
        batch.drop_constraint(KIND_CHECK, type_="check")
        batch.create_check_constraint(KIND_CHECK, LEGACY_KIND_PREDICATE)
