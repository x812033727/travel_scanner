from datetime import date, datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

from app.models import TripPlanItem
from app.trips.router import ItineraryItemRequest, apply_item_request
from app.trips.schedule import canonicalize_positions, insert_scheduled_rows

DAY = date(2026, 11, 11)


def row(title: str, position: int, role: str | None = None, hour: int = 10) -> TripPlanItem:
    return TripPlanItem(
        id=uuid4(),
        trip_plan_id=uuid4(),
        item_type="custom",
        title=title,
        position=position,
        day_date=DAY,
        system_role=role,
        locked=role is not None,
        is_skipped=False,
        fixed_time=role is not None,
        start_time=datetime(2026, 11, 11, hour, tzinfo=ZoneInfo("Asia/Tokyo")),
        data={},
    )


def titles(rows: list[TripPlanItem]) -> list[str]:
    return [item.title for item in sorted(rows, key=lambda item: item.position)]


def test_manual_location_does_not_keep_old_catalogue_coordinate_provenance() -> None:
    record = row("Temple", 1)
    record.data = {"catalog_selection": {"kind": "hotspot", "id": str(uuid4())}}
    record.coordinate_source_type = "wikidata"
    record.coordinate_source_url = "https://www.wikidata.org/wiki/Q617422"
    apply_item_request(
        record,
        ItineraryItemRequest(
            item_type="custom", title="My new stop", day_date=DAY, position=1, data={}
        ),
    )
    assert record.coordinate_source_type is None
    assert record.coordinate_source_url is None


def test_manual_position_wins_over_old_route_times_and_fixed_start_times() -> None:
    rows = [
        row("hotel", 0, "hotel_start", 9),
        row("later", 1, hour=17),
        row("lunch", 2, "lunch", 12),
        row("earlier", 3, hour=10),
        row("dinner", 4, "dinner", 18),
        row("home", 5, "hotel_end", 22),
    ]
    rows[1].fixed_time = True
    assert not canonicalize_positions(rows)
    assert titles(rows) == ["hotel", "later", "lunch", "earlier", "dinner", "home"]
    assert not canonicalize_positions(rows)
    assert rows[1].start_time.hour == 17


def test_anchors_keep_outer_edges_and_meal_relative_order() -> None:
    rows = [
        row("home", 0, "hotel_end"),
        row("dinner", 1, "dinner"),
        row("ordinary", 2),
        row("lunch", 3, "lunch"),
        row("hotel", 4, "hotel_start"),
        row("return", 5, "return_flight"),
        row("outbound", 6, "outbound_flight"),
    ]
    canonicalize_positions(rows)
    assert titles(rows) == ["outbound", "hotel", "lunch", "ordinary", "dinner", "home", "return"]
    assert not canonicalize_positions(rows)


def test_new_ai_stop_uses_proposed_time_without_resorting_preserved_manual_rows() -> None:
    rows = [
        row("hotel", 0, "hotel_start", 9),
        row("manual later", 1, hour=16),
        row("manual earlier", 2, hour=10),
        row("home", 3, "hotel_end", 22),
    ]
    addition = row("AI", 0, hour=11)
    rows.append(addition)
    insert_scheduled_rows(rows, [addition])
    canonicalize_positions(rows)
    assert titles(rows) == ["hotel", "AI", "manual later", "manual earlier", "home"]


def test_skipped_meal_stays_in_user_order_without_rearranging_other_cards() -> None:
    rows = [
        row("lunch", 0, "lunch", 12),
        row("morning stop", 1, hour=9),
        row("dinner", 2, "dinner", 18),
    ]
    rows[0].is_skipped = True
    canonicalize_positions(rows)
    assert titles(rows) == ["lunch", "morning stop", "dinner"]
