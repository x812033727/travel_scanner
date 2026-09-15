"""Propose two-level topics for the lifestyle packs, from their slugs and series membership.

818 lifestyle packs carry the flat vocabulary 0074 seeded -- ``ai`` on 529 of them,
``tutorial`` on 659 -- and 0076 gave that vocabulary a second level. Nobody is going to
re-file 818 articles by hand, and the importer must not guess. This module is the middle
ground: a rule table an editor can read, a dry run that prints what every rule would do,
and an ``apply`` that rewrites nothing but the ``topics`` array of the packs it names.

    uv run python -m app.guides.pack_cli retopic --kind life --dry-run
    uv run python -m app.guides.pack_cli retopic --kind life --prefix ai-term- --apply

The rules only ever add a sub-topic (and its parent when the parent is new), and drop
``misc`` once an article has a real subject. They never remove ``finance``, never touch a
travel article, and never propose a slug outside the lifestyle vocabulary. Getting the
result into the database is the existing ``guides-import``: a changed ``topics`` array is
a taxonomy-only update there, which is idempotent and leaves the published text alone.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from app.guides.content_pack import ArticlePack, default_directory, load_packs
from app.guides.schemas import Kind
from app.guides.taxonomy import LIFE_SEED_SUBTOPICS, LIFE_SEED_TOPICS

SUBTOPIC_PARENT: dict[str, str] = {slug: parent for slug, parent, _ in LIFE_SEED_SUBTOPICS}
LIFE_VOCABULARY: frozenset[str] = frozenset(
    {slug for slug, _ in LIFE_SEED_TOPICS} | set(SUBTOPIC_PARENT)
)
# A sub-topic makes ``misc`` redundant; a parent that is only there because a child needs
# it is added, never removed. Nothing else in the existing list is touched.
DROP_WHEN_FILED = frozenset({"misc"})


@dataclass(frozen=True)
class Rule:
    """One way a slug earns a sub-topic. The first matching prefix wins for a rule, but an
    article may match several rules and carry several sub-topics."""

    subtopic: str
    prefixes: tuple[str, ...] = ()
    slugs: frozenset[str] = frozenset()
    exclude_prefixes: tuple[str, ...] = ()

    def matches(self, slug: str) -> bool:
        if slug in self.slugs:
            return True
        if any(slug.startswith(prefix) for prefix in self.exclude_prefixes):
            return False
        return any(slug.startswith(prefix) for prefix in self.prefixes)


RULES: tuple[Rule, ...] = (
    Rule(
        "ai-terms",
        prefixes=("ai-term-",),
        slugs=frozenset(
            {
                "ai-glossary-50-terms",
                "ai-terms-index",
                "what-is-a-large-language-model",
                "ai-benchmarks-explained",
                "ai-open-vs-closed-models",
            }
        ),
    ),
    Rule(
        "ai-news",
        prefixes=("ai-news-",),
        slugs=frozenset({"ai-model-release-timeline-2026", "ai-hype-vs-reality-2026"}),
    ),
    Rule(
        "ai-search",
        prefixes=("ai-search-", "google-ai-overviews-", "google-ai-mode-", "zero-click-"),
        slugs=frozenset(
            {"ai-site-search-design", "llms-txt-evaluation", "perplexity-ai-search-guide"}
        ),
    ),
    Rule(
        "ai-chat",
        prefixes=(
            "chatgpt-",
            "claude-",
            "gemini-",
            "deepseek-",
            "minimax-",
            "qwen-",
            "doubao-",
            "kimi-",
            "grok-",
            "mistral-",
            "meta-ai-",
            "notebooklm-",
            "apple-intelligence-",
            "microsoft-copilot-",
            "chinese-ai-models-",
            "line-ai-",
            "ai-chat-prompt-",
        ),
        exclude_prefixes=(
            "claude-code-",
            "claude-api-",
            "claude-mcp-",
            "claude-plans-",
            "claude-memory-",
            "gemini-cli-",
            "gemini-api-",
            "gemini-image-",
            "gemini-plans-",
            "deepseek-local-",
            "deepseek-privacy-",
            "minimax-hailuo-",
            "minimax-music-",
            "minimax-speech-",
            "qwen-local-",
        ),
    ),
    Rule("claude-code", prefixes=("claude-code-",)),
    Rule("codex", prefixes=("codex-",)),
    Rule(
        "gemini-dev",
        prefixes=("gemini-cli-", "gemini-api-"),
    ),
    Rule(
        "ai-coding",
        prefixes=(
            "ai-coding-",
            "ai-code-",
            "cursor-",
            "github-copilot-",
            "ollama-",
            "local-ai-",
            "local-llm-",
            "local-rag-",
            "lm-studio-",
            "open-webui-",
            "gguf-",
            "self-host-ai-",
            "deploy-ai-built-",
            "vibe-coding-",
            "lovable-",
            "huggingface-",
            "gemma-",
            "gpt-oss-",
            "llama-",
            "mcp-servers-",
            "claude-api-",
            "claude-mcp-",
            "deepseek-local-",
            "qwen-local-",
            "ai-agent-frameworks-",
            "agent-service-",
        ),
        exclude_prefixes=("ai-coding-cost-",),
        slugs=frozenset(
            {
                "whisper-local-transcription",
                "transcription-desktop-tools",
                "ai-taiwan-local-models-taide",
            }
        ),
    ),
    Rule(
        "ai-create",
        prefixes=(
            "ai-image-",
            "ai-video-",
            "ai-art-",
            "ai-avatar-",
            "ai-voice-",
            "ai-3d-",
            "ai-photo-",
            "ai-remove-background-",
            "ai-product-photo-",
            "ai-design-prompt-",
            "midjourney-",
            "stable-diffusion-",
            "nano-banana-",
            "sora-",
            "veo-",
            "kling-",
            "suno-",
            "adobe-podcast-",
            "canva-ai-",
            "google-flow-",
            "gemini-image-",
            "minimax-hailuo-",
            "minimax-music-",
            "minimax-speech-",
            "figma-ai-",
        ),
        exclude_prefixes=("ai-image-copyright-", "ai-image-watermark-"),
    ),
    Rule(
        "ai-work",
        prefixes=(
            "ai-for-",
            "ai-meeting-",
            "ai-email-",
            "ai-slides-",
            "ai-spreadsheet-",
            "ai-calendar-",
            "ai-note-taking-",
            "ai-second-brain-",
            "ai-weekly-review-",
            "ai-prompt-library-",
            "ai-customer-service-",
            "ai-build-",
            "ai-tools-",
            "ai-pdf-",
            "ai-at-work-",
            "ai-reading-list-",
            "n8n-",
            "zapier-",
            "notion-ai-",
            "google-workspace-ai-",
            "immersive-translate-",
            "ai-browsers-",
            "social-chatbot-",
        ),
        slugs=frozenset({"ai-hallucination-fact-check"}),
    ),
    Rule(
        "ai-safety",
        prefixes=(
            "ai-account-security-",
            "ai-privacy-",
            "ai-prompt-injection-",
            "ai-scams-",
            "ai-and-copyright-",
            "ai-image-copyright-",
            "ai-image-watermark-",
            "ai-regulation-",
            "ai-detection-tools-",
            "ai-chat-history-",
            "chinese-ai-apps-security-",
            "deepseek-privacy-",
            "claude-memory-",
            "ai-companion-",
            "ai-energy-",
        ),
        slugs=frozenset({"ai-generated-content-disclosure"}),
    ),
    Rule(
        "ai-plans",
        prefixes=(
            "ai-free-vs-paid-",
            "ai-subscription-",
            "ai-api-pricing-",
            "ai-token-cost-",
            "ai-model-tiers-",
            "openrouter-",
            "claude-plans-",
            "gemini-plans-",
            "ai-coding-cost-",
        ),
        slugs=frozenset({"local-vs-cloud-ai-cost", "claude-api-prompt-caching-cost"}),
    ),
    Rule(
        "wordpress",
        prefixes=(
            "wordpress-",
            "astra-",
            "avada-",
            "blocksy-",
            "divi-",
            "elementor-",
            "bluehost-",
            "cloudways-",
            "fastcomet-",
            "hostgator-",
            "hosting-com-",
            "hostinger-",
            "siteground-",
            "mailchimp-wordpress-",
            "themeforest-",
        ),
    ),
    Rule(
        "woocommerce",
        prefixes=("woocommerce-",),
        slugs=frozenset(
            {"ecommerce-product-seo", "independent-store-marketplace", "omo-channel-integration"}
        ),
    ),
    Rule(
        "web-basics",
        prefixes=(
            "domain-",
            "dns-",
            "website-",
            "hosting-types-",
            "managed-hosting-",
            "https-certificate-",
            "css-",
            "sass-",
            "responsive-layout-",
            "web-layout-",
            "web-design-",
            "wireframe-",
            "ui-ux-",
            "lazy-loading-",
            "image-formats-",
            "lottie-",
            "font-license-",
            "amp-website-",
            "core-web-vitals-",
            "pagespeed-",
            "open-graph-",
            "namecheap-",
            "gandi-",
            "wix-",
            "saas-paas-",
            "short-url-",
            "figma-design-",
            "figma-plugin-",
            "rgb-cmyk-",
            "logo-design-",
            "licensed-assets-",
            "envato-",
            "google-site-kit-",
            "google-tag-manager-",
            "ga4-",
            "microsoft-clarity-",
            "online-course-platform-",
            "newspaper-editorial-",
        ),
        exclude_prefixes=("website-404-",),
    ),
    Rule(
        "seo",
        prefixes=(
            "seo-",
            "ahrefs-",
            "dataforseo-",
            "semrush-",
            "ubersuggest-",
            "similarweb-",
            "google-search-console-",
            "google-trends-",
            "google-ranking-",
            "google-business-profile",
            "knowledge-graph-",
            "technical-seo-",
            "on-page-seo-",
            "image-seo-",
            "canonical-url-",
            "redirects-",
            "hreflang-",
            "sitemap-website-",
            "structured-data-",
            "crawl-budget-",
            "search-crawlers-",
            "search-results-",
            "yahoo-search-",
            "website-404-",
        ),
    ),
    Rule(
        "ads",
        prefixes=(
            "google-ads-",
            "google-pmax-",
            "meta-ads-",
            "line-ads-",
            "dcard-advertising-",
            "adsense-",
            "affiliate-",
            "paid-vs-organic-",
            "sms-marketing-",
            "influencer-",
        ),
    ),
    Rule(
        "content-marketing",
        prefixes=(
            "content-marketing-",
            "brand-",
            "email-newsletter-",
            "brevo-",
            "kit-newsletter-",
            "customer-journey-",
            "business-models-",
            "ansoff-",
            "bcg-",
            "pestle-",
            "porter-",
            "swot-",
            "stp-",
            "design-thinking-",
            "social-media-",
            "short-video-",
            "ugc-",
            "marketing-",
            "martech-",
            "landing-page-",
            "utm-link-",
            "portfolio-case-",
        ),
    ),
    Rule(
        "finance-basics",
        prefixes=(
            "personal-finance-",
            "household-",
            "expense-tracking-",
            "savings-goal-",
            "emergency-fund-",
            "monthly-money-",
            "personal-balance-",
            "spending-triggers-",
            "kids-allowance-",
            "couple-money-",
            "fixed-cost-",
            "financial-document-",
            "finance-glossary-",
        ),
    ),
    Rule(
        "banking",
        prefixes=(
            "bank-",
            "digital-bank-",
            "mobile-payment-",
            "epayment-",
            "einvoice-",
            "online-banking-",
            "warning-account-",
            "foreign-currency-",
            "online-forex-",
            "overseas-atm-",
            "overseas-card-",
            "high-interest-savings-",
            "wise-transfer-",
        ),
    ),
    Rule(
        "credit",
        prefixes=(
            "credit-card-",
            "credit-score-",
            "build-credit-",
            "debit-vs-credit-",
            "installment-",
        ),
    ),
    Rule(
        "tax-insurance",
        prefixes=("labor-insurance-", "labor-pension-", "payslip-"),
        slugs=frozenset({"youtube-payment-tax-info", "taiwan-company-registration"}),
    ),
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@lru_cache(maxsize=1)
def series_members() -> dict[str, str]:
    """``slug -> sub-topic`` for every article a series catalogue lists, so a lesson whose
    slug does not carry the series prefix is still filed with its series."""
    members: dict[str, str] = {}
    from app.guides.series import catalogues

    for catalogue in catalogues():
        subtopic = {"claude-code": "claude-code", "codex": "codex"}.get(catalogue.slug)
        if subtopic is None:
            continue
        for entry in catalogue.entries:
            members.setdefault(entry.slug, subtopic)
        members.setdefault(catalogue.hub, subtopic)
    gemini = _repo_root() / "apps" / "web" / "lib" / "guide-series.json"
    if gemini.exists():
        data = json.loads(gemini.read_text(encoding="utf-8"))
        for article in data.get("articles", []):
            slug = article.get("slug")
            if isinstance(slug, str):
                dev = slug.startswith(("gemini-cli-", "gemini-api-"))
                members.setdefault(slug, "gemini-dev" if dev else "ai-chat")
        hub = data.get("hubSlug")
        if isinstance(hub, str):
            members.setdefault(hub, "ai-chat")
    terms = _repo_root() / "docs" / "ai-terms-series" / "catalogue.json"
    if terms.exists():
        data = json.loads(terms.read_text(encoding="utf-8"))
        for term in data.get("terms", []):
            slug = term.get("slug")
            if isinstance(slug, str):
                members.setdefault(slug, "ai-terms")
    return members


@dataclass
class Proposal:
    slug: str
    current: list[str]
    proposed: list[str]
    rules: list[str] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        return self.current != self.proposed


def propose(pack: ArticlePack) -> Proposal:
    """The topics ``pack`` should carry. Only lifestyle packs are ever changed; a travel
    pack is returned as it is, with no rule, so the table shows it was seen and left."""
    current = list(pack.topics)
    if pack.kind != "life":
        return Proposal(pack.slug, current, current)
    found: list[str] = []
    rules: list[str] = []
    for rule in RULES:
        if rule.matches(pack.slug) and rule.subtopic not in found:
            found.append(rule.subtopic)
            rules.append(f"prefix:{rule.subtopic}")
    series = series_members().get(pack.slug)
    if series is not None and series not in found:
        found.append(series)
        rules.append(f"series:{series}")
    if not found:
        return Proposal(pack.slug, current, current)
    proposed = [topic for topic in current if topic not in DROP_WHEN_FILED]
    for subtopic in found:
        parent = SUBTOPIC_PARENT[subtopic]
        if parent not in proposed and parent not in {slug for slug, _ in LIFE_SEED_TOPICS[:8]}:
            # ``website`` and ``marketing`` are new parents: an article filed under one of
            # their children has to carry the parent too, or the hub for that parent is
            # empty of everything that came before the split. The original eight parents
            # stay as they were: adding ``ai`` to a Codex lesson would be the rule deciding
            # the article's subject, which is the editor's call.
            proposed.append(parent)
        if subtopic not in proposed:
            proposed.append(subtopic)
    unknown = set(proposed) - LIFE_VOCABULARY
    if unknown:  # pragma: no cover - the rule table is checked by the tests
        raise ValueError(f"{pack.slug}: not a lifestyle topic: {sorted(unknown)}")
    return Proposal(pack.slug, current, proposed, rules)


def proposals(
    directory: Path | None = None,
    *,
    kind: Kind | None = "life",
    prefixes: tuple[str, ...] = (),
    slugs: set[str] | None = None,
) -> list[Proposal]:
    packs = load_packs(directory, slugs=slugs)
    chosen = [
        pack
        for pack in packs
        if (kind is None or pack.kind == kind)
        and (not prefixes or any(pack.slug.startswith(prefix) for prefix in prefixes))
    ]
    return [propose(pack) for pack in chosen]


def render_table(rows: list[Proposal]) -> str:
    """A Markdown table of what changes, for a pull request description or an editor's
    review. Unchanged packs are summarised in one line rather than listed."""
    lines = ["| slug | current | proposed | rules |", "| --- | --- | --- | --- |"]
    changed = [row for row in rows if row.changed]
    for row in changed:
        lines.append(
            f"| `{row.slug}` | {', '.join(row.current)} | {', '.join(row.proposed)} | "
            f"{', '.join(row.rules)} |"
        )
    lines.append("")
    lines.append(f"{len(changed)} of {len(rows)} packs would change")
    return "\n".join(lines)


def apply(rows: list[Proposal], directory: Path | None = None) -> list[Path]:
    """Rewrite the ``topics`` array of every changed pack, and nothing else. Every shipped
    pack round-trips through ``json.dumps(indent=2)`` unchanged, so the diff is the one
    line that moved."""
    root = directory or default_directory()
    written: list[Path] = []
    for row in rows:
        if not row.changed:
            continue
        path = root / f"{row.slug}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["topics"] = row.proposed
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append(path)
    return written
