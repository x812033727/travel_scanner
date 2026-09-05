"""Conversational re-planning: turn a sentence into a reviewable itinerary diff.

The traveller types what they want changed ("第二天下雨，改室內"). This module
re-runs the planner over the same coordinate-verified candidate set the AI
planner already uses, with the sentence carried as additional preference text,
and writes the result into the *existing* itinerary preview envelope.

Two properties are load-bearing:

* **Nothing is written here.** The endpoint only produces a Redis envelope.
  ``POST /trips/{id}/itinerary/apply`` consumes it unchanged, keeping its
  version check, its candidate-signature staleness guard, its idempotent
  replay and its catalog-fallback charge release. There is one apply path.
* **The model cannot invent a place.** It only ever emits
  ``candidate_key + start_time + reason`` from the supplied set, and the
  intent text reaches it as user-content preference data, never as
  instructions — see the injection clause in ``ai/itinerary.SYSTEM_PROMPT``.
"""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime, time
from typing import Annotated, Any, Literal
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.itinerary import AIPlannerCandidate, AIPlanningResult
from app.auth.service import CurrentUser
from app.db import get_session
from app.infra import enforce_named_rate_limit, get_redis
from app.models import TripPlanItem
from app.trips.itinerary import ItineraryItem
from app.trips.router import (
    AI_ITINERARY_PREVIEW_TTL_SECONDS,
    ItineraryGenerateRequest,
    _build_ai_planning,
    _itinerary_preview_key,
    _replaceable_ai_items,
    build_itinerary_preview_envelope,
    load_items,
    owned_trip,
    unset_meal_title,
)

router = APIRouter(prefix="/trips", tags=["trips"])
Session = Annotated[AsyncSession, Depends(get_session)]

INTENT_MAX_LENGTH = 400
# Shared with /itinerary/preview: an intent preview costs the same provider call
# as a planner preview, so the two draw on one hourly budget.
INTENT_PREVIEW_LIMIT = 12
INTENT_PREVIEW_WINDOW_SECONDS = 3_600
# Applying a refinement is free (ai_itinerary_refine seeds at 0 uses), so the
# usage ledger cannot bound a refine loop. This per-trip daily ceiling does.
INTENT_TRIP_LIMIT = 40
INTENT_TRIP_WINDOW_SECONDS = 24 * 60 * 60
REFINE_OPERATION = "ai_itinerary_refine"
MEAL_ROLES = frozenset({"lunch", "dinner"})


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


def _zone(timezone_name: str | None) -> ZoneInfo:
    try:
        return ZoneInfo(timezone_name or "UTC")
    except (ZoneInfoNotFoundError, ValueError):
        return ZoneInfo("UTC")


def _hhmm(value: datetime | time | None, zone: ZoneInfo) -> str | None:
    """Wall-clock HH:MM in the trip's own timezone.

    Stored rows come back with whatever offset the driver hands over while the
    planner's drafts are already in the trip zone; without this normalisation a
    stop that did not move would read as moved.
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        moment = value.astimezone(zone) if value.tzinfo is not None else value
        return moment.strftime("%H:%M")
    return value.strftime("%H:%M")


def _row_entry(item: TripPlanItem, zone: ZoneInfo) -> dict[str, Any]:
    return {
        "candidate_key": item.data.get("candidate_key"),
        "title": item.title,
        "location_name": item.location_name,
        "day_date": item.day_date.isoformat() if item.day_date else None,
        "start_time": _hhmm(item.start_time, zone),
        "duration_minutes": item.duration_minutes,
        "reason": item.data.get("reason") or item.notes,
    }


def _planned_entry(item: ItineraryItem, zone: ZoneInfo) -> dict[str, Any]:
    return {
        "candidate_key": item.data.get("candidate_key"),
        "title": item.title,
        "location_name": item.location_name,
        "day_date": item.day_date.isoformat(),
        "start_time": _hhmm(item.start_time, zone),
        "duration_minutes": item.duration_minutes,
        "reason": item.data.get("reason") or item.notes,
    }


def projected_meal_titles(
    preserved: list[TripPlanItem],
    generated_meals: list[ItineraryItem],
    target_date: date | None,
) -> dict[UUID, str]:
    """Titles the preserved meal rows will carry once apply has run.

    A pure mirror of ``_sync_ai_meal_slots``'s title branch. Apply mutates meal
    rows in place rather than deleting and inserting them, and it builds its
    duplicate-title guard from the *post-sync* titles — so the diff has to know
    them too, without touching the ORM rows this request loaded.
    """
    generated_by_role: dict[tuple[date | None, str | None], ItineraryItem] = {
        (meal.day_date, meal.system_role): meal
        for meal in generated_meals
        if meal.system_role in MEAL_ROLES
    }
    titles: dict[UUID, str] = {}
    for item in preserved:
        if item.title is not None:
            titles[item.id] = item.title
        if target_date is not None and item.day_date != target_date:
            continue
        if item.system_role not in MEAL_ROLES:
            continue
        if item.data.get("meal_selection_source") == "user":
            continue
        meal = generated_by_role.get((item.day_date, item.system_role))
        titles[item.id] = meal.title if meal is not None else unset_meal_title(item.system_role)
    return titles


def build_intent_diff(
    *,
    replaceable: list[TripPlanItem],
    preserved: list[TripPlanItem],
    planning: AIPlanningResult,
    candidates: list[AIPlannerCandidate],
    existing: list[TripPlanItem],
    target_date: date | None,
    timezone: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Describe what applying this envelope would do, and how much room is left.

    Modelled on apply's own write rules rather than on the raw plan:

    * ``replaceable`` is exactly the set apply deletes.
    * A generated row apply would drop — a meal slot, or an activity whose
      ``(day, casefolded title)`` collides with a preserved row — is never
      listed as added, because approving a row that then silently vanishes is
      worse than not offering it.
    * Meals are reported as changed, never as added or removed, because apply
      rewrites those rows in place.
    """
    zone = _zone(timezone)
    generated_meals = [
        item
        for day in planning.itinerary
        for item in day.items
        if item.system_role in MEAL_ROLES
    ]
    meal_titles = projected_meal_titles(preserved, generated_meals, target_date)
    preserved_keys = {
        (item.day_date, (meal_titles.get(item.id) or "").casefold()) for item in preserved
    }
    generated = [
        item
        for day in planning.itinerary
        for item in day.items
        if item.system_role is None
        and (item.day_date, item.title.casefold()) not in preserved_keys
    ]

    old_by_key: dict[str, TripPlanItem] = {}
    unkeyed_removed: list[TripPlanItem] = []
    for item in replaceable:
        key = item.data.get("candidate_key")
        if key:
            old_by_key[str(key)] = item
        else:
            unkeyed_removed.append(item)
    new_by_key: dict[str, ItineraryItem] = {}
    unkeyed_added: list[ItineraryItem] = []
    for planned in generated:
        planned_key = planned.data.get("candidate_key")
        if planned_key:
            new_by_key[str(planned_key)] = planned
        else:
            unkeyed_added.append(planned)

    removed = [
        _row_entry(item, zone) for key, item in old_by_key.items() if key not in new_by_key
    ]
    removed.extend(_row_entry(item, zone) for item in unkeyed_removed)
    added = [
        _planned_entry(item, zone) for key, item in new_by_key.items() if key not in old_by_key
    ]
    added.extend(_planned_entry(item, zone) for item in unkeyed_added)

    moved: list[dict[str, Any]] = []
    unchanged = 0
    for key, new_item in new_by_key.items():
        old_item = old_by_key.get(key)
        if old_item is None:
            continue
        before = (
            old_item.day_date.isoformat() if old_item.day_date else None,
            _hhmm(old_item.start_time, zone),
        )
        after = (new_item.day_date.isoformat(), _hhmm(new_item.start_time, zone))
        if before == after:
            unchanged += 1
            continue
        moved.append(
            {
                "candidate_key": key,
                "title": new_item.title,
                "location_name": new_item.location_name,
                "from": {"day_date": before[0], "start_time": before[1]},
                "to": {"day_date": after[0], "start_time": after[1]},
                "reason": new_item.data.get("reason") or new_item.notes,
            }
        )

    meals: list[dict[str, Any]] = []
    for item in preserved:
        projected = meal_titles.get(item.id)
        if item.system_role not in MEAL_ROLES or projected is None or projected == item.title:
            continue
        meals.append(
            {
                "system_role": item.system_role,
                "day_date": item.day_date.isoformat() if item.day_date else None,
                "before_title": item.title,
                "after_title": projected,
                "cleared": projected == unset_meal_title(item.system_role),
            }
        )

    has_changes = bool(removed or added or moved or meals)
    diff: dict[str, Any] = {
        "removed": removed,
        "added": added,
        "moved": moved,
        "meals": meals,
        "unchanged_count": unchanged,
        "has_changes": has_changes,
    }

    # Every verified place in this area that neither the new plan nor the rest
    # of the trip is already using. Zero means the pool really is spent, which
    # is the only honest basis for 這區已經沒有其他選擇了.
    on_trip = {
        str(item.data.get("candidate_key"))
        for item in existing
        if item.data.get("candidate_key")
    }
    alternatives = [
        candidate.key
        for candidate in candidates
        if candidate.kind == "hotspot"
        and candidate.key not in new_by_key
        and candidate.key not in on_trip
    ]
    activity_delta = len(generated) - len(replaceable)
    exhaustion = {
        "exhausted": not has_changes,
        "reason": (
            None
            if has_changes
            else "no_alternatives"
            if not alternatives
            else "no_change"
        ),
        "alternative_candidate_count": len(alternatives),
        "activity_delta": activity_delta,
        # A shorter day with nothing left to offer is exhaustion; a shorter day
        # with options left is a real choice the traveller may have asked for.
        "fewer_stops_without_alternatives": activity_delta < 0 and not alternatives,
    }
    return diff, exhaustion


def _client_view(envelope: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in envelope.items()
        if key not in {"candidate_keys", "candidate_signatures"}
    }


def _intent_request_key(user_id: UUID, trip_id: UUID, idempotency_key: str, text: str) -> str:
    """Replay key that also covers the intent text.

    The planner's own replay key hashes the Idempotency-Key alone. Here the
    request body is the whole point, so a client that reuses a key for a
    different sentence must not be handed the previous sentence's plan.
    """
    digest = hashlib.sha256(f"{idempotency_key}\n{text}".encode()).hexdigest()
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
    request_key = _intent_request_key(user.id, trip_id, idempotency_key, payload.text)
    replay_id = await redis.get(request_key)
    if replay_id:
        cached = await redis.get(_itinerary_preview_key(user.id, trip_id, UUID(str(replay_id))))
        if cached:
            return _client_view(json.loads(str(cached)))
    # Replay is checked before the limits, exactly as /itinerary/preview does,
    # so a client retry does not spend a second slot from the shared budget.
    await enforce_named_rate_limit(
        "ai-itinerary-preview-user",
        str(user.id),
        limit=INTENT_PREVIEW_LIMIT,
        window_seconds=INTENT_PREVIEW_WINDOW_SECONDS,
    )
    await enforce_named_rate_limit(
        "ai-itinerary-intent-trip",
        f"{user.id}:{trip_id}",
        limit=INTENT_TRIP_LIMIT,
        window_seconds=INTENT_TRIP_WINDOW_SECONDS,
    )
    trip = await owned_trip(session, user.id, trip_id)
    generation = ItineraryGenerateRequest(
        version=payload.version,
        scope=payload.scope,
        day_date=payload.day_date,
    )
    planning, preserved, planning_preserved, candidates = await _build_ai_planning(
        session, trip, generation, extra_notes=payload.text
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
    existing = await load_items(session, trip.id)
    replaceable, _ = _replaceable_ai_items(existing, target_date)
    diff, exhaustion = build_intent_diff(
        replaceable=replaceable,
        preserved=preserved,
        planning=planning,
        candidates=candidates,
        existing=existing,
        target_date=target_date,
        timezone=trip.timezone,
    )
    extras: dict[str, Any] = {
        "intent": {"text": payload.text},
        "diff": diff,
        "exhaustion": exhaustion,
        # Apply reads this to charge the refinement operation instead of a
        # first generation; anything it does not recognise falls back.
        "usage_operation": REFINE_OPERATION,
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
    "TripIntentRequest",
    "build_intent_diff",
    "projected_meal_titles",
    "router",
]
