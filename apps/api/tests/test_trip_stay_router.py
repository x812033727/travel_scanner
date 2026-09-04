from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Any
from urllib.parse import unquote
from uuid import NAMESPACE_URL, uuid4, uuid5

import fakeredis.aioredis
import pytest

import app.infra as infra
import app.trips.stay_router as stay_router
from app.config import Settings
from app.hotspots.areas import city_areas
from app.models import AffiliateClick, TripPlan, TripPlanItem, User
from app.problems import AppError
from app.providers.mock import MockProvider
from app.providers.schemas import HotelOffer, SourceMode
from app.search.schemas import SearchCreate
from app.trips.stay_router import StayHotelSelectRequest

NRT_AREAS = city_areas("NRT")
URBAN = [area for area in NRT_AREAS if area.radius_km <= 3.0]


class FakeSession:
    def __init__(self) -> None:
        self.added: list[Any] = []
        self.commits = 0

    def add(self, value: Any) -> None:
        self.added.append(value)

    async def commit(self) -> None:
        self.commits += 1

    async def get(self, _model: Any, _key: Any) -> None:
        return None


class CountingMockProvider(MockProvider):
    def __init__(self, latency: float = 0) -> None:
        super().__init__(latency=latency)
        self.calls = 0

    async def search_hotels_near(
        self, query: SearchCreate, *, latitude: float, longitude: float, radius_km: float
    ) -> list[HotelOffer]:
        self.calls += 1
        return await super().search_hotels_near(
            query, latitude=latitude, longitude=longitude, radius_km=radius_km
        )


class FakeBookingProvider:
    name = "booking"
    source_mode = SourceMode.LIVE

    async def search_hotels_near(
        self, query: SearchCreate, *, latitude: float, longitude: float, radius_km: float
    ) -> list[HotelOffer]:
        now = datetime.now(UTC)
        return [
            HotelOffer(
                id=uuid5(NAMESPACE_URL, "test:booking:777"),
                provider="booking",
                provider_offer_id="777:rate",
                booking_url="https://www.booking.com/hotel/jp/test.html?aid=999",
                retrieved_at=now,
                expires_at=now + timedelta(minutes=10),
                source_mode=SourceMode.LIVE,
                is_mock=False,
                hotel_id="777",
                hotel_name="淺草測試飯店",
                latitude=latitude,
                longitude=longitude,
                rating=4,
                room_type="雙人房",
                check_in=now,
                check_out=now + timedelta(days=5),
                nights=5,
                base_price=Decimal(20000),
                taxes=Decimal(0),
                fees=Decimal(0),
                total_price=Decimal(20000),
                breakfast_included=True,
                refundable=True,
                station_walk_minutes=0,
                nightly_price=Decimal(4000),
            )
        ]

    async def search_hotels(self, query: SearchCreate) -> list[HotelOffer]:
        return []

    async def get_hotel_details(self, hotel_id: str) -> dict[str, str]:
        return {}


def make_trip(user: User, **overrides: Any) -> TripPlan:
    values: dict[str, Any] = {
        "id": uuid4(),
        "user_id": user.id,
        "name": "東京五日",
        "mode": "manual",
        "total_price": Decimal("0"),
        "currency": "TWD",
        "data": {"travelers": {"adults": 2}, "preferences": {"hotel_min_rating": 3}},
        "version": 3,
        "destination_name": "東京",
        "start_date": date.today() + timedelta(days=60),
        "end_date": date.today() + timedelta(days=65),
        "timezone": "Asia/Tokyo",
        "route_preference": "FEWER_TRANSFERS",
    }
    values.update(overrides)
    return TripPlan(**values)


def make_rows(trip: TripPlan) -> list[TripPlanItem]:
    rows: list[TripPlanItem] = []
    for position, area in enumerate([URBAN[0], URBAN[0], URBAN[1]]):
        rows.append(
            TripPlanItem(
                id=uuid4(),
                trip_plan_id=trip.id,
                item_type="custom",
                day_date=trip.start_date,
                position=position,
                title=f"景點 {position}",
                latitude=Decimal(str(area.latitude)),
                longitude=Decimal(str(area.longitude)),
                duration_minutes=90,
                locked=False,
                is_estimated=False,
                fixed_time=False,
                is_skipped=False,
                data={},
            )
        )
    for role in ("hotel_start", "hotel_end"):
        rows.append(
            TripPlanItem(
                id=uuid4(),
                trip_plan_id=trip.id,
                item_type="custom",
                day_date=trip.start_date,
                position=len(rows),
                title="尚未設定飯店",
                system_role=role,
                locked=False,
                is_estimated=True,
                fixed_time=True,
                is_skipped=False,
                data={"source_mode": "system"},
            )
        )
    return rows


def partner_settings(**overrides: Any) -> Settings:
    values: dict[str, Any] = {
        "travel_provider_mode": "mock",
        "agoda_enabled": True,
        "agoda_cid": "cid-secret",
        "agoda_affiliate_url_template": "https://www.agoda.com/search?textToSearch={query}",
        "booking_enabled": True,
        "booking_affiliate_id": "aff-booking",
        "booking_affiliate_url_template": "https://www.booking.com/searchresults.html?ss={query}",
        "booking_demand_affiliate_id": "demand-aid",
    }
    values.update(overrides)
    return Settings.model_validate(values)


@pytest.fixture
def harness(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    user = User(id=uuid4(), email="member@example.com", password_hash="unused", is_active=True)
    trip = make_trip(user)
    rows = make_rows(trip)
    provider = CountingMockProvider()
    settings = partner_settings()
    persisted: list[tuple[int, str]] = []

    async def fake_owned_trip(_session: Any, user_id: Any, trip_id: Any) -> TripPlan:
        if user_id != user.id or trip_id != trip.id:
            raise AppError(404, "trip_not_found", "找不到這個已儲存旅程")
        return trip

    async def fake_load_items(_session: Any, _trip_id: Any) -> list[TripPlanItem]:
        return rows

    async def fake_hydrate(
        _session: Any, _trip: Any, items: list[TripPlanItem]
    ) -> list[TripPlanItem]:
        return items

    async def fake_runtime_settings(_session: Any) -> Settings:
        return settings

    async def fake_persist(
        _session: Any,
        target: TripPlan,
        _user_id: Any,
        expected_version: int,
        _rows: list[TripPlanItem],
        *,
        warning: str,
        target_day: date | None = None,
    ) -> dict[str, Any]:
        persisted.append((expected_version, warning))
        return {"id": str(target.id), "version": expected_version + 1}

    async def no_rate_limit(*_args: Any, **_kwargs: Any) -> None:
        return None

    # fakeredis has no Lua scripting, and the limiter itself is covered elsewhere.
    monkeypatch.setattr(stay_router, "enforce_named_rate_limit", no_rate_limit)
    monkeypatch.setattr(stay_router, "owned_trip", fake_owned_trip)
    monkeypatch.setattr(stay_router, "load_items", fake_load_items)
    monkeypatch.setattr(stay_router, "hydrate_legacy_items", fake_hydrate)
    monkeypatch.setattr(stay_router, "load_runtime_settings", fake_runtime_settings)
    monkeypatch.setattr(stay_router, "persist_system_schedule_change", fake_persist)
    monkeypatch.setattr(stay_router, "get_redis", lambda: redis)
    monkeypatch.setattr(infra, "get_redis", lambda: redis)
    monkeypatch.setattr(stay_router, "build_hotel_provider", lambda *_args, **_kwargs: provider)
    return {
        "redis": redis,
        "user": user,
        "trip": trip,
        "rows": rows,
        "provider": provider,
        "settings": settings,
        "persisted": persisted,
        "session": FakeSession(),
        "monkeypatch": monkeypatch,
    }


@pytest.mark.asyncio
async def test_stay_areas_recommends_from_trip_items(harness: dict[str, Any]) -> None:
    payload = await stay_router.stay_areas(
        harness["trip"].id, harness["user"], harness["session"], "zh-TW"
    )

    assert payload["status"] == "recommended"
    assert payload["city_code"] == "NRT"
    assert payload["pricing"]["available"] is True
    assert payload["current_lodging_area_code"] is None
    assert payload["areas"][0]["code"] == URBAN[0].code
    assert payload["areas"][0]["item_count"] == 2
    assert "most_items" in payload["areas"][0]["reasons"]
    assert len(payload["areas"]) >= 2

    english = await stay_router.stay_areas(
        harness["trip"].id, harness["user"], harness["session"], "en"
    )
    assert english["areas"][0]["name"].isascii()
    assert english["areas"][0]["name"] != payload["areas"][0]["name"]


@pytest.mark.asyncio
async def test_stay_areas_is_unsupported_for_unknown_destination(harness: dict[str, Any]) -> None:
    harness["trip"].destination_name = "火星基地"

    payload = await stay_router.stay_areas(
        harness["trip"].id, harness["user"], harness["session"], "zh-TW"
    )

    assert payload["status"] == "unsupported"
    assert payload["areas"] == []
    with pytest.raises(AppError) as error:
        await stay_router.stay_area_hotels(
            harness["trip"].id, URBAN[0].code, harness["user"], harness["session"], "zh-TW"
        )
    assert error.value.code == "unsupported_destination"


@pytest.mark.asyncio
async def test_other_users_get_404_and_unknown_areas_422(harness: dict[str, Any]) -> None:
    stranger = User(id=uuid4(), email="other@example.com", password_hash="x", is_active=True)
    with pytest.raises(AppError) as error:
        await stay_router.stay_areas(harness["trip"].id, stranger, harness["session"], "zh-TW")
    assert error.value.code == "trip_not_found"

    with pytest.raises(AppError) as area_error:
        await stay_router.stay_area_hotels(
            harness["trip"].id, "nowhere", harness["user"], harness["session"], "zh-TW"
        )
    assert area_error.value.code == "unsupported_area"


@pytest.mark.asyncio
async def test_area_hotels_are_priced_sorted_cached_and_linked_in_owner_order(
    harness: dict[str, Any],
) -> None:
    area = URBAN[0]
    first = await stay_router.stay_area_hotels(
        harness["trip"].id, area.code, harness["user"], harness["session"], "zh-TW"
    )

    assert first["pricing"]["status"] == "mock"
    assert first["pricing"]["cached"] is False
    assert first["nights"] == 5
    assert first["travelers"] == {"adults": 2, "children": 0, "rooms": 1}
    assert first["filters"]["applied"] == {"hotel_min_rating": 3}
    prices = [Decimal(hotel["nightly_price"]) for hotel in first["hotels"]]
    assert prices == sorted(prices)
    assert all(hotel["in_area"] for hotel in first["hotels"])
    assert all(hotel["distance_km"] <= area.radius_km for hotel in first["hotels"])
    assert [item["partner"] for item in first["hotels"][0]["partners"]] == ["agoda", "booking"]
    assert all(item["kind"] == "hotel_search" for item in first["hotels"][0]["partners"])
    assert [item["kind"] for item in first["area_partners"]] == ["area_search", "area_search"]
    assert "clickout_url" not in first["hotels"][0]["partners"][0]
    assert first["disclosure"]
    assert "cid-secret" not in str(first)
    assert "aff-booking" not in str(first)

    second = await stay_router.stay_area_hotels(
        harness["trip"].id, area.code, harness["user"], harness["session"], "zh-TW"
    )
    assert second["pricing"]["cached"] is True
    assert harness["provider"].calls == 1

    refreshed = await stay_router.stay_area_hotels(
        harness["trip"].id, area.code, harness["user"], harness["session"], "zh-TW", refresh=True
    )
    assert refreshed["pricing"]["cached"] is False
    assert harness["provider"].calls == 2


@pytest.mark.asyncio
async def test_area_hotels_degrade_without_dates_provider_or_within_timeout(
    harness: dict[str, Any],
) -> None:
    area = URBAN[0]
    monkeypatch: pytest.MonkeyPatch = harness["monkeypatch"]
    trip: TripPlan = harness["trip"]

    trip.start_date = None
    undated = await stay_router.stay_area_hotels(
        trip.id, area.code, harness["user"], harness["session"], "zh-TW"
    )
    assert undated["pricing"]["status"] == "dates_missing"
    assert undated["hotels"] == []
    assert [item["partner"] for item in undated["area_partners"]] == ["agoda", "booking"]
    assert harness["provider"].calls == 0
    trip.start_date = date.today() + timedelta(days=60)

    monkeypatch.setattr(stay_router, "build_hotel_provider", lambda *_a, **_k: None)
    unconfigured = await stay_router.stay_area_hotels(
        trip.id, area.code, harness["user"], harness["session"], "zh-TW"
    )
    assert unconfigured["pricing"]["status"] == "not_configured"
    assert unconfigured["area_partners"]

    slow = CountingMockProvider(latency=0.2)
    monkeypatch.setattr(stay_router, "build_hotel_provider", lambda *_a, **_k: slow)
    harness["settings"].hotel_area_search_timeout_seconds = 0.01
    timed_out = await stay_router.stay_area_hotels(
        trip.id, area.code, harness["user"], harness["session"], "zh-TW"
    )
    assert timed_out["pricing"]["status"] == "timeout"
    assert timed_out["hotels"] == []


@pytest.mark.asyncio
async def test_select_writes_provider_lodging_and_persists_with_version(
    harness: dict[str, Any],
) -> None:
    area = URBAN[0]
    trip: TripPlan = harness["trip"]
    listing = await stay_router.stay_area_hotels(
        trip.id, area.code, harness["user"], harness["session"], "zh-TW"
    )
    chosen = listing["hotels"][0]

    result = await stay_router.select_stay_hotel(
        trip.id,
        area.code,
        StayHotelSelectRequest(version=3, provider=chosen["provider"], hotel_id=chosen["hotel_id"]),
        harness["user"],
        harness["session"],
        "zh-TW",
    )

    assert result["version"] == 4
    assert harness["persisted"] == [(3, stay_router.LODGING_WARNING)]
    lodging = trip.data["primary_lodging"]
    assert lodging["name"] == chosen["hotel_name"]
    assert lodging["selection_source"] == "user"
    assert lodging["location_source"] == "provider"
    assert lodging["hotel_id"] == chosen["hotel_id"]
    assert lodging["provider"] == "mock"
    assert lodging["area_code"] == area.code
    assert lodging["price_snapshot"]["currency"] == "TWD"
    assert Decimal(lodging["price_snapshot"]["nightly_price"]) == Decimal(chosen["nightly_price"])
    anchors = [row for row in harness["rows"] if row.system_role in {"hotel_start", "hotel_end"}]
    assert all(chosen["hotel_name"] in (row.title or "") for row in anchors)
    assert all(row.latitude is not None and not row.is_estimated for row in anchors)
    assert all(row.data.get("needs_place_confirmation") is False for row in anchors)

    again = await stay_router.stay_area_hotels(
        trip.id, area.code, harness["user"], harness["session"], "zh-TW"
    )
    assert [hotel["is_current_lodging"] for hotel in again["hotels"]].count(True) == 1

    with pytest.raises(AppError) as error:
        await stay_router.select_stay_hotel(
            trip.id,
            area.code,
            StayHotelSelectRequest(version=4, provider="mock", hotel_id="ghost"),
            harness["user"],
            harness["session"],
            "zh-TW",
        )
    assert error.value.code == "hotel_offer_expired"
    assert len(harness["persisted"]) == 1


@pytest.mark.asyncio
async def test_clickout_renders_partner_link_at_click_time_and_records_click(
    harness: dict[str, Any],
) -> None:
    area = URBAN[0]
    trip: TripPlan = harness["trip"]
    session: Any = harness["session"]
    listing = await stay_router.stay_area_hotels(
        trip.id, area.code, harness["user"], harness["session"], "zh-TW"
    )
    chosen = listing["hotels"][0]

    response = await stay_router.stay_area_clickout(
        trip.id, area.code, "agoda", harness["user"], session, "zh-TW", hotel_id=chosen["hotel_id"]
    )

    assert response.status_code == 303
    location = response.headers["location"]
    assert location.startswith("https://www.agoda.com/search?textToSearch=")
    assert "cid=cid-secret" in location
    assert chosen["hotel_name"].split(" ")[0] in _unquote(location)
    click = session.added[-1]
    assert isinstance(click, AffiliateClick)
    assert click.trip_id == trip.id
    assert str(click.offer_id) == chosen["id"]
    assert click.partner == "agoda" and click.module == "hotel"
    assert click.target_host == "www.agoda.com"
    assert session.commits == 1

    area_only = await stay_router.stay_area_clickout(
        trip.id, area.code, "booking", harness["user"], session, "zh-TW"
    )
    assert area_only.headers["location"].startswith("https://www.booking.com/searchresults.html")
    assert "aid=aff-booking" in area_only.headers["location"]

    with pytest.raises(AppError) as unknown:
        await stay_router.stay_area_clickout(
            trip.id, area.code, "klook", harness["user"], session, "zh-TW"
        )
    assert unknown.value.code == "affiliate_partner_not_found"
    with pytest.raises(AppError) as disabled:
        await stay_router.stay_area_clickout(
            trip.id, area.code, "trip_com", harness["user"], session, "zh-TW"
        )
    assert disabled.value.code == "affiliate_partner_not_found"


@pytest.mark.asyncio
async def test_clickout_uses_booking_deep_link_without_affiliate_template(
    harness: dict[str, Any],
) -> None:
    area = URBAN[0]
    trip: TripPlan = harness["trip"]
    monkeypatch: pytest.MonkeyPatch = harness["monkeypatch"]
    monkeypatch.setattr(
        stay_router, "build_hotel_provider", lambda *_a, **_k: FakeBookingProvider()
    )
    settings = partner_settings(booking_enabled=False, booking_affiliate_url_template=None)

    async def runtime(_session: Any) -> Settings:
        return settings

    monkeypatch.setattr(stay_router, "load_runtime_settings", runtime)
    listing = await stay_router.stay_area_hotels(
        trip.id, area.code, harness["user"], harness["session"], "zh-TW"
    )
    hotel = listing["hotels"][0]
    assert hotel["provider"] == "booking"
    assert [(item["partner"], item["kind"]) for item in hotel["partners"]] == [
        ("agoda", "hotel_search"),
        ("booking", "deep_link"),
    ]
    assert "booking_url" not in str(hotel["partners"])

    response = await stay_router.stay_area_clickout(
        trip.id, area.code, "booking", harness["user"], harness["session"], "zh-TW", hotel_id="777"
    )

    location = response.headers["location"]
    assert location.startswith("https://www.booking.com/hotel/jp/test.html")
    assert location.count("aid=") == 1 and "aid=999" in location


def _unquote(value: str) -> str:
    return unquote(value)
