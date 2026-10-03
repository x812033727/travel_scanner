"""The one-pass CatchTable candidate importer: the file's rules, every outcome, honest dry runs.

``import-catchtable-candidates`` replaced a two-pass flow (``tools/catchtable_build_batches.py``
→ ``import-trend-merchants`` → worklist → ``apply-food-platform-reviews``), so besides its own
behaviour these tests pin that it writes what those two passes wrote for the committed batches.
SQLite only; every URL here is synthetic and nothing is fetched.
"""

from __future__ import annotations

import importlib.util
import json
from collections import Counter
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Any
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base
from app.foods.area_catalog import ALL_AREA_SEEDS
from app.foods.catchtable_import import (
    AUDIT_SOURCE,
    CandidateFileError,
    CandidateOutcome,
    import_candidate_batch,
    load_candidate_file,
    merchant_rows,
    platform_row,
    prepare_candidates,
    summarize,
)
from app.foods.category_catalog import CATEGORY_SEEDS
from app.foods.platform_review_import import AUDIT_ACTION as PLATFORM_AUDIT_ACTION
from app.foods.trend_import import AUDIT_ACTION as MERCHANT_AUDIT_ACTION
from app.models import (
    AdminAuditLog,
    FoodArea,
    FoodCategory,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantPlatformLink,
    FoodMerchantSource,
    User,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "app" / "foods" / "data" / "catchtable"
TOOL = Path(__file__).resolve().parents[3] / "tools" / "catchtable_build_batches.py"
CHECKED_AT = "2026-10-01T03:12:00+00:00"
RANKING_PAGE = "https://www.catchtable.net/zh-TW/ranking/location/location-seoul"
OBSERVATION = "2026-10-01 zh-TW 店頁：DINING 分頁有日期列與「尋找可用時間」。"
PREFIXES = {"zh-TW": "/zh-TW", "zh-CN": "/zh-CN", "ja": "/ja-JP"}


def shop(alias: str, prefix: str = "") -> str:
    return f"https://www.catchtable.net{prefix}/shop/{alias}"


def listing(alias: str, booking: str = "reservation", **extra: Any) -> dict[str, Any]:
    block: dict[str, Any] = {
        "listed_name": f"{alias} 본점",
        "listed_address": "서울 성동구 성수이로 1",
        "listed_cuisine": "韓式料理",
        "listed_area": "聖水",
        "booking": booking,
        "booking_observation": OBSERVATION if booking != "unclear" else None,
    }
    if booking != "unclear":
        block["localized_urls"] = {locale: shop(alias, p) for locale, p in PREFIXES.items()}
    return block | extra


def merchant_block(name: str, **overrides: Any) -> dict[str, Any]:
    block: dict[str, Any] = {
        "district_key": "seongsu",
        "name_zh": name,
        "name_en": "Fixture Kitchen",
        "local_name": name,
        "address_local": "서울특별시 성동구 성수이로 1",
        "category_slugs": ["home-style"],
        "source": {
            "url": "https://restaurant.example.com/seongsu",
            "title": "Fixture Kitchen official",
            "kind": "merchant_official",
            "quote": f"{name} 서울특별시 성동구 성수이로 1",
        },
    }
    return block | overrides


def record(alias: str, outcome: str = "import", **overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "alias": alias,
        "outcome": outcome,
        "checked_at": CHECKED_AT,
        "ranking_evidence": [
            {"page": RANKING_PAGE, "rank": 7, "captured_at": "2026-10-01T02:00:00+00:00"}
        ],
        "catchtable": listing(alias),
        "notes": None,
    }
    return values | overrides


def document(*records: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "batch_id": "2026-10-01-catchtable-fixture",
        "destination": "seoul",
        "collected_at": "2026-10-01T02:00:00+00:00",
        "researched_by": "test",
        "method": "synthetic",
        "rankings": [],
        "records": list(records),
    }


@pytest_asyncio.fixture
async def factory() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)
    try:
        yield maker
    finally:
        await engine.dispose()


def taxonomy(destination: str = "seoul") -> list[Any]:
    """The destination's areas and every category, as ``seed-foods`` would leave them."""
    areas: list[Any] = [
        FoodArea(
            slug=seed.slug,
            destination_id=seed.destination_id,
            country_code="KR",
            names_json=dict(seed.names),
            match_terms_json=list(seed.match_terms),
            is_active=True,
        )
        for seed in ALL_AREA_SEEDS
        if seed.destination_id == destination
    ]
    return areas + [
        FoodCategory(slug=seed.slug, names_json=dict(seed.names), is_active=True)
        for seed in CATEGORY_SEEDS
    ]


def catalog_merchant(slug: str, local_name: str) -> FoodMerchant:
    return FoodMerchant(
        id=uuid4(),
        slug=slug,
        destination_id="seoul",
        country_code="KR",
        name=local_name,
        local_name=local_name,
        review_status="approved",
        map_match_status="verified",
        is_active=True,
    )


def catchtable_row(merchant: FoodMerchant, alias: str, **values: Any) -> FoodMerchantPlatformLink:
    defaults: dict[str, Any] = {
        "merchant_id": merchant.id,
        "provider": "catchtable_global",
        "status": "verified",
        "canonical_url": shop(alias),
        "localized_urls_json": {locale: shop(alias, p) for locale, p in PREFIXES.items()},
        "review_note": "An earlier batch's note.",
        "checked_at": datetime(2026, 9, 23, tzinfo=UTC),
    }
    return FoodMerchantPlatformLink(**(defaults | values))


async def seed(maker: async_sessionmaker[AsyncSession], *rows: Any) -> None:
    async with maker() as session:
        session.add_all(rows)
        await session.commit()


async def count(maker: async_sessionmaker[AsyncSession], model: Any) -> int:
    async with maker() as session:
        return int(await session.scalar(select(func.count()).select_from(model)) or 0)


async def run(
    maker: async_sessionmaker[AsyncSession], raw: dict[str, Any], *, apply: bool, **kwargs: Any
) -> tuple[list[CandidateOutcome], dict[str, Any]]:
    prepared = prepare_candidates(raw)
    async with maker() as session:
        outcomes = await import_candidate_batch(session, prepared, apply=apply, **kwargs)
    return outcomes, summarize(prepared, outcomes, apply=apply)


def as_applied(value: Any) -> Any:
    """What a dry run's action becomes when the same run is applied."""
    return {"would_create": "created", "would_update": "updated"}.get(value, value)


def actions(outcomes: list[CandidateOutcome]) -> dict[str, tuple[Any, ...]]:
    return {o.alias: (o.merchant, o.platform, o.status) for o in outcomes}


# --- the candidate file ---------------------------------------------------------------------


def test_a_ko_url_is_refused_because_catchtable_publishes_no_korean_page() -> None:
    alias = "fixture_ko"
    urls = {locale: shop(alias, p) for locale, p in PREFIXES.items()}
    raw = document(
        record(
            alias,
            catchtable=listing(alias, localized_urls=urls | {"ko": shop(alias, "/ko")}),
            merchant=merchant_block("픽스처 식당"),
        )
    )
    with pytest.raises(CandidateFileError, match="there is no ko"):
        prepare_candidates(raw)


@pytest.mark.parametrize(
    ("kind", "url"),
    [
        ("official_tourism", "https://www.instagram.com/fixture_kitchen/"),
        ("merchant_official", "https://www.catchtable.net/zh-TW/shop/fixture_platform"),
        ("merchant_official", "https://map.naver.com/p/entry/place/12345678"),
        ("official_tourism", "https://www.tripadvisor.com/Restaurant_Review-fixture"),
    ],
)
def test_a_platform_host_is_never_an_official_source(kind: str, url: str) -> None:
    source = merchant_block("픽스처 식당")["source"] | {"kind": kind, "url": url}
    raw = document(
        record("fixture_platform", merchant=merchant_block("픽스처 식당", source=source))
    )
    with pytest.raises(CandidateFileError, match="never a source"):
        prepare_candidates(raw)


def test_merchant_platform_accepts_only_the_shops_own_page_or_the_account_it_registered() -> None:
    """The weaker merchant_platform tier (2026-09-23) needs a chain of custody: this alias's own
    CatchTable page or /info tab, or exactly the URL its /info tab lists as the website."""
    alias = "fixture_platform"
    registered = "https://www.instagram.com/fixture_kitchen/"

    def candidate(url: str, website: str | None = None) -> dict[str, Any]:
        source = {
            "url": url,
            "title": "CatchTable：픽스처 식당",
            "kind": "merchant_platform",
            "quote": "픽스처 식당 서울특별시 성동구 성수이로 1",
        }
        block = listing(alias, website=website) if website else listing(alias)
        return document(
            record(alias, catchtable=block, merchant=merchant_block("픽스처 식당", source=source))
        )

    own_info = prepare_candidates(candidate(shop(alias, "/zh-TW") + "/info"))
    assert merchant_rows(own_info.candidates)[0]["source_kind"] == "merchant_platform"
    assert prepare_candidates(candidate(registered, website=registered)).merchants
    for url, website in [
        ("https://www.instagram.com/explore/locations/183777154813291/", registered),
        (registered, None),
        (shop("someone_else"), None),
    ]:
        with pytest.raises(CandidateFileError, match="catchtable.website"):
            prepare_candidates(candidate(url, website=website))


def test_a_naver_page_in_the_candidate_file_is_refused_not_imported() -> None:
    """Whether a candidate file may carry the Naver place page is the design document's open
    question 2; until the owner decides, the schema refuses the field rather than drop it."""
    block = merchant_block("픽스처 식당") | {
        "naver_map_url": "https://map.naver.com/p/entry/place/12345678"
    }
    with pytest.raises(CandidateFileError, match="naver_map_url"):
        prepare_candidates(document(record("fixture_naver", merchant=block)))


def test_every_problem_in_the_file_is_reported_at_once() -> None:
    raw = document(
        record("fixture_one", merchant=merchant_block("하나", category_slugs=["bubble-tea"])),
        record("fixture_two", outcome="duplicate", duplicate_of=None),
        record("fixture_three", outcome="no_official_source", merchant=merchant_block("셋")),
    )
    with pytest.raises(CandidateFileError) as raised:
        prepare_candidates(raw)
    message = str(raised.value)
    assert "records[0] fixture_one" in message and "unknown categories" in message
    assert "records[1] fixture_two" in message and "duplicate_of is required" in message
    assert "records[2] fixture_three" in message and "must not carry a merchant" in message


def test_the_importers_own_rules_run_before_any_session_opens() -> None:
    """A row the trend importer would refuse fails the whole file at load, not on the host:
    here a slug the curated catalog already uses for a different shop."""
    raw = document(
        record("fixture_one", merchant=merchant_block("하나", slug="seoul-korea-house")),
    )
    with pytest.raises(CandidateFileError, match="curated catalog"):
        prepare_candidates(raw)
    twice = document(
        record("fixture_one", merchant=merchant_block("하나", slug="seoul-same")),
        record("fixture_two", merchant=merchant_block("둘", slug="seoul-same")),
    )
    with pytest.raises(CandidateFileError, match="appears twice"):
        prepare_candidates(twice)


# --- writing --------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_every_outcome_and_a_dry_run_shaped_like_the_apply(
    factory: async_sessionmaker[AsyncSession],
) -> None:
    listed = catalog_merchant("seoul-fixture-listed", "목록 식당")
    await seed(factory, *taxonomy(), listed)
    raw = document(
        record(
            "fixture_seongsu",
            merchant=merchant_block("성수 식당", slug="seoul-fixture-seongsu"),
        ),
        record(
            "fixture_waiting",
            catchtable=listing("fixture_waiting", booking="waiting_only"),
            merchant=merchant_block("줄서는 식당", district_key=None),
        ),
        record(
            "fixture_closed",
            catchtable=listing("fixture_closed", booking="unclear"),
            merchant=merchant_block("휴무 식당"),
        ),
        record("fixture_listed", outcome="duplicate", duplicate_of="seoul-fixture-listed"),
        record("fixture_no_source", outcome="no_official_source"),
        record("fixture_bar", outcome="not_a_restaurant"),
        record("fixture_unclear", outcome="unclear", catchtable=listing("x", booking="unclear")),
    )

    dry, dry_report = await run(factory, raw, apply=False)
    assert actions(dry) == {
        "fixture_seongsu": ("would_create", "would_create", "verified"),
        "fixture_waiting": ("would_create", "would_create", "disabled"),
        "fixture_closed": ("would_create", None, None),
        "fixture_listed": (None, "would_create", "verified"),
        "fixture_no_source": (None, None, None),
        "fixture_bar": (None, None, None),
        "fixture_unclear": (None, None, None),
    }
    assert [o.detail for o in dry][2:] == [
        "booking unclear: no platform row",
        None,
        "nothing to write",
        "nothing to write",
        "nothing to write",
    ]
    assert dry_report["statuses"] == {"disabled": 1, "verified": 2}
    assert await count(factory, FoodMerchant) == 1
    assert await count(factory, FoodMerchantPlatformLink) == 0
    assert await count(factory, AdminAuditLog) == 0

    applied, applied_report = await run(factory, raw, apply=True)
    assert {
        alias: tuple(as_applied(value) for value in row) for alias, row in actions(dry).items()
    } == actions(applied)
    assert applied_report.keys() == dry_report.keys()
    for key in ("merchants", "platform_rows"):
        assert {as_applied(k): v for k, v in dry_report[key].items()} == applied_report[key]
    assert applied_report["statuses"] == dry_report["statuses"]

    async with factory() as session:
        created = {
            row.slug: row
            for row in (
                await session.scalars(select(FoodMerchant).where(FoodMerchant.id != listed.id))
            ).all()
        }
        assert sorted(created) == [
            "seoul-fixture-closed",
            "seoul-fixture-seongsu",
            "seoul-fixture-waiting",
        ]
        for row in created.values():
            # Never coordinates, a Naver page, a map identity or a review decision.
            assert (row.review_status, row.is_active, row.map_match_status) == (
                "pending",
                False,
                "unverified",
            )
            assert row.naver_map_url is None and row.google_place_id is None
            assert row.latitude is None and row.longitude is None
        area = await session.get(FoodArea, created["seoul-fixture-seongsu"].area_id)
        assert area is not None and area.slug == "seoul-seongsu"
        assert created["seoul-fixture-waiting"].area_id is None
        sources = (await session.scalars(select(FoodMerchantSource))).all()
        assert {(s.source_type, s.source_scope) for s in sources} == {
            ("merchant_official", "merchant_website")
        }
        assert len((await session.scalars(select(FoodMerchantCategory))).all()) == 3

        links = {
            row.merchant_id: row
            for row in (await session.scalars(select(FoodMerchantPlatformLink))).all()
        }
        seongsu = links[created["seoul-fixture-seongsu"].id]
        assert (seongsu.status, seongsu.canonical_url) == ("verified", shop("fixture_seongsu"))
        assert sorted(seongsu.localized_urls_json or {}) == ["ja", "zh-CN", "zh-TW"]
        assert seongsu.checked_by_user_id is None
        assert links[created["seoul-fixture-waiting"].id].status == "disabled"
        assert created["seoul-fixture-closed"].id not in links
        assert links[listed.id].status == "verified"
        listed_row = await session.get(FoodMerchant, listed.id)
        assert listed_row is not None and listed_row.review_status == "approved"

        audits = (await session.scalars(select(AdminAuditLog))).all()
        by_action = Counter(audit.action for audit in audits)
        assert by_action == {MERCHANT_AUDIT_ACTION: 3, PLATFORM_AUDIT_ACTION: 3}
        for audit in audits:
            assert audit.actor_user_id is None
            assert audit.metadata_json["source"] == AUDIT_SOURCE
            assert audit.metadata_json["ranking_evidence"] == [
                {"page": RANKING_PAGE, "rank": 7, "captured_at": "2026-10-01T02:00:00+00:00"}
            ]
        merchant_audit = next(
            a for a in audits if a.target == f"food_merchant:{created['seoul-fixture-seongsu'].id}"
            and a.action == MERCHANT_AUDIT_ACTION
        )
        assert merchant_audit.metadata_json["alias"] == "fixture_seongsu"
        assert merchant_audit.metadata_json["slug"] == "seoul-fixture-seongsu"
        listed_audit = next(a for a in audits if a.target == f"food_merchant:{listed.id}")
        assert listed_audit.action == PLATFORM_AUDIT_ACTION
        assert listed_audit.metadata_json["alias"] == "fixture_listed"
        assert listed_audit.metadata_json["batch_id"] == "2026-10-01-catchtable-fixture-platforms"

    again, _ = await run(factory, raw, apply=True)
    assert actions(again) == {
        "fixture_seongsu": ("skipped_existing_slug", "unchanged", "verified"),
        "fixture_waiting": ("skipped_existing_slug", "unchanged", "disabled"),
        "fixture_closed": ("skipped_existing_slug", None, None),
        "fixture_listed": (None, "unchanged", "verified"),
        "fixture_no_source": (None, None, None),
        "fixture_bar": (None, None, None),
        "fixture_unclear": (None, None, None),
    }
    assert await count(factory, AdminAuditLog) == 6


@pytest.mark.asyncio
async def test_an_existing_merchants_platform_row_is_protected(
    factory: async_sessionmaker[AsyncSession],
) -> None:
    admin = User(id=uuid4(), email="admin@example.com")
    reviewed = catalog_merchant("seoul-fixture-reviewed", "검토 식당")
    earlier = catalog_merchant("seoul-fixture-earlier", "이전 식당")
    changed = catalog_merchant("seoul-fixture-changed", "변경 식당")
    await seed(
        factory,
        admin,
        reviewed,
        earlier,
        changed,
        catchtable_row(
            reviewed, "fixture_reviewed", status="disabled", checked_by_user_id=admin.id
        ),
        catchtable_row(earlier, "fixture_earlier"),
        catchtable_row(changed, "fixture_changed", status="disabled"),
    )
    raw = document(
        record("fixture_reviewed", outcome="duplicate", duplicate_of="seoul-fixture-reviewed"),
        record("fixture_earlier", outcome="duplicate", duplicate_of="seoul-fixture-earlier"),
        record("fixture_changed", outcome="duplicate", duplicate_of="seoul-fixture-changed"),
        record("fixture_gone", outcome="duplicate", duplicate_of="seoul-fixture-gone"),
    )
    outcomes, report = await run(factory, raw, apply=True)
    assert actions(outcomes) == {
        # An administrator's review is never overwritten by a batch.
        "fixture_reviewed": (None, "skipped_admin_reviewed", None),
        # An earlier batch's row with the same link keeps its own note and evidence.
        "fixture_earlier": (None, "unchanged", "verified"),
        # A row nobody reviewed whose link changed is updated, as apply-food-platform-reviews does.
        "fixture_changed": (None, "updated", "verified"),
        "fixture_gone": (None, "skipped_missing_merchant", None),
    }
    assert [item["alias"] for item in report["skipped"]] == ["fixture_reviewed", "fixture_gone"]
    async with factory() as session:
        rows = {
            row.merchant_id: row
            for row in (await session.scalars(select(FoodMerchantPlatformLink))).all()
        }
        assert (rows[reviewed.id].status, rows[reviewed.id].checked_by_user_id) == (
            "disabled",
            admin.id,
        )
        assert rows[earlier.id].review_note == "An earlier batch's note."
        assert rows[changed.id].status == "verified"
        audits = (await session.scalars(select(AdminAuditLog))).all()
        assert [a.target for a in audits] == [f"food_merchant:{changed.id}"]
        assert audits[0].metadata_json["previous"]["status"] == "disabled"


@pytest.mark.asyncio
async def test_a_new_shop_whose_catchtable_page_another_merchant_holds_is_not_created(
    factory: async_sessionmaker[AsyncSession],
) -> None:
    """The alias is the one reliable identity: if it is linked already, the research missed a
    duplicate, and creating the merchant would put the same shop in the catalog twice."""
    holder = catalog_merchant("seoul-fixture-holder", "다른 이름 식당")
    await seed(factory, *taxonomy(), holder, catchtable_row(holder, "fixture_taken"))
    raw = document(record("fixture_taken", merchant=merchant_block("새 이름 식당")))
    for apply in (False, True):
        outcomes, _ = await run(factory, raw, apply=apply)
        assert actions(outcomes) == {
            "fixture_taken": ("skipped_branch_conflict", "skipped_branch_conflict", None)
        }
        assert outcomes[0].detail == f"the CatchTable page belongs to merchant {holder.id}"
    assert await count(factory, FoodMerchant) == 1
    assert await count(factory, AdminAuditLog) == 0


@pytest.mark.asyncio
async def test_merchant_dedupe_follows_the_trend_importer_and_limit_counts_writable_records(
    factory: async_sessionmaker[AsyncSession],
) -> None:
    other = catalog_merchant("seoul-fixture-slug", "다른 가게")
    named = catalog_merchant("seoul-fixture-elsewhere", "같은 이름")
    await seed(factory, *taxonomy(), other, named)
    raw = document(
        record("fixture_no_source", outcome="no_official_source"),
        record("fixture_slug", merchant=merchant_block("슬러그 가게", slug="seoul-fixture-slug")),
        record("fixture_name", merchant=merchant_block("같은 이름")),
        record("fixture_area", merchant=merchant_block("상권 가게", district_key="atlantis")),
        record("fixture_late", merchant=merchant_block("늦은 가게")),
    )
    outcomes, report = await run(factory, raw, apply=True, limit=3)
    assert actions(outcomes) == {
        "fixture_no_source": (None, None, None),
        # A slug another shop holds is no permission to give that shop this platform row.
        "fixture_slug": ("skipped_existing_slug", None, None),
        "fixture_name": ("skipped_same_name", None, None),
        "fixture_area": ("missing_area", None, None),
    }
    assert [o.detail for o in outcomes[1:]] == [
        "held by 다른 가게",
        "seoul-fixture-elsewhere",
        "seoul-atlantis",
    ]
    assert report["processed"] == 4 and report["records"] == 5
    assert await count(factory, FoodMerchant) == 2
    assert await count(factory, FoodMerchantPlatformLink) == 0


# --- the committed batches -----------------------------------------------------------------


def committed_batches() -> list[Path]:
    paths = sorted(DATA_DIR.glob("*/candidates*.json"))
    assert len(paths) >= 5
    return paths


def sibling(candidates: Path, kind: str) -> Path:
    return candidates.with_name(f"{kind}{candidates.stem.removeprefix('candidates')}.json")


@pytest.mark.parametrize(
    "candidates", committed_batches(), ids=lambda path: f"{path.parent.name}/{path.name}"
)
def test_every_committed_batch_loads_and_reproduces_its_two_pass_files(candidates: Path) -> None:
    prepared = load_candidate_file(candidates)
    merchants = json.loads(sibling(candidates, "merchants").read_text(encoding="utf-8"))
    assert merchant_rows(prepared.candidates) == merchants
    platforms = json.loads(sibling(candidates, "platform-reviews").read_text(encoding="utf-8"))
    committed = {row.pop("slug"): row for row in platforms["records"]}
    generated: dict[str, dict[str, Any]] = {}
    for item in prepared.candidates.records:
        row = platform_row(item, "merchant id comes from the worklist")
        if row is not None:
            generated[row.pop("slug")] = row
    for slug, row in committed.items():
        row.pop("merchant_id")
        generated[slug].pop("merchant_id")
        assert generated[slug] == row, slug
    # Batch 2 met batch 1's alice_cheongdam again and deleted that row by hand rather than
    # rewrite batch 1's note; the importer now reports such a row as unchanged instead.
    batch_2_seoul = candidates.parent.name == "2026-09-23-catchtable-batch-2" and (
        candidates.name == "candidates-seoul.json"
    )
    assert set(generated) - set(committed) == (
        {"seoul-alice-cheongdam"} if batch_2_seoul else set()
    )


@pytest.mark.asyncio
async def test_the_first_batch_dry_run_matches_what_its_two_passes_wrote(
    factory: async_sessionmaker[AsyncSession],
) -> None:
    batch = DATA_DIR / "2026-09-23-catchtable-seoul-1" / "candidates.json"
    # The one duplicate in that batch points at a merchant the production catalog holds.
    await seed(factory, *taxonomy(), catalog_merchant("seoul-buchon-yukhoe", "부촌육회"))
    prepared = load_candidate_file(batch)
    async with factory() as session:
        outcomes = await import_candidate_batch(session, prepared, apply=False)
    report = summarize(prepared, outcomes, apply=False)

    two_pass_merchants = json.loads(sibling(batch, "merchants").read_text(encoding="utf-8"))
    two_pass_platforms = json.loads(
        sibling(batch, "platform-reviews").read_text(encoding="utf-8")
    )["records"]
    assert {o.slug for o in outcomes if o.merchant == "would_create"} == {
        row["slug"] for row in two_pass_merchants
    }
    assert {o.slug for o in outcomes if o.platform == "would_create"} == {
        row["slug"] for row in two_pass_platforms
    }
    assert report["statuses"] == dict(Counter(row["status"] for row in two_pass_platforms))
    assert report["statuses"] == {"disabled": 3, "verified": 12}
    assert report["skipped"] == []
    assert await count(factory, FoodMerchant) == 1


def load_tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("catchtable_build_batches", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_two_pass_tool_now_only_calls_the_model(tmp_path: Path) -> None:
    """The converter keeps its flags for the two-pass fallback, and with the model behind it
    still writes the committed first batch byte for byte."""
    tool = load_tool()
    batch = DATA_DIR / "2026-09-23-catchtable-seoul-1"
    platforms = json.loads((batch / "platform-reviews.json").read_text(encoding="utf-8"))
    worklist = tmp_path / "worklist.json"
    rows = [{"id": r["merchant_id"], "slug": r["slug"]} for r in platforms["records"]]
    worklist.write_text(json.dumps({"merchants": rows}), encoding="utf-8")
    code = tool.main(
        [
            "--candidates",
            str(batch / "candidates.json"),
            "--merchants-out",
            str(tmp_path / "merchants.json"),
            "--worklist",
            str(worklist),
            "--platform-out",
            str(tmp_path / "platform-reviews.json"),
        ]
    )
    assert code == 0
    for name in ("merchants.json", "platform-reviews.json"):
        assert (tmp_path / name).read_bytes() == (batch / name).read_bytes(), name

    broken = tmp_path / "broken.json"
    broken.write_text(json.dumps(document(record("fixture", merchant=None))), encoding="utf-8")
    assert tool.main(["--candidates", str(broken), "--check"]) == 2
