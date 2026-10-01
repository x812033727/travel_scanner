"""Approved language batches cannot silently use an older original-only upload package."""

from __future__ import annotations

import copy
import json
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from app.models import VideoProject, VideoReview
from app.video_reviews.admin_service import review_store
from app.video_youtube import language_package, sync
from app.video_youtube.errors import Refused
from tests.test_video_youtube import Site, open_site
from tests.test_video_youtube_sync import SLUG, SRT, _entry, _package, _put

LOCALES = ("en", "ja", "ko", "zh-CN")
CHOICES = {locale: {"metadata": True, "captions": True, "dub": False} for locale in LOCALES}


@dataclass
class LanguageBatch:
    project_id: UUID
    publish_id: UUID
    final_id: UUID
    script_id: UUID | None
    review_id: UUID
    manifest: dict[str, Any]
    metadata: dict[str, Any]
    base_metadata: dict[str, Any]


async def _language_batch(
    site: Site,
    *,
    selected: dict[str, Any] | None = None,
    video_format: str = "slides",
    compilation: bool = False,
) -> LanguageBatch:
    """A real review-store fixture, shared with VPS tests; all four locales by default."""
    original = await _package(site)
    selected = copy.deepcopy(CHOICES if selected is None else selected)
    store = review_store(site.settings)
    async with site.factory() as session:
        project = await session.get(VideoProject, original.project_id)
        publish = await session.get(VideoReview, original.review_id)
        assert project is not None and publish is not None
        original_file = store.path(SLUG, original.metadata_sha)
        assert original_file is not None
        base = json.loads(original_file.read_bytes())
        base["localizations"] = {}
        base["language_choice"] = {}
        if compilation:
            base["compilation"] = True
        raw = json.dumps(base, ensure_ascii=False).encode()
        publish.content_sha256 = _put(store, raw)
        publish.files = [
            file
            for file in publish.files
            if file["role"] not in ("metadata", "captions_en", "captions_ja")
        ] + [_entry("metadata", publish.content_sha256, raw, "application/json")]
        publish.payload = {"locales": ["zh-TW"]}
        now = datetime.now(UTC)
        publish.created_at = now - timedelta(seconds=2)
        project.locales = selected
        project.locales_decided_at = now
        project.format = video_format
        final = VideoReview(
            id=uuid4(),
            project_id=project.id,
            gate="final",
            status="approved",
            content_sha256=original.final_sha,
            summary="approved cut",
            payload={},
            files=[],
            created_at=now - timedelta(seconds=3),
            decided_at=now - timedelta(seconds=3),
        )
        script = VideoReview(
            id=uuid4(),
            project_id=project.id,
            gate="script",
            status="approved",
            content_sha256="b" * 64,
            summary="approved script",
            payload={},
            files=[],
            created_at=now - timedelta(seconds=4),
            decided_at=now - timedelta(seconds=4),
        )
        translated = {**base, "language_choice": selected, "localizations": {}}
        files = []
        reported: dict[str, Any] = {}
        for locale, choice in selected.items():
            parts: dict[str, Any] = {}
            if choice.get("metadata"):
                entry = {"title": f"Title {locale}", "description": f"Description {locale}"}
                translated["localizations"][locale] = entry
                body = f"{entry['title']}\n\n{entry['description']}\n".encode()
                files.append(_entry(f"description_{locale}", _put(store, body), body, "text/plain"))
                parts["metadata"] = "ready"
            if choice.get("captions"):
                body = SRT + locale.encode()
                files.append(_entry(f"captions_{locale}", _put(store, body), body, "text/plain"))
                parts["captions"] = "ready"
            if choice.get("dub"):
                body = f"dub-{locale}".encode()
                role = f"dub_{locale.lower().replace('-', '_')}"
                files.append(_entry(role, _put(store, body), body, "audio/mp4"))
                parts["dub"] = "ready"
            reported[locale] = parts
        raw = json.dumps(translated, ensure_ascii=False).encode()
        files.append(_entry("metadata", _put(store, raw), raw, "application/json"))
        manifest = {
            "schema_version": 1,
            "slug": SLUG,
            "source": {
                "publish": language_package.identity(publish),
                "final": language_package.identity(final),
                "script": language_package.identity(script)
                if video_format == "drama" and not compilation
                else None,
                "branding_hash": None,
                "speech_hash": None if compilation else "1" * 16,
                "compilation_hash": "2" * 16 if compilation else None,
            },
            "choice": {"locales": selected, "decided_at": now.isoformat()},
            "locales": reported,
            "files": files,
        }
        raw = json.dumps(manifest, ensure_ascii=False).encode()
        sha = _put(store, raw)
        batch = VideoReview(
            id=uuid4(),
            project_id=project.id,
            gate="languages",
            status="approved",
            content_sha256=sha,
            summary="approved language batch",
            payload={"locales": reported},
            files=[*files, _entry("languages_manifest", sha, raw, "application/json")],
            created_at=now,
            decided_at=now,
        )
        session.add_all([final, batch])
        if video_format == "drama" and not compilation:
            session.add(script)
        await session.commit()
        return LanguageBatch(
            project.id,
            publish.id,
            final.id,
            script.id if video_format == "drama" and not compilation else None,
            batch.id,
            manifest,
            translated,
            base,
        )


async def _replace_manifest(
    site: Site,
    batch: LanguageBatch,
    mutate: Callable[[dict[str, Any]], None],
) -> None:
    manifest = copy.deepcopy(batch.manifest)
    mutate(manifest)
    raw = json.dumps(manifest, ensure_ascii=False).encode()
    sha = _put(review_store(site.settings), raw)
    async with site.factory() as session:
        row = await session.get(VideoReview, batch.review_id)
        assert row is not None
        row.content_sha256 = sha
        row.files = [*manifest["files"], _entry("languages_manifest", sha, raw, "application/json")]
        row.payload = {"locales": manifest["locales"]}
        await session.commit()
    batch.manifest = manifest


async def _composed(site: Site) -> sync.Package:
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        return sync.read_approved_package(
            review_store(site.settings),
            SLUG,
            project,
            await sync._project_reviews(session, project),
        )


@pytest.fixture
async def site(monkeypatch: pytest.MonkeyPatch, tmp_path: Any) -> AsyncIterator[Site]:
    async with open_site(monkeypatch, tmp_path) as value:
        yield value


async def test_latest_approved_batch_adds_four_languages_and_keeps_original_video_fields(
    site: Site,
) -> None:
    batch = await _language_batch(site)
    result = await _composed(site)
    assert set(result.metadata["localizations"]) == set(LOCALES)
    assert set(result.captions) == {"zh-TW", *LOCALES}
    for key, value in batch.base_metadata.items():
        if key != "localizations":
            assert result.metadata[key] == value
    assert result.final and result.final.sha256 == batch.base_metadata["final_sha256"]
    assert result.thumbnail is not None
    assert result.review_id == str(batch.publish_id)
    assert result.approval_pin["languages"]["review_id"] == str(batch.review_id)
    assert result.sha256 != result.approval_pin["publish"]["content_sha256"]
    assert (await _composed(site)).sha256 == result.sha256


@pytest.mark.parametrize("status", ["pending", "rejected", "superseded"])
async def test_latest_unapproved_batch_never_falls_back_to_older_approved(
    site: Site, status: str
) -> None:
    batch = await _language_batch(site)
    async with site.factory() as session:
        row = await session.get(VideoReview, batch.review_id)
        assert row is not None
        session.add(
            VideoReview(
                id=uuid4(),
                project_id=batch.project_id,
                gate="languages",
                status=status,
                content_sha256="c" * 64,
                summary="replacement",
                payload={},
                files=[],
                created_at=datetime.now(UTC) + timedelta(seconds=1),
            )
        )
        await session.commit()
    with pytest.raises(Refused, match="最新語言包尚未核准"):
        await _composed(site)


@pytest.mark.parametrize("gate", ["publish", "final", "script"])
async def test_source_approval_identity_must_be_the_current_one(site: Site, gate: str) -> None:
    batch = await _language_batch(site, video_format="drama" if gate == "script" else "slides")
    await _replace_manifest(
        site, batch, lambda manifest: manifest["source"][gate].update(review_id=str(uuid4()))
    )
    with pytest.raises(Refused):
        await _composed(site)


@pytest.mark.parametrize(
    "change",
    [
        "choice",
        "metadata",
        "caption",
        "final",
        "branding",
        "speech",
        "schema",
        "slug",
        "manifest",
        "size",
    ],
)
async def test_incompatible_or_tampered_language_package_is_refused(
    site: Site, change: str
) -> None:
    batch = await _language_batch(site)
    store = review_store(site.settings)
    if change == "choice":
        async with site.factory() as session:
            project = await session.get(VideoProject, batch.project_id)
            assert project is not None
            project.locales = {"en": CHOICES["en"]}
            await session.commit()
    elif change in ("metadata", "caption", "manifest"):
        role = {"metadata": "metadata", "caption": "captions_en", "manifest": "languages_manifest"}[
            change
        ]
        async with site.factory() as session:
            review = await session.get(VideoReview, batch.review_id)
            assert review is not None
            item = next(item for item in review.files if item["role"] == role)
        path = store.path(SLUG, item["sha256"])
        assert path is not None
        path.write_bytes(b"x" * item["size"])
    else:

        def mutate(manifest: dict[str, Any]) -> None:
            if change == "final":
                manifest["source"]["final"]["content_sha256"] = "f" * 64
            elif change == "branding":
                manifest["source"]["branding_hash"] = "f" * 64
            elif change == "speech":
                manifest["source"]["speech_hash"] = "not-a-hash"
            elif change == "schema":
                manifest["schema_version"] = True
            elif change == "slug":
                manifest["slug"] = "another-video"
            elif change == "size":
                manifest["files"][0]["size"] += 1

        await _replace_manifest(site, batch, mutate)
    with pytest.raises(Refused):
        await _composed(site)


async def test_legacy_separate_language_review_requires_resubmission(site: Site) -> None:
    batch = await _language_batch(site)
    async with site.factory() as session:
        row = await session.get(VideoReview, batch.review_id)
        assert row is not None
        row.files = [
            file for file in row.files if file["role"] not in ("metadata", "languages_manifest")
        ]
        await session.commit()
    with pytest.raises(Refused, match="舊語言審核"):
        await _composed(site)


async def test_missing_selected_batch_cannot_report_one_language_success(site: Site) -> None:
    batch = await _language_batch(site)
    async with site.factory() as session:
        row = await session.get(VideoReview, batch.review_id)
        assert row is not None
        await session.delete(row)
        await session.commit()
    with pytest.raises(Refused):
        await _composed(site)


async def test_original_only_and_complete_legacy_publish_keep_their_original_identity(
    site: Site,
) -> None:
    package = await _package(site)
    original = await _composed(site)
    assert original.sha256 == package.metadata_sha
    assert set(original.captions) == {"zh-TW", "en", "ja"}
    async with site.factory() as session:
        project = await session.get(VideoProject, package.project_id)
        assert project is not None
        project.locales = {locale: CHOICES[locale] for locale in ("en", "ja")}
        project.locales_decided_at = datetime.now(UTC)
        await session.commit()
    assert (await _composed(site)).sha256 == package.metadata_sha
    async with site.factory() as session:
        project = await session.get(VideoProject, package.project_id)
        assert project is not None
        project.locales = {}
        await session.commit()
    only = await _composed(site)
    assert only.metadata["localizations"] == {} and set(only.captions) == {"zh-TW"}


async def test_ready_parts_need_files_but_explicit_skipped_caption_is_allowed(site: Site) -> None:
    batch = await _language_batch(site)

    def skip(manifest: dict[str, Any]) -> None:
        manifest["locales"]["ko"]["captions"] = {
            "status": "skipped",
            "reason": "translation missing",
        }
        manifest["files"] = [file for file in manifest["files"] if file["role"] != "captions_ko"]

    await _replace_manifest(site, batch, skip)
    result = await _composed(site)
    assert set(result.captions) == {"zh-TW", "en", "ja", "zh-CN"}
    await _replace_manifest(
        site, batch, lambda manifest: manifest["locales"]["ko"].update(captions="ready")
    )
    with pytest.raises(Refused, match="缺少附件"):
        await _composed(site)


async def test_choice_decided_at_is_not_used_as_the_choice_version(site: Site) -> None:
    batch = await _language_batch(site)
    before = await _composed(site)
    async with site.factory() as session:
        project = await session.get(VideoProject, batch.project_id)
        assert project is not None
        project.locales_decided_at = datetime.now(UTC) + timedelta(days=1)
        await session.commit()
    assert (await _composed(site)).approval_pin == before.approval_pin


async def _replace_metadata(
    site: Site, batch: LanguageBatch, mutate: Callable[[dict[str, Any]], None]
) -> None:
    metadata = copy.deepcopy(batch.metadata)
    mutate(metadata)
    raw = json.dumps(metadata, ensure_ascii=False).encode()
    item = _entry("metadata", _put(review_store(site.settings), raw), raw, "application/json")

    def replace(manifest: dict[str, Any]) -> None:
        manifest["files"] = [file for file in manifest["files"] if file["role"] != "metadata"] + [
            item
        ]

    await _replace_manifest(site, batch, replace)
    batch.metadata = metadata


async def test_translated_package_cannot_replace_original_title_tags_or_privacy(site: Site) -> None:
    batch = await _language_batch(site)
    await _replace_metadata(
        site,
        batch,
        lambda meta: meta.update(
            title="Unapproved original title",
            description="Unapproved original description",
            tags=["new tags"],
            privacy_status="public",
            made_for_kids=True,
            thumbnail="new-thumbnail.jpg",
        ),
    )
    result = await _composed(site)
    for key in ("title", "description", "tags", "privacy_status", "made_for_kids", "thumbnail"):
        assert result.metadata.get(key) == batch.base_metadata.get(key)
    assert set(result.metadata["localizations"]) == set(LOCALES)


@pytest.mark.parametrize("change", ["choice", "text", "final", "default", "type"])
async def test_even_rehashed_approved_metadata_must_match_the_manifest_and_original(
    site: Site, change: str
) -> None:
    batch = await _language_batch(site)

    def mutate(metadata: dict[str, Any]) -> None:
        if change == "choice":
            metadata["language_choice"]["en"]["metadata"] = 1
        elif change == "text":
            metadata["localizations"]["en"]["title"] = (
                "Another approved text without its attachment"
            )
        elif change == "final":
            metadata["final_sha256"] = "f" * 64
        elif change == "default":
            metadata["default_language"] = "en"
        else:
            metadata["compilation"] = True

    await _replace_metadata(site, batch, mutate)
    with pytest.raises(Refused):
        await _composed(site)


async def test_chinese_dub_role_uses_the_producers_canonical_underscore_form(site: Site) -> None:
    selected = {"zh-CN": {"metadata": False, "captions": True, "dub": True}}
    await _language_batch(site, selected=selected)
    result = await _composed(site)
    assert result.metadata["localizations"] == {}
    assert set(result.captions) == {"zh-TW", "zh-CN"}


@pytest.mark.parametrize("status", ["pending", "rejected", "approved"])
async def test_newer_drama_script_cannot_be_borrowed_by_an_older_batch(
    site: Site, status: str
) -> None:
    batch = await _language_batch(site, video_format="drama")
    async with site.factory() as session:
        session.add(
            VideoReview(
                id=uuid4(),
                project_id=batch.project_id,
                gate="script",
                status=status,
                content_sha256="c" * 64,
                summary="new script",
                payload={},
                files=[],
                created_at=datetime.now(UTC) + timedelta(seconds=1),
            )
        )
        await session.commit()
    with pytest.raises(Refused):
        await _composed(site)


@pytest.mark.parametrize(("video_format", "compilation"), [("slides", False), ("drama", True)])
async def test_non_script_formats_require_null_and_ignore_residual_script_reviews(
    site: Site, video_format: str, compilation: bool
) -> None:
    batch = await _language_batch(site, video_format=video_format, compilation=compilation)
    async with site.factory() as session:
        stale = VideoReview(
            id=uuid4(),
            project_id=batch.project_id,
            gate="script",
            status="rejected",
            content_sha256="c" * 64,
            summary="residual old script",
            payload={},
            files=[],
            created_at=datetime.now(UTC) + timedelta(seconds=1),
        )
        session.add(stale)
        await session.commit()
    assert batch.manifest["source"]["script"] is None
    assert set((await _composed(site)).captions) == {"zh-TW", *LOCALES}
    await _replace_manifest(
        site,
        batch,
        lambda manifest: manifest["source"].update(script=language_package.identity(stale)),
    )
    with pytest.raises(Refused):
        await _composed(site)


@pytest.mark.parametrize("missing", ["manifest_identity", "approved_review"])
async def test_drama_language_batch_requires_its_script_approval(site: Site, missing: str) -> None:
    batch = await _language_batch(site, video_format="drama")
    assert set((await _composed(site)).captions) == {"zh-TW", *LOCALES}
    if missing == "manifest_identity":
        await _replace_manifest(
            site, batch, lambda manifest: manifest["source"].update(script=None)
        )
    else:
        async with site.factory() as session:
            script = await session.get(VideoReview, batch.script_id)
            assert script is not None
            await session.delete(script)
            await session.commit()
    with pytest.raises(Refused):
        await _composed(site)
