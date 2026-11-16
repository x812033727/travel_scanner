"""What the host's auto deploy timer last reported (migration 0146).

The admin deployment page shows the host timer (``ops/autodeploy``) through this single row:
the timer runs as root on the host, outside every container, and at the end of each tick it
upserts what it saw (live and target SHA, the CI result it read, its decision, its last deploy,
the paused file's first line) with ``psql`` in the postgres container. Nothing in the API writes
it. A row older than a few ticks means the timer is not running, and the page says so instead of
offering a button that nothing would pick up.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Boolean, CheckConstraint, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class DeploymentHostStatus(Base):
    __tablename__ = "deployment_host_status"
    __table_args__ = (CheckConstraint("id = 1", name="ck_deployment_host_status_single"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    reported_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    dry_run: Mapped[bool] = mapped_column(Boolean, default=False)
    live_sha: Mapped[str | None] = mapped_column(String(40), nullable=True)
    target_sha: Mapped[str | None] = mapped_column(String(40), nullable=True)
    target_commit_subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ci_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ci_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    paused_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    # last_decision, last_deploy, auto_deploys_today, last_missed_window, deploy_windows,
    # commits: the subset of the timer's state.json the page shows. Never a secret.
    state_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
