"""Real isolated tables: privacy boundaries, versioned transactions and admin capabilities.

PostgreSQL variants run in their own disposable schema only when the existing
integration flag is enabled. SQLite is not presented as evidence of PG row races.
"""

from __future__ import annotations

import asyncio
import copy
import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy import event, func, select, text, update
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.auth.service import current_user
from app.config import get_settings
from app.db import Base, get_session
from app.i18n import ERROR_DETAILS, LOCALES
from app.models import AdminAuditLog, SitePage, SitePageRevision, User
from app.problems import AppError, app_error_handler, validation_error_handler
from app.site_pages import service
from app.site_pages.router import admin_router, public_router
from app.site_pages.schemas import (
    PAGE_SLUGS,
    DraftWrite,
    LinkBlock,
    PageDocument,
    PublishWrite,
    RestoreWrite,
)

TABLES = [User.__table__, SitePage.__table__, SitePageRevision.__table__, AdminAuditLog.__table__]


@pytest.fixture(params=["sqlite", "postgresql"])
async def database(request, tmp_path) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    schema = f"site_pages_test_{uuid4().hex}"
    if request.param == "postgresql":
        if os.getenv("RUN_INTEGRATION_TESTS") != "1":
            pytest.skip("requires isolated PostgreSQL integration services")
        url = get_settings().database_url
        assert make_url(url).host in {"localhost", "127.0.0.1", "::1", "postgres", "db"}
        engine = create_async_engine(
            url, poolclass=NullPool, execution_options={"schema_translate_map": {None: schema}}
        )
        async with engine.begin() as connection:
            await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
    else:
        engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'site-pages.db'}")

        @event.listens_for(engine.sync_engine, "connect")
        def foreign_keys(connection, _record):
            connection.execute("PRAGMA foreign_keys=ON")

    async with engine.begin() as connection:
        await connection.run_sync(lambda conn: Base.metadata.create_all(conn, tables=TABLES))
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        yield factory
    finally:
        async with engine.begin() as connection:
            if request.param == "postgresql":
                await connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
            else:
                await connection.run_sync(lambda conn: Base.metadata.drop_all(conn, tables=TABLES))
        await engine.dispose()


@pytest.fixture
async def actor(database) -> User:
    user = User(
        id=uuid4(),
        email=f"site-pages-{uuid4().hex}@example.com",
        password_hash="test-hash",
        is_admin=True,
        is_active=True,
    )
    async with database() as session:
        session.add(user)
        await session.commit()
    return user


def confirmed_document(slug="privacy", locale="en") -> PageDocument:
    payload = service.initial_document(slug, locale).model_dump(mode="json")
    payload["effective_date"] = datetime.now(UTC).date().isoformat()
    payload["requirements"] = {
        key: f"Test-only confirmed {key}; not a real operator policy"
        for key in ("operator", "location", "contact", "retention", "legal")
    }
    return PageDocument.model_validate(payload)


async def counts(session) -> tuple[int, int, int]:
    values = [
        int(await session.scalar(select(func.count()).select_from(model)))
        for model in (SitePage, SitePageRevision, AdminAuditLog)
    ]
    return values[0], values[1], values[2]


def make_app(database, actor=None) -> FastAPI:
    application = FastAPI()
    application.include_router(admin_router, prefix="/api/v1")
    application.include_router(public_router, prefix="/api/v1")
    application.add_exception_handler(AppError, app_error_handler)
    application.add_exception_handler(RequestValidationError, validation_error_handler)

    async def session_dependency():
        async with database() as session:
            yield session

    application.dependency_overrides[get_session] = session_dependency
    if actor is not None:
        application.dependency_overrides[current_user] = lambda: actor
    return application


@pytest.mark.parametrize("locale", LOCALES)
def test_all_twenty_initial_documents_are_localized_unpublished_and_pending(locale) -> None:
    titles = []
    for slug in PAGE_SLUGS:
        document = service.initial_document(slug, locale)
        titles.append(document.title)
        assert document.effective_date is None
        assert set(document.requirements.model_dump().values()) == {""}
        assert len(document.blocks) >= 4
        assert "operator" in service.pending_requirements(slug, document)
        assert "contact" in service.pending_requirements(slug, document)
        assert "effective_date" in service.pending_requirements(slug, document)
        assert "@" not in document.model_dump_json()
    assert len(set(titles)) == 4


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "data:text/html,hello",
        "//example.com",
        "/privacy",
        "https://name:password@example.com",
        "https://example.com:99999/",
        "https://example.com\\@evil.example",
        "https://example.com/\npath",
        "mailto:person@example.com?bcc=other@example.com",
        "mailto:invalid",
        "file:///etc/passwd",
        "https:///missing-host",
        "https://[invalid",
    ],
)
def test_links_reject_unsafe_protocols_credentials_headers_and_malformed_hosts(url) -> None:
    with pytest.raises(ValidationError):
        LinkBlock(type="link", text="Example", url=url)


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/privacy",
        "http://example.com/contact",
        "mailto:privacy@example.com",
    ],
)
def test_safe_external_links_are_preserved_without_fetching(url) -> None:
    assert LinkBlock(type="link", text="Example", url=url).url == url


@pytest.mark.parametrize(
    "patch",
    [
        {"title": "  "},
        {"description": "\x00private"},
        {"title": "<script>alert(1)</script>"},
        {"blocks": []},
        {"blocks": [{"type": "html", "html": "x"}]},
        {"blocks": [{"type": "paragraph", "text": "fine", "html": "ignored?"}]},
        {"blocks": [{"type": "heading", "level": 1, "text": "No duplicate H1"}]},
        {"blocks": [{"type": "list", "items": [" "]}]},
        {"blocks": [{"type": "paragraph", "text": "a" * 4001}]},
        {"requirements": {"operator": "<img src=x>"}},
        {"publish_now": True},
    ],
)
def test_document_validation_is_plain_structured_bounded_and_closed(patch) -> None:
    document = confirmed_document().model_dump(mode="json")
    document.update(patch)
    with pytest.raises(ValidationError):
        PageDocument.model_validate(document)


def test_document_total_size_is_bounded() -> None:
    payload = confirmed_document().model_dump(mode="json")
    payload["blocks"] = [{"type": "paragraph", "text": "x" * 4000}] * 20
    with pytest.raises(ValidationError):
        PageDocument.model_validate(payload)


@pytest.mark.parametrize("confirmed", [False, "true", 1, None])
def test_publish_requires_a_real_explicit_true_boolean(confirmed) -> None:
    with pytest.raises(ValidationError):
        PublishWrite(expected_version=1, confirmed=confirmed, reason="Reviewed by operator")


@pytest.mark.parametrize("version", [0, -1, True, "1", 2_147_483_647])
def test_mutation_versions_require_positive_integers(version) -> None:
    with pytest.raises(ValidationError):
        DraftWrite(expected_version=version, document=confirmed_document())


def test_error_codes_are_translated_in_all_five_locales() -> None:
    for locale in LOCALES:
        for code in (
            "site_page_not_found",
            "site_page_revision_not_found",
            "site_page_version_conflict",
            "site_page_requirements_pending",
            "site_page_unavailable",
        ):
            assert ERROR_DETAILS[locale][code]


async def test_public_read_does_not_initialize_or_expose_any_drafts(database, actor) -> None:
    application = make_app(database)
    async with AsyncClient(
        transport=ASGITransport(app=application), base_url="http://test"
    ) as client:
        for locale in LOCALES:
            for slug in PAGE_SLUGS:
                response = await client.get(f"/api/v1/site-pages/{slug}?locale={locale}")
                assert response.status_code == 200
                assert response.headers["cache-control"] == "no-store"
                assert response.json() == {
                    "slug": slug,
                    "locale": locale,
                    "status": "unpublished",
                    "document": None,
                }
        assert (await client.get("/api/v1/site-pages/privacy?locale=xx")).status_code == 422
        assert (await client.get("/api/v1/site-pages/unknown")).status_code == 422
    async with database() as session:
        assert await counts(session) == (0, 0, 0)
        await service.initialize_pages(session, actor)
        for locale in LOCALES:
            for slug in PAGE_SLUGS:
                assert (await service.public_page(session, slug, locale)).document is None


async def test_initialize_is_explicit_atomic_and_does_not_overwrite_existing_documents(
    database,
    actor,
) -> None:
    async with database() as session:
        first = await service.initialize_pages(session, actor)
        assert first.created == 20 and len(first.pages) == 20
        assert await counts(session) == (20, 20, 20)
        updated = await service.save_draft(
            session,
            actor,
            "about",
            "ja",
            DraftWrite(expected_version=1, document=confirmed_document("about", "ja")),
        )
        await service.publish_page(
            session,
            actor,
            "about",
            "ja",
            PublishWrite(expected_version=2, confirmed=True, reason="Test operator confirmation"),
        )
        again = await service.initialize_pages(session, actor)
        assert again.created == 0
        assert await counts(session) == (20, 22, 22)
        preserved = await service.page_detail(session, "about", "ja")
        assert preserved.draft == updated.draft
        assert preserved.version == preserved.published_version == 3


async def test_save_publish_edit_restore_preserve_history_and_public_snapshot(
    database, actor
) -> None:
    async with database() as session:
        await service.initialize_pages(session, actor)
        original = await service.page_detail(session, "privacy", "en")
        saved = await service.save_draft(
            session,
            actor,
            "privacy",
            "en",
            DraftWrite(expected_version=1, document=confirmed_document()),
        )
        assert saved.version == 2 and saved.published is None
        assert saved.pending_requirements == []
        published = await service.publish_page(
            session,
            actor,
            "privacy",
            "en",
            PublishWrite(expected_version=2, confirmed=True, reason="Reviewed test draft"),
        )
        assert published.version == published.published_version == 3
        public = await service.public_page(session, "privacy", "en")
        assert public.document is not None and public.document.version == 3
        assert (await service.public_page(session, "privacy", "ja")).document is None
        assert "actor" not in public.model_dump_json()
        changed = published.draft.model_copy(update={"title": "Private replacement title"})
        await service.save_draft(
            session, actor, "privacy", "en", DraftWrite(expected_version=3, document=changed)
        )
        assert (await service.public_page(session, "privacy", "en")) == public
        restored = await service.restore_revision(
            session,
            actor,
            "privacy",
            "en",
            RestoreWrite(
                expected_version=4,
                revision_id=original.revisions[0].id,
                reason="Restore first draft",
            ),
        )
        assert restored.version == 5 and restored.published_version == 3
        assert restored.draft == original.draft
        assert (await service.public_page(session, "privacy", "en")) == public
        assert [row.action for row in restored.revisions] == [
            "restored",
            "draft_saved",
            "published",
            "draft_saved",
            "initialized",
        ]
        for summary in restored.revisions:
            revision = await service.get_revision(session, "privacy", "en", summary.id)
            assert revision.version == summary.version
            assert revision.created_by_user_id == actor.id
        audit = next(row for row in restored.audit if row.action == "site_page_published")
        assert audit.actor_user_id == actor.id
        assert audit.metadata["after"] == saved.draft.model_dump(mode="json")
        assert len(str(audit.metadata["after"])) > 500  # Never truncate legal history.
        assert audit.metadata["operator_confirmed"] is True
        assert audit.metadata["reason"] == "Reviewed test draft"
        assert await counts(session) == (20, 24, 24)


async def test_pending_or_future_effective_documents_cannot_publish(database, actor) -> None:
    async with database() as session:
        await service.initialize_pages(session, actor)
        with pytest.raises(AppError) as pending:
            await service.publish_page(
                session,
                actor,
                "privacy",
                "en",
                PublishWrite(expected_version=1, confirmed=True, reason="Not enough information"),
            )
        assert pending.value.code == "site_page_requirements_pending"
        document = confirmed_document()
        document.effective_date = datetime.now(UTC).date() + timedelta(days=1)
        await service.save_draft(
            session, actor, "privacy", "en", DraftWrite(expected_version=1, document=document)
        )
        with pytest.raises(AppError) as future:
            await service.publish_page(
                session,
                actor,
                "privacy",
                "en",
                PublishWrite(expected_version=2, confirmed=True, reason="No scheduled publication"),
            )
        assert future.value.code == "site_page_requirements_pending"
        assert await counts(session) == (20, 21, 21)
        assert (await service.public_page(session, "privacy", "en")).document is None


async def test_stale_draft_publish_restore_replays_cannot_create_duplicate_history(database, actor):
    async with database() as session:
        await service.initialize_pages(session, actor)
        original = await service.page_detail(session, "privacy", "en")
        await service.save_draft(
            session,
            actor,
            "privacy",
            "en",
            DraftWrite(expected_version=1, document=confirmed_document()),
        )
        for action in (
            lambda: service.save_draft(
                session,
                actor,
                "privacy",
                "en",
                DraftWrite(expected_version=1, document=confirmed_document()),
            ),
            lambda: service.publish_page(
                session,
                actor,
                "privacy",
                "en",
                PublishWrite(expected_version=1, confirmed=True, reason="stale"),
            ),
            lambda: service.restore_revision(
                session,
                actor,
                "privacy",
                "en",
                RestoreWrite(
                    expected_version=1, revision_id=original.revisions[0].id, reason="stale"
                ),
            ),
        ):
            with pytest.raises(AppError) as stale:
                await action()
            assert stale.value.code == "site_page_version_conflict"
        assert await counts(session) == (20, 21, 21)


async def test_revision_ids_are_bound_to_page_and_locale(database, actor) -> None:
    async with database() as session:
        await service.initialize_pages(session, actor)
        original = await service.page_detail(session, "privacy", "en")
        for slug, locale in [("terms", "en"), ("privacy", "ja")]:
            with pytest.raises(AppError) as rejected:
                await service.restore_revision(
                    session,
                    actor,
                    slug,
                    locale,
                    RestoreWrite(
                        expected_version=1,
                        revision_id=original.revisions[0].id,
                        reason="wrong document",
                    ),
                )
            assert rejected.value.code == "site_page_revision_not_found"
        assert await counts(session) == (20, 20, 20)


async def test_commit_failure_rolls_back_pointer_revision_and_audit(database, actor, monkeypatch):
    async with database() as session:
        await service.initialize_pages(session, actor)
        await service.save_draft(
            session,
            actor,
            "privacy",
            "en",
            DraftWrite(expected_version=1, document=confirmed_document()),
        )
        original_commit = session.commit

        async def fail_commit():
            await session.flush()
            raise RuntimeError("test-only transaction failure")

        monkeypatch.setattr(session, "commit", fail_commit)
        with pytest.raises(RuntimeError, match="test-only"):
            await service.publish_page(
                session,
                actor,
                "privacy",
                "en",
                PublishWrite(expected_version=2, confirmed=True, reason="Must roll back together"),
            )
        monkeypatch.setattr(session, "commit", original_commit)
    async with database() as verification:
        assert await counts(verification) == (20, 21, 21)
        detail = await service.page_detail(verification, "privacy", "en")
        assert detail.version == 2 and detail.published_version is None


@pytest.mark.parametrize(
    "role,can_read,can_write",
    [
        ("member", False, False),
        ("viewer", True, False),
        ("support", False, False),
        ("content", False, False),
        ("operations", True, True),
        ("owner", True, True),
    ],
)
async def test_route_capabilities_apply_to_every_read_and_write(
    database, actor, role, can_read, can_write
):
    actor.__dict__["_admin_roles_cache"] = frozenset() if role == "member" else frozenset({role})
    application = make_app(database, actor)
    async with AsyncClient(
        transport=ASGITransport(app=application), base_url="http://test"
    ) as client:
        listed = await client.get("/api/v1/admin/site-pages")
        assert listed.status_code == (200 if can_read else 403)
        initialized = await client.post("/api/v1/admin/site-pages/initialize")
        assert initialized.status_code == (200 if can_write else 403)
        if can_write:
            current = await client.get("/api/v1/admin/site-pages/privacy?locale=en")
            assert current.status_code == 200
            revision_id = current.json()["revisions"][0]["id"]
            detail = await client.get(
                f"/api/v1/admin/site-pages/privacy/revisions/{revision_id}?locale=en"
            )
            assert detail.status_code == 200
            written = await client.put(
                "/api/v1/admin/site-pages/privacy/draft?locale=en",
                json={
                    "expected_version": 1,
                    "document": confirmed_document().model_dump(mode="json"),
                },
            )
            assert written.status_code == 200
            published = await client.post(
                "/api/v1/admin/site-pages/privacy/publish?locale=en",
                json={
                    "expected_version": 2,
                    "confirmed": True,
                    "reason": "Test confirmation",
                },
            )
            assert published.status_code == 200
            restored = await client.post(
                "/api/v1/admin/site-pages/privacy/restore?locale=en",
                json={
                    "expected_version": 3,
                    "revision_id": revision_id,
                    "reason": "Test restoration",
                },
            )
            assert restored.status_code == 200
        else:
            for path, body in [
                ("publish", {"expected_version": 1, "confirmed": True, "reason": "Denied"}),
                (
                    "restore",
                    {"expected_version": 1, "revision_id": str(uuid4()), "reason": "Denied"},
                ),
            ]:
                assert (
                    await client.post(
                        f"/api/v1/admin/site-pages/privacy/{path}?locale=en", json=body
                    )
                ).status_code == 403
            assert (
                await client.put(
                    "/api/v1/admin/site-pages/privacy/draft?locale=en",
                    json={
                        "expected_version": 1,
                        "document": confirmed_document().model_dump(mode="json"),
                    },
                )
            ).status_code == 403


async def test_anonymous_admin_access_is_rejected_without_initializing(database) -> None:
    application = make_app(database)
    async with AsyncClient(
        transport=ASGITransport(app=application), base_url="http://test"
    ) as client:
        assert (await client.get("/api/v1/admin/site-pages")).status_code == 401
        assert (await client.post("/api/v1/admin/site-pages/initialize")).status_code == 401
    async with database() as session:
        assert await counts(session) == (0, 0, 0)


async def test_two_postgres_sessions_with_same_version_have_one_winner(database, actor):
    async with database() as setup:
        if setup.get_bind().dialect.name != "postgresql":
            pytest.skip("PostgreSQL row-lock behavior is not proved by SQLite")
        await service.initialize_pages(setup, actor)
    barrier = asyncio.Barrier(2)

    async def writer(title: str):
        async with database() as session:
            page = await service._require_page(session, "privacy", "en")
            document = copy.deepcopy(confirmed_document())
            document.title = title
            await barrier.wait()
            try:
                await service._write_revision(session, actor, page, 1, document, "draft_saved")
                return "ok"
            except AppError as error:
                return error.code

    outcomes = await asyncio.wait_for(
        asyncio.gather(writer("Writer A"), writer("Writer B")), timeout=30
    )
    assert sorted(outcomes) == ["ok", "site_page_version_conflict"]
    async with database() as session:
        assert await counts(session) == (20, 21, 21)
        assert (await service.page_detail(session, "privacy", "en")).version == 2


async def test_public_published_response_is_allowlisted_and_not_cached(database, actor):
    async with database() as session:
        await service.initialize_pages(session, actor)
        await service.save_draft(
            session,
            actor,
            "privacy",
            "en",
            DraftWrite(expected_version=1, document=confirmed_document()),
        )
        await service.publish_page(
            session,
            actor,
            "privacy",
            "en",
            PublishWrite(expected_version=2, confirmed=True, reason="Private audit reason"),
        )
    application = make_app(database)
    async with AsyncClient(
        transport=ASGITransport(app=application), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/site-pages/privacy?locale=en")
        assert response.status_code == 200
        assert response.headers["cache-control"] == "no-store"
        payload = response.json()
        assert set(payload) == {"slug", "locale", "status", "document"}
        assert set(payload["document"]) == {
            "title",
            "description",
            "blocks",
            "requirements",
            "effective_date",
            "version",
            "published_at",
        }
        assert payload["status"] == "published"
        assert actor.email not in response.text
        assert str(actor.id) not in response.text
        assert "Private audit reason" not in response.text


async def test_broken_published_pointer_never_falls_back_to_draft(database, actor):
    async with database() as session:
        await service.initialize_pages(session, actor)
        await session.execute(
            update(SitePage)
            .where(SitePage.slug == "privacy", SitePage.locale == "en")
            .values(published_version=1)
        )  # Revision 1 is a draft, not a publication.
        await session.commit()
        with pytest.raises(AppError) as failed:
            await service.public_page(session, "privacy", "en")
        assert failed.value.code == "site_page_unavailable"


async def test_two_postgres_initializers_do_not_duplicate_or_overwrite(database, actor):
    async with database() as setup:
        if setup.get_bind().dialect.name != "postgresql":
            pytest.skip("PostgreSQL insert conflict behavior is not proved by SQLite")
    barrier = asyncio.Barrier(2)

    async def initialize():
        async with database() as session:
            await barrier.wait()
            return (await service.initialize_pages(session, actor)).created

    outcomes = await asyncio.wait_for(asyncio.gather(initialize(), initialize()), timeout=30)
    assert sum(outcomes) == 20
    async with database() as session:
        assert await counts(session) == (20, 20, 20)
        assert all(
            page.published_version is None for page in (await service.list_pages(session)).pages
        )
