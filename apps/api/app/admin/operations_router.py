from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.operations_schemas import AdminAuditItem, AdminAuditPage, AdminBootstrap
from app.admin.operations_service import admin_bootstrap, get_audit_log, list_audit_logs
from app.auth.service import AdminUser, require_capability
from app.db import get_session
from app.models import User
from app.problems import AppError

router = APIRouter(prefix="/admin", tags=["admin operations"])
Session = Annotated[AsyncSession, Depends(get_session)]
AuditReader = Annotated[User, Depends(require_capability("audit.read"))]


def _audit_boundary(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None or value.utcoffset() is None:
        raise AppError(
            422,
            "audit_timezone_required",
            "稽核日期範圍必須包含時區",
        )
    return value.astimezone(UTC)


@router.get("/bootstrap", response_model=AdminBootstrap)
async def get_admin_bootstrap(
    response: Response, user: AdminUser, session: Session
) -> AdminBootstrap:
    response.headers["Cache-Control"] = "no-store"
    return await admin_bootstrap(session, user)


@router.get("/audit", response_model=AdminAuditPage)
async def get_admin_audit(
    user: AuditReader,
    session: Session,
    response: Response,
    actor: Annotated[str | None, Query(max_length=320)] = None,
    action: Annotated[str | None, Query(max_length=64)] = None,
    target: Annotated[str | None, Query(max_length=128)] = None,
    result: Annotated[Literal["succeeded", "failed"] | None, Query()] = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> AdminAuditPage:
    del user
    response.headers["Cache-Control"] = "no-store"
    date_from = _audit_boundary(date_from)
    date_to = _audit_boundary(date_to)
    if date_from and date_to and date_from > date_to:
        raise AppError(422, "audit_date_range_invalid", "開始日期不可晚於結束日期")
    return await list_audit_logs(
        session,
        actor=actor,
        action=action,
        target=target,
        result=result,
        date_from=date_from,
        date_to=date_to,
        page=page,
        limit=limit,
    )


@router.get("/audit/{event_id}", response_model=AdminAuditItem)
async def get_admin_audit_event(
    event_id: UUID,
    user: AuditReader,
    session: Session,
    response: Response,
) -> AdminAuditItem:
    del user
    response.headers["Cache-Control"] = "no-store"
    return await get_audit_log(session, event_id)
