from typing import Any
from uuid import uuid4

import pytest

from app.config import Settings
from app.foods.place_matching import (
    MerchantMatchReport,
    match_merchant_places,
    search_query,
    summarize,
    unmatched_merchants,
)
from app.models import FoodMerchant


def merchant(**overrides: Any) -> FoodMerchant:
    values: dict[str, Any] = {
        "id": uuid4(),
        "slug": "tokyo-sushi-dai",
        "destination_id": "tokyo",
        "country_code": "JP",
        "name": "壽司大",
        "local_name": "寿司大",
        "google_place_id": None,
        "review_status": "pending",
        "map_match_status": "unverified",
        "is_active": False,
        "display_order": 1,
    }
    values.update(overrides)
    return FoodMerchant(**values)


class MatchSession:
    """Just enough session for the matcher: an owner lookup and commit counting."""

    def __init__(self, owner: str | None = None) -> None:
        self.owner = owner
        self.commits = 0
        self.added: list[Any] = []

    async def scalar(self, _statement: object) -> str | None:
        return self.owner

    def add(self, value: Any) -> None:
        self.added.append(value)

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        return None


def preview(place_id: str | None, *, configured: bool = True) -> dict[str, Any]:
    if not configured:
        return {"configured": False, "candidates": []}
    if place_id is None:
        return {"configured": True, "candidates": []}
    return {
        "configured": True,
        "candidates": [
            {
                "place_id": place_id,
                "name": "Sushi Dai",
                "address": "Toyosu Market, Koto City",
                "suggested_status": "unverified",
            }
        ],
    }


@pytest.fixture(autouse=True)
def allow_usage(monkeypatch: pytest.MonkeyPatch) -> None:
    async def allowed(_redis: object, _settings: object) -> bool:
        return True

    monkeypatch.setattr("app.foods.place_matching.automatic_refresh_allowed", allowed)


def stub_preview(monkeypatch: pytest.MonkeyPatch, *bodies: dict[str, Any]) -> list[str]:
    queries: list[str] = []
    queue = list(bodies)

    async def fake(_session: object, _redis: object, **kwargs: Any) -> dict[str, Any]:
        queries.append(str(kwargs["query"]))
        return queue.pop(0)

    monkeypatch.setattr("app.foods.place_matching.preview_google_place_match", fake)
    return queries


def test_the_query_carries_the_endonym_and_the_city() -> None:
    assert search_query(merchant()) == "壽司大 寿司大 tokyo"
    assert search_query(merchant(local_name="壽司大")) == "壽司大 tokyo"
    assert search_query(merchant(address="豐洲市場")) == "壽司大 寿司大 豐洲市場"


@pytest.mark.asyncio
async def test_a_dry_run_reports_the_candidate_without_writing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = MatchSession()
    queries = stub_preview(monkeypatch, preview("place-1"))
    row = merchant()

    reports = await match_merchant_places(
        session, None, Settings(), [row], apply=False  # type: ignore[arg-type]
    )

    assert [r.outcome for r in reports] == ["would_match"]
    assert reports[0].place_id == "place-1"
    assert row.google_place_id is None
    assert session.commits == 0
    assert queries == ["壽司大 寿司大 tokyo"]


@pytest.mark.asyncio
async def test_applying_writes_only_the_place_id(monkeypatch: pytest.MonkeyPatch) -> None:
    session = MatchSession()
    stub_preview(monkeypatch, preview("place-1"))
    row = merchant()

    reports = await match_merchant_places(
        session, None, Settings(), [row], apply=True  # type: ignore[arg-type]
    )

    assert [r.outcome for r in reports] == ["matched"]
    assert row.google_place_id == "place-1"
    # Publication needs a durable non-Google coordinate and a human check, so nothing
    # else may advance here.
    assert row.map_match_status == "unverified"
    assert row.review_status == "pending"
    assert row.is_active is False
    assert row.latitude is None and row.longitude is None
    assert session.commits == 1
    assert session.added and session.added[0].action == "food_merchant.cli_place_matched"


@pytest.mark.asyncio
async def test_a_place_id_another_merchant_owns_is_reported_not_written(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = MatchSession(owner="osaka-sushi-dai")
    stub_preview(monkeypatch, preview("place-1"))
    row = merchant()

    reports = await match_merchant_places(
        session, None, Settings(), [row], apply=True  # type: ignore[arg-type]
    )

    assert [r.outcome for r in reports] == ["duplicate"]
    assert row.google_place_id is None
    assert session.commits == 0
    assert (reports[0].candidate or {})["owner"] == "osaka-sushi-dai"


@pytest.mark.asyncio
async def test_no_candidate_and_provider_failure_do_not_stop_the_batch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = MatchSession()
    calls = {"n": 0}

    async def fake(_session: object, _redis: object, **_kwargs: Any) -> dict[str, Any]:
        calls["n"] += 1
        if calls["n"] == 1:
            return preview(None)
        if calls["n"] == 2:
            raise TimeoutError("slow")
        return preview("place-3")

    monkeypatch.setattr("app.foods.place_matching.preview_google_place_match", fake)
    rows = [merchant(slug="a"), merchant(slug="b"), merchant(slug="c")]

    reports = await match_merchant_places(
        session, None, Settings(), rows, apply=True  # type: ignore[arg-type]
    )

    assert [r.outcome for r in reports] == ["no_candidate", "failed", "matched"]
    assert rows[2].google_place_id == "place-3"


@pytest.mark.asyncio
async def test_the_usage_guard_stops_the_batch(monkeypatch: pytest.MonkeyPatch) -> None:
    async def refused(_redis: object, _settings: object) -> bool:
        return False

    monkeypatch.setattr("app.foods.place_matching.automatic_refresh_allowed", refused)
    stub_preview(monkeypatch, preview("place-1"))
    session = MatchSession()

    reports = await match_merchant_places(
        session,  # type: ignore[arg-type]
        None,  # type: ignore[arg-type]
        Settings(),
        [merchant(slug="a"), merchant(slug="b")],
        apply=True,
    )

    assert [r.outcome for r in reports] == ["usage_guard"]
    assert session.commits == 0


@pytest.mark.asyncio
async def test_an_unconfigured_provider_stops_the_batch(monkeypatch: pytest.MonkeyPatch) -> None:
    stub_preview(monkeypatch, preview(None, configured=False))
    session = MatchSession()

    reports = await match_merchant_places(
        session, None, Settings(), [merchant()], apply=True  # type: ignore[arg-type]
    )

    assert [r.outcome for r in reports] == ["not_configured"]


@pytest.mark.asyncio
async def test_an_already_matched_row_costs_no_call(monkeypatch: pytest.MonkeyPatch) -> None:
    queries = stub_preview(monkeypatch)
    session = MatchSession()

    reports = await match_merchant_places(
        session,  # type: ignore[arg-type]
        None,  # type: ignore[arg-type]
        Settings(),
        [merchant(google_place_id="kept")],
        apply=True,
    )

    assert [r.outcome for r in reports] == ["already_matched"]
    assert queries == []


@pytest.mark.asyncio
async def test_korea_is_excluded_from_the_target_query() -> None:
    captured: dict[str, Any] = {}

    class QuerySession:
        async def scalars(self, statement: object) -> Any:
            captured["sql"] = str(statement)

            class Result:
                def all(self) -> list[FoodMerchant]:
                    return []

            return Result()

    await unmatched_merchants(
        QuerySession(), destination_ids=("seoul",), limit=5  # type: ignore[arg-type]
    )

    sql = captured["sql"]
    assert "google_place_id IS NULL" in sql
    assert "country_code NOT IN" in sql
    assert "review_status !=" in sql


def test_the_summary_counts_outcomes() -> None:
    reports = [
        MerchantMatchReport("a", "A", "matched", "p1", {"name": "A"}),
        MerchantMatchReport("b", "B", "no_candidate"),
        MerchantMatchReport("c", "C", "matched", "p2", {"name": "C"}),
    ]

    summary = summarize(reports)

    assert summary["processed"] == 3
    assert summary["outcomes"] == {"matched": 2, "no_candidate": 1}
    assert summary["rows"][0]["place_id"] == "p1"
