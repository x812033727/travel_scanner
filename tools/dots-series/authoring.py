"""Small, strict Markdown adapter to the existing GuideDocument block vocabulary.

This module has no network or publishing operations. Unsupported authored constructs
fail with their line number rather than disappearing from a tutorial.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

INLINE = re.compile(r"`([^`]+)`|\[([^\]]+)\]\(([^\s)]+)\)")
SECTION = re.compile(r"^#{1,3}\s+")
SOURCE_SECTION = re.compile(r"^##\s+(?:官方來源|來源與查核|參考來源|來源與查證|來源)(?:與|\s|：|:|$)")
DATE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")


def plain(value: str) -> str:
    return re.sub(r"\*\*([^*]+)\*\*", r"\1", value).strip()


def table_text(value: str) -> str:
    # Guide tables contain plain strings. Links belong in publication-aware rich
    # paragraphs or the live series directory, never as visible Markdown syntax.
    return INLINE.sub(lambda match: match.group(1) if match.group(1) is not None else match.group(2), plain(value))


def inlines(value: str) -> list[dict]:
    result = []
    offset = 0
    value = plain(value)
    for match in INLINE.finditer(value):
        if match.start() > offset:
            result.append({"type": "text", "text": value[offset:match.start()]})
        if match.group(1) is not None:
            result.append({"type": "code", "text": match.group(1)})
        else:
            title, target = match.group(2), match.group(3)
            article = re.fullmatch(r"(?:article:|(?:https://mokaair\.com)?/zh-TW/life/)([a-z0-9-]+)", target)
            if article:
                result.append({"type": "article", "text": title, "kind": "life", "slug": article.group(1)})
            else:
                result.append({"type": "link", "text": title, "url": target})
        offset = match.end()
    if offset < len(value):
        result.append({"type": "text", "text": value[offset:]})
    return result


def source_footer(lines: list[str]) -> tuple[list[str], list[dict]]:
    starts = [i for i, line in enumerate(lines) if SOURCE_SECTION.match(line.strip())]
    if len(starts) != 1:
        raise ValueError("Exactly one final ## 官方來源 section is required")
    start = starts[0]
    footer = lines[start + 1:]
    if any(SECTION.match(line.strip()) for line in footer):
        raise ValueError("官方來源 must be the final section")
    dates = {match.group(1) for line in footer for match in DATE.finditer(line)}
    sources = []
    for line in footer:
        for match in INLINE.finditer(line):
            if match.group(3) is None:
                continue
            title, url = match.group(2), match.group(3)
            parsed = urlsplit(url)
            if parsed.scheme not in {"https", "http"} or not parsed.hostname or parsed.username is not None or parsed.password is not None:
                raise ValueError(f"Unsafe source URL: {url}")
            checked = DATE.search(line)
            stamp = checked.group(1) if checked else next(iter(dates)) if len(dates) == 1 else None
            if stamp is None:
                raise ValueError(f"Source lacks an unambiguous checked_on date: {url}")
            date.fromisoformat(stamp)
            source = {"title": plain(title), "url": url, "checked_on": stamp}
            if any(old["url"] == url for old in sources):
                raise ValueError(f"Duplicate source URL: {url}")
            sources.append(source)
    if not sources:
        raise ValueError("The source footer contains no checked official link")
    return lines[:start], sources


def parse_markdown(text: str) -> dict:
    lines, sources = source_footer(text.replace("\r\n", "\n").splitlines())
    titles = [plain(line[2:]) for line in lines if line.startswith("# ")]
    if len(titles) != 1:
        raise ValueError("Exactly one # article title is required")
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("# "):
            i += 1
            continue
        if line == ":::summary":
            items = []
            i += 1
            while i < len(lines) and lines[i].strip() != ":::" :
                value = lines[i].strip()
                if value:
                    if not value.startswith("- "):
                        raise ValueError(f"Line {i + 1}: summary entries must be authored list items")
                    items.append(plain(value[2:]))
                i += 1
            if i == len(lines):
                raise ValueError("Unclosed summary block")
            blocks.append({"type": "summary", "items": items})
        elif line.startswith("```"):
            parts = line[3:].split(" ", 1)
            if len(parts) != 2 or not parts[1].strip():
                raise ValueError(f"Line {i + 1}: code fence requires language and copy label")
            code = []
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                code.append(lines[i])
                i += 1
            if i == len(lines):
                raise ValueError("Unclosed code fence")
            blocks.append({"type": "code", "language": parts[0], "label": plain(parts[1]), "code": "\n".join(code) + "\n"})
        elif line.startswith(("## ", "### ")):
            prefix = 3 if line.startswith("## ") else 4
            blocks.append({"type": "heading", "level": prefix - 1, "text": plain(line[prefix:])})
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [table_text(cell) for cell in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                    rows.append(cells)
                i += 1
            if len(rows) < 2:
                raise ValueError("A table requires a header and at least one data row")
            blocks.append({"type": "table", "header": rows[0], "rows": rows[1:]})
            continue
        elif line.startswith("> "):
            lines_in_box = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                lines_in_box.append(plain(lines[i].strip()[2:]))
                i += 1
            blocks.append({"type": "callout", "tone": "info", "title": "操作提醒", "text": "\n".join(lines_in_box)})
            continue
        elif line.startswith("- ") or re.match(r"^\d+\. ", line):
            ordered = not line.startswith("- ")
            pattern = r"^\d+\. " if ordered else r"^- "
            items = []
            while i < len(lines) and re.match(pattern, lines[i].strip()):
                items.append(plain(re.sub(pattern, "", lines[i].strip())))
                i += 1
            blocks.append({"type": "list", "ordered": ordered, "items": items})
            continue
        elif line.startswith(("![", "<", "~~~")):
            raise ValueError(f"Line {i + 1}: use existing image metadata via assets, no raw HTML or alternate fences")
        elif line == "---":
            i += 1
            continue
        else:
            paragraph = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,3} |```|:::|\||> |- |\d+\. |!\[|<|~~~|---$)", lines[i].strip()):
                paragraph.append(lines[i].strip())
                i += 1
            value = plain("\n".join(paragraph))
            blocks.append({"type": "rich_paragraph", "inlines": inlines(value)} if INLINE.search(value) else {"type": "paragraph", "text": value})
            continue
        i += 1
    lead = next((block["text"] for block in blocks if block["type"] == "paragraph"), "")
    if not lead:
        raise ValueError("An authored introductory paragraph is required")
    return {"title": titles[0], "description": lead[:500], "blocks": blocks, "sources": sources}


def read_lesson(path: Path) -> dict:
    if not path.is_file():
        raise ValueError(f"Missing authored lesson: {path}")
    return parse_markdown(path.read_text(encoding="utf-8-sig"))
