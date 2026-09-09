"""Discovery/social boundaries; no external provider or production database calls."""

from __future__ import annotations

import asyncio
import runpy
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError
from sqlalchemy import delete, func, inspect, null, select, update
from test_community_foundation import Harness
from test_community_foundation import harness as community_harness

from app.community import collections as private_collections
from app.community.content import public_media_refs, published_post, serialize_post
from app.community.discovery import community_public_candidates
from app.community.jobs import erase_account
from app.community.models import (
    CollectionItem,
    CreatorInvitation,
    Media,
    Post,
    PostRevision,
    Profile,
    Relationship,
)
from app.community.schemas import PostInput
from app.community.videos import public_video_refs, youtube_embed_metadata, youtube_source_id
from app.config import get_settings
from app.discovery.models import DiscoveryDismissal, DiscoveryPreference
from app.models import (
    AdminAuditLog,
    HotspotGuide,
    ProviderConfig,
    TravelHotspot,
    TravelServiceConfig,
    TravelServiceProduct,
    User,
)
from app.problems import AppError

VIDEO = "dQw4w9WgXcQ"
OTHER_VIDEO = "abcdefghijk"
harness = community_harness


@pytest.fixture(autouse=True)
def discovery_rollout_off(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(get_settings(), "discovery_enabled", False)


@pytest.mark.parametrize(
    "identifier",
    ["", "short", VIDEO + "x", "é" * 11, "https://youtu.be/" + VIDEO, "abc defghij", "<script>abc"],
)
def test_video_reference_rejects_noncanonical_ids(identifier: str) -> None:
    with pytest.raises(ValidationError):
        PostInput(video_refs=[{"provider": "youtube", "video_id": identifier}])


def test_video_reference_contract_never_accepts_client_trust_or_duplicate_ids() -> None:
    ref = {"provider": "youtube", "video_id": VIDEO}
    assert PostInput(video_refs=[ref]).video_refs[0].model_dump() == ref
    for refs in (
        [ref, ref],
        [{**ref, "embed_url": "https://evil.test"}],
        [{**ref, "provider": "vimeo"}],
        [{"provider": "youtube", "video_id": f"abcdefghij{i}"} for i in range(6)],
    ):
        with pytest.raises(ValidationError):
            PostInput.model_validate({"video_refs": refs})


def guide_fixture(**changes: Any) -> HotspotGuide:
    now = datetime.now(UTC)
    return HotspotGuide(
        **{
            "hotspot_id": uuid4(),
            "content_type": "video",
            "provider": "youtube",
            "locale": "zh-TW",
            "title": "Reviewed source",
            "creator_name": "Creator",
            "canonical_url": f"https://www.youtube.com/watch?v={VIDEO}",
            "provider_content_id": VIDEO,
            "review_status": "approved",
            "last_verified_at": now - timedelta(hours=1),
            "metadata_expires_at": now + timedelta(days=20),
            "metadata_json": {"youtube_status": {"embeddable": True, "privacyStatus": "public"}},
            **changes,
        }
    )


@pytest.mark.parametrize(
    "changes",
    [
        {"review_status": "pending"},
        {"provider": "manual"},
        {"content_type": "article"},
        {"canonical_url": "https://evil.test/watch?v=" + VIDEO},
        {"canonical_url": "https://www.youtube.com/watch?v=" + OTHER_VIDEO},
        {"metadata_json": {"embeddable": True}},
        {"metadata_json": {"youtube_status": {"embeddable": "true", "privacyStatus": "public"}}},
        {"metadata_json": {"youtube_status": {"embeddable": False, "privacyStatus": "public"}}},
        {"metadata_json": {"youtube_status": {"embeddable": True, "privacyStatus": "private"}}},
        {"metadata_expires_at": datetime(2000, 1, 1, tzinfo=UTC)},
        {"last_verified_at": datetime(2000, 1, 1, tzinfo=UTC)},
        {"last_verified_at": datetime(2100, 1, 1, tzinfo=UTC)},
        {"last_verified_at": None},
    ],
)
def test_video_embed_requires_current_explicit_provider_proof(changes: dict[str, Any]) -> None:
    result = youtube_embed_metadata(guide_fixture(**changes))
    assert result["status"] == "link_only" and result["embed_url"] is None


def test_video_verified_embed_uses_privacy_host_and_canonical_source() -> None:
    result = youtube_embed_metadata(guide_fixture())
    assert result["status"] == "embeddable" and result["metadata_status"] == "verified"
    assert result["embed_url"] == f"https://www.youtube-nocookie.com/embed/{VIDEO}"
    assert youtube_source_id(f"https://youtu.be/{VIDEO}") == VIDEO
    assert youtube_source_id(f"https://www.youtube.com/shorts/{VIDEO}") == VIDEO
    for source in (
        f"https://www.youtube.com@evil.test/watch?v={VIDEO}",
        f"https://www.youtube.com:443/watch?v={VIDEO}",
        f"https://www.youtube.com/watch?v={VIDEO}&v={OTHER_VIDEO}",
    ):
        assert youtube_source_id(source) is None


async def invite(
    h: Harness, *, actor: int = 0, version: int = 0, invited: bool = True
) -> dict[str, Any]:
    return (
        await h.call(
            "PUT",
            f"/admin/community/creator-invitations/{h.ids[actor]}",
            actor=2,
            json={"version": version, "invited": invited, "reason": "Creator checked"},
        )
    ).json()


@pytest.mark.asyncio
async def test_creator_invitation_capability_version_audit_and_publish_gate(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = harness
    monkeypatch.setattr(get_settings(), "discovery_enabled", True)
    lookup = f"/admin/community/creator-invitations?user_id={h.ids[0]}"
    await h.call("GET", lookup, actor=0, expected=403)
    await h.call("GET", lookup, actor=None, expected=401)
    state = (await h.call("GET", lookup, actor=2)).json()["items"][0]
    assert state["version"] == 0 and not state["invited"] and "email" not in state
    me = (await h.call("GET", "/community/me")).json()
    assert me["invitation_required"] and not me["can_publish"]
    draft = await h.post()
    await h.call(
        "POST",
        f"/community/posts/{draft['id']}/publish",
        expected=403,
        json={"version": draft["version"]},
    )
    granted = await invite(h)
    assert granted["version"] == 1 and granted["invited"]
    assert (await h.call("GET", "/community/me")).json()["can_publish"]
    await h.call(
        "PUT",
        f"/admin/community/creator-invitations/{h.ids[0]}",
        actor=2,
        expected=409,
        json={"version": 0, "invited": False, "reason": "Stale browser"},
    )
    pending = await h.publish(draft)
    assert pending["state"] == "pending"  # Invitation does not bypass first-post moderation.
    await invite(h, version=1, invited=False)
    await h.call(
        "PUT",
        f"/admin/community/posts/{draft['id']}",
        actor=2,
        expected=403,
        json={"version": pending["version"], "action": "approve", "reason": "Recheck"},
    )
    await invite(h, version=2)
    approved = await h.approve(pending)
    assert approved["state"] == "published"
    await invite(h, version=3, invited=False)
    await h.call(
        "GET", f"/community/posts/{draft['id']}", actor=None
    )  # Revocation is not takedown.
    async with h.factory() as session:
        logs = (
            await session.scalars(
                select(AdminAuditLog).where(AdminAuditLog.action == "community_creator_invitation")
            )
        ).all()
        assert len(logs) == 4 and all(row.actor_user_id == h.ids[2] for row in logs)


@pytest.mark.asyncio
async def test_rollout_off_keeps_existing_publishing_and_video_snapshots_need_review(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = harness
    request = AsyncMock(side_effect=AssertionError("Provider calls must not run"))
    monkeypatch.setattr("httpx.AsyncClient.get", request)
    async with h.factory() as session:
        profile = await session.get(Profile, h.ids[0])
        assert profile
        profile.approved_posts = 5
        await session.commit()
    draft = await h.post(video_refs=[{"provider": "youtube", "video_id": VIDEO}])
    assert draft["video_refs"][0]["status"] == "link_only"
    pending = await h.publish(draft)
    assert pending["state"] == "pending"  # New external video still needs review.
    approved = await h.approve(pending)
    edited = (
        await h.call(
            "PUT",
            f"/community/posts/{draft['id']}",
            json={
                "version": approved["version"],
                "title": "Edited",
                "body": "Still original text",
                "destination": "Tokyo",
                "video_refs": [{"provider": "youtube", "video_id": OTHER_VIDEO}],
            },
        )
    ).json()
    public = (await h.call("GET", f"/community/posts/{draft['id']}", actor=None)).json()
    assert public["video_refs"][0]["video_id"] == VIDEO
    second = await h.publish(edited)
    assert second["pending_revision_id"]
    public = (await h.call("GET", f"/community/posts/{draft['id']}", actor=None)).json()
    assert public["video_refs"][0]["video_id"] == VIDEO
    ordinary = await h.publish(await h.post(title="No videos"))
    assert ordinary["state"] == "published"
    assert not (await h.call("GET", "/community/me")).json()["invitation_required"]
    request.assert_not_awaited()


@pytest.mark.asyncio
async def test_public_media_refs_preserve_reviewed_order_and_exclude_removed_images(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    h = harness
    storage = Mock(side_effect=AssertionError("Metadata must not access image storage"))
    monkeypatch.setattr("app.community.media.storage", storage)
    identifiers = [uuid4() for _ in range(5)]
    first, second, removed, missing, draft_only = identifiers
    async with h.factory() as session:
        session.add_all(
            Media(
                id=identifier,
                owner_id=h.ids[0],
                object_key=f"private/{identifier}/full",
                thumbnail_key=f"private/{identifier}/thumbnail",
                width=800,
                height=600,
                size=1024,
                alt=f"Reviewed photograph {index}",
            )
            for index, identifier in enumerate(identifiers)
        )
        await session.commit()
    draft = await h.post(media_ids=[str(value) for value in [second, removed, first, missing]])
    approved = await h.approve(await h.publish(draft))
    await h.call(
        "PUT",
        f"/community/posts/{draft['id']}",
        json={
            "version": approved["version"],
            "title": "Unreviewed replacement",
            "body": "A new draft photograph must not replace the approved images.",
            "media_ids": [str(draft_only)],
        },
    )
    async with h.factory() as session:
        await session.execute(
            update(Media).where(Media.id == removed).values(deleted_at=datetime.now(UTC))
        )
        await session.execute(delete(Media).where(Media.id == missing))
        await session.commit()
        post, revision, profile = await published_post(session, UUID(draft["id"]), None)
        refs = await public_media_refs(session, revision)
        assert refs == [
            {"id": str(second), "alt": "Reviewed photograph 1", "width": 800, "height": 600},
            {"id": str(first), "alt": "Reviewed photograph 0", "width": 800, "height": 600},
        ]
        assert (await serialize_post(session, post, revision, profile))["media"] == refs
    public = (await h.call("GET", f"/community/posts/{draft['id']}", actor=None)).json()
    assert public["media"] == refs
    storage.assert_not_called()


@pytest.mark.asyncio
async def test_public_media_refs_empty_revision_needs_no_query() -> None:
    session = AsyncMock()
    assert await public_media_refs(session, PostRevision(media_ids=[])) == []
    session.scalars.assert_not_awaited()


@pytest.mark.asyncio
async def test_invitation_never_bypasses_verification_restriction_or_deleted_account(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = harness
    monkeypatch.setattr(get_settings(), "discovery_enabled", True)
    await invite(h, actor=3)
    me = (await h.call("GET", "/community/me", actor=3)).json()
    assert me["creator_invited"] and not me["can_publish"]
    await h.call(
        "POST",
        "/community/posts",
        actor=3,
        expected=403,
        json={"title": "Not verified", "body": "Draft", "destination": "Tokyo"},
    )
    draft = await h.post()
    await invite(h)
    async with h.factory() as session:
        await session.execute(
            update(Profile).where(Profile.user_id == h.ids[0]).values(restricted=True)
        )
        await session.commit()
    await h.call(
        "POST",
        f"/community/posts/{draft['id']}/publish",
        expected=403,
        json={"version": draft["version"]},
    )
    async with h.factory() as session:
        await session.execute(
            update(User)
            .where(User.id == h.ids[0])
            .values(is_active=False, deleted_at=datetime.now(UTC))
        )
        await session.commit()
    await h.call(
        "PUT",
        f"/admin/community/creator-invitations/{h.ids[0]}",
        actor=2,
        expected=404,
        json={"version": 1, "invited": True, "reason": "Must not restore deleted account"},
    )
    await h.call(
        "PUT",
        f"/admin/community/creator-invitations/{uuid4()}",
        actor=2,
        expected=404,
        json={"version": 0, "invited": True, "reason": "Unknown account"},
    )


@pytest.mark.asyncio
async def test_existing_community_collection_reuses_reviewed_hotel_reference_gates(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = harness
    monkeypatch.setattr(get_settings(), "discovery_enabled", True)
    async with h.factory() as session:
        session.add(
            TravelServiceConfig(
                id=1,
                data={
                    "public_enabled": True,
                    "enabled_kinds": ["hotel"],
                    "enabled_destinations": ["tokyo"],
                },
            )
        )
        product = TravelServiceProduct(
            source_key="test:discovery:hotel",
            kind="hotel",
            destination_id="tokyo",
            title="Reviewed Tokyo hotel",
            source_url="https://example.org/hotel",
            status="pending",
            verified_at=datetime.now(UTC),
        )
        session.add(product)
        await session.commit()
        hotel_id = product.id
    collection = (
        await h.call(
            "POST", "/community/collections", expected=201, json={"name": "Reviewed stays"}
        )
    ).json()
    path = f"/community/collections/{collection['id']}/items"
    await h.call("PUT", path, expected=404, json={"kind": "hotel", "target": str(hotel_id)})
    async with h.factory() as session:
        await session.execute(
            update(TravelServiceProduct)
            .where(TravelServiceProduct.id == hotel_id)
            .values(status="approved")
        )
        await session.commit()
    await h.call("PUT", path, json={"kind": "hotel", "target": str(hotel_id)})
    await h.call("PUT", path, json={"kind": "hotel", "target": hotel_id.hex})
    rows = (await h.call("GET", path)).json()["items"]
    assert len(rows) == 1 and rows[0]["discovery"]["kind"] == "hotel"
    assert "price" not in rows[0]["discovery"]
    async with h.factory() as session:
        await session.execute(
            update(TravelServiceProduct)
            .where(TravelServiceProduct.id == hotel_id)
            .values(verified_at=datetime(2000, 1, 1, tzinfo=UTC))
        )
        await session.commit()
    unavailable = (await h.call("GET", path)).json()["items"][0]
    assert unavailable["unavailable"] and "discovery" not in unavailable
    await h.call("GET", path, actor=1, expected=404)
    await h.call("PUT", path, expected=422, json={"kind": "hotel", "target": "arbitrary URL"})
    await h.call("DELETE", path + "/" + unavailable["id"])


async def catalog_guide(h: Harness, **changes: Any) -> UUID:
    async with h.factory() as session:
        hotspot = TravelHotspot(
            slug="discovery-" + uuid4().hex,
            name="Tokyo Garden",
            city_code="TYO",
            city_name="Tokyo",
            destination_id="tokyo",
            country_code="JP",
            country_name="Japan",
            category="park",
            search_text="garden",
            review_status="approved",
        )
        session.add(hotspot)
        await session.flush()
        guide = guide_fixture(hotspot_id=hotspot.id, **changes)
        session.add(guide)
        await session.commit()
        return guide.id


@pytest.mark.asyncio
async def test_public_video_cache_rechecks_parent_and_never_fetches(harness: Harness) -> None:
    identifier = await catalog_guide(harness)
    refs = [{"provider": "youtube", "video_id": VIDEO}]
    async with harness.factory() as session:
        assert (await public_video_refs(session, refs))[0]["status"] == "embeddable"
        guide = await session.get(HotspotGuide, identifier)
        assert guide
        await session.execute(
            update(TravelHotspot)
            .where(TravelHotspot.id == guide.hotspot_id)
            .values(review_status="rejected")
        )
        assert (await public_video_refs(session, refs))[0]["status"] == "link_only"


@pytest.mark.asyncio
async def test_private_discovery_collections_need_account_not_social_profile_and_reauthorize(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = harness
    monkeypatch.setattr(get_settings(), "discovery_enabled", True)
    guide_id = await catalog_guide(
        h,
        content_type="article",
        provider="manual",
        canonical_url="https://example.org/approved-guide",
    )
    recorded = AsyncMock(return_value=True)
    monkeypatch.setattr("app.analytics.service.record_event", recorded)
    async with h.factory() as session:
        user, other = await session.get(User, h.ids[0]), await session.get(User, h.ids[1])
        assert user and other
        user.email_verified_at = None
        await session.execute(delete(Profile).where(Profile.user_id == user.id))
        config = await session.scalar(
            select(ProviderConfig).where(ProviderConfig.provider == "community")
        )
        assert config
        config.config = {"enabled": False}
        await session.commit()
        collection = await private_collections.create_collection(session, user, "Japan ideas")
        identifier = UUID(collection["id"])
        first = await private_collections.collect_reference(
            session, user, identifier, "guide", str(guide_id)
        )
        replay = await private_collections.collect_reference(
            session, user, identifier, "guide", guide_id.hex
        )
        assert first["created"] and not replay["created"]
        assert recorded.await_count == 1
        listed = await private_collections.collection_items(session, user, identifier, "zh-TW")
        assert listed["items"][0]["discovery"]["kind"] == "article"
        with pytest.raises(AppError) as denied:
            await private_collections.collection_items(session, other, identifier, "zh-TW")
        assert denied.value.status == 404
        await session.execute(
            update(HotspotGuide).where(HotspotGuide.id == guide_id).values(review_status="rejected")
        )
        await session.commit()
        stale = await private_collections.collection_items(session, user, identifier, "zh-TW")
        assert stale["items"][0]["unavailable"] and "discovery" not in stale["items"][0]
        await private_collections.remove_reference(
            session, user, identifier, UUID(stale["items"][0]["id"])
        )
        assert not (await private_collections.collection_items(session, user, identifier, "zh-TW"))[
            "items"
        ]
    await h.call("GET", "/community/feed", expected=403)


@pytest.mark.asyncio
async def test_discovery_candidates_following_locale_blocks_and_cached_withdrawal(
    harness: Harness,
) -> None:
    h = harness
    post = await h.post(topics=["nature"])
    await h.approve(await h.publish(post))
    async with h.factory() as session:
        viewer = await session.get(User, h.ids[1])
        assert viewer
        assert not await community_public_candidates(
            session, viewer, "", [], [], following_only=True
        )
        session.add(Relationship(actor_id=viewer.id, target_id=h.ids[0], kind="follow"))
        await session.commit()
        rows = await community_public_candidates(
            session,
            viewer,
            "Tokyo",
            ["tokyo"],
            ["nature"],
            limit=1,
            following_only=True,
            locale="zh-TW",
        )
        assert len(rows) == 1 and str(rows[0][0].id) == post["id"]
        assert not await community_public_candidates(session, viewer, "", [], [], locale="en")
        session.add(Relationship(actor_id=h.ids[0], target_id=viewer.id, kind="block"))
        await session.flush()
        assert not await community_public_candidates(session, viewer, "", [], [])
        await session.execute(
            update(Post)
            .where(Post.id == UUID(post["id"]))
            .values(state="draft", published_revision_id=None),
            execution_options={"synchronize_session": False},
        )
        with pytest.raises(AppError) as unavailable:
            await published_post(session, UUID(post["id"]), None)
        assert unavailable.value.status == 404


@pytest.mark.asyncio
async def test_legacy_collection_kinds_do_not_break_discovery_collection(harness: Harness) -> None:
    async with harness.factory() as session:
        user = await session.get(User, harness.ids[0])
        assert user
        collection = await private_collections.create_collection(
            session, user, "Existing collection"
        )
        identifier = UUID(collection["id"])
        session.add_all(
            [
                CollectionItem(collection_id=identifier, kind="pet_place", target=str(uuid4())),
                CollectionItem(
                    collection_id=identifier, kind="restaurant", target="legacy:provider-id"
                ),
            ]
        )
        await session.commit()
        response = await private_collections.collection_items(session, user, identifier, "zh-TW")
        assert len(response["items"]) == 2 and all(
            item["unavailable"] for item in response["items"]
        )
        await private_collections.remove_reference(
            session, user, identifier, UUID(response["items"][0]["id"])
        )
        assert (
            len(
                (await private_collections.collection_items(session, user, identifier, "zh-TW"))[
                    "items"
                ]
            )
            == 1
        )


@pytest.mark.asyncio
async def test_discovery_post_search_matches_destination_alias_without_title_keyword(
    harness: Harness,
) -> None:
    post = await harness.post(title="Weekend notes", body="A peaceful walk", destination="Tokyo")
    await harness.approve(await harness.publish(post))
    async with harness.factory() as session:
        for query in ("東京", "tokyo"):
            matches = await community_public_candidates(session, None, query, [], [], limit=1)
            assert len(matches) == 1 and str(matches[0][0].id) == post["id"]
        assert not await community_public_candidates(session, None, "Osaka", [], [])


@pytest.mark.asyncio
async def test_publish_analytics_only_records_new_public_revision(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    recorded = AsyncMock(return_value=True)
    monkeypatch.setattr("app.analytics.service.record_event", recorded)
    post = await harness.post()
    pending = await harness.publish(post)
    recorded.assert_not_awaited()
    approved = await harness.approve(pending)
    assert recorded.await_count == 1
    args = recorded.await_args
    assert args and args.args[1] == "post_published"
    assert args.kwargs["path"] == "/community"
    assert args.kwargs["user_id"] == harness.ids[2]
    assert args.kwargs["properties"] == {"kind": "story", "publication_source": "moderator"}
    async with harness.factory() as session:
        await session.execute(
            update(Profile).where(Profile.user_id == harness.ids[0]).values(approved_posts=5)
        )
        await session.commit()
    await harness.call(
        "POST", f"/community/posts/{post['id']}/publish", json={"version": approved["version"]}
    )
    assert recorded.await_count == 1
    authored = await harness.publish(await harness.post(title="Author-published story"))
    assert authored["state"] == "published"
    assert recorded.await_count == 2
    args = recorded.await_args
    assert args and args.args[1] == "post_published"
    assert args.kwargs["user_id"] == harness.ids[0]
    assert args.kwargs["properties"] == {"kind": "story", "publication_source": "author"}
    await harness.publish(authored)
    assert recorded.await_count == 2


@pytest.mark.asyncio
async def test_collection_replay_canonicalizes_legacy_post_uuid_without_overwrite(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = harness
    post = await h.post()
    await h.approve(await h.publish(post))
    monkeypatch.setattr(get_settings(), "discovery_enabled", True)
    recorded = AsyncMock(return_value=True)
    monkeypatch.setattr("app.analytics.service.record_event", recorded)
    async with h.factory() as session:
        user = await session.get(User, h.ids[0])
        assert user
        collection = await private_collections.create_collection(session, user, "Legacy UUID")
        identifier = UUID(collection["id"])
        legacy = CollectionItem(
            collection_id=identifier, kind="post", target=UUID(post["id"]).hex.upper()
        )
        session.add(legacy)
        await session.commit()
        saved = await private_collections.collect_reference(
            session, user, identifier, "post", post["id"]
        )
        assert not saved["created"] and legacy.target == UUID(post["id"]).hex.upper()
        assert await session.scalar(select(func.count()).select_from(CollectionItem)) == 1
    await h.call(
        "PUT",
        f"/community/collections/{identifier}/items",
        json={"kind": "post", "target": post["id"]},
    )
    recorded.assert_not_awaited()
    async with h.factory() as session:
        assert await session.scalar(select(func.count()).select_from(CollectionItem)) == 1


@pytest.mark.asyncio
async def test_discovery_post_kind_filter_precedes_limit_for_json_and_sql_null(
    harness: Harness,
) -> None:
    h = harness
    itinerary = await h.post(title="Earlier itinerary")
    async with h.factory() as session:
        revision = await session.get(PostRevision, UUID(itinerary["revision_id"]))
        assert revision
        revision.itinerary = {"destination": "Tokyo", "days": 1, "stops": []}
        await session.commit()
    await h.approve(await h.publish(itinerary))
    ordinary = await h.post(title="Latest story")
    await h.approve(await h.publish(ordinary))
    async with h.factory() as session:
        routes = await community_public_candidates(
            session, None, "", [], [], limit=1, itinerary_only=True
        )
        assert len(routes) == 1 and str(routes[0][0].id) == itinerary["id"]
        stories = await community_public_candidates(
            session, None, "", [], [], limit=1, itinerary_only=False
        )
        assert len(stories) == 1 and str(stories[0][0].id) == ordinary["id"]
        await session.execute(
            update(PostRevision)
            .where(PostRevision.id == UUID(ordinary["revision_id"]))
            .values(itinerary=null())
        )
        stories = await community_public_candidates(
            session, None, "", [], [], limit=1, itinerary_only=False
        )
        assert len(stories) == 1 and str(stories[0][0].id) == ordinary["id"]


@pytest.mark.asyncio
async def test_erasure_removes_discovery_preferences_invites_and_video_refs(
    harness: Harness,
) -> None:
    h = harness
    draft = await h.post(video_refs=[{"provider": "youtube", "video_id": VIDEO}])
    await invite(h)
    async with h.factory() as session:
        user = await session.get(User, h.ids[0])
        assert user
        session.add(DiscoveryPreference(user_id=user.id, destinations=["tokyo"], topics=[]))
        session.add(DiscoveryDismissal(user_id=user.id, content_key="post:" + draft["id"]))
        user.deleted_at = datetime.now(UTC)
        user.is_active = False
        await session.flush()
        await erase_account(session, user.id)
        await session.commit()
        assert await session.get(CreatorInvitation, user.id) is None
        assert await session.get(DiscoveryPreference, user.id) is None
        assert not await session.scalar(select(func.count()).select_from(DiscoveryDismissal))
        revision = await session.get(PostRevision, UUID(draft["revision_id"]))
        assert revision and revision.video_refs == [] and revision.place_refs == []


@pytest.mark.asyncio
@pytest.mark.parametrize("legacy", [False, True])
async def test_discovery_community_migration_fresh_and_legacy_idempotent(
    harness: Harness,
    legacy: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from alembic import context
    from alembic.migration import MigrationContext
    from alembic.operations import Operations

    module = runpy.run_path(
        str(Path(__file__).parents[1] / "migrations" / "versions" / "0066_discovery_community.py")
    )
    assert module["down_revision"] == "0065_travel_discovery"
    monkeypatch.setattr(context, "is_offline_mode", lambda: False)

    def verify(connection: Any) -> None:
        module["upgrade"].__globals__["op"] = Operations(MigrationContext.configure(connection))
        if legacy:
            module["downgrade"]()
        module["upgrade"]()
        module["upgrade"]()
        assert "video_refs" in {
            c["name"] for c in inspect(connection).get_columns("community_post_revisions")
        }
        assert inspect(connection).has_table("community_creator_invitations")
        assert connection.scalar(select(func.count()).select_from(User)) == 4

    async with harness.factory() as session:
        connection = await session.connection()
        await connection.run_sync(verify)
        await session.commit()


@pytest.mark.asyncio
async def test_concurrent_first_invitation_has_one_winner_without_missing_row_race(
    harness: Harness,
) -> None:
    async with harness.factory() as session:
        if session.get_bind().dialect.name != "postgresql":
            pytest.skip("Row-lock concurrency is verified with PostgreSQL CI")
    path = f"/api/v1/admin/community/creator-invitations/{harness.ids[0]}"

    async def grant() -> int:
        response = await harness.client.put(
            path,
            headers={"x-test-user": str(harness.ids[2])},
            json={"version": 0, "invited": True, "reason": "Concurrent grant"},
        )
        return response.status_code

    statuses = await asyncio.wait_for(asyncio.gather(grant(), grant()), timeout=10)
    assert sorted(statuses) == [200, 409]
