"""Serialise a saved trip as an RFC 5545 calendar.

Every time in the itinerary is already an instant with a timezone, so the events are
written in UTC with a trailing ``Z``. That is unambiguous in every calendar client and
avoids shipping a ``VTIMEZONE`` block whose rules would go stale the next time a country
changes its offset; the reader still sees the local time of wherever they are, and the
trip's own timezone travels along in ``X-WR-TIMEZONE`` for clients that show it.

Travel between two stops is written into the description of the stop it leads to, so a
traveller reading tomorrow's calendar sees how they get there. A leg nobody has routed
yet says so in the reader's language rather than pretending to be a timetable.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Final
from uuid import UUID

from app.i18n import DEFAULT_LOCALE, Locale
from app.models import TripPlan, TripPlanItem
from app.trips.route_planner import ESTIMATED_SEGMENT_PROVIDER
from app.trips.routing import RouteSegment

PRODUCT_ID: Final = "-//Mokaair//Trip Planner//EN"
# 75 octets per RFC 5545 section 3.1, counted before the leading space of a folded line.
FOLD_LIMIT: Final = 75

TRAVEL_MODE_LABELS: Final[dict[str, dict[Locale, str]]] = {
    "transit": {
        "zh-TW": "大眾運輸",
        "zh-CN": "公共交通",
        "en": "Transit",
        "ja": "公共交通",
        "ko": "대중교통",
    },
    "walk": {"zh-TW": "步行", "zh-CN": "步行", "en": "Walk", "ja": "徒歩", "ko": "도보"},
    "drive": {"zh-TW": "開車", "zh-CN": "开车", "en": "Drive", "ja": "車", "ko": "자동차"},
}
LABELS: Final[dict[str, dict[Locale, str]]] = {
    "travel": {
        "zh-TW": "前往方式",
        "zh-CN": "前往方式",
        "en": "Getting there",
        "ja": "移動",
        "ko": "이동",
    },
    "minutes": {
        "zh-TW": "{minutes} 分鐘",
        "zh-CN": "{minutes} 分钟",
        "en": "{minutes} min",
        "ja": "{minutes} 分",
        "ko": "{minutes}분",
    },
    "estimated": {
        "zh-TW": "估算",
        "zh-CN": "估算",
        "en": "estimated",
        "ja": "推定",
        "ko": "추정",
    },
    "transfers": {
        "zh-TW": "轉乘 {count} 次",
        "zh-CN": "换乘 {count} 次",
        "en": "{count} transfers",
        "ja": "乗換 {count} 回",
        "ko": "환승 {count}회",
    },
    "fare": {"zh-TW": "車資", "zh-CN": "车资", "en": "Fare", "ja": "運賃", "ko": "요금"},
    "platform": {
        "zh-TW": "月台 {value}",
        "zh-CN": "站台 {value}",
        "en": "Platform {value}",
        "ja": "{value} 番線",
        "ko": "{value} 승강장",
    },
    "exit": {
        "zh-TW": "出口 {value}",
        "zh-CN": "出口 {value}",
        "en": "Exit {value}",
        "ja": "{value} 出口",
        "ko": "{value} 출구",
    },
    "notes": {"zh-TW": "備註", "zh-CN": "备注", "en": "Notes", "ja": "メモ", "ko": "메모"},
    "calendarName": {
        "zh-TW": "{name}（行程）",
        "zh-CN": "{name}（行程）",
        "en": "{name} (itinerary)",
        "ja": "{name}（旅程）",
        "ko": "{name}(일정)",
    },
}


def label(key: str, locale: Locale, **values: object) -> str:
    text = LABELS[key].get(locale) or LABELS[key][DEFAULT_LOCALE]
    return text.format(**values) if values else text


def escape_text(value: str) -> str:
    """Escape the four characters RFC 5545 reserves inside a TEXT value."""
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
        .replace("\r", "\\n")
    )


def fold(line: str) -> list[str]:
    """Split a content line so no line exceeds 75 octets, continuing with one space."""
    encoded = line.encode("utf-8")
    if len(encoded) <= FOLD_LIMIT:
        return [line]
    parts: list[str] = []
    chunk = bytearray()
    limit = FOLD_LIMIT
    for character in line:
        raw = character.encode("utf-8")
        if len(chunk) + len(raw) > limit:
            parts.append(chunk.decode("utf-8"))
            chunk = bytearray()
            limit = FOLD_LIMIT - 1  # the continuation space counts toward the octets
        chunk.extend(raw)
    if chunk:
        parts.append(chunk.decode("utf-8"))
    return [parts[0], *(f" {part}" for part in parts[1:])]


def stamp(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")


def travel_description(segment: RouteSegment, locale: Locale) -> str:
    mode = TRAVEL_MODE_LABELS.get(segment.travel_mode, {}).get(locale) or segment.travel_mode
    minutes = label("minutes", locale, minutes=segment.duration_minutes)
    parts = [f"{label('travel', locale)}: {mode} {minutes}"]
    if segment.provider == ESTIMATED_SEGMENT_PROVIDER or segment.status == "estimated":
        parts[0] = f"{parts[0]}（{label('estimated', locale)}）"
    rides = [step for step in segment.steps if step.travel_mode.upper() == "TRANSIT"]
    if len(rides) > 1:
        parts.append(label("transfers", locale, count=len(rides) - 1))
    lines = [step.line_short_name or step.line_name for step in rides]
    named_lines = [line for line in lines if line]
    if named_lines:
        parts.append(" · ".join(named_lines))
    if segment.fare is not None:
        currency = f"{segment.currency} " if segment.currency else ""
        parts.append(f"{label('fare', locale)}: {currency}{segment.fare}")
    platform = next((step.platform for step in segment.steps if step.platform), None)
    if platform:
        parts.append(label("platform", locale, value=platform))
    exit_name = next((step.exit_name for step in segment.steps if step.exit_name), None)
    if exit_name:
        parts.append(label("exit", locale, value=exit_name))
    return " · ".join(parts)


def event_lines(
    item: TripPlanItem,
    trip: TripPlan,
    arriving: RouteSegment | None,
    locale: Locale,
    now: datetime,
) -> list[str]:
    start, end = item.start_time, item.end_time
    if start is None:
        return []
    finish = end if end is not None and end > start else start
    description: list[str] = []
    if arriving is not None:
        description.append(travel_description(arriving, locale))
    if item.notes:
        description.append(f"{label('notes', locale)}: {item.notes}")
    lines = [
        "BEGIN:VEVENT",
        f"UID:{item.id}@mokaair.com",
        f"DTSTAMP:{stamp(now)}",
        f"DTSTART:{stamp(start)}",
        f"DTEND:{stamp(finish)}",
        f"SUMMARY:{escape_text(item.title or item.item_type)}",
    ]
    location = item.location_name or item.title
    if location:
        lines.append(f"LOCATION:{escape_text(location)}")
    if description:
        lines.append(f"DESCRIPTION:{escape_text('\\n'.join(description))}")
    if item.latitude is not None and item.longitude is not None:
        lines.append(f"GEO:{float(item.latitude):.6f};{float(item.longitude):.6f}")
    lines.append("END:VEVENT")
    return lines


def trip_calendar(
    trip: TripPlan,
    items: list[TripPlanItem],
    segments: list[RouteSegment],
    *,
    locale: Locale = DEFAULT_LOCALE,
    now: datetime | None = None,
) -> str:
    """Render the trip as a calendar; skipped stops and untimed rows are left out."""
    observed_at = now or datetime.now(UTC)
    arriving_by_item: dict[UUID, RouteSegment] = {
        segment.to_item_id: segment for segment in segments
    }
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:{PRODUCT_ID}",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{escape_text(label('calendarName', locale, name=trip.name))}",
    ]
    if trip.timezone:
        lines.append(f"X-WR-TIMEZONE:{escape_text(trip.timezone)}")
    for item in sorted(
        (row for row in items if not row.is_skipped and row.start_time is not None),
        key=lambda row: (row.start_time or observed_at, row.position),
    ):
        lines.extend(
            event_lines(item, trip, arriving_by_item.get(item.id), locale, observed_at)
        )
    lines.append("END:VCALENDAR")
    folded = [part for line in lines for part in fold(line)]
    return "\r\n".join(folded) + "\r\n"
