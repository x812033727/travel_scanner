"""The language batch the video tool sends is the one YouTube sync composes.

``fixtures/video_language_contract/`` holds what the real producer sent: ``package`` and
``review-push --gate languages`` run on fixture videos against a double of the review site, and
the site's rows and stored files are kept as they are
(``tools/video/review/language-contract.test.mjs`` fails while the copy is not what the producer
sends now). Here they go into the review store and the database and through the real consumer,
files verified, so a manifest the consumer cannot read fails here instead of at an upload
(docs/videos/APPROVED-LANGUAGE-PACKAGE.md).
"""

from __future__ import annotations

import copy
import json
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from app.models import VideoProject, VideoReview
from app.video_reviews.admin_service import review_store
from app.video_youtube import sync
from app.video_youtube.errors import Refused
from tests.test_video_youtube import Site, open_site

CONTRACT = Path(__file__).parent / "fixtures" / "video_language_contract"
CASES = sorted(path.name for path in CONTRACT.iterdir() if path.is_dir())
# What each case's batch adds to its confirmation: the translated titles YouTube gets, and the
# caption tracks (the narration's and zh-TW's always come from the confirmation itself).
EXPECTED = {
    "zh-tw-narration": ({"en", "ko"}, {"zh-TW", "en", "ja", "ko"}),
    "zh-tw-dubbed": (set(), {"zh-TW", "ja"}),
    "en-narration": ({"zh-TW", "ja"}, {"en", "zh-TW", "ja"}),
}


def _record(name: str) -> dict[str, Any]:
    value = json.loads((CONTRACT / name / "case.json").read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _stamp(value: str | None) -> datetime | None:
    return None if value is None else datetime.fromisoformat(value)


def _row(record: dict[str, Any], gate: str) -> dict[str, Any]:
    row = next(row for row in record["reviews"] if row["gate"] == gate)
    assert isinstance(row, dict)
    return row


@dataclass
class Contract:
    name: str
    slug: str
    project_id: UUID
    record: dict[str, Any]

    @property
    def batch(self) -> dict[str, Any]:
        return _row(self.record, "languages")


async def _load(
    site: Site, name: str, mutate: Callable[[dict[str, Any]], None] | None = None
) -> Contract:
    """The case's stored files and rows, as the site held them after the batch."""
    record = _record(name)
    if mutate is not None:
        mutate(record)
    slug = record["project"]["slug"]
    store = review_store(site.settings)
    for file in sorted((CONTRACT / name / "files").iterdir()):
        body = file.read_bytes()
        store.put_part(slug, file.name, index=0, count=1, size=len(body), data=body)
    stamp = _stamp(record["reviews"][-1]["created_at"])
    assert stamp is not None
    project = VideoProject(
        id=uuid4(),
        slug=slug,
        title=slug,
        format=record["project"]["format"],
        stage="done",
        checklist=[],
        last_synced_at=stamp,
        locales=record["project"]["locales"],
        locales_decided_at=_stamp(record["project"]["locales_decided_at"]),
    )
    rows = [
        VideoReview(
            id=UUID(row["id"]),
            project_id=project.id,
            gate=row["gate"],
            subject=row["subject"],
            content_sha256=row["content_sha256"],
            revision=row.get("revision", 0),
            summary=row["summary"],
            payload=row["payload"],
            files=row["files"],
            status=row["status"],
            choice=row["choice"],
            note=row["note"],
            decided_at=_stamp(row["decided_at"]),
            created_at=_stamp(row["created_at"]),
            updated_at=_stamp(row["created_at"]),
        )
        for row in record["reviews"]
    ]
    async with site.factory() as session:
        session.add(project)
        await session.flush()
        session.add_all(rows)
        await session.commit()
    return Contract(name, slug, project.id, record)


async def _composed(site: Site, contract: Contract) -> sync.Package:
    async with site.factory() as session:
        project = await session.scalar(
            select(VideoProject).where(VideoProject.slug == contract.slug)
        )
        assert project is not None
        rows = await sync._project_reviews(session, project)
        return sync.read_approved_package(review_store(site.settings), contract.slug, project, rows)


def _stored(contract: Contract, sha256: str) -> bytes:
    return (CONTRACT / contract.name / "files" / sha256).read_bytes()


@pytest.fixture
async def site(monkeypatch: pytest.MonkeyPatch, tmp_path: Any) -> AsyncIterator[Site]:
    async with open_site(monkeypatch, tmp_path) as value:
        yield value


def test_every_case_has_its_expectation() -> None:
    assert set(CASES) == set(EXPECTED)


@pytest.mark.parametrize("name", CASES)
async def test_the_producers_batch_composes_with_the_confirmation_it_names(
    site: Site, name: str
) -> None:
    contract = await _load(site, name)
    batch, publish = contract.batch, _row(contract.record, "publish")
    result = await _composed(site, contract)
    assert result.review_id == publish["id"]
    assert result.approval_pin["publish"] == {
        "review_id": publish["id"],
        "content_sha256": publish["content_sha256"],
    }
    assert result.approval_pin["languages"] == {
        "review_id": batch["id"],
        "content_sha256": batch["content_sha256"],
    }
    assert result.approval_pin["choice"] == contract.record["project"]["locales"]
    titles, captions = EXPECTED[name]
    assert set(result.metadata["localizations"]) == titles
    assert set(result.captions) == captions
    # The titles are the batch's own metadata; the original fields stay the confirmation's.
    translated = json.loads(_stored(contract, _sha_of(batch, "metadata")))
    approved = json.loads(_stored(contract, publish["content_sha256"]))
    for locale in titles - {"zh-TW"}:
        assert result.metadata["localizations"][locale] == translated["localizations"][locale]
    for key in ("title", "description", "tags", "default_language", "final_sha256"):
        assert result.metadata[key] == approved[key]
    # Each caption track is the exact file sent: the batch's, or the confirmation's own.
    for locale, item in result.captions.items():
        sent = _file_of(batch, f"captions_{locale}") or _file_of(publish, f"captions_{locale}")
        assert sent is not None and item.sha256 == sent["sha256"], locale
    assert (await _composed(site, contract)).sha256 == result.sha256


def _file_of(row: dict[str, Any], role: str) -> dict[str, Any] | None:
    return next((item for item in row["files"] if item["role"] == role), None)


def _sha_of(row: dict[str, Any], role: str) -> str:
    item = _file_of(row, role)
    assert item is not None
    return str(item["sha256"])


def _changed_choice(record: dict[str, Any]) -> None:
    first = next(iter(record["project"]["locales"].values()))
    first["metadata"] = not first["metadata"]


def _added_language(record: dict[str, Any]) -> None:
    record["project"]["locales"]["ko"] = {"metadata": False, "captions": True, "dub": False}


@pytest.mark.parametrize("name", CASES)
@pytest.mark.parametrize("change", [_changed_choice, _added_language], ids=["part", "language"])
async def test_a_choice_changed_after_the_batch_is_refused(
    site: Site, name: str, change: Callable[[dict[str, Any]], None]
) -> None:
    contract = await _load(site, name, change)
    with pytest.raises(Refused) as caught:
        await _composed(site, contract)
    assert caught.value.code == "video_youtube_languages_invalid"


ATTACHMENTS = [
    (name, item["role"]) for name in CASES for item in _row(_record(name), "languages")["files"]
]


@pytest.mark.parametrize(("name", "role"), ATTACHMENTS)
async def test_an_attachment_whose_stored_bytes_changed_is_refused(
    site: Site, name: str, role: str
) -> None:
    contract = await _load(site, name)
    sha256 = _sha_of(contract.batch, role)
    path = review_store(site.settings).path(contract.slug, sha256)
    assert path is not None
    body = bytearray(path.read_bytes())
    body[-2] ^= 1  # same size, other bytes
    path.write_bytes(bytes(body))
    with pytest.raises(Refused) as caught:
        await _composed(site, contract)
    assert caught.value.code == "video_youtube_languages_invalid"


def _later(record: dict[str, Any], gate: str, *, status: str, **fields: Any) -> dict[str, Any]:
    """A newer review of ``gate``, sent after the batch."""
    source = copy.deepcopy(_row(record, gate))
    stamp = _stamp(record["reviews"][0]["created_at"])
    assert stamp is not None
    source.update(
        id=str(uuid4()),
        status=status,
        created_at=(stamp + timedelta(minutes=1)).isoformat(),
        decided_at=None if status == "pending" else (stamp + timedelta(minutes=2)).isoformat(),
        **fields,
    )
    record["reviews"].insert(0, source)
    return source


SOURCE_CHANGES = {
    "pending final": lambda record: _later(
        record, "final", status="pending", content_sha256="e" * 64
    ),
    "new approved final": lambda record: _later(
        record, "final", status="approved", content_sha256="e" * 64
    ),
}


@pytest.mark.parametrize("name", CASES)
@pytest.mark.parametrize("change", SOURCE_CHANGES.values(), ids=SOURCE_CHANGES.keys())
async def test_a_batch_older_than_its_final_cut_is_refused(
    site: Site, name: str, change: Callable[[dict[str, Any]], None]
) -> None:
    contract = await _load(site, name, change)
    with pytest.raises(Refused):
        await _composed(site, contract)


def _confirmed_again(record: dict[str, Any]) -> None:
    """The confirmation the worker sends after the batch while the package changed: the package
    written for the choice (the batch's own metadata.json, titles and captions) with the cut."""
    batch, publish = _row(record, "languages"), _row(record, "publish")
    sent = [item for item in batch["files"] if item["role"] != "languages_manifest"]
    own = {item["role"] for item in sent}
    files = [item for item in publish["files"] if item["role"] not in own] + [
        item for item in sent if not item["role"].startswith("dub_")
    ]
    captions = sorted(
        item["role"].removeprefix("captions_")
        for item in files
        if item["role"].startswith("captions_")
    )
    _later(
        record,
        "publish",
        status="approved",
        content_sha256=_sha_of(batch, "metadata"),
        files=files,
        payload={**publish["payload"], "locales": captions},
    )


@pytest.mark.parametrize("name", CASES)
async def test_a_confirmation_sent_after_the_batch_is_read_from_its_own_package(
    site: Site, name: str
) -> None:
    contract = await _load(site, name, _confirmed_again)
    confirmation = contract.record["reviews"][0]
    if name == "zh-tw-dubbed":
        # A confirmation carries no dub track, and the batch that does is older than it: filed as
        # tasks/open/2026-10-07-the-worker-sends-a-language-batch.md.
        with pytest.raises(Refused, match="配音尚未核准"):
            await _composed(site, contract)
        return
    result = await _composed(site, contract)
    assert result.review_id == confirmation["id"]
    assert result.approval_pin["languages"] is None
    titles, captions = EXPECTED[name]
    assert set(result.metadata["localizations"]) == titles
    assert set(result.captions) == captions
