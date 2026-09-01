from __future__ import annotations

import hashlib
import math
from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, Field
from redis.asyncio import Redis
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import AdminUser
from app.db import get_session
from app.hotspots.service import PUBLIC_REVIEW_STATUSES
from app.infra import get_redis
from app.models import (
    AdminAuditLog,
    HotspotRestaurantCandidate,
    RestaurantPlace,
    RestaurantScanRun,
    TravelHotspot,
)
from app.problems import AppError
from app.providers.usage_meter import google_maps_usage_snapshot
from app.restaurants.service import create_scan_run
from app.restaurants.tasks import enqueue_restaurant_scan

router = APIRouter(prefix="/admin/hotspots/restaurants", tags=["admin hotspot restaurants"])
Session = Annotated[AsyncSession, Depends(get_session)]
RedisDep = Annotated[Redis, Depends(get_redis)]


class RestaurantScanRequest(BaseModel):
    hotspot_ids: list[UUID] = Field(default_factory=list, max_length=100)
    all_missing: bool = False


class RestaurantSuppressionRequest(BaseModel):
    suppressed: bool
    reason: str | None = Field(default=None, max_length=500)


def _run_view(run: RestaurantScanRun) -> dict[str, object]:
    return {
        "run_id": str(run.id),
        "hotspot_id": str(run.hotspot_id),
        "status": run.status,
        "cells_completed": run.cells_completed,
        "cells_total": run.cells_total,
        "candidate_count": run.candidate_count,
        "aggregate_calls": run.aggregate_calls,
        "details_calls": run.details_calls,
        "failure_code": run.failure_code,
        "started_at": run.started_at.isoformat() if run.started_at else None,
        "completed_at": run.completed_at.isoformat() if run.completed_at else None,
        "updated_at": run.updated_at.isoformat(),
    }


@router.post("/scans", status_code=202)
async def start_restaurant_scans(
    payload: RestaurantScanRequest,
    user: AdminUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, object]:
    if not payload.hotspot_ids and not payload.all_missing:
        raise AppError(422, "restaurant_hotspot_required", "請選擇要掃描的景點")
    settings = await load_runtime_settings(session)
    if not settings.restaurant_scan_enabled or not settings.google_maps_api_key:
        raise AppError(503, "restaurant_google_not_configured", "Google 餐廳掃描尚未啟用")
    query = select(TravelHotspot).where(
        TravelHotspot.is_active.is_(True),
        TravelHotspot.review_status.in_(PUBLIC_REVIEW_STATUSES),
        TravelHotspot.latitude.is_not(None),
        TravelHotspot.longitude.is_not(None),
    )
    if payload.hotspot_ids:
        query = query.where(TravelHotspot.id.in_(payload.hotspot_ids))
    hotspots = list((await session.scalars(query.order_by(TravelHotspot.updated_at.desc()))).all())
    if payload.all_missing:
        covered = set(
            (
                await session.scalars(
                    select(RestaurantScanRun.hotspot_id).where(
                        RestaurantScanRun.status.in_(("completed", "running", "queued"))
                    )
                )
            ).all()
        )
        hotspots = [item for item in hotspots if item.id not in covered][:100]
    if not hotspots:
        return {"runs": [], "status": "nothing_to_scan"}
    runs: list[RestaurantScanRun] = []
    for hotspot in hotspots:
        digest = hashlib.sha256(f"{user.id}:{idempotency_key}:{hotspot.id}".encode()).hexdigest()
        key = f"admin:{digest}"
        existing = await session.scalar(
            select(RestaurantScanRun).where(RestaurantScanRun.idempotency_key == key)
        )
        run = existing or await create_scan_run(
            session,
            hotspot.id,
            actor_user_id=user.id,
            idempotency_key=key,
        )
        if existing is None:
            enqueue_restaurant_scan(run.id, settings)
        runs.append(run)
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="restaurant_scans_started",
            target="hotspot-restaurants",
            metadata_json={"run_ids": [str(run.id) for run in runs]},
        )
    )
    await session.commit()
    return {"runs": [_run_view(run) for run in runs], "status": "queued"}


@router.get("/scans/{run_id}")
async def restaurant_scan_status(
    run_id: UUID,
    user: AdminUser,
    session: Session,
) -> dict[str, object]:
    del user
    run = await session.get(RestaurantScanRun, run_id)
    if run is None:
        raise AppError(404, "restaurant_scan_not_found", "找不到這次餐廳掃描")
    return _run_view(run)


@router.get("/coverage")
async def restaurant_coverage(
    user: AdminUser, session: Session, redis: RedisDep
) -> dict[str, object]:
    del user
    settings = await load_runtime_settings(session)
    usage = await google_maps_usage_snapshot(
        redis,
        essentials_free_limit=settings.google_maps_essentials_free_limit,
        pro_free_limit=settings.google_maps_pro_free_limit,
        enterprise_free_limit=settings.google_maps_enterprise_free_limit,
        history_months=1,
    )
    sku_usage = {item.sku: item for item in usage.sku_usage}
    hotspots = list(
        (
            await session.scalars(
                select(TravelHotspot)
                .where(
                    TravelHotspot.is_active.is_(True),
                    TravelHotspot.review_status.in_(PUBLIC_REVIEW_STATUSES),
                )
                .order_by(TravelHotspot.country_code, TravelHotspot.city_name, TravelHotspot.name)
            )
        ).all()
    )
    count_rows = (
        await session.execute(
            select(
                HotspotRestaurantCandidate.hotspot_id,
                func.count(HotspotRestaurantCandidate.id),
            )
            .join(
                RestaurantPlace,
                RestaurantPlace.id == HotspotRestaurantCandidate.restaurant_place_id,
            )
            .where(
                RestaurantPlace.is_suppressed.is_(False),
                RestaurantPlace.identity_status.not_in(("moved", "not_found")),
            )
            .group_by(HotspotRestaurantCandidate.hotspot_id)
        )
    ).all()
    counts: dict[UUID, int] = {
        hotspot_id: int(candidate_count) for hotspot_id, candidate_count in count_rows
    }
    runs = list(
        (
            await session.scalars(
                select(RestaurantScanRun)
                .where(RestaurantScanRun.hotspot_id.in_([hotspot.id for hotspot in hotspots]))
                .order_by(
                    RestaurantScanRun.hotspot_id,
                    RestaurantScanRun.created_at.desc(),
                )
            )
        ).all()
    )
    latest_runs: dict[UUID, RestaurantScanRun] = {}
    for run in runs:
        latest_runs.setdefault(run.hotspot_id, run)
    call_totals: dict[UUID, tuple[int, int]] = {}
    call_rows = (
        await session.execute(
            select(
                RestaurantScanRun.hotspot_id,
                func.sum(RestaurantScanRun.aggregate_calls),
                func.sum(RestaurantScanRun.details_calls),
            ).group_by(RestaurantScanRun.hotspot_id)
        )
    ).all()
    for hotspot_id, aggregate_calls, details_calls in call_rows:
        call_totals[hotspot_id] = (int(aggregate_calls or 0), int(details_calls or 0))
    items: list[dict[str, object]] = []
    for hotspot in hotspots:
        latest_run = latest_runs.get(hotspot.id)
        items.append(
            {
                "hotspot_id": str(hotspot.id),
                "name": hotspot.name,
                "city_name": hotspot.city_name,
                "country_code": hotspot.country_code,
                "candidate_count": int(counts.get(hotspot.id, 0)),
                "status": latest_run.status if latest_run else "not_started",
                "run_id": str(latest_run.id) if latest_run else None,
                "updated_at": latest_run.updated_at.isoformat() if latest_run else None,
                "usage": {
                    "aggregate_calls": call_totals.get(hotspot.id, (0, 0))[0],
                    "details_calls": call_totals.get(hotspot.id, (0, 0))[1],
                    "total_paid_calls": sum(call_totals.get(hotspot.id, (0, 0))),
                },
            }
        )
    elapsed_days = max(1, (datetime.now(UTC).date() - usage.period_start).days + 1)
    period_days = (usage.period_end - usage.period_start).days + 1

    def operation_view(*, used: int, feature_used: int, budget: int) -> dict[str, object]:
        projected = math.ceil(feature_used / elapsed_days * period_days)
        percentage = round(feature_used / budget * 100, 1)
        projected_percentage = round(projected / budget * 100, 1)
        risk_percentage = max(percentage, projected_percentage)
        alert = (
            "critical"
            if risk_percentage >= 90
            else "warning"
            if risk_percentage >= 80
            else "watch"
            if risk_percentage >= 70
            else "normal"
        )
        return {
            "used": used,
            "feature_used": feature_used,
            "budget": budget,
            "percentage": percentage,
            "projected_month_end": projected,
            "projected_percentage": projected_percentage,
            "alert": alert,
        }

    return {
        "total": len(items),
        "completed": sum(item["status"] == "completed" for item in items),
        "items": items,
        "automation_enabled": settings.restaurant_scan_enabled,
        "usage": {
            "period": usage.period,
            "available": usage.available,
            "operations": {
                "aggregate": {
                    **operation_view(
                        used=sku_usage["places_aggregate"].used,
                        feature_used=usage.breakdown.get("places_aggregate_restaurants", 0),
                        budget=min(
                            settings.restaurant_aggregate_monthly_budget,
                            sku_usage["places_aggregate"].free_limit,
                        ),
                    ),
                },
                "nearby": {
                    **operation_view(
                        used=sku_usage["nearby_search_enterprise"].used,
                        feature_used=usage.breakdown.get("places_nearby_restaurants", 0),
                        budget=min(
                            settings.restaurant_nearby_monthly_budget,
                            sku_usage["nearby_search_enterprise"].free_limit,
                        ),
                    ),
                },
                "details": {
                    **operation_view(
                        used=sku_usage["place_details_enterprise"].used,
                        feature_used=usage.breakdown.get("place_details_restaurant", 0),
                        budget=min(
                            settings.restaurant_details_monthly_budget,
                            sku_usage["place_details_enterprise"].free_limit,
                        ),
                    ),
                },
                "ids_only": {
                    "used": usage.breakdown.get("places_text_search_ids_only", 0)
                    + usage.breakdown.get("place_id_refresh", 0),
                    "billing": "no_charge",
                    "budget": None,
                    "operations": {
                        "text_search": usage.breakdown.get("places_text_search_ids_only", 0),
                        "place_id_refresh": usage.breakdown.get("place_id_refresh", 0),
                    },
                },
            },
            "skus": [
                {
                    "sku": sku.sku,
                    "used": sku.used,
                    "free_limit": sku.free_limit,
                    "free_remaining": sku.free_remaining,
                }
                for sku in usage.sku_usage
                if sku.sku
                in {"places_aggregate", "nearby_search_enterprise", "place_details_enterprise"}
            ],
        },
    }


@router.patch("/places/{place_id}")
async def suppress_restaurant(
    place_id: str,
    payload: RestaurantSuppressionRequest,
    user: AdminUser,
    session: Session,
) -> dict[str, object]:
    place = await session.scalar(
        select(RestaurantPlace).where(RestaurantPlace.google_place_id == place_id)
    )
    if place is None:
        raise AppError(404, "restaurant_place_not_found", "找不到這個餐飲地點")
    place.is_suppressed = payload.suppressed
    place.suppression_reason = payload.reason if payload.suppressed else None
    place.suppressed_at = datetime.now(UTC) if payload.suppressed else None
    place.suppressed_by_user_id = user.id if payload.suppressed else None
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="restaurant_place_suppression_updated",
            target=f"restaurant-place:{place.id}",
            metadata_json={"suppressed": payload.suppressed, "reason": payload.reason},
        )
    )
    await session.commit()
    return {"place_id": place.google_place_id, "suppressed": place.is_suppressed}
