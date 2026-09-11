import json
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest
from sqlalchemy import select
from test_discovery_flow import seed_reservation_merchant
from test_travel_discovery import harness as harness

from app.foods.platform_links import serialize_reservation_link
from app.foods.platform_review_import import (
    AUDIT_ACTION,
    DEFAULT_REVIEW_FILE,
    ReviewFileError,
    apply_platform_reviews,
    load_review_file,
    summarize,
)
from app.models import AdminAuditLog, FoodMerchantPlatformLink

SEVENROOMS = "https://www.sevenrooms.com/reservations/mokaair-fixture"
EVIDENCE = [{
    "url": "https://restaurant.example.com/branch",
    "role": "owner_reservations",
    "observation": "The owner links this venue page.",
}]


def write_batch(tmp_path: Path, records: list[dict[str, Any]]) -> Path:
    path = tmp_path / "review.json"
    path.write_text(json.dumps({
        "schema_version": 1,
        "batch_id": "test-batch",
        "researched_at": "2026-09-12T00:00:00+00:00",
        "records": records,
    }), encoding="utf-8")
    return path


def record(merchant: Any, **overrides: Any) -> dict[str, Any]:
    return {
        "merchant_id": str(merchant.id),
        "slug": merchant.slug,
        "provider": "sevenrooms",
        "status": "verified",
        "canonical_url": SEVENROOMS,
        "review_note": "Owner links this SevenRooms venue page.",
        "evidence": EVIDENCE,
    } | overrides


def not_found(merchant: Any) -> dict[str, Any]:
    return record(
        merchant, provider="tablecheck", status="not_found", canonical_url=None,
        review_note="Searched TableCheck and ikyu; no page for this branch.", evidence=[],
    )


@pytest.mark.asyncio
async def test_dry_run_writes_nothing_and_apply_writes_one_audited_public_row(
    harness: Any, tmp_path: Path
) -> None:
    _, factory, _, _, _ = harness
    _, merchant = await seed_reservation_merchant(factory)
    batch = load_review_file(write_batch(tmp_path, [record(merchant)]))
    async with factory() as session:
        dry = await apply_platform_reviews(session, batch, apply=False)
        assert [item.action for item in dry] == ["would_create"]
        assert summarize(batch, dry, apply=False)["statuses"] == {"verified": 1}
        assert len((await session.scalars(select(FoodMerchantPlatformLink))).all()) == 1
        assert not (await session.scalars(select(AdminAuditLog))).all()

        applied = await apply_platform_reviews(session, batch, apply=True)
        assert [item.action for item in applied] == ["created"]
        row = await session.scalar(
            select(FoodMerchantPlatformLink).where(
                FoodMerchantPlatformLink.provider == "sevenrooms"
            )
        )
        assert row is not None and row.checked_by_user_id is None
        public = serialize_reservation_link(row, country_code="JP", locale="en")
        assert public is not None and public["url"] == SEVENROOMS
        audit = (await session.scalars(select(AdminAuditLog))).one()
        assert audit.action == AUDIT_ACTION and audit.actor_user_id is None
        assert audit.target == f"food_merchant:{merchant.id}"
        assert audit.metadata_json["canonical_url"] == SEVENROOMS
        assert audit.metadata_json["previous"] is None

        again = await apply_platform_reviews(session, batch, apply=True)
        assert [item.action for item in again] == ["unchanged"]
        assert len((await session.scalars(select(AdminAuditLog))).all()) == 1


@pytest.mark.asyncio
async def test_batch_updates_unreviewed_rows_but_needs_the_version_of_an_admin_review(
    harness: Any, tmp_path: Path
) -> None:
    _, factory, users, _, _ = harness
    seeded_at = datetime(2026, 9, 8, tzinfo=UTC)
    reviewed_at = datetime(2026, 9, 11, 12, 0, tzinfo=UTC)
    _, unreviewed = await seed_reservation_merchant(
        factory, status="ambiguous", canonical_url=None, checked_at=seeded_at
    )
    _, reviewed = await seed_reservation_merchant(
        factory, canonical_url="https://www.tablecheck.com/en/shops/second-fixture/reserve",
        checked_at=reviewed_at, checked_by_user_id=users[0],
    )
    pinned_url = "https://www.tablecheck.com/en/shops/third-fixture/reserve"
    _, pinned = await seed_reservation_merchant(
        factory, canonical_url=pinned_url, checked_at=reviewed_at, checked_by_user_id=users[0]
    )
    batch = load_review_file(write_batch(tmp_path, [
        not_found(unreviewed),
        not_found(reviewed),
        record(
            pinned, provider="tablecheck", status="disabled", canonical_url=pinned_url,
            review_note="The branch page says it no longer takes bookings.",
            expected_checked_at=reviewed_at.isoformat(),
        ),
    ]))
    async with factory() as session:
        outcomes = await apply_platform_reviews(session, batch, apply=True)
        assert [item.action for item in outcomes] == [
            "updated", "skipped_admin_reviewed", "updated",
        ]
        rows = {
            row.merchant_id: row
            for row in (await session.scalars(select(FoodMerchantPlatformLink))).all()
        }
        assert rows[unreviewed.id].status == "not_found"
        assert rows[reviewed.id].status == "verified"
        assert rows[reviewed.id].checked_by_user_id == users[0]
        assert rows[pinned.id].status == "disabled"
        assert serialize_reservation_link(rows[pinned.id], country_code="JP", locale="en") is None
        audits = (await session.scalars(select(AdminAuditLog))).all()
        assert sorted(audit.metadata_json["previous"]["status"] for audit in audits) == [
            "ambiguous", "verified",
        ]

        rerun = await apply_platform_reviews(session, batch, apply=True)
        assert [item.action for item in rerun] == [
            "unchanged", "skipped_admin_reviewed", "skipped_changed_since_research",
        ]


@pytest.mark.asyncio
async def test_branch_conflicts_and_identity_mismatches_write_nothing(
    harness: Any, tmp_path: Path
) -> None:
    _, factory, _, _, _ = harness
    _, owner = await seed_reservation_merchant(factory)
    other_url = "https://www.tablecheck.com/en/shops/other-fixture/reserve"
    _, other = await seed_reservation_merchant(factory, canonical_url=other_url)
    # Another route to the owner's branch: the same venue identity under a new locale path.
    alias = "https://www.tablecheck.com/ja/mokaair-fixture/reserve/message"
    missing = SimpleNamespace(id=uuid4(), slug="gone-fixture")
    batch = load_review_file(write_batch(tmp_path, [
        record(other, provider="tablecheck", canonical_url=alias),
        record(SimpleNamespace(id=owner.id, slug="renamed-fixture")),
        record(missing, canonical_url="https://www.sevenrooms.com/reservations/missing-fixture"),
    ]))
    async with factory() as session:
        outcomes = await apply_platform_reviews(session, batch, apply=True)
        assert [item.action for item in outcomes] == [
            "skipped_branch_conflict", "skipped_slug_mismatch", "skipped_missing_merchant",
        ]
        assert outcomes[0].detail == str(owner.id)
        assert not (await session.scalars(select(AdminAuditLog))).all()
        row = await session.scalar(
            select(FoodMerchantPlatformLink).where(FoodMerchantPlatformLink.merchant_id == other.id)
        )
        assert row is not None and row.canonical_url == other_url


@pytest.mark.parametrize("change,message", [
    ({"provider": "tabelog"}, "不支援這個訂位平台"),
    ({"canonical_url": "https://www.sevenrooms.com/explore"}, "merchant-specific page"),
    ({"canonical_url": f"{SEVENROOMS}?utm_source=website"}, "unsupported query parameters"),
    ({"canonical_url": None}, "已驗證狀態必須提供精準店家頁"),
    ({"evidence": []}, "needs evidence"),
    ({"expected_checked_at": "2026-09-11T12:00:00"}, "timezone"),
])
def test_one_invalid_record_rejects_the_whole_file(
    tmp_path: Path, change: dict[str, Any], message: str
) -> None:
    good = record(
        SimpleNamespace(id=uuid4(), slug="good-fixture"),
        canonical_url="https://www.sevenrooms.com/reservations/good-fixture",
    )
    bad = record(SimpleNamespace(id=uuid4(), slug="bad-fixture")) | change
    with pytest.raises(ReviewFileError) as error:
        load_review_file(write_batch(tmp_path, [good, bad]))
    assert message in str(error.value)


def test_file_rejects_a_repeated_row_and_one_branch_for_two_merchants(tmp_path: Path) -> None:
    first = SimpleNamespace(id=uuid4(), slug="first-fixture")
    second = SimpleNamespace(id=uuid4(), slug="second-fixture")
    with pytest.raises(ReviewFileError) as repeated:
        load_review_file(write_batch(tmp_path, [record(first), record(first)]))
    assert "appear twice" in str(repeated.value)
    with pytest.raises(ReviewFileError) as shared:
        load_review_file(write_batch(tmp_path, [record(first), record(second)]))
    assert "another merchant" in str(shared.value)


def test_committed_review_file_is_valid() -> None:
    batch = load_review_file(DEFAULT_REVIEW_FILE)
    assert batch.records
    assert all(item.status != "verified" or item.evidence for item in batch.records)
