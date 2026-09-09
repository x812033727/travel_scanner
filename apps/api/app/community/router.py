from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy import and_, delete, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser, OptionalCurrentUser
from app.community.content import (
    check_version,
    fork_post,
    new_revision,
    owned_post,
    published_post,
    serialize_post,
)
from app.community.invitations import (
    creator_invited,
    invitation_required,
    require_creator_invitation,
)
from app.community.media import check_media, complete_upload, create_upload, media_url
from app.community.models import Comment, Post, PostRevision, Profile, Reaction, Relationship
from app.community.policy import (
    cursor_decode,
    cursor_encode,
    event,
    fail,
    member,
    metric,
    notify,
    public_profile,
    rate,
    require_open,
    risky,
    settings_for,
    signal,
    visible_profile,
)
from app.community.schemas import (
    CommentInput,
    ForkInput,
    NotificationPreferences,
    PostInput,
    ProfileInput,
    UploadInput,
    VersionInput,
)
from app.db import get_session
from app.models import User

router = APIRouter(prefix="/community", tags=["community"])
Session = Annotated[AsyncSession, Depends(get_session)]


async def open_session(session: Session, response: Response) -> AsyncSession:
    response.headers["Cache-Control"] = "private, no-store"
    await require_open(session)
    return session


OpenSession = Annotated[AsyncSession, Depends(open_session)]


@router.get("/status")
async def status(session: Session, response: Response) -> dict[str, Any]:
    response.headers["Cache-Control"] = "no-store"
    settings = await settings_for(session)
    return {
        key: value
        for key, value in settings.model_dump().items()
        if key
        in {
            "enabled",
            "posting_enabled",
            "comments_enabled",
            "messaging_enabled",
            "translation_enabled",
            "pet_reports_enabled",
        }
    }


@router.get("/me")
async def me(user: CurrentUser, session: OpenSession) -> dict[str, Any]:
    profile = await session.get(Profile, user.id)
    required = invitation_required()
    invited = await creator_invited(session, user.id) if required else False
    settings = await settings_for(session)
    return {
        "profile": public_profile(profile) if profile and not profile.deleted_at else None,
        "verified": user.email_verified_at is not None,
        "restricted": bool(profile and profile.restricted),
        "notification_preferences": profile.notification_preferences if profile else {},
        "creator_invited": invited,
        "invitation_required": required,
        "can_publish": bool(
            settings.posting_enabled
            and user.email_verified_at
            and profile
            and not profile.restricted
            and not profile.deleted_at
            and (not required or invited)
        ),
    }


@router.put("/me")
async def save_profile(
    payload: ProfileInput, user: CurrentUser, session: OpenSession
) -> dict[str, Any]:
    await rate(session, user)
    await session.scalar(select(User).where(User.id == user.id).with_for_update())
    await check_media(session, user, [payload.avatar_id] if payload.avatar_id else [])
    profile = await session.get(Profile, user.id)
    if profile and (profile.restricted or profile.deleted_at):
        raise fail("community_restricted", 403)
    if profile and profile.handle != payload.handle:
        raise fail("community_handle_immutable", 422)
    if not profile:
        profile = Profile(user_id=user.id, **payload.model_dump())
        session.add(profile)
    else:
        for key, value in payload.model_dump().items():
            setattr(profile, key, value)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise fail("community_handle_taken", 409) from exc
    return public_profile(profile)


@router.put("/me/notification-preferences")
async def preferences(
    payload: NotificationPreferences,
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, bool]:
    profile = await member(session, user)
    profile.notification_preferences = payload.model_dump()
    await session.commit()
    return profile.notification_preferences


@router.get("/profiles/{handle}")
async def profile_page(
    handle: str, viewer: OptionalCurrentUser, session: OpenSession
) -> dict[str, Any]:
    profile = await session.scalar(select(Profile).where(Profile.handle == handle))
    if profile is None:
        raise fail("community_not_found", 404)
    await visible_profile(session, profile.user_id, viewer)
    followers = await session.scalar(
        select(func.count())
        .select_from(Relationship)
        .where(
            Relationship.target_id == profile.user_id,
            Relationship.kind == "follow",
        )
    )
    following = False
    mutual = False
    if viewer:
        following = (
            await session.scalar(
                select(Relationship.id).where(
                    Relationship.actor_id == viewer.id,
                    Relationship.target_id == profile.user_id,
                    Relationship.kind == "follow",
                )
            )
            is not None
        )
        mutual = (
            following
            and await session.scalar(
                select(Relationship.id).where(
                    Relationship.actor_id == profile.user_id,
                    Relationship.target_id == viewer.id,
                    Relationship.kind == "follow",
                )
            )
            is not None
        )
    return {
        **public_profile(profile),
        "followers": followers or 0,
        "following": following,
        "can_message": mutual and profile.user_id != (viewer.id if viewer else None),
    }


@router.put("/profiles/{identifier}/{kind}")
async def set_relationship(
    identifier: UUID,
    kind: Literal["follow", "block"],
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, bool]:
    await session.execute(
        select(Profile)
        .where(Profile.user_id.in_([user.id, identifier]))
        .order_by(Profile.user_id)
        .with_for_update()
    )
    await member(session, user, verified=True)
    await rate(session, user)
    if identifier == user.id:
        raise fail("community_self_action", 422)
    await visible_profile(session, identifier, user if kind == "follow" else None)
    row = await session.scalar(
        select(Relationship).where(
            Relationship.actor_id == user.id,
            Relationship.target_id == identifier,
            Relationship.kind == kind,
        )
    )
    if row is None:
        session.add(Relationship(actor_id=user.id, target_id=identifier, kind=kind))
        if kind == "follow":
            await notify(session, identifier, user.id, "follow", str(user.id))
    if kind == "block":
        await session.execute(
            delete(Relationship).where(
                Relationship.kind == "follow",
                or_(
                    and_(Relationship.actor_id == user.id, Relationship.target_id == identifier),
                    and_(Relationship.actor_id == identifier, Relationship.target_id == user.id),
                ),
            )
        )
    await event(session, identifier, "relationship", str(user.id))
    await session.commit()
    await signal(identifier)
    return {"active": True}


@router.delete("/profiles/{identifier}/{kind}")
async def remove_relationship(
    identifier: UUID,
    kind: Literal["follow", "block"],
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, bool]:
    await session.execute(
        select(Profile)
        .where(Profile.user_id.in_([user.id, identifier]))
        .order_by(Profile.user_id)
        .with_for_update()
    )
    await member(session, user)
    await session.execute(
        delete(Relationship).where(
            Relationship.actor_id == user.id,
            Relationship.target_id == identifier,
            Relationship.kind == kind,
        )
    )
    await event(session, identifier, "relationship", str(user.id))
    await session.commit()
    await signal(identifier)
    return {"active": False}


@router.get("/blocks")
async def blocks(user: CurrentUser, session: OpenSession) -> dict[str, Any]:
    profiles = (
        await session.scalars(
            select(Profile)
            .join(
                Relationship,
                Relationship.target_id == Profile.user_id,
            )
            .where(Relationship.actor_id == user.id, Relationship.kind == "block")
        )
    ).all()
    return {"items": [public_profile(profile) for profile in profiles]}


@router.post("/posts", status_code=201)
async def create_post(
    payload: PostInput, user: CurrentUser, session: OpenSession
) -> dict[str, Any]:
    await require_open(session, "posting_enabled")
    profile = await member(session, user, verified=True, lock=True)
    await rate(session, user)
    post = Post(author_id=user.id)
    session.add(post)
    await session.flush()
    revision = await new_revision(session, user, post, payload)
    post.draft_revision_id = revision.id
    await session.commit()
    return await serialize_post(session, post, revision, profile, user, owner=True)


@router.get("/drafts")
async def drafts(user: CurrentUser, session: OpenSession) -> dict[str, Any]:
    profile = await member(session, user)
    rows = (
        await session.execute(
            select(Post, PostRevision)
            .join(
                PostRevision,
                PostRevision.id == Post.draft_revision_id,
            )
            .where(Post.author_id == user.id, Post.state != "deleted")
            .order_by(Post.updated_at.desc())
            .limit(100)
        )
    ).all()
    return {
        "items": [
            await serialize_post(session, post, revision, profile, user, owner=True)
            for post, revision in rows
        ]
    }


@router.get("/posts/{identifier}/draft")
async def get_draft(identifier: UUID, user: CurrentUser, session: OpenSession) -> dict[str, Any]:
    profile = await member(session, user)
    post = await owned_post(session, user, identifier)
    revision = await session.get(PostRevision, post.draft_revision_id)
    if revision is None:
        raise fail("community_not_found", 404)
    return await serialize_post(session, post, revision, profile, user, owner=True)


@router.put("/posts/{identifier}")
async def edit_post(
    identifier: UUID,
    payload: PostInput,
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, Any]:
    await require_open(session, "posting_enabled")
    profile = await member(session, user, verified=True, lock=True)
    post = await owned_post(session, user, identifier)
    check_version(post, payload.version)
    await rate(session, user)
    revision = await new_revision(session, user, post, payload)
    post.draft_revision_id = revision.id
    post.pending_revision_id = None
    if post.state == "pending":
        post.state = "draft"
    post.version += 1
    await session.commit()
    return await serialize_post(session, post, revision, profile, user, owner=True)


@router.post("/posts/{identifier}/publish")
async def publish_post(
    identifier: UUID,
    payload: VersionInput,
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, Any]:
    settings = await require_open(session, "posting_enabled")
    await require_creator_invitation(session, user.id)
    profile = await member(session, user, verified=True, lock=True)
    post = await owned_post(session, user, identifier)
    check_version(post, payload.version)
    if post.state == "hidden":
        raise fail("community_restricted", 403)
    revision = await session.get(PostRevision, post.draft_revision_id)
    if revision is None or not revision.title or not revision.body or not revision.destination:
        raise fail("community_post_incomplete", 422)
    await rate(session, user, "publish")
    previous = (
        await session.get(PostRevision, post.published_revision_id)
        if post.published_revision_id
        else None
    )
    new_video = bool(revision.video_refs) and (
        previous is None or revision.video_refs != previous.video_refs
    )
    if (
        profile.approved_posts < 3
        or new_video
        or risky(revision.title + "\n" + revision.body, settings)
    ):
        post.pending_revision_id = revision.id
        if post.published_revision_id is None:
            post.state = "pending"
    else:
        post.published_revision_id = revision.id
        post.pending_revision_id = None
        post.state = "published"
        post.published_at = post.published_at or datetime.now(UTC)
        if previous is None or previous.id != revision.id:
            from app.analytics.service import record_event

            await record_event(
                session,
                "post_published",
                path="/community",
                user_id=user.id,
                properties={"kind": revision.kind, "publication_source": "author"},
            )
    post.version += 1
    await session.commit()
    return await serialize_post(session, post, revision, profile, user, owner=True)


@router.delete("/posts/{identifier}")
async def delete_post(identifier: UUID, user: CurrentUser, session: OpenSession) -> dict[str, bool]:
    await member(session, user, lock=True)
    post = await owned_post(session, user, identifier)
    post.state = "deleted"
    post.pending_revision_id = None
    post.version += 1
    await session.commit()
    return {"deleted": True}


@router.post("/posts/{identifier}/withdraw")
async def withdraw_post(
    identifier: UUID, user: CurrentUser, session: OpenSession
) -> dict[str, bool]:
    await member(session, user, lock=True)
    post = await owned_post(session, user, identifier)
    if post.state == "hidden":
        raise fail("community_restricted", 403)
    post.state = "draft"
    post.published_revision_id = None
    post.pending_revision_id = None
    post.version += 1
    await session.commit()
    return {"withdrawn": True}


@router.get("/posts/{identifier}")
async def get_post(
    identifier: UUID, viewer: OptionalCurrentUser, session: OpenSession
) -> dict[str, Any]:
    post, revision, profile = await published_post(session, identifier, viewer)
    if viewer and viewer.id != post.author_id:
        await metric(session, viewer.id, "read", str(post.id))
        await session.commit()
    return await serialize_post(session, post, revision, profile, viewer)


@router.post("/posts/{identifier}/fork", status_code=201)
async def fork(
    identifier: UUID,
    payload: ForkInput,
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, Any]:
    await rate(session, user)
    return await fork_post(session, user, identifier, payload)


@router.put("/posts/{identifier}/reactions/{kind}")
async def react(
    identifier: UUID,
    kind: Literal["like", "save"],
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, bool]:
    await member(session, user, lock=True)
    await rate(session, user)
    post, _, _ = await published_post(session, identifier, user)
    existing = await session.scalar(
        select(Reaction).where(
            Reaction.post_id == identifier,
            Reaction.user_id == user.id,
            Reaction.kind == kind,
        )
    )
    if existing is None:
        session.add(Reaction(post_id=identifier, user_id=user.id, kind=kind))
        if kind == "save" and user.id != post.author_id:
            await metric(session, user.id, "save", str(identifier))
        if kind == "like":
            await notify(session, post.author_id, user.id, "like", str(identifier))
    await session.commit()
    await signal(post.author_id)
    return {"active": True}


@router.delete("/posts/{identifier}/reactions/{kind}")
async def unreact(
    identifier: UUID,
    kind: Literal["like", "save"],
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, bool]:
    await member(session, user, lock=True)
    await session.execute(
        delete(Reaction).where(
            Reaction.post_id == identifier,
            Reaction.user_id == user.id,
            Reaction.kind == kind,
        )
    )
    await session.commit()
    return {"active": False}


@router.post("/posts/{identifier}/comments", status_code=201)
async def add_comment(
    identifier: UUID,
    payload: CommentInput,
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, Any]:
    import re

    settings = await require_open(session, "comments_enabled")
    profile = await member(session, user, verified=True)
    await rate(session, user)
    # A post serializes comment timestamps until commit, so cursors cannot skip
    # an earlier allocated comment that commits after a later comment.
    # Its ID is immutable: NO KEY UPDATE preserves that ordering while allowing
    # foreign-key inserts (such as forks) to acquire KEY SHARE without a cycle.
    await session.scalar(select(Post).where(Post.id == identifier).with_for_update(key_share=True))
    post, _, _ = await published_post(session, identifier, user)
    parent = None
    if payload.parent_id:
        parent = await session.get(Comment, payload.parent_id)
        if (
            parent is None
            or parent.post_id != identifier
            or parent.parent_id
            or parent.hidden
            or parent.deleted_at
        ):
            raise fail("community_reply_invalid", 422)
        await visible_profile(session, parent.author_id, user)
    row = Comment(
        post_id=identifier,
        author_id=user.id,
        body=payload.body,
        locale=payload.locale,
        parent_id=payload.parent_id,
        hidden=risky(payload.body, settings),
    )
    session.add(row)
    await session.flush()
    if not row.hidden:
        recipient = parent.author_id if parent else post.author_id
        await notify(session, recipient, user.id, "reply" if parent else "comment", str(post.id))
        handles = list(
            dict.fromkeys(re.findall(r"(?<!\w)@([a-z][a-z0-9_]{2,29})\b", payload.body))
        )[:10]
        for mentioned in (
            await session.scalars(select(Profile).where(Profile.handle.in_(handles)))
        ).all():
            if mentioned.user_id != recipient:
                await notify(session, mentioned.user_id, user.id, "mention", str(post.id))
    await session.commit()
    return {"id": str(row.id), "pending": row.hidden, "author": public_profile(profile)}


@router.get("/posts/{identifier}/comments")
async def comments(
    identifier: UUID,
    viewer: OptionalCurrentUser,
    session: OpenSession,
    cursor: str | None = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
) -> dict[str, Any]:
    await published_post(session, identifier, viewer)
    query = (
        select(Comment, Profile)
        .join(Profile, Profile.user_id == Comment.author_id)
        .join(
            User,
            User.id == Profile.user_id,
        )
        .where(
            Comment.post_id == identifier,
            Comment.hidden.is_(False),
            Comment.deleted_at.is_(None),
            Profile.restricted.is_(False),
            Profile.deleted_at.is_(None),
            User.is_active.is_(True),
        )
    )
    if viewer:
        query = query.where(
            Comment.author_id.not_in(
                select(Relationship.target_id)
                .where(Relationship.actor_id == viewer.id, Relationship.kind == "block")
                .union(
                    select(Relationship.actor_id).where(
                        Relationship.target_id == viewer.id, Relationship.kind == "block"
                    )
                )
            )
        )
    boundary = cursor_decode(cursor)
    if boundary:
        moment, identifier_boundary = boundary
        query = query.where(
            or_(
                Comment.created_at > moment,
                and_(Comment.created_at == moment, Comment.id > identifier_boundary),
            )
        )
    rows = (
        await session.execute(query.order_by(Comment.created_at, Comment.id).limit(limit + 1))
    ).all()
    selected = rows[:limit]
    return {
        "items": [
            {
                "id": str(row.id),
                "body": row.body,
                "locale": row.locale,
                "parent_id": str(row.parent_id) if row.parent_id else None,
                "created_at": row.created_at,
                "author": public_profile(profile),
            }
            for row, profile in selected
        ],
        "next_cursor": cursor_encode(selected[-1][0].created_at, selected[-1][0].id)
        if len(rows) > limit
        else None,
    }


@router.put("/comments/{identifier}")
async def edit_comment(
    identifier: UUID,
    payload: CommentInput,
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, bool]:
    settings = await require_open(session, "comments_enabled")
    await member(session, user, verified=True)
    await rate(session, user)
    row = await session.get(Comment, identifier)
    if row is None or row.author_id != user.id or row.deleted_at:
        raise fail("community_not_found", 404)
    if row.hidden:
        raise fail("community_restricted", 403)
    await published_post(session, row.post_id, user)
    if risky(payload.body, settings):
        raise fail("community_comment_review", 422)
    row.body, row.locale = payload.body, payload.locale
    await session.commit()
    return {"updated": True}


@router.delete("/comments/{identifier}")
async def remove_comment(
    identifier: UUID, user: CurrentUser, session: OpenSession
) -> dict[str, bool]:
    row = await session.get(Comment, identifier)
    if row is None or row.author_id != user.id:
        raise fail("community_not_found", 404)
    row.deleted_at = datetime.now(UTC)
    row.body = ""
    await session.commit()
    return {"deleted": True}


@router.post("/media/uploads", status_code=201)
async def upload(payload: UploadInput, user: CurrentUser, session: OpenSession) -> dict[str, Any]:
    await require_open(session, "posting_enabled")
    await member(session, user, verified=True)
    await rate(session, user, "upload")
    return await create_upload(session, user, payload)


@router.post("/media/{identifier}/complete")
async def complete(identifier: UUID, user: CurrentUser, session: OpenSession) -> dict[str, Any]:
    await require_open(session, "posting_enabled")
    await member(session, user, verified=True)
    return await complete_upload(session, user, identifier)


@router.get("/media/{identifier}")
async def image_access(
    identifier: UUID,
    viewer: OptionalCurrentUser,
    session: OpenSession,
    thumbnail: bool = False,
) -> dict[str, Any]:
    return await media_url(session, identifier, viewer, thumbnail=thumbnail)
