import os
from collections.abc import AsyncIterator
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.config import get_settings
from app.db import SessionFactory, engine
from app.deployments.agent import DeploymentAgentClient
from app.deployments.schemas import AgentCreateResponse, AgentOverview, CommitSummary
from app.infra import get_redis
from app.main import app
from app.models import AdminAuditLog, DeploymentRun, User

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL and Redis services",
)


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_clients() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    get_redis.cache_clear()
    yield
    await engine.dispose()
    await get_redis().aclose()
    get_redis.cache_clear()


@pytest.mark.asyncio(loop_scope="module")
async def test_deployment_requires_allowlist_reauth_confirmation_and_is_idempotent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    email = f"deploy-admin-{uuid4().hex}@example.com"
    password = "integration-password-123"
    target = "b" * 40
    settings = get_settings()
    originals = (
        settings.deployments_enabled,
        settings.deploy_admin_emails,
        settings.deploy_agent_hmac_key,
    )
    settings.deployments_enabled = True
    settings.deploy_admin_emails = email
    settings.deploy_agent_hmac_key = "x" * 32
    overview_mock = AsyncMock(
        return_value=AgentOverview(
            deployed_sha="a" * 40,
            target_sha=target,
            target_commit_subject="Green deployment",
            ci_status="success",
            ci_url="https://github.com/x812033727/travel_scanner/actions/runs/1",
            commits=[CommitSummary(sha=target, subject="Green deployment")],
        )
    )
    create_mock = AsyncMock(
        return_value=AgentCreateResponse(job_id=str(uuid4()), status="preflight")
    )
    monkeypatch.setattr(DeploymentAgentClient, "overview", overview_mock)
    monkeypatch.setattr(DeploymentAgentClient, "create", create_mock)
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            registration = await client.post(
                "/api/v1/auth/register",
                json={"email": email, "password": password},
            )
            assert registration.status_code == 201
            user_id = UUID(registration.json()["user"]["id"])
            headers = {"Authorization": f"Bearer {registration.json()['access_token']}"}
            async with SessionFactory() as session:
                user = await session.get(User, user_id)
                assert user is not None
                user.is_admin = True
                await session.commit()

            me = await client.get("/api/v1/auth/me", headers=headers)
            assert me.status_code == 200
            assert me.json()["can_deploy"] is True

            overview = await client.get(
                "/api/v1/admin/deployments/overview", headers=headers
            )
            assert overview.status_code == 200
            assert overview.json()["target_sha"] == target

            wrong_password = await client.post(
                "/api/v1/admin/deployments",
                headers={**headers, "Idempotency-Key": f"deploy-{uuid4()}"},
                json={
                    "expected_target_sha": target,
                    "password": "wrong",
                    "confirmation": "DEPLOY bbbbbbb",
                },
            )
            assert wrong_password.status_code == 401
            assert wrong_password.json()["code"] == "deployment_reauth_failed"

            key = f"deploy-{uuid4()}"
            payload = {
                "expected_target_sha": target,
                "password": password,
                "confirmation": "DEPLOY bbbbbbb",
            }
            created = await client.post(
                "/api/v1/admin/deployments",
                headers={**headers, "Idempotency-Key": key},
                json=payload,
            )
            assert created.status_code == 202
            assert created.json()["status"] == "preflight"
            replay = await client.post(
                "/api/v1/admin/deployments",
                headers={**headers, "Idempotency-Key": key},
                json=payload,
            )
            assert replay.status_code == 202
            assert replay.json()["id"] == created.json()["id"]
            create_mock.assert_awaited_once()

            async with SessionFactory() as session:
                audit = await session.scalar(
                    select(AdminAuditLog)
                    .where(AdminAuditLog.action == "deployment.requested")
                    .order_by(AdminAuditLog.created_at.desc())
                )
                assert audit is not None
                assert password not in str(audit.metadata_json)
                run = await session.get(DeploymentRun, UUID(created.json()["id"]))
                assert run is not None
                run.status = "succeeded"
                await session.commit()
    finally:
        (
            settings.deployments_enabled,
            settings.deploy_admin_emails,
            settings.deploy_agent_hmac_key,
        ) = originals
