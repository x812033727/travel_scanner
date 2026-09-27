"""The requests the site sends YouTube for one video, as pure functions over what it has.

Nothing here calls anything: the upload package's metadata.json, the video as YouTube holds
it now, the owner's language choice and the publish time go in, and the bodies to send come
out (docs/videos/HANDS-OFF.md §YouTube API 第一步, docs/videos/LANGUAGES.md).
"""

from __future__ import annotations

import json
import secrets
from datetime import UTC, datetime
from typing import Any

from app.video_reviews.schemas import DUB_LOCALES, LocaleChoice

NARRATION_LOCALE = "zh-TW"
# The language codes YouTube files the captions under, when they differ from the site's
# locales. Blank until the first video is checked with captions.list (HANDS-OFF.md lists the
# question: zh-TW/zh-CN or zh-Hant/zh-Hans); a code not listed goes as the locale itself.
CAPTION_LANGUAGE_CODES: dict[str, str] = {}
# What each call costs against the daily quota of 10,000 units
# (developers.google.com/youtube/v3/determine_quota_cost).
QUOTA_UNITS = {
    "videos.list": 1,
    "videos.update": 50,
    "captions.list": 50,
    "captions.insert": 400,
    "thumbnails.set": 50,
}
# The snippet and status fields videos.update takes; the rest of what videos.list returns is
# read-only and would be refused or ignored.
WRITABLE_SNIPPET = (
    "title",
    "description",
    "tags",
    "categoryId",
    "defaultLanguage",
    "defaultAudioLanguage",
)
KEPT_STATUS = ("license", "embeddable", "publicStatsViewable")


def caption_language(locale: str) -> str:
    return CAPTION_LANGUAGE_CODES.get(locale, locale)


def description_locales(choices: dict[str, LocaleChoice], metadata: dict[str, Any]) -> list[str]:
    """The localizations to send: the languages the owner chose titles and descriptions for,
    in the page's order, when the upload package translated them."""
    localizations = metadata.get("localizations")
    available = set(localizations) if isinstance(localizations, dict) else set()
    return [
        locale
        for locale in DUB_LOCALES
        if choices.get(locale) is not None and choices[locale].metadata and locale in available
    ]


def caption_locales(choices: dict[str, LocaleChoice], files: set[str]) -> list[str]:
    """The caption tracks to send: zh-TW, then the chosen ones the package holds a file for
    (``files`` are the review's file roles, ``captions_<locale>``)."""
    wanted = [NARRATION_LOCALE]
    wanted.extend(
        locale
        for locale in DUB_LOCALES
        if choices.get(locale) is not None
        and choices[locale].captions
        and f"captions_{locale}" in files
    )
    return [locale for locale in wanted if f"captions_{locale}" in files]


def schedule_problem(status: dict[str, Any], publish_at: datetime, now: datetime) -> str | None:
    """Why ``publishAt`` cannot be set now, or None: YouTube takes it only on a private video
    that was never public, and only for a time still ahead."""
    privacy = status.get("privacyStatus")
    if privacy != "private":
        return f"影片現在是 {privacy or '不明'}，不是私人；排程只能設在從沒公開過的私人影片上"
    if publish_at <= now:
        return f"上架時間 {publish_at.astimezone(UTC).isoformat()} 已經過了"
    return None


def _part(current: dict[str, Any], name: str) -> dict[str, Any]:
    """One part of the video as YouTube returned it, or nothing."""
    value = current.get(name)
    return dict(value) if isinstance(value, dict) else {}


def _iso(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def update_body(
    *,
    video_id: str,
    current: dict[str, Any],
    metadata: dict[str, Any],
    locales: list[str],
    publish_at: datetime | None,
) -> dict[str, Any]:
    """The ``videos.update`` body: the current snippet and status merged with the package's
    zh-TW title, description, tags and category, ``defaultLanguage`` (required with
    localizations), the localizations of the chosen languages over the ones already there,
    ``privacyStatus`` private, made-for-kids no, the disclosure answer, and ``publishAt`` only
    when given. Every part sent is sent whole: a field left out of a part is cleared by YouTube."""
    snippet_now = _part(current, "snippet")
    status_now = _part(current, "status")
    localized_now = _part(current, "localizations")
    snippet: dict[str, Any] = {
        key: snippet_now[key] for key in WRITABLE_SNIPPET if key in snippet_now
    }
    snippet.update(
        {
            "title": metadata.get("title", snippet.get("title", "")),
            "description": metadata.get("description", snippet.get("description", "")),
            "tags": list(metadata.get("tags") or snippet.get("tags") or []),
            "categoryId": str(metadata.get("category_id") or snippet.get("categoryId") or "28"),
            "defaultLanguage": NARRATION_LOCALE,
        }
    )
    snippet.setdefault("defaultAudioLanguage", NARRATION_LOCALE)
    localizations = dict(localized_now)
    for locale in locales:
        fields = metadata["localizations"][locale]
        localizations[locale] = {"title": fields["title"], "description": fields["description"]}
    status: dict[str, Any] = {key: status_now[key] for key in KEPT_STATUS if key in status_now}
    status.update(
        {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": bool(metadata.get("made_for_kids", False)),
            "containsSyntheticMedia": bool(metadata.get("contains_synthetic_media", False)),
        }
    )
    if publish_at is not None:
        status["publishAt"] = _iso(publish_at)
    return {"id": video_id, "snippet": snippet, "status": status, "localizations": localizations}


def existing_caption_languages(items: list[dict[str, Any]]) -> set[str]:
    """The languages ``captions.list`` says the video already has, lower-cased for comparing."""
    found: set[str] = set()
    for item in items:
        snippet = item.get("snippet") if isinstance(item, dict) else None
        language = snippet.get("language") if isinstance(snippet, dict) else None
        if isinstance(language, str) and language:
            found.add(language.lower())
    return found


def missing_captions(items: list[dict[str, Any]], wanted: list[str]) -> list[str]:
    """The wanted locales with no track on YouTube yet, so a retry never uploads one twice."""
    have = existing_caption_languages(items)
    return [locale for locale in wanted if caption_language(locale).lower() not in have]


def caption_metadata(video_id: str, locale: str) -> dict[str, Any]:
    return {
        "snippet": {
            "videoId": video_id,
            "language": caption_language(locale),
            "name": locale,
            "isDraft": False,
        }
    }


def multipart_related(
    metadata: dict[str, Any], body: bytes, content_type: str
) -> tuple[bytes, str]:
    """A ``multipart/related`` upload body (the JSON part, then the file) and its boundary."""
    boundary = f"mokaair-{secrets.token_hex(12)}"
    parts = [
        f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n".encode(),
        json.dumps(metadata, ensure_ascii=False).encode(),
        f"\r\n--{boundary}\r\nContent-Type: {content_type}\r\n\r\n".encode(),
        body,
        f"\r\n--{boundary}--\r\n".encode(),
    ]
    return b"".join(parts), boundary
