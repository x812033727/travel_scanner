from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import cast
from unittest.mock import Mock

import pytest
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base
from app.guides.schemas import GuideDocument
from app.i18n import Locale
from app.news_automation import assets, jobs
from app.news_automation.models import NewsAsset, NewsCandidate, NewsEvidence, NewsSource
from app.news_automation.policy import hard_policy_problems
from app.problems import AppError

LOCALES: tuple[Locale, ...] = ("zh-TW", "zh-CN", "en", "ja", "ko")


def no_object_storage() -> None:
    raise AppError(503, "community_storage_unavailable", "community_storage_unavailable")


async def database() -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite://")
    tables = cast(
        list[Table],
        [
            NewsSource.__table__,
            NewsCandidate.__table__,
            NewsEvidence.__table__,
            NewsAsset.__table__,
        ],
    )
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    return async_sessionmaker(engine, expire_on_commit=False)


async def seed_candidate(session: AsyncSession) -> NewsCandidate:
    source = NewsSource(
        name="Official",
        url="https://example.com/feed",
        format="rss",
        role="evidence",
        vertical="ai",
    )
    session.add(source)
    await session.flush()
    candidate = NewsCandidate(
        source_id=source.id,
        vertical="ai",
        canonical_url="https://example.com/a",
        source_title="Release",
        content_hash="a" * 64,
        idempotency_key="b" * 64,
    )
    session.add(candidate)
    await session.commit()
    return candidate


def documents() -> dict[Locale, GuideDocument]:
    return {
        locale: GuideDocument.model_validate(
            {
                "title": f"Release {locale}",
                "description": "What changed.",
                "blocks": [{"type": "paragraph", "text": "Body."}],
                "sources": [],
            }
        )
        for locale in LOCALES
    }


@pytest.fixture
def complete_news_documents() -> dict[Locale, GuideDocument]:
    """Five complete news documents before the asset stage adds their cover images."""
    copy: dict[Locale, tuple[str, str, tuple[str, str, str], str, str, str]] = {
        "zh-TW": (
            "Example 公布字幕搜尋更新",
            "Example 表示，新功能讓使用者在字幕中搜尋文字。",
            ("更新內容", "使用方式", "待確認事項"),
            "這次更新了什麼？",
            "消息來自哪裡？",
            "查看同分類最新消息",
        ),
        "zh-CN": (
            "Example 公布字幕搜索更新",
            "Example 表示，新功能让用户在字幕中搜索文字。",
            ("更新内容", "使用方式", "待确认事项"),
            "这次更新了什么？",
            "消息来自哪里？",
            "查看同分类最新消息",
        ),
        "en": (
            "Example announces caption search",
            "Example says its new feature lets users search text in captions.",
            ("What changed", "How it works", "What remains to be confirmed"),
            "What does the update add?",
            "Where did the announcement come from?",
            "Browse the latest news in this topic",
        ),
        "ja": (
            "Example が字幕検索の更新を発表",
            "Example によると、新機能で字幕内の文字を検索できます。",
            ("更新内容", "利用方法", "確認が必要な点"),
            "今回何が追加されましたか？",
            "発表の情報源はどこですか？",
            "このトピックの最新ニュースを見る",
        ),
        "ko": (
            "Example, 자막 검색 업데이트 발표",
            "Example은 새 기능으로 자막의 텍스트를 검색할 수 있다고 밝혔습니다.",
            ("업데이트 내용", "이용 방법", "추가 확인 사항"),
            "이번 업데이트에서 무엇이 추가되었나요?",
            "발표의 출처는 어디인가요?",
            "이 주제의 최신 뉴스 보기",
        ),
    }
    output: dict[Locale, GuideDocument] = {}
    for locale, (title, lead, headings, first_question, second_question, link_text) in copy.items():
        output[locale] = GuideDocument.model_validate(
            {
                "title": title,
                "description": lead,
                "blocks": [
                    {"type": "summary", "items": [title, lead]},
                    {"type": "heading", "level": 2, "text": headings[0]},
                    {"type": "paragraph", "text": lead},
                    {"type": "heading", "level": 2, "text": headings[1]},
                    {"type": "table", "header": list(headings[:2]), "rows": [[title, lead]]},
                    {"type": "heading", "level": 2, "text": headings[2]},
                    {"type": "callout", "tone": "info", "text": lead},
                    {
                        "type": "faq",
                        "items": [
                            {"question": first_question, "answer": lead},
                            {"question": second_question, "answer": title},
                        ],
                    },
                    {
                        "type": "link",
                        "text": link_text,
                        "url": f"https://mokaair.com/{locale}/life/topics/ai-news",
                    },
                ],
                "sources": [
                    {
                        "title": "Example announcement",
                        "url": "https://example.com/a",
                        "checked_on": "2026-10-01",
                    }
                ],
            }
        )
    return output


@pytest.mark.asyncio
async def test_real_news_assets_pass_publication_checks_without_the_retired_figure(
    monkeypatch: pytest.MonkeyPatch,
    complete_news_documents: dict[Locale, GuideDocument],
) -> None:
    """The cover-only asset output must agree with the actual publication policy."""
    factory = await database()
    monkeypatch.setattr(assets, "storage", no_object_storage)
    async with factory() as session:
        candidate = await seed_candidate(session)
        rendered = await assets.ensure_assets(session, candidate, complete_news_documents)
        await session.commit()
        rows = list(await session.scalars(select(NewsAsset)))
        assert {row.variant for row in rows} == {"hero", "social"}
    for document in rendered.values():
        assert document.hero is not None
        assert not any(block.type == "image" for block in document.blocks)
    assert {
        locale: hard_policy_problems(document, "ai", locale, source_count=1)
        for locale, document in rendered.items()
    } == {locale: [] for locale in LOCALES}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("fault", "expected_code"),
    [
        ("faq", "news_faq"),
        ("topic", "news_topic_link"),
        ("sources", "news_sources"),
        ("punctuation", "news_punctuation"),
    ],
)
async def test_cover_only_news_still_requires_the_other_publication_checks(
    monkeypatch: pytest.MonkeyPatch,
    complete_news_documents: dict[Locale, GuideDocument],
    fault: str,
    expected_code: str,
) -> None:
    factory = await database()
    monkeypatch.setattr(assets, "storage", no_object_storage)
    async with factory() as session:
        candidate = await seed_candidate(session)
        rendered = await assets.ensure_assets(session, candidate, complete_news_documents)
    for locale, document in rendered.items():
        if fault == "punctuation" and locale not in {"zh-TW", "zh-CN", "ja"}:
            continue
        encoded = document.model_dump(mode="json")
        source_count = 1
        if fault == "faq":
            encoded["blocks"] = [block for block in encoded["blocks"] if block["type"] != "faq"]
        elif fault == "topic":
            encoded["blocks"] = [block for block in encoded["blocks"] if block["type"] != "link"]
        elif fault == "sources":
            encoded["sources"] = []
            source_count = 0
        else:
            encoded["title"] = "新聞:標題"
        damaged = GuideDocument.model_validate(encoded)
        problems = hard_policy_problems(damaged, "ai", locale, source_count=source_count)
        assert any(problem.startswith(f"{expected_code}:") for problem in problems), (
            locale,
            problems,
        )
        if fault == "sources":
            assert any(problem.startswith("no_sources:") for problem in problems)


@pytest.mark.asyncio
async def test_without_object_storage_images_live_in_the_row_and_are_served_from_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    factory = await database()
    monkeypatch.setattr(assets, "storage", no_object_storage)
    async with factory() as session:
        candidate = await seed_candidate(session)
        rendered = await assets.ensure_assets(session, candidate, documents())
        await session.commit()
        rows = list(await session.scalars(select(NewsAsset)))
        assert len(rows) == 2
        assert all(row.content for row in rows)
        hero = rendered["en"].hero
        assert hero is not None
        filename = hero.src.rsplit("/", 1)[-1]
        with pytest.raises(AppError):
            await assets.public_asset(session, filename)
        await assets.mark_assets_public(session, candidate.id)
        await session.commit()
        body, content_type, _ = await assets.public_asset(session, filename)
    assert content_type == "image/webp"
    assert body[:4] == b"RIFF"


@pytest.mark.asyncio
async def test_with_object_storage_images_go_to_s3_and_not_the_row(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    factory = await database()
    client = Mock()
    monkeypatch.setattr(assets, "storage", lambda: client)
    async with factory() as session:
        candidate = await seed_candidate(session)
        await assets.ensure_assets(session, candidate, documents())
        await session.commit()
        rows = list(await session.scalars(select(NewsAsset)))
    assert client.put_object.call_count == 2
    assert all(row.content is None for row in rows)


@pytest.mark.asyncio
async def test_retention_clears_row_images_without_needing_object_storage(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    factory = await database()
    monkeypatch.setattr(assets, "storage", no_object_storage)
    monkeypatch.setattr(jobs, "SessionFactory", factory)
    async with factory() as session:
        candidate = await seed_candidate(session)
        await assets.ensure_assets(session, candidate, documents())
        for row in await session.scalars(select(NewsAsset)):
            row.created_at = datetime.now(UTC) - timedelta(days=120)
        await session.commit()
        candidate_id = candidate.id
    result = await jobs.cleanup_retention()
    async with factory() as session:
        rows = list(
            await session.scalars(select(NewsAsset).where(NewsAsset.candidate_id == candidate_id))
        )
    assert result["deleted_assets"] == 2
    assert all(row.content is None and row.deleted_at is not None for row in rows)


@pytest.mark.asyncio
async def test_no_process_figure_and_an_old_one_is_dropped(monkeypatch: pytest.MonkeyPatch) -> None:
    """The fixed "editorial verification flow" figure named an internal tool and used the
    article title as alt text. New articles get no body figure, and a candidate processed
    again loses the one it already had, in the text and as a public asset."""
    factory = await database()
    monkeypatch.setattr(assets, "storage", no_object_storage)
    async with factory() as session:
        candidate = await seed_candidate(session)
        old = NewsAsset(
            candidate_id=candidate.id,
            variant="diagram",
            locale="en",
            storage_key=f"news/{candidate.id}/old-diagram-en.svg",
            public_filename="old-diagram-en.svg",
            content_type="image/svg+xml",
            sha256="c" * 64,
            size=5,
            width=1600,
            height=900,
            content=b"<svg/>",
            is_public=True,
        )
        session.add(old)
        await session.commit()
        drafted = documents()
        drafted["en"] = GuideDocument.model_validate(
            {
                "title": "Release en",
                "description": "What changed.",
                "blocks": [
                    {"type": "paragraph", "text": "Body."},
                    {
                        "type": "image",
                        "src": f"{assets.PUBLIC_PREFIX}/old-diagram-en.svg",
                        "alt": "Release en",
                        "width": 1600,
                        "height": 900,
                    },
                ],
                "sources": [],
            }
        )
        rendered = await assets.ensure_assets(session, candidate, drafted)
        await session.commit()
        for document in rendered.values():
            assert [block.type for block in document.blocks] == ["paragraph"]
        await session.refresh(old)
        assert old.deleted_at is not None and old.is_public is False
        with pytest.raises(AppError):
            await assets.public_asset(session, "old-diagram-en.svg")
