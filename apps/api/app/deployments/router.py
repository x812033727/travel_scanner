from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import DeployAdminUser
from app.db import get_session
from app.deployments.schemas import (
    DeploymentCreateRequest,
    DeploymentOverview,
    DeploymentPreflightResult,
    DeploymentRunList,
    DeploymentRunView,
)
from app.deployments.service import (
    create_deployment,
    deployment_detail,
    deployment_overview,
    list_deployments,
    preflight_deployment,
)
from app.infra import client_ip, enforce_named_rate_limit

router = APIRouter(prefix="/admin/deployments", tags=["admin deployments"])
Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("/overview", response_model=DeploymentOverview)
async def get_deployment_overview(user: DeployAdminUser, session: Session) -> DeploymentOverview:
    _ = user
    return await deployment_overview(session)


@router.post("/preflight", response_model=DeploymentPreflightResult)
async def post_deployment_preflight(
    user: DeployAdminUser,
) -> DeploymentPreflightResult:
    _ = user
    return await preflight_deployment()


@router.post("", response_model=DeploymentRunView, status_code=status.HTTP_202_ACCEPTED)
async def post_deployment(
    payload: DeploymentCreateRequest,
    user: DeployAdminUser,
    session: Session,
    request: Request,
    idempotency_key: Annotated[
        str,
        Header(alias="Idempotency-Key", min_length=8, max_length=120),
    ],
) -> DeploymentRunView:
    await enforce_named_rate_limit(
        "deployment-reauth",
        f"{user.id}:{client_ip(request)}",
        limit=5,
        window_seconds=3_600,
    )
    return await create_deployment(session, user, payload, idempotency_key)


@router.get("", response_model=DeploymentRunList)
async def get_deployments(
    user: DeployAdminUser,
    session: Session,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> DeploymentRunList:
    _ = user
    return await list_deployments(session, limit)


@router.get("/{run_id}", response_model=DeploymentRunView)
async def get_deployment(
    run_id: UUID, user: DeployAdminUser, session: Session
) -> DeploymentRunView:
    _ = user
    return await deployment_detail(session, run_id)
