"""The job rows against PostgreSQL: dedupe by request hash, the month's spend, and pruning."""

from __future__ import annotations

import copy
import hashlib
import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import uuid4

import fakeredis
import httpx
import pytest
import pytest_asyncio
from sqlalchemy import delete, select

from app.config import Settings
from app.db import SessionFactory, engine
from app.models import VideoProject
from app.video_automation.models import DEFAULT_DRAMA, VideoAutomationSettings
from app.video_media import jobs as service
from app.video_media import meter
from app.video_media.jobs import MediaContext, prune, submit_job
from app.video_media.models import VideoMediaJob
from app.video_media.providers import MediaRequest, Submitted
from app.video_media.schemas import ImageJobIn
from app.video_media.settings import MediaSettings
from app.video_media.storage import MediaStore

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 30


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    yield
    async with SessionFactory() as session:
        await session.execute(delete(VideoMediaJob).where(VideoMediaJob.slug.like("it-media-%")))
        await session.execute(delete(VideoProject).where(VideoProject.slug.like("it-media-%")))
        await session.commit()
    await engine.dispose()


class InlineProvider:
    name = "gemini"

    def __init__(self, data: bytes) -> None:
        self.data = data

    async def submit(self, request: MediaRequest, client: httpx.AsyncClient) -> Submitted:
        return Submitted(inline=self.data, content_type="image/png")

    async def poll(self, vendor_ref: str, client: httpx.AsyncClient) -> Any:
        raise AssertionError("not polled")

    def fetch(self, download: Any) -> tuple[str, dict[str, str]]:
        raise AssertionError("not fetched")


@pytest.mark.asyncio(loop_scope="module")
async def test_jobs_dedupe_by_hash_count_toward_the_month_and_are_pruned(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    slug = f"it-media-{uuid4().hex[:10]}"
    monkeypatch.setattr(service, "provider_for", lambda runtime, vendor, kind: InlineProvider(PNG))
    store = MediaStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)
    media = MediaSettings(video_media_dir=str(tmp_path), video_media_keep_days=2)
    redis = fakeredis.aioredis.FakeRedis()
    row = VideoAutomationSettings(id=1, **{**copy.deepcopy(DEFAULT_DRAMA), "drama_enabled": True})
    async with SessionFactory() as session:
        ctx = MediaContext(
            session=session,
            redis=redis,
            store=store,
            runtime=Settings(hotspot_guide_gemini_api_key="g"),
            media=media,
            row=row,
        )
        payload = ImageJobIn.model_validate({"slug": slug, "purpose": "keyframe", "prompt": "dawn"})
        job, created = await submit_job(ctx, "image", payload)
        assert created and job.status == "ready"
        assert job.file_sha256 == hashlib.sha256(PNG).hexdigest()
        same, again = await submit_job(ctx, "image", payload)
        assert same.id == job.id and not again
        other, _ = await submit_job(ctx, "image", payload.model_copy(update={"seed": 5}))
        assert other.id != job.id
        rows = list(await session.scalars(select(VideoMediaJob).where(VideoMediaJob.slug == slug)))
        assert len(rows) == 2
        assert await meter.slug_usd(session, slug) == 0.268
        assert await meter.month_usd(session, redis) >= 0.268

        # Nothing is old yet, so a prune keeps everything.
        untouched = await prune(session, store, media)
        assert untouched.expired_jobs == 0 and store.path(slug, job.file_sha256 or "") is not None
        # Once the video is on YouTube its generations are gone for good.
        session.add(
            VideoProject(slug=slug, title="t", stage="published", youtube_video_id="abcDEF123_-")
        )
        await session.commit()
        pruned = await prune(session, store, media, datetime.now(UTC) + timedelta(days=1))
        assert pruned.expired_jobs == 2 and pruned.deleted_files == 1
        assert store.path(slug, job.file_sha256 or "") is None
        statuses = {
            r.status
            for r in await session.scalars(select(VideoMediaJob).where(VideoMediaJob.slug == slug))
        }
        assert statuses == {"expired"}
