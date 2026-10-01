"""The brand-story backlog: checking a compiled stories.json and importing it as episode rows.

The backlog is planned in the repository (docs/videos/story-plans/<plan>/, checked by
tools/video/story-plans/validate.mjs) and compiled into one ``stories.json``: the series row,
then every story in production order with its ``number``, its ``publish`` slot and the
``caveats`` its fact checker left. The host imports that file (docs/videos/STORY.md
§企劃清單與集數列), since the worker's document volume does not follow a deploy.

``check_story_file`` holds every story to the backlog checker's own rules: ``storyProblems``,
``seriesProblems`` and the limits and patterns at the top of tools/video/story-plans/plan.mjs,
copied here (change both together), so a file the checker passes imports and a story it would
refuse is refused. One bad story refuses the whole file, and nothing is written.

``import_story_rows`` makes the stories the episode rows of one story series. The number is the
production order, the chapter is 1, the title, the logline and the video slug become columns,
and everything else stays in ``beats`` for the worker. A story is known by its ``id``: importing
it again updates its row only while the row has not started (``planned`` or ``ready``); a row
that started, finished or was skipped is left alone and counted, and a dropped story being made
again keeps the remake's slug (``series.redo_episode``). When the schedule moved a
story, the rows that have not started are renumbered through temporary numbers, so
``uq_video_drama_episode_number`` never sees two rows on one number; a started row keeps its
number, and a story the file puts on it is a problem, not something settled silently. The dry
run is the default and writes nothing; running ``apply`` twice changes nothing the second time.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal, TypeGuard
from urllib.parse import urlsplit
from uuid import uuid4

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User, VideoProject
from app.video_automation.models import (
    VideoAutomationSettings,
    VideoDramaEpisode,
    VideoDramaSeries,
)
from app.video_automation.schemas import STORY_MAX_PER_DAY, SeriesIn
from app.video_automation.series import add_series, is_redo_of

# --- the backlog checker's rules (tools/video/story-plans/plan.mjs) ----------------------------

SCHEMA_VERSION = 1
CATEGORIES = ("everyday", "asia-brand", "tech")
REGIONS = ("global", "jp", "kr", "tw")
CHAPTER_KEYS = ("hook", "origin", "idea", "engine", "turn", "now")
SLOTS = ("12:00", "20:00")
# A source that settles a fact on its own, against one that needs a second, independent one.
PRIMARY_KINDS = ("official", "court", "academic", "archive")
SOURCE_KINDS = (*PRIMARY_KINDS, "reference", "news", "book")
SENSITIVITY = ("none", "care")
MIN_SOURCES = 3
MAX_CAST = 3
MIN_CLAIMS = 4
MAX_CLAIMS = 10
# The id's letter says what the story is: A everyday objects and invisible standards, B, K and
# T a brand a traveller meets in Japan, Korea or Taiwan, C technology and software.
PREFIXES: dict[str, tuple[str, str | None]] = {
    "A": ("everyday", None),
    "B": ("asia-brand", "jp"),
    "K": ("asia-brand", "kr"),
    "T": ("asia-brand", "tw"),
    "C": ("tech", None),
}
LIMITS = {
    "title": 60,
    "logline": 120,
    "question": 120,
    "takeaway": 120,
    "subject": 40,
    "point_min": 60,
    "point_max": 400,
    "headline": 12,
    "appearance": 800,
    "claim": 200,
    "supports": 240,
    "image_notes": 400,
    "caveats": 800,
    "look_style": 600,
    "look_negative": 400,
}
STORY_MINUTES = (12, 15)
# The fields of a story file, then what the compiled file adds to each story: its place in the
# production order, what its fact checker left for the writer (optional), and its upload slot.
STORY_KEYS = (
    "id",
    "slug",
    "category",
    "region",
    "subject",
    "title",
    "logline",
    "question",
    "chapters",
    "takeaway",
    "must_verify",
    "sources",
    "names",
    "cast",
    "image_notes",
    "sensitivity",
    "related_guide",
    "thumbnail",
)
FILE_KEYS = frozenset(("number", *STORY_KEYS, "caveats", "publish"))
# A fact to check: the claim and the indexes of its sources, and three optional flags: the claim
# the title rests on (``core``), an anecdote told as somebody's account (``attributed``), and a
# fact whose every source is a document the worker's reader cannot turn into text, a PDF or a
# page over 3 MB, which the worker takes on the plan's word (``reviewer_only``; the compiled
# file sets it from the story's review).
CLAIM_FLAGS = ("core", "attributed", "reviewer_only")
CLAIM_KEYS = frozenset(("claim", "sources", *CLAIM_FLAGS))
# What becomes a column of the episode row; the rest of the story is its ``beats``.
COLUMN_KEYS = ("number", "title", "logline", "slug")

# fullmatch throughout: ``$`` would let a trailing newline through, where JavaScript's does not.
ID = re.compile(r"[ABKTC][0-9]{2}")
SLUG = re.compile(r"story-[a-z0-9](?:[a-z0-9-]{0,52}[a-z0-9])?")
SERIES_SLUG = re.compile(r"[a-z0-9][a-z0-9-]{1,39}")
GUIDE_SLUG = re.compile(r"[a-z0-9][a-z0-9-]{0,118}[a-z0-9]")
CAST_ID = re.compile(r"[a-z][a-z0-9-]{1,23}")
DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
HTTPS = re.compile(r"https://[^\s/]+\.[^\s/]+(?:/\S*)?")
ASCII = re.compile(r"[\x20-\x7e]+")
# Sites whose every edition and mirror are one voice: two of them do not corroborate each other.
ONE_VOICE = ("wikipedia.org", "wikimedia.org", "wikiwand.com", "wikimili.com")

# The rows the import may still change: the worker has not taken them.
NOT_STARTED = ("planned", "ready")


def _is_text(value: object) -> TypeGuard[str]:
    return isinstance(value, str) and bool(value.strip())


def _is_int(value: object) -> TypeGuard[int]:
    # JSON has no separate booleans for Python: True is an int there, and never a number here.
    return isinstance(value, int) and not isinstance(value, bool)


def _get(value: object, key: str) -> Any:
    return value.get(key) if isinstance(value, dict) else None


def _list(value: object) -> list[Any]:
    return value if isinstance(value, list) else []


def _text(story: dict[str, Any], key: str, limit: int, problems: list[str]) -> None:
    """A short text field: present, trimmed, and within its limit (in characters)."""
    value = story.get(key)
    if not _is_text(value):
        problems.append(f"{key} is missing")
    elif value != value.strip():
        problems.append(f"{key} has leading or trailing space")
    elif len(value) > limit:
        problems.append(f"{key} is {len(value)} characters, at most {limit}")


def host_of(url: Any) -> str:
    """The host a source speaks from, every edition of a one-voice site counting as one."""
    try:
        host = (urlsplit(str(url)).hostname or "").lower()
    except ValueError:
        return ""
    host = host.removeprefix("www.")
    return next(
        (site for site in ONE_VOICE if host == site or host.endswith(f".{site}")),
        host,
    )


def claim_supported(claim: dict[str, Any], sources: list[Any]) -> bool:
    """Whether the sources a claim cites are enough (docs/videos/STORY.md §查核與來源規則): one
    primary source, or two from different publishers and different hosts; a claim marked
    ``attributed`` is told as somebody's account, and one source will do."""
    indexes = claim.get("sources") or []
    cited = [
        sources[index]
        for index in indexes
        if _is_int(index) and 0 <= index < len(sources) and sources[index]
    ]
    if not cited:
        return False
    if claim.get("attributed") is True:
        return True
    if any(_get(source, "kind") in PRIMARY_KINDS for source in cited):
        return True
    publishers = {str(_get(source, "publisher")).strip().lower() for source in cited}
    hosts = {host_of(_get(source, "url")) for source in cited}
    return len(publishers) >= 2 and len(hosts) >= 2


def story_problems(story: Any) -> list[str]:
    """Everything wrong with one story of the compiled file, as sentences; empty when sound.

    ``storyProblems`` of plan.mjs, with the compiled file's additions: a ``number`` from 1, a
    ``publish`` slot and, when present, ``caveats`` of at most 800 characters.
    """
    if not isinstance(story, dict):
        return ["the story is not a JSON object"]
    problems = [f'unknown field "{key}"' for key in story if key not in FILE_KEYS]
    story_id = story.get("id")
    if not isinstance(story_id, str) or not ID.fullmatch(story_id):
        problems.append(f'id "{story_id}" is not a letter A, B, K, T or C and two digits')
    slug = story.get("slug")
    if not isinstance(slug, str) or not SLUG.fullmatch(slug):
        problems.append(
            f'slug "{slug}" must be story-<lowercase letters, digits, hyphens>, '
            "at most 60 characters"
        )
    prefix = PREFIXES.get(str(story_id or "")[:1])
    category, region = story.get("category"), story.get("region")
    if category not in CATEGORIES:
        problems.append(f"category must be one of {', '.join(CATEGORIES)}")
    elif prefix and category != prefix[0]:
        problems.append(f'category "{category}" does not fit id {story_id} ({prefix[0]})')
    if region not in REGIONS:
        problems.append(f"region must be one of {', '.join(REGIONS)}")
    elif prefix and prefix[1] and region != prefix[1]:
        problems.append(f'region "{region}" does not fit id {story_id} ({prefix[1]})')
    for key in ("subject", "title", "logline", "question", "takeaway"):
        _text(story, key, LIMITS[key], problems)
    title = story.get("title")
    if _is_text(title) and re.search(r"[<>]", title):
        problems.append("title has an angle bracket, which YouTube refuses")

    chapters = story.get("chapters")
    if not isinstance(chapters, list) or len(chapters) != len(CHAPTER_KEYS):
        problems.append(f"chapters must be the {len(CHAPTER_KEYS)} parts {', '.join(CHAPTER_KEYS)}")
    else:
        for index, (chapter, key) in enumerate(zip(chapters, CHAPTER_KEYS, strict=True)):
            if _get(chapter, "key") != key:
                problems.append(
                    f'chapters[{index}].key is "{_get(chapter, "key")}", expected "{key}"'
                )
            point = _get(chapter, "point")
            if not _is_text(point):
                problems.append(f"chapters[{index}] ({key}) has no point")
            elif not LIMITS["point_min"] <= len(point) <= LIMITS["point_max"]:
                problems.append(
                    f"chapters[{index}] ({key}) is {len(point)} characters, "
                    f"expected {LIMITS['point_min']}-{LIMITS['point_max']}"
                )

    sources = _list(story.get("sources"))
    if len(sources) < MIN_SOURCES:
        problems.append(f"sources has {len(sources)} entries, at least {MIN_SOURCES}")
    urls: set[str] = set()
    for index, source in enumerate(sources):
        where = f"sources[{index}]"
        if not isinstance(source, dict):
            problems.append(f"{where} is not an object")
            continue
        url = source.get("url")
        if not isinstance(url, str) or not HTTPS.fullmatch(url):
            problems.append(f"{where}.url must be an https URL")
        elif url in urls:
            problems.append(f"{where}.url repeats an earlier source")
        else:
            urls.add(url)
        if not _is_text(source.get("publisher")):
            problems.append(f"{where}.publisher is missing")
        if source.get("kind") not in SOURCE_KINDS:
            problems.append(f"{where}.kind must be one of {', '.join(SOURCE_KINDS)}")
        supports = source.get("supports")
        if not _is_text(supports):
            problems.append(f"{where}.supports is missing: say what this page is the evidence for")
        elif len(supports) > LIMITS["supports"]:
            problems.append(f"{where}.supports is over {LIMITS['supports']} characters")
        checked = source.get("checked")
        if not isinstance(checked, str) or not DATE.fullmatch(checked):
            problems.append(f"{where}.checked must be the date the page was read, YYYY-MM-DD")

    claims = _list(story.get("must_verify"))
    if not MIN_CLAIMS <= len(claims) <= MAX_CLAIMS:
        problems.append(f"must_verify has {len(claims)} claims, expected {MIN_CLAIMS}-{MAX_CLAIMS}")
    for index, claim in enumerate(claims):
        where = f"must_verify[{index}]"
        if not isinstance(claim, dict) or not _is_text(claim.get("claim")):
            problems.append(f"{where} needs a claim")
            continue
        problems.extend(
            f'{where} has unknown field "{key}"' for key in claim if key not in CLAIM_KEYS
        )
        problems.extend(
            f"{where}.{key} must be true or false"
            for key in CLAIM_FLAGS
            if key in claim and not isinstance(claim[key], bool)
        )
        if len(claim["claim"]) > LIMITS["claim"]:
            problems.append(f"{where}.claim is over {LIMITS['claim']} characters")
        indexes = claim.get("sources")
        if (
            not isinstance(indexes, list)
            or not indexes
            or not all(_is_int(each) and 0 <= each < len(sources) for each in indexes)
        ):
            problems.append(f"{where}.sources must list indexes into sources")
            continue
        if not claim_supported(claim, sources):
            problems.append(
                f"{where} rests on one secondary source: cite a primary one, a second "
                "independent one, or mark it attributed (the narration then says whose "
                "account it is)"
            )
    if _is_text(title) and claims and not any(_get(claim, "core") is True for claim in claims):
        problems.append("no must_verify claim is marked core: the one the title rests on")

    names = _list(story.get("names"))
    if not names or not all(_is_text(name) for name in names):
        problems.append(
            "names must list the brand, product and personal names the pictures may not show"
        )

    cast = story.get("cast")
    if not isinstance(cast, list):
        problems.append("cast must be an array (empty when no figure recurs)")
    else:
        if len(cast) > MAX_CAST:
            problems.append(f"cast has {len(cast)} figures, at most {MAX_CAST}")
        ids: set[str] = set()
        for index, figure in enumerate(cast):
            where = f"cast[{index}]"
            figure_id = _get(figure, "id")
            if (
                not isinstance(figure_id, str)
                or not CAST_ID.fullmatch(figure_id)
                or figure_id == "narrator"
            ):
                problems.append(
                    f"{where}.id must be 2-24 lowercase letters, digits or hyphens, "
                    'and not "narrator"'
                )
            elif figure_id in ids:
                problems.append(f"{where}.id repeats")
            else:
                ids.add(figure_id)
            if not _is_text(_get(figure, "role")):
                problems.append(f"{where}.role is missing")
            appearance = _get(figure, "appearance")
            if (
                not _is_text(appearance)
                or not ASCII.fullmatch(appearance)
                or len(appearance) > LIMITS["appearance"]
            ):
                problems.append(
                    f"{where}.appearance must be English for the image model, "
                    f"at most {LIMITS['appearance']} characters"
                )
            else:
                lower = appearance.lower()
                for name in names:
                    if _is_text(name) and ASCII.fullmatch(name) and name.lower() in lower:
                        problems.append(
                            f'{where}.appearance names "{name}": a figure is generic, '
                            "never a likeness"
                        )

    image_notes = story.get("image_notes")
    if not _is_text(image_notes):
        problems.append("image_notes is missing: say what the pictures show and what they must not")
    elif len(image_notes) > LIMITS["image_notes"]:
        problems.append(f"image_notes is over {LIMITS['image_notes']} characters")
    if story.get("sensitivity") not in SENSITIVITY:
        problems.append(f"sensitivity must be one of {', '.join(SENSITIVITY)}")
    guide = story.get("related_guide", "")
    if guide is not None and not (isinstance(guide, str) and GUIDE_SLUG.fullmatch(guide)):
        problems.append("related_guide must be a site article's slug, or null")
    headline = _get(story.get("thumbnail"), "headline")
    if not _is_text(headline) or not _is_text(_get(story.get("thumbnail"), "idea")):
        problems.append("thumbnail needs a headline and an idea")
    elif len(headline) > LIMITS["headline"]:
        problems.append(
            f"thumbnail.headline is {len(headline)} characters, at most {LIMITS['headline']}"
        )

    number = story.get("number")
    if not _is_int(number) or number < 1:
        problems.append("number must be a whole number from 1: the story's place in production")
    day = _get(story.get("publish"), "day")
    if not _is_int(day) or day < 1 or _get(story.get("publish"), "slot") not in SLOTS:
        problems.append(f"publish must be {{day: 1 or more, slot: {' or '.join(SLOTS)}}}")
    if "caveats" in story:
        caveats = story["caveats"]
        if not isinstance(caveats, str) or len(caveats) > LIMITS["caveats"]:
            problems.append(f"caveats must be text of at most {LIMITS['caveats']} characters")
    return problems


def series_problems(series: Any) -> list[str]:
    """``seriesProblems`` of plan.mjs: the series row the stories are imported under."""
    if not isinstance(series, dict):
        return ["series is not a JSON object"]
    problems: list[str] = []
    slug = series.get("slug")
    if not isinstance(slug, str) or not SERIES_SLUG.fullmatch(slug):
        problems.append(
            "series.slug must be lowercase letters, digits and hyphens, 2-40 characters"
        )
    if not _is_text(series.get("title")):
        problems.append("series.title is missing")
    if series.get("kind") != "story":
        problems.append('series.kind must be "story"')
    if series.get("visual_tier") != "stills":
        problems.append('series.visual_tier must be "stills"')
    if series.get("hands_off") is not True:
        problems.append("series.hands_off must be true")
    if series.get("compilation", False) is not False:
        problems.append("series.compilation must be false")
    minutes = series.get("target_minutes")
    low, high = STORY_MINUTES
    if not _is_int(minutes) or not low <= minutes <= high:
        problems.append(f"series.target_minutes must be {low} to {high}")
    per_day = series.get("episodes_per_day")
    if not _is_int(per_day) or not 1 <= per_day <= STORY_MAX_PER_DAY:
        problems.append(f"series.episodes_per_day must be 1 to {STORY_MAX_PER_DAY}")
    if not _is_text(series.get("image_model")):
        problems.append("series.image_model is missing")
    style = _get(series.get("look"), "style")
    negative = _get(series.get("look"), "negative")
    if not _is_text(style) or not _is_text(negative):
        problems.append("series.look needs a style and a negative prompt")
    else:
        if len(style) > LIMITS["look_style"]:
            problems.append(f"series.look.style is over {LIMITS['look_style']} characters")
        if len(negative) > LIMITS["look_negative"]:
            problems.append(f"series.look.negative is over {LIMITS['look_negative']} characters")
    return problems


@dataclass
class FileCheck:
    """A compiled file, checked: its series object, its stories in production order, every
    problem (labelled with the story it is about), and the stories that have one."""

    series: dict[str, Any]
    stories: list[dict[str, Any]]
    problems: list[str]
    refused: list[str]
    ignored: list[str]


def _label(story: Any, index: int) -> str:
    story_id = _get(story, "id")
    return story_id if isinstance(story_id, str) and ID.fullmatch(story_id) else f"stories[{index}]"


def check_story_file(document: Any, series_slug: str) -> FileCheck:
    """Everything wrong with a compiled stories.json for the series named ``series_slug``.

    Besides each story's own rules and the series': ``schema_version`` is 1, the series is the
    one named, the ids, slugs and titles do not repeat, the numbers run 1 to N without a gap,
    and no two stories share an upload slot.
    """
    if not isinstance(document, dict):
        return FileCheck({}, [], ["the file is not a JSON object"], [], [])
    problems: list[str] = []
    ignored = [
        f"{key} (top level)"
        for key in document
        if key not in ("schema_version", "series", "stories")
    ]
    version = document.get("schema_version")
    if not _is_int(version) or version != SCHEMA_VERSION:
        problems.append(f"schema_version is {version!r}, this server reads {SCHEMA_VERSION}")
    series = document.get("series")
    problems.extend(series_problems(series))
    series_object = series if isinstance(series, dict) else {}
    if isinstance(series, dict) and series.get("slug") != series_slug:
        problems.append(f"series.slug is {series.get('slug')!r}, but --series is {series_slug!r}")
    raw = document.get("stories")
    stories: list[Any] = raw if isinstance(raw, list) else []
    if not stories:
        problems.append("stories must list at least one story")
    refused: list[str] = []
    for index, story in enumerate(stories):
        own = story_problems(story)
        if own:
            label = _label(story, index)
            refused.append(label)
            problems.extend(f"{label}: {problem}" for problem in own)
    # Across the file: what must not repeat, and the production order without a gap.
    for key in ("id", "slug", "title"):
        seen: dict[Any, str] = {}
        for index, story in enumerate(stories):
            value = _get(story, key)
            if not isinstance(value, str):
                continue
            label = _label(story, index)
            if value in seen:
                problems.append(f'{label}: {key} "{value}" is also {seen[value]}\'s')
                if label not in refused:
                    refused.append(label)
            else:
                seen[value] = label
    slots: dict[tuple[Any, Any], str] = {}
    for index, story in enumerate(stories):
        publish = _get(story, "publish")
        place = (_get(publish, "day"), _get(publish, "slot"))
        if not _is_int(place[0]) or place[1] not in SLOTS:
            continue
        label = _label(story, index)
        if place in slots:
            problems.append(f"{label}: publish day {place[0]} {place[1]} is also {slots[place]}'s")
            if label not in refused:
                refused.append(label)
        else:
            slots[place] = label
    numbers = [_get(story, "number") for story in stories]
    if stories and all(_is_int(number) for number in numbers):
        if sorted(numbers) != list(range(1, len(stories) + 1)):
            problems.append(
                f"the stories must be numbered 1 to {len(stories)}, each once, without a gap"
            )
    ordered = sorted(
        (story for story in stories if isinstance(story, dict) and _is_int(story.get("number"))),
        key=lambda story: story["number"],
    )
    return FileCheck(series_object, ordered, problems, refused, ignored)


# --- the import --------------------------------------------------------------------------------

Action = Literal["create", "update", "unchanged", "started"]


@dataclass
class RowPlan:
    """What the import does with one story: create its row, update it, leave it as it is (the
    same content), or leave it alone because the worker took it."""

    story_id: str
    action: Action
    values: dict[str, Any]
    row: VideoDramaEpisode | None = None


@dataclass
class StoryImportReport:
    """What an import did or would do; ``as_dict`` is what the command prints."""

    series: str
    apply: bool
    series_exists: bool = False
    series_created: bool = False
    stories: int = 0
    selected: int = 0
    create: list[str] = field(default_factory=list)
    update: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    started: list[str] = field(default_factory=list)
    renumbered: list[str] = field(default_factory=list)
    refused: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    series_differs: dict[str, dict[str, Any]] = field(default_factory=dict)
    written: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "series": self.series,
            "dry_run": not self.apply,
            # No problem anywhere: with --apply the rows are (or were) written.
            "accepted": not self.problems,
            "written": self.written,
            "series_exists": self.series_exists,
            # Created by this run, or, in a dry run, what --apply would create.
            "series_created": self.series_created,
            "stories_in_file": self.stories,
            "stories_imported": self.selected,
            "create": len(self.create),
            "update": len(self.update),
            "leave_alone": len(self.unchanged) + len(self.started),
            "refuse": len(self.refused),
            "rows": {
                "create": self.create,
                "update": self.update,
                "renumbered": self.renumbered,
                "unchanged": self.unchanged,
                "started": self.started,
                "refused": self.refused,
            },
            "series_differs": self.series_differs,
            "problems": self.problems,
            "notes": self.notes,
        }


def episode_values(story: dict[str, Any]) -> dict[str, Any]:
    """The episode row's columns for a story; the fields that are not columns are its beats."""
    return {
        "number": story["number"],
        "chapter_number": 1,
        "title": story["title"],
        "logline": story["logline"],
        "slug": story["slug"],
        "beats": {key: value for key, value in story.items() if key not in COLUMN_KEYS},
        "status": "ready",
    }


def _differs(row: VideoDramaEpisode, values: dict[str, Any]) -> bool:
    return any(getattr(row, key) != value for key, value in values.items())


def _row_label(row: VideoDramaEpisode) -> str:
    story_id = (row.beats or {}).get("id")
    label = f"episode {row.number}"
    return f"{label} ({story_id})" if isinstance(story_id, str) else label


def plan_rows(
    stories: list[dict[str, Any]], rows: list[VideoDramaEpisode], *, in_file: set[str]
) -> tuple[list[RowPlan], list[str], list[str]]:
    """What happens to every story imported now, with the problems and notes it raises.

    ``stories`` are the ones imported this time, ``in_file`` the ids of every story of the file,
    ``rows`` the series' episodes. A row whose story is not imported this time (``--limit``
    stopped before it, or the file no longer has it) keeps its number and its slug, as a
    started row does; a story the file puts on either is a problem.
    """
    problems: list[str] = []
    notes: list[str] = []
    by_id: dict[str, VideoDramaEpisode] = {}
    foreign: list[VideoDramaEpisode] = []
    for row in rows:
        story_id = (row.beats or {}).get("id")
        if not isinstance(story_id, str):
            foreign.append(row)
        elif story_id in by_id:
            problems.append(
                f"episodes {by_id[story_id].number} and {row.number} both carry story {story_id}"
            )
        else:
            by_id[story_id] = row
    imported = {story["id"] for story in stories}
    plans: list[RowPlan] = []
    for story in stories:
        values = episode_values(story)
        found = by_id.get(story["id"])
        if found is None:
            plans.append(RowPlan(story["id"], "create", values))
        elif found.status in NOT_STARTED:
            if is_redo_of(found.slug, values["slug"]):
                # A dropped story being made again (``redo_episode``): the planned slug is the
                # dropped video's, and the remake keeps its own.
                values["slug"] = found.slug
            action: Action = "update" if _differs(found, values) else "unchanged"
            plans.append(RowPlan(story["id"], action, values, found))
        else:
            plans.append(RowPlan(story["id"], "started", values, found))
            if found.number != story["number"]:
                notes.append(
                    f"{story['id']} is {found.status} as episode {found.number} and keeps that "
                    f"number; the file places it at {story['number']}"
                )
    # The rows that keep their number and their slug whatever the file says.
    pinned: dict[int, tuple[VideoDramaEpisode, str]] = {}
    for plan in plans:
        if plan.action == "started" and plan.row is not None:
            pinned[plan.row.number] = (plan.row, f"has {plan.row.status}")
    for story_id, row in by_id.items():
        if story_id in imported:
            continue
        if story_id in in_file:
            pinned[row.number] = (row, "is not imported this time (--limit)")
        else:
            pinned[row.number] = (row, "is not in the file")
            notes.append(f"{_row_label(row)} is not in the file; it is left as it is")
    for row in foreign:
        pinned[row.number] = (row, "has no story id")
        notes.append(f"{_row_label(row)} has no story id; it is left as it is")
    pinned_slugs = {row.slug: (row, why) for row, why in pinned.values() if row.slug is not None}
    for plan in plans:
        if plan.action == "started":
            continue
        number, slug = plan.values["number"], plan.values["slug"]
        held = pinned.get(number)
        if held is not None and held[0] is not plan.row:
            problems.append(
                f"{plan.story_id}: number {number} is {_row_label(held[0])}, which {held[1]}; "
                "the file cannot put another story there"
            )
        owner = pinned_slugs.get(slug)
        if owner is not None and owner[0] is not plan.row:
            problems.append(
                f"{plan.story_id}: slug {slug} is {_row_label(owner[0])}'s, which {owner[1]}"
            )
    return plans, problems, notes


def _series_fields(series: dict[str, Any], episodes_per_day: int | None) -> dict[str, Any]:
    fields = {key: value for key, value in series.items() if key in SeriesIn.model_fields}
    if episodes_per_day is not None:
        fields["episodes_per_day"] = episodes_per_day
    return fields


def _validation_problems(error: ValidationError) -> list[str]:
    return [
        f"series.{'.'.join(str(part) for part in problem['loc'])}: {problem['msg']}"
        if problem["loc"]
        else f"series: {problem['msg']}"
        for problem in error.errors()
    ]


# The series fields the report compares with an existing row; the import never changes them.
COMPARED = (
    "title",
    "premise",
    "note",
    "target_minutes",
    "planned_episodes",
    "episodes_per_day",
    "image_model",
    "look",
    "style_preset",
    "hands_off",
    "visual_tier",
    "compilation",
)


def series_differences(row: VideoDramaSeries, series: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        key: {"file": series[key], "series": getattr(row, key)}
        for key in COMPARED
        if key in series and series[key] != getattr(row, key)
    }


async def _slug_conflicts(
    session: AsyncSession, series: VideoDramaSeries | None, plans: list[RowPlan]
) -> list[str]:
    """A slug the import would give a row that another series' episode or a video already has.

    Only new slugs are asked about: a created row's, and an updated row's when it changes.
    """
    wanted = {
        plan.values["slug"]: plan.story_id
        for plan in plans
        if plan.action == "create"
        or (
            plan.action == "update"
            and plan.row is not None
            and plan.row.slug != plan.values["slug"]
        )
    }
    if not wanted:
        return []
    problems: list[str] = []
    others = select(VideoDramaEpisode.slug).where(VideoDramaEpisode.slug.in_(list(wanted)))
    if series is not None:
        others = others.where(VideoDramaEpisode.series_id != series.id)
    for slug in (await session.scalars(others)).all():
        problems.append(f"{wanted[str(slug)]}: slug {slug} is already an episode of another series")
    videos = select(VideoProject.slug).where(VideoProject.slug.in_(list(wanted)))
    for slug in (await session.scalars(videos)).all():
        problems.append(f"{wanted[str(slug)]}: slug {slug} is already a video on /admin/videos")
    return problems


async def import_story_rows(
    session: AsyncSession,
    document: Any,
    *,
    series_slug: str,
    apply: bool = False,
    limit: int | None = None,
    episodes_per_day: int | None = None,
    actor: User | None = None,
) -> StoryImportReport:
    """Check a compiled stories.json and import its stories into the story series named.

    Nothing is written unless ``apply`` and no problem was found. When the series does not
    exist, ``apply`` creates it from the file's series object (kind ``story``, active), with
    ``episodes_per_day`` in place of the file's when given; an existing series row is never
    changed (the owner may have edited it), and the fields that differ are reported. ``limit``
    imports only the first stories in production order; a later run without it adds the rest.
    A run that writes leaves one audit record: who ran it (``actor``; none from the host
    command), the stories created, updated and left alone, and the ``limit`` it ran with.
    """
    report = StoryImportReport(series=series_slug, apply=apply)
    check = check_story_file(document, series_slug)
    report.stories = len(check.stories)
    report.problems.extend(check.problems)
    report.refused.extend(check.refused)
    report.notes.extend(f"{key} is not read by the server" for key in check.ignored)
    report.notes.extend(
        f"series.{key} is not kept by the server"
        for key in check.series
        if key not in SeriesIn.model_fields
    )
    if limit is not None and limit < 1:
        report.problems.append("--limit must be 1 or more")
    if episodes_per_day is not None and not 1 <= episodes_per_day <= STORY_MAX_PER_DAY:
        report.problems.append(f"--episodes-per-day must be 1 to {STORY_MAX_PER_DAY}")
    if report.problems:
        return report

    selected = check.stories[:limit] if limit is not None else check.stories
    report.selected = len(selected)
    statement = select(VideoDramaSeries).where(VideoDramaSeries.slug == series_slug)
    if apply:
        statement = statement.with_for_update()
    series = await session.scalar(statement)
    new_series: SeriesIn | None = None
    rows: list[VideoDramaEpisode] = []
    if series is None:
        report.series_created = True
        try:
            new_series = SeriesIn.model_validate(_series_fields(check.series, episodes_per_day))
        except ValidationError as error:
            report.problems.extend(_validation_problems(error))
    else:
        report.series_exists = True
        if series.kind != "story":
            report.problems.append(
                f"{series_slug} is a {series.kind} series; only a story series takes stories"
            )
            return report
        report.series_differs = series_differences(series, check.series)
        if episodes_per_day is not None:
            report.notes.append(
                "--episodes-per-day applies only when the import creates the series; "
                "change the daily count on /admin/videos"
            )
        rows = list(
            (
                await session.scalars(
                    select(VideoDramaEpisode)
                    .where(VideoDramaEpisode.series_id == series.id)
                    .order_by(VideoDramaEpisode.number)
                )
            ).all()
        )
    planned = check.series.get("planned_episodes")
    if _is_int(planned) and planned != report.stories:
        report.notes.append(
            f"the file has {report.stories} stories and series.planned_episodes is {planned}"
        )
    enabled = await session.scalar(
        select(VideoAutomationSettings.drama_enabled).where(VideoAutomationSettings.id == 1)
    )
    if not enabled:
        report.notes.append(
            "the drama route is switched off in the settings: no story starts until it is on"
        )

    plans, problems, notes = plan_rows(
        selected, rows, in_file={story["id"] for story in check.stories}
    )
    report.problems.extend(problems)
    report.notes.extend(notes)
    report.problems.extend(await _slug_conflicts(session, series, plans))
    for plan in plans:
        getattr(report, plan.action).append(plan.story_id)
        if plan.action == "update" and plan.row is not None:
            if plan.row.number != plan.values["number"]:
                report.renumbered.append(plan.story_id)
    for problem in report.problems:
        head = problem.split(":", 1)[0]
        if ID.fullmatch(head) and head not in report.refused:
            report.refused.append(head)
    if report.problems or not apply:
        return report

    now = datetime.now(UTC)
    if series is None:
        if new_series is None:  # its problems were reported above
            return report
        series = await add_series(session, actor, new_series)
        await session.flush()
    updates = [
        (plan, plan.row) for plan in plans if plan.action == "update" and plan.row is not None
    ]
    creates = [plan for plan in plans if plan.action == "create"]
    if not report.series_created and not updates and not creates:
        return report
    # Out of the way first: a row that moves takes a number no row has, and a row whose slug
    # changes gives its old one up, so no two rows ever share a number or a slug in between.
    movers = [
        (plan, row)
        for plan, row in updates
        if row.number != plan.values["number"] or row.slug != plan.values["slug"]
    ]
    if movers:
        spare = max([row.number for row in rows] + [plan.values["number"] for plan in plans]) + 1
        for offset, (plan, row) in enumerate(movers):
            if row.number != plan.values["number"]:
                row.number = spare + offset
            if row.slug != plan.values["slug"]:
                row.slug = None
        await session.flush()
    for plan, row in updates:
        for key, value in plan.values.items():
            setattr(row, key, value)
        row.updated_at = now
    await session.flush()
    for plan in creates:
        session.add(
            VideoDramaEpisode(
                id=uuid4(),
                series_id=series.id,
                **plan.values,
                state_json={},
                created_at=now,
                updated_at=now,
            )
        )
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id if actor else None,
            action="video_story_imported",
            target=f"video-series:{series.slug}",
            metadata_json={
                "series_created": report.series_created,
                "created": report.create,
                "updated": report.update,
                "renumbered": report.renumbered,
                "left_alone": len(report.unchanged) + len(report.started),
                "limit": limit,
            },
        )
    )
    await session.commit()
    report.written = True
    return report
