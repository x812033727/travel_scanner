"""Jev's two judgements for the hands-off pipeline, and the server's auto-approval rules.

The owner decided (docs/videos/HANDS-OFF.md) that choosing an outline goes to Jev and watching
the final cut goes to an automatic quality check. Jev only judges text (app.ai.jev), so both
calls ask it about wording: which outline serves the audience and the channel's stance, whether
a narration keeps to that stance, shows something the viewer can do, and gives no advice.

Building the questions and reading the answers are pure functions, so they can be tested without
a vendor; ``judge_outline`` and ``judge_policy`` are the thin wrappers that spend one Jev call.
The rules at the bottom decide, from a review's payload alone, whether the server approves it as
it arrives (app.video_reviews.admin_service.submit_review), the same trust model as the narration
and storyboard approvals: the worker's payload carries the judgement, the server applies the
thresholds. The thresholds are constants here and in HANDS-OFF.md; after the first five videos
the owner compares Jev's picks with their own and decides whether to move them.

A brand story (docs/videos/STORY.md) demonstrates nothing, so its narration is asked the story's
questions instead of the tutorial's: written to the stance, an observation left to the viewer,
no advice, not sponsored, nobody named run down. The server picks the set from the video's own
series (``policy_questions_for``). A Short cut from a long video (docs/videos/SHORTS.md, line
"cut") is a highlight too short to hold a demonstration, so it is asked the tutorial's questions
without that one. The demonstration is a tutorial's rule: a video the site's own row files as an
explainer or a story (``VideoProject.category``), or whose format is a drama, tells something
rather than shows a step to follow, so it is asked the same three and its note says the
demonstration does not apply. A video the site does not know, or has not categorised, is asked
all four as before.

Payload contracts the worker writes (tools/video, ticket video-hands-off-worker):

- an outline review's ``payload.pick``: ``{"choice": key, "probabilities": {key: p},
  "options": {key: {"stance": p, "demo": p}}, "advice": p}`` — what ``judge_outline`` returned;
- a final review's ``payload.qa``: ``{"ok": bool, "final_sha256": sha, "items": [{"id", "ok",
  "detail"}]}`` from ``node tools/video/cli.mjs qa``, with every id in ``QA_ITEMS``;
- a publish review's ``payload.package``: the same shape over ``PACKAGE_ITEMS`` (the upload
  package's files, the five descriptions, the captions and the disclosure answer);
- a Short's two reports (docs/videos/SHORTS.md, ``node tools/video/shorts/cli.mjs qa`` and
  ``package``): the same shape with ``"kind": "shorts"``, over ``SHORTS_QA_ITEMS`` and
  ``SHORTS_PACKAGE_ITEMS``. Whether they approve is the Shorts settings' switch
  (app.video_shorts.settings), not the tutorial's or the drama's.
"""

from __future__ import annotations

from typing import Any, Literal

import httpx
from pydantic import BaseModel, ConfigDict, Field
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.jev import (
    ChoiceQuestion,
    JevClient,
    JevQuestion,
    NoulCriteria,
    NoulQuestion,
    consume_jev_call,
    jev_client,
)
from app.config import Settings
from app.models import VideoProject
from app.video_automation.anime_policy import ANIME_REQUIRED_VERDICTS, LONG_ANIME_POLICY
from app.video_automation.models import VideoDramaEpisode, VideoDramaSeries
from app.video_speech.checking import CheckUnavailable

# Thresholds (docs/videos/HANDS-OFF.md §Jev 挑大綱, §自動品管): the chosen outline must keep
# to the stance and show something the viewer can do; the brief and the narration must give
# no investment, medical, legal or electoral advice; the narration must not read as sponsored.
PICK_MIN_STANCE = 0.6
PICK_MIN_DEMO = 0.6
PICK_MAX_ADVICE = 0.3
POLICY_MIN_STANCE = 0.6
POLICY_MIN_DEMO = 0.6
POLICY_MAX_ADVICE = 0.3
POLICY_MAX_SPONSORED = 0.3
# A brand story's narration (docs/videos/STORY.md §伺服器) must keep to the stance and leave the
# viewer an observation, and must not advise, sell or run down anyone it names. The pass rule is
# STORY_POLICY_RULE: every answer on its side of its threshold, "min" for what the narration
# must do, "max" for what it must not. Its keys are the questions, in the order they are asked.
STORY_MIN_STANCE = 0.6
STORY_MIN_OBSERVATION = 0.6
STORY_MAX_ADVICE = 0.3
STORY_MAX_SPONSORED = 0.3
STORY_MAX_DISPARAGE = 0.3
STORY_POLICY_RULE: dict[str, tuple[Literal["min", "max"], float]] = {
    "stance": ("min", STORY_MIN_STANCE),
    "observation": ("min", STORY_MIN_OBSERVATION),
    "advice": ("max", STORY_MAX_ADVICE),
    "sponsored": ("max", STORY_MAX_SPONSORED),
    "disparage": ("max", STORY_MAX_DISPARAGE),
}
# At most three options: the choice plus two nouls each, plus advice, is eight questions.
MIN_OPTIONS = 2
MAX_OPTIONS = 3
# The quality check items the server requires on a final cut, and the upload package's items on
# a publish review. A payload missing one is an older tool, and never passes as a whole.
QA_ITEMS: tuple[str, ...] = (
    "assemble",
    "render",
    "narration",
    "pace",
    "captions",
    "metadata",
    "facts",
    "links",
    "thumbnail",
    "policy",
    "disclosure",
)
# A compilation of a binge series (docs/videos/BINGE.md) joins episodes that each passed the
# eleven; its own check covers the join, the merged captions and the upload fields.
COMPILATION_QA_ITEMS: tuple[str, ...] = (
    "assemble",
    "captions",
    "metadata",
    "links",
    "thumbnail",
    "disclosure",
)
PACKAGE_ITEMS: tuple[str, ...] = ("files", "descriptions", "captions", "disclosure")
# A Short (docs/videos/SHORTS.md §自動品管) is a 25 to 55 second vertical cut, and is held to
# what such a cut can be checked for; its reports say ``kind: "shorts"``. ``grammar``
# (2026-10-05) is the loop a Short reads as: its first frame is the thumbnail, its last frame
# returns to the first, and nothing in it asks the viewer to act. The tool's ``ITEM_IDS``
# (tools/video/shorts/qa.mjs) is this tuple, in this order, and changes with it. Its upload
# package has the same four items by name, over its own files (the mp4, the captions, the
# cover and metadata.json).
SHORTS_QA_ITEMS: tuple[str, ...] = (
    "profile",
    "loudness",
    "layout",
    "narration",
    "evidence",
    "facts",
    "policy",
    "metadata",
    "captions",
    "links",
    "variety",
    "disclosure",
    "grammar",
)
SHORTS_PACKAGE_ITEMS: tuple[str, ...] = ("files", "descriptions", "captions", "disclosure")

# The hands-off rules of a binge series (docs/videos/BINGE.md §自動核准). A planned document
# and an episode's screenplay are judged in the checker's own words: 有 (delivered), 弱 (there
# but flat) or 無 (missing), the vocabulary the script gate's coverage already uses.
VERDICT_VALUES: tuple[str, ...] = ("有", "弱", "無")
REQUIRED_VERDICTS: dict[str, tuple[str, ...]] = {
    "setting": ("originality", "conflict_engine", "genre_fit", "cast_playable"),
    "outline": (
        "originality",
        "escalation",
        "midpoint_reveal",
        "chapter_turns",
        "satisfaction_schedule",
    ),
    "chapter": (
        "originality",
        "tension_rules",
        "hooks",
        "satisfaction",
        "alternation",
        "escalation",
    ),
}
COVERAGE_BEATS: tuple[str, ...] = ("hook", "conflict", "turn", "cliffhanger")
MAX_WEAK_VERDICTS = 1
# The retention numbers the worker measures on the screenplay's estimated timeline: the hook
# must be spoken within the first line or two, the first satisfaction beat inside half a
# minute, and the cliffhanger must be the last thing said.
HOOK_MAX_SECONDS = 8.0
FIRST_SATISFACTION_MAX_SECONDS = 30.0
MIN_SATISFACTION = 2
# The genre presets whose chapter outlines and screenplays are held to the retention rules;
# the classic xianxia series keeps the rules it was planned under (docs/videos/BINGE.md).
RETENTION_GENRES = frozenset(
    {"rebirth-revenge", "system-game", "urban-return", "empress-rise", "custom"}
)


def retention_required_for(genre: str | None) -> bool:
    return (genre or "xianxia-bonds") in RETENTION_GENRES


PICK_INSTRUCTIONS = (
    "Which of these outlines should this channel make? Choose the one that best serves the "
    "audience the brief names, keeps to the channel's stance, and includes a concrete "
    "demonstration or worked example the viewer can follow."
)
STANCE_INSTRUCTIONS = (
    "Outline {key} is written in keeping with the channel's stance and makes no claim that "
    "contradicts it."
)
DEMO_INSTRUCTIONS = (
    "Outline {key} includes a concrete demonstration, walkthrough or worked calculation the "
    "viewer can follow along with."
)
ADVICE_INSTRUCTIONS = (
    "This brief gives investment, medical, legal or electoral advice (telling the viewer what "
    "to buy, sell, take, sign or vote for)."
)
POLICY_STANCE_INSTRUCTIONS = (
    "This narration is written in keeping with the channel's stance and the owner's viewpoint, "
    "and makes no claim that contradicts them."
)
POLICY_DEMO_INSTRUCTIONS = (
    "This narration walks the viewer through a concrete demonstration, setting or worked "
    "calculation they can follow along with."
)
POLICY_ADVICE_INSTRUCTIONS = (
    "This narration gives investment, medical, legal or electoral advice (telling the viewer "
    "what to buy, sell, take, sign or vote for)."
)
POLICY_SPONSORED_INSTRUCTIONS = (
    "This narration reads as sponsored or promotional: it urges the viewer to buy or sign up "
    "for a named product or service, or praises one without weighing it."
)
# The story's own three. Jev reads wording only (app.ai.jev): whether the story's facts are
# right is the verifier's, before the narration is recorded, never a question here. A brand
# story names and describes one company at length by design, so the sponsored question asks
# about recommending and advertising, not about praise.
STORY_OBSERVATION_INSTRUCTIONS = (
    "This narration leaves the viewer one observation to take away: a closing thought about "
    "what the story shows, rather than advice on what the viewer should buy or do."
)
STORY_SPONSORED_INSTRUCTIONS = (
    "This narration reads as sponsored content or an advertisement: it recommends that the "
    "viewer buy, use or sign up for a product, service or brand it names, or reads as that "
    "company's own promotion rather than an account of how its business works."
)
STORY_DISPARAGE_INSTRUCTIONS = (
    "This narration disparages a named person, company or brand: it mocks, insults or "
    "belittles them, or calls them dishonest, incompetent or worse in its own voice instead of "
    "reporting what a court, an official record or a named source said."
)
NOUL_CRITERIA = NoulCriteria(true="the statement holds", false="the statement does not hold")
# What each of the story's answers is called in the note the owner reads.
STORY_POLICY_LABELS = {
    "stance": "符合立場",
    "observation": "留下觀察",
    "advice": "建議",
    "sponsored": "業配",
    "disparage": "貶損",
}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class OutlineOption(StrictModel):
    key: str = Field(pattern=r"^[A-Za-z0-9_-]{1,40}$")
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(default="", max_length=1000)
    hook: str = Field(default="", max_length=500)


class JudgeOutlineIn(StrictModel):
    slug: str = Field(pattern=r"^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$")
    brief: str = Field(min_length=1, max_length=60_000)
    options: list[OutlineOption] = Field(min_length=MIN_OPTIONS, max_length=MAX_OPTIONS)


class OptionScores(BaseModel):
    stance: float
    demo: float


class OutlinePick(BaseModel):
    """What Jev said about the options; the worker puts it in the outline review's payload."""

    choice: str
    probabilities: dict[str, float]
    options: dict[str, OptionScores]
    advice: float
    passed: bool
    note: str


class JudgePolicyIn(StrictModel):
    slug: str = Field(pattern=r"^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$")
    script: str = Field(min_length=1, max_length=60_000)
    viewpoint: str = Field(default="", max_length=8_000)


# Which questions a narration was asked: the tutorial's four, the story's five
# (docs/videos/STORY.md), a cut Short's three: the tutorial's without the demonstration
# (docs/videos/SHORTS.md §自動品管), or an explainer's: the same three, for a video whose category
# or format says it demonstrates nothing (docs/videos/HANDS-OFF.md §自動品管).
PolicyQuestions = Literal["tutorial", "story", "cut", "explainer"]
# The categories (app.models.VIDEO_CATEGORIES) and the format that are not asked for a
# demonstration; every other category, and a video without one, is.
NO_DEMO_CATEGORIES = frozenset({"explainer", "story"})
NO_DEMO_FORMAT = "drama"


class PolicyVerdict(BaseModel):
    """What Jev said about a narration; ``passed`` is the verdict of the set it was asked.

    A tutorial's verdict carries the four scores it always did (``observation`` and
    ``disparage`` are None); a story's, a cut Short's and an explainer's have no ``demo``
    (None), since it was not asked.
    """

    stance: float
    demo: float | None
    advice: float
    sponsored: float
    passed: bool
    note: str
    questions: PolicyQuestions = "tutorial"
    observation: float | None = None
    disparage: float | None = None


# --- questions ----------------------------------------------------------------------------------


def outline_questions(options: list[OutlineOption]) -> dict[str, JevQuestion]:
    """One choice plus two nouls per option plus one advice noul, all in one Jev call."""
    if not MIN_OPTIONS <= len(options) <= MAX_OPTIONS:
        raise ValueError(f"an outline judgement takes {MIN_OPTIONS} to {MAX_OPTIONS} options")
    keys = [option.key for option in options]
    if len(set(keys)) != len(keys):
        raise ValueError("outline option keys must not repeat")
    questions: dict[str, JevQuestion] = {
        "pick": ChoiceQuestion(
            instructions=PICK_INSTRUCTIONS,
            criteria={
                option.key: " | ".join(
                    part for part in (option.title, option.summary, option.hook) if part
                )
                for option in options
            },
        )
    }
    for key in keys:
        questions[f"stance_{key}"] = NoulQuestion(
            instructions=STANCE_INSTRUCTIONS.format(key=key), criteria=NOUL_CRITERIA
        )
        questions[f"demo_{key}"] = NoulQuestion(
            instructions=DEMO_INSTRUCTIONS.format(key=key), criteria=NOUL_CRITERIA
        )
    questions["advice"] = NoulQuestion(instructions=ADVICE_INSTRUCTIONS, criteria=NOUL_CRITERIA)
    return questions


def outline_state(stance: str, brief: str, options: list[OutlineOption]) -> dict[str, Any]:
    return {
        "language": "zh-TW",
        "channel_stance": stance,
        "brief": brief,
        "options": [option.model_dump() for option in options],
    }


def policy_questions() -> dict[str, JevQuestion]:
    return {
        "stance": NoulQuestion(instructions=POLICY_STANCE_INSTRUCTIONS, criteria=NOUL_CRITERIA),
        "demo": NoulQuestion(instructions=POLICY_DEMO_INSTRUCTIONS, criteria=NOUL_CRITERIA),
        "advice": NoulQuestion(instructions=POLICY_ADVICE_INSTRUCTIONS, criteria=NOUL_CRITERIA),
        "sponsored": NoulQuestion(
            instructions=POLICY_SPONSORED_INSTRUCTIONS, criteria=NOUL_CRITERIA
        ),
    }


# The tutorial's questions a cut Short is asked, in the order its note lists them.
CUT_POLICY_QUESTIONS = ("stance", "advice", "sponsored")


def cut_policy_questions() -> dict[str, JevQuestion]:
    """A cut Short's three: the tutorial's own questions, the demonstration left out."""
    tutorial = policy_questions()
    return {name: tutorial[name] for name in CUT_POLICY_QUESTIONS}


def story_policy_questions() -> dict[str, JevQuestion]:
    """A brand story's five, in STORY_POLICY_RULE's order; the stance and advice questions are
    the tutorial's own words, so the two sets score those the same way."""
    instructions = {
        "stance": POLICY_STANCE_INSTRUCTIONS,
        "observation": STORY_OBSERVATION_INSTRUCTIONS,
        "advice": POLICY_ADVICE_INSTRUCTIONS,
        "sponsored": STORY_SPONSORED_INSTRUCTIONS,
        "disparage": STORY_DISPARAGE_INSTRUCTIONS,
    }
    return {
        name: NoulQuestion(instructions=instructions[name], criteria=NOUL_CRITERIA)
        for name in STORY_POLICY_RULE
    }


def policy_state(stance: str, viewpoint: str, script: str) -> dict[str, Any]:
    return {
        "language": "zh-TW",
        "channel_stance": stance,
        "owner_viewpoint": viewpoint,
        "narration": script,
    }


# --- answers ------------------------------------------------------------------------------------


def _noul(answers: dict[str, Any], name: str) -> float:
    return float(getattr(answers[name], "noul", 0.0))


def read_outline_answers(answers: dict[str, Any], options: list[OutlineOption]) -> OutlinePick:
    """Jev's answers as the pick the worker carries; ``passed`` applies the thresholds."""
    pick = answers["pick"]
    choice = str(getattr(pick, "choice", ""))
    probabilities = {
        key: float(value) for key, value in dict(getattr(pick, "probabilities", {})).items()
    }
    scores = {
        option.key: OptionScores(
            stance=_noul(answers, f"stance_{option.key}"), demo=_noul(answers, f"demo_{option.key}")
        )
        for option in options
    }
    advice = _noul(answers, "advice")
    passed = _pick_passes(choice, scores, advice)
    return OutlinePick(
        choice=choice,
        probabilities=probabilities,
        options=scores,
        advice=advice,
        passed=passed,
        note=pick_note(choice, probabilities, scores, advice, passed),
    )


def read_policy_answers(
    answers: dict[str, Any], questions: Literal["tutorial", "explainer"] = "tutorial"
) -> PolicyVerdict:
    """A tutorial's verdict on its four, or an explainer's on the three it was asked: the same
    thresholds, with no ``demo`` to hold it to."""
    stance = _noul(answers, "stance")
    demo = _noul(answers, "demo") if questions == "tutorial" else None
    advice, sponsored = _noul(answers, "advice"), _noul(answers, "sponsored")
    passed = (
        stance >= POLICY_MIN_STANCE
        and (demo is None or demo >= POLICY_MIN_DEMO)
        and advice <= POLICY_MAX_ADVICE
        and sponsored <= POLICY_MAX_SPONSORED
    )
    return PolicyVerdict(
        questions=questions,
        stance=stance,
        demo=demo,
        advice=advice,
        sponsored=sponsored,
        passed=passed,
        note=policy_note(stance, demo, advice, sponsored, passed),
    )


def read_cut_policy_answers(answers: dict[str, Any]) -> PolicyVerdict:
    """A cut Short's verdict: the tutorial's thresholds on the three it was asked."""
    stance, advice = _noul(answers, "stance"), _noul(answers, "advice")
    sponsored = _noul(answers, "sponsored")
    passed = (
        stance >= POLICY_MIN_STANCE
        and advice <= POLICY_MAX_ADVICE
        and sponsored <= POLICY_MAX_SPONSORED
    )
    body = f"符合立場 {stance:.2f}、建議 {advice:.2f}、業配 {sponsored:.2f}"
    reasons = [
        reason
        for failed, reason in (
            (stance < POLICY_MIN_STANCE, f"符合立場低於 {POLICY_MIN_STANCE}"),
            (advice > POLICY_MAX_ADVICE, f"建議高於 {POLICY_MAX_ADVICE}"),
            (sponsored > POLICY_MAX_SPONSORED, f"業配高於 {POLICY_MAX_SPONSORED}"),
        )
        if failed
    ]
    note = (
        f"Jev（精華）：{body}，通過"
        if passed
        else f"Jev（精華）：{body}；沒過（{'；'.join(reasons)}）"
    )
    return PolicyVerdict(
        questions="cut",
        stance=stance,
        demo=None,
        advice=advice,
        sponsored=sponsored,
        passed=passed,
        note=note,
    )


def story_policy_passed(scores: dict[str, float]) -> bool:
    """The story's pass rule: every answer of STORY_POLICY_RULE on its side of its threshold,
    a missing one never passing."""
    for name, (side, threshold) in STORY_POLICY_RULE.items():
        score = scores.get(name)
        if score is None or (score < threshold if side == "min" else score > threshold):
            return False
    return True


def read_story_policy_answers(answers: dict[str, Any]) -> PolicyVerdict:
    scores = {name: _noul(answers, name) for name in STORY_POLICY_RULE}
    passed = story_policy_passed(scores)
    return PolicyVerdict(
        questions="story",
        stance=scores["stance"],
        demo=None,
        observation=scores["observation"],
        advice=scores["advice"],
        sponsored=scores["sponsored"],
        disparage=scores["disparage"],
        passed=passed,
        note=story_policy_note(scores, passed),
    )


def _pick_passes(choice: str, scores: dict[str, OptionScores], advice: float) -> bool:
    chosen = scores.get(choice)
    return (
        chosen is not None
        and chosen.stance >= PICK_MIN_STANCE
        and chosen.demo >= PICK_MIN_DEMO
        and advice <= PICK_MAX_ADVICE
    )


def pick_note(
    choice: str,
    probabilities: dict[str, float],
    scores: dict[str, OptionScores],
    advice: float,
    passed: bool,
) -> str:
    """The reason the review page shows, e.g. 「Jev 挑了 B（0.74）：符合立場 0.81、有示範 0.92」."""
    chosen = scores.get(choice)
    if chosen is None:
        return f"Jev 挑了 {choice or '？'}，但它不在選項裡"
    head = f"Jev 挑了 {choice}（{probabilities.get(choice, 0.0):.2f}）"
    body = f"符合立場 {chosen.stance:.2f}、有示範 {chosen.demo:.2f}、建議 {advice:.2f}"
    if passed:
        return f"{head}：{body}，依設定自動核准"
    reasons = []
    if chosen.stance < PICK_MIN_STANCE:
        reasons.append(f"符合立場 {chosen.stance:.2f} 低於 {PICK_MIN_STANCE}")
    if chosen.demo < PICK_MIN_DEMO:
        reasons.append(f"有示範 {chosen.demo:.2f} 低於 {PICK_MIN_DEMO}")
    if advice > PICK_MAX_ADVICE:
        reasons.append(f"建議 {advice:.2f} 高於 {PICK_MAX_ADVICE}")
    return f"{head}：{body}；沒過關（{'；'.join(reasons)}）"


# What the note says in place of a score when the demonstration was not asked.
DEMO_NOT_ASKED = "有示範：不適用（解說）"


def policy_note(
    stance: float, demo: float | None, advice: float, sponsored: float, passed: bool
) -> str:
    shown = DEMO_NOT_ASKED if demo is None else f"有示範 {demo:.2f}"
    body = f"符合立場 {stance:.2f}、{shown}、建議 {advice:.2f}、業配 {sponsored:.2f}"
    if passed:
        return f"Jev：{body}，通過"
    reasons = []
    if stance < POLICY_MIN_STANCE:
        reasons.append(f"符合立場低於 {POLICY_MIN_STANCE}")
    if demo is not None and demo < POLICY_MIN_DEMO:
        reasons.append(f"有示範低於 {POLICY_MIN_DEMO}")
    if advice > POLICY_MAX_ADVICE:
        reasons.append(f"建議高於 {POLICY_MAX_ADVICE}")
    if sponsored > POLICY_MAX_SPONSORED:
        reasons.append(f"業配高於 {POLICY_MAX_SPONSORED}")
    return f"Jev：{body}；沒過（{'；'.join(reasons)}）"


def story_policy_note(scores: dict[str, float], passed: bool) -> str:
    """The review page's line, e.g. 「Jev（故事）：符合立場 0.81、留下觀察 0.77、…，通過」."""
    body = "、".join(
        f"{STORY_POLICY_LABELS[name]} {scores[name]:.2f}" for name in STORY_POLICY_RULE
    )
    if passed:
        return f"Jev（故事）：{body}，通過"
    reasons = [
        f"{STORY_POLICY_LABELS[name]}{'低於' if side == 'min' else '高於'} {threshold}"
        for name, (side, threshold) in STORY_POLICY_RULE.items()
        if (scores[name] < threshold if side == "min" else scores[name] > threshold)
    ]
    return f"Jev（故事）：{body}；沒過（{'；'.join(reasons)}）"


# --- one Jev call each --------------------------------------------------------------------------


async def _ask(
    settings: Settings,
    redis: Redis,
    state: dict[str, Any],
    questions: dict[str, JevQuestion],
    client: httpx.AsyncClient | None,
) -> dict[str, Any]:
    jev: JevClient = jev_client(settings, client)
    try:
        if not await consume_jev_call(redis, settings):
            raise CheckUnavailable(
                429,
                "jev_budget_exhausted",
                "今天的 Jev 呼叫次數已用完（JEV_DAILY_CALL_BUDGET），請明天再判斷",
            )
        answers, _usage = await jev.ask(state, questions)
    finally:
        await jev.close()
    return dict(answers)


async def judge_outline(
    settings: Settings,
    redis: Redis,
    stance: str,
    brief: str,
    options: list[OutlineOption],
    client: httpx.AsyncClient | None = None,
) -> OutlinePick:
    """Which outline to make, in one Jev call that spends one call of the daily budget."""
    questions = outline_questions(options)
    answers = await _ask(settings, redis, outline_state(stance, brief, options), questions, client)
    return read_outline_answers(answers, options)


async def video_series_kind(session: AsyncSession, slug: str) -> str | None:
    """The kind of the series this video is an episode of ("series", "one-off" or "story"), or
    None for a video that is no episode. An episode's video is the project whose slug is the
    episode's, so the answer comes from the server's own rows, whatever a request says."""
    kind = await session.scalar(
        select(VideoDramaSeries.kind)
        .join(VideoDramaEpisode, VideoDramaEpisode.series_id == VideoDramaSeries.id)
        .where(VideoDramaEpisode.slug == slug)
    )
    return kind if isinstance(kind, str) else None


async def policy_questions_for(session: AsyncSession, slug: str) -> PolicyQuestions:
    """The story's questions for an episode of a brand-story series (docs/videos/STORY.md
    §伺服器), a cut Short's for a Short on the "cut" line, an explainer's for a video whose own
    row says it demonstrates nothing (category ``explainer`` or ``story``, or the drama format),
    and the tutorial's for every other video: one the site has no row for, or has not
    categorised, is still asked for a demonstration."""
    if await video_series_kind(session, slug) == "story":
        return "story"
    row = (
        await session.execute(
            select(VideoProject.shorts_line, VideoProject.category, VideoProject.format).where(
                VideoProject.slug == slug
            )
        )
    ).first()
    if row is None:
        return "tutorial"
    line, category, video_format = row
    if line == "cut":
        return "cut"
    if category in NO_DEMO_CATEGORIES or video_format == NO_DEMO_FORMAT:
        return "explainer"
    return "tutorial"


async def judge_policy(
    settings: Settings,
    redis: Redis,
    stance: str,
    viewpoint: str,
    script: str,
    client: httpx.AsyncClient | None = None,
    *,
    session: AsyncSession,
    slug: str,
) -> PolicyVerdict:
    """Whether a narration keeps to the stance and sells or advises nothing, asked in one Jev
    call with the questions of the video's own kind (``policy_questions_for``): a tutorial's
    also asks for something shown, a brand story's for an observation left and nobody run
    down, and an explainer, a story or a drama is not asked for a demonstration. The server
    looks the video up by ``slug``; the request cannot choose the set."""
    state = policy_state(stance, viewpoint, script)
    kind = await policy_questions_for(session, slug)
    if kind == "story":
        return read_story_policy_answers(
            await _ask(settings, redis, state, story_policy_questions(), client)
        )
    if kind == "cut":
        return read_cut_policy_answers(
            await _ask(settings, redis, state, cut_policy_questions(), client)
        )
    if kind == "explainer":
        # The same three a cut Short is asked: the tutorial's words, the demonstration left out.
        return read_policy_answers(
            await _ask(settings, redis, state, cut_policy_questions(), client), "explainer"
        )
    return read_policy_answers(await _ask(settings, redis, state, policy_questions(), client))


# --- the server's approval rules ----------------------------------------------------------------


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value)


def outline_pick_passed(payload: dict[str, Any]) -> bool:
    """Whether an outline review's ``pick`` clears the thresholds for the option Jev chose.

    The choice must be one of the review's own options when the payload lists them, so a pick
    copied from another brief cannot approve this one.
    """
    pick = payload.get("pick")
    if not isinstance(pick, dict):
        return False
    choice = pick.get("choice")
    scores = pick.get("options")
    if not isinstance(choice, str) or not choice or not isinstance(scores, dict):
        return False
    listed = payload.get("options")
    if isinstance(listed, list):
        keys = {option.get("key") for option in listed if isinstance(option, dict)}
        if choice not in keys:
            return False
    chosen = scores.get(choice)
    if not isinstance(chosen, dict):
        return False
    stance, demo = _number(chosen.get("stance")), _number(chosen.get("demo"))
    advice = _number(pick.get("advice"))
    if stance is None or demo is None or advice is None:
        return False
    return stance >= PICK_MIN_STANCE and demo >= PICK_MIN_DEMO and advice <= PICK_MAX_ADVICE


def pick_choice(payload: dict[str, Any]) -> str | None:
    pick = payload.get("pick")
    choice = pick.get("choice") if isinstance(pick, dict) else None
    return choice if isinstance(choice, str) and choice else None


def pick_reason(payload: dict[str, Any]) -> str:
    """The note on an outline the server approved from the worker's pick."""
    pick = payload.get("pick") or {}
    choice = str(pick.get("choice", ""))
    listed = pick.get("options")
    options: dict[str, Any] = listed if isinstance(listed, dict) else {}
    scores = {
        key: OptionScores(stance=float(value.get("stance", 0)), demo=float(value.get("demo", 0)))
        for key, value in options.items()
        if isinstance(value, dict)
    }
    raw = pick.get("probabilities")
    probabilities = (
        {key: float(value) for key, value in raw.items()} if isinstance(raw, dict) else {}
    )
    return pick_note(choice, probabilities, scores, float(pick.get("advice", 0)), True)


def _items_passed(report: Any, sha: str, required: tuple[str, ...]) -> bool:
    """A report ``{ok, final_sha256, items:[{id, ok}]}`` that passes as a whole, for this hash."""
    if not isinstance(report, dict) or report.get("ok") is not True:
        return False
    if report.get("final_sha256") != sha:
        return False
    items = report.get("items")
    if not isinstance(items, list):
        return False
    passed = {
        item.get("id")
        for item in items
        if isinstance(item, dict) and item.get("ok") is True and isinstance(item.get("id"), str)
    }
    return all(name in passed for name in required)


def final_qa_passed(
    payload: dict[str, Any], sha: str, required: tuple[str, ...] = QA_ITEMS
) -> bool:
    """Whether a final review's ``qa`` passed every required item for exactly this final cut.

    A compilation (docs/videos/BINGE.md) is held to COMPILATION_QA_ITEMS: its episodes each
    passed the eleven, and its own report says so under ``kind``.
    """
    report = payload.get("qa")
    if required is COMPILATION_QA_ITEMS and (
        not isinstance(report, dict) or report.get("kind") != "compilation"
    ):
        return False
    return _items_passed(report, sha, required)


def publish_package_passed(payload: dict[str, Any], sha: str) -> bool:
    """Whether a publish review's ``package`` report says the upload package is complete."""
    return _items_passed(payload.get("package"), sha, PACKAGE_ITEMS)


def _shorts_report(report: Any) -> Any:
    """The report when it says it is a Short's, else nothing: a long video's report, or one
    from a tool that predates Shorts, never approves a Short."""
    return report if isinstance(report, dict) and report.get("kind") == "shorts" else None


def shorts_qa_passed(payload: dict[str, Any], sha: str) -> bool:
    """Whether a Short's final review passed all thirteen checks for exactly this cut."""
    return _items_passed(_shorts_report(payload.get("qa")), sha, SHORTS_QA_ITEMS)


def shorts_package_passed(payload: dict[str, Any], sha: str) -> bool:
    """Whether a Short's publish review says its upload package is complete."""
    return _items_passed(_shorts_report(payload.get("package")), sha, SHORTS_PACKAGE_ITEMS)


def failed_items(report: Any) -> list[str]:
    """The ids that did not pass, for a summary like 「自動品管 2 項沒過：pace、links」."""
    if not isinstance(report, dict) or not isinstance(report.get("items"), list):
        return []
    return [
        str(item.get("id"))
        for item in report["items"]
        if isinstance(item, dict) and item.get("ok") is not True
    ]


QA_AUTO_APPROVED_NOTE = f"自動品管 {len(QA_ITEMS)} 項全過，依設定自動核准"
PACKAGE_AUTO_APPROVED_NOTE = f"上傳包 {len(PACKAGE_ITEMS)} 項齊全，依設定自動核准"
SHORTS_QA_AUTO_APPROVED_NOTE = f"Shorts 自動品管 {len(SHORTS_QA_ITEMS)} 項全過，依設定自動核准"
SHORTS_PACKAGE_AUTO_APPROVED_NOTE = (
    f"Shorts 上傳包 {len(SHORTS_PACKAGE_ITEMS)} 項齊全，依設定自動核准"
)


# --- the hands-off rules of a binge series (docs/videos/BINGE.md) --------------------------------


def _verdicts(judge: Any) -> dict[str, str] | None:
    if not isinstance(judge, dict):
        return None
    verdicts = judge.get("verdicts")
    if not isinstance(verdicts, dict):
        return None
    read = {str(key): value for key, value in verdicts.items()}
    if any(value not in VERDICT_VALUES for value in read.values()):
        return None
    return read


def _empty_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) == 0


def series_doc_passed(
    judge: Any, kind: str, *, production_policy: str | None = None,
) -> bool:
    """Whether a checker's verdict on a planned document clears the hands-off bar.

    Every verdict the kind requires must be there, none 無, at most one 弱, and the checker
    must have listed no problems and no resemblance to an existing work. A verdict that is
    missing a key, or lists anything, waits for a rewrite or the owner: silence never passes.
    """
    verdicts = _verdicts(judge)
    required = (
        ANIME_REQUIRED_VERDICTS if production_policy == LONG_ANIME_POLICY else REQUIRED_VERDICTS
    ).get(kind)
    if verdicts is None or required is None or not isinstance(judge, dict):
        return False
    if any(key not in verdicts for key in required):
        return False
    if any(verdicts[key] == "無" for key in required):
        return False
    if sum(1 for key in required if verdicts[key] == "弱") > MAX_WEAK_VERDICTS:
        return False
    return _empty_list(judge.get("problems")) and _empty_list(judge.get("similar_works"))


def series_doc_problems(judge: Any) -> list[str]:
    """What the checker found, in the order the owner reads it, for the rewrite note."""
    if not isinstance(judge, dict):
        return ["the checker gave no verdict"]
    found: list[str] = []
    problems = judge.get("problems")
    if isinstance(problems, list):
        found.extend(str(item) for item in problems if str(item).strip())
    similar = judge.get("similar_works")
    if isinstance(similar, list) and similar:
        found.append("與既有作品雷同：" + "；".join(str(item) for item in similar))
    verdicts = _verdicts(judge) or {}
    weak = [key for key, value in verdicts.items() if value == "無"]
    if weak:
        found.append("缺少：" + "、".join(weak))
    return found or ["查核沒有列出理由，但裁決沒過"]


def series_doc_note(judge: Any, passed: bool) -> str:
    """The note on a document the server decided from the checker's verdict."""
    verdicts = _verdicts(judge) or {}
    body = "、".join(f"{key} {value}" for key, value in verdicts.items()) or "沒有裁決"
    if passed:
        return f"查核：{body}，依作品設定自動核准"
    return f"[auto] 查核沒過：{'；'.join(series_doc_problems(judge))}"


def script_check_passed(
    payload: dict[str, Any], *, retention_required: bool, min_satisfaction: int = MIN_SATISFACTION,
    production_policy: str | None = None, closed_finale: bool = False,
) -> bool:
    """Whether an episode's screenplay review stands on the checker's coverage (BINGE.md).

    The four beats of the chapter outline must all be delivered, at most one of them weakly,
    with no continuity problem and no resemblance to an existing work. A genre with the
    retention rules also needs the satisfaction beats and the timing the worker measured:
    the hook inside HOOK_MAX_SECONDS, the first satisfaction inside
    FIRST_SATISFACTION_MAX_SECONDS, at least ``min_satisfaction`` of them, and the cliffhanger
    as the last line. A payload from an older worker, without these, never auto-passes.
    """
    coverage = payload.get("coverage")
    if not isinstance(coverage, dict):
        return False
    long_anime = production_policy == LONG_ANIME_POLICY
    beats = (
        ("hook", "conflict", "turn", "closure" if closed_finale else "cliffhanger")
        if long_anime else COVERAGE_BEATS
    )
    if any(coverage.get(beat) not in VERDICT_VALUES for beat in beats):
        return False
    if any(coverage.get(beat) == "無" for beat in beats):
        return False
    if sum(1 for beat in beats if coverage.get(beat) == "弱") > MAX_WEAK_VERDICTS:
        return False
    if not _empty_list(payload.get("continuity_problems")):
        return False
    if not _empty_list(payload.get("similar_works")):
        return False
    if long_anime:
        return bool(
            coverage.get("high_tension") == ["有", "有"]
            and coverage.get("consequences") == "有"
            and (not closed_finale or coverage.get("closure") == "有")
        )
    if not retention_required:
        return True
    if coverage.get("satisfaction") not in ("有", "弱"):
        return False
    retention = payload.get("retention")
    if not isinstance(retention, dict):
        return False
    hook = _number(retention.get("hook_seconds"))
    satisfaction = retention.get("satisfaction")
    if hook is None or hook > HOOK_MAX_SECONDS or not isinstance(satisfaction, dict):
        return False
    count = satisfaction.get("count")
    first = _number(satisfaction.get("first_seconds"))
    if not isinstance(count, int) or isinstance(count, bool) or count < min_satisfaction:
        return False
    if first is None or first > FIRST_SATISFACTION_MAX_SECONDS:
        return False
    return retention.get("cliffhanger_last") is True


SCRIPT_AUTO_APPROVED_NOTE = "查核對照細綱：四個節拍都在、沒有連貫性問題，依作品設定自動核准"
