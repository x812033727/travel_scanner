"""Content-pack production: turn a writing agent's workspace into a reviewable pack, and lint
the packs that already ship.

The first three article batches each rewrote the same throwaway script in a session
scratchpad: validate the pack, copy the SVG, fetch the photographs from Wikimedia Commons with
their licence, write sizes and credits. This module is that script, kept, tested and run the
same way for every batch. It adds one step the travel batches never needed: an article about
software has no photograph to take, so its hero is a self-drawn ``hero.svg`` that is rendered
to the raster ``hero.jpg`` the schema requires (``HERO_SRC_PATTERN``: social crawlers do not
render SVG).

Two entry points, both reachable through ``python -m app.guides.pack_cli``:

- ``ingest(workdir, slug, ...)`` reads ``<workdir>/<slug>/`` -- ``pack.json``, ``diagram-N.svg``,
  ``hero.svg`` or an ``images.json`` naming Commons files -- and writes
  ``app/guides/content/<slug>.json`` plus ``apps/web/public/guides/<slug>/``. Everything is
  built in a staging directory first; a single error and nothing lands.
- ``lint_all(...)`` runs the editorial rules over the packs in the repository, optionally
  rendering every SVG to PNG so a person can look at it (an agent cannot see its own layout),
  and compares the packs with the series catalogue.

I/O is injected -- the Commons client is an ``httpx.Client``, the renderer a callable -- so the
tests run without a network or a browser.
"""

from __future__ import annotations

import html
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from email.message import Message
from glob import glob
from pathlib import Path
from typing import Any, Literal
from xml.etree import ElementTree

import httpx
from PIL import Image
from pydantic import ValidationError

from app.guides import admin_service
from app.guides.autolink import SITE_LINK
from app.guides.content_pack import ArticlePack, ContentPackError, load_packs
from app.guides.schemas import (
    MAX_IMAGE_SIDE,
    ArticleInline,
    CalloutBlock,
    CodeBlock,
    FaqBlock,
    GuideDocument,
    ImageBlock,
    ImageCredit,
    Kind,
    LinkInline,
    PartnerLinkBlock,
    RichParagraphBlock,
    SummaryBlock,
    TableBlock,
    section_of,
)
from app.guides.taxonomy import (
    LIFE_SEED_SUBTOPICS,
    LIFE_SEED_TOPICS,
    SEED_TOPICS,
    TRAVEL_SEED_SUBTOPICS,
)
from app.i18n import Locale
from app.problems import AppError
from app.site_pages.schemas import HeadingBlock, LinkBlock, ListBlock, ParagraphBlock

# --- the editorial numbers, in one place --------------------------------------------------

HERO_SIZE = (1600, 900)
HERO_MAX_BYTES = 200_000
PHOTO_MAX_WIDTH = 1200
PHOTO_MAX_BYTES = 150_000
#: What ``tests/test_guides_content_pack.py`` refuses; the two above are the editorial guideline.
IMAGE_HARD_CAP = 300_000
MIN_LEVEL_2_HEADINGS = 3
#: Warn outside this: a stub or a monster. The guideline is 1,800–3,000 CJK characters, but
#: the reviewed travel articles run to 4,000 and an English translation to 8,000.
TEXT_RANGE = (1_500, 6_000)
INTEL_TEXT_RANGE = (700, 3_000)
#: ``GuideDocument`` refuses 120,000; warn well before an editor's next paragraph trips it.
DOCUMENT_JSON_LIMIT = 110_000
MIN_LABEL_PX = 15
DIAGRAM_VIEWBOX = "0 0 1600 900"
SITE_ORIGIN = "https://mokaair.com/"
#: The disclaimer template in ``docs/life-finance-series-brief.md`` and the crypto brief must
#: contain one of these verbatim. ``lint_all`` lints one locale document at a time and is not
#: told which locale it is looking at, so any of the five satisfies the rule; a Chinese-only
#: marker would turn the four translations of every multilingual finance article into errors.
#: Compared casefolded, so an English sentence may open "This is not investment advice".
FINANCE_DISCLAIMER_MARKERS = (
    "不是投資建議",  # zh-TW
    "不是投资建议",  # zh-CN
    "not investment advice",  # en
    "投資助言ではありません",  # ja
    "투자 조언이 아닙니다",  # ko
)
_CASEFOLDED_MARKERS = tuple(marker.casefold() for marker in FINANCE_DISCLAIMER_MARKERS)
#: The investment-shaped topics, which are not the whole money vertical. ``finance`` is what
#: the finance series carries, ``investing`` its investment children, and ``crypto`` matters on
#: its own because ``retopic`` only supplies a missing parent for the two post-split ones
#: (``website``, ``marketing``) -- ``finance`` is one of the original eight, so a ``crypto-*``
#: article is never given it automatically and would otherwise escape the rule.
#:
#: ``banking``, ``credit``, ``tax-insurance`` and ``finance-basics`` are deliberately absent.
#: Four shipped articles carry one of them and no disclaimer -- registering a company, a Wise
#: transfer checklist, YouTube payment tax, a household inventory spreadsheet -- and none is
#: about investing. Demanding 「不是投資建議」 there is the false positive the ticket's own notes
#: warn about: it would teach writers that the callout is boilerplate to paste, which is how a
#: disclaimer stops being read.
FINANCE_TOPICS = frozenset({"finance", "investing", "crypto"})
#: Absolute promises a finance article must not make in its own voice. A *warning*, not an
#: error: ``investment-scam-red-flags`` quotes these very phrases as the marks of a scam, and
#: an error there would either block a legitimate article or teach the next writer to spell
#: its way around the linter.
FINANCE_CLAIM_WORDS = re.compile(
    r"保證(獲利|賺|不賠)|穩賺|包賺|必漲|必跌|無風險|報明牌|飆股|老師帶單|躺著賺"
)
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
MOKAAIR_CREDIT = ImageCredit(author="Mokaair", license="© Mokaair")
#: Wikimedia's robot policy wants ``name/version (contact)``; without an address it answers 403
#: "Please respect our robot policy". The mailbox is the site's public support address.
USER_AGENT = "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)"

#: Commons ``LicenseShortName`` values the site may use, after ``_normalise_license``. Anchored
#: at both ends so "CC BY-NC 2.0" (starts with "CC BY") and KOGL are refused.
ALLOWED_LICENSE = re.compile(r"^(cc0|public domain|pd|cc by(-sa)?)(\s+\d+(\.\d+)?)?$")

#: ``info`` is for the record only: it never fails a run, not even under ``--warnings``.
Level = Literal["error", "warning", "info"]


@dataclass(frozen=True)
class Problem:
    level: Level
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.level}: {self.code}: {self.message}"


def errors(problems: Iterable[Problem]) -> list[Problem]:
    return [problem for problem in problems if problem.level == "error"]


class PackIngestError(ValueError):
    """A workspace that cannot become a pack. Not an ``AppError``: nothing here is shown to a
    reader, and ``tests/test_error_localization.py`` holds every reader-facing module to a
    translated sentence per code."""


# --- the document rules -------------------------------------------------------------------


def _document_text(document: GuideDocument) -> str:
    """Every string a reader sees, joined, for the length rule and the diagram-number rule.
    Summary and FAQ count: they are read like any other section, so a figure the diagram draws
    and only the summary states is carried by the article, and a simplified character there is
    still a simplified character on the page."""
    parts = [document.title, document.description]
    for block in document.blocks:
        if isinstance(block, ParagraphBlock | HeadingBlock):
            parts.append(block.text)
        elif isinstance(block, RichParagraphBlock):
            parts.append("".join(node.text for node in block.inlines))
        elif isinstance(block, CodeBlock):
            parts.extend((block.label, block.code))
        elif isinstance(block, ListBlock):
            parts.extend(block.items)
        elif isinstance(block, TableBlock):
            parts.extend(block.header)
            for row in block.rows:
                parts.extend(row)
            parts.append(block.caption)
        elif isinstance(block, CalloutBlock):
            parts.extend((block.title, block.text))
        elif isinstance(block, ImageBlock):
            parts.append(block.caption)
        elif isinstance(block, LinkBlock):
            parts.append(block.text)
        elif isinstance(block, SummaryBlock):
            parts.extend(block.items)
        elif isinstance(block, FaqBlock):
            parts.extend(item.question for item in block.items)
            parts.extend(item.answer for item in block.items)
    return "\n".join(part for part in parts if part)


def _body_parts(document: GuideDocument) -> list[str]:
    """The running text, block by block: paragraphs, lists, tables and callouts, not the title,
    captions or link labels. ``_body_length`` counts it and ``finance_claim_language`` reads it,
    so a block type added to one is never missing from the other."""
    parts: list[str] = []
    for block in document.blocks:
        if isinstance(block, ParagraphBlock):
            parts.append(block.text)
        elif isinstance(block, RichParagraphBlock):
            parts.append("".join(node.text for node in block.inlines))
        elif isinstance(block, ListBlock):
            parts.extend(block.items)
        elif isinstance(block, TableBlock):
            parts.extend(block.header)
            for row in block.rows:
                parts.extend(row)
        elif isinstance(block, CalloutBlock):
            parts.extend((block.title, block.text))
        elif isinstance(block, SummaryBlock):
            parts.extend(block.items)
        elif isinstance(block, FaqBlock):
            parts.extend(f"{item.question}{item.answer}" for item in block.items)
    return parts


def _body_length(document: GuideDocument) -> int:
    """Characters of running text -- what "an article runs about 1,800–3,000 characters" counts."""
    return sum(len(re.sub(r"\s+", "", part)) for part in _body_parts(document))


def _raw_site_urls(document: GuideDocument) -> Iterator[str]:
    for block in document.blocks:
        if isinstance(block, LinkBlock):
            yield block.url
        elif isinstance(block, RichParagraphBlock):
            for node in block.inlines:
                if isinstance(node, LinkInline):
                    yield node.url


def lint_document(
    document: GuideDocument, kind: Kind, *, topics: Sequence[str] = ()
) -> list[Problem]:
    """The review standard in ``docs/travel-guides.md`` "Editorial rules", as far as a machine
    can read it. Errors are what a reviewer would send back; warnings are worth a look.

    ``topics`` carries the pack's subjects because two of the rules only apply to one of them:
    finance is a YMYL subject, and Taiwan's 證券投資信託及顧問法 restricts who may
    offer securities analysis for reward. It is keyword-only with a default so a caller that
    has no pack in hand -- every test that lints a bare document -- keeps working unchanged."""
    problems: list[Problem] = []
    headings = [b for b in document.blocks if isinstance(b, HeadingBlock) and b.level == 2]
    if len(headings) < MIN_LEVEL_2_HEADINGS:
        problems.append(
            Problem(
                "error",
                "too_few_headings",
                f"{len(headings)} level-2 headings; at least {MIN_LEVEL_2_HEADINGS} "
                "(the table of contents starts at three)",
            )
        )
    if not any(isinstance(b, TableBlock) for b in document.blocks):
        problems.append(Problem("error", "no_table", "an article carries at least one table"))
    if not any(isinstance(b, CalloutBlock) for b in document.blocks):
        problems.append(Problem("error", "no_callout", "an article carries at least one callout"))
    if document.hero is None:
        problems.append(Problem("error", "no_hero", "an article has a hero image"))
    partner_links = [b for b in document.blocks if isinstance(b, PartnerLinkBlock)]
    if len(partner_links) > admin_service.MAX_PARTNER_LINK_BLOCKS:
        problems.append(
            Problem("error", "partner_link_limit", "at most three partner links per article")
        )
    if not document.sources:
        problems.append(Problem("error", "no_sources", "an article cites its sources"))
    unchecked = [source.title for source in document.sources if source.checked_on is None]
    if unchecked:
        problems.append(
            Problem(
                "error",
                "source_not_checked",
                "every source records checked_on; missing on: " + "; ".join(unchecked),
            )
        )
    if not any(isinstance(b, ImageBlock) and b.src.endswith(".svg") for b in document.blocks):
        problems.append(Problem("warning", "no_diagram", "no self-drawn SVG diagram in the body"))
    if kind != "intel" and not any(isinstance(b, SummaryBlock) for b in document.blocks):
        problems.append(
            Problem(
                "warning",
                "no_summary",
                "no summary block: the answer in two to five sentences, before the first "
                "section, is what a reader skims and an answer engine quotes",
            )
        )
    if not any(
        (isinstance(b, LinkBlock) and b.url.startswith(SITE_ORIGIN))
        or (
            isinstance(b, RichParagraphBlock)
            and any(isinstance(node, ArticleInline) for node in b.inlines)
        )
        for b in document.blocks
    ):
        problems.append(
            Problem(
                "warning",
                "no_internal_link",
                f"no link block into this site ({SITE_ORIGIN}...): readers have nowhere to go next",
            )
        )
    raw_urls = [url for url in _raw_site_urls(document) if SITE_LINK.match(url) is not None]
    if raw_urls:
        problems.append(
            Problem(
                "warning",
                "raw_internal_url",
                f"{len(raw_urls)} article link(s) as raw URLs; run `pack_cli relink` so they "
                "become article inlines that follow the target's publication",
            )
        )
    encoded = len(json.dumps(document.model_dump(mode="json"), ensure_ascii=False))
    if encoded > DOCUMENT_JSON_LIMIT:
        problems.append(
            Problem(
                "error",
                "document_too_long",
                f"{encoded} characters of JSON; the model refuses 120,000, stop at "
                f"{DOCUMENT_JSON_LIMIT}",
            )
        )
    length = _body_length(document)
    low, high = TEXT_RANGE
    if kind == "intel":
        low, high = INTEL_TEXT_RANGE
    if not low <= length <= high:
        problems.append(
            Problem(
                "warning",
                "text_length",
                f"{length} characters of body text; the guideline for {kind} is {low}–{high}",
            )
        )
    problems.extend(_finance_problems(document, topics))
    return problems


def _finance_problems(document: GuideDocument, topics: Sequence[str]) -> list[Problem]:
    """The two rules that only a ``finance`` article answers to.

    The template check is an error and the wording check a warning, and the split is the whole
    point: whether the disclaimer is present is a fact a machine settles, while "does this
    amount to recommending a security" is a judgement it does not. Every batch ticket keeps
    that second reading with a person; this function only promises the paragraph is there."""
    if not FINANCE_TOPICS.intersection(topic.casefold() for topic in topics):
        return []
    problems: list[Problem] = []
    if not any(
        isinstance(block, CalloutBlock)
        and any(marker in block.text.casefold() for marker in _CASEFOLDED_MARKERS)
        for block in document.blocks
    ):
        problems.append(
            Problem(
                "error",
                "finance_no_disclaimer",
                "a finance article needs a callout whose text contains one of "
                + "、".join(FINANCE_DISCLAIMER_MARKERS)
                + "; see the template in docs/life-finance-series-brief.md",
            )
        )
    claims = sorted(
        {m.group(0) for part in _body_parts(document) for m in FINANCE_CLAIM_WORDS.finditer(part)}
    )
    if claims:
        problems.append(
            Problem(
                "warning",
                "finance_claim_language",
                "absolute claims in a finance article: "
                + "、".join(claims)
                + " -- fine when the article is quoting them as a scam's own words, "
                "otherwise rewrite",
            )
        )
    return problems


# --- the SVG rules ------------------------------------------------------------------------

SVG_NS = "{http://www.w3.org/2000/svg}"
_FONT_SIZE = re.compile(r"font-size\s*[:=]\s*[\"']?\s*(\d+(?:\.\d+)?)")
_NUMBER = re.compile(r"\d+(?:[.,:]\d+)*")
_SVG_NUMBER = re.compile(
    r"[+-]?(?:(?:[0-9]+(?:\.[0-9]*)?)|(?:\.[0-9]+))(?:[eE][+-]?[0-9]+)?"
)


def _parse_svg(text: str) -> ElementTree.Element:
    try:
        return ElementTree.fromstring(text)
    except ElementTree.ParseError as error:
        raise PackIngestError(f"not well-formed XML: {error}") from error


def _svg_decimal(value: str | None) -> Decimal | None:
    if value is None:
        return None
    stripped = value.strip()
    # Decimal deliberately accepts Python conveniences such as underscores and Unicode
    # decimal digits. Browsers' SVG number grammar does not, so validate its ASCII lexical
    # form before using Decimal for exact numeric comparisons.
    if _SVG_NUMBER.fullmatch(stripped) is None:
        return None
    try:
        number = Decimal(stripped)
    except InvalidOperation:
        return None
    return number if number.is_finite() else None


def _body_svg_dimensions(root: ElementTree.Element) -> tuple[tuple[int, int] | None, list[Problem]]:
    """Return a body diagram's exact dimensions after validating its coordinate space.

    Body diagrams may grow vertically so translated labels stay readable. They keep the
    established 1600 px width and use an integral height within the GuideDocument schema's
    image bound. Explicit root dimensions must match the viewBox; accepting a matching aspect
    ratio would let incorrect image metadata reserve the wrong amount of page space.
    """
    problems: list[Problem] = []
    pieces = re.split(r"\s+", root.get("viewBox", "").strip())
    viewbox: list[Decimal] = []
    if len(pieces) == 4:
        for piece in pieces:
            value = _svg_decimal(piece)
            if value is None:
                break
            viewbox.append(value)
    if len(viewbox) != 4:
        problems.append(
            Problem(
                "error",
                "svg_viewbox",
                "body diagram viewBox must contain four finite unitless numbers",
            )
        )
        return None, problems
    origin_x, origin_y, view_width, view_height = viewbox
    if origin_x != 0 or origin_y != 0:
        problems.append(
            Problem("error", "svg_viewbox", "body diagram viewBox origin must be 0 0")
        )
    if view_width != HERO_SIZE[0]:
        problems.append(
            Problem(
                "error",
                "svg_viewbox",
                f"body diagram viewBox width must be {HERO_SIZE[0]}",
            )
        )
    if (
        view_height <= 0
        or view_height != view_height.to_integral_value()
        or view_height > MAX_IMAGE_SIDE
    ):
        problems.append(
            Problem(
                "error",
                "svg_viewbox",
                f"body diagram viewBox height must be a positive integer up to {MAX_IMAGE_SIDE}",
            )
        )

    raw_width = root.get("width")
    raw_height = root.get("height")
    # Older reviewed 1600x900 diagrams relied on viewBox alone, which is valid SVG and is
    # already represented as 1600x900 in every pack. Preserve that exact legacy case while
    # requiring explicit dimensions on every variable-height diagram and on newly authored
    # fixed diagrams that provide either attribute.
    legacy_fixed_without_root_size = (
        raw_width is None
        and raw_height is None
        and view_width == HERO_SIZE[0]
        and view_height == HERO_SIZE[1]
    )
    width = _svg_decimal(raw_width)
    height = _svg_decimal(raw_height)
    if not legacy_fixed_without_root_size and (width is None or height is None):
        problems.append(
            Problem(
                "error",
                "svg_dimensions",
                "body diagram root width and height must be finite unitless numbers",
            )
        )
    elif not legacy_fixed_without_root_size and (width != view_width or height != view_height):
        problems.append(
            Problem(
                "error",
                "svg_dimensions",
                "body diagram root width and height must equal its viewBox dimensions",
            )
        )
    if problems:
        return None, problems
    return (int(view_width), int(view_height)), []


def _validated_body_svg_dimensions(text: str) -> tuple[int, int] | None:
    """Return dimensions only when the SVG root and body coordinate-space rules pass."""
    try:
        root = _parse_svg(text)
    except PackIngestError:
        return None
    if root.tag != f"{SVG_NS}svg":
        return None
    dimensions, problems = _body_svg_dimensions(root)
    return dimensions if not problems else None


def check_svg(text: str, *, body: bool = False) -> list[Problem]:
    """Validate a safe, accessible diagram with readable labels.

    The default keeps the fixed 1600x900 contract used by hero and series callers. ``body``
    enables only the validated 1600px-wide, variable-height coordinate-space contract; title,
    description, external-resource, script and minimum-label checks remain identical.
    """
    problems: list[Problem] = []
    try:
        root = _parse_svg(text)
    except PackIngestError as error:
        return [Problem("error", "svg_invalid", str(error))]
    if root.tag != f"{SVG_NS}svg":
        return [Problem("error", "svg_invalid", "the root element is not <svg>")]
    if body:
        _dimensions, dimension_problems = _body_svg_dimensions(root)
        problems.extend(dimension_problems)
    else:
        viewbox = re.sub(r"\s+", " ", root.get("viewBox", "").strip())
        if viewbox != DIAGRAM_VIEWBOX:
            problems.append(
                Problem(
                    "error",
                    "svg_viewbox",
                    f"viewBox is '{viewbox}', must be '{DIAGRAM_VIEWBOX}'",
                )
            )
    for name in ("title", "desc"):
        node = root.find(f"{SVG_NS}{name}")
        if node is None or not "".join(node.itertext()).strip():
            problems.append(Problem("error", f"svg_no_{name}", f"the SVG has no <{name}>"))
    for tag in ("script", "foreignObject", "image", "use"):
        if root.find(f".//{SVG_NS}{tag}") is not None:
            problems.append(Problem("error", "svg_forbidden_element", f"<{tag}> is not allowed"))
    # External references: anything that would make the reader's browser fetch a resource.
    # Namespace declarations are URLs too, so they are stripped before looking.
    stripped = re.sub(r"xmlns(?::\w+)?\s*=\s*\"[^\"]*\"", "", text)
    if re.search(r"https?://", stripped):
        problems.append(Problem("error", "svg_external_reference", "an http(s) URL"))
    if "@import" in stripped:
        problems.append(Problem("error", "svg_external_reference", "a CSS @import"))
    if re.search(r"url\(\s*[\"']?(?!#)", stripped):
        problems.append(
            Problem("error", "svg_external_reference", "a url() that is not a #fragment")
        )
    small = sorted({float(m) for m in _FONT_SIZE.findall(text) if float(m) < MIN_LABEL_PX})
    if small:
        problems.append(
            Problem(
                "error",
                "svg_small_label",
                f"font-size {', '.join(str(s) for s in small)} below {MIN_LABEL_PX} px",
            )
        )
    return problems


def diagram_numbers(text: str) -> set[str]:
    """Every number drawn as a label. ``<title>``/``<desc>`` are not labels."""
    root = _parse_svg(text)
    found: set[str] = set()
    for tag in ("text", "tspan"):
        for node in root.iter(f"{SVG_NS}{tag}"):
            for piece in (node.text or "", node.tail or ""):
                found.update(_NUMBER.findall(piece))
    return found


def missing_diagram_numbers(text: str, document: GuideDocument) -> list[str]:
    """Numbers on the diagram the article's own text does not carry -- the rule that a fare or
    a time the article never verified is not drawn. Both sides are compared with thousands
    separators and leading zeros dropped, so 1,000 and 1000 agree and so do 06:30 and 6:30."""
    body = _normalise_numbers(_document_text(document))
    return sorted(
        number for number in diagram_numbers(text) if _normalise_number(number) not in body
    )


def _normalise_number(token: str) -> str:
    """``1,000`` → ``1000``, ``06:30`` → ``6:30``, ``09`` → ``9``: the same figure however the
    writer typed it."""
    groups = [group.lstrip("0") or "0" for group in token.replace(",", "").split(":")]
    return ":".join(groups)


def _normalise_numbers(text: str) -> str:
    return _NUMBER.sub(lambda m: _normalise_number(m.group(0)), text)


# --- pictures -----------------------------------------------------------------------------


@dataclass(frozen=True)
class CommonsInfo:
    title: str
    author: str
    license: str
    file_page: str
    image_url: str
    width: int
    height: int


def _normalise_license(value: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", "", value)).strip().lower()
    # "CC-BY-SA-3.0" and "CC BY-SA 3.0" are the same licence written two ways.
    text = re.sub(r"^cc-by", "cc by", text)
    text = re.sub(r"-(?=\d)", " ", text)
    return re.sub(r"\s+", " ", text)


def license_allowed(short_name: str) -> bool:
    return ALLOWED_LICENSE.match(_normalise_license(short_name)) is not None


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Stop urllib from following a redirect, so the caller can decide about the next hop."""

    def redirect_request(self, *_: object, **__: object) -> None:
        return None


def _header_bytes(message: Message) -> list[tuple[bytes, bytes]]:
    """A urllib response's headers as the bytes the server sent, for ``httpx.Response``.

    ``http.client`` decodes every header line as ISO-8859-1, so a value that carries UTF-8 --
    the file name of a Commons picture, which is Japanese, Korean, Thai or Vietnamese for
    many of the places this site writes about -- reaches Python as a ``str`` of mojibake.
    Handed to ``httpx.Response`` as ``str`` it is re-encoded as ASCII, and the first byte
    over 0x7F raises ``UnicodeEncodeError`` (batch 7's 瑞鳳殿 photograph). Reversing the
    ISO-8859-1 decode cannot fail and gives back the exact bytes; httpx then chooses the
    charset itself (ASCII, UTF-8, ISO-8859-1), so ``response.headers[...]`` reads the UTF-8
    the server meant, and a redirect ``Location`` with such bytes is followed rather than
    fatal. Pairs rather than a dict, so a repeated header (``Vary``, ``Set-Cookie``) keeps
    every value."""
    return [(name.encode("latin-1"), value.encode("latin-1")) for name, value in message.items()]


class UrllibTransport(httpx.BaseTransport):
    """httpx over the standard library's ``urllib``.

    Wikimedia's edge answers httpx's own connections with 403 "Please respect our robot
    policy" whatever the User-Agent says, while the same request from ``urllib`` (and curl)
    goes through; the block keys on the client, not the header. Routing httpx through
    ``urllib`` keeps the ``httpx.Client`` seam the tests mock while sending a request the
    edge accepts. Only GET is needed here.
    """

    #: ``urlopen`` is not an HTTP client: it also opens ``file:``, ``ftp:`` and ``data:``.
    #: The URL it is handed is not always a constant of this module — ``fetch_image`` passes
    #: whatever Commons returned as ``thumburl`` or ``url`` — so without this the set of
    #: things it can open is "whatever Commons says" rather than "an HTTPS URL", and a
    #: ``file:///…`` answer would be read off the operator's disk into an article image.
    ALLOWED_SCHEMES = frozenset({"http", "https"})

    #: Redirects are httpx's job, not urllib's. Left to itself ``urlopen`` follows them
    #: internally, which means the hop never comes back through ``handle_request`` and the
    #: check above sees only the first URL — and urllib's own redirect rule allows ``ftp:``
    #: as well as http and https, so a redirect could still leave the two schemes this
    #: transport is willing to speak. Handing the 3xx back to httpx (``commons_client`` sets
    #: ``follow_redirects=True``) makes every hop re-enter this method and face the same check.
    _OPENER = urllib.request.build_opener(_NoRedirect)

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        if request.url.scheme not in self.ALLOWED_SCHEMES:
            # Raised rather than returned as a status: `_get` retries some of those, and this
            # is not a condition a retry can improve.
            raise PackIngestError(f"refusing a {request.url.scheme!r} URL: {request.url}")
        raw = urllib.request.Request(
            str(request.url),
            headers={key.decode(): value.decode() for key, value in request.headers.raw},
            method=request.method,
        )
        try:
            with self._OPENER.open(raw, timeout=60) as answer:
                return httpx.Response(
                    answer.status, headers=_header_bytes(answer.headers), content=answer.read()
                )
        except urllib.error.HTTPError as error:
            # A 3xx arrives here too, now that urllib no longer follows it, and is returned
            # with its Location intact for httpx to follow.
            return httpx.Response(
                error.code, headers=_header_bytes(error.headers), content=error.read()
            )


def commons_client() -> httpx.Client:
    """The client the CLI uses for Commons: urllib underneath, redirects followed."""
    return httpx.Client(transport=UrllibTransport(), follow_redirects=True, timeout=60)


#: Commons rate-limits a busy egress with 429; wait and retry a few times before giving up.
RETRY_STATUSES = frozenset({429, 502, 503})
RETRY_ATTEMPTS = 5


def _get(client: httpx.Client, url: str, **kwargs: Any) -> httpx.Response:
    response = client.get(url, headers={"User-Agent": USER_AGENT}, **kwargs)
    for _ in range(RETRY_ATTEMPTS):
        if response.status_code not in RETRY_STATUSES:
            break
        wait = response.headers.get("retry-after")
        time.sleep(min(float(wait), 120.0) if wait and wait.isdigit() else 30.0)
        response = client.get(url, headers={"User-Agent": USER_AGENT}, **kwargs)
    return response


def _strip_html(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", value))).strip()


def commons_file_info(client: httpx.Client, title: str) -> CommonsInfo:
    """The licence, author, file page and a ≤1600 px rendition of one Commons file, from the
    API rather than a page scrape. Refuses a licence outside the allowlist."""
    name = title if title.startswith("File:") else f"File:{title}"
    response = _get(
        client,
        COMMONS_API,
        params={
            "action": "query",
            "titles": name,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|size",
            "iiurlwidth": str(HERO_SIZE[0]),
            "format": "json",
        },
    )
    _raise_for_status(response, name)
    pages = response.json().get("query", {}).get("pages", {})
    page: dict[str, Any] = next(iter(pages.values()), {})
    info = (page.get("imageinfo") or [None])[0]
    if info is None:
        raise PackIngestError(f"{name}: not found on Commons")
    meta = info.get("extmetadata", {})
    short = _strip_html(meta.get("LicenseShortName", {}).get("value", ""))
    if not short or not license_allowed(short):
        raise PackIngestError(f"{name}: licence '{short or 'unknown'}' is not allowed")
    author = _strip_html(meta.get("Artist", {}).get("value", ""))
    if not author:
        raise PackIngestError(f"{name}: no author on the file page")
    return CommonsInfo(
        title=name,
        author=author[:120],
        license=short[:60],
        file_page=info["descriptionurl"],
        image_url=info.get("thumburl") or info["url"],
        width=int(info.get("thumbwidth") or info["width"]),
        height=int(info.get("thumbheight") or info["height"]),
    )


def _raise_for_status(response: httpx.Response, what: str) -> None:
    """A refused or failed download is a workspace problem the report should name, not a
    traceback."""
    if response.is_error:
        raise PackIngestError(f"{what}: Commons answered HTTP {response.status_code}")


def fetch_image(client: httpx.Client, url: str) -> Image.Image:
    response = _get(client, url)
    _raise_for_status(response, url)
    image = Image.open(io.BytesIO(response.content))
    image.load()
    return image


def fit_bytes(
    image: Image.Image,
    dest: Path,
    max_bytes: int,
    fmt: Literal["JPEG", "WEBP"],
    *,
    hard_cap: int | None = None,
) -> tuple[int, int]:
    """Save under the byte cap: quality first, then size. Returns the final (width, height).

    With ``hard_cap``, a picture that only reaches the cap at the quality floor is kept at full
    size as long as it stays under the hard cap -- a hero must stay 1600×900, and 243 KB at
    the floor is the documented case (batch 2's ``osaka-kyoto-where-to-stay``)."""
    picture = image.convert("RGB")
    first_pass = True
    while True:
        for quality in range(85, 55, -5):
            options: dict[str, Any] = {"quality": quality, "optimize": True}
            if fmt == "JPEG":
                options["progressive"] = True
            else:
                options["method"] = 6
            picture.save(dest, fmt, **options)
            if dest.stat().st_size <= max_bytes:
                return picture.size
        if first_pass and hard_cap is not None and dest.stat().st_size <= hard_cap:
            return picture.size
        first_pass = False
        if picture.width < 400:
            raise PackIngestError(f"{dest.name}: cannot fit under {max_bytes} bytes")
        picture = picture.resize(
            (round(picture.width * 0.9), round(picture.height * 0.9)), Image.Resampling.LANCZOS
        )


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Centre-crop to the aspect ratio, then resize: a hero is always 1600×900."""
    width, height = size
    scale = max(width / image.width, height / image.height)
    resized = image.resize(
        (max(width, round(image.width * scale)), max(height, round(image.height * scale))),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


Renderer = Callable[[Path, Path], None]


def chromium_binary() -> str:
    """The browser that renders SVG to PNG: ``CHROMIUM_BIN``, else Playwright's install."""
    configured = os.environ.get("CHROMIUM_BIN")
    if configured:
        return configured
    for pattern in (
        "/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell",
        "/opt/pw-browsers/chromium-*/chrome-linux/chrome",
    ):
        matches = sorted(glob(pattern))
        if matches:
            return matches[-1]
    for name in ("chromium", "chromium-browser", "google-chrome"):
        found = shutil.which(name)
        if found:
            return found
    raise PackIngestError("no Chromium found; set CHROMIUM_BIN")


def render_svg(svg: Path, png: Path, *, chromium: str | None = None) -> None:
    """Screenshot the SVG at 1600×900 with headless Chromium. The SVG is inlined into a
    one-element HTML page so it is laid out at exactly that size whatever its own width and
    height attributes say."""
    width, height = HERO_SIZE
    page = (
        "<!doctype html><meta charset='utf-8'><style>html,body{margin:0;padding:0;"
        f"background:#fff}}svg{{display:block;width:{width}px;height:{height}px}}</style>"
        + svg.read_text(encoding="utf-8")
    )
    with tempfile.TemporaryDirectory() as folder:
        html_path = Path(folder) / "render.html"
        html_path.write_text(page, encoding="utf-8")
        command = [
            chromium or chromium_binary(),
            "--headless",
            "--no-sandbox",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            f"--screenshot={png}",
            html_path.as_uri(),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if result.returncode != 0 or not png.is_file():
        raise PackIngestError(f"rendering {svg.name} failed: {result.stderr.strip()[-400:]}")


# --- ingest -------------------------------------------------------------------------------


@dataclass
class IngestReport:
    slug: str
    problems: list[Problem] = field(default_factory=list)
    written: list[Path] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not errors(self.problems)


def _known_topics(kind: Kind) -> set[str]:
    """Every topic slug the write path accepts for this section: parents and subtopics.

    ``admin_service._resolve_topics`` resolves against the ``guide_topics`` rows the
    migrations seed from these same tuples, so a pack that names a subtopic imports fine;
    until 2026-09-16 this check read the parents only and refused 805 published packs.
    """
    if section_of(kind) == "life":
        return {slug for slug, _ in LIFE_SEED_TOPICS} | {
            slug for slug, _parent, _labels in LIFE_SEED_SUBTOPICS
        }
    return {slug for slug, _ in SEED_TOPICS} | {
        slug for slug, _parent, _labels in TRAVEL_SEED_SUBTOPICS
    }


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise PackIngestError(f"{path.name}: {error}") from error


def _image_name(src: str) -> str:
    return src.rsplit("/", 1)[-1]


def _stage_hero(
    raw_hero: dict[str, Any],
    *,
    slug: str,
    source: Path,
    staging: Path,
    manifest: dict[str, Any],
    client: httpx.Client | None,
    renderer: Renderer | None,
) -> None:
    raw_hero["src"] = f"/guides/{slug}/hero.jpg"
    drawn = source / "hero.svg"
    if drawn.is_file():
        svg_problems = errors(check_svg(drawn.read_text(encoding="utf-8")))
        if svg_problems:
            raise PackIngestError("hero.svg: " + "; ".join(p.message for p in svg_problems))
        if renderer is None:
            raise PackIngestError("hero.svg needs a renderer (or pass --no-render to skip)")
        png = staging / "hero.png"
        renderer(drawn, png)
        with Image.open(png) as rendered:
            picture = cover(rendered, HERO_SIZE)
        png.unlink()
        width, height = fit_bytes(
            picture, staging / "hero.jpg", HERO_MAX_BYTES, "JPEG", hard_cap=IMAGE_HARD_CAP
        )
        shutil.copyfile(drawn, staging / "hero.svg")
        raw_hero.update(
            {"width": width, "height": height, "credit": MOKAAIR_CREDIT.model_dump(mode="json")}
        )
        return
    title = (manifest.get("hero") or {}).get("title")
    if not title:
        raise PackIngestError("no hero.svg in the workspace and images.json names no hero file")
    if client is None:
        raise PackIngestError("a Commons hero needs a network client")
    info = commons_file_info(client, title)
    picture = cover(fetch_image(client, info.image_url), HERO_SIZE)
    width, height = fit_bytes(
        picture, staging / "hero.jpg", HERO_MAX_BYTES, "JPEG", hard_cap=IMAGE_HARD_CAP
    )
    raw_hero.update(
        {
            "width": width,
            "height": height,
            "credit": {
                "author": info.author,
                "license": info.license,
                "source_url": info.file_page,
            },
        }
    )


def _stage_image_block(
    block: dict[str, Any],
    *,
    slug: str,
    source: Path,
    staging: Path,
    manifest: dict[str, Any],
    client: httpx.Client | None,
) -> list[Problem]:
    name = _image_name(str(block.get("src", "")))
    block["src"] = f"/guides/{slug}/{name}"
    stem = name.rsplit(".", 1)[0]
    if name.endswith(".svg"):
        file = source / name
        if not file.is_file():
            raise PackIngestError(f"{name}: not in the workspace")
        text = file.read_text(encoding="utf-8")
        problems = check_svg(text, body=True)
        if errors(problems):
            raise PackIngestError(f"{name}: " + "; ".join(p.message for p in errors(problems)))
        dimensions = _validated_body_svg_dimensions(text)
        if dimensions is None:
            raise PackIngestError(f"{name}: has no validated body diagram dimensions")
        shutil.copyfile(file, staging / name)
        block.update(
            {
                "width": dimensions[0],
                "height": dimensions[1],
                "credit": MOKAAIR_CREDIT.model_dump(mode="json"),
            }
        )
        return problems
    entry = (manifest.get("photos") or {}).get(stem) or {}
    if not entry.get("title"):
        raise PackIngestError(f"{name}: images.json names no Commons file for '{stem}'")
    if client is None:
        raise PackIngestError(f"{name}: a Commons photo needs a network client")
    info = commons_file_info(client, entry["title"])
    picture = fetch_image(client, info.image_url)
    if picture.width > PHOTO_MAX_WIDTH:
        picture = picture.resize(
            (PHOTO_MAX_WIDTH, round(picture.height * PHOTO_MAX_WIDTH / picture.width)),
            Image.Resampling.LANCZOS,
        )
    target = staging / f"{stem}.webp"
    width, height = fit_bytes(picture, target, PHOTO_MAX_BYTES, "WEBP")
    block["src"] = f"/guides/{slug}/{stem}.webp"
    block.update(
        {
            "width": width,
            "height": height,
            "credit": {
                "author": info.author,
                "license": info.license,
                "source_url": info.file_page,
            },
        }
    )
    return []


def ingest(
    workdir: Path,
    slug: str,
    *,
    content_dir: Path,
    public_dir: Path,
    client: httpx.Client | None = None,
    renderer: Renderer | None = None,
    dry_run: bool = False,
) -> IngestReport:
    """Build the pack and its pictures from ``<workdir>/<slug>/`` and, if nothing is wrong,
    write them into the repository: the pack under ``content_dir``, the pictures under
    ``public_dir/guides/<slug>/`` (``public_dir`` is the web app's ``public`` folder).

    Raises ``PackIngestError`` for a workspace that cannot be read; rule violations come back
    as problems, and errors among them mean nothing was written."""
    report = IngestReport(slug)
    source = workdir / slug
    if not source.is_dir():
        raise PackIngestError(f"{source}: no such workspace")
    raw = _load_json(source / "pack.json")
    if not isinstance(raw, dict):
        raise PackIngestError("pack.json must hold one object")
    raw.setdefault("slug", slug)
    if raw["slug"] != slug:
        raise PackIngestError(f"pack.json says slug '{raw['slug']}', the workspace is '{slug}'")
    manifest_path = source / "images.json"
    manifest = _load_json(manifest_path) if manifest_path.is_file() else {}

    with tempfile.TemporaryDirectory() as folder:
        staging = Path(folder)
        for locale_key, document in (raw.get("locales") or {}).items():
            if not isinstance(document, dict):
                raise PackIngestError(f"{locale_key}: the document must be an object")
            hero = document.get("hero")
            if isinstance(hero, dict) and not (staging / "hero.jpg").is_file():
                _stage_hero(
                    hero,
                    slug=slug,
                    source=source,
                    staging=staging,
                    manifest=manifest,
                    client=client,
                    renderer=renderer,
                )
            for block in document.get("blocks") or []:
                if isinstance(block, dict) and block.get("type") == "image":
                    name = _image_name(str(block.get("src", "")))
                    if (staging / name).is_file() and name.endswith(".svg"):
                        staged_text = (staging / name).read_text(encoding="utf-8")
                        dimensions = _validated_body_svg_dimensions(staged_text)
                        if dimensions is None:
                            raise PackIngestError(
                                f"{name}: staged SVG has no validated body diagram dimensions"
                            )
                        block.update(
                            {
                                "src": f"/guides/{slug}/{name}",
                                "width": dimensions[0],
                                "height": dimensions[1],
                                "credit": MOKAAIR_CREDIT.model_dump(mode="json"),
                            }
                        )
                        continue
                    report.problems.extend(
                        _stage_image_block(
                            block,
                            slug=slug,
                            source=source,
                            staging=staging,
                            manifest=manifest,
                            client=client,
                        )
                    )

        try:
            pack = ArticlePack.model_validate(raw)
        except ValidationError as error:
            report.problems.append(Problem("error", "pack_invalid", str(error)))
            return report
        unknown = set(pack.topics) - _known_topics(pack.kind)
        if unknown:
            report.problems.append(
                Problem(
                    "error",
                    "topic_unknown",
                    f"topics not in the {section_of(pack.kind)} vocabulary: "
                    + ", ".join(sorted(unknown)),
                )
            )
        try:
            destination = admin_service._validate_destination(pack.destination_id)
            for document_model in pack.locales.values():
                admin_service._validate_document(document_model, destination)
        except AppError as error:
            report.problems.append(Problem("error", error.code, error.detail))
        for locale, document_model in pack.locales.items():
            report.problems.extend(
                Problem(p.level, p.code, f"{locale}: {p.message}")
                for p in lint_document(document_model, pack.kind, topics=pack.topics)
            )
            for block_model in document_model.blocks:
                if isinstance(block_model, ImageBlock) and block_model.src.endswith(".svg"):
                    svg_text = (staging / _image_name(block_model.src)).read_text(encoding="utf-8")
                    missing = missing_diagram_numbers(svg_text, document_model)
                    if missing:
                        report.problems.append(
                            Problem(
                                "error",
                                "diagram_number_not_in_text",
                                f"{locale}: {_image_name(block_model.src)} draws "
                                f"{', '.join(missing)}, which the text does not carry",
                            )
                        )
        for file in staging.iterdir():
            size = file.stat().st_size
            if size > IMAGE_HARD_CAP:
                report.problems.append(
                    Problem("error", "image_too_large", f"{file.name} exceeds {IMAGE_HARD_CAP}")
                )
            elif file.name == "hero.jpg" and size > HERO_MAX_BYTES:
                report.problems.append(
                    Problem(
                        "warning",
                        "hero_over_guideline",
                        f"hero.jpg is {size} bytes at the quality floor; the guideline is "
                        f"{HERO_MAX_BYTES}",
                    )
                )
        if not report.ok or dry_run:
            return report

        target = public_dir / "guides" / slug
        target.mkdir(parents=True, exist_ok=True)
        for file in sorted(staging.iterdir()):
            shutil.copyfile(file, target / file.name)
            report.written.append(target / file.name)
        content_dir.mkdir(parents=True, exist_ok=True)
        pack_path = content_dir / f"{slug}.json"
        encoded = pack.model_dump(mode="json")
        # The optional link fields are left out while empty, so a pack reads as it did
        # before they existed and a later ``relink``/``autolink`` diff is the links alone.
        for optional in ("aliases", "related"):
            if not encoded.get(optional):
                encoded.pop(optional, None)
        pack_path.write_text(
            json.dumps(encoded, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        report.written.append(pack_path)
    return report


# --- lint ---------------------------------------------------------------------------------

_CATALOGUE_ROW = re.compile(r"^\|\s*\d+\s*\|\s*`([a-z0-9-]+)`\s*\|")


def catalogue_slugs(markdown: str) -> set[str]:
    """The slugs a series catalogue (``docs/life-ai-series.md``) lists: one table row each,
    the slug in backticks in the second column."""
    return {m.group(1) for line in markdown.splitlines() if (m := _CATALOGUE_ROW.match(line))}


def _iter_svgs(
    pack: ArticlePack, public_dir: Path
) -> Iterator[tuple[Locale, GuideDocument, ImageBlock, Path]]:
    for locale, document in pack.locales.items():
        for block in document.blocks:
            if isinstance(block, ImageBlock) and block.src.endswith(".svg"):
                yield locale, document, block, public_dir / block.src.lstrip("/")


def lint_all(
    content_dir: Path,
    public_dir: Path,
    *,
    kind: Kind | None = None,
    slugs: set[str] | None = None,
    render_dir: Path | None = None,
    renderer: Renderer | None = None,
    catalogue: Path | None = None,
) -> dict[str, list[Problem]]:
    """The rules over every pack that ships, keyed by slug. Two extra keys: ``catalogue`` for
    the difference between the series list and the packs, and ``sitemap`` when one child
    sitemap's (article, locale) rows approach its limit -- counted over every pack, whatever
    ``kind`` or ``slugs`` narrowed the run to, because the budget is the site's."""
    findings: dict[str, list[Problem]] = {}
    try:
        packs = load_packs(content_dir)
    except ContentPackError as error:
        return {"content": [Problem("error", "pack_invalid", str(error))]}
    chosen = [
        pack
        for pack in packs
        if (kind is None or pack.kind == kind) and (slugs is None or pack.slug in slugs)
    ]
    for pack in chosen:
        problems: list[Problem] = []
        for locale, document in pack.locales.items():
            problems.extend(
                Problem(p.level, p.code, f"{locale}: {p.message}")
                for p in lint_document(document, pack.kind, topics=pack.topics)
            )
            pictures = [document.hero.src] if document.hero else []
            pictures += [b.src for b in document.blocks if isinstance(b, ImageBlock)]
            for src in pictures:
                file = public_dir / src.lstrip("/")
                if not file.is_file():
                    problems.append(Problem("error", "image_missing", f"{locale}: {src}"))
                elif file.stat().st_size > IMAGE_HARD_CAP:
                    problems.append(Problem("error", "image_too_large", f"{locale}: {src}"))
        seen: set[Path] = set()
        svg_cache: dict[Path, tuple[str, list[Problem], tuple[int, int] | None]] = {}
        for locale, document, block, svg in _iter_svgs(pack, public_dir):
            if not svg.is_file():
                continue
            cached = svg_cache.get(svg)
            if cached is None:
                text = svg.read_text(encoding="utf-8")
                svg_problems = check_svg(text, body=True)
                dimensions = _validated_body_svg_dimensions(text)
                svg_cache[svg] = (text, svg_problems, dimensions)
                seen.add(svg)
                problems.extend(
                    Problem(p.level, p.code, f"{svg.name}: {p.message}") for p in svg_problems
                )
            else:
                text, svg_problems, dimensions = cached
            if dimensions is not None and (block.width, block.height) != dimensions:
                problems.append(
                    Problem(
                        "error",
                        "svg_dimensions_mismatch",
                        f"{locale}: {svg.name} declares {block.width}x{block.height}; "
                        f"the SVG is {dimensions[0]}x{dimensions[1]}",
                    )
                )
            if not errors(svg_problems):
                missing = missing_diagram_numbers(text, document)
                if missing:
                    problems.append(
                        Problem(
                            "error",
                            "diagram_number_not_in_text",
                            f"{locale}: {svg.name} draws {', '.join(missing)}, "
                            "which the text does not carry",
                        )
                    )
        if render_dir is not None:
            render = renderer or render_svg
            render_dir.mkdir(parents=True, exist_ok=True)
            hero_svg = public_dir / "guides" / pack.slug / "hero.svg"
            targets = list(seen) + ([hero_svg] if hero_svg.is_file() else [])
            for svg in targets:
                try:
                    render(svg, render_dir / f"{pack.slug}-{svg.stem}.png")
                except PackIngestError as error:
                    problems.append(Problem("warning", "render_failed", str(error)))
        findings[pack.slug] = problems
    if catalogue is not None:
        listed = catalogue_slugs(catalogue.read_text(encoding="utf-8"))
        have = {pack.slug for pack in packs}
        notes: list[Problem] = []
        for slug in sorted(listed - have):
            notes.append(Problem("warning", "catalogue_missing_pack", f"{slug}: not written yet"))
        # A catalogue lists one series; the section holds articles outside it (the household
        # and productivity pieces, the finance batches). Those are not gaps, so they get one
        # line for the record rather than a warning each, which buried the real gaps.
        outside = sorted(
            pack.slug for pack in packs if pack.kind == "life" and pack.slug not in listed
        )
        if outside:
            shown = ", ".join(outside[:5]) + (", …" if len(outside) > 5 else "")
            notes.append(
                Problem(
                    "info",
                    "packs_outside_catalogue",
                    f"{len(outside)} life pack(s) are not in this list, which is fine: {shown}",
                )
            )
        findings["catalogue"] = notes
    return findings


def sitemap_children(packs: list[ArticlePack]) -> dict[str, int]:
    """(article, locale) rows per section and locale, keyed ``{section}-{locale}`` as the
    web names the first child sitemap of each. Informational only: the web slices a section
    and locale into as many numbered children as its rows need (``SITEMAP_CHILD_LIMIT`` in
    ``apps/web/lib/guides.server.ts``), so there is no ceiling for a lint to warn about."""
    rows: dict[str, int] = {}
    for pack in packs:
        for locale in pack.locales:
            key = f"{section_of(pack.kind)}-{locale}"
            rows[key] = rows.get(key, 0) + 1
    return rows
