"""``python -m app.cli video-story-import --series <slug> [--apply] [--limit N]
[--episodes-per-day N] < stories.json``: the brand-story backlog into its series.

The file is the compiled ``stories.json`` of a plan under docs/videos/story-plans
(docs/videos/STORY.md §企劃清單與集數列), read from standard input so the host can pipe it into
the API container. The run is a dry run unless ``--apply``: it prints how many rows it would
create, update, leave alone and refuse, and every problem; one problem refuses the whole file
and nothing is written. The rules and the import live in ``app.video_automation.stories``.

On the host, after a deploy and with the owner's go-ahead, the pilot imports two stories::

    docker compose -f docker-compose.prod.yml exec -T api python -m app.cli video-story-import \\
        --series brand-stories --limit 2 --episodes-per-day 1 < stories.json
"""

from __future__ import annotations

import json
from typing import Any

from app.db import SessionFactory
from app.video_automation.stories import StoryImportReport, import_story_rows


async def import_story_file(
    text: str,
    *,
    series: str,
    apply: bool = False,
    limit: int | None = None,
    episodes_per_day: int | None = None,
) -> dict[str, Any]:
    """Parse the file and import it; the report as the command prints it."""
    try:
        document = json.loads(text)
    except json.JSONDecodeError as error:
        refused = StoryImportReport(series=series, apply=apply)
        refused.problems.append(f"the file is not valid JSON: {error}")
        return refused.as_dict()
    async with SessionFactory() as session:
        report = await import_story_rows(
            session,
            document,
            series_slug=series,
            apply=apply,
            limit=limit,
            episodes_per_day=episodes_per_day,
        )
    return report.as_dict()
