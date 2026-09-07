"""An administrator's override reaches the public payload and can be taken back.

Runs only with PostgreSQL and Redis (``RUN_INTEGRATION_TESTS=1``): the unit tests in
``test_ui_text.py`` stand in for the table, this one drives the real one through the
app, including the Redis cache that every write must clear.
"""

import os
from collections.abc import AsyncIterator
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.db import SessionFactory, engine
from app.infra import get_redis
from app.main import app
from app.models import User

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL and Redis services",
)


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    yield
    await engine.dispose()
    await get_redis().aclose()
    get_redis.cache_clear()


@pytest.mark.asyncio(loop_scope="module")
async def test_override_reaches_the_public_payload_and_restores_cleanly() -> None:
    suffix = uuid4()
    admin_email = f"ui-text-admin-{suffix}@example.com"
    # A key no reader uses: the web loader ignores overrides without a catalog default,
    # so the test cannot change what a real page shows even if it is left behind.
    key = f"integration-{suffix.hex[:12]}"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        registration = await client.post(
            "/api/v1/auth/register",
            json={"email": admin_email, "password": "integration-password-123"},
        )
        assert registration.status_code == 201
        headers = {"Authorization": f"Bearer {registration.json()['access_token']}"}
        async with SessionFactory() as session:
            admin = await session.get(User, UUID(registration.json()["user"]["id"]))
            assert admin is not None
            admin.is_admin = True
            await session.commit()

        before = await client.get("/api/v1/runtime/ui-text", params={"locale": "ja"})
        assert before.status_code == 200
        assert before.headers["cache-control"] == "no-store"
        assert f"common.{key}" not in before.json()["entries"]

        # A separate client: registering above put a travel_access cookie in this one's
        # jar, so the same client would reach the endpoint as the administrator.
        async with AsyncClient(transport=transport, base_url="http://test") as guest:
            anonymous = await guest.put(
                f"/api/v1/admin/ui-text/ja/common/{key}",
                json={"value": "テスト {count}", "default_value": "Test {count}"},
            )
        assert anonymous.status_code == 401

        rejected = await client.put(
            f"/api/v1/admin/ui-text/ja/common/{key}",
            json={"value": "テスト", "default_value": "Test {count}"},
            headers=headers,
        )
        assert rejected.status_code == 422
        assert rejected.json()["code"] == "ui_text_parameters_mismatch"

        written = await client.put(
            f"/api/v1/admin/ui-text/ja/common/{key}",
            json={"value": "テスト {count}", "default_value": "Test {count}"},
            headers=headers,
        )
        assert written.status_code == 200
        snapshot = written.json()
        entry = next(item for item in snapshot["entries"] if item["key"] == key)
        assert entry["value"] == "テスト {count}"
        assert entry["default_snapshot"] == "Test {count}"
        assert entry["updated_by_email"] == admin_email
        assert snapshot["namespace_counts"]["common"] >= 1
        assert snapshot["audit"][0]["action"] == "ui_text_updated"

        after = await client.get("/api/v1/runtime/ui-text", params={"locale": "ja"})
        assert after.json()["entries"][f"common.{key}"] == "テスト {count}"
        assert after.json()["version"] != before.json()["version"]

        other_locale = await client.get("/api/v1/runtime/ui-text", params={"locale": "en"})
        assert f"common.{key}" not in other_locale.json()["entries"]

        listed = await client.get(
            "/api/v1/admin/ui-text",
            params={"locale": "ja", "namespace": "common"},
            headers=headers,
        )
        assert listed.status_code == 200
        assert any(item["key"] == key for item in listed.json()["entries"])

        restored = await client.delete(f"/api/v1/admin/ui-text/ja/common/{key}", headers=headers)
        assert restored.status_code == 200
        assert not any(item["key"] == key for item in restored.json()["entries"])

        final = await client.get("/api/v1/runtime/ui-text", params={"locale": "ja"})
        assert f"common.{key}" not in final.json()["entries"]
        assert final.json()["version"] == before.json()["version"]

        missing = await client.delete(f"/api/v1/admin/ui-text/ja/common/{key}", headers=headers)
        assert missing.status_code == 404
        assert missing.json()["code"] == "ui_text_override_not_found"
