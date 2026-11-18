"""More than one linked YouTube channel (migration 0147; docs/videos/YOUTUBE-REPORTS.md §頻道).

The owner runs @Mokaair and 摩卡劇場 Mokaair. Each channel is a connection row with its own key
and grant; row 1 is "default" and holds the OAuth client the others sign in with. A video names
the channel it goes to, and the reports of a channel stay until that channel is unlinked.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select

from app.db import Base
from app.models import VideoProject, VideoYoutubeConnection
from app.video_reviews.admin_service import review_store
from app.video_youtube import connection, reports, sync
from app.video_youtube.client import refresh_access_token as real_refresh
from app.video_youtube.errors import Refused
from app.video_youtube.models import (
    VideoYoutubeReport,
    VideoYoutubeReportJob,
    VideoYoutubeReportState,
)
from app.video_youtube.schemas import OAuthExchangeIn, OAuthStartIn
from tests.test_video_youtube import BINDING, CHANNEL, Site, _app, open_site
from tests.test_video_youtube_sync import SLUG, STUDIO_ID, _package, _publish, _studio_video

THEATER = "UCtheaterchannel0000000"


@pytest.fixture
async def site(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> AsyncIterator[Site]:
    async with open_site(monkeypatch, tmp_path) as value:
        yield value


@pytest.fixture
def launched(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    started: list[str] = []
    monkeypatch.setattr(sync, "launch", started.append)
    return started


async def _link_theater(site: Site, *, channel: str = THEATER) -> None:
    """The second channel added and linked the way the card does it."""
    async with site.factory() as session:
        await connection.create_channel(session, site.owner, "theater", "摩卡劇場")
    site.google.channel = {"id": channel, "snippet": {"title": "摩卡劇場 Mokaair"}}
    site.google.issued_refresh_token = "refresh-2"
    async with site.factory() as session:
        started = await connection.start_link(
            session, site.owner, OAuthStartIn(browser_binding=BINDING), key="theater"
        )
    async with site.factory() as session:
        await connection.finish_link(
            session,
            site.owner,
            OAuthExchangeIn(
                flow_id=started.flow_id,
                state=started.state,
                code="the-code",
                browser_binding=BINDING,
            ),
        )


async def _rows(site: Site) -> dict[str, VideoYoutubeConnection]:
    async with site.factory() as session:
        rows = await connection.connections(session)
    return {connection.channel_key(row.key): row for row in rows}


async def test_a_second_channel_signs_in_with_the_default_client_and_keeps_its_own_grant(
    site: Site, monkeypatch: pytest.MonkeyPatch
) -> None:
    await site.link()
    await _link_theater(site)

    rows = await _rows(site)
    assert list(rows) == ["default", "theater"]
    assert rows["default"].channel_id == CHANNEL
    assert rows["theater"].channel_id == THEATER
    assert rows["theater"].label == "摩卡劇場"
    assert rows["theater"].client_id is None, "only row 1 keeps the OAuth client"
    assert connection.stored_secrets(rows["default"])["refresh_token"] == "refresh-1"
    assert connection.stored_secrets(rows["theater"]) == {"refresh_token": "refresh-2"}

    async with site.factory() as session:
        views = await connection.channel_views(session)
    assert [(view.key, view.channel_id, view.configured) for view in views] == [
        ("default", CHANNEL, True),
        ("theater", THEATER, True),
    ]

    used: list[str] = []

    async def watch(http: Any, *, client_id: str, client_secret: str, refresh_token: str) -> str:
        used.append(refresh_token)
        return await real_refresh(
            http, client_id=client_id, client_secret=client_secret, refresh_token=refresh_token
        )

    monkeypatch.setattr(connection, "refresh_access_token", watch)
    async with site.factory() as session, connection.http_client() as http:
        await connection.access_token(session, http, key="theater")
        await connection.access_token(session, http)
    assert used == ["refresh-2", "refresh-1"]


async def test_one_youtube_channel_cannot_be_linked_under_two_keys(site: Site) -> None:
    await site.link()
    with pytest.raises(Refused) as refused:
        await _link_theater(site, channel=CHANNEL)
    assert refused.value.code == "video_youtube_channel_already_linked"
    assert (await _rows(site))["theater"].channel_id is None


async def test_a_channel_key_must_be_added_first_and_be_well_formed(site: Site) -> None:
    async with site.factory() as session:
        with pytest.raises(Refused) as unknown:
            await connection.connection_row(session, key="theater")
        assert unknown.value.code == "video_youtube_channel_unknown"
        for bad in ("default", "Theater", "1st", "x"):
            with pytest.raises(Refused) as invalid:
                await connection.create_channel(session, site.owner, bad, None)
            assert invalid.value.code == "video_youtube_channel_key_invalid"
        await connection.create_channel(session, site.owner, "theater", None)
    async with site.factory() as session:
        with pytest.raises(Refused) as twice:
            await connection.create_channel(session, site.owner, "theater", None)
        assert twice.value.code == "video_youtube_channel_exists"


async def test_unlinking_one_channel_leaves_the_other_linked(site: Site) -> None:
    await site.link()
    await _link_theater(site)
    async with site.factory() as session:
        revoked, view = await connection.unlink(session, site.owner, key="theater")
    assert revoked and not view.linked and view.key == "theater"
    rows = await _rows(site)
    assert connection.linked(rows["default"]) and not connection.linked(rows["theater"])


async def test_a_video_goes_to_the_channel_it_names_and_keeps_it_once_on_youtube(
    site: Site, launched: list[str]
) -> None:
    await site.link()
    await _link_theater(site)
    await _package(site)
    _studio_video(site, channel=THEATER)

    async with site.factory() as session:
        view = await sync.choose_channel(session, SLUG, site.owner, "theater")
    assert view.youtube_channel_key == "theater"
    async with site.factory() as session:
        await sync.request_sync(session, review_store(site.settings), SLUG, site.owner, _publish())
    assert launched == [SLUG]
    await sync.run_sync(SLUG, site.factory)

    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
    assert project is not None and project.youtube_sync is not None
    assert project.youtube_sync["status"] == "done", project.youtube_sync
    assert project.youtube_video_id == STUDIO_ID

    async with site.factory() as session:
        with pytest.raises(Refused) as locked:
            await sync.choose_channel(session, SLUG, site.owner, "default")
    assert locked.value.code == "video_youtube_channel_locked"


async def test_a_video_of_the_other_channel_is_refused_at_the_details_step(
    site: Site, launched: list[str]
) -> None:
    await site.link()
    await _link_theater(site)
    await _package(site)
    _studio_video(site, channel=CHANNEL)
    async with site.factory() as session:
        await sync.choose_channel(session, SLUG, site.owner, "theater")
    async with site.factory() as session:
        await sync.request_sync(session, review_store(site.settings), SLUG, site.owner, _publish())
    await sync.run_sync(SLUG, site.factory)
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
    assert project is not None and project.youtube_sync is not None
    assert project.youtube_sync["status"] != "done"
    assert project.youtube_video_id is None


async def _report_tables(site: Site) -> None:
    async with site.factory() as session:
        await session.run_sync(
            lambda sync_session: Base.metadata.create_all(
                sync_session.connection(),
                tables=[
                    VideoYoutubeReportJob.__table__,
                    VideoYoutubeReport.__table__,
                    VideoYoutubeReportState.__table__,
                ],
            )
        )
        await session.commit()


async def _store_report(site: Site, channel_id: str) -> None:
    moment = datetime(2026, 11, 1, tzinfo=UTC)
    async with site.factory() as session:
        session.add(
            VideoYoutubeReportJob(
                job_id=f"job-{channel_id}",
                channel_id=channel_id,
                report_type_id="channel_basic_a3",
                name="mokaair",
                recorded_at=moment,
            )
        )
        session.add(
            VideoYoutubeReport(
                report_id=f"report-{channel_id}",
                job_id=f"job-{channel_id}",
                channel_id=channel_id,
                report_type_id="channel_basic_a3",
                day=date(2026, 11, 1),
                start_time=moment,
                end_time=moment,
                create_time=moment,
                downloaded_at=moment,
                columns=["date"],
                row_count=0,
                size_bytes=0,
                content_gzip=b"",
            )
        )
        await session.commit()


async def _kept(site: Site) -> list[str]:
    async with site.factory() as session:
        return sorted(
            (await session.scalars(select(VideoYoutubeReport.channel_id))).all()
        )


async def test_each_linked_channel_keeps_its_reports_until_it_is_unlinked(site: Site) -> None:
    await _report_tables(site)
    await site.link()
    await _link_theater(site)
    await _store_report(site, CHANNEL)
    await _store_report(site, THEATER)
    await _store_report(site, "UCsomeoneelse0000000000")

    async with site.factory() as session:
        assert await reports.forget_other_channels(session) == CHANNEL
        await session.commit()
    assert await _kept(site) == sorted([CHANNEL, THEATER]), "only an unheld channel's go"

    async with site.factory() as session:
        theater = await connection.connection_row(session, key="theater")
        state = await reports.state_row(session, theater)
        await session.commit()
    assert state.id != 1 and state.channel_id == THEATER

    async with site.factory() as session:
        await connection.unlink(session, site.owner, key="theater")
    async with site.factory() as session:
        await reports.forget_other_channels(session)
        await session.commit()
        states = (await session.scalars(select(VideoYoutubeReportState.id))).all()
    assert await _kept(site) == [CHANNEL]
    assert list(states) == [], "the theater's state went with it, and row 1 was never made"

    async with site.factory() as session:
        view = await reports.overview(session, key="theater")
    assert view["key"] == "theater" and view["linked"] is False and view["reports"] == []
    assert [item["key"] for item in view["channels"]] == ["default", "theater"]


async def test_the_channel_routes_list_add_and_guard_the_channels(site: Site) -> None:
    await site.link()
    reader = ASGITransport(app=_app({"content"}, site))
    async with AsyncClient(transport=reader, base_url="http://test") as client:
        listed = await client.get("/api/v1/admin/video-youtube/channels")
        refused = await client.post(
            "/api/v1/admin/video-youtube/channels", json={"key": "theater", "label": "劇場"}
        )
    assert listed.status_code == 200 and [item["key"] for item in listed.json()] == ["default"]
    assert refused.status_code == 403

    owner = ASGITransport(app=_app({"owner"}, site))
    async with AsyncClient(transport=owner, base_url="http://test") as client:
        added = await client.post(
            "/api/v1/admin/video-youtube/channels", json={"key": "theater", "label": "劇場"}
        )
        one = await client.get("/api/v1/admin/video-youtube/channels/theater")
        unknown = await client.get("/api/v1/admin/video-youtube/channels/nope")
        default = await client.get("/api/v1/admin/video-youtube")
    assert added.status_code == 201 and added.json()["key"] == "theater"
    assert one.json()["label"] == "劇場" and one.json()["configured"] is True
    assert unknown.status_code == 404
    assert default.json()["key"] == "default" and default.json()["channel_id"] == CHANNEL
    async with site.factory() as session:
        count = await session.scalar(select(func.count(VideoYoutubeConnection.id)))
    assert count == 2
