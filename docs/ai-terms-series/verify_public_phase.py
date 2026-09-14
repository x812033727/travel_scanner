"""Read-only checks between the AI-terms publication phases.

Example (uses anonymous GET only; never imports or publishes content):
  python verify_public_phase.py --phase drafts --journal /private/journal.json \
    --manifest-sha256 <reviewed release-manifest SHA256>

The journal stays private. Reports contain public slugs, hashes and versions only.
Requests are sequential and at least 0.55 seconds apart, including image requests.
HTTP 403/429 stop the run immediately; there are no automatic retries or redirects.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LOCALE = "zh-TW"
INDEX = "ai-terms-index"
PACK_PREFIX = "apps/api/app/guides/content/"
ASSET_PREFIX = "apps/web/public/"
REQUEST_INTERVAL = 0.55
REPORTS = {
    "drafts": "draft-public-verification.json",
    "articles": "preindex-public-verification.json",
}


class Refused(RuntimeError):
    """A safe diagnostic which never contains the private journal or its identifiers."""


def require(condition, message):
    if not condition:
        raise Refused(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def valid_hash(value):
    return isinstance(value, str) and re.fullmatch(r"[a-f0-9]{64}", value) is not None


def positive_version(value):
    return type(value) is int and value > 0


def reviewed_scope():
    # Reuse the reviewed literal allowlist without importing the DB-backed publisher.
    tree = ast.parse((HERE / "publish_batch.py").read_text(encoding="utf-8"))
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id in {"SLUGS", "UPDATED"}:
                values[target.id] = ast.literal_eval(node.value)
    slugs = list(values["SLUGS"])
    updated = set(values["UPDATED"])
    require(len(slugs) == len(set(slugs)) == 83, "Reviewed scope must contain 83 slugs")
    require(
        len(updated) == 6 and updated < set(slugs), "Invalid six-article update scope"
    )
    require(INDEX in slugs and INDEX not in updated, "Invalid index scope")
    return slugs, updated


def load_public_helpers():
    spec = importlib.util.spec_from_file_location(
        "ai_terms_public_helpers", HERE / "verify_public.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def checked_asset_path(relative):
    require(relative.startswith(ASSET_PREFIX), "Unexpected asset prefix")
    local = relative.removeprefix(ASSET_PREFIX)
    rel = PurePosixPath(local)
    require(
        local.startswith("guides/")
        and not rel.is_absolute()
        and ".." not in rel.parts
        and bool(re.fullmatch(r"[A-Za-z0-9_./-]+", local)),
        "Unsafe asset path",
    )
    root = (ROOT / "apps/web/public").resolve()
    path = (root / local).resolve()
    require(path.is_relative_to(root), "Asset path escapes public directory")
    return path


def validate_inputs(args, public):
    require(valid_hash(args.manifest_sha256), "Supply the reviewed manifest SHA256")
    raw = args.manifest.read_bytes()
    require(sha(raw) == args.manifest_sha256, "Manifest SHA256 changed")
    manifest = json.loads(raw)
    slugs, updated = reviewed_scope()
    new = set(slugs) - updated
    nonindex = [slug for slug in slugs if slug != INDEX]
    require(
        manifest.get("locale") == LOCALE
        and manifest.get("index_last") == INDEX
        and manifest.get("slugs") == slugs,
        "Manifest must match the exact reviewed 83-slug zh-TW scope",
    )
    require(
        len(manifest.get("new_slugs", [])) == 77
        and set(manifest["new_slugs"]) == new
        and len(manifest.get("updated_slugs", [])) == 6
        and set(manifest["updated_slugs"]) == updated,
        "Manifest new/updated classification changed",
    )
    files = manifest.get("files")
    require(
        isinstance(files, dict) and len(files) == 249,
        "Expected 83 packs and 166 assets",
    )
    require(all(valid_hash(value) for value in files.values()), "Invalid file SHA256")
    expected_files = set()
    wanted = {}
    for slug in slugs:
        key = PACK_PREFIX + slug + ".json"
        data = (ROOT / key).read_bytes()
        require(files.get(key) == sha(data), f"{slug}: local pack bytes changed")
        pack = json.loads(data)
        require(
            pack.get("slug") == slug
            and pack.get("kind") == "life"
            and set(pack.get("locales", {})) == {LOCALE},
            f"{slug}: pack scope changed",
        )
        document = public.GuideDocument.model_validate(pack["locales"][LOCALE])
        wanted[slug] = public.document_hash(document.model_dump(mode="json"))
        expected_files.add(key)
        require(document.hero is not None, f"{slug}: missing reviewed hero")
        sources = [document.hero.src] + [
            block.src for block in document.blocks if block.type == "image"
        ]
        for source in sources:
            require(source.startswith("/guides/"), f"{slug}: unexpected image location")
            asset_key = ASSET_PREFIX + source.lstrip("/")
            asset_path = checked_asset_path(asset_key)
            require(
                files.get(asset_key) == sha(asset_path.read_bytes()),
                "Local asset bytes changed",
            )
            expected_files.add(asset_key)
    assets = [
        (key, value) for key, value in files.items() if key.startswith(ASSET_PREFIX)
    ]
    require(
        len(assets) == 166 and set(files) == expected_files, "Asset/file scope changed"
    )

    journal = json.loads(args.journal.read_text(encoding="utf-8"))
    require(
        journal.get("schema") == 1
        and journal.get("locale") == LOCALE
        and journal.get("manifest_sha256") == args.manifest_sha256
        and journal.get("slugs") == slugs
        and journal.get("dry_run") is True,
        "Journal does not match the reviewed bundle",
    )
    require(
        "pending" in journal and journal["pending"] is None,
        "Journal has an unresolved intent",
    )
    done = journal.get("done")
    require(
        isinstance(done, dict)
        and set(done) == {"drafts", "publish-articles", "publish-index"},
        "Journal phase scope changed",
    )
    require(done["drafts"] == slugs, "Draft phase is incomplete")
    require(done["publish-index"] == [], "Index publication has already begun")
    require(
        done["publish-articles"] == ([] if args.phase == "drafts" else nonindex),
        "Journal does not describe the requested completed phase",
    )
    expected = journal.get("expected")
    require(
        isinstance(expected, dict) and set(expected) == set(slugs),
        "Journal snapshot scope changed",
    )
    # Keep only the public comparison fields; never return actor or database identifiers.
    pins = {}
    for slug in slugs:
        article = expected[slug]
        require(
            isinstance(article, dict)
            and article.get("is_active") is True
            and article.get("kind") == "life",
            f"{slug}: invalid article state",
        )
        locale = article.get("locales", {}).get(LOCALE)
        require(isinstance(locale, dict), f"{slug}: missing zh-TW snapshot")
        require(
            positive_version(locale.get("version"))
            and locale.get("draft_sha256") == wanted[slug],
            f"{slug}: journal draft does not match the reviewed pack",
        )
        hidden = slug in new if args.phase == "drafts" else slug == INDEX
        if hidden:
            require(
                locale.get("published_version") is None
                and locale.get("published_at") is None
                and locale.get("published_sha256") is None,
                f"{slug}: journal no longer describes a hidden draft",
            )
        else:
            require(
                positive_version(locale.get("published_version"))
                and valid_hash(locale.get("published_sha256"))
                and locale["version"] >= locale["published_version"],
                f"{slug}: invalid public revision pin",
            )
            if args.phase == "articles":
                require(
                    locale["version"] == locale["published_version"]
                    and locale["published_sha256"] == wanted[slug],
                    f"{slug}: journal publication differs from reviewed content",
                )
        pins[slug] = {
            "published_version": locale.get("published_version"),
            "published_sha256": locale.get("published_sha256"),
        }
    return slugs, updated, assets, pins


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class AnonymousReader:
    def __init__(self, base, *, opener=None, clock=time.monotonic, pause=time.sleep):
        self.base = base
        self.opener = opener or urllib.request.build_opener(NoRedirect())
        self.clock = clock
        self.pause = pause
        self.next_request = 0.0
        self.requests = 0

    def fetch(self, path, expected_status):
        require(
            path.startswith("/") and not path.startswith("//"), "Invalid public path"
        )
        delay = self.next_request - self.clock()
        if delay > 0:
            self.pause(delay)
        self.next_request = self.clock() + REQUEST_INTERVAL
        self.requests += 1
        request = urllib.request.Request(
            self.base + path,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; MokaairPublicationCheck/1.0)",
                "Cache-Control": "no-cache",
            },
            method="GET",
        )
        try:
            with self.opener.open(request, timeout=45) as response:
                status = response.status
                headers = dict(response.headers)
                url = response.geturl()
                data = response.read()
        except urllib.error.HTTPError as error:
            status = error.code
            headers = dict(error.headers or {})
            url = error.geturl()
            data = b""
            error.close()
        require(status not in {403, 429}, f"HTTP {status}: stopped without retries")
        require(
            status == expected_status,
            f"{path}: expected HTTP {expected_status}, got {status}",
        )
        require(url == self.base + path, f"{path}: unexpected redirect")
        return data, headers, url

    def get(self, path):
        return self.fetch(path, 200)


def hidden_article(slug, reader):
    reader.fetch("/api/travel/guides/life/" + slug + "?locale=zh-TW", 404)
    reader.fetch("/zh-TW/life/" + slug, 404)
    return {"slug": slug, "api_status": 404, "html_status": 404, "status": "pass"}


def preserved_article(slug, pin, reader, public):
    payload, _, _ = reader.get("/api/travel/guides/life/" + slug + "?locale=zh-TW")
    result = json.loads(payload)
    require(
        result.get("status") == "published"
        and result.get("locale") == LOCALE
        and result.get("slug") == slug,
        f"{slug}: unexpected public API identity",
    )
    document = result["document"]
    normalized = public.GuideDocument.model_validate(
        {key: document[key] for key in public.GuideDocument.model_fields}
    )
    actual_hash = public.document_hash(normalized.model_dump(mode="json"))
    require(
        actual_hash == pin["published_sha256"],
        f"{slug}: previous public content changed",
    )
    require(
        positive_version(document.get("version"))
        and document["version"] == pin["published_version"],
        f"{slug}: previous public version changed",
    )
    path = "/zh-TW/life/" + slug
    raw, _, url = reader.get(path)
    metadata = public.Metadata()
    metadata.feed(raw.decode("utf-8"))
    require(metadata.canonical == [public.BASE + path], f"{slug}: canonical differs")
    return {
        "slug": slug,
        "url": url,
        "document_sha256": actual_hash,
        "version": document["version"],
        "canonical": metadata.canonical[0],
        "api_status": 200,
        "html_status": 200,
        "status": "pass",
    }


def check_phase(args, public, reader):
    slugs, updated, assets, pins = validate_inputs(args, public)
    hidden, articles, checked_assets = [], [], []
    original_get = public.get
    public.get = reader.get
    try:
        for slug in slugs:
            is_hidden = slug not in updated if args.phase == "drafts" else slug == INDEX
            if is_hidden:
                hidden.append(hidden_article(slug, reader))
            elif args.phase == "drafts":
                articles.append(preserved_article(slug, pins[slug], reader, public))
            else:
                result = public.article(slug)
                require(
                    result["version"] == pins[slug]["published_version"]
                    and result["document_sha256"] == pins[slug]["published_sha256"],
                    f"{slug}: public revision differs from journal",
                )
                articles.append(
                    {
                        key: result[key]
                        for key in (
                            "slug",
                            "url",
                            "document_sha256",
                            "version",
                            "canonical",
                            "status",
                        )
                    }
                )
        if args.phase == "articles":
            for item in assets:
                result = public.asset(item)
                checked_assets.append(
                    {key: result[key] for key in ("path", "sha256", "bytes", "status")}
                )
    finally:
        public.get = original_get
    return {
        "checked_at": datetime.now(UTC).isoformat(),
        "phase": args.phase,
        "locale": LOCALE,
        "manifest_sha256": args.manifest_sha256,
        "status": "passed",
        "hidden": hidden,
        "articles": articles,
        "assets": checked_assets,
        "http_requests": reader.requests,
        "minimum_request_interval_seconds": REQUEST_INTERVAL,
    }


def write_report(path, report):
    temporary = path.with_suffix(".json.tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=REPORTS, required=True)
    parser.add_argument(
        "--journal",
        type=Path,
        required=True,
        help="Private downloaded journal snapshot",
    )
    parser.add_argument("--manifest", type=Path, default=HERE / "release-manifest.json")
    parser.add_argument("--manifest-sha256", required=True)
    args = parser.parse_args(argv)
    reader = None
    try:
        require(
            not sys.flags.optimize,
            "Run without Python optimization; helper assertions are required",
        )
        public = load_public_helpers()
        reader = AnonymousReader(public.BASE)
        result = check_phase(args, public, reader)
    except Exception as error:  # noqa: BLE001 - redact private paths and journal/schema values
        result = {
            "checked_at": datetime.now(UTC).isoformat(),
            "phase": args.phase,
            "locale": LOCALE,
            "status": "failed",
            "error_type": type(error).__name__,
            "reason": str(error)
            if isinstance(error, Refused)
            else "Verification could not complete",
            "http_requests": reader.requests if reader else 0,
        }
    try:
        # A failed run replaces any previous passed report with an explicit failure.
        write_report(HERE / REPORTS[args.phase], result)
    except OSError:
        print(
            json.dumps(
                {
                    "phase": args.phase,
                    "status": "failed",
                    "reason": "Could not write verification report",
                }
            )
        )
        return 1
    print(
        json.dumps(
            {
                "phase": args.phase,
                "status": result["status"],
                "hidden": len(result.get("hidden", [])),
                "articles": len(result.get("articles", [])),
                "assets": len(result.get("assets", [])),
                "http_requests": result["http_requests"],
            }
        )
    )
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
