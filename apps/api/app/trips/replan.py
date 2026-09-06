"""What an AI re-plan writes — described once, so apply and the diff cannot disagree.

``POST /trips/{id}/itinerary/apply`` deletes every replaceable ``ai_planner``
row and re-creates it from the draft, and mutates meal slots in place. The
intent bar shows the traveller a diff *before* that happens. When the diff is
built from a second, parallel model of those rules it drifts, and a diff that
under-reports is worse than no diff at all — so both sides call
:func:`build_replan_write` and read the same projection.

Two rules the projection encodes:

* **A stop the planner re-proposes keeps the traveller's own edits.** A note,
  a stay length, a renamed stop and a hand-picked place all survive the
  delete-and-recreate, because losing work the traveller did is a bug whether
  or not a diff line confesses it. Everything the *planner* wrote — its
  reason, its catalog coordinates — is refreshed as usual.
* **A field that would still change is named.** :attr:`RowPair.changed` and
  :attr:`MealWrite.changed` list the traveller-visible fields the write would
  overwrite, so ``unchanged`` means unchanged rather than "same slot".
* **A row nothing changes keeps its id.** ``trip_route_segments`` points at
  ``trip_plan_items.id`` with ``ON DELETE CASCADE``, so deleting and
  re-inserting a stop destroys the travel time and note the traveller typed
  between it and its neighbour. A pair the diff counts as *unchanged* is
  therefore reused in place (:attr:`RowPair.reused`) rather than rebuilt —
  "stays exactly as it is" has to include the row's identity, not only the
  values printed on it.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Any
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from app.localized_names import ITEM_LOCATION_KEY, ITEM_TITLE_KEY, item_names
from app.models import TripPlanItem
from app.trips.itinerary import ItineraryDay, ItineraryItem
from app.trips.schedule import MEAL_PLACEHOLDER_LABELS

MEAL_ROLES = frozenset({"lunch", "dinner"})

# ``location_source`` values ``draft_to_itinerary`` writes. Anything else on an
# ai_planner row is a place the traveller picked or typed.
PLANNER_LOCATION_SOURCES = frozenset({"hotspot_catalog", "food_merchant_catalog"})

# Meal ``data`` keys that describe *which place* the slot points at. They are
# dropped before the new merchant's own data is merged in, so a cleared slot
# keeps no trace of the previous restaurant.
MEAL_LOCATION_DATA_KEYS = frozenset(
    {
        "attribution",
        "candidate_key",
        "food_id",
        "generated_by",
        "google_maps_url",
        "map_links",
        "merchant_id",
        "naver_maps_url",
        "place_match_status",
        "place_provider",
    }
)

# ``data`` keys owned by the traveller's own place pick; they travel with the
# coordinates when a confirmed place is carried onto a re-created row.
PLACE_DATA_KEYS = frozenset(
    {
        "attribution",
        "google_maps_url",
        "naver_maps_url",
        "needs_place_confirmation",
        "opening_hours",
        "place_match_status",
        "place_provider",
    }
)

# Fields a traveller sees on a stop. The planner's own ``reason`` is not one of
# them: it is regenerated every run and reporting it would bury the changes
# that matter.
COMPARED_FIELDS = (
    "title",
    "location_name",
    "provider_place_id",
    "latitude",
    "longitude",
    "duration_minutes",
)


def trip_zone(timezone_name: str | None) -> ZoneInfo:
    """The trip's timezone, falling back to UTC rather than raising."""
    try:
        return ZoneInfo(timezone_name or "UTC")
    except (ZoneInfoNotFoundError, ValueError):
        return ZoneInfo("UTC")


def wall_clock(value: datetime | time | None, zone: ZoneInfo) -> str | None:
    """HH:MM as the traveller reads it, in the trip's own timezone.

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


def same_slot(stored: TripPlanItem, planned: ItineraryItem, zone: ZoneInfo) -> bool:
    """Does the draft put this stop back on the day and minute it already sits?

    One definition, used by the write (to decide whether the row survives) and
    by the diff (to decide whether to report it as moved). Two answers here is
    how a row gets deleted under a line that called it unchanged.
    """
    return stored.day_date == planned.day_date and wall_clock(
        stored.start_time, zone
    ) == wall_clock(planned.start_time, zone)


def unset_meal_title(system_role: str | None) -> str:
    """Title a meal row falls back to when no merchant was selected for it.

    Reads the shared label table so this string and the row's five-locale
    ``names_json`` can never drift apart.
    """
    role = system_role if system_role in MEAL_PLACEHOLDER_LABELS else "dinner"
    return MEAL_PLACEHOLDER_LABELS[role]["zh-TW"]


def _names_after_carry(names: Mapping[str, Any], carried: Mapping[str, Any]) -> dict[str, Any]:
    """Per-locale labels that still describe a row after the traveller's edits land.

    A carried title is a rename and a carried location is the traveller's own
    pick; the catalog label for that field no longer applies, exactly as
    ``apply_item_request`` drops it on a manual save.
    """
    kept = dict(names)
    if "title" in carried:
        kept.pop(ITEM_TITLE_KEY, None)
    if "location_name" in carried:
        kept.pop(ITEM_LOCATION_KEY, None)
    return kept


def replaceable_ai_items(
    existing: list[TripPlanItem], target_date: date | None
) -> tuple[list[TripPlanItem], list[TripPlanItem]]:
    """Split stored rows into the ones apply deletes and the ones it keeps."""
    replaceable = [
        item
        for item in existing
        if item.data.get("generated_by") == "ai_planner"
        and not item.locked
        and not item.fixed_time
        and (target_date is None or item.day_date == target_date)
    ]
    replaceable_ids = {item.id for item in replaceable}
    return replaceable, [item for item in existing if item.id not in replaceable_ids]


def traveller_notes(row: TripPlanItem) -> str | None:
    """The row's note when the traveller wrote it, ``None`` when the planner did.

    ``draft_to_itinerary`` writes the same string into ``notes`` and into
    ``data["reason"]``. A note that still matches the stored reason is the
    planner's own text and may be replaced; anything else was typed by a
    person and must survive a re-plan.
    """
    notes = (row.notes or "").strip()
    if not notes:
        return None
    return None if notes == str(row.data.get("reason") or "").strip() else row.notes


def traveller_place(row: TripPlanItem) -> bool:
    """Did the traveller choose this row's location rather than the planner?"""
    source = row.location_source
    if source is None:
        # PlacePicker's free-text branch clears the source and flags the row.
        return bool(row.data.get("needs_place_confirmation")) or (
            row.data.get("place_match_status") == "unresolved"
        )
    return source not in PLANNER_LOCATION_SOURCES


def _coordinate(value: Decimal | float | None) -> float | None:
    return None if value is None else round(float(value), 6)


def _same(before: Any, after: Any) -> bool:
    if isinstance(before, Decimal) or isinstance(after, Decimal):
        return _coordinate(before) == _coordinate(after)
    return bool(before == after)


def _changed_fields(stored: TripPlanItem, after: dict[str, Any]) -> list[str]:
    """Traveller-visible fields the projected write would overwrite."""
    changed = [
        name
        for name in COMPARED_FIELDS
        if name in after and not _same(getattr(stored, name), after[name])
    ]
    own = traveller_notes(stored)
    if own is not None and (after.get("notes") or "").strip() != own.strip():
        changed.append("notes")
    return changed


def carried_values(stored: TripPlanItem | None, planned: ItineraryItem) -> dict[str, Any]:
    """Traveller-authored values a re-created row keeps from the stored one.

    Empty when the planner proposes this stop for the first time — there is
    nothing of the traveller's to keep.
    """
    if stored is None:
        return {}
    carried: dict[str, Any] = {}
    notes = traveller_notes(stored)
    if notes is not None:
        carried["notes"] = notes
    if stored.title and stored.title != planned.title:
        carried["title"] = stored.title
    if stored.duration_minutes is not None and stored.duration_minutes != planned.duration_minutes:
        carried["duration_minutes"] = stored.duration_minutes
    if stored.is_skipped:
        carried["is_skipped"] = True
    if traveller_place(stored):
        carried.update(
            {
                "location_name": stored.location_name,
                "latitude": stored.latitude,
                "longitude": stored.longitude,
                "provider_place_id": stored.provider_place_id,
                "location_source": stored.location_source,
                "is_estimated": stored.is_estimated,
                "coordinate_source_type": stored.coordinate_source_type,
                "coordinate_source_url": stored.coordinate_source_url,
                "coordinate_verified_at": stored.coordinate_verified_at,
                "data": {
                    **planned.data,
                    **{
                        key: value
                        for key, value in stored.data.items()
                        if key in PLACE_DATA_KEYS
                    },
                },
            }
        )
    return carried


def apply_carried_values(record: TripPlanItem, carried: dict[str, Any]) -> None:
    """Write the carried edits onto a freshly built record, in place."""
    for name, value in carried.items():
        setattr(record, name, value)
    record.names_json = _names_after_carry(record.names_json or {}, carried)
    if "duration_minutes" in carried and record.start_time is not None:
        minutes = record.duration_minutes
        if minutes is not None:
            record.end_time = record.start_time + timedelta(minutes=minutes)


@dataclass(slots=True)
class RowPair:
    """One stored row and the draft row that replaces it — either may be absent.

    ``reused`` marks the pair the diff counts as unchanged: same day, same
    minute, and not one traveller-visible field between them. Apply keeps that
    stored row — id and all — instead of rebuilding it.
    """

    stored: TripPlanItem | None
    planned: ItineraryItem | None
    carried: dict[str, Any] = field(default_factory=dict)
    changed: list[str] = field(default_factory=list)
    reused: bool = False


@dataclass(slots=True)
class MealWrite:
    """A meal slot apply rewrites in place, and what it would become."""

    row: TripPlanItem
    meal: ItineraryItem | None
    title: str
    notes: str | None
    changed: list[str] = field(default_factory=list)

    @property
    def cleared(self) -> bool:
        return self.meal is None


@dataclass(slots=True)
class ReplanWrite:
    """Everything apply does to the item rows, before it does any of it."""

    replaceable: list[TripPlanItem]
    preserved: list[TripPlanItem]
    meals: list[MealWrite]
    generated: list[ItineraryItem]
    pairs: list[RowPair]

    @property
    def reused(self) -> list[TripPlanItem]:
        """Replaceable rows apply keeps as they are, ids intact."""
        return [pair.stored for pair in self.pairs if pair.reused and pair.stored is not None]

    @property
    def deleted(self) -> list[TripPlanItem]:
        """Replaceable rows apply really does delete — the DELETE's own set.

        Never ``replaceable``: a row the diff calls unchanged is not deleted,
        and deleting it would cascade away the route segments hanging off it.
        """
        kept = {row.id for row in self.reused}
        return [row for row in self.replaceable if row.id not in kept]


def project_meal_writes(
    preserved: list[TripPlanItem],
    generated_meals: list[ItineraryItem],
    target_date: date | None = None,
) -> list[MealWrite]:
    """Project every AI-owned meal slot apply would rewrite, changed or not."""
    generated_by_role: dict[tuple[date | None, str | None], ItineraryItem] = {
        (meal.day_date, meal.system_role): meal
        for meal in generated_meals
        if meal.system_role in MEAL_ROLES
    }
    writes: list[MealWrite] = []
    for row in preserved:
        if target_date is not None and row.day_date != target_date:
            continue
        if row.system_role not in MEAL_ROLES:
            continue
        if row.data.get("meal_selection_source") == "user":
            continue
        meal = generated_by_role.get((row.day_date, row.system_role))
        own_notes = traveller_notes(row)
        if meal is None:
            title = unset_meal_title(row.system_role)
            after: dict[str, Any] = {
                "title": title,
                "location_name": None,
                "provider_place_id": None,
                "latitude": None,
                "longitude": None,
                "notes": own_notes,
            }
        else:
            title = meal.title
            after = {
                "title": title,
                "location_name": meal.location_name,
                "provider_place_id": meal.provider_place_id,
                "latitude": meal.latitude,
                "longitude": meal.longitude,
                "notes": own_notes if own_notes is not None else meal.notes,
            }
        writes.append(
            MealWrite(
                row=row,
                meal=meal,
                title=title,
                notes=after["notes"],
                changed=_changed_fields(row, after),
            )
        )
    return writes


def projected_titles(
    preserved: list[TripPlanItem], meals: list[MealWrite]
) -> dict[UUID, str]:
    """Titles the preserved rows carry once the meal slots have been rewritten.

    Apply builds its duplicate-title guard from the *post-sync* titles, so the
    projection has to know them without touching the ORM rows.
    """
    titles = {row.id: row.title for row in preserved if row.title is not None}
    for write in meals:
        titles[write.row.id] = write.title
    return titles


def projected_meal_titles(
    preserved: list[TripPlanItem],
    generated_meals: list[ItineraryItem],
    target_date: date | None,
) -> dict[UUID, str]:
    """Convenience wrapper: project the meal writes, then read off the titles."""
    return projected_titles(preserved, project_meal_writes(preserved, generated_meals, target_date))


def apply_meal_writes(writes: list[MealWrite]) -> None:
    """Rewrite the projected meal slots in place, exactly as projected."""
    for write in writes:
        row, meal = write.row, write.meal
        kept = {
            key: value for key, value in row.data.items() if key not in MEAL_LOCATION_DATA_KEYS
        }
        row.title = write.title
        row.notes = write.notes
        if meal is not None:
            row.location_name = meal.location_name
            row.names_json = dict(meal.names)
            row.latitude = Decimal(str(meal.latitude)) if meal.latitude is not None else None
            row.longitude = Decimal(str(meal.longitude)) if meal.longitude is not None else None
            row.provider_place_id = meal.provider_place_id
            row.location_source = meal.location_source
            row.is_estimated = meal.is_estimated
            row.data = {**kept, **meal.data, "meal_selection_source": "ai"}
            continue
        row.location_name = None
        row.names_json = item_names(
            title=MEAL_PLACEHOLDER_LABELS[row.system_role or "dinner"]
        )
        row.latitude = None
        row.longitude = None
        row.provider_place_id = None
        row.location_source = None
        row.coordinate_source_type = None
        row.coordinate_source_url = None
        row.coordinate_verified_at = None
        row.is_estimated = True
        row.data = {
            **kept,
            "source_mode": "system",
            "meal_kind": row.system_role,
            "meal_selection_source": "unset",
            "needs_place_confirmation": True,
        }


def sync_ai_meal_slots(
    preserved: list[TripPlanItem],
    generated_meals: list[ItineraryItem],
    target_date: date | None = None,
) -> None:
    """Project the AI-owned meal slots and rewrite them in one step."""
    apply_meal_writes(project_meal_writes(preserved, generated_meals, target_date))


def _pair_rows(
    replaceable: list[TripPlanItem], generated: list[ItineraryItem], zone: ZoneInfo
) -> list[RowPair]:
    """Pair stored rows with draft rows by candidate key, same day first.

    A candidate the trip legitimately holds twice — day-scoped applies do not
    deduplicate across days — must not collapse into one entry, or one of the
    two deletions goes unreported. Surplus stored rows become removals and
    surplus draft rows become additions, so every row lands in exactly one
    group.
    """
    by_key: dict[str, list[TripPlanItem]] = {}
    for row in replaceable:
        key = row.data.get("candidate_key")
        if key:
            by_key.setdefault(str(key), []).append(row)
    matched: set[UUID] = set()
    pairs: list[RowPair] = []
    for planned in generated:
        key = planned.data.get("candidate_key")
        bucket = by_key.get(str(key), []) if key else []
        available = [row for row in bucket if row.id not in matched]
        stored = next(
            (row for row in available if row.day_date == planned.day_date),
            next(iter(available), None),
        )
        if stored is not None:
            matched.add(stored.id)
        carried = carried_values(stored, planned)
        changed = (
            _changed_fields(
                stored,
                {
                    **{name: getattr(planned, name) for name in COMPARED_FIELDS},
                    "notes": planned.notes,
                    **carried,
                },
            )
            if stored is not None
            else []
        )
        pairs.append(
            RowPair(
                stored=stored,
                planned=planned,
                carried=carried,
                changed=changed,
                reused=(
                    stored is not None and not changed and same_slot(stored, planned, zone)
                ),
            )
        )
    pairs.extend(RowPair(stored=row, planned=None) for row in replaceable if row.id not in matched)
    return pairs


def reuse_rows(pairs: list[RowPair]) -> list[TripPlanItem]:
    """Refresh the rows a re-plan keeps, in place, and hand them back.

    A reused pair is one nothing the traveller can see would change, so there
    is nothing to overwrite: only the planner's own text is refreshed — its
    reason and the catalog metadata beside it. Rebuilding the row instead
    would churn its primary key and cascade away every route segment that
    names it, which is how a hand-typed travel time disappears under a line
    promising the stop stays exactly as it is.
    """
    rows: list[TripPlanItem] = []
    for pair in pairs:
        if not pair.reused or pair.stored is None or pair.planned is None:
            continue
        row, planned = pair.stored, pair.planned
        row.position = planned.position
        # The catalog's labels are refreshed like its reason is, minus the fields
        # the traveller owns on this row.
        row.names_json = _names_after_carry(planned.names, pair.carried)
        row.data = pair.carried.get("data", planned.data)
        if "notes" not in pair.carried:
            row.notes = planned.notes
        if row.start_time is not None and row.duration_minutes is not None:
            row.end_time = row.start_time + timedelta(minutes=row.duration_minutes)
        rows.append(row)
    return rows


def build_replan_write(
    existing: list[TripPlanItem],
    itinerary: list[ItineraryDay],
    target_date: date | None,
    *,
    timezone: str | None = None,
) -> ReplanWrite:
    """Everything a re-plan would write, computed without writing any of it.

    ``timezone`` is the trip's, and it decides which stops sit in the same
    slot they already occupy — the rows apply keeps rather than rebuilds.
    """
    replaceable, preserved = replaceable_ai_items(existing, target_date)
    generated_meals = [
        item for day in itinerary for item in day.items if item.system_role in MEAL_ROLES
    ]
    meals = project_meal_writes(preserved, generated_meals, target_date)
    titles = projected_titles(preserved, meals)
    preserved_keys = {
        (row.day_date, (titles.get(row.id) or "").casefold()) for row in preserved
    }
    generated = [
        item
        for day in itinerary
        for item in day.items
        if item.system_role is None
        and (item.day_date, item.title.casefold()) not in preserved_keys
    ]
    return ReplanWrite(
        replaceable=replaceable,
        preserved=preserved,
        meals=meals,
        generated=generated,
        pairs=_pair_rows(replaceable, generated, trip_zone(timezone)),
    )


__all__ = [
    "COMPARED_FIELDS",
    "MEAL_LOCATION_DATA_KEYS",
    "MEAL_ROLES",
    "MealWrite",
    "ReplanWrite",
    "RowPair",
    "apply_carried_values",
    "apply_meal_writes",
    "build_replan_write",
    "carried_values",
    "project_meal_writes",
    "projected_meal_titles",
    "projected_titles",
    "replaceable_ai_items",
    "reuse_rows",
    "same_slot",
    "sync_ai_meal_slots",
    "traveller_notes",
    "traveller_place",
    "trip_zone",
    "unset_meal_title",
    "wall_clock",
]
