"""Self-check for one article of this batch: ``check_article.py <slug> [--full] [--assets]``.

Run from ``apps/api`` with the API virtualenv. Without ``--full`` only the zh-TW original and
its research record are checked; ``--full`` adds the four translations, ``--assets`` the
published images. Prints OK or the list of failures; writes nothing.

The slug prefix decides everything that differs between the three verticals: which workspace
holds the research record, which index the first closing link points at and which topics the
article must carry. See ``verticals.py``. How many callouts it carries follows from the pack's
own topics, the way the site's ``_finance_problems`` does it.

The site's own rules are imported, never retyped: the disclaimer markers, the finance topics,
the topic taxonomy, the hero's size and byte caps, the summary and faq item bounds, the SVG
rules and the diagram-number rule all come from ``app.guides``, so a rule that changes there
changes here too. The bounds are read off the schema's own metadata rather than copied,
because the rules that use them sit behind ``ArticlePack.model_validate`` and a copy would
drift without anything failing.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from verticals import (  # noqa: E402
    CONTENT,
    LOCALES,
    PUBLIC,
    ROOT,
    block_kind,
    block_text,
    chinese_date,
    event_date_of,
    link_of,
    locale_markers,
    suffix,
    vertical_of,
    workspace_of,
)

from app.guides.content_pack import ArticlePack  # noqa: E402
from app.guides.pack_ingest import (  # noqa: E402
    FINANCE_TOPICS,
    HERO_MAX_BYTES,
    HERO_SIZE,
    IMAGE_HARD_CAP,
    _body_parts,
    _document_text,
    check_svg,
    errors,
    lint_document,
    missing_diagram_numbers,
)
from app.guides.schemas import FaqBlock, GuideDocument, SummaryBlock  # noqa: E402
from app.guides.taxonomy import LIFE_SEED_SUBTOPICS, LIFE_SEED_TOPICS  # noqa: E402

# slug -> the article its second closing link points at. One line per article of the batch, in
# publication order within its vertical: `display_order` is the vertical's base plus the
# position here, the way batch 3 numbered from 142. Fill this in as the articles are agreed.
#
# Crypto, batch 4.1. The site had no crypto article before this batch, so the vertical has no
# earlier news to point back at. The Taiwan act is written first and is the anchor: it is the
# one story a reader here is actually governed by, and every international piece ends by
# linking to what Taiwan did. Its own second link is the MiCA piece: the end of the EU's
# transitional period is the closest story this batch has to the 12- and 21-month transition
# in article 55. While the act was the only crypto article it pointed at an evergreen,
# `epayment-vs-ewallet-taiwan`, but that pack carries zh-TW only, so the four translations had
# no title to link to and `--full` could never pass; a link target has to exist in all five.
# Cross-links within a cluster (the four GENIUS Act rules, the two JFSA pieces) are not wired
# here: `pack_cli autolink` adds them once all eleven exist, which is what that pass is for.
RELATED: dict[str, str] = {
    "crypto-news-taiwan-vasp-act-20260630": "crypto-news-mica-transition-ends-20260701",
    "crypto-news-mica-transition-ends-20260701": "crypto-news-taiwan-vasp-act-20260630",
    "crypto-news-sec-crypto-interpretation-20260323": "crypto-news-taiwan-vasp-act-20260630",
    "crypto-news-sec-regulation-crypto-assets-20260821": "crypto-news-taiwan-vasp-act-20260630",
    "crypto-news-genius-act-occ-20260302": "crypto-news-taiwan-vasp-act-20260630",
    "crypto-news-stablecoin-aml-20260410": "crypto-news-taiwan-vasp-act-20260630",
    "crypto-news-fdic-genius-act-20260410": "crypto-news-taiwan-vasp-act-20260630",
    "crypto-news-ncua-genius-act-20260518": "crypto-news-taiwan-vasp-act-20260630",
    "crypto-news-eba-psd2-mica-20260212": "crypto-news-taiwan-vasp-act-20260630",
    "crypto-news-jfsa-working-group-20260216": "crypto-news-taiwan-vasp-act-20260630",
    "crypto-news-jfsa-cybersecurity-20260723": "crypto-news-taiwan-vasp-act-20260630",
    # Tech, batch 4.2, in the owner's list order (T1-T11 with T4a-c): `display_order` 300-312.
    # No single anchor here: each article's second link is the nearest story of its own cluster
    # (the 9/9 Apple event, the EU rules, the three MODA stories, the two platform updates, the
    # three NVIDIA announcements). The thirteen are written concurrently, so a writer cannot know
    # its target's title yet; `align_links.py --apply` fills the link texts in once all exist.
    "tech-news-iphone-duo-20260909": "tech-news-apple-september-hardware-20260909",
    "tech-news-apple-september-hardware-20260909": "tech-news-iphone-duo-20260909",
    "tech-news-eu-cra-reporting-20260911": "tech-news-apple-eu-business-terms-20260818",
    "tech-news-taiwan-sovereign-ai-corpus-20260915": "tech-news-taiwan-6g-spectrum-20260910",
    "tech-news-taiwan-6g-spectrum-20260910": "tech-news-taiwan-matsu-cable-20260623",
    "tech-news-taiwan-matsu-cable-20260623": "tech-news-taiwan-6g-spectrum-20260910",
    "tech-news-apple-eu-business-terms-20260818": "tech-news-eu-cra-reporting-20260911",
    "tech-news-windows-project-zenith-20260904": "tech-news-pixel-drop-20260915",
    "tech-news-pixel-drop-20260915": "tech-news-windows-project-zenith-20260904",
    "tech-news-apple-m6-m5-ultra-20260825": "tech-news-apple-september-hardware-20260909",
    "tech-news-nvidia-cuda-q-20260914": "tech-news-nvidia-vera-rubin-20260915",
    "tech-news-nvidia-mediatek-20260831": "tech-news-nvidia-vera-rubin-20260915",
    "tech-news-nvidia-vera-rubin-20260915": "tech-news-nvidia-cuda-q-20260914",
    # AI, batch 4.3, in the owner's list order (B1-B10, A1, A3): `display_order` 149-160. The
    # index is the existing `ai-news-2026-january-september-index`, retitled in place.
    "ai-news-openai-astral-20260319": "ai-news-nvidia-hugging-face-20260903",
    "ai-news-openai-funding-20260331": "ai-news-openai-s1-20260608",
    "ai-news-gpt-55-instant-20260505": "ai-news-gemini-38-live-20260915",
    "ai-news-chatgpt-ads-20260505": "ai-news-chatgpt-financial-services-20260910",
    "ai-news-frontier-governance-20260528": "ai-news-gpt-55-instant-20260505",
    "ai-news-openai-s1-20260608": "ai-news-openai-funding-20260331",
    "ai-news-openai-broadcom-chip-20260624": "ai-news-chatgpt-storage-scale-20260911",
    "ai-news-chatgpt-financial-services-20260910": "ai-news-chatgpt-ads-20260505",
    "ai-news-gpt-live-1-api-20260910": "ai-news-gemini-38-live-20260915",
    "ai-news-chatgpt-storage-scale-20260911": "ai-news-openai-broadcom-chip-20260624",
    "ai-news-gemini-38-live-20260915": "ai-news-gpt-live-1-api-20260910",
    "ai-news-nvidia-hugging-face-20260903": "ai-news-openai-astral-20260319",
    # Batch 4.5: only what was published from 2026-09-16 on, in event-date order within each
    # vertical (the owner's selection of 2026-09-18). Appended, never inserted: the position here
    # is the display_order, and the earlier batches' numbers must not move.
    "ai-news-chatgpt-sponsored-agents-20260916": "ai-news-chatgpt-ads-20260505",
    "ai-news-firefox-smart-window-mistral-20260916": "ai-news-siri-ai-ios-27-20260914",
    "ai-news-openai-misalignment-reports-20260917": "ai-news-frontier-governance-20260528",
    "ai-news-anthropic-pace-metrics-20260917": "ai-news-pace-the-frontier-20260912",
    "ai-news-astra-for-law-20260917": "ai-news-chatgpt-financial-services-20260910",
    "ai-news-google-cc-family-agent-20260918": "ai-news-google-assistant-gemini-20260904",
    "tech-news-apple-att-eu-20260916": "tech-news-apple-eu-business-terms-20260818",
    "tech-news-app-store-bundles-multiseat-20260916": "tech-news-apple-att-eu-20260916",
    "tech-news-eu-kids-act-20260917": "tech-news-eu-cra-reporting-20260911",
    "tech-news-taiwan-matsu-cable-tm4-20260918": "tech-news-taiwan-matsu-cable-20260623",
    "crypto-news-fca-perimeter-guidance-20260916": "crypto-news-mica-transition-ends-20260701",
    "crypto-news-cftc-passive-software-20260917": "crypto-news-sec-crypto-interpretation-20260323",
    "crypto-news-fca-p2p-crypto-crackdown-20260917": "crypto-news-fca-perimeter-guidance-20260916",
    # 4.6（2026-09-18 起，只做 zh-TW）：AI 167–170、科技 317–320；幣圈 214–216 待研究紀錄定 slug 後補。
    "ai-news-anthropic-accenture-evaluation-20260918": "ai-news-pace-the-frontier-20260912",
    "ai-news-openai-australia-youth-safety-20260918": "ai-news-google-cc-family-agent-20260918",
    "ai-news-gemini-notebook-study-tools-20260918": "ai-news-gemini-38-live-20260915",
    "ai-news-kimi-k3-bedrock-20260918": "ai-news-nvidia-hugging-face-20260903",
    "tech-news-npm-stage-only-tokens-20260918": "tech-news-eu-cra-reporting-20260911",
    "tech-news-cisa-kev-linux-kernel-20260918": "tech-news-pixel-drop-20260915",
    "tech-news-windows-cloud-rebuild-20260918": "tech-news-windows-project-zenith-20260904",
    "tech-news-iphone-duo-dev-resources-20260918": "tech-news-iphone-duo-20260909",
}

def items_bounds(block: type) -> tuple[int, int]:
    """How many items this block may carry, read off the schema instead of retyped -- the way
    ``update_index.MAX_SOURCES`` reads the source cap. ``SummaryBlock`` and ``FaqBlock`` state
    2-5 and 2-10 as ``annotated_types`` metadata, and the rules below are unreachable while
    ``ArticlePack.model_validate`` refuses first, so a copy of those numbers would drift here
    without anything ever failing."""
    metadata = block.model_fields["items"].metadata
    low = next(rule.min_length for rule in metadata if hasattr(rule, "min_length"))
    high = next(rule.max_length for rule in metadata if hasattr(rule, "max_length"))
    return low, high


SUMMARY_ITEMS = items_bounds(SummaryBlock)
FAQ_ITEMS = items_bounds(FaqBlock)
SIMPLIFIED = re.compile("[价单适发应实来体结条轮对构补现这们说时让为么过还开关语问题网页务处设备]")
NUMBER = re.compile(r"\d+(?:[.:]\d+)*")
# The hub topics and the subtopic -> parent map, from the taxonomy the database is seeded from.
HUBS = {slug for slug, _ in LIFE_SEED_TOPICS}
PARENT = {slug: parent for slug, parent, _ in LIFE_SEED_SUBTOPICS}
LOCALE_MARKER = locale_markers()


def paragraphs(blocks: list[dict]) -> str:
    """Every paragraph the reader reads, joined -- ``rich_paragraph`` included."""
    return "".join(block_text(b) for b in blocks if block_kind(b) == "paragraph")


def cjk_units(text: str) -> float:
    return sum(1 if ord(c) > 255 else 0.55 for c in text)


def body_without_summary(document: GuideDocument) -> str:
    """The article's own running text, without the summary, for "a number the summary states
    and the article does not".

    ``_body_parts`` is the site's own idea of the body -- paragraphs, lists, tables, callouts
    and the FAQ, but not the title, the description, a caption or a link label -- so a figure
    the writer puts in the 120-200 character description and in the summary, and states nowhere
    in the article, is caught. ``_document_text`` is the wrong basis twice over: it opens with
    the title and the description, and it counts the summary, which would make this rule
    compare the summary with itself."""
    rest = document.model_copy(
        update={"blocks": [b for b in document.blocks if not isinstance(b, SummaryBlock)]}
    )
    return re.sub(r"[,，]", "", "".join(_body_parts(rest)))


def order_of(slug: str) -> int | None:
    """The `display_order` this article should carry, or None where no band is assigned yet."""
    vertical = vertical_of(slug)
    if vertical.order_base is None:
        return None
    peers = [s for s in RELATED if s.startswith(vertical.prefix)]
    return vertical.order_base + peers.index(slug)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    full, assets = "--full" in sys.argv, "--assets" in sys.argv
    if len(args) != 1 or args[0] not in RELATED:
        print("usage: check_article.py <slug> [--full] [--assets]")
        print("slug one of:", *RELATED or ["(RELATED in this file is still empty)"])
        return 2
    slug = args[0]
    vertical = vertical_of(slug)
    fails: list[str] = []
    # ``pack_ingest`` has two levels and so does this: what a reviewer would send back, and
    # what is worth a look. The hero's editorial byte guideline is the second kind there
    # (``hero_over_guideline`` is a warning), so it is the second kind here too.
    warns: list[str] = []

    def need(ok: bool, message: str) -> None:
        if not ok:
            fails.append(message)

    raw = json.loads((CONTENT / f"{slug}.json").read_text(encoding="utf-8"))
    try:
        pack = ArticlePack.model_validate(raw)
    except ValueError as error:
        # A misplaced summary or a sixth FAQ is refused by the model itself, and a traceback
        # is a worse answer than the line the writer has to fix.
        print("FAIL\n -", str(error).replace("\n", "\n   "))
        return 1
    research_path = workspace_of(slug) / "research" / f"{slug}.json"
    if not research_path.is_file():
        print(f"FAIL\n - no research record at {research_path.relative_to(ROOT)}")
        return 1
    research = json.loads(research_path.read_text(encoding="utf-8"))
    event_date = event_date_of(slug)
    # Batch 3 checked everything against one frozen batch date. Batch 4 runs over weeks and
    # BRIEF.md says checked_on is the day the writer actually verified, so the research record
    # is the single source of truth and the pack has to agree with it everywhere.
    checked = str(research.get("checked_on", ""))

    need(pack.slug == slug and pack.kind == "life" and pack.destination_id is None, "slug/kind/destination")
    need(pack.topics[:1] == [vertical.topics[0]], f"topics start with {vertical.topics[0]}: {pack.topics}")
    need(set(vertical.topics) <= set(pack.topics), f"topics must include {list(vertical.topics)}: {pack.topics}")
    unknown = sorted(set(pack.topics) - HUBS - set(PARENT))
    need(not unknown, f"topics not in the taxonomy: {unknown}")
    orphans = sorted(t for t in pack.topics if t in PARENT and PARENT[t] not in pack.topics)
    need(not orphans, f"subtopics whose parent hub is missing from topics: {orphans}")
    order = order_of(slug)
    if order is None:
        # No band assigned to this vertical yet; only insist the field was set on purpose.
        need(pack.display_order != 100, "display_order is still the default 100")
    else:
        need(pack.display_order == order, f"display_order should be {order}")
    # news_date drives `sort=news` on /life and the news topic pages, and its absence is a
    # test failure since PR #537, not a cosmetic one.
    need(pack.news_date is not None, "news_date is missing")
    need(pack.news_date is None or str(pack.news_date) == event_date,
         f"news_date {pack.news_date} is not the slug's event date {event_date}")
    wanted = LOCALES if full else ["zh-TW"]
    need(list(raw["locales"]) == wanted, f"locales {list(raw['locales'])} != {wanted}")
    if "zh-TW" not in pack.locales:
        # Everything below reads the original. A pack mid-batch may be missing a translation,
        # which is reported above and checked around; missing the original is nothing to check.
        print(f"FAIL\n - locales {list(raw['locales'])}: there is no zh-TW to check")
        return 1

    zh = pack.locales["zh-TW"]
    zh_blocks = raw["locales"]["zh-TW"]["blocks"]
    text = paragraphs(zh_blocks)
    need(1800 <= len(text) <= 3000, f"zh-TW paragraph characters {len(text)} not in 1800–3000")
    need(len(zh.title) <= 60, f"title {len(zh.title)} > 60")
    need(120 <= len(zh.description) <= 200, f"description length {len(zh.description)} not in 120–200")
    found = SIMPLIFIED.findall(_document_text(zh))
    need(not found, f"simplified characters in zh-TW: {''.join(sorted(set(found)))}")
    first_two = " ".join(block_text(b) for b in zh_blocks[:2] if block_kind(b) == "paragraph")
    need(chinese_date(event_date) in first_two or event_date in first_two,
         "event date not in the opening paragraphs")
    need(bool(checked), "research record has no checked_on")
    if checked:
        need(chinese_date(checked) in first_two or checked in first_two,
             "checked date not in the opening paragraphs")
        need(event_date <= checked <= str(date.today()),
             f"checked_on {checked} is before the event ({event_date}) or in the future")
    need(research["event_date"] == event_date and research["slug"] == slug, "research slug/event_date")
    need(research.get("title") == zh.title, "research title differs from zh-TW title")

    # The pack's own topics go in, so `finance_no_disclaimer` actually fires on a crypto
    # article. Batch 3 called this without topics and the finance rules never ran.
    for problem in errors(lint_document(zh, "life", topics=pack.topics)):
        fails.append(f"lint zh-TW: {problem}")

    # The disclaimer, on finance/investing/crypto articles only, in each locale's own wording,
    # and the second callout that comes with it. Both follow the pack's topics rather than the
    # vertical, because that is what the site keys on (``_finance_problems``): an article that
    # carries `finance` needs the disclaimer whatever its slug says, and crypto's two callouts
    # fall out of its own topics. Which is also why the batch's two specs disagreeing about
    # whether an ai-news article may carry `finance` -- `ai.md` "沒有免責 callout" against B8
    # of `tasks/open/2026-09-16-news-batch-4-3-ai-news.md` -- does not need settling here: it
    # is filed as `tasks/open/2026-09-16-ai-md-and-b8-disagree-about.md`, and this rule is
    # right either way.
    finance = bool(FINANCE_TOPICS.intersection(topic.casefold() for topic in pack.topics))
    wanted_callouts = 2 if finance else 1

    # Block order (BRIEF.md "blocks 的順序"): two paragraphs, the summary, five sections with
    # the table closing section 2 and the diagram closing section 3, the FAQ, the callout(s),
    # two links. Compared by role, so it holds before and after relink/autolink.
    kinds = [block_kind(b) for b in zh_blocks]
    headings = [i for i, b in enumerate(zh_blocks) if b["type"] == "heading" and b["level"] == 2]
    # Where the two blocks batch 4 adds sit, or None. An article that is missing one is what
    # this check exists to report, so nothing below may index() its way to a ValueError.
    summary_at = kinds.index("summary") if "summary" in kinds else None
    faq_at = kinds.index("faq") if "faq" in kinds else None
    need(len(headings) == 5, f"{len(headings)} level-2 headings, want 5")
    need(kinds[:3] == ["paragraph", "paragraph", "summary"], "blocks must open paragraph, paragraph, summary")
    need(kinds.count("table") == 1 and kinds.count("image") == 1, "one table, one diagram")
    need(kinds.count("summary") == 1 and kinds.count("faq") == 1, "one summary, one faq")
    need(kinds.count("callout") == wanted_callouts,
         f"{kinds.count('callout')} callouts, want {wanted_callouts}"
         + (" (the article's own and the finance disclaimer)" if finance else ""))
    tail = ["faq"] + ["callout"] * wanted_callouts + ["link", "link"]
    need(kinds[-len(tail):] == tail, "blocks must end " + ", ".join(tail))
    if len(headings) == 5 and "table" in kinds and "image" in kinds:
        need(headings[1] < kinds.index("table") < headings[2], "table belongs at the end of section 2")
        need(headings[2] < kinds.index("image") < headings[3], "diagram belongs at the end of section 3")
    if len(headings) == 5 and summary_at is not None:
        need(summary_at < headings[0], "the summary belongs before the first heading")
    if len(headings) == 5 and faq_at is not None:
        need(faq_at > headings[4], "the faq belongs after the last section")
        bounds = headings + [faq_at]
        for n, (start, stop) in enumerate(zip(bounds, bounds[1:]), start=1):
            count = kinds[start + 1:stop].count("paragraph")
            need(2 <= count <= 4, f"section {n} has {count} paragraphs, want 2–4")

    # zh-TW's own summary and faq, kept for the per-locale count comparison below. Their
    # contents are checked inside the locale loop, against each locale's own document.
    summary = next((b for b in zh.blocks if isinstance(b, SummaryBlock)), None)
    faq = next((b for b in zh.blocks if isinstance(b, FaqBlock)), None)

    # A pack mid-batch carries the locales merge_locale has reached so far. The `locales ... !=
    # ...` failure above reports the gap; reading past it is how batch 3's checker died with a
    # KeyError instead of printing it.
    for locale in [locale for locale in wanted if locale in pack.locales]:
        doc = pack.locales[locale]
        blocks = raw["locales"][locale]["blocks"]
        s = suffix(locale)
        need(doc.hero is not None and doc.hero.src == f"/guides/{slug}/hero{s}.jpg", f"{locale} hero src")
        need(doc.hero is not None and (doc.hero.width, doc.hero.height) == HERO_SIZE,
             f"{locale} hero size, want {HERO_SIZE[0]}x{HERO_SIZE[1]}")
        images = [b for b in doc.blocks if b.type == "image"]
        need(len(images) == 1 and images[0].src == f"/guides/{slug}/diagram-1{s}.svg", f"{locale} diagram src")
        need(all(str(src.checked_on) == checked for src in doc.sources),
             f"{locale} sources checked_on must all be {checked}")
        need(2 <= len(doc.sources) <= 4, f"{locale} {len(doc.sources)} sources, want 2–4")
        for table in (b for b in doc.blocks if b.type == "table"):
            need(len(table.header) <= 4, f"{locale} table has {len(table.header)} columns (max 4)")
            need(all(len(row) == len(table.header) for row in table.rows), f"{locale} table row width")
            need(3 <= len(table.rows) <= 6, f"{locale} table rows {len(table.rows)}")
        # The summary: the answer, before the first section, in that locale's own numbers --
        # and the FAQ: questions this article answers, in plain text. Per locale, because
        # BRIEF.md states both rules for the block and all five are written, not derived; a
        # URL pasted into a translated answer is the likeliest way one arrives.
        doc_summary = next((b for b in doc.blocks if isinstance(b, SummaryBlock)), None)
        need(doc_summary is not None, f"{locale} has no summary block")
        if doc_summary is not None:
            need(SUMMARY_ITEMS[0] <= len(doc_summary.items) <= SUMMARY_ITEMS[1],
                 f"{locale} summary has {len(doc_summary.items)} sentences, "
                 f"want {SUMMARY_ITEMS[0]}–{SUMMARY_ITEMS[1]}")
            need("".join(doc_summary.items) != doc.description,
                 f"{locale} the summary just repeats the description")
            body_numbers = body_without_summary(doc)
            for number in NUMBER.findall(" ".join(doc_summary.items)):
                need(number in body_numbers, f"{locale} number {number} in the summary is not in the body")
        doc_faq = next((b for b in doc.blocks if isinstance(b, FaqBlock)), None)
        need(doc_faq is not None, f"{locale} has no faq block")
        if doc_faq is not None:
            need(FAQ_ITEMS[0] <= len(doc_faq.items) <= FAQ_ITEMS[1],
                 f"{locale} faq has {len(doc_faq.items)} pairs, want {FAQ_ITEMS[0]}–{FAQ_ITEMS[1]}")
            linked = [item.question for item in doc_faq.items if "://" in item.answer]
            need(not linked, f"{locale} faq answers are plain text, no links: {linked}")
        if finance:
            # Some callout carries the marker -- the rule pack_ingest._finance_problems states
            # and merge_locale.py and apply_corrections.py check. Which of the two callouts it
            # is nobody's rule: crypto.md pins both to the same span and stops there.
            marker = LOCALE_MARKER[locale]
            callouts = [b for b in doc.blocks if b.type == "callout"]
            need(any(marker.casefold() in b.text.casefold() for b in callouts),
                 f"{locale} needs a disclaimer callout containing {marker!r}")
        links = [b for b in blocks if block_kind(b) == "link"]
        targets = [vertical.index, RELATED[slug]]
        need(len(links) == 2, f"{locale} {len(links)} closing links, want 2")
        for block, target in zip(links, targets):
            pointed, label = link_of(block, locale)
            need(pointed == target, f"{locale} link points at {pointed}, want {target}")
            other_path = CONTENT / f"{target}.json"
            need(other_path.is_file(), f"{locale} link target {target}.json does not exist yet")
            if other_path.is_file():
                other = json.loads(other_path.read_text(encoding="utf-8"))["locales"].get(locale)
                need(other is not None and label == other["title"],
                     f"{locale} link text must be the title of {target}")
        if locale != "zh-TW":
            need([block_kind(b) for b in blocks] == kinds, f"{locale} block structure differs from zh-TW")
            need([src.url for src in doc.sources] == [src.url for src in zh.sources], f"{locale} source urls differ")
            # Positional pairs, so only a pair that plays the same part is comparable: a
            # translation that gained or lost a block is already reported one line up.
            for a, b in zip(doc.blocks, zh.blocks):
                if a.type == b.type == "table":
                    need((len(a.header), len(a.rows)) == (len(b.header), len(b.rows)), f"{locale} table shape")
                if a.type == b.type == "heading":
                    need(a.level == b.level, f"{locale} heading level")
            need(doc_summary is not None and summary is not None
                 and len(doc_summary.items) == len(summary.items), f"{locale} summary sentence count differs")
            need(doc_faq is not None and faq is not None
                 and len(doc_faq.items) == len(faq.items), f"{locale} faq question count differs")
            need(len(paragraphs(blocks)) >= 0.45 * len(text) if locale != "en" else True, f"{locale} translation looks short")
            for problem in errors(lint_document(doc, "life", topics=pack.topics)):
                fails.append(f"lint {locale}: {problem}")

    diagram = research.get("diagram") or {}
    nodes = diagram.get("nodes") or []
    need(len(nodes) == 4 and all(len(n) == 2 for n in nodes), "research diagram needs 4 [heading, detail] nodes")
    need(cjk_units(research.get("hero_label", "")) <= 13, "hero_label too long")
    need(cjk_units(diagram.get("title", "")) <= 21, "diagram title too long")
    # Only the well-formed nodes are measured: the arity failure is already recorded above, and
    # unpacking a malformed one here would end the run before the other failures are printed.
    for heading, detail in (n for n in nodes if len(n) == 2):
        need(cjk_units(heading) <= 9, f"node heading too long: {heading}")
        need(cjk_units(detail) <= 15, f"node detail too long: {detail}")
    image = next((b for b in zh.blocks if b.type == "image"), None)
    need(image is not None and diagram.get("caption") == image.caption, "research diagram caption differs from pack")
    need([s["url"] for s in research.get("sources", [])] == [s.url for s in zh.sources], "research sources differ from pack")
    need(all(str(s.get("checked_on")) == checked for s in research.get("sources", [])), "research sources checked_on")
    need(bool(research.get("verified_facts")), "research verified_facts empty")
    # BRIEF.md: an article whose writer wrote nothing down here is suspect, not clean.
    need(bool(research.get("unverified_or_excluded")), "research unverified_or_excluded empty")
    body = re.sub(r"[,，]", "", _document_text(zh))
    drawn = " ".join([diagram.get("title", ""), research.get("hero_label", "")] + [" ".join(n) for n in nodes])
    for number in NUMBER.findall(drawn):
        need(number in body, f"number {number} on the artwork is not in the zh-TW text")
    if full:
        for locale in LOCALES[1:]:
            tr = research.get("translations", {}).get(locale, {})
            tdiagram = tr.get("diagram") or {}
            tnodes = tdiagram.get("nodes") or []
            # Everything ``build_assets`` draws from this record, not a part of it:
            # ``hero_svg_text`` reads ``hero_label`` and ``diagram_svg_text`` reads the
            # diagram's ``title``, ``nodes`` and ``caption``. A record this check called clean
            # while it was missing the title reached the drawing step as a bare KeyError.
            need(bool(tr.get("hero_label")) and len(tnodes) == 4
                 and bool(tdiagram.get("title")) and bool(tdiagram.get("caption")),
                 f"research translations.{locale} incomplete "
                 "(hero_label, diagram title, 4 nodes, diagram caption)")
            limit = 1.9 if locale == "en" else 1.25
            need(cjk_units(tr.get("hero_label", "")) <= 13 * limit, f"{locale} hero_label too long")
            # The zh-TW title is held to 21 units above, for the width the drawing has for it.
            need(cjk_units(tdiagram.get("title", "")) <= 21 * limit, f"{locale} diagram title too long")
            for heading, detail in (n for n in tnodes if len(n) == 2):
                need(cjk_units(heading) <= 9 * limit + 2, f"{locale} node heading too long: {heading}")
                need(cjk_units(detail) <= 15 * limit + 3, f"{locale} node detail too long: {detail}")
            if locale in pack.locales:
                timage = next((b for b in pack.locales[locale].blocks if b.type == "image"), None)
                need(timage is not None and tdiagram.get("caption") == timage.caption, f"{locale} diagram caption differs")

    if assets:
        for locale in LOCALES:
            s = suffix(locale)
            for name in (f"hero{s}.jpg", f"hero{s}.svg", f"diagram-1{s}.svg"):
                path = PUBLIC / "guides" / slug / name
                need(path.is_file(), f"missing {path.relative_to(ROOT)}")
                if not path.is_file():
                    continue
                # pack_ingest's own two levels, so the checker, the writer and the importer
                # cannot disagree about what ships: over IMAGE_HARD_CAP is an error there
                # (``image_too_large``, and what tests/test_guides_content_pack.py refuses),
                # while a hero over the editorial HERO_MAX_BYTES is a warning
                # (``hero_over_guideline``). Batch 3 failed the hero at 200 KB, which is
                # stricter than the site itself and than build_assets.py, so a drawing that
                # fit_bytes legitimately writes at 210 KB could never pass its own check.
                size = path.stat().st_size
                need(size <= IMAGE_HARD_CAP, f"{name} is {size} bytes, over {IMAGE_HARD_CAP}")
                if name.endswith(".jpg") and size > HERO_MAX_BYTES:
                    warns.append(f"{name} is {size} bytes, over the {HERO_MAX_BYTES} a hero is "
                                 "held to; simplify the drawing and render it again")
                if name.endswith(".svg"):
                    for problem in errors(check_svg(path.read_text(encoding="utf-8"))):
                        fails.append(f"svg {name}: {problem}")
            diagram_svg = PUBLIC / "guides" / slug / f"diagram-1{s}.svg"
            if diagram_svg.is_file() and locale in pack.locales:
                # The real rule, on the real drawing, rather than on the research record.
                drawn_only = missing_diagram_numbers(diagram_svg.read_text(encoding="utf-8"), pack.locales[locale])
                need(not drawn_only, f"{locale} diagram draws numbers the text lacks: {drawn_only}")

    for message in warns:
        print("WARN -", message)
    if fails:
        print("FAIL")
        for message in fails:
            print(" -", message)
        return 1
    print("OK", slug, f"zh-TW paragraphs {len(text)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
