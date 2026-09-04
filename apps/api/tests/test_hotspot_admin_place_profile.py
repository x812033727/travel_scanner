from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from app.hotspots.admin_router import _sync_map_match_status
from app.models import TravelHotspot


def _hotspot(*, country_code: str = "JP", **changes: object) -> TravelHotspot:
    fields: dict[str, object] = {
        "id": uuid4(),
        "slug": "sensoji",
        "name": "淺草寺",
        "city_code": "NRT",
        "destination_id": "tokyo",
        "city_name": "東京",
        "country_code": country_code,
        "country_name": "日本",
        "category": "culture",
        "search_text": "淺草寺",
        "latitude": Decimal("35.714765"),
        "longitude": Decimal("139.796655"),
        "coordinate_source_type": "wikidata",
        "coordinate_source_url": "https://www.wikidata.org/wiki/Q252039",
        "map_match_status": "unverified",
        "metadata_json": {},
    }
    fields.update(changes)
    return TravelHotspot(**fields)


def test_assigning_a_place_id_verifies_the_map_match() -> None:
    actor = uuid4()
    hotspot = _hotspot(google_place_id="ChIJ8T1GpMGOGGARDYGSgpooDWw")

    _sync_map_match_status(hotspot, actor_id=actor)

    assert hotspot.map_match_status == "verified"
    assert hotspot.map_verified_by_user_id == actor
    assert hotspot.map_verified_at is not None


def test_a_google_place_id_never_verifies_a_korean_hotspot() -> None:
    # Korea's exact identity is a Naver place URL; a Google ID says nothing there.
    hotspot = _hotspot(country_code="KR", google_place_id="ChIJ8T1GpMGOGGARDYGSgpooDWw")

    _sync_map_match_status(hotspot, actor_id=uuid4())

    assert hotspot.map_match_status == "unverified"
    assert hotspot.map_verified_at is None


def test_a_naver_place_url_verifies_a_korean_hotspot() -> None:
    hotspot = _hotspot(
        country_code="KR",
        naver_map_url="https://map.naver.com/p/entry/place/11592031",
    )

    _sync_map_match_status(hotspot, actor_id=uuid4())

    assert hotspot.map_match_status == "verified"


def test_clearing_the_place_id_drops_the_verification() -> None:
    hotspot = _hotspot(
        google_place_id=None,
        map_match_status="verified",
        map_verified_at=datetime.now(UTC),
        map_verified_by_user_id=uuid4(),
    )

    _sync_map_match_status(hotspot, actor_id=uuid4())

    assert hotspot.map_match_status == "unverified"
    assert hotspot.map_verified_at is None
    assert hotspot.map_verified_by_user_id is None


def test_an_already_verified_hotspot_keeps_its_original_reviewer() -> None:
    original_actor = uuid4()
    verified_at = datetime.now(UTC)
    hotspot = _hotspot(
        google_place_id="ChIJ8T1GpMGOGGARDYGSgpooDWw",
        map_match_status="verified",
        map_verified_at=verified_at,
        map_verified_by_user_id=original_actor,
    )

    _sync_map_match_status(hotspot, actor_id=uuid4())

    assert hotspot.map_verified_by_user_id == original_actor
    assert hotspot.map_verified_at == verified_at
