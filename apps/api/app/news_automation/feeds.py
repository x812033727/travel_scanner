from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
from xml.etree import ElementTree

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
        if title and link:
            rows.append(
                Entry(
                    title=title[:500],
                    url=urljoin(base_url, link),
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
        url = raw.get(url_field)
        if not isinstance(title, str) or not isinstance(url, str) or not title.strip():
            continue
        summary = raw.get(summary_field)
        rows.append(
            Entry(
                title=_plain(title)[:500],
                url=urljoin(base_url, url),
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


class _ArticleParser(HTMLParser):
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


def _plain(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", value)).strip()


def parse_html_listing(body: bytes, base_url: str, config: dict[str, object]) -> list[Entry]:
    parser = _AnchorParser()
    parser.feed(body.decode("utf-8", errors="replace"))
    raw_include = config.get("include_path_prefixes", [])
    raw_exclude = config.get("exclude_path_prefixes", [])
    include = [str(value) for value in raw_include] if isinstance(raw_include, list) else []
    exclude = [str(value) for value in raw_exclude] if isinstance(raw_exclude, list) else []
    raw_minimum = config.get("minimum_title_length", 12)
    minimum = int(raw_minimum) if isinstance(raw_minimum, (int, str)) else 12
    seen: set[str] = set()
    rows: list[Entry] = []
    for href, raw_title in parser.links:
        url = urljoin(base_url, href)
        parsed = urlsplit(url)
        title = _plain(raw_title)
        if parsed.scheme != "https" or not title or len(title) < minimum:
            continue
        if include and not any(parsed.path.startswith(prefix) for prefix in include):
            continue
        if any(parsed.path.startswith(prefix) for prefix in exclude) or url in seen:
            continue
        seen.add(url)
        rows.append(Entry(title=title[:500], url=url))
        if len(rows) >= MAX_ENTRIES:
            break
    return rows


def extract_article(
    body: bytes, base_url: str, config: dict[str, object] | None = None
) -> tuple[str, str, list[str]]:
    parser = _ArticleParser(config or {})
    parser.feed(body.decode("utf-8", errors="replace"))
    text = "\n".join(parser.text)
    return parser.title[:500], text[:40_000], [urljoin(base_url, url) for url in parser.links]


def parse_entries(
    body: bytes, source_format: SourceFormat, base_url: str, config: dict[str, object]
) -> list[Entry]:
    if source_format in {"rss", "atom"}:
        return parse_xml_feed(body, base_url)
    if source_format in {"json", "api"}:
        return parse_json_feed(body, base_url, config)
    return parse_html_listing(body, base_url, config)
