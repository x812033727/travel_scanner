from collections.abc import Callable
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import fakeredis.aioredis
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.hotspots.place_matching import approve_pending_candidate, match_missing_places
from app.models import AdminAuditLog, HotspotPlaceProfile, TravelHotspot
from app.places.google import GoogleTravelService

NOW = datetime(2026, 9, 3, tzinfo=UTC)
DETAILS = {
    "place_id": "ChIJ-nakamise",
    "name": "仲見世通り",
    "address": "日本東京都台東區淺草",
    "latitude": 35.712,
    "longitude": 139.7965,
    "google_maps_url": "https://www.google.com/maps/place/example",
    "opening_hours_structured": {"weekday_descriptions": ["星期一: 09:00–19:00"], "periods": []},
    "website_url": "https://www.asakusa-nakamise.jp/",
    "attributions": [],
    "data_locale": "zh-TW",
}


def _hotspot() -> TravelHotspot:
    return TravelHotspot(
        id=uuid4(),
        slug="nrt-nakamise-dori",
        name="仲見世商店街",
        city_code="NRT",
        destination_id="tokyo",
        city_name="東京",
        country_code="JP",
        country_name="日本",
        category="shopping",
        search_text="仲見世商店街 仲見世通り nakamise-dori",
        latitude=Decimal("35.712"),
        longitude=Decimal("139.7965"),
        coordinate_source_type="wikidata",
        coordinate_source_url="https://www.wikidata.org/wiki/Q11397116",
        metadata_json={
            "local_name": "仲見世通り",
            "aliases": ["Nakamise-dori"],
            "provenance": "gemini",
        },
        source_urls=[],
        is_active=True,
        review_status="approved",
    )


def _session(scalar: Callable[[int], Any]) -> tuple[AsyncMock, list[Any]]:
    """Session double whose ``scalar`` answers by call index and remembers ``add`` calls."""

    added: list[Any] = []
    session = AsyncMock(spec=AsyncSession)
    session.add = MagicMock(side_effect=added.append)
    calls = {"count": 0}

    async def _scalar(*_args: Any, **_kwargs: Any) -> Any:
        calls["count"] += 1
        return scalar(calls["count"])

    session.scalar = AsyncMock(side_effect=_scalar)
    return session, added


def _candidate(name: str) -> dict[str, Any]:
    return {
        "place_id": "ChIJ-nakamise",
        "name": name,
        "address": "日本東京都台東區淺草",
        "country_code": "JP",
        "latitude": 35.7121,
        "longitude": 139.7964,
    }


@pytest.mark.asyncio
async def test_exact_match_publishes_place_id_and_marks_verified(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session, added = _session(lambda _index: None)
    monkeypatch.setattr(
        GoogleTravelService,
        "search_place_candidates",
        AsyncMock(return_value=[_candidate("仲見世通り")]),
    )
    monkeypatch.setattr(GoogleTravelService, "place_details", AsyncMock(return_value=DETAILS))
    hotspot = _hotspot()

    reports = await match_missing_places(
        session,
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(google_maps_api_key="key"),
        [hotspot],
        now=NOW,
    )

    assert [(item.outcome, item.calls) for item in reports] == [("published", 2)]
    assert hotspot.google_place_id == "ChIJ-nakamise"
    assert hotspot.map_match_status == "verified"
    assert hotspot.map_verified_at == NOW
    profile = next(item for item in added if isinstance(item, HotspotPlaceProfile))
    assert profile.match_status == "auto_approved"
    assert profile.place_id_source == "automatic"
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_loose_match_stays_pending_and_reports_the_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    added_profiles: list[HotspotPlaceProfile] = []

    def scalar(_index: int) -> HotspotPlaceProfile | None:
        return added_profiles[0] if added_profiles else None

    session, added = _session(scalar)
    session.add = MagicMock(
        side_effect=lambda item: (
            added_profiles.append(item) if isinstance(item, HotspotPlaceProfile) else None
        )
    )
    search = AsyncMock(return_value=[_candidate("浅草観光案内所 雷門前")])
    details = AsyncMock(return_value=DETAILS)
    monkeypatch.setattr(GoogleTravelService, "search_place_candidates", search)
    monkeypatch.setattr(GoogleTravelService, "place_details", details)
    hotspot = _hotspot()

    reports = await match_missing_places(
        session,
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(google_maps_api_key="key"),
        [hotspot],
        now=NOW,
    )

    assert len(reports) == 1
    assert reports[0].outcome == "pending"
    assert reports[0].calls == 1
    assert reports[0].candidate is not None
    assert reports[0].candidate["place_id"] == "ChIJ-nakamise"
    assert reports[0].candidate["name"] == "浅草観光案内所 雷門前"
    assert 0 < float(reports[0].candidate["confidence"]) < 0.9
    assert hotspot.google_place_id is None
    details.assert_not_awaited()
    del added


@pytest.mark.asyncio
async def test_usage_guard_stops_the_batch_before_calling_google(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session, _added = _session(lambda _index: None)
    search = AsyncMock(return_value=[_candidate("仲見世通り")])
    monkeypatch.setattr(GoogleTravelService, "search_place_candidates", search)
    monkeypatch.setattr(
        "app.hotspots.place_matching.automatic_refresh_allowed", AsyncMock(return_value=False)
    )

    reports = await match_missing_places(
        session,
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(google_maps_api_key="key"),
        [_hotspot(), _hotspot()],
        now=NOW,
    )

    assert [item.outcome for item in reports] == ["usage_guard"]
    search.assert_not_awaited()
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_place_id_owned_by_another_hotspot_keeps_the_match_pending(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner = uuid4()
    added_profiles: list[HotspotPlaceProfile] = []

    def scalar(index: int) -> Any:
        # 1: profile lookup, 2: google_place_id owner check, 3: profile re-read for the report
        return None if index == 1 else owner if index == 2 else added_profiles[0]

    session, _added = _session(scalar)
    session.add = MagicMock(
        side_effect=lambda item: (
            added_profiles.append(item) if isinstance(item, HotspotPlaceProfile) else None
        )
    )
    monkeypatch.setattr(
        GoogleTravelService,
        "search_place_candidates",
        AsyncMock(return_value=[_candidate("仲見世通り")]),
    )
    details = AsyncMock(return_value=DETAILS)
    monkeypatch.setattr(GoogleTravelService, "place_details", details)
    hotspot = _hotspot()

    reports = await match_missing_places(
        session,
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(google_maps_api_key="key"),
        [hotspot],
        now=NOW,
    )

    assert reports[0].outcome == "pending"
    assert hotspot.google_place_id is None
    assert added_profiles[0].match_status == "pending"
    assert added_profiles[0].match_evidence_json["duplicate_place_id"] == str(owner)
    details.assert_not_awaited()


@pytest.mark.asyncio
async def test_approving_a_pending_candidate_promotes_it_and_fetches_details(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    hotspot = _hotspot()
    profile = HotspotPlaceProfile(
        hotspot_id=hotspot.id,
        place_id_source="none",
        match_status="pending",
        match_confidence=Decimal("0.6100"),
        candidate_place_id="ChIJ-nakamise",
        candidate_name="浅草観光案内所 雷門前",
        candidate_address="日本東京都台東區淺草",
    )
    # 1: profile lookup, 2: owner check, 3: profile lookup inside enrich_hotspot_place
    session, added = _session(lambda index: None if index == 2 else profile)
    monkeypatch.setattr(GoogleTravelService, "place_details", AsyncMock(return_value=DETAILS))
    search = AsyncMock(return_value=[])
    monkeypatch.setattr(GoogleTravelService, "search_place_candidates", search)

    report = await approve_pending_candidate(
        session,
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(google_maps_api_key="key"),
        hotspot,
        now=NOW,
    )

    assert (report.outcome, report.calls) == ("published", 1)
    assert hotspot.google_place_id == "ChIJ-nakamise"
    assert hotspot.map_match_status == "verified"
    assert hotspot.map_verified_at == NOW
    assert profile.place_id_source == "manual"
    assert profile.match_status == "approved"
    assert profile.candidate_place_id is None
    audit = next(item for item in added if isinstance(item, AdminAuditLog))
    assert audit.action == "hotspot_place_profile.cli_approved"
    assert audit.metadata_json["place_id"] == "ChIJ-nakamise"
    search.assert_not_awaited()
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_approving_without_a_stored_candidate_is_a_noop() -> None:
    hotspot = _hotspot()
    session, added = _session(lambda _index: None)

    report = await approve_pending_candidate(
        session,
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(google_maps_api_key="key"),
        hotspot,
        now=NOW,
    )

    assert report.outcome == "no_candidate"
    assert hotspot.google_place_id is None
    assert added == []
    session.commit.assert_not_awaited()
