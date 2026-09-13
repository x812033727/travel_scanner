"""Editorial content packs: articles authored in the repository, imported through the same
write path the back office uses.

``app/guides/content/<slug>.json`` holds one article -- its identity and taxonomy plus one
``GuideDocument`` per locale -- next to the images it references under
``apps/web/public/guides/<slug>/``. A pull request is where an article is reviewed; the
command is how it reaches the database. A migration never writes an article.

The command is idempotent and honest about its transaction boundary. ``plan_import`` reads
everything and validates every pack first; if any pack fails, nothing is written.
``apply_import`` then writes per (slug, locale) through ``admin_service`` -- create, new
translation, draft, optional publish -- and each of those commits on its own, exactly as the
editor's clicks do. A failure stops the run there and is reported; the packs already written
stay written, and rerunning finishes the rest, because an article that already matches its
pack is reported ``unchanged`` and left alone.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from importlib.resources import files
from pathlib import Path
from typing import Any, Literal, cast
from uuid import UUID

from pydantic import Field, ValidationError, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.guides import admin_service
from app.guides.models import GuideArticle
from app.guides.schemas import (
    ArticleCreate,
    ArticleUpdate,
    DraftWrite,
    GuideDocument,
    Kind,
    PublishWrite,
    article_slug,
    section_of,
)
from app.guides.service import _locale_rows, _published_document, _topics_for, document_hash
from app.i18n import Locale
from app.models import User
from app.problems import AppError
from app.site_pages.schemas import StrictModel


class ContentPackError(ValueError):
    """A pack that cannot be imported.

    Deliberately not an ``AppError``: nothing here is a sentence a reader is shown, and
    ``tests/test_error_localization.py`` holds every non-operator module to a translated
    sentence per error code. Operator errors raised by ``admin_service`` are re-wrapped with
    their code so the report names the rule that refused the pack.
    """


class ArticlePack(StrictModel):
    slug: str = Field(min_length=2, max_length=120)
    kind: Kind
    destination_id: str | None = Field(default=None, max_length=64)
    topics: list[str] = Field(default_factory=list, max_length=10)
    valid_until: date | None = None
    featured: bool = False
    display_order: int = Field(default=100, ge=0, le=100_000)
    # Insertion order matters: the first locale is the one the article is created with.
    locales: dict[Locale, GuideDocument] = Field(min_length=1)

    @field_validator("slug")
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        return article_slug(value)


def default_directory() -> Path:
    return Path(str(files("app.guides").joinpath("content")))


def load_packs(
    directory: Path | None = None, *, slugs: set[str] | None = None
) -> list[ArticlePack]:
    """Every ``<slug>.json`` in the directory, validated. A pack whose slug does not match
    its file name is refused: the file name is what a reviewer greps for."""
    root = directory or default_directory()
    paths = sorted(root.glob("*.json")) if root.is_dir() else []
    packs: list[ArticlePack] = []
    for path in paths:
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise ContentPackError(f"{path.name}: {error}") from error
        try:
            pack = ArticlePack.model_validate(raw)
        except ValidationError as error:
            raise ContentPackError(f"{path.name}: {error}") from error
        if pack.slug != path.stem:
            raise ContentPackError(f"{path.name}: slug '{pack.slug}' must match the file name")
        if slugs is None or pack.slug in slugs:
            packs.append(pack)
    return packs


LocaleAction = Literal["create", "update", "unchanged"]
TaxonomyAction = Literal["create", "update", "unchanged"]


@dataclass
class LocalePlan:
    locale: Locale
    action: LocaleAction
    # Whether ``--publish`` has anything to do: no public version yet, or one that differs.
    publish: bool


@dataclass
class ArticlePlan:
    pack: ArticlePack
    article_id: UUID | None
    taxonomy: TaxonomyAction
    locales: list[LocalePlan]


@dataclass
class ImportPlan:
    articles: list[ArticlePlan] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "articles": [
                {
                    "slug": entry.pack.slug,
                    "taxonomy": entry.taxonomy,
                    "locales": [
                        {"locale": item.locale, "action": item.action, "publish": item.publish}
                        for item in entry.locales
                    ],
                }
                for entry in self.articles
            ]
        }


def _key(slug: str, locale: str) -> str:
    return f"{slug}:{locale}"


def _same_taxonomy(
    article: GuideArticle, pack: ArticlePack, destination: str | None, topics: list[str]
) -> bool:
    wanted = {slug.strip().casefold() for slug in pack.topics if slug.strip()}
    return (
        article.kind == pack.kind
        and article.destination_id == destination
        and article.valid_until == pack.valid_until
        and article.featured == pack.featured
        and article.display_order == pack.display_order
        and set(topics) == wanted
    )


async def plan_import(
    session: AsyncSession, packs: list[ArticlePack], *, locales: set[Locale] | None = None
) -> ImportPlan:
    """Validate every pack and compare it with the database. Reads only.

    Raises ``ContentPackError`` on the first pack that could not be imported, before any
    plan is returned -- so a run with one bad pack writes nothing at all.
    """
    plan = ImportPlan()
    for pack in packs:
        chosen = {
            locale: document
            for locale, document in pack.locales.items()
            if locales is None or locale in locales
        }
        if not chosen:
            continue
        try:
            destination = admin_service._validate_destination(pack.destination_id)
            await admin_service._resolve_topics(session, pack.topics, section_of(pack.kind))
            for document in chosen.values():
                admin_service._validate_document(document, destination)
        except AppError as error:
            raise ContentPackError(f"{pack.slug}: {error.code}: {error.detail}") from error

        article = await session.scalar(select(GuideArticle).where(GuideArticle.slug == pack.slug))
        if article is None:
            plan.articles.append(
                ArticlePlan(
                    pack=pack,
                    article_id=None,
                    taxonomy="create",
                    locales=[LocalePlan(locale, "create", True) for locale in chosen],
                )
            )
            continue

        topics = [
            row.slug for row in (await _topics_for(session, [article.id])).get(article.id, [])
        ]
        rows = {
            cast(Locale, row.locale): row
            for row in (await _locale_rows(session, [article.id])).get(article.id, [])
        }
        locale_plans: list[LocalePlan] = []
        for locale, document in chosen.items():
            wanted = document.model_dump(mode="json")
            row = rows.get(locale)
            if row is None:
                locale_plans.append(LocalePlan(locale, "create", True))
                continue
            # Normalised on both sides: a row written before ``hero`` existed lacks the key,
            # and comparing raw JSON would report every old article as changed.
            current = GuideDocument.model_validate(row.draft_json).model_dump(mode="json")
            try:
                published = await _published_document(session, row)
            except AppError as error:
                raise ContentPackError(f"{pack.slug}: {error.code}: {error.detail}") from error
            live = (
                published.model_dump(
                    mode="json", exclude={"version", "published_at", "modified_at"}
                )
                if published is not None
                else None
            )
            locale_plans.append(
                LocalePlan(locale, "unchanged" if current == wanted else "update", live != wanted)
            )
        plan.articles.append(
            ArticlePlan(
                pack=pack,
                article_id=article.id,
                taxonomy="unchanged"
                if _same_taxonomy(article, pack, destination, topics)
                else "update",
                locales=locale_plans,
            )
        )
    return plan


@dataclass
class ImportReport:
    created: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    published: list[str] = field(default_factory=list)
    taxonomy_updated: list[str] = field(default_factory=list)
    failed: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "created": self.created,
            "updated": self.updated,
            "unchanged": self.unchanged,
            "published": self.published,
            "taxonomy_updated": self.taxonomy_updated,
            "failed": self.failed,
        }


def _taxonomy_payload(pack: ArticlePack, expected_version: int) -> ArticleUpdate:
    return ArticleUpdate(
        expected_version=expected_version,
        kind=pack.kind,
        destination_id=pack.destination_id,
        topics=pack.topics,
        valid_until=pack.valid_until,
        featured=pack.featured,
        display_order=pack.display_order,
    )


async def _locale_version(session: AsyncSession, article_id: UUID, locale: Locale) -> int:
    detail = await admin_service.article_detail(session, article_id, locale)
    return next(state.version for state in detail.locales if state.locale == locale)


async def _apply_article(
    session: AsyncSession, actor: User, entry: ArticlePlan, *, publish: bool, report: ImportReport
) -> None:
    pack = entry.pack
    article_id = entry.article_id
    if article_id is None:
        first = entry.locales[0]
        detail = await admin_service.create_article(
            session,
            actor,
            ArticleCreate(
                slug=pack.slug,
                kind=pack.kind,
                destination_id=pack.destination_id,
                topics=pack.topics,
                valid_until=pack.valid_until,
                document=pack.locales[first.locale],
                locale=first.locale,
            ),
        )
        article_id = detail.id
        report.created.append(_key(pack.slug, first.locale))
        # ``ArticleCreate`` carries neither flag, so the defaults are corrected right after.
        if pack.featured or pack.display_order != 100:
            await admin_service.update_article(
                session, actor, article_id, _taxonomy_payload(pack, detail.version), first.locale
            )
        for item in entry.locales[1:]:
            await admin_service.start_translation(
                session, actor, article_id, item.locale, pack.locales[item.locale]
            )
            report.created.append(_key(pack.slug, item.locale))
    else:
        if entry.taxonomy == "update":
            article = await admin_service._find_article(session, article_id)
            await admin_service.update_article(
                session,
                actor,
                article_id,
                _taxonomy_payload(pack, article.version),
                entry.locales[0].locale,
            )
            report.taxonomy_updated.append(pack.slug)
        for item in entry.locales:
            if item.action == "create":
                await admin_service.start_translation(
                    session, actor, article_id, item.locale, pack.locales[item.locale]
                )
                report.created.append(_key(pack.slug, item.locale))
            elif item.action == "update":
                version = await _locale_version(session, article_id, item.locale)
                await admin_service.save_draft(
                    session,
                    actor,
                    article_id,
                    item.locale,
                    DraftWrite(expected_version=version, document=pack.locales[item.locale]),
                )
                report.updated.append(_key(pack.slug, item.locale))
            else:
                report.unchanged.append(_key(pack.slug, item.locale))

    if not publish:
        return
    for item in entry.locales:
        if not item.publish:
            continue
        version = await _locale_version(session, article_id, item.locale)
        digest = document_hash(pack.locales[item.locale].model_dump(mode="json"))[:12]
        await admin_service.publish_locale(
            session,
            actor,
            article_id,
            item.locale,
            PublishWrite(expected_version=version, confirmed=True, reason=f"content pack {digest}"),
        )
        report.published.append(_key(pack.slug, item.locale))


async def apply_import(
    session: AsyncSession, actor: User, plan: ImportPlan, *, publish: bool
) -> ImportReport:
    """Write the plan, article by article, stopping at the first refusal.

    Each ``admin_service`` call commits on its own, so this cannot promise all-or-nothing
    across articles; it promises that what was written is exactly what the report says, and
    that rerunning after fixing the cause finishes the rest.
    """
    report = ImportReport()
    for entry in plan.articles:
        try:
            await _apply_article(session, actor, entry, publish=publish, report=report)
        except AppError as error:
            report.failed = f"{entry.pack.slug}: {error.code}: {error.detail}"
            break
    return report
