"""Verify an independently approved, unselected repository-locale preservation.

The localization baseline intentionally keeps the live published document as the
translation source and concurrency pin.  This receipt can preserve one reviewed
repository description in the full pack without selecting, importing, or publishing
that locale.
"""

import copy
import hashlib
import re
from datetime import datetime

from app.guides.schemas import GuideDocument
from app.guides.service import document_hash

HASH = re.compile(r"[0-9a-f]{64}\Z")
GIT_HASH = re.compile(r"[0-9a-f]{40}\Z")
FIELDS = {
    "schema_version",
    "status",
    "reviewer",
    "reviewed_at",
    "reason",
    "evidence_sha256",
    "slug",
    "article_id",
    "article_version",
    "locale",
    "locale_id",
    "locale_version",
    "published_version",
    "live_published_sha256",
    "live_draft_sha256",
    "baseline_source_sha256",
    "baseline_locale_sha256",
    "repo_commit",
    "repo_pack_path",
    "repo_pack_git_blob_sha1",
    "repo_pack_sha256",
    "repo_document_sha256",
    "changes",
}


def normalized(document):
    return GuideDocument.model_validate(document).model_dump(mode="json")


def git_blob_sha1(raw):
    header = f"blob {len(raw)}\0".encode()
    return hashlib.sha1(header + raw).hexdigest()


def verify_review(
    review, baseline, article, locale, repository_document, repository_pack_raw
):
    """Return the closed manifest binding after recomputing every receipt assertion."""
    if not isinstance(review, dict) or set(review) != FIELDS:
        raise ValueError("Invalid repository preservation review schema")
    if type(review["schema_version"]) is not int or review["schema_version"] != 1:
        raise ValueError("Invalid repository preservation review schema version")
    if review["status"] != "PASS":
        raise ValueError("Repository preservation lacks independent PASS review")
    if not all(
        isinstance(review[key], str) and review[key].strip()
        for key in (
            "reviewer",
            "reviewed_at",
            "reason",
            "slug",
            "article_id",
            "locale",
            "locale_id",
            "repo_pack_path",
        )
    ):
        raise ValueError("Repository preservation identity and review details required")
    try:
        reviewed_at = datetime.fromisoformat(
            review["reviewed_at"].replace("Z", "+00:00")
        )
    except ValueError as error:
        raise ValueError(
            "Repository preservation review time must be ISO 8601"
        ) from error
    if reviewed_at.tzinfo is None:
        raise ValueError("Repository preservation review time must include a timezone")
    if not all(
        type(review[key]) is int and review[key] >= 1
        for key in ("article_version", "locale_version", "published_version")
    ):
        raise ValueError("Repository preservation versions must be positive integers")
    if not all(
        isinstance(review[key], str) and HASH.fullmatch(review[key])
        for key in (
            "evidence_sha256",
            "live_published_sha256",
            "live_draft_sha256",
            "baseline_source_sha256",
            "baseline_locale_sha256",
            "repo_pack_sha256",
            "repo_document_sha256",
        )
    ) or not all(
        isinstance(review[key], str) and GIT_HASH.fullmatch(review[key])
        for key in ("repo_commit", "repo_pack_git_blob_sha1")
    ):
        raise ValueError("Invalid repository preservation hash")

    pinned = article.get("database")
    if pinned is None or article.get("status") != "published":
        raise ValueError("Repository preservation requires an existing public article")
    old = pinned["locales"].get(locale)
    if old is None or locale not in article["published_locales"]:
        raise ValueError(
            "Repository preservation requires an existing published locale"
        )
    if not (
        old["version"] == old["published_version"]
        and old["draft_sha256"] == old["published_sha256"]
    ):
        raise ValueError("Repository preservation requires a clean published locale")

    baseline_document = normalized(article["locale_documents"][locale])
    source_document = normalized(article["source_document"])
    repository_document = normalized(repository_document)
    pack_sha256 = hashlib.sha256(repository_pack_raw).hexdigest()
    pack_blob = git_blob_sha1(repository_pack_raw)
    if not (
        review["slug"] == article["slug"]
        and review["article_id"] == pinned["id"]
        and review["article_version"] == pinned["version"]
        and review["locale"] == locale
        and review["locale_id"] == old["id"]
        and review["locale_version"] == old["version"]
        and review["published_version"] == old["published_version"]
        and review["live_published_sha256"] == old["published_sha256"]
        and review["live_draft_sha256"] == old["draft_sha256"]
        and review["baseline_source_sha256"] == article["source_sha256"]
        and review["baseline_locale_sha256"] == document_hash(baseline_document)
        and review["repo_commit"] == baseline.get("repo_commit")
        and review["repo_pack_path"] == article["pack_path"]
        and review["repo_pack_sha256"] == article["pack_sha256"] == pack_sha256
        and review["repo_pack_git_blob_sha1"] == pack_blob
        and review["repo_document_sha256"] == document_hash(repository_document)
    ):
        raise ValueError(
            "Repository preservation does not match pinned article or pack"
        )
    if document_hash(source_document) != article["source_sha256"]:
        raise ValueError("Repository preservation baseline source hash mismatch")
    if locale == article["source_locale"] and source_document != baseline_document:
        raise ValueError(
            "Repository preservation source locale differs from live source"
        )
    if review["baseline_locale_sha256"] != old["published_sha256"]:
        raise ValueError("Repository preservation baseline is not the live publication")

    changes = review["changes"]
    if not isinstance(changes, list) or len(changes) != 1:
        raise ValueError("Repository preservation currently allows only /description")
    change = changes[0]
    if not isinstance(change, dict) or set(change) != {"pointer", "before", "after"}:
        raise ValueError("Repository preservation change must pin pointer/before/after")
    if change["pointer"] != "/description":
        raise ValueError("Repository preservation currently allows only /description")
    if (
        change["before"] != baseline_document["description"]
        or change["after"] != repository_document["description"]
        or change["before"] == change["after"]
    ):
        raise ValueError("Repository preservation description binding mismatch")
    rebuilt = copy.deepcopy(baseline_document)
    rebuilt["description"] = change["after"]
    if rebuilt != repository_document:
        raise ValueError("Repository preservation includes unreviewed document changes")

    return {
        "from_live_document_sha256": review["baseline_locale_sha256"],
        "to_repository_document_sha256": review["repo_document_sha256"],
        "repo_commit": review["repo_commit"],
        "repo_pack_git_blob_sha1": review["repo_pack_git_blob_sha1"],
        "repo_pack_sha256": review["repo_pack_sha256"],
    }
