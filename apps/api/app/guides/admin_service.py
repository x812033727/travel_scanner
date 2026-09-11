"""Authoring travel intel and guide articles: draft, version, publish, withdraw, restore.

Every write goes through ``_write_revision``: one conditional UPDATE on the version the
caller last read, one appended revision, one audit row, one commit. That is the shape
``app.site_pages.service`` already uses, and it is what makes a lost update a 409 the
editor can recover from rather than a silently overwritten draft.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, cast
from uuid import UUID, uuid4

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.schemas import AdminAuditView
from app.destinations.catalog import destination_for_id
from app.guides.models import (
    GuideArticle,
    GuideArticleLocale,
    GuideArticleRevision,
    GuideArticleTopic,
    GuideTopic,
)
from app.guides.publication import article_is_live, today
from app.guides.schemas import (
    ArticleCreate,
    ArticleDetail,
    ArticleList,
    ArticleSummary,
    ArticleUpdate,
    DraftWrite,
    GuideDocument,
    Kind,
    LocaleState,
    PublishWrite,
    RestoreWrite,
    RevisionAction,
    RevisionDetail,
    RevisionSummary,
)
from app.guides.service import (
    MAX_PAGE,
    _locale_rows,
    _published_document,
    _target,
    _topics_for,
    destination_label,
    document_hash,
)
from app.guides.taxonomy import topic_option
from app.i18n import Locale
from app.models import AdminAuditLog, User
from app.problems import AppError

AUDIT_ACTIONS = (
    "guide_article_created",
    "guide_article_updated",
    "guide_article_draft_saved",
    "guide_article_published",
    "guide_article_unpublished",
    "guide_article_restored",
)


async def _resolve_topics(session: AsyncSession, slugs: list[str]) -> list[GuideTopic]:
    wanted = list(dict.fromkeys(slug.strip().casefold() for slug in slugs if slug.strip()))
    if not wanted:
        return []
    rows = list(
        await session.scalars(
            select(GuideTopic).where(GuideTopic.slug.in_(wanted), GuideTopic.is_active.is_(True))
        )
    )
    found = {row.slug for row in rows}
    missing = [slug for slug in wanted if slug not in found]
    if missing:
        raise AppError(422, "guide_topic_unknown", f"找不到主題：{', '.join(missing)}")
    order = {slug: index for index, slug in enumerate(wanted)}
    return sorted(rows, key=lambda row: order[row.slug])


async def _set_topics(
    session: AsyncSession, article: GuideArticle, topics: list[GuideTopic]
) -> None:
    await session.execute(
        delete(GuideArticleTopic).where(GuideArticleTopic.article_id == article.id)
    )
    for topic in topics:
        session.add(GuideArticleTopic(article_id=article.id, topic_id=topic.id))


async def _find_article(session: AsyncSession, article_id: UUID) -> GuideArticle:
    article = await session.scalar(
        select(GuideArticle)
        .where(GuideArticle.id == article_id)
        .execution_options(populate_existing=True)
    )
    if article is None:
        raise AppError(404, "guide_article_not_found", "找不到這篇文章")
    return article


async def _find_locale_row(
    session: AsyncSession, article: GuideArticle, locale: Locale
) -> GuideArticleLocale | None:
    row: GuideArticleLocale | None = await session.scalar(
        select(GuideArticleLocale)
        .where(
            GuideArticleLocale.article_id == article.id,
            GuideArticleLocale.locale == locale,
        )
        .execution_options(populate_existing=True)
    )
    return row


async def _require_locale_row(
    session: AsyncSession, article: GuideArticle, locale: Locale
) -> GuideArticleLocale:
    row = await _find_locale_row(session, article, locale)
    if row is None:
        raise AppError(404, "guide_locale_not_found", "這篇文章還沒有這個語言的草稿")
    return row


def _document_title(row: GuideArticleLocale) -> str:
    value = (row.draft_json or {}).get("title")
    return value if isinstance(value, str) else ""


def _locale_state(row: GuideArticleLocale) -> LocaleState:
    return LocaleState(
        locale=cast(Locale, row.locale),
        version=row.version,
        published_version=row.published_version,
        published_at=row.published_at,
        title=_document_title(row),
        updated_at=row.updated_at,
    )


def _summary(
    article: GuideArticle,
    rows: list[GuideArticleLocale],
    topics: list[GuideTopic],
    locale: Locale,
) -> ArticleSummary:
    return ArticleSummary(
        id=article.id,
        slug=article.slug,
        kind=cast(Kind, article.kind),
        destination_id=article.destination_id,
        destination_label=destination_label(article.destination_id, locale),
        topics=[topic_option(topic, locale) for topic in topics],
        valid_until=article.valid_until,
        expired=article.valid_until is not None and article.valid_until < today(),
        featured=article.featured,
        display_order=article.display_order,
        is_active=article.is_active,
        version=article.version,
        locales=[_locale_state(row) for row in rows],
        updated_at=article.updated_at,
    )


def _validate_destination(destination_id: str | None) -> str | None:
    if destination_id is None or not destination_id.strip():
        return None
    normalized = destination_id.strip().casefold()
    if destination_for_id(normalized) is None:
        raise AppError(422, "guide_destination_unknown", "找不到這個目的地代碼")
    return normalized


# --- the single mutation path -------------------------------------------------


async def _write_revision(
    session: AsyncSession,
    actor: User,
    article: GuideArticle,
    row: GuideArticleLocale,
    expected_version: int,
    document: GuideDocument,
    action: RevisionAction,
    *,
    reason: str | None = None,
    source_revision_id: UUID | None = None,
) -> ArticleDetail:
    new_version = expected_version + 1
    encoded = document.model_dump(mode="json")
    now = datetime.now(UTC)
    before = dict(row.draft_json)
    previous_published = row.published_version
    revision_id = uuid4()
    try:
        values: dict[str, Any] = {
            "version": new_version,
            "draft_json": encoded,
            "updated_at": now,
        }
        if action == "published":
            values["published_version"] = new_version
            # First publication stamps the date readers and the sitemap sort by; a later
            # republication is an update to the same article, not a new one.
            values["published_at"] = row.published_at or now
        elif action == "unpublished":
            values["published_version"] = None
        changed = await session.scalar(
            update(GuideArticleLocale)
            .where(
                GuideArticleLocale.id == row.id,
                GuideArticleLocale.version == expected_version,
            )
            .values(**values)
            .returning(GuideArticleLocale.id)
            .execution_options(synchronize_session=False)
        )
        if changed is None:
            raise AppError(409, "guide_version_conflict", "這篇文章已被更新，請重新載入後再操作")
        session.add(
            GuideArticleRevision(
                id=revision_id,
                article_locale_id=row.id,
                version=new_version,
                action=action,
                document_json=encoded,
                created_by_user_id=actor.id,
                created_at=now,
            )
        )
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action=f"guide_article_{action}",
                target=_target(article.id, row.locale),
                metadata_json={
                    "article_id": str(article.id),
                    "revision_id": str(revision_id),
                    "before_version": expected_version,
                    "version": new_version,
                    "before": before,
                    "after": encoded,
                    "previous_published_version": previous_published,
                    "published_version": (
                        new_version
                        if action == "published"
                        else None
                        if action == "unpublished"
                        else previous_published
                    ),
                    "reason": reason,
                    "document_sha256": document_hash(encoded),
                    "source_revision_id": str(source_revision_id) if source_revision_id else None,
                    "operator_confirmed": action in {"published", "unpublished"},
                },
            )
        )
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    return await article_detail(session, article.id, cast(Locale, row.locale))


# --- admin operations ---------------------------------------------------------


async def create_article(
    session: AsyncSession, actor: User, payload: ArticleCreate
) -> ArticleDetail:
    destination_id = _validate_destination(payload.destination_id)
    topics = await _resolve_topics(session, payload.topics)
    now = datetime.now(UTC)
    encoded = payload.document.model_dump(mode="json")
    # The id is assigned here, not left to the column default: ``row`` needs it now, and a
    # column default is only applied at INSERT time, so ``article.id`` would still be None.
    article = GuideArticle(
        id=uuid4(),
        slug=payload.slug,
        kind=payload.kind,
        destination_id=destination_id,
        valid_until=payload.valid_until,
        created_at=now,
        updated_at=now,
    )
    row = GuideArticleLocale(
        id=uuid4(),
        article_id=article.id,
        locale=payload.locale,
        version=1,
        draft_json=encoded,
        created_at=now,
        updated_at=now,
    )
    try:
        session.add(article)
        session.add(row)
        await session.flush()
        await _set_topics(session, article, topics)
        session.add(
            GuideArticleRevision(
                article_locale_id=row.id,
                version=1,
                action="created",
                document_json=encoded,
                created_by_user_id=actor.id,
                created_at=now,
            )
        )
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action="guide_article_created",
                target=_target(article.id, payload.locale),
                metadata_json={
                    "article_id": str(article.id),
                    "kind": payload.kind,
                    "destination_id": destination_id,
                    "topics": [topic.slug for topic in topics],
                    "after": encoded,
                    "document_sha256": document_hash(encoded),
                },
            )
        )
        await session.commit()
    except IntegrityError as error:
        await session.rollback()
        if "slug" not in str(error.orig).lower():
            # Reporting every constraint failure as a taken slug would send an editor
            # hunting for a duplicate that does not exist. Let the real error surface.
            raise
        raise AppError(409, "guide_slug_taken", "這個網址代稱已經有人用了") from error
    except Exception:
        await session.rollback()
        raise
    return await article_detail(session, article.id, payload.locale)


async def update_article(
    session: AsyncSession, actor: User, article_id: UUID, payload: ArticleUpdate, locale: Locale
) -> ArticleDetail:
    article = await _find_article(session, article_id)
    destination_id = _validate_destination(payload.destination_id)
    topics = await _resolve_topics(session, payload.topics)
    before = {
        "kind": article.kind,
        "destination_id": article.destination_id,
        "valid_until": article.valid_until.isoformat() if article.valid_until else None,
        "featured": article.featured,
        "display_order": article.display_order,
        "is_active": article.is_active,
    }
    try:
        changed = await session.scalar(
            update(GuideArticle)
            .where(
                GuideArticle.id == article.id,
                GuideArticle.version == payload.expected_version,
            )
            .values(
                kind=payload.kind,
                destination_id=destination_id,
                valid_until=payload.valid_until,
                featured=payload.featured,
                display_order=payload.display_order,
                is_active=payload.is_active,
                version=payload.expected_version + 1,
                updated_at=datetime.now(UTC),
            )
            .returning(GuideArticle.id)
            .execution_options(synchronize_session=False)
        )
        if changed is None:
            raise AppError(409, "guide_version_conflict", "這篇文章已被更新，請重新載入後再操作")
        await _set_topics(session, article, topics)
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action="guide_article_updated",
                target=_target(article.id),
                metadata_json={
                    "article_id": str(article.id),
                    "before_version": payload.expected_version,
                    "version": payload.expected_version + 1,
                    "before": before,
                    "after": {
                        "kind": payload.kind,
                        "destination_id": destination_id,
                        "valid_until": (
                            payload.valid_until.isoformat() if payload.valid_until else None
                        ),
                        "featured": payload.featured,
                        "display_order": payload.display_order,
                        "is_active": payload.is_active,
                    },
                    "topics": [topic.slug for topic in topics],
                },
            )
        )
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    return await article_detail(session, article.id, locale)


async def start_translation(
    session: AsyncSession, actor: User, article_id: UUID, locale: Locale, document: GuideDocument
) -> ArticleDetail:
    """Open a new language on an existing article. Never copies another locale's text."""
    article = await _find_article(session, article_id)
    if await _find_locale_row(session, article, locale) is not None:
        raise AppError(409, "guide_locale_exists", "這個語言的草稿已經存在")
    now = datetime.now(UTC)
    encoded = document.model_dump(mode="json")
    row = GuideArticleLocale(
        id=uuid4(),
        article_id=article.id,
        locale=locale,
        version=1,
        draft_json=encoded,
        created_at=now,
        updated_at=now,
    )
    try:
        session.add(row)
        await session.flush()
        session.add(
            GuideArticleRevision(
                article_locale_id=row.id,
                version=1,
                action="created",
                document_json=encoded,
                created_by_user_id=actor.id,
                created_at=now,
            )
        )
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action="guide_article_created",
                target=_target(article.id, locale),
                metadata_json={
                    "article_id": str(article.id),
                    "after": encoded,
                    "document_sha256": document_hash(encoded),
                },
            )
        )
        await session.commit()
    except IntegrityError as error:
        await session.rollback()
        raise AppError(409, "guide_locale_exists", "這個語言的草稿已經存在") from error
    except Exception:
        await session.rollback()
        raise
    return await article_detail(session, article.id, locale)


async def save_draft(
    session: AsyncSession, actor: User, article_id: UUID, locale: Locale, payload: DraftWrite
) -> ArticleDetail:
    article = await _find_article(session, article_id)
    row = await _require_locale_row(session, article, locale)
    return await _write_revision(
        session, actor, article, row, payload.expected_version, payload.document, "draft_saved"
    )


async def publish_locale(
    session: AsyncSession, actor: User, article_id: UUID, locale: Locale, payload: PublishWrite
) -> ArticleDetail:
    article = await _find_article(session, article_id)
    row = await _require_locale_row(session, article, locale)
    if not article.is_active:
        raise AppError(409, "guide_article_inactive", "這篇文章已下架，請先重新啟用")
    # Publishing something already past its own validity would put a URL in the sitemap
    # that the list will not show. Refuse rather than publish an invisible page.
    if not article_is_live(article):
        raise AppError(409, "guide_article_expired", "這篇文章的有效期限已過，請先更新期限")
    document = GuideDocument.model_validate(row.draft_json)
    return await _write_revision(
        session,
        actor,
        article,
        row,
        payload.expected_version,
        document,
        "published",
        reason=payload.reason,
    )


async def unpublish_locale(
    session: AsyncSession, actor: User, article_id: UUID, locale: Locale, payload: PublishWrite
) -> ArticleDetail:
    article = await _find_article(session, article_id)
    row = await _require_locale_row(session, article, locale)
    if row.published_version is None:
        raise AppError(409, "guide_not_published", "這個語言目前並未公開")
    document = GuideDocument.model_validate(row.draft_json)
    return await _write_revision(
        session,
        actor,
        article,
        row,
        payload.expected_version,
        document,
        "unpublished",
        reason=payload.reason,
    )


async def restore_revision(
    session: AsyncSession, actor: User, article_id: UUID, locale: Locale, payload: RestoreWrite
) -> ArticleDetail:
    article = await _find_article(session, article_id)
    row = await _require_locale_row(session, article, locale)
    revision = await session.scalar(
        select(GuideArticleRevision).where(
            GuideArticleRevision.id == payload.revision_id,
            GuideArticleRevision.article_locale_id == row.id,
        )
    )
    if revision is None:
        raise AppError(404, "guide_revision_not_found", "找不到這篇文章的指定版本")
    # Restoring writes a new draft. It never moves the public pointer, so a restore cannot
    # publish old text by accident.
    return await _write_revision(
        session,
        actor,
        article,
        row,
        payload.expected_version,
        GuideDocument.model_validate(revision.document_json),
        "restored",
        reason=payload.reason,
        source_revision_id=revision.id,
    )


def _revision_view(revision: GuideArticleRevision) -> RevisionDetail:
    return RevisionDetail(
        id=revision.id,
        version=revision.version,
        action=cast(RevisionAction, revision.action),
        created_at=revision.created_at,
        created_by_user_id=revision.created_by_user_id,
        document=GuideDocument.model_validate(revision.document_json),
    )


async def get_revision(
    session: AsyncSession, article_id: UUID, locale: Locale, revision_id: UUID
) -> RevisionDetail:
    article = await _find_article(session, article_id)
    row = await _require_locale_row(session, article, locale)
    revision = await session.scalar(
        select(GuideArticleRevision).where(
            GuideArticleRevision.id == revision_id,
            GuideArticleRevision.article_locale_id == row.id,
        )
    )
    if revision is None:
        raise AppError(404, "guide_revision_not_found", "找不到這篇文章的指定版本")
    return _revision_view(revision)


async def article_detail(session: AsyncSession, article_id: UUID, locale: Locale) -> ArticleDetail:
    article = await _find_article(session, article_id)
    rows = (await _locale_rows(session, [article.id])).get(article.id, [])
    topics = (await _topics_for(session, [article.id])).get(article.id, [])
    row = next((item for item in rows if item.locale == locale), None)
    if row is None:
        raise AppError(404, "guide_locale_not_found", "這篇文章還沒有這個語言的草稿")
    revisions = await session.scalars(
        select(GuideArticleRevision)
        .where(GuideArticleRevision.article_locale_id == row.id)
        .order_by(GuideArticleRevision.version.desc())
        .limit(100)
    )
    audit = await session.scalars(
        select(AdminAuditLog)
        .where(
            AdminAuditLog.target.in_([_target(article.id), _target(article.id, locale)]),
            AdminAuditLog.action.in_(AUDIT_ACTIONS),
        )
        .order_by(AdminAuditLog.created_at.desc())
        .limit(20)
    )
    return ArticleDetail(
        **_summary(article, rows, topics, locale).model_dump(),
        locale=locale,
        draft=GuideDocument.model_validate(row.draft_json),
        published=await _published_document(session, row),
        revisions=[
            RevisionSummary(**_revision_view(item).model_dump(exclude={"document"}))
            for item in revisions
        ],
        audit=[
            AdminAuditView(
                id=item.id,
                actor_user_id=item.actor_user_id,
                action=item.action,
                target=item.target,
                metadata=item.metadata_json,
                created_at=item.created_at,
            )
            for item in audit
        ],
    )


async def list_articles(
    session: AsyncSession,
    locale: Locale,
    *,
    kind: Kind | None = None,
    destination: str | None = None,
    topic: str | None = None,
    limit: int = MAX_PAGE,
) -> ArticleList:
    query = select(GuideArticle)
    if kind is not None:
        query = query.where(GuideArticle.kind == kind)
    if destination:
        query = query.where(GuideArticle.destination_id == destination.casefold())
    if topic:
        query = query.where(
            GuideArticle.id.in_(
                select(GuideArticleTopic.article_id)
                .join(GuideTopic, GuideTopic.id == GuideArticleTopic.topic_id)
                .where(GuideTopic.slug == topic.casefold())
            )
        )
    rows = list(
        await session.scalars(
            query.order_by(
                GuideArticle.featured.desc(),
                GuideArticle.display_order,
                GuideArticle.updated_at.desc(),
            ).limit(min(max(limit, 1), MAX_PAGE))
        )
    )
    ids = [row.id for row in rows]
    locales = await _locale_rows(session, ids)
    topics = await _topics_for(session, ids)
    return ArticleList(
        articles=[
            _summary(row, locales.get(row.id, []), topics.get(row.id, []), locale) for row in rows
        ]
    )
