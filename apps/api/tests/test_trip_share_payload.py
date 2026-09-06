"""The share link shows the itinerary, not what the owner wrote or paid.

``serialize_item`` is the owner's view and also the round trip back into the
editor, so it carries ``notes`` and the whole ``data`` blob. ``public_item`` is what
``GET /shared-trips/{token}`` hands to anyone with the URL: an allowlist of the
fields the shared timeline draws. These tests pin that allowlist without a
database; the integration suite checks the endpoint end to end.
"""

from datetime import UTC, date, datetime
from uuid import uuid4

from app.models import TripPlanItem
from app.trips.router import PUBLIC_ITEM_KEYS, PUBLIC_TRIP_KEYS, public_item, serialize_item


def _row(**overrides: object) -> TripPlanItem:
    values: dict[str, object] = {
        "id": uuid4(),
        "trip_plan_id": uuid4(),
        "item_type": "activity",
        "day_date": date(2026, 11, 11),
        "position": 2,
        "title": "淺草寺",
        "location_name": "淺草寺",
        "names_json": {},
        "start_time": datetime(2026, 11, 11, 1, 0, tzinfo=UTC),
        "end_time": datetime(2026, 11, 11, 2, 30, tzinfo=UTC),
        "latitude": 35.714765,
        "longitude": 139.796655,
        "locked": False,
        "is_estimated": False,
        "fixed_time": False,
        "is_skipped": False,
        "duration_minutes": 90,
        "notes": "記得帶零錢，御守要買給媽媽",
        "offer_id": uuid4(),
        "provider_place_id": "ChIJ8T1GpMGOGGARDYGSgpooDWw",
        "location_source": "hotspot_catalog",
        "data": {
            "timeline_section": "activity",
            "reason": "AI 覺得你會喜歡",
            "generated_by": "ai_planner",
            "price_snapshot": {"total_price": "1200", "currency": "TWD"},
            "hotspot_id": "hotspot-1",
        },
    }
    values.update(overrides)
    return TripPlanItem(**values)


def test_public_item_keeps_only_what_the_timeline_draws() -> None:
    row = _row()
    full = serialize_item(row, locale="zh-TW")
    public = public_item(full)

    assert set(public) == {*PUBLIC_ITEM_KEYS, "data"}
    assert "notes" not in public
    assert "offer_id" not in public
    assert "provider_place_id" not in public
    assert "location_source" not in public
    assert "location_provider" not in public
    assert public["data"] == {"timeline_section": "activity"}
    # What survives is exactly the owner's value, so the two views cannot drift.
    for key in PUBLIC_ITEM_KEYS:
        assert public[key] == full[key]


def test_public_item_keeps_the_flight_schedule_but_not_the_quote() -> None:
    row = _row(
        item_type="flight",
        system_role="return_flight",
        title="JAL JL802",
        data={
            "timeline_section": "flight_anchor",
            "source_mode": "manual",
            "flight_selection_source": "manual",
            "price_snapshot": {"total_price": "18800", "currency": "TWD"},
            "flight_info": {
                "airline": "JAL",
                "flight_number": "JL802",
                "origin": "NRT",
                "destination": "TPE",
                "departure_local": "2026-11-12T14:05",
                "arrival_local": "2026-11-12T17:10",
                "departure_timezone": "Asia/Tokyo",
                "arrival_timezone": "Asia/Taipei",
                "booking_reference": "ABC123",
                "fare_family": "Economy Saver",
            },
        },
    )
    public = public_item(serialize_item(row, locale="en"))
    assert public["data"] == {
        "timeline_section": "flight_anchor",
        "flight_info": {
            "airline": "JAL",
            "flight_number": "JL802",
            "origin": "NRT",
            "destination": "TPE",
            "departure_local": "2026-11-12T14:05",
            "arrival_local": "2026-11-12T17:10",
            "departure_timezone": "Asia/Tokyo",
            "arrival_timezone": "Asia/Taipei",
        },
    }


def test_an_unset_anchor_and_a_bare_row_serialize_without_surprises() -> None:
    unset = _row(data={"timeline_section": "flight_anchor", "flight_info": None}, notes=None)
    assert public_item(serialize_item(unset))["data"] == {"timeline_section": "flight_anchor"}
    bare = _row(data={}, notes=None, offer_id=None)
    assert public_item(serialize_item(bare))["data"] == {}


def test_the_trip_level_allowlist_names_no_private_field() -> None:
    private = {
        "data",
        "notes",
        "day_notes",
        "cost",
        "pricing",
        "total_price",
        "currency",
        "usage",
        "share_enabled",
        "user_id",
        "primary_lodging",
        "planning",
        "version",
    }
    assert not private & set(PUBLIC_TRIP_KEYS)
