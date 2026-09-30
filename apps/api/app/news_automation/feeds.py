from __future__ import annotations

import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
from xml.etree import ElementTree

from app.news_automation.evidence import evidence_excerpt
from app.news_automation.schemas import Entry, SourceFormat

MAX_ENTRIES = 100


def _date(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = parsedate_to_datetime(raw)
        except (TypeError, ValueError):
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _join(base_url: str, href: str) -> str | None:
    """Absolute URL, or None for an href urljoin cannot parse (e.g. "https://[broken")."""
    try:
        return urljoin(base_url, href.strip())
    except ValueError:
        return None


def _tag(value: str) -> str:
    return value.rsplit("}", 1)[-1].casefold()


def _child_text(node: ElementTree.Element, *names: str) -> str:
    wanted = set(names)
    for child in node.iter():
        if child is node:
            continue
        if _tag(child.tag) in wanted and child.text:
            return child.text.strip()
    return ""


def parse_xml_feed(body: bytes, base_url: str) -> list[Entry]:
    head = body[:2048].decode("ascii", errors="ignore").casefold()
    if "<!doctype" in head or "<!entity" in head:
        raise ValueError("XML declarations with DTD or entities are not allowed")
    root = ElementTree.fromstring(body)  # noqa: S314 - guarded above, bounded by fetcher
    rows: list[Entry] = []
    for node in root.iter():
        if _tag(node.tag) not in {"item", "entry"}:
            continue
        title = _child_text(node, "title")
        link = _child_text(node, "link")
        if not link:
            for child in node:
                if _tag(child.tag) == "link" and child.attrib.get("href"):
                    rel = child.attrib.get("rel", "alternate")
                    if rel in {"alternate", ""}:
                        link = child.attrib["href"]
                        break
        summary = _child_text(node, "summary", "description", "content")
        published = _child_text(node, "published", "updated", "pubdate", "date")
        url = _join(base_url, link) if link else None
        if title and url:
            rows.append(
                Entry(
                    title=title[:500],
                    url=url,
                    summary=_plain(summary)[:20_000],
                    published_at=_date(published),
                )
            )
        if len(rows) >= MAX_ENTRIES:
            break
    return rows


def _items_at(payload: object, path: str) -> list[object]:
    current = payload
    for part in [piece for piece in path.split(".") if piece]:
        if not isinstance(current, dict):
            return []
        current = current.get(part)
    return current if isinstance(current, list) else []


def parse_json_feed(body: bytes, base_url: str, config: dict[str, object]) -> list[Entry]:
    payload = json.loads(body)
    path = str(config.get("items_path") or "items")
    title_field = str(config.get("title_field") or "title")
    url_field = str(config.get("url_field") or "url")
    summary_field = str(config.get("summary_field") or "summary")
    date_field = str(config.get("date_field") or "date_published")
    rows: list[Entry] = []
    for raw in _items_at(payload, path)[:MAX_ENTRIES]:
        if not isinstance(raw, dict):
            continue
        title = raw.get(title_field)
        raw_url = raw.get(url_field)
        url = _join(base_url, raw_url) if isinstance(raw_url, str) else None
        if not isinstance(title, str) or url is None or not title.strip():
            continue
        summary = raw.get(summary_field)
        rows.append(
            Entry(
                title=_plain(title)[:500],
                url=url,
                summary=_plain(summary if isinstance(summary, str) else "")[:20_000],
                published_at=_date(raw.get(date_field)),
            )
        )
    return rows


class _AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.casefold() != "a":
            return
        values = dict(attrs)
        self._href = values.get("href")
        self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._text)))
            self._href = None
            self._text = []


class _LegacyArticleParser(HTMLParser):
    """The extractor every evidence hash stored before 2026-09-28 was computed with.

    It ends the capture at the first self-closing tag (``<img/>``, ``<br/>``) and pops end
    tags by depth without checking the name, so on Cloudflare, Chainalysis and SEC pages it
    kept a tag list or site navigation instead of the story. The publish revalidation
    (``validation._legacy_match``) still compares against it when its authenticated text
    covers the entire current story. Truncated legacy captures require fresh evidence.
    Once no such candidate waits (retention clears them after 90 days) this class can go.
    """

    _void_tags = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(self, config: dict[str, object]) -> None:
        super().__init__(convert_charrefs=True)
        raw_tags = config.get("article_tags", ["article", "main"])
        raw_ids = config.get("article_ids", [])
        raw_classes = config.get("article_classes", [])
        self.tags = (
            {str(value).casefold() for value in raw_tags}
            if isinstance(raw_tags, list)
            else {"article", "main"}
        )
        self.ids = {str(value) for value in raw_ids} if isinstance(raw_ids, list) else set()
        self.classes = (
            {str(value) for value in raw_classes} if isinstance(raw_classes, list) else set()
        )
        self.depth = 0
        self.capture_depths: list[int] = []
        self.text: list[str] = []
        self.links: list[str] = []
        self.title = ""
        self._title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        lowered = tag.casefold()
        if lowered not in self._void_tags:
            self.depth += 1
        values = dict(attrs)
        element_classes = set((values.get("class") or "").split())
        if (
            lowered in self.tags
            or (values.get("id") or "") in self.ids
            or bool(element_classes & self.classes)
        ):
            self.capture_depths.append(self.depth)
        if lowered == "title":
            self._title = True
        if lowered == "a" and self.capture_depths:
            href = values.get("href")
            if href:
                self.links.append(href)

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.casefold()
        if lowered == "title":
            self._title = False
        if self.capture_depths and self.capture_depths[-1] == self.depth:
            self.capture_depths.pop()
        if lowered not in self._void_tags and self.depth:
            self.depth -= 1

    def handle_data(self, data: str) -> None:
        if self._title and not self.title:
            self.title = _plain(data)
        if self.capture_depths:
            value = _plain(data)
            if value:
                self.text.append(value)


# Subtrees that are never the story: scripts carry per-render ids, and navigation, tag
# lists, share buttons and "most popular" rails change between renders or crowd the
# story out of the 8,000-character excerpt.
SKIPPED_TAGS = frozenset(
    {
        "script",
        "style",
        "noscript",
        "template",
        "svg",
        "iframe",
        "nav",
        "aside",
        "footer",
        "form",
        "button",
        "select",
    }
)


# The elements whose text is the story itself, for the body fingerprint. Loose text in a
# <div> or <span> (bylines, relative times, "most popular" counters) is left out, and each
# element's text is taken whole, so a link wrapped around other words does not split it.
BODY_TAGS = frozenset(
    {
        "p",
        "li",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "blockquote",
        "pre",
        "td",
        "th",
        "dd",
        "dt",
        "figcaption",
    }
)


class _ArticleParser(HTMLParser):
    _void_tags = _LegacyArticleParser._void_tags

    def __init__(self, config: dict[str, object]) -> None:
        super().__init__(convert_charrefs=True)
        self.tags = _names(config.get("article_tags", ["article", "main"]), {"article", "main"})
        self.ids = _values(config.get("article_ids", []))
        self.classes = _values(config.get("article_classes", []))
        self.skip_tags = SKIPPED_TAGS | _names(config.get("exclude_tags", []), set())
        self.skip_ids = _values(config.get("exclude_ids", []))
        self.skip_classes = _values(config.get("exclude_classes", []))
        # Open elements by name. An end tag closes up to its nearest open namesake, so an
        # unclosed <p> or <li> neither ends the region early nor keeps it open past its end.
        self.stack: list[str] = []
        self.capture_depths: list[int] = []
        self.skip_depths: list[int] = []
        self.text: list[str] = []
        self.links: list[str] = []
        self.title = ""
        self._title = False
        # Body fingerprint inputs: whole story elements, the first page <h1> outside the
        # skipped chrome (a story region often starts below it), and JSON-LD blocks.
        self.paragraphs: list[str] = []
        self.headline = ""
        self.json_ld: list[str] = []
        self._body_open: list[tuple[int, list[str]]] = []
        self._h1: tuple[int, list[str]] | None = None
        self._json_ld: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._start(tag, attrs, closed=False)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # "<br/>" or "<img/>": an element with nothing inside, never an end of the region.
        self._start(tag, attrs, closed=True)

    def _start(self, tag: str, attrs: list[tuple[str, str | None]], *, closed: bool) -> None:
        lowered = tag.casefold()
        values = dict(attrs)
        element_id = values.get("id") or ""
        element_classes = set((values.get("class") or "").split())
        if lowered == "title":
            self._title = not closed
        if closed or lowered in self._void_tags:
            if lowered == "a":
                self._link(values)
            return
        self.stack.append(lowered)
        depth = len(self.stack)
        if (
            lowered in self.skip_tags
            or element_id in self.skip_ids
            or bool(element_classes & self.skip_classes)
        ):
            self.skip_depths.append(depth)
        elif (
            lowered in self.tags or element_id in self.ids or bool(element_classes & self.classes)
        ):
            self.capture_depths.append(depth)
        if lowered == "script" and "ld+json" in (values.get("type") or "").casefold():
            self._json_ld = []
        if not self.skip_depths:
            if lowered == "h1" and self._h1 is None and not self.headline:
                self._h1 = (depth, [])
            if lowered in BODY_TAGS and self.capture_depths:
                self._body_open.append((depth, []))
        if lowered == "a":
            self._link(values)

    def _link(self, values: dict[str, str | None]) -> None:
        href = values.get("href")
        if href and self.capture_depths and not self.skip_depths:
            self.links.append(href)

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.casefold()
        if lowered == "title":
            self._title = False
        if lowered == "script" and self._json_ld is not None:
            self.json_ld.append("".join(self._json_ld))
            self._json_ld = None
        if lowered not in self.stack:
            return
        while self.stack:
            closed = self.stack.pop()
            depth = len(self.stack) + 1
            self._close_body(depth)
            while self.capture_depths and self.capture_depths[-1] >= depth:
                self.capture_depths.pop()
            while self.skip_depths and self.skip_depths[-1] >= depth:
                self.skip_depths.pop()
            if closed == lowered:
                break

    def _close_body(self, depth: int) -> None:
        while self._body_open and self._body_open[-1][0] >= depth:
            _, chunks = self._body_open.pop()
            value = " ".join("".join(chunks).split())
            if value:
                self.paragraphs.append(value)
        if self._h1 is not None and self._h1[0] >= depth:
            self.headline = " ".join("".join(self._h1[1]).split())
            self._h1 = None

    def finish(self) -> None:
        """Take what the page left open, so an unclosed last <p> still counts.

        Deliberately not ``close()``: that would flush trailing text into ``text`` and
        change the ``content_hash`` of every page stored before the body fingerprint.
        """
        self._close_body(1)

    def handle_data(self, data: str) -> None:
        if self._title and not self.title:
            self.title = _plain(data)
        if self._json_ld is not None:
            self._json_ld.append(data)
        if self.skip_depths:
            return
        if self._h1 is not None:
            self._h1[1].append(data)
        if self.capture_depths:
            if self._body_open:
                self._body_open[-1][1].append(data)
            value = _plain(data)
            if value:
                self.text.append(value)


def _names(raw: object, default: set[str]) -> set[str]:
    return {str(value).casefold() for value in raw} if isinstance(raw, list) else default


def _values(raw: object) -> set[str]:
    return {str(value) for value in raw} if isinstance(raw, list) else set()


def _plain(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", value)).strip()


def parse_html_listing(body: bytes, base_url: str, config: dict[str, object]) -> list[Entry]:
    parser = _AnchorParser()
    parser.feed(body.decode("utf-8", errors="replace"))
    raw_include = config.get("include_path_prefixes", [])
    raw_exclude = config.get("exclude_path_prefixes", [])
    include = [str(value) for value in raw_include] if isinstance(raw_include, list) else []
    exclude = [str(value) for value in raw_exclude] if isinstance(raw_exclude, list) else []
    query_include = _strings(config.get("include_query_contains"))
    raw_minimum = config.get("minimum_title_length", 12)
    minimum = int(raw_minimum) if isinstance(raw_minimum, (int, str)) else 12
    seen: set[str] = set()
    rows: list[Entry] = []
    for href, raw_title in parser.links:
        joined = _join(base_url, href)
        if joined is None:
            continue
        url = joined
        parsed = urlsplit(url)
        title = _plain(raw_title)
        if parsed.scheme != "https" or not title or len(title) < minimum:
            continue
        if include and not any(parsed.path.startswith(prefix) for prefix in include):
            continue
        # Sites that serve every page from one script (the FSC's /ch/home.jsp) tell a news
        # item from the menu only by its query string.
        if query_include and not any(fragment in parsed.query for fragment in query_include):
            continue
        if any(parsed.path.startswith(prefix) for prefix in exclude) or url in seen:
            continue
        seen.add(url)
        rows.append(Entry(title=title[:500], url=url))
        if len(rows) >= MAX_ENTRIES:
            break
    return rows


@dataclass(frozen=True)
class Article:
    """One page read with the current extractor.

    ``text`` is the story region line by line (what ``content_hash`` covers). The rest
    feeds ``policy.body_fingerprint``: whole story elements, the page headline, the
    JSON-LD ``articleBody`` and the size of the region they were taken from.
    """

    title: str
    text: str
    links: list[str]
    headline: str = ""
    paragraphs: tuple[str, ...] = ()
    article_body: str = ""
    region_characters: int = 0


def _article_body(blocks: list[str]) -> str:
    """The first JSON-LD ``articleBody`` string on the page, or "" when there is none."""

    def find(node: object) -> str:
        if isinstance(node, dict):
            value = node.get("articleBody")
            if isinstance(value, str) and value.strip():
                return value
            nodes: Iterable[object] = node.values()
        elif isinstance(node, list):
            nodes = node
        else:
            return ""
        for child in nodes:
            found = find(child)
            if found:
                return found
        return ""

    for block in blocks:
        try:
            payload = json.loads(block)
            found = find(payload)
        except (ValueError, RecursionError):
            continue
        if found:
            return found
    return ""


def read_article(
    body: bytes, base_url: str, config: dict[str, object] | None = None
) -> Article:
    """Title, story text, in-story links and body-fingerprint inputs of one page."""

    parser = _ArticleParser(config or {})
    parser.feed(body.decode("utf-8", errors="replace"))
    parser.finish()
    text = "\n".join(parser.text)
    links = [url for url in (_join(base_url, href) for href in parser.links) if url]
    return Article(
        title=parser.title[:500],
        text=evidence_excerpt(text),
        links=links,
        headline=parser.headline,
        paragraphs=tuple(parser.paragraphs),
        article_body=_article_body(parser.json_ld),
        region_characters=sum(len(line) for line in parser.text),
    )


def extract_article(
    body: bytes,
    base_url: str,
    config: dict[str, object] | None = None,
    *,
    legacy: bool = False,
) -> tuple[str, str, list[str]]:
    """Title, story text and in-story links of one page.

    ``legacy`` reproduces the pre-2026-09-28 extractor, only so evidence stored with it can
    still be compared (see ``_LegacyArticleParser``).
    """

    if not legacy:
        article = read_article(body, base_url, config)
        return article.title, article.text, article.links
    parser = _LegacyArticleParser(config or {})
    parser.feed(body.decode("utf-8", errors="replace"))
    text = "\n".join(parser.text)
    links = [url for url in (_join(base_url, href) for href in parser.links) if url]
    return parser.title[:500], evidence_excerpt(text), links


def _strings(value: object) -> list[str]:
    return [str(item) for item in value if str(item)] if isinstance(value, list) else []


def parse_entries(
    body: bytes, source_format: SourceFormat, base_url: str, config: dict[str, object]
) -> list[Entry]:
    if source_format in {"rss", "atom"}:
        entries = parse_xml_feed(body, base_url)
    elif source_format in {"json", "api"}:
        entries = parse_json_feed(body, base_url, config)
    else:
        entries = parse_html_listing(body, base_url, config)
    # A publisher whose feed is mostly outside the three verticals (Taiwan's FSC: funds,
    # insurance, statistics) is read only for the entries whose title names one of them.
    keywords = [word.casefold() for word in _strings(config.get("include_title_keywords"))]
    if keywords:
        entries = [row for row in entries if any(word in row.title.casefold() for word in keywords)]
    return entries
