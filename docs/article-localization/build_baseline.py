"""Pin the source documents and current publication state before translating anything."""

import copy
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

from app.guides.schemas import GuideDocument

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
LOCALES = ["zh-TW", "en", "ja", "ko", "zh-CN"]


def digest(value):
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, ensure_ascii=False, separators=(",", ":")
        ).encode()
    ).hexdigest()


def normalized(value):
    return GuideDocument.model_validate(value).model_dump(mode="json")


def locale_work(documents, published, status):
    """Keep authoring gaps separate from publication gaps.

    A public article can already have a complete repository document or database
    draft that only needs independent review and publication. Such a locale is a
    release target, but it must never be sent through translation again.
    """
    existing = set(documents)
    published = set(published)
    translation_missing = [locale for locale in LOCALES if locale not in existing]
    publication_missing = (
        [locale for locale in LOCALES if locale not in published]
        if status == "published"
        else []
    )
    targets = set(translation_missing) | set(publication_missing)
    return {
        # Keep the old name for consumers that have not yet migrated. Its
        # meaning remains strictly "no document exists".
        "missing_locales": translation_missing,
        "translation_missing_locales": translation_missing,
        "publication_missing_locales": publication_missing,
        "publication_locales": publication_missing,
        "target_locales": [locale for locale in LOCALES if locale in targets],
    }


def locale_provenance(repository_locales, database_locales):
    result = {locale: "repository-only" for locale in repository_locales}
    for locale, row in database_locales.items():
        result[locale] = (
            "database-published"
            if row["published_version"] is not None
            else "database-draft"
        )
    return result


def main():
    snapshot = json.loads(
        (OUT / "production-baseline.json").read_text(encoding="utf-8-sig")
    )
    live = {a["slug"]: a for a in snapshot["articles"]}
    packs = {}
    for path in sorted((ROOT / "apps/api/app/guides/content").glob("*.json")):
        packs[path.stem] = (path, json.loads(path.read_text(encoding="utf-8")))
    if set(live) - set(packs):
        raise ValueError(
            f"Export database-only articles first: {sorted(set(live) - set(packs))}"
        )
    articles = []
    differences = []
    for slug, (path, pack) in packs.items():
        state = live.get(slug)
        repository_documents = {
            locale: normalized(doc) for locale, doc in pack["locales"].items()
        }
        documents = copy.deepcopy(repository_documents)
        provenance = locale_provenance(documents, state["locales"] if state else {})
        published = []
        database = None
        if state:
            database = {"id": state["id"], "version": state["version"], "locales": {}}
            for locale, row in state["locales"].items():
                database["locales"][locale] = {
                    key: row[key]
                    for key in (
                        "id",
                        "version",
                        "published_version",
                        "published_sha256",
                        "draft_sha256",
                    )
                }
                current = row["published"] or row["draft"]
                if locale in documents and digest(documents[locale]) != digest(current):
                    differences.append(
                        {
                            "slug": slug,
                            "locale": locale,
                            "repository_sha256": digest(documents[locale]),
                            "database_sha256": digest(current),
                            "selected": "database",
                        }
                    )
                documents[locale] = current
                if row["published_version"] is not None:
                    published.append(locale)
        source_locale = next(
            locale
            for locale in LOCALES
            if locale in documents and (not published or locale in published)
        )
        metadata_source = state or pack
        metadata = {
            key: metadata_source.get(key, default)
            for key, default in (
                ("slug", slug),
                ("kind", pack["kind"]),
                ("destination_id", None),
                ("topics", []),
                ("valid_until", None),
                ("featured", False),
                ("display_order", 100),
            )
        }
        sources = set()
        for doc in documents.values():
            if doc.get("hero"):
                sources.add(doc["hero"]["src"])
            sources.update(
                block["src"] for block in doc["blocks"] if block["type"] == "image"
            )
        assets = []
        for src in sorted(sources):
            asset = ROOT / "apps/web/public" / src.lstrip("/")
            if not asset.is_file():
                raise ValueError(f"Missing source image {src}")
            assets.append(
                {"src": src, "sha256": hashlib.sha256(asset.read_bytes()).hexdigest()}
            )
        work = locale_work(documents, published, state["status"] if state else "draft")
        articles.append(
            {
                "slug": slug,
                "kind": pack["kind"],
                "status": state["status"] if state else "draft",
                "pack_path": path.relative_to(ROOT).as_posix(),
                "pack_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "metadata": metadata,
                "source_locale": source_locale,
                "source_document": documents[source_locale],
                "source_sha256": digest(documents[source_locale]),
                "existing_locales": [
                    locale for locale in LOCALES if locale in documents
                ],
                **work,
                "locale_provenance": {
                    locale: provenance[locale]
                    for locale in LOCALES
                    if locale in provenance
                },
                "published_locales": [
                    locale for locale in LOCALES if locale in published
                ],
                "locale_documents": documents,
                "database": database,
                "assets": assets,
            }
        )
    pending = sorted(
        (a for a in articles if a["target_locales"]),
        key=lambda a: (a["status"] != "published", a["kind"], a["slug"]),
    )
    batches = []
    for start in range(0, len(pending), 20):
        batch = f"batch-{start // 20 + 1:03d}"
        group = pending[start : start + 20]
        for article in group:
            article["batch"] = batch
            article["batch_locales"] = article["target_locales"]
        batches.append(
            {
                "id": batch,
                "slugs": [a["slug"] for a in group],
                "targets": [
                    {"slug": a["slug"], "locales": a["target_locales"]} for a in group
                ],
            }
        )
    summary = {
        "articles": len(articles),
        "complete_packs": sum(not a["translation_missing_locales"] for a in articles),
        "statuses": dict(Counter(a["status"] for a in articles)),
        "missing_language_documents": sum(
            len(a["translation_missing_locales"]) for a in articles
        ),
        "translation_missing_language_documents": sum(
            len(a["translation_missing_locales"]) for a in articles
        ),
        "published_missing_languages": sum(
            len(a["publication_missing_locales"]) for a in articles
        ),
        "publication_missing_language_documents": sum(
            len(a["publication_missing_locales"]) for a in articles
        ),
        "repository_database_differences": len(differences),
        "batches": len(batches),
    }
    baseline = {
        "schema_version": 1,
        "repo_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "captured_at": snapshot["captured_at"],
        "locales": LOCALES,
        "summary": summary,
        "articles": articles,
        "batches": batches,
    }
    for name, value in (
        ("baseline.json", baseline),
        ("source-differences.json", differences),
    ):
        (OUT / name).write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
