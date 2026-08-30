from datetime import UTC, date, datetime, time, timedelta
from typing import Any
from uuid import NAMESPACE_URL, UUID, uuid5

from pydantic import BaseModel, Field

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


def _at(day: date, hour: int, minute: int = 0) -> datetime:
    return datetime.combine(day, time(hour, minute), tzinfo=UTC)


def _date_range(start: date, end: date) -> list[date]:
    return [start + timedelta(days=offset) for offset in range(max(1, (end - start).days + 1))]


def _interest_title(interests: list[str], index: int) -> str:
    labels = {
        "food": "在地美食與市場探索",
        "shopping": "特色商圈與選物散步",
        "culture": "文化街區與博物館",
        "nature": "公園與自然景觀",
    }
    if not interests:
        return "自由探索推薦街區"
    return labels.get(interests[index % len(interests)], "依照興趣探索城市")


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
            data={"source_mode": flight.source_mode, "is_bookable": flight.is_bookable},
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
            data={"source_mode": transport.source_mode},
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
            data={"source_mode": hotel.source_mode},
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
                    start_time=_at(day, start_hour),
                    end_time=_at(day, start_hour) + timedelta(minutes=duration),
                    latitude=activity.latitude,
                    longitude=activity.longitude,
                    data={"source_mode": activity.source_mode},
                )
                activity_used = True
            else:
                title = _interest_title(query.preferences.interests, day_index + block)
                add(
                    day,
                    item_type="suggestion",
                    title=title,
                    location_name=query.preferences.preferred_area or query.destination,
                    start_time=_at(day, start_hour),
                    end_time=_at(day, start_hour + 2),
                    is_estimated=True,
                    data={"source_mode": "estimate", "needs_place_confirmation": True},
                )
            if block < blocks - 1:
                add(
                    day,
                    item_type="travel",
                    title="行程間移動緩衝",
                    start_time=_at(day, start_hour + 2),
                    end_time=_at(day, start_hour + 2, 30),
                    is_estimated=True,
                    data={"source_mode": "estimate", "minutes": 30},
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
            data={"source_mode": hotel.source_mode},
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
            data={"source_mode": flight.source_mode, "is_bookable": flight.is_bookable},
        )

    labels = [
        "抵達與入住",
        *[f"城市探索 Day {index + 2}" for index in range(len(days) - 2)],
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
