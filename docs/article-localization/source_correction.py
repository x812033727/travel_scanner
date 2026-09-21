"""Verify an independently approved, exact published-document correction.

The receipt carries the old published document so its pointer diff can be checked
without trusting a prose summary or replacing an editor's unmerged draft.
"""

import copy
import re

from app.guides.schemas import GuideDocument
from app.guides.service import document_hash

HASH = re.compile(r"[0-9a-f]{64}\Z")
FIELDS = {
    "schema_version",
    "approved",
    "reviewer",
    "reason",
    "evidence_sha256",
    "slug",
    "article_id",
    "article_version",
    "locale",
    "locale_version",
    "published_version",
    "published_sha256",
    "draft_sha256",
    "corrected_sha256",
    "old_document",
    "changes",
    "assets",
}


def valid_hash(value):
    return isinstance(value, str) and HASH.fullmatch(value) is not None


def normalized(document):
    return GuideDocument.model_validate(document).model_dump(mode="json")


def pointer_parts(pointer):
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("Correction needs an absolute JSON pointer")
    parts = pointer[1:].split("/")
    if any("~" in re.sub(r"~[01]", "", part) for part in parts):
        raise ValueError("Invalid correction JSON pointer escape")
    return [part.replace("~1", "/").replace("~0", "~") for part in parts]


def apply_change(document, change):
    if not isinstance(change, dict) or set(change) != {"pointer", "before", "after"}:
        raise ValueError("Correction change must include exact pointer/before/after")
    current = document
    for part in pointer_parts(change["pointer"])[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    leaf = pointer_parts(change["pointer"])[-1]
    key = int(leaf) if isinstance(current, list) else leaf
    if current[key] != change["before"]:
        raise ValueError("Correction before value does not match published document")
    current[key] = change["after"]


def verify_review(review, article, locale, corrected_document, asset_hashes):
    """Return canonical old/new hashes after checking every authorization binding."""
    if not isinstance(review, dict) or set(review) != FIELDS:
        raise ValueError("Invalid source correction review schema")
    if review["schema_version"] != 1 or review["approved"] is not True:
        raise ValueError("Source correction lacks independent approval")
    if not all(
        isinstance(review[key], str) and review[key].strip() for key in ("reviewer", "reason")
    ):
        raise ValueError("Source correction reviewer and reason required")
    if not all(
        valid_hash(review[key])
        for key in ("evidence_sha256", "published_sha256", "draft_sha256", "corrected_sha256")
    ):
        raise ValueError("Invalid source correction hash")
    pinned = article.get("database")
    if pinned is None or article.get("status") != "published":
        raise ValueError("Source correction requires an existing public article")
    old = pinned["locales"].get(locale)
    if old is None or locale not in article["published_locales"]:
        raise ValueError("Source correction requires an existing published locale")
    if not (
        review["slug"] == article["slug"]
        and review["article_id"] == pinned["id"]
        and review["article_version"] == pinned["version"]
        and review["locale"] == locale
        and review["locale_version"] == old["version"]
        and review["published_version"] == old["published_version"]
        and review["published_sha256"] == old["published_sha256"]
        and review["draft_sha256"] == old["draft_sha256"]
    ):
        raise ValueError("Source correction does not match pinned article/version")
    if not (
        old["version"] == old["published_version"]
        and old["draft_sha256"] == old["published_sha256"]
    ):
        raise ValueError("Source correction would overwrite an unpublished edit")
    old_document = normalized(review["old_document"])
    if document_hash(old_document) != review["published_sha256"]:
        raise ValueError("Old source correction document hash mismatch")
    wanted = normalized(corrected_document)
    if document_hash(wanted) != review["corrected_sha256"]:
        raise ValueError("Corrected source document hash mismatch")
    changes = review["changes"]
    if not isinstance(changes, list) or not changes:
        raise ValueError("Source correction needs exact nonempty changes")
    pointers = [change.get("pointer") for change in changes if isinstance(change, dict)]
    if len(pointers) != len(changes) or len(set(pointers)) != len(pointers):
        raise ValueError("Repeated or malformed source correction pointers")
    decoded = [pointer_parts(pointer) for pointer in pointers]
    for index, left in enumerate(decoded):
        for right in decoded[index + 1 :]:
            if left == right[: len(left)] or right == left[: len(right)]:
                raise ValueError("Overlapping source correction pointers")
    rebuilt = copy.deepcopy(old_document)
    try:
        for change in changes:
            apply_change(rebuilt, change)
    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise ValueError("Invalid exact source correction change") from error
    if rebuilt != wanted:
        raise ValueError("Source correction includes unreviewed document changes")
    assets = review["assets"]
    if not isinstance(assets, list):
        raise ValueError("Invalid source correction assets")
    paths = set()
    for asset in assets:
        if not isinstance(asset, dict) or set(asset) != {"path", "before_sha256", "after_sha256"}:
            raise ValueError("Invalid source correction asset binding")
        path = asset["path"]
        if (
            not isinstance(path, str)
            or not path.startswith("public/guides/")
            or ".." in path.split("/")
            or path in paths
            or not valid_hash(asset["before_sha256"])
            or not valid_hash(asset["after_sha256"])
            or asset_hashes.get(path) != asset["after_sha256"]
        ):
            raise ValueError("Source correction asset hash/path mismatch")
        paths.add(path)
    return {
        "from_published_sha256": review["published_sha256"],
        "to_document_sha256": review["corrected_sha256"],
    }
