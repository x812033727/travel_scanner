"""Compile independently reviewed Route B packs into one guarded publication bundle.

Route B (agent translation, per-locale independent review, content PR) leaves complete
five-language packs and hash-bound review receipts, but none of the Route A job
artifacts that ``assemble_bundle.reviewed_document`` expects. This compiler turns exactly
the selected *missing* locales of public articles into the schema-1 bundle that
``publish_bundle.py`` already verifies and publishes through its durable journal:

  uv run --project apps/api python docs/article-localization/prepare_route_b_bundle.py \
    --candidate <CANDIDATE>/candidate-manifest.json --candidate-sha256 <SHA256> \
    --review <REVIEW>.json --review-sha256 <SHA256> \
    --baseline <BASELINE>.json --baseline-sha256 <SHA256> \
    --slug <SLUG> [--slug ...] --locale en [--locale ...] --output <WORK>/<new-directory>

Every input is pinned by a SHA-256 supplied outside the file and parsed from the bytes
that were hashed. The output directory must be new and outside both the repository and
the candidate; a refusal leaves no manifest behind. Nothing here opens a database or
writes the repository's packs, public images or publish_holds.json. Success authorizes
nothing: review the manifest and the provenance receipt, then run publish_bundle.py
dry-run, drafts, publish-articles and publish-hubs. Input schemas and every refusal are
listed in route-b-bundle.md beside this file.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import time
from datetime import UTC, date, datetime
from pathlib import Path, PurePosixPath
from uuid import UUID, uuid4

from app.guides.content_pack import (
    ArticlePack,
    ContentPackError,
    load_publish_holds,
    publish_holds_path,
)
from app.guides.service import document_hash
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[2]


def _load(name, filename, *, register=False):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    if register:
        # publish_bundle declares a dataclass, which looks its module up in sys.modules.
        sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


publish_bundle = _load("article_localization_publish_bundle", "publish_bundle.py", register=True)
build_baseline = _load("article_localization_build_baseline", "build_baseline.py")

Refused = publish_bundle.Refused
require = publish_bundle.require
sha = publish_bundle.sha

CANDIDATE_SCHEMA = "route-b-candidate-v1"
REVIEW_SCHEMA = "route-b-review-v1"
PROVENANCE_SCHEMA = "route-b-bundle-provenance-v1"
PROVENANCE_FILE = "route-b-provenance.json"
# The localization order (source first); publish_bundle only compares these as sets.
LOCALES = tuple(build_baseline.LOCALES)
# The same hub set as assemble_bundle.HUBS: a hub needs dependency pins this route lacks.
HUBS = frozenset({"gemini-guide", "claude-code-tutorials", "ai-terms-index"})
MAX_ARTICLES = 20
MAX_IMAGE_BYTES = 300_000
RASTERS = frozenset({".jpg", ".png", ".webp"})
CHECKS = ("text", "visual", "glyph", "links")
HASH = re.compile(r"[0-9a-f]{64}\Z")
GIT = re.compile(r"[0-9a-f]{40}\Z")
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
ASSET = re.compile(
    r"public/guides/[a-z0-9]+(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*\.(?:webp|jpg|png|svg)\Z"
)
REVIEW_TARGET_FIELDS = frozenset(
    {
        "slug",
        "locale",
        "status",
        "translator",
        "reviewer",
        "reviewed_at",
        "source_sha256",
        "document_sha256",
        "assets",
        "checks",
        "open_findings",
    }
)
BASELINE_ARTICLE_FIELDS = frozenset(
    {
        "slug",
        "kind",
        "status",
        "pack_path",
        "pack_sha256",
        "metadata",
        "source_locale",
        "source_document",
        "source_sha256",
        "existing_locales",
        "missing_locales",
        "translation_missing_locales",
        "publication_missing_locales",
        "publication_locales",
        "target_locales",
        "locale_provenance",
        "published_locales",
        "locale_documents",
        "database",
        "assets",
    }
)
METADATA_FIELDS = frozenset(
    {"slug", "kind", "destination_id", "topics", "valid_until", "featured", "display_order"}
)
DATABASE_LOCALE_FIELDS = frozenset(
    {"id", "version", "published_version", "published_sha256", "draft_sha256"}
)


def valid_hash(value):
    return isinstance(value, str) and HASH.fullmatch(value) is not None


def text_value(value):
    return isinstance(value, str) and bool(value.strip())


def positive(value):
    return type(value) is int and value >= 1


def uuid_text(value):
    try:
        return isinstance(value, str) and str(UUID(value)) == value
    except ValueError:
        return False


def aware_time(value, label):
    require(text_value(value), f"{label} needs an ISO 8601 time")
    try:
        moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise Refused(f"{label} needs an ISO 8601 time") from error
    require(moment.tzinfo is not None, f"{label} time must include a timezone")
    return moment


def strict_json(raw, label):
    """Parse UTF-8 JSON and refuse a repeated key, which would hide one value from review."""

    def unique(pairs):
        keys = [key for key, _ in pairs]
        require(len(keys) == len(set(keys)), f"{label} repeats a JSON key")
        return dict(pairs)

    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=unique)
    except (UnicodeDecodeError, ValueError) as error:
        raise Refused(f"{label} is not strict UTF-8 JSON") from error


def read_pinned(path, expected, label):
    """Hash the exact bytes that will be parsed; the pin always comes from outside the file."""
    require(valid_hash(expected), f"Supply the external {label} SHA256")
    path = Path(path)
    require(not path.is_symlink() and path.is_file(), f"{label} file is absent")
    raw = path.read_bytes()
    require(sha(raw) == expected, f"{label} SHA256 mismatch")
    return raw


def read_inside(root, relative, label):
    """Read one candidate file without following a link or leaving the candidate.

    Every component is checked for a link before ``safe_path`` resolves the path, so a
    link is refused as a link wherever it points (inside the candidate or out of it).
    Both callers have already pinned ``relative`` to a fixed relative shape.
    """
    current = root
    for part in PurePosixPath(relative).parts:
        current = current / part
        require(not current.is_symlink(), f"{label}: linked candidate path")
    path = publish_bundle.safe_path(root, relative)
    require(path.is_file(), f"{label}: candidate file is absent")
    return path.read_bytes()


def load_candidate(path, pinned):
    raw = read_pinned(path, pinned, "Candidate manifest")
    manifest = strict_json(raw, "Candidate manifest")
    require(
        isinstance(manifest, dict)
        and set(manifest) == {"schema", "source_git_commit", "articles", "assets"}
        and manifest["schema"] == CANDIDATE_SCHEMA,
        "Unsupported candidate manifest schema",
    )
    require(
        isinstance(manifest["source_git_commit"], str)
        and GIT.fullmatch(manifest["source_git_commit"]) is not None,
        "Candidate needs its 40-hex source Git commit",
    )
    root = Path(path).parent
    rows = manifest["articles"]
    require(isinstance(rows, list) and bool(rows), "Candidate has no articles")
    packs = {}
    for row in rows:
        require(
            isinstance(row, dict) and set(row) == {"slug", "pack_path", "pack_sha256"},
            "Invalid candidate article",
        )
        slug = row["slug"]
        require(
            isinstance(slug, str) and SLUG.fullmatch(slug) is not None and slug not in packs,
            "Repeated or invalid candidate article slug",
        )
        require(row["pack_path"] == f"packs/{slug}.json", f"{slug}: unsafe candidate pack path")
        require(valid_hash(row["pack_sha256"]), f"{slug}: invalid candidate pack SHA256")
        pack_raw = read_inside(root, row["pack_path"], slug)
        require(sha(pack_raw) == row["pack_sha256"], f"{slug}: candidate pack SHA256 mismatch")
        try:
            pack = ArticlePack.model_validate(strict_json(pack_raw, f"{slug} pack"))
        except ValidationError as error:
            raise Refused(f"{slug}: candidate pack is not a valid ArticlePack") from error
        require(pack.slug == slug, f"{slug}: candidate pack slug mismatch")
        packs[slug] = pack
    rows = manifest["assets"]
    require(isinstance(rows, list), "Candidate assets must be a list")
    assets = {}
    for row in rows:
        require(
            isinstance(row, dict) and set(row) == {"path", "sha256"},
            "Invalid candidate asset",
        )
        relative = row["path"]
        require(
            isinstance(relative, str) and ASSET.fullmatch(relative) is not None,
            "Unsafe candidate asset path",
        )
        require(relative not in assets, "Repeated candidate asset")
        require(valid_hash(row["sha256"]), f"{relative}: invalid candidate asset SHA256")
        data = read_inside(root, relative, relative)
        require(sha(data) == row["sha256"], f"{relative}: candidate asset SHA256 mismatch")
        assets[relative] = data
    return {
        "sha256": pinned,
        "root": root,
        "source_git_commit": manifest["source_git_commit"],
        "packs": packs,
        "assets": assets,
    }


def load_review(path, pinned):
    raw = read_pinned(path, pinned, "Review")
    review = strict_json(raw, "Review")
    require(
        isinstance(review, dict)
        and set(review) == {"schema", "evidence_sha256", "targets"}
        and review["schema"] == REVIEW_SCHEMA,
        "Unsupported review schema",
    )
    require(valid_hash(review["evidence_sha256"]), "Review needs its evidence SHA256")
    rows = review["targets"]
    require(isinstance(rows, list) and bool(rows), "Review has no targets")
    targets = {}
    now = datetime.now(UTC)
    for row in rows:
        require(
            isinstance(row, dict) and set(row) == REVIEW_TARGET_FIELDS,
            "Invalid review target schema",
        )
        key = (row["slug"], row["locale"])
        require(
            isinstance(row["slug"], str)
            and SLUG.fullmatch(row["slug"]) is not None
            and row["locale"] in LOCALES
            and key not in targets,
            "Repeated or invalid review target",
        )
        label = f"{row['slug']}:{row['locale']}"
        require(row["status"] == "PASS", f"{label}: review is not an independent PASS")
        require(
            text_value(row["translator"])
            and text_value(row["reviewer"])
            and row["translator"].strip().casefold() != row["reviewer"].strip().casefold(),
            f"{label}: the reviewer must be independent of the translator",
        )
        require(aware_time(row["reviewed_at"], f"{label} review") <= now, f"{label}: future review")
        require(
            valid_hash(row["source_sha256"]) and valid_hash(row["document_sha256"]),
            f"{label}: invalid review hash",
        )
        checks = row["checks"]
        require(
            isinstance(checks, dict)
            and set(checks) == set(CHECKS)
            and all(checks[name] is True for name in CHECKS),
            f"{label}: text, visual, glyph and link review must all pass",
        )
        require(
            type(row["open_findings"]) is int and row["open_findings"] == 0,
            f"{label}: review has unresolved findings",
        )
        images = row["assets"]
        require(
            isinstance(images, dict)
            and all(
                isinstance(src, str)
                and ASSET.fullmatch("public" + src) is not None
                and valid_hash(digest)
                for src, digest in images.items()
            ),
            f"{label}: invalid reviewed image binding",
        )
        targets[key] = row
    return {"sha256": pinned, "evidence_sha256": review["evidence_sha256"], "targets": targets}


def load_baseline(path, pinned):
    raw = read_pinned(path, pinned, "Baseline")
    baseline = strict_json(raw, "Baseline")
    require(
        isinstance(baseline, dict) and baseline.get("schema_version") == 1,
        "Unsupported baseline schema",
    )
    require(
        isinstance(baseline.get("repo_commit"), str)
        and GIT.fullmatch(baseline["repo_commit"]) is not None,
        "Baseline lacks its repository commit",
    )
    aware_time(baseline.get("captured_at"), "Baseline capture")
    rows = baseline.get("articles")
    require(isinstance(rows, list) and bool(rows), "Baseline has no articles")
    articles = {}
    for row in rows:
        require(
            isinstance(row, dict) and isinstance(row.get("slug"), str) and row["slug"] not in articles,
            "Repeated or invalid baseline article",
        )
        articles[row["slug"]] = row
    return {
        "sha256": pinned,
        "path": Path(path),
        "repo_commit": baseline["repo_commit"],
        "captured_at": baseline["captured_at"],
        "articles": articles,
    }


def normalized_document(document, label):
    try:
        return publish_bundle.normalized(document)
    except ValidationError as error:
        raise Refused(f"{label}: baseline document is not a GuideDocument") from error


def public_source(slug, article, today):
    """Return the normalized baseline documents of a fully pinned, public, unexpired source.

    A public API projection carries no database identity or versions, so it can never pin
    a publication; the guarded publisher compares these exact values with the live rows.
    """
    missing = BASELINE_ARTICLE_FIELDS - set(article)
    require(not missing, f"{slug}: incomplete baseline article ({', '.join(sorted(missing))})")
    database = article["database"]
    require(
        isinstance(database, dict),
        f"{slug}: baseline has no database identity; a public projection cannot pin a release",
    )
    require(
        set(database) == {"id", "version", "locales"}
        and uuid_text(database["id"])
        and positive(database["version"])
        and isinstance(database["locales"], dict)
        and bool(database["locales"]),
        f"{slug}: incomplete baseline database identity/version",
    )
    for locale, row in database["locales"].items():
        require(
            locale in LOCALES
            and isinstance(row, dict)
            and set(row) == DATABASE_LOCALE_FIELDS
            and uuid_text(row["id"])
            and positive(row["version"])
            and (row["published_version"] is None or positive(row["published_version"]))
            and valid_hash(row["draft_sha256"])
            and (row["published_sha256"] is None or valid_hash(row["published_sha256"]))
            and (row["published_version"] is None) == (row["published_sha256"] is None),
            f"{slug}:{locale}: incomplete baseline locale version",
        )
    require(
        article["status"] == "published",
        f"{slug}: baseline source is not public ({article['status']})",
    )
    metadata = article["metadata"]
    require(
        isinstance(metadata, dict)
        and set(metadata) == METADATA_FIELDS
        and metadata["slug"] == slug
        and metadata["kind"] == article["kind"]
        and isinstance(metadata["topics"], list),
        f"{slug}: incomplete baseline metadata",
    )
    valid_until = metadata["valid_until"]
    if valid_until is not None:
        try:
            expiry = date.fromisoformat(valid_until)
        except (TypeError, ValueError) as error:
            raise Refused(f"{slug}: invalid baseline expiry") from error
        require(expiry >= today, f"{slug}: source article is expired")
    documents = article["locale_documents"]
    require(
        isinstance(documents, dict) and bool(documents) and set(documents) <= set(LOCALES),
        f"{slug}: incomplete baseline documents",
    )
    normal = {
        locale: normalized_document(document, f"{slug}:{locale}")
        for locale, document in documents.items()
    }
    source = normalized_document(article["source_document"], slug)
    source_locale = article["source_locale"]
    require(source_locale in LOCALES, f"{slug}: invalid baseline source locale")
    pinned = database["locales"].get(source_locale)
    require(
        source_locale in normal
        and source_locale in article["published_locales"]
        and pinned is not None
        and pinned["published_version"] is not None
        and pinned["version"] == pinned["published_version"]
        and pinned["draft_sha256"] == pinned["published_sha256"],
        f"{slug}: source locale is not cleanly published",
    )
    require(
        document_hash(source) == article["source_sha256"] == pinned["published_sha256"]
        and normal[source_locale] == source,
        f"{slug}: baseline source does not match its pinned publication",
    )
    for locale, row in database["locales"].items():
        require(
            locale in normal
            and document_hash(normal[locale])
            == (row["published_sha256"] or row["draft_sha256"]),
            f"{slug}:{locale}: baseline document differs from its pinned version",
        )
    published = [
        locale
        for locale in LOCALES
        if locale in database["locales"]
        and database["locales"][locale]["published_version"] is not None
    ]
    work = build_baseline.locale_work(normal, published, article["status"])
    provenance = build_baseline.locale_provenance(list(normal), database["locales"])
    require(
        article["published_locales"] == published
        and article["existing_locales"] == [locale for locale in LOCALES if locale in normal]
        and all(article[key] == value for key, value in work.items())
        and article["locale_provenance"] == provenance,
        f"{slug}: baseline locale targets are inconsistent; rebuild it",
    )
    images = article["assets"]
    require(
        isinstance(images, list)
        and all(
            isinstance(row, dict)
            and set(row) == {"src", "sha256"}
            and isinstance(row["src"], str)
            and valid_hash(row["sha256"])
            for row in images
        )
        and len({row["src"] for row in images}) == len(images),
        f"{slug}: incomplete baseline assets",
    )
    return normal, {row["src"]: row["sha256"] for row in images}


def read_holds(path=None):
    """Read the hold list exactly as guides-import and the publisher do; never change it."""
    source = Path(path) if path is not None else publish_holds_path()
    raw = source.read_bytes() if source.is_file() else None
    try:
        holds = load_publish_holds(source)
    except ContentPackError as error:
        raise Refused("Cannot read publication hold list") from error
    return holds, sha(raw) if raw is not None else None


def reviewed_images(label, document, reviewed, candidate_assets, baseline_assets):
    """Return the bundle paths of exactly the images this reviewed document needs."""
    referenced = publish_bundle.image_sources(document)
    approved = reviewed["assets"]
    chosen = {}
    for src in referenced:
        path = "public" + src
        require(path in candidate_assets, f"{label}: image is absent from the candidate: {src}")
        data = candidate_assets[path]
        digest = sha(data)
        require(approved.get(src) == digest, f"{label}: reviewed image changed: {src}")
        require(
            baseline_assets.get(src, digest) == digest,
            f"{label}: image differs from the baseline: {src}",
        )
        require(
            len(data) <= MAX_IMAGE_BYTES,
            f"{label}: image exceeds packaged-content limit: {src}",
        )
        chosen[path] = digest
    # publish_bundle allows one extra asset kind: the same-stem editable SVG of a raster
    # the document uses. It ships only when the reviewer pinned it for this document.
    masters = {
        str(PurePosixPath(src).with_suffix(".svg"))
        for src in referenced
        if PurePosixPath(src).suffix in RASTERS
    }
    for src, digest in approved.items():
        if src in referenced:
            continue
        require(src in masters, f"{label}: review lists an image the document does not use: {src}")
        path = "public" + src
        require(
            path in candidate_assets and sha(candidate_assets[path]) == digest,
            f"{label}: reviewed SVG master changed or is absent: {src}",
        )
        chosen[path] = digest
    return chosen


def native_pack(pack):
    """The deterministic ArticlePack serialization assemble_bundle writes."""
    return (json.dumps(pack.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n").encode(
        "utf-8"
    )


def new_output(output, candidate_root):
    output = Path(output)
    require(
        not output.exists() and not output.is_symlink(),
        "Output already exists; preserve it and choose a new directory",
    )
    parent = output.parent.resolve()
    require(parent.is_dir(), "Output parent directory is absent")
    target = parent / output.name
    for protected, label in ((ROOT, "repository"), (candidate_root.resolve(), "candidate")):
        require(not target.is_relative_to(protected), f"Output must be outside the {label}")
    return target


def promote(staging, target):
    require(not target.exists(), "Output appeared during compilation")
    for attempt in range(5):
        try:
            os.rename(staging, target)
            return
        except PermissionError:
            if os.name != "nt" or attempt == 4:
                raise
            # Windows scanners can briefly hold a file that was just written.
            time.sleep(0.05 * (attempt + 1))


def compile_bundle(
    *,
    candidate,
    candidate_sha256,
    review,
    review_sha256,
    baseline,
    baseline_sha256,
    slugs,
    locales,
    output,
    holds_path=None,
):
    """Write one verified bundle into a new directory, or refuse and leave none."""
    slugs, locales = list(slugs), list(locales)
    require(
        1 <= len(slugs) <= MAX_ARTICLES and len(set(slugs)) == len(slugs),
        "Select one to twenty distinct slugs",
    )
    require(
        bool(locales) and len(set(locales)) == len(locales) and set(locales) <= set(LOCALES),
        "Select distinct supported locales",
    )
    target = new_output(output, Path(candidate).parent)
    pinned_candidate = load_candidate(candidate, candidate_sha256)
    pinned_review = load_review(review, review_sha256)
    pinned_baseline = load_baseline(baseline, baseline_sha256)
    holds, holds_sha256 = read_holds(holds_path)
    today = datetime.now(UTC).date()
    chosen_locales = [locale for locale in LOCALES if locale in locales]
    packs = {}
    assets = {}
    provenance_targets = []
    for slug in sorted(slugs):
        require(
            slug not in HUBS,
            f"{slug}: a hub needs Route A dependency pins; this compiler takes lessons only",
        )
        require(slug in pinned_candidate["packs"], f"{slug}: selection is outside the candidate")
        require(slug in pinned_baseline["articles"], f"{slug}: article is outside the baseline")
        require(slug not in holds, f"{slug}: publication held: {holds.get(slug, '')}")
        article = pinned_baseline["articles"][slug]
        live, baseline_assets = public_source(slug, article, today)
        pack = pinned_candidate["packs"][slug]
        require(set(pack.locales) == set(LOCALES), f"{slug}: full five-language pack required")
        wanted = {key: article["metadata"][key] for key in publish_bundle.metadata(pack)}
        wanted["topics"] = sorted(wanted["topics"])
        require(
            publish_bundle.metadata(pack) == wanted,
            f"{slug}: classification/order differs from the baseline",
        )
        for locale in chosen_locales:
            label = f"{slug}:{locale}"
            require(
                locale != article["source_locale"],
                f"{label}: the source locale cannot be selected; a correction needs "
                "source_correction.py",
            )
            require(
                locale not in article["database"]["locales"],
                f"{label}: target already exists in the baseline; only missing locales compile",
            )
            require(
                locale in article["publication_locales"] and locale in article["target_locales"],
                f"{label}: not a baseline publication target",
            )
            require(
                locale not in pack.aliases,
                f"{label}: the guarded publisher writes documents only, not aliases",
            )
            document = pack.locales[locale].model_dump(mode="json")
            if locale in live:
                # A merged content PR puts the reviewed document in the repository pack the
                # baseline was built from. It must be exactly that document.
                require(
                    article["locale_provenance"][locale] == "repository-only"
                    and live[locale] == document,
                    f"{label}: repository document differs from the reviewed candidate",
                )
            reviewed = pinned_review["targets"].get((slug, locale))
            require(reviewed is not None, f"{label}: selection exceeds the independent review")
            require(
                reviewed["source_sha256"] == article["source_sha256"],
                f"{label}: review is stale; the source changed after it",
            )
            require(
                reviewed["document_sha256"] == document_hash(document),
                f"{label}: reviewed document changed",
            )
            images = reviewed_images(
                label,
                pack.locales[locale],
                reviewed,
                pinned_candidate["assets"],
                baseline_assets,
            )
            assets.update(images)
            provenance_targets.append(
                {
                    "slug": slug,
                    "locale": locale,
                    "translator": reviewed["translator"],
                    "reviewer": reviewed["reviewer"],
                    "reviewed_at": reviewed["reviewed_at"],
                    "source_sha256": reviewed["source_sha256"],
                    "document_sha256": reviewed["document_sha256"],
                    "repository_document": locale in live,
                    "assets": [
                        {"path": path, "sha256": digest} for path, digest in sorted(images.items())
                    ],
                }
            )
        for locale, document in live.items():
            if locale in chosen_locales:
                continue
            require(
                pack.locales[locale].model_dump(mode="json") == document,
                f"{slug}:{locale}: unselected or source text differs from the baseline",
            )
        packs[slug] = pack
    files = {f"packs/{slug}.json": native_pack(pack) for slug, pack in packs.items()}
    for path in sorted(assets):
        files[path] = pinned_candidate["assets"][path]
    manifest = {
        "schema_version": 1,
        "baseline_sha256": pinned_baseline["sha256"],
        "articles": [
            {
                "slug": slug,
                "pack_path": f"packs/{slug}.json",
                "pack_sha256": sha(files[f"packs/{slug}.json"]),
                "locales": chosen_locales,
                "publish_locales": chosen_locales,
                "hub": False,
            }
            for slug in packs
        ],
        "assets": [{"path": path, "sha256": assets[path]} for path in sorted(assets)],
    }
    manifest_raw = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
    manifest_sha256 = sha(manifest_raw)
    files["release-manifest.json"] = manifest_raw
    provenance = {
        "schema": PROVENANCE_SCHEMA,
        "authorizes_production": False,
        "manifest_sha256": manifest_sha256,
        "compiler_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "candidate": {
            "sha256": pinned_candidate["sha256"],
            "source_git_commit": pinned_candidate["source_git_commit"],
        },
        "review": {
            "sha256": pinned_review["sha256"],
            "evidence_sha256": pinned_review["evidence_sha256"],
        },
        "baseline": {
            "sha256": pinned_baseline["sha256"],
            "repo_commit": pinned_baseline["repo_commit"],
            "captured_at": pinned_baseline["captured_at"],
        },
        "publish_holds_sha256": holds_sha256,
        "selection": {"slugs": list(packs), "locales": chosen_locales},
        "targets": provenance_targets,
        "next": [
            "Review this receipt and release-manifest.json; neither authorizes production.",
            (
                "Run publish_bundle.py dry-run, drafts, publish-articles and publish-hubs with "
                "this bundle, the same baseline, this manifest SHA256 and one state directory."
            ),
        ],
    }
    files[PROVENANCE_FILE] = (
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")
    staging = target.parent / f".{target.name}.partial-{uuid4().hex}"
    staging.mkdir()
    try:
        for relative, data in files.items():
            path = staging / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as handle:
                handle.write(data)
        # The existing publisher contract is the acceptance test: it re-reads every byte.
        bundle = publish_bundle.verify_bundle(staging, pinned_baseline["path"], manifest_sha256)
        for row in provenance_targets:
            document = bundle.packs[row["slug"]].locales[row["locale"]].model_dump(mode="json")
            require(
                document_hash(document) == row["document_sha256"],
                f"{row['slug']}:{row['locale']}: compiled document differs from the review",
            )
        promote(staging, target)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return {
        "status": "compiled",
        "authorizes_production": False,
        "articles": len(packs),
        "documents": len(provenance_targets),
        "assets": len(assets),
        "manifest_sha256": manifest_sha256,
        "output": str(target),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--candidate-sha256", required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--review-sha256", required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--baseline-sha256", required=True)
    parser.add_argument("--slug", action="append", required=True)
    parser.add_argument("--locale", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = compile_bundle(
            candidate=args.candidate,
            candidate_sha256=args.candidate_sha256,
            review=args.review,
            review_sha256=args.review_sha256,
            baseline=args.baseline,
            baseline_sha256=args.baseline_sha256,
            slugs=args.slug,
            locales=args.locale,
            output=args.output,
        )
    except Exception as error:  # noqa: BLE001 -- CLI boundary prints a content-free refusal
        print(
            json.dumps(
                {
                    "status": "refused",
                    "reason": str(error) if isinstance(error, Refused) else type(error).__name__,
                    "next": "No manifest was written; fix the input and use a new output",
                }
            ),
            file=sys.stderr,
        )
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
