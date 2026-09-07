"""Public community tables; compatible with fresh metadata-based installs."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0057_community"
down_revision: str | None = "0056_travel_services"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    offline = context.is_offline_mode()
    names = set() if offline else set(sa.inspect(op.get_bind()).get_table_names())
    columns = (
        set() if offline else {c["name"] for c in sa.inspect(op.get_bind()).get_columns("users")}
    )
    if "email_verified_at" not in columns:
        op.add_column(
            "users", sa.Column("email_verified_at", sa.DateTime(timezone=True), nullable=True)
        )
    if "deleted_at" not in columns:
        op.add_column("users", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    if "community_translation_budgets" not in names:
        op.create_table(
            "community_translation_budgets",
            sa.Column("month", sa.String(length=7), nullable=False),
            sa.Column("characters", sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint("month"),
        )
    if "community_translations" not in names:
        op.create_table(
            "community_translations",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("source_hash", sa.String(length=64), nullable=False),
            sa.Column("locale", sa.String(length=16), nullable=False),
            sa.Column("body", sa.Text(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("source_hash", "locale", name="uq_community_translation"),
        )
    if "community_account_tokens" not in names:
        op.create_table(
            "community_account_tokens",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("user_id", sa.Uuid(), nullable=False),
            sa.Column("digest", sa.String(length=64), nullable=False),
            sa.Column("purpose", sa.String(length=16), nullable=False),
            sa.Column("auth_version", sa.Integer(), nullable=False),
            sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("digest"),
        )
        op.create_index(
            op.f("ix_community_account_tokens_user_id"),
            "community_account_tokens",
            ["user_id"],
            unique=False,
        )
    if "community_collections" not in names:
        op.create_table(
            "community_collections",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("user_id", sa.Uuid(), nullable=False),
            sa.Column("name", sa.String(length=80), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            op.f("ix_community_collections_user_id"),
            "community_collections",
            ["user_id"],
            unique=False,
        )
    if "community_conversations" not in names:
        op.create_table(
            "community_conversations",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("first_user_id", sa.Uuid(), nullable=False),
            sa.Column("second_user_id", sa.Uuid(), nullable=False),
            sa.Column("first_read_id", sa.Integer(), nullable=False),
            sa.Column("second_read_id", sa.Integer(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "first_user_id <> second_user_id", name="ck_community_conversation_pair"
            ),
            sa.ForeignKeyConstraint(
                ["first_user_id"],
                ["users.id"],
            ),
            sa.ForeignKeyConstraint(
                ["second_user_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint(
                "first_user_id", "second_user_id", name="uq_community_conversation"
            ),
        )
        op.create_index(
            op.f("ix_community_conversations_first_user_id"),
            "community_conversations",
            ["first_user_id"],
            unique=False,
        )
        op.create_index(
            op.f("ix_community_conversations_second_user_id"),
            "community_conversations",
            ["second_user_id"],
            unique=False,
        )
    if "community_events" not in names:
        op.create_table(
            "community_events",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("recipient_id", sa.Uuid(), nullable=False),
            sa.Column("kind", sa.String(length=24), nullable=False),
            sa.Column("target", sa.String(length=120), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["recipient_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            op.f("ix_community_events_recipient_id"),
            "community_events",
            ["recipient_id"],
            unique=False,
        )
    if "community_jobs" not in names:
        op.create_table(
            "community_jobs",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("kind", sa.String(length=24), nullable=False),
            sa.Column("user_id", sa.Uuid(), nullable=False),
            sa.Column("payload_encrypted", sa.Text(), nullable=True),
            sa.Column("status", sa.String(length=16), nullable=False),
            sa.Column("attempts", sa.Integer(), nullable=False),
            sa.Column("available_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_community_jobs_kind"), "community_jobs", ["kind"], unique=False)
        op.create_index(
            op.f("ix_community_jobs_status"), "community_jobs", ["status"], unique=False
        )
        op.create_index(
            op.f("ix_community_jobs_user_id"), "community_jobs", ["user_id"], unique=False
        )
    if "community_media" not in names:
        op.create_table(
            "community_media",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("owner_id", sa.Uuid(), nullable=False),
            sa.Column("object_key", sa.String(length=200), nullable=False),
            sa.Column("thumbnail_key", sa.String(length=200), nullable=False),
            sa.Column("content_type", sa.String(length=32), nullable=False),
            sa.Column("width", sa.Integer(), nullable=False),
            sa.Column("height", sa.Integer(), nullable=False),
            sa.Column("size", sa.Integer(), nullable=False),
            sa.Column("alt", sa.String(length=300), nullable=False),
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["owner_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("object_key"),
            sa.UniqueConstraint("thumbnail_key"),
        )
        op.create_index(
            op.f("ix_community_media_owner_id"), "community_media", ["owner_id"], unique=False
        )
    if "community_metrics" not in names:
        op.create_table(
            "community_metrics",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("day", sa.String(length=10), nullable=False),
            sa.Column("user_id", sa.Uuid(), nullable=False),
            sa.Column("kind", sa.String(length=24), nullable=False),
            sa.Column("target", sa.String(length=120), nullable=False),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("day", "user_id", "kind", "target", name="uq_community_metric"),
        )
        op.create_index(
            op.f("ix_community_metrics_day"), "community_metrics", ["day"], unique=False
        )
        op.create_index(
            op.f("ix_community_metrics_user_id"), "community_metrics", ["user_id"], unique=False
        )
    if "community_notifications" not in names:
        op.create_table(
            "community_notifications",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("recipient_id", sa.Uuid(), nullable=False),
            sa.Column("actor_id", sa.Uuid(), nullable=True),
            sa.Column("kind", sa.String(length=24), nullable=False),
            sa.Column("target", sa.String(length=120), nullable=False),
            sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["actor_id"],
                ["users.id"],
            ),
            sa.ForeignKeyConstraint(
                ["recipient_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            op.f("ix_community_notifications_recipient_id"),
            "community_notifications",
            ["recipient_id"],
            unique=False,
        )
    if "community_posts" not in names:
        op.create_table(
            "community_posts",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("author_id", sa.Uuid(), nullable=False),
            sa.Column("state", sa.String(length=16), nullable=False),
            sa.Column("draft_revision_id", sa.Uuid(), nullable=True),
            sa.Column("published_revision_id", sa.Uuid(), nullable=True),
            sa.Column("pending_revision_id", sa.Uuid(), nullable=True),
            sa.Column("version", sa.Integer(), nullable=False),
            sa.Column("approved_once", sa.Boolean(), nullable=False),
            sa.Column("featured", sa.Boolean(), nullable=False),
            sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "state IN ('draft','pending','published','hidden','deleted')",
                name="ck_community_post_state",
            ),
            sa.ForeignKeyConstraint(
                ["author_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            "ix_community_post_feed",
            "community_posts",
            ["state", "published_at", "id"],
            unique=False,
        )
        op.create_index(
            op.f("ix_community_posts_author_id"), "community_posts", ["author_id"], unique=False
        )
    if "community_profiles" not in names:
        op.create_table(
            "community_profiles",
            sa.Column("user_id", sa.Uuid(), nullable=False),
            sa.Column("handle", sa.String(length=30), nullable=False),
            sa.Column("display_name", sa.String(length=80), nullable=False),
            sa.Column("bio", sa.String(length=1000), nullable=False),
            sa.Column("languages", sa.JSON(), nullable=False),
            sa.Column("destinations", sa.JSON(), nullable=False),
            sa.Column("avatar_id", sa.Uuid(), nullable=True),
            sa.Column("approved_posts", sa.Integer(), nullable=False),
            sa.Column("restricted", sa.Boolean(), nullable=False),
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("notification_preferences", sa.JSON(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("user_id"),
            sa.UniqueConstraint("handle"),
        )
    if "community_relationships" not in names:
        op.create_table(
            "community_relationships",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("actor_id", sa.Uuid(), nullable=False),
            sa.Column("target_id", sa.Uuid(), nullable=False),
            sa.Column("kind", sa.String(length=12), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint("kind IN ('follow','block')", name="ck_community_relationship_kind"),
            sa.CheckConstraint("actor_id <> target_id", name="ck_community_relationship_not_self"),
            sa.ForeignKeyConstraint(
                ["actor_id"],
                ["users.id"],
            ),
            sa.ForeignKeyConstraint(
                ["target_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("actor_id", "target_id", "kind", name="uq_community_relationship"),
        )
        op.create_index(
            op.f("ix_community_relationships_actor_id"),
            "community_relationships",
            ["actor_id"],
            unique=False,
        )
        op.create_index(
            op.f("ix_community_relationships_target_id"),
            "community_relationships",
            ["target_id"],
            unique=False,
        )
    if "community_reports" not in names:
        op.create_table(
            "community_reports",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("reporter_id", sa.Uuid(), nullable=False),
            sa.Column("kind", sa.String(length=20), nullable=False),
            sa.Column("target", sa.String(length=120), nullable=False),
            sa.Column("reason", sa.String(length=2000), nullable=False),
            sa.Column("evidence", sa.JSON(), nullable=False),
            sa.Column("status", sa.String(length=16), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["reporter_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            op.f("ix_community_reports_reporter_id"),
            "community_reports",
            ["reporter_id"],
            unique=False,
        )
        op.create_index(
            op.f("ix_community_reports_status"), "community_reports", ["status"], unique=False
        )
    if "community_collection_items" not in names:
        op.create_table(
            "community_collection_items",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("collection_id", sa.Uuid(), nullable=False),
            sa.Column("kind", sa.String(length=20), nullable=False),
            sa.Column("target", sa.String(length=160), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["collection_id"],
                ["community_collections.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint(
                "collection_id", "kind", "target", name="uq_community_collection_item"
            ),
        )
        op.create_index(
            op.f("ix_community_collection_items_collection_id"),
            "community_collection_items",
            ["collection_id"],
            unique=False,
        )
    if "community_comments" not in names:
        op.create_table(
            "community_comments",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("post_id", sa.Uuid(), nullable=False),
            sa.Column("author_id", sa.Uuid(), nullable=False),
            sa.Column("parent_id", sa.Uuid(), nullable=True),
            sa.Column("body", sa.Text(), nullable=False),
            sa.Column("locale", sa.String(length=16), nullable=False),
            sa.Column("hidden", sa.Boolean(), nullable=False),
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["author_id"],
                ["users.id"],
            ),
            sa.ForeignKeyConstraint(
                ["parent_id"],
                ["community_comments.id"],
            ),
            sa.ForeignKeyConstraint(
                ["post_id"],
                ["community_posts.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            op.f("ix_community_comments_author_id"),
            "community_comments",
            ["author_id"],
            unique=False,
        )
        op.create_index(
            op.f("ix_community_comments_post_id"), "community_comments", ["post_id"], unique=False
        )
    if "community_messages" not in names:
        op.create_table(
            "community_messages",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("conversation_id", sa.Uuid(), nullable=False),
            sa.Column("sender_id", sa.Uuid(), nullable=False),
            sa.Column("body", sa.Text(), nullable=False),
            sa.Column("card_post_id", sa.Uuid(), nullable=True),
            sa.Column("idempotency_key", sa.String(length=100), nullable=False),
            sa.Column("request_hash", sa.String(length=64), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["card_post_id"],
                ["community_posts.id"],
            ),
            sa.ForeignKeyConstraint(
                ["conversation_id"],
                ["community_conversations.id"],
            ),
            sa.ForeignKeyConstraint(
                ["sender_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("sender_id", "idempotency_key", name="uq_community_message_replay"),
        )
        op.create_index(
            "ix_community_message_thread",
            "community_messages",
            ["conversation_id", "id"],
            unique=False,
        )
    if "community_post_revisions" not in names:
        op.create_table(
            "community_post_revisions",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("post_id", sa.Uuid(), nullable=False),
            sa.Column("title", sa.String(length=160), nullable=False),
            sa.Column("body", sa.Text(), nullable=False),
            sa.Column("locale", sa.String(length=16), nullable=False),
            sa.Column("destination", sa.String(length=160), nullable=False),
            sa.Column("kind", sa.String(length=24), nullable=False),
            sa.Column("topics", sa.JSON(), nullable=False),
            sa.Column("place_ids", sa.JSON(), nullable=False),
            sa.Column("media_ids", sa.JSON(), nullable=False),
            sa.Column("itinerary", sa.JSON(), nullable=True),
            sa.Column("allow_fork", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["post_id"],
                ["community_posts.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            op.f("ix_community_post_revisions_destination"),
            "community_post_revisions",
            ["destination"],
            unique=False,
        )
        op.create_index(
            op.f("ix_community_post_revisions_locale"),
            "community_post_revisions",
            ["locale"],
            unique=False,
        )
        op.create_index(
            op.f("ix_community_post_revisions_post_id"),
            "community_post_revisions",
            ["post_id"],
            unique=False,
        )
    if "community_reactions" not in names:
        op.create_table(
            "community_reactions",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("user_id", sa.Uuid(), nullable=False),
            sa.Column("post_id", sa.Uuid(), nullable=False),
            sa.Column("kind", sa.String(length=12), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint("kind IN ('like','save')", name="ck_community_reaction_kind"),
            sa.ForeignKeyConstraint(
                ["post_id"],
                ["community_posts.id"],
            ),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("user_id", "post_id", "kind", name="uq_community_reaction"),
        )
        op.create_index(
            op.f("ix_community_reactions_post_id"), "community_reactions", ["post_id"], unique=False
        )
        op.create_index(
            op.f("ix_community_reactions_user_id"), "community_reactions", ["user_id"], unique=False
        )
    if "community_forks" not in names:
        op.create_table(
            "community_forks",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("user_id", sa.Uuid(), nullable=False),
            sa.Column("post_id", sa.Uuid(), nullable=False),
            sa.Column("revision_id", sa.Uuid(), nullable=False),
            sa.Column("trip_id", sa.Uuid(), nullable=False),
            sa.Column("idempotency_key", sa.String(length=100), nullable=False),
            sa.Column("request_hash", sa.String(length=64), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["post_id"],
                ["community_posts.id"],
            ),
            sa.ForeignKeyConstraint(
                ["revision_id"],
                ["community_post_revisions.id"],
            ),
            sa.ForeignKeyConstraint(
                ["trip_id"],
                ["trip_plans.id"],
            ),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("user_id", "idempotency_key", name="uq_community_fork"),
        )
        op.create_index(
            op.f("ix_community_forks_post_id"), "community_forks", ["post_id"], unique=False
        )
        op.create_index(
            op.f("ix_community_forks_user_id"), "community_forks", ["user_id"], unique=False
        )


def downgrade() -> None:
    op.drop_table("community_forks")
    op.drop_table("community_reactions")
    op.drop_table("community_post_revisions")
    op.drop_table("community_messages")
    op.drop_table("community_comments")
    op.drop_table("community_collection_items")
    op.drop_table("community_reports")
    op.drop_table("community_relationships")
    op.drop_table("community_profiles")
    op.drop_table("community_posts")
    op.drop_table("community_notifications")
    op.drop_table("community_metrics")
    op.drop_table("community_media")
    op.drop_table("community_jobs")
    op.drop_table("community_events")
    op.drop_table("community_conversations")
    op.drop_table("community_collections")
    op.drop_table("community_account_tokens")
    op.drop_table("community_translations")
    op.drop_table("community_translation_budgets")
    op.drop_column("users", "deleted_at")
    op.drop_column("users", "email_verified_at")
