"""``pack_cli jev-review``: Jev reads the packs and says what to look at. Nothing is written.

Two checks, both advisory, both offline in the sense that matters -- they run from a
terminal over a directory of files, never from a request, and no pack, database row or
rendered page is touched by either.

``editorial`` asks, once per text unit of one document, whether that unit is talking to the
article's editor instead of to the traveller. That is the defect the owner's 2026-09-21
rejection named: verification discipline written into the body ("the official page does not
state it, so we did not label it"), a Korean field name copied out of a listing, a sentence
left untranslated. The question is phrased as the defect, so a high noul means "look at
this", and the deterministic ``signals`` column beside it is the regex baseline the model
has to beat before a network call is worth making. Counting rules -- one self-reference per
article, one sourcing sentence per section -- stay with the regexes: TypeSafe publishes that
Jev does not count reliably, so nothing here asks it to.

``overlap`` asks whether a proposed article repeats one that is already published. The
catalogue is bigger than one question can hold, so it is ranked by character-bigram Dice
similarity (the likeliest duplicates first, where a spent budget costs least), split into
chunks under the vendor's option and token caps, and the union of each chunk's best answers
is re-asked in one final round -- without that round two chunks' probabilities are not
comparable, and the report says so rather than pretending otherwise.

Why there is no Redis budget here. Every other Jev call site spends ``consume_jev_call``'s
daily counter, because it runs inside the API or the worker where an unbounded number of
requests share one vendor account. This one is a command a person runs: one process, one
directory, a call count known before the first call is sent (``--dry-run`` prints it) and
refused outright when it is over ``--max-calls``. The measured corpus costs about two cents.
A Redis dependency would only mean the command cannot run on a laptop or against a
``git archive`` export of an older content directory, which is exactly where it is useful.

The answers are for a person to read. ``JEV_CJK_AUTOPILOT_ENABLED`` ships false and every
document here is Chinese, so ``route_answer`` can never return ``act``; the report says so at
the top and at the bottom, and the exit code is 0 however many units are flagged.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx
from pydantic import ValidationError

from app.ai.jev import (
    MAX_CHOICE_OPTIONS,
    USD_PER_INPUT_TOKEN,
    ChoiceAnswer,
    ChoiceQuestion,
    JevAnswer,
    JevClient,
    JevError,
    JevQuestion,
    JevRequestTooLarge,
    NoulAnswer,
    NoulQuestion,
    estimate_tokens,
    jev_client,
    route_answer,
)
from app.config import Settings
from app.guides.content_pack import ArticlePack, default_directory
from app.guides.schemas import (
    SECTION_KINDS,
    CalloutBlock,
    FaqBlock,
    GuideDocument,
    ImageBlock,
    Kind,
    RichParagraphBlock,
    SummaryBlock,
    TableBlock,
    section_of,
)
from app.site_pages.schemas import HeadingBlock, ListBlock, ParagraphBlock


class JevReviewError(ValueError):
    """A run that cannot start, or a report that cannot be read.

    Deliberately not an ``AppError``: nothing here is a sentence a reader is ever shown,
    and ``tests/test_error_localization.py`` holds every reader-facing module to a
    translated sentence per error code.
    """


NOTICE = (
    "Advisory only. TypeSafe publishes Jev's accuracy for English only; while "
    "JEV_CJK_AUTOPILOT_ENABLED is false a zh-TW answer is at most 'confirm' and is for a "
    "person to read. No pack was modified."
)

# --- the editorial question ---------------------------------------------------------------

EDITORIAL_QUESTION = (
    "Unit {unit_id} addresses the article's editor or describes how the article was "
    "researched, instead of telling the traveller about the place."
)
EDITORIAL_CRITERIA: dict[str, str] = {
    "true": (
        "The unit refers to the article itself (本文, 這篇), narrates verification "
        "or sourcing (what the official page wrote or did not state, what we could "
        "not confirm and so did not label), reproduces a Korean or Japanese field "
        "name from an official page, or leaves a Korean or Japanese sentence "
        "untranslated."
    ),
    "false": (
        "The unit tells the traveller what the place, shop, dish or route is, how to "
        "get there, when it opens, what to order or what to watch out for, in Chinese "
        "a reader who knows no Korean or Japanese can follow; a foreign name carries a "
        "Chinese name or a romanisation."
    ),
}

# --- the overlap questions ----------------------------------------------------------------

SAME_ARTICLE_QUESTION = (
    "Which article in existing_articles answers the same reader question as the proposal: "
    "the same place or subject and the same task, so a reader who has read it would learn "
    "nothing new from the proposal?"
)
NONE_OPTION = "No listed article answers the same reader question."
OVERLAP_QUESTION = (
    "At least one article in existing_articles substantially overlaps the proposal: it "
    "covers the same place or subject and the same reader task, so publishing the proposal "
    "would repeat it."
)
OVERLAP_CRITERIA: dict[str, str] = {
    "true": (
        "Same subject and same task, for example two three-day itineraries of the same "
        "city, or two explanations of the same fee table."
    ),
    "false": (
        "Only the destination or the topic is shared; the proposal answers a different "
        "question, such as a different day trip, a different procedure or a different "
        "year's rule."
    ),
}

# --- the numbers ---------------------------------------------------------------------------

DEFAULT_MAX_CALLS = 50
DEFAULT_CHUNK_SIZE = 80
DEFAULT_TOP = 5
#: ``none`` takes the last of the vendor's option slots, so a chunk holds one fewer article.
MAX_CHUNK_CANDIDATES = MAX_CHOICE_OPTIONS - 1
#: How much of ``jev_max_state_tokens`` a chunk may plan to fill. The estimate is a model of
#: the vendor's tokeniser, not the tokeniser; the fifth left over is what keeps a chunk that
#: measured just under the cap from arriving just over it.
STATE_HEADROOM = 0.8
EXCERPT_CHARS = 80
#: Above this share of Hangul a zh-TW unit is quoting a Korean page, not translating it.
HANGUL_SHARE = 0.3

_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("self_reference", re.compile(r"本文|這篇")),
    ("sourcing", re.compile(r"官方頁(寫|說|的)|我們(就)?不標|不是我們加的")),
    ("field_name_ko", re.compile(r"교통\s?정보|대표메뉴")),
)
_HANGUL = re.compile(r"[가-힣]")


def signals_for(text: str) -> list[str]:
    """The deterministic baseline: what a regex alone can see in one unit.

    This is not a fallback for Jev and not a filter in front of it. It is the number the
    model is measured against -- a check whose flags the regexes already found has not
    earned its network call -- and the ``flagged_without_signal`` total is where the value,
    if there is any, shows up.
    """
    found = [name for name, pattern in _SIGNALS if pattern.search(text)]
    letters = len(text)
    if letters and len(_HANGUL.findall(text)) / letters > HANGUL_SHARE:
        found.append("hangul_heavy")
    return found


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _excerpt(text: str) -> str:
    return " ".join(text.split())[:EXCERPT_CHARS]


@dataclass(frozen=True)
class TextUnit:
    """One thing a reader reads, and the smallest thing worth asking a question about."""

    unit_id: str
    block_index: int
    kind: str
    text: str

    @property
    def sha(self) -> str:
        """Stable across versions of the same article, so ``compare`` can tell a unit that
        was rewritten from one that was left alone."""
        return _sha(self.text)

    @property
    def signals(self) -> list[str]:
        return signals_for(self.text)

    def as_state(self) -> dict[str, str]:
        return {"id": self.unit_id, "kind": self.kind, "text": self.text}

    def as_row(self) -> dict[str, Any]:
        return {
            "unit_id": self.unit_id,
            "block_index": self.block_index,
            "kind": self.kind,
            "chars": len(self.text),
            "sha": self.sha,
            "excerpt": _excerpt(self.text),
            "signals": self.signals,
        }


def extract_units(document: GuideDocument) -> list[TextUnit]:
    """Every text unit of one document, in reading order.

    Several block types are deliberately absent. ``image.description`` is a transcription of
    what a diagram already draws -- field names and all -- so it would be flagged forever and
    never be wrong. Table cells are fragments that no question about editorial voice can be
    asked of; the caption above them can. ``code`` is a command, and ``link``, ``offer`` and
    ``partner_link`` are labels on a button.
    """
    units: list[TextUnit] = []

    def add(block_index: int, kind: str, text: str) -> None:
        if not text.strip():
            return
        units.append(TextUnit(f"u{len(units) + 1:03d}", block_index, kind, text))

    add(-1, "title", document.title)
    add(-1, "description", document.description)
    for index, block in enumerate(document.blocks):
        if isinstance(block, HeadingBlock):
            add(index, "heading", block.text)
        elif isinstance(block, ParagraphBlock):
            add(index, "paragraph", block.text)
        elif isinstance(block, RichParagraphBlock):
            add(index, "rich_paragraph", "".join(node.text for node in block.inlines))
        elif isinstance(block, ListBlock):
            add(index, "list", "\n".join(block.items))
        elif isinstance(block, CalloutBlock):
            add(index, "callout", "\n".join(part for part in (block.title, block.text) if part))
        elif isinstance(block, TableBlock):
            add(index, "table.caption", block.caption)
        elif isinstance(block, ImageBlock):
            add(index, "image.caption", block.caption)
        elif isinstance(block, SummaryBlock):
            for item in block.items:
                add(index, "summary", item)
        elif isinstance(block, FaqBlock):
            for entry in block.items:
                add(index, "faq", f"{entry.question}\n{entry.answer}")
    return units


# --- budget and report plumbing -------------------------------------------------------------


@dataclass
class Usage:
    max_calls: int = DEFAULT_MAX_CALLS
    calls: int = 0
    input_tokens: int = 0
    planned_calls: int = 0
    planned_input_tokens: int = 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "calls": self.calls,
            "input_tokens": self.input_tokens,
            "usd": round(self.input_tokens * USD_PER_INPUT_TOKEN, 6),
            "max_calls": self.max_calls,
            "planned_calls": self.planned_calls,
            "planned_input_tokens": self.planned_input_tokens,
            "planned_usd": round(self.planned_input_tokens * USD_PER_INPUT_TOKEN, 6),
        }


def _error_line(exc: BaseException) -> str:
    """One line about a failure, with no key, URL or response body in it."""
    return f"{type(exc).__name__}: {str(exc)[:160]}"


def _header(tool: str, content_dir: Path, settings: Settings, *, dry_run: bool) -> dict[str, Any]:
    return {
        "tool": tool,
        "advisory": True,
        "notice": NOTICE,
        "generated_at": datetime.now(UTC).isoformat(),
        "content_dir": str(content_dir),
        "model": settings.jev_model,
        "dry_run": dry_run,
        "thresholds": {
            "act": settings.jev_act_confidence,
            "flag": settings.jev_flag_confidence,
            "cjk_autopilot": settings.jev_cjk_autopilot_enabled,
        },
    }


def _require_key(settings: Settings) -> None:
    if not settings.jev_configured:
        raise JevReviewError(
            "JEV_API_KEY is not set in the environment or ../../.env; nothing was sent"
        )


def _require_budget(planned: int, max_calls: int, *, narrow: str) -> None:
    if planned > max_calls:
        raise JevReviewError(
            f"the plan needs {planned} calls and --max-calls is {max_calls}; "
            f"narrow the run ({narrow}) or raise --max-calls"
        )


def _noul_of(answer: JevAnswer) -> float | None:
    return answer.noul if isinstance(answer, NoulAnswer) else None


def _rate(part: int, whole: int) -> float | None:
    return round(part / whole, 4) if whole else None


# --- check one: editorial -------------------------------------------------------------------


@dataclass
class DocumentPlan:
    slug: str
    kind: Kind
    destination_id: str | None
    locale: str
    units: list[TextUnit]

    def state(self, units: Sequence[TextUnit]) -> dict[str, Any]:
        return {
            "slug": self.slug,
            "kind": self.kind,
            "destination_id": self.destination_id,
            "locale": self.locale,
            "units": [unit.as_state() for unit in units],
        }

    def questions(self, units: Sequence[TextUnit]) -> dict[str, JevQuestion]:
        return {
            unit.unit_id: NoulQuestion(
                instructions=EDITORIAL_QUESTION.format(unit_id=unit.unit_id),
                criteria=dict(EDITORIAL_CRITERIA),
            )
            for unit in units
        }

    def input_tokens(self) -> int:
        questions = self.questions(self.units)
        return estimate_tokens(self.state(self.units)) + sum(
            estimate_tokens(question.model_dump(exclude_none=True))
            for question in questions.values()
        )


@dataclass
class EditorialPlan:
    content_dir: Path
    locale: str
    documents: list[DocumentPlan] = field(default_factory=list)
    skipped: list[dict[str, str]] = field(default_factory=list)

    @property
    def calls(self) -> int:
        """One call per document. A document too big for one is halved on the vendor's own
        refusal, which spends more, so ``--max-calls`` is checked again before every call."""
        return len(self.documents)

    @property
    def units(self) -> int:
        return sum(len(document.units) for document in self.documents)

    @property
    def input_tokens(self) -> int:
        return sum(document.input_tokens() for document in self.documents)


def _matches(raw: Mapping[str, Any], kinds: Sequence[str], topics: Sequence[str]) -> bool:
    if kinds and str(raw.get("kind")) not in kinds:
        return False
    if topics:
        found = {str(topic) for topic in raw.get("topics") or []}
        if not found & set(topics):
            return False
    return True


def _read_raw(path: Path) -> dict[str, Any] | None:
    """One pack, or ``None`` when the file is not a pack-shaped object.

    Read file by file rather than through ``load_packs``: this command is pointed at
    ``git archive`` exports of older content directories, and one pack that no longer
    validates must not take the other nine hundred with it.
    """
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return raw if isinstance(raw, dict) else None


def plan_editorial(
    content_dir: Path | None = None,
    *,
    locale: str = "zh-TW",
    kinds: Sequence[str] = (),
    slugs: set[str] | None = None,
    prefixes: Sequence[str] = (),
    limit: int | None = None,
) -> EditorialPlan:
    root = content_dir or default_directory()
    plan = EditorialPlan(root, locale)
    for path in sorted(root.glob("*.json")) if root.is_dir() else []:
        slug = path.stem
        if slugs is not None and slug not in slugs:
            continue
        if prefixes and not any(slug.startswith(prefix) for prefix in prefixes):
            continue
        raw = _read_raw(path)
        if raw is None:
            plan.skipped.append({"slug": slug, "reason": "not readable as a content pack"})
            continue
        if not _matches(raw, kinds, ()):
            continue
        try:
            pack = ArticlePack.model_validate(raw)
        except ValidationError as error:
            plan.skipped.append({"slug": slug, "reason": f"invalid pack: {str(error)[:160]}"})
            continue
        document = next((doc for loc, doc in pack.locales.items() if loc == locale), None)
        if document is None:
            plan.skipped.append({"slug": slug, "reason": f"no {locale} document"})
            continue
        units = extract_units(document)
        if not units:
            plan.skipped.append({"slug": slug, "reason": "no reviewable text units"})
            continue
        plan.documents.append(
            DocumentPlan(pack.slug, pack.kind, pack.destination_id, locale, units)
        )
        if limit is not None and len(plan.documents) >= limit:
            break
    return plan


async def _ask_document(
    jev: JevClient,
    document: DocumentPlan,
    usage: Usage,
) -> tuple[dict[str, JevAnswer], list[str], bool]:
    """One document's answers, halving on the vendor's size refusal rather than dropping.

    A batch that comes back too large is split and both halves go to the front of the queue,
    so every unit is still asked about -- the pattern ``hotspots/ai_search`` uses for the
    same reason. Returns ``(answers, errors, halt)``; ``halt`` means the run should stop
    rather than move on to the next document.
    """
    answers: dict[str, JevAnswer] = {}
    errors: list[str] = []
    pending: list[list[TextUnit]] = [list(document.units)]
    while pending:
        batch = pending.pop(0)
        if not batch:
            continue
        if usage.calls >= usage.max_calls:
            errors.append(f"max_calls_reached after {usage.calls} calls")
            return answers, errors, True
        try:
            batch_answers, call_usage = await jev.ask(
                document.state(batch), document.questions(batch)
            )
        except JevRequestTooLarge:
            if len(batch) == 1:
                errors.append(f"too_large: {batch[0].unit_id}")
                continue
            middle = len(batch) // 2
            pending[:0] = [batch[:middle], batch[middle:]]
            continue
        except (JevError, httpx.HTTPError) as exc:
            errors.append(_error_line(exc))
            return answers, errors, True
        usage.calls += 1
        usage.input_tokens += int(call_usage.get("input_tokens", 0))
        answers.update(batch_answers)
    return answers, errors, False


def _document_report(
    document: DocumentPlan,
    answers: Mapping[str, JevAnswer],
    settings: Settings,
    *,
    errors: Sequence[str],
    calls: int,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    answered = 0
    flagged = 0
    regex_hits = 0
    total_noul = 0.0
    for unit in document.units:
        row = unit.as_row()
        answer = answers.get(unit.unit_id)
        noul = _noul_of(answer) if answer is not None else None
        if answer is not None and noul is not None:
            answered += 1
            total_noul += noul
            row["noul"] = round(noul, 4)
            row["tier"] = route_answer(answer, settings, locale=document.locale)
            row["flagged"] = noul >= settings.jev_flag_confidence
        else:
            row["noul"] = None
            row["tier"] = None
            row["flagged"] = False
        flagged += int(bool(row["flagged"]))
        regex_hits += int(bool(row["signals"]))
        rows.append(row)
    return {
        "slug": document.slug,
        "kind": document.kind,
        "units": len(document.units),
        "answered": answered,
        "flagged": flagged,
        "flag_rate": _rate(flagged, answered),
        "mean_noul": round(total_noul / answered, 4) if answered else None,
        "regex_hits": regex_hits,
        "calls": calls,
        "errors": list(errors),
        "rows": rows,
    }


async def run_editorial(
    plan: EditorialPlan,
    settings: Settings,
    *,
    dry_run: bool = False,
    max_calls: int = DEFAULT_MAX_CALLS,
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    usage = Usage(max_calls=max_calls)
    usage.planned_calls = plan.calls
    usage.planned_input_tokens = plan.input_tokens
    errors: list[str] = []
    answers: dict[str, dict[str, JevAnswer]] = {}
    document_calls: dict[str, int] = {}
    document_errors: dict[str, list[str]] = {}

    if not dry_run:
        _require_key(settings)
        _require_budget(plan.calls, max_calls, narrow="--slug, --prefix, --kind or --limit")
        jev = jev_client(settings, client)
        try:
            for document in plan.documents:
                before = usage.calls
                found, failures, halt = await _ask_document(jev, document, usage)
                answers[document.slug] = found
                document_calls[document.slug] = usage.calls - before
                document_errors[document.slug] = failures
                errors.extend(f"{document.slug}: {failure}" for failure in failures)
                if halt:
                    break
        finally:
            await jev.close()

    report = _header("jev-review editorial", plan.content_dir, settings, dry_run=dry_run)
    report["locale"] = plan.locale
    report["question"] = {
        "instructions": EDITORIAL_QUESTION,
        "criteria": dict(EDITORIAL_CRITERIA),
    }
    documents = [
        _document_report(
            document,
            answers.get(document.slug, {}),
            settings,
            errors=document_errors.get(document.slug, []),
            calls=document_calls.get(document.slug, 0),
        )
        for document in plan.documents
    ]
    report["documents"] = documents
    report["skipped"] = plan.skipped
    answered = sum(int(entry["answered"]) for entry in documents)
    flagged = sum(int(entry["flagged"]) for entry in documents)
    without_signal = sum(
        1 for entry in documents for row in entry["rows"] if row["flagged"] and not row["signals"]
    )
    report["totals"] = {
        "documents": len(documents),
        "units": sum(int(entry["units"]) for entry in documents),
        "answered": answered,
        "flagged": flagged,
        "flag_rate": _rate(flagged, answered),
        "regex_hits": sum(int(entry["regex_hits"]) for entry in documents),
        "flagged_without_signal": without_signal,
    }
    report["usage"] = usage.as_dict()
    report["errors"] = errors
    return report


async def editorial_report(
    *,
    settings: Settings,
    content_dir: Path | None = None,
    locale: str = "zh-TW",
    kinds: Sequence[str] = (),
    slugs: set[str] | None = None,
    prefixes: Sequence[str] = (),
    limit: int | None = None,
    dry_run: bool = False,
    max_calls: int = DEFAULT_MAX_CALLS,
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    plan = plan_editorial(
        content_dir, locale=locale, kinds=kinds, slugs=slugs, prefixes=prefixes, limit=limit
    )
    return await run_editorial(plan, settings, dry_run=dry_run, max_calls=max_calls, client=client)


# --- check two: overlap ---------------------------------------------------------------------


@dataclass(frozen=True)
class Proposal:
    source: str
    slug: str | None
    title: str
    description: str
    summary: list[str] = field(default_factory=list)

    def as_state(self) -> dict[str, Any]:
        state: dict[str, Any] = {"title": self.title, "description": self.description}
        if self.summary:
            state["summary"] = self.summary
        return state

    def text(self) -> str:
        return f"{self.title}{self.description}"


@dataclass
class Candidate:
    slug: str
    kind: str
    locale: str
    title: str
    description: str
    lexical: float = 0.0

    def as_state(self) -> dict[str, str]:
        return {"id": self.slug, "title": self.title, "description": self.description}

    def option(self) -> str:
        return f"{self.title} — {self.description}"

    def tokens(self) -> int:
        """What one candidate costs a chunk: it is in the state and in the option list."""
        return estimate_tokens(self.as_state()) + estimate_tokens({self.slug: self.option()})


def load_proposal(path: Path) -> Proposal:
    """``{title, description, summary?}``, the shape a writer has before there is a pack."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise JevReviewError(f"{path.name}: {error}") from error
    if not isinstance(raw, dict):
        raise JevReviewError(f"{path.name}: expected an object with title and description")
    title = str(raw.get("title") or "").strip()
    description = str(raw.get("description") or "").strip()
    if not title or not description:
        raise JevReviewError(f"{path.name}: title and description are both required")
    summary = [str(item) for item in raw.get("summary") or [] if str(item).strip()]
    return Proposal(str(path), None, title, description, summary)


def load_draft(path: Path, *, locale: str = "zh-TW") -> tuple[Proposal, Kind]:
    """A full pack read as a proposal. Its own slug is what the catalogue must exclude."""
    raw = _read_raw(path)
    if raw is None:
        raise JevReviewError(f"{path.name}: not readable as a content pack")
    try:
        pack = ArticlePack.model_validate(raw)
    except ValidationError as error:
        raise JevReviewError(f"{path.name}: {str(error)[:160]}") from error
    document = next((doc for loc, doc in pack.locales.items() if loc == locale), None)
    if document is None:
        document = next(iter(pack.locales.values()))
    summary = [
        item for block in document.blocks if isinstance(block, SummaryBlock) for item in block.items
    ]
    return (
        Proposal(str(path), pack.slug, document.title, document.description, summary),
        pack.kind,
    )


def load_candidates(
    content_dir: Path,
    *,
    kinds: Sequence[str] = (),
    topics: Sequence[str] = (),
    exclude: Iterable[str] = (),
    locale: str = "zh-TW",
) -> tuple[list[Candidate], list[dict[str, str]]]:
    excluded = set(exclude)
    candidates: list[Candidate] = []
    skipped: list[dict[str, str]] = []
    for path in sorted(content_dir.glob("*.json")) if content_dir.is_dir() else []:
        slug = path.stem
        if slug in excluded:
            continue
        raw = _read_raw(path)
        if raw is None:
            skipped.append({"slug": slug, "reason": "not readable as a content pack"})
            continue
        if not _matches(raw, kinds, topics):
            continue
        if slug == "none":
            # ``none`` is the choice question's own "no article matches" option.
            skipped.append({"slug": slug, "reason": "slug collides with the none option"})
            continue
        locales = raw.get("locales")
        if not isinstance(locales, dict) or not locales:
            skipped.append({"slug": slug, "reason": "no locales"})
            continue
        chosen = locale if locale in locales else next(iter(locales))
        document = locales.get(chosen)
        document = document if isinstance(document, dict) else {}
        title = str(document.get("title") or "").strip()
        description = str(document.get("description") or "").strip()
        if not title:
            skipped.append({"slug": slug, "reason": f"no title in {chosen}"})
            continue
        candidates.append(
            Candidate(slug, str(raw.get("kind") or ""), str(chosen), title, description)
        )
    return candidates, skipped


def _bigrams(text: str) -> set[str]:
    squeezed = "".join(text.split())
    return {squeezed[index : index + 2] for index in range(len(squeezed) - 1)}


def dice(left: str, right: str) -> float:
    """Character-bigram Dice similarity: the cheap first stage of the 2026-09-15 dedupe.

    It knows nothing about meaning, which is the point -- it only has to put the likeliest
    duplicates in the first chunk, so that a budget spent early is spent on them.
    """
    first, second = _bigrams(left), _bigrams(right)
    if not first or not second:
        return 0.0
    return round(2 * len(first & second) / (len(first) + len(second)), 6)


def rank_candidates(proposal: Proposal, candidates: Sequence[Candidate]) -> list[Candidate]:
    text = proposal.text()
    for candidate in candidates:
        candidate.lexical = dice(text, f"{candidate.title}{candidate.description}")
    return sorted(candidates, key=lambda item: (-item.lexical, item.slug))


def overlap_questions(candidates: Sequence[Candidate]) -> dict[str, JevQuestion]:
    criteria = {candidate.slug: candidate.option() for candidate in candidates}
    criteria["none"] = NONE_OPTION
    return {
        "same_article": ChoiceQuestion(instructions=SAME_ARTICLE_QUESTION, criteria=criteria),
        "overlaps": NoulQuestion(instructions=OVERLAP_QUESTION, criteria=dict(OVERLAP_CRITERIA)),
    }


def overlap_state(proposal: Proposal, candidates: Sequence[Candidate]) -> dict[str, Any]:
    return {
        "proposal": proposal.as_state(),
        "existing_articles": [candidate.as_state() for candidate in candidates],
    }


def chunk_tokens(proposal: Proposal, candidates: Sequence[Candidate]) -> int:
    questions = overlap_questions(candidates)
    return estimate_tokens(overlap_state(proposal, candidates)) + sum(
        estimate_tokens(question.model_dump(exclude_none=True))
        for question in questions.values()
    )


def plan_chunks(
    proposal: Proposal,
    candidates: Sequence[Candidate],
    *,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    max_state_tokens: int,
) -> list[list[Candidate]]:
    """Greedy fill under three ceilings, in ranked order.

    ``--chunk-size`` is the one an operator sets; the vendor's 255 options (254 articles plus
    ``none``) and four fifths of ``JEV_MAX_STATE_TOKENS`` are the ones it cannot be set past.
    A candidate that on its own is over the token ceiling still goes into a chunk of its own:
    this command never silently stops asking about an article.
    """
    width = max(1, min(chunk_size, MAX_CHUNK_CANDIDATES))
    ceiling = int(STATE_HEADROOM * max_state_tokens)
    base = chunk_tokens(proposal, ())
    chunks: list[list[Candidate]] = []
    current: list[Candidate] = []
    used = base
    for candidate in candidates:
        cost = candidate.tokens()
        if current and (len(current) >= width or used + cost > ceiling):
            chunks.append(current)
            current = []
            used = base
        current.append(candidate)
        used += cost
    if current:
        chunks.append(current)
    return chunks


@dataclass
class OverlapPlan:
    content_dir: Path
    proposal: Proposal
    kinds: list[str]
    topics: list[str]
    locale: str
    chunks: list[list[Candidate]] = field(default_factory=list)
    skipped: list[dict[str, str]] = field(default_factory=list)
    excluded: list[str] = field(default_factory=list)
    not_asked: int = 0
    final_round: bool = True

    @property
    def candidates(self) -> int:
        return sum(len(chunk) for chunk in self.chunks)

    @property
    def wants_final_round(self) -> bool:
        """One chunk saw every candidate at once, so its ranking is already comparable."""
        return self.final_round and len(self.chunks) > 1

    @property
    def calls(self) -> int:
        return len(self.chunks) + (1 if self.wants_final_round else 0)

    @property
    def input_tokens(self) -> int:
        planned = sum(chunk_tokens(self.proposal, chunk) for chunk in self.chunks)
        if self.wants_final_round and self.chunks:
            planned += chunk_tokens(self.proposal, self.chunks[0][:DEFAULT_TOP])
        return planned


def plan_overlap(
    proposal: Proposal,
    settings: Settings,
    *,
    content_dir: Path | None = None,
    kinds: Sequence[str] = (),
    topics: Sequence[str] = (),
    locale: str = "zh-TW",
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    limit: int | None = None,
    final_round: bool = True,
) -> OverlapPlan:
    root = content_dir or default_directory()
    excluded = [proposal.slug] if proposal.slug else []
    candidates, skipped = load_candidates(
        root, kinds=kinds, topics=topics, exclude=excluded, locale=locale
    )
    ranked = rank_candidates(proposal, candidates)
    asked = ranked[:limit] if limit is not None else ranked
    chunks = plan_chunks(
        proposal, asked, chunk_size=chunk_size, max_state_tokens=settings.jev_max_state_tokens
    )
    return OverlapPlan(
        content_dir=root,
        proposal=proposal,
        kinds=list(kinds),
        topics=list(topics),
        locale=locale,
        chunks=chunks,
        skipped=skipped,
        excluded=excluded,
        not_asked=len(ranked) - len(asked),
        final_round=final_round,
    )


def _empty_chunk(proposal: Proposal, candidates: Sequence[Candidate]) -> dict[str, Any]:
    return {
        "candidates": len(candidates),
        "state_tokens": estimate_tokens(overlap_state(proposal, candidates)),
        "noul": None,
        "noul_tier": None,
        "choice": None,
        "confidence": None,
        "none_probability": None,
        "top": [],
    }


def _top_options(
    answer: ChoiceAnswer, candidates: Sequence[Candidate], *, top: int
) -> list[dict[str, Any]]:
    by_slug = {candidate.slug: candidate for candidate in candidates}
    scored = [
        (slug, probability)
        for slug, probability in answer.probabilities.items()
        if slug != "none" and slug in by_slug
    ]
    if not scored and answer.choice != "none" and answer.choice in by_slug:
        scored = [(answer.choice, answer.confidence)]
    scored.sort(key=lambda item: (-item[1], item[0]))
    return [
        {
            "slug": slug,
            "title": by_slug[slug].title,
            "probability": round(probability, 4),
            "lexical": by_slug[slug].lexical,
        }
        for slug, probability in scored[:top]
    ]


async def _ask_chunk(
    jev: JevClient,
    proposal: Proposal,
    candidates: Sequence[Candidate],
    settings: Settings,
    usage: Usage,
    *,
    top: int,
) -> tuple[dict[str, Any], str | None]:
    """One chunk, one round trip, two questions. Returns ``(block, error)``."""
    block = _empty_chunk(proposal, candidates)
    if usage.calls >= usage.max_calls:
        return block, f"max_calls_reached after {usage.calls} calls"
    try:
        answers, call_usage = await jev.ask(
            overlap_state(proposal, candidates), overlap_questions(candidates)
        )
    except (JevError, httpx.HTTPError) as exc:
        return block, _error_line(exc)
    usage.calls += 1
    usage.input_tokens += int(call_usage.get("input_tokens", 0))
    overlaps = answers.get("overlaps")
    if isinstance(overlaps, NoulAnswer):
        block["noul"] = round(overlaps.noul, 4)
        block["noul_tier"] = route_answer(overlaps, settings, locale=OVERLAP_LOCALE)
    same = answers.get("same_article")
    if isinstance(same, ChoiceAnswer):
        block["choice"] = same.choice
        block["confidence"] = round(same.confidence, 4)
        none_probability = same.probabilities.get("none")
        block["none_probability"] = (
            round(none_probability, 4) if none_probability is not None else None
        )
        block["top"] = _top_options(same, candidates, top=top)
    return block, None


#: Titles and descriptions are the article's own, and every one of them is Chinese. Named
#: rather than inlined so the non-English downgrade is visible at this call site too.
OVERLAP_LOCALE = "zh-TW"


async def run_overlap(
    plan: OverlapPlan,
    settings: Settings,
    *,
    dry_run: bool = False,
    max_calls: int = DEFAULT_MAX_CALLS,
    top: int = DEFAULT_TOP,
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    usage = Usage(max_calls=max_calls)
    usage.planned_calls = plan.calls
    usage.planned_input_tokens = plan.input_tokens
    errors: list[str] = []
    chunks: list[dict[str, Any]] = []
    final: dict[str, Any] | None = None
    asked_candidates = 0

    if dry_run:
        chunks = [
            {"index": index, **_empty_chunk(plan.proposal, chunk)}
            for index, chunk in enumerate(plan.chunks)
        ]
    else:
        _require_key(settings)
        _require_budget(plan.calls, max_calls, narrow="--kind, --topic, --limit or --chunk-size")
        jev = jev_client(settings, client)
        try:
            for index, chunk in enumerate(plan.chunks):
                block, error = await _ask_chunk(jev, plan.proposal, chunk, settings, usage, top=top)
                chunks.append({"index": index, **block})
                if error:
                    errors.append(f"chunk {index}: {error}")
                    break
                asked_candidates += len(chunk)
            union = _union_of_tops(plan, chunks, top=top)
            if plan.wants_final_round and not errors and union:
                block, error = await _ask_chunk(
                    jev, plan.proposal, union, settings, usage, top=top
                )
                final = {"asked": not error, **block}
                if error:
                    errors.append(f"final round: {error}")
            elif len(plan.chunks) > 1:
                final = {"asked": False, **_empty_chunk(plan.proposal, union)}
        finally:
            await jev.close()

    report = _header("jev-review overlap", plan.content_dir, settings, dry_run=dry_run)
    report["locale"] = plan.locale
    report["questions"] = {
        "same_article": SAME_ARTICLE_QUESTION,
        "overlaps": {"instructions": OVERLAP_QUESTION, "criteria": dict(OVERLAP_CRITERIA)},
        "none": NONE_OPTION,
    }
    report["proposal"] = {
        "source": plan.proposal.source,
        "slug": plan.proposal.slug,
        "title": plan.proposal.title,
        "description": plan.proposal.description,
        "summary": list(plan.proposal.summary),
    }
    report["catalogue"] = {
        "content_dir": str(plan.content_dir),
        "kinds": plan.kinds,
        "topics": plan.topics,
        "candidates": plan.candidates,
        "excluded": plan.excluded,
        "not_asked": plan.not_asked
        + (0 if dry_run else max(0, plan.candidates - asked_candidates)),
    }
    report["chunks"] = chunks
    report["final_round"] = final
    report["verdict"] = _verdict(chunks, final, settings, top=top)
    report["skipped"] = plan.skipped
    report["usage"] = usage.as_dict()
    report["errors"] = errors
    return report


def _union_of_tops(
    plan: OverlapPlan, chunks: Sequence[Mapping[str, Any]], *, top: int
) -> list[Candidate]:
    """Every chunk's best answers, deduplicated, for the one round that ranks them together."""
    by_slug = {candidate.slug: candidate for chunk in plan.chunks for candidate in chunk}
    seen: dict[str, Candidate] = {}
    for block in chunks:
        for row in list(block.get("top") or [])[:top]:
            slug = str(row["slug"])
            if slug in by_slug and slug not in seen:
                seen[slug] = by_slug[slug]
    ordered = list(seen.values())[:MAX_CHUNK_CANDIDATES]
    return ordered if len(ordered) > 1 else []


def _verdict(
    chunks: Sequence[Mapping[str, Any]],
    final: Mapping[str, Any] | None,
    settings: Settings,
    *,
    top: int,
) -> dict[str, Any]:
    """The one number a coordinator reads, and how much to trust the list under it.

    ``overlap_noul`` is the maximum over every round: a proposal that repeats one article in
    one chunk repeats it, whatever the other chunks answered. The ranking is only comparable
    when a single round saw every finalist, because two chunks' probabilities are normalised
    over different option sets.
    """
    nouls = [float(block["noul"]) for block in chunks if block.get("noul") is not None]
    if final is not None and final.get("noul") is not None:
        nouls.append(float(final["noul"]))
    overlap_noul = max(nouls) if nouls else None
    answered = [block for block in chunks if block.get("choice")]
    comparable = bool(final and final.get("asked")) or len(answered) <= 1
    if final is not None and final.get("asked"):
        choice = final.get("choice")
        ranking = list(final.get("top") or [])
    elif len(answered) == 1:
        choice = answered[0].get("choice")
        ranking = list(answered[0].get("top") or [])
    else:
        merged = [row for block in answered for row in block.get("top") or []]
        merged.sort(key=lambda row: (-float(row["probability"]), str(row["slug"])))
        ranking = merged[:top]
        picked = [block for block in answered if block.get("choice") not in (None, "none")]
        choice = str(ranking[0]["slug"]) if ranking and picked else "none"
    return {
        "overlap_noul": overlap_noul,
        "tier": _noul_tier(overlap_noul, settings),
        "flagged": overlap_noul is not None and overlap_noul >= settings.jev_flag_confidence,
        "choice": choice,
        "top": ranking,
        "comparable": comparable,
    }


def _noul_tier(noul: float | None, settings: Settings) -> str | None:
    if noul is None:
        return None
    return route_answer(NoulAnswer(type="noul", noul=noul), settings, locale=OVERLAP_LOCALE)


async def overlap_report(
    *,
    settings: Settings,
    proposal: Proposal,
    content_dir: Path | None = None,
    kinds: Sequence[str] = (),
    topics: Sequence[str] = (),
    locale: str = "zh-TW",
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    limit: int | None = None,
    top: int = DEFAULT_TOP,
    final_round: bool = True,
    dry_run: bool = False,
    max_calls: int = DEFAULT_MAX_CALLS,
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    plan = plan_overlap(
        proposal,
        settings,
        content_dir=content_dir,
        kinds=kinds,
        topics=topics,
        locale=locale,
        chunk_size=chunk_size,
        limit=limit,
        final_round=final_round,
    )
    return await run_overlap(
        plan, settings, dry_run=dry_run, max_calls=max_calls, top=top, client=client
    )


def kinds_for_draft(kind: Kind) -> tuple[Kind, ...]:
    """A draft is compared against its own section: a how-to can repeat an intel piece."""
    return SECTION_KINDS[section_of(kind)]


# --- check three: compare (never touches the network) ----------------------------------------


def read_report(path: Path) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise JevReviewError(f"{path.name}: {error}") from error
    if not isinstance(raw, dict) or not isinstance(raw.get("documents"), list):
        raise JevReviewError(f"{path.name}: not a jev-review editorial report")
    return raw


def _by_slug(report: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(entry["slug"]): entry for entry in report["documents"]}


def _residual(entry: Mapping[str, Any]) -> int:
    """Flagged rows the regexes never found: the only ones Jev is being paid for."""
    return sum(1 for row in entry["rows"] if row.get("flagged") and not row.get("signals"))


def _pair_rows(
    before: Mapping[str, dict[str, Any]],
    after: Mapping[str, dict[str, Any]],
    slugs: Sequence[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for slug in slugs:
        first, second = before.get(slug), after.get(slug)
        rate_before = first["flag_rate"] if first else None
        rate_after = second["flag_rate"] if second else None
        delta = (
            round(rate_after - rate_before, 4)
            if rate_before is not None and rate_after is not None
            else None
        )
        rows.append(
            {
                "slug": slug,
                "units_before": first["units"] if first else 0,
                "units_after": second["units"] if second else 0,
                "flagged_before": first["flagged"] if first else 0,
                "flagged_after": second["flagged"] if second else 0,
                "rate_before": rate_before,
                "rate_after": rate_after,
                "delta": delta,
            }
        )
    return rows


def _group(
    rows: Sequence[Mapping[str, Any]],
    before: Mapping[str, dict[str, Any]],
    after: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    wins = sum(1 for row in rows if row["delta"] is not None and row["delta"] < 0)
    losses = sum(1 for row in rows if row["delta"] is not None and row["delta"] > 0)
    ties = sum(1 for row in rows if row["delta"] == 0)
    units_before = sum(int(row["units_before"]) for row in rows)
    units_after = sum(int(row["units_after"]) for row in rows)
    flagged_before = sum(int(row["flagged_before"]) for row in rows)
    flagged_after = sum(int(row["flagged_after"]) for row in rows)
    slugs = [str(row["slug"]) for row in rows]
    return {
        "slugs": slugs,
        "articles": len(rows),
        "rows": list(rows),
        "paired": {"wins": wins, "losses": losses, "ties": ties},
        "totals": {
            "units_before": units_before,
            "units_after": units_after,
            "flagged_before": flagged_before,
            "flagged_after": flagged_after,
            "rate_before": _rate(flagged_before, units_before),
            "rate_after": _rate(flagged_after, units_after),
        },
        "residual": {
            "before": sum(_residual(before[slug]) for slug in slugs if slug in before),
            "after": sum(_residual(after[slug]) for slug in slugs if slug in after),
        },
    }


SAMPLE_COLUMNS = ("slug", "unit_id", "kind", "noul", "signals", "text", "label")


def _sample_rows(
    before: Mapping[str, dict[str, Any]],
    after: Mapping[str, dict[str, Any]],
    slugs: Sequence[str],
    *,
    size: int,
    seed: int,
) -> list[dict[str, str]]:
    """A stratified, deliberately blind draw for hand labelling.

    Eight strata -- each side, flagged or not, with a regex signal or not -- are drawn from
    round robin, so the sample carries both the flags whose precision is being measured and
    the ones the regexes never found. The rows do not say which side they came from: a
    labeller who can see that is grading the rewrite rather than the check. ``label`` is left
    empty for the person, and a row is found again by its slug and its text.
    """
    strata: dict[tuple[str, bool, bool], list[dict[str, str]]] = {}
    for side, reports in (("before", before), ("after", after)):
        for slug in slugs:
            entry = reports.get(slug)
            if entry is None:
                continue
            for row in entry["rows"]:
                key = (side, bool(row.get("flagged")), bool(row.get("signals")))
                strata.setdefault(key, []).append(
                    {
                        "slug": slug,
                        "unit_id": str(row["unit_id"]),
                        "kind": str(row["kind"]),
                        "noul": "" if row.get("noul") is None else str(row["noul"]),
                        "signals": " ".join(str(item) for item in row.get("signals") or []),
                        "text": " ".join(str(row.get("excerpt") or "").split()),
                        "label": "",
                    }
                )
    rng = random.Random(seed)  # noqa: S311 -- a reproducible sample, not a secret
    pools = [rng.sample(rows, len(rows)) for _, rows in sorted(strata.items())]
    drawn: list[dict[str, str]] = []
    while pools and len(drawn) < size:
        for pool in pools:
            if pool and len(drawn) < size:
                drawn.append(pool.pop())
        pools = [pool for pool in pools if pool]
    rng.shuffle(drawn)
    return drawn


def write_sample(rows: Sequence[Mapping[str, str]], path: Path) -> None:
    lines = ["\t".join(SAMPLE_COLUMNS)]
    lines.extend("\t".join(row[column] for column in SAMPLE_COLUMNS) for row in rows)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def compare_reports(
    before_path: Path,
    after_path: Path,
    *,
    sample: int = 0,
    seed: int = 1,
    out: Path | None = None,
    control: Sequence[str] = (),
) -> dict[str, Any]:
    """Two editorial reports, paired by slug. Reads files; sends nothing anywhere."""
    before_report, after_report = read_report(before_path), read_report(after_path)
    before, after = _by_slug(before_report), _by_slug(after_report)
    controls = [slug for slug in control if slug in before or slug in after]
    paired = [slug for slug in before if slug in after and slug not in controls]
    subject_rows = _pair_rows(before, after, sorted(paired))
    control_rows = _pair_rows(before, after, sorted(controls))
    drawn = (
        _sample_rows(before, after, sorted(set(paired) | set(controls)), size=sample, seed=seed)
        if sample > 0
        else []
    )
    if out is not None and drawn:
        write_sample(drawn, out)
    return {
        "tool": "jev-review compare",
        "advisory": True,
        "notice": NOTICE,
        "generated_at": datetime.now(UTC).isoformat(),
        "before": str(before_path),
        "after": str(after_path),
        "subject": _group(subject_rows, before, after),
        "control": _group(control_rows, before, after),
        "only_before": sorted(set(before) - set(after)),
        "only_after": sorted(set(after) - set(before)),
        "sample": {
            "rows": len(drawn),
            "size": sample,
            "seed": seed,
            "path": str(out) if out is not None and drawn else None,
            "columns": list(SAMPLE_COLUMNS),
        },
    }


# --- what a person reads ---------------------------------------------------------------------


def _percent(value: float | None) -> str:
    return "-" if value is None else f"{value * 100:.1f}%"


def _usage_line(usage: Mapping[str, Any]) -> str:
    return (
        f"usage: {usage['calls']} calls, {usage['input_tokens']} input tokens, "
        f"est. USD {usage['usd']:.4f}"
    )


def render_editorial(report: Mapping[str, Any], *, top: int = DEFAULT_TOP) -> str:
    usage, totals = report["usage"], report["totals"]
    lines = [
        NOTICE,
        "",
        f"jev-review editorial  {report['content_dir']}  locale={report['locale']}  "
        f"model={report['model']}",
        f"plan: {totals['documents']} documents, {totals['units']} units, "
        f"{usage['planned_calls']} calls, about {usage['planned_input_tokens']} input tokens, "
        f"est. USD {usage['planned_usd']:.4f}",
        "",
    ]
    for entry in report["documents"]:
        lines.append(
            f"{entry['slug']}  units={entry['units']} answered={entry['answered']} "
            f"flagged={entry['flagged']} ({_percent(entry['flag_rate'])}) "
            f"regex={entry['regex_hits']}"
        )
        flagged = sorted(
            (row for row in entry["rows"] if row["flagged"]),
            key=lambda row: -float(row["noul"] or 0),
        )
        for row in flagged[:top]:
            signals = ",".join(row["signals"]) or "-"
            lines.append(
                f"  {row['unit_id']} b{row['block_index']:+d} {row['kind']:<14} "
                f"{row['noul']:.2f} {row['tier']:<7} {signals:<28} {row['excerpt']}"
            )
        lines.extend(f"  ! {failure}" for failure in entry["errors"])
    if report["skipped"]:
        lines.extend(["", f"skipped: {len(report['skipped'])} packs"])
        lines.extend(f"  {item['slug']}: {item['reason']}" for item in report["skipped"][:10])
    lines.extend(
        [
            "",
            f"totals: {totals['documents']} documents, {totals['units']} units, "
            f"{totals['flagged']} flagged ({_percent(totals['flag_rate'])}), "
            f"{totals['regex_hits']} with a regex signal, "
            f"{totals['flagged_without_signal']} flagged without one",
            _usage_line(usage),
        ]
    )
    lines.extend(f"error: {failure}" for failure in report["errors"])
    lines.extend(["", NOTICE])
    return "\n".join(lines)


def render_overlap(report: Mapping[str, Any]) -> str:
    catalogue, verdict, proposal = report["catalogue"], report["verdict"], report["proposal"]
    kinds = f" of kinds {','.join(catalogue['kinds'])}" if catalogue["kinds"] else ""
    topics = f" topics {','.join(catalogue['topics'])}" if catalogue["topics"] else ""
    lines = [
        NOTICE,
        "",
        f"jev-review overlap  {catalogue['content_dir']}  model={report['model']}",
        f"proposal: {proposal['title']}  ({proposal['source']})",
        f"catalogue: {catalogue['candidates']} candidates{kinds}{topics}, "
        f"{len(report['chunks'])} chunks, {catalogue['not_asked']} not asked",
        "",
    ]
    for block in report["chunks"]:
        noul = "-" if block["noul"] is None else f"{block['noul']:.2f}"
        lines.append(
            f"chunk {block['index']}  {block['candidates']} candidates  "
            f"{block['state_tokens']} state tokens  noul={noul}  choice={block['choice']}"
        )
    final = report["final_round"]
    if final is not None:
        lines.append(
            f"final round: {'asked' if final['asked'] else 'not asked'}, "
            f"{final['candidates']} candidates"
        )
    overlap_noul = verdict["overlap_noul"]
    lines.extend(
        [
            "",
            f"verdict: overlap_noul={'-' if overlap_noul is None else f'{overlap_noul:.2f}'} "
            f"tier={verdict['tier']} flagged={verdict['flagged']} "
            f"choice={verdict['choice']} comparable={verdict['comparable']}",
        ]
    )
    for row in verdict["top"]:
        lines.append(
            f"  {row['probability']:.2f}  lexical {row['lexical']:.3f}  "
            f"{row['slug']}  {row['title']}"
        )
    if not verdict["comparable"]:
        lines.append("  (probabilities come from different chunks and are not comparable)")
    lines.append(_usage_line(report["usage"]))
    lines.extend(f"error: {failure}" for failure in report["errors"])
    lines.extend(["", NOTICE])
    return "\n".join(lines)


def render_compare(result: Mapping[str, Any]) -> str:
    lines = [
        NOTICE,
        "",
        f"jev-review compare  before={result['before']}  after={result['after']}",
        "",
        f"{'slug':<46}{'units':>12}{'before':>9}{'after':>9}{'delta':>9}",
    ]
    for name in ("subject", "control"):
        group = result[name]
        if not group["rows"]:
            continue
        lines.append(f"-- {name} ({group['articles']} articles)")
        for row in group["rows"]:
            units = f"{row['units_before']}/{row['units_after']}"
            delta = "-" if row["delta"] is None else f"{row['delta'] * 100:+.1f}%"
            lines.append(
                f"{row['slug']:<46}{units:>12}{_percent(row['rate_before']):>9}"
                f"{_percent(row['rate_after']):>9}{delta:>9}"
            )
        paired, totals, residual = group["paired"], group["totals"], group["residual"]
        lines.append(
            f"   paired: {paired['wins']} down, {paired['losses']} up, {paired['ties']} equal; "
            f"rate {_percent(totals['rate_before'])} -> {_percent(totals['rate_after'])}; "
            f"residual flags {residual['before']} -> {residual['after']}"
        )
    sample = result["sample"]
    if sample["rows"]:
        lines.append(f"sample: {sample['rows']} rows, seed {sample['seed']} -> {sample['path']}")
    lines.extend(["", NOTICE])
    return "\n".join(lines)
