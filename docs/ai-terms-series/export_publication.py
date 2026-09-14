"""Export a public receipt from completed, local publication evidence only.

Requires private downloaded --release-state, --journal and --backup-receipt files,
the reviewed --release-sha and --manifest-sha256, and every final QA report beside
this script. No network, database, SSH, container or publication action is performed.
Only a fully consistent result writes publication.json; refusal leaves it untouched.
Private snapshots are never copied into the output or exception diagnostics.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = "https://mokaair.com"
LOCALE = "zh-TW"
INDEX = "ai-terms-index"
GLOSSARY = "ai-glossary-50-terms"
PACK_PREFIX = "apps/api/app/guides/content/"
ASSET_PREFIX = "apps/web/public/"
SERVICES = {
    "api",
    "web",
    "worker",
    "alert-worker",
    "alert-scheduler",
    "hotspot-collector",
    "analytics-scheduler",
    "community-sweeper",
}
TABLE_PAGES = {
    "bangkok-airport-to-city": "/zh-TW/guides/howto/bangkok-airport-to-city",
    "ai-model-tiers-explained": "/zh-TW/life/ai-model-tiers-explained",
    "privacy": "/zh-TW/privacy",
}
TABLE_SOURCES = {
    "apps/api/app/guides/content/bangkok-airport-to-city.json",
    "apps/api/app/guides/content/ai-model-tiers-explained.json",
    "apps/web/components/content-blocks.tsx",
    "apps/web/components/guides/article.tsx",
    "apps/web/components/site-information-page.tsx",
    "apps/web/components/site-page-content.tsx",
    "apps/web/app/[locale]/privacy/page.tsx",
    "apps/web/app/[locale]/terms/page.tsx",
}
REPORT_NAMES = (
    "public-verification",
    "live-browser-check",
    "table-live-regression",
    "draft-public-verification",
    "preindex-public-verification",
    "postgresql-validation",
)


class Refused(RuntimeError):
    """Safe public diagnostic; never interpolate private values or paths."""


def require(condition, message):
    if not condition:
        raise Refused(message)


def sha(data):
    import hashlib

    return hashlib.sha256(data).hexdigest()


def valid_hash(value, length=64):
    return (
        isinstance(value, str)
        and re.fullmatch(r"[a-f0-9]{" + str(length) + "}", value) is not None
    )


def positive(value):
    return type(value) is int and value > 0


def timestamp(value, label):
    require(isinstance(value, str), label + ": missing timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise Refused(label + ": invalid timestamp") from None
    require(parsed.utcoffset() is not None, label + ": timestamp needs a timezone")
    require(
        parsed <= datetime.now(UTC) + timedelta(minutes=5), label + ": future timestamp"
    )
    return parsed


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_helpers():
    spec = importlib.util.spec_from_file_location(
        "receipt_phase_helpers", HERE / "verify_public_phase.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.load_public_helpers()


def exact_rows(rows, expected, key, label):
    require(
        isinstance(rows, list) and len(rows) == len(expected), label + ": count differs"
    )
    require(all(isinstance(row, dict) for row in rows), label + ": invalid row")
    keys = [row.get(key) for row in rows]
    require(
        len(set(keys)) == len(keys) and set(keys) == set(expected),
        label + ": scope differs",
    )
    return {row[key]: row for row in rows}


def bundle(args, helpers, public):
    raw = (HERE / "release-manifest.json").read_bytes()
    require(
        valid_hash(args.manifest_sha256) and sha(raw) == args.manifest_sha256,
        "Reviewed manifest SHA256 differs",
    )
    manifest = json.loads(raw)
    slugs, updated = helpers.reviewed_scope()
    require(
        manifest.get("locale") == LOCALE
        and manifest.get("slugs") == slugs
        and manifest.get("index_last") == INDEX
        and GLOSSARY in slugs,
        "Expected the exact 83-page zh-TW manifest",
    )
    require(
        len(manifest.get("new_slugs", [])) == 77
        and set(manifest["new_slugs"]) == set(slugs) - updated
        and len(manifest.get("updated_slugs", [])) == 6
        and set(manifest["updated_slugs"]) == updated,
        "Manifest new/updated classification differs",
    )
    files = manifest.get("files")
    require(
        isinstance(files, dict)
        and len(files) == 249
        and all(valid_hash(h) for h in files.values()),
        "Expected 83 pack hashes and 166 asset hashes",
    )
    documents, assets, used = {}, {}, set()
    for slug in slugs:
        key = PACK_PREFIX + slug + ".json"
        raw = (ROOT / key).read_bytes()
        require(files.get(key) == sha(raw), slug + ": local pack bytes differ")
        pack = json.loads(raw)
        require(
            pack.get("slug") == slug
            and pack.get("kind") == "life"
            and set(pack.get("locales", {})) == {LOCALE},
            slug + ": pack identity differs",
        )
        doc = public.GuideDocument.model_validate(pack["locales"][LOCALE])
        require(doc.hero is not None, slug + ": missing hero")
        sources = [doc.hero.src] + [
            block.src for block in doc.blocks if block.type == "image"
        ]
        require(
            len(sources) == 2 and len(set(sources)) == 2,
            slug + ": expected two distinct images",
        )
        documents[slug] = {
            "title": doc.title,
            "hash": public.document_hash(doc.model_dump(mode="json")),
            "pack_hash": files[key],
            "images": sources,
        }
        used.add(key)
        for source in sources:
            require(source.startswith("/guides/"), slug + ": unexpected image location")
            relative = ASSET_PREFIX + source.lstrip("/")
            raw_asset = helpers.checked_asset_path(relative).read_bytes()
            require(
                files.get(relative) == sha(raw_asset),
                slug + ": local asset bytes differ",
            )
            assets[source] = {"sha256": files[relative], "bytes": len(raw_asset)}
            used.add(relative)
    require(
        len(assets) == 166 and used == set(files), "Manifest asset/file scope differs"
    )
    return slugs, updated, documents, assets


def backup_summary(receipt, label, *, with_time):
    require(
        positive(receipt.get("bytes"))
        and valid_hash(receipt.get("sha256"))
        and receipt.get("index_verified") is True,
        label + ": backup is incomplete or its index was not verified",
    )
    result = {
        "bytes": receipt["bytes"],
        "sha256": receipt["sha256"],
        "index_readable": True,
        "restore_tested": False,
    }
    if with_time:
        timestamp(receipt.get("created_at"), label)
        result["created_at"] = receipt["created_at"]
    return result


def deployment(args, state, backup):
    require(
        valid_hash(args.release_sha, 40) and state.get("target") == args.release_sha,
        "Release target differs from the reviewed full SHA",
    )
    require(
        not state.get("failed_at")
        and not state.get("error")
        and not state.get("rollback_status")
        and state.get("status") in {None, "activated"},
        "Release failed or entered rollback",
    )
    activated = timestamp(state.get("activated_at"), "Release activation")
    require(
        timestamp(state.get("built_at"), "Release build") <= activated,
        "Release build/activation order differs",
    )
    ci = state.get("ci_run")
    require(
        isinstance(ci, str)
        and re.fullmatch(
            r"https://github.com/x812033727/travel_scanner/actions/runs/[0-9]+", ci
        ),
        "Missing verified repository CI run URL",
    )
    images = {name: state.get(name + "_image") for name in ("api", "web")}
    require(
        all(
            isinstance(value, str) and re.fullmatch(r"sha256:[a-f0-9]{64}", value)
            for value in images.values()
        ),
        "Missing immutable deployment image SHA256",
    )
    before, after = state.get("before"), state.get("after")
    require(
        isinstance(before, dict)
        and isinstance(after, dict)
        and set(before) == set(after) == SERVICES | {"postgres", "redis"},
        "Deployment service snapshot scope differs",
    )
    for service in SERVICES:
        row = after[service]
        require(
            row.get("status") == "running"
            and row.get("restarts") == 0
            and row.get("image") == images["web" if service == "web" else "api"],
            "Deployed service image/health differs",
        )
        require(
            row.get("image_tag")
            == "travel-scanner-"
            + ("web" if service == "web" else "api")
            + ":"
            + args.release_sha,
            "Deployed service image tag differs",
        )
        require(
            valid_hash(row.get("env_hash"))
            and row["env_hash"] == before[service].get("env_hash"),
            "Deployed service environment differs",
        )
    require(
        all(
            before[s] == after[s] and after[s].get("status") == "running"
            for s in ("postgres", "redis")
        ),
        "Database/cache service baseline changed",
    )
    predeploy = backup_summary(
        state.get("backup", {}), "Deployment backup", with_time=False
    )
    prepublish = backup_summary(backup, "Publication backup", with_time=True)
    require(
        activated <= timestamp(backup["created_at"], "Publication backup"),
        "Publication backup predates activation",
    )
    return {
        "release_sha": args.release_sha,
        "activated_at": state["activated_at"],
        "ci_url": ci,
        "images": images,
        "backups": {"predeployment": predeploy, "prepublication": prepublish},
    }


def journal_state(args, journal, slugs, documents, backup):
    nonindex = [slug for slug in slugs if slug != INDEX]
    require(
        journal.get("schema") == 1
        and journal.get("locale") == LOCALE
        and journal.get("manifest_sha256") == args.manifest_sha256
        and journal.get("slugs") == slugs
        and journal.get("dry_run") is True,
        "Journal bundle/scope differs",
    )
    require(
        "pending" in journal and journal["pending"] is None,
        "Journal still has an unresolved intent",
    )
    expected_done = {
        "drafts": slugs,
        "publish-articles": nonindex,
        "publish-index": [INDEX],
    }
    require(
        journal.get("done") == expected_done,
        "Journal publication phases are incomplete or out of scope",
    )
    expected = journal.get("expected")
    require(
        isinstance(expected, dict) and set(expected) == set(slugs),
        "Journal final snapshot scope differs",
    )
    pins = {}
    for slug in slugs:
        row = expected[slug]
        require(
            isinstance(row, dict)
            and row.get("kind") == "life"
            and row.get("is_active") is True,
            slug + ": inactive or invalid final article",
        )
        locale = row.get("locales", {}).get(LOCALE, {})
        require(
            positive(locale.get("version"))
            and positive(locale.get("published_version"))
            and locale.get("version") == locale.get("published_version")
            and locale.get("draft_sha256")
            == locale.get("published_sha256")
            == documents[slug]["hash"]
            and locale.get("latest_action") == "published",
            slug + ": current/public revision differs from the reviewed pack",
        )
        timestamp(locale.get("published_at"), slug + " publication")
        pins[slug] = {
            "published_version": locale["published_version"],
            "published_at": locale["published_at"],
            "document_sha256": documents[slug]["hash"],
        }
    history = journal.get("history")
    require(isinstance(history, list), "Journal completion history is missing")
    successful = [
        row
        for row in history
        if row.get("status") in {"committed", "committed_reconciled", "unchanged"}
    ]
    sequence = [
        (phase, slug)
        for phase, phase_slugs in expected_done.items()
        for slug in phase_slugs
    ]
    require(
        [(row.get("phase"), row.get("slug")) for row in successful] == sequence,
        "Journal completion history is incomplete or out of order",
    )
    times = [timestamp(row.get("at"), "Journal completion") for row in successful]
    require(
        times == sorted(times)
        and timestamp(backup["created_at"], "Publication backup") <= times[0],
        "Backup/completion chronology differs",
    )
    require(
        all(row.get("locale") == LOCALE for row in successful),
        "Journal completion locale differs",
    )
    return pins, {
        "drafts_done": times[82],
        "articles_started": times[83],
        "articles_done": times[164],
        "index_done": times[165],
    }


def check_article_rows(rows, slugs, documents, pins, label):
    mapped = exact_rows(rows, slugs, "slug", label)
    for slug, row in mapped.items():
        url = BASE + "/zh-TW/life/" + slug
        require(
            row.get("status") == "pass"
            and row.get("url") == row.get("canonical") == url
            and row.get("document_sha256") == documents[slug]["hash"]
            and type(row.get("version")) is int
            and row["version"] == pins[slug]["published_version"],
            label + ": public article revision or canonical differs",
        )
    return mapped


def check_assets(rows, assets, label):
    mapped = exact_rows(rows, assets, "path", label)
    require(
        all(
            row.get("status") == "pass"
            and row.get("sha256") == assets[path]["sha256"]
            and type(row.get("bytes")) is int
            and row["bytes"] == assets[path]["bytes"]
            for path, row in mapped.items()
        ),
        label + ": asset hash or size differs",
    )


def phase_proofs(args, reports, slugs, updated, documents, assets, pins, times):
    stamps = {}
    for phase, name, hidden_slugs, visible_slugs in (
        ("drafts", "draft-public-verification", set(slugs) - updated, updated),
        ("articles", "preindex-public-verification", {INDEX}, set(slugs) - {INDEX}),
    ):
        report = reports[name]
        require(
            report.get("status") == "passed"
            and report.get("phase") == phase
            and report.get("locale") == LOCALE
            and report.get("manifest_sha256") == args.manifest_sha256,
            name + ": missing completed proof for this manifest",
        )
        hidden = exact_rows(report.get("hidden"), hidden_slugs, "slug", name)
        require(
            all(
                row.get("status") == "pass"
                and row.get("api_status") == row.get("html_status") == 200
                and row.get("api_unpublished") is True
                and row.get("body_hidden") is True
                and row.get("content_links_hidden") is True
                and row.get("noindex") is True
                and row.get("canonical") == BASE + "/zh-TW/life/" + row["slug"]
                for row in hidden.values()
            ),
            name + ": hidden article proof differs",
        )
        visible = exact_rows(report.get("articles"), visible_slugs, "slug", name)
        if phase == "articles":
            check_article_rows(
                list(visible.values()), visible_slugs, documents, pins, name
            )
            check_assets(report.get("assets"), assets, name)
        else:
            require(
                report.get("assets") == [],
                "Draft proof unexpectedly includes an asset phase",
            )
            for slug, row in visible.items():
                url = BASE + "/zh-TW/life/" + slug
                require(
                    row.get("status") == "pass"
                    and row.get("api_status") == row.get("html_status") == 200
                    and row.get("url") == row.get("canonical") == url
                    and valid_hash(row.get("document_sha256"))
                    and positive(row.get("version"))
                    and row["version"] < pins[slug]["published_version"],
                    "Draft proof does not preserve an earlier public revision",
                )
        count = 166 if phase == "drafts" else 332
        require(
            type(report.get("http_requests")) is int
            and report["http_requests"] == count
            and isinstance(report.get("minimum_request_interval_seconds"), (int, float))
            and report["minimum_request_interval_seconds"] >= 0.5,
            name + ": request count/rate differs",
        )
        stamps[phase] = timestamp(report.get("checked_at"), name)
    require(
        times["drafts_done"] <= stamps["drafts"] <= times["articles_started"],
        "Draft proof was not captured between publication phases",
    )
    require(
        times["articles_done"] <= stamps["articles"] <= times["index_done"],
        "Preindex proof was not captured before index publication",
    )


def browser_proof(args, report, slugs, documents, completed):
    require(
        report.get("status") == "passed"
        and report.get("mode") == "full"
        and report.get("origin") == BASE
        and report.get("fullSeriesVerified") is True
        and report.get("manifestSha256") == args.manifest_sha256
        and report.get("fatalError") is None,
        "Full live browser proof is missing",
    )
    require(
        report.get("plannedPages") == 83
        and report.get("plannedViewportChecks") == 166
        and report.get("summary")
        == {"passed": 166, "failed": 0, "notRun": 0, "pagesAttempted": 83},
        "Live browser totals differ",
    )
    started = timestamp(report.get("startedAt"), "Live browser start")
    require(
        completed
        <= started
        <= timestamp(report.get("finishedAt"), "Live browser finish"),
        "Live browser proof predates completed publication",
    )
    rows = report.get("results")
    require(
        isinstance(rows, list) and len(rows) == 166,
        "Live browser viewport count differs",
    )
    expected = {
        (slug, viewport) for slug in slugs for viewport in ("mobile", "desktop")
    }
    require(
        {(row.get("slug"), row.get("viewport")) for row in rows} == expected,
        "Live browser viewport scope differs",
    )
    for row in rows:
        slug = row["slug"]
        url = BASE + "/zh-TW/life/" + slug
        width, height = (375, 812) if row["viewport"] == "mobile" else (1440, 1000)
        require(
            row.get("status") == "passed"
            and row.get("failures") == []
            and row.get("httpStatus") == 200
            and row.get("url") == row.get("finalUrl") == url
            and row.get("canonical") == [url]
            and row.get("width") == width
            and row.get("height") == height
            and row.get("packSha256") == documents[slug]["pack_hash"],
            "Live browser observation contradicts its summary",
        )
        require(
            row.get("h1") == [" ".join(documents[slug]["title"].split())],
            "Live browser article title differs",
        )
        images = exact_rows(
            row.get("images"), documents[slug]["images"], "path", "Live browser images"
        )
        require(
            all(
                image.get("loaded") is True
                and image.get("naturalWidth", 0) > 0
                and image.get("naturalHeight", 0) > 0
                for image in images.values()
            ),
            "Live browser includes an unloaded image",
        )


def table_proof(report, activated):
    require(
        report.get("status") == "passed"
        and report.get("mode") == "run"
        and report.get("origin") == BASE
        and report.get("fatalError") is None
        and report.get("summary") == {"passed": 6, "failed": 0, "notRun": 0}
        and report.get("viewportChecks") == 6,
        "Table regression proof is incomplete",
    )
    require(
        activated
        <= timestamp(report.get("startedAt"), "Table regression start")
        <= timestamp(report.get("finishedAt"), "Table regression finish"),
        "Table regression proof predates activation",
    )
    pages = exact_rows(
        report.get("pages"), TABLE_PAGES, "slug", "Table regression pages"
    )
    require(
        all(row.get("url") == BASE + TABLE_PAGES[slug] for slug, row in pages.items()),
        "Table regression page routes differ",
    )
    sources = exact_rows(
        report.get("sourceEvidence"), TABLE_SOURCES, "file", "Table source evidence"
    )
    require(
        all(
            row.get("sha256") == sha((ROOT / file).read_bytes())
            for file, row in sources.items()
        ),
        "Table renderer/source changed after regression proof",
    )
    rows = report.get("results")
    require(
        isinstance(rows, list)
        and len(rows) == 6
        and {(row.get("slug"), row.get("viewport")) for row in rows}
        == {
            (slug, viewport)
            for slug in TABLE_PAGES
            for viewport in ("mobile", "desktop")
        },
        "Table regression viewport scope differs",
    )
    require(
        all(
            row.get("status") == "passed"
            and row.get("failures") == []
            and row.get("httpStatus") == 200
            and row.get("url") == row.get("finalUrl") == BASE + TABLE_PAGES[row["slug"]]
            for row in rows
        ),
        "Table regression observations contradict the summary",
    )


def postgresql_proof(args, report):
    require(
        report.get("schema") == 1
        and report.get("status") == "passed"
        and report.get("cleanup", {}).get("complete") is True,
        "PostgreSQL validation or cleanup is incomplete",
    )
    checks = report.get("checks", {})
    pg, local = checks.get("postgresql", {}), checks.get("local", {})
    for label, check in (("PostgreSQL", pg), ("Local", local)):
        require(
            check.get("passed") == 4
            and check.get("failed") == 0
            and check.get("skipped") == 0,
            label + " validation has missing, failed or skipped cases",
        )
        cases = check.get("cases")
        require(
            isinstance(cases, list)
            and len(cases) == 4
            and len({row.get("nodeid") for row in cases}) == 4
            and all(row.get("status") == "passed" for row in cases),
            label + " case-level proof differs",
        )
    race = checks.get("index_lock_race", {})
    require(
        race.get("passed") is True and race.get("sqlstate") == "55P03",
        "PostgreSQL index publication race proof is missing",
    )
    tested_bundle = checks.get("bundle", {})
    require(
        tested_bundle.get("passed") is True
        and tested_bundle.get("pack_count") == 83
        and tested_bundle.get("manifest_sha256") == args.manifest_sha256,
        "PostgreSQL tested bundle differs",
    )
    source = checks.get("source", {})
    require(
        valid_hash(source.get("git_ref"), 40), "PostgreSQL source revision is missing"
    )
    # Git stores LF; this Windows checkout may contain CRLF in the driver.
    require(
        source.get("driver_git_sha256")
        == sha((HERE / "publish_batch.py").read_bytes().replace(b"\r\n", b"\n"))
        and source.get("test_sha256")
        == sha((HERE / "test_publish_batch.py").read_bytes().replace(b"\r\n", b"\n")),
        "Publisher driver/tests changed after PostgreSQL validation",
    )
    require(
        isinstance(pg.get("server_version"), str)
        and re.fullmatch(r"[0-9]+(?:\.[0-9]+)+", pg["server_version"]),
        "PostgreSQL server version is missing",
    )
    return {
        "status": "passed",
        "postgresql_passed": 4,
        "local_passed": 4,
        "failed": 0,
        "skipped": 0,
        "server_version": pg["server_version"],
        "index_lock_sqlstate": "55P03",
        "cleanup_complete": True,
        "tested_source_sha": source["git_ref"],
        "driver_sha256": source["driver_git_sha256"],
        "tests_sha256": source["test_sha256"],
    }


def build_receipt(args):
    helpers, public = load_helpers()
    slugs, updated, documents, assets = bundle(args, helpers, public)
    state, journal, backup = (
        read_json(path)
        for path in (args.release_state, args.journal, args.backup_receipt)
    )
    deployed = deployment(args, state, backup)
    pins, times = journal_state(args, journal, slugs, documents, backup)
    reports, evidence = {}, {}
    for name in REPORT_NAMES:
        raw = (HERE / (name + ".json")).read_bytes()
        reports[name] = json.loads(raw)
        evidence[name + ".json"] = sha(raw)
    phase_proofs(args, reports, slugs, updated, documents, assets, pins, times)
    final = reports["public-verification"]
    require(
        final.get("status") == "passed"
        and type(final.get("sitemap_present")) is int
        and final["sitemap_present"] == 83,
        "Final public verification/sitemap proof is incomplete",
    )
    require(
        timestamp(final.get("checked_at"), "Final public verification")
        >= times["index_done"],
        "Final public proof predates index publication",
    )
    check_article_rows(
        final.get("articles"), slugs, documents, pins, "Final public verification"
    )
    check_assets(final.get("assets"), assets, "Final public verification")
    browser_proof(
        args, reports["live-browser-check"], slugs, documents, times["index_done"]
    )
    table_proof(
        reports["table-live-regression"],
        timestamp(state["activated_at"], "Release activation"),
    )
    pg = postgresql_proof(args, reports["postgresql-validation"])
    return {
        "schema": 1,
        "status": "published_and_verified",
        "exported_at": datetime.now(UTC).isoformat(),
        "locale": LOCALE,
        "manifest_sha256": args.manifest_sha256,
        "publication_completed_at": times["index_done"].isoformat(),
        "totals": {
            "pages": 83,
            "new": 77,
            "updated": 6,
            "concepts": 81,
            "excluded": 0,
            "indexes": 1,
            "glossaries": 1,
            "assets": 166,
        },
        "deployment": deployed,
        "verification": {
            "public_articles": 83,
            "assets": 166,
            "sitemap_present": 83,
            "browser_pages": 83,
            "browser_viewports": 166,
            "table_regression_checks": 6,
            "drafts_hidden": 77,
            "drafts_preserved": 6,
            "preindex_public_articles": 82,
            "preindex_hidden": 1,
            "postgresql": pg,
        },
        "evidence_sha256": evidence,
        "articles": [
            {
                "title": documents[slug]["title"],
                "slug": slug,
                "url": BASE + "/zh-TW/life/" + slug,
                "publication_action": "updated" if slug in updated else "new",
                **pins[slug],
            }
            for slug in slugs
        ],
        "limitations": [
            "This receipt summarizes completed local evidence snapshots; it does not perform a new live verification.",
            "Backup index readability was verified; a database restore was not tested.",
            "published_at is the original publication timestamp; updated pages may retain an earlier date.",
            "Sitemap presence is not proof that a search engine has indexed a page.",
        ],
    }


def write_receipt(receipt):
    target = HERE / "publication.json"
    temporary = target.with_suffix(".json.tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(receipt, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, target)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("release-state", "journal", "backup-receipt"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--release-sha", required=True)
    parser.add_argument("--manifest-sha256", required=True)
    args = parser.parse_args(argv)
    try:
        receipt = build_receipt(args)
        write_receipt(receipt)
    except Exception as error:  # noqa: BLE001 - redact private paths, IDs and snapshot values
        print(
            json.dumps(
                {
                    "status": "refused",
                    "reason": str(error)
                    if isinstance(error, Refused)
                    else "Required evidence is missing, invalid, or could not be exported",
                    "publication_written": False,
                }
            )
        )
        return 1
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "pages": 83,
                "new": 77,
                "updated": 6,
                "publication_written": True,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
