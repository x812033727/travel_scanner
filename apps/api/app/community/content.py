from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.community.media import check_media
from app.community.models import Fork, Media, Post, PostRevision, Profile, Reaction
from app.community.places import canonical_refs, public_places
from app.community.policy import digest, fail, member, metric, public_profile, visible_profile
from app.community.schemas import ForkInput, PlaceInput, PostInput
from app.community.videos import public_video_refs
from app.localized_names import item_names, sanitize_localized_names
from app.models import TripPlan, TripPlanItem, User


async def owned_post(session: AsyncSession, user: User, identifier: UUID) -> Post:
    post = await session.scalar(
        select(Post)
        .where(
            Post.id == identifier,
            Post.author_id == user.id,
            Post.state != "deleted",
        )
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if post is None:
        raise fail("community_not_found", 404)
    return post


async def published_post(
    session: AsyncSession, identifier: UUID, viewer: User | None
) -> tuple[Post, PostRevision, Profile]:
    post = await session.scalar(
        select(Post).where(Post.id == identifier).execution_options(populate_existing=True)
    )
    if post is None or post.state != "published" or post.published_revision_id is None:
        raise fail("community_not_found", 404)
    profile = await visible_profile(session, post.author_id, viewer)
    revision = await session.get(PostRevision, post.published_revision_id)
    if revision is None or revision.post_id != post.id:
        raise fail("community_not_found", 404)
    return post, revision, profile


def check_version(post: Post, version: int | None) -> None:
    if version != post.version:
        raise fail("community_version_conflict", 409)


def itinerary_snapshot(trip: TripPlan, items: list[TripPlanItem]) -> dict[str, Any]:
    dated = [row.day_date for row in items if row.day_date is not None]
    start = trip.start_date or (min(dated) if dated else date.today())
    stops: list[dict[str, Any]] = []
    for row in items:
        if row.is_skipped or row.item_type in {"flight", "hotel", "lodging"}:
            continue
        if row.system_role in {"outbound_flight", "return_flight", "hotel_start", "hotel_end"}:
            continue
        day = ((row.day_date or start) - start).days + 1
        if day < 1 or day > 90:
            continue
        stops.append(
            {
                "day": day,
                "position": row.position,
                "title": row.title or "",
                "location_name": row.location_name or "",
                "item_type": row.item_type,
                "duration_minutes": row.duration_minutes,
                "provider_place_id": row.provider_place_id,
                "names": sanitize_localized_names((row.names_json or {}).get("title")),
                # Persist only coordinates whose independent provenance was reviewed.
                "latitude": float(row.latitude)
                if row.coordinate_verified_at and row.latitude is not None
                else None,
                "longitude": float(row.longitude)
                if row.coordinate_verified_at and row.longitude is not None
                else None,
                "coordinate_source_type": row.coordinate_source_type
                if row.coordinate_verified_at
                else None,
                "coordinate_source_url": row.coordinate_source_url
                if row.coordinate_verified_at
                else None,
                "coordinate_verified_at": row.coordinate_verified_at.isoformat()
                if row.coordinate_verified_at
                else None,
            }
        )
    return {
        "destination": trip.destination_name or "",
        "timezone": trip.timezone,
        "days": max((row["day"] for row in stops), default=1),
        "stops": stops,
    }


async def new_revision(
    session: AsyncSession,
    user: User,
    post: Post,
    payload: PostInput,
) -> PostRevision:
    await check_media(session, user, payload.media_ids)
    places = canonical_refs(
        payload.places
        if payload.places is not None
        else [PlaceInput(kind="pet_place", id=value) for value in payload.place_ids]
    )
    if len(await public_places(session, places)) != len(places):
        raise fail("community_place_invalid", 422)
    itinerary = None
    if payload.keep_itinerary and post.draft_revision_id:
        previous = await session.get(PostRevision, post.draft_revision_id)
        itinerary = previous.itinerary if previous else None
    if payload.source_trip_id:
        source = await session.scalar(
            select(TripPlan).where(
                TripPlan.id == payload.source_trip_id,
                TripPlan.user_id == user.id,
            )
        )
        if source is None:
            raise fail("community_not_found", 404)
        items = list(
            (
                await session.scalars(
                    select(TripPlanItem)
                    .where(
                        TripPlanItem.trip_plan_id == source.id,
                    )
                    .order_by(TripPlanItem.day_date, TripPlanItem.position)
                )
            ).all()
        )
        itinerary = itinerary_snapshot(source, items)
    revision = PostRevision(
        post_id=post.id,
        title=payload.title,
        body=payload.body,
        locale=payload.locale,
        destination=payload.destination,
        kind=payload.kind,
        topics=payload.topics,
        place_ids=[ref["id"] for ref in places if ref["kind"] == "pet_place"],
        place_refs=places,
        media_ids=[str(value) for value in payload.media_ids],
        video_refs=[ref.model_dump() for ref in payload.video_refs],
        itinerary=itinerary,
        allow_fork=payload.allow_fork and itinerary is not None,
    )
    session.add(revision)
    await session.flush()
    return revision


async def public_media_refs(
    session: AsyncSession, revision: PostRevision
) -> list[dict[str, Any]]:
    """Project ordered metadata only from a caller-authorized revision.

    This does not grant image access: the media endpoint reauthorizes every
    short-lived URL. Never expose storage keys or signed URLs in this projection.
    """
    if not revision.media_ids:
        return []
    images = (
        await session.scalars(
            select(Media).where(
                Media.id.in_([UUID(value) for value in revision.media_ids]),
                Media.deleted_at.is_(None),
            )
        )
    ).all()
    by_id = {str(image.id): image for image in images}
    return [
        {
            "id": value,
            "alt": by_id[value].alt,
            "width": by_id[value].width,
            "height": by_id[value].height,
        }
        for value in revision.media_ids
        if value in by_id
    ]


async def serialize_post(
    session: AsyncSession,
    post: Post,
    revision: PostRevision,
    profile: Profile,
    viewer: User | None = None,
    *,
    owner: bool = False,
) -> dict[str, Any]:
    reactions = {
        kind: count
        for kind, count in (
            await session.execute(
                select(Reaction.kind, func.count())
                .where(
                    Reaction.post_id == post.id,
                )
                .group_by(Reaction.kind)
            )
        ).all()
    }
    mine = (
        set(
            (
                await session.scalars(
                    select(Reaction.kind).where(
                        Reaction.post_id == post.id,
                        Reaction.user_id == viewer.id,
                    )
                )
            ).all()
        )
        if viewer
        else set()
    )
    places = await public_places(
        session,
        revision.place_refs or [{"kind": "pet_place", "id": value} for value in revision.place_ids],
    )
    result: dict[str, Any] = {
        "id": str(post.id),
        "revision_id": str(revision.id),
        "author": public_profile(profile),
        "title": revision.title,
        "body": revision.body,
        "locale": revision.locale,
        "destination": revision.destination,
        "kind": revision.kind,
        "topics": revision.topics,
        "place_ids": [place["id"] for place in places if place["kind"] == "pet_place"],
        "places": places,
        "video_refs": await public_video_refs(session, revision.video_refs or []),
        "media": await public_media_refs(session, revision),
        "itinerary": revision.itinerary,
        "allow_fork": revision.allow_fork,
        "published_at": post.published_at,
        "featured": post.featured,
        "likes": reactions.get("like", 0),
        "saves": reactions.get("save", 0),
        "liked": "like" in mine,
        "saved": "save" in mine,
    }
    if owner:
        result.update(
            version=post.version,
            state=post.state,
            pending_revision_id=str(post.pending_revision_id) if post.pending_revision_id else None,
        )
    return result


async def fork_post(
    session: AsyncSession,
    user: User,
    identifier: UUID,
    payload: ForkInput,
) -> dict[str, Any]:
    from app.trips.router import limit_for
    from app.trips.schedule import ensure_system_slots

    # Serialize same-member forks without blocking foreign-key KEY SHARE locks
    # from comments. FOR UPDATE here forms a cycle with their post-row lock.
    await session.scalar(select(User).where(User.id == user.id).with_for_update(key_share=True))
    await member(session, user)
    fingerprint = digest({"post": str(identifier), "date": payload.start_date})
    replay = await session.scalar(
        select(Fork).where(
            Fork.user_id == user.id,
            Fork.idempotency_key == payload.idempotency_key,
        )
    )
    if replay:
        if replay.request_hash != fingerprint:
            raise fail("community_idempotency_conflict", 409)
        return {"trip_id": str(replay.trip_id), "replayed": True}
    post, revision, profile = await published_post(session, identifier, user)
    if not revision.allow_fork or not revision.itinerary:
        raise fail("community_fork_disabled", 403)
    count = await session.scalar(
        select(func.count())
        .select_from(TripPlan)
        .where(
            TripPlan.user_id == user.id,
        )
    )
    if (count or 0) >= await limit_for(session, user.id, "saved_trips"):
        raise fail("trip_limit_reached", 403)
    snapshot = revision.itinerary
    trip = TripPlan(
        user_id=user.id,
        name=revision.title,
        mode="manual",
        total_price=0,
        currency=user.preferred_currency,
        start_date=payload.start_date,
        end_date=payload.start_date + timedelta(days=snapshot["days"] - 1),
        destination_name=snapshot["destination"],
        timezone=snapshot["timezone"],
        data={
            "source": "community",
            "creation_mode": "shared_trip",
            "prices_checked": False,
            "community_source": {
                "post_id": str(post.id),
                "revision_id": str(revision.id),
                "author": profile.handle,
            },
            "routing": {"status": "stale", "total": 0, "completed": 0},
            "planning_mode": "manual_blank",
        },
    )
    session.add(trip)
    await session.flush()
    copied_items = []
    for stop in snapshot["stops"]:
        day = payload.start_date + timedelta(days=stop["day"] - 1)
        item = TripPlanItem(
            trip_plan_id=trip.id,
            item_type=stop["item_type"],
            day_date=day,
            position=stop["position"],
            title=stop["title"],
            location_name=stop["location_name"],
            duration_minutes=stop["duration_minutes"],
            provider_place_id=stop["provider_place_id"],
            names_json=item_names(title=stop["names"]),
            latitude=stop["latitude"],
            longitude=stop["longitude"],
            coordinate_source_type=stop["coordinate_source_type"],
            coordinate_source_url=stop["coordinate_source_url"],
            coordinate_verified_at=datetime.fromisoformat(stop["coordinate_verified_at"])
            if stop["coordinate_verified_at"]
            else None,
            locked=False,
            fixed_time=False,
            is_skipped=False,
            data={},
        )
        session.add(item)
        copied_items.append(item)
    # Match ordinary trip creation: initialize empty schedule anchors atomically
    # with the private copy. Otherwise simultaneous first reads each try to add
    # the same system roles during legacy hydration and can fail with HTTP 500.
    # These are blank placeholders, never the source traveller's private details.
    ensure_system_slots(session, trip, copied_items)
    session.add(
        Fork(
            user_id=user.id,
            post_id=post.id,
            revision_id=revision.id,
            trip_id=trip.id,
            idempotency_key=payload.idempotency_key,
            request_hash=fingerprint,
        )
    )
    if post.author_id != user.id:
        await metric(session, user.id, "fork", str(post.id))
        await metric(session, user.id, "trip_created", str(post.id))
    await session.commit()
    return {"trip_id": str(trip.id), "replayed": False}
