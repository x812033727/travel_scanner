from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.admin.users import list_admin_users
from app.community.models import Comment, Post
from app.db import Base
from app.models import (
    AccountErasureRequest,
    AdminRoleAssignment,
    PriceAlert,
    SearchRequest,
    TripPlan,
    UsageAccount,
    User,
    UserAuthIdentity,
)

TABLES = [
    User.__table__,
    UsageAccount.__table__,
    SearchRequest.__table__,
    TripPlan.__table__,
    PriceAlert.__table__,
    Post.__table__,
    Comment.__table__,
    AdminRoleAssignment.__table__,
    UserAuthIdentity.__table__,
    AccountErasureRequest.__table__,
]


@pytest.mark.asyncio
async def test_user_list_aggregates_activity_and_sorts_stable_ties(tmp_path: Path) -> None:
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{(tmp_path / 'admin-user-activity.db').as_posix()}"
    )
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=TABLES))
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    base = datetime(2026, 9, 1, 9, tzinfo=UTC)
    quiet_a = User(
        id=UUID("00000000-0000-4000-8000-000000000001"),
        email="quiet-a@example.com",
        password_hash="unused",
        created_at=base,
        updated_at=base,
    )
    quiet_b = User(
        id=UUID("00000000-0000-4000-8000-000000000002"),
        email="quiet-b@example.com",
        password_hash="unused",
        created_at=base,
        updated_at=base,
    )
    active = User(
        id=UUID("00000000-0000-4000-8000-000000000003"),
        email="active@example.com",
        password_hash="unused",
        created_at=base,
        updated_at=base,
    )
    actor = User(
        id=UUID("00000000-0000-4000-8000-000000000004"),
        email="owner@example.com",
        password_hash="unused",
        created_at=base,
        updated_at=base,
    )
    async with sessions() as session:
        session.add_all([quiet_a, quiet_b, active, actor])
        session.add_all(
            [
                UsageAccount(user_id=user.id, remaining_uses=3, reserved_uses=0)
                for user in (quiet_a, quiet_b, active, actor)
            ]
        )
        search = SearchRequest(
            user_id=active.id,
            operation="search",
            request_json={},
            updated_at=base + timedelta(hours=1),
        )
        trip = TripPlan(
            user_id=active.id,
            name="Tokyo",
            mode="manual",
            total_price=Decimal("0"),
            data={},
            updated_at=base + timedelta(hours=2),
        )
        post = Post(
            author_id=active.id,
            updated_at=base + timedelta(hours=3),
        )
        session.add_all([search, trip, post])
        await session.flush()
        session.add_all(
            [
                PriceAlert(
                    user_id=active.id,
                    resource_type="trip",
                    resource_id=trip.id,
                    updated_at=base + timedelta(hours=4),
                ),
                Comment(
                    post_id=post.id,
                    author_id=active.id,
                    body="Useful",
                    locale="en",
                    updated_at=base + timedelta(hours=5),
                ),
            ]
        )
        await session.commit()

        listed = await list_admin_users(
            session,
            actor,
            None,
            1,
            20,
            sort="activity_count",
            direction="asc",
        )
        assert [item.id for item in listed.items] == [quiet_a.id, quiet_b.id, actor.id, active.id]
        active_item = listed.items[-1]
        assert active_item.activity.model_dump() == {
            "trips": 1,
            "searches": 1,
            "alerts": 1,
            "community_posts": 1,
            "community_comments": 1,
        }
        assert active_item.last_activity_at is not None
        assert active_item.last_activity_at.replace(tzinfo=UTC) == base + timedelta(hours=5)
        assert listed.items[0].activity.model_dump() == {
            "trips": 0,
            "searches": 0,
            "alerts": 0,
            "community_posts": 0,
            "community_comments": 0,
        }
        assert listed.items[0].last_activity_at is None

        inactive_only = await list_admin_users(
            session,
            actor,
            None,
            1,
            20,
            activity="no_activity",
            sort="activity_count",
            direction="asc",
        )
        assert [item.id for item in inactive_only.items] == [quiet_a.id, quiet_b.id, actor.id]
        assert inactive_only.total == 3

        active_only = await list_admin_users(
            session,
            actor,
            None,
            1,
            20,
            activity="has_activity",
            sort="last_activity_at",
            direction="desc",
        )
        assert [item.id for item in active_only.items] == [active.id]
        assert active_only.total == 1

    await engine.dispose()
