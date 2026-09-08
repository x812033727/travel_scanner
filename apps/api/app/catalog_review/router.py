from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import AdminUser
from app.catalog_review.scope import SCOPE_KINDS, CatalogScope, request_scope
from app.catalog_review.service import (
    ApplyRequest,
    StartRequest,
    apply_decisions,
    create_run,
    get_run,
    item_view,
    overview,
    prepare_resume,
    run_view,
)
from app.db import get_session
from app.infra import enforce_named_rate_limit
from app.models import CatalogReviewItem, CatalogReviewRun

router = APIRouter(prefix="/admin/catalog-review", tags=["admin catalog review"])
Session = Annotated[AsyncSession, Depends(get_session)]
IdempotencyKey = Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=128)]


async def enqueue_saved_run(session: AsyncSession, run: CatalogReviewRun) -> None:
    from app.catalog_review.jobs import enqueue_catalog_run

    try:
        enqueue_catalog_run(run.id)
    except Exception:
        # Keep the committed snapshot resumable if Redis/RQ is unavailable.
        run.status = "failed"
        run.error_code = "catalog_queue_unavailable"
        run.error_message = "工作已保存，但目前無法排入佇列，請稍後續跑"
        await session.commit()


@router.get("")
async def catalog_overview(
    user: AdminUser, session: Session, scope: CatalogScope | None = None
) -> dict[str, Any]:
    return await overview(session, await load_runtime_settings(session), scope)


@router.post("/runs", status_code=202)
async def start_catalog_run(
    payload: StartRequest, user: AdminUser, session: Session, idempotency_key: IdempotencyKey
) -> dict[str, Any]:
    await enforce_named_rate_limit("catalog-start", str(user.id), limit=6, window_seconds=3600)
    run, created = await create_run(
        session, await load_runtime_settings(session), user.id, payload, idempotency_key
    )
    if created:
        await enqueue_saved_run(session, run)
    return await run_view(session, run)


@router.get("/runs/{run_id}")
async def read_catalog_run(
    run_id: UUID, user: AdminUser, session: Session, scope: CatalogScope | None = None
) -> dict[str, Any]:
    return await run_view(session, await get_run(session, run_id, scope=scope))


@router.get("/runs/{run_id}/items")
async def catalog_items(
    run_id: UUID,
    user: AdminUser,
    session: Session,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=30, ge=1, le=100),
    scope: CatalogScope | None = None,
) -> dict[str, Any]:
    run = await get_run(session, run_id, scope=scope)
    kinds = SCOPE_KINDS[request_scope(run.request_json)]
    total = int(
        await session.scalar(
            select(func.count())
            .select_from(CatalogReviewItem)
            .where(CatalogReviewItem.run_id == run_id, CatalogReviewItem.kind.in_(kinds))
        )
        or 0
    )
    rows = (
        await session.scalars(
            select(CatalogReviewItem)
            .where(CatalogReviewItem.run_id == run_id, CatalogReviewItem.kind.in_(kinds))
            .order_by(CatalogReviewItem.created_at, CatalogReviewItem.id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).all()
    return {
        "items": [item_view(item) for item in rows],
        "total": total,
        "page": page,
        "page_size": page_size,
        "has_more": page * page_size < total,
    }


@router.post("/runs/{run_id}/resume", status_code=202)
async def resume_catalog_run(
    run_id: UUID, user: AdminUser, session: Session, scope: CatalogScope | None = None
) -> dict[str, Any]:
    await enforce_named_rate_limit("catalog-resume", str(user.id), limit=6, window_seconds=3600)
    run = await prepare_resume(session, run_id, user.id, scope=scope)
    await enqueue_saved_run(session, run)
    return await run_view(session, run)


@router.post("/runs/{run_id}/apply")
async def apply_catalog_run(
    run_id: UUID,
    payload: ApplyRequest,
    user: AdminUser,
    session: Session,
    idempotency_key: IdempotencyKey,
    scope: CatalogScope | None = None,
) -> dict[str, Any]:
    return await apply_decisions(session, run_id, user.id, payload, idempotency_key, scope=scope)
