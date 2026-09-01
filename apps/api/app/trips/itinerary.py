from datetime import UTC, date, datetime, time, timedelta
from typing import Any
from uuid import NAMESPACE_URL, UUID, uuid5
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field

from app.destinations.catalog import DestinationProfile, destination_for_code
from app.providers.schemas import ActivityOffer, FlightOffer, HotelOffer, TransportOffer
from app.search.schemas import SearchCreate, TripPace


class ItineraryItem(BaseModel):
    id: UUID
    item_type: str
    offer_id: UUID | None = None
    day_date: date
    position: int
    title: str
    location_name: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    latitude: float | None = None
    longitude: float | None = None
    locked: bool = False
    is_estimated: bool = False
    data: dict[str, Any] = Field(default_factory=dict)
    provider_place_id: str | None = None
    location_source: str | None = None
    duration_minutes: int | None = None
    notes: str | None = None
    fixed_time: bool = False
    system_role: str | None = None
    is_skipped: bool = False


class ItineraryDay(BaseModel):
    date: date
    label: str
    items: list[ItineraryItem]


class ItineraryHotspot(BaseModel):
    hotspot_id: UUID
    name: str
    category: str
    latitude: float
    longitude: float
    depth_kind: str
    depth_score: float
    depth_reason: str
    access_minutes: int
    recommended_duration_minutes: int
    destination_id: str | None = None
    destination_role: str = "primary"
    parent_destination_id: str | None = None
    is_cross_city: bool = False


def _id(day: date, position: int, title: str) -> UUID:
    return uuid5(NAMESPACE_URL, f"travel-scanner:itinerary:{day}:{position}:{title}")


def _at(day: date, hour: int, minute: int = 0, timezone: ZoneInfo | None = None) -> datetime:
    return datetime.combine(day, time(hour, minute), tzinfo=timezone or UTC)


def _date_range(start: date, end: date) -> list[date]:
    return [start + timedelta(days=offset) for offset in range(max(1, (end - start).days + 1))]


def _suggestion_pool(
    interests: list[str], destination: DestinationProfile | None = None
) -> list[tuple[str | None, str]]:
    labels = {
        "food": "在地美食與市場探索",
        "shopping": "特色商圈與選物散步",
        "culture": "文化街區與博物館",
        "nature": "公園與自然景觀",
        "family": "親子友善城市體驗",
        "nightlife": "夜景與夜間街區",
        "spa": "按摩、溫泉與療癒時段",
        "beach": "海灘與海岸慢遊",
        "deep_travel": "在地巷弄與深度街區",
    }
    if not interests:
        return [(None, "自由探索推薦街區")]
    destination_suggestions = destination.suggestions if destination else {}
    max_titles = max(
        (len(destination_suggestions.get(interest, ())) for interest in interests),
        default=0,
    )
    pool: list[tuple[str | None, str]] = []
    for title_index in range(max(1, max_titles)):
        for interest in interests:
            titles = destination_suggestions.get(interest, ())
            title = titles[title_index] if title_index < len(titles) else labels.get(interest)
            if title and all(existing_title != title for _, existing_title in pool):
                pool.append((interest, title))
    return pool or [(None, "依照興趣探索城市")]


def _cluster_urban_hotspots(
    hotspots: list[ItineraryHotspot], start: tuple[float, float] | None
) -> list[ItineraryHotspot]:
    """Nearest-neighbour ordering keeps each day's urban route geographically compact."""
    remaining = list(hotspots)
    ordered: list[ItineraryHotspot] = []
    current = start
    while remaining:
        if current is None:
            selected = min(remaining, key=lambda item: (item.latitude, item.longitude))
        else:
            origin = current
            selected = min(
                remaining,
                key=lambda item: (
                    (item.latitude - origin[0]) ** 2 + (item.longitude - origin[1]) ** 2
                ),
            )
        ordered.append(selected)
        remaining.remove(selected)
        current = (selected.latitude, selected.longitude)
    return ordered


def build_itinerary(
    query: SearchCreate,
    flight: FlightOffer | None,
    hotel: HotelOffer | None,
    activity: ActivityOffer | None,
    transport: TransportOffer | None,
    hotspots: list[ItineraryHotspot] | None = None,
) -> list[ItineraryDay]:
    departure = query.departure_date or datetime.now(UTC).date()
    returning = query.return_date or departure + timedelta(days=4)
    days = _date_range(departure, returning)
    rows: dict[date, list[ItineraryItem]] = {day: [] for day in days}
    destination = destination_for_code(query.destination)
    destination_timezone = ZoneInfo(destination.timezone) if destination else None
    destination_context = {
        "destination_city": destination.city if destination else query.destination,
        "destination_country": destination.country_label if destination else None,
        "destination_timezone": destination.timezone if destination else "UTC",
        "local_currency": destination.currency if destination else None,
        "preferred_area": query.preferences.preferred_area,
    }

    def add(day: date, **values: Any) -> None:
        target = day if day in rows else days[0]
        position = len(rows[target])
        title = str(values["title"])
        rows[target].append(
            ItineraryItem(
                id=_id(target, position, title),
                day_date=target,
                position=position,
                **values,
            )
        )

    if flight:
        add(
            days[0],
            item_type="flight",
            offer_id=flight.id,
            title=f"{flight.airline} {flight.flight_number} 抵達旅程",
            location_name=f"{flight.origin} → {flight.destination}",
            start_time=flight.departure_time,
            end_time=flight.arrival_time,
            locked=True,
            data={
                "source_mode": flight.source_mode,
                "is_bookable": flight.is_bookable,
                "timeline_section": "logistics",
                **destination_context,
            },
        )
    if transport:
        add(
            days[0],
            item_type="transport",
            offer_id=transport.id,
            title=transport.transport_type,
            location_name=f"{transport.origin} → {transport.destination}",
            start_time=transport.departure_time,
            end_time=transport.arrival_time,
            locked=True,
            is_estimated=transport.is_estimated,
            data={
                "source_mode": transport.source_mode,
                "timeline_section": "logistics",
                **destination_context,
            },
        )
    if hotel:
        add(
            days[0],
            item_type="hotel",
            offer_id=hotel.id,
            title=f"入住 {hotel.hotel_name}",
            location_name=hotel.address or hotel.hotel_name,
            start_time=hotel.check_in,
            end_time=hotel.check_in + timedelta(minutes=30),
            latitude=hotel.latitude,
            longitude=hotel.longitude,
            locked=True,
            data={
                "source_mode": hotel.source_mode,
                "timeline_section": "logistics",
                **destination_context,
            },
        )

    full_days = days[1:-1] if len(days) > 2 else days[1:]
    activity_used = False
    blocks = 1 if query.preferences.pace == TripPace.RELAXED else 2
    if query.preferences.pace == TripPace.PACKED:
        blocks = 3
    suggestion_pool = _suggestion_pool(query.preferences.interests, destination)
    suggestion_index = 0
    deep_requested = "deep_travel" in query.preferences.interests or any(
        item.is_cross_city for item in (hotspots or [])
    )
    deep_candidates = (hotspots or []) if deep_requested else []
    day_trip_limit = 0 if len(full_days) <= 1 else (2 if len(full_days) >= 5 else 1)
    cross_city_limit = 0 if len(days) < 4 else (2 if len(days) >= 7 else 1)
    cross_city = [item for item in deep_candidates if item.is_cross_city][:cross_city_limit]
    day_trips = [
        item for item in deep_candidates if item.depth_kind == "day_trip" and not item.is_cross_city
    ][:day_trip_limit]
    urban = _cluster_urban_hotspots(
        [
            item
            for item in deep_candidates
            if item.depth_kind == "urban_local" and not item.is_cross_city
        ],
        (hotel.latitude, hotel.longitude)
        if hotel and hotel.latitude is not None and hotel.longitude is not None
        else None,
    )
    urban_index = 0
    day_trip_index = 0
    cross_city_index = 0
    for day in full_days:
        if cross_city_index < len(cross_city):
            hotspot = cross_city[cross_city_index]
            cross_city_index += 1
            start = _at(day, 8, 30, timezone=destination_timezone)
            add(
                day,
                item_type="hotspot",
                title=f"{hotspot.name}跨城深度行程",
                location_name=hotspot.name,
                start_time=start,
                end_time=start
                + timedelta(
                    minutes=hotspot.access_minutes * 2 + hotspot.recommended_duration_minutes + 90
                ),
                latitude=hotspot.latitude,
                longitude=hotspot.longitude,
                duration_minutes=hotspot.recommended_duration_minutes,
                is_estimated=False,
                location_source="hotspot_catalog",
                data={
                    "source_mode": "approved_hotspot",
                    "hotspot_id": str(hotspot.hotspot_id),
                    "destination_id": hotspot.destination_id,
                    "parent_destination_id": hotspot.parent_destination_id,
                    "is_cross_city": True,
                    "access_minutes_each_way": hotspot.access_minutes,
                    "round_trip_buffer_minutes": 90,
                    "interest": "deep_travel",
                    **destination_context,
                },
            )
            continue
        if day_trip_index < len(day_trips):
            hotspot = day_trips[day_trip_index]
            day_trip_index += 1
            start = _at(day, 9, timezone=destination_timezone)
            add(
                day,
                item_type="hotspot",
                title=hotspot.name,
                location_name=hotspot.name,
                start_time=start,
                end_time=start
                + timedelta(
                    minutes=hotspot.access_minutes * 2 + hotspot.recommended_duration_minutes + 60
                ),
                latitude=hotspot.latitude,
                longitude=hotspot.longitude,
                duration_minutes=hotspot.recommended_duration_minutes,
                is_estimated=False,
                location_source="hotspot_catalog",
                data={
                    "source_mode": "approved_hotspot",
                    "hotspot_id": str(hotspot.hotspot_id),
                    "depth_kind": hotspot.depth_kind,
                    "depth_score": hotspot.depth_score,
                    "depth_reason": hotspot.depth_reason,
                    "access_minutes_each_way": hotspot.access_minutes,
                    "round_trip_buffer_minutes": 60,
                    "interest": "deep_travel",
                    **destination_context,
                },
            )
            continue
        for block in range(blocks):
            start_hour = 10 + block * 3
            if urban_index < len(urban):
                hotspot = urban[urban_index]
                urban_index += 1
                start = _at(day, start_hour, timezone=destination_timezone)
                add(
                    day,
                    item_type="hotspot",
                    title=hotspot.name,
                    location_name=hotspot.name,
                    start_time=start,
                    end_time=start + timedelta(minutes=hotspot.recommended_duration_minutes),
                    latitude=hotspot.latitude,
                    longitude=hotspot.longitude,
                    duration_minutes=hotspot.recommended_duration_minutes,
                    is_estimated=False,
                    location_source="hotspot_catalog",
                    data={
                        "source_mode": "approved_hotspot",
                        "hotspot_id": str(hotspot.hotspot_id),
                        "depth_kind": hotspot.depth_kind,
                        "depth_score": hotspot.depth_score,
                        "depth_reason": hotspot.depth_reason,
                        "access_minutes": hotspot.access_minutes,
                        "interest": "deep_travel",
                        **destination_context,
                    },
                )
            elif activity and not activity_used:
                title = activity.title
                duration = activity.duration_minutes
                add(
                    day,
                    item_type="activity",
                    offer_id=activity.id,
                    title=title,
                    location_name=activity.address or activity.city,
                    start_time=_at(day, start_hour, timezone=destination_timezone),
                    end_time=_at(day, start_hour, timezone=destination_timezone)
                    + timedelta(minutes=duration),
                    latitude=activity.latitude,
                    longitude=activity.longitude,
                    data={"source_mode": activity.source_mode, **destination_context},
                )
                activity_used = True
            else:
                interest, title = suggestion_pool[suggestion_index % len(suggestion_pool)]
                suggestion_index += 1
                add(
                    day,
                    item_type="suggestion",
                    title=title,
                    location_name=query.preferences.preferred_area
                    or (destination.city if destination else query.destination),
                    start_time=_at(day, start_hour, timezone=destination_timezone),
                    end_time=_at(day, start_hour + 2, timezone=destination_timezone),
                    is_estimated=True,
                    data={
                        "source_mode": "estimate",
                        "needs_place_confirmation": True,
                        "interest": interest,
                        **destination_context,
                    },
                )
            if block < blocks - 1:
                add(
                    day,
                    item_type="travel",
                    title="行程間移動緩衝",
                    start_time=_at(day, start_hour + 2, timezone=destination_timezone),
                    end_time=_at(day, start_hour + 2, 30, timezone=destination_timezone),
                    is_estimated=True,
                    data={"source_mode": "estimate", "minutes": 30, **destination_context},
                )

    if hotel and len(days) > 1:
        add(
            days[-1],
            item_type="hotel",
            offer_id=hotel.id,
            title=f"從 {hotel.hotel_name} 退房",
            location_name=hotel.address or hotel.hotel_name,
            start_time=hotel.check_out,
            end_time=hotel.check_out + timedelta(minutes=20),
            latitude=hotel.latitude,
            longitude=hotel.longitude,
            locked=True,
            data={
                "source_mode": hotel.source_mode,
                "timeline_section": "logistics",
                **destination_context,
            },
        )
    if flight and flight.return_departure_time:
        add(
            days[-1],
            item_type="flight",
            offer_id=flight.id,
            title=f"搭乘 {flight.airline} 返回",
            location_name=f"{flight.destination} → {flight.origin}",
            start_time=flight.return_departure_time,
            end_time=flight.return_arrival_time,
            locked=True,
            data={
                "source_mode": flight.source_mode,
                "is_bookable": flight.is_bookable,
                "timeline_section": "logistics",
                **destination_context,
            },
        )

    meal_titles = list((destination.suggestions if destination else {}).get("food", ()))
    hotel_name = hotel.hotel_name if hotel else "尚未設定飯店"
    hotel_location = (hotel.address or hotel.hotel_name) if hotel else None
    for day_index, day_value in enumerate(days):
        add(
            day_value,
            item_type="hotel_anchor",
            title=f"從 {hotel_name} 出發",
            location_name=hotel_location,
            start_time=_at(day_value, 9, timezone=destination_timezone),
            end_time=_at(day_value, 9, timezone=destination_timezone),
            latitude=hotel.latitude if hotel else None,
            longitude=hotel.longitude if hotel else None,
            locked=True,
            fixed_time=True,
            is_estimated=hotel is None,
            duration_minutes=0,
            system_role="hotel_start",
            data={
                "source_mode": "system",
                "needs_place_confirmation": hotel is None,
                **destination_context,
            },
        )
        for role, hour, minute, duration, offset, label in (
            ("lunch", 12, 0, 60, 0, "午餐"),
            ("dinner", 18, 30, 90, 1, "晚餐"),
        ):
            title = (
                meal_titles[(day_index * 2 + offset) % len(meal_titles)]
                if meal_titles
                else label
            )
            starts = _at(day_value, hour, minute, timezone=destination_timezone)
            add(
                day_value,
                item_type="meal",
                title=title,
                location_name=(destination.city if destination else query.destination),
                start_time=starts,
                end_time=starts + timedelta(minutes=duration),
                locked=True,
                fixed_time=True,
                is_estimated=True,
                duration_minutes=duration,
                system_role=role,
                data={
                    "source_mode": "catalog",
                    "meal_kind": role,
                    "meal_selection_source": "catalog" if meal_titles else "unset",
                    "needs_place_confirmation": True,
                    **destination_context,
                },
            )
        add(
            day_value,
            item_type="hotel_anchor",
            title=f"返回 {hotel_name}",
            location_name=hotel_location,
            latitude=hotel.latitude if hotel else None,
            longitude=hotel.longitude if hotel else None,
            locked=True,
            is_estimated=hotel is None,
            duration_minutes=0,
            system_role="hotel_end",
            data={
                "source_mode": "system",
                "needs_place_confirmation": hotel is None,
                **destination_context,
            },
        )

    logistics_types = {"flight", "transport", "hotel"}
    for day_value in days:
        route_rows = [
            item
            for item in rows[day_value]
            if not (item.system_role is None and item.item_type in logistics_types)
        ]
        logistics = [item for item in rows[day_value] if item not in route_rows]
        route_rows.sort(
            key=lambda item: (
                0
                if item.system_role == "hotel_start"
                else 2
                if item.system_role == "hotel_end"
                else 1,
                item.start_time or datetime.max.replace(tzinfo=destination_timezone or UTC),
                item.position,
            )
        )
        rows[day_value] = [*route_rows, *logistics]
        for position, item in enumerate(rows[day_value]):
            item.position = position

    labels = [
        "抵達與入住",
        *[
            f"{destination.city if destination else '城市'}探索 Day {index + 2}"
            for index in range(len(days) - 2)
        ],
        "返程",
    ]
    if len(days) == 1:
        labels = ["一日旅程"]
    elif len(days) == 2:
        labels = ["抵達與入住", "返程"]
    return [
        ItineraryDay(date=day, label=labels[index], items=rows[day])
        for index, day in enumerate(days)
    ]
