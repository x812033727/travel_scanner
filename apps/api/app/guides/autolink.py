"""Linking articles to each other inside the content packs, as a reviewable diff.

Two rewrites, both pure functions over a pack's raw JSON so ``pack_cli`` can print what
would change and write exactly that:

``relink`` turns a raw site URL (``https://mokaair.com/zh-TW/life/<slug>``, in a ``link``
block or a ``link`` inline) into an ``article`` inline. A raw URL is a string: it stays a
link when its target is withdrawn, names whatever kind it likes, and is invisible to the
link graph. An ``article`` inline renders only while the target is published in the
reader's language, is checked against the target's kind, and is what
``guide_article_links`` is built from.

``autolink`` links the first mention of a glossary term or a suffix keyword to the article
that defines it, once per target and at most a few per article, so a reader meets the
definition where the word first appears. Only prose is touched -- a ``paragraph`` block or
a ``text`` inline -- never a heading, a list, a table, a callout or code. The rules are
deterministic and a second run is a no-op, since the linked words now sit inside an
``article`` inline where the matcher does not look.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, cast

from app.guides.aliases import SeedAlias, keyword_aliases, term_aliases
from app.guides.content_pack import default_directory
from app.guides.schemas import Kind

#: An article's address on the site, as a raw URL in a pack. Group 1 is the kind for a
#: travel article (empty for ``life/``), group 2 the slug. Anchored to the locale prefix
#: so the web-only series routes (``/guides/codex-…``) never match.
SITE_LINK = re.compile(
    r"https://mokaair\.com/(?:en|ja|ko|zh-CN|zh-TW)/(?:life/|guides/(howto|intel)/)([a-z0-9-]+)"
)

MAX_AUTOLINKS = 8
MIN_ALIAS_LENGTH = 2
#: Inline caps of ``RichParagraphBlock`` and ``TextInline`` (``schemas.py``): a paragraph
#: is split only while the result still validates.
MAX_INLINES = 80
MAX_INLINE_TEXT = 4000

Locale = str


@dataclass(frozen=True)
class SiteLink:
    kind: Kind
    slug: str
    #: What follows the slug: empty, a query string or a fragment.
    remainder: str


def parse_site_link(url: str) -> SiteLink | None:
    match = SITE_LINK.match(url)
    if match is None:
        return None
    kind = cast(Kind, match.group(1) or "life")
    return SiteLink(kind, match.group(2), url[match.end() :])


def pack_kinds(directory: Path | None = None) -> dict[str, Kind]:
    """slug -> kind for every shipped pack, from the file name and the ``kind`` key alone."""
    root = directory or default_directory()
    kinds: dict[str, Kind] = {}
    for path in sorted(root.glob("*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        kinds[path.stem] = raw.get("kind", "life")
    return kinds


# --- relink -------------------------------------------------------------------


@dataclass
class RelinkReport:
    converted: int = 0
    #: ``(locale, url, reason)`` for every site link left as it was.
    kept: list[tuple[str, str, str]] = field(default_factory=list)


def _article_inline(text: str, link: SiteLink) -> dict[str, Any]:
    return {"type": "article", "text": text, "kind": link.kind, "slug": link.slug}


def _keep_reason(link: SiteLink | None, *, self_slug: str, kinds: dict[str, Kind]) -> str | None:
    """Why a site URL stays a raw link, or ``None`` when it may become an article inline."""
    if link is None:
        return "not_an_article"
    if link.remainder and not link.remainder.startswith(("?", "#")):
        return "not_an_article"
    if link.slug == self_slug:
        return "self_link"
    kind = kinds.get(link.slug)
    if kind is None:
        return "no_pack"
    if kind != link.kind:
        return "wrong_kind"
    return None


def relink_document(
    document: dict[str, Any], *, self_slug: str, kinds: dict[str, Kind], locale: str
) -> tuple[dict[str, Any], RelinkReport]:
    """The document with its convertible site URLs turned into article inlines."""
    report = RelinkReport()
    blocks: list[dict[str, Any]] = []
    for block in document.get("blocks", []):
        kind = block.get("type")
        if (
            kind == "link"
            and isinstance(block.get("url"), str)
            and block["url"].startswith("https://mokaair.com/")
        ):
            link = parse_site_link(block["url"])
            reason = _keep_reason(link, self_slug=self_slug, kinds=kinds)
            if reason is None and link is not None:
                report.converted += 1
                blocks.append(
                    {"type": "rich_paragraph", "inlines": [_article_inline(block["text"], link)]}
                )
                continue
            report.kept.append((locale, block["url"], reason or "not_an_article"))
            blocks.append(block)
            continue
        if kind == "rich_paragraph":
            inlines: list[dict[str, Any]] = []
            for node in block.get("inlines", []):
                if (
                    node.get("type") == "link"
                    and isinstance(node.get("url"), str)
                    and node["url"].startswith("https://mokaair.com/")
                ):
                    link = parse_site_link(node["url"])
                    reason = _keep_reason(link, self_slug=self_slug, kinds=kinds)
                    if reason is None and link is not None:
                        report.converted += 1
                        inlines.append(_article_inline(node["text"], link))
                        continue
                    report.kept.append((locale, node["url"], reason or "not_an_article"))
                inlines.append(node)
            blocks.append({**block, "inlines": inlines})
            continue
        blocks.append(block)
    return {**document, "blocks": blocks}, report


# --- autolink -----------------------------------------------------------------


@dataclass(frozen=True)
class Term:
    alias: str
    slug: str
    kind: Kind
    pattern: re.Pattern[str]


def _pattern(alias: str) -> re.Pattern[str]:
    """ASCII words need boundaries (``AI`` must not link inside ``OpenAI``) and case does
    not matter to them; a name with CJK in it is matched as written, since CJK text has
    no word boundaries to respect and no case to fold."""
    if alias.isascii():
        return re.compile(rf"(?<![A-Za-z0-9_]){re.escape(alias)}(?![A-Za-z0-9_])", re.IGNORECASE)
    return re.compile(re.escape(alias))


@dataclass
class AliasIndex:
    """Per locale, the names that point at exactly one article, longest first."""

    terms: dict[str, list[Term]]

    @classmethod
    def build(
        cls,
        directory: Path | None = None,
        *,
        terms_file: Path | None = None,
        keywords_file: Path | None = None,
        kinds: dict[str, Kind] | None = None,
    ) -> AliasIndex:
        root = directory or default_directory()
        known = kinds if kinds is not None else pack_kinds(root)
        rows: list[SeedAlias] = [
            *term_aliases(terms_file, root),
            *keyword_aliases(keywords_file, root),
            *_pack_aliases(root),
        ]
        # A name several articles share is a search hint, not a link target.
        owners: dict[tuple[str, str], set[str]] = {}
        for row in rows:
            owners.setdefault((row.locale, row.alias_norm), set()).add(row.slug)
        by_locale: dict[str, dict[str, Term]] = {}
        for row in rows:
            alias = " ".join(row.alias.split())
            key = (row.locale, row.alias_norm)
            if len(owners[key]) != 1 or len(alias) < MIN_ALIAS_LENGTH or row.slug not in known:
                continue
            by_locale.setdefault(row.locale, {}).setdefault(
                row.alias_norm, Term(alias, row.slug, known[row.slug], _pattern(alias))
            )
        return cls(
            {
                locale: sorted(items.values(), key=lambda term: (-len(term.alias), term.alias))
                for locale, items in by_locale.items()
            }
        )


def _pack_aliases(root: Path) -> list[SeedAlias]:
    rows: list[SeedAlias] = []
    for path in sorted(root.glob("*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        for locale, names in (raw.get("aliases") or {}).items():
            rows.extend(SeedAlias(path.stem, locale, name, "editor") for name in names)
    return rows


@dataclass(frozen=True)
class Linked:
    locale: str
    alias: str
    slug: str


def _linked_targets(document: dict[str, Any]) -> set[str]:
    return {
        node["slug"]
        for block in document.get("blocks", [])
        if block.get("type") == "rich_paragraph"
        for node in block.get("inlines", [])
        if node.get("type") == "article" and isinstance(node.get("slug"), str)
    }


def _split(
    text: str, terms: list[Term], done: set[str], budget: int, linked: list[Linked], locale: str
) -> list[dict[str, Any]]:
    """``text`` as inlines, with the first mention of each still-unlinked term turned into
    an article inline. Terms are tried longest first, so ``machine learning`` wins over
    ``learning``; each term links once per document; the budget is what is left of the
    per-article cap."""
    nodes: list[dict[str, Any]] = []
    cursor = 0
    while cursor < len(text) and len(linked) < budget:
        best: tuple[int, Term, re.Match[str]] | None = None
        for term in terms:
            if term.slug in done:
                continue
            match = term.pattern.search(text, cursor)
            if match is not None and (best is None or match.start() < best[0]):
                best = (match.start(), term, match)
        if best is None:
            break
        start, term, match = best
        if start > cursor:
            nodes.append({"type": "text", "text": text[cursor:start]})
        nodes.append(
            {"type": "article", "text": match.group(0), "kind": term.kind, "slug": term.slug}
        )
        done.add(term.slug)
        linked.append(Linked(locale, term.alias, term.slug))
        cursor = match.end()
    if cursor < len(text):
        nodes.append({"type": "text", "text": text[cursor:]})
    return nodes


def autolink_document(
    document: dict[str, Any],
    *,
    locale: str,
    self_slug: str,
    index: AliasIndex,
    limit: int = MAX_AUTOLINKS,
) -> tuple[dict[str, Any], list[Linked]]:
    """The document with its first mentions of known names linked, and what was linked."""
    terms = [term for term in index.terms.get(locale, []) if term.slug != self_slug]
    if not terms:
        return document, []
    done = _linked_targets(document)
    linked: list[Linked] = []
    blocks: list[dict[str, Any]] = []
    for block in document.get("blocks", []):
        if len(linked) >= limit:
            blocks.append(block)
            continue
        if block.get("type") == "paragraph" and isinstance(block.get("text"), str):
            nodes = _split(block["text"], terms, done, limit, linked, locale)
            if any(node["type"] == "article" for node in nodes) and _fits(nodes):
                blocks.append({"type": "rich_paragraph", "inlines": nodes})
            else:
                _unlink(nodes, done, linked)
                blocks.append(block)
            continue
        if block.get("type") == "rich_paragraph":
            inlines: list[dict[str, Any]] = []
            changed = False
            for node in block.get("inlines", []):
                if (
                    node.get("type") == "text"
                    and isinstance(node.get("text"), str)
                    and len(linked) < limit
                ):
                    nodes = _split(node["text"], terms, done, limit, linked, locale)
                    if any(item["type"] == "article" for item in nodes):
                        inlines.extend(nodes)
                        changed = True
                        continue
                inlines.append(node)
            if changed and _fits(inlines):
                blocks.append({**block, "inlines": inlines})
            else:
                if changed:
                    _unlink(
                        [node for node in inlines if node not in block.get("inlines", [])],
                        done,
                        linked,
                    )
                blocks.append(block)
            continue
        blocks.append(block)
    return {**document, "blocks": blocks}, linked


def _fits(nodes: list[dict[str, Any]]) -> bool:
    return (
        len(nodes) <= MAX_INLINES
        and all(len(node.get("text", "")) <= MAX_INLINE_TEXT for node in nodes)
        and sum(len(node.get("text", "")) for node in nodes) <= MAX_INLINE_TEXT
    )


def _unlink(nodes: list[dict[str, Any]], done: set[str], linked: list[Linked]) -> None:
    """Take back the links of a block that could not be rewritten within the limits."""
    for node in nodes:
        if node.get("type") == "article":
            done.discard(node["slug"])
            for index, item in enumerate(linked):
                if item.slug == node["slug"]:
                    del linked[index]
                    break


# --- the command ------------------------------------------------------------------

Mode = Literal["relink", "autolink"]


@dataclass
class Proposal:
    slug: str
    mode: Mode
    #: locale -> the rewritten document, for the locales that changed.
    documents: dict[str, dict[str, Any]] = field(default_factory=dict)
    converted: int = 0
    kept: list[tuple[str, str, str]] = field(default_factory=list)
    linked: list[Linked] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        return bool(self.documents)


def proposals(
    directory: Path | None = None,
    mode: Mode = "relink",
    *,
    kind: Kind | None = None,
    prefixes: tuple[str, ...] = (),
    slugs: set[str] | None = None,
    limit: int = MAX_AUTOLINKS,
    terms_file: Path | None = None,
    keywords_file: Path | None = None,
) -> list[Proposal]:
    root = directory or default_directory()
    kinds = pack_kinds(root)
    index = (
        AliasIndex.build(root, terms_file=terms_file, keywords_file=keywords_file, kinds=kinds)
        if mode == "autolink"
        else None
    )
    rows: list[Proposal] = []
    for path in sorted(root.glob("*.json")):
        slug = path.stem
        if slugs is not None and slug not in slugs:
            continue
        if prefixes and not any(slug.startswith(prefix) for prefix in prefixes):
            continue
        if kind is not None and kinds.get(slug) != kind:
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        row = Proposal(slug, mode)
        for locale, document in raw.get("locales", {}).items():
            if mode == "relink":
                rewritten, report = relink_document(
                    document, self_slug=slug, kinds=kinds, locale=locale
                )
                row.converted += report.converted
                row.kept.extend(report.kept)
                if report.converted:
                    row.documents[locale] = rewritten
            else:
                assert index is not None
                rewritten, linked = autolink_document(
                    document, locale=locale, self_slug=slug, index=index, limit=limit
                )
                row.linked.extend(linked)
                if linked:
                    row.documents[locale] = rewritten
        rows.append(row)
    return rows


def render_table(rows: list[Proposal]) -> str:
    """A Markdown table of what changes, for a pull request description or an editor's
    review; unchanged packs are summarised in one line."""
    changed = [row for row in rows if row.changed]
    if rows and rows[0].mode == "relink":
        lines = ["| slug | converted | kept |", "| --- | --- | --- |"]
        for row in changed:
            kept = "; ".join(f"{url} ({reason})" for _, url, reason in row.kept) or "-"
            lines.append(f"| `{row.slug}` | {row.converted} | {kept} |")
        total = sum(row.converted for row in rows)
        kept_total = sum(len(row.kept) for row in rows)
        lines.extend(
            [
                "",
                f"{len(changed)} of {len(rows)} packs would change: "
                f"{total} links converted, {kept_total} kept",
            ]
        )
    else:
        lines = ["| slug | linked |", "| --- | --- |"]
        for row in changed:
            lines.append(
                f"| `{row.slug}` | "
                + "; ".join(f"{item.locale}: {item.alias} → `{item.slug}`" for item in row.linked)
                + " |"
            )
        total = sum(len(row.linked) for row in rows)
        lines.extend(["", f"{len(changed)} of {len(rows)} packs would change: {total} links added"])
    return "\n".join(lines)


def apply(rows: list[Proposal], directory: Path | None = None) -> list[Path]:
    """Rewrite the ``blocks`` of every changed locale, and nothing else. Every shipped pack
    round-trips through ``json.dumps(indent=2)`` unchanged, so the diff is the links."""
    root = directory or default_directory()
    written: list[Path] = []
    for row in rows:
        if not row.changed:
            continue
        path = root / f"{row.slug}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for locale, document in row.documents.items():
            data["locales"][locale]["blocks"] = document["blocks"]
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append(path)
    return written
