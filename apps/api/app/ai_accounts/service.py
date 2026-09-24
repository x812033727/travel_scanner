from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai_accounts.agent import AiAccountsAgentClient
from app.ai_accounts.schemas import (
    TERMINAL_LOGIN_STATUSES,
    AiAccountsOverview,
    AiLoginSession,
)
from app.config import Settings, get_settings
from app.models import AdminAuditLog, User
from app.problems import AppError

LOGIN_FINISHED_ACTIONS = tuple(
    f"ai_account.login_{status}" for status in sorted(TERMINAL_LOGIN_STATUSES)
)


def agent_client(settings: Settings | None = None) -> AiAccountsAgentClient:
    selected = settings or get_settings()
    if not selected.ai_accounts_configured:
        raise AppError(503, "ai_accounts_disabled", "AI 帳號管理尚未啟用")
    return AiAccountsAgentClient(selected)


async def overview(*, fresh: bool = False) -> AiAccountsOverview:
    settings = get_settings()
    if not settings.ai_accounts_configured:
        return AiAccountsOverview(enabled=False, agent_reachable=False)
    try:
        agent = await AiAccountsAgentClient(settings).overview(fresh=fresh)
    except AppError as exc:
        # The page still renders and says what is wrong instead of failing as a whole.
        return AiAccountsOverview(enabled=True, agent_reachable=False, agent_error=exc.detail)
    return AiAccountsOverview(
        enabled=True,
        agent_reachable=True,
        slots=agent.slots,
        defaults=agent.defaults,
        allowlist_configured=agent.allowlist_configured,
    )


async def audit(
    session: AsyncSession, actor: User, action: str, target: str, metadata: dict[str, Any]
) -> None:
    session.add(
        AdminAuditLog(actor_user_id=actor.id, action=action, target=target, metadata_json=metadata)
    )
    await session.commit()


async def audit_login_outcome(
    session: AsyncSession, actor: User, login: AiLoginSession
) -> None:
    """Record how a login ended, once, the first time a poll sees it finished.

    Only the agent knows when a login ends, and the page learns it by polling, so the
    first poll that sees the end writes the row and the ones after it find that row.
    """
    if login.status not in TERMINAL_LOGIN_STATUSES:
        return
    target = f"ai-login:{login.id}"
    recorded = await session.scalar(
        select(AdminAuditLog.id)
        .where(AdminAuditLog.target == target, AdminAuditLog.action.in_(LOGIN_FINISHED_ACTIONS))
        .limit(1)
    )
    if recorded is not None:
        return
    metadata: dict[str, Any] = {"tool": login.tool, "slot": login.slot, "status": login.status}
    if login.error:
        metadata["error"] = login.error
    await audit(session, actor, f"ai_account.login_{login.status}", target, metadata)
