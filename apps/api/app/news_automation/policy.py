from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections.abc import Iterable, Mapping
from datetime import UTC, date, datetime
from typing import Any, Protocol
from urllib.parse import urlsplit

from app.guides.pack_ingest import lint_document
from app.guides.schemas import CalloutBlock, FaqBlock, GuideDocument, ImageBlock, SummaryBlock
from app.news_automation.schemas import GateView, Vertical
from app.site_pages.schemas import LinkBlock

CRYPTO_MARKERS: Mapping[str, str] = {
    "zh-TW": "不是投資建議",
    "zh-CN": "不是投资建议",
    "en": "not investment advice",
    "ja": "投資助言ではありません",
    "ko": "투자 조언이 아닙니다",
}
FORBIDDEN_CRYPTO = (
    "漲跌幅",
    "買進",
    "賣出",
    "price target",
    "buy signal",
    "sell signal",
    "entry point",
    "exit point",
)
FORBIDDEN_TECH = (
    "值得買",
    "該不該買",
    "buy now",
    "step-by-step exploit",
    "proof-of-concept exploit",
)
ALLOWED_TRANSITIONS: Mapping[str, frozenset[str]] = {
    "discovered": frozenset(
        {"drafting", "manual_review", "needs_evidence", "duplicate", "failed"}
    ),
    "drafting": frozenset({"verifying", "manual_review", "needs_redraft", "failed"}),
    "verifying": frozenset({"locale_review", "manual_review", "needs_redraft", "failed"}),
    "locale_review": frozenset({"jev_review", "manual_review", "needs_redraft", "failed"}),
    "jev_review": frozenset({"shadow_review", "manual_review", "published", "failed"}),
    "shadow_review": frozenset({"published", "rejected", "drafting"}),
    "manual_review": frozenset({"published", "rejected", "drafting"}),
    # A retry puts it back to discovered; nothing here can be published.
    "needs_evidence": frozenset({"discovered", "rejected"}),
    "needs_redraft": frozenset({"discovered", "rejected"}),
    "failed": frozenset({"drafting", "rejected"}),
    "duplicate": frozenset({"rejected"}),
    "published": frozenset(),
    "rejected": frozenset(),
}


# Manual-review holds that are steps of the workflow rather than problems: a verified
# Traditional Chinese draft waiting for the owner's decision, and a checked five-locale
# article (re-verified in the editor) waiting for the publish button.
ZH_DRAFT_READY = "news_zh_draft_ready"
READY_TO_PUBLISH = "news_ready_to_publish"
# The last two gates before publication (owner decision, 2026-09-25): the final editor found a
# problem it cannot fix without new evidence, or Jev's last call on the five locales was not
# "act" everywhere. The article is saved either way, so the owner can still publish it.
FINAL_EDIT_HOLD = "news_final_edit_hold"
JEV_FINAL_HOLD = "news_jev_final_hold"
# Set when an editor re-checks a candidate held for changed evidence against the current
# pages: the saved article is re-verified like an edited one, and then Jev makes the last
# call before anything is published.
EVIDENCE_REFRESH_MARKER = "news_evidence_refreshed"


class EvidenceLike(Protocol):
    role: str
    url: str
    is_first_party: bool


def evidence_site(url: str) -> str:
    """The website a page belongs to: its host, without a leading ``www.``."""
    host = (urlsplit(url).hostname or "").casefold().rstrip(".")
    return host.removeprefix("www.")


def evidence_site_count(rows: Iterable[EvidenceLike]) -> int:
    return len({evidence_site(row.url) for row in rows if row.role == "evidence"})


def evidence_present(rows: Iterable[EvidenceLike]) -> bool:
    """At least one evidence page, which is all a draft for the owner needs (owner
    decision, 2026-09-25): every enabled source is an official or trusted feed, and a
    person confirms each single-source article before it is translated and published."""
    return any(row.role == "evidence" for row in rows)


def evidence_sufficient(rows: Iterable[EvidenceLike]) -> bool:
    """Two evidence pages from two different websites, one of them first-party.

    Pages of one website are one source (owner decision, 2026-09-24): an announcement and
    its own related pages do not corroborate each other. Since 2026-09-25 this only
    guards automatic publication; a person may publish a single-source article.
    """
    usable = [row for row in rows if row.role == "evidence"]
    return evidence_site_count(usable) >= 2 and any(row.is_first_party for row in usable)


def auto_evidence_ok(rows: Iterable[EvidenceLike]) -> bool:
    """Enough evidence to publish without a person: two websites, or one first-party page.

    The owner decided on 2026-09-25 that an official announcement (the company's own site,
    blog or feed) may be published automatically on its own, reported as that company's
    statement; any other single website still waits for a person.
    """
    usable = [row for row in rows if row.role == "evidence"]
    return evidence_sufficient(usable) or any(row.is_first_party for row in usable)


def transition_allowed(current: str, target: str) -> bool:
    return target in ALLOWED_TRANSITIONS.get(current, frozenset())


def normalized_title(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"[\w\u3400-\u9fff\u3040-\u30ff\uac00-\ud7af]+", normalized))


def content_fingerprint(*parts: str) -> str:
    encoded = "\n".join(part.strip() for part in parts).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def evidence_fingerprint(rows: list[dict[str, Any]]) -> str:
    normalized = [
        {"url": row["url"], "content_hash": row["content_hash"]}
        for row in sorted(rows, key=lambda item: str(item["url"]))
    ]
    return hashlib.sha256(
        json.dumps(normalized, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


NEWS_ASSET_PREFIX = "/guides/news-assets/"
# The link to the vertical's topic hub the pipeline appends to each locale. Its URL names the
# locale, so it differs between locales on purpose.
TOPIC_LINK = re.compile(
    r"^https://mokaair\.com/(?:en|ja|ko|zh-TW|zh-CN)/life/topics/(?:ai-news|tech-news|crypto)$"
)


def is_topic_link(block: object) -> bool:
    return (
        isinstance(block, dict)
        and block.get("type") == "link"
        and TOPIC_LINK.match(str(block.get("url", ""))) is not None
    )


# The site's own non-investment-advice notice for crypto news, one per locale, each containing
# its CRYPTO_MARKERS phrase. The pipeline adds it where a model left none (on 2026-09-26 the
# writer and the translators omitted it in three locales), so no crypto story stops at the
# disclaimer check for something the site can write itself.
CRYPTO_DISCLAIMERS: Mapping[str, tuple[str, str]] = {
    "zh-TW": (
        "這篇是新聞整理，不是投資建議",
        "本文整理公開報導與官方資訊，不推薦任何代幣、平台或操作，不是投資建議。"
        "加密資產風險高，做任何決定前請自行查證並評估風險。",
    ),
    "zh-CN": (
        "这篇是新闻整理，不是投资建议",
        "本文整理公开报道与官方信息，不推荐任何代币、平台或操作，不是投资建议。"
        "加密资产风险高，做任何决定前请自行核实并评估风险。",
    ),
    "en": (
        "A news summary, not investment advice",
        "This article summarises public reporting and official information. It recommends no "
        "token, platform or action, and it is not investment advice. Crypto assets carry high "
        "risk; check the facts and weigh the risks yourself before any decision.",
    ),
    "ja": (
        "ニュースのまとめであり、投資助言ではありません",
        "本記事は公開された報道と公式情報をまとめたもので、特定のトークン、プラットフォーム、"
        "行動を勧めるものではなく、投資助言ではありません。暗号資産はリスクが高いため、"
        "判断の前にご自身で事実を確認し、リスクを検討してください。",
    ),
    "ko": (
        "뉴스 정리이며 투자 조언이 아닙니다",
        "이 글은 공개 보도와 공식 정보를 정리한 것으로, 특정 토큰·플랫폼·행동을 권하지 않으며 "
        "투자 조언이 아닙니다. 암호화폐는 위험이 크니 결정하기 전에 직접 사실을 확인하고 "
        "위험을 판단하세요.",
    ),
}
_DISCLAIMER_TEXTS = frozenset(text for _title, text in CRYPTO_DISCLAIMERS.values())


def is_site_disclaimer(block: object) -> bool:
    return (
        isinstance(block, dict)
        and block.get("type") == "callout"
        and block.get("text") in _DISCLAIMER_TEXTS
    )


def with_crypto_disclaimer(document: GuideDocument, vertical: str, locale: str) -> GuideDocument:
    """A crypto story with a disclaimer callout the hard checks accept, added if it has none."""
    if vertical != "crypto":
        return document
    marker = CRYPTO_MARKERS[locale].casefold()
    if any(
        isinstance(block, CalloutBlock) and marker in block.text.casefold()
        for block in document.blocks
    ):
        return document
    title, text = CRYPTO_DISCLAIMERS[locale]
    encoded = document.model_dump(mode="json")
    notice = {"type": "callout", "tone": "info", "title": title, "text": text}
    # Before the topic link, which stays last.
    position = next(
        (index for index, block in enumerate(encoded["blocks"]) if is_topic_link(block)),
        len(encoded["blocks"]),
    )
    encoded["blocks"].insert(position, notice)
    return GuideDocument.model_validate(encoded)


def is_site_asset(block: object) -> bool:
    """An image the pipeline drew for the story (``ensure_assets``), not one a model wrote."""
    return (
        isinstance(block, dict)
        and block.get("type") == "image"
        and str(block.get("src", "")).startswith(NEWS_ASSET_PREFIX)
    )


def _without_site_additions(document: GuideDocument) -> dict[str, Any]:
    encoded = document.model_dump(mode="json")
    hero = encoded.get("hero")
    if isinstance(hero, dict) and str(hero.get("src", "")).startswith(NEWS_ASSET_PREFIX):
        encoded["hero"] = None
    encoded["blocks"] = [
        block
        for block in encoded["blocks"]
        if not (is_topic_link(block) or is_site_asset(block))
    ]
    return encoded


def site_additions_removed(document: GuideDocument) -> GuideDocument:
    """The article as the models wrote it: no topic link, and no artwork the pipeline drew.

    Stage two adds both after every model step. A rerun starts from a zh-TW text that already
    carries them, and a reviewer comparing it with a fresh translation (told to add no image)
    held the translation for a "missing" hero and diagram on 2026-09-26.
    """
    return GuideDocument.model_validate(_without_site_additions(document))


def for_review(document: GuideDocument) -> dict[str, Any]:
    """The document as a reviewing model sees it, without anything the pipeline adds.

    The topic link names the locale in its URL, so a reviewer comparing a translation with
    the zh-TW source reported it as a mismatch and held the article (2026-09-26).
    """
    return _without_site_additions(document)


def document_fingerprint(document: GuideDocument) -> str:
    encoded = _without_site_additions(document)
    # The site's own notice, so adding it where a model left none keeps a verification of the
    # text valid.
    encoded["blocks"] = [block for block in encoded["blocks"] if not is_site_disclaimer(block)]
    return hashlib.sha256(
        json.dumps(
            encoded,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def event_date_problems(
    event_date: date,
    slug: str,
    evidence_dates: list[date],
    *,
    today: date | None = None,
) -> list[str]:
    problems: list[str] = []
    current = today or datetime.now(UTC).date()
    if event_date > current:
        problems.append("event_date_future")
    if evidence_dates and event_date > max(evidence_dates):
        problems.append("event_date_after_evidence")
    if not slug.endswith(event_date.strftime("%Y%m%d")):
        problems.append("event_date_slug_mismatch")
    return problems


def _visible_text(document: GuideDocument) -> str:
    return json.dumps(document.model_dump(mode="json"), ensure_ascii=False).casefold()


def hard_policy_problems(
    document: GuideDocument, vertical: Vertical, locale: str, *, source_count: int
) -> list[str]:
    topics: list[str] = {
        "ai": ["ai", "ai-news"],
        "tech": ["tech", "tech-news"],
        "crypto": ["finance", "crypto"],
    }[vertical]
    problems = [
        f"{problem.code}: {problem.message}"
        for problem in lint_document(document, "life", topics=topics)
        if problem.level == "error"
    ]
    if not any(isinstance(block, SummaryBlock) for block in document.blocks):
        problems.append("news_summary: a summary block is required")
    if not any(isinstance(block, FaqBlock) for block in document.blocks):
        problems.append("news_faq: an FAQ block is required")
    if not any(
        isinstance(block, ImageBlock)
        and block.src.startswith("/guides/news-assets/")
        and block.src.endswith(".svg")
        for block in document.blocks
    ):
        problems.append("news_diagram: an original SVG diagram is required")
    topic = {"ai": "ai-news", "tech": "tech-news", "crypto": "crypto"}[vertical]
    topic_url = f"https://mokaair.com/{locale}/life/topics/{topic}"
    if not any(
        isinstance(block, LinkBlock) and block.url == topic_url for block in document.blocks
    ):
        problems.append("news_topic_link: the localized dynamic topic link is required")
    if source_count < 1:
        problems.append("news_sources: evidence from at least one website is required")
    text = _visible_text(document)
    if vertical == "crypto":
        marker = CRYPTO_MARKERS[locale].casefold()
        if marker not in text:
            problems.append(f"crypto_disclaimer: missing {CRYPTO_MARKERS[locale]}")
        if any(term.casefold() in text for term in FORBIDDEN_CRYPTO):
            problems.append("crypto_recommendation: price or trading language is not allowed")
        disclaimer_blocks = [
            block
            for block in document.blocks
            if isinstance(block, CalloutBlock) and marker in block.text.casefold()
        ]
        if not disclaimer_blocks:
            problems.append("crypto_disclaimer_block: disclaimer must be a callout")
    if vertical == "tech" and any(term.casefold() in text for term in FORBIDDEN_TECH):
        problems.append("tech_recommendation: buying or actionable exploit advice is not allowed")
    return problems


def gate_result(
    vertical: Vertical,
    *,
    started_at: datetime,
    labelled: int,
    agreements: int,
    serious_false_positives: int,
    min_days: int,
    min_candidates: int,
    min_agreement: float,
    now: datetime | None = None,
) -> GateView:
    current = now or datetime.now(UTC)
    if started_at.tzinfo is None:
        started_at = started_at.replace(tzinfo=UTC)
    days = max(0, int((current - started_at).total_seconds() // 86_400))
    rate = agreements / labelled if labelled else 0.0
    reasons: list[str] = []
    if days < min_days:
        reasons.append(f"shadow_days:{days}/{min_days}")
    if labelled < min_candidates:
        reasons.append(f"labelled_candidates:{labelled}/{min_candidates}")
    if rate < min_agreement:
        reasons.append(f"agreement_rate:{rate:.3f}/{min_agreement:.3f}")
    if serious_false_positives:
        reasons.append(f"serious_false_positives:{serious_false_positives}")
    return GateView(
        vertical=vertical,
        days=days,
        labelled_candidates=labelled,
        agreements=agreements,
        agreement_rate=rate,
        serious_false_positives=serious_false_positives,
        eligible=not reasons,
        reasons=reasons,
    )
