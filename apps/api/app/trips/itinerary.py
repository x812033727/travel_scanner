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


class ItineraryDay(BaseModel):
    date: date
    label: str
    items: list[ItineraryItem]


def _id(day: date, position: int, title: str) -> UUID:
    return uuid5(NAMESPACE_URL, f"travel-scanner:itinerary:{day}:{position}:{title}")


def _at(day: date, hour: int, minute: int = 0, timezone: ZoneInfo | None = None) -> datetime:
    return datetime.combine(day, time(hour, minute), tzinfo=timezone or UTC)


def _date_range(start: date, end: date) -> list[date]:
    return [start + timedelta(days=offset) for offset in range(max(1, (end - start).days + 1))]


def _interest_title(
    interests: list[str], index: int, destination: DestinationProfile | None = None
) -> str:
    labels = {
        "food": "在地美食與市場探索",
        "shopping": "特色商圈與選物散步",
        "culture": "文化街區與博物館",
        "nature": "公園與自然景觀",
        "family": "親子友善城市體驗",
        "nightlife": "夜景與夜間街區",
        "spa": "按摩、溫泉與療癒時段",
        "beach": "海灘與海岸慢遊",
    }
    if not interests:
        return "自由探索推薦街區"
    interest = interests[index % len(interests)]
    destination_titles = destination.suggestions.get(interest, ()) if destination else ()
    if destination_titles:
        return destination_titles[index % len(destination_titles)]
    return labels.get(interest, "依照興趣探索城市")


def build_itinerary(
    query: SearchCreate,
    flight: FlightOffer | None,
    hotel: HotelOffer | None,
    activity: ActivityOffer | None,
    transport: TransportOffer | None,
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
            data={"source_mode": transport.source_mode, **destination_context},
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
            data={"source_mode": hotel.source_mode, **destination_context},
        )

    full_days = days[1:-1] if len(days) > 2 else days[1:]
    activity_used = False
    blocks = 1 if query.preferences.pace == TripPace.RELAXED else 2
    if query.preferences.pace == TripPace.PACKED:
        blocks = 3
    for day_index, day in enumerate(full_days):
        for block in range(blocks):
            start_hour = 10 + block * 3
            if activity and not activity_used:
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
                title = _interest_title(query.preferences.interests, day_index + block, destination)
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
            data={"source_mode": hotel.source_mode, **destination_context},
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
                **destination_context,
            },
        )

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
