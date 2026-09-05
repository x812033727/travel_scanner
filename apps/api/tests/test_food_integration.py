import os
from collections.abc import AsyncIterator
from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
import pytest_asyncio
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.listing import COUNTRY_RANK
from app.db import SessionFactory, engine
from app.foods.admin_router import (
    FoodAreaWritePayload,
    FoodBatchPayload,
    FoodMerchantUpdatePayload,
    batch_foods,
    create_food_area,
    list_admin_foods,
    update_food_merchant,
)
from app.foods.catalog import COUNTRY_NAMES
from app.foods.service import (
    food_facets,
    list_foods,
    list_merchants,
    merchant_categories,
    merchant_cities,
    seed_food_catalog,
)
from app.hotspots.service import seed_catalog
from app.models import (
    AdminAuditLog,
    FoodArea,
    FoodCategory,
    FoodDestination,
    FoodHotspot,
    FoodLocalization,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantFood,
    FoodMerchantSource,
    TravelFood,
    TravelHotspot,
    User,
)
from app.problems import AppError
from app.restaurants.admin_sources_router import restaurant_editorial_coverage

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


async def _clear(session: AsyncSession) -> None:
    await session.execute(delete(FoodMerchantSource))
    await session.execute(delete(FoodMerchantFood))
    await session.execute(delete(FoodMerchantCategory))
    await session.execute(delete(FoodMerchant))
    await session.execute(delete(FoodArea))
    await session.execute(delete(FoodCategory))
    await session.execute(delete(FoodHotspot))
    await session.execute(delete(FoodDestination))
    await session.execute(delete(FoodLocalization))
    await session.execute(delete(TravelFood))
    await session.execute(delete(TravelHotspot))
    await session.commit()


@pytest.mark.asyncio(loop_scope="module")
async def test_food_seed_public_filters_maps_and_admin_state_are_idempotent() -> None:
    async with SessionFactory() as session:
        await _clear(session)
        await seed_catalog(session, date(2026, 9, 1))
        assert await seed_food_catalog(session) == 80
        await session.commit()

    async with SessionFactory() as session:
        assert int(await session.scalar(select(func.count(TravelFood.id))) or 0) == 80
        assert int(await session.scalar(select(func.count(FoodLocalization.id))) or 0) == 400
        assert int(await session.scalar(select(func.count(FoodDestination.id))) or 0) >= 70
        assert int(await session.scalar(select(func.count(FoodHotspot.id))) or 0) >= 70
        assert int(await session.scalar(select(func.count(FoodMerchant.id))) or 0) == 173
        # One row per merchant-dish. Higher than the 185 distinct (city, dish) pairs the
        # catalog validator counts, because a city can have several places for one dish.
        assert int(await session.scalar(select(func.count(FoodMerchantFood.id))) or 0) == 192
        assert int(await session.scalar(select(func.count(FoodMerchantSource.id))) or 0) == 236
        assert int(await session.scalar(select(func.count(FoodArea.id))) or 0) == 132
        assert int(await session.scalar(select(func.count(FoodCategory.id))) or 0) == 18
        assert int(await session.scalar(select(func.count(FoodMerchantCategory.id))) or 0) == 271
        assert (
            int(
                await session.scalar(
                    select(func.count(FoodMerchant.id)).where(FoodMerchant.area_id.is_not(None))
                )
                or 0
            )
            == 80
        )
        assert (
            int(
                await session.scalar(
                    select(func.count(FoodMerchant.id)).where(FoodMerchant.area_source == "seed")
                )
                or 0
            )
            == 80
        )
        assert (
            int(
                await session.scalar(
                    select(func.count(func.distinct(FoodMerchantSource.merchant_id))).where(
                        FoodMerchantSource.source_scope.in_(
                            ("merchant_listing", "merchant_website")
                        )
                    )
                )
                or 0
            )
            == 63
        )
        assert (
            int(
                await session.scalar(
                    select(func.count(FoodMerchant.id)).where(
                        FoodMerchant.official_website_url.is_not(None)
                    )
                )
                or 0
            )
            == 28
        )
        coverage = await restaurant_editorial_coverage(
            User(email="coverage@example.test", password_hash="not-used", is_admin=True),
            session,
            limit=200,
        )
        food_merchant_coverage = coverage["food_merchants"]
        assert food_merchant_coverage["direct_merchant_evidence"] == 63
        assert food_merchant_coverage["official_website"] == 28
        by_country = {
            country["country_code"]: country for country in food_merchant_coverage["by_country"]
        }
        # Japan was zero until Okinawa, Yokohama and Kamakura brought first-party pages.
        assert by_country["JP"]["direct_merchant_evidence"] == 16
        assert by_country["TW"]["direct_merchant_evidence"] == 14
        assert by_country["SG"]["official_website"] == 6

        korean_food = await session.scalar(
            select(TravelFood).where(TravelFood.country_code == "KR").limit(1)
        )
        assert korean_food is not None
        latitude, longitude = Decimal("37.570100"), Decimal("126.999600")
        merchant = FoodMerchant(
            slug="integration-verified-korean-merchant",
            destination_id="seoul",
            country_code="KR",
            name="Verified Korean Merchant",
            local_name="검증 식당",
            latitude=latitude,
            longitude=longitude,
            coordinate_source_type="official_tourism",
            coordinate_source_url="https://english.visitseoul.net/restaurants",
            coordinate_verified_at=datetime.now(UTC),
            naver_map_url="https://map.naver.com/p/entry/place/13543735",
            map_match_status="verified",
            review_status="approved",
            is_active=True,
            verified_at=datetime.now(UTC),
        )
        myeongdong = await session.scalar(
            select(FoodArea).where(FoodArea.slug == "seoul-myeongdong")
        )
        home_style = await session.scalar(
            select(FoodCategory).where(FoodCategory.slug == "home-style")
        )
        assert myeongdong is not None and home_style is not None
        merchant.area_id = myeongdong.id
        merchant.area_source = "admin"
        session.add(merchant)
        await session.flush()
        session.add(
            FoodMerchantCategory(
                merchant_id=merchant.id,
                category_id=home_style.id,
                is_primary=True,
                display_order=1,
                source="admin",
            )
        )
        session.add(
            FoodMerchantFood(
                merchant_id=merchant.id,
                food_id=korean_food.id,
                is_primary=True,
                display_order=1,
            )
        )
        session.add(
            FoodMerchantSource(
                merchant_id=merchant.id,
                source_type="official_tourism",
                source_title="Official test source",
                source_url="https://english.visitseoul.net/restaurants",
                is_current=True,
                last_verified_at=datetime.now(UTC),
            )
        )
        await session.commit()

        korean = await list_foods(
            session, locale="ko", country_code="KR", destination_id="seoul", limit=20
        )
        assert korean["total"] == 10
        assert all(item["name"] for item in korean["items"])
        assert all(item["food_hotspots"] for item in korean["items"])
        published_merchants = [
            merchant for item in korean["items"] for merchant in item["recommended_merchants"]
        ]
        assert len(published_merchants) == 1
        assert published_merchants[0]["map_links"][0]["provider"] == "naver"
        assert "plus_code_global" not in published_merchants[0]
        facets = await food_facets(session)
        assert facets["total"] == 80
        assert len(facets["countries"]) == 7
        assert published_merchants[0]["area"]["slug"] == "seoul-myeongdong"
        assert published_merchants[0]["categories"][0]["slug"] == "home-style"

        directory = await list_merchants(session, locale="ko", destination_id="seoul")
        assert directory["total"] == 1 and directory["has_more"] is False
        card = directory["items"][0]
        assert card["area"]["slug"] == "seoul-myeongdong"
        assert card["area"]["name"] == "명동"
        assert card["categories"] == [
            {"slug": "home-style", "name": "정식·백반", "is_primary": True}
        ]
        assert card["signature_dishes"] and card["signature_dishes"][0]["food_id"] == str(
            korean_food.id
        )
        assert card["map_links"][0]["provider"] == "naver"
        assert card["destination_name"] == "首爾"
        facet_areas = {
            area["slug"]: area["merchant_count"] for area in directory["facets"]["areas"]
        }
        assert facet_areas["seoul-myeongdong"] == 1 and facet_areas["seoul-hongdae"] == 0
        assert directory["facets"]["unassigned_area_count"] == 0
        facet_categories = {
            item["slug"]: item["merchant_count"] for item in directory["facets"]["categories"]
        }
        assert facet_categories["home-style"] == 1 and facet_categories["ramen"] == 0
        assert (
            await list_merchants(
                session, locale="zh-TW", destination_id="seoul", area_slug="seoul-myeongdong"
            )
        )["total"] == 1
        assert (
            await list_merchants(session, locale="zh-TW", destination_id="seoul", area_slug="other")
        )["total"] == 0
        assert (
            await list_merchants(
                session, locale="zh-TW", destination_id="seoul", category_slug="street-food"
            )
        )["total"] == 0
        assert (await list_merchants(session, locale="zh-TW", q="검증"))["total"] == 1
        assert (await list_merchants(session, locale="zh-TW", destination_id="tokyo"))["total"] == 0
        with pytest.raises(AppError) as unknown_area:
            await list_merchants(session, locale="zh-TW", area_slug="seoul-nowhere")
        assert unknown_area.value.code == "food_area_not_found"
        cities = await merchant_cities(session, locale="zh-TW")
        assert cities["total_merchants"] == 1
        by_city = {
            city["id"]: city for country in cities["countries"] for city in country["cities"]
        }
        assert len(by_city) == 33
        assert by_city["seoul"]["merchant_count"] == 1 and by_city["seoul"]["area_count"] == 4
        assert by_city["yokohama"]["area_count"] == 4
        assert by_city["kamakura"]["area_count"] == 4
        assert by_city["okinawa"]["merchant_count"] == 0
        assert by_city["tainan"]["parent_destination_id"] == "kaohsiung"
        assert cities["countries"][0]["code"] == "KR"
        seoul_categories = await merchant_categories(session, locale="en", destination_id="seoul")
        assert {item["slug"]: item["merchant_count"] for item in seoul_categories["items"]}[
            "home-style"
        ] == 1

        admin_listing = await list_admin_foods(
            User(email="food-listing@example.test", password_hash="not-used", is_admin=True),
            session,
            locale="ja",
            food_kind="dessert",
            limit=100,
        )
        assert admin_listing["total"] == len(admin_listing["items"]) > 0
        assert all(item["food_kind"] == "dessert" for item in admin_listing["items"])
        assert all(
            item["country_name"] == COUNTRY_NAMES[item["country_code"]]["ja"]
            for item in admin_listing["items"]
        )
        ranks = [COUNTRY_RANK[item["country_code"]] for item in admin_listing["items"]]
        assert ranks == sorted(ranks)
        # The kind facet ignores the kind filter; the country facet honours it.
        assert sum(kind["count"] for kind in admin_listing["facets"]["food_kinds"]) == 80
        assert (
            sum(country["count"] for country in admin_listing["facets"]["countries"])
            == admin_listing["total"]
        )

        seeded_merchant = await session.scalar(
            select(FoodMerchant).where(FoodMerchant.slug == "taipei-din-tai-fung")
        )
        assert seeded_merchant is not None
        seeded_merchant.official_website_url = "https://example.test/admin-verified"
        ximending = await session.scalar(
            select(FoodArea).where(FoodArea.slug == "taipei-ximending")
        )
        assert ximending is not None
        seeded_merchant.area_id = ximending.id
        seeded_merchant.area_source = "admin"
        await session.execute(
            delete(FoodMerchantCategory).where(
                FoodMerchantCategory.merchant_id == seeded_merchant.id
            )
        )
        session.add(
            FoodMerchantCategory(
                merchant_id=seeded_merchant.id,
                category_id=home_style.id,
                is_primary=True,
                display_order=1,
                source="admin",
            )
        )
        cleared_merchant = await session.scalar(
            select(FoodMerchant).where(FoodMerchant.slug == "seoul-lees-gimbap")
        )
        assert cleared_merchant is not None and cleared_merchant.area_id is not None
        cleared_merchant.area_id = None
        cleared_merchant.area_source = "admin"
        backfilled_merchant = await session.scalar(
            select(FoodMerchant).where(FoodMerchant.slug == "tokyo-ichiran-shibuya")
        )
        assert backfilled_merchant is not None
        await session.execute(
            delete(FoodMerchantCategory).where(
                FoodMerchantCategory.merchant_id == backfilled_merchant.id
            )
        )
        disabled_area = await session.scalar(select(FoodArea).where(FoodArea.slug == "tokyo-umeda"))
        renamed_category = await session.scalar(
            select(FoodCategory).where(FoodCategory.slug == "ramen")
        )
        assert disabled_area is None  # umeda belongs to osaka-kyoto
        disabled_area = await session.scalar(
            select(FoodArea).where(FoodArea.slug == "osaka-kyoto-umeda")
        )
        assert disabled_area is not None and renamed_category is not None
        disabled_area.is_active = False
        renamed_category.names_json = {**renamed_category.names_json, "zh-TW": "拉麵專門店"}

        disabled = await session.scalar(select(TravelFood).order_by(TravelFood.slug).limit(1))
        assert disabled is not None
        disabled.review_status = "disabled"
        disabled.is_active = False
        await session.commit()

    async with SessionFactory() as session:
        assert await seed_food_catalog(session) == 80
        await session.commit()
        disabled = await session.scalar(select(TravelFood).order_by(TravelFood.slug).limit(1))
        assert disabled is not None
        assert disabled.review_status == "disabled"
        assert disabled.is_active is False
        assert int(await session.scalar(select(func.count(TravelFood.id))) or 0) == 80
        seeded_merchant = await session.scalar(
            select(FoodMerchant).where(FoodMerchant.slug == "taipei-din-tai-fung")
        )
        assert seeded_merchant is not None
        assert seeded_merchant.official_website_url == "https://example.test/admin-verified"
        ximending = await session.scalar(
            select(FoodArea).where(FoodArea.slug == "taipei-ximending")
        )
        assert ximending is not None and seeded_merchant.area_id == ximending.id
        seeded_links = list(
            (
                await session.scalars(
                    select(FoodMerchantCategory).where(
                        FoodMerchantCategory.merchant_id == seeded_merchant.id
                    )
                )
            ).all()
        )
        assert [link.source for link in seeded_links] == ["admin"]
        cleared_merchant = await session.scalar(
            select(FoodMerchant).where(FoodMerchant.slug == "seoul-lees-gimbap")
        )
        assert cleared_merchant is not None and cleared_merchant.area_id is None
        backfilled_merchant = await session.scalar(
            select(FoodMerchant).where(FoodMerchant.slug == "tokyo-ichiran-shibuya")
        )
        assert backfilled_merchant is not None
        assert (
            int(
                await session.scalar(
                    select(func.count(FoodMerchantCategory.id)).where(
                        FoodMerchantCategory.merchant_id == backfilled_merchant.id
                    )
                )
                or 0
            )
            == 1
        )
        # 271 seeded links plus the one on the verified fixture merchant.
        assert int(await session.scalar(select(func.count(FoodMerchantCategory.id))) or 0) == 272
        disabled_area = await session.scalar(
            select(FoodArea).where(FoodArea.slug == "osaka-kyoto-umeda")
        )
        assert disabled_area is not None and disabled_area.is_active is False
        renamed_category = await session.scalar(
            select(FoodCategory).where(FoodCategory.slug == "ramen")
        )
        assert renamed_category is not None and renamed_category.names_json["zh-TW"] == "拉麵專門店"
        assert int(await session.scalar(select(func.count(FoodArea.id))) or 0) == 132
        assert int(await session.scalar(select(func.count(FoodCategory.id))) or 0) == 18

        admin = User(
            email="food-admin-integration@example.test",
            password_hash="not-used",
            is_admin=True,
        )
        session.add(admin)
        await session.flush()
        admin_id = admin.id
        candidate = await session.scalar(
            select(TravelFood).where(TravelFood.review_status == "approved").limit(1)
        )
        assert candidate is not None
        result = await batch_foods(
            FoodBatchPayload(ids=[candidate.id], action="disable"), admin, session
        )
        assert result == {"updated": 1, "status": "disabled"}
        await session.refresh(candidate)
        assert candidate.review_status == "disabled"
        assert candidate.is_active is False
        audit = await session.scalar(
            select(AdminAuditLog).where(
                AdminAuditLog.actor_user_id == admin.id,
                AdminAuditLog.action == "foods_batch_updated",
            )
        )
        assert audit is not None

        created_area = await create_food_area(
            FoodAreaWritePayload(
                slug="seoul-euljiro",
                destination_id="seoul",
                names={
                    "zh-TW": "乙支路",
                    "zh-CN": "乙支路",
                    "en": "Euljiro",
                    "ja": "乙支路",
                    "ko": "을지로",
                },
                latitude=37.566,
                longitude=126.991,
            ),
            admin,
            session,
        )
        assert created_area["country_code"] == "KR" and created_area["source"] == "admin"
        verified = await session.scalar(
            select(FoodMerchant).where(
                FoodMerchant.slug == "integration-verified-korean-merchant"
            )
        )
        assert verified is not None
        with pytest.raises(AppError) as mismatch:
            await update_food_merchant(
                verified.id,
                FoodMerchantUpdatePayload(area_slug="taipei-ximending"),
                admin,
                session,
            )
        assert mismatch.value.code == "merchant_area_destination_mismatch"
        await session.rollback()
        admin = await session.get(User, admin_id)
        assert admin is not None
        verified = await session.scalar(
            select(FoodMerchant).where(
                FoodMerchant.slug == "integration-verified-korean-merchant"
            )
        )
        assert verified is not None
        linked_food_ids = list(
            (
                await session.scalars(
                    select(FoodMerchantFood.food_id).where(
                        FoodMerchantFood.merchant_id == verified.id
                    )
                )
            ).all()
        )
        updated = await update_food_merchant(
            verified.id,
            FoodMerchantUpdatePayload(
                area_slug="seoul-euljiro",
                category_slugs=["home-style", "rice-dishes"],
                food_ids=linked_food_ids,
            ),
            admin,
            session,
        )
        assert updated["area"]["slug"] == "seoul-euljiro"
        assert updated["area_source"] == "admin"
        assert [item["slug"] for item in updated["categories"]] == ["home-style", "rice-dishes"]
        assert [item["is_primary"] for item in updated["categories"]] == [True, False]
        with pytest.raises(AppError) as no_category:
            await update_food_merchant(
                verified.id,
                FoodMerchantUpdatePayload(category_slugs=[]),
                admin,
                session,
            )
        assert no_category.value.code == "merchant_category_required"
        await session.rollback()
        admin = await session.get(User, admin_id)
        assert admin is not None

        await session.execute(delete(AdminAuditLog).where(AdminAuditLog.actor_user_id == admin.id))
        admin = await session.get(User, admin_id)
        assert admin is not None
        await session.delete(admin)
        await session.commit()
        await _clear(session)


@pytest.mark.asyncio(loop_scope="module")
async def test_reseeding_extends_an_existing_dish_to_a_newly_listed_city(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The only way a city joins the catalog is by appearing in a dish's destination_ids.

    The seeder used to write destination links only for a dish that had none, so adding a
    city to an existing dish and re-running seed-foods reported success and changed nothing.
    """

    from dataclasses import replace

    from app.foods import service as food_service
    from app.foods.catalog import FOOD_SEEDS

    async with SessionFactory() as session:
        await _clear(session)
        await seed_catalog(session, date(2026, 9, 1))
        await seed_food_catalog(session)
        await session.commit()

    # A pair the seeds do not carry, checked rather than assumed: this test broke once
    # already when a later change gave jp-ramen the city it was using.
    original = next(item for item in FOOD_SEEDS if item.slug == "jp-sushi")
    assert "kamakura" not in original.destination_ids
    extended = replace(original, destination_ids=(*original.destination_ids, "kamakura"))
    patched = tuple(extended if item.slug == "jp-sushi" else item for item in FOOD_SEEDS)

    async with SessionFactory() as session:
        food_id = await session.scalar(select(TravelFood.id).where(TravelFood.slug == "jp-sushi"))
        before = set(
            (
                await session.scalars(
                    select(FoodDestination.destination_id).where(
                        FoodDestination.food_id == food_id
                    )
                )
            ).all()
        )
        assert "kamakura" not in before

        monkeypatch.setattr(food_service, "FOOD_SEEDS", patched)
        await seed_food_catalog(session)
        await session.commit()
        monkeypatch.undo()

    async with SessionFactory() as session:
        after = list(
            (
                await session.scalars(
                    select(FoodDestination.destination_id).where(
                        FoodDestination.food_id == food_id
                    )
                )
            ).all()
        )
        assert "kamakura" in after
        # The cities it already served are untouched, and none is duplicated.
        assert before <= set(after)
        assert len(after) == len(set(after)) == len(before) + 1

    async with SessionFactory() as session:
        await _clear(session)
        await session.commit()


@pytest.mark.asyncio(loop_scope="module")
async def test_filling_coordinates_survives_a_real_session_across_many_rows() -> None:
    """The session handling here only breaks against a real session.

    Releasing the read transaction with rollback() expires every loaded merchant whatever
    expire_on_commit says, so the next plain ``merchant.slug`` needed a refresh SELECT from
    sync attribute access and the command died with MissingGreenlet on the first row. The
    unit tests could not see it: they drive the loop with hand-built objects.
    """

    from app.foods.coordinate_fill import FetchResult
    from app.foods.coordinate_fill_cli import fill_food_merchant_coordinates

    page = (
        '<script type="application/ld+json">'
        '{"@type":"Restaurant","geo":{"latitude":35.3192,"longitude":139.5467}}</script>'
    )

    async def fetch(_url: str) -> FetchResult:
        return FetchResult(page, "ok")

    async with SessionFactory() as session:
        await _clear(session)
        await seed_catalog(session, date(2026, 9, 1))
        await seed_food_catalog(session)
        await session.commit()

    # Kamakura, because its merchants are the ones that carry first-party pages; the
    # older Japanese cities still have only their destination guide.
    report = await fill_food_merchant_coordinates(["kamakura"], None, True, fetch)

    assert report["applied"] is True
    assert report["processed"] >= 2, report
    # One page serves every row here, so the first row is filled and the rest report
    # duplicate. Anything else means the loop died partway.
    assert set(report["outcomes"]) <= {"filled", "duplicate"}
    assert report["outcomes"].get("filled") == 1

    async with SessionFactory() as session:
        written = list(
            (
                await session.scalars(
                    select(FoodMerchant).where(
                        FoodMerchant.destination_id == "kamakura",
                        FoodMerchant.latitude.is_not(None),
                    )
                )
            ).all()
        )
        assert written, report
        first = written[0]
        assert first.coordinate_source_type in {"merchant_official", "official_tourism"}
        assert first.coordinate_verified_at is not None
        # Still nobody's review state moved.
        assert first.review_status == "pending"
        assert first.map_match_status == "unverified"
        assert first.is_active is False

    async with SessionFactory() as session:
        await _clear(session)
        await session.commit()

