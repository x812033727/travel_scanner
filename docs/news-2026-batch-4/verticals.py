"""The three verticals of news batch 4, and the block shapes the five scripts here share.

Batch 3 was one vertical in one workspace, so ``ai-news-*``, ``docs/ai-news-2026-09-mid`` and
the January–September index were spelled out in every script. Batch 4 has three verticals with
three workspaces and three indexes, and all five scripts need the same answer to "which
vertical is this slug", so they import it from here instead of each carrying a copy that can
drift. Importing this module also puts ``apps/api`` on ``sys.path``, which every script needs.

Not a package and not installed: the scripts sit beside this file, and Python puts a script's
own directory on ``sys.path`` first, so ``import verticals`` works from any working directory.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _root() -> Path:
    """The repository root: two levels above this file once these scripts sit in
    ``docs/news-2026-batch-4``. ``MOKAAIR_ROOT`` overrides it, which is how the batch's tooling
    is exercised from a scratchpad before it is moved into the repository."""
    override = os.environ.get("MOKAAIR_ROOT")
    return Path(override).resolve() if override else HERE.parents[1]


ROOT = _root()
sys.path.insert(0, str(ROOT / "apps/api"))

CONTENT = ROOT / "apps/api/app/guides/content"
PUBLIC = ROOT / "apps/web/public"
LOCALES = ["zh-TW", "en", "ja", "ko", "zh-CN"]


@dataclass(frozen=True)
class Vertical:
    name: str
    #: Slug prefix. Every slug is ``<prefix><topic>-<YYYYMMDD>`` with the event date at the end.
    prefix: str
    #: Where the research records, the manifest and the contact sheets of this vertical live.
    workspace: str
    #: The index article the first closing link points at.
    index: str
    #: The topics every article of this vertical carries, hub first. An article may carry more
    #: (``gadgets``, ``software``); it may not carry fewer. Checked against the real taxonomy.
    topics: tuple[str, ...]
    #: Printed top-left on every hero, and the accent the vertical is drawn in. The colour must
    #: be one of the album's six palette constants; ``build_assets.py`` asserts that it is.
    eyebrow: str
    accent: str
    #: ``display_order`` of this vertical's first article of the batch. ``ai.md`` continues from
    #: 148 (``ai-news-siri-ai-ios-27-20260914``). The owner has not assigned a band to the two
    #: new verticals, and guessing one is how two series end up interleaved on the hub page, so
    #: theirs stays ``None`` and ``check_article.py`` only demands the field was set on purpose.
    order_base: int | None


VERTICALS = (
    Vertical(
        name="crypto",
        prefix="crypto-news-",
        workspace="docs/crypto-news-2026",
        index="crypto-news-2026-index",
        topics=("finance", "crypto"),
        eyebrow="MOKAAIR  /  CRYPTO NEWS",
        accent="#D97A2B",  # ORANGE
        # The owner's band, 2026-09-17. 200 upwards was wholly unused: 110-196 is the crowded
        # tutorial and series range (119 packs there already interleave with the AI news run,
        # which is 100-148 and continues at 149), so a fresh hundred keeps this series whole
        # and leaves it about a hundred slots of headroom. Tech has 300 for the same reason.
        order_base=200,
    ),
    Vertical(
        name="tech",
        prefix="tech-news-",
        workspace="docs/tech-news-2026",
        index="tech-news-2026-index",
        topics=("tech", "tech-news"),
        eyebrow="MOKAAIR  /  TECH NEWS",
        accent="#2F6F9F",  # BLUE
        # The band the crypto comment above already names for this vertical: 300-312 in the
        # order of `check_article.RELATED`, the index at 299.
        order_base=300,
    ),
    Vertical(
        name="ai",
        prefix="ai-news-",
        workspace="docs/ai-news-2026-09-late",
        # Frozen URL: docs/article-architecture.md keeps every existing URL, so the index is
        # retitled in place and never renamed. See update_index.py.
        index="ai-news-2026-january-september-index",
        topics=("ai", "ai-news"),
        eyebrow="MOKAAIR  /  AI NEWS",
        accent="#0D6B68",  # TEAL
        order_base=149,
    ),
)
BY_NAME = {vertical.name: vertical for vertical in VERTICALS}


def vertical_of(slug: str) -> Vertical:
    for vertical in VERTICALS:
        if slug.startswith(vertical.prefix):
            return vertical
    raise SystemExit(f"{slug}: no vertical; the prefix is one of " + ", ".join(v.prefix for v in VERTICALS))


def workspace_of(slug: str) -> Path:
    return ROOT / vertical_of(slug).workspace


def event_date_of(slug: str) -> str:
    """The event date the slug ends in, as ``YYYY-MM-DD``. Also the pack's ``news_date``."""
    stamp = slug[-8:]
    if not stamp.isdigit():
        raise SystemExit(f"{slug}: the slug ends in the event date, YYYYMMDD")
    value = f"{stamp[:4]}-{stamp[4:6]}-{stamp[6:]}"
    try:
        date.fromisoformat(value)
    except ValueError:
        raise SystemExit(f"{slug}: {value} is not a date") from None
    return value


def suffix(locale: str) -> str:
    return "" if locale == "zh-TW" else "-" + locale.lower()


def chinese_date(value: str) -> str:
    """``2026-06-30`` → ``2026 年 6 月 30 日``, the form the opening paragraphs are written in."""
    y, m, d = (int(part) for part in value.split("-"))
    return f"{y} 年 {m} 月 {d} 日"


# --- block shapes, after relink and autolink ----------------------------------------------
#
# ``pack_cli relink`` and ``pack_cli autolink`` run after the content is final (BRIEF.md,
# "站內連結"). They rewrite a paragraph that gained an article inline into a ``rich_paragraph``,
# and the two closing ``link`` blocks into ``rich_paragraph``s holding a single ``article``
# inline -- per locale, so zh-TW and en of the same article legitimately end up with different
# raw block types. Batch 3's checker predates them and now fails its own shipped articles on
# "two opening paragraphs", "blocks must end callout, link, link" and "en block types differ
# from zh-TW". Everything here therefore compares the block's *role*, not its stored type.

LINK_INLINES = ("article", "link")


def block_kind(block: dict) -> str:
    """What the block is for: a ``rich_paragraph`` of nothing but links is one of the two
    closing links, any other ``rich_paragraph`` is a paragraph, everything else is itself."""
    if block["type"] != "rich_paragraph":
        return block["type"]
    if all(node["type"] in LINK_INLINES for node in block["inlines"]):
        return "link"
    return "paragraph"


def block_text(block: dict) -> str:
    """The reader-visible text of a paragraph-shaped block, rich or plain."""
    if block["type"] == "rich_paragraph":
        return "".join(node["text"] for node in block["inlines"])
    return block.get("text", "")


def link_of(block: dict, locale: str) -> tuple[str | None, str]:
    """``(target slug, link text)`` of a closing link, whichever form it is stored in."""
    if block["type"] == "link":
        return _slug_of_url(block["url"], locale), block.get("text", "")
    nodes = block["inlines"]
    if len(nodes) != 1:
        return None, block_text(block)
    node = nodes[0]
    if node["type"] == "article":
        return node["slug"], node["text"]
    return _slug_of_url(node.get("url", ""), locale), node["text"]


def _slug_of_url(url: str, locale: str) -> str | None:
    prefix = f"https://mokaair.com/{locale}/life/"
    return url[len(prefix):] if url.startswith(prefix) else None


# --- the crypto disclaimer, per locale ----------------------------------------------------

_LOCALE_MARKER = {
    "zh-TW": "不是投資建議",
    "zh-CN": "不是投资建议",
    "en": "not investment advice",
    "ja": "投資助言ではありません",
    "ko": "투자 조언이 아닙니다",
}


def locale_markers() -> dict[str, str]:
    """``crypto.md``'s table of disclaimer markers, keyed by locale.

    ``lint_document`` accepts any of the five in any locale, because it lints one document at a
    time and is not told which locale it is reading: a translation that kept the zh-TW sentence
    would pass the linter and still read as untranslated boilerplate. The brief asks for the
    stricter rule, so the batch's own tooling checks the locale's own marker -- cross-checked
    against the real tuple here, so a marker edited in ``pack_ingest`` cannot silently disagree
    with this file. Imported inside the function so the scripts that never touch the API
    environment can still import this module."""
    from app.guides.pack_ingest import FINANCE_DISCLAIMER_MARKERS

    assert set(_LOCALE_MARKER) == set(LOCALES), _LOCALE_MARKER
    assert set(_LOCALE_MARKER.values()) == set(FINANCE_DISCLAIMER_MARKERS), _LOCALE_MARKER
    return _LOCALE_MARKER
