from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Any, cast
from uuid import UUID

from pydantic import BaseModel, Field
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TripPlan, TripPlanItem, TripRouteDaySetting, TripRouteSegment
from app.trips.routing import RouteSegment, RouteStep, TravelMode

DEFAULT_TRAVEL_MODE: TravelMode = "transit"
DEFAULT_BUFFER_MINUTES = 10
ROUTE_PREVIEW_TTL_SECONDS = 15 * 60


class RoutingOptions(BaseModel):
    auto_compute: bool = True
    default_travel_mode: TravelMode = DEFAULT_TRAVEL_MODE
    default_buffer_minutes: int = Field(default=DEFAULT_BUFFER_MINUTES, ge=0, le=180)


class RouteItemChange(BaseModel):
    item_id: UUID
    title: str
    old_start_time: datetime | None
    new_start_time: datetime | None
    delta_minutes: int
    fixed_time: bool


class RouteScheduleConflict(BaseModel):
    item_id: UUID
    title: str
    scheduled_start_time: datetime
    projected_start_time: datetime
    late_minutes: int
    suggestions: list[str] = Field(
        default_factory=lambda: ["提早離開前一站", "改用汽車", "縮短前一個安排"]
    )


class RouteScheduleImpact(BaseModel):
    affected_items: list[RouteItemChange] = Field(default_factory=list)
    conflicts: list[RouteScheduleConflict] = Field(default_factory=list)


class ProjectedSchedule(BaseModel):
    impact: RouteScheduleImpact
    item_times: dict[UUID, tuple[datetime | None, datetime | None]]
    segments: list[RouteSegment]


def item_end(item: TripPlanItem, start: datetime | None = None) -> datetime | None:
    effective_start = start or item.start_time
    if effective_start is None:
        return item.end_time
    if item.duration_minutes is not None:
        return effective_start + timedelta(minutes=item.duration_minutes)
    if item.start_time and item.end_time:
        return effective_start + (item.end_time - item.start_time)
    return effective_start + timedelta(minutes=60)


def project_day_schedule(
    rows: list[TripPlanItem],
    segments: list[RouteSegment],
) -> ProjectedSchedule:
    by_pair = {(segment.from_item_id, segment.to_item_id): segment for segment in segments}
    item_times: dict[UUID, tuple[datetime | None, datetime | None]] = {
        row.id: (row.start_time, row.end_time) for row in rows
    }
    changes: list[RouteItemChange] = []
    conflicts: list[RouteScheduleConflict] = []
    projected_segments: list[RouteSegment] = []
    projected_start = rows[0].start_time if rows else None
    projected_end = item_end(rows[0], projected_start) if rows else None

    for previous, following in zip(rows, rows[1:], strict=False):
        segment = by_pair.get((previous.id, following.id))
        if segment is None or projected_end is None:
            projected_start = following.start_time
            projected_end = item_end(following, projected_start)
            continue
        departure = projected_end
        arrival = departure + timedelta(minutes=segment.duration_minutes)
        ready = arrival + timedelta(minutes=segment.buffer_minutes)
        segment_warnings = list(segment.warnings)
        next_start = ready
        if following.fixed_time and following.start_time is not None:
            next_start = max(following.start_time, ready)
            if ready > following.start_time:
                late_minutes = max(1, round((ready - following.start_time).total_seconds() / 60))
                conflict = RouteScheduleConflict(
                    item_id=following.id,
                    title=following.title or following.item_type,
                    scheduled_start_time=following.start_time,
                    projected_start_time=ready,
                    late_minutes=late_minutes,
                )
                conflicts.append(conflict)
                segment_warnings.append(f"固定預約可能遲到 {late_minutes} 分鐘")
        else:
            old_start = following.start_time
            delta = (
                round((next_start - old_start).total_seconds() / 60) if old_start else 0
            )
            if old_start != next_start:
                changes.append(
                    RouteItemChange(
                        item_id=following.id,
                        title=following.title or following.item_type,
                        old_start_time=old_start,
                        new_start_time=next_start,
                        delta_minutes=delta,
                        fixed_time=False,
                    )
                )
            item_times[following.id] = (next_start, item_end(following, next_start))
        if following.fixed_time:
            item_times[following.id] = (following.start_time, following.end_time)
        projected_segments.append(
            segment.model_copy(
                update={
                    "status": (
                        "conflict" if segment_warnings != segment.warnings else segment.status
                    ),
                    "departure_time": departure,
                    "arrival_time": arrival,
                    "ready_time": ready,
                    "warnings": list(dict.fromkeys(segment_warnings)),
                }
            )
        )
        projected_start = next_start
        projected_end = item_end(following, projected_start)

    return ProjectedSchedule(
        impact=RouteScheduleImpact(affected_items=changes, conflicts=conflicts),
        item_times=item_times,
        segments=projected_segments,
    )


def segment_from_record(record: TripRouteSegment) -> RouteSegment:
    status = record.status
    if (
        record.provider != "manual"
        and record.expires_at is not None
        and record.expires_at <= datetime.now(UTC)
    ):
        status = "stale"
    return RouteSegment(
        from_item_id=record.from_item_id,
        to_item_id=record.to_item_id,
        status=status,
        travel_mode=cast(TravelMode, record.travel_mode),
        is_override=record.is_override,
        provider=record.provider,
        attribution=record.attribution,
        generated_at=record.generated_at,
        requested_departure_time=record.requested_departure_time,
        departure_time=record.departure_time,
        arrival_time=record.arrival_time,
        ready_time=record.ready_time,
        expires_at=record.expires_at,
        schedule_mode=record.schedule_mode,
        preference=record.preference,
        duration_minutes=record.duration_minutes,
        buffer_minutes=record.buffer_minutes,
        distance_meters=record.distance_meters,
        fare=record.fare,
        currency=record.currency,
        encoded_polyline=record.encoded_polyline,
        maps_url=record.maps_url,
        provider_route_key=record.provider_route_key,
        route_option_rank=record.route_option_rank,
        steps=[RouteStep.model_validate(step) for step in record.steps],
        details_available=record.details_available,
        warnings=record.warnings,
    )


async def load_route_segments(
    session: AsyncSession,
    trip_id: UUID,
    *,
    day_date: date | None = None,
) -> list[TripRouteSegment]:
    statement = select(TripRouteSegment).where(TripRouteSegment.trip_plan_id == trip_id)
    if day_date is not None:
        statement = statement.where(TripRouteSegment.day_date == day_date)
    return list((await session.scalars(statement.order_by(TripRouteSegment.departure_time))).all())


async def load_day_settings(
    session: AsyncSession,
    trip_id: UUID,
) -> list[TripRouteDaySetting]:
    return list(
        (
            await session.scalars(
                select(TripRouteDaySetting)
                .where(TripRouteDaySetting.trip_plan_id == trip_id)
                .order_by(TripRouteDaySetting.day_date)
            )
        ).all()
    )


async def get_or_create_day_setting(
    session: AsyncSession,
    trip: TripPlan,
    day_date: date,
    *,
    travel_mode: TravelMode | None = None,
    buffer_minutes: int | None = None,
    route_preference: str | None = None,
    auto_compute: bool = True,
    update_existing: bool = True,
) -> TripRouteDaySetting:
    setting = await session.scalar(
        select(TripRouteDaySetting).where(
            TripRouteDaySetting.trip_plan_id == trip.id,
            TripRouteDaySetting.day_date == day_date,
        )
    )
    if setting is None:
        setting = TripRouteDaySetting(
            trip_plan_id=trip.id,
            day_date=day_date,
            default_travel_mode=travel_mode or DEFAULT_TRAVEL_MODE,
            default_buffer_minutes=(
                DEFAULT_BUFFER_MINUTES if buffer_minutes is None else buffer_minutes
            ),
            route_preference=route_preference or trip.route_preference,
            auto_compute=auto_compute,
        )
        session.add(setting)
    elif update_existing:
        if travel_mode is not None:
            setting.default_travel_mode = travel_mode
        if buffer_minutes is not None:
            setting.default_buffer_minutes = buffer_minutes
        if route_preference is not None:
            setting.route_preference = route_preference
        setting.auto_compute = auto_compute
    return setting


def update_record_from_segment(
    record: TripRouteSegment,
    segment: RouteSegment,
    *,
    day_date: date,
    is_override: bool,
    expires_at: datetime | None,
    manual_note: str | None = None,
) -> None:
    record.day_date = day_date
    record.status = segment.status
    record.travel_mode = segment.travel_mode
    record.is_override = is_override
    record.provider = segment.provider
    record.attribution = segment.attribution
    record.preference = segment.preference
    record.schedule_mode = segment.schedule_mode
    record.requested_departure_time = segment.requested_departure_time
    record.departure_time = segment.departure_time
    record.arrival_time = segment.arrival_time
    record.ready_time = segment.ready_time
    record.duration_minutes = segment.duration_minutes
    record.buffer_minutes = segment.buffer_minutes
    record.distance_meters = segment.distance_meters
    record.fare = Decimal(str(segment.fare)) if segment.fare is not None else None
    record.currency = segment.currency
    record.encoded_polyline = segment.encoded_polyline
    record.maps_url = segment.maps_url
    record.provider_route_key = segment.provider_route_key
    record.route_option_rank = segment.route_option_rank
    record.steps = [step.model_dump(mode="json") for step in segment.steps]
    record.details_available = segment.details_available
    record.warnings = segment.warnings
    record.manual_note = manual_note
    record.generated_at = segment.generated_at
    record.expires_at = expires_at


async def persist_projected_segments(
    session: AsyncSession,
    trip_id: UUID,
    day_date: date,
    segments: list[RouteSegment],
    *,
    override_pairs: set[tuple[UUID, UUID]] | None = None,
    manual_notes: dict[tuple[UUID, UUID], str | None] | None = None,
    ttl_seconds: int = 86_400,
) -> None:
    existing = {
        (record.from_item_id, record.to_item_id): record
        for record in await load_route_segments(session, trip_id, day_date=day_date)
    }
    valid_pairs = {(segment.from_item_id, segment.to_item_id) for segment in segments}
    stale_ids = [record.id for pair, record in existing.items() if pair not in valid_pairs]
    if stale_ids:
        await session.execute(delete(TripRouteSegment).where(TripRouteSegment.id.in_(stale_ids)))
    default_expires_at = datetime.now(UTC) + timedelta(seconds=ttl_seconds)
    for segment in segments:
        pair = (segment.from_item_id, segment.to_item_id)
        record = existing.get(pair)
        if record is None:
            record = TripRouteSegment(
                trip_plan_id=trip_id,
                day_date=day_date,
                from_item_id=segment.from_item_id,
                to_item_id=segment.to_item_id,
                provider=segment.provider,
                attribution=segment.attribution,
                duration_minutes=segment.duration_minutes,
            )
            session.add(record)
        update_record_from_segment(
            record,
            segment,
            day_date=day_date,
            is_override=pair in (override_pairs or set()),
            expires_at=(
                None
                if segment.provider == "manual"
                else segment.expires_at or default_expires_at
            ),
            manual_note=(manual_notes or {}).get(pair),
        )


def routing_summary(
    trip: TripPlan,
    settings: list[TripRouteDaySetting],
    records: list[TripRouteSegment],
) -> dict[str, Any]:
    raw_status = cast(dict[str, Any], trip.data.get("routing") or {})
    total = int(raw_status.get("total") or 0)
    completed = len(records)
    status = str(raw_status.get("status") or ("complete" if records else "idle"))
    if status in {"queued", "processing"} and total and completed >= total:
        status = "complete"
    return {
        **raw_status,
        "status": status,
        "total": total,
        "completed": completed,
        "day_settings": [
            {
                "day_date": setting.day_date,
                "default_travel_mode": setting.default_travel_mode,
                "default_buffer_minutes": setting.default_buffer_minutes,
                "route_preference": setting.route_preference,
                "auto_compute": setting.auto_compute,
            }
            for setting in settings
        ],
    }
