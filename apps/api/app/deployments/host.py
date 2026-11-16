"""The host timer executor: the admin button queues a run, the root timer on the host runs it.

``DEPLOYMENT_EXECUTOR=host_timer`` (docs/ops/admin-redeploy-button-and-daily-autodeploy-plan.md).
The API never touches Docker, git or the host. It inserts a ``queued`` ``deployment_runs`` row
with ``metadata_json.executor = "host_timer"``; the auto deploy timer (``ops/autodeploy``) claims
it on its next tick, walks the same gates as an automatic deploy (minus the schedule), runs
``/root/deploy-travel-scanner.sh`` and writes stages, events and the result back to the row. What
the timer saw on its last tick is in ``deployment_host_status``.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from pydantic import BaseModel, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.deployments.models import DeploymentHostStatus
from app.deployments.schemas import (
    CommitSummary,
    HostTimerDecision,
    HostTimerDeploy,
    HostTimerMissedWindow,
    HostTimerStatus,
    PreflightCheck,
)
from app.models import DeploymentRun

EXECUTOR = "host_timer"
# The timer ticks every five minutes; three missed ticks means it is not running.
RESPONDING_WITHIN = timedelta(minutes=15)
# A queued request nobody claimed in two ticks never will be: the timer is stopped or broken.
UNCLAIMED_AFTER = timedelta(minutes=10)


def is_host_run(run: DeploymentRun) -> bool:
    return (run.metadata_json or {}).get("executor") == EXECUTOR


def _aware(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return value if value.tzinfo else value.replace(tzinfo=UTC)


def unclaimed_too_long(run: DeploymentRun, now: datetime | None = None) -> bool:
    created = _aware(run.created_at)
    return bool(
        run.status == "queued"
        and created is not None
        and (now or datetime.now(UTC)) - created > UNCLAIMED_AFTER
    )


def _model[M: BaseModel](cls: type[M], raw: Any) -> M | None:
    if not isinstance(raw, dict):
        return None
    try:
        return cls.model_validate(raw)
    except ValidationError:
        return None


async def read_host_status(
    session: AsyncSession,
) -> tuple[DeploymentHostStatus | None, HostTimerStatus]:
    row = await session.get(DeploymentHostStatus, 1)
    if row is None:
        return None, HostTimerStatus()
    state = row.state_json if isinstance(row.state_json, dict) else {}
    reported = _aware(row.reported_at)
    today = state.get("auto_deploys_today")
    count = 0
    if isinstance(today, dict) and isinstance(today.get("count"), int):
        count = today["count"]
    windows = state.get("deploy_windows")
    last_deploy = state.get("last_deploy")
    if isinstance(last_deploy, dict) and isinstance(last_deploy.get("verify"), dict):
        last_deploy = {**last_deploy, "verify": last_deploy["verify"].get("result")}
    return row, HostTimerStatus(
        reported_at=reported,
        responding=bool(reported and datetime.now(UTC) - reported <= RESPONDING_WITHIN),
        dry_run=row.dry_run,
        paused_reason=row.paused_reason,
        deploy_windows=[str(w) for w in windows] if isinstance(windows, list) else [],
        auto_deploys_today=count,
        last_decision=_model(HostTimerDecision, state.get("last_decision")),
        last_deploy=_model(HostTimerDeploy, last_deploy),
        last_missed_window=_model(HostTimerMissedWindow, state.get("last_missed_window")),
    )


def host_commits(row: DeploymentHostStatus | None) -> list[CommitSummary]:
    raw = (row.state_json or {}).get("commits") if row else None
    if not isinstance(raw, list):
        return []
    commits = [_model(CommitSummary, item) for item in raw[:20]]
    return [commit for commit in commits if commit is not None]


def host_checks(status: HostTimerStatus) -> list[PreflightCheck]:
    checks = [
        PreflightCheck(
            name="host_timer",
            status="ok" if status.responding else "failed",
            detail=(
                "主機自動部署排程器正常回報"
                if status.responding
                else "主機自動部署排程器超過 15 分鐘沒有回報"
            ),
        ),
        PreflightCheck(
            name="autodeploy_paused",
            status="failed" if status.paused_reason else "ok",
            detail=status.paused_reason or "沒有自動部署暫停檔",
        ),
    ]
    if status.dry_run:
        checks.append(
            PreflightCheck(
                name="dry_run",
                status="warning",
                detail="排程器在乾跑模式（AUTODEPLOY_ENABLED=false），按下只會記錄會不會部署",
            )
        )
    return checks
