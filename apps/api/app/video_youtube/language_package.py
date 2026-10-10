"""Validate a separately approved language batch against its original approved upload.

No database writes or inferred legacy provenance: the manifest, its metadata and every
attachment must describe the same approved cut and the owner's current language choices.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from app.models import VideoProject, VideoReview
from app.video_reviews.schemas import (
    DUB_LOCALES,
    LOCALE_PARTS,
    RETIRED_LOCALES,
    LocalesIn,
    without_retired_locales,
)
from app.video_reviews.storage import ReviewStore, valid_sha256
from app.video_youtube.errors import Refused
from app.video_youtube.requests import localizations, text_problem

HASH = re.compile(r"^(?:[0-9a-f]{16}|[0-9a-f]{64})$")
FILE_KEYS = ("role", "sha256", "size", "content_type")


def invalid(detail: str) -> Refused:
    return Refused(409, "video_youtube_languages_invalid", detail)


def choices(raw: Any) -> dict[str, dict[str, bool]]:
    """The owner's choice as the worker and the manifest read it, in the page's order.

    A language the video is no longer made in (zh-CN before 2026-10-09) is left out rather
    than refused, whether it comes from the project or from an approved batch's manifest: the
    batch's other languages were approved and keep syncing.
    """
    if not isinstance(raw, dict):
        raise invalid("語言選擇格式不正確，請重新儲存語言設定")
    raw = without_retired_locales(raw)
    for locale, entry in raw.items():
        if locale not in DUB_LOCALES or not isinstance(entry, dict):
            raise invalid("語言選擇格式不正確，請重新儲存語言設定")
        if set(entry) - set(LOCALE_PARTS) or any(
            type(value) is not bool for value in entry.values()
        ):
            raise invalid("語言選擇格式不正確，請重新儲存語言設定")
    normalized = LocalesIn.model_validate({"locales": raw}).locales
    return {str(locale): value.model_dump() for locale, value in normalized.items()}


def identity(review: VideoReview) -> dict[str, str]:
    return {"review_id": str(review.id), "content_sha256": review.content_sha256}


def files_by_role(raw: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(raw, list):
        raise invalid("核准的語言附件清單格式不正確，請重新送審")
    result: dict[str, dict[str, Any]] = {}
    for value in raw:
        if not isinstance(value, dict):
            raise invalid("核准的語言附件格式不正確，請重新送審")
        item = {key: value.get(key) for key in FILE_KEYS}
        role, sha, size, content_type = (item[key] for key in FILE_KEYS)
        if (
            not isinstance(role, str)
            or not role
            or role in result
            or not isinstance(sha, str)
            or not valid_sha256(sha)
            or type(size) is not int
            or size <= 0
            or not isinstance(content_type, str)
            or not content_type
        ):
            raise invalid("核准的附件有重複角色或不完整的雜湊與大小，請重新送審")
        result[role] = item
    return result


def checked_file(store: ReviewStore, slug: str, item: dict[str, Any]) -> bytes:
    """Read the small JSON/text assets only after checking their exact approved bytes."""
    path = store.path(slug, item["sha256"])
    if path is None or path.stat().st_size != item["size"]:
        raise invalid("核准的語言附件遺失或大小改變，請重新送審")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != item["sha256"]:
        raise invalid("語言附件已不是核准的內容，請重新送審")
    return raw


def verify_file(store: ReviewStore, slug: str, item: dict[str, Any]) -> None:
    path = store.path(slug, item["sha256"])
    if path is None or path.stat().st_size != item["size"]:
        raise invalid("核准的附件遺失或大小改變，請重新送審")
    with path.open("rb") as handle:
        digest = hashlib.file_digest(handle, "sha256").hexdigest()
    if digest != item["sha256"]:
        raise invalid("附件已不是核准的內容，請重新送審")


def read_json(store: ReviewStore, slug: str, item: dict[str, Any]) -> dict[str, Any]:
    if item["content_type"] != "application/json":
        raise invalid("語言清單與 metadata 必須是 JSON 附件")
    try:
        value = json.loads(checked_file(store, slug, item))
    except (ValueError, UnicodeError) as error:
        raise invalid("核准的語言 JSON 讀不懂，請重新送審") from error
    if not isinstance(value, dict):
        raise invalid("核准的語言 JSON 格式不正確，請重新送審")
    return value


def _stamp(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def _latest(rows: list[VideoReview], gate: str) -> VideoReview | None:
    return next((row for row in rows if row.gate == gate and row.subject is None), None)


def _state(value: Any) -> str:
    if value == "ready":
        return "ready"
    if (
        isinstance(value, dict)
        and value.get("status") == "skipped"
        and isinstance(value.get("reason"), str)
        and value["reason"].strip()
    ):
        return "skipped"
    raise invalid("選取的語言項目尚未完成，或沒有明確的略過原因，請重新送審")


def _localized(metadata: dict[str, Any], locale: str) -> dict[str, str]:
    values = metadata.get("localizations")
    entry = values.get(locale) if isinstance(values, dict) else None
    if (
        not isinstance(entry, dict)
        or not isinstance(entry.get("title"), str)
        or not isinstance(entry.get("description"), str)
        or text_problem(entry["title"], entry["description"])
    ):
        raise invalid(f"核准的 {locale} 標題說明缺漏或不正確，請重新送審")
    return {"title": entry["title"], "description": entry["description"]}


def _original(metadata: dict[str, Any]) -> dict[str, str]:
    title, description = metadata.get("title"), metadata.get("description")
    if (
        not isinstance(title, str)
        or not isinstance(description, str)
        or text_problem(title, description)
    ):
        raise invalid("核准的原語言標題說明缺漏或不正確，請重新送審")
    return {"title": title, "description": description}


def _source(
    manifest: dict[str, Any],
    rows: list[VideoReview],
    publish: VideoReview,
    base: dict[str, Any],
    translated: dict[str, Any],
    project: VideoProject,
) -> None:
    source = manifest.get("source")
    keys = {"publish", "final", "script", "branding_hash", "speech_hash", "compilation_hash"}
    if not isinstance(source, dict) or set(source) != keys:
        raise invalid("語言包缺少完整的原片核准來源，請重新產生並送審")
    if source["publish"] != identity(publish):
        raise invalid("語言包屬於另一份上傳核准，請重新送審")
    # A screenplay the owner reviewed on the site binds a drama's batch. A drama whose screenplay
    # only the worker approved (a brand story, or one made with the screenplay gate off) has no
    # review to bind; its batch names none, and the approved final cut is the owner's review.
    script_required = (
        project.format == "drama"
        and not base.get("compilation")
        and _latest(rows, "script") is not None
    )
    if not script_required and source["script"] is not None:
        raise invalid("這類影片的語言包不應綁定劇本審核，請重新送審")
    for gate in ("final", "script") if script_required else ("final",):
        review = _latest(rows, gate)
        if review is None:
            raise invalid("語言包缺少目前的成片或劇本核准，請重新送審")
        elif review.status != "approved" or source[gate] != identity(review):
            raise invalid("語言包的成片或劇本核准已變更，請重新送審")
    final = _latest(rows, "final")
    assert final is not None
    if (
        base.get("final_sha256") != final.content_sha256
        or translated.get("final_sha256") != final.content_sha256
    ):
        raise invalid("語言包的原片與核准成片不同，請重新送審")
    if translated.get("default_language", "zh-TW") != base.get("default_language", "zh-TW"):
        raise invalid("語言包不能變更原片語言，請重新送審")
    final_payload = final.payload if isinstance(final.payload, dict) else {}
    for key in ("branding_hash", "speech_hash", "compilation_hash"):
        value = source[key]
        if value is not None and (not isinstance(value, str) or not HASH.fullmatch(value)):
            raise invalid("語言包的來源雜湊格式不正確，請重新送審")
        if key == "branding_hash":
            if any(container.get(key) != value for container in (base, translated, final_payload)):
                raise invalid("語言包與核准成片使用不同的片頭片尾，請重新送審")
        elif any(
            key in container and container[key] != value
            for container in (base, translated, final_payload)
        ):
            raise invalid("語言包的旁白或合輯來源不符，請重新送審")
    if bool(base.get("compilation")) != bool(translated.get("compilation")):
        raise invalid("語言包的影片類型與核准成片不同，請重新送審")


@dataclass(frozen=True)
class Composition:
    metadata: dict[str, Any]
    captions: dict[str, dict[str, Any]]
    sha256: str
    approval_pin: dict[str, Any]


def compose(
    store: ReviewStore,
    slug: str,
    project: VideoProject,
    rows: list[VideoReview],
    publish: VideoReview,
    base: dict[str, Any],
    base_captions: dict[str, dict[str, Any]],
    *,
    verify_files: bool = True,
) -> Composition:
    current = choices(project.locales or {})
    chosen = project.locales_decided_at is not None or bool(current)
    pin: dict[str, Any] = {"publish": identity(publish), "languages": None, "choice": current}
    metadata = copy.deepcopy(base)
    captions = dict(base_captions)
    narration = base.get("default_language", "zh-TW")
    if not isinstance(narration, str) or not narration:
        raise invalid("核准上傳包的原旁白語言不正確，請重新送審")
    automatic = {narration, "zh-TW"}
    batch = _latest(rows, "languages")
    if batch is not None and _stamp(batch.created_at) <= _stamp(publish.created_at):
        batch = None  # A later approved publish already contains its own approved package.
    # The narration and zh-TW are automatic, independently of optional foreign choices.
    # Undecided legacy packages keep their complete original publish contents.
    if chosen:
        metadata["localizations"] = {}
        base_localizations = base.get("localizations")
        if (
            narration != "zh-TW"
            and isinstance(base_localizations, dict)
            and "zh-TW" in base_localizations
        ):
            metadata["localizations"]["zh-TW"] = _localized(base, "zh-TW")
        captions = {
            key: value for key, value in captions.items() if key in automatic
        }
    if batch is not None and current:
        if batch.status != "approved":
            raise invalid("最新語言包尚未核准，請完成語言審核後再送出")
        files = files_by_role(batch.files)
        manifest_file = files.get("languages_manifest")
        metadata_file = files.get("metadata")
        if (
            manifest_file is None
            or manifest_file["sha256"] != batch.content_sha256
            or metadata_file is None
        ):
            raise invalid("舊語言審核缺少可驗證的來源清單與 metadata，請重新送審")
        manifest = read_json(store, slug, manifest_file)
        translated = read_json(store, slug, metadata_file)
        if (
            type(manifest.get("schema_version")) is not int
            or manifest["schema_version"] != 1
            or manifest.get("slug") != slug
        ):
            raise invalid("語言來源清單版本或影片不符，請重新送審")
        # A batch approved with a language the video is no longer made in (zh-CN before
        # 2026-10-09) still matches once that language is ignored on both sides; its files stay
        # in the batch, verified like the rest, and are sent nowhere.
        choice = manifest.get("choice")
        stored = (
            without_retired_locales(choice.get("locales")) if isinstance(choice, dict) else None
        )
        if (
            not isinstance(choice, dict)
            or "decided_at" not in choice
            or stored != current
            or choices(stored) != stored
        ):
            raise invalid("語言選擇已變更，請依目前勾選內容重新送審")
        declared = without_retired_locales(translated.get("language_choice"))
        if declared != current or choices(declared) != declared:
            raise invalid("語言 metadata 不是目前勾選的語言，請重新送審")
        expected_files = files_by_role(manifest.get("files"))
        if expected_files != {
            role: item for role, item in files.items() if role != "languages_manifest"
        }:
            raise invalid("語言來源清單與核准附件不符，請重新送審")
        _source(manifest, rows, publish, base, translated, project)
        reported = manifest.get("locales")
        if (
            not isinstance(reported, dict)
            or set(reported) - RETIRED_LOCALES != set(current)
            or batch.payload.get("locales") != reported
        ):
            raise invalid("語言清單與審核項目不符，請重新送審")
        retired = {locale for locale in reported if locale in RETIRED_LOCALES}
        retired_roles = {
            f"{prefix}{locale}" for locale in retired for prefix in ("description_", "captions_")
        } | {f"dub_{locale.lower().replace('-', '_')}" for locale in retired}
        allowed_roles = {"metadata", "languages_manifest"}
        for locale, selection in current.items():
            parts = reported[locale]
            if not isinstance(parts, dict):
                raise invalid("語言項目格式不正確，請重新送審")
            for part, selected in selection.items():
                if not selected:
                    continue
                state = _state(parts.get(part))
                suffix = locale.lower().replace("-", "_") if part == "dub" else locale
                role = f"{('description' if part == 'metadata' else part)}_{suffix}"
                if state == "skipped":
                    if role in files:
                        raise invalid("略過的語言項目仍附有素材，請重新送審")
                    continue
                if part == "dub" and locale == narration:
                    raise invalid("原旁白語言必須明確略過重複配音，請重新送審")
                allowed_roles.add(role)
                item = files.get(role)
                if item is None:
                    raise invalid(f"核准的 {locale} {part} 缺少附件，請重新送審")
                if part == "metadata":
                    if locale == narration:
                        entry = _original(base)
                        if _original(translated) != entry:
                            raise invalid("原語言標題說明已不是核准的內容，請重新送審")
                    else:
                        entry = _localized(translated, locale)
                    expected = f"{entry['title']}\n\n{entry['description']}\n".encode()
                    if checked_file(store, slug, item) != expected:
                        raise invalid("語言 metadata 與核准的標題說明附件不同，請重新送審")
                    if locale != narration:
                        metadata["localizations"][locale] = entry
                elif part == "captions":
                    if item["content_type"] not in (
                        "text/plain",
                        "application/x-subrip",
                        "text/vtt",
                    ):
                        raise invalid("字幕附件格式不正確，請重新送審")
                    if locale == narration and item != base_captions.get(locale):
                        raise invalid("原旁白字幕已不是核准上傳包的時軸，請重新送審")
                    captions[locale] = item
                elif item["content_type"] not in ("audio/mp4", "audio/mpeg", "audio/wav"):
                    raise invalid("配音附件格式不正確，請重新送審")
        if set(files) - retired_roles != allowed_roles:
            raise invalid("語言包附有未選取或未完成的素材，請重新送審")
        if verify_files:
            for item in files.values():
                verify_file(store, slug, item)
        pin["languages"] = identity(batch)
    elif current:
        # Complete older publish packages remain useful; a selected but absent part cannot
        # silently become a successful one-language upload while its batch is still missing.
        declared = base.get("language_choice")
        if declared is not None and choices(declared) != current:
            raise invalid("上傳包的語言選擇已過期，請重新產生語言包")
        for locale, selection in current.items():
            if selection["metadata"]:
                if locale == narration:
                    _original(base)
                else:
                    metadata["localizations"][locale] = _localized(base, locale)
            if selection["captions"]:
                if locale in base_captions:
                    captions[locale] = base_captions[locale]
                else:
                    skipped = base.get("skipped_caption_locales")
                    reason = skipped.get(locale) if isinstance(skipped, dict) else None
                    if not reason or not isinstance(reason, str | list):
                        raise invalid(f"已選取的 {locale} 字幕尚未核准，請先完成語言包")
            if selection["dub"]:
                role = f"dub_{locale.lower().replace('-', '_')}"
                publish_files = files_by_role(publish.files)
                if locale == narration:
                    if role in publish_files:
                        raise invalid("原旁白語言附有重複配音，請重新送審")
                    continue
                skipped = base.get("skipped_dub_locales")
                reason = skipped.get(locale) if isinstance(skipped, dict) else None
                if role not in publish_files and not (
                    isinstance(reason, str) and reason.strip()
                ):
                    raise invalid(f"已選取的 {locale} 配音尚未核准，請先完成語言包")
    same_text = localizations(metadata) == localizations(base)
    if pin["languages"] is None and same_text and captions == base_captions:
        sha = publish.content_sha256
    else:
        sha = hashlib.sha256(
            json.dumps(pin, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
    return Composition(metadata, dict(sorted(captions.items())), sha, pin)
