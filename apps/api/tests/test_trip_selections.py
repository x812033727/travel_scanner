"""The four ``trip-selections`` endpoints share one placement (app.trips.selections).

``append`` (the default) adds a stop after the day's last position; ``replace_meal``
fills the day's lunch or dinner card in place. A card the traveller already chose a
place for answers ``409 meal_slot_occupied`` until the request says ``overwrite``.
Every case runs through all four routers, because the point is that they agree.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

import fakeredis
import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.auth.service import current_user
from app.db import Base, get_session
from app.foods.router import router as foods_router
from app.hotspots.router import router as hotspots_router
from app.models import (
    FoodMerchant,
    FoodMerchantFood,
    FoodMerchantSource,
    RestaurantPlace,
    TravelFood,
    TravelHotspot,
    TripPlan,
    TripPlanItem,
    User,
)
from app.problems import AppError, app_error_handler, validation_error_handler
from app.restaurants.user_router import router as restaurants_router
from app.trips import router as trips
from app.trips.schedule import MEAL_PLACEHOLDER_LABELS, ensure_system_slots

KINDS = ("hotspot", "restaurant", "food", "merchant")
DAY = date(2027, 3, 11)


class Harness:
    def __init__(self, client: AsyncClient, factory: Any, ids: dict[str, Any]) -> None:
        self.client = client
        self.factory = factory
        self.ids = ids
        self.version = 1

    def path(self, kind: str) -> str:
        return {
            "hotspot": f"/hotspots/{self.ids['hotspot']}/trip-selections",
            "restaurant": f"/restaurants/{self.ids['place_id']}/trip-selections",
            "food": f"/foods/{self.ids['food']}/trip-selections",
            "merchant": f"/foods/merchants/{self.ids['merchant']}/trip-selections",
        }[kind]

    def body(self, kind: str, **extra: Any) -> dict[str, Any]:
        base: dict[str, Any] = {
            "trip_id": str(self.ids["trip"]),
            "version": self.version,
            "day_date": DAY.isoformat(),
        }
        if kind == "food":
            base["merchant_id"] = str(self.ids["merchant"])
        return {**base, **extra}

    async def select(self, kind: str, **extra: Any) -> Any:
        response = await self.client.post(self.path(kind), json=self.body(kind, **extra))
        if response.status_code == 200:
            self.version = response.json()["version"]
        return response

    async def day_rows(self, day: date = DAY) -> list[TripPlanItem]:
        async with self.factory() as session:
            rows = await trips.load_items(session, self.ids["trip"])
        return [row for row in rows if row.day_date == day]


def meal_card(rows: list[TripPlanItem], role: str) -> TripPlanItem:
    return next(row for row in rows if row.system_role == role)


def placeholder(card: TripPlanItem) -> bool:
    return (
        card.title == MEAL_PLACEHOLDER_LABELS[card.system_role or ""]["zh-TW"]
        and card.provider_place_id is None
        and card.data.get("meal_selection_source") == "unset"
    )


@pytest_asyncio.fixture
async def harness(monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[Harness]:
    engine = create_async_engine("sqlite+aiosqlite://")

    @event.listens_for(engine.sync_engine, "connect")
    def sqlite_functions(connection: Any, _: Any) -> None:
        # publishable_merchant_filters() trims the Google place id in SQL.
        connection.create_function("btrim", 1, lambda value: value.strip() if value else value)
        connection.execute("PRAGMA foreign_keys=ON")

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(trips, "get_redis", lambda: redis)

    async def no_routing(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("adding a place must not spend a routing request")

    monkeypatch.setattr(trips, "enqueue_trip_routing", no_routing)
    now = datetime.now(UTC)
    suffix = uuid4().hex
    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        factory = async_sessionmaker(engine, expire_on_commit=False)
        async with factory() as session:
            user = User(id=uuid4(), email=f"{suffix}@example.test", is_active=True)
            session.add(user)
            await session.flush()
            trip = TripPlan(
                id=uuid4(),
                user_id=user.id,
                name="Tokyo",
                mode="manual",
                total_price=Decimal("0"),
                currency="TWD",
                version=1,
                destination_name="Tokyo",
                start_date=DAY,
                end_date=date(2027, 3, 13),
                timezone="Asia/Tokyo",
                data={},
            )
            session.add(trip)
            await session.flush()
            ensure_system_slots(session, trip, [])
            hotspot = TravelHotspot(
                slug=f"selection-hotspot-{suffix}",
                name="淺草寺",
                city_code="NRT",
                destination_id="tokyo",
                city_name="東京",
                country_code="JP",
                country_name="日本",
                category="culture",
                search_text="sensoji",
                latitude=Decimal("35.714765"),
                longitude=Decimal("139.796655"),
                coordinate_source_type="wikidata",
                coordinate_source_url="https://www.wikidata.org/wiki/Q617422",
                coordinate_verified_at=now,
                google_place_id=f"hotspot-place-{suffix}",
                map_match_status="verified",
                review_status="approved",
                is_active=True,
                metadata_json={"local_name": "浅草寺", "recommended_duration_minutes": 75},
            )
            merchant = FoodMerchant(
                slug=f"selection-merchant-{suffix}",
                destination_id="tokyo",
                country_code="JP",
                name="Ichiran Shibuya",
                local_name="一蘭 渋谷店",
                names_json={"zh-TW": "一蘭 澀谷店"},
                latitude=Decimal("35.661777"),
                longitude=Decimal("139.700294"),
                coordinate_source_type="merchant_official",
                coordinate_source_url="https://example.test/ichiran/shibuya",
                coordinate_verified_at=now,
                google_place_id=f"merchant-place-{suffix}",
                map_match_status="verified",
                review_status="approved",
                is_active=True,
                verified_at=now,
            )
            food = TravelFood(
                slug=f"selection-food-{suffix}",
                country_code="JP",
                local_name="ラーメン",
                romanized_name="Ramen",
                food_kind="noodle_soup",
                meal_types=["lunch", "dinner"],
                search_text="ramen",
                source_urls=["https://example.test/ramen"],
                review_status="approved",
                is_active=True,
            )
            place = RestaurantPlace(
                google_place_id=f"restaurant-place-{suffix}",
                generated_maps_url="https://www.google.com/maps/place/?q=place_id:x",
                identity_status="active",
            )
            session.add_all([hotspot, merchant, food, place])
            await session.flush()
            session.add_all(
                [
                    FoodMerchantFood(merchant_id=merchant.id, food_id=food.id, is_primary=True),
                    FoodMerchantSource(
                        merchant_id=merchant.id,
                        source_type="merchant_official",
                        source_scope="merchant_listing",
                        source_title="Official shop page",
                        source_url="https://example.test/ichiran/shibuya",
                        claims_json=["name"],
                        is_current=True,
                    ),
                ]
            )
            await session.commit()
            ids = {
                "user": user.id,
                "trip": trip.id,
                "hotspot": hotspot.id,
                "merchant": merchant.id,
                "food": food.id,
                "place_id": place.google_place_id,
                "hotspot_place_id": hotspot.google_place_id,
                "merchant_place_id": merchant.google_place_id,
            }

        async def database() -> AsyncIterator[Any]:
            async with factory() as session:
                yield session

        async def member() -> User:
            async with factory() as session:
                found = await session.get(User, ids["user"])
                assert found is not None
                return found

        app = FastAPI()
        app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
        app.add_exception_handler(RequestValidationError, validation_error_handler)  # type: ignore[arg-type]
        for router in (hotspots_router, restaurants_router, foods_router):
            app.include_router(router)
        app.dependency_overrides[get_session] = database
        app.dependency_overrides[current_user] = member
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield Harness(client, factory, ids)
    finally:
        await redis.aclose()
        await engine.dispose()


def expected_place_id(h: Harness, kind: str) -> str:
    """The Google place id the row should point at after selecting ``kind``."""
    key = {"hotspot": "hotspot_place_id", "restaurant": "place_id"}.get(kind, "merchant_place_id")
    return str(h.ids[key])


@pytest.mark.parametrize("kind", KINDS)
async def test_append_is_the_default_and_leaves_the_meal_cards_alone(
    harness: Harness, kind: str
) -> None:
    before = await harness.day_rows()

    response = await harness.select(kind)

    assert response.status_code == 200, response.text
    assert response.json()["version"] == 2
    rows = await harness.day_rows()
    assert len(rows) == len(before) + 1
    added = next(row for row in rows if row.system_role is None)
    assert added.position == max(row.position for row in before) + 1
    assert added.provider_place_id == expected_place_id(harness, kind)
    assert "meal_selection_source" not in added.data
    for role in ("lunch", "dinner"):
        assert placeholder(meal_card(rows, role)), role
    if kind == "hotspot":
        # The hotspot stop is exactly what the endpoint always appended.
        assert (added.item_type, added.duration_minutes) == ("activity", 75)
        assert added.title == added.location_name == "淺草寺"
        assert added.data["selection_source"] == "hotspot_card"
        assert set(added.data) >= {"hotspot_id", "hotspot_slug", "map_links", "opening_hours"}
    else:
        assert (added.item_type, added.duration_minutes) == ("custom", 60)
    if kind in {"food", "merchant"}:
        assert added.data["merchant_id"] == str(harness.ids["merchant"])
        assert added.data["food_id"] == (str(harness.ids["food"]) if kind == "food" else None)


@pytest.mark.parametrize("meal", ["lunch", "dinner"])
@pytest.mark.parametrize("kind", KINDS)
async def test_replace_meal_fills_that_card_and_keeps_its_time(
    harness: Harness, kind: str, meal: str
) -> None:
    before = await harness.day_rows()
    card_before = meal_card(before, meal)
    other = "dinner" if meal == "lunch" else "lunch"

    response = await harness.select(kind, mode="replace_meal", meal=meal)

    assert response.status_code == 200, response.text
    rows = await harness.day_rows()
    assert len(rows) == len(before), "a meal replacement adds no row"
    card = meal_card(rows, meal)
    assert card.id == card_before.id
    assert card.provider_place_id == expected_place_id(harness, kind)
    assert not placeholder(card)
    assert card.data["meal_selection_source"] == "user"
    assert card.data["meal_kind"] == meal
    assert card.data["needs_place_confirmation"] is False
    assert card.is_skipped is False
    # The card keeps its role and slot in the day; only the place changed.
    kept = ("system_role", "position", "start_time", "end_time", "duration_minutes", "item_type")
    assert [getattr(card, name) for name in kept] == [getattr(card_before, name) for name in kept]
    assert (card.locked, card.fixed_time) == (card_before.locked, card_before.fixed_time)
    assert placeholder(meal_card(rows, other))
    served = next(item for item in response.json()["items"] if item.get("system_role") == meal)
    assert served["data"]["meal_selection_source"] == "user"
    if kind == "hotspot":
        assert card.title == "淺草寺"
        assert card.data["hotspot_id"] == str(harness.ids["hotspot"])
    if kind == "merchant":
        assert card.title == "Ichiran Shibuya"
    if kind == "food":
        assert card.title == "ラーメン · Ichiran Shibuya"


@pytest.mark.parametrize("kind", KINDS)
async def test_replace_meal_without_a_meal_is_rejected(harness: Harness, kind: str) -> None:
    before = await harness.day_rows()

    missing = await harness.select(kind, mode="replace_meal")
    assert missing.status_code == 422, missing.text
    assert "meal" in missing.text
    # A meal with no replace_meal would silently append: the bug this contract closes.
    stray = await harness.select(kind, meal="lunch")
    assert stray.status_code == 422, stray.text
    appended = await harness.select(kind, mode="append", meal_role="lunch")
    assert appended.status_code == 422, appended.text
    disagreeing = await harness.select(kind, meal="lunch", meal_role="dinner")
    assert disagreeing.status_code == 422, disagreeing.text
    unknown = await harness.select(kind, mode="replace_meal", meal="breakfast")
    assert unknown.status_code == 422, unknown.text

    assert [row.id for row in await harness.day_rows()] == [row.id for row in before]
    assert placeholder(meal_card(await harness.day_rows(), "lunch"))


@pytest.mark.parametrize("kind", KINDS)
async def test_legacy_meal_role_still_fills_the_card(harness: Harness, kind: str) -> None:
    """The first clients sent only ``meal_role``; it still means replace that meal."""

    response = await harness.select(kind, meal_role="dinner")

    assert response.status_code == 200, response.text
    rows = await harness.day_rows()
    card = meal_card(rows, "dinner")
    assert card.provider_place_id == expected_place_id(harness, kind)
    assert card.data["meal_selection_source"] == "user"
    assert sum(row.system_role is None for row in rows) == 0


@pytest.mark.parametrize("kind", KINDS)
async def test_occupied_meal_slot_answers_409_until_the_request_overwrites(
    harness: Harness, kind: str
) -> None:
    first = await harness.select("hotspot", mode="replace_meal", meal="lunch")
    assert first.status_code == 200, first.text
    chosen = meal_card(await harness.day_rows(), "lunch")

    refused = await harness.select(kind, mode="replace_meal", meal="lunch")

    assert refused.status_code == 409, refused.text
    assert refused.json()["code"] == "meal_slot_occupied"
    card = meal_card(await harness.day_rows(), "lunch")
    assert (card.title, card.provider_place_id) == (chosen.title, chosen.provider_place_id)

    replaced = await harness.select(kind, mode="replace_meal", meal="lunch", overwrite=True)

    assert replaced.status_code == 200, replaced.text
    card = meal_card(await harness.day_rows(), "lunch")
    assert card.provider_place_id == expected_place_id(harness, kind)
    assert card.data["meal_selection_source"] == "user"
    if kind != "hotspot":
        # The previous place's identity does not linger under the new one.
        assert not {"hotspot_id", "hotspot_slug", "opening_hours"} & set(card.data)
    # The dinner card was never touched, and appending never asks.
    assert placeholder(meal_card(await harness.day_rows(), "dinner"))
    assert (await harness.select(kind)).status_code == 200


async def test_planner_suggestions_and_placeholders_are_replaced_without_asking(
    harness: Harness,
) -> None:
    async with harness.factory() as session:
        rows = await trips.load_items(session, harness.ids["trip"])
        card = meal_card([row for row in rows if row.day_date == DAY], "lunch")
        card.title = "Planner pick"
        card.location_name = "Somewhere"
        card.data = {**card.data, "meal_selection_source": "ai", "reason": "close by"}
        await session.commit()

    response = await harness.select("merchant", mode="replace_meal", meal="lunch")

    assert response.status_code == 200, response.text
    card = meal_card(await harness.day_rows(), "lunch")
    assert card.title == "Ichiran Shibuya"
    assert card.data["meal_selection_source"] == "user"


async def test_wrong_day_and_stale_version_keep_their_own_answers(harness: Harness) -> None:
    outside = await harness.client.post(
        harness.path("hotspot"),
        json={**harness.body("hotspot"), "day_date": "2027-03-20", "mode": "replace_meal", "meal": "lunch"},
    )
    assert outside.status_code == 422
    assert outside.json()["code"] == "itinerary_date_out_of_range"

    stale = await harness.client.post(
        harness.path("merchant"), json={**harness.body("merchant"), "version": 7}
    )
    assert stale.status_code == 409
    assert stale.json()["code"] == "trip_version_conflict"
    assert all(row.system_role is not None for row in await harness.day_rows())


async def test_unknown_places_are_still_404(harness: Harness) -> None:
    missing: UUID = uuid4()
    for path in (
        f"/hotspots/{missing}/trip-selections",
        "/restaurants/no-such-place/trip-selections",
        f"/foods/{missing}/trip-selections",
        f"/foods/merchants/{missing}/trip-selections",
    ):
        response = await harness.client.post(path, json=harness.body("food"))
        assert response.status_code == 404, path


def test_meal_slot_occupied_has_five_locale_copy() -> None:
    from app.i18n import ERROR_DETAILS, LOCALES

    assert all(ERROR_DETAILS[locale].get("meal_slot_occupied") for locale in LOCALES)
    assert len({ERROR_DETAILS[locale]["meal_slot_occupied"] for locale in LOCALES}) == len(LOCALES)
