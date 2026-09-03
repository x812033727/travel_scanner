from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any
from uuid import UUID

import pytest

from app.hotspots import service

RankingsFake = Callable[..., Awaitable[dict[str, Any]]]


def ranked(rank: int, *, verified: bool, category: str = "culture") -> dict[str, Any]:
    return {
        "id": UUID(int=rank),
        "name": f"景點 {rank}",
        "category": category,
        "latitude": 35.6 + rank * 0.001,
        "longitude": 139.7 + rank * 0.001,
        "map_links": [{"provider": "google", "url": "https://maps.example/x"}] if verified else [],
        "map_match_status": "verified" if verified else "unverified",
        "coordinate_source": {"type": "wikidata", "url": "https://www.wikidata.org/wiki/Q1"},
        "depth_kind": "urban_local",
        "depth_score": 1,
        "depth_reason": "",
        "access_minutes": 10,
        "recommended_duration_minutes": 90,
        "destination_id": "tokyo",
        "destination_role": "primary",
        "parent_destination_id": None,
        "is_cross_city": False,
        "rank": rank,
    }


def paging_fake(ranking: list[dict[str, Any]], calls: list[int | None]) -> RankingsFake:
    async def fake_list_rankings(
        session: object,
        *,
        after_rank: int | None = None,
        limit: int = 20,
        category: str | None = None,
        **_: object,
    ) -> dict[str, Any]:
        calls.append(after_rank)
        rows = [
            item
            for item in ranking
            if (after_rank is None or item["rank"] > after_rank)
            and (category is None or item["category"] == category)
        ]
        page = rows[:limit]
        has_more = len(rows) > limit
        return {
            "items": page,
            "has_more": has_more,
            "next_cursor": page[-1]["rank"] if has_more and page else None,
        }

    return fake_list_rankings


@pytest.mark.asyncio
async def test_planner_pages_past_unverified_imports(monkeypatch: pytest.MonkeyPatch) -> None:
    """A fresh import fills the top of the ranking with unverified rows; the
    planner must keep paging until it reaches the verified ones."""
    ranking = [ranked(rank, verified=rank > 50) for rank in range(1, 59)]
    calls: list[int | None] = []
    monkeypatch.setattr(service, "list_rankings", paging_fake(ranking, calls))

    rows = await service.load_planner_hotspots(
        None, destination_id="tokyo", limit=12, days=6, style="all"  # type: ignore[arg-type]
    )

    assert [row.name for row in rows] == [f"景點 {rank}" for rank in range(51, 59)]
    assert calls == [None, 50]


@pytest.mark.asyncio
async def test_planner_stops_paging_once_it_has_enough(monkeypatch: pytest.MonkeyPatch) -> None:
    ranking = [ranked(rank, verified=True) for rank in range(1, 121)]
    calls: list[int | None] = []
    monkeypatch.setattr(service, "list_rankings", paging_fake(ranking, calls))

    rows = await service.load_planner_hotspots(
        None, destination_id="tokyo", limit=12, days=6, style="all"  # type: ignore[arg-type]
    )

    assert len(rows) == 12
    assert calls == [None]


@pytest.mark.asyncio
async def test_planner_pulls_interest_categories_from_below_the_cut(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Shops ranked below 50 landmarks must still reach a shopping trip's pool,
    while the top landmarks keep their reserved share."""
    ranking = [ranked(rank, verified=True) for rank in range(1, 51)] + [
        ranked(rank, verified=True, category="shopping") for rank in range(51, 61)
    ]
    calls: list[int | None] = []
    monkeypatch.setattr(service, "list_rankings", paging_fake(ranking, calls))

    rows = await service.load_planner_hotspots(
        None,  # type: ignore[arg-type]
        destination_id="tokyo",
        interests=["shopping", "spa", "deep_travel"],
        limit=12,
        days=6,
        style="all",
    )

    names = [row.name for row in rows]
    assert len(rows) == 12
    assert names[:8] == [f"景點 {rank}" for rank in range(51, 59)]  # 2/3 of 12 shops first
    assert names[8:] == [f"景點 {rank}" for rank in range(1, 5)]  # then top landmarks
    assert calls[0] is None and len(calls) >= 2


@pytest.mark.asyncio
async def test_planner_without_interests_keeps_plain_ranking_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ranking = [ranked(rank, verified=True, category="shopping") for rank in range(1, 21)]
    calls: list[int | None] = []
    monkeypatch.setattr(service, "list_rankings", paging_fake(ranking, calls))

    rows = await service.load_planner_hotspots(
        None, destination_id="tokyo", limit=12, days=6, style="all"  # type: ignore[arg-type]
    )

    assert [row.name for row in rows] == [f"景點 {rank}" for rank in range(1, 13)]
    assert calls == [None]


@pytest.mark.asyncio
async def test_planner_gives_up_after_the_page_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    ranking = [ranked(rank, verified=False) for rank in range(1, 1001)]
    calls: list[int | None] = []
    monkeypatch.setattr(service, "list_rankings", paging_fake(ranking, calls))

    rows = await service.load_planner_hotspots(
        None, destination_id="tokyo", limit=12, days=6, style="all"  # type: ignore[arg-type]
    )

    assert rows == []
    assert len(calls) == service.PLANNER_RANKING_MAX_PAGES
