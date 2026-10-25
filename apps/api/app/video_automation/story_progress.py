"""Read-only progress for the twenty Everyday Reversals brand stories.

Planning and script intake are distinct from a completed film.  Keep these counters
separate so the admin page can explain why a series with authored work still says 0/20
finished videos.
"""

from __future__ import annotations

from hashlib import sha256
from typing import Literal

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import VideoProject, VideoReview
from app.video_automation.models import VideoDramaEpisode, VideoDramaSeries
from app.video_automation.stories import EVERYDAY_REVERSALS_SLUG, story_problems

EPISODE_COUNT = 20
ScriptStatus = Literal["approved", "pending"]


class StoryPreproductionEpisode(BaseModel):
    number: int
    slug: str | None
    title: str
    full_plan: bool
    script_status: ScriptStatus | None
    source_markdown_verified: bool
    film_status: str


class StoryPreproductionOut(BaseModel):
    series_slug: str
    total_episodes: int
    full_plans: int
    scripts_approved: int
    scripts_pending: int
    source_markdown_verified: int
    finished_films: int
    episodes: list[StoryPreproductionEpisode]


def _full_plan(episode: VideoDramaEpisode) -> bool:
    if not 1 <= episode.number <= EPISODE_COUNT or episode.chapter_number != 1:
        return False
    beats = episode.beats
    if not isinstance(beats, dict) or beats.get("id") != f"C{episode.number:02d}":
        return False
    # The importer keeps the remaining story fields in beats.  Reconstruct exactly
    # what it validated, including the row's current number, slug, title and logline.
    story = {
        **beats,
        "number": episode.number,
        "slug": episode.slug,
        "title": episode.title,
        "logline": episode.logline,
    }
    return not story_problems(story, series_slug=EVERYDAY_REVERSALS_SLUG)


def _verified_source(review: VideoReview | None) -> bool:
    if review is None or review.status not in {"approved", "pending"}:
        return False
    payload = review.payload
    source = payload.get("source_md") if isinstance(payload, dict) else None
    return (
        isinstance(source, str)
        and bool(source.strip())
        and sha256(source.encode("utf-8")).hexdigest() == review.content_sha256.lower()
    )


async def story_preproduction(session: AsyncSession) -> StoryPreproductionOut:
    """Count the target series from persisted rows with bounded, batched reads."""
    empty = StoryPreproductionOut(
        series_slug=EVERYDAY_REVERSALS_SLUG,
        total_episodes=EPISODE_COUNT,
        full_plans=0,
        scripts_approved=0,
        scripts_pending=0,
        source_markdown_verified=0,
        finished_films=0,
        episodes=[],
    )
    series = await session.scalar(
        select(VideoDramaSeries).where(
            VideoDramaSeries.slug == EVERYDAY_REVERSALS_SLUG,
            VideoDramaSeries.kind == "story",
        )
    )
    if series is None:
        return empty

    episodes = list(
        (
            await session.scalars(
                select(VideoDramaEpisode)
                .where(VideoDramaEpisode.series_id == series.id)
                .order_by(VideoDramaEpisode.number)
            )
        ).all()
    )
    target_episodes = [episode for episode in episodes if 1 <= episode.number <= EPISODE_COUNT]
    projects = list(
        (
            await session.scalars(
                select(VideoProject).where(
                    VideoProject.series_slug == EVERYDAY_REVERSALS_SLUG,
                    VideoProject.format == "drama",
                    VideoProject.shorts_line.is_(None),
                    VideoProject.dropped_at.is_(None),
                )
            )
        ).all()
    )
    project_by_episode = {
        (project.episode_number, project.slug): project
        for project in projects
        if project.episode_number is not None
    }
    candidate_ids = [
        project.id
        for episode in target_episodes
        if episode.slug is not None
        if (project := project_by_episode.get((episode.number, episode.slug))) is not None
    ]
    current_review: dict[object, VideoReview] = {}
    if candidate_ids:
        reviews = (
            await session.scalars(
                select(VideoReview)
                .where(
                    VideoReview.project_id.in_(candidate_ids),
                    VideoReview.gate == "script",
                    VideoReview.subject.is_(None),
                )
                .order_by(
                    VideoReview.created_at.desc(),
                    VideoReview.revision.desc(),
                    VideoReview.id.desc(),
                )
            )
        ).all()
        # A later rejected or superseded card makes an older approval non-current.
        for candidate in reviews:
            current_review.setdefault(candidate.project_id, candidate)

    results: list[StoryPreproductionEpisode] = []
    for episode in target_episodes:
        project = (
            project_by_episode.get((episode.number, episode.slug))
            if episode.slug is not None
            else None
        )
        review = current_review.get(project.id) if project is not None else None
        script_status: ScriptStatus | None = None
        if review is not None and review.status == "approved":
            script_status = "approved"
        elif review is not None and review.status == "pending":
            script_status = "pending"
        results.append(
            StoryPreproductionEpisode(
                number=episode.number,
                slug=episode.slug,
                title=episode.title,
                full_plan=_full_plan(episode),
                script_status=script_status,
                source_markdown_verified=_verified_source(review),
                film_status=episode.status,
            )
        )
    return StoryPreproductionOut(
        series_slug=EVERYDAY_REVERSALS_SLUG,
        total_episodes=EPISODE_COUNT,
        full_plans=sum(item.full_plan for item in results),
        scripts_approved=sum(item.script_status == "approved" for item in results),
        scripts_pending=sum(item.script_status == "pending" for item in results),
        source_markdown_verified=sum(item.source_markdown_verified for item in results),
        finished_films=sum(item.film_status == "done" for item in results),
        episodes=results,
    )
