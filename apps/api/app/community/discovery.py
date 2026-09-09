from __future__ import annotations

import json
import re
import secrets
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Query
from sqlalchemy import Text, and_, case, cast, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser, OptionalCurrentUser
from app.community.content import published_post, serialize_post
from app.community.models import (
    Collection,
    CollectionItem,
    Fork,
    Post,
    PostRevision,
    Profile,
    Reaction,
    Relationship,
)
from app.community.policy import (
    cursor_decode,
    cursor_encode,
    digest,
    fail,
    member,
    public_profile,
    rate,
    settings_for,
)
from app.community.router import OpenSession
from app.community.schemas import CollectionInput, CollectionItemInput
from app.db import escape_like
from app.infra import get_redis
from app.models import User
from app.problems import AppError
from app.saved.router import RequestLocale, list_saved_items

router = APIRouter(prefix="/community", tags=["community discovery"])


async def community_public_candidates(
    session: AsyncSession,
    viewer: User | None,
    q: str,
    destinations: list[str],
    topics: list[str],
    limit: int = 100,
    following_only: bool = False,
    locale: str = "",
    itinerary_only: bool | None = None,
) -> list[tuple[Post, PostRevision, Profile]]:
    """IDs are candidates only; every result rechecks the current public snapshot."""
    if not (await settings_for(session)).enabled:
        return []
    if following_only and viewer is None:
        return []
    query = (
        select(Post.id)
        .join(PostRevision, PostRevision.id == Post.published_revision_id)
        .join(Profile, Profile.user_id == Post.author_id)
        .join(User, User.id == Post.author_id)
        .where(
            Post.state == "published",
            Profile.restricted.is_(False),
            Profile.deleted_at.is_(None),
            User.is_active.is_(True),
            User.deleted_at.is_(None),
        )
    )
    if q:
        from app.destinations.catalog import match_destination

        pattern = f"%{escape_like(q[:200])}%"
        match = match_destination(q)
        search_aliases = [q] if match is None else [q, match.id, match.city, *match.aliases]
        query = query.where(
            or_(
                PostRevision.title.ilike(pattern, escape="\\"),
                PostRevision.body.ilike(pattern, escape="\\"),
                *[
                    PostRevision.destination.ilike(f"%{escape_like(alias)}%", escape="\\")
                    for alias in search_aliases
                    if alias
                ],
            )
        )
    if locale:
        query = query.where(PostRevision.locale == locale)
    if itinerary_only is not None:
        no_itinerary = or_(
            PostRevision.itinerary.is_(None), cast(PostRevision.itinerary, Text) == "null"
        )
        query = query.where(~no_itinerary if itinerary_only else no_itinerary)
    if following_only and viewer:
        query = query.where(
            Post.author_id.in_(
                select(Relationship.target_id).where(
                    Relationship.actor_id == viewer.id, Relationship.kind == "follow"
                )
            )
        )
    if destinations:
        from app.destinations.catalog import match_destination

        aliases = set(destinations)
        for destination in destinations:
            matched = match_destination(destination)
            if matched:
                aliases.update([matched.id, matched.city, *matched.aliases])
        query = query.where(
            or_(
                *[
                    PostRevision.destination.ilike(f"%{escape_like(alias)}%", escape="\\")
                    for alias in aliases
                    if alias
                ]
            )
        )
    if topics:
        query = query.where(
            or_(
                *[
                    cast(PostRevision.topics, Text).contains(
                        json.dumps(topic, ensure_ascii=ascii_only)
                    )
                    for topic in topics
                    for ascii_only in (True, False)
                ]
            )
        )
    if viewer:
        blocked = (
            select(Relationship.target_id)
            .where(Relationship.actor_id == viewer.id, Relationship.kind == "block")
            .union(
                select(Relationship.actor_id).where(
                    Relationship.target_id == viewer.id, Relationship.kind == "block"
                )
            )
        )
        query = query.where(Post.author_id.not_in(blocked))
    ids = (
        await session.scalars(
            query.order_by(Post.published_at.desc(), Post.id.desc()).limit(max(1, min(limit, 200)))
        )
    ).all()
    result = []
    for identifier in ids:
        try:
            result.append(await published_post(session, identifier, viewer))
        except AppError as exc:
            if exc.status != 404:
                raise
    return result


@router.get("/feed")
async def feed(
    viewer: OptionalCurrentUser,
    session: OpenSession,
    mode: Literal["latest", "following", "recommended", "saved"] = "latest",
    destination: str = "",
    locale: str = "",
    topic: str = "",
    q: str = "",
    author: UUID | None = None,
    cursor: str | None = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
) -> dict[str, Any]:
    if any(len(value) > 160 for value in (destination, locale, topic, q)):
        raise fail("validation_error", 422)
    if mode in {"following", "saved"} and viewer is None:
        raise fail("authentication_required", 401)
    query = (
        select(Post.id)
        .join(PostRevision, PostRevision.id == Post.published_revision_id)
        .join(
            Profile,
            Profile.user_id == Post.author_id,
        )
        .join(User, User.id == Post.author_id)
        .where(
            Post.state == "published",
            Profile.restricted.is_(False),
            Profile.deleted_at.is_(None),
            User.is_active.is_(True),
        )
    )
    if viewer:
        excluded = (
            select(Relationship.target_id)
            .where(
                Relationship.actor_id == viewer.id,
                Relationship.kind == "block",
            )
            .union(
                select(Relationship.actor_id).where(
                    Relationship.target_id == viewer.id,
                    Relationship.kind == "block",
                )
            )
        )
        query = query.where(Post.author_id.not_in(excluded))
        if mode == "following":
            query = query.where(
                Post.author_id.in_(
                    select(Relationship.target_id).where(
                        Relationship.actor_id == viewer.id,
                        Relationship.kind == "follow",
                    )
                )
            )
        if mode == "saved":
            query = query.where(
                Post.id.in_(
                    select(Reaction.post_id).where(
                        Reaction.user_id == viewer.id,
                        Reaction.kind == "save",
                    )
                )
            )
    if author:
        query = query.where(Post.author_id == author)
    if destination:
        from app.destinations.catalog import match_destination

        matched = match_destination(destination)
        aliases = [destination]
        if matched:
            aliases.extend([matched.id, matched.city, *matched.aliases])
        query = query.where(
            or_(
                *[
                    PostRevision.destination.ilike(f"%{escape_like(alias)}%", escape="\\")
                    for alias in aliases
                    if alias
                ]
            )
        )
    if locale:
        query = query.where(PostRevision.locale == locale)
    if topic:
        query = query.where(
            or_(
                cast(PostRevision.topics, Text).contains(json.dumps(topic, ensure_ascii=False)),
                cast(PostRevision.topics, Text).contains(json.dumps(topic)),
            )
        )
    if q:
        pattern = f"%{escape_like(q)}%"
        query = query.where(
            or_(
                PostRevision.title.ilike(pattern, escape="\\"),
                PostRevision.body.ilike(pattern, escape="\\"),
            )
        )

    if mode == "recommended":
        # Store a short-lived, reader-bound ordering, not content. Subsequent pages
        # re-authorize every post, so withdrawals and blocks take effect immediately.
        fingerprint = digest(
            [str(viewer.id) if viewer else None, destination, locale, topic, q, author]
        )
        if cursor:
            if not re.fullmatch(r"[a-f0-9]{32}:\d{1,4}", cursor):
                raise fail("community_invalid_cursor", 422)
            key, raw_offset = cursor.split(":")
            offset = int(raw_offset)
            cached = await get_redis().get(f"community:feed:{key}")
            if not cached:
                raise fail("community_feed_expired", 409)
            snapshot = json.loads(cached)
            if snapshot["reader"] != fingerprint:
                raise fail("community_invalid_cursor", 422)
            identifiers = snapshot["ids"]
        else:
            cutoff = datetime.now(UTC) - timedelta(days=7)
            saves = (
                select(func.count(func.distinct(Reaction.user_id)))
                .where(
                    Reaction.post_id == Post.id,
                    Reaction.kind == "save",
                    Reaction.user_id != Post.author_id,
                    Reaction.created_at >= cutoff,
                )
                .correlate(Post)
                .scalar_subquery()
            )
            forks = (
                select(func.count(func.distinct(Fork.user_id)))
                .where(
                    Fork.post_id == Post.id,
                    Fork.user_id != Post.author_id,
                    Fork.created_at >= cutoff,
                )
                .correlate(Post)
                .scalar_subquery()
            )
            preference = viewer.preferred_locale if viewer else locale
            profile = await session.get(Profile, viewer.id) if viewer else None
            preferred_languages = (
                profile.languages if profile and profile.languages else [preference]
            )
            preferred_destinations = profile.destinations if profile else []
            ordered = query.order_by(
                case((PostRevision.destination.in_(preferred_destinations), 1), else_=0).desc(),
                case((PostRevision.locale.in_(preferred_languages), 1), else_=0).desc(),
                Post.featured.desc(),
                (saves + forks).desc(),
                Post.published_at.desc(),
                Post.id.desc(),
            ).limit(500)
            identifiers = [str(value) for value in (await session.scalars(ordered)).all()]
            key, offset = secrets.token_hex(16), 0
            await get_redis().set(
                f"community:feed:{key}",
                json.dumps(
                    {
                        "reader": fingerprint,
                        "ids": identifiers,
                    }
                ),
                ex=300,
            )
        items: list[dict[str, Any]] = []
        while offset < len(identifiers) and len(items) < limit:
            identifier = UUID(identifiers[offset])
            offset += 1
            try:
                post, revision, profile = await published_post(session, identifier, viewer)
                items.append(await serialize_post(session, post, revision, profile, viewer))
            except AppError as exc:
                if exc.status != 404:
                    raise
        return {
            "items": items,
            "next_cursor": f"{key}:{offset}" if offset < len(identifiers) else None,
        }

    boundary = cursor_decode(cursor)
    if boundary:
        moment, identifier_boundary = boundary
        query = query.where(
            or_(
                Post.published_at < moment,
                and_(Post.published_at == moment, Post.id < identifier_boundary),
            )
        )
    identifiers = (
        await session.scalars(
            query.order_by(
                Post.published_at.desc(),
                Post.id.desc(),
            ).limit(limit + 1)
        )
    ).all()
    items = []
    next_cursor = None
    for identifier in identifiers[:limit]:
        post, revision, profile = await published_post(session, identifier, viewer)
        items.append(await serialize_post(session, post, revision, profile, viewer))
        if post.published_at:
            next_cursor = cursor_encode(post.published_at, post.id)
    return {"items": items, "next_cursor": next_cursor if len(identifiers) > limit else None}


@router.get("/search/profiles")
async def search_profiles(
    viewer: OptionalCurrentUser,
    session: OpenSession,
    q: Annotated[str, Query(max_length=100)] = "",
) -> dict[str, Any]:
    query = (
        select(Profile)
        .join(User, User.id == Profile.user_id)
        .where(
            Profile.deleted_at.is_(None),
            Profile.restricted.is_(False),
            User.is_active.is_(True),
            or_(
                Profile.handle.ilike(f"%{escape_like(q)}%", escape="\\"),
                Profile.display_name.ilike(f"%{escape_like(q)}%", escape="\\"),
            ),
        )
    )
    if viewer:
        query = query.where(
            Profile.user_id.not_in(
                select(Relationship.target_id)
                .where(
                    Relationship.actor_id == viewer.id,
                    Relationship.kind == "block",
                )
                .union(
                    select(Relationship.actor_id).where(
                        Relationship.target_id == viewer.id,
                        Relationship.kind == "block",
                    )
                )
            )
        )
    return {
        "items": [
            public_profile(row)
            for row in (
                await session.scalars(
                    query.order_by(Profile.handle).limit(50),
                )
            ).all()
        ]
    }


@router.get("/search/places")
async def search_places(
    session: OpenSession,
    locale: RequestLocale,
    q: Annotated[str, Query(max_length=160)] = "",
) -> dict[str, Any]:
    from urllib.parse import urlencode

    from app.community.pet_models import PetPlace, PlaceReference
    from app.destinations.catalog import DESTINATIONS, match_destination
    from app.destinations.localized import CITY_NAMES, city_name_for
    from app.foods.publication import publishable_merchant_filters
    from app.hotspots.service import load_hotspot_names
    from app.i18n import LOCALES
    from app.localized_names import resolve_localized_name
    from app.models import FoodMerchant, HotspotLocalization, TravelHotspot

    pattern = f"%{escape_like(q)}%"
    matched = match_destination(q) if q else None
    destinations = {
        profile.id
        for profile in DESTINATIONS
        if (matched and profile.id == matched.id)
        or (
            q
            and q.casefold()
            in {name.casefold() for name in CITY_NAMES.get(profile.id, {}).values()}
        )
    }
    pets = (
        await session.scalars(
            select(PetPlace)
            .where(
                PetPlace.status == "approved",
                or_(
                    PetPlace.name.ilike(pattern, escape="\\"),
                    *[
                        PetPlace.names[language].as_string().ilike(pattern, escape="\\")
                        for language in LOCALES
                    ],
                    PetPlace.destination.ilike(pattern, escape="\\"),
                    PetPlace.destination.in_(destinations),
                ),
            )
            .order_by(PetPlace.name, PetPlace.id)
            .limit(50)
        )
    ).all()
    references = (
        await session.scalars(
            select(PlaceReference).where(PlaceReference.place_id.in_([place.id for place in pets]))
        )
    ).all()
    linked = {(reference.kind, reference.target) for reference in references}
    items: list[dict[str, Any]] = [
        {
            "id": str(place.id),
            "kind": "pet_place",
            "name": resolve_localized_name(place.names, locale, fallback=place.name),
            "destination": place.destination,
            "href": f"/pet-friendly/{place.id}",
        }
        for place in pets
    ]
    hotspots = (
        await session.scalars(
            select(TravelHotspot)
            .where(
                TravelHotspot.is_active.is_(True),
                TravelHotspot.review_status == "approved",
                or_(
                    TravelHotspot.name.ilike(pattern, escape="\\"),
                    TravelHotspot.search_text.ilike(pattern, escape="\\"),
                    TravelHotspot.destination_id.in_(destinations),
                    TravelHotspot.id.in_(
                        select(HotspotLocalization.hotspot_id).where(
                            HotspotLocalization.name.ilike(pattern, escape="\\")
                        )
                    ),
                ),
            )
            .order_by(TravelHotspot.name, TravelHotspot.id)
            .limit(50)
        )
    ).all()
    names = await load_hotspot_names(session, hotspots)
    for hotspot in hotspots:
        if ("hotspot", str(hotspot.id)) not in linked:
            items.append(
                {
                    "id": str(hotspot.id),
                    "kind": "hotspot",
                    "name": resolve_localized_name(
                        names.get(hotspot.id), locale, fallback=hotspot.name
                    ),
                    "destination": city_name_for(
                        hotspot.destination_id, locale, fallback=hotspot.city_name
                    ),
                    "href": "/hotspots?"
                    + urlencode(
                        {"hotspot": str(hotspot.id), "destination": hotspot.destination_id}
                    ),
                }
            )
    merchants = (
        await session.scalars(
            select(FoodMerchant)
            .where(
                *publishable_merchant_filters(),
                or_(
                    FoodMerchant.name.ilike(pattern, escape="\\"),
                    FoodMerchant.local_name.ilike(pattern, escape="\\"),
                    *[
                        FoodMerchant.names_json[language].as_string().ilike(pattern, escape="\\")
                        for language in LOCALES
                    ],
                    FoodMerchant.destination_id.in_(destinations),
                ),
            )
            .order_by(FoodMerchant.name, FoodMerchant.id)
            .limit(50)
        )
    ).all()
    for merchant in merchants:
        if ("merchant", str(merchant.id)) not in linked:
            items.append(
                {
                    "id": str(merchant.id),
                    "kind": "merchant",
                    "name": resolve_localized_name(
                        merchant.names_json, locale, fallback=merchant.name
                    ),
                    "destination": city_name_for(
                        merchant.destination_id, locale, fallback=merchant.destination_id
                    ),
                    "href": "/foods?"
                    + urlencode(
                        {"merchant": str(merchant.id), "destination": merchant.destination_id}
                    ),
                }
            )
    return {"items": sorted(items, key=lambda item: (item["name"].casefold(), item["id"]))[:100]}


@router.get("/saved")
async def unified_saved(
    user: CurrentUser, session: OpenSession, locale: RequestLocale
) -> dict[str, Any]:
    await member(session, user)
    return {
        "posts": await feed(user, session, mode="saved", limit=50),
        "places": await list_saved_items(user, session, locale, type="all", limit=100),
        "collections": await collections(user, session),
    }


@router.get("/collections")
async def collections(user: CurrentUser, session: OpenSession) -> dict[str, Any]:
    rows = (
        await session.scalars(
            select(Collection)
            .where(Collection.user_id == user.id, Collection.system_role.is_(None))
            .order_by(Collection.created_at)
        )
    ).all()
    return {"items": [{"id": str(row.id), "name": row.name} for row in rows]}


@router.post("/collections", status_code=201)
async def create_collection(
    payload: CollectionInput,
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, str]:
    await member(session, user, lock=True)
    await rate(session, user)
    count = await session.scalar(
        select(func.count())
        .select_from(Collection)
        .where(Collection.user_id == user.id, Collection.system_role.is_(None))
    )
    if (count or 0) >= 100:
        raise fail("community_collection_limit", 403)
    row = Collection(user_id=user.id, name=payload.name)
    session.add(row)
    await session.commit()
    return {"id": str(row.id), "name": row.name}


async def owned_collection(session: AsyncSession, identifier: UUID, user: User) -> Collection:
    from app.community.collections import owned_collection as owned

    return await owned(session, user, identifier, lock=True)


@router.put("/collections/{identifier}")
async def rename_collection(
    identifier: UUID,
    payload: CollectionInput,
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, str]:
    row = await owned_collection(session, identifier, user)
    row.name = payload.name
    await session.commit()
    return {"id": str(row.id), "name": row.name}


@router.delete("/collections/{identifier}")
async def delete_collection(
    identifier: UUID, user: CurrentUser, session: OpenSession
) -> dict[str, bool]:
    from app.community.collections import delete_collection as remove

    return await remove(session, user, identifier)


@router.get("/collections/{identifier}/items")
async def collection_items(
    identifier: UUID, user: CurrentUser, session: OpenSession
) -> dict[str, Any]:
    await owned_collection(session, identifier, user)
    rows = (
        await session.scalars(
            select(CollectionItem)
            .where(
                CollectionItem.collection_id == identifier,
            )
            .order_by(CollectionItem.created_at.desc())
            .limit(500)
        )
    ).all()
    items: list[dict[str, Any]] = []
    for row in rows:
        item: dict[str, Any] = {"id": str(row.id), "kind": row.kind, "target": row.target}
        if row.kind == "post":
            try:
                post, revision, profile = await published_post(session, UUID(row.target), user)
                item["post"] = await serialize_post(session, post, revision, profile, user)
            except AppError as exc:
                if exc.status != 404:
                    raise
                item["unavailable"] = True
        elif row.kind in {"guide", "hotel"}:
            from app.discovery.service import resolve_discovery_items

            values = await resolve_discovery_items(
                session, [f"{row.kind}:{row.target}"], user, "zh-TW"
            )
            if values:
                item["discovery"] = values[0].model_dump(mode="json")
            else:
                item["unavailable"] = True
        else:
            try:
                await resolve_place(session, row.kind, row.target)
            except AppError as exc:
                if exc.status != 404:
                    raise
                item["unavailable"] = True
        items.append(item)
    return {"items": items}


@router.put("/collections/{identifier}/items")
async def collect(
    identifier: UUID,
    payload: CollectionItemInput,
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, bool]:
    from app.saved.service import ensure_base, lock_account

    await lock_account(session, user)
    await member(session, user, lock=True)
    await owned_collection(session, identifier, user)
    if payload.kind == "post":
        try:
            target = UUID(payload.target)
        except ValueError as exc:
            raise fail("community_not_found", 404) from exc
        await published_post(session, target, user)
        payload.target = str(target)
    elif payload.kind in {"guide", "hotel"}:
        from app.discovery.service import resolve_discovery_items

        if not await resolve_discovery_items(
            session, [f"{payload.kind}:{payload.target}"], user, "zh-TW"
        ):
            raise fail("community_not_found", 404)
    else:
        await resolve_place(session, payload.kind, payload.target)
    await ensure_base(session, user, payload.kind, payload.target)
    target_filter = CollectionItem.target == payload.target
    if payload.kind in {"post", "guide", "hotel"}:
        target_filter = (
            func.lower(func.replace(CollectionItem.target, "-", "")) == UUID(payload.target).hex
        )
    row = await session.scalar(
        select(CollectionItem).where(
            CollectionItem.collection_id == identifier,
            CollectionItem.kind == payload.kind,
            target_filter,
        )
    )
    if row is None:
        count = await session.scalar(
            select(func.count())
            .select_from(CollectionItem)
            .where(CollectionItem.collection_id == identifier)
        )
        if (count or 0) >= 500:
            raise fail("community_collection_limit", 403)
        session.add(
            CollectionItem(collection_id=identifier, kind=payload.kind, target=payload.target)
        )
        from app.analytics.service import record_event

        await record_event(
            session,
            "content_saved",
            path="/explore/collections",
            user_id=user.id,
            properties={"kind": payload.kind},
        )
    await session.commit()
    return {"collected": True}


async def resolve_place(session: AsyncSession, kind: str, target: str) -> None:
    if kind == "pet_place":
        from app.community.pet_models import PetPlace

        try:
            place = await session.get(PetPlace, UUID(target))
        except ValueError as exc:
            raise fail("community_not_found", 404) from exc
        if place is None or place.status != "approved":
            raise fail("community_not_found", 404)
    else:
        from app.saved.router import _food, _hotspot, _merchant, _restaurant

        resolver = {
            "food": _food,
            "hotspot": _hotspot,
            "merchant": _merchant,
            "restaurant": _restaurant,
        }
        if kind not in resolver:
            raise fail("community_not_found", 404)
        await resolver[kind](session, target)


@router.delete("/collections/{identifier}/items/{item_id}")
async def remove_collected(
    identifier: UUID,
    item_id: UUID,
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, Any]:
    from app.community.collections import remove_reference

    return await remove_reference(session, user, identifier, item_id)
