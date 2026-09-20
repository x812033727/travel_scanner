"""Read-only editorial snapshot. Run through stdin inside the deployed API container."""

import asyncio
import hashlib
import json
from datetime import UTC, datetime

from app.db import SessionFactory
from app.guides.models import (
    GuideArticle,
    GuideArticleLocale,
    GuideArticleRevision,
    GuideArticleTopic,
    GuideTopic,
)
from app.guides.publication import article_status
from app.guides.schemas import GuideDocument
from sqlalchemy import select, text


def normalized(document):
    return GuideDocument.model_validate(document).model_dump(mode="json")


def digest(document):
    return hashlib.sha256(
        json.dumps(
            document, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()


async def main():
    async with SessionFactory() as session:
        await session.execute(
            text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY")
        )
        articles = (
            await session.scalars(select(GuideArticle).order_by(GuideArticle.slug))
        ).all()
        locale_rows = (await session.scalars(select(GuideArticleLocale))).all()
        revision_rows = (await session.scalars(select(GuideArticleRevision))).all()
        topic_rows = await session.execute(
            select(GuideArticleTopic.article_id, GuideTopic.slug).join(
                GuideTopic, GuideTopic.id == GuideArticleTopic.topic_id
            )
        )
        topics = {}
        for article_id, slug in topic_rows:
            topics.setdefault(article_id, []).append(slug)
        by_id = {}
        for row in locale_rows:
            by_id.setdefault(row.article_id, []).append(row)
        revisions = {(r.article_locale_id, r.version): r for r in revision_rows}
        result = []
        for article in articles:
            rows = by_id.get(article.id, [])
            item = {
                "id": str(article.id),
                "slug": article.slug,
                "kind": article.kind,
                "version": article.version,
                "status": article_status(article, rows),
                "is_active": article.is_active,
                "destination_id": article.destination_id,
                "topics": sorted(topics.get(article.id, [])),
                "featured": article.featured,
                "display_order": article.display_order,
                "valid_until": article.valid_until.isoformat()
                if article.valid_until
                else None,
                "locales": {},
            }
            for row in sorted(rows, key=lambda r: r.locale):
                draft = normalized(row.draft_json)
                revision = revisions.get((row.id, row.published_version))
                if row.published_version is not None and (
                    revision is None or revision.action != "published"
                ):
                    raise RuntimeError(
                        f"Invalid published pointer: {article.slug}:{row.locale}"
                    )
                published = normalized(revision.document_json) if revision else None
                item["locales"][row.locale] = {
                    "id": str(row.id),
                    "version": row.version,
                    "published_version": row.published_version,
                    "published_at": row.published_at.isoformat()
                    if row.published_at
                    else None,
                    "draft": draft,
                    "draft_sha256": digest(draft),
                    "published": published,
                    "published_sha256": digest(published) if published else None,
                }
            result.append(item)
        print(
            json.dumps(
                {
                    "schema_version": 1,
                    "captured_at": datetime.now(UTC).isoformat(),
                    "read_only": True,
                    "articles": result,
                },
                ensure_ascii=False,
            )
        )
        await session.rollback()


if __name__ == "__main__":
    asyncio.run(main())
