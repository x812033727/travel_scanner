from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import (
    effective_admin_roles,
    require_admin_step_up,
    require_capability,
)
from app.config import get_settings
from app.database_admin.schemas import (
    DatabaseBackupRequest,
    DatabaseMaintenanceRequest,
    DatabaseOperationList,
    DatabaseOperationView,
    DatabaseOverview,
    DatabaseTableList,
)
from app.database_admin.service import (
    create_database_operation,
    database_operation_detail,
    database_overview,
    database_tables,
    list_database_operations,
)
from app.db import get_session
from app.infra import client_ip, enforce_named_rate_limit
from app.models import User
from app.problems import AppError

router = APIRouter(prefix="/admin/database", tags=["admin database"])
Session = Annotated[AsyncSession, Depends(get_session)]
DatabaseReader = Annotated[User, Depends(require_capability("database.read"))]
DatabaseMaintainer = Annotated[User, Depends(require_capability("database.maintain"))]
IdempotencyKey = Annotated[
    str,
    Header(alias="Idempotency-Key", min_length=8, max_length=255),
]


def _no_store(response: Response) -> None:
    response.headers["Cache-Control"] = "no-store"


async def _authorize_maintenance(
    session: AsyncSession,
    request: Request,
    user: User,
    scope: str,
) -> None:
    if not get_settings().admin_database_maintenance_enabled:
        raise AppError(503, "database_maintenance_disabled", "資料庫維護功能目前未啟用")
    roles = await effective_admin_roles(session, user)
    settings = get_settings()
    if user.email.lower() not in settings.database_admin_email_set or not (
        {"owner", "database_operator"} & roles
    ):
        raise AppError(
            403,
            "database_operator_required",
            "資料庫維護需要 database_operator 角色與主機 allowlist",
        )
    await require_admin_step_up(request, user, scope)


@router.get("/overview", response_model=DatabaseOverview)
async def get_database_overview(
    response: Response, user: DatabaseReader, session: Session
) -> DatabaseOverview:
    del user
    _no_store(response)
    return await database_overview(session)


@router.get("/tables", response_model=DatabaseTableList)
async def get_database_tables(
    response: Response, user: DatabaseReader, session: Session
) -> DatabaseTableList:
    del user
    _no_store(response)
    return await database_tables(session)


@router.get("/backups", response_model=DatabaseOperationList)
async def get_database_backups(
    response: Response,
    user: DatabaseReader,
    session: Session,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> DatabaseOperationList:
    del user
    _no_store(response)
    return await list_database_operations(session, operation_type="backup", limit=limit)


@router.post(
    "/backups",
    response_model=DatabaseOperationView,
    status_code=status.HTTP_202_ACCEPTED,
)
async def post_database_backup(
    payload: DatabaseBackupRequest,
    response: Response,
    user: DatabaseMaintainer,
    session: Session,
    request: Request,
    idempotency_key: IdempotencyKey,
) -> DatabaseOperationView:
    _no_store(response)
    await _authorize_maintenance(session, request, user, "database.backup")
    await enforce_named_rate_limit(
        "admin-database-operation",
        f"{user.id}:{client_ip(request)}",
        limit=10,
        window_seconds=3_600,
    )
    return await create_database_operation(
        session, user, "backup", payload.confirmation, idempotency_key
    )


@router.post(
    "/maintenance",
    response_model=DatabaseOperationView,
    status_code=status.HTTP_202_ACCEPTED,
)
async def post_database_maintenance(
    payload: DatabaseMaintenanceRequest,
    response: Response,
    user: DatabaseMaintainer,
    session: Session,
    request: Request,
    idempotency_key: IdempotencyKey,
) -> DatabaseOperationView:
    _no_store(response)
    await _authorize_maintenance(session, request, user, "database.analyze")
    await enforce_named_rate_limit(
        "admin-database-operation",
        f"{user.id}:{client_ip(request)}",
        limit=10,
        window_seconds=3_600,
    )
    return await create_database_operation(
        session, user, payload.action, payload.confirmation, idempotency_key
    )


@router.get("/operations/{operation_id}", response_model=DatabaseOperationView)
async def get_database_operation(
    operation_id: UUID,
    response: Response,
    user: DatabaseReader,
    session: Session,
) -> DatabaseOperationView:
    del user
    _no_store(response)
    return await database_operation_detail(session, operation_id)
