"""What the site sends YouTube, built from the approved upload package. Pure functions.

The package is the approved upload confirmation (gate ``publish``) the worker submitted
(docs/videos/HANDS-OFF.md §上傳包與「可以上架」): ``metadata.json`` with the title and
description in the narration language (``default_language``, zh-TW when absent), the other
locales' ``localizations``, the tags, the category and the disclosure answer, plus the caption
files and the thumbnail. The owner may rewrite that title and description on the card before
sending (YouTube's Required Minimum Functionality asks that the
uploader can set them), and chooses the visibility and the time.
"""

from __future__ import annotations

import copy
from datetime import UTC, datetime
from typing import Any, cast

from app.video_reviews.schemas import DUB_LOCALES

# The narration language of a package that names none: every video made before the dubs.
DEFAULT_LANGUAGE = "zh-TW"
# What a package may be narrated in: the languages the site makes videos in.
NARRATION_LANGUAGES: tuple[str, ...] = (DEFAULT_LANGUAGE, *DUB_LOCALES)
# snippet.title: 100 characters; snippet.description: 5000 bytes; neither may hold < or >.
TITLE_MAX_CHARS = 100
DESCRIPTION_MAX_BYTES = 5000
FORBIDDEN_CHARACTERS = ("<", ">")
# The package's category when metadata.json names none: Science & Technology.
DEFAULT_CATEGORY = "28"
# The caption track's name. The name shows next to the language in the player's menu, so the
# tracks carry none and read as plain "Chinese (Taiwan)", "English"...
CAPTION_NAME = ""
# What a videos.update may carry in the two parts besides the localizations; everything else
# YouTube returns (thumbnails, channelTitle, uploadStatus...) is read-only and left out.
SNIPPET_FIELDS = ("title", "description", "tags", "categoryId", "defaultLanguage")
STATUS_FIELDS = (
    "privacyStatus",
    "embeddable",
    "license",
    "publicStatsViewable",
    "selfDeclaredMadeForKids",
    "containsSyntheticMedia",
    "publishAt",
)
# The same language under the tags YouTube may hand back for it.
LANGUAGE_ALIASES = {"zh-hant": "zh-tw", "zh-hans": "zh-cn"}


def as_dict(value: object) -> dict[str, Any]:
    """``value`` when it is a JSON object, else an empty one: YouTube's answers are read loosely."""
    return cast(dict[str, Any], value) if isinstance(value, dict) else {}


def text_problem(title: str, description: str) -> str | None:
    """Why YouTube would refuse this title or description, in the owner's words, or None."""
    if not title.strip():
        return "標題不能空白"
    if len(title) > TITLE_MAX_CHARS:
        return f"標題最多 {TITLE_MAX_CHARS} 個字元，現在是 {len(title)} 個"
    size = len(description.encode())
    if size > DESCRIPTION_MAX_BYTES:
        return f"說明最多 {DESCRIPTION_MAX_BYTES} 位元組，現在是 {size} 位元組"
    for character in FORBIDDEN_CHARACTERS:
        if character in title or character in description:
            return f"標題與說明不能有 {character}（YouTube 會拒絕）"
    return None


def publish_at_text(value: datetime) -> str:
    """RFC 3339 in UTC, the form status.publishAt takes."""
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _synthetic(metadata: dict[str, Any]) -> bool | None:
    value = metadata.get("contains_synthetic_media")
    return value if isinstance(value, bool) else None


def _tags(metadata: dict[str, Any]) -> list[str]:
    tags = metadata.get("tags")
    return [str(tag) for tag in tags if str(tag).strip()] if isinstance(tags, list) else []


def _category(metadata: dict[str, Any], current: str | None = None) -> str:
    value = metadata.get("category_id")
    if isinstance(value, int | str) and str(value).isdigit():
        return str(value)
    return current or DEFAULT_CATEGORY


def narration_language(metadata: dict[str, Any]) -> str:
    """The language the approved package is narrated in: the video's default and audio language.

    ``default_language`` is in metadata.json, which the approval binds by its SHA-256, and a
    language batch cannot change it; the owner's request never carries one. A package without
    it is zh-TW, as every video was before the dubs. Any other value is refused rather than sent
    to YouTube under a language the site does not make.
    """
    value = metadata.get("default_language")
    if value is None:
        return DEFAULT_LANGUAGE
    if not isinstance(value, str) or value not in NARRATION_LANGUAGES:
        raise ValueError(f"unsupported narration language: {value!r}")
    return value


def localizations(metadata: dict[str, Any]) -> dict[str, dict[str, str]]:
    """The package's other locales, {locale: {title, description}}; the narration language is
    the snippet itself, so its own copy is left out (a zh-TW copy stays for English narration).
    """
    own = narration_language(metadata)
    found = metadata.get("localizations")
    result: dict[str, dict[str, str]] = {}
    if not isinstance(found, dict):
        return result
    for locale, values in found.items():
        if locale == own or not isinstance(values, dict):
            continue
        title, description = values.get("title"), values.get("description")
        if isinstance(title, str) and title.strip() and isinstance(description, str):
            result[str(locale)] = {"title": title, "description": description}
    return result


def insert_body(metadata: dict[str, Any], title: str, description: str) -> dict[str, Any]:
    """The videos.insert resource: private, with no publish time yet.

    The details step right after the upload sends the whole of it again with the time and the
    localizations, so what the upload itself carries only has to be valid and private.
    """
    language = narration_language(metadata)
    status: dict[str, Any] = {
        "privacyStatus": "private",
        "selfDeclaredMadeForKids": bool(metadata.get("made_for_kids", False)),
    }
    synthetic = _synthetic(metadata)
    if synthetic is not None:
        status["containsSyntheticMedia"] = synthetic
    return {
        "snippet": {
            "title": title,
            "description": description,
            "tags": _tags(metadata),
            "categoryId": _category(metadata),
            "defaultLanguage": language,
            "defaultAudioLanguage": language,
        },
        "status": status,
    }


def update_body(
    current: dict[str, Any],
    metadata: dict[str, Any],
    *,
    title: str,
    description: str,
    visibility: str,
    publish_at: datetime | None,
) -> dict[str, Any]:
    """The videos.update body: what the video has now, with the package and the owner's choice.

    videos.update deletes any property of a sent part that the body leaves out, so the current
    values are read first (videos.list) and carried over, and only the fields the site owns are
    replaced. ``visibility`` is "scheduled" (private until ``publish_at``, when YouTube makes it
    public), "unlisted" or "private"; the site never sets public itself.
    """
    language = narration_language(metadata)
    snippet_now = as_dict(current.get("snippet"))
    status_now = as_dict(current.get("status"))
    snippet = {key: copy.deepcopy(snippet_now[key]) for key in SNIPPET_FIELDS if key in snippet_now}
    snippet.update(
        title=title,
        description=description,
        tags=_tags(metadata),
        categoryId=_category(metadata, snippet_now.get("categoryId")),
        defaultLanguage=language,
        # The approved narration language (the dubs are separate audio tracks).
        defaultAudioLanguage=language,
    )
    status = {key: status_now[key] for key in STATUS_FIELDS if key in status_now}
    status["selfDeclaredMadeForKids"] = bool(metadata.get("made_for_kids", False))
    synthetic = _synthetic(metadata)
    if synthetic is not None:
        status["containsSyntheticMedia"] = synthetic
    if visibility == "scheduled":
        if publish_at is None:
            raise ValueError("a scheduled video needs a publish time")
        status["privacyStatus"] = "private"
        status["publishAt"] = publish_at_text(publish_at)
    else:
        status["privacyStatus"] = visibility
        status.pop("publishAt", None)
    existing = current.get("localizations")
    merged: dict[str, Any] = copy.deepcopy(existing) if isinstance(existing, dict) else {}
    # A copy of the default language would go stale beside the snippet it duplicates.
    merged.pop(language, None)
    merged.update(localizations(metadata))
    return {"id": current.get("id"), "snippet": snippet, "status": status, "localizations": merged}


def unschedule_body(current: dict[str, Any]) -> dict[str, Any]:
    """The videos.update body that takes a scheduled video off the schedule: everything it has
    now, private, with no publish time. Nothing else of the video changes, so the other
    languages it has are sent back as they are: a part that is left out is emptied."""
    snippet_now = as_dict(current.get("snippet"))
    status_now = as_dict(current.get("status"))
    snippet = {key: copy.deepcopy(snippet_now[key]) for key in SNIPPET_FIELDS if key in snippet_now}
    status = {key: status_now[key] for key in STATUS_FIELDS if key in status_now}
    status["privacyStatus"] = "private"
    status.pop("publishAt", None)
    return {
        "id": current.get("id"),
        "snippet": snippet,
        "status": status,
        "localizations": copy.deepcopy(as_dict(current.get("localizations"))),
    }


def language_key(value: str) -> str:
    key = value.strip().lower().replace("_", "-")
    return LANGUAGE_ALIASES.get(key, key)


def caption_languages(tracks: list[dict[str, Any]]) -> set[str]:
    """The languages that already have a track someone uploaded (automatic ones do not count)."""
    found = set()
    for track in tracks:
        snippet = as_dict(track.get("snippet"))
        if str(snippet.get("trackKind", "")).lower() == "asr":
            continue
        language = snippet.get("language")
        if isinstance(language, str) and language:
            found.add(language_key(language))
    return found


def locale_of_role(role: str, prefix: str, locales: list[str]) -> str:
    """The locale a package file names (captions_zh-TW), matched to the listed locales.

    An older worker lower-cased the locale with "_" (captions_zh_tw); both read as zh-TW.
    """
    suffix = role[len(prefix) :]
    flat = suffix.lower().replace("-", "_")
    for locale in locales:
        if locale.lower().replace("-", "_") == flat:
            return locale
    return suffix
