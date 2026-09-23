from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections.abc import Mapping
from datetime import UTC, date, datetime
from typing import Any

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
    "discovered": frozenset({"drafting", "manual_review", "duplicate", "failed"}),
    "drafting": frozenset({"verifying", "manual_review", "failed"}),
    "verifying": frozenset({"locale_review", "manual_review", "failed"}),
    "locale_review": frozenset({"jev_review", "manual_review", "failed"}),
    "jev_review": frozenset({"shadow_review", "manual_review", "published", "failed"}),
    "shadow_review": frozenset({"published", "rejected", "drafting"}),
    "manual_review": frozenset({"published", "rejected", "drafting"}),
    "failed": frozenset({"drafting", "rejected"}),
    "duplicate": frozenset({"rejected"}),
    "published": frozenset(),
    "rejected": frozenset(),
}


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


def document_fingerprint(document: GuideDocument) -> str:
    encoded = document.model_dump(mode="json")
    hero = encoded.get("hero")
    if isinstance(hero, dict) and str(hero.get("src", "")).startswith("/guides/news-assets/"):
        encoded["hero"] = None
    encoded["blocks"] = [
        block
        for block in encoded["blocks"]
        if not (
            isinstance(block, dict)
            and (
                (
                    block.get("type") == "image"
                    and str(block.get("src", "")).startswith("/guides/news-assets/")
                )
                or (
                    block.get("type") == "link"
                    and re.match(
                        r"^https://mokaair\.com/(?:en|ja|ko|zh-TW|zh-CN)/life/topics/"
                        r"(?:ai-news|tech-news|crypto)$",
                        str(block.get("url", "")),
                    )
                    is not None
                )
            )
        )
    ]
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
    if source_count < 2:
        problems.append("news_sources: at least two evidence sources are required")
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
