from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from app.hotspots.maps import build_map_links, has_exact_map_identity
from app.locations.map_identity import (
    MapIdentity,
    catalog_map_identities,
    naver_place_id,
    normalize_map_identities,
)
from app.models import FoodMerchant, TravelHotspot, TravelServiceProduct
from app.travel_services.service import public_product


def verified(place_id="ChIJreviewed"):
    return MapIdentity(
        provider="google_places",
        place_id=place_id,
        status="verified",
        verified_at=datetime.now(UTC),
        verified_by_user_id=uuid4(),
        evidence_url="https://editorial.example/review",
    ).model_dump(mode="json")


def merchant(**changes):
    values = dict(
        id=uuid4(),
        name="한국식당",
        local_name="한국식당",
        country_code="KR",
        destination_id="seoul",
        google_place_id="ChIJreviewed",
        naver_map_url="https://map.naver.com/p/entry/place/12345",
        map_match_status="verified",
        latitude=Decimal("37.57"),
        longitude=Decimal("126.98"),
        map_identity_metadata={},
    )
    return FoodMerchant(**{**values, **changes})


def links(row):
    return build_map_links(
        name=row.name,
        local_name=row.local_name,
        city_name="Seoul",
        country_code=row.country_code,
        latitude=row.latitude,
        longitude=row.longitude,
        google_place_id=row.google_place_id,
        naver_map_url=row.naver_map_url,
        map_match_status=row.map_match_status,
        map_identities=catalog_map_identities(row),
    )


def test_legacy_korean_google_id_needs_independent_review_but_naver_stays_public():
    row = merchant()
    assert catalog_map_identities(row)["google_places"]["status"] == "unverified"
    assert [link["provider"] for link in links(row)] == ["naver"]
    assert has_exact_map_identity("KR", None, row.naver_map_url)
    assert not has_exact_map_identity("KR", row.google_place_id, None)


def test_reviewed_secondary_google_link_is_exact_and_not_primary():
    row = merchant(map_identity_metadata={"map_identities": {"google_places": verified()}})
    assert [link["provider"] for link in links(row)] == ["naver", "google"]
    assert links(row)[1]["primary"] is False
    assert "query_place_id=ChIJreviewed" in links(row)[1]["url"]
    assert "verified_by_user_id" not in catalog_map_identities(row)["google_places"]
    assert "evidence_url" not in catalog_map_identities(row)["google_places"]


@pytest.mark.parametrize("status", ["pending", "rejected", "unverified"])
def test_unverified_secondary_identity_never_gains_exact_link(status):
    identity = {**verified(), "status": status}
    row = merchant(map_identity_metadata={"map_identities": {"google_places": identity}})
    assert [link["provider"] for link in links(row)] == ["naver"]


def test_changed_scalar_id_does_not_reuse_a_different_google_verification():
    row = merchant(
        google_place_id="ChIJchanged",
        map_identity_metadata={
            "map_identities": {"google_places": verified()},
        },
    )
    assert [link["provider"] for link in links(row)] == ["naver"]


@pytest.mark.parametrize("status", ["verified", "pending", "rejected", "unverified"])
def test_matching_naver_metadata_preserves_independent_status_and_time(status):
    naver = MapIdentity(
        provider="naver_maps",
        place_id="12345",
        map_url="https://map.naver.com/v5/entry/place/12345?review=1",
        status=status,
        verified_at=datetime(2026, 8, 1, tzinfo=UTC),
        verified_by_user_id=uuid4(),
        evidence_url="https://editorial.example/naver-review",
    ).model_dump(mode="json")
    google = verified()
    row = merchant(
        map_identity_metadata={"map_identities": {"naver_maps": naver, "google_places": google}}
    )
    projected = catalog_map_identities(row)
    assert projected["naver_maps"]["status"] == status
    assert projected["naver_maps"]["verified_at"] == naver["verified_at"]
    assert "evidence_url" not in projected["naver_maps"]
    assert "verified_by_user_id" not in projected["naver_maps"]
    assert row.map_identity_metadata["map_identities"]["naver_maps"] == naver
    assert projected["google_places"]["verified_at"] == google["verified_at"]
    assert projected["google_places"]["status"] == "verified"
    row.map_match_status = "disabled"
    assert catalog_map_identities(row)["naver_maps"]["status"] == status
    assert links(row) == []


def test_changed_naver_url_does_not_reuse_previous_provider_review():
    row = merchant(
        map_identity_metadata={
            "map_identities": {
                "naver_maps": {
                    "provider": "naver_maps",
                    "map_url": "https://map.naver.com/p/entry/place/99999",
                    "status": "verified",
                    "verified_at": "2026-08-01T00:00:00Z",
                },
                "google_places": verified(),
            }
        }
    )
    projected = catalog_map_identities(row)
    assert projected["naver_maps"]["place_id"] == "12345"
    assert projected["naver_maps"]["status"] == "unverified"
    assert projected["naver_maps"]["verified_at"] is None
    assert projected["google_places"]["status"] == "verified"


def test_legacy_hotspot_uses_map_review_time_without_changing_publication_gate():
    row = TravelHotspot(
        country_code="KR",
        map_match_status="verified",
        naver_map_url="https://map.naver.com/p/entry/place/12345",
        map_verified_at=datetime(2026, 8, 1, tzinfo=UTC),
        metadata_json={},
    )
    projected = catalog_map_identities(row)
    assert projected["naver_maps"]["verified_at"] == "2026-08-01T00:00:00Z"
    row.map_match_status = "disabled"
    assert catalog_map_identities(row)["naver_maps"]["status"] == "unverified"
    assert build_map_links(
        name="Palace", local_name=None, city_name="Seoul", country_code="KR",
        latitude=None, longitude=None, naver_map_url=row.naver_map_url,
        map_match_status=row.map_match_status, map_identities=projected,
    ) == []


@pytest.mark.parametrize(
    "url",
    [
        "https://map.naver.com/p/search/12345",
        "https://map.naver.com/p/entry/place/hash-key",
        "https://map.naver.com.evil.test/p/entry/place/12345",
        "nmap://place/12345",
    ],
)
def test_search_hash_and_untrusted_urls_cannot_be_exact_naver_identity(url):
    assert naver_place_id(url) is None


def test_identity_normalizer_generates_official_targets_and_redacts_own_review_details():
    normalized = normalize_map_identities(
        {
            "google_places": {
                **verified(),
                "map_url": "https://malicious.example/path",
            }
        }
    )
    assert normalized["google_places"]["map_url"].startswith("https://www.google.com/maps/search/")
    assert set(normalized["google_places"]) == {
        "provider",
        "place_id",
        "map_url",
        "status",
        "verified_at",
    }


def test_hotspot_adapter_uses_existing_metadata_without_new_catalog_row():
    row = TravelHotspot(
        country_code="KR",
        google_place_id="ChIJreviewed",
        map_match_status="verified",
        naver_map_url="https://map.naver.com/v5/entry/place/12345?x=1",
        metadata_json={"map_identities": {"google_places": verified()}},
    )
    assert catalog_map_identities(row)["naver_maps"]["place_id"] == "12345"
    assert catalog_map_identities(row)["google_places"]["status"] == "verified"


def test_public_hotel_exposes_both_links_without_private_review_metadata():
    row = TravelServiceProduct(
        id=uuid4(),
        kind="hotel",
        destination_id="seoul",
        title="서울호텔",
        names_json={},
        source_url="https://hotel.example/",
        facts={
            "google_place_id": "ChIJreviewed",
            "naver_map_url": "https://map.naver.com/p/entry/place/12345",
            "map_verified": True,
            "map_identities": {"google_places": verified()},
            "map_identity_review": {"revision": 2, "note": "private review note"},
        },
    )
    result = public_product(row, "ko", datetime.now(UTC))
    assert [link["provider"] for link in result["map_links"]] == ["naver", "google"]
    assert "map_identity_review" not in result["facts"]
    assert "verified_by_user_id" not in result["facts"]["map_identities"]["google_places"]


def test_additive_migration_preserves_legacy_identity_and_coordinates(monkeypatch):
    import importlib.util
    from pathlib import Path

    import sqlalchemy as sa
    from alembic.migration import MigrationContext
    from alembic.operations import Operations

    path = Path(__file__).parents[1] / "migrations/versions/0070_map_identity_metadata.py"
    spec = importlib.util.spec_from_file_location("map_identity_migration", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    engine = sa.create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(
            sa.text(
                "CREATE TABLE food_merchants (id INTEGER PRIMARY KEY, latitude TEXT, "
                "google_place_id TEXT, naver_map_url TEXT, review_status TEXT)"
            )
        )
        connection.execute(
            sa.text(
                "INSERT INTO food_merchants VALUES (1, '37.570000', 'legacy-google', "
                "'https://map.naver.com/p/entry/place/12345', 'pending')"
            )
        )
        before = connection.execute(sa.text("SELECT * FROM food_merchants")).first()
        with Operations.context(MigrationContext.configure(connection)):
            module.upgrade()
            module.upgrade()
            after = connection.execute(sa.text("SELECT * FROM food_merchants")).first()
            assert after[:5] == tuple(before) and after[5] == "{}"
            module.downgrade()
            assert tuple(
                connection.execute(sa.text("SELECT * FROM food_merchants")).first()
            ) == tuple(before)
    engine.dispose()
