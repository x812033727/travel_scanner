"""Reader-bound short-lived ordering, with live authorization on every page."""

from __future__ import annotations

import hashlib
import json
import re
import secrets
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.community.models import Collection, CollectionItem, Reaction, Relationship
from app.config import get_settings
from app.discovery.models import DiscoveryDismissal
from app.discovery.policy import parse_key
from app.discovery.preferences import get_preferences, payload
from app.discovery.schemas import CATEGORY_KINDS, Category, DiscoveryItem
from app.discovery.sources import catalog_items, community_item
from app.i18n import Locale
from app.infra import get_redis
from app.models import (
    FoodFavorite,
    FoodMerchantFavorite,
    HotspotFavorite,
    TravelServiceFavorite,
    User,
)
from app.problems import AppError

SNAPSHOT_LIMIT = 500
SNAPSHOT_TTL = 300


async def resolve_discovery_items(
    session: AsyncSession,
    identifiers: list[str],
    viewer: User | None,
    locale: Locale,
    *,
    destinations: list[str] | None = None,
) -> list[DiscoveryItem]:
    if not get_settings().discovery_enabled:
        return []
    if len(identifiers) > 100:
        raise AppError(422, "validation_error", "Too many discovery references")
    grouped: dict[str, list[Any]] = {}
    canonical = []
    for value in identifiers:
        kind, identifier = parse_key(value)
        grouped.setdefault(kind, []).append(identifier)
        canonical.append(f"{kind}:{identifier}")
    if not canonical:
        return []
    items = await catalog_items(session, locale, identifiers=grouped, destinations=destinations)
    for identifier in grouped.get("post", []):
        item = await community_item(session, identifier, viewer, locale)
        if item:
            items.append(item)
    by_id = {item.id: item for item in items}
    return [by_id[key] for key in dict.fromkeys(canonical) if key in by_id]


async def saved_keys(session: AsyncSession, viewer: User) -> list[str]:
    keys: list[str] = []
    for kind, model, column in (
        ("hotspot", HotspotFavorite, HotspotFavorite.hotspot_id),
        ("food", FoodFavorite, FoodFavorite.food_id),
        ("merchant", FoodMerchantFavorite, FoodMerchantFavorite.merchant_id),
        ("hotel", TravelServiceFavorite, TravelServiceFavorite.product_id),
    ):
        rows = await session.scalars(
            select(column)
            .where(model.user_id == viewer.id)
            .order_by(model.updated_at.desc())
            .limit(100)
        )
        keys.extend(f"{kind}:{identifier}" for identifier in rows)
    collection_rows = (
        await session.execute(
            select(CollectionItem.kind, CollectionItem.target)
            .join(Collection, Collection.id == CollectionItem.collection_id)
            .where(Collection.user_id == viewer.id)
            .order_by(CollectionItem.created_at.desc())
            .limit(100)
        )
    ).all()
    keys.extend(
        f"{kind}:{target}"
        for kind, target in collection_rows
        if kind in {"hotspot", "food", "merchant", "hotel", "guide", "post"}
    )
    posts = await session.scalars(
        select(Reaction.post_id)
        .where(Reaction.user_id == viewer.id, Reaction.kind == "save")
        .order_by(Reaction.created_at.desc())
        .limit(100)
    )
    keys.extend(f"post:{identifier}" for identifier in posts)
    return list(dict.fromkeys(keys))[:500]


async def explicit_context(
    session: AsyncSession, viewer: User | None, locale: Locale
) -> dict[str, Any]:
    prefs = await get_preferences(session, viewer.id) if viewer else payload(None)
    context: dict[str, Any] = {
        "preferences": prefs,
        "saved_ids": set(),
        "saved_destinations": set(),
        "saved_topics": set(),
        "following": set(),
    }
    if viewer and prefs["include_saved"]:
        keys = await saved_keys(session, viewer)
        for start in range(0, len(keys), 100):
            for item in await resolve_discovery_items(
                session, keys[start : start + 100], viewer, locale
            ):
                context["saved_ids"].add(item.id)
                if item.destination:
                    context["saved_destinations"].add(item.destination["id"])
                context["saved_topics"].update(item.topics)
    if viewer and prefs["include_following"]:
        context["following"] = {
            str(value)
            for value in await session.scalars(
                select(Relationship.target_id)
                .where(Relationship.actor_id == viewer.id, Relationship.kind == "follow")
                .order_by(Relationship.target_id)
                .limit(200)
            )
        }
    return context


def reason(item: DiscoveryItem, context: dict[str, Any]) -> tuple[int, str]:
    prefs = context["preferences"]
    if item.destination and item.destination["id"] in prefs["destinations"]:
        return 4, "destination_interest"
    if set(item.topics) & set(prefs["topics"]):
        return 3, "topic_interest"
    if item.author and item.author["id"] in context["following"]:
        return 2, "following"
    if (
        item.id in context["saved_ids"]
        or set(item.topics) & context["saved_topics"]
        or (item.destination and item.destination["id"] in context["saved_destinations"])
    ):
        return 1, "saved_interest"
    return 0, "latest"


async def candidates(
    session: AsyncSession,
    viewer: User | None,
    locale: Locale,
    *,
    q: str,
    kinds: set[str],
    destinations: list[str],
    topics: list[str],
    mode: str,
    content_locale: Locale | None = None,
) -> list[DiscoveryItem]:
    items = (
        []
        if mode == "following"
        else await catalog_items(
            session,
            locale,
            q=q,
            kinds=kinds,
            destinations=destinations,
            content_locale=content_locale,
            topics=topics,
        )
    )
    if not kinds or kinds & {"post", "itinerary"}:
        from app.community.discovery import community_public_candidates

        posts = await community_public_candidates(
            session,
            viewer,
            q,
            destinations,
            topics,
            limit=100,
            following_only=mode == "following",
            locale=content_locale or "",
            itinerary_only=True if kinds == {"itinerary"} else False if kinds == {"post"} else None,
        )
        for post, _revision, _profile in posts:
            item = await community_item(session, post.id, viewer, locale)
            if item:
                items.append(item)
    return [
        item
        for item in items
        if (not kinds or item.kind in kinds) and (not topics or set(topics) & set(item.topics))
    ]


async def page(
    session: AsyncSession,
    viewer: User | None,
    locale: Locale,
    *,
    q: str = "",
    kinds: set[str] | None = None,
    destinations: list[str] | None = None,
    topics: list[str] | None = None,
    mode: str = "latest",
    cursor: str | None = None,
    limit: int = 20,
    content_locale: Locale | None = None,
    category: Category = "all",
) -> dict[str, Any]:
    kinds, destinations, topics = kinds or set(), destinations or [], topics or []
    if category != "all":
        kinds = kinds & CATEGORY_KINDS[category] if kinds else CATEGORY_KINDS[category].copy()
    no_matches = category != "all" and not kinds
    if mode == "following" and not viewer:
        raise AppError(401, "authentication_required", "請先登入")
    prefs = await get_preferences(session, viewer.id) if viewer else payload(None)
    # No raw queries, visited content, private trip fields or preference payloads
    # are retained in Redis. This digest binds the ephemeral ordering to the reader.
    fingerprint = hashlib.sha256(
        json.dumps(
            [
                str(viewer.id) if viewer else None,
                locale,
                content_locale,
                q,
                sorted(kinds),
                destinations,
                topics,
                mode,
                category,
                prefs,
            ],
            sort_keys=True,
        ).encode()
    ).hexdigest()
    context = None
    if cursor:
        if not re.fullmatch(r"[a-f0-9]{32}:\d{1,4}", cursor):
            raise AppError(422, "community_invalid_cursor", "分頁參數無效")
        key, raw_offset = cursor.split(":")
        offset = int(raw_offset)
        raw = await get_redis().get(f"discovery:page:{key}")
        if not raw:
            raise AppError(409, "community_feed_expired", "分頁已過期，請重新整理")
        snapshot = json.loads(raw)
        if snapshot.get("reader") != fingerprint or offset > len(snapshot["ids"]):
            raise AppError(422, "community_invalid_cursor", "分頁參數無效")
        keys = snapshot["ids"]
    else:
        items = (
            []
            if no_matches
            else await candidates(
                session,
                viewer,
                locale,
                q=q,
                kinds=kinds,
                destinations=destinations,
                topics=topics,
                mode=mode,
                content_locale=content_locale,
            )
        )
        context = (
            await explicit_context(session, viewer, locale)
            if mode == "recommended" and not no_matches
            else None
        )
        if context:
            # Retrieve explicit interests before the bounded recency window; an
            # older relevant city/topic must not disappear behind 100 newer rows.
            interest_destinations = sorted(
                set(context["preferences"]["destinations"]) | context["saved_destinations"]
            )
            interest_topics = sorted(
                set(context["preferences"]["topics"]) | context["saved_topics"]
            )
            if context["following"]:
                items.extend(
                    await candidates(
                        session,
                        viewer,
                        locale,
                        q=q,
                        kinds=kinds,
                        destinations=destinations,
                        topics=topics,
                        mode="following",
                        content_locale=content_locale,
                    )
                )
            if interest_destinations and not destinations:
                items.extend(
                    await candidates(
                        session,
                        viewer,
                        locale,
                        q=q,
                        kinds=kinds,
                        destinations=interest_destinations[:20],
                        topics=topics,
                        mode=mode,
                        content_locale=content_locale,
                    )
                )
            if interest_topics and not topics:
                items.extend(
                    await candidates(
                        session,
                        viewer,
                        locale,
                        q=q,
                        kinds=kinds,
                        destinations=destinations,
                        topics=interest_topics[:20],
                        mode=mode,
                        content_locale=content_locale,
                    )
                )
        items.sort(
            key=lambda item: (
                reason(item, context)[0] if context else 0,
                item.published_at or item.updated_at or "",
                item.id,
            ),
            reverse=True,
        )
        keys = list(dict.fromkeys(item.id for item in items))[:SNAPSHOT_LIMIT]
        offset, key = 0, secrets.token_hex(16)
        await get_redis().set(
            f"discovery:page:{key}",
            json.dumps({"reader": fingerprint, "ids": keys}),
            ex=SNAPSHOT_TTL,
        )
    dismissed = (
        set(
            await session.scalars(
                select(DiscoveryDismissal.content_key).where(
                    DiscoveryDismissal.user_id == viewer.id,
                    DiscoveryDismissal.content_key.in_(keys),
                )
            )
        )
        if viewer and keys
        else set()
    )
    output: list[DiscoveryItem] = []
    while offset < len(keys) and len(output) < limit:
        batch = keys[offset : offset + min(100, limit - len(output))]
        offset += len(batch)
        for item in await resolve_discovery_items(
            session, batch, viewer, locale, destinations=destinations
        ):
            if (
                content_locale
                and item.kind in {"article", "video", "post", "itinerary"}
                and item.locale != content_locale
            ):
                continue
            if (
                item.id in dismissed
                or (kinds and item.kind not in kinds)
                or (topics and not set(topics) & set(item.topics))
            ):
                continue
            if destinations and (
                not item.destination or item.destination["id"] not in destinations
            ):
                continue
            if mode == "following" and viewer:
                if not item.author or not await session.scalar(
                    select(Relationship.target_id)
                    .where(
                        Relationship.actor_id == viewer.id,
                        Relationship.target_id == parse_author(item),
                        Relationship.kind == "follow",
                    )
                    .limit(1)
                ):
                    continue
            if mode == "recommended":
                context = context or await explicit_context(session, viewer, locale)
                item.recommendation_reason = reason(item, context)[1]
            else:
                item.recommendation_reason = "following" if mode == "following" else "latest"
            output.append(item)
    return {
        "enabled": True,
        "items": output,
        "next_cursor": f"{key}:{offset}" if offset < len(keys) else None,
        "query": q,
        "filters": {
            "category": category,
            "kinds": sorted(kinds),
            "destinations": destinations,
            "topics": topics,
        },
    }


def parse_author(item: DiscoveryItem) -> Any:
    from uuid import UUID

    return UUID(item.author["id"]) if item.author else None
