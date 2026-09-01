from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field, model_validator
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AdminUser
from app.db import get_session
from app.destinations.catalog import destination_for_id
from app.i18n import LOCALES, Locale
from app.models import (
    AdminAuditLog,
    FoodDestination,
    FoodHotspot,
    FoodLocalization,
    TravelFood,
    TravelHotspot,
)
from app.problems import AppError

router = APIRouter(prefix="/admin/foods", tags=["admin foods"])
Session = Annotated[AsyncSession, Depends(get_session)]
FoodKind = Literal["main", "noodle_soup", "street_food", "dessert", "drink"]
ReviewStatus = Literal["pending", "approved", "rejected", "disabled"]


class FoodLocalizationPayload(BaseModel):
    locale: Locale
    name: str = Field(min_length=1, max_length=255)
    summary: str = Field(min_length=1, max_length=2000)


class FoodWritePayload(BaseModel):
    slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=128)
    country_code: str = Field(min_length=2, max_length=2)
    local_name: str = Field(min_length=1, max_length=255)
    romanized_name: str = Field(min_length=1, max_length=255)
    food_kind: FoodKind
    meal_types: list[str] = Field(min_length=1, max_length=5)
    ingredient_tags: list[str] = Field(default_factory=list, max_length=20)
    dietary_notes: list[str] = Field(default_factory=list, max_length=20)
    source_urls: list[str] = Field(min_length=1, max_length=10)
    review_status: ReviewStatus = "pending"
    is_active: bool = True
    display_order: int = Field(default=100, ge=0, le=10_000)
    localizations: list[FoodLocalizationPayload] = Field(min_length=5, max_length=5)
    destination_ids: list[str] = Field(min_length=1, max_length=31)
    hotspot_ids: list[UUID] = Field(default_factory=list, max_length=50)

    @model_validator(mode="after")
    def validate_locales(self) -> FoodWritePayload:
        locales = [item.locale for item in self.localizations]
        if set(locales) != set(LOCALES) or len(locales) != len(set(locales)):
            raise ValueError("美食內容必須包含且僅包含五種網站語系")
        return self


class FoodUpdatePayload(BaseModel):
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    local_name: str | None = Field(default=None, min_length=1, max_length=255)
    romanized_name: str | None = Field(default=None, min_length=1, max_length=255)
    food_kind: FoodKind | None = None
    meal_types: list[str] | None = Field(default=None, min_length=1, max_length=5)
    ingredient_tags: list[str] | None = Field(default=None, max_length=20)
    dietary_notes: list[str] | None = Field(default=None, max_length=20)
    source_urls: list[str] | None = Field(default=None, min_length=1, max_length=10)
    review_status: ReviewStatus | None = None
    is_active: bool | None = None
    display_order: int | None = Field(default=None, ge=0, le=10_000)
    localizations: list[FoodLocalizationPayload] | None = Field(default=None, max_length=5)
    destination_ids: list[str] | None = Field(default=None, min_length=1, max_length=31)
    hotspot_ids: list[UUID] | None = Field(default=None, max_length=50)


class FoodBatchPayload(BaseModel):
    ids: list[UUID] = Field(min_length=1, max_length=100)
    action: Literal["approve", "reject", "disable", "activate"]
    reason: str | None = Field(default=None, max_length=500)


async def _validate_relations(
    session: AsyncSession, destination_ids: list[str], hotspot_ids: list[UUID]
) -> None:
    if any(destination_for_id(item) is None for item in destination_ids):
        raise AppError(422, "unsupported_destination", "目的地關聯包含不支援的項目")
    if not hotspot_ids:
        return
    rows = list(
        (
            await session.scalars(select(TravelHotspot).where(TravelHotspot.id.in_(hotspot_ids)))
        ).all()
    )
    if len(rows) != len(set(hotspot_ids)):
        raise AppError(404, "food_hotspot_not_found", "部分美食景點不存在")
    if any(
        row.category != "food"
        or row.review_status not in ("approved", "auto_approved")
        or not row.is_active
        for row in rows
    ):
        raise AppError(422, "invalid_food_hotspot", "只能關聯已核准且啟用的美食景點")


async def _replace_relations(
    session: AsyncSession,
    food: TravelFood,
    destination_ids: list[str] | None,
    hotspot_ids: list[UUID] | None,
) -> None:
    if destination_ids is not None:
        destination_relations = list(
            (
                await session.scalars(
                    select(FoodDestination).where(FoodDestination.food_id == food.id)
                )
            ).all()
        )
        for destination_relation in destination_relations:
            await session.delete(destination_relation)
        for order, destination_id in enumerate(destination_ids, start=1):
            session.add(
                FoodDestination(
                    food_id=food.id,
                    destination_id=destination_id.casefold(),
                    display_order=order,
                )
            )
    if hotspot_ids is not None:
        hotspot_relations = list(
            (await session.scalars(select(FoodHotspot).where(FoodHotspot.food_id == food.id))).all()
        )
        for hotspot_relation in hotspot_relations:
            await session.delete(hotspot_relation)
        for order, hotspot_id in enumerate(hotspot_ids, start=1):
            session.add(FoodHotspot(food_id=food.id, hotspot_id=hotspot_id, display_order=order))


async def _upsert_localizations(
    session: AsyncSession,
    food: TravelFood,
    values: list[FoodLocalizationPayload] | None,
) -> None:
    if values is None:
        return
    existing = {
        row.locale: row
        for row in (
            await session.scalars(
                select(FoodLocalization).where(FoodLocalization.food_id == food.id)
            )
        ).all()
    }
    for value in values:
        row = existing.get(value.locale)
        if row is None:
            row = FoodLocalization(food_id=food.id, locale=value.locale)
        row.name = value.name
        row.summary = value.summary
        session.add(row)


async def _admin_item(session: AsyncSession, food: TravelFood) -> dict[str, object]:
    localizations = list(
        (
            await session.scalars(
                select(FoodLocalization)
                .where(FoodLocalization.food_id == food.id)
                .order_by(FoodLocalization.locale)
            )
        ).all()
    )
    destinations = list(
        (
            await session.scalars(
                select(FoodDestination)
                .where(FoodDestination.food_id == food.id)
                .order_by(FoodDestination.display_order)
            )
        ).all()
    )
    hotspots = (
        await session.execute(
            select(FoodHotspot.hotspot_id, TravelHotspot.name)
            .join(TravelHotspot, TravelHotspot.id == FoodHotspot.hotspot_id)
            .where(FoodHotspot.food_id == food.id)
            .order_by(FoodHotspot.display_order)
        )
    ).all()
    return {
        "id": str(food.id),
        "slug": food.slug,
        "country_code": food.country_code,
        "local_name": food.local_name,
        "romanized_name": food.romanized_name,
        "food_kind": food.food_kind,
        "meal_types": food.meal_types,
        "ingredient_tags": food.ingredient_tags,
        "dietary_notes": food.dietary_notes,
        "source_urls": food.source_urls,
        "review_status": food.review_status,
        "is_active": food.is_active,
        "display_order": food.display_order,
        "localizations": [
            {"locale": row.locale, "name": row.name, "summary": row.summary}
            for row in localizations
        ],
        "destination_ids": [row.destination_id for row in destinations],
        "hotspots": [{"id": str(hotspot_id), "name": name} for hotspot_id, name in hotspots],
    }


@router.get("")
async def list_admin_foods(
    user: AdminUser,
    session: Session,
    country_code: Annotated[str | None, Query(min_length=2, max_length=2)] = None,
    destination_id: Annotated[str | None, Query(min_length=2, max_length=64)] = None,
    status: ReviewStatus | None = None,
    q: Annotated[str | None, Query(max_length=100)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 30,
) -> dict[str, object]:
    _ = user
    filters = []
    if country_code:
        filters.append(TravelFood.country_code == country_code.upper())
    if status:
        filters.append(TravelFood.review_status == status)
    if q:
        filters.append(TravelFood.search_text.ilike(f"%{q.strip()}%"))
    if destination_id:
        food_ids = select(FoodDestination.food_id).where(
            FoodDestination.destination_id == destination_id.casefold()
        )
        filters.append(TravelFood.id.in_(food_ids))
    total = int(await session.scalar(select(func.count(TravelFood.id)).where(*filters)) or 0)
    rows = list(
        (
            await session.scalars(
                select(TravelFood)
                .where(*filters)
                .order_by(TravelFood.display_order, TravelFood.slug)
                .offset((page - 1) * limit)
                .limit(limit)
            )
        ).all()
    )
    return {
        "items": [await _admin_item(session, food) for food in rows],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.post("", status_code=201)
async def create_food(
    payload: FoodWritePayload, user: AdminUser, session: Session
) -> dict[str, object]:
    if await session.scalar(select(TravelFood.id).where(TravelFood.slug == payload.slug)):
        raise AppError(409, "food_slug_exists", "美食 slug 已存在")
    await _validate_relations(session, payload.destination_ids, payload.hotspot_ids)
    food = TravelFood(
        slug=payload.slug,
        country_code=payload.country_code.upper(),
        local_name=payload.local_name,
        romanized_name=payload.romanized_name,
        food_kind=payload.food_kind,
        meal_types=payload.meal_types,
        ingredient_tags=payload.ingredient_tags,
        dietary_notes=payload.dietary_notes,
        search_text=" ".join(
            [payload.slug, payload.local_name, payload.romanized_name]
            + [item.name for item in payload.localizations]
        ),
        source_urls=payload.source_urls,
        review_status=payload.review_status,
        is_active=payload.is_active,
        display_order=payload.display_order,
    )
    session.add(food)
    await session.flush()
    await _upsert_localizations(session, food, payload.localizations)
    await _replace_relations(session, food, payload.destination_ids, payload.hotspot_ids)
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="food_created",
            target=f"food:{food.id}",
            metadata_json={"slug": food.slug},
        )
    )
    await session.commit()
    return await _admin_item(session, food)


@router.patch("/{food_id}")
async def update_food(
    food_id: UUID, payload: FoodUpdatePayload, user: AdminUser, session: Session
) -> dict[str, object]:
    food = await session.get(TravelFood, food_id)
    if food is None:
        raise AppError(404, "food_not_found", "找不到這筆美食資料")
    destinations = payload.destination_ids
    if destinations is None:
        destinations = list(
            (
                await session.scalars(
                    select(FoodDestination.destination_id).where(FoodDestination.food_id == food.id)
                )
            ).all()
        )
    await _validate_relations(session, destinations, payload.hotspot_ids or [])
    scalar_fields = (
        "country_code",
        "local_name",
        "romanized_name",
        "food_kind",
        "meal_types",
        "ingredient_tags",
        "dietary_notes",
        "source_urls",
        "review_status",
        "is_active",
        "display_order",
    )
    for field in scalar_fields:
        value = getattr(payload, field)
        if value is not None:
            setattr(food, field, value.upper() if field == "country_code" else value)
    await _upsert_localizations(session, food, payload.localizations)
    await _replace_relations(session, food, payload.destination_ids, payload.hotspot_ids)
    food.search_text = f"{food.slug} {food.local_name} {food.romanized_name}"
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="food_updated",
            target=f"food:{food.id}",
            metadata_json={"fields": sorted(payload.model_fields_set)},
        )
    )
    await session.commit()
    return await _admin_item(session, food)


@router.post("/batch")
async def batch_foods(
    payload: FoodBatchPayload, user: AdminUser, session: Session
) -> dict[str, int | str]:
    foods = list(
        (await session.scalars(select(TravelFood).where(TravelFood.id.in_(payload.ids)))).all()
    )
    if len(foods) != len(set(payload.ids)):
        raise AppError(404, "food_not_found", "部分美食資料不存在")
    statuses = {
        "approve": ("approved", True),
        "reject": ("rejected", False),
        "disable": ("disabled", False),
        "activate": ("approved", True),
    }
    status, active = statuses[payload.action]
    for food in foods:
        food.review_status = status
        food.is_active = active
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="foods_batch_updated",
            target=f"foods:{len(foods)}",
            metadata_json={
                "action": payload.action,
                "ids": [str(food.id) for food in foods],
                "reason": payload.reason,
                "at": datetime.now(UTC).isoformat(),
            },
        )
    )
    await session.commit()
    return {"updated": len(foods), "status": status}
