"""Authenticated saved-library endpoints, independent of community enrollment."""

from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.community import collections
from app.db import get_session
from app.i18n import Locale, current_locale
from app.saved import service

router = APIRouter()


async def private_session(
    response: Response,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AsyncSession:
    response.headers["Cache-Control"] = "private, no-store"
    return session


Session = Annotated[AsyncSession, Depends(private_session)]
RequestLocale = Annotated[Locale, Depends(current_locale)]
SavedFilter = Literal[
    "all",
    "hotspot",
    "food",
    "merchant",
    "restaurant",
    "service",
    "hotel",
    "guide",
    "article",
    "video",
    "post",
    "itinerary",
    "pet_place",
]


class StateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    keys: list[Annotated[str, Field(min_length=1, max_length=280)]] = Field(max_length=100)


class CollectionInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=80)


class ReferenceInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal[
        "hotspot",
        "food",
        "merchant",
        "restaurant",
        "service",
        "hotel",
        "guide",
        "article",
        "video",
        "post",
        "itinerary",
    ]
    id: str = Field(min_length=1, max_length=255)


@router.get("/all")
async def all_items(
    user: CurrentUser,
    session: Session,
    locale: RequestLocale,
    type: SavedFilter = "all",
    destination: Annotated[str, Query(max_length=64)] = "",
    collection: UUID | None = None,
    cursor: Annotated[str | None, Query(max_length=1024)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 24,
) -> dict[str, Any]:
    return await service.all_saved(
        session,
        user,
        locale,
        item_type=type,
        destination=destination,
        collection=collection,
        cursor=cursor,
        limit=limit,
    )


@router.post("/states")
async def saved_states(data: StateInput, user: CurrentUser, session: Session) -> dict[str, Any]:
    await collections.active_account(session, user)
    return await service.states(session, user, data.keys)


@router.get("/collections")
async def lists(user: CurrentUser, session: Session) -> dict[str, Any]:
    return await collections.list_collections(session, user)


@router.post("/collections")
async def create_list(
    data: CollectionInput,
    user: CurrentUser,
    session: Session,
    expected_user_id: UUID | None = None,
) -> dict[str, str]:
    await service.lock_account(session, user, expected_user_id)
    return await collections.create_collection(session, user, data.name)


@router.get("/collections/{identifier}")
async def list_items(
    identifier: UUID,
    user: CurrentUser,
    session: Session,
    locale: RequestLocale,
) -> dict[str, Any]:
    return await collections.collection_items(session, user, identifier, locale)


@router.delete("/collections/{identifier}")
async def delete_list(
    identifier: UUID,
    user: CurrentUser,
    session: Session,
    expected_user_id: UUID | None = None,
) -> dict[str, bool]:
    await service.lock_account(session, user, expected_user_id)
    return await collections.delete_collection(session, user, identifier)


@router.post("/collections/{identifier}/items")
async def add_to_list(
    identifier: UUID,
    data: ReferenceInput,
    user: CurrentUser,
    session: Session,
    locale: RequestLocale,
    expected_user_id: UUID | None = None,
) -> dict[str, Any]:
    await service.lock_account(session, user, expected_user_id)
    return await collections.collect_reference(
        session, user, identifier, data.kind, data.id, locale
    )


@router.delete("/collections/{identifier}/items/{item_id}")
async def remove_from_list(
    identifier: UUID,
    item_id: UUID,
    user: CurrentUser,
    session: Session,
    expected_user_id: UUID | None = None,
) -> dict[str, Any]:
    await service.lock_account(session, user, expected_user_id)
    return await collections.remove_reference(session, user, identifier, item_id)
