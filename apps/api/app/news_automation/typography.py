"""Mechanical typography for generated news prose, before it is reviewed or hashed.

This is deliberately separate from GuideDocument validation: saved articles and human
edits keep their exact text. Only the news provider reply models call this helper.
"""

from __future__ import annotations

import re
from typing import Any

from app.guides.schemas import GuideDocument

# The same immediate Han/kana adjacency that the news hard check reports. Provider
# replies have no locale field, so generated CJK prose uses this typography in every
# locale, including Japanese commas; whole Latin runs and numeric punctuation stay put.
_CJK = r"[\u3005\u3007\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\U00020000-\U0002fa1f]"
_PUNCTUATION = re.compile(rf"(?<={_CJK})[,:;?!()]|[,:;?!()](?={_CJK})")
_FULL_WIDTH = dict(zip(",:;?!()", "，：；？！（）", strict=True))
# Keep the hard check's URL boundaries: full-width punctuation can be part of a
# Unicode URL, and is never inferred to be the end of its path or query.
_URL = re.compile(r'''(?:https?://|mailto:|www\.)[^\s<>"']+''', re.I)
_PROSE_FIELDS = {
    "heading": ("text",),
    "paragraph": ("text",),
    "list": ("items",),
    "summary": ("items",),
    "table": ("header", "rows", "caption"),
    "callout": ("title", "text"),
    "faq": ("items",),
    "image": ("alt", "caption", "description"),
    "link": ("text",),
    "partner_link": ("label", "note"),
    "offer": ("heading",),
    "code": ("label",),
}


def _mask_urls(text: str) -> str:
    return _URL.sub(lambda match: " " * len(match.group()), text)


def _normalize_text(text: str) -> str:
    positions = {match.start() for match in _PUNCTUATION.finditer(_mask_urls(text))}
    return "".join(_FULL_WIDTH[char] if index in positions else char
                   for index, char in enumerate(text))


def _normalize_value(value: Any) -> Any:
    if isinstance(value, str):
        return _normalize_text(value)
    if isinstance(value, list):
        return [_normalize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _normalize_value(item) for key, item in value.items()}
    return value


def _normalize_inlines(inlines: list[dict[str, Any]]) -> None:
    # Match the rendered text, including adjacency across nodes. Mask each link label
    # independently, but join adjacent text nodes first so a split URL stays opaque.
    parts: list[str] = []
    text_run: list[str] = []
    for node in inlines:
        text = str(node["text"])
        if node["type"] == "text":
            text_run.append(text)
            continue
        parts.append(_mask_urls("".join(text_run)))
        text_run = []
        parts.append(" " * len(text) if node["type"] == "code" else _mask_urls(text))
    parts.append(_mask_urls("".join(text_run)))
    positions = {match.start() for match in _PUNCTUATION.finditer("".join(parts))}
    offset = 0
    for node in inlines:
        text = str(node["text"])
        if node["type"] != "code":
            node["text"] = "".join(
                _FULL_WIDTH[char] if offset + index in positions else char
                for index, char in enumerate(text)
            )
        offset += len(text)


def normalize_generated_document(document: GuideDocument) -> GuideDocument:
    """Return CJK prose with ASCII punctuation fixed; never mutate the input.

    Every replacement is one character. Code, link targets, source metadata, image
    credits, numbers and URL tokens are opaque; the block and inline structure stays
    intact. Revalidate the result before the pipeline takes any review fingerprints.
    """
    encoded = document.model_dump(mode="json")
    encoded["title"] = _normalize_text(encoded["title"])
    encoded["description"] = _normalize_text(encoded["description"])
    if encoded["hero"] is not None:
        encoded["hero"]["alt"] = _normalize_text(encoded["hero"]["alt"])
    for block in encoded["blocks"]:
        if block["type"] == "rich_paragraph":
            _normalize_inlines(block["inlines"])
        else:
            for field in _PROSE_FIELDS.get(block["type"], ()):
                block[field] = _normalize_value(block[field])
    return GuideDocument.model_validate(encoded)
