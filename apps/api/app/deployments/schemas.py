from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

DeploymentStatus = Literal[
    "queued",
    "preflight",
    "building",
    "backing_up",
    "migrating",
    "activating",
    "verifying",
    "rolling_back",
    "succeeded",
    "failed",
    "rolled_back",
    "manual_intervention_required",
]


class DeploymentEventView(BaseModel):
    sequence: int
    stage: str
    status: str
    message: str
    created_at: datetime


class DeploymentRunView(BaseModel):
    id: UUID
    requested_by_email: str | None = None
    agent_job_id: str | None = None
    status: DeploymentStatus
    stage: str
    previous_sha: str | None = None
    target_sha: str
    target_commit_subject: str | None = None
    ci_url: str | None = None
    backup_name: str | None = None
    rollback_status: str | None = None
    failure_code: str | None = None
    failure_detail: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    events: list[DeploymentEventView] = Field(default_factory=list)


class CommitSummary(BaseModel):
    sha: str
    subject: str


class PreflightCheck(BaseModel):
    name: str
    status: Literal["ok", "warning", "failed"]
    detail: str


class AgentOverview(BaseModel):
    connected: bool = True
    deployed_sha: str | None = None
    target_sha: str | None = None
    target_commit_subject: str | None = None
    ci_status: str = "unknown"
    ci_url: str | None = None
    commits: list[CommitSummary] = Field(default_factory=list)
    checks: list[PreflightCheck] = Field(default_factory=list)


class AgentDeploymentEvent(BaseModel):
    sequence: int
    stage: str
    status: str
    message: str
    created_at: datetime


class AgentDeploymentJob(BaseModel):
    job_id: str
    status: DeploymentStatus
    stage: str
    previous_sha: str | None = None
    target_sha: str
    target_commit_subject: str | None = None
    ci_url: str | None = None
    backup_name: str | None = None
    rollback_status: str | None = None
    failure_code: str | None = None
    failure_detail: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    events: list[AgentDeploymentEvent] = Field(default_factory=list)


class HostTimerDecision(BaseModel):
    action: str | None = None
    gate: str | None = None
    reason: str | None = None
    sha: str | None = None


class HostTimerDeploy(BaseModel):
    sha: str | None = None
    finished_at: datetime | None = None
    seconds: int | None = None
    exit: int | None = None
    verify: str | None = None


class HostTimerMissedWindow(BaseModel):
    window: str | None = None
    gate: str | None = None
    reason: str | None = None
    sha: str | None = None
    notified_at: datetime | None = None


class HostTimerStatus(BaseModel):
    """What the root auto deploy timer on the host last reported (deployment_host_status)."""

    reported_at: datetime | None = None
    responding: bool = False
    dry_run: bool = False
    paused_reason: str | None = None
    deploy_windows: list[str] = Field(default_factory=list)
    auto_deploys_today: int = 0
    last_decision: HostTimerDecision | None = None
    last_deploy: HostTimerDeploy | None = None
    last_missed_window: HostTimerMissedWindow | None = None


class DeploymentOverview(BaseModel):
    enabled: bool
    executor: Literal["host_timer", "agent"] = "agent"
    agent_connected: bool
    deployed_sha: str | None = None
    target_sha: str | None = None
    target_commit_subject: str | None = None
    update_available: bool = False
    ci_status: str = "unknown"
    ci_url: str | None = None
    commits: list[CommitSummary] = Field(default_factory=list)
    checks: list[PreflightCheck] = Field(default_factory=list)
    active_run: DeploymentRunView | None = None
    last_success: DeploymentRunView | None = None
    cooldown_until: datetime | None = None
    host: HostTimerStatus | None = None


class DeploymentCreateRequest(BaseModel):
    expected_target_sha: str = Field(min_length=40, max_length=40, pattern=r"^[0-9a-f]{40}$")
    password: str = Field(min_length=1, max_length=128)
    confirmation: str = Field(min_length=1, max_length=32)
    # host_timer only: "latest" deploys the newest green main, "rebuild" rebuilds the live
    # commit (the deploy script's --force) and so needs no new CI result.
    mode: Literal["latest", "rebuild"] = "latest"
    wait_for_paid_work: bool = True

    @field_validator("expected_target_sha")
    @classmethod
    def normalize_sha(cls, value: str) -> str:
        return value.lower()


class DeploymentPreflightResult(BaseModel):
    ok: bool
    checked_at: datetime
    checks: list[PreflightCheck]
    target_sha: str | None = None


class DeploymentRunList(BaseModel):
    items: list[DeploymentRunView]


class AgentCreateRequest(BaseModel):
    run_id: UUID
    target_sha: str


class AgentCreateResponse(BaseModel):
    job_id: str
    status: DeploymentStatus
