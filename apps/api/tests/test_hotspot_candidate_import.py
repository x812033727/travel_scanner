from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock

import pytest

from app.hotspots.candidate_import import CANDIDATE_ORIGIN, persist_resolutions
from app.hotspots.candidates import CandidateInput, CandidateResolution, NearbyArticle
from app.models import TravelHotspot

NOW = datetime(2026, 9, 4, tzinfo=UTC)
TAINAN = (23.0, 120.2)


def resolution(
    lane: str = "confirmed",
    *,
    reason: str = "three_sources_agree",
    qid: str = "Q123",
    place_id: str | None = "ChIJ-fort",
    city_code: str = "TNN",
) -> CandidateResolution:
    return CandidateResolution(
        candidate=CandidateInput(name="赤崁樓", city_code=city_code, city_qualifier="中西區 台南"),
        lane=lane,
        reason=reason,
        google_place_id=place_id,
        article=NearbyArticle(
            wikipedia_project="zh.wikipedia.org",
            title="赤崁樓",
            qid=qid,
            latitude=TAINAN[0],
            longitude=TAINAN[1],
        ),
        category="culture",
    )


class FakeSession:
    """Answers the two lookups the writer makes: by wikidata id, then by place id."""

    def __init__(self, existing: TravelHotspot | None = None, place_id_owner: Any = None) -> None:
        self.existing = existing
        self.place_id_owner = place_id_owner
        self.added: list[TravelHotspot] = []
        self.commits = 0
        self._calls = 0

    async def scalar(self, _statement: object) -> Any:
        self._calls += 1
        return self.existing if self._calls == 1 else self.place_id_owner

    def add(self, row: TravelHotspot) -> None:
        self.added.append(row)

    async def commit(self) -> None:
        self.commits += 1


@pytest.mark.asyncio
async def test_a_dry_run_reports_without_writing_or_committing() -> None:
    session = FakeSession()

    counts = await persist_resolutions(session, [resolution()], now=NOW, apply=False)  # type: ignore[arg-type]

    assert counts == {"would_create:confirmed": 1}
    assert session.added == []
    assert session.commits == 0


@pytest.mark.asyncio
async def test_a_confirmed_row_is_published_and_cites_the_article_not_google() -> None:
    session = FakeSession()

    counts = await persist_resolutions(session, [resolution()], now=NOW, apply=True)  # type: ignore[arg-type]

    assert counts == {"created:confirmed": 1}
    row = session.added[0]
    assert row.slug == "wikidata-q123"
    assert row.review_status == "approved"
    assert row.map_match_status == "verified"
    assert row.map_verified_at == NOW
    assert row.google_place_id == "ChIJ-fort"
    assert row.origin == CANDIDATE_ORIGIN
    # The coordinate came from the Wikipedia article, so that is what is cited.
    assert row.coordinate_source_type == "curated"
    assert row.coordinate_source_url == "https://zh.wikipedia.org/wiki/%E8%B5%A4%E5%B4%81%E6%A8%93"


@pytest.mark.asyncio
async def test_a_row_held_for_review_is_written_unverified_with_its_reason() -> None:
    session = FakeSession()

    counts = await persist_resolutions(
        session,  # type: ignore[arg-type]
        [resolution("needs_review", reason="coordinates_disagree")],
        now=NOW,
        apply=True,
    )

    assert counts == {"created:needs_review": 1}
    row = session.added[0]
    assert row.review_status == "pending"
    assert row.review_reason == "coordinates_disagree"
    assert row.map_match_status == "unverified"
    assert row.map_verified_at is None


@pytest.mark.asyncio
async def test_a_place_id_another_hotspot_owns_is_reported_rather_than_written() -> None:
    # google_place_id is unique; assigning a taken one aborts the whole transaction.
    session = FakeSession(place_id_owner="00000000-0000-4000-8000-000000000009")

    counts = await persist_resolutions(session, [resolution()], now=NOW, apply=True)  # type: ignore[arg-type]

    assert counts == {"skipped:place_id_taken": 1}
    assert session.added == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("field", "value", "expected"),
    (
        ("review_status", "rejected", "skipped:previously_rejected"),
        ("map_match_status", "verified", "skipped:already_verified"),
    ),
)
async def test_existing_decisions_are_never_overwritten(
    field: str, value: str, expected: str
) -> None:
    existing = TravelHotspot(slug="wikidata-q123", wikidata_item_id="Q123")
    existing.review_status = "approved"
    existing.map_match_status = "unverified"
    setattr(existing, field, value)
    session = FakeSession(existing=existing)

    counts = await persist_resolutions(session, [resolution()], now=NOW, apply=True)  # type: ignore[arg-type]

    assert counts == {expected: 1}


@pytest.mark.asyncio
async def test_a_rejected_candidate_never_reaches_the_database() -> None:
    session = FakeSession()

    counts = await persist_resolutions(
        session,  # type: ignore[arg-type]
        [resolution("rejected", reason="denylisted_type")],
        now=NOW,
        apply=True,
    )

    assert counts == {"skipped:denylisted_type": 1}
    assert session.added == []


@pytest.mark.asyncio
async def test_a_city_missing_from_the_catalog_is_skipped_not_guessed() -> None:
    session = AsyncMock()

    counts = await persist_resolutions(
        session, [resolution(city_code="ZZZ")], now=NOW, apply=True
    )

    assert counts == {"skipped:unknown_city_code": 1}
