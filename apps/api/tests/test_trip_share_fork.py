"""What a copied stop keeps, and what stays with the author."""

from __future__ import annotations

from datetime import UTC, date, datetime
from uuid import uuid4

from app.models import TripPlanItem
from app.trips.share_router import copied_item


def source_item() -> TripPlanItem:
    return TripPlanItem(
        id=uuid4(),
        trip_plan_id=uuid4(),
        item_type="activity",
        day_date=date(2026, 11, 10),
        position=2,
        title="淺草寺",
        location_name="淺草",
        start_time=datetime(2026, 11, 10, 9, tzinfo=UTC),
        end_time=datetime(2026, 11, 10, 10, tzinfo=UTC),
        duration_minutes=60,
        latitude=35.7148,
        longitude=139.7967,
        provider_place_id="google-asakusa",
        location_source="google_places",
        locked=True,
        fixed_time=True,
        is_skipped=False,
        system_role=None,
        notes="記得帶御朱印帳",
        names_json={"title": {"original_locale": "ja"}},
        data={
            "timeline_section": "morning",
            "flight_info": {"number": "BR195"},
            "price_snapshot": {"amount": 1200},
            "ai_prompt": "作者的提示詞",
        },
    )


def test_a_copied_stop_keeps_the_plan_and_leaves_the_author_their_own_working_notes() -> None:
    trip_id = uuid4()
    source = source_item()

    copy = copied_item(trip_id, source)

    assert copy.trip_plan_id == trip_id
    assert copy.id != source.id
    assert (copy.title, copy.location_name, copy.position) == ("淺草寺", "淺草", 2)
    assert (copy.start_time, copy.end_time) == (source.start_time, source.end_time)
    assert (copy.latitude, copy.longitude) == (source.latitude, source.longitude)
    assert copy.provider_place_id == "google-asakusa"
    assert copy.locked is True and copy.fixed_time is True
    assert copy.names_json == {"title": {"original_locale": "ja"}}
    assert copy.notes is None
    assert copy.data == {
        "timeline_section": "morning",
        "flight_info": {"number": "BR195"},
    }


def test_a_stop_with_nothing_worth_copying_still_produces_a_row() -> None:
    source = TripPlanItem(
        id=uuid4(),
        trip_plan_id=uuid4(),
        item_type="suggestion",
        position=0,
        data={},
    )
    copy = copied_item(uuid4(), source)
    assert copy.data == {} and copy.notes is None
