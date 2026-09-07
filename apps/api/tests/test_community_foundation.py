"""Always-on SQLite contract tests; the same metadata also runs through PostgreSQL CI."""

from __future__ import annotations

import hashlib
import io
import os
import runpy
from collections.abc import AsyncIterator
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Annotated, Any
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from fastapi import Depends, Header
from httpx import ASGITransport, AsyncClient, Response
from PIL import Image
from sqlalchemy import event, func, inspect, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import current_user, optional_current_user
from app.community.content import itinerary_snapshot
from app.community.media import clean_image
from app.community.models import (
    AccountToken,
    Fork,
    Media,
    Message,
    Notification,
    Profile,
    TranslationBudget,
)
from app.community.pet_models import PetPlace
from app.community.pet_schemas import PetRequirements, PetRule
from app.community.pets import eligibility
from app.community.policy import fail
from app.db import Base, get_session
from app.main import app
from app.models import AdminAuditLog, ProviderConfig, TripPlan, TripPlanItem, User


class Harness:
    def __init__(
        self, factory: async_sessionmaker[AsyncSession], client: AsyncClient, ids: list[UUID]
    ):
        self.factory, self.client, self.ids = factory, client, ids

    async def call(
        self, method: str, path: str, *, actor: int | None = 0, expected: int = 200, **kwargs: Any
    ) -> Response:
        headers = {"x-test-user": str(self.ids[actor])} if actor is not None else {}
        response = await self.client.request(method, "/api/v1" + path, headers=headers, **kwargs)
        assert response.status_code == expected, response.text
        return response

    async def post(self, *, actor: int = 0, **fields: Any) -> dict[str, Any]:
        response = await self.call(
            "POST",
            "/community/posts",
            actor=actor,
            expected=201,
            json={
                "title": "Tokyo trip",
                "body": "Original experience",
                "destination": "Tokyo",
                **fields,
            },
        )
        return response.json()

    async def publish(self, post: dict[str, Any], actor: int = 0) -> dict[str, Any]:
        return (
            await self.call(
                "POST",
                f"/community/posts/{post['id']}/publish",
                actor=actor,
                json={"version": post["version"]},
            )
        ).json()

    async def approve(self, post: dict[str, Any]) -> dict[str, Any]:
        return (
            await self.call(
                "PUT",
                f"/admin/community/posts/{post['id']}",
                actor=2,
                json={"version": post["version"], "action": "approve", "reason": "Source checked"},
            )
        ).json()


@pytest_asyncio.fixture(
    params=["sqlite"] + (["postgresql"] if os.getenv("RUN_INTEGRATION_TESTS") == "1" else [])
)
async def harness(
    monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest
) -> AsyncIterator[Harness]:
    schema = "community_test_" + uuid4().hex
    administrator = None
    if request.param == "postgresql":
        from app.config import get_settings

        administrator = create_async_engine(get_settings().database_url)
        async with administrator.begin() as connection:
            await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
        engine = create_async_engine(
            get_settings().database_url, connect_args={"server_settings": {"search_path": schema}}
        )
    else:
        engine = create_async_engine("sqlite+aiosqlite://")

        @event.listens_for(engine.sync_engine, "connect")
        def sqlite_functions(connection: Any, _: Any) -> None:
            connection.create_function(
                "btrim", 1, lambda value: value.strip() if value is not None else None
            )
            connection.execute("PRAGMA foreign_keys=ON")

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    ids = [uuid4() for _ in range(4)]
    async with factory() as session:
        for index, identifier in enumerate(ids):
            session.add(
                User(
                    id=identifier,
                    email=f"private-{index}@example.com",
                    is_admin=index == 2,
                    email_verified_at=datetime.now(UTC) if index != 3 else None,
                )
            )
            await session.flush()
            session.add(
                Profile(
                    user_id=identifier, handle=f"traveler_{index}", display_name=f"Traveler {index}"
                )
            )
        session.add(ProviderConfig(provider="community", config={"enabled": True}))
        await session.commit()

    async def database() -> AsyncIterator[AsyncSession]:
        async with factory() as session:
            yield session

    async def optional(
        session: Annotated[AsyncSession, Depends(get_session)],
        x_test_user: Annotated[str | None, Header()] = None,
    ) -> User | None:
        if x_test_user is None:
            return None
        user = await session.get(User, UUID(x_test_user))
        if user is None or not user.is_active:
            raise fail("invalid_user", 401)
        return user

    required_dependency = Depends(optional)

    async def required(user: User | None = required_dependency) -> User:
        if user is None:
            raise fail("authentication_required", 401)
        return user

    monkeypatch.setattr("app.community.policy.enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr("app.community.accounts.enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr("app.community.jobs.enqueue_jobs", lambda: False)
    for module in ("app.community.router", "app.community.messaging", "app.community.admin"):
        monkeypatch.setattr(module + ".signal", AsyncMock())
    app.dependency_overrides[get_session] = database
    app.dependency_overrides[current_user] = required
    app.dependency_overrides[optional_current_user] = optional
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield Harness(factory, client, ids)
    finally:
        app.dependency_overrides.clear()
        await engine.dispose()
        if administrator is not None:
            # Only the randomly named schema created by this fixture is removed.
            assert schema.startswith("community_test_") and len(schema) == 47
            async with administrator.begin() as connection:
                await connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
            await administrator.dispose()


@pytest.mark.asyncio
@pytest.mark.parametrize("legacy", [False, True])
@pytest.mark.parametrize(
    "backend", ["sqlite"] + (["postgresql"] if os.getenv("RUN_INTEGRATION_TESTS") == "1" else [])
)
async def test_community_migrations_fresh_and_existing_database(
    legacy: bool, backend: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    from alembic import context
    from alembic.migration import MigrationContext
    from alembic.operations import Operations

    schema = "community_migration_test_" + uuid4().hex
    administrator = None
    if backend == "postgresql":
        from app.config import get_settings

        administrator = create_async_engine(get_settings().database_url)
        async with administrator.begin() as connection:
            await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
        engine = create_async_engine(
            get_settings().database_url, connect_args={"server_settings": {"search_path": schema}}
        )
    else:
        engine = create_async_engine("sqlite+aiosqlite://")
    modules = [
        runpy.run_path(str(Path(__file__).parents[1] / "migrations" / "versions" / name))
        for name in ["0058_community.py", "0059_pet_friendly.py", "0060_community_places.py"]
    ]
    monkeypatch.setattr(context, "is_offline_mode", lambda: False)

    def verify(sync: Any) -> None:
        operations = Operations(MigrationContext.configure(sync))
        for module in modules:
            module["upgrade"].__globals__["op"] = operations
        if legacy:
            # Emulate the schema before this additive change, then preserve an
            # existing account through upgrade. All data is in this fresh fixture.
            for module in reversed(modules):
                module["downgrade"]()
            sync.execute(
                text(
                    "INSERT INTO users (id, email, is_active, is_admin, created_at, "
                    "updated_at, preferred_locale, preferred_currency, auth_version) "
                    "VALUES (:id, 'existing@example.test', true, false, "
                    "CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'en', 'TWD', 1)"
                ),
                {"id": uuid4().hex},
            )
        for _ in range(2):
            for module in modules:
                module["upgrade"]()
        inspector = inspect(sync)
        for name, table in Base.metadata.tables.items():
            if name.startswith(("community_", "pet_")):
                assert {column["name"] for column in inspector.get_columns(name)} == set(
                    table.columns.keys()
                )
        assert {"email_verified_at", "deleted_at"} <= {
            column["name"] for column in inspector.get_columns("users")
        }
        if legacy:
            assert (
                sync.scalar(
                    text("SELECT COUNT(*) FROM users WHERE email = 'existing@example.test'")
                )
                == 1
            )

    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
            await connection.run_sync(verify)
    finally:
        await engine.dispose()
        if administrator is not None:
            # This exact, generated schema is owned exclusively by this test.
            assert schema.startswith("community_migration_test_") and len(schema) == 57
            async with administrator.begin() as connection:
                await connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
            await administrator.dispose()


@pytest.mark.asyncio
async def test_default_off_admin_settings_and_private_profile(harness: Harness) -> None:
    h = harness
    response = await h.call("GET", "/community/profiles/traveler_0", actor=None)
    assert "email" not in response.text and "private-" not in response.text
    await h.call("GET", "/admin/community/settings", actor=0, expected=403)
    settings = (await h.call("GET", "/admin/community/settings", actor=2)).json()["settings"]
    invalid = {**settings, "enabled": "true"}
    await h.call(
        "PUT",
        "/admin/community/settings",
        actor=2,
        expected=422,
        json={"settings": invalid, "reason": "Invalid type test"},
    )
    settings["enabled"] = False
    await h.call(
        "PUT",
        "/admin/community/settings",
        actor=2,
        json={"settings": settings, "reason": "Acceptance not complete"},
    )
    status = await h.call("GET", "/community/status", actor=None)
    assert status.headers["cache-control"] == "no-store"
    assert status.json()["enabled"] is False
    await h.call("GET", "/community/feed", actor=None, expected=403)
    async with h.factory() as session:
        assert await session.scalar(select(func.count()).select_from(AdminAuditLog)) == 1
        row = await session.scalar(
            select(ProviderConfig).where(ProviderConfig.provider == "community")
        )
        assert row
        await session.delete(row)
        await session.commit()
    assert (await h.call("GET", "/community/status", actor=None)).json()["enabled"] is False


@pytest.mark.asyncio
async def test_three_distinct_posts_and_approved_revision_preserved(harness: Harness) -> None:
    h = harness
    await h.call("POST", "/community/posts", actor=3, expected=403, json={"title": "unverified"})
    for _ in range(3):
        post = await h.publish(await h.post())
        assert post["state"] == "pending"
        await h.call("GET", f"/community/posts/{post['id']}", actor=None, expected=404)
        approved = await h.approve(post)
        assert approved["state"] == "published"
        await h.call(
            "PUT",
            f"/admin/community/posts/{post['id']}",
            actor=2,
            expected=409,
            json={"version": post["version"], "action": "approve", "reason": "Stale review"},
        )
    fourth = await h.publish(await h.post())
    assert fourth["state"] == "published"
    async with h.factory() as session:
        row = await session.scalar(
            select(ProviderConfig).where(ProviderConfig.provider == "community")
        )
        assert row
        row.config = {"enabled": True, "risk_terms": ["review-trigger"]}
        await session.commit()
    edited = (
        await h.call(
            "PUT",
            f"/community/posts/{fourth['id']}",
            json={
                "version": fourth["version"],
                "title": "review-trigger",
                "body": "new body",
                "destination": "Tokyo",
            },
        )
    ).json()
    pending = await h.publish(edited)
    public = (await h.call("GET", f"/community/posts/{fourth['id']}", actor=None)).json()
    assert public["title"] == "Tokyo trip" and pending["pending_revision_id"]
    await h.approve(pending)
    assert (await h.call("GET", f"/community/posts/{fourth['id']}", actor=None)).json()[
        "title"
    ] == "review-trigger"


@pytest.mark.asyncio
async def test_mutual_messages_idempotency_block_and_report_scope(harness: Harness) -> None:
    h = harness
    other = h.ids[1]
    await h.call("POST", f"/community/conversations/{other}", expected=403)
    await h.call("PUT", f"/community/profiles/{other}/follow")
    await h.call("PUT", f"/community/profiles/{h.ids[0]}/follow", actor=1)
    conversation = (await h.call("POST", f"/community/conversations/{other}", expected=201)).json()[
        "id"
    ]
    payload = {"body": "hello", "idempotency_key": "message-retry-001"}
    sent = await h.call(
        "POST", f"/community/conversations/{conversation}/messages", json=payload, expected=201
    )
    replay = await h.call(
        "POST", f"/community/conversations/{conversation}/messages", json=payload, expected=201
    )
    assert sent.json()["id"] == replay.json()["id"]
    await h.call(
        "POST",
        f"/community/conversations/{conversation}/messages",
        expected=409,
        json={**payload, "body": "changed"},
    )
    await h.call("GET", f"/community/conversations/{conversation}/messages", actor=2, expected=404)
    report = (
        await h.call(
            "POST",
            "/community/reports",
            expected=201,
            json={
                "kind": "message",
                "target": conversation,
                "reason": "Review this selected message",
                "message_ids": [sent.json()["id"]],
            },
        )
    ).json()
    cases = (await h.call("GET", "/admin/community/reports", actor=2)).json()["items"]
    assert cases[0]["id"] == report["id"]
    assert len(cases[0]["evidence"]["messages"]) == 1
    await h.call("DELETE", f"/community/profiles/{other}/follow")
    await h.call(
        "POST",
        f"/community/conversations/{conversation}/messages",
        json={**payload, "idempotency_key": "after-unfollow"},
        expected=403,
    )
    await h.call("PUT", f"/community/profiles/{other}/block")
    await h.call("GET", "/community/profiles/traveler_0", actor=1, expected=404)
    await h.call("GET", "/community/profiles/traveler_0", actor=None)
    await h.call("GET", f"/community/conversations/{conversation}/messages", actor=1, expected=404)
    async with h.factory() as session:
        assert await session.scalar(select(func.count()).select_from(Message)) == 1


def test_snapshot_allowlist_excludes_private_travel_data() -> None:
    trip = TripPlan(
        destination_name="Tokyo",
        start_date=date(2026, 10, 1),
        timezone="Asia/Tokyo",
        data={"booking": "secret"},
    )
    base = {
        "day_date": date(2026, 10, 1),
        "position": 0,
        "is_skipped": False,
        "names_json": {},
        "duration_minutes": 60,
    }
    rows = [
        TripPlanItem(item_type=kind, title=kind, notes="private note", data={"price": 999}, **base)
        for kind in ("flight", "hotel", "hotspot")
    ]
    snapshot = itinerary_snapshot(trip, rows)
    assert len(snapshot["stops"]) == 1
    encoded = str(snapshot)
    assert "2026-10-01" not in encoded and "private note" not in encoded and "999" not in encoded
    assert snapshot["stops"][0]["day"] == 1


@pytest.mark.asyncio
async def test_free_fork_snapshot_and_replay_after_withdraw(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    h = harness
    from app.trips.schedule import ensure_system_slots

    monkeypatch.setattr("app.trips.router.limit_for", AsyncMock(return_value=100))
    async with h.factory() as session:
        trip = TripPlan(
            user_id=h.ids[0],
            name="Source private",
            mode="manual",
            total_price=9000,
            currency="TWD",
            destination_name="Tokyo",
            timezone="Asia/Tokyo",
            start_date=date(2026, 10, 1),
            data={"secret": "booking"},
        )
        session.add(trip)
        await session.flush()
        session.add(
            TripPlanItem(
                trip_plan_id=trip.id,
                item_type="hotspot",
                title="Park",
                notes="private",
                day_date=trip.start_date,
                position=0,
                duration_minutes=90,
            )
        )
        await session.commit()
        trip_id = str(trip.id)
    post = await h.publish(await h.post(source_trip_id=trip_id, allow_fork=True))
    await h.approve(post)
    payload = {"start_date": "2027-01-10", "idempotency_key": "fork-retry-001"}
    first = (
        await h.call(
            "POST", f"/community/posts/{post['id']}/fork", actor=1, json=payload, expected=201
        )
    ).json()
    await h.call("POST", f"/community/posts/{post['id']}/withdraw")
    replay = (
        await h.call(
            "POST", f"/community/posts/{post['id']}/fork", actor=1, json=payload, expected=201
        )
    ).json()
    assert first["trip_id"] == replay["trip_id"] and replay["replayed"]
    await h.call(
        "POST",
        f"/community/posts/{post['id']}/fork",
        actor=1,
        expected=404,
        json={**payload, "idempotency_key": "fresh-key-after-withdraw"},
    )
    async with h.factory() as session:
        assert await session.scalar(select(func.count()).select_from(Fork)) == 1
        copy = await session.get(TripPlan, UUID(first["trip_id"]))
        assert copy and copy.start_date == date(2027, 1, 10) and copy.total_price == 0
        assert "booking" not in str(copy.data) and not copy.data["prices_checked"]
        items = list(
            (
                await session.scalars(
                    select(TripPlanItem)
                    .where(TripPlanItem.trip_plan_id == copy.id)
                    .order_by(TripPlanItem.day_date, TripPlanItem.position)
                )
            ).all()
        )
        assert any(row.system_role == "outbound_flight" for row in items)
        if session.get_bind().dialect.name == "sqlite":
            # SQLite drops timezone offsets from DateTime(timezone=True), unlike
            # the production PostgreSQL contract used by schedule ordering.
            for row in items:
                if row.start_time is not None:
                    row.start_time = row.start_time.replace(tzinfo=UTC)
        assert not ensure_system_slots(session, copy, items)
        assert all(not row.notes and row.offer_id is None for row in items)
        assert len({(row.day_date, row.system_role) for row in items if row.system_role}) == sum(
            row.system_role is not None for row in items
        )


@pytest.mark.asyncio
async def test_postgres_comment_and_fork_lock_overlap_has_no_deadlock(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import asyncio

    from sqlalchemy.dialects import postgresql

    h = harness
    async with h.factory() as session:
        if session.get_bind().dialect.name != "postgresql":
            pytest.skip("Requires real PostgreSQL row and foreign-key locks")
        trip = TripPlan(
            user_id=h.ids[0],
            name="Public source",
            mode="manual",
            total_price=0,
            currency="TWD",
            data={},
            start_date=date(2026, 10, 1),
            end_date=date(2026, 10, 1),
            destination_name="Tokyo",
            timezone="Asia/Tokyo",
        )
        session.add(trip)
        await session.commit()
        trip_id = str(trip.id)
    post = await h.approve(await h.publish(await h.post(source_trip_id=trip_id, allow_fork=True)))
    post_locked, member_locked = asyncio.Event(), asyncio.Event()
    original = AsyncSession.scalar

    async def overlapping_locks(
        self: AsyncSession, statement: Any, *args: Any, **kwargs: Any
    ) -> Any:
        result = await original(self, statement, *args, **kwargs)
        sql = str(statement.compile(dialect=postgresql.dialect()))
        if "FOR " in sql and "FROM users " in sql.replace("\n", " "):
            member_locked.set()
            await asyncio.wait_for(post_locked.wait(), timeout=5)
        elif "FOR " in sql and "FROM community_posts " in sql.replace("\n", " "):
            post_locked.set()
            await asyncio.wait_for(member_locked.wait(), timeout=5)
        return result

    monkeypatch.setattr(AsyncSession, "scalar", overlapping_locks)
    payload = {"start_date": "2026-10-10", "idempotency_key": "concurrent-fork-key"}
    async with asyncio.timeout(15):
        comment, first, replay = await asyncio.gather(
            h.call(
                "POST",
                f"/community/posts/{post['id']}/comments",
                actor=1,
                expected=201,
                json={"body": "Comment during a fork", "locale": "en"},
            ),
            h.call(
                "POST", f"/community/posts/{post['id']}/fork", actor=1, expected=201, json=payload
            ),
            h.call(
                "POST", f"/community/posts/{post['id']}/fork", actor=1, expected=201, json=payload
            ),
        )
    assert comment.json()["id"]
    assert first.json()["trip_id"] == replay.json()["trip_id"]
    assert sorted([first.json()["replayed"], replay.json()["replayed"]]) == [False, True]


@pytest.mark.asyncio
async def test_pet_trip_updates_preserve_data_and_reject_stale_inserts(harness: Harness) -> None:
    h = harness
    async with h.factory() as session:
        trip = TripPlan(
            user_id=h.ids[0],
            name="Private trip",
            mode="manual",
            total_price=0,
            currency="TWD",
            start_date=date(2027, 1, 10),
            end_date=date(2027, 1, 10),
            data={"private": "Keep my notes", "preferences": {"slow_travel": True}},
        )
        place = PetPlace(
            name="Reviewed identity, unknown pet rules",
            kind="cafe",
            country="JP",
            destination="Tokyo",
            status="approved",
            verified_at=datetime.now(UTC),
        )
        session.add_all([trip, place])
        await session.commit()
        trip_id, place_id = str(trip.id), str(place.id)
    payload = {"version": 1, "requirements": {"species": "dog", "weight_kg": 5}}
    settings = (
        await h.call("PUT", f"/community/trips/{trip_id}/pet-preferences", json=payload)
    ).json()
    assert settings["version"] == 2 and settings["requirements"]["species"] == "dog"
    await h.call("PUT", f"/community/trips/{trip_id}/pet-preferences", json=payload, expected=409)
    await h.call("GET", f"/community/trips/{trip_id}/pet-preferences", actor=1, expected=404)
    insertion = {"version": 2, "place_id": place_id, "day": "2027-01-10"}
    warned = (
        await h.call("POST", f"/community/trips/{trip_id}/pet-places", json=insertion, expected=201)
    ).json()
    assert warned["confirmation_required"] and warned["conflicts"]
    async with h.factory() as session:
        assert await session.scalar(select(func.count()).select_from(TripPlanItem)) == 0
    added = (
        await h.call(
            "POST",
            f"/community/trips/{trip_id}/pet-places",
            json={**insertion, "confirm_conflicts": True},
            expected=201,
        )
    ).json()
    assert added["version"] == 3 and not added["confirmation_required"]
    await h.call(
        "POST",
        f"/community/trips/{trip_id}/pet-places",
        json={**insertion, "confirm_conflicts": True},
        expected=409,
    )
    async with h.factory() as session:
        stored = await session.get(TripPlan, UUID(trip_id))
        assert stored and stored.data["private"] == "Keep my notes"
        assert stored.data["preferences"]["slow_travel"]
        assert await session.scalar(select(func.count()).select_from(TripPlanItem)) == 1


@pytest.mark.asyncio
async def test_account_tokens_single_use_and_delete_revokes(harness: Harness) -> None:
    h = harness
    token = "verified_token_" + "a" * 32
    deletion = "delete_token_" + "b" * 32
    async with h.factory() as session:
        for value, purpose in ((token, "verify"), (deletion, "delete")):
            session.add(
                AccountToken(
                    user_id=h.ids[3],
                    digest=hashlib.sha256(value.encode()).hexdigest(),
                    purpose=purpose,
                    auth_version=1,
                    expires_at=datetime.now(UTC) + timedelta(minutes=5),
                )
            )
        await session.commit()
    await h.call("POST", "/auth/verify-email", actor=None, json={"token": token})
    await h.call("POST", "/auth/verify-email", actor=None, expected=400, json={"token": token})
    await h.call(
        "POST",
        "/auth/delete-account",
        actor=None,
        expected=202,
        json={"token": deletion, "confirmation": "DELETE"},
    )
    await h.call("GET", "/community/me", actor=3, expected=401)
    await h.call("GET", "/community/profiles/traveler_3", actor=None, expected=404)
    async with h.factory() as session:
        user = await session.get(User, h.ids[3])
        assert user and user.auth_version == 2 and user.deleted_at


@pytest.mark.asyncio
async def test_deleted_member_cannot_log_in_even_before_cleanup(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    from app.auth.service import hash_password

    monkeypatch.setattr("app.auth.router.enforce_named_rate_limit", AsyncMock())
    async with harness.factory() as session:
        user = await session.get(User, harness.ids[0])
        assert user is not None
        user.password_hash = hash_password("old-valid-password-123")
        user.is_active = False
        user.deleted_at = datetime.now(UTC)
        await session.commit()
    response = await harness.call(
        "POST",
        "/auth/login",
        actor=None,
        expected=401,
        json={"email": "private-0@example.com", "password": "old-valid-password-123"},
    )
    assert "invalid_credentials" in response.text
    assert "set-cookie" not in response.headers


@pytest.mark.asyncio
async def test_conversion_requires_order_and_same_member_and_post(harness: Harness) -> None:
    from app.community.models import CommunityMetric

    now = datetime.now(UTC)
    async with harness.factory() as session:
        # A complete chain for one reader. Another member saves before reading;
        # a third reads one post but saves a different one. Neither is converted.
        events = [
            (0, "post-a", "read", 0),
            (0, "post-a", "save", 1),
            (0, "post-a", "fork", 2),
            (0, "post-a", "trip_created", 3),
            (1, "post-a", "save", 0),
            (1, "post-a", "read", 1),
            (3, "post-b", "read", 0),
            (3, "post-c", "save", 1),
        ]
        for actor, target, kind, offset in events:
            session.add(
                CommunityMetric(
                    user_id=harness.ids[actor],
                    target=target,
                    kind=kind,
                    day=now.date().isoformat(),
                    created_at=now - timedelta(minutes=10 - offset),
                )
            )
        await session.commit()
    result = (await harness.call("GET", "/admin/community/overview", actor=2)).json()
    assert result["conversion_funnel_30d"] == {"read": 3, "save": 1, "fork": 1, "trip_created": 1}
    assert result["unique_users_30d"]["save"] == 3
    await harness.call("GET", "/admin/community/overview", expected=403)


@pytest.mark.asyncio
async def test_review_results_only_expose_owned_targets(harness: Harness) -> None:
    post = await harness.post()
    await harness.approve(await harness.publish(post))
    await harness.approve(await harness.publish(await harness.post(actor=1), actor=1))
    async with harness.factory() as session:
        session.add(
            AdminAuditLog(
                actor_user_id=harness.ids[2],
                action="usage_adjusted",
                target=str(harness.ids[0]),
                metadata_json={"reason": "Unrelated sensitive accounting"},
            )
        )
        await session.commit()
    result = (await harness.call("GET", "/community/me/reviews")).json()
    assert len(result["items"]) == 1
    assert result["items"][0]["reason"] == "Source checked"
    assert set(result["items"][0]) == {"id", "action", "reason", "created_at"}
    assert "Unrelated sensitive" not in str(result)
    assert str(harness.ids[2]) not in str(result)
    assert post["id"] not in str(result)
    await harness.call("GET", "/community/me/reviews", actor=None, expected=401)


def test_media_decodes_reencodes_strips_metadata_and_rejects_fake() -> None:
    original = Image.new("RGB", (80, 40), "red")
    exif = Image.Exif()
    exif[0x010E] = "private GPS narrative"
    stream = io.BytesIO()
    original.save(stream, format="JPEG", exif=exif)
    full, thumb, width, height = clean_image(stream.getvalue())
    assert (width, height) == (80, 40) and thumb
    with Image.open(io.BytesIO(full)) as image:
        assert image.format == "WEBP" and not image.getexif() and "exif" not in image.info
    with pytest.raises(Exception, match="community_image_invalid"):
        clean_image(b"<svg>not a raster</svg>")


@pytest.mark.asyncio
async def test_pet_ai_only_receives_current_verified_compatible_candidates(
    harness: Harness,
) -> None:
    from app.ai.itinerary import AIPlannerCandidate
    from app.community.pet_models import PlaceReference
    from app.community.pet_planning import filter_candidates
    from app.problems import AppError

    rule = PetRule(
        species="dog",
        status="conditional",
        weight_limit="limited",
        max_weight_kg=10,
        count_limit="limited",
        max_count=2,
        outdoor_allowed=True,
        leash_required=True,
        carrier_required=False,
        stroller_required=False,
        diaper_required=False,
    )
    candidates = [
        AIPlannerCandidate(
            key=f"hotspot:{key}",
            kind="hotspot",
            name=key,
            category="attraction",
            latitude=25,
            longitude=121,
            duration_minutes=60,
        )
        for key in ["compatible", "unknown", "stale", "disputed", "unlinked"]
    ]
    async with harness.factory() as session:
        for candidate in candidates[:-1]:
            place = PetPlace(
                name=candidate.name,
                country="TW",
                destination="Taipei",
                kind="attraction",
                status="approved",
                disputed=candidate.name == "disputed",
                policies=[
                    (
                        rule.model_copy(update={"weight_limit": "unknown", "max_weight_kg": None})
                        if candidate.name == "unknown"
                        else rule
                    ).model_dump()
                ],
                source_url="https://example.com/pet-rules",
                verified_at=datetime.now(UTC)
                - timedelta(days=181 if candidate.name == "stale" else 0),
            )
            session.add(place)
            await session.flush()
            session.add(PlaceReference(place_id=place.id, kind="hotspot", target=candidate.name))
        await session.commit()
        requirements = PetRequirements(species="dog", weight_kg=5)
        result = await filter_candidates(session, candidates, requirements)
        assert [row.key for row in result] == ["hotspot:compatible"]
        for incompatible in [
            {"species": "cat"},
            {"weight_kg": 20},
            {"count": 3},
            {"area": "indoor"},
            {"has_leash": False},
            {"has_stroller": True},
            {"overnight": True},
        ]:
            with pytest.raises(AppError) as error:
                await filter_candidates(
                    session, candidates, requirements.model_copy(update=incompatible)
                )
            assert error.value.code == "pet_candidates_insufficient"
            assert error.value.status == 422


def test_pet_eligibility_species_limits_and_unknown_are_not_matches() -> None:
    rule = PetRule(
        species="dog",
        status="conditional",
        weight_limit="limited",
        max_weight_kg=10,
        count_limit="limited",
        max_count=2,
        outdoor_allowed=True,
        leash_required=True,
        carrier_required=False,
        stroller_required=False,
        diaper_required=False,
    )
    place = PetPlace(
        status="approved",
        disputed=False,
        policies=[rule.model_dump()],
        source_url="https://example.com/pets",
        verified_at=datetime.now(UTC),
    )
    req = PetRequirements(species="dog", weight_kg=5)
    assert eligibility(place, req, 180) == []
    assert eligibility(place, req.model_copy(update={"species": "cat"}), 180) == ["species_unknown"]
    assert "weight_exceeded" in eligibility(place, req.model_copy(update={"weight_kg": 20}), 180)
    assert "stroller_unavailable" in eligibility(
        place, req.model_copy(update={"has_stroller": True}), 180
    )
    place.policies = [
        rule.model_copy(update={"weight_limit": "unknown", "max_weight_kg": None}).model_dump()
    ]
    assert "weight_unknown" in eligibility(place, req, 180)
    place.verified_at = datetime.now(UTC) - timedelta(days=181)
    assert eligibility(place, req, 180) == ["verification_required"]


@pytest.mark.asyncio
async def test_translation_cache_edit_invalidation_and_budget(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    h = harness
    async with h.factory() as session:
        config = await session.scalar(
            select(ProviderConfig).where(ProviderConfig.provider == "community")
        )
        assert config
        config.config = {
            "enabled": True,
            "translation_enabled": True,
            "translation_characters_per_month": 200,
        }
        profile = await session.get(Profile, h.ids[0])
        assert profile
        profile.approved_posts = 3
        await session.commit()
    provider = AsyncMock(return_value="Translated content")
    monkeypatch.setattr("app.community.translation.translate_text", provider)
    post = await h.publish(await h.post())
    payload = {"kind": "post", "target_id": post["id"], "locale": "en"}
    await h.call("POST", "/community/translations", json=payload)
    await h.call("POST", "/community/translations", json=payload)
    assert provider.await_count == 1
    edited = (
        await h.call(
            "PUT",
            f"/community/posts/{post['id']}",
            json={
                "version": post["version"],
                "title": "New title",
                "body": "New experience",
                "destination": "Tokyo",
            },
        )
    ).json()
    await h.publish(edited)
    await h.call("POST", "/community/translations", json=payload)
    assert provider.await_count == 2
    async with h.factory() as session:
        budget = await session.get(TranslationBudget, datetime.now(UTC).strftime("%Y-%m"))
        assert budget and budget.characters > 0


@pytest.mark.asyncio
async def test_collections_private_blocked_and_withdrawn_content(harness: Harness) -> None:
    h = harness
    post = await h.publish(await h.post())
    await h.approve(post)
    collection = (
        await h.call(
            "POST",
            "/community/collections",
            actor=1,
            expected=201,
            json={"name": "Private favorites"},
        )
    ).json()["id"]
    path = f"/community/collections/{collection}/items"
    for _ in range(2):
        await h.call("PUT", path, actor=1, json={"kind": "post", "target": post["id"]})
    assert len((await h.call("GET", path, actor=1)).json()["items"]) == 1
    await h.call("GET", path, actor=0, expected=404)
    await h.call("PUT", f"/community/profiles/{h.ids[1]}/block")
    assert (await h.call("GET", path, actor=1)).json()["items"][0]["unavailable"]
    await h.call("DELETE", f"/community/profiles/{h.ids[1]}/block")
    await h.call("POST", f"/community/posts/{post['id']}/withdraw")
    assert (await h.call("GET", path, actor=1)).json()["items"][0]["unavailable"]


@pytest.mark.asyncio
async def test_comments_one_level_mentions_verification_and_cursors(harness: Harness) -> None:
    h = harness
    post = await h.publish(await h.post())
    await h.approve(post)
    path = f"/community/posts/{post['id']}/comments"
    await h.call("POST", path, actor=3, expected=403, json={"body": "unverified"})
    first = (
        await h.call(
            "POST",
            path,
            actor=1,
            expected=201,
            json={"body": "@traveler_0 @traveler_2 A visit", "locale": "en"},
        )
    ).json()
    reply = (
        await h.call(
            "POST", path, expected=201, json={"body": "Thank you", "parent_id": first["id"]}
        )
    ).json()
    await h.call(
        "POST", path, actor=1, expected=422, json={"body": "too deep", "parent_id": reply["id"]}
    )
    rows = (await h.call("GET", path, actor=None)).json()["items"]
    assert [row["id"] for row in rows] == [first["id"], reply["id"]]
    async with h.factory() as session:
        notices = (await session.scalars(select(Notification))).all()
        assert {"comment", "mention", "reply"} <= {row.kind for row in notices}
        assert len([row for row in notices if row.kind == "mention"]) == 1
    await h.call("PUT", f"/community/profiles/{h.ids[1]}/block")
    await h.call("POST", path, actor=1, expected=404, json={"body": "after block"})
    rows = (await h.call("GET", path)).json()["items"]
    assert all(row["author"]["id"] != str(h.ids[1]) for row in rows)


def allowed_dog_rule() -> dict[str, Any]:
    return PetRule(
        species="dog",
        status="conditional",
        weight_limit="limited",
        max_weight_kg=10,
        count_limit="limited",
        max_count=2,
        outdoor_allowed=True,
        indoor_allowed=False,
        leash_required=True,
        carrier_required=False,
        stroller_required=False,
        stroller_allowed=True,
        diaper_required=False,
        ground_allowed=True,
        overnight_allowed=False,
        reservation_required=True,
        fee_amount=0,
        fee_currency="TWD",
    ).model_dump()


@pytest.mark.asyncio
async def test_pet_directory_review_reports_history_and_staleness(harness: Harness) -> None:
    h = harness
    suggestion = {
        "name": "Verified café",
        "kind": "cafe",
        "country": "TW",
        "destination": "Taipei",
        "official_url": "https://example.com/cafe",
    }
    place = (await h.call("POST", "/pet-friendly/places", expected=201, json=suggestion)).json()[
        "id"
    ]
    duplicate = (await h.call("POST", "/pet-friendly/places", expected=201, json=suggestion)).json()
    assert duplicate["id"] == place
    await h.call("GET", f"/pet-friendly/places/{place}", actor=None, expected=404)
    review = {
        "version": 1,
        "status": "approved",
        "source_url": "https://example.com/pet-policy",
        "policies": [allowed_dog_rule()],
        "reason": "Official conditions checked",
    }
    path = f"/admin/pet-friendly/places/{place}"
    await h.call("PUT", path, actor=0, expected=403, json=review)
    await h.call("PUT", path, actor=2, json=review)
    await h.call("PUT", path, actor=2, expected=409, json=review)
    matching = (
        await h.call("GET", "/pet-friendly/places?species=dog&weight_kg=5", actor=None)
    ).json()["items"]
    assert [row["id"] for row in matching] == [place]
    for query in (
        "species=cat&weight_kg=5",
        "species=dog&weight_kg=20",
        "species=dog&weight_kg=5&area=indoor",
        "species=dog&weight_kg=5&overnight=true",
    ):
        assert not (await h.call("GET", "/pet-friendly/places?" + query, actor=None)).json()[
            "items"
        ]
    report = (
        await h.call(
            "POST",
            f"/pet-friendly/places/{place}/reports",
            expected=201,
            json={
                "body": "Conflicting new rule",
                "proposed_policies": [PetRule(species="dog", status="not_allowed").model_dump()],
            },
        )
    ).json()
    assert (await h.call("GET", f"/pet-friendly/places/{place}", actor=None)).json()[
        "verification_current"
    ]
    await h.call(
        "PUT",
        f"/admin/pet-friendly/reports/{report['id']}",
        actor=2,
        json={"status": "resolved", "reason": "Conflicting experience reviewed"},
    )
    public = (await h.call("GET", f"/pet-friendly/places/{place}", actor=None)).json()
    assert public["disputed"] and public["policies"][0]["status"] == "conditional"
    assert not (await h.call("GET", "/pet-friendly/places", actor=None)).json()["items"]
    assert (await h.call("GET", "/pet-friendly/places?include_uncertain=true", actor=None)).json()[
        "items"
    ]
    history = (await h.call("GET", path + "/history", actor=2)).json()["items"]
    assert history[0]["actor_id"] == str(h.ids[2])
    async with h.factory() as session:
        row = await session.get(PetPlace, UUID(place))
        assert row
        row.disputed = False
        row.verified_at = datetime.now(UTC) - timedelta(days=181)
        await session.commit()
    assert not (await h.call("GET", "/pet-friendly/places", actor=None)).json()["items"]


@pytest.mark.parametrize(
    "patch,reason",
    [
        ({"weight_kg": 11}, "weight_exceeded"),
        ({"count": 3}, "count_exceeded"),
        ({"area": "indoor"}, "area_unavailable"),
        ({"has_leash": False}, "leash_required"),
        ({"overnight": True}, "overnight_unavailable"),
        ({"species": "cat"}, "species_unknown"),
    ],
)
def test_pet_filters_never_infer_compatibility(patch: dict[str, Any], reason: str) -> None:
    place = PetPlace(
        status="approved",
        disputed=False,
        verified_at=datetime.now(UTC),
        source_url="https://example.com/pets",
        policies=[allowed_dog_rule()],
    )
    request = PetRequirements(species="dog", weight_kg=5).model_copy(update=patch)
    assert reason in eligibility(place, request, 180)
    assert PetRequirements(species="貓", weight_kg=5).species == "cat"


@pytest.mark.asyncio
async def test_media_private_pending_public_withdraw_and_review_access(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = harness
    fake = MagicMock()
    fake.generate_presigned_url.return_value = "https://private-storage.example/signed"
    monkeypatch.setattr("app.community.media.storage", lambda **_: fake)
    async with h.factory() as session:
        media = Media(
            owner_id=h.ids[0],
            object_key="images/private.webp",
            thumbnail_key="thumbs/private.webp",
            width=20,
            height=20,
            size=100,
            alt="Trip",
        )
        session.add(media)
        await session.commit()
        media_id = str(media.id)
    await h.call("GET", f"/community/media/{media_id}", actor=1, expected=404)
    await h.call("GET", f"/community/media/{media_id}", actor=None, expected=404)
    unrelated = await h.publish(await h.post(actor=1, body=media_id), actor=1)
    await h.approve(unrelated)
    await h.call(
        "POST",
        "/community/reports",
        expected=201,
        json={"kind": "post", "target": unrelated["id"], "reason": "Review quoted identifier"},
    )
    await h.call("GET", f"/admin/community/media/{media_id}", actor=2, expected=404)
    post = await h.publish(await h.post(media_ids=[media_id]))
    await h.call("GET", f"/admin/community/media/{media_id}", actor=2)
    await h.call("GET", f"/admin/community/media/{media_id}", actor=1, expected=403)
    await h.approve(post)
    response = await h.call("GET", f"/community/media/{media_id}", actor=None)
    assert response.headers["cache-control"] == "private, no-store"
    assert fake.generate_presigned_url.call_args.kwargs["ExpiresIn"] == 60
    await h.call(
        "POST",
        "/community/reports",
        actor=1,
        expected=201,
        json={"kind": "post", "target": post["id"], "reason": "Review attached photograph"},
    )
    await h.call("POST", f"/community/posts/{post['id']}/withdraw")
    await h.call("GET", f"/community/media/{media_id}", actor=None, expected=404)
    await h.call("GET", f"/community/media/{media_id}")
    await h.call("GET", f"/admin/community/media/{media_id}", actor=2)


@pytest.mark.asyncio
async def test_each_feature_switch_is_enforced_by_api(harness: Harness) -> None:
    h = harness
    settings = (await h.call("GET", "/admin/community/settings", actor=2)).json()["settings"]
    settings.update(
        posting_enabled=False,
        comments_enabled=False,
        messaging_enabled=False,
        translation_enabled=False,
        pet_reports_enabled=False,
    )
    await h.call(
        "PUT",
        "/admin/community/settings",
        actor=2,
        json={"settings": settings, "reason": "Temporarily pause operations"},
    )
    for method, path, payload in [
        ("POST", "/community/posts", {"title": "No write"}),
        ("POST", f"/community/posts/{uuid4()}/comments", {"body": "No comment"}),
        ("POST", f"/community/conversations/{h.ids[1]}", None),
        (
            "POST",
            "/community/translations",
            {"kind": "post", "target_id": str(uuid4()), "locale": "en"},
        ),
        (
            "POST",
            "/pet-friendly/places",
            {"name": "Place", "kind": "shop", "country": "TW", "destination": "Taipei"},
        ),
    ]:
        response = await h.call(
            method, path, expected=403, **({"json": payload} if payload else {})
        )
        assert response.json()["code"] == "community_closed"
    await h.call("GET", "/community/feed", actor=None)


@pytest.mark.asyncio
async def test_delete_job_erases_private_data_but_keeps_delivered_messages(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.community.jobs import erase_account

    h = harness
    await h.call("PUT", f"/community/profiles/{h.ids[1]}/follow")
    await h.call("PUT", f"/community/profiles/{h.ids[0]}/follow", actor=1)
    conversation = (
        await h.call("POST", f"/community/conversations/{h.ids[1]}", expected=201)
    ).json()["id"]
    await h.call(
        "POST",
        f"/community/conversations/{conversation}/messages",
        expected=201,
        json={"body": "Already delivered", "idempotency_key": "before-deletion-001"},
    )
    async with h.factory() as session:
        user = await session.get(User, h.ids[0])
        assert user
        user.deleted_at = datetime.now(UTC)
        user.is_active = False
        profile = await session.get(Profile, user.id)
        assert profile
        profile.deleted_at = user.deleted_at
        trip = TripPlan(
            user_id=user.id,
            name="Private booking",
            mode="manual",
            total_price=42,
            data={"booking": "secret"},
            start_date=date(2026, 10, 1),
        )
        session.add(trip)
        await session.flush()
        session.add(
            TripPlanItem(
                trip_plan_id=trip.id,
                item_type="hotel",
                title="Private hotel",
                notes="Door PIN",
                latitude=25,
                longitude=121,
                data={"guest": "name"},
            )
        )
        await session.flush()
        await erase_account(session, user.id)
        await session.commit()
        assert user.email.endswith("@deleted.invalid") and profile.handle.startswith("deleted_")
        assert trip.start_date is None and trip.data == {}
        item = await session.scalar(
            select(TripPlanItem).where(TripPlanItem.trip_plan_id == trip.id)
        )
        assert item and item.latitude is None and item.notes is None and not item.data
    delivered = (
        await h.call("GET", f"/community/conversations/{conversation}/messages", actor=1)
    ).json()
    assert delivered["items"][0]["body"] == "Already delivered"
    assert delivered["items"][0]["sender_id"] is None and not delivered["can_send"]


@pytest.mark.asyncio
async def test_post_catalog_references_are_typed_public_and_legacy_compatible(
    harness: Harness,
) -> None:
    from app.community.models import PostRevision
    from app.models import FoodMerchant, FoodMerchantSource, TravelHotspot

    h = harness
    async with h.factory() as session:
        pet = PetPlace(
            name="Dog cafe",
            names={"ja": "犬カフェ"},
            kind="cafe",
            country="JP",
            destination="tokyo",
            address="",
            status="approved",
        )
        hotspot = TravelHotspot(
            slug="public-trip-place",
            name="Public museum",
            city_code="NRT",
            destination_id="tokyo",
            city_name="Tokyo",
            country_code="JP",
            country_name="Japan",
            category="culture",
            search_text="Tokyo",
            review_status="approved",
            is_active=True,
        )
        merchant = FoodMerchant(
            slug="public-trip-merchant",
            name="Public restaurant",
            local_name="餐廳",
            names_json={"zh-TW": "已查核餐廳"},
            destination_id="tokyo",
            country_code="JP",
            review_status="approved",
            is_active=True,
            map_match_status="verified",
            google_place_id="exact-test-place",
            latitude=35.68,
            longitude=139.76,
            coordinate_source_type="merchant_official",
            coordinate_source_url="https://example.com/map",
        )
        session.add_all([pet, hotspot, merchant])
        await session.flush()
        source = FoodMerchantSource(
            merchant_id=merchant.id,
            source_type="merchant_official",
            source_scope="merchant_website",
            source_title="Official",
            source_url="https://example.com",
        )
        session.add(source)
        await session.commit()
        refs = [
            {"kind": "pet_place", "id": str(pet.id)},
            {"kind": "hotspot", "id": str(hotspot.id)},
            {"kind": "merchant", "id": str(merchant.id)},
        ]
        source_id, hotspot_id, pet_id = source.id, hotspot.id, pet.id
    post = await h.post(places=[*refs, refs[0]])
    assert [{"kind": place["kind"], "id": place["id"]} for place in post["places"]] == refs
    assert post["place_ids"] == [str(pet_id)]
    assert post["places"][2]["names"]["zh-TW"] == "已查核餐廳"
    assert set(post["places"][2]) == {"id", "kind", "name", "names", "destination", "href"}
    await h.approve(await h.publish(post))
    for invalid in [
        [{"kind": "hotel", "id": str(pet_id)}],
        [{"kind": "hotspot", "id": str(uuid4())}],
        [{**refs[0], "href": "https://attacker.example"}],
        refs * 7,
    ]:
        await h.call("POST", "/community/posts", expected=422, json={"places": invalid})
    await h.call(
        "POST", "/community/posts", expected=422, json={"places": refs, "place_ids": [str(pet_id)]}
    )
    async with h.factory() as session:
        source = await session.get(FoodMerchantSource, source_id)
        assert source is not None
        source.is_current = False
        hotspot = await session.get(TravelHotspot, hotspot_id)
        assert hotspot is not None
        hotspot.review_status = "disabled"
        await session.commit()
    public = (await h.call("GET", f"/community/posts/{post['id']}", actor=None)).json()
    assert [place["kind"] for place in public["places"]] == ["pet_place"]
    for ref in refs[1:]:
        await h.call("POST", "/community/posts", expected=422, json={"places": [ref]})
    legacy = await h.post(place_ids=[str(pet_id)])
    async with h.factory() as session:
        revision = await session.get(PostRevision, UUID(legacy["revision_id"]))
        assert revision is not None
        revision.place_refs = []  # Version written before 0060, only legacy IDs.
        await session.commit()
    draft = (await h.call("GET", f"/community/posts/{legacy['id']}/draft")).json()
    assert draft["places"][0]["id"] == str(pet_id)
    assert draft["places"][0]["name"] == "Dog cafe"


@pytest.mark.asyncio
async def test_public_place_search_locales_private_saved_and_collection_limit(
    harness: Harness,
) -> None:
    from app.community.models import Collection, CollectionItem
    from app.community.pet_models import PlaceReference
    from app.models import TravelHotspot

    h = harness
    async with h.factory() as session:
        hotspot = TravelHotspot(
            slug="verified-spot",
            name="Official spot",
            city_code="NRT",
            destination_id="tokyo",
            city_name="Tokyo",
            country_code="JP",
            country_name="Japan",
            category="culture",
            search_text="Tokyo",
            review_status="approved",
            is_active=True,
        )
        session.add(hotspot)
        await session.flush()
        pet = PetPlace(
            name="Official pet place",
            names={"ko": "반려동물카페"},
            kind="cafe",
            country="JP",
            destination="tokyo",
            address="",
            status="approved",
            policies=[],
        )
        session.add(pet)
        await session.flush()
        session.add(PlaceReference(place_id=pet.id, kind="hotspot", target=str(hotspot.id)))
        collection = Collection(user_id=h.ids[0], name="Full private list")
        session.add(collection)
        await session.flush()
        session.add_all(
            [
                CollectionItem(collection_id=collection.id, kind="pet_place", target=str(uuid4()))
                for _ in range(500)
            ]
        )
        await session.commit()
        pet_id, collection_id = pet.id, collection.id
    result = (
        await h.call("GET", "/community/search/places", actor=None, params={"q": "반려동물카페"})
    ).json()
    assert [row["id"] for row in result["items"]] == [str(pet_id)]
    result = (
        await h.call("GET", "/community/search/places", actor=None, params={"q": "Tokyo"})
    ).json()
    assert [row["kind"] for row in result["items"]] == ["pet_place"]  # One shared place.
    await h.call("GET", "/community/saved", actor=None, expected=401)
    result = (await h.call("GET", "/community/saved")).json()
    assert result["collections"]["items"][0]["name"] == "Full private list"
    result = (await h.call("GET", "/community/saved", actor=1)).json()
    assert result["collections"]["items"] == []
    await h.call(
        "PUT",
        f"/community/collections/{collection_id}/items",
        expected=403,
        json={"kind": "pet_place", "target": str(pet_id)},
    )
    stale = (await h.call("GET", f"/community/collections/{collection_id}/items")).json()
    assert all(row["unavailable"] for row in stale["items"])


@pytest.mark.asyncio
@pytest.mark.skipif(os.getenv("COMMUNITY_TEST_S3") != "1", reason="Requires isolated S3 companion")
async def test_real_private_s3_upload_decode_and_publication(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    import asyncio

    from app.community.media import storage
    from app.config import get_settings

    h = harness
    bucket = "community-test-" + uuid4().hex
    monkeypatch.setattr(get_settings(), "community_s3_bucket", bucket)
    client = storage()
    await asyncio.to_thread(client.create_bucket, Bucket=bucket)
    try:
        raw = io.BytesIO()
        Image.new("RGB", (32, 24), (14, 90, 80)).save(raw, format="PNG")
        created = (
            await h.call(
                "POST",
                "/community/media/uploads",
                expected=201,
                json={"size": len(raw.getvalue()), "content_type": "image/png", "alt": "Pet visit"},
            )
        ).json()
        async with AsyncClient() as browser:
            uploaded = await browser.post(
                created["upload"]["url"],
                data=created["upload"]["fields"],
                files={"file": ("visit.png", raw.getvalue(), "image/png")},
            )
            assert uploaded.status_code in {200, 204}, uploaded.text
            media_path = f"/community/media/{created['id']}"
            await h.call("POST", media_path + "/complete", actor=1, expected=404)
            complete = (await h.call("POST", media_path + "/complete")).json()
            assert (complete["width"], complete["height"]) == (32, 24)
            await h.call("GET", media_path, actor=None, expected=404)
            owner_url = (await h.call("GET", media_path)).json()["url"]
            assert (await browser.get(owner_url.split("?")[0])).status_code == 403
            post = await h.publish(await h.post(media_ids=[created["id"]]))
            await h.call("GET", media_path, actor=None, expected=404)
            await h.approve(post)
            public = (await h.call("GET", media_path, actor=None)).json()
            assert public["expires_in"] == 60
            image = await browser.get(public["url"])
            assert image.status_code == 200 and "no-store" in image.headers["cache-control"]
            assert Image.open(io.BytesIO(image.content)).format == "WEBP"
            await h.call("POST", f"/community/posts/{post['id']}/withdraw")
            await h.call("GET", media_path, actor=None, expected=404)
    finally:
        # Test-created bucket only; never enumerate a configured production bucket.
        assert bucket.startswith("community-test-") and len(bucket) == 47
        objects = await asyncio.to_thread(client.list_objects_v2, Bucket=bucket)
        for item in objects.get("Contents", []):
            await asyncio.to_thread(client.delete_object, Bucket=bucket, Key=item["Key"])
        await asyncio.to_thread(client.delete_bucket, Bucket=bucket)
