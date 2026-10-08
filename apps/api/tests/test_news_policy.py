from __future__ import annotations

from typing import Any

import pytest

from app.guides.schemas import CalloutBlock, GuideDocument
from app.news_automation.policy import (
    CRYPTO_DISCLAIMERS,
    CRYPTO_MARKERS,
    document_fingerprint,
    hard_policy_problems,
    is_site_disclaimer,
    with_crypto_disclaimer,
)

# Snapshots of the notice bodies attached to articles before the source-neutral notice.
# A wording change must not bring these site additions into old verification hashes.
LEGACY_NOTICES = {
    "zh-TW": (
        "本文整理公開報導與官方資訊，不推薦任何代幣、平台或操作，不是投資建議。"
        "加密資產風險高，做任何決定前請自行查證並評估風險。"
    ),
    "zh-CN": (
        "本文整理公开报道与官方信息，不推荐任何代币、平台或操作，不是投资建议。"
        "加密资产风险高，做任何决定前请自行核实并评估风险。"
    ),
    "en": (
        "This article summarises public reporting and official information. It recommends no "
        "token, platform or action, and it is not investment advice. Crypto assets carry high "
        "risk; check the facts and weigh the risks yourself before any decision."
    ),
    "ja": (
        "本記事は公開された報道と公式情報をまとめたもので、特定のトークン、プラットフォーム、"
        "行動を勧めるものではなく、投資助言ではありません。暗号資産はリスクが高いため、"
        "判断の前にご自身で事実を確認し、リスクを検討してください。"
    ),
    "ko": (
        "이 글은 공개 보도와 공식 정보를 정리한 것으로, 특정 토큰·플랫폼·행동을 권하지 않으며 "
        "투자 조언이 아닙니다. 암호화폐는 위험이 크니 결정하기 전에 직접 사실을 확인하고 "
        "위험을 판단하세요."
    ),
}


def document(locale: str, *blocks: dict[str, Any]) -> GuideDocument:
    return GuideDocument.model_validate({
        "title": "News report",
        "description": "What happened.",
        "blocks": [
            {"type": "paragraph", "text": "The attributed report."},
            *blocks,
            {
                "type": "link",
                "text": "More news",
                "url": f"https://mokaair.com/{locale}/life/topics/crypto",
            },
        ],
    })


def disclaimer_problems(item: GuideDocument, locale: str) -> list[str]:
    return [
        problem
        for problem in hard_policy_problems(item, "crypto", locale, source_count=1)
        if problem.startswith(("finance_no_disclaimer", "crypto_disclaimer"))
    ]


@pytest.mark.parametrize("locale", list(CRYPTO_MARKERS))
@pytest.mark.parametrize("field", ["title", "text"])
def test_explicit_warning_in_either_callout_field_does_not_create_a_second_notice(
    locale: str, field: str,
) -> None:
    block = {"type": "callout", "title": "Notice", "text": "Reader notice."}
    block[field] = CRYPTO_MARKERS[locale]
    original = document(locale, block)
    before = original.model_dump(mode="json")

    # The news policy and generic finance lint agree even on an existing title-only warning.
    assert disclaimer_problems(original, locale) == []
    noticed = with_crypto_disclaimer(original, "crypto", locale)
    callouts = [block for block in noticed.blocks if isinstance(block, CalloutBlock)]
    assert len(callouts) == 1
    assert callouts[0].title == before["blocks"][1]["title"]
    assert CRYPTO_MARKERS[locale] in callouts[0].text
    assert noticed.blocks[-1] == original.blocks[-1]
    assert disclaimer_problems(noticed, locale) == []
    assert with_crypto_disclaimer(noticed, "crypto", locale) == noticed
    assert original.model_dump(mode="json") == before


@pytest.mark.parametrize("locale,title,text", [
    (
        "ja", "本記事はニュースの整理であり、投資助言ではありません",
        "本記事は Decrypt の報道を整理したもので、投資助言でもありません。",
    ),
    (
        "ja", "これはニュースの整理であり、投資助言ではありません",
        "本記事は CoinDesk の報道内容を整理したもので、投資助言ではない。",
    ),
    (
        "ko", "이 글은 뉴스 정리이며 투자 조언이 아니다",
        "이 글은 CoinDesk 보도를 정리한 것으로 투자 조언이 아니다.",
    ),
    ("ko", "중요 안내", "이 글은 투자 조언이 아님."),
    ("ko", "투자 조언 아님", "이 글은 기술 소식을 전한다."),
])
def test_reported_japanese_and_korean_endings_survive_the_correction_round(
    locale: str, title: str, text: str,
) -> None:
    # A reviewer removed the site's extra notice and returned this legitimate translated
    # callout. Previously the exact-body test would attach that extra notice again.
    corrected = document(locale, {"type": "callout", "title": title, "text": text})
    original_hash = document_fingerprint(corrected)
    assert disclaimer_problems(corrected, locale) == []

    normalized = with_crypto_disclaimer(corrected, "crypto", locale)
    callouts = [block for block in normalized.blocks if isinstance(block, CalloutBlock)]
    assert len(callouts) == 1
    assert callouts[0].title == title
    assert CRYPTO_MARKERS[locale] in callouts[0].text
    assert disclaimer_problems(normalized, locale) == []
    assert with_crypto_disclaimer(normalized, "crypto", locale) == normalized
    # Normalizing model-authored wording requires a new review hash; it is not silently
    # treated as a site addition or rebound to an old passing assessment.
    assert document_fingerprint(normalized) != original_hash
    assert document_fingerprint(corrected) == original_hash


@pytest.mark.parametrize("locale", list(CRYPTO_MARKERS))
def test_missing_warning_gets_one_source_neutral_notice_before_the_topic_link(locale: str) -> None:
    bare = document(locale)
    noticed = with_crypto_disclaimer(bare, "crypto", locale)
    callouts = [block for block in noticed.blocks if isinstance(block, CalloutBlock)]
    assert len(callouts) == 1
    assert noticed.blocks[-1] == bare.blocks[-1]
    assert CRYPTO_MARKERS[locale] in callouts[0].text
    assert disclaimer_problems(noticed, locale) == []
    assert with_crypto_disclaimer(noticed, "crypto", locale) == noticed
    assert document_fingerprint(noticed) == document_fingerprint(bare)
    assert all(
        term not in callouts[0].text.casefold()
        for term in ("官方", "official", "公式情報", "공식 정보")
    )


@pytest.mark.parametrize("locale,text", list(LEGACY_NOTICES.items()))
def test_historical_site_notices_keep_their_existing_hash_exclusion(
    locale: str, text: str,
) -> None:
    bare = document(locale)
    old_block = {"type": "callout", "title": CRYPTO_DISCLAIMERS[locale][0], "text": text}
    old_notice = document(locale, old_block)
    assert is_site_disclaimer(old_block)
    assert document_fingerprint(old_notice) == document_fingerprint(bare)
    assert with_crypto_disclaimer(old_notice, "crypto", locale) == old_notice

    # A similar authored warning must stay in the hash so evidence-bound reviews notice edits.
    authored_block = {**old_block, "text": text + " Additional reader context."}
    assert not is_site_disclaimer(authored_block)
    assert document_fingerprint(document(locale, authored_block)) != document_fingerprint(bare)
    changed_body = document(locale, old_block).model_dump(mode="json")
    changed_body["blocks"][0]["text"] = "A changed material claim."
    assert document_fingerprint(GuideDocument.model_validate(changed_body)) != (
        document_fingerprint(old_notice)
    )


@pytest.mark.parametrize("locale,text", [
    ("en", "Crypto assets have risks."),
    ("ja", "暗号資産にはリスクがある。"),
    ("ko", "암호화폐에는 위험이 있습니다."),
])
def test_general_risk_warnings_are_not_inferred_to_be_investment_disclaimers(
    locale: str, text: str,
) -> None:
    original = document(locale, {"type": "callout", "title": "Risk", "text": text})
    assert disclaimer_problems(original, locale)
    noticed = with_crypto_disclaimer(original, "crypto", locale)
    assert len([block for block in noticed.blocks if isinstance(block, CalloutBlock)]) == 2
    assert noticed.blocks[1] == original.blocks[1]
    assert disclaimer_problems(noticed, locale) == []


def test_a_warning_in_plain_prose_does_not_satisfy_the_required_callout() -> None:
    original = document("en", {"type": "paragraph", "text": "This is not investment advice."})
    assert "crypto_disclaimer_block: disclaimer must be a callout" in (
        disclaimer_problems(original, "en")
    )
    noticed = with_crypto_disclaimer(original, "crypto", "en")
    assert len([block for block in noticed.blocks if isinstance(block, CalloutBlock)]) == 1
    assert disclaimer_problems(noticed, "en") == []


def test_a_full_callout_is_held_without_truncating_it_or_creating_a_duplicate() -> None:
    original = document("ja", {
        "type": "callout", "title": "投資助言ではありません", "text": "本文" * 1000,
    })
    noticed = with_crypto_disclaimer(original, "crypto", "ja")
    assert noticed == original
    assert len([block for block in noticed.blocks if isinstance(block, CalloutBlock)]) == 1
    assert any(
        problem.startswith("finance_no_disclaimer")
        for problem in disclaimer_problems(noticed, "ja")
    )


@pytest.mark.parametrize("vertical", ["ai", "tech"])
def test_non_crypto_content_is_not_changed(vertical: str) -> None:
    original = document("ja", {
        "type": "callout", "title": "投資助言ではありません", "text": "投資助言でもありません。",
    })
    assert with_crypto_disclaimer(original, vertical, "ja") is original
