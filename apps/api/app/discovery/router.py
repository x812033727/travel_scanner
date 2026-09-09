from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser, OptionalCurrentUser
from app.config import get_settings
from app.db import get_session
from app.destinations.catalog import DESTINATIONS
from app.destinations.localized import city_name
from app.discovery.models import DiscoveryDismissal
from app.discovery.policy import destination_id, parse_key, require_enabled
from app.discovery.preferences import get_preferences, locked_user, update_preferences
from app.discovery.schemas import DismissInput, Kind, PreferenceInput
from app.discovery.service import page, resolve_discovery_items
from app.i18n import Locale, current_locale
from app.problems import AppError

router = APIRouter(prefix="/discovery", tags=["travel discovery"])


async def open_session(
    response: Response, session: Annotated[AsyncSession, Depends(get_session)]
) -> AsyncSession:
    response.headers["Cache-Control"] = "no-store"
    require_enabled(get_settings())
    return session


Session = Annotated[AsyncSession, Depends(open_session)]
TextQuery = Annotated[str, Query(max_length=160)]
DisplayLocale = Annotated[Locale, Depends(current_locale)]


@router.get("/status")
async def status(response: Response) -> dict[str, bool]:
    response.headers["Cache-Control"] = "no-store"
    return {"enabled": get_settings().discovery_enabled}


@router.get("/search")
async def search(
    session: Session,
    viewer: OptionalCurrentUser,
    display_locale: DisplayLocale,
    mode: Literal["recommended", "latest", "following"] = "latest",
    q: TextQuery = "",
    type: Kind | Literal["all"] = "all",
    destination: TextQuery = "",
    topic: TextQuery = "",
    locale: Locale | None = None,
    cursor: str | None = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
) -> dict[str, Any]:
    result = await page(
        session,
        viewer,
        display_locale,
        content_locale=locale,
        mode=mode,
        q=q.strip(),
        kinds=set() if type == "all" else {type},
        destinations=[destination_id(destination)] if destination else [],
        topics=[topic] if topic else [],
        cursor=cursor,
        limit=limit,
    )
    if cursor is None:
        from app.analytics.service import record_event

        recorded = await record_event(
            session,
            "discovery_search",
            path="/explore",
            user_id=viewer.id if viewer else None,
            properties={"kind": type, "result_count": len(result["items"])},
        )
        if not result["items"]:
            recorded = (
                await record_event(
                    session,
                    "discovery_empty",
                    path="/explore",
                    user_id=viewer.id if viewer else None,
                    properties={"kind": type},
                )
                or recorded
            )
        if recorded:
            await session.commit()
    return result


@router.get("/feed")
async def feed(
    session: Session,
    viewer: OptionalCurrentUser,
    display_locale: DisplayLocale,
    mode: Literal["recommended", "latest", "following"] = "recommended",
    q: TextQuery = "",
    type: Kind | Literal["all"] = "all",
    destination: TextQuery = "",
    topic: TextQuery = "",
    locale: Locale | None = None,
    cursor: str | None = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
) -> dict[str, Any]:
    return await page(
        session,
        viewer,
        display_locale,
        content_locale=locale,
        q=q.strip(),
        kinds=set() if type == "all" else {type},
        destinations=[destination_id(destination)] if destination else [],
        topics=[topic] if topic else [],
        mode=mode,
        cursor=cursor,
        limit=limit,
    )


@router.get("/suggestions")
async def suggestions(
    session: Session,
    viewer: OptionalCurrentUser,
    display_locale: DisplayLocale,
    q: TextQuery = "",
    locale: Locale | None = None,
) -> dict[str, Any]:
    from app.discovery.service import candidates

    query = q.strip()
    destinations = [
        {"id": item.id, "name": city_name(item, display_locale)}
        for item in DESTINATIONS
        if item.role != "extension"
    ]
    items: list[dict[str, str]] = []
    if query:
        for city in DESTINATIONS:
            if any(
                query.casefold() in name.casefold() for name in (city.id, city.city, *city.aliases)
            ):
                items.append(
                    {
                        "query": city_name(city, display_locale),
                        "label": city_name(city, display_locale),
                        "kind": "destination",
                        "destination": city.id,
                    }
                )
        if len(items) < 8:
            rows = await candidates(
                session,
                viewer,
                display_locale,
                content_locale=locale,
                q=query,
                kinds=set(),
                destinations=[],
                topics=[],
                mode="latest",
            )
            seen = {item["query"] for item in items}
            for row in rows:
                if row.title not in seen:
                    items.append({"query": row.title, "label": row.title, "kind": "content"})
                    seen.add(row.title)
                if len(items) >= 8:
                    break
    from app.discovery.taxonomy import topic_options

    return {
        "query": q,
        "items": items[:8],
        "destinations": destinations,
        "topics": await topic_options(session, display_locale),
    }


@router.get("/content/{kind}/{identifier}")
async def content(
    kind: Kind,
    identifier: UUID,
    session: Session,
    viewer: OptionalCurrentUser,
    locale: DisplayLocale,
) -> Any:
    key_kind = "guide" if kind in {"article", "video"} else "post" if kind == "itinerary" else kind
    items = await resolve_discovery_items(session, [f"{key_kind}:{identifier}"], viewer, locale)
    if not items or items[0].kind != kind:
        raise AppError(404, "community_not_found", "找不到這筆公開內容")
    return items[0]


@router.get("/preferences")
async def preferences(session: Session, user: CurrentUser) -> dict[str, Any]:
    return await get_preferences(session, user.id)


@router.put("/preferences")
async def save_preferences(
    data: PreferenceInput, session: Session, user: CurrentUser
) -> dict[str, Any]:
    result = await update_preferences(session, user.id, data)
    await session.commit()
    return result


@router.delete("/preferences")
async def reset_preferences(
    session: Session, user: CurrentUser, version: Annotated[int, Query(ge=0)]
) -> dict[str, Any]:
    # Keep a monotonic version after a reset: stale pre-reset writes must not win.
    result = await update_preferences(session, user.id, PreferenceInput(version=version))
    await session.execute(delete(DiscoveryDismissal).where(DiscoveryDismissal.user_id == user.id))
    await session.commit()
    return result


@router.post("/dismiss")
async def dismiss(
    data: DismissInput, session: Session, user: CurrentUser, locale: DisplayLocale
) -> dict[str, Any]:
    kind, identifier = parse_key(data.id)
    key = f"{kind}:{identifier}"
    await locked_user(session, user.id)
    existing = await session.get(DiscoveryDismissal, (user.id, key))
    if data.dismissed and not existing:
        if not await resolve_discovery_items(session, [key], user, locale):
            raise AppError(404, "community_not_found", "找不到這筆公開內容")
        count = await session.scalar(
            select(func.count())
            .select_from(DiscoveryDismissal)
            .where(DiscoveryDismissal.user_id == user.id)
        )
        if (count or 0) >= 500:
            raise AppError(422, "validation_error", "請先重設推薦偏好")
        session.add(DiscoveryDismissal(user_id=user.id, content_key=key))
    elif not data.dismissed and existing:
        await session.delete(existing)
    await session.commit()
    return {"id": key, "dismissed": data.dismissed}


class CollectionInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=80)


class CollectionReference(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["hotspot", "food", "merchant", "hotel", "guide", "post"]
    id: UUID


@router.get("/collections")
async def collections(session: Session, user: CurrentUser) -> Any:
    from app.community.collections import list_collections

    return await list_collections(session, user)


@router.post("/collections")
async def create_collection(data: CollectionInput, session: Session, user: CurrentUser) -> Any:
    from app.community.collections import create_collection as create

    return await create(session, user, data.name)


@router.get("/collections/{identifier}")
async def collection(
    identifier: UUID, session: Session, user: CurrentUser, locale: DisplayLocale
) -> Any:
    from app.community.collections import collection_items

    return await collection_items(session, user, identifier, locale)


@router.delete("/collections/{identifier}")
async def delete_collection(identifier: UUID, session: Session, user: CurrentUser) -> Any:
    from app.community.collections import delete_collection as remove

    return await remove(session, user, identifier)


@router.post("/collections/{identifier}/items")
async def collect(
    identifier: UUID,
    data: CollectionReference,
    session: Session,
    user: CurrentUser,
    locale: DisplayLocale,
) -> Any:
    from app.community.collections import collect_reference

    return await collect_reference(
        session, user, identifier, data.kind, str(data.id), locale=locale
    )


@router.delete("/collections/{identifier}/items/{item_id}")
async def remove_collected(
    identifier: UUID, item_id: UUID, session: Session, user: CurrentUser
) -> Any:
    from app.community.collections import remove_reference

    return await remove_reference(session, user, identifier, item_id)
