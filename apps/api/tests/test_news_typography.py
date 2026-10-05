from __future__ import annotations

from copy import deepcopy
from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest
from pydantic import ValidationError
from sqlalchemy import select

from app.config import get_settings
from app.guides.schemas import GuideDocument
from app.news_automation import ai, pipeline
from app.news_automation.models import NewsAssessment, NewsAutomationSettings, NewsCandidate
from app.news_automation.policy import document_fingerprint, hard_policy_problems
from app.news_automation.schemas import (
    EditorialDraft,
    LocaleReviewResult,
    LocalizedDocument,
    VerificationResult,
)
from app.news_automation.typography import normalize_generated_document
from tests.test_news_pipeline import (
    database,
    seed_single_source_candidate,
    stage_one_mocks,
    stage_two_mocks,
)


def document(**changes: Any) -> GuideDocument:
    return GuideDocument.model_validate({
        "title": "A news report",
        "description": "A report description.",
        "blocks": [{"type": "paragraph", "text": "Body text."}],
        **changes,
    })


def punctuation_problems(item: GuideDocument, locale: str = "zh-TW") -> list[str]:
    return [
        problem for problem in hard_policy_problems(item, "ai", locale, source_count=1)
        if problem.startswith("news_punctuation:")
    ]


@pytest.mark.parametrize("model", [
    EditorialDraft, VerificationResult, LocalizedDocument, LocaleReviewResult,
])
def test_each_generated_reply_fixes_punctuation_before_its_review_fingerprint(
    model: type[EditorialDraft | VerificationResult | LocalizedDocument | LocaleReviewResult],
) -> None:
    original = document(
        title="模型,發布", description="新聞:說明",
        blocks=[{"type": "paragraph", "text": "這裡;保留"}],
    )
    before = original.model_dump(mode="json")
    old_fingerprint = document_fingerprint(original)
    assert len(punctuation_problems(original)) == 3
    field = "document" if model in {EditorialDraft, LocalizedDocument} else "corrected_document"
    payload: dict[str, Any] = {field: before}
    if model is EditorialDraft:
        payload.update(
            eligible=True, exclusion_reason="", vertical="ai", event_date="2026-10-05",
            slug="ai-news-model-release-20261005", topics=["ai-news"],
            claims=[{"claim": "模型發布", "source_urls": ["https://example.test/release"]}],
        )
    elif model in {VerificationResult, LocaleReviewResult}:
        payload.update(verdict="revise", issues=["Typesetting corrected."])
    reply = model.model_validate(payload)
    normalized = getattr(reply, field)
    assert normalized.title == "模型，發布"
    assert normalized.description == "新聞：說明"
    assert normalized.blocks[0].text == "這裡；保留"
    assert punctuation_problems(normalized) == []
    assert document_fingerprint(normalized) != old_fingerprint
    assert original.model_dump(mode="json") == before
    assert document_fingerprint(original) == old_fingerprint
    # Direct GuideDocument parsing, used by saved articles and human edits, keeps the
    # old text and its old hash; no prior review is rebound by this provider-only rule.
    assert GuideDocument.model_validate(before).title == "模型,發布"
    assert document_fingerprint(GuideDocument.model_validate(before)) == old_fingerprint


@pytest.mark.parametrize("mark,full_width", tuple(zip(",:;?!()", "，：；？！（）", strict=True)))
@pytest.mark.parametrize("text", ["更新{mark}Latin", "Latin{mark}更新"])
def test_every_reported_ascii_mark_and_both_cjk_neighbors(
    mark: str, full_width: str, text: str,
) -> None:
    source = document(title=text.format(mark=mark))
    result = normalize_generated_document(source)
    assert result.title == text.format(mark=full_width)
    assert len(result.title) == len(source.title)
    assert punctuation_problems(result) == []


@pytest.mark.parametrize("text,expected", [
    ("かな?カナ", "かな？カナ"),
    ("漢字,説明", "漢字，説明"),
    ("〇:々", "〇：々"),
    ("𠀀!更新", "𠀀！更新"),
])
def test_generated_japanese_and_supplementary_han_use_cjk_typography(
    text: str, expected: str,
) -> None:
    result = normalize_generated_document(document(title=text))
    assert result.title == expected
    assert punctuation_problems(result, "ja") == []


@pytest.mark.parametrize("block", [
    {"type": "heading", "level": 2, "text": "更新:內容"},
    {"type": "paragraph", "text": "更新:內容"},
    {"type": "list", "items": ["更新:內容"]},
    {"type": "summary", "items": ["更新:內容", "第二項。"]},
    {"type": "table", "header": ["更新:內容"], "rows": [["值:內容"]],
     "caption": "表格:說明"},
    {"type": "callout", "title": "更新:內容", "text": "內容!說明"},
    {"type": "faq", "items": [
        {"question": "問題?", "answer": "答案:說明"},
        {"question": "另一個問題？", "answer": "另一個答案。"},
    ]},
    {"type": "image", "src": "/guides/news-assets/example.svg", "alt": "圖片:內容",
     "caption": "圖片:說明", "description": "圖表:說明", "width": 800, "height": 600},
    {"type": "link", "text": "更新:內容", "url": "https://example.test/中文:連結"},
    {"type": "partner_link", "partner": "example", "url": "https://example.test/中文:連結",
     "label": "更新:內容", "note": "內容:說明"},
    {"type": "offer", "module": "flight", "heading": "更新:內容"},
    {"type": "code", "label": "範例:說明", "code": "函式(參數); // 中文,註解!"},
])
def test_nested_reader_fields_pass_the_actual_punctuation_policy_without_losing_blocks(
    block: dict[str, Any],
) -> None:
    source = document(blocks=[block])
    before = source.model_dump(mode="json")
    assert punctuation_problems(source)
    result = normalize_generated_document(source)
    assert punctuation_problems(result) == []
    assert len(result.blocks) == len(source.blocks)
    assert result.blocks[0].type == source.blocks[0].type
    assert source.model_dump(mode="json") == before
    assert normalize_generated_document(result) == result


@pytest.mark.parametrize("inlines,expected", [
    ([{"type": "text", "text": "更新"}, {"type": "text", "text": ":details"}],
     ["更新", "：details"]),
    ([{"type": "link", "text": "Update:", "url": "https://example.test/中文:連結"},
      {"type": "text", "text": "更新"}], ["Update：", "更新"]),
    ([{"type": "article", "text": "更新", "slug": "other-article"},
      {"type": "text", "text": "?"}], ["更新", "？"]),
    ([{"type": "text", "text": "https://example.test/"},
      {"type": "link", "text": ",其餘另議。", "url": "https://example.test/next"}],
     ["https://example.test/", "，其餘另議。"]),
    ([{"type": "link", "text": "https://example.test/", "url": "https://example.test/"},
      {"type": "text", "text": ",其餘另議。"}], ["https://example.test/", "，其餘另議。"]),
])
def test_rich_inline_boundaries_are_fixed_in_the_original_nodes(
    inlines: list[dict[str, Any]], expected: list[str],
) -> None:
    source = document(blocks=[{"type": "rich_paragraph", "inlines": inlines}])
    result = normalize_generated_document(source)
    output = result.model_dump(mode="json")["blocks"][0]["inlines"]
    assert [node["text"] for node in output] == expected
    assert len(output) == len(inlines)
    assert [{key: value for key, value in node.items() if key != "text"} for node in output] == [
        {key: value for key, value in node.items() if key != "text"}
        for node in source.model_dump(mode="json")["blocks"][0]["inlines"]
    ]
    assert punctuation_problems(result) == []


def test_urls_code_source_metadata_and_latin_numeric_runs_remain_byte_identical() -> None:
    credit = {"author": "攝影:本人", "license": "授權:原文",
              "source_url": "https://example.test/中文?查詢=更新"}
    source = document(
        title="50.1% at 17:35, ACME, Inc. (US): APIs; ready? Yes!",
        description="持股50.1%，時間17:35，英文 ACME, Inc. (US): ready? Yes! "
                    "網址 https://example.test/中文:路徑?q=內容,其他!",
        hero={"src": "/guides/news-assets/example.png", "alt": "主圖",
              "width": 1200, "height": 630, "credit": credit},
        sources=[{"title": "來源:原文", "url": "https://example.test/中文?查詢=更新"}],
        blocks=[
            {"type": "code", "label": "範例", "code": "函式(參數); // 中文,註解!"},
            {"type": "rich_paragraph", "inlines": [
                {"type": "text", "text": "更新"},
                {"type": "code", "text": "函式(參數)"},
                {"type": "text", "text": ": Latin"},
            ]},
            {"type": "rich_paragraph", "inlines": [
                {"type": "text", "text": "網址 https://example.test/?q="},
                {"type": "text", "text": "中文:說明,內容!"},
            ]},
            {"type": "rich_paragraph", "inlines": [
                {"type": "link", "text": "https://example.test/中文:路徑?q=更新,內容",
                 "url": "https://example.test/中文:路徑?q=更新,內容"},
            ]},
            {"type": "paragraph", "text": "https://example.test/?q=說明（中文?）"},
            {"type": "image", "src": "/guides/news-assets/example.svg", "alt": "圖表",
             "width": 800, "height": 600, "credit": credit},
        ],
    )
    before = source.model_dump(mode="json")
    assert normalize_generated_document(source).model_dump(mode="json") == before


def test_typography_does_not_hide_other_policy_errors_or_invalid_provider_shapes() -> None:
    source = document(title="更新:內容")
    before = hard_policy_problems(source, "ai", "zh-TW", source_count=0)
    after = hard_policy_problems(normalize_generated_document(source), "ai", "zh-TW",
                                 source_count=0)
    assert after == [problem for problem in before if not problem.startswith("news_punctuation:")]
    invalid = deepcopy(source.model_dump(mode="json"))
    invalid["blocks"] = [{"type": "heading", "level": 2, "text": "更新:" * 100}]
    with pytest.raises(ValidationError):
        LocalizedDocument.model_validate({"document": invalid})
    with pytest.raises(ValidationError, match="revise requires"):
        VerificationResult.model_validate({"verdict": "revise", "corrected_document": None})
    assert VerificationResult(verdict="pass").corrected_document is None
    assert LocaleReviewResult(verdict="manual").corrected_document is None


@pytest.mark.asyncio
async def test_pipeline_reviews_and_hashes_the_normalized_provider_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    try:
        async with factory() as session:
            candidate = await seed_single_source_candidate(session)
            settings = await session.get(NewsAutomationSettings, 1)
            assert settings is not None
            settings.mode, settings.auto_publish_ai = "automatic", True
            await session.commit()
            candidate_id = candidate.id
        monkeypatch.setattr(
            ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, [])),
        )
        mocks = stage_one_mocks(monkeypatch)
        stage_two_mocks(monkeypatch)
        draft, usage, model = mocks["draft"].return_value
        encoded = draft.model_dump(mode="json")
        encoded["document"]["title"] = "模型,發布"
        mocks["draft"].return_value = EditorialDraft.model_validate(encoded), usage, model

        async def translate(*_args: Any) -> tuple[LocalizedDocument, dict[str, int], str]:
            return LocalizedDocument.model_validate({
                "document": document(title="翻譯:內容").model_dump(mode="json"),
            }), {}, "writer"

        monkeypatch.setattr(ai, "translate_article", translate)
        async with factory() as session:
            assert await pipeline.process_candidate(
                session, Mock(), get_settings(), candidate_id,
            ) == "published"
            stored = await session.get(NewsCandidate, candidate_id)
            assert stored is not None
            saved = {
                locale: GuideDocument.model_validate(value)
                for locale, value in stored.draft_bundle_json.items()
            }
            assessments = list(await session.scalars(select(NewsAssessment).where(
                NewsAssessment.candidate_id == candidate_id,
            )))
        assert saved["zh-TW"].title == "模型，發布"
        assert all(saved[locale].title == "翻譯：內容" for locale in ("zh-CN", "en", "ja", "ko"))
        final_reviews = {
            row.locale: row for row in assessments
            if row.assessment_type == "locale_review"
            and row.details_json.get("stage") == "final_edit"
        }
        assert set(final_reviews) == set(saved)
        for locale, item in saved.items():
            assert punctuation_problems(item, locale) == []
            reviewed_hash = final_reviews[locale].details_json["document_sha256"]
            assert reviewed_hash == document_fingerprint(item)
        assert any(
            row.assessment_type == "verification" and row.verdict == "pass"
            and row.details_json.get("document_sha256") == document_fingerprint(saved["zh-TW"])
            for row in assessments
        )
    finally:
        await engine.dispose()
