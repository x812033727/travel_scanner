from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


class Timestamped:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow,
    )


class Profile(Timestamped, Base):
    __tablename__ = "community_profiles"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    handle: Mapped[str] = mapped_column(String(30), unique=True)
    display_name: Mapped[str] = mapped_column(String(80))
    bio: Mapped[str] = mapped_column(String(1000), default="")
    languages: Mapped[list[str]] = mapped_column(JSON, default=list)
    destinations: Mapped[list[str]] = mapped_column(JSON, default=list)
    avatar_id: Mapped[UUID | None] = mapped_column(nullable=True)
    approved_posts: Mapped[int] = mapped_column(default=0)
    restricted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notification_preferences: Mapped[dict[str, bool]] = mapped_column(JSON, default=dict)


class CreatorInvitation(Timestamped, Base):
    __tablename__ = "community_creator_invitations"
    __table_args__ = (CheckConstraint("version >= 1", name="ck_creator_invitation_version"),)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    invited: Mapped[bool] = mapped_column(Boolean, default=False)
    version: Mapped[int] = mapped_column(default=1)
    granted_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class Post(Timestamped, Base):
    __tablename__ = "community_posts"
    __table_args__ = (
        CheckConstraint(
            "state IN ('draft','pending','published','hidden','deleted')",
            name="ck_community_post_state",
        ),
        Index("ix_community_post_feed", "state", "published_at", "id"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    state: Mapped[str] = mapped_column(String(16), default="draft")
    # Revision identifiers have no FK cycle. Each use also checks the owning post.
    draft_revision_id: Mapped[UUID | None] = mapped_column(nullable=True)
    published_revision_id: Mapped[UUID | None] = mapped_column(nullable=True)
    pending_revision_id: Mapped[UUID | None] = mapped_column(nullable=True)
    version: Mapped[int] = mapped_column(default=1)
    approved_once: Mapped[bool] = mapped_column(Boolean, default=False)
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class PostRevision(Base):
    __tablename__ = "community_post_revisions"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    post_id: Mapped[UUID] = mapped_column(ForeignKey("community_posts.id"), index=True)
    title: Mapped[str] = mapped_column(String(160))
    body: Mapped[str] = mapped_column(Text)
    locale: Mapped[str] = mapped_column(String(16), index=True)
    destination: Mapped[str] = mapped_column(String(160), index=True)
    kind: Mapped[str] = mapped_column(String(24))
    topics: Mapped[list[str]] = mapped_column(JSON, default=list)
    place_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    place_refs: Mapped[list[dict[str, str]]] = mapped_column(
        JSON, default=list, server_default="[]"
    )
    media_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    video_refs: Mapped[list[dict[str, str]]] = mapped_column(
        JSON, default=list, server_default="[]"
    )
    # This is an allowlisted snapshot, never a dump of TripPlan.data.
    itinerary: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    allow_fork: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Media(Timestamped, Base):
    __tablename__ = "community_media"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    object_key: Mapped[str] = mapped_column(String(200), unique=True)
    thumbnail_key: Mapped[str] = mapped_column(String(200), unique=True)
    content_type: Mapped[str] = mapped_column(String(32), default="image/webp")
    width: Mapped[int] = mapped_column()
    height: Mapped[int] = mapped_column()
    size: Mapped[int] = mapped_column()
    alt: Mapped[str] = mapped_column(String(300), default="")
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Relationship(Base):
    __tablename__ = "community_relationships"
    __table_args__ = (
        UniqueConstraint("actor_id", "target_id", "kind", name="uq_community_relationship"),
        CheckConstraint("kind IN ('follow','block')", name="ck_community_relationship_kind"),
        CheckConstraint("actor_id <> target_id", name="ck_community_relationship_not_self"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    actor_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    target_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    kind: Mapped[str] = mapped_column(String(12))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Reaction(Base):
    __tablename__ = "community_reactions"
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", "kind", name="uq_community_reaction"),
        CheckConstraint("kind IN ('like','save')", name="ck_community_reaction_kind"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    post_id: Mapped[UUID] = mapped_column(ForeignKey("community_posts.id"), index=True)
    kind: Mapped[str] = mapped_column(String(12))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Collection(Timestamped, Base):
    __tablename__ = "community_collections"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(80))


class CollectionItem(Base):
    __tablename__ = "community_collection_items"
    __table_args__ = (
        UniqueConstraint("collection_id", "kind", "target", name="uq_community_collection_item"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    collection_id: Mapped[UUID] = mapped_column(ForeignKey("community_collections.id"), index=True)
    kind: Mapped[str] = mapped_column(String(20))
    target: Mapped[str] = mapped_column(String(160))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Comment(Timestamped, Base):
    __tablename__ = "community_comments"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    post_id: Mapped[UUID] = mapped_column(ForeignKey("community_posts.id"), index=True)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    parent_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("community_comments.id"), nullable=True
    )
    body: Mapped[str] = mapped_column(Text)
    locale: Mapped[str] = mapped_column(String(16))
    hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Fork(Base):
    __tablename__ = "community_forks"
    __table_args__ = (UniqueConstraint("user_id", "idempotency_key", name="uq_community_fork"),)
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    post_id: Mapped[UUID] = mapped_column(ForeignKey("community_posts.id"), index=True)
    revision_id: Mapped[UUID] = mapped_column(ForeignKey("community_post_revisions.id"))
    trip_id: Mapped[UUID] = mapped_column(ForeignKey("trip_plans.id"))
    idempotency_key: Mapped[str] = mapped_column(String(100))
    request_hash: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Conversation(Timestamped, Base):
    __tablename__ = "community_conversations"
    __table_args__ = (
        UniqueConstraint("first_user_id", "second_user_id", name="uq_community_conversation"),
        CheckConstraint("first_user_id <> second_user_id", name="ck_community_conversation_pair"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    first_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    second_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    first_read_id: Mapped[int] = mapped_column(default=0)
    second_read_id: Mapped[int] = mapped_column(default=0)


class Message(Base):
    __tablename__ = "community_messages"
    __table_args__ = (
        UniqueConstraint("sender_id", "idempotency_key", name="uq_community_message_replay"),
        Index("ix_community_message_thread", "conversation_id", "id"),
    )
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    conversation_id: Mapped[UUID] = mapped_column(ForeignKey("community_conversations.id"))
    sender_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    body: Mapped[str] = mapped_column(Text)
    card_post_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("community_posts.id"), nullable=True
    )
    idempotency_key: Mapped[str] = mapped_column(String(100))
    request_hash: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Notification(Base):
    __tablename__ = "community_notifications"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    recipient_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    actor_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    kind: Mapped[str] = mapped_column(String(24))
    target: Mapped[str] = mapped_column(String(120))
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Event(Base):
    __tablename__ = "community_events"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    recipient_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    kind: Mapped[str] = mapped_column(String(24))
    target: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Translation(Timestamped, Base):
    __tablename__ = "community_translations"
    __table_args__ = (UniqueConstraint("source_hash", "locale", name="uq_community_translation"),)
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    source_hash: Mapped[str] = mapped_column(String(64))
    locale: Mapped[str] = mapped_column(String(16))
    body: Mapped[str] = mapped_column(Text)


class TranslationBudget(Base):
    __tablename__ = "community_translation_budgets"
    month: Mapped[str] = mapped_column(String(7), primary_key=True)
    characters: Mapped[int] = mapped_column(default=0)


class Report(Timestamped, Base):
    __tablename__ = "community_reports"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    reporter_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    kind: Mapped[str] = mapped_column(String(20))
    target: Mapped[str] = mapped_column(String(120))
    reason: Mapped[str] = mapped_column(String(2000))
    # Only messages explicitly selected by the reporting conversation participant.
    evidence: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(16), default="pending", index=True)


class AccountToken(Base):
    __tablename__ = "community_account_tokens"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    digest: Mapped[str] = mapped_column(String(64), unique=True)
    purpose: Mapped[str] = mapped_column(String(16))
    auth_version: Mapped[int] = mapped_column()
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    consumed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Job(Timestamped, Base):
    __tablename__ = "community_jobs"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    kind: Mapped[str] = mapped_column(String(24), index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    payload_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(16), default="pending", index=True)
    attempts: Mapped[int] = mapped_column(default=0)
    available_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class CommunityMetric(Base):
    __tablename__ = "community_metrics"
    __table_args__ = (
        UniqueConstraint("day", "user_id", "kind", "target", name="uq_community_metric"),
        Index("ix_community_metrics_funnel", "kind", "created_at", "user_id", "target"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    day: Mapped[str] = mapped_column(String(10), index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    kind: Mapped[str] = mapped_column(String(24))
    target: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
