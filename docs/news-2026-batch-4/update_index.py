"""Add this batch's articles to their vertical's index, in place, in the locales it publishes.

``update_index.py [crypto|tech|ai]... [--locale=<locale>] [--dry-run]`` -- with no vertical
named, every vertical that has something to add; with no locale named, all five. Run once,
after that vertical's packs carry the locales the run edits. Every sentence edit is an exact
replacement that must match once, so a second run fails instead of editing twice.

Three things changed from batch 3:

* Three indexes instead of one, so every table here is keyed by vertical first. The AI index
  keeps its slug forever (``docs/article-architecture.md``: every existing URL stays), so it is
  retitled in place, never renamed.
* The index's own link lists are ``article`` inlines now, not ``link`` blocks -- ``pack_cli
  relink`` ran over them -- and so are its opening paragraphs. Batch 3 looked up anchors by URL
  and asserted ``block["type"] == "paragraph"``; both now miss. Everything here addresses a
  block by its role and edits a rich paragraph's text nodes in place.
* Retitling an index breaks the link text of every article that points at it, because an
  ``article`` inline's ``text`` is frozen into the pack and rendered as it stands
  (``tasks/open/2026-09-16-retitled-guides-stale-link-text.md``). ``retitle`` walks the JSON
  structure of every pack and rewrites only the inlines whose ``slug`` is the index -- never a
  regular expression over the file, because the batches do not agree on field order.

Batch 3's one-off repair of the Japanese month headings is gone: batch #497's damage was fixed
by that run and the headings now read 2026年N月のニュース解説.

Batch 3 wrote whatever it produced. This one reads the site's own rules -- the schema, the
source cap, the reader-text walk -- and validates the finished index before it is written, so
an index that the importer would refuse is a refusal here instead of a red CI run.

Batch 4.5 (the news since 2026-09-16) added ``INSERT``: the crypto and tech indexes are
grouped by region and topic, and a batch that opens a group the index does not have -- the
United Kingdom, in crypto -- needs a heading and a paragraph the tables above cannot place.
Their generators (``build_*_index.py``) are not rerun, because they rewrite zh-TW from scratch
and would discard the relinked inlines and the four translations.

Batch 4.6 (the eleven articles of 2026-09-18) is zh-TW only, so this run learned ``--locale``:

    update_index.py ai tech crypto --locale=zh-TW [--dry-run]

Repeatable, or a comma list; without it the run is all five locales, which is what every batch
before this one was. The tables were keyed by locale already, so what the flag changes is the
pack check -- a zh-TW-only article carries no five locales -- and the guards in ``main``, which
refuse the three things one locale cannot decide on its own: an edit written for a locale the
run does not touch, citing a source (the five locale documents of one index would end up
citing different ones) and retitling. ``--dry-run`` prints the diff the run would write, and
writes nothing.

Batch 4.7 (the fifteen articles of 2026-09-20 onwards, with three earlier events written up
late) is zh-TW only as well, and changes nothing in this script: the same three tables, the
same flag, the same refusal on a second run. What it does change is the AI index's callout,
which names the last event the series covers as well as the day it was last expanded -- the
batch's newest AI article happened on 2026-09-21, so this time both dates in that sentence
move, not only the second.
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from verticals import (  # noqa: E402
    BY_NAME,
    CONTENT,
    LOCALES,
    VERTICALS,
    block_kind,
    block_text,
    link_of,
)

from app.guides.content_pack import ArticlePack  # noqa: E402
from app.guides.pack_ingest import _document_text  # noqa: E402
from app.guides.schemas import GuideDocument  # noqa: E402

# An edit whose replacement is still an editorial decision. The run stops and lists them all
# before it touches anything, so a half-filled table cannot write the word TODO into an index.
TODO = "«TODO»"

#: How many sources a document may carry, read off the schema instead of retyped. The index
#: already cites nine, and a batch that cites one source per article reaches the cap long
#: before anyone notices -- ``GuideDocument`` is the only place that number should live.
MAX_SOURCES = next(
    rule.max_length
    for rule in GuideDocument.model_fields["sources"].metadata
    if hasattr(rule, "max_length")
)

# The day this run expands the indexes: the one date the sentences below print, so the next
# batch changes this constant and the same sentences instead of finding new ones to edit.
EXPANDED_ON = "2026-09-23"
EXPANDED = {
    "zh-TW": "2026 年 9 月 23 日",
    "en": "September 23, 2026",
    "ja": "2026年9月23日",
    "ko": "2026년 9월 23일",
    "zh-CN": "2026 年 9 月 23 日",
}

# vertical -> (slug, where to put the link). ``after`` is the existing slug to place the link
# after (a leading "<" means before it), or an anchor of the ``INSERT`` kind -- per locale,
# as a dict, when it names a heading whose text differs by locale. Applied in order: an entry
# may name a slug inserted just before it.
#
# Batch 4.7 (2026-09-23): the twelve articles of the window that opened on 2026-09-20 and
# three write-ups of earlier events, zh-TW only. The AI index lists by month, so the six go
# after September's last link, in their ``display_order``; the tech and crypto indexes group
# by topic and region, and every link joins a group those indexes already have, so ``INSERT``
# again has nothing to place. Two rows anchor on a link this same run inserts, which the
# table allows because it is applied in order.
NEW: dict[str, list[tuple[str, object]]] = {
    "crypto": [
        # Taiwan's group, in the order a reader meets them: the act is already linked there,
        # the FSC's deposit-token pilot says what the act does not reach, and the finance
        # ministry's ruling taxes what it does.
        ("crypto-news-taiwan-deposit-token-pilot-20260922", "crypto-news-taiwan-vasp-act-20260630"),
        ("crypto-news-sec-innovation-exemption-20260917", "crypto-news-sec-regulation-crypto-assets-20260821"),
        ("crypto-news-taiwan-vasp-tax-ruling-20260903", "crypto-news-taiwan-deposit-token-pilot-20260922"),
    ],
    "tech": [
        ("tech-news-googlebook-launch-20260921", "tech-news-iphone-duo-dev-resources-20260918"),
        ("tech-news-eu-data-centre-rating-20260921", "tech-news-eu-cra-reporting-20260911"),
        # Batch 4.6 put CISA's Linux kernel advisory in platforms and software because the
        # index's only security group is the European Union's; the Zyxel advisory is the same
        # mechanism one case later, so it follows it rather than opening a group of its own.
        ("tech-news-cisa-kev-zyxel-gs1900-20260921", "tech-news-cisa-kev-linux-kernel-20260918"),
        # Petal is a France-United States cable. It was placed beside the Matsu cables at
        # first, as the index's other subsea-cable articles; the owner ruled on 2026-09-23
        # that a group headed "Taiwan: telecommunications and digital policy" is the wrong
        # home for it and moved it to the end of compute infrastructure, so the anchor here
        # is that group's last link.
        ("tech-news-meta-petal-subsea-cable-20260921", "tech-news-nvidia-mediatek-20260831"),
        ("tech-news-enisa-threat-landscape-20260922", "tech-news-cisa-kev-zyxel-gs1900-20260921"),
        ("tech-news-moda-mydata-student-loan-20260917", "tech-news-taiwan-sovereign-ai-corpus-20260915"),
    ],
    "ai": [
        ("ai-news-openai-math-advisory-20260921", "ai-news-kimi-k3-bedrock-20260918"),
        ("ai-news-openai-frontier-standards-20260921", "ai-news-openai-math-advisory-20260921"),
        ("ai-news-anthropic-life-sciences-verification-20260917", "ai-news-openai-frontier-standards-20260921"),
        ("ai-news-meta-one-subscription-20260915", "ai-news-anthropic-life-sciences-verification-20260917"),
        ("ai-news-openai-academy-paths-20260921", "ai-news-meta-one-subscription-20260915"),
        ("ai-news-nvidia-physical-ai-safety-20260921", "ai-news-openai-academy-paths-20260921"),
    ],
}
# What batch 4.6 (2026-09-22) added, kept for the record. Its comment said the same thing this
# one does about CISA: the index has no security group outside the European Union's.
#
#     "crypto": [
#         ("crypto-news-occ-three-trust-charters-20260918", "crypto-news-ncua-genius-act-20260518"),
#         ("crypto-news-sec-crypto-fraud-patterns-20260918", "crypto-news-cftc-passive-software-20260917"),
#         ("crypto-news-eba-third-party-risk-20260918", "crypto-news-eba-psd2-mica-20260212"),
#     ],
#     "tech": [
#         ("tech-news-iphone-duo-dev-resources-20260918", "tech-news-iphone-duo-20260909"),
#         ("tech-news-windows-cloud-rebuild-20260918", "tech-news-windows-project-zenith-20260904"),
#         ("tech-news-npm-stage-only-tokens-20260918", "tech-news-app-store-bundles-multiseat-20260916"),
#         ("tech-news-cisa-kev-linux-kernel-20260918", "tech-news-npm-stage-only-tokens-20260918"),
#     ],
#     "ai": [
#         ("ai-news-anthropic-accenture-evaluation-20260918", "ai-news-google-cc-family-agent-20260918"),
#         ("ai-news-openai-australia-youth-safety-20260918", "ai-news-anthropic-accenture-evaluation-20260918"),
#         ("ai-news-gemini-notebook-study-tools-20260918", "ai-news-openai-australia-youth-safety-20260918"),
#         ("ai-news-kimi-k3-bedrock-20260918", "ai-news-gemini-notebook-study-tools-20260918"),
#     ],
# vertical -> the articles whose first source the index cites. A source the index already
# carries is skipped, not appended twice.
#
# Nothing this batch either, and not because the sources are unsuitable. The AI index already
# cites 19 of the 20 sources a document may carry and the tech index 17, so six more do not
# fit either index. And citing is a five-locale act: the source list belongs to a locale
# document, so a zh-TW-only run would leave the five documents of one index citing different
# sources, which no later batch could put back without editing four locales it never read.
# The fifteen packs of this batch carry no other locale to cite from either. ``main`` refuses
# a non-empty table unless all five locales are in the run.
CITED: dict[str, list[str]] = {"crypto": [], "tech": [], "ai": []}

# vertical -> locale -> new title. Empty leaves the title alone: none of the three titles
# names a date or a count, so none of them is wrong after this batch.
RETITLE: dict[str, dict[str, str]] = {
    "crypto": {},
    "tech": {},
    "ai": {},
}

# vertical -> locale -> (where, old, new). ``where`` is "description" or a block index.
#
# Batch 4.7 fills only the "zh-TW" row of each vertical, and leaves the four other locales
# alone on purpose: every one of them states the day its own document was last expanded, and
# that sentence stays true for as long as this run does not add anything to it. Each sentence
# below is the one batch 4.6 left behind, so mostly only the date moves. Nothing else changes
# -- the index prose that introduces a batch by name (the AI index's second paragraph, the
# tech and crypto group paragraphs) is five-locale text, and a sentence added to zh-TW alone
# would make the five documents of one index describe different things. The block indexes are
# those of the indexes as they read on 2026-09-23, before this run's links; batch 4.6 appended
# its links behind every prose block, so the three AI indexes below did not move.
EDITS: dict[str, dict[str, list[tuple[object, str, str]]]] = {
    "crypto": {
        "zh-TW": [
            (1, "之後多次增補（最近一次 2026 年 9 月 22 日）。", f"之後多次增補（最近一次 {EXPANDED['zh-TW']}）。"),
        ],
        "en": [],
        "ja": [],
        "ko": [],
        "zh-CN": [],
    },
    "tech": {
        "zh-TW": [
            (1, "之後多次增補（最近一次 2026 年 9 月 22 日）。", f"之後多次增補（最近一次 {EXPANDED['zh-TW']}）。"),
        ],
        "en": [],
        "ja": [],
        "ko": [],
        "zh-CN": [],
    },
    "ai": {
        "zh-TW": [
            (0, "之後多次增補（最近一次 2026-09-22），", f"之後多次增補（最近一次 {EXPANDED_ON}），"),
            (24, "之後多次增補（最近一次 2026-09-22），", f"之後多次增補（最近一次 {EXPANDED_ON}），"),
            # The callout states both the last event the series covers and the day it was last
            # expanded. Batch 4.6 moved only the second date because every one of its articles
            # happened on 2026-09-18; this batch's newest AI article happened on 2026-09-21,
            # so both move, in one replacement so the sentence is matched as it reads.
            (25, "本輯收錄的事件到 2026-09-18 為止，最後增補於 2026-09-22。", f"本輯收錄的事件到 2026-09-21 為止，最後增補於 {EXPANDED_ON}。"),
        ],
        "en": [],
        "ja": [],
        "ko": [],
        "zh-CN": [],
    },
}

# vertical -> locale -> (row label in column 0, column index, current cell, new cell). Nothing
# this batch: the AI month table's reading-focus cells were widened in batch 4.3 and September
# already reads "models, agents, security, assistants, voice, infrastructure".
TABLE: dict[str, dict[str, list[tuple[str, int, str, str]]]] = {
    "crypto": {locale: [] for locale in LOCALES},
    "tech": {locale: [] for locale in LOCALES},
    "ai": {locale: [] for locale in LOCALES},
}
# vertical -> locale -> the header cell of a table column to remove. The AI index's count
# column went in batch 4.3; nothing is left to drop.
DROP_COLUMN: dict[str, dict[str, str]] = {
    "crypto": {},
    "tech": {},
    "ai": {},
}
# vertical -> locale -> (old caption fragment, new caption fragment). None this batch.
CAPTION: dict[str, dict[str, tuple[str, str]]] = {
    "crypto": {},
    "tech": {},
    "ai": {},
}


def _p(text: str) -> dict:
    return {"type": "paragraph", "text": text}


def _h(text: str) -> dict:
    return {"type": "heading", "level": 2, "text": text}


# vertical -> locale -> (anchor, block). A whole block the index does not have yet: batch 4.5
# gave the tech index one paragraph per group that gained articles, and the crypto index a
# whole United Kingdom section. The anchor names a block by what it is: ``link:<slug>``,
# ``heading:<exact text>`` or ``paragraph:<opening text>``, with a leading ``<`` to insert
# before it instead of after. Applied in order, before ``NEW``.
#
# Nothing this batch either. Every one of the fifteen links joins a group all three indexes
# already have, and an inserted block is prose: written for zh-TW alone it would leave the
# five locale documents of one index saying different things, which is the same reason
# ``EDITS`` adds no sentence naming this batch's subjects.
INSERT: dict[str, dict[str, list[tuple[str, dict]]]] = {
    "crypto": {locale: [] for locale in LOCALES},
    "tech": {locale: [] for locale in LOCALES},
    "ai": {locale: [] for locale in LOCALES},
}

#: A number of articles shown to the reader is wrong from the next batch onwards, so an index
#: states none (``docs/article-architecture.md`` Phase 5, the owner's decision of 2026-09-16).
#: The run refuses while one survives anywhere a reader sees it.
#:
#: What makes a number a count of articles is the unit or the noun beside it, never the digits,
#: and the five locales write it five ways: 38 則 / thirty-eight news reports / 38件 / 38편 /
#: 三十八条. So the quantity is Arabic, a Chinese numeral or an English number word, and then:
#:
#: * ``則 则 篇 편 本`` count written pieces and nothing else, so they stand on their own --
#:   simplified 则 as well as traditional 則, because zh-CN is one of the five locales this
#:   batch publishes and 「一月的三则消息」 is how it writes the sentence 「一月的三則消息」;
#: * ``條 条 件 건`` also count legal clauses and enforcement actions -- ``crypto.md``'s own
#:   vocabulary (「第 5 條」, 「本法第 12 条」, 「3件の行政処分」, 「2건의 제재」) -- so they
#:   count articles only beside a word that says so, which is why this is one rule for all
#:   three verticals rather than three that drift;
#: * in spaced text a quantity a few words from 新聞/ニュース/뉴스/articles/stories is a count
#:   whatever unit it uses ("38 key AI news stories", 「38건의 뉴스」).
#:
#: Years and version numbers are not quantities (2026-09-14, GPT-5.4, Lyria 3.5), and 同/每/第
#: turn a numeral into a determiner (「同一篇完整解析」). A false positive that survives all
#: that is still visible -- the refusal prints what it matched -- which is the right way round.
_QUANTITY = (
    r"(?<![\d.-])\d{1,3}(?![\d.-])"
    r"|(?<![同每這这其另某第])[一二兩两三四五六七八九十百]+"
    r"|(?:twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)-\w+"
    r"|(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen"
    r"|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy"
    r"|eighty|ninety)"
)
_PIECES = r"則|则|篇|편|本"
_CLAUSES = r"條|条|件|건"
_ARTICLES = (
    r"新聞|新闻|ニュース|뉴스|記事|기사|文章|報導|报道|事件|사건"
    r"|articles?|stories|reports?|pieces|events?|analyses|news|more"
)
_ADDED = r"收錄|收录|納入|纳入|補上|补上|增補|增补|追補|追加|보완|추가"
_NEAR = r"[^。．.!?！？]{0,12}?"
#: Which indexes the count rule guards. The AI index once printed its article count and must
#: never do so again. The crypto and tech indexes were generated by ``build_*_index.py`` without
#: any count, and their prose refers to documents and announcements by number (「那一篇」,
#: 「兩篇微軟公告」, "three of these articles"), which the rule cannot tell from a count: on
#: 2026-09-18 it matched 17/8/6/2/17 places in the tech index and 1/2/0/0/1 in crypto, none a
#: count of articles. Guarding those two would refuse every update for the wrong reason.
COUNT_RULE = {"crypto": False, "tech": False, "ai": True}

COUNT = re.compile(
    rf"(?:{_QUANTITY})\s*(?:{_PIECES})"
    rf"|(?:{_ARTICLES}|{_ADDED}){_NEAR}(?:{_QUANTITY})\s*(?:{_CLAUSES})"
    rf"|(?:{_QUANTITY})\s*(?:{_CLAUSES}){_NEAR}(?:{_ARTICLES}|{_ADDED})"
    rf"|(?:{_QUANTITY})(?:\W+\w+){{0,2}}\W+(?:{_ARTICLES})"
)


def replace_once(text: str, old: str, new: str, where: str) -> str:
    count = text.count(old)
    if count != 1:
        sys.exit(f"{where}: expected one '{old[:40]}', found {count}")
    return text.replace(old, new)


def edit_block(block: dict, old: str, new: str, where: str) -> None:
    """Replace inside a paragraph, rich or plain. Only ``text`` inlines are touched: an
    ``article`` inline's text is a link label owned by the target article's title."""
    # A callout's body is prose like any paragraph: the AI index's callout states the date the
    # series runs to, which is wrong the day a later event is added. A heading is a sentence
    # too: a group that gains a second kind of document is renamed, not given a second heading.
    if block["type"] in ("paragraph", "callout", "heading"):
        block["text"] = replace_once(block["text"], old, new, where)
        return
    if block["type"] != "rich_paragraph":
        sys.exit(f"{where}: block is a {block['type']}, not a paragraph")
    hits = [node for node in block["inlines"] if node["type"] == "text" and old in node["text"]]
    if len(hits) != 1 or hits[0]["text"].count(old) != 1:
        sys.exit(f"{where}: expected one '{old[:40]}' in the paragraph's text nodes, found {len(hits)}")
    hits[0]["text"] = hits[0]["text"].replace(old, new)


def as_document(doc: dict, where: str) -> GuideDocument:
    """The edited locale, read by the site's own schema. Every edit above works on raw JSON, so
    this is where a source list grown past the cap or a paragraph edited into nonsense is
    caught -- with the field named, rather than as a traceback or a pack CI refuses tomorrow."""
    try:
        return GuideDocument.model_validate(doc)
    except ValueError as error:
        sys.exit(f"{where}: the edited document is invalid\n - " + str(error).replace("\n", "\n   "))


def reader_text(doc: dict, document: GuideDocument) -> list[tuple[str, str]]:
    """(where, text) for everything in the index a reader sees, for the count rule.

    Every block, not only the prose ones: a count in a month heading, a diagram caption or a
    table header is a count. ``doc`` is the raw JSON, which is what can name where a match is;
    ``document`` is the site's own reading of it, and the assert holds this walk to everything
    ``pack_ingest`` reads, so a block type added to the schema -- ``summary`` and ``faq`` were
    added to that walk while this batch was being written -- cannot fall out of the guard."""
    parts = [("title", doc["title"]), ("description", doc["description"])]
    for i, block in enumerate(doc["blocks"]):
        where, kind = f"block {i}", block_kind(block)
        if kind in ("paragraph", "link", "heading"):
            parts.append((where, block_text(block)))
        elif kind == "list":
            parts.extend((f"{where} item", item) for item in block["items"])
        elif kind == "image":
            parts.append((f"{where} caption", block.get("caption", "")))
            parts.append((f"{where} alt", block["alt"]))
        elif kind == "table":
            parts.append((f"{where} caption", block.get("caption", "")))
            parts.extend((f"{where} header", cell) for cell in block["header"])
            parts.extend((f"{where} cell", cell) for row in block["rows"] for cell in row)
        elif kind == "callout":
            parts.append((f"{where} title", block.get("title", "")))
            parts.append((where, block["text"]))
        elif kind == "summary":
            parts.extend((f"{where} item", item) for item in block["items"])
        elif kind == "faq":
            parts.extend((f"{where} question", item["question"]) for item in block["items"])
            parts.extend((f"{where} answer", item["answer"]) for item in block["items"])
        elif kind == "code":
            parts.append((f"{where} label", block["label"]))
            parts.append((where, block["code"]))
    read = "".join(text for _, text in parts)
    missed = [line for line in _document_text(document).split("\n") if line not in read]
    assert not missed, f"reader_text does not read what pack_ingest reads: {missed[:3]}"
    return parts


def find_link(blocks: list[dict], target: str, locale: str) -> int:
    for i, block in enumerate(blocks):
        if block_kind(block) == "link" and link_of(block, locale)[0] == target:
            return i
    sys.exit(f"{locale}: no link to {target} in the index")


def find_anchor(blocks: list[dict], anchor: str, locale: str) -> int:
    """The index of the block an anchor names, whichever kind it names: ``link:<slug>``,
    ``heading:<exact text>`` or ``paragraph:<opening text>`` (a prose block that starts with
    it), each of which must match exactly one block."""
    kind, _, key = anchor.lstrip("<").partition(":")
    if kind == "link":
        return find_link(blocks, key, locale)
    if kind == "heading":
        hits = [i for i, b in enumerate(blocks) if block_kind(b) == "heading" and block_text(b) == key]
    elif kind == "paragraph":
        hits = [i for i, b in enumerate(blocks) if block_kind(b) == "paragraph" and block_text(b).startswith(key)]
    else:
        sys.exit(f"{locale}: an anchor is link:<slug>, heading:<text> or paragraph:<text>, not {anchor!r}")
    if len(hits) != 1:
        sys.exit(f"{locale}: expected one {kind} {key[:40]!r}, found {len(hits)}")
    return hits[0]


def insert_blocks(blocks: list[dict], inserts: list[tuple[str, dict]], locale: str) -> None:
    for anchor, block in inserts:
        if block_kind(block) == "heading" and any(
            block_kind(b) == "heading" and block_text(b) == block_text(block) for b in blocks
        ):
            sys.exit(f"{locale}: the index already has the heading {block_text(block)!r}")
        position = find_anchor(blocks, anchor, locale)
        offset = 0 if anchor.startswith("<") else 1
        blocks.insert(position + offset, block)


def link_block(slug: str, title: str) -> dict:
    """The relinked form the index already uses, so ``pack_cli relink`` has nothing to do."""
    return {"type": "rich_paragraph", "inlines": [{"type": "article", "text": title, "kind": "life", "slug": slug}]}


def has_work(name: str) -> bool:
    """Whether this vertical has anything wired up at all. Every table the run acts on, not the
    three batch 3 had: a vertical whose only pending change is a table cell, a caption or a
    cited source must not be reported as "nothing to add" and skipped in silence."""
    return bool(
        NEW[name]
        or CITED[name]
        or RETITLE[name]
        or any(EDITS[name].values())
        or any(TABLE[name].values())
        or DROP_COLUMN[name]
        or CAPTION[name]
        or any(INSERT[name].values())
    )


def unwritten(name: str) -> list[str]:
    """Every edit of this vertical whose replacement is still an editorial decision -- from all
    four tables, so the pre-flight names the work instead of the run dying half way through."""
    pending = [
        f"{name} {locale}: {old[:40]}"
        for locale in LOCALES
        for _, old, new in EDITS[name][locale]
        if new == TODO
    ]
    pending += [f"{name} {locale} title" for locale, title in RETITLE[name].items() if title == TODO]
    pending += [
        f"{name} {locale} table row {row_label}, column {column}"
        for locale in LOCALES
        for row_label, column, _, new in TABLE[name][locale]
        if new == TODO
    ]
    pending += [f"{name} {locale} caption" for locale, (_, new) in CAPTION[name].items() if new == TODO]
    pending += [
        f"{name} {locale} inserted {block_kind(block)} at {anchor}"
        for locale in LOCALES
        for anchor, block in INSERT[name][locale]
        if TODO in block_text(block)
    ]
    return pending


def misdirected(name: str, locales: list[str]) -> list[str]:
    """Every entry of this vertical written for a locale ``--locale`` leaves out.

    A table keyed by locale is only safe under a narrowed run while nothing is left in the
    rows the run skips: content there would be passed over in silence, which is how one locale
    ends up saying the index was expanded on a day the other four never heard of. Named here,
    before anything is read, rather than found in a diff later."""
    def many(entries: list, thing: str) -> str:
        return f"{len(entries)} {thing}" + ("" if len(entries) == 1 else "s")

    outside = [locale for locale in LOCALES if locale not in locales]
    lines = [
        f"{name} {locale}: {many(EDITS[name][locale], 'sentence edit')}"
        for locale in outside
        if EDITS[name][locale]
    ]
    lines += [
        f"{name} {locale}: {many(INSERT[name][locale], 'inserted block')}"
        for locale in outside
        if INSERT[name][locale]
    ]
    lines += [
        f"{name} {locale}: {many(TABLE[name][locale], 'table cell')}"
        for locale in outside
        if TABLE[name][locale]
    ]
    lines += [f"{name} {locale}: a dropped table column" for locale in outside if locale in DROP_COLUMN[name]]
    lines += [f"{name} {locale}: a caption" for locale in outside if locale in CAPTION[name]]
    lines += [f"{name} {locale}: a new title" for locale in outside if locale in RETITLE[name]]
    return lines


def retitle(index_slug: str, titles: dict[str, str]) -> int:
    """Carry a new index title into the link text of every article that points at it."""
    touched = 0
    for path in sorted(CONTENT.glob("*.json")):
        pack = json.loads(path.read_text(encoding="utf-8"))
        if pack.get("slug") == index_slug:
            continue
        changed = False
        for locale, doc in pack.get("locales", {}).items():
            if locale not in titles:
                continue
            for block in doc["blocks"]:
                if block["type"] != "rich_paragraph":
                    continue
                for node in block["inlines"]:
                    if node["type"] == "article" and node["slug"] == index_slug and node["text"] != titles[locale]:
                        node["text"] = titles[locale]
                        changed = True
        if changed:
            path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            touched += 1
    return touched


def update(vertical, locales: list[str], dry_run: bool) -> None:
    name = vertical.name
    path = CONTENT / f"{vertical.index}.json"
    if not path.is_file():
        sys.exit(f"{name}: {path.name} does not exist yet; the index article is written first")
    index = json.loads(path.read_text(encoding="utf-8"))
    # Linked and cited are different lists: an article may be cited without being new to the
    # index, and reading its pack for a source it does not have is a traceback, not an answer.
    wanted = list(dict.fromkeys([slug for slug, _ in NEW[name]] + CITED[name]))
    for slug in wanted:
        if not (CONTENT / f"{slug}.json").is_file():
            sys.exit(f"{name}: {slug}.json does not exist")
    packs = {slug: json.loads((CONTENT / f"{slug}.json").read_text(encoding="utf-8")) for slug in wanted}
    for slug, pack in packs.items():
        # A five-locale run wants the five, in the order every pack writes them: a batch that
        # publishes all five and has translated only four is not ready for its index. A run
        # narrowed by ``--locale`` asks only for the locales it is going to read, which is
        # what lets a zh-TW-only batch be linked at all.
        if locales == LOCALES:
            if list(pack["locales"]) != LOCALES:
                sys.exit(f"{slug} does not carry all five locales yet")
        else:
            missing = [locale for locale in locales if locale not in pack["locales"]]
            if missing:
                sys.exit(f"{slug} carries no {', '.join(missing)}; run with --locale=" + ",".join(pack["locales"]))
    already: list[str] = []

    for locale in locales:
        doc = index["locales"][locale]
        blocks = doc["blocks"]
        if locale in RETITLE[name]:
            doc["title"] = RETITLE[name][locale]
        for target, old, new in EDITS[name][locale]:
            if target == "description":
                doc["description"] = replace_once(doc["description"], old, new, f"{locale} description")
            else:
                # The block index is written by hand and shifts every time the index grows a
                # link, so a stale one is the ordinary mistake in this table. Named, like every
                # other misdirection here, rather than left to an IndexError.
                if not isinstance(target, int) or not 0 <= target < len(blocks):
                    sys.exit(f"{locale}: there is no block {target}; the index has {len(blocks)}")
                edit_block(blocks[target], old, new, f"{locale} block {target}")

        table = next((b for b in blocks if b["type"] == "table"), None)
        if TABLE[name][locale] or locale in DROP_COLUMN[name] or locale in CAPTION[name]:
            if table is None:
                sys.exit(f"{locale}: the index has no table to edit")
            for row_label, column, old, new in TABLE[name][locale]:
                row = next((r for r in table["rows"] if r[0] == row_label), None)
                if row is None:
                    sys.exit(f"{locale}: no table row labelled {row_label}")
                if not 0 <= column < len(row):
                    sys.exit(f"{locale}: row {row_label} has {len(row)} columns, no column {column}")
                if row[column] != old:
                    sys.exit(f"{locale}: row {row_label} column {column} is {row[column]!r}, expected {old!r}")
                row[column] = new
            if locale in DROP_COLUMN[name]:
                label = DROP_COLUMN[name][locale]
                if table["header"].count(label) != 1:
                    sys.exit(f"{locale}: expected one table column headed {label!r}, found {table['header']}")
                column = table["header"].index(label)
                if len(table["header"]) < 3:
                    sys.exit(f"{locale}: dropping {label!r} would leave a table of one column")
                del table["header"][column]
                for row in table["rows"]:
                    del row[column]
            if locale in CAPTION[name]:
                old, new = CAPTION[name][locale]
                table["caption"] = replace_once(table["caption"], old, new, f"{locale} caption")

        insert_blocks(blocks, INSERT[name][locale], locale)

        for slug, after in NEW[name]:
            if any(block_kind(b) == "link" and link_of(b, locale)[0] == slug for b in blocks):
                sys.exit(f"{locale}: {slug} is already linked")
            # A bare slug anchors on that article's link; a ``heading:`` anchor -- per locale
            # when the heading's text differs by locale -- places the first link of a group the
            # index gains in this batch, straight after its inserted heading.
            anchor = after[locale] if isinstance(after, dict) else after
            position = find_anchor(blocks, anchor, locale) if ":" in anchor else find_link(blocks, anchor.lstrip("<"), locale)
            offset = 0 if anchor.startswith("<") else 1
            blocks.insert(position + offset, link_block(slug, packs[slug]["locales"][locale]["title"]))

        # The index cites one source per article, and it already cites nine -- several of them
        # this batch's own subjects. A repeat is the same URL listed twice under the article,
        # and the cap is the schema's, so both are decided here rather than discovered by the
        # importer after the file is written.
        cited = doc["sources"]
        seen = {source["url"] for source in cited}
        for slug in CITED[name]:
            sources = packs[slug]["locales"][locale]["sources"]
            if not sources:
                sys.exit(f"{locale}: {slug} carries no source for the index to cite")
            source = dict(sources[0])
            if not source.get("checked_on"):
                sys.exit(f"{locale}: the source cited from {slug} has no checked_on")
            if source["url"] in seen:
                already.append(slug)
                continue
            if len(cited) >= MAX_SOURCES:
                sys.exit(
                    f"{locale}: the index already cites {len(cited)} sources and a document carries"
                    f" at most {MAX_SOURCES}; {slug}'s source does not fit. Cite fewer articles."
                )
            cited.append(source)
            seen.add(source["url"])

        document = as_document(doc, f"{name} {locale}")
        left = [(where, m.group(0))
                for where, value in reader_text(doc, document) for m in COUNT.finditer(value)]
        if left and COUNT_RULE[name]:
            sys.exit(f"{locale}: the index still shows an article count: {left}")

    try:
        ArticlePack.model_validate(index)
    except ValueError as error:
        sys.exit(f"{name}: the updated index is not a valid pack\n - " + str(error).replace("\n", "\n   "))

    # One serialisation, whether it is printed or written, so a dry run shows the bytes the
    # real run would put on disk -- indentation and all -- and never a reflowed near-miss.
    before = path.read_text(encoding="utf-8")
    after = json.dumps(index, ensure_ascii=False, indent=2) + "\n"
    counted = {locale: len(index["locales"][locale]["blocks"]) for locale in LOCALES}
    if dry_run:
        sys.stdout.writelines(
            difflib.unified_diff(
                before.splitlines(keepends=True),
                after.splitlines(keepends=True),
                fromfile=f"a/{path.name}",
                tofile=f"b/{path.name}",
            )
        )
        print(f"{name}: dry run over {', '.join(locales)}, nothing written;", counted)
        if RETITLE[name]:
            print(f"{name}: dry run, the link text in the other packs is not refreshed either")
        return

    path.write_text(after, encoding="utf-8")
    print(f"{name}: index updated,", counted)
    if already:
        print(f"{name}: already cited, not added again:", sorted(set(already)))
    if RETITLE[name]:
        print(f"{name}: link text refreshed in {retitle(vertical.index, RETITLE[name])} packs")


def parse_args(argv: list[str]) -> tuple[list[str], list[str], bool]:
    """``(verticals, locales, dry run)`` off the command line.

    ``--locale`` may be repeated and may carry a comma list; without it the run is all five
    locales, in the order every pack writes them, which is what every batch up to 4.5 was. The
    locales are returned in that same order however they were typed, so two runs of the same
    command cannot differ in which locale was edited first."""
    names: list[str] = []
    chosen_locales: list[str] = []
    dry_run = False
    rest = list(argv)
    while rest:
        argument = rest.pop(0)
        if argument == "--dry-run":
            dry_run = True
        elif argument == "--locale" or argument.startswith("--locale="):
            value = argument.partition("=")[2] if "=" in argument else (rest.pop(0) if rest else "")
            wanted = [part.strip() for part in value.split(",") if part.strip()]
            if not wanted:
                sys.exit("--locale takes a locale: --locale=zh-TW, or --locale=zh-TW,en")
            chosen_locales += wanted
        elif argument.startswith("-"):
            sys.exit(f"unknown option {argument}; this script takes --locale=<locale> and --dry-run")
        else:
            names.append(argument)
    unknown = [n for n in names if n not in BY_NAME]
    if unknown:
        sys.exit(f"unknown vertical {unknown}; one of " + ", ".join(BY_NAME))
    stray = [locale for locale in chosen_locales if locale not in LOCALES]
    if stray:
        sys.exit(f"unknown locale {stray}; one of " + ", ".join(LOCALES))
    locales = [locale for locale in LOCALES if locale in chosen_locales] or list(LOCALES)
    return names, locales, dry_run


def main() -> None:
    # The dry run prints a diff of Chinese, Japanese and Korean text; a console that is not
    # already UTF-8 would raise UnicodeEncodeError part way through it.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    named, locales, dry_run = parse_args(sys.argv[1:])
    chosen = [BY_NAME[n] for n in named] if named else list(VERTICALS)
    # Only the verticals this run touches: an AI sentence nobody has written yet is no reason
    # to refuse a crypto run that has nothing to do with it.
    pending = [line for vertical in chosen for line in unwritten(vertical.name)]
    if pending:
        sys.exit("edits still to write:\n - " + "\n - ".join(pending))
    if locales != LOCALES:
        # What a narrowed run may not do. Each of these three would leave the five documents of
        # one index disagreeing with each other, and four of them unread by whoever ran this.
        skipped = [line for vertical in chosen for line in misdirected(vertical.name, locales)]
        if skipped:
            sys.exit(
                f"this run is {', '.join(locales)}, and these edits are written for a locale it"
                " does not touch:\n - " + "\n - ".join(skipped)
            )
        citing = [vertical.name for vertical in chosen if CITED[vertical.name]]
        if citing:
            sys.exit(
                f"{', '.join(citing)}: CITED needs all five locales -- a source added to one"
                " locale document is a source the other four do not carry. Run without"
                " --locale, or empty the table."
            )
        renaming = [vertical.name for vertical in chosen if RETITLE[vertical.name]]
        if renaming:
            sys.exit(
                f"{', '.join(renaming)}: RETITLE needs all five locales -- it rewrites the link"
                " text of every pack that points at the index, and the locales this run skips"
                " would keep pointing at a title that no longer exists. Run without --locale."
            )
    for vertical in chosen:
        if not has_work(vertical.name):
            print("nothing to add:", vertical.name)
            continue
        update(vertical, locales, dry_run)


if __name__ == "__main__":
    main()
