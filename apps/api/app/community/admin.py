from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, Response
from sqlalchemy import String, and_, cast, func, literal, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AdminUser, CurrentUser
from app.community.accounts import smtp_ready
from app.community.content import check_version, published_post, serialize_post
from app.community.invitations import lock_creator, require_creator_invitation, serialize_invitation
from app.community.messaging import conversation_for
from app.community.models import (
    Comment,
    CommunityMetric,
    CreatorInvitation,
    Job,
    Message,
    Post,
    PostRevision,
    Profile,
    Report,
    TranslationBudget,
)
from app.community.policy import (
    audit,
    aware,
    fail,
    member,
    notify,
    public_profile,
    rate,
    settings_for,
    signal,
    visible_profile,
)
from app.community.router import OpenSession, Session
from app.community.schemas import (
    CreatorInvitationInput,
    ModerationInput,
    ReportInput,
    ResolveReportInput,
    RestrictionInput,
    ReviewCommentInput,
    SettingsUpdate,
)
from app.config import get_settings
from app.models import AdminAuditLog, ProviderConfig, User

router = APIRouter(prefix="/admin/community", tags=["community administration"])
report_router = APIRouter(prefix="/community", tags=["community reports"])


@router.get("/creator-invitations")
async def creator_invitations(
    admin: AdminUser, session: Session, response: Response, user_id: UUID | None = None
) -> dict[str, Any]:
    response.headers["Cache-Control"] = "private, no-store"
    if user_id is not None:
        user = await session.get(User, user_id)
        if user is None or not user.is_active or user.deleted_at:
            raise fail("community_not_found", 404)
        row = await session.get(CreatorInvitation, user_id)
        return {"items": [serialize_invitation(user_id, row)]}
    rows = (
        await session.scalars(
            select(CreatorInvitation)
            .join(User, User.id == CreatorInvitation.user_id)
            .where(User.is_active.is_(True), User.deleted_at.is_(None))
            .order_by(CreatorInvitation.updated_at.desc(), CreatorInvitation.user_id)
            .limit(100)
        )
    ).all()
    return {"items": [serialize_invitation(row.user_id, row) for row in rows]}


@router.put("/creator-invitations/{user_id}")
async def set_creator_invitation(
    user_id: UUID,
    payload: CreatorInvitationInput,
    admin: AdminUser,
    session: Session,
    response: Response,
) -> dict[str, Any]:
    response.headers["Cache-Control"] = "private, no-store"
    await lock_creator(session, user_id)
    row = await session.scalar(
        select(CreatorInvitation)
        .where(CreatorInvitation.user_id == user_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if payload.version != (row.version if row else 0):
        raise fail("community_version_conflict", 409)
    before = serialize_invitation(user_id, row)
    if row is None:
        row = CreatorInvitation(user_id=user_id, invited=payload.invited, version=1)
        session.add(row)
    else:
        row.invited = payload.invited
        row.version += 1
    row.granted_by_user_id = admin.id
    await session.flush()
    audit(
        session,
        admin,
        "community_creator_invitation",
        str(user_id),
        before=before["invited"],
        after=row.invited,
        version=row.version,
        reason=payload.reason,
    )
    await session.commit()
    return serialize_invitation(user_id, row)


@report_router.get("/me/reviews")
async def my_review_results(user: CurrentUser, session: OpenSession) -> dict[str, Any]:
    from app.community.pet_models import PetReport

    await member(session, user)
    # Restrict in SQL to targets owned by this member. Never expose another
    # reporter's evidence, the moderator's identity, or general admin logs.
    targets = (
        select(func.replace(cast(Post.id, String), "-", ""))
        .where(Post.author_id == user.id)
        .union(
            select(func.replace(cast(Comment.id, String), "-", "")).where(
                Comment.author_id == user.id
            ),
            select(func.replace(cast(Report.id, String), "-", "")).where(
                Report.reporter_id == user.id
            ),
            select(func.replace(cast(PetReport.id, String), "-", "")).where(
                PetReport.reporter_id == user.id
            ),
            select(literal(user.id.hex)),
        )
    )
    logs = (
        await session.scalars(
            select(AdminAuditLog)
            .where(
                or_(AdminAuditLog.action.like("community_%"), AdminAuditLog.action.like("pet_%")),
                func.replace(AdminAuditLog.target, "-", "").in_(targets),
            )
            .order_by(AdminAuditLog.created_at.desc())
            .limit(50)
        )
    ).all()
    pet_reports = (
        await session.scalars(
            select(PetReport)
            .where(
                PetReport.reporter_id == user.id,
            )
            .order_by(PetReport.updated_at.desc())
            .limit(50)
        )
    ).all()
    return {
        "items": [
            {
                "id": str(row.id),
                "action": row.action,
                "reason": row.metadata_json.get("reason", ""),
                "created_at": row.created_at,
            }
            for row in logs
        ],
        "pet_reports": [
            {
                "id": str(row.id),
                "place_id": str(row.place_id),
                "status": row.status,
                "body": row.body,
            }
            for row in pet_reports
        ],
    }


@router.get("/media/{identifier}")
async def review_media(
    identifier: UUID, admin: AdminUser, session: Session, response: Response
) -> dict[str, Any]:
    from app.community.media import media_url

    response.headers["Cache-Control"] = "private, no-store"
    return await media_url(session, identifier, admin, review=True)


@router.get("/settings")
async def get_settings_page(
    admin: AdminUser, session: Session, response: Response
) -> dict[str, Any]:
    response.headers["Cache-Control"] = "private, no-store"
    settings = await settings_for(session)
    row = await session.scalar(select(ProviderConfig).where(ProviderConfig.provider == "community"))
    environment = get_settings()
    return {
        "settings": settings.model_dump(),
        "sources": {
            key: "database"
            if row and key in row.config
            else "environment"
            if key == "enabled"
            else "default"
            for key in type(settings).model_fields
        },
        "services": {
            "mail_configured": smtp_ready(),
            "storage_configured": bool(
                environment.community_s3_access_key and environment.community_s3_secret_key
            ),
        },
    }


@router.put("/settings")
async def update_settings(
    payload: SettingsUpdate, admin: AdminUser, session: Session
) -> dict[str, Any]:
    # Serialize first-time creation as well as updates without relying on Redis.
    if session.get_bind().dialect.name == "postgresql":
        await session.execute(text("SELECT pg_advisory_xact_lock(6842061908)"))
    row = await session.scalar(
        select(ProviderConfig).where(ProviderConfig.provider == "community").with_for_update()
    )
    before = (await settings_for(session)).model_dump()
    after = payload.settings.model_dump()
    if row is None:
        row = ProviderConfig(provider="community", config=after, updated_by_user_id=admin.id)
        session.add(row)
    else:
        row.config = after
        row.updated_by_user_id = admin.id
    changes = {
        key: {"before": before[key], "after": value}
        for key, value in after.items()
        if before[key] != value
    }
    if changes:
        audit(
            session,
            admin,
            "community_settings_updated",
            "community",
            reason=payload.reason,
            changes=changes,
        )
    await session.commit()
    return {"settings": after}


@router.get("/posts")
async def review_posts(
    admin: AdminUser, session: Session, state: Literal["pending", "published", "hidden"] = "pending"
) -> dict[str, Any]:
    query = select(Post).where(Post.state != "deleted")
    query = (
        query.where(Post.pending_revision_id.is_not(None))
        if state == "pending"
        else query.where(Post.state == state)
    )
    rows = (await session.scalars(query.order_by(Post.updated_at, Post.id).limit(100))).all()
    items = []
    for post in rows:
        revision_id = post.pending_revision_id if state == "pending" else post.published_revision_id
        revision = await session.get(PostRevision, revision_id) if revision_id else None
        profile = await session.get(Profile, post.author_id)
        if revision and profile and not profile.deleted_at:
            items.append(await serialize_post(session, post, revision, profile, owner=True))
    return {"items": items}


@router.put("/posts/{identifier}")
async def moderate_post(
    identifier: UUID, payload: ModerationInput, admin: AdminUser, session: Session
) -> dict[str, Any]:
    post = await session.get(Post, identifier)
    if post is None or post.state == "deleted":
        raise fail("community_not_found", 404)
    if payload.action in {"approve", "restore"}:
        await require_creator_invitation(session, post.author_id)
    profile = await session.scalar(
        select(Profile).where(Profile.user_id == post.author_id).with_for_update()
    )
    post = await session.scalar(
        select(Post)
        .where(Post.id == identifier)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if post is None or post.state == "deleted":
        raise fail("community_not_found", 404)
    check_version(post, payload.version)
    if profile is None or profile.deleted_at is not None:
        raise fail("community_not_found", 404)
    before = {
        "state": post.state,
        "revision_id": str(post.published_revision_id),
        "featured": post.featured,
    }
    action = payload.action
    if action in {"approve", "return"}:
        if post.pending_revision_id is None:
            raise fail("community_version_conflict", 409)
        revision = await session.get(PostRevision, post.pending_revision_id)
        if revision is None or revision.post_id != post.id:
            raise fail("community_version_conflict", 409)
        if action == "approve":
            if profile.restricted:
                raise fail("community_restricted", 403)
            if post.published_revision_id != revision.id:
                from app.analytics.service import record_event

                await record_event(
                    session,
                    "post_published",
                    path="/community",
                    user_id=admin.id,
                    properties={"kind": revision.kind, "publication_source": "moderator"},
                )
            post.published_revision_id = revision.id
            post.state = "published"
            post.published_at = post.published_at or datetime.now(UTC)
            if not post.approved_once:
                profile.approved_posts += 1
                post.approved_once = True
        elif post.published_revision_id is None:
            post.state = "draft"
        post.pending_revision_id = None
    elif action == "hide":
        post.state = "hidden"
        post.pending_revision_id = None
        post.featured = False
    elif action == "restore":
        if post.state != "hidden" or post.published_revision_id is None or profile.restricted:
            raise fail("community_version_conflict", 409)
        post.state = "published"
    else:
        if post.state != "published":
            raise fail("community_version_conflict", 409)
        post.featured = action == "feature"
    post.version += 1
    after = {
        "state": post.state,
        "revision_id": str(post.published_revision_id),
        "featured": post.featured,
    }
    audit(
        session,
        admin,
        f"community_post_{action}",
        str(post.id),
        reason=payload.reason,
        before=before,
        after=after,
    )
    await notify(session, post.author_id, None, "review", str(post.id))
    await session.commit()
    await signal(post.author_id)
    return {"state": post.state, "version": post.version}


@router.get("/comments")
async def review_comments(
    admin: AdminUser, session: Session, hidden: bool = True
) -> dict[str, Any]:
    rows = (
        await session.scalars(
            select(Comment)
            .where(Comment.hidden == hidden, Comment.deleted_at.is_(None))
            .order_by(Comment.created_at)
            .limit(100)
        )
    ).all()
    return {
        "items": [
            {
                "id": str(row.id),
                "post_id": str(row.post_id),
                "author_id": str(row.author_id),
                "body": row.body,
                "locale": row.locale,
                "hidden": row.hidden,
            }
            for row in rows
        ]
    }


@router.put("/comments/{identifier}")
async def moderate_comment(
    identifier: UUID, payload: ReviewCommentInput, admin: AdminUser, session: Session
) -> dict[str, bool]:
    row = await session.get(Comment, identifier, with_for_update=True)
    if row is None or row.deleted_at:
        raise fail("community_not_found", 404)
    before = row.hidden
    row.hidden = payload.hidden
    audit(
        session,
        admin,
        "community_comment_reviewed",
        str(row.id),
        reason=payload.reason,
        before={"hidden": before},
        after={"hidden": row.hidden},
    )
    await notify(session, row.author_id, None, "review", str(row.post_id))
    await session.commit()
    return {"hidden": row.hidden}


@router.get("/profiles")
async def review_profiles(admin: AdminUser, session: Session, q: str = "") -> dict[str, Any]:
    if len(q) > 80:
        raise fail("validation_error", 422)
    from app.db import escape_like

    query = select(Profile).where(Profile.deleted_at.is_(None))
    if q:
        query = query.where(
            or_(
                Profile.handle.ilike(f"%{escape_like(q)}%", escape="\\"),
                Profile.display_name.ilike(f"%{escape_like(q)}%", escape="\\"),
            )
        )
    rows = (await session.scalars(query.order_by(Profile.created_at.desc()).limit(100))).all()
    return {
        "items": [
            {
                **public_profile(row),
                "restricted": row.restricted,
                "approved_posts": row.approved_posts,
            }
            for row in rows
        ]
    }


@router.put("/profiles/{identifier}/restriction")
async def restrict_profile(
    identifier: UUID, payload: RestrictionInput, admin: AdminUser, session: Session
) -> dict[str, bool]:
    row = await session.get(Profile, identifier, with_for_update=True)
    if row is None or row.deleted_at:
        raise fail("community_not_found", 404)
    if identifier == admin.id:
        raise fail("admin_self_action", 403)
    before = row.restricted
    row.restricted = payload.restricted
    audit(
        session,
        admin,
        "community_member_restricted",
        str(identifier),
        reason=payload.reason,
        before={"restricted": before},
        after={"restricted": row.restricted},
    )
    await session.commit()
    await signal(identifier)
    return {"restricted": row.restricted}


@report_router.post("/reports", status_code=201)
async def report(payload: ReportInput, user: CurrentUser, session: OpenSession) -> dict[str, str]:
    await member(session, user)
    await rate(session, user)
    evidence: dict[str, Any] = {}
    try:
        identifier = UUID(payload.target)
    except ValueError as exc:
        raise fail("validation_error", 422) from exc
    if payload.kind == "post":
        _, revision, _ = await published_post(session, identifier, user)
        evidence = {
            "revision_id": str(revision.id),
            "title": revision.title,
            "body": revision.body,
            "media_ids": revision.media_ids,
            "locale": revision.locale,
            "destination": revision.destination,
        }
    elif payload.kind == "profile":
        await visible_profile(session, identifier, user)
    elif payload.kind == "comment":
        comment = await session.get(Comment, identifier)
        if comment is None or comment.hidden or comment.deleted_at:
            raise fail("community_not_found", 404)
        await published_post(session, comment.post_id, user)
        await visible_profile(session, comment.author_id, user)
        evidence = {
            "body": comment.body,
            "author_id": str(comment.author_id),
            "post_id": str(comment.post_id),
        }
    else:
        await conversation_for(session, identifier, user)
        ids = set(payload.message_ids)
        if not ids:
            raise fail("validation_error", 422)
        rows = (
            await session.scalars(
                select(Message)
                .where(Message.conversation_id == identifier, Message.id.in_(ids))
                .order_by(Message.id)
            )
        ).all()
        if len(rows) != len(ids):
            raise fail("community_not_found", 404)
        # No unrestricted inbox endpoint. Only explicitly selected messages are frozen.
        evidence = {
            "messages": [
                {
                    "id": row.id,
                    "sender_id": str(row.sender_id),
                    "body": row.body,
                    "card_post_id": str(row.card_post_id) if row.card_post_id else None,
                    "created_at": aware(row.created_at).isoformat(),
                }
                for row in rows
            ]
        }
    row = Report(
        reporter_id=user.id,
        kind=payload.kind,
        target=payload.target,
        reason=payload.reason,
        evidence=evidence,
    )
    session.add(row)
    await session.commit()
    return {"id": str(row.id)}


@router.get("/reports")
async def reports(
    admin: AdminUser,
    session: Session,
    status: Literal["pending", "resolved", "dismissed"] = "pending",
) -> dict[str, Any]:
    rows = (
        await session.scalars(
            select(Report).where(Report.status == status).order_by(Report.created_at).limit(100)
        )
    ).all()
    return {
        "items": [
            {
                "id": str(row.id),
                "kind": row.kind,
                "target": row.target,
                "reason": row.reason,
                "evidence": row.evidence,
                "status": row.status,
                "created_at": row.created_at,
            }
            for row in rows
        ]
    }


@router.put("/reports/{identifier}")
async def resolve_report(
    identifier: UUID, payload: ResolveReportInput, admin: AdminUser, session: Session
) -> dict[str, str]:
    row = await session.get(Report, identifier, with_for_update=True)
    if row is None:
        raise fail("community_not_found", 404)
    before = row.status
    row.status = payload.status
    audit(
        session,
        admin,
        "community_report_resolved",
        str(row.id),
        reason=payload.reason,
        before={"status": before},
        after={"status": row.status},
    )
    await notify(session, row.reporter_id, None, "review", str(row.id))
    await session.commit()
    return {"status": row.status}


async def conversion_funnel(session: AsyncSession, since: datetime) -> dict[str, int]:
    # Each stage must follow the previous one for the SAME member and source
    # post. Independent activity totals are not a conversion funnel. Only
    # authenticated member activity is recorded; anonymous readers are not inferred.
    metric = CommunityMetric
    stage = (
        select(metric.user_id, metric.target, func.min(metric.created_at).label("occurred_at"))
        .where(metric.kind == "read", metric.created_at >= since)
        .group_by(metric.user_id, metric.target)
        .cte("funnel_read")
    )
    stages = {"read": stage}
    for kind in ("save", "fork", "trip_created"):
        stage = (
            select(metric.user_id, metric.target, func.min(metric.created_at).label("occurred_at"))
            .join(
                stage,
                and_(
                    metric.user_id == stage.c.user_id,
                    metric.target == stage.c.target,
                    metric.created_at >= stage.c.occurred_at,
                ),
            )
            .where(metric.kind == kind)
            .group_by(metric.user_id, metric.target)
            .cte(f"funnel_{kind}")
        )
        stages[kind] = stage
    counts = (
        (
            await session.execute(
                select(
                    *[
                        select(func.count(func.distinct(stage.c.user_id)))
                        .scalar_subquery()
                        .label(kind)
                        for kind, stage in stages.items()
                    ]
                )
            )
        )
        .mappings()
        .one()
    )
    return {kind: int(counts[kind]) for kind in stages}


@router.get("/overview")
async def overview(admin: AdminUser, session: Session, response: Response) -> dict[str, Any]:
    response.headers["Cache-Control"] = "private, no-store"
    since = datetime.now(UTC) - timedelta(days=30)
    metrics = (
        await session.execute(
            select(CommunityMetric.kind, func.count(func.distinct(CommunityMetric.user_id)))
            .where(CommunityMetric.day >= since.date().isoformat())
            .group_by(CommunityMetric.kind)
        )
    ).all()
    active_authors = await session.scalar(
        select(func.count(func.distinct(Post.author_id))).where(
            Post.state == "published", Post.published_at >= since
        )
    )
    returning = (
        select(CommunityMetric.user_id)
        .where(CommunityMetric.day >= since.date().isoformat())
        .group_by(CommunityMetric.user_id)
        .having(func.count(func.distinct(CommunityMetric.day)) > 1)
        .subquery()
    )
    returning_users = await session.scalar(select(func.count()).select_from(returning))
    pending = (
        await session.scalars(select(Post).where(Post.pending_revision_id.is_not(None)))
    ).all()
    budget = await session.get(TranslationBudget, datetime.now(UTC).strftime("%Y-%m"))
    jobs = (
        await session.execute(
            select(Job.kind, Job.status, func.count()).group_by(Job.kind, Job.status)
        )
    ).all()
    logs = (
        await session.scalars(
            select(AdminAuditLog)
            .where(
                or_(AdminAuditLog.action.like("community_%"), AdminAuditLog.action.like("pet_%"))
            )
            .order_by(AdminAuditLog.created_at.desc())
            .limit(50)
        )
    ).all()
    return {
        "conversion_funnel_30d": await conversion_funnel(session, since),
        "unique_users_30d": {kind: count for kind, count in metrics},
        "active_authors_30d": active_authors or 0,
        "returning_users_30d": returning_users or 0,
        "pending_posts": len(pending),
        "oldest_review_seconds": max(
            (int((datetime.now(UTC) - aware(row.updated_at)).total_seconds()) for row in pending),
            default=0,
        ),
        "translation_characters_this_month": budget.characters if budget else 0,
        "jobs": [{"kind": kind, "status": status, "count": count} for kind, status, count in jobs],
        "audit_logs": [
            {
                "id": str(row.id),
                "actor_id": str(row.actor_user_id),
                "action": row.action,
                "target": row.target,
                "metadata": row.metadata_json,
                "created_at": row.created_at,
            }
            for row in logs
        ],
    }
