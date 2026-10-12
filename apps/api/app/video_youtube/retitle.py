"""Give the videos already on the channel the captions tag their titles now end with.

Since 2026-10-12 every title the site sends ends with its language's captions tag
(``requests.CAPTION_TAGS``); the owner then asked for the videos uploaded before that, public ones
included, to carry it too. This walks the channel's uploads playlist (playlistItems.list, 1 unit
per fifty), reads the videos (videos.list, 1 unit per fifty) and, for a video whose title or one of
whose localized titles lacks the tag, sends videos.update (50 units) with everything the video has
now and only those titles changed. A title the tag would push past YouTube's 100 characters is
reported and the video left alone: shortening a title is the owner's call. Nothing is sent unless
``apply``, and ``limit`` caps the updates of one run so the daily quota (10,000) stays for the rest.
"""

from __future__ import annotations

import copy
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User
from app.video_reviews.admin_service import _linked_youtube
from app.video_youtube.client import YoutubeError
from app.video_youtube.requests import (
    DEFAULT_LANGUAGE,
    SNIPPET_FIELDS,
    STATUS_FIELDS,
    TITLE_MAX_CHARS,
    as_dict,
    captioned,
    language_key,
)

# 150 updates are 7,500 units: a run leaves a quarter of the day's quota for everything else.
DEFAULT_LIMIT = 150
UPDATE_UNITS = 50


def tag_language(code: object) -> str:
    """The CAPTION_TAGS key for a language YouTube names (zh-Hant, en-US...): English otherwise."""
    key = language_key(code) if isinstance(code, str) and code.strip() else "zh-tw"
    if key.startswith("zh"):
        return "zh-TW"
    for language in ("en", "ja", "ko"):
        if key == language or key.startswith(f"{language}-"):
            return language
    return "en"


def plan(video: dict[str, Any]) -> dict[str, Any]:
    """What tagging ``video`` changes: {id, privacy, titles: {language: [old, new]}, problem}.

    ``titles`` is empty when every title already ends with its tag. A video without a default
    language is the channel's zh-TW, as every video was before the dubs.
    """
    snippet = as_dict(video.get("snippet"))
    language = snippet.get("defaultLanguage") or DEFAULT_LANGUAGE
    titles: dict[str, list[str]] = {}
    problem = None
    candidates = [(str(language), snippet.get("title"))]
    candidates += [
        (str(locale), as_dict(entry).get("title"))
        for locale, entry in as_dict(video.get("localizations")).items()
    ]
    for locale, title in candidates:
        if not isinstance(title, str) or not title.strip():
            continue
        new = captioned(title, tag_language(locale))
        if new == title:
            continue
        titles[locale] = [title, new]
        if len(new) > TITLE_MAX_CHARS:
            problem = f"{locale} 加標記後 {len(new)} 字，超過 {TITLE_MAX_CHARS}，要先縮短標題"
    return {
        "id": video.get("id"),
        "privacy": as_dict(video.get("status")).get("privacyStatus"),
        "titles": titles,
        "problem": problem,
    }


def update_body(video: dict[str, Any]) -> dict[str, Any]:
    """The videos.update body: everything ``video`` has now, every title with its tag.

    videos.update empties any property of a sent part that the body leaves out, so the snippet,
    the status and the localizations are carried over whole (defaultAudioLanguage included).
    """
    snippet_now = as_dict(video.get("snippet"))
    status_now = as_dict(video.get("status"))
    language = str(snippet_now.get("defaultLanguage") or DEFAULT_LANGUAGE)
    keep = (*SNIPPET_FIELDS, "defaultAudioLanguage")
    snippet = {key: copy.deepcopy(snippet_now[key]) for key in keep if key in snippet_now}
    if isinstance(snippet.get("title"), str):
        snippet["title"] = captioned(snippet["title"], tag_language(language))
    localizations = copy.deepcopy(as_dict(video.get("localizations")))
    for locale, entry in localizations.items():
        if isinstance(entry, dict) and isinstance(entry.get("title"), str) and entry["title"]:
            entry["title"] = captioned(entry["title"], tag_language(locale))
    return {
        "id": video.get("id"),
        "snippet": snippet,
        "status": {key: status_now[key] for key in STATUS_FIELDS if key in status_now},
        "localizations": localizations,
    }


async def caption_channel_titles(
    session: AsyncSession,
    *,
    apply: bool,
    limit: int = DEFAULT_LIMIT,
    skip: frozenset[str] = frozenset(),
    actor: User | None = None,
) -> dict[str, Any]:
    """Tag the titles of every video on the linked channel; report only unless ``apply``.

    ``Refused`` when no channel is linked. An update YouTube refuses (a quota run out among them)
    ends the run: what was sent stays sent, the rest is reported as left for the next run. The
    videos in ``skip`` (the OAuth verification demo, say) are read and left alone.
    """
    report: dict[str, Any] = {
        "apply": apply,
        "limit": limit,
        "videos": 0,
        "to_change": 0,
        "changed": 0,
        "too_long": 0,
        "left": 0,
        "units_for_updates": 0,
        "error": None,
        "skipped": sorted(skip),
        "plans": [],
    }
    async with _linked_youtube(session) as (_channel_id, client):
        uploads = await client.uploads_playlist()
        if uploads is None:
            report["error"] = "連結的帳號沒有頻道的上傳清單"
            return report
        ids: list[str] = []
        token: str | None = None
        while True:
            page, token = await client.playlist_page(uploads, token)
            ids += [video_id for video_id in page if video_id not in ids]
            if token is None:
                break
        videos: list[dict[str, Any]] = []
        for start in range(0, len(ids), 50):
            batch = ids[start : start + 50]
            videos += await client.videos(batch, parts="snippet,status,localizations")
        report["videos"] = len(videos)
        sent = 0
        for video in videos:
            if video.get("id") in skip:
                continue
            found = plan(video)
            if not found["titles"]:
                continue
            report["plans"].append(found)
            if found["problem"]:
                report["too_long"] += 1
                continue
            report["to_change"] += 1
            if not apply:
                continue
            if report["error"] is not None or sent >= limit:
                report["left"] += 1
                continue
            try:
                await client.update_video(update_body(video))
            except YoutubeError as error:
                report["error"] = f"{found['id']}：{error}"
                report["left"] += 1
                continue
            sent += 1
            found["sent"] = True
            session.add(
                AdminAuditLog(
                    actor_user_id=actor.id if actor else None,
                    action="video_youtube_title_captioned",
                    target=f"youtube_video:{found['id']}",
                    metadata_json={"youtube_video_id": found["id"], "titles": found["titles"]},
                )
            )
            await session.commit()
        report["changed"] = sent
        if not apply:
            report["left"] = report["to_change"]
        report["units_for_updates"] = UPDATE_UNITS * (sent if apply else report["to_change"])
        report["finished_at"] = datetime.now(UTC).isoformat()
    return report
