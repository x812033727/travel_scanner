"""Summary and FAQ blocks for packs that already exist, rewritten the way ``autolink`` and
``retopic`` rewrite a pack: a proposal table to read, then ``--apply`` on the same rows.

Two sources for a summary, and no third:

- **The article's own lead.** A paragraph that opens with 「先講結論」 already is the
  summary; the tool lifts its sentences, never rephrasing them.
- **A batch the owner reviewed.** ``--from batch.json`` carries summaries the model drafted
  from the article and the owner read before applying (the owner's decision of
  2026-09-16, which replaced "never generated"). Every number in a batch sentence has to
  occur in the document itself, or the whole batch is refused: the one thing an answer
  engine must never quote from here is a figure the article does not state.

A 「常見問題」 section that already is a list of 問題：答案 pairs, or question headings each
answered by one plain paragraph and nothing else, becomes the ``faq`` block and leaves the
body, so the page does not say it twice. Anything richer stays where it is:
``FaqItem.answer`` is plain text, and an answer with links would lose them.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from app.guides.autolink import pack_kinds
from app.guides.content_pack import default_directory
from app.guides.schemas import FaqBlock, Kind, SummaryBlock

#: A paragraph opening with one of these wrote the summary itself.
LEAD_MARKERS = ("先講結論", "先看結論", "結論先講", "結論：", "一句話", "用一句話")
LEAD_PREFIX = re.compile(
    r"^(?:先講結論|先看結論|結論先講|用一句話(?:說|講)?|一句話(?:的結論)?|結論)[：:，,]\s*"
)
SENTENCE_END = re.compile(r"(?<=[。！？；])")
MAX_SUMMARY_SENTENCES = 5
FAQ_HEADING = "常見問題"
#: ``pack_ingest`` wants at least three level-2 headings; converting the FAQ section must
#: not take an article below that.
MIN_LEVEL_2_HEADINGS = 3
NUMBER = re.compile(r"\d+(?:[.,:]\d+)*")

Document = dict[str, Any]
Block = dict[str, Any]


class SummarizeError(ValueError):
    """A batch that cannot be applied as a whole. Nothing is written on one."""


def _text(block: Block) -> str | None:
    if block.get("type") == "paragraph":
        return str(block.get("text", ""))
    if block.get("type") == "rich_paragraph":
        return "".join(str(inline.get("text", "")) for inline in block.get("inlines", []))
    return None


def _is_heading(block: Block, level: int | None = None) -> bool:
    return block.get("type") == "heading" and (level is None or block.get("level") == level)


def lead_summary(document: Document) -> list[str] | None:
    """The sentences of the article's own 「先講結論」 paragraph, at most five, or None when
    the article has no such paragraph or it does not make a valid summary as it stands."""
    for block in document.get("blocks", []):
        text = _text(block)
        if text is None or not text.strip().startswith(LEAD_MARKERS):
            continue
        body = LEAD_PREFIX.sub("", text.strip(), count=1)
        sentences = [part.strip() for part in SENTENCE_END.split(body) if part.strip()]
        items = sentences[:MAX_SUMMARY_SENTENCES]
        try:
            SummaryBlock.model_validate({"type": "summary", "items": items})
        except ValidationError:
            return None
        return items
    return None


def _pairs_from_list(section: list[Block]) -> list[dict[str, str]] | None:
    """A single list whose every item is 問題：答案 (or 問題？答案)."""
    if len(section) != 1 or section[0].get("type") != "list":
        return None
    items: list[dict[str, str]] = []
    for raw in section[0].get("items", []):
        text = str(raw).strip()
        match = re.search(r"[：？]", text)
        if not match:
            return None
        cut = match.end() if text[match.start()] == "？" else match.start()
        question, answer = text[:cut].strip(), text[match.end() :].strip()
        if not question or not answer:
            return None
        items.append({"question": question, "answer": answer})
    return items


def _pairs_from_headings(section: list[Block]) -> list[dict[str, str]] | None:
    """Question headings (level 3) each answered by exactly one plain paragraph, and nothing
    else in the section: a further block would be lost with the section, and a rich
    paragraph's links with the answer."""
    if len(section) < 4 or len(section) % 2:
        return None
    items: list[dict[str, str]] = []
    for question_block, answer_block in zip(section[0::2], section[1::2], strict=True):
        if not _is_heading(question_block, 3) or answer_block.get("type") != "paragraph":
            return None
        question = str(question_block.get("text", "")).strip()
        answer = str(answer_block.get("text", "")).strip()
        if not question or not answer:
            return None
        items.append({"question": question, "answer": answer})
    return items


def faq_from_section(document: Document) -> tuple[int, int, str, list[dict[str, str]]] | None:
    """``(start, end, shape, items)`` for a 常見問題 section the rules can convert, where
    ``blocks[start:end]`` is the heading and its section; None otherwise."""
    blocks: list[Block] = document.get("blocks", [])
    if any(block.get("type") == "faq" for block in blocks):
        return None
    for index, block in enumerate(blocks):
        if not _is_heading(block, 2) or FAQ_HEADING not in str(block.get("text", "")):
            continue
        end = index + 1
        while end < len(blocks) and not _is_heading(blocks[end], 2):
            end += 1
        section = blocks[index + 1 : end]
        items = _pairs_from_list(section)
        shape = "list"
        if items is None:
            items = _pairs_from_headings(section)
            shape = "pairs"
        if items is None:
            return None
        remaining = blocks[:index] + blocks[end:]
        if sum(1 for item in remaining if _is_heading(item, 2)) < MIN_LEVEL_2_HEADINGS:
            return None
        try:
            FaqBlock.model_validate({"type": "faq", "items": items})
        except ValidationError:
            return None
        return index, end, shape, items
    return None


@dataclass(frozen=True)
class DocumentReport:
    """What the table says about one (pack, locale)."""

    summary: str  # "lead (N)" | "batch (N)" | "has summary" | "no candidate"
    faq: str  # "list→faq (N)" | "pairs→faq (N)" | "batch (N)" | "has faq" | "kept as section" | "-"


def summarize_document(
    document: Document, *, entry: dict[str, Any] | None = None, replace: bool = False
) -> tuple[Document, DocumentReport]:
    """The document with its summary (at index 0, which is before the first heading) and
    FAQ block, from the batch entry when given and from the article's own text otherwise.
    A summary already there is kept unless ``replace``; so is a FAQ block."""
    blocks: list[Block] = list(document.get("blocks", []))
    has_summary = any(block.get("type") == "summary" for block in blocks)
    has_faq = any(block.get("type") == "faq" for block in blocks)

    summary_note = "has summary" if has_summary and not replace else "no candidate"
    items: list[str] | None = None
    if not has_summary or replace:
        if entry and entry.get("summary"):
            items = list(entry["summary"])
            summary_note = f"batch ({len(items)})"
        else:
            items = lead_summary(document)
            if items is not None:
                summary_note = f"lead ({len(items)})"
    if items is not None:
        blocks = [block for block in blocks if block.get("type") != "summary"]
        blocks.insert(0, {"type": "summary", "items": items})

    faq_note = "-"
    faq_items: list[dict[str, str]] | None = None
    if has_faq and not replace:
        faq_note = "has faq"
    elif entry and entry.get("faq"):
        faq_items = [dict(item) for item in entry["faq"]]
        faq_note = f"batch ({len(faq_items)})"
        blocks = [block for block in blocks if block.get("type") != "faq"]
    else:
        found = faq_from_section({**document, "blocks": blocks}) if not has_faq else None
        if found is not None:
            start, end, shape, faq_items = found
            blocks = blocks[:start] + blocks[end:]
            faq_note = f"{shape}→faq ({len(faq_items)})"
        elif any(
            _is_heading(block) and FAQ_HEADING in str(block.get("text", "")) for block in blocks
        ):
            faq_note = "kept as section"
    if faq_items is not None:
        blocks.append({"type": "faq", "items": faq_items})
    return {**document, "blocks": blocks}, DocumentReport(summary_note, faq_note)


def numbers_missing(document: Document, texts: list[str]) -> list[str]:
    """Every figure in ``texts`` that the document (its sources aside) does not carry as
    written: ``1,100`` is not ``1100``, and a batch sentence must match the article."""
    haystack = json.dumps(
        {key: value for key, value in document.items() if key != "sources"}, ensure_ascii=False
    )
    return [number for text in texts for number in NUMBER.findall(text) if number not in haystack]


Batch = dict[str, dict[str, dict[str, Any]]]


def load_batch(path: Path) -> Batch:
    """``{slug: {locale: {"summary": [...], "faq"?: [{"question", "answer"}]}}}``, each entry
    validated as the block it becomes; a bad entry names its slug and locale."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise SummarizeError(f"batch: cannot read {path}: {error}") from None
    if not isinstance(data, dict):
        raise SummarizeError("batch: expected an object of slug → locale → entry")
    batch: Batch = {}
    for slug, locales in data.items():
        if not isinstance(locales, dict):
            raise SummarizeError(f"batch: {slug}: expected locale → entry")
        batch[slug] = {}
        for locale, entry in locales.items():
            if not isinstance(entry, dict) or not isinstance(entry.get("summary"), list):
                raise SummarizeError(f"batch: {slug} {locale}: expected a summary list")
            summary = [str(item).strip() for item in entry["summary"]]
            cleaned: dict[str, Any] = {"summary": summary}
            try:
                SummaryBlock.model_validate({"type": "summary", "items": summary})
                if "faq" in entry:
                    FaqBlock.model_validate({"type": "faq", "items": entry["faq"]})
                    cleaned["faq"] = [
                        {
                            "question": str(item["question"]).strip(),
                            "answer": str(item["answer"]).strip(),
                        }
                        for item in entry["faq"]
                    ]
            except (ValidationError, KeyError, TypeError) as error:
                detail = (
                    error.errors()[0]["msg"] if isinstance(error, ValidationError) else str(error)
                )
                raise SummarizeError(f"batch: {slug} {locale}: {detail}") from None
            batch[slug][locale] = cleaned
    return batch


@dataclass
class Proposal:
    slug: str
    documents: dict[str, Document] = field(default_factory=dict)
    reports: dict[str, DocumentReport] = field(default_factory=dict)

    @property
    def changed(self) -> bool:
        return bool(self.documents)


def _selected(
    root: Path, *, kind: Kind | None, prefixes: tuple[str, ...], slugs: set[str] | None
) -> Iterator[tuple[str, Path, str | None]]:
    kinds = pack_kinds(root)
    for path in sorted(root.glob("*.json")):
        slug = path.stem
        if slugs is not None and slug not in slugs:
            continue
        if prefixes and not slug.startswith(tuple(prefixes)):
            continue
        if kind is not None and kinds.get(slug) != kind:
            continue
        yield slug, path, kinds.get(slug)


def proposals(
    directory: Path | None = None,
    *,
    kind: Kind | None = None,
    prefixes: tuple[str, ...] = (),
    slugs: set[str] | None = None,
    batch: Batch | None = None,
    replace: bool = False,
) -> list[Proposal]:
    """One row per selected pack. With a batch, only its slugs are visited, and a slug or
    locale the selection cannot answer, a summary already present without ``--replace``, or
    a figure the article does not state refuses the whole batch before anything is
    returned -- ``apply`` never writes part of one."""
    root = Path(directory) if directory else default_directory()
    wanted = set(batch) if batch is not None else slugs
    rows: list[Proposal] = []
    for slug, path, _ in _selected(root, kind=kind, prefixes=prefixes, slugs=wanted):
        raw = json.loads(path.read_text(encoding="utf-8"))
        locales: dict[str, Document] = raw.get("locales", {})
        entries = (batch or {}).get(slug, {})
        for locale in entries:
            if locale not in locales:
                raise SummarizeError(f"batch: {slug} has no locale {locale}")
        row = Proposal(slug=slug)
        for locale, document in locales.items():
            entry = entries.get(locale)
            if entry is not None:
                present = any(b.get("type") == "summary" for b in document.get("blocks", []))
                if present and not replace:
                    raise SummarizeError(
                        f"batch: {slug} {locale} already has a summary (--replace)"
                    )
                texts = list(entry["summary"]) + [
                    item["question"] + item["answer"] for item in entry.get("faq", [])
                ]
                missing = numbers_missing(document, texts)
                if missing:
                    raise SummarizeError(
                        f"numbers_not_in_text: {slug} {locale}: {', '.join(missing)}"
                    )
            rewritten, report = summarize_document(document, entry=entry, replace=replace)
            row.reports[locale] = report
            if rewritten["blocks"] != document.get("blocks", []):
                row.documents[locale] = rewritten
        rows.append(row)
    if batch is not None:
        seen = {row.slug for row in rows}
        for slug in batch:
            if slug not in seen:
                raise SummarizeError(f"batch: no pack named {slug} in the selection")
    return rows


def render_table(rows: list[Proposal]) -> str:
    """The changed documents, one line each, and the count of what the rules found."""
    lines = ["| slug | locale | summary | faq |", "| --- | --- | --- | --- |"]
    summaries = lead = batch = faqs = none = 0
    for row in rows:
        for locale, report in row.reports.items():
            if report.summary.startswith("lead"):
                lead += 1
                summaries += 1
            elif report.summary.startswith("batch"):
                batch += 1
                summaries += 1
            elif report.summary == "no candidate":
                none += 1
            if "→faq" in report.faq or report.faq.startswith("batch"):
                faqs += 1
            if locale in row.documents:
                lines.append(f"| `{row.slug}` | {locale} | {report.summary} | {report.faq} |")
    changed = sum(1 for row in rows if row.changed)
    lines.append("")
    lines.append(
        f"{changed} of {len(rows)} packs would change: {summaries} summaries "
        f"({lead} lead, {batch} batch), {faqs} FAQs; {none} documents without a candidate"
    )
    return "\n".join(lines)


def apply(rows: list[Proposal], directory: Path | None = None) -> list[Path]:
    """Rewrite the changed packs' blocks, nothing else: a pack round-trips byte for byte
    under this dump, so the diff is the inserted and removed blocks alone."""
    root = Path(directory) if directory else default_directory()
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


def _faq_shape(document: Document) -> str:
    blocks: list[Block] = document.get("blocks", [])
    for index, block in enumerate(blocks):
        if not _is_heading(block, 2) or FAQ_HEADING not in str(block.get("text", "")):
            continue
        end = index + 1
        while end < len(blocks) and not _is_heading(blocks[end], 2):
            end += 1
        section = blocks[index + 1 : end]
        if (items := _pairs_from_list(section)) is not None:
            return f"list×{len(items)}"
        if (items := _pairs_from_headings(section)) is not None:
            return f"pairs×{len(items)}"
        return "prose"
    return "none"


def render_digest(
    directory: Path | None = None,
    *,
    kind: Kind | None = None,
    prefixes: tuple[str, ...] = (),
    slugs: set[str] | None = None,
) -> str:
    """What a summary is written from, per document still without one: the description,
    the headings, the first two paragraphs, each table's header, the lead if any, and the
    shape of the FAQ section -- enough to draft from without inventing, and a pointer to
    open the pack when it is not."""
    root = Path(directory) if directory else default_directory()
    lines: list[str] = []
    for slug, path, pack_kind in _selected(root, kind=kind, prefixes=prefixes, slugs=slugs):
        raw = json.loads(path.read_text(encoding="utf-8"))
        for locale, document in raw.get("locales", {}).items():
            blocks: list[Block] = document.get("blocks", [])
            if any(block.get("type") == "summary" for block in blocks):
                continue
            lines.append(f"## {slug} ({locale}, {pack_kind})")
            lines.append(f"title: {document.get('title', '')}")
            lines.append(f"description: {document.get('description', '')}")
            lines.append("headings:")
            for block in blocks:
                if _is_heading(block):
                    indent = "  " if block.get("level") == 3 else ""
                    lines.append(f"{indent}- {block.get('text', '')}")
            lines.append("paragraphs:")
            shown = 0
            for block in blocks:
                text = _text(block)
                if text is None:
                    continue
                lines.append(f"- {text}")
                shown += 1
                if shown == 2:
                    break
            tables = [block for block in blocks if block.get("type") == "table"]
            if tables:
                lines.append("tables:")
                for table in tables:
                    header = " | ".join(str(cell) for cell in table.get("header", []))
                    caption = table.get("caption")
                    lines.append(f"- {caption + ': ' if caption else ''}{header}")
            lead = lead_summary(document)
            if lead is not None:
                lines.append("lead: " + " ".join(lead))
            lines.append(f"faq shape: {_faq_shape(document)}")
            lines.append("")
    return "\n".join(lines)
