from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any, cast
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError
from sqlalchemy import Table, func, select, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.admin.listing import HOTSPOT_CATEGORY_ORDER
from app.db import Base
from app.hotspots.admin_router import (
    HotspotReviewRequest,
    list_hotspot_candidates,
    review_hotspot_candidates,
)
from app.models import (
    AdminAuditLog,
    HotspotSignal,
    HotspotTheme,
    HotspotThemeLink,
    TravelHotspot,
    User,
)
from app.problems import AppError

STAMP = datetime(2026, 9, 10, 1, 0, 0, 123456, tzinfo=UTC)


@pytest.fixture
async def session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite://")
    tables = [
        cast(Table, model.__table__)
        for model in (
            User,
            TravelHotspot,
            AdminAuditLog,
            HotspotSignal,
            HotspotTheme,
            HotspotThemeLink,
        )
    ]
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    async with async_sessionmaker(engine, expire_on_commit=False)() as value:
        yield value
    await engine.dispose()


def actor() -> User:
    return User(id=uuid4(), email="review-editor@example.test", is_admin=True)


def hotspot(**changes: Any) -> TravelHotspot:
    identity = uuid4()
    return TravelHotspot(
        **{
            "id": identity,
            "slug": f"editor-{identity}",
            "name": "Review fixture",
            "destination_id": "taipei",
            "city_code": "TPE",
            "city_name": "Taipei",
            "country_code": "TW",
            "country_name": "Taiwan",
            "category": "culture",
            "search_text": "Review fixture",
            "review_status": "pending",
            "is_active": False,
            "metadata_json": {},
            "source_urls": [],
            "map_match_status": "unverified",
            "updated_at": STAMP,
            **changes,
        }
    )


def payload(row: TravelHotspot, **changes: Any) -> HotspotReviewRequest:
    return HotspotReviewRequest.model_validate(
        {"ids": [str(row.id)], "action": "update", **changes}
    )


async def audit_count(session: AsyncSession) -> int:
    return int(await session.scalar(select(func.count(AdminAuditLog.id))) or 0)


@pytest.mark.parametrize("category", HOTSPOT_CATEGORY_ORDER)
def test_all_existing_categories_are_valid(category: str) -> None:
    assert payload(hotspot(), category=category).category == category


@pytest.mark.parametrize("category", ["sports", "unknown", "", None])
def test_invalid_or_cleared_category_is_rejected(category: str | None) -> None:
    with pytest.raises(ValidationError):
        payload(hotspot(), category=category)


@pytest.mark.parametrize("qid", ["Q0", "Q01", "q123", " Q123", "Q123 ", "https://x/Q123", "Q1x"])
def test_invalid_qid_is_rejected(qid: str) -> None:
    with pytest.raises(ValidationError):
        payload(hotspot(), wikidata_item_id=qid)


@pytest.mark.parametrize("field", [{"category": "nature"}, {"wikidata_item_id": "Q123"}])
def test_identity_fields_are_update_only_and_single_entity(field: dict[str, str]) -> None:
    row = hotspot()
    with pytest.raises(ValidationError):
        payload(row, action="approve", **field)
    with pytest.raises(ValidationError):
        payload(row, ids=[str(row.id), str(uuid4())], **field)


@pytest.mark.parametrize(
    "changes",
    [
        {"expected_updated_at": None},
        {"expected_updated_at": "2026-09-10T01:00:00"},
        {"expected_updated_at": STAMP, "action": "approve"},
        {"expected_updated_ats": {}},
        {"expected_updated_ats": None, "action": "reject"},
        {"expected_updated_ats": {str(uuid4()): STAMP}, "action": "reject"},
    ],
)
def test_version_shape_is_strict_when_supplied(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        payload(hotspot(), **changes)


async def test_fill_identity_and_category_preserves_pending_and_audits(
    session: AsyncSession,
) -> None:
    row = hotspot(
        review_reason="old rationale", latitude=Decimal("25.1"), longitude=Decimal("121.1")
    )
    session.add(row)
    await session.commit()
    result = await review_hotspot_candidates(
        payload(
            row,
            category="nature",
            wikidata_item_id="Q12345",
            reason="Official park: https://parks.example.test/12345",
            expected_updated_at=STAMP,
        ),
        actor(),
        session,
    )
    assert result == {"updated": 1, "status": "pending"}
    await session.refresh(row)
    assert (row.review_status, row.is_active, row.map_match_status) == (
        "pending",
        False,
        "unverified",
    )
    assert (row.latitude, row.longitude) == (Decimal("25.100000"), Decimal("121.100000"))
    assert row.coordinate_verified_at is None
    assert row.map_verified_at is None
    assert (row.category, row.wikidata_item_id) == ("nature", "Q12345")
    audit = await session.scalar(select(AdminAuditLog))
    assert audit is not None
    assert audit.metadata_json["identity_changes"] == [
        {
            "id": str(row.id),
            "before": {"category": "culture", "wikidata_item_id": None, "reason": "old rationale"},
            "after": {
                "category": "nature",
                "wikidata_item_id": "Q12345",
                "reason": "Official park: https://parks.example.test/12345",
            },
        }
    ]
    listing = await list_hotspot_candidates(actor(), session, locale="zh-TW")
    items = cast(list[dict[str, Any]], listing["items"])
    assert items[0]["updated_at"] == row.updated_at.isoformat()
    assert items[0]["qid"] == "Q12345"


@pytest.mark.parametrize("changes", [{"category": "nature"}, {"wikidata_item_id": "Q123"}])
@pytest.mark.parametrize("reason", [None, "", "   "])
async def test_identity_change_requires_nonblank_rationale(
    session: AsyncSession, changes: dict[str, str], reason: str | None
) -> None:
    row = hotspot()
    session.add(row)
    await session.commit()
    with pytest.raises(AppError) as error:
        await review_hotspot_candidates(payload(row, reason=reason, **changes), actor(), session)
    assert error.value.code == "hotspot_review_reason_required"
    assert (row.category, row.wikidata_item_id) == ("culture", None)
    assert await audit_count(session) == 0


@pytest.mark.parametrize("qid", ["Q77", "Q88", None])
async def test_existing_identity_cannot_be_replaced_cleared_or_reapplied(
    session: AsyncSession, qid: str | None
) -> None:
    row = hotspot(wikidata_item_id="Q77")
    session.add(row)
    await session.commit()
    with pytest.raises(AppError) as error:
        await review_hotspot_candidates(
            payload(row, wikidata_item_id=qid, reason="Source evidence"), actor(), session
        )
    assert error.value.status == 409
    assert error.value.code == "hotspot_wikidata_identity_locked"
    assert row.wikidata_item_id == "Q77"
    assert await audit_count(session) == 0


async def test_duplicate_identity_conflicts_without_any_mutation(session: AsyncSession) -> None:
    row = hotspot()
    duplicate = hotspot(wikidata_item_id="Q99")
    session.add_all([row, duplicate])
    await session.commit()
    with pytest.raises(AppError) as error:
        await review_hotspot_candidates(
            payload(row, wikidata_item_id="Q99", category="nature", reason="Source"),
            actor(),
            session,
        )
    assert error.value.code == "hotspot_wikidata_identity_exists"
    assert row.wikidata_item_id is None and row.category == "culture"
    assert await audit_count(session) == 0


async def test_blank_existing_identity_can_be_filled(session: AsyncSession) -> None:
    row = hotspot(wikidata_item_id=" ")
    session.add(row)
    await session.commit()
    await review_hotspot_candidates(
        payload(row, wikidata_item_id="Q123", reason="Confirmed source"), actor(), session
    )
    assert row.wikidata_item_id == "Q123"


async def test_null_fill_is_not_an_identity_clear_operation(session: AsyncSession) -> None:
    row = hotspot()
    session.add(row)
    await session.commit()
    with pytest.raises(AppError) as error:
        await review_hotspot_candidates(payload(row, wikidata_item_id=None), actor(), session)
    assert error.value.code == "hotspot_wikidata_identity_required"
    assert await audit_count(session) == 0


async def test_stale_update_and_complete_batch_conflict_before_first_write(
    session: AsyncSession,
) -> None:
    rows = [
        hotspot(id=UUID(int=1)),
        hotspot(id=UUID(int=2), updated_at=STAMP + timedelta(seconds=1)),
    ]
    session.add_all(rows)
    await session.commit()
    stale_batch = HotspotReviewRequest.model_validate(
        {
            "ids": [str(row.id) for row in reversed(rows)],
            "action": "reject",
            "reason": "Scope evidence",
            "expected_updated_ats": {str(row.id): STAMP for row in rows},
        }
    )
    with pytest.raises(AppError) as error:
        await review_hotspot_candidates(stale_batch, actor(), session)
    assert error.value.status == 409 and error.value.code == "hotspot_review_conflict"
    assert all(row.review_status == "pending" and not session.is_modified(row) for row in rows)
    assert await audit_count(session) == 0
    with pytest.raises(AppError) as single:
        await review_hotspot_candidates(
            payload(rows[1], expected_updated_at=STAMP, reason="new"), actor(), session
        )
    assert single.value.code == "hotspot_review_conflict"
    assert await audit_count(session) == 0


async def test_matched_batch_versions_allow_all_decisions(session: AsyncSession) -> None:
    rows = [hotspot(), hotspot()]
    session.add_all(rows)
    await session.commit()
    result = await review_hotspot_candidates(
        HotspotReviewRequest.model_validate(
            {
                "ids": [str(row.id) for row in rows],
                "action": "reject",
                "reason": "Exact administrative scope source",
                "expected_updated_ats": {str(row.id): STAMP for row in rows},
            }
        ),
        actor(),
        session,
    )
    assert result == {"updated": 2, "status": "rejected"}
    assert all(row.review_status == "rejected" and not row.is_active for row in rows)
    assert await audit_count(session) == 1


async def test_legacy_reason_update_preserves_status_and_omitted_reason(
    session: AsyncSession,
) -> None:
    row = hotspot(review_status="rejected", review_reason="before")
    session.add(row)
    await session.commit()
    await review_hotspot_candidates(payload(row, reason="Source URL"), actor(), session)
    assert (row.review_reason, row.review_status, row.is_active) == (
        "Source URL",
        "rejected",
        False,
    )
    await review_hotspot_candidates(payload(row), actor(), session)
    assert row.review_reason == "Source URL"
    await review_hotspot_candidates(payload(row, reason=None), actor(), session)
    assert row.review_reason is None
    await review_hotspot_candidates(payload(row, action="disable"), actor(), session)
    assert row.review_status == "disabled" and not row.is_active


@pytest.mark.parametrize("action", ["approve", "reject", "disable"])
@pytest.mark.parametrize(
    "reason_update",
    [{}, {"reason": "Explicit replacement source"}, {"reason": None}],
    ids=["omitted-preserves", "replacement", "explicit-null-clears"],
)
async def test_decision_reason_presence_preserves_each_row_and_audits(
    session: AsyncSession, action: str, reason_update: dict[str, str | None]
) -> None:
    rows = [
        hotspot(
            wikidata_item_id=f"Q{index}",
            review_reason=f"Independent source {index}",
            map_match_status="verified",
            google_place_id=f"ChIJ-fixture-{index}",
            latitude=Decimal("25.1"),
            longitude=Decimal("121.1"),
            coordinate_source_type="wikidata",
            coordinate_source_url=f"https://www.wikidata.org/wiki/Q{index}",
            map_verified_at=STAMP,
            coordinate_verified_at=STAMP,
        )
        for index in (1, 2)
    ]
    session.add_all(rows)
    await session.commit()
    before = {
        str(row.id): {
            "category": row.category,
            "wikidata_item_id": row.wikidata_item_id,
            "reason": row.review_reason,
        }
        for row in rows
    }
    request = HotspotReviewRequest.model_validate(
        {
            "ids": [str(row.id) for row in rows],
            "action": action,
            "expected_updated_ats": {str(row.id): STAMP for row in rows},
            **reason_update,
        }
    )
    result = await review_hotspot_candidates(request, actor(), session)
    status = {"approve": "approved", "reject": "rejected", "disable": "disabled"}[action]
    assert result == {"updated": 2, "status": status}
    for row in rows:
        await session.refresh(row)
        expected_reason = reason_update.get("reason", before[str(row.id)]["reason"])
        assert row.review_reason == expected_reason
        assert (row.review_status, row.is_active) == (status, action == "approve")
    assert await audit_count(session) == 1
    audit = await session.scalar(select(AdminAuditLog))
    assert audit is not None
    assert audit.metadata_json["action"] == action
    assert {
        change["id"]: {"before": change["before"], "after": change["after"]}
        for change in audit.metadata_json["identity_changes"]
    } == {
        str(row.id): {
            "before": before[str(row.id)],
            "after": {**before[str(row.id)], "reason": row.review_reason},
        }
        for row in rows
    }


@pytest.mark.parametrize(
    ("fields", "code"),
    [
        ({}, "map_verification_required"),
        ({"map_match_status": "verified"}, "exact_map_identity_required"),
        (
            {"map_match_status": "verified", "google_place_id": "ChIJ-fixture"},
            "permanent_coordinates_required",
        ),
        (
            {
                "map_match_status": "verified",
                "google_place_id": "ChIJ-fixture",
                "latitude": 25.1,
                "longitude": 121.1,
            },
            "coordinate_source_required",
        ),
    ],
)
async def test_approval_map_and_coordinate_guards_remain(
    session: AsyncSession, fields: dict[str, Any], code: str
) -> None:
    row = hotspot(wikidata_item_id="Q100")
    session.add(row)
    await session.commit()
    with pytest.raises(AppError) as error:
        await review_hotspot_candidates(payload(row, action="approve", **fields), actor(), session)
    assert error.value.code == code
    assert row.review_status == "pending"
    assert await audit_count(session) == 0


async def test_existing_complete_map_can_still_be_approved(session: AsyncSession) -> None:
    row = hotspot(
        wikidata_item_id="Q100",
        map_match_status="verified",
        google_place_id="ChIJ-fixture",
        latitude=Decimal("25.1"),
        longitude=Decimal("121.1"),
        coordinate_source_type="wikidata",
        coordinate_source_url="https://www.wikidata.org/wiki/Q100",
        map_verified_at=STAMP,
        coordinate_verified_at=STAMP,
    )
    session.add(row)
    await session.commit()
    await review_hotspot_candidates(payload(row, action="approve"), actor(), session)
    assert row.review_status == "approved" and row.is_active


async def test_query_locks_in_stable_order(
    session: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = session.scalars
    statements: list[str] = []

    async def capture(statement: Any, *args: Any, **kwargs: Any) -> Any:
        statements.append(str(statement.compile(dialect=cast(Any, postgresql.dialect)())))
        return await original(statement, *args, **kwargs)

    monkeypatch.setattr(session, "scalars", capture)
    row = hotspot()
    session.add(row)
    await session.commit()
    await review_hotspot_candidates(payload(row), actor(), session)
    assert "ORDER BY travel_hotspots.id FOR UPDATE" in statements[0]


async def test_concurrent_unique_constraint_is_rolled_back_and_redacted(
    session: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    row = hotspot()
    session.add(row)
    await session.commit()
    monkeypatch.setattr(
        session,
        "commit",
        AsyncMock(
            side_effect=IntegrityError("hidden SQL", {}, Exception("UNIQUE wikidata_item_id"))
        ),
    )
    with pytest.raises(AppError) as error:
        await review_hotspot_candidates(
            payload(row, wikidata_item_id="Q321", reason="Source"), actor(), session
        )
    assert error.value.code == "hotspot_wikidata_identity_exists"
    await session.refresh(row)
    assert row.wikidata_item_id is None
    assert await audit_count(session) == 0


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
async def test_postgres_stale_writer_waits_and_competing_qid_fill_is_unique() -> None:
    from app.config import get_settings

    schema = "hotspot_identity_editor_" + uuid4().hex
    administrator = create_async_engine(get_settings().database_url)
    async with administrator.begin() as connection:
        await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
    engine = create_async_engine(
        get_settings().database_url, connect_args={"server_settings": {"search_path": schema}}
    )
    try:
        async with engine.begin() as connection:
            await connection.run_sync(
                lambda sync: Base.metadata.create_all(
                    sync,
                    tables=[
                        cast(Table, model.__table__)
                        for model in (User, TravelHotspot, AdminAuditLog)
                    ],
                )
            )
        factory = async_sessionmaker(engine, expire_on_commit=False)
        user = actor()
        row = hotspot()
        async with factory() as setup:
            setup.add_all([user, row])
            await setup.commit()
        async with factory() as winner, factory() as loser:
            # The loser has an old identity-map object even before its locking read.
            stale = await loser.get(TravelHotspot, row.id)
            assert stale is not None
            locked = await winner.scalar(
                select(TravelHotspot).where(TravelHotspot.id == row.id).with_for_update()
            )
            assert locked is not None
            locked.review_reason = "Concurrent winner"
            locked.updated_at = STAMP + timedelta(seconds=1)
            await winner.flush()
            waiting = asyncio.create_task(
                review_hotspot_candidates(
                    payload(row, reason="Stale writer", expected_updated_at=STAMP), user, loser
                )
            )
            try:
                done, _ = await asyncio.wait({waiting}, timeout=0.1)
                assert not done
                await winner.commit()
                with pytest.raises(AppError) as conflict:
                    await asyncio.wait_for(waiting, timeout=5)
                assert conflict.value.code == "hotspot_review_conflict"
                await loser.rollback()
            finally:
                if not waiting.done():
                    waiting.cancel()
                    await asyncio.gather(waiting, return_exceptions=True)
            assert await audit_count(loser) == 0
            await loser.refresh(stale)
            assert stale.review_reason == "Concurrent winner"

        targets = [hotspot(), hotspot()]
        async with factory() as setup:
            setup.add_all(targets)
            await setup.commit()

        async def fill(target: TravelHotspot) -> dict[str, int | str]:
            async with factory() as worker:
                return await review_hotspot_candidates(
                    payload(target, wikidata_item_id="Q999", reason="Independent source"),
                    user,
                    worker,
                )

        outcomes = await asyncio.gather(
            *(fill(target) for target in targets), return_exceptions=True
        )
        assert sum(isinstance(outcome, dict) for outcome in outcomes) == 1
        conflicts = [outcome for outcome in outcomes if isinstance(outcome, AppError)]
        assert len(conflicts) == 1 and conflicts[0].code == "hotspot_wikidata_identity_exists"
        async with factory() as check:
            assert await audit_count(check) == 1
            assert (
                await check.scalar(
                    select(func.count(TravelHotspot.id)).where(
                        TravelHotspot.wikidata_item_id == "Q999"
                    )
                )
                == 1
            )
    finally:
        await engine.dispose()
        async with administrator.begin() as connection:
            await connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        await administrator.dispose()
