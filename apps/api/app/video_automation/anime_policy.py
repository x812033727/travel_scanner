"""An explicit long-anime contract; category and style alone never enable it.

Runtime budgets are authored seconds. Measured body QA permits only +/-60 seconds
around the declared target; OP/ED and unused broadcast reserve do not count as body.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

LONG_ANIME_POLICY = "long-anime-v1"
ANIME_MIN_MINUTES = 9
ANIME_MAX_MINUTES = 30
BODY_TOLERANCE_SECONDS = 60
STATE_FIELDS = ("time", "knowledge", "character_state", "evidence", "carry_forward")
ENDING_TYPES = {"danger", "reveal", "choice", "reversal", "emotion"}
ANIME_REQUIRED_VERDICTS: dict[str, tuple[str, ...]] = {
    "setting": ("originality", "conflict_engine", "genre_fit", "cast_playable"),
    "outline": ("originality", "escalation", "midpoint_reveal", "chapter_turns", "payoff_schedule"),
    "chapter": (
        "originality",
        "tension_rules",
        "hooks",
        "high_tension",
        "consequences",
        "escalation",
    ),
}


class AnimeRuntimeSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    body_target_seconds: int = Field(
        ge=ANIME_MIN_MINUTES * 60, le=ANIME_MAX_MINUTES * 60, strict=True
    )
    op_ed_budget_seconds: int = Field(ge=0, le=300, strict=True)
    broadcast_slot_seconds: int = Field(gt=0, le=3600, strict=True)
    slot_reserve_seconds: int = Field(ge=0, le=900, strict=True)

    @model_validator(mode="after")
    def _budgets(self) -> Self:
        if self.body_target_seconds % 60:
            raise ValueError("long anime body must be a whole number of minutes")
        if self.broadcast_slot_seconds != (
            self.body_target_seconds + self.op_ed_budget_seconds + self.slot_reserve_seconds
        ):
            raise ValueError("broadcast slot must equal body + OP/ED budget + reserved slot")
        return self


def _read(value: Any, field: str, default: Any = None) -> Any:
    return value.get(field, default) if isinstance(value, dict) else getattr(value, field, default)


def is_long_anime(series: Any) -> bool:
    return _read(series, "production_policy") == LONG_ANIME_POLICY and not _read(
        series, "planning_only", False
    )


def runtime_problem(spec: Any, target_minutes: Any) -> str | None:
    try:
        runtime = (
            spec if isinstance(spec, AnimeRuntimeSpec) else AnimeRuntimeSpec.model_validate(spec)
        )
    except ValidationError as error:
        return f"invalid long-anime runtime: {error.errors()[0]['msg']}"
    if type(target_minutes) is not int or runtime.body_target_seconds != target_minutes * 60:
        return "target_minutes must equal runtime_spec.body_target_seconds / 60"
    return None


def is_closed_anime_finale(series: Any, episode: Any) -> bool:
    return bool(
        is_long_anime(series)
        and _read(series, "open_ended") is False
        and type(_read(episode, "number")) is int
        and _read(episode, "number") == _read(series, "planned_episodes")
        and _read(episode, "closed_ending") is True
    )


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _strings(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (not nonempty or bool(value))
        and all(_text(item) for item in value)
        and len(value) == len(set(value))
    )


def anime_episode_problem(series: Any, episode: Any) -> str | None:
    if not isinstance(episode, dict) or type(episode.get("number")) is not int:
        return "long-anime episode needs an integer number"
    number = episode["number"]
    if not 1 <= number <= _read(series, "planned_episodes", 0):
        return f"episode {number} is outside the series"
    for field in ("title", "logline", "hook", "conflict", "turn", "theme", "consequence"):
        if not _text(episode.get(field)):
            return f"episode {number} needs {field}"
    tension = episode.get("tension")
    if (
        not isinstance(tension, list)
        or len(tension) != 5
        or any(type(score) is not int or not 1 <= score <= 5 for score in tension)
    ):
        return f"episode {number} needs five integer tension scores from 1 to 5"
    closed = episode.get("closed_ending")
    if type(closed) is not bool:
        return f"episode {number} needs an explicit closed_ending boolean"
    finale = is_closed_anime_finale(series, episode)
    if closed and not finale:
        return f"episode {number}: quiet closure belongs only to the closed series' last episode"
    if _read(series, "open_ended") is False and number == _read(series, "planned_episodes"):
        if not finale:
            return f"episode {number}: the closed series must declare its final resolution"
    ending = episode.get("cliffhanger")
    if not isinstance(ending, dict) or not _text(ending.get("text")):
        return f"episode {number} needs its ending text"
    if ending.get("type") not in ENDING_TYPES:
        return f"episode {number} has an invalid ending type"
    if finale:
        if not 1 <= tension[-1] <= 3 or ending.get("type") != "emotion":
            return f"episode {number}: quiet final resolution ends with emotion and tension 1 to 3"
    elif tension[-1] < 4:
        return f"episode {number} must end tense (tension[4] >= 4)"
    events = episode.get("high_tension")
    if not isinstance(events, list) or len(events) != 2:
        return f"episode {number} needs two high-tension events"
    for event, beat in zip(events, ("first_half", "second_half"), strict=True):
        if (
            not isinstance(event, dict)
            or event.get("beat") != beat
            or not all(_text(event.get(key)) for key in ("event", "stakes", "consequence"))
        ):
            return f"episode {number}: {beat} needs event, stakes and consequence"
    if events[0]["event"].strip() == events[1]["event"].strip():
        return f"episode {number} must play two distinct high-tension events"
    state = episode.get("state")
    if not isinstance(state, dict) or not all(_text(state.get(key)) for key in STATE_FIELDS):
        return f"episode {number} needs complete continuity state"
    for key in ("setups", "payoffs", "general_payoffs", "characters", "locations"):
        if not _strings(episode.get(key), nonempty=key in ("characters", "locations")):
            return f"episode {number} needs a distinct text list for {key}"
    return None


def anime_chapter_problem(
    series: Any, episodes: Sequence[dict[str, Any]], previous: Sequence[dict[str, Any]] = ()
) -> str | None:
    for episode in episodes:
        problem = anime_episode_problem(series, episode)
        if problem:
            return problem
    for episode in previous:
        if not isinstance(episode, dict) or anime_episode_problem(series, episode):
            return "previous chapter has invalid long-anime continuity data"
    tail = sorted(previous, key=lambda episode: episode["number"])[-3:]
    ordered = sorted([*tail, *episodes], key=lambda episode: episode["number"])
    for before, now in zip(ordered, ordered[1:], strict=False):
        if now["number"] != before["number"] + 1:
            continue
        if before.get("cliffhanger", {}).get("type") == now["cliffhanger"]["type"]:
            return f"episodes {before['number']} and {now['number']} must vary their ending types"
    for start in range(max(0, len(ordered) - 3)):
        window = ordered[start : start + 4]
        if [episode["number"] for episode in window] != list(
            range(window[0]["number"], window[0]["number"] + 4)
        ):
            continue
        if not any(episode.get("payoffs") or episode.get("general_payoffs") for episode in window):
            return (
                f"episodes {window[0]['number']} to {window[-1]['number']} need a completed payoff"
            )
    return None
