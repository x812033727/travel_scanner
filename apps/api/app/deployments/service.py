from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import verify_password
from app.config import get_settings
from app.deployments.agent import DeploymentAgentClient
from app.deployments.schemas import (
    AgentOverview,
    DeploymentCreateRequest,
    DeploymentEventView,
    DeploymentOverview,
    DeploymentPreflightResult,
    DeploymentRunList,
    DeploymentRunView,
)
from app.models import (
    ACTIVE_DEPLOYMENT_STATUSES,
    AdminAuditLog,
    DeploymentEvent,
    DeploymentRun,
    User,
)
from app.problems import AppError


def _safe_text(value: str | None, limit: int = 500) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(value.replace("\x00", "").split())
    return cleaned[:limit] or None


async def _view(
    session: AsyncSession,
    run: DeploymentRun,
    *,
    include_events: bool = False,
) -> DeploymentRunView:
    requester = (
        await session.get(User, run.requested_by_user_id)
        if run.requested_by_user_id
        else None
    )
    events: list[DeploymentEventView] = []
    if include_events:
        rows = list(
            (
                await session.scalars(
                    select(DeploymentEvent)
                    .where(DeploymentEvent.run_id == run.id)
                    .order_by(DeploymentEvent.sequence)
                )
            ).all()
        )
        events = [
            DeploymentEventView(
                sequence=row.sequence,
                stage=row.stage,
                status=row.status,
                message=row.message,
                created_at=row.created_at,
            )
            for row in rows
        ]
    return DeploymentRunView(
        id=run.id,
        requested_by_email=requester.email if requester else None,
        agent_job_id=run.agent_job_id,
        status=run.status,
        stage=run.stage,
        previous_sha=run.previous_sha,
        target_sha=run.target_sha,
        target_commit_subject=run.target_commit_subject,
        ci_url=run.ci_url,
        backup_name=run.backup_name,
        rollback_status=run.rollback_status,
        failure_code=run.failure_code,
        failure_detail=run.failure_detail,
        started_at=run.started_at,
        finished_at=run.finished_at,
        created_at=run.created_at,
        updated_at=run.updated_at,
        events=events,
    )


async def _reconcile(session: AsyncSession, run: DeploymentRun) -> DeploymentRun:
    if not run.agent_job_id or run.status not in ACTIVE_DEPLOYMENT_STATUSES:
        return run
    try:
        job = await DeploymentAgentClient().job(run.agent_job_id)
    except AppError as exc:
        if exc.code != "deployment_not_found":
            raise
        run.status = "failed"
        run.failure_code = "deployment_agent_lost_job"
        run.failure_detail = "部署代理恢復連線後找不到這筆工作"
        run.finished_at = datetime.now(UTC)
        run.metadata_json = {**(run.metadata_json or {}), "terminal_audited": True}
        session.add(
            AdminAuditLog(
                actor_user_id=run.requested_by_user_id,
                action="deployment.failed",
                target=str(run.id),
                metadata_json={
                    "run_id": str(run.id),
                    "target_sha": run.target_sha,
                    "status": "failed",
                },
            )
        )
        await session.commit()
        return run
    previous_status = run.status
    run.status = job.status
    run.stage = job.stage
    run.previous_sha = job.previous_sha
    run.target_commit_subject = _safe_text(job.target_commit_subject, 255)
    run.ci_url = job.ci_url
    run.backup_name = _safe_text(job.backup_name, 255)
    run.rollback_status = job.rollback_status
    run.failure_code = _safe_text(job.failure_code, 64)
    run.failure_detail = _safe_text(job.failure_detail)
    run.started_at = job.started_at
    run.finished_at = job.finished_at
    known_sequences = set(
        (
            await session.scalars(
                select(DeploymentEvent.sequence).where(DeploymentEvent.run_id == run.id)
            )
        ).all()
    )
    for event in job.events:
        if event.sequence in known_sequences:
            continue
        session.add(
            DeploymentEvent(
                run_id=run.id,
                sequence=event.sequence,
                stage=event.stage[:32],
                status=event.status[:32],
                message=_safe_text(event.message) or "狀態已更新",
                created_at=event.created_at,
            )
        )
    terminal = run.status not in ACTIVE_DEPLOYMENT_STATUSES
    metadata = dict(run.metadata_json or {})
    if terminal and not metadata.get("terminal_audited"):
        metadata["terminal_audited"] = True
        run.metadata_json = metadata
        action = {
            "succeeded": "deployment.succeeded",
            "rolled_back": "deployment.rolled_back",
        }.get(run.status, "deployment.failed")
        duration = None
        if run.started_at and run.finished_at:
            duration = max(0, int((run.finished_at - run.started_at).total_seconds()))
        session.add(
            AdminAuditLog(
                actor_user_id=run.requested_by_user_id,
                action=action,
                target=str(run.id),
                metadata_json={
                    "run_id": str(run.id),
                    "target_sha": run.target_sha,
                    "status": run.status,
                    "duration_seconds": duration,
                },
            )
        )
    if previous_status != run.status or job.events:
        await session.commit()
    return run


async def deployment_overview(session: AsyncSession) -> DeploymentOverview:
    agent_connected = True
    active = await session.scalar(
        select(DeploymentRun)
        .where(DeploymentRun.status.in_(ACTIVE_DEPLOYMENT_STATUSES))
        .order_by(DeploymentRun.created_at.desc())
    )
    if active is not None:
        try:
            active = await _reconcile(session, active)
            if active.status not in ACTIVE_DEPLOYMENT_STATUSES:
                active = None
        except AppError as exc:
            if exc.code != "deployment_agent_unavailable":
                raise
            agent_connected = False
    latest_success = await session.scalar(
        select(DeploymentRun)
        .where(DeploymentRun.status == "succeeded")
        .order_by(DeploymentRun.finished_at.desc())
        .limit(1)
    )
    try:
        agent = await DeploymentAgentClient().overview()
    except AppError as exc:
        if exc.code != "deployment_agent_unavailable":
            raise
        agent_connected = False
        agent = AgentOverview(connected=False)
    cooldown_until = None
    latest_terminal = await session.scalar(
        select(DeploymentRun)
        .where(~DeploymentRun.status.in_(ACTIVE_DEPLOYMENT_STATUSES))
        .order_by(DeploymentRun.finished_at.desc())
        .limit(1)
    )
    if latest_terminal and latest_terminal.finished_at:
        cooldown_until = latest_terminal.finished_at + timedelta(
            seconds=get_settings().deploy_cooldown_seconds
        )
        if cooldown_until <= datetime.now(UTC):
            cooldown_until = None
    return DeploymentOverview(
        enabled=get_settings().deployments_configured,
        agent_connected=agent_connected and agent.connected,
        deployed_sha=agent.deployed_sha,
        target_sha=agent.target_sha,
        target_commit_subject=agent.target_commit_subject,
        update_available=bool(
            agent.target_sha
            and agent.ci_status == "success"
            and agent.target_sha != agent.deployed_sha
        ),
        ci_status=agent.ci_status,
        ci_url=agent.ci_url,
        commits=agent.commits,
        checks=agent.checks,
        active_run=await _view(session, active, include_events=True) if active else None,
        last_success=await _view(session, latest_success) if latest_success else None,
        cooldown_until=cooldown_until,
    )


async def preflight_deployment() -> DeploymentPreflightResult:
    return await DeploymentAgentClient().preflight()


async def create_deployment(
    session: AsyncSession,
    actor: User,
    payload: DeploymentCreateRequest,
    idempotency_key: str,
) -> DeploymentRunView:
    replay = await session.scalar(
        select(DeploymentRun).where(
            DeploymentRun.requested_by_user_id == actor.id,
            DeploymentRun.idempotency_key == idempotency_key,
        )
    )
    if replay is not None:
        return await _view(session, replay, include_events=True)
    if not actor.password_hash or not verify_password(payload.password, actor.password_hash):
        raise AppError(401, "deployment_reauth_failed", "目前密碼不正確")
    overview = await deployment_overview(session)
    if overview.active_run is not None:
        raise AppError(409, "deployment_in_progress", "目前已有部署正在執行")
    if overview.cooldown_until is not None:
        raise AppError(429, "deployment_cooldown", "前一次部署剛完成，請稍候五分鐘")
    if not overview.agent_connected or not overview.target_sha:
        raise AppError(503, "deployment_agent_unavailable", "部署代理目前無法取得版本資訊")
    if overview.ci_status != "success":
        raise AppError(409, "deployment_ci_not_green", "最新 main 尚未通過 CI")
    if overview.target_sha != payload.expected_target_sha:
        raise AppError(409, "deployment_target_changed", "main 已更新，請重新檢查後再部署")
    if overview.target_sha == overview.deployed_sha:
        raise AppError(409, "deployment_already_current", "目前已是最新綠燈版本")
    if payload.confirmation != f"DEPLOY {overview.target_sha[:7]}":
        raise AppError(422, "deployment_confirmation_invalid", "部署確認文字不正確")
    run = DeploymentRun(
        id=uuid4(),
        requested_by_user_id=actor.id,
        idempotency_key=idempotency_key,
        status="queued",
        stage="queued",
        previous_sha=overview.deployed_sha,
        target_sha=overview.target_sha,
        target_commit_subject=_safe_text(overview.target_commit_subject, 255),
        ci_url=overview.ci_url,
        metadata_json={},
    )
    run.agent_job_id = str(run.id)
    session.add(run)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="deployment.requested",
            target=str(run.id),
            metadata_json={"run_id": str(run.id), "target_sha": overview.target_sha},
        )
    )
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        concurrent_replay = await session.scalar(
            select(DeploymentRun).where(
                DeploymentRun.requested_by_user_id == actor.id,
                DeploymentRun.idempotency_key == idempotency_key,
            )
        )
        if concurrent_replay is not None:
            return await _view(session, concurrent_replay, include_events=True)
        raise AppError(409, "deployment_in_progress", "目前已有部署正在執行") from exc
    try:
        created = await DeploymentAgentClient().create(str(run.id), run.target_sha)
    except AppError as exc:
        if exc.code == "deployment_agent_unavailable":
            run.failure_code = "deployment_agent_ack_pending"
            run.failure_detail = "尚未收到部署代理確認；恢復連線後會自動同步"
            await session.commit()
            raise
        run.status = "failed"
        run.stage = "queued"
        run.failure_code = exc.code
        run.failure_detail = _safe_text(exc.detail)
        run.finished_at = datetime.now(UTC)
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action="deployment.failed",
                target=str(run.id),
                metadata_json={
                    "run_id": str(run.id),
                    "target_sha": run.target_sha,
                    "status": "failed",
                },
            )
        )
        await session.commit()
        raise
    if created.job_id != str(run.id):
        raise AppError(502, "deployment_agent_invalid_response", "部署代理工作識別碼不正確")
    run.status = created.status
    await session.commit()
    return await _view(session, run, include_events=True)


async def list_deployments(session: AsyncSession, limit: int) -> DeploymentRunList:
    runs = list(
        (
            await session.scalars(
                select(DeploymentRun).order_by(DeploymentRun.created_at.desc()).limit(limit)
            )
        ).all()
    )
    return DeploymentRunList(items=[await _view(session, run) for run in runs])


async def deployment_detail(session: AsyncSession, run_id: UUID) -> DeploymentRunView:
    run = await session.get(DeploymentRun, run_id)
    if run is None:
        raise AppError(404, "deployment_not_found", "找不到這筆部署紀錄")
    try:
        run = await _reconcile(session, run)
    except AppError as exc:
        if exc.code != "deployment_agent_unavailable":
            raise
    return await _view(session, run, include_events=True)
