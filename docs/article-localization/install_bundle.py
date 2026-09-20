"""Install an explicitly pinned, reviewed bundle locally; never import or publish.

The durable journal records original bytes before any content changes. Interrupted
installs resume only when every destination still equals its recorded before/after
hash. Completed per-article receipts let the translation pipeline retain its
original baseline without treating this exact admitted installation as drift.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps/api"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


publisher = load(
    "installation_publisher", Path(__file__).with_name("publish_bundle.py")
)
assembler = load(
    "installation_assembler", Path(__file__).with_name("assemble_bundle.py")
)
pipeline = assembler.pipeline
require = publisher.require
STATE = "docs/article-localization/installations"


def relative(root, path):
    value = path.resolve()
    require(
        value.is_relative_to(root.resolve()),
        "Installation inputs must be inside repository",
    )
    return value.relative_to(root.resolve()).as_posix()


def destination(root, path):
    value = publisher.safe_path(root, path)
    # Refuse links even if their targets stay inside the repository.
    current = root / path
    while current != root:
        require(not current.is_symlink(), "Installation destination contains a symlink")
        current = current.parent
    return value


def optional_hash(path):
    return publisher.sha(path.read_bytes()) if path.is_file() else None


def write_bytes(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.install-{os.getpid()}.tmp")
    with temporary.open("wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def backup_path(directory, operation):
    # Keep Windows paths below MAX_PATH; the journal retains and verifies full hashes.
    return directory / "backups" / f"{operation['before_sha256'][:24]}.bin"


def reviewed_jobs(bundle, work):
    """Bind selected documents back to their independent editorial/image reviews."""
    jobs = {}
    for entry in bundle.entries:
        article = bundle.baseline[entry["slug"]]
        selected = {}
        for locale in entry["locales"]:
            wanted = bundle.packs[entry["slug"]].locales[locale].model_dump(mode="json")
            existing = article["locale_documents"].get(locale)
            if existing is not None and wanted == publisher.normalized(existing):
                continue
            directory = work / entry["slug"] / locale
            document, _ = assembler.reviewed_document(directory, article, locale)
            source = pipeline.read_json(directory / "source.json")
            require(
                source["slug"] == entry["slug"]
                and source["locale"] == locale
                and source["pack_path"] == article["pack_path"]
                and source["pack_sha256"] == article["pack_sha256"]
                and source["baseline_source_sha256"] == article["source_sha256"]
                and pipeline.digest(
                    {k: v for k, v in source.items() if k != "job_sha256"}
                )
                == source["job_sha256"],
                "Reviewed source job differs from pinned baseline",
            )
            if existing is None:
                document, _ = assembler.localize_links(
                    document, locale, bundle.baseline
                )
            require(
                document == wanted,
                "Installed document differs from independently reviewed content",
            )
            selected[locale] = {
                "job_sha256": source["job_sha256"],
                "source_sha256": source["source_sha256"],
                "source_job_sha256": pipeline.file_hash(directory / "source.json"),
                "artifact_manifest_sha256": pipeline.file_hash(
                    directory / "artifact-manifest.json"
                ),
                "review_sha256": pipeline.file_hash(directory / "review.json"),
            }
        jobs[entry["slug"]] = selected
    return jobs


def install(bundle_path, baseline_path, pinned_sha, work, *, root=ROOT):
    root = root.resolve()
    bundle_path, baseline_path, work = (
        bundle_path.resolve(),
        baseline_path.resolve(),
        work.resolve(),
    )
    bundle_relative = relative(root, bundle_path)
    baseline_relative = relative(root, baseline_path)
    work_relative = relative(root, work)
    state = destination(root, STATE)
    with publisher.journal_lock(state):
        bundle = publisher.verify_bundle(bundle_path, baseline_path, pinned_sha)
        jobs = reviewed_jobs(bundle, work)
        directory = state / "bundles" / pinned_sha[:16]
        journal_path = directory / "journal.json"
        journal_relative = relative(root, journal_path)
        prior = pipeline.read_json(journal_path) if journal_path.exists() else None
        if prior:
            require(
                prior.get("schema_version") == 1
                and prior.get("manifest_sha256") == pinned_sha
                and prior.get("status") in {"installing", "installed"}
                and isinstance(prior.get("files"), list),
                "Installation journal is invalid or its pin changed",
            )
        prior_files = {item["path"]: item for item in prior["files"]} if prior else {}
        operations = []
        for entry in bundle.entries:
            article = bundle.baseline[entry["slug"]]
            require(
                article["pack_path"]
                == f"apps/api/app/guides/content/{entry['slug']}.json",
                "Unexpected repository article path",
            )
            for asset in article["assets"]:
                require(
                    optional_hash(
                        destination(root, "apps/web/public/" + asset["src"].lstrip("/"))
                    )
                    == asset["sha256"],
                    "Original article image changed after baseline",
                )
            operations.append(
                {
                    "path": article["pack_path"],
                    "source": entry["pack_path"],
                    "before_sha256": article["pack_sha256"],
                    "after_sha256": entry["pack_sha256"],
                }
            )
        # Assets first: a partially installed article never references missing new assets.
        for asset in reversed(bundle.manifest["assets"]):
            path = "apps/web/" + asset["path"]
            before = (
                prior_files[path]["before_sha256"]
                if path in prior_files
                else optional_hash(destination(root, path))
            )
            require(
                before in (None, asset["sha256"]), "Existing image would be overwritten"
            )
            operations.insert(
                0,
                {
                    "path": path,
                    "source": asset["path"],
                    "before_sha256": before,
                    "after_sha256": asset["sha256"],
                },
            )
        require(
            len({item["path"] for item in operations}) == len(operations),
            "Repeated install destination",
        )
        identity = {
            "schema_version": 1,
            "manifest_sha256": pinned_sha,
            "bundle_path": bundle_relative,
            "baseline_path": baseline_relative,
            "baseline_sha256": bundle.manifest["baseline_sha256"],
            "work_path": work_relative,
            "journal_path": journal_relative,
            "jobs": jobs,
            "files": operations,
        }
        if prior:
            require(
                all(prior.get(key) == value for key, value in identity.items()),
                "Installation intent changed",
            )
        for operation in operations:
            current = optional_hash(destination(root, operation["path"]))
            accepted = {operation["before_sha256"]}
            if prior:
                accepted.add(operation["after_sha256"])
            require(current in accepted, f"Destination drift: {operation['path']}")
        for entry in bundle.entries:
            existing_receipt = state / f"{entry['slug']}.json"
            if existing_receipt.exists():
                require(
                    pipeline.read_json(existing_receipt).get("manifest_sha256")
                    == pinned_sha,
                    "Article already belongs to another admitted installation",
                )
        if not prior:
            # Verify/copy every original before recording any intent or mutating content.
            for operation in operations:
                if operation["before_sha256"] is not None:
                    original = destination(root, operation["path"]).read_bytes()
                    require(
                        publisher.sha(original) == operation["before_sha256"],
                        "Source changed while backing up",
                    )
                    backup = backup_path(directory, operation)
                    require(
                        not backup.exists()
                        or optional_hash(backup) == operation["before_sha256"],
                        "Backup name collision or prior backup drift",
                    )
                    write_bytes(backup, original)
            prior = {
                **identity,
                "created_at": publisher.stamp(),
                "status": "installing",
            }
            publisher.persist(journal_path, prior)
        for operation in operations:
            if operation["before_sha256"] is not None:
                require(
                    optional_hash(backup_path(directory, operation))
                    == operation["before_sha256"],
                    "Original byte backup is missing or changed",
                )
        for operation in operations:
            path = destination(root, operation["path"])
            current = optional_hash(path)
            require(
                current in {operation["before_sha256"], operation["after_sha256"]},
                "Destination changed during installation",
            )
            if current != operation["after_sha256"]:
                data = publisher.safe_path(
                    bundle_path, operation["source"]
                ).read_bytes()
                require(
                    publisher.sha(data) == operation["after_sha256"],
                    "Bundle changed during installation",
                )
                # Recheck after reading source bytes, directly before replacing destination.
                require(optional_hash(path) == current, "Concurrent destination edit")
                write_bytes(path, data)
            require(
                optional_hash(path) == operation["after_sha256"],
                "Installed bytes failed verification",
            )
        publisher.verify_bundle(bundle_path, baseline_path, pinned_sha)
        require(
            reviewed_jobs(bundle, work) == jobs,
            "Reviewed source jobs changed during installation",
        )
        for operation in operations:
            require(
                optional_hash(destination(root, operation["path"]))
                == operation["after_sha256"],
                "Final installation drift",
            )
        completed = {**prior, "status": "installed"}
        if completed != prior:
            publisher.persist(journal_path, completed)
        prior = completed
        journal_sha256 = pipeline.file_hash(journal_path)
        for entry in bundle.entries:
            article = bundle.baseline[entry["slug"]]
            receipt = {
                "schema_version": 1,
                "status": "installed",
                "slug": entry["slug"],
                "manifest_sha256": pinned_sha,
                "bundle_path": bundle_relative,
                "baseline_path": baseline_relative,
                "baseline_sha256": bundle.manifest["baseline_sha256"],
                "work_path": work_relative,
                "journal_path": journal_relative,
                "journal_sha256": journal_sha256,
                "pack_path": article["pack_path"],
                "original_pack_sha256": article["pack_sha256"],
                "installed_pack_sha256": entry["pack_sha256"],
                "source_sha256": article["source_sha256"],
                "jobs": jobs[entry["slug"]],
                "created_at": prior["created_at"],
            }
            publisher.persist(state / f"{entry['slug']}.json", receipt)
    return {
        "status": "installed",
        "articles": bundle.slugs,
        "files": len(operations),
        "manifest_sha256": pinned_sha,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument(
        "--work", type=Path, default=ROOT / "docs/article-localization/work"
    )
    args = parser.parse_args()
    print(
        json.dumps(install(args.bundle, args.baseline, args.manifest_sha256, args.work))
    )


if __name__ == "__main__":
    main()
