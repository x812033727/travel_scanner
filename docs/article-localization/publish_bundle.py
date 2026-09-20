"""Publish one reviewed localization bundle through the existing editorial services.

Run in the deployed API environment with durable state, one phase at a time:
  python publish_bundle.py --bundle /bundle --baseline /baseline.json \
    --manifest-sha256 REVIEWED_SHA256 --deployed-root /app \
    --state-dir /durable/bundle-id dry-run
Then run drafts, publish-articles, publish-hubs with the same arguments. No SSH or
automatic execution. The CLI requires PostgreSQL; tests exercise SQLite separately.

Manifest schema 1: baseline_sha256, articles (1..20) with slug, pack_path,
pack_sha256, locales, publish_locales, hub, optional requires (slug, locale,
document_sha256); assets with path and sha256. Paths are relative to --bundle.
Only selected locales are written. Existing documents may change image src only;
repository-only articles become five private drafts, never publications.

Each existing admin-service operation commits once. A durable intent precedes it;
resume accepts only the exact version/hash/action/actor transition, including an
uncertain commit. Database guards run under SERIALIZABLE and row locks, sharing
advisory lock 817420260914 with the existing editorial release driver.
"""

from __future__ import annotations

import argparse
import asyncio
import copy
import hashlib
import json
import os
import re
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from uuid import UUID, uuid4

from app.auth.service import cached_admin_capabilities, user_is_suspended
from app.config import get_settings
from app.db import engine
from app.guides import admin_service
from app.guides.content_pack import ArticlePack
from app.guides.models import GuideArticle, GuideArticleLocale, GuideArticleRevision
from app.guides.schemas import (
    ArticleCreate,
    ArticleUpdate,
    DraftWrite,
    GuideDocument,
    PublishWrite,
)
from app.guides.service import _topics_for, document_hash
from app.i18n import LOCALES
from app.models import AdminAuditLog, User
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

PHASES = ("dry-run", "drafts", "publish-articles", "publish-hubs")
LOCK_KEY = 817420260914
HASH = re.compile(r"[0-9a-f]{64}")


class Refused(RuntimeError):
    """A safe operator message: no document, email, SQL parameters or credentials."""


def require(condition, message):
    if not condition:
        raise Refused(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def normalized(document):
    return GuideDocument.model_validate(document).model_dump(mode="json")


def stamp():
    return datetime.now(UTC).isoformat()


def safe_path(root, relative):
    require(isinstance(relative, str) and bool(relative), "Missing bundle path")
    rel = PurePosixPath(relative)
    require(
        not rel.is_absolute()
        and ".." not in rel.parts
        and "\\" not in relative
        and ":" not in relative,
        "Unsafe bundle path",
    )
    path = (root / str(rel)).resolve()
    require(path.is_relative_to(root.resolve()), "Bundle path escapes its root")
    return path


def image_sources(document):
    sources = [document.hero.src] if document.hero else []
    return sources + [block.src for block in document.blocks if block.type == "image"]


def without_image_sources(document):
    result = normalized(document)
    if result.get("hero"):
        result["hero"]["src"] = "<reviewed-image>"
    for block in result["blocks"]:
        if block["type"] == "image":
            block["src"] = "<reviewed-image>"
    return result


def metadata(pack):
    return {
        "kind": pack.kind,
        "destination_id": pack.destination_id,
        "topics": sorted(pack.topics),
        "valid_until": str(pack.valid_until) if pack.valid_until else None,
        "featured": pack.featured,
        "display_order": pack.display_order,
    }


@dataclass
class Bundle:
    root: Path
    baseline_path: Path
    manifest_sha256: str
    manifest: dict
    baseline: dict
    packs: dict

    @property
    def entries(self):
        return self.manifest["articles"]

    @property
    def slugs(self):
        return [entry["slug"] for entry in self.entries]


def canonical_sha256(value):
    return sha(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    )


def verify_bundle(root: Path, baseline_path: Path, pinned_sha: str) -> Bundle:
    require(bool(HASH.fullmatch(pinned_sha)), "Supply the reviewed manifest SHA256")
    raw = (root / "release-manifest.json").read_bytes()
    require(sha(raw) == pinned_sha, "Manifest SHA256 mismatch")
    manifest = json.loads(raw)
    require(manifest.get("schema_version") == 1, "Unsupported manifest schema")
    baseline_raw = baseline_path.read_bytes()
    require(
        sha(baseline_raw) == manifest.get("baseline_sha256"), "Baseline SHA256 mismatch"
    )
    baseline_doc = json.loads(baseline_raw)
    require(baseline_doc.get("schema_version") == 1, "Unsupported baseline schema")
    baseline = {row["slug"]: row for row in baseline_doc["articles"]}
    entries = manifest.get("articles")
    require(
        isinstance(entries, list) and 1 <= len(entries) <= 20,
        "Bundle needs 1..20 articles",
    )
    require(
        len({row["slug"] for row in entries}) == len(entries),
        "Repeated article in bundle",
    )
    assets = manifest.get("assets")
    require(isinstance(assets, list), "Manifest assets must be a list")
    asset_hashes = {row["path"]: row["sha256"] for row in assets}
    require(len(asset_hashes) == len(assets), "Repeated asset in bundle")
    for path, expected in asset_hashes.items():
        require(path.startswith("public/guides/"), "Unexpected asset location")
        require(
            sha(safe_path(root, path).read_bytes()) == expected, "Asset SHA256 mismatch"
        )
    packs = {}
    used_assets = set()
    for entry in entries:
        slug = entry["slug"]
        require(slug in baseline, "Article is outside the pinned baseline")
        source = baseline[slug]
        pack_path = entry["pack_path"]
        require(pack_path == f"packs/{slug}.json", f"{slug}: unexpected pack path")
        pack_raw = safe_path(root, pack_path).read_bytes()
        require(sha(pack_raw) == entry["pack_sha256"], f"{slug}: pack SHA256 mismatch")
        pack = ArticlePack.model_validate_json(pack_raw)
        require(pack.slug == slug, f"{slug}: pack slug mismatch")
        require(
            set(pack.locales) == set(LOCALES),
            f"{slug}: full five-language pack required",
        )
        wanted_metadata = {key: source["metadata"][key] for key in metadata(pack)}
        wanted_metadata["topics"] = sorted(wanted_metadata["topics"])
        require(
            metadata(pack) == wanted_metadata, f"{slug}: classification/order changed"
        )
        require(
            pack.valid_until is None or pack.valid_until >= datetime.now(UTC).date(),
            f"{slug}: expired article cannot be imported by this release",
        )
        selected, publish = entry.get("locales"), entry.get("publish_locales")
        require(
            isinstance(selected, list)
            and bool(selected)
            and len(set(selected)) == len(selected)
            and set(selected) <= set(LOCALES),
            f"{slug}: invalid selected locales",
        )
        require(
            isinstance(publish, list)
            and len(set(publish)) == len(publish)
            and set(publish) <= set(selected),
            f"{slug}: invalid publish locales",
        )
        require(type(entry.get("hub")) is bool, f"{slug}: explicit hub flag required")
        require(
            document_hash(normalized(source["source_document"]))
            == source["source_sha256"],
            f"{slug}: source document hash mismatch",
        )
        publication = source.get("publication_locales")
        require(
            isinstance(publication, list)
            and len(set(publication)) == len(publication)
            and set(publication) <= set(LOCALES),
            f"{slug}: baseline publication locales are required",
        )
        if source["database"] is None:
            require(
                set(selected) == set(LOCALES) and not publish and not publication,
                f"{slug}: repository-only article must remain five private drafts",
            )
        else:
            require(
                source["status"] == "published",
                f"{slug}: baseline article is not public",
            )
            require(
                set(publish) <= set(publication) | set(source["published_locales"]),
                f"{slug}: publishing an existing unpublished draft is not authorized",
            )
        for locale, old_document in source["locale_documents"].items():
            wanted = pack.locales[locale].model_dump(mode="json")
            if locale not in selected:
                require(
                    wanted == normalized(old_document),
                    f"{slug}:{locale}: unselected text changed",
                )
            else:
                require(
                    without_image_sources(wanted)
                    == without_image_sources(old_document),
                    f"{slug}:{locale}: existing document changes more than image src",
                )
        for locale in selected:
            for src in image_sources(pack.locales[locale]):
                asset = "public/" + src.lstrip("/")
                require(
                    asset in asset_hashes,
                    f"{slug}:{locale}: image absent from manifest",
                )
                used_assets.add(asset)
        requires = entry.get("requires", [])
        require(isinstance(requires, list), f"{slug}: invalid hub dependencies")
        require(
            entry["hub"] or not requires,
            f"{slug}: only a hub can require other articles",
        )
        require(
            not (entry["hub"] and publish) or bool(requires),
            f"{slug}: published hub needs explicit article dependencies",
        )
        for dependency in requires:
            require(
                dependency.get("slug") in baseline
                and dependency.get("locale") in LOCALES
                and bool(HASH.fullmatch(dependency.get("document_sha256", ""))),
                f"{slug}: invalid hub dependency",
            )
        packs[slug] = pack
    # Editable vector sources accompany localized raster heroes. Only a same-stem SVG
    # of a directly referenced, hash-pinned raster is allowed as an extra asset.
    companions = {
        str(PurePosixPath(path).with_suffix(".svg"))
        for path in used_assets
        if PurePosixPath(path).suffix in {".jpg", ".png", ".webp"}
    }
    require(
        set(asset_hashes) <= used_assets | companions,
        "Manifest has unrelated or unused assets",
    )
    return Bundle(root, baseline_path, pinned_sha, manifest, baseline, packs)


def verify_deployed(bundle: Bundle, deployed_root: Path):
    """Require the installed pack and assets to be the exact reviewed bundle bytes."""
    root = deployed_root.resolve()
    require(root.is_dir(), "Deployed root is absent")
    for entry in bundle.entries:
        path = safe_path(root, bundle.baseline[entry["slug"]]["pack_path"])
        require(path.is_file(), f"{entry['slug']}: deployed content pack is absent")
        require(
            sha(path.read_bytes()) == entry["pack_sha256"],
            f"{entry['slug']}: deployed content pack SHA256 mismatch",
        )
    for asset in bundle.manifest["assets"]:
        path = safe_path(root, f"apps/web/{asset['path']}")
        require(path.is_file(), f"{asset['path']}: deployed asset is absent")
        require(
            sha(path.read_bytes()) == asset["sha256"],
            f"{asset['path']}: deployed asset SHA256 mismatch",
        )


@contextmanager
def journal_lock(directory):
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ".lock").open("a+b") as handle:
        if os.name == "nt":
            import msvcrt

            handle.seek(0)
            handle.write(b"0")
            handle.flush()
            handle.seek(0)
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as error:
                raise Refused("Another publisher holds the journal lock") from error
        else:
            import fcntl

            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as error:
                raise Refused("Another publisher holds the journal lock") from error
        try:
            yield
        finally:
            if os.name == "nt":
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def persist(path, value):
    """Atomically replace and fsync a journal whose intent must survive a lost response."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        if os.name != "nt":
            os.fchmod(handle.fileno(), 0o600)
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    for attempt in range(5):
        try:
            os.replace(temporary, path)
            break
        except PermissionError:
            if os.name != "nt" or attempt == 4:
                raise
            # Windows scanners can briefly hold the old journal after a read.
            time.sleep(0.05 * (attempt + 1))
    if os.name != "nt":
        fd = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def journal_seal(journal):
    sealed = {key: value for key, value in journal.items() if key != "seal_sha256"}
    return canonical_sha256(sealed)


def seal_journal(journal):
    journal["seal_sha256"] = journal_seal(journal)


def persist_journal(path, journal):
    """Seal publisher progress without changing the generic atomic persistence helper."""
    seal_journal(journal)
    persist(path, journal)


async def snapshot(session, slugs, *, lock=False):
    query = (
        select(GuideArticle)
        .where(GuideArticle.slug.in_(slugs))
        .order_by(GuideArticle.id)
    )
    if lock:
        query = query.with_for_update(nowait=True)
    articles = list(
        await session.scalars(query.execution_options(populate_existing=True))
    )
    ids = [article.id for article in articles]
    query = select(GuideArticleLocale).where(GuideArticleLocale.article_id.in_(ids))
    if lock:
        query = query.order_by(GuideArticleLocale.id).with_for_update(nowait=True)
    locales = list(
        await session.scalars(query.execution_options(populate_existing=True))
    )
    topics = await _topics_for(session, ids)
    revisions = {
        (row.article_locale_id, row.version): row
        for row in await session.scalars(
            select(GuideArticleRevision).where(
                GuideArticleRevision.article_locale_id.in_([row.id for row in locales])
            )
        )
    }
    audits = list(
        await session.scalars(
            select(AdminAuditLog)
            .where(AdminAuditLog.action == "guide_article_updated")
            .where(
                AdminAuditLog.target.in_([f"guide:{article_id}" for article_id in ids])
            )
            .order_by(AdminAuditLog.created_at.desc(), AdminAuditLog.id.desc())
        )
    )
    result = dict.fromkeys(slugs)
    for article in articles:
        state = {
            "id": str(article.id),
            "version": article.version,
            "kind": article.kind,
            "destination_id": article.destination_id,
            "valid_until": str(article.valid_until) if article.valid_until else None,
            "featured": article.featured,
            "display_order": article.display_order,
            "is_active": article.is_active,
            "updated_at": article.updated_at.isoformat(),
            "topics": sorted(topic.slug for topic in topics.get(article.id, [])),
            "metadata_audit": None,
            "locales": {},
        }
        audit = next(
            (
                row
                for row in audits
                if row.target == f"guide:{article.id}"
                and row.metadata_json.get("version") == article.version
            ),
            None,
        )
        if audit:
            state["metadata_audit"] = {
                "id": str(audit.id),
                "actor_id": str(audit.actor_user_id),
                "action": audit.action,
                "version": article.version,
            }
        for row in locales:
            if row.article_id != article.id:
                continue
            latest = revisions.get((row.id, row.version))
            require(
                latest is not None,
                f"{article.slug}:{row.locale}: missing current revision",
            )
            published = revisions.get((row.id, row.published_version))
            if row.published_version is not None:
                require(
                    published is not None and published.action == "published",
                    f"{article.slug}:{row.locale}: broken published pointer",
                )
            state["locales"][row.locale] = {
                "id": str(row.id),
                "version": row.version,
                "published_version": row.published_version,
                "published_at": row.published_at.isoformat()
                if row.published_at
                else None,
                "updated_at": row.updated_at.isoformat(),
                "draft_sha256": document_hash(normalized(row.draft_json)),
                "published_sha256": document_hash(normalized(published.document_json))
                if published
                else None,
                "latest_sha256": document_hash(normalized(latest.document_json)),
                "latest_action": latest.action,
                "latest_actor": str(latest.created_by_user_id),
            }
        result[article.slug] = state
    return result


def require_live(row, slug):
    require(row is not None and row["is_active"], f"{slug}: absent or hidden")
    require(
        row["valid_until"] is None
        or row["valid_until"] >= datetime.now(UTC).date().isoformat(),
        f"{slug}: expired",
    )


def validate_initial(bundle, state):
    for entry in bundle.entries:
        slug = entry["slug"]
        baseline = bundle.baseline[slug]
        row = state[slug]
        pinned = baseline["database"]
        if pinned is None:
            require(
                row is None,
                f"{slug}: repository-only article now exists; refresh baseline",
            )
            continue
        require_live(row, slug)
        require(
            row["id"] == pinned["id"] and row["version"] == pinned["version"],
            f"{slug}: article identity/version changed",
        )
        require(
            all(
                row[key] == value for key, value in metadata(bundle.packs[slug]).items()
            ),
            f"{slug}: classification/order changed",
        )
        require(
            set(row["locales"]) == set(pinned["locales"]), f"{slug}: locale set changed"
        )
        for locale, expected in pinned["locales"].items():
            actual = row["locales"][locale]
            require(
                all(actual[key] == value for key, value in expected.items()),
                f"{slug}:{locale}: version/source/publication changed",
            )
        source = row["locales"][baseline["source_locale"]]
        require(
            source["published_sha256"] == baseline["source_sha256"],
            f"{slug}: source publication changed",
        )
        for locale in entry["locales"]:
            existing = row["locales"].get(locale)
            if existing:
                clean_publication = (
                    existing["version"] == existing["published_version"]
                    and existing["draft_sha256"] == existing["published_sha256"]
                )
                baseline_document = baseline["locale_documents"].get(locale)
                reviewed_unpublished_draft = (
                    locale in entry["publish_locales"]
                    and baseline_document is not None
                    and existing["published_version"] is None
                    and existing["published_sha256"] is None
                    and existing["draft_sha256"]
                    == document_hash(normalized(baseline_document))
                    and existing["latest_sha256"] == existing["draft_sha256"]
                )
                require(
                    clean_publication or reviewed_unpublished_draft,
                    f"{slug}:{locale}: unpublished edits must not be overwritten",
                )


def planned_operations(bundle, state):
    operations = {phase: [] for phase in PHASES[1:]}
    for entry in bundle.entries:
        slug = entry["slug"]
        row = state[slug]
        for index, locale in enumerate(entry["locales"]):
            old = row["locales"].get(locale) if row else None
            wanted = document_hash(
                bundle.packs[slug].locales[locale].model_dump(mode="json")
            )
            action = (
                (
                    "create_article"
                    if index == 0 and row is None
                    else "start_translation"
                )
                if old is None
                else "unchanged"
                if old["draft_sha256"] == wanted
                else "save_draft"
            )
            operations["drafts"].append(
                {"slug": slug, "locale": locale, "action": action}
            )
            if (
                index == 0
                and row is None
                and (
                    bundle.packs[slug].featured
                    or bundle.packs[slug].display_order != 100
                )
            ):
                operations["drafts"].append(
                    {"slug": slug, "locale": locale, "action": "update_metadata"}
                )
        phase = "publish-hubs" if entry["hub"] else "publish-articles"
        for locale in entry["publish_locales"]:
            old = row["locales"].get(locale) if row else None
            wanted = document_hash(
                bundle.packs[slug].locales[locale].model_dump(mode="json")
            )
            action = (
                "unchanged" if old and old["published_sha256"] == wanted else "publish"
            )
            operations[phase].append({"slug": slug, "locale": locale, "action": action})
    for phase, items in operations.items():
        for index, item in enumerate(items):
            item["id"] = f"{phase}:{index}:{item['slug']}:{item['locale']}"
            item["phase"] = phase
    return operations


def journal_authorization(bundle, initial, operations):
    """Bind progress to authorization recomputed from reviewed, immutable inputs."""
    return canonical_sha256(
        {
            "manifest_sha256": bundle.manifest_sha256,
            "baseline_sha256": bundle.manifest["baseline_sha256"],
            "slugs": bundle.slugs,
            "initial": initial,
            "operations": operations,
        }
    )


def validate_journal(bundle, journal):
    """Validate progress only; never accept its operation plan as authorization."""
    keys = {
        "schema_version",
        "manifest_sha256",
        "baseline_sha256",
        "slugs",
        "actor_id",
        "created_at",
        "initial",
        "authorization_sha256",
        "seal_sha256",
        "expected",
        "pending",
        "history",
        "operations",
        "done",
        "dry_run",
    }
    require(
        isinstance(journal, dict) and set(journal) == keys, "Invalid journal schema"
    )
    require(journal["schema_version"] == 2, "Unsupported journal schema")
    require(journal["seal_sha256"] == journal_seal(journal), "Journal seal mismatch")
    require(
        journal["manifest_sha256"] == bundle.manifest_sha256
        and journal["baseline_sha256"] == bundle.manifest["baseline_sha256"]
        and journal["slugs"] == bundle.slugs,
        "Journal belongs to another bundle",
    )
    try:
        UUID(journal["actor_id"])
    except (TypeError, ValueError, AttributeError) as error:
        raise Refused("Invalid journal actor") from error
    require(isinstance(journal["created_at"], str), "Invalid journal creation time")
    initial = journal["initial"]
    require(
        isinstance(initial, dict) and set(initial) == set(bundle.slugs),
        "Invalid initial state",
    )
    validate_initial(bundle, initial)
    operations = planned_operations(bundle, initial)
    require(journal["operations"] == operations, "Journal operation plan was forged")
    require(
        journal["authorization_sha256"]
        == journal_authorization(bundle, initial, operations),
        "Journal authorization binding mismatch",
    )
    require(
        isinstance(journal["expected"], dict)
        and set(journal["expected"]) == set(bundle.slugs),
        "Invalid expected state",
    )
    require(type(journal["dry_run"]) is bool, "Invalid journal dry-run state")
    require(isinstance(journal["history"], list), "Invalid journal history")
    require(
        isinstance(journal["done"], dict) and set(journal["done"]) == set(PHASES[1:]),
        "Invalid completed operations",
    )
    by_id = {}
    for phase in PHASES[1:]:
        phase_operations = operations[phase]
        expected_ids = [item["id"] for item in phase_operations]
        done = journal["done"][phase]
        require(
            isinstance(done, list)
            and len(done) == len(set(done))
            and done == expected_ids[: len(done)],
            f"Invalid completed operations for {phase}",
        )
        by_id.update({item["id"]: item for item in phase_operations})
    for index, phase in enumerate(PHASES[1:]):
        if journal["done"][phase]:
            for earlier in PHASES[1 : index + 1]:
                require(
                    journal["done"][earlier]
                    == [item["id"] for item in operations[earlier]],
                    f"Completed operations are out of phase before {phase}",
                )
    pending = journal["pending"]
    if pending is not None:
        require(isinstance(pending, dict), "Invalid pending operation")
        operation = by_id.get(pending.get("id"))
        require(operation is not None, "Pending operation is unauthorized")
        require(
            set(pending) == set(operation) | {"actor_id", "at"}
            and all(pending[key] == value for key, value in operation.items())
            and pending["actor_id"] == journal["actor_id"]
            and isinstance(pending["at"], str),
            "Pending operation was forged",
        )
        phase_ids = [item["id"] for item in operations[pending["phase"]]]
        done = journal["done"][pending["phase"]]
        require(
            len(done) < len(phase_ids) and pending["id"] == phase_ids[len(done)],
            "Pending operation is out of order",
        )
        for earlier in PHASES[1 : PHASES.index(pending["phase"])]:
            require(
                journal["done"][earlier]
                == [item["id"] for item in operations[earlier]],
                f"Pending operation is out of phase before {pending['phase']}",
            )
    require(
        journal["dry_run"] or not any(journal["done"].values()),
        "Dry-run state was forged",
    )
    require(
        not journal["dry_run"]
        or any(
            isinstance(item, dict)
            and item.get("phase") == "dry-run"
            and item.get("status") == "read_only"
            for item in journal["history"]
        ),
        "Dry-run completion evidence is absent",
    )
    validate_expected_progress(bundle, journal)
    return operations


def authorize_operation(bundle, journal, phase, operation):
    operations = validate_journal(bundle, journal)
    require(
        phase in PHASES[1:] and operation in operations[phase], "Unauthorized operation"
    )
    require(operation["phase"] == phase, "Operation phase mismatch")


def same_state(actual, expected):
    changed = [slug for slug in expected if actual[slug] != expected[slug]]
    require(not changed, "Concurrent/unexpected change: " + ", ".join(changed))


async def active_actor(session, actor_id=None):
    allowed = get_settings().admin_email_set
    require(bool(allowed), "No configured owner available")
    query = select(User).where(
        func.lower(User.email).in_(allowed), User.is_active.is_(True)
    )
    if actor_id:
        query = query.where(User.id == UUID(str(actor_id)))
    actor = await session.scalar(
        query.order_by(User.id)
        .limit(1)
        .with_for_update(nowait=True)
        .execution_options(populate_existing=True)
    )
    require(
        actor is not None and not user_is_suspended(actor),
        "No active configured owner available",
    )
    require(
        "content.manage" in cached_admin_capabilities(actor),
        "Actor lacks content permission",
    )
    return actor


async def require_dependencies(session, bundle, entry):
    required = list(entry.get("requires", []))
    for other in bundle.entries:
        if not other["hub"]:
            required.extend(
                {
                    "slug": other["slug"],
                    "locale": locale,
                    "document_sha256": document_hash(
                        bundle.packs[other["slug"]]
                        .locales[locale]
                        .model_dump(mode="json")
                    ),
                }
                for locale in other["publish_locales"]
            )
    states = await snapshot(
        session, sorted({item["slug"] for item in required}), lock=True
    )
    for item in required:
        row = states[item["slug"]]
        require_live(row, item["slug"])
        locale = row["locales"].get(item["locale"])
        require(
            locale is not None
            and locale["published_sha256"] == item["document_sha256"],
            f"{item['slug']}:{item['locale']}: hub dependency is not published as reviewed",
        )


def accept_transition(before, after, intent, bundle):
    slug, language, action = intent["slug"], intent["locale"], intent["action"]
    for other in before:
        if other != slug:
            require(
                after[other] == before[other], f"{other}: unrelated article changed"
            )
    old, new = before[slug], after[slug]
    if action == "unchanged":
        require(new == old, f"{slug}: unexpected write")
        return
    require_live(new, slug)
    pack = bundle.packs[slug]
    if action == "update_metadata":
        require(
            bundle.baseline[slug]["database"] is None,
            f"{slug}: existing metadata is protected",
        )
        expected = copy.deepcopy(old)
        expected.update(metadata(pack))
        expected["version"] += 1
        expected["updated_at"] = new["updated_at"]
        expected["metadata_audit"] = new["metadata_audit"]
        require(new == expected, f"{slug}: unexpected metadata transition")
        audit = new["metadata_audit"]
        require(
            audit is not None
            and audit["actor_id"] == intent["actor_id"]
            and audit["action"] == "guide_article_updated"
            and audit["version"] == new["version"],
            f"{slug}: metadata update author/action mismatch",
        )
        return
    wanted = document_hash(pack.locales[language].model_dump(mode="json"))
    locale = new["locales"].get(language)
    require(locale is not None, f"{slug}:{language}: result locale absent")
    old_locale = old["locales"].get(language) if old else None
    revision_action = {
        "create_article": "created",
        "start_translation": "created",
        "save_draft": "draft_saved",
        "publish": "published",
    }[action]
    require(
        locale["version"] == (old_locale["version"] + 1 if old_locale else 1)
        and locale["draft_sha256"] == wanted
        and locale["latest_sha256"] == wanted
        and locale["latest_action"] == revision_action
        and locale["latest_actor"] == intent["actor_id"],
        f"{slug}:{language}: resulting version/hash/action/actor mismatch",
    )
    require(
        {k: v for k, v in new["locales"].items() if k != language}
        == ({k: v for k, v in old["locales"].items() if k != language} if old else {}),
        f"{slug}: unrelated locale changed",
    )
    if old:
        require(
            {k: v for k, v in new.items() if k != "locales"}
            == {k: v for k, v in old.items() if k != "locales"},
            f"{slug}: metadata changed",
        )
    else:
        expected = {
            **metadata(pack),
            "version": 1,
            "featured": False,
            "display_order": 100,
        }
        require(
            all(new[k] == v for k, v in expected.items()),
            f"{slug}: unexpected create metadata",
        )
    if old_locale:
        require(
            locale["id"] == old_locale["id"],
            f"{slug}:{language}: locale identity changed",
        )
    if action == "publish":
        require(
            locale["published_version"] == locale["version"]
            and locale["published_sha256"] == wanted
            and locale["published_at"] is not None,
            f"{slug}:{language}: publication mismatch",
        )
        if old_locale["published_at"] is not None:
            require(
                locale["published_at"] == old_locale["published_at"],
                f"{slug}:{language}: first publication timestamp changed",
            )
    else:
        expected = {
            key: old_locale[key] if old_locale else None
            for key in ("published_version", "published_sha256", "published_at")
        }
        require(
            all(locale[key] == value for key, value in expected.items()),
            f"{slug}:{language}: draft write changed publication",
        )


def validate_expected_progress(bundle, journal):
    """Rebuild completed transitions so forged progress cannot bless an arbitrary state."""
    state = copy.deepcopy(journal["initial"])
    final = journal["expected"]
    actor_id = journal["actor_id"]
    for phase in PHASES[1:]:
        done = set(journal["done"][phase])
        for operation in journal["operations"][phase]:
            if operation["id"] not in done:
                break
            intent = {**operation, "actor_id": actor_id}
            action = operation["action"]
            if action == "unchanged":
                continue
            slug, locale = operation["slug"], operation["locale"]
            old_article = state[slug]
            final_article = final.get(slug)
            require(
                final_article is not None, f"{slug}: journal result article is absent"
            )
            if action == "update_metadata":
                new_article = copy.deepcopy(old_article)
                new_article.update(metadata(bundle.packs[slug]))
                new_article["version"] += 1
                new_article["updated_at"] = final_article["updated_at"]
                new_article["metadata_audit"] = final_article["metadata_audit"]
            else:
                wanted = document_hash(
                    bundle.packs[slug].locales[locale].model_dump(mode="json")
                )
                final_locale = final_article["locales"].get(locale)
                require(
                    final_locale is not None,
                    f"{slug}:{locale}: journal result is absent",
                )
                if old_article is None:
                    new_article = copy.deepcopy(final_article)
                    new_article["version"] = 1
                    new_article["featured"] = False
                    new_article["display_order"] = 100
                    new_article["metadata_audit"] = None
                    new_article["locales"] = {}
                else:
                    new_article = copy.deepcopy(old_article)
                old_locale = (
                    old_article["locales"].get(locale)
                    if old_article is not None
                    else None
                )
                new_locale = copy.deepcopy(old_locale or final_locale)
                new_locale.update(
                    {
                        "version": old_locale["version"] + 1 if old_locale else 1,
                        "draft_sha256": wanted,
                        "latest_sha256": wanted,
                        "latest_action": {
                            "create_article": "created",
                            "start_translation": "created",
                            "save_draft": "draft_saved",
                            "publish": "published",
                        }[action],
                        "latest_actor": actor_id,
                        "updated_at": final_locale["updated_at"],
                    }
                )
                if action == "publish":
                    new_locale.update(
                        {
                            "published_version": new_locale["version"],
                            "published_sha256": wanted,
                            "published_at": final_locale["published_at"],
                        }
                    )
                else:
                    new_locale.update(
                        {
                            key: old_locale[key] if old_locale else None
                            for key in (
                                "published_version",
                                "published_sha256",
                                "published_at",
                            )
                        }
                    )
                new_article["locales"][locale] = new_locale
            after = copy.deepcopy(state)
            after[slug] = new_article
            accept_transition(state, after, intent, bundle)
            state = after
    require(
        state == final, "Journal expected state does not match completed operations"
    )


def complete_intent(journal, state, path, status):
    pending = journal["pending"]
    journal["expected"] = state
    journal["done"][pending["phase"]].append(pending["id"])
    journal["history"].append({"id": pending["id"], "at": stamp(), "status": status})
    journal["pending"] = None
    persist_journal(path, journal)


def reconcile(journal, actual, path, bundle):
    pending = journal.get("pending")
    if pending is None:
        same_state(actual, journal["expected"])
    elif actual == journal["expected"]:
        journal["history"].append(
            {"id": pending["id"], "at": stamp(), "status": "not_written_reconciled"}
        )
        journal["pending"] = None
        persist_journal(path, journal)
    else:
        accept_transition(journal["expected"], actual, pending, bundle)
        complete_intent(journal, actual, path, "committed_reconciled")


async def write_operation(session, actor, operation, before, bundle):
    slug, locale, action = operation["slug"], operation["locale"], operation["action"]
    pack = bundle.packs[slug]
    document = pack.locales[locale]
    row = before[slug]
    if action == "unchanged":
        return
    if action == "create_article":
        await admin_service.create_article(
            session,
            actor,
            ArticleCreate(
                slug=slug,
                kind=pack.kind,
                destination_id=pack.destination_id,
                topics=pack.topics,
                valid_until=pack.valid_until,
                locale=locale,
                document=document,
            ),
        )
    elif action == "start_translation":
        await admin_service.start_translation(
            session, actor, UUID(row["id"]), locale, document
        )
    elif action == "save_draft":
        await admin_service.save_draft(
            session,
            actor,
            UUID(row["id"]),
            locale,
            DraftWrite(
                expected_version=row["locales"][locale]["version"],
                document=document,
            ),
        )
    elif action == "update_metadata":
        await admin_service.update_article(
            session,
            actor,
            UUID(row["id"]),
            ArticleUpdate(
                expected_version=row["version"],
                **metadata(pack),
            ),
            locale,
        )
    elif action == "publish":
        wanted = document_hash(document.model_dump(mode="json"))
        require(
            row["locales"][locale]["draft_sha256"] == wanted,
            f"{slug}:{locale}: reviewed draft absent",
        )
        await admin_service.publish_locale(
            session,
            actor,
            UUID(row["id"]),
            locale,
            PublishWrite(
                expected_version=row["locales"][locale]["version"],
                confirmed=True,
                reason=f"Reviewed localization bundle {bundle.manifest_sha256}",
            ),
        )
    else:
        raise Refused("Unknown journal operation")


async def execute_phase(
    bundle, phase, journal_path, *, deployed_root, actor_id=None, db_engine=engine
):
    """Caller holds the durable file lock; production also holds the shared DB lock."""
    require(phase in PHASES, "Unknown phase")
    async with db_engine.connect() as connection:
        postgres = connection.dialect.name == "postgresql"
        locked = False
        if postgres:
            await connection.execution_options(isolation_level="SERIALIZABLE")
            locked = bool(
                await connection.scalar(
                    text("SELECT pg_try_advisory_lock(:key)"), {"key": LOCK_KEY}
                )
            )
            await connection.commit()
            require(locked, "Another editorial publisher is running")
        journal = None
        try:
            async with AsyncSession(bind=connection, expire_on_commit=False) as session:
                # Verify even on a no-op resume. A changed file never inherits old approval.
                verify_bundle(bundle.root, bundle.baseline_path, bundle.manifest_sha256)
                verify_deployed(bundle, deployed_root)
                actual = await snapshot(session, bundle.slugs)
                if journal_path.exists():
                    candidate = json.loads(journal_path.read_text("utf-8"))
                    validate_journal(bundle, candidate)
                    journal = candidate
                    if actor_id:
                        require(
                            str(actor_id) == journal["actor_id"],
                            "Journal actor is pinned",
                        )
                    actor = await active_actor(session, journal["actor_id"])
                    reconcile(journal, actual, journal_path, bundle)
                    validate_journal(bundle, journal)
                else:
                    require(phase == "dry-run", "Run dry-run first with durable state")
                    validate_initial(bundle, actual)
                    actor = await active_actor(session, actor_id)
                    operations = planned_operations(bundle, actual)
                    journal = {
                        "schema_version": 2,
                        "manifest_sha256": bundle.manifest_sha256,
                        "baseline_sha256": bundle.manifest["baseline_sha256"],
                        "slugs": bundle.slugs,
                        "actor_id": str(actor.id),
                        "created_at": stamp(),
                        "initial": actual,
                        "authorization_sha256": journal_authorization(
                            bundle, actual, operations
                        ),
                        "seal_sha256": "",
                        "expected": actual,
                        "pending": None,
                        "history": [],
                        "operations": operations,
                        "done": {item: [] for item in PHASES[1:]},
                        "dry_run": False,
                    }
                    seal_journal(journal)
                    validate_journal(bundle, journal)
                if phase == "dry-run":
                    journal["dry_run"] = True
                    journal["history"].append(
                        {"phase": phase, "status": "read_only", "at": stamp()}
                    )
                    persist_journal(journal_path, journal)
                    return {
                        "phase": phase,
                        "status": "read_only",
                        "articles": len(bundle.slugs),
                        "operations": journal["operations"],
                    }
                require(journal["dry_run"], "Successful dry-run required")
                validate_journal(bundle, journal)
                for earlier in PHASES[1 : PHASES.index(phase)]:
                    require(
                        journal["done"][earlier]
                        == [op["id"] for op in journal["operations"][earlier]],
                        f"Complete {earlier} before {phase}",
                    )
                await session.rollback()
                for operation in journal["operations"][phase]:
                    if operation["id"] in journal["done"][phase]:
                        continue
                    verify_bundle(
                        bundle.root, bundle.baseline_path, bundle.manifest_sha256
                    )
                    verify_deployed(bundle, deployed_root)
                    authorize_operation(bundle, journal, phase, operation)
                    if postgres:
                        await session.execute(text("SET LOCAL lock_timeout = '5s'"))
                    before = await snapshot(session, bundle.slugs, lock=True)
                    same_state(before, journal["expected"])
                    for slug, row in before.items():
                        if row is not None:
                            require_live(row, slug)
                    entry = next(
                        item
                        for item in bundle.entries
                        if item["slug"] == operation["slug"]
                    )
                    if phase == "publish-hubs":
                        await require_dependencies(session, bundle, entry)
                    actor = await active_actor(session, journal["actor_id"])
                    journal["pending"] = {
                        **operation,
                        "actor_id": str(actor.id),
                        "at": stamp(),
                    }
                    persist_journal(journal_path, journal)
                    # Recheck the installed bytes after the durable intent and directly
                    # before the database write. The journal cannot bless file drift.
                    verify_deployed(bundle, deployed_root)
                    await write_operation(session, actor, operation, before, bundle)
                    await session.rollback()
                    after = await snapshot(session, bundle.slugs)
                    accept_transition(before, after, journal["pending"], bundle)
                    complete_intent(
                        journal,
                        after,
                        journal_path,
                        "unchanged"
                        if operation["action"] == "unchanged"
                        else "committed",
                    )
                    validate_journal(bundle, journal)
                    await session.rollback()
                final = await snapshot(session, bundle.slugs)
                same_state(final, journal["expected"])
                for slug, row in final.items():
                    if row is not None:
                        require_live(row, slug)
                return {
                    "phase": phase,
                    "status": "complete",
                    "operations": len(journal["done"][phase]),
                }
        except Exception as error:
            if journal is not None:
                journal["history"].append(
                    {
                        "phase": phase,
                        "at": stamp(),
                        "status": "stopped",
                        "reason": str(error)
                        if isinstance(error, Refused)
                        else type(error).__name__,
                    }
                )
                persist_journal(journal_path, journal)
            raise
        finally:
            await connection.rollback()
            if locked:
                await connection.execute(
                    text("SELECT pg_advisory_unlock(:key)"), {"key": LOCK_KEY}
                )
                await connection.commit()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--deployed-root", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--actor-id", type=UUID)
    parser.add_argument("phase", choices=PHASES)
    args = parser.parse_args(argv)
    try:
        require(
            engine.dialect.name == "postgresql", "Production CLI requires PostgreSQL"
        )
        bundle = verify_bundle(args.bundle, args.baseline, args.manifest_sha256)
        with journal_lock(args.state_dir):
            result = asyncio.run(
                execute_phase(
                    bundle,
                    args.phase,
                    args.state_dir / "journal.json",
                    deployed_root=args.deployed_root,
                    actor_id=args.actor_id,
                )
            )
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as error:  # noqa: BLE001 -- CLI boundary emits a stopped journal-safe result
        print(
            json.dumps(
                {
                    "status": "stopped",
                    "reason": str(error)
                    if isinstance(error, Refused)
                    else type(error).__name__,
                    "next": "Review journal; reuse the same bundle and state for reconciliation",
                }
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
