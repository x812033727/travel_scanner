from __future__ import annotations

import asyncio
from datetime import UTC, date, datetime, timedelta
from typing import Any, cast
from uuid import UUID

from redis import Redis as SyncRedis
from rq import Queue
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.config import get_settings
from app.db import SessionFactory, engine
from app.infra import get_redis
from app.models import TripPlan, TripPlanItem
from app.trips.route_planner import (
    get_or_create_day_setting,
    item_end,
    load_route_segments,
    persist_projected_segments,
    project_day_schedule,
    segment_from_record,
)
from app.trips.routing import RoutePoint, RouteSegment, RouteService, TravelMode, is_japan_trip


def _route_point(item: TripPlanItem) -> RoutePoint | None:
    if item.latitude is None or item.longitude is None:
        return None
    return RoutePoint(
        item_id=item.id,
        name=item.location_name or item.title or item.item_type,
        latitude=float(item.latitude),
        longitude=float(item.longitude),
        provider_place_id=item.provider_place_id,
    )


async def _items(session: AsyncSession, trip_id: UUID) -> list[TripPlanItem]:
    return list(
        (
            await session.scalars(
                select(TripPlanItem)
                .where(TripPlanItem.trip_plan_id == trip_id)
                .order_by(TripPlanItem.day_date, TripPlanItem.position)
            )
        ).all()
    )


def _advance_projected_time(
    following: TripPlanItem,
    previous_end: datetime | None,
    segment: RouteSegment,
) -> tuple[datetime | None, datetime | None]:
    arrival = (
        previous_end + timedelta(minutes=segment.duration_minutes)
        if previous_end is not None
        else None
    )
    ready = (
        arrival + timedelta(minutes=segment.buffer_minutes)
        if arrival is not None
        else None
    )
    next_start = (
        max(following.start_time, ready)
        if following.fixed_time
        and following.start_time is not None
        and ready is not None
        else ready or following.start_time
    )
    return next_start, item_end(following, next_start)


async def compute_and_apply_routes(
    session: AsyncSession,
    trip: TripPlan,
    *,
    expected_version: int,
    target_day: date | None = None,
    refresh: bool = False,
) -> dict[str, Any]:
    rows = await _items(session, trip.id)
    target_days = (
        [target_day]
        if target_day is not None
        else sorted({row.day_date for row in rows if row.day_date is not None})
    )
    runtime = await load_runtime_settings(session)
    service = RouteService(get_redis(), runtime)
    computed_by_day: dict[date, list[RouteSegment]] = {}
    override_by_day: dict[date, set[tuple[UUID, UUID]]] = {}
    item_updates: dict[UUID, tuple[datetime | None, datetime | None]] = {}
    warnings: list[str] = []
    conflicts: list[dict[str, Any]] = []
    total_pairs = sum(
        max(0, len([row for row in rows if row.day_date == day_value]) - 1)
        for day_value in target_days
    )

    for day_value in target_days:
        day_rows = [row for row in rows if row.day_date == day_value]
        if len(day_rows) < 2:
            continue
        defaults = cast(dict[str, Any], trip.data.get("routing_defaults") or {})
        setting = await get_or_create_day_setting(
            session,
            trip,
            day_value,
            travel_mode=cast(TravelMode, str(defaults.get("default_travel_mode") or "transit")),
            buffer_minutes=int(defaults.get("default_buffer_minutes") or 10),
            auto_compute=bool(defaults.get("auto_compute", True)),
            update_existing=False,
        )
        existing = {
            (record.from_item_id, record.to_item_id): record
            for record in await load_route_segments(session, trip.id, day_date=day_value)
        }
        segments: list[RouteSegment] = []
        override_pairs: set[tuple[UUID, UUID]] = set()
        projected_start = day_rows[0].start_time
        projected_end = item_end(day_rows[0], projected_start)
        for previous, following in zip(day_rows, day_rows[1:], strict=False):
            pair = (previous.id, following.id)
            saved = existing.get(pair)
            if saved is not None and saved.is_override:
                is_override = True
                travel_mode = cast(TravelMode, saved.travel_mode)
                buffer_minutes = saved.buffer_minutes
            else:
                is_override = False
                travel_mode = cast(TravelMode, setting.default_travel_mode)
                buffer_minutes = setting.default_buffer_minutes
            if saved is not None and saved.is_override and saved.provider == "manual":
                segment = segment_from_record(saved).model_copy(
                    update={"buffer_minutes": buffer_minutes, "expires_at": None}
                )
                segments.append(segment)
                override_pairs.add(pair)
                projected_start, projected_end = _advance_projected_time(
                    following,
                    projected_end,
                    segment,
                )
                continue
            origin, destination = _route_point(previous), _route_point(following)
            if origin is None or destination is None:
                warnings.append(
                    f"{previous.title or previous.item_type} → "
                    f"{following.title or following.item_type} 缺少已確認座標"
                )
                if saved is not None:
                    retained = segment_from_record(saved)
                    segments.append(retained)
                    projected_start, projected_end = _advance_projected_time(
                        following,
                        projected_end,
                        retained,
                    )
                else:
                    projected_start = following.start_time
                    projected_end = item_end(following, projected_start)
                continue
            computed_segment = await service.compute(
                origin,
                destination,
                projected_end,
                setting.route_preference,
                japan=is_japan_trip(trip.timezone, trip.destination_name, trip.data),
                travel_mode=travel_mode,
                refresh=refresh,
            )
            if computed_segment is None:
                warnings.append(
                    f"{previous.title or previous.item_type} → "
                    f"{following.title or following.item_type} 暫無可用路線"
                )
                if saved is not None:
                    stale = segment_from_record(saved)
                    retained = stale.model_copy(
                        update={
                            "status": "stale",
                            "warnings": list(
                                dict.fromkeys(
                                    [*stale.warnings, "重新查詢失敗，暫時保留先前路線。"]
                                )
                            ),
                        }
                    )
                    segments.append(retained)
                    projected_start, projected_end = _advance_projected_time(
                        following,
                        projected_end,
                        retained,
                    )
                else:
                    projected_start = following.start_time
                    projected_end = item_end(following, projected_start)
                continue
            segment = computed_segment.model_copy(
                update={
                    "buffer_minutes": buffer_minutes,
                    "is_override": is_override,
                    "expires_at": (
                        None
                        if segment.provider == "manual"
                        else datetime.now(UTC)
                        + timedelta(seconds=runtime.route_cache_ttl_seconds)
                    ),
                }
            )
            segments.append(segment)
            if is_override:
                override_pairs.add(pair)
            projected_start, projected_end = _advance_projected_time(
                following,
                projected_end,
                segment,
            )
        projection = project_day_schedule(day_rows, segments)
        computed_by_day[day_value] = projection.segments
        override_by_day[day_value] = override_pairs
        item_updates.update(projection.item_times)
        conflicts.extend(
            conflict.model_dump(mode="json") for conflict in projection.impact.conflicts
        )

    completed = sum(len(value) for value in computed_by_day.values())
    has_stale = any(
        segment.status in {"stale", "failed"}
        for segments in computed_by_day.values()
        for segment in segments
    )
    routing_status = "complete" if completed == total_pairs and not has_stale else "partial"
    next_data = {
        **trip.data,
        "routing": {
            "status": routing_status,
            "total": total_pairs,
            "completed": completed,
            "warnings": list(dict.fromkeys(warnings)),
            "conflicts": conflicts,
            "updated_at": datetime.now(UTC).isoformat(),
        },
    }
    next_version = await session.scalar(
        update(TripPlan)
        .where(TripPlan.id == trip.id, TripPlan.version == expected_version)
        .values(version=TripPlan.version + 1, data=next_data)
        .returning(TripPlan.version)
    )
    if next_version is None:
        await session.rollback()
        return {"status": "stale", "total": total_pairs, "completed": 0, "warnings": []}

    for row in rows:
        if row.fixed_time or row.id not in item_updates:
            continue
        start_time, end_time = item_updates[row.id]
        row.start_time = start_time
        row.end_time = end_time
    for day_value, segments in computed_by_day.items():
        await persist_projected_segments(
            session,
            trip.id,
            day_value,
            segments,
            override_pairs=override_by_day[day_value],
            ttl_seconds=runtime.route_cache_ttl_seconds,
        )
    await session.commit()
    return cast(dict[str, Any], next_data["routing"])


async def _run(trip_id: UUID, expected_version: int, target_day: date | None) -> None:
    async with SessionFactory() as session:
        trip = await session.get(TripPlan, trip_id)
        if trip is None:
            return
        try:
            await compute_and_apply_routes(
                session,
                trip,
                expected_version=expected_version,
                target_day=target_day,
            )
        except Exception:
            await session.rollback()
            current = await session.get(TripPlan, trip_id)
            if current is not None and current.version == expected_version:
                current.data = {
                    **current.data,
                    "routing": {
                        "status": "failed",
                        "total": int(
                            cast(dict[str, Any], current.data.get("routing") or {}).get("total")
                            or 0
                        ),
                        "completed": 0,
                        "warnings": ["自動交通計算暫時失敗，可在行程頁重新計算。"],
                        "updated_at": datetime.now(UTC).isoformat(),
                    },
                }
                await session.commit()
            raise


def run_trip_routing_job(
    trip_id: str,
    expected_version: int,
    target_day: str | None = None,
) -> None:
    async def run_and_close_resources() -> None:
        try:
            await _run(
                UUID(trip_id),
                expected_version,
                date.fromisoformat(target_day) if target_day else None,
            )
        finally:
            try:
                await get_redis().aclose()
            finally:
                get_redis.cache_clear()
                await engine.dispose()

    asyncio.run(run_and_close_resources())


def enqueue_trip_routing(
    trip_id: UUID,
    expected_version: int,
    target_day: date | None = None,
) -> str:
    connection = SyncRedis.from_url(get_settings().redis_url)
    queued = Queue("trip-routes", connection=connection).enqueue(
        "app.trips.route_tasks.run_trip_routing_job",
        str(trip_id),
        expected_version,
        target_day.isoformat() if target_day else None,
        job_timeout=180,
    )
    return str(queued.id)
