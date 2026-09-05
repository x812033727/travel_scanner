from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import uuid4

import pytest

from app.foods import coordinate_queue
from app.foods.coordinate_queue import (
    CandidateMatch,
    apply_approval,
    extract_match,
    judge,
    merchant_search_query,
)
from app.models import FoodMerchant


def make_merchant(**overrides: Any) -> FoodMerchant:
    defaults: dict[str, Any] = {
        "id": uuid4(),
        "slug": "dadong-night-market",
        "destination_id": "tainan",
        "country_code": "TW",
        "name": "大東夜市",
        "local_name": "大東夜市",
        "address": "台南市東區林森路一段276號",
        "latitude": None,
        "longitude": None,
        "coordinate_source_type": None,
        "coordinate_source_url": None,
        "google_place_id": None,
        "naver_map_url": None,
        "map_match_status": "unverified",
        "review_status": "pending",
        "is_active": False,
    }
    defaults.update(overrides)
    return FoodMerchant(**defaults)


def make_match(**overrides: Any) -> CandidateMatch:
    defaults: dict[str, Any] = {
        "place_id": "ChIJexample1234567890",
        "name": "大東夜市",
        "address": "701台南市東區林森路一段276號",
        "google_maps_url": "https://maps.google.com/?cid=1",
        "latitude": 22.980,
        "longitude": 120.224,
    }
    defaults.update(overrides)
    return CandidateMatch(**defaults)


def test_search_query_prefers_the_local_name_and_skips_blanks() -> None:
    merchant = make_merchant(local_name="ダイトウ夜市", address=None)
    assert merchant_search_query(merchant) == "ダイトウ夜市 tainan"


def test_extract_match_requires_id_and_location_and_https_url() -> None:
    assert extract_match({}) is None
    assert extract_match({"id": "x", "location": {}}) is None
    downgraded = extract_match(
        {
            "id": "ChIJabc",
            "location": {"latitude": 1.0, "longitude": 2.0},
            "displayName": {"text": "店"},
            "googleMapsUri": "http://insecure.example",
        }
    )
    assert downgraded is not None and downgraded.google_maps_url is None


def test_judge_agrees_on_exact_and_contained_names() -> None:
    merchant = make_merchant()
    assert judge(merchant, make_match(), place_id_taken=False).verdict == "agree"
    salt_field = make_merchant(name="井仔腳瓦盤鹽田", local_name="井仔腳瓦盤鹽田")
    contained = judge(salt_field, make_match(name="北門井仔腳瓦盤鹽田"), place_id_taken=False)
    assert contained.verdict == "agree" and contained.name_score == 0.92


def test_judge_flags_mismatch_drift_and_conflicts() -> None:
    merchant = make_merchant()
    assert judge(merchant, make_match(name="完全無關的店"), place_id_taken=False).verdict == "check"
    assert judge(merchant, make_match(), place_id_taken=True).verdict == "check"
    seated = make_merchant(latitude=Decimal("22.980"), longitude=Decimal("120.224"))
    near = judge(seated, make_match(), place_id_taken=False)
    assert near.verdict == "agree" and near.distance_km == 0
    drifted = judge(seated, make_match(latitude=23.10), place_id_taken=False)
    assert drifted.verdict == "check" and drifted.distance_km > coordinate_queue.MAX_DRIFT_KM


class FakeRedis:
    def __init__(self) -> None:
        self.store: dict[str, str] = {}

    async def exists(self, key: str) -> int:
        return 1 if key in self.store else 0

    async def set(self, key: str, value: str, ex: int | None = None) -> None:
        self.store[key] = value


class FakeGoogle:
    def __init__(self, place: dict[str, Any]) -> None:
        self.place = place
        self.redis = FakeRedis()
        self.searches = 0

    async def search_place(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        self.searches += 1
        return self.place


def google_returning(match: CandidateMatch) -> FakeGoogle:
    return FakeGoogle(
        {
            "id": match.place_id,
            "displayName": {"text": match.name},
            "formattedAddress": match.address,
            "googleMapsUri": match.google_maps_url,
            "location": {"latitude": match.latitude, "longitude": match.longitude},
        }
    )


def own_the_place(monkeypatch: pytest.MonkeyPatch, owners: dict[str, Any]) -> None:
    async def fake_taken(session: Any, place_ids: list[str]) -> dict[str, Any]:
        return owners

    monkeypatch.setattr(coordinate_queue, "taken_place_ids", fake_taken)


@pytest.mark.asyncio
async def test_approval_writes_admin_verified_and_flips_verified(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    merchant = make_merchant()
    match = make_match()
    own_the_place(monkeypatch, {})
    actor = uuid4()
    now = datetime(2026, 9, 5, tzinfo=UTC)
    outcome = await apply_approval(
        None,  # session is only consulted through the patched ownership lookup
        google_returning(match),  # type: ignore[arg-type]
        merchant,
        expected_place_id=match.place_id,
        actor_id=actor,
        now=now,
    )
    assert outcome == "verified"
    assert merchant.coordinate_source_type == "admin_verified"
    assert merchant.coordinate_source_url == match.google_maps_url
    assert float(merchant.latitude) == match.latitude
    assert merchant.google_place_id == match.place_id
    assert merchant.map_match_status == "verified"
    assert merchant.verified_by_user_id == actor
    assert merchant.coordinate_verified_at == now


@pytest.mark.asyncio
async def test_approval_without_a_maps_url_still_cites_an_https_source(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    merchant = make_merchant()
    match = make_match(google_maps_url=None)
    own_the_place(monkeypatch, {})
    outcome = await apply_approval(
        None,
        google_returning(match),  # type: ignore[arg-type]
        merchant,
        expected_place_id=match.place_id,
        actor_id=uuid4(),
    )
    assert outcome == "verified"
    assert merchant.coordinate_source_url == (
        f"https://www.google.com/maps/place/?q=place_id:{match.place_id}"
    )


@pytest.mark.asyncio
async def test_korean_merchants_keep_coordinates_but_wait_for_naver(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    merchant = make_merchant(country_code="KR", destination_id="seoul")
    match = make_match()
    own_the_place(monkeypatch, {})
    outcome = await apply_approval(
        None,
        google_returning(match),  # type: ignore[arg-type]
        merchant,
        expected_place_id=match.place_id,
        actor_id=uuid4(),
    )
    assert outcome == "coordinates_saved"
    assert merchant.coordinate_source_type == "admin_verified"
    assert merchant.map_match_status == "unverified"
    assert merchant.verified_at is None


@pytest.mark.asyncio
async def test_approval_refuses_when_google_changed_its_mind(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    merchant = make_merchant()
    own_the_place(monkeypatch, {})
    outcome = await apply_approval(
        None,
        google_returning(make_match(place_id="ChIJsomethingelse00")),  # type: ignore[arg-type]
        merchant,
        expected_place_id="ChIJexample1234567890",
        actor_id=uuid4(),
    )
    assert outcome == "candidate_changed"
    assert merchant.coordinate_source_type is None


@pytest.mark.asyncio
async def test_approval_skips_conflicts_missing_results_and_done_rows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    match = make_match()
    taken = make_merchant()
    own_the_place(monkeypatch, {match.place_id: uuid4()})
    assert (
        await apply_approval(
            None,
            google_returning(match),  # type: ignore[arg-type]
            taken,
            expected_place_id=match.place_id,
            actor_id=uuid4(),
        )
        == "place_id_taken"
    )
    assert (
        await apply_approval(
            None,
            FakeGoogle({}),  # type: ignore[arg-type]
            make_merchant(),
            expected_place_id=match.place_id,
            actor_id=uuid4(),
        )
        == "no_result"
    )
    durable = make_merchant(
        latitude=Decimal("22.98"),
        longitude=Decimal("120.22"),
        coordinate_source_type="wikidata",
        coordinate_source_url="https://www.wikidata.org/wiki/Q1",
    )
    assert (
        await apply_approval(
            None,
            google_returning(match),  # type: ignore[arg-type]
            durable,
            expected_place_id=match.place_id,
            actor_id=uuid4(),
        )
        == "already_durable"
    )
    for ineligible in (
        make_merchant(review_status="rejected"),
        make_merchant(map_match_status="ambiguous"),
    ):
        assert (
            await apply_approval(
                None,
                google_returning(match),  # type: ignore[arg-type]
                ineligible,
                expected_place_id=match.place_id,
                actor_id=uuid4(),
            )
            == "not_eligible"
        )


@pytest.mark.asyncio
async def test_a_durable_type_without_a_source_url_is_still_repairable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The publication gate also demands an https source URL, so a row with only the
    type set must stay reachable by the queue instead of being stuck unpublishable."""
    match = make_match()
    own_the_place(monkeypatch, {})
    half_durable = make_merchant(
        latitude=Decimal("22.98"),
        longitude=Decimal("120.22"),
        coordinate_source_type="wikidata",
        coordinate_source_url=None,
    )
    outcome = await apply_approval(
        None,
        google_returning(match),  # type: ignore[arg-type]
        half_durable,
        expected_place_id=match.place_id,
        actor_id=uuid4(),
    )
    assert outcome == "verified"
    assert half_durable.coordinate_source_url == match.google_maps_url


@pytest.mark.asyncio
async def test_a_merchant_google_cannot_resolve_is_only_searched_once() -> None:
    from app.foods.coordinate_queue import resolve_merchant

    merchant = make_merchant()
    google = FakeGoogle({})
    assert await resolve_merchant(google, merchant) is None  # type: ignore[arg-type]
    assert await resolve_merchant(google, merchant) is None  # type: ignore[arg-type]
    assert google.searches == 1, "the empty answer must be remembered, not re-billed"


@pytest.mark.asyncio
async def test_a_resolvable_merchant_never_writes_the_negative_sentinel() -> None:
    from app.foods.coordinate_queue import resolve_merchant

    merchant = make_merchant()
    google = google_returning(make_match())
    match = await resolve_merchant(google, merchant)  # type: ignore[arg-type]
    assert match is not None and match.place_id == make_match().place_id
    assert not google.redis.store
