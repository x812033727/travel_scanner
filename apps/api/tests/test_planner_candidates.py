from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any
from uuid import UUID

import pytest

from app.hotspots import service

RankingsFake = Callable[..., Awaitable[dict[str, Any]]]


def ranked(
    rank: int,
    *,
    verified: bool,
    category: str = "culture",
    themes: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "id": UUID(int=rank),
        "name": f"景點 {rank}",
        "category": category,
        "themes": [
            {"slug": slug, "kind": "season", "name": slug, "months": []} for slug in themes
        ],
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


def paging_fake(
    ranking: list[dict[str, Any]],
    calls: list[int | None],
    themes_seen: list[str | None] | None = None,
) -> RankingsFake:
    async def fake_list_rankings(
        session: object,
        *,
        after_rank: int | None = None,
        limit: int = 20,
        category: str | None = None,
        theme: str | None = None,
        **_: object,
    ) -> dict[str, Any]:
        calls.append(after_rank)
        if themes_seen is not None:
            themes_seen.append(theme)
        rows = [
            item
            for item in ranking
            if (after_rank is None or item["rank"] > after_rank)
            and (category is None or item["category"] == category)
            and (theme is None or theme in {entry["slug"] for entry in item.get("themes", [])})
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


@pytest.mark.asyncio
async def test_collect_ranked_pages_one_theme(monkeypatch: pytest.MonkeyPatch) -> None:
    """A theme filter reaches list_rankings unchanged, so the planner can pull
    every 賞櫻 spot of a city before it fills the pool from the general ranking."""
    ranking = [
        ranked(rank, verified=True, themes=("sakura",) if rank % 3 == 0 else ())
        for rank in range(1, 31)
    ]
    calls: list[int | None] = []
    themes_seen: list[str | None] = []
    monkeypatch.setattr(service, "list_rankings", paging_fake(ranking, calls, themes_seen))

    rows = await service._collect_ranked(
        None,  # type: ignore[arg-type]
        city_code=None,
        destination_id="tokyo",
        style="all",
        wanted=3,
        theme="sakura",
    )

    assert themes_seen == ["sakura"]
    assert [row["rank"] for row in rows] == [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
    assert all("sakura" in {entry["slug"] for entry in row["themes"]} for row in rows)


@pytest.mark.asyncio
async def test_planner_rows_carry_theme_slugs(monkeypatch: pytest.MonkeyPatch) -> None:
    ranking = [
        ranked(rank, verified=True, themes=("sakura", "market-street") if rank == 1 else ())
        for rank in range(1, 15)
    ]
    monkeypatch.setattr(service, "list_rankings", paging_fake(ranking, []))

    rows = await service.load_planner_hotspots(
        None, destination_id="tokyo", limit=12, days=6, style="all"  # type: ignore[arg-type]
    )

    assert rows[0].themes == ["sakura", "market-street"]
    assert rows[1].themes == []
