"""First-party travel intel and guide articles with per-locale publication.

Revision ID: 0072_travel_guides
Revises: 0071_collection_item_lookup
"""

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from alembic import context, op

revision: str = "0072_travel_guides"
down_revision: str | None = "0071_collection_item_lookup"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LOCALE_CHECK = "locale IN ('en', 'ja', 'ko', 'zh-TW', 'zh-CN')"

# slug, display_order, (en, ja, ko, zh-TW, zh-CN)
SEED_TOPICS: tuple[tuple[str, int, tuple[str, str, str, str, str]], ...] = (
    ("transport", 10, ("Transport", "交通", "교통", "交通", "交通")),
    ("entry", 20, ("Entry rules", "入国手続き", "입국 규정", "簽證入境", "签证入境")),
    ("packing", 30, ("Before you go", "出発前の準備", "출발 전 준비", "行前準備", "行前准备")),
    ("itinerary", 40, ("Itineraries", "モデルコース", "추천 일정", "行程範例", "行程范例")),
    ("budget", 50, ("Budget", "予算", "예산", "預算", "预算")),
    ("deal", 60, ("Deals", "お得情報", "할인 정보", "優惠情報", "优惠情报")),
    ("season", 70, ("Seasonal", "季節の催し", "계절 행사", "季節活動", "季节活动")),
    (
        "connectivity",
        80,
        ("Staying online", "通信・ネット", "통신・인터넷", "網路通訊", "网络通讯"),
    ),
    ("etiquette", 90, ("Etiquette", "マナー", "에티켓", "禮儀文化", "礼仪文化")),
    ("safety", 100, ("Safety", "安全・緊急時", "안전・비상", "安全應變", "安全应变")),
    ("food", 110, ("Food", "グルメ", "음식", "美食", "美食")),
    ("shopping", 120, ("Shopping", "ショッピング", "쇼핑", "購物", "购物")),
    ("hotel", 130, ("Hotels", "ホテル", "호텔", "飯店", "酒店")),
    ("culture", 140, ("Culture", "文化", "문화", "文化", "文化")),
    ("nature", 150, ("Nature", "自然", "자연", "自然", "自然")),
    ("family", 160, ("Family", "家族向け", "가족 여행", "親子", "亲子")),
    ("nightlife", 170, ("Nightlife", "ナイトライフ", "야간 활동", "夜生活", "夜生活")),
    ("viewpoint", 180, ("Viewpoints", "展望スポット", "전망 명소", "觀景", "观景")),
    ("beach", 190, ("Beaches", "ビーチ", "해변", "海灘", "海滩")),
)
LOCALES = ("en", "ja", "ko", "zh-TW", "zh-CN")


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    # 0001 creates current metadata on a fresh database. Never recreate those tables, and
    # never let a migration publish an article as a side effect.
    if inspector is None or not inspector.has_table("guide_topics"):
        op.create_table(
            "guide_topics",
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column("slug", sa.String(64), nullable=False),
            sa.Column("names_json", sa.JSON(), nullable=False),
            sa.Column("display_order", sa.Integer(), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("source", sa.String(16), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("slug", name="uq_guide_topic_slug"),
            sa.CheckConstraint("source IN ('seed', 'admin')", name="ck_guide_topic_source"),
        )
        op.create_index("ix_guide_topics_slug", "guide_topics", ["slug"])
        op.create_index(
            "ix_guide_topics_active_order", "guide_topics", ["is_active", "display_order"]
        )
        _seed_topics()

    if inspector is None or not inspector.has_table("guide_articles"):
        op.create_table(
            "guide_articles",
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column("slug", sa.String(120), nullable=False),
            sa.Column("kind", sa.String(16), nullable=False),
            sa.Column("destination_id", sa.String(64), nullable=True),
            sa.Column("valid_until", sa.Date(), nullable=True),
            sa.Column("featured", sa.Boolean(), nullable=False),
            sa.Column("display_order", sa.Integer(), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("version", sa.Integer(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("slug", name="uq_guide_article_slug"),
            sa.CheckConstraint("kind IN ('intel', 'howto')", name="ck_guide_article_kind"),
            sa.CheckConstraint("version >= 1", name="ck_guide_article_version"),
        )
        op.create_index("ix_guide_articles_slug", "guide_articles", ["slug"])
        op.create_index("ix_guide_articles_destination_id", "guide_articles", ["destination_id"])
        op.create_index("ix_guide_articles_is_active", "guide_articles", ["is_active"])
        op.create_index("ix_guide_articles_kind_active", "guide_articles", ["kind", "is_active"])

    if inspector is None or not inspector.has_table("guide_article_locales"):
        op.create_table(
            "guide_article_locales",
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column(
                "article_id",
                sa.Uuid(),
                sa.ForeignKey("guide_articles.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("locale", sa.String(16), nullable=False),
            sa.Column("version", sa.Integer(), nullable=False),
            sa.Column("draft_json", sa.JSON(), nullable=False),
            sa.Column("published_version", sa.Integer(), nullable=True),
            sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("article_id", "locale", name="uq_guide_article_locale"),
            sa.CheckConstraint(LOCALE_CHECK, name="ck_guide_article_locale_locale"),
            sa.CheckConstraint("version >= 1", name="ck_guide_article_locale_version"),
            sa.CheckConstraint(
                "published_version IS NULL OR "
                "(published_version >= 1 AND published_version <= version)",
                name="ck_guide_article_locale_published_version",
            ),
        )
        op.create_index(
            "ix_guide_article_locales_article_id", "guide_article_locales", ["article_id"]
        )
        op.create_index("ix_guide_article_locales_locale", "guide_article_locales", ["locale"])
        op.create_index(
            "ix_guide_article_locales_public",
            "guide_article_locales",
            ["locale", "published_at"],
        )

    if inspector is None or not inspector.has_table("guide_article_revisions"):
        op.create_table(
            "guide_article_revisions",
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column(
                "article_locale_id",
                sa.Uuid(),
                sa.ForeignKey("guide_article_locales.id"),
                nullable=False,
            ),
            sa.Column("version", sa.Integer(), nullable=False),
            sa.Column("action", sa.String(32), nullable=False),
            sa.Column("document_json", sa.JSON(), nullable=False),
            sa.Column(
                "created_by_user_id",
                sa.Uuid(),
                sa.ForeignKey("users.id", ondelete="SET NULL"),
                nullable=True,
            ),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint(
                "article_locale_id", "version", name="uq_guide_article_revision_version"
            ),
            sa.CheckConstraint("version >= 1", name="ck_guide_article_revision_version"),
            sa.CheckConstraint(
                "action IN ('created', 'draft_saved', 'published', 'unpublished', 'restored')",
                name="ck_guide_article_revision_action",
            ),
        )
        op.create_index(
            "ix_guide_article_revisions_article_locale_id",
            "guide_article_revisions",
            ["article_locale_id"],
        )
        op.create_index(
            "ix_guide_article_revisions_created_by_user_id",
            "guide_article_revisions",
            ["created_by_user_id"],
        )

    if inspector is None or not inspector.has_table("guide_article_topics"):
        op.create_table(
            "guide_article_topics",
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column(
                "article_id",
                sa.Uuid(),
                sa.ForeignKey("guide_articles.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column(
                "topic_id",
                sa.Uuid(),
                sa.ForeignKey("guide_topics.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.UniqueConstraint("article_id", "topic_id", name="uq_guide_article_topic"),
        )
        op.create_index(
            "ix_guide_article_topics_article_id", "guide_article_topics", ["article_id"]
        )
        op.create_index("ix_guide_article_topics_topic_id", "guide_article_topics", ["topic_id"])

    _append_only_guard()


def _seed_topics() -> None:
    """The subject vocabulary, not any article. Adding a topic is not publishing content."""
    if context.is_offline_mode():
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
                "created_at": now,
                "updated_at": now,
            }
            for slug, order, labels in SEED_TOPICS
        ],
    )


def _append_only_guard() -> None:
    """History a reviewer can trust has to be enforced where the writes land, not in the
    service that writes them. Nulling ``created_by_user_id`` stays allowed: account
    erasure must still be able to detach a person from a revision."""
    if context.is_offline_mode():
        return
    dialect = op.get_bind().dialect.name
    if dialect == "postgresql":
        op.execute("""
            CREATE OR REPLACE FUNCTION public.prevent_guide_article_revision_mutation()
            RETURNS trigger AS $$
            BEGIN
                IF TG_OP = 'UPDATE'
                   AND OLD.created_by_user_id IS NOT NULL
                   AND NEW.created_by_user_id IS NULL
                   AND (to_jsonb(NEW) - 'created_by_user_id') =
                       (to_jsonb(OLD) - 'created_by_user_id')
                THEN
                    RETURN NEW;
                END IF;
                RAISE EXCEPTION 'guide_article_revisions is append-only';
            END;
            $$ LANGUAGE plpgsql
        """)
        op.execute(
            "DROP TRIGGER IF EXISTS guide_article_revisions_append_only ON guide_article_revisions"
        )
        op.execute("""
            CREATE TRIGGER guide_article_revisions_append_only
            BEFORE UPDATE OR DELETE ON guide_article_revisions
            FOR EACH ROW EXECUTE FUNCTION public.prevent_guide_article_revision_mutation()
        """)
    elif dialect == "sqlite":
        op.execute("""
            CREATE TRIGGER IF NOT EXISTS guide_article_revisions_no_delete
            BEFORE DELETE ON guide_article_revisions
            BEGIN SELECT RAISE(ABORT, 'guide_article_revisions is append-only'); END
        """)
        op.execute("""
            CREATE TRIGGER IF NOT EXISTS guide_article_revisions_no_update
            BEFORE UPDATE ON guide_article_revisions
            WHEN NOT (
                OLD.created_by_user_id IS NOT NULL AND NEW.created_by_user_id IS NULL
                AND NEW.id IS OLD.id AND NEW.article_locale_id IS OLD.article_locale_id
                AND NEW.version IS OLD.version AND NEW.action IS OLD.action
                AND NEW.document_json IS OLD.document_json AND NEW.created_at IS OLD.created_at
            )
            BEGIN SELECT RAISE(ABORT, 'guide_article_revisions is append-only'); END
        """)


def downgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    for table in (
        "guide_article_topics",
        "guide_article_revisions",
        "guide_article_locales",
        "guide_articles",
        "guide_topics",
    ):
        if inspector is None or inspector.has_table(table):
            op.drop_table(table)
    if not context.is_offline_mode() and op.get_bind().dialect.name == "postgresql":
        op.execute("DROP FUNCTION IF EXISTS public.prevent_guide_article_revision_mutation()")
