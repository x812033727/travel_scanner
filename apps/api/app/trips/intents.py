"""Conversational re-planning: turn a sentence into a reviewable itinerary diff.

The traveller types what they want changed ("第二天下雨，改室內"). This module
re-runs the planner over the same coordinate-verified candidate set the AI
planner already uses, with the sentence carried as additional preference text,
and writes the result into the *existing* itinerary preview envelope.

Three properties are load-bearing:

* **Nothing is written here.** The endpoint only produces a Redis envelope.
  ``POST /trips/{id}/itinerary/apply`` consumes it unchanged, keeping its
  version check, its candidate-signature staleness guard, its idempotent
  replay and its catalog-fallback charge release. There is one apply path.
* **The diff is what apply does.** Both are read off one projection —
  ``app.trips.replan.build_replan_write`` — rather than from two models of the
  same rules, because a diff that under-reports is worse than no diff at all.
* **The model cannot invent a place.** It only ever emits
  ``candidate_key + start_time + reason`` from the supplied set, and the
  intent text reaches it as user-content preference data, never as
  instructions — see the injection clause in ``ai/itinerary.SYSTEM_PROMPT``.
"""

from __future__ import annotations

import hashlib
import json
from datetime import date
from typing import Annotated, Any, Literal
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.itinerary import AIPlannerCandidate
from app.auth.service import CurrentUser
from app.db import get_session
from app.infra import enforce_named_rate_limit, get_redis
from app.models import TripPlanItem
from app.problems import AppError
from app.trips.itinerary import ItineraryItem
from app.trips.replan import ReplanWrite, build_replan_write, trip_zone, wall_clock
from app.trips.router import (
    AI_ITINERARY_PREVIEW_TTL_SECONDS,
    GENERATE_OPERATION,
    REFINE_OPERATION,
    ItineraryGenerateRequest,
    _build_ai_planning,
    _itinerary_preview_key,
    build_itinerary_preview_envelope,
    hydrate_legacy_items,
    load_items,
    owned_trip,
)

router = APIRouter(prefix="/trips", tags=["trips"])
Session = Annotated[AsyncSession, Depends(get_session)]

INTENT_MAX_LENGTH = 400
# Shared with /itinerary/preview: an intent preview costs the same provider call
# as a planner preview, so the two draw on one hourly budget.
INTENT_PREVIEW_LIMIT = 12
INTENT_PREVIEW_WINDOW_SECONDS = 3_600
# Applying a day refinement is free (ai_itinerary_refine seeds at 0 uses), so
# the usage ledger cannot bound a refine loop. This per-trip daily ceiling does.
INTENT_TRIP_LIMIT = 40
INTENT_TRIP_WINDOW_SECONDS = 24 * 60 * 60
# The namespace /itinerary/preview also draws on. Named here because a request
# this endpoint refuses to serve has to hand its slot back.
SHARED_PREVIEW_NAMESPACE = "ai-itinerary-preview-user"

# Field names the diff reports, collapsed into the vocabulary the review sheet
# has copy for. Coordinates and a place id are one idea to a traveller.
_FIELD_LABELS = {
    "title": "title",
    "location_name": "place",
    "provider_place_id": "place",
    "latitude": "place",
    "longitude": "place",
    "duration_minutes": "duration",
    "notes": "notes",
}


class TripIntentRequest(BaseModel):
    version: int = Field(ge=1)
    text: str = Field(min_length=2, max_length=INTENT_MAX_LENGTH)
    scope: Literal["day", "trip"] = "day"
    day_date: date | None = None

    @field_validator("text")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        collapsed = " ".join(value.split())
        if len(collapsed) < 2:
            raise ValueError("text must contain at least 2 characters")
        return collapsed

    @model_validator(mode="after")
    def validate_scope(self) -> TripIntentRequest:
        # The target day is optional: omit both and the whole trip is re-planned.
        if "scope" not in self.model_fields_set:
            self.scope = "day" if self.day_date is not None else "trip"
        if self.scope == "day" and self.day_date is None:
            raise ValueError("day_date is required for day scope")
        if self.scope == "trip":
            self.day_date = None
        return self


def intent_usage_operation(scope: str, *, refinable: bool) -> str:
    """Which metered operation an intent envelope should charge on apply.

    Refinement ships free because nudging one day is a small ask, not because
    the intent bar is a free door onto the planner. Two things have to be true
    for a sentence to be a nudge:

    * it is scoped to one day. A trip-scoped intent re-plans every day from
      the same candidate set and costs the same provider call as
      ``/itinerary/preview``, so it charges what that path charges.
    * that day already holds an AI plan to nudge (``refinable``). A day with
      no replaceable ``ai_planner`` rows is not being refined, it is being
      planned for the first time — which is the paid single-day generation,
      whatever sentence is attached to it. Without this, a traveller with no
      uses left could type one word per day and assemble a whole trip for
      free through the door meant for "還是走太多路了".

    The price is confirmed again at the charge point against the write itself;
    see ``trips.router.apply_usage_operation``.
    """
    return REFINE_OPERATION if scope == "day" and refinable else GENERATE_OPERATION


def _labels(fields: list[str]) -> list[str]:
    seen: list[str] = []
    for name in fields:
        label = _FIELD_LABELS.get(name, name)
        if label not in seen:
            seen.append(label)
    return seen


def _row_entry(item: TripPlanItem, zone: ZoneInfo) -> dict[str, Any]:
    return {
        "candidate_key": item.data.get("candidate_key"),
        "title": item.title,
        "location_name": item.location_name,
        "day_date": item.day_date.isoformat() if item.day_date else None,
        "start_time": wall_clock(item.start_time, zone),
        "duration_minutes": item.duration_minutes,
        "reason": item.data.get("reason") or item.notes,
    }


def _planned_entry(item: ItineraryItem, zone: ZoneInfo) -> dict[str, Any]:
    return {
        "candidate_key": item.data.get("candidate_key"),
        "title": item.title,
        "location_name": item.location_name,
        "day_date": item.day_date.isoformat(),
        "start_time": wall_clock(item.start_time, zone),
        "duration_minutes": item.duration_minutes,
        "reason": item.data.get("reason") or item.notes,
    }


def build_intent_diff(
    *,
    plan: ReplanWrite,
    candidates: list[AIPlannerCandidate],
    existing: list[TripPlanItem],
    timezone: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Describe what applying this envelope would do, and how much room is left.

    Read entirely off ``plan``, the same projection apply executes:

    * every replaceable row lands in exactly one of ``removed``, ``moved``,
      ``changed`` or ``unchanged_count`` — a stop cannot go missing between
      the groups;
    * a generated row apply would drop — a meal slot, or an activity whose
      ``(day, casefolded title)`` collides with a preserved row — is never
      listed as added, because approving a row that then silently vanishes is
      worse than not offering it;
    * meals are reported as changed, never as added or removed, because apply
      rewrites those rows in place.
    """
    zone = trip_zone(timezone)
    removed: list[dict[str, Any]] = []
    added: list[dict[str, Any]] = []
    moved: list[dict[str, Any]] = []
    changed: list[dict[str, Any]] = []
    unchanged = 0
    for pair in plan.pairs:
        if pair.planned is None:
            if pair.stored is not None:
                removed.append(_row_entry(pair.stored, zone))
            continue
        if pair.stored is None:
            added.append(_planned_entry(pair.planned, zone))
            continue
        before = (
            pair.stored.day_date.isoformat() if pair.stored.day_date else None,
            wall_clock(pair.stored.start_time, zone),
        )
        after = (pair.planned.day_date.isoformat(), wall_clock(pair.planned.start_time, zone))
        if pair.reused:
            # The write keeps this row untouched, id included. Nothing to say.
            unchanged += 1
            continue
        if before != after:
            moved.append(
                {
                    "candidate_key": str(pair.planned.data.get("candidate_key") or ""),
                    "title": pair.planned.title,
                    "location_name": pair.planned.location_name,
                    "from": {"day_date": before[0], "start_time": before[1]},
                    "to": {"day_date": after[0], "start_time": after[1]},
                    "fields": _labels(pair.changed),
                    "reason": pair.planned.data.get("reason") or pair.planned.notes,
                }
            )
            continue
        if pair.changed:
            # Same day, same slot, but apply would still overwrite something
            # the traveller can see. Never counted as unchanged.
            changed.append(
                {
                    **_planned_entry(pair.planned, zone),
                    "fields": _labels(pair.changed),
                }
            )
            continue
        unchanged += 1

    meals = [
        {
            "system_role": write.row.system_role,
            "day_date": write.row.day_date.isoformat() if write.row.day_date else None,
            "before_title": write.row.title,
            "after_title": write.title,
            "fields": _labels(write.changed),
            "cleared": write.cleared,
        }
        for write in plan.meals
        if write.changed
    ]

    has_changes = bool(removed or added or moved or changed or meals)
    diff: dict[str, Any] = {
        "removed": removed,
        "added": added,
        "moved": moved,
        "changed": changed,
        "meals": meals,
        "unchanged_count": unchanged,
        "has_changes": has_changes,
    }

    # Every verified place in this area that neither the new plan nor the rest
    # of the trip is already using. Zero means the pool really is spent, which
    # is the only honest basis for 這區已經沒有其他選擇了. Restaurants are
    # counted separately: "try a different day" is false advice when it is the
    # merchant pool that ran out.
    on_trip = {
        str(item.data.get("candidate_key"))
        for item in existing
        if item.data.get("candidate_key")
    }
    used = {
        str(item.data.get("candidate_key"))
        for item in plan.generated
        if item.data.get("candidate_key")
    } | {
        str(write.meal.data.get("candidate_key"))
        for write in plan.meals
        if write.meal is not None and write.meal.data.get("candidate_key")
    }
    hotspots = [
        candidate.key
        for candidate in candidates
        if candidate.kind == "hotspot" and candidate.key not in used | on_trip
    ]
    merchants = [
        candidate.key
        for candidate in candidates
        if candidate.kind == "merchant" and candidate.key not in used | on_trip
    ]
    activity_delta = len(plan.generated) - len(plan.replaceable)
    exhaustion = {
        "exhausted": not has_changes,
        "reason": (
            None
            if has_changes
            else "no_alternatives"
            if not hotspots and not merchants
            else "no_change"
        ),
        "alternative_candidate_count": len(hotspots),
        "alternative_merchant_count": len(merchants),
        # Reported whether or not the diff changed anything: a re-plan that
        # merely reorders the same two stops still leaves the pool spent, and
        # the traveller deserves to know before asking a third time.
        "pool_spent": not hotspots,
        "meal_pool_spent": not merchants,
        "activity_delta": activity_delta,
        # A shorter day with nothing left to offer is exhaustion; a shorter day
        # with options left is a real choice the traveller may have asked for.
        "fewer_stops_without_alternatives": activity_delta < 0 and not hotspots,
    }
    return diff, exhaustion


def _client_view(envelope: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in envelope.items()
        if key not in {"candidate_keys", "candidate_signatures"}
    }


def _intent_request_key(
    user_id: UUID,
    trip_id: UUID,
    idempotency_key: str,
    payload: TripIntentRequest,
) -> str:
    """Replay key that also covers the request body.

    The planner's own replay key hashes the Idempotency-Key alone. Here the
    body is the whole point, so a client that reuses a key for a different
    sentence — or the same sentence on a different day, scope or trip version
    — must not be handed the previous request's plan.
    """
    parts = "\n".join(
        [
            idempotency_key,
            payload.text,
            payload.scope,
            payload.day_date.isoformat() if payload.day_date else "",
            str(payload.version),
        ]
    )
    digest = hashlib.sha256(parts.encode()).hexdigest()
    return f"itinerary:intent-request:{user_id}:{trip_id}:{digest}"


@router.post("/{trip_id}/intents")
async def create_trip_intent(
    trip_id: UUID,
    payload: TripIntentRequest,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    redis = get_redis()
    request_key = _intent_request_key(user.id, trip_id, idempotency_key, payload)
    replay_id = await redis.get(request_key)
    if replay_id:
        cached = await redis.get(_itinerary_preview_key(user.id, trip_id, UUID(str(replay_id))))
        if cached:
            return _client_view(json.loads(str(cached)))
    # Replay is checked before the limits, exactly as /itinerary/preview does,
    # so a client retry does not spend a second slot from the shared budget.
    #
    # Ownership first, then the narrow limit, then the shared one: every gate
    # here counts the calls it rejects, so a request that was never going to
    # run must not spend a slot of the hourly budget /itinerary/preview draws
    # on for the user's other trips.
    trip = await owned_trip(session, user.id, trip_id)
    await enforce_named_rate_limit(
        "ai-itinerary-intent-trip",
        f"{user.id}:{trip_id}",
        limit=INTENT_TRIP_LIMIT,
        window_seconds=INTENT_TRIP_WINDOW_SECONDS,
    )
    await enforce_named_rate_limit(
        "ai-itinerary-preview-user",
        str(user.id),
        limit=INTENT_PREVIEW_LIMIT,
        window_seconds=INTENT_PREVIEW_WINDOW_SECONDS,
    )
    generation = ItineraryGenerateRequest(
        version=payload.version,
        scope=payload.scope,
        day_date=payload.day_date,
    )
    planning, preserved, planning_preserved, candidates = await _build_ai_planning(
        session, trip, generation, extra_notes=payload.text
    )
    if planning.planning.status == "fallback":
        # The catalog fallback re-sorts approved places by coordinate and pace;
        # it never reads `notes`, so the sentence had no effect at all.
        # Shipping that as "your refinement" is the dishonesty this feature
        # exists to avoid, and it is not appliable either.
        raise AppError(
            503,
            "ai_planner_unavailable",
            "AI 規劃暫時無法使用，這次沒有讀到你的描述，請稍後再試",
        )
    result, cached_payload = await build_itinerary_preview_envelope(
        session,
        trip,
        generation,
        planning=planning,
        preserved=preserved,
        planning_preserved=planning_preserved,
        candidates=candidates,
    )
    target_date = payload.day_date if payload.scope == "day" else None
    existing = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    plan = build_replan_write(existing, planning.itinerary, target_date)
    diff, exhaustion = build_intent_diff(
        plan=plan,
        candidates=candidates,
        existing=existing,
        timezone=trip.timezone,
    )
    extras: dict[str, Any] = {
        "intent": {"text": payload.text},
        "diff": diff,
        "exhaustion": exhaustion,
        # Apply reads this to charge the refinement operation instead of a
        # first generation; anything it does not recognise falls back.
        "usage_operation": intent_usage_operation(payload.scope),
    }
    result = {**result, **extras}
    await redis.set(
        _itinerary_preview_key(user.id, trip.id, UUID(str(result["preview_id"]))),
        json.dumps({**cached_payload, **extras}, ensure_ascii=False),
        ex=AI_ITINERARY_PREVIEW_TTL_SECONDS,
    )
    await redis.set(
        request_key,
        str(result["preview_id"]),
        ex=AI_ITINERARY_PREVIEW_TTL_SECONDS,
    )
    return result


__all__ = [
    "GENERATE_OPERATION",
    "REFINE_OPERATION",
    "TripIntentRequest",
    "build_intent_diff",
    "intent_usage_operation",
    "router",
]
