"""Shorts the owner uploads by hand stay off the site's calendar (owner, 2026-11-21;
docs/videos/SHORTS.md §手動上架): no slot, nothing sent under the standing consent, no second
upload, and the Studio link can be recorded without an approved upload package.

The site is test_video_shorts_publish.py's: SQLite (PostgreSQL too where CI runs the integration
tests, for the JSON the rule reads and the locks), a real review store and a fake YouTube.
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from sqlalchemy import select

from app.models import VideoProject, VideoReview, VideoToolToken
from app.video_automation.models import VideoDramaEpisode, VideoDramaRequest
from app.video_reviews import admin_service
from app.video_reviews.schemas import DecisionIn, ReviewFile, ReviewIn
from app.video_shorts import claim, hand_upload, overview, slots
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.schemas import SlotPatch
from app.video_youtube import sync, vps, vps_settings
from app.video_youtube.errors import Refused
from app.video_youtube.schemas import PublishIn
from app.video_youtube.state import new_state
from tests.test_video_shorts_publish import (
    HOURS,
    VIDEO,
    ShortsSite,
    agree,
    change,
    open_shorts_site,
    project_of,
    ready,
    request_for,
    send,
    short,
    slot,
    slot_of,
    ticked,
)

SLUG = "receipt"


@pytest.fixture(
    params=["sqlite"] + (["postgresql"] if os.getenv("RUN_INTEGRATION_TESTS") == "1" else [])
)
async def site(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> AsyncIterator[ShortsSite]:
    async with open_shorts_site(monkeypatch, tmp_path, request.param) as value:
        async with value.factory() as session:
            # An approval asks whether the video is an episode of a drama series. PostgreSQL wants
            # the table an episode's foreign key points at; SQLite would not notice.
            db = await session.connection()
            await db.run_sync(
                VideoDramaEpisode.metadata.create_all,
                [VideoDramaRequest.__table__, VideoDramaEpisode.__table__],
            )
            await session.commit()
        yield value


@pytest.fixture
def now() -> datetime:
    return datetime.now(UTC).replace(microsecond=0)


async def reviews_of(site: ShortsSite, slug: str = SLUG) -> dict[str, VideoReview]:
    project = await project_of(site, slug)
    async with site.factory() as session:
        rows = await session.scalars(
            select(VideoReview).where(VideoReview.project_id == project.id)
        )
        return {row.gate: row for row in rows}


async def edit_review(site: ShortsSite, gate: str, slug: str = SLUG, **fields: Any) -> None:
    review = (await reviews_of(site, slug))[gate]
    async with site.factory() as session:
        row = await session.get(VideoReview, review.id)
        assert row is not None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.commit()


async def push_by_hand(site: ShortsSite, slug: str = SLUG, gate: str = "final") -> None:
    payload = (await reviews_of(site, slug))[gate].payload
    await edit_review(site, gate, slug, payload={**payload, "hand_pushed": True})


async def without_package(site: ShortsSite, status: str = "superseded") -> None:
    """The cut is approved and no upload package is, as of an hour ago."""
    await edit_review(
        site, "publish", status=status, decided_at=None, updated_at=datetime.now(UTC) - HOURS
    )


async def link(site: ShortsSite, publish_at: datetime | None = None) -> Any:
    async with site.factory() as session:
        return await admin_service.link_youtube(session, SLUG, site.owner, VIDEO, publish_at)


async def is_by_hand(site: ShortsSite, slug: str = SLUG) -> bool:
    project = await project_of(site, slug)
    async with site.factory() as session:
        return await hand_upload.is_hand_uploaded(session, project)


async def freed(site: ShortsSite, held: UUID) -> bool:
    row = await slot_of(site, held)
    return row.status == "open" and row.project_slug is None


async def test_a_hand_pushed_short_pushed_again_gets_a_package_and_no_slot(
    site: ShortsSite, now: datetime
) -> None:
    await short(site, SLUG)
    stored = await reviews_of(site)
    final, package = stored["final"], stored["publish"]
    payload = {**final.payload, "hand_pushed": True}
    await edit_review(site, "final", payload=payload)
    async with site.factory() as session:
        old = await session.get(VideoReview, package.id)
        assert old is not None
        await session.delete(old)
        token = VideoToolToken(name="tool", token_hash="h" * 64, token_prefix="mkv_test")
        session.add(token)
        await session.commit()
    ahead = await slot(site, now + 30 * HOURS)

    async def push(gate: str, sha: str, body: dict[str, Any], files: list[dict[str, Any]]) -> Any:
        async with site.factory() as session:
            return await admin_service.submit_review(
                session,
                site.store,
                SLUG,
                ReviewIn(
                    gate=gate,  # type: ignore[arg-type]
                    content_sha256=sha,
                    summary=gate,
                    payload=body,
                    files=[ReviewFile(**item) for item in files],
                ),
                token,
            )

    again = await push("final", final.content_sha256, payload, [*final.files, package.files[0]])
    assert (again.id, again.status) == (final.id, "approved")
    assert "metadata" not in [file.role for file in again.files], "what was approved stays"

    sent = await push(
        "publish",
        package.content_sha256,
        {**package.payload, "final_review_id": str(final.id), "hand_pushed": True},
        package.files,
    )
    assert sent.status == "pending"
    assert "metadata" in [file.role for file in sent.files], "the page reads the package here"

    async with site.factory() as session:
        decided = await admin_service.decide(
            session, SLUG, sent.id, site.owner, DecisionIn(decision="approve")
        )
    assert decided.status == "approved"
    assert await freed(site, ahead), "an approved package of a hand upload takes no slot"


async def test_approving_the_package_gives_back_the_slot_a_hand_upload_held(
    site: ShortsSite, now: datetime
) -> None:
    await short(site, SLUG)
    await push_by_hand(site)
    await edit_review(site, "publish", status="pending", decided_at=None)
    held = await slot(site, now + 30 * HOURS, SLUG, "assigned")
    package = (await reviews_of(site))["publish"]
    async with site.factory() as session:
        await admin_service.decide(
            session, SLUG, package.id, site.owner, DecisionIn(decision="approve")
        )
    assert await freed(site, held)


@pytest.mark.parametrize("gate", ["final", "publish"])
@pytest.mark.parametrize("status", ["pending", "approved"])
async def test_a_live_review_pushed_by_hand_makes_a_hand_upload(
    site: ShortsSite, gate: str, status: str
) -> None:
    await short(site, SLUG)
    await push_by_hand(site, gate=gate)
    await edit_review(site, gate, status=status)
    assert await is_by_hand(site)


@pytest.mark.parametrize(
    ("status", "mark"),
    [
        ("superseded", True),
        ("rejected", True),
        ("approved", "true"),
        ("approved", 1),
        ("approved", False),
        ("approved", None),
    ],
)
async def test_only_a_live_review_s_true_counts(
    site: ShortsSite, status: str, mark: object
) -> None:
    await short(site, SLUG)
    await edit_review(site, "final", status=status, payload={"hand_pushed": mark})
    assert not await is_by_hand(site)


async def test_the_calendar_takes_no_hand_upload_from_the_library(
    site: ShortsSite, now: datetime
) -> None:
    await site.link()
    await agree(site, now)
    # Uploaded and earliest: before the API audit this is the one the library would give first.
    await short(site, SLUG, video_id=VIDEO, approved=timedelta(minutes=-5))
    await push_by_hand(site)
    site.youtube.put(VIDEO)
    await short(site, "spare")
    due = await slot(site, now + 20 * HOURS)

    await ticked(site, now)

    assert (await slot_of(site, due)).project_slug == "spare"
    assert site.launched == []


async def test_a_knock_gives_back_every_slot_a_hand_upload_held_before_it_was_one(
    site: ShortsSite, now: datetime
) -> None:
    locked = await ready(site, now)
    await push_by_hand(site)
    await short(site, "later")
    await push_by_hand(site, "later")
    assigned = await slot(site, now + 200 * HOURS, "later", "assigned")

    answer = await ticked(site, now)

    assert answer.sent == 0 and site.launched == []
    assert await freed(site, assigned), "however far ahead"
    row = await slot_of(site, locked)
    assert (row.status, row.project_slug) == ("missed", None), "due, and the library is empty"


async def test_a_new_run_counts_and_takes_no_hand_upload(site: ShortsSite, now: datetime) -> None:
    await short(site, SLUG, approved=timedelta(minutes=-5))
    await push_by_hand(site)
    await short(site, "spare")
    async with site.factory() as session:
        assert (await overview.overview(session, now)).stock.count == 1
    async with site.factory() as session:
        started = await slots.start_campaign(
            session, site.owner, (now + timedelta(days=3)).date(), now
        )
        held = await slots.holds(session, [SLUG, "spare"])
    assert started.assigned == 1 and list(held) == ["spare"]


async def test_the_owner_cannot_put_a_hand_upload_on_the_calendar(
    site: ShortsSite, now: datetime
) -> None:
    await short(site, SLUG)
    await push_by_hand(site)
    ahead = await slot(site, now + 30 * HOURS)
    async with site.factory() as session:
        with pytest.raises(ShortsRefused) as refused:
            await slots.patch_slot(
                session, site.owner, ahead, SlotPatch(action="assign", project_slug=SLUG), now
            )
    assert refused.value.code == "video_shorts_hand_upload"


async def test_a_hand_upload_is_not_among_the_files_the_site_waits_to_claim(
    site: ShortsSite, now: datetime
) -> None:
    await site.link()
    await short(site, SLUG)
    await push_by_hand(site)
    await slot(site, now + 20 * HOURS, SLUG, "assigned")
    async with site.factory() as session:
        assert (await claim.uploads_view(session, now)).items == []
        assert "upload" not in [need.kind for need in (await overview.overview(session, now)).needs]


@pytest.mark.parametrize("package", ["none", "waiting"])
async def test_the_studio_link_is_recorded_without_an_approved_package(
    site: ShortsSite, now: datetime, package: str
) -> None:
    await site.link()
    await agree(site, now)
    await short(site, SLUG)
    await without_package(site, "pending" if package == "waiting" else "superseded")
    site.youtube.put(VIDEO)
    held = await slot(site, now + 20 * HOURS, SLUG, "assigned")

    view = await link(site)

    assert (view.youtube_video_id, view.youtube_publish_at) == (VIDEO, None)
    assert await is_by_hand(site), "from the link's commit"
    assert (await send(site, now)).sent == 0

    # A package approved afterwards does not bring it back to the calendar.
    await edit_review(site, "publish", status="approved", decided_at=datetime.now(UTC))
    await ticked(site, now)
    assert site.launched == [] and site.google.updates == []
    project = await project_of(site)
    assert project.youtube_sync is None and project.youtube_publish_at is None
    assert (await slot_of(site, held)).project_slug is None


async def test_the_publish_time_can_be_recorded_afterwards(site: ShortsSite, now: datetime) -> None:
    await site.link()
    await short(site, SLUG)
    await without_package(site)
    site.youtube.put(VIDEO)
    await link(site)

    view = await link(site, now + 48 * HOURS)

    assert view.youtube_publish_at == now + 48 * HOURS
    assert view.shorts_state == "scheduled"
    assert await is_by_hand(site)


async def test_a_hand_pushed_short_with_an_approved_package_is_linked_as_one(
    site: ShortsSite, now: datetime
) -> None:
    await short(site, SLUG)
    await push_by_hand(site)
    held = await slot(site, now + 20 * HOURS, SLUG, "locked")
    await link(site, now + 48 * HOURS)
    assert await is_by_hand(site)
    await ticked(site, now)
    assert (await slot_of(site, held)).project_slug is None


async def test_a_worker_s_short_linked_after_its_package_stays_on_the_site_s_route(
    site: ShortsSite, now: datetime
) -> None:
    await site.link()
    await agree(site, now)
    await short(site, SLUG)
    site.youtube.put(VIDEO)
    held = await slot(site, now + 20 * HOURS, SLUG, "locked")

    # The VPS uploader's "record" links this way too.
    await link(site)

    assert not await is_by_hand(site)
    assert (await slot_of(site, held)).project_slug == SLUG
    assert (await send(site, now)).sent == 1


async def test_a_run_queued_before_the_link_stops_before_it_writes(
    site: ShortsSite, now: datetime
) -> None:
    await ready(site, now)
    assert (await send(site, now)).sent == 1
    # The package is withdrawn, then the owner records their own upload.
    await without_package(site)
    await edit_review(site, "publish", updated_at=now - HOURS)
    await link(site, now + 48 * HOURS)

    await sync.run_sync(SLUG, site.factory)

    assert site.google.updates == []
    assert (await project_of(site)).youtube_publish_at == now + 48 * HOURS


async def test_a_corrected_link_stays_the_owner_s_after_the_package_is_approved(
    site: ShortsSite, now: datetime
) -> None:
    await short(site, SLUG)
    await without_package(site, "pending")
    await link(site, now + 48 * HOURS)
    await edit_review(site, "publish", status="approved", decided_at=datetime.now(UTC))
    async with site.factory() as session:
        await admin_service.link_youtube(session, SLUG, site.owner, "ShortVid002", now + 72 * HOURS)
    assert await is_by_hand(site)


async def test_an_unlink_ends_the_hand_upload(site: ShortsSite, now: datetime) -> None:
    await site.link()
    await short(site, SLUG)
    await without_package(site, "pending")
    site.youtube.put(VIDEO)
    await link(site)
    await edit_review(site, "publish", status="approved", decided_at=datetime.now(UTC))
    async with site.factory() as session:
        await admin_service.unlink_youtube(session, SLUG, site.owner)
    await link(site)
    assert not await is_by_hand(site)


async def test_a_package_replaced_after_the_link_leaves_it_on_the_site_s_route(
    site: ShortsSite, now: datetime
) -> None:
    await short(site, SLUG)
    await link(site, now + 48 * HOURS)
    await edit_review(site, "publish", status="superseded", updated_at=now + HOURS)
    assert not await is_by_hand(site)


async def test_a_locked_slot_that_still_holds_a_hand_upload_is_not_sent(
    site: ShortsSite, now: datetime
) -> None:
    held = await ready(site, now)
    await push_by_hand(site)
    sent = await send(site, now)
    assert (sent.sent, sent.held) == (0, 1)
    assert (await slot_of(site, held)).note == hand_upload.NOT_SENT
    assert site.launched == []


@pytest.mark.parametrize("again", [False, True], ids=["request", "retry"])
async def test_the_standing_consent_is_refused_under_the_project_s_lock(
    site: ShortsSite, now: datetime, again: bool
) -> None:
    await ready(site, now)
    await push_by_hand(site)
    behalf = {"auto": True, "consent_id": None}
    if again:
        failed = {**new_state(request_for(now + 20 * HOURS)), "status": "failed"}
        await change(site, SLUG, youtube_sync=failed)
    async with site.factory() as session:
        with pytest.raises(Refused) as refused:
            if again:
                await sync.retry_sync(session, SLUG, site.owner, on_behalf=behalf)
            else:
                await sync.request_sync(
                    session,
                    site.store,
                    SLUG,
                    site.owner,
                    PublishIn(
                        mode="studio",
                        url=VIDEO,
                        visibility="scheduled",
                        publish_at=now + 20 * HOURS,
                    ),
                    on_behalf=behalf,
                )
    assert refused.value.code == "video_youtube_hand_upload"
    assert site.launched == []


async def test_a_queued_automatic_run_stops_before_it_writes(
    site: ShortsSite, now: datetime
) -> None:
    await ready(site, now)
    assert (await send(site, now)).sent == 1
    await push_by_hand(site)

    await sync.run_sync(SLUG, site.factory)

    assert site.google.updates == []
    state = (await project_of(site)).youtube_sync
    assert state is not None and state["status"] == "failed"
    assert hand_upload.NOT_SENT in state["error"]


@pytest.mark.parametrize("again", [False, True], ids=["request", "retry"])
async def test_the_site_does_not_upload_a_second_copy(
    site: ShortsSite, now: datetime, again: bool
) -> None:
    await site.link()
    await short(site, SLUG)
    await push_by_hand(site)
    if again:
        request = {**request_for(now + 20 * HOURS), "mode": "upload", "video_id": None}
        await change(site, SLUG, youtube_sync={**new_state(request), "status": "failed"})
    async with site.factory() as session:
        with pytest.raises(Refused) as refused:
            if again:
                await sync.retry_sync(session, SLUG, site.owner)
            else:
                await sync.request_sync(
                    session,
                    site.store,
                    SLUG,
                    site.owner,
                    PublishIn(mode="upload", visibility="private", accept_private_lock=True),
                )
    assert refused.value.code == "video_youtube_hand_upload"
    assert site.launched == []


async def test_the_vps_does_not_upload_a_second_copy(
    site: ShortsSite, monkeypatch: pytest.MonkeyPatch
) -> None:
    await short(site, SLUG)
    await push_by_hand(site)
    settings = vps.Config("https://vps.test", "s" * 32, "UC" + "a" * 22)
    monkeypatch.setattr(vps_settings, "resolve", AsyncMock(return_value=settings))
    monkeypatch.setattr(vps, "load_runtime_settings", AsyncMock(return_value=site.settings))
    monkeypatch.setattr(vps, "latest", AsyncMock(return_value=None))
    remote = AsyncMock()
    monkeypatch.setattr(vps, "remote", remote)
    async with site.factory() as session:
        with pytest.raises(Refused) as refused:
            await vps.start(session, SLUG, site.owner, vps.StartIn())
    assert refused.value.code == "vps_hand_upload"
    remote.assert_not_awaited()


async def test_what_is_not_a_short_is_never_a_hand_upload(site: ShortsSite) -> None:
    await short(site, SLUG)
    await push_by_hand(site)
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        project.shorts_line = None
        assert await hand_upload.hand_uploaded(session, [project]) == frozenset()
