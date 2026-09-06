from __future__ import annotations

from collections.abc import Awaitable, Callable
from datetime import date
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
    months: tuple[int, ...] = (),
    kind: str = "season",
    destination_id: str = "tokyo",
) -> dict[str, Any]:
    return {
        "id": UUID(int=rank),
        "name": f"景點 {rank}",
        "category": category,
        "themes": [
            {"slug": slug, "kind": kind, "name": slug, "months": list(months)} for slug in themes
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
        "destination_id": destination_id,
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


def _season_slugs(slugs: list[str]) -> Callable[..., Awaitable[list[str]]]:
    async def fake(session: object, travel_months: list[int]) -> list[str]:
        return slugs if travel_months else []

    return fake


@pytest.mark.asyncio
async def test_planner_pages_past_unverified_imports(monkeypatch: pytest.MonkeyPatch) -> None:
    """A fresh import fills the top of the ranking with unverified rows; the
    planner must keep paging until it reaches the verified ones."""
    ranking = [ranked(rank, verified=rank > 50) for rank in range(1, 59)]
    calls: list[int | None] = []
    monkeypatch.setattr(service, "list_rankings", paging_fake(ranking, calls))

    rows = await service.load_planner_hotspots(
        None,
        destination_id="tokyo",
        limit=12,
        days=6,
        style="all",  # type: ignore[arg-type]
    )

    assert [row.name for row in rows] == [f"景點 {rank}" for rank in range(51, 59)]
    assert calls == [None, 50]


@pytest.mark.asyncio
async def test_planner_stops_paging_once_it_has_enough(monkeypatch: pytest.MonkeyPatch) -> None:
    ranking = [ranked(rank, verified=True) for rank in range(1, 121)]
    calls: list[int | None] = []
    monkeypatch.setattr(service, "list_rankings", paging_fake(ranking, calls))

    rows = await service.load_planner_hotspots(
        None,
        destination_id="tokyo",
        limit=12,
        days=6,
        style="all",  # type: ignore[arg-type]
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
        None,
        destination_id="tokyo",
        limit=12,
        days=6,
        style="all",  # type: ignore[arg-type]
    )

    assert [row.name for row in rows] == [f"景點 {rank}" for rank in range(1, 13)]
    assert calls == [None]


@pytest.mark.asyncio
async def test_planner_gives_up_after_the_page_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    ranking = [ranked(rank, verified=False) for rank in range(1, 1001)]
    calls: list[int | None] = []
    monkeypatch.setattr(service, "list_rankings", paging_fake(ranking, calls))

    rows = await service.load_planner_hotspots(
        None,
        destination_id="tokyo",
        limit=12,
        days=6,
        style="all",  # type: ignore[arg-type]
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
        None,
        destination_id="tokyo",
        limit=12,
        days=6,
        style="all",  # type: ignore[arg-type]
    )

    assert rows[0].themes == ["sakura", "market-street"]
    assert rows[1].themes == []


@pytest.mark.asyncio
async def test_named_shop_types_come_before_the_city_s_landmarks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A traveller who said 藥妝 means that shop, and it sits far below the city's
    landmarks — and below its plain shopping streets — in a popularity ranking."""
    ranking = [
        *[ranked(rank, verified=True) for rank in range(1, 21)],
        *[ranked(rank, verified=True, category="shopping") for rank in range(21, 31)],
        *[
            ranked(rank, verified=True, category="shopping", themes=("drugstore",), kind="shop")
            for rank in range(31, 36)
        ],
    ]
    monkeypatch.setattr(service, "list_rankings", paging_fake(ranking, []))

    rows = await service.load_planner_hotspots(
        None,  # type: ignore[arg-type]
        destination_id="tokyo",
        limit=12,
        days=6,
        style="all",
        shop_themes=["drugstore"],
    )

    assert [row.name for row in rows[:3]] == ["景點 31", "景點 32", "景點 33"]
    assert all("drugstore" in row.themes for row in rows[:3])
    # Shops still cannot take the whole pool: the interest quota bounds them.
    shopping = [row for row in rows if row.category == "shopping"]
    assert len(shopping) <= int(12 * service.PLANNER_INTEREST_SHARE)


@pytest.mark.asyncio
async def test_a_spot_in_season_is_pulled_in_but_kept_to_its_share(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ranking = [
        *[ranked(rank, verified=True) for rank in range(1, 31)],
        *[
            ranked(rank, verified=True, category="nature", themes=("sakura",), months=(3, 4))
            for rank in range(31, 41)
        ],
    ]
    monkeypatch.setattr(service, "list_rankings", paging_fake(ranking, []))
    monkeypatch.setattr(service, "season_slugs_for", _season_slugs(["sakura"]))

    rows = await service.load_planner_hotspots(
        None,  # type: ignore[arg-type]
        destination_id="tokyo",
        limit=12,
        days=6,
        style="all",
        travel_months=[4],
    )

    seasonal = [row for row in rows if row.in_season]
    assert seasonal, "an April trip should surface the blossoms at all"
    # ...but an April trip to Kyoto is not ten cherry trees in a row.
    assert len(seasonal) == max(1, int(12 * service.PLANNER_SEASONAL_SHARE))


@pytest.mark.asyncio
async def test_nothing_is_in_season_outside_its_months(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ranking = [
        ranked(rank, verified=True, category="nature", themes=("sakura",), months=(3, 4))
        for rank in range(1, 13)
    ]
    monkeypatch.setattr(service, "list_rankings", paging_fake(ranking, []))
    monkeypatch.setattr(service, "season_slugs_for", _season_slugs([]))

    rows = await service.load_planner_hotspots(
        None,  # type: ignore[arg-type]
        destination_id="tokyo",
        limit=12,
        days=6,
        style="all",
        travel_months=[11],
    )

    assert rows and not any(row.in_season for row in rows)


@pytest.mark.asyncio
async def test_an_extension_city_s_season_does_not_reshape_the_main_trip(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Blossoms in a day-trip town are not a reason to rearrange the days in Tokyo."""
    ranking = [
        ranked(
            rank,
            verified=True,
            category="nature",
            themes=("sakura",),
            months=(3, 4),
            destination_id="kamakura",
        )
        for rank in range(1, 13)
    ]
    monkeypatch.setattr(service, "list_rankings", paging_fake(ranking, []))
    monkeypatch.setattr(service, "season_slugs_for", _season_slugs(["sakura"]))

    rows = await service.load_planner_hotspots(
        None,  # type: ignore[arg-type]
        destination_id="tokyo",
        limit=12,
        days=6,
        style="all",
        travel_months=[4],
    )

    assert rows and not any(row.in_season for row in rows)


@pytest.mark.asyncio
async def test_a_shop_without_a_seeded_duration_gets_a_shop_sized_one(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    row = ranked(1, verified=True, category="shopping")
    row["recommended_duration_minutes"] = None
    landmark = ranked(2, verified=True)
    landmark["recommended_duration_minutes"] = None
    monkeypatch.setattr(service, "list_rankings", paging_fake([row, landmark], []))

    rows = await service.load_planner_hotspots(
        None,
        destination_id="tokyo",
        limit=12,
        days=6,
        style="all",  # type: ignore[arg-type]
    )

    by_name = {item.name: item for item in rows}
    assert by_name["景點 1"].recommended_duration_minutes == service.SHOP_DEFAULT_DURATION_MINUTES
    assert by_name["景點 2"].recommended_duration_minutes == 120


def test_months_in_span_covers_the_calendar_months_a_trip_touches() -> None:
    assert service.months_in_span(date(2026, 4, 3), date(2026, 4, 9)) == [4]
    assert service.months_in_span(date(2026, 11, 28), date(2026, 12, 2)) == [11, 12]
    # A new-year trip is December and January, not thirteen months.
    assert service.months_in_span(date(2026, 12, 30), date(2027, 1, 2)) == [12, 1]
    # Reversed dates are still a span.
    assert service.months_in_span(date(2026, 5, 2), date(2026, 4, 28)) == [4, 5]


def test_in_season_reads_the_effective_months_of_the_trip_s_own_city() -> None:
    item = {
        "destination_id": "tokyo",
        "themes": [{"slug": "sakura", "kind": "season", "months": [5]}],
    }
    assert service.in_season(item, [5], "tokyo") is True
    assert service.in_season(item, [3], "tokyo") is False
    assert service.in_season(item, [5], "osaka-kyoto") is False
    # A shop type is never "in season", whatever months somebody puts on it.
    shop = {
        "destination_id": "tokyo",
        "themes": [{"slug": "outlet", "kind": "shop", "months": [5]}],
    }
    assert service.in_season(shop, [5], "tokyo") is False
