"""Add this batch's articles to their vertical's index, in place, in five languages.

``update_index.py [crypto|tech|ai]...`` -- with no vertical named, every vertical that has
something to add. Run once, after that vertical's packs carry all five locales. Every sentence
edit is an exact replacement that must match once, so a second run fails instead of editing
twice.

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
"""
from __future__ import annotations

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
EXPANDED_ON = "2026-09-19"
EXPANDED = {
    "zh-TW": "2026 年 9 月 19 日",
    "en": "September 19, 2026",
    "ja": "2026年9月19日",
    "ko": "2026년 9월 19일",
    "zh-CN": "2026 年 9 月 19 日",
}

# vertical -> (slug, where to put the link). ``after`` is the existing slug to place the link
# after (a leading "<" means before it), or an anchor of the ``INSERT`` kind -- per locale,
# as a dict, when it names a heading whose text differs by locale. Applied in order: an entry
# may name a slug inserted just before it.
#
# Batch 4.6 (2026-09-19): the two AI announcements of 2026-09-18 that have a first-party page
# to write from. The AI index lists by month, so both go after September's last link. Crypto
# and tech have nothing in this batch, and their tables below are empty rather than carrying
# batch 4.5's entries, which have already been applied to the shipped indexes.
NEW: dict[str, list[tuple[str, object]]] = {
    "crypto": [],
    "tech": [],
    "ai": [
        ("ai-news-anthropic-accenture-evaluation-20260918", "ai-news-google-cc-family-agent-20260918"),
        ("ai-news-google-flow-fashion-20260918", "ai-news-anthropic-accenture-evaluation-20260918"),
    ],
}
# vertical -> the articles whose first source the index cites. A source the index already
# carries is skipped, not appended twice. The AI index already cites 19 against a cap of 20,
# so only one of this batch's two first sources fits: the Anthropic announcement is cited, and
# the Google post is reachable from its own article's sources.
CITED: dict[str, list[str]] = {
    "crypto": [],
    "tech": [],
    "ai": ["ai-news-anthropic-accenture-evaluation-20260918"],
}

# vertical -> locale -> new title. Empty leaves the title alone: none of the three titles
# names a date or a count, so none of them is wrong after this batch.
RETITLE: dict[str, dict[str, str]] = {
    "crypto": {},
    "tech": {},
    "ai": {},
}

# vertical -> locale -> (where, old, new). ``where`` is "description" or a block index.
#
# Batch 4.6 touches only the AI index, and only the dates: batch 4.5 already rewrote the
# opening, closing and callout sentences into the "expanded several times since, most recently
# on <EXPANDED_ON>" shape, so this run changes that one date in three places and adds one
# undated sentence naming this batch's subjects. The events the index covers still run to
# 2026-09-18 -- both new articles are 2026-09-18 events -- so the callout's event date stays
# and only its expansion date moves. The block indexes are those of the index as it reads on
# 2026-09-19, after batch 4.5's inserts. The added sentence carries no article count, which
# ``COUNT_RULE["ai"]`` would otherwise refuse.
EDITS: dict[str, dict[str, list[tuple[object, str, str]]]] = {
    "crypto": {locale: [] for locale in EXPANDED},
    "tech": {locale: [] for locale in EXPANDED},
    "ai": {
        "zh-TW": [
            (0, "（最近一次 2026-09-18）", f"（最近一次 {EXPANDED_ON}）"),
            (1, "以及 Google CC 的家庭版。", "以及 Google CC 的家庭版。9 月 19 日又補上同樣發生在 9 月 18 日的消息：Anthropic 與 Accenture 合作的內嵌式評估，以及 Google Flow 在紐約時裝週的設計師工具。"),
            (24, "（最近一次 2026-09-18）", f"（最近一次 {EXPANDED_ON}）"),
            (25, "最後增補於 2026-09-18。", f"最後增補於 {EXPANDED_ON}。"),
        ],
        "en": [
            (0, "(most recently on 2026-09-18)", f"(most recently on {EXPANDED_ON})"),
            (1, "and the family version of Google's CC.", "and the family version of Google's CC. Added on September 19, both announced on September 18: Anthropic's embedded-evaluation partnership with Accenture, and the designer tools built in Google Flow for New York Fashion Week."),
            (24, "(most recently on 2026-09-18)", f"(most recently on {EXPANDED_ON})"),
            (25, "was last expanded on 2026-09-18.", f"was last expanded on {EXPANDED_ON}."),
        ],
        "ja": [
            (0, "（最終追補は2026-09-18）", f"（最終追補は{EXPANDED_ON}）"),
            (1, "Google CCの家族版です。", "Google CCの家族版です。9月19日には、同じく9月18日のニュースを追加しました。AnthropicとAccentureによる埋め込み型評価の提携と、ニューヨーク・ファッションウィーク向けにGoogle Flowで作られたデザイナー向けツールです。"),
            (24, "（最終追補は2026-09-18）", f"（最終追補は{EXPANDED_ON}）"),
            (25, "最終追補は2026-09-18です。", f"最終追補は{EXPANDED_ON}です。"),
        ],
        "ko": [
            (0, "(마지막 보완 2026-09-18)", f"(마지막 보완 {EXPANDED_ON})"),
            (1, "그리고 Google CC의 가족용 버전입니다.", "그리고 Google CC의 가족용 버전입니다. 9월 19일에는 같은 9월 18일 소식을 더 추가했습니다. Anthropic과 Accenture의 내장형 평가 협력, 그리고 뉴욕 패션위크를 위해 Google Flow로 만든 디자이너 도구입니다."),
            (24, "(마지막 보완 2026-09-18)", f"(마지막 보완 {EXPANDED_ON})"),
            (25, "마지막 보완은 2026-09-18입니다.", f"마지막 보완은 {EXPANDED_ON}입니다."),
        ],
        "zh-CN": [
            (0, "（最近一次 2026-09-18）", f"（最近一次 {EXPANDED_ON}）"),
            (1, "以及 Google CC 的家庭版。", "以及 Google CC 的家庭版。9 月 19 日又补上同样发生在 9 月 18 日的消息：Anthropic 与 Accenture 合作的内嵌式评估，以及 Google Flow 在纽约时装周的设计师工具。"),
            (24, "（最近一次 2026-09-18）", f"（最近一次 {EXPANDED_ON}）"),
            (25, "最后增补于 2026-09-18。", f"最后增补于 {EXPANDED_ON}。"),
        ],
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


# vertical -> locale -> (anchor, block). A whole block the index does not have yet: the tech
# index's prose describes every article in its group, so each group that gains articles gets
# one paragraph after its last one; the crypto index gains a United Kingdom section -- a prose
# heading and paragraph before Japan's, and a link-list heading before Japan's -- and a
# paragraph on the CFTC letter after the securities-law paragraph. The anchor names a block by
# what it is: ``link:<slug>``, ``heading:<exact text>`` or ``paragraph:<opening text>``, with a
# leading ``<`` to insert before it instead of after. Applied in order, before ``NEW``.
def _p(text: str) -> dict:
    return {"type": "paragraph", "text": text}


def _h(text: str) -> dict:
    return {"type": "heading", "level": 2, "text": text}


# vertical -> locale -> (anchor, block). Batch 4.6 inserts no new prose into any index:
# the AI index lists by month and both new links go after September's last one, which NEW
# handles on its own. Batch 4.5 filled this table for the crypto and tech indexes and those
# edits are already in the shipped packs, so re-running them would refuse.
INSERT: dict[str, dict[str, list[tuple[str, dict]]]] = {
    name: {locale: [] for locale in EXPANDED} for name in ("crypto", "tech", "ai")
}


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


def update(vertical) -> None:
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
        if list(pack["locales"]) != LOCALES:
            sys.exit(f"{slug} does not carry all five locales yet")
    already: list[str] = []

    for locale in LOCALES:
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

    path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{name}: index updated,", {locale: len(index["locales"][locale]["blocks"]) for locale in LOCALES})
    if already:
        print(f"{name}: already cited, not added again:", sorted(set(already)))
    if RETITLE[name]:
        print(f"{name}: link text refreshed in {retitle(vertical.index, RETITLE[name])} packs")


def main() -> None:
    named = [a for a in sys.argv[1:] if not a.startswith("--")]
    unknown = [n for n in named if n not in BY_NAME]
    if unknown:
        sys.exit(f"unknown vertical {unknown}; one of " + ", ".join(BY_NAME))
    chosen = [BY_NAME[n] for n in named] if named else list(VERTICALS)
    # Only the verticals this run touches: an AI sentence nobody has written yet is no reason
    # to refuse a crypto run that has nothing to do with it.
    pending = [line for vertical in chosen for line in unwritten(vertical.name)]
    if pending:
        sys.exit("edits still to write:\n - " + "\n - ".join(pending))
    for vertical in chosen:
        if not has_work(vertical.name):
            print("nothing to add:", vertical.name)
            continue
        update(vertical)


if __name__ == "__main__":
    main()
