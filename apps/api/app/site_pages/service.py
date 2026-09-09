from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from importlib.resources import files
from typing import Any, cast
from uuid import UUID, uuid4

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.schemas import AdminAuditView
from app.i18n import LOCALES, Locale
from app.models import AdminAuditLog, SitePage, SitePageRevision, User
from app.problems import AppError
from app.site_pages.schemas import (
    PAGE_SLUGS,
    REQUIRED_FIELDS,
    DraftWrite,
    InitializationResult,
    PageDetail,
    PageDocument,
    PageList,
    PageSlug,
    PageSummary,
    PublicPage,
    PublishedDocument,
    PublishWrite,
    RestoreWrite,
    RevisionDetail,
    RevisionSummary,
)

AUDIT_ACTIONS = (
    "site_page_initialized",
    "site_page_draft_saved",
    "site_page_published",
    "site_page_restored",
)


def _target(slug: str, locale: str) -> str:
    return f"site-page:{slug}:{locale}"


def document_hash(document: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(document, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()


def initial_document(slug: PageSlug, locale: Locale) -> PageDocument:
    source = files("app.site_pages").joinpath("drafts", f"{locale}.json")
    payload = json.loads(source.read_text(encoding="utf-8"))
    return PageDocument.model_validate(payload[slug])


def pending_requirements(slug: str, document: PageDocument) -> list[str]:
    requirements = document.requirements.model_dump()
    pending: list[str] = [
        field for field in REQUIRED_FIELDS[slug] if not requirements[field].strip()
    ]
    # There is no scheduled publication in this module. A future date is not
    # silently treated as a timer or exposed as an already-effective policy.
    if document.effective_date is None or document.effective_date > datetime.now(UTC).date():
        pending.append("effective_date")
    return pending


async def _find_page(session: AsyncSession, slug: PageSlug, locale: Locale) -> SitePage | None:
    page: SitePage | None = await session.scalar(
        select(SitePage)
        .where(SitePage.slug == slug, SitePage.locale == locale)
        .execution_options(populate_existing=True)
    )
    return page


async def _require_page(session: AsyncSession, slug: PageSlug, locale: Locale) -> SitePage:
    page = await _find_page(session, slug, locale)
    if page is None:
        raise AppError(404, "site_page_not_found", "請先初始化網站資訊草稿")
    return page


def _summary(page: SitePage) -> PageSummary:
    return PageSummary(
        slug=cast(PageSlug, page.slug),
        locale=cast(Locale, page.locale),
        version=page.version,
        published_version=page.published_version,
        updated_at=page.updated_at,
        pending_requirements=pending_requirements(
            page.slug, PageDocument.model_validate(page.draft_json)
        ),
    )


async def list_pages(session: AsyncSession) -> PageList:
    rows = await session.scalars(select(SitePage).order_by(SitePage.slug, SitePage.locale))
    return PageList(pages=[_summary(row) for row in rows])


async def _published(session: AsyncSession, page: SitePage) -> PublishedDocument | None:
    if page.published_version is None:
        return None
    revision = await session.scalar(
        select(SitePageRevision).where(
            SitePageRevision.page_id == page.id,
            SitePageRevision.version == page.published_version,
            SitePageRevision.action == "published",
        )
    )
    if revision is None:
        # A damaged pointer must never turn the current draft into a public fallback.
        raise AppError(503, "site_page_unavailable", "暫時無法取得網站資訊，請稍後再試")
    document = PageDocument.model_validate(revision.document_json)
    return PublishedDocument(
        **document.model_dump(), version=revision.version, published_at=revision.created_at
    )


async def public_page(session: AsyncSession, slug: PageSlug, locale: Locale) -> PublicPage:
    page = await _find_page(session, slug, locale)
    published = await _published(session, page) if page is not None else None
    return PublicPage(
        slug=slug,
        locale=locale,
        status="published" if published is not None else "unpublished",
        document=published,
    )


def _revision_view(revision: SitePageRevision) -> RevisionDetail:
    return RevisionDetail(
        id=revision.id,
        version=revision.version,
        action=cast(Any, revision.action),
        created_at=revision.created_at,
        created_by_user_id=revision.created_by_user_id,
        document=PageDocument.model_validate(revision.document_json),
    )


async def get_revision(
    session: AsyncSession, slug: PageSlug, locale: Locale, revision_id: UUID
) -> RevisionDetail:
    page = await _require_page(session, slug, locale)
    revision = await session.scalar(
        select(SitePageRevision).where(
            SitePageRevision.id == revision_id, SitePageRevision.page_id == page.id
        )
    )
    if revision is None:
        raise AppError(404, "site_page_revision_not_found", "找不到這份文件的指定版本")
    return _revision_view(revision)


async def page_detail(session: AsyncSession, slug: PageSlug, locale: Locale) -> PageDetail:
    page = await _require_page(session, slug, locale)
    revisions = await session.scalars(
        select(SitePageRevision)
        .where(SitePageRevision.page_id == page.id)
        .order_by(SitePageRevision.version.desc())
        .limit(100)
    )
    audit = await session.scalars(
        select(AdminAuditLog)
        .where(
            AdminAuditLog.target == _target(slug, locale),
            AdminAuditLog.action.in_(AUDIT_ACTIONS),
        )
        .order_by(AdminAuditLog.created_at.desc())
        .limit(20)
    )
    return PageDetail(
        **_summary(page).model_dump(),
        draft=PageDocument.model_validate(page.draft_json),
        published=await _published(session, page),
        revisions=[
            RevisionSummary(**_revision_view(row).model_dump(exclude={"document"}))
            for row in revisions
        ],
        audit=[
            AdminAuditView(
                id=row.id,
                actor_user_id=row.actor_user_id,
                action=row.action,
                target=row.target,
                metadata=row.metadata_json,
                created_at=row.created_at,
            )
            for row in audit
        ],
    )


async def initialize_pages(session: AsyncSession, actor: User) -> InitializationResult:
    """Explicit admin write only; never run at import, startup or public GET.

    The unique slug/locale insert is atomic even for concurrent initializers.
    No draft, published pointer or history that already exists is overwritten.
    """
    created = 0
    insert = sqlite_insert if session.get_bind().dialect.name == "sqlite" else pg_insert
    try:
        for slug in PAGE_SLUGS:
            for locale in LOCALES:
                document = initial_document(slug, locale).model_dump(mode="json")
                now = datetime.now(UTC)
                page_id = await session.scalar(
                    insert(SitePage)
                    .values(
                        id=uuid4(),
                        slug=slug,
                        locale=locale,
                        version=1,
                        draft_json=document,
                        published_version=None,
                        created_at=now,
                        updated_at=now,
                    )
                    .on_conflict_do_nothing(index_elements=[SitePage.slug, SitePage.locale])
                    .returning(SitePage.id)
                )
                if page_id is None:
                    continue
                created += 1
                revision_id = uuid4()
                session.add(
                    SitePageRevision(
                        id=revision_id,
                        page_id=page_id,
                        version=1,
                        action="initialized",
                        document_json=document,
                        created_by_user_id=actor.id,
                        created_at=now,
                    )
                )
                session.add(
                    AdminAuditLog(
                        actor_user_id=actor.id,
                        action="site_page_initialized",
                        target=_target(slug, locale),
                        metadata_json={
                            "revision_id": str(revision_id),
                            "version": 1,
                            "before": None,
                            "after": document,
                            "document_sha256": document_hash(document),
                        },
                    )
                )
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    result = await list_pages(session)
    return InitializationResult(pages=result.pages, created=created)


async def _write_revision(
    session: AsyncSession,
    actor: User,
    page: SitePage,
    expected_version: int,
    document: PageDocument,
    action: str,
    *,
    reason: str | None = None,
    source_revision_id: UUID | None = None,
) -> PageDetail:
    new_version = expected_version + 1
    encoded = document.model_dump(mode="json")
    now = datetime.now(UTC)
    before = dict(page.draft_json)
    previous_published = page.published_version
    revision_id = uuid4()
    try:
        values: dict[str, Any] = {
            "version": new_version,
            "draft_json": encoded,
            "updated_at": now,
        }
        if action == "published":
            values["published_version"] = new_version
        changed = await session.scalar(
            update(SitePage)
            .where(SitePage.id == page.id, SitePage.version == expected_version)
            .values(**values)
            .returning(SitePage.id)
            .execution_options(synchronize_session=False)
        )
        if changed is None:
            raise AppError(409, "site_page_version_conflict", "文件已被更新，請重新載入後再操作")
        session.add(
            SitePageRevision(
                id=revision_id,
                page_id=page.id,
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
                action=f"site_page_{action}",
                target=_target(page.slug, page.locale),
                metadata_json={
                    "revision_id": str(revision_id),
                    "before_version": expected_version,
                    "version": new_version,
                    "before": before,
                    "after": encoded,
                    "previous_published_version": previous_published,
                    "published_version": new_version
                    if action == "published"
                    else previous_published,
                    "reason": reason,
                    "document_sha256": document_hash(encoded),
                    "source_revision_id": str(source_revision_id) if source_revision_id else None,
                    "operator_confirmed": action == "published",
                },
            )
        )
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    return await page_detail(session, cast(PageSlug, page.slug), cast(Locale, page.locale))


async def save_draft(
    session: AsyncSession, actor: User, slug: PageSlug, locale: Locale, payload: DraftWrite
) -> PageDetail:
    page = await _require_page(session, slug, locale)
    return await _write_revision(
        session, actor, page, payload.expected_version, payload.document, "draft_saved"
    )


async def publish_page(
    session: AsyncSession, actor: User, slug: PageSlug, locale: Locale, payload: PublishWrite
) -> PageDetail:
    page = await _require_page(session, slug, locale)
    if page.version != payload.expected_version:
        raise AppError(409, "site_page_version_conflict", "文件已被更新，請重新載入後再操作")
    document = PageDocument.model_validate(page.draft_json)
    if pending_requirements(slug, document):
        raise AppError(409, "site_page_requirements_pending", "請填妥待確認資料及生效日期後再發布")
    return await _write_revision(
        session, actor, page, payload.expected_version, document, "published", reason=payload.reason
    )


async def restore_revision(
    session: AsyncSession, actor: User, slug: PageSlug, locale: Locale, payload: RestoreWrite
) -> PageDetail:
    page = await _require_page(session, slug, locale)
    revision = await get_revision(session, slug, locale, payload.revision_id)
    return await _write_revision(
        session,
        actor,
        page,
        payload.expected_version,
        revision.document,
        "restored",
        reason=payload.reason,
        source_revision_id=revision.id,
    )
