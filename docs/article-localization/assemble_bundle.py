"""Assemble at most twenty independently reviewed five-language articles for import.

This writes only a review bundle. It cannot change the application packs or database.
Internal article links in NEW translations become publication-aware ArticleInline
references, so a translated article cannot link to another locale's private draft.
"""

import argparse
import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from app.guides.content_pack import ArticlePack
from app.guides.schemas import GuideDocument

ROOT = Path(__file__).resolve().parents[2]
LOCALES = ("zh-TW", "en", "ja", "ko", "zh-CN")
HUBS = {"gemini-guide", "claude-code-tutorials", "ai-terms-index"}
PIPELINE_SPEC = importlib.util.spec_from_file_location(
    "article_localization_pipeline", ROOT / "tools/article-localization/pipeline.py"
)
pipeline = importlib.util.module_from_spec(PIPELINE_SPEC)
PIPELINE_SPEC.loader.exec_module(pipeline)
CORRECTION_SPEC = importlib.util.spec_from_file_location(
    "article_localization_source_correction", Path(__file__).with_name("source_correction.py")
)
source_correction = importlib.util.module_from_spec(CORRECTION_SPEC)
CORRECTION_SPEC.loader.exec_module(source_correction)
PRESERVATION_SPEC = importlib.util.spec_from_file_location(
    "article_localization_repository_preservation",
    Path(__file__).with_name("repository_preservation.py"),
)
repository_preservation = importlib.util.module_from_spec(PRESERVATION_SPEC)
PRESERVATION_SPEC.loader.exec_module(repository_preservation)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git_blob(revision, path):
    try:
        blob = subprocess.run(
            ["git", "rev-parse", f"{revision}:{path}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise ValueError(f"Pinned Git pack is unavailable: {revision}:{path}") from error
    if not repository_preservation.GIT_HASH.fullmatch(blob):
        raise ValueError(f"Pinned Git pack has invalid blob id: {revision}:{path}")
    return blob


def write_text_lf(path, value):
    """Write text exactly as Git will check it out on every supported platform."""
    Path(path).write_text(
        value.replace("\r\n", "\n").replace("\r", "\n"),
        encoding="utf-8",
        newline="\n",
    )


def digest(document):
    return hashlib.sha256(
        json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def inside(root, relative):
    result = (root / relative).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError(f"Path outside bundle: {relative}")
    return result


def localize_links(document, locale, articles):
    result = copy.deepcopy(document)
    changes = []

    def link(node):
        parsed = urlsplit(node["url"])
        if parsed.hostname not in {"mokaair.com", "www.mokaair.com"}:
            return node
        parts = parsed.path.strip("/").split("/")
        if not parts or parts[0] not in LOCALES:
            return node
        target_slug = None
        if len(parts) == 3 and parts[1] == "life":
            target_slug = parts[2]
        elif len(parts) == 4 and parts[1] == "guides" and parts[2] in {"howto", "intel"}:
            target_slug = parts[3]
        if target_slug:
            if parsed.query or parsed.fragment:
                raise ValueError(f"Review article query/fragment before rewriting: {node['url']}")
            if target_slug not in articles:
                raise ValueError(f"Unknown internal article: {node['url']}")
            reference = {
                "type": "article",
                "text": node["text"],
                "kind": articles[target_slug]["kind"],
                "slug": target_slug,
            }
            changes.append({"from": node["url"], "article": target_slug, "locale": locale})
            return reference
        parts[0] = locale
        url = urlunsplit(parsed._replace(path="/" + "/".join(parts)))
        if url != node["url"]:
            changes.append({"from": node["url"], "to": url})
        return {**node, "url": url}

    for index, block in enumerate(result["blocks"]):
        if block["type"] == "link":
            rewritten = link(block)
            result["blocks"][index] = (
                {"type": "rich_paragraph", "inlines": [rewritten]}
                if rewritten["type"] == "article"
                else rewritten
            )
        elif block["type"] == "rich_paragraph":
            block["inlines"] = [
                link(node) if node["type"] == "link" else node for node in block["inlines"]
            ]
    return GuideDocument.model_validate(result).model_dump(mode="json"), changes


def image_sources(document):
    sources = [document["hero"]["src"]] if document.get("hero") else []
    return sources + [block["src"] for block in document["blocks"] if block["type"] == "image"]


def only_image_paths_changed(before, after):
    def mask(document):
        value = copy.deepcopy(document)
        if value.get("hero"):
            value["hero"]["src"] = "IMAGE"
        for block in value["blocks"]:
            if block["type"] == "image":
                block["src"] = "IMAGE"
        return value

    return mask(before) == mask(after)


def baseline_targets(article):
    """Validate the pinned distinction between translation and release work."""
    required = (
        "translation_missing_locales",
        "publication_missing_locales",
        "publication_locales",
        "target_locales",
        "locale_provenance",
    )
    if any(field not in article for field in required):
        raise ValueError(f"Baseline predates split locale targets; rebuild it: {article['slug']}")
    documents = set(article["locale_documents"])
    published = set(article["published_locales"])
    translation_missing = [locale for locale in LOCALES if locale not in documents]
    publication_missing = (
        [locale for locale in LOCALES if locale not in published]
        if article["status"] == "published"
        else []
    )
    targets = [
        locale
        for locale in LOCALES
        if locale in set(translation_missing) | set(publication_missing)
    ]
    if (
        article["missing_locales"] != translation_missing
        or article["translation_missing_locales"] != translation_missing
        or article["publication_missing_locales"] != publication_missing
        or article["publication_locales"] != publication_missing
        or article["target_locales"] != targets
        or set(article["locale_provenance"]) != documents
        or any(
            source not in {"repository-only", "database-draft", "database-published"}
            for source in article["locale_provenance"].values()
        )
    ):
        raise ValueError(f"Inconsistent baseline locale targets: {article['slug']}")
    if "batch_locales" in article and article["batch_locales"] != targets:
        raise ValueError(f"Inconsistent baseline batch targets: {article['slug']}")
    return set(translation_missing), set(publication_missing), set(targets)


def reviewed_document(directory, article, locale):
    receipt = read(directory / "receipt.json")
    review = read(directory / "review.json")
    source = read(directory / "source.json")
    pipeline.verify_artifacts(directory, source, receipt)
    if review.get("artifact_manifest_sha256") != receipt.get("artifact_manifest_sha256"):
        raise ValueError(f"Review is not bound to current artifacts: {article['slug']}:{locale}")
    document = GuideDocument.model_validate(read(directory / "document.json")).model_dump(
        mode="json"
    )
    rendered = receipt["status"] == "rendered" and receipt.get("automated_layout_passed") is True
    review_only = (
        receipt["status"] == "pending_review"
        and source.get("mode") == "review-only"
        and receipt.get("schema_validated") is True
        and receipt.get("document_sha256") == digest(document)
    )
    if (
        not (rendered or review_only)
        or review.get("text_reviewed") is not True
        or review.get("visual_reviewed") is not True
        or review.get("glyph_reviewed") is not True
    ):
        raise ValueError(f"Incomplete independent review: {article['slug']}:{locale}")
    expected_source = article["locale_documents"].get(locale, article["source_document"])
    if source["source_sha256"] != digest(expected_source):
        raise ValueError(f"Translation source changed: {article['slug']}:{locale}")
    if (
        digest(document) != receipt["document_sha256"]
        or digest(document) != review["document_sha256"]
    ):
        raise ValueError(f"Reviewed document changed: {article['slug']}:{locale}")
    for src in receipt.get("raster_review_required", []):
        assessment = review.get("source_rasters", {}).get(src, {})
        original = next((asset for asset in article["assets"] if asset["src"] == src), None)
        if (
            original is None
            or assessment.get("sha256") != original["sha256"]
            or assessment.get("editorial_overlay") is not False
            or assessment.get("reusable_without_pixel_translation") is not True
            or not assessment.get("reason")
            or (
                assessment.get("caption_review_required") and not assessment.get("caption_reviewed")
            )
        ):
            raise ValueError(
                f"Source raster still needs inspection: {article['slug']}:{locale}:{src}"
            )
    for src, expected in review.get("assets", {}).items():
        if sha(inside(directory / "assets", src.lstrip("/"))) != expected:
            raise ValueError(f"Reviewed asset changed: {src}")
    assets = read(directory / "assets.json")
    for asset in assets:
        for src in {asset["public_svg"], *asset["targets"]}:
            if src not in review.get("assets", {}):
                raise ValueError(f"Asset has no independent review: {src}")
    return document, assets


def hub_requirements(packs, articles, prior_manifests=()):
    """Require every originally public lesson, including API-only catalogue entries."""
    released = {}
    for path in prior_manifests:
        previous = read(path)
        for entry in previous["articles"]:
            pack_path = inside(Path(path).parent, entry["pack_path"])
            if sha(pack_path) != entry["pack_sha256"]:
                raise ValueError(f"Earlier bundle changed: {entry['slug']}")
            pack = read(pack_path)
            for locale in entry["publish_locales"]:
                released[(entry["slug"], locale)] = digest(pack["locales"][locale])
    for article, pack, selected in packs:
        if article["status"] == "published":
            for locale in selected:
                released[(pack.slug, locale)] = digest(pack.locales[locale].model_dump(mode="json"))
    result = {}
    catalogue_root = ROOT / "apps/api/app/guides/series_data"
    catalogues = [read(path) for path in catalogue_root.glob("*.json")]
    for article, pack, selected in packs:
        if article["slug"] not in HUBS or article["status"] != "published" or not selected:
            continue
        referenced = set()
        catalogue_slugs = {
            entry["slug"]
            for catalogue in catalogues
            if catalogue["hub"] == article["slug"]
            for entry in catalogue["entries"]
        }
        for locale in selected:
            document = pack.locales[locale].model_dump(mode="json")
            targets = catalogue_slugs | {
                node["slug"]
                for block in document["blocks"]
                for node in block.get("inlines", [])
                if node["type"] == "article"
            }
            for slug in targets - {article["slug"]}:
                if slug not in articles:
                    raise ValueError(f"Unknown hub lesson: {slug}")
                # Private originals stay private; ArticleInline renders them as text.
                if articles[slug]["status"] == "published":
                    referenced.add((slug, locale))
        requirements = []
        for slug, locale in sorted(referenced):
            expected = released.get((slug, locale))
            if expected is None and locale in articles[slug]["published_locales"]:
                expected = articles[slug]["database"]["locales"][locale]["published_sha256"]
            if expected is None:
                raise ValueError(f"Hub requires an earlier reviewed release: {slug}:{locale}")
            requirements.append({"slug": slug, "locale": locale, "document_sha256": expected})
        result[article["slug"]] = requirements
    return result


def copy_pinned_asset(original, target, expected):
    shutil.copyfile(original, target)
    if sha(target) != expected:
        raise ValueError(f"Asset changed while copying reviewed bytes: {original.name}")
    if target.suffix.lower() == ".svg" and b"\r" in target.read_bytes():
        raise ValueError(f"Reviewed SVG must use LF line endings; re-render it: {original.name}")
    if target.suffix.lower() == ".svg" and any(
        line.rstrip() != line for line in target.read_bytes().splitlines()
    ):
        raise ValueError(
            f"Reviewed SVG contains trailing whitespace; re-render it: {original.name}"
        )


def assemble(
    baseline_path,
    work,
    slugs,
    output,
    prior_manifests=(),
    source_correction_reviews=(),
    repository_preservation_reviews=(),
):
    if not slugs or len(slugs) > 20 or len(slugs) != len(set(slugs)):
        raise ValueError("Choose one to twenty distinct article slugs")
    baseline = read(baseline_path)
    articles = {article["slug"]: article for article in baseline["articles"]}
    if set(slugs) - articles.keys():
        raise ValueError("Selection includes articles outside the pinned baseline")
    if output.exists():
        raise ValueError("Bundle output already exists; preserve it and use a new directory")
    packs = []
    assets_to_copy = {}
    transformations = []
    correction_inputs = {}
    for path in source_correction_reviews:
        review = read(path)
        key = (review.get("slug"), review.get("locale"))
        if key in correction_inputs:
            raise ValueError(f"Repeated source correction review: {key}")
        correction_inputs[key] = (Path(path), review)
    preservation_inputs = {}
    for path in repository_preservation_reviews:
        review = read(path)
        key = (review.get("slug"), review.get("locale"))
        if key in preservation_inputs:
            raise ValueError(f"Repeated repository preservation review: {key}")
        preservation_inputs[key] = (Path(path), review)
    used_corrections = set()
    corrections_by_slug = {}
    used_preservations = set()
    preservations_by_slug = {}

    def remember_asset(src, path, expected):
        if src in assets_to_copy and assets_to_copy[src][1] != expected:
            raise ValueError(f"Conflicting reviewed asset bytes: {src}")
        assets_to_copy[src] = (path, expected)

    for slug in slugs:
        article = articles[slug]
        repository_pack_path = ROOT / article["pack_path"]
        repository_pack_raw = repository_pack_path.read_bytes()
        if hashlib.sha256(repository_pack_raw).hexdigest() != article["pack_sha256"]:
            raise ValueError(f"Source pack changed: {slug}")
        repository_pack = ArticlePack.model_validate_json(repository_pack_raw)
        if repository_pack.slug != slug:
            raise ValueError(f"Source pack slug changed: {slug}")
        translation_targets, publication_targets, targets = baseline_targets(article)
        if not targets and not any(key[0] == slug for key in correction_inputs):
            raise ValueError(f"Article has no missing locale or reviewed correction work: {slug}")
        for locale, document in article["locale_documents"].items():
            if (slug, locale) in correction_inputs or article["database"] is None:
                continue
            pinned_locale = article["database"]["locales"].get(locale)
            if pinned_locale is not None:
                old_hash = pinned_locale["published_sha256"] or pinned_locale["draft_sha256"]
                if (
                    digest(GuideDocument.model_validate(document).model_dump(mode="json"))
                    != old_hash
                ):
                    raise ValueError(
                        f"Published/draft source differs without correction review: {slug}:{locale}"
                    )
        documents = copy.deepcopy(article["locale_documents"])
        selected = []
        preservations = []
        for locale in LOCALES:
            key = (slug, locale)
            if key not in preservation_inputs:
                continue
            if (
                locale in targets
                or locale in article.get("batch_locales", [])
                or key in correction_inputs
            ):
                raise ValueError(
                    f"Repository preservation overlaps selected/source-correction work: "
                    f"{slug}:{locale}"
                )
            if locale not in repository_pack.locales:
                raise ValueError(f"Repository preservation locale is absent: {slug}:{locale}")
            path, review = preservation_inputs[key]
            repository_document = repository_pack.locales[locale].model_dump(mode="json")
            if git_blob(baseline["repo_commit"], article["pack_path"]) != (
                repository_preservation.git_blob_sha1(repository_pack_raw)
            ):
                raise ValueError(f"Repository preservation pack is not at pinned Git commit: {slug}")
            binding = repository_preservation.verify_review(
                review,
                baseline,
                article,
                locale,
                repository_document,
                repository_pack_raw,
            )
            relative = f"reviews/{slug}-{locale}-repository-preservation.json"
            preservations.append(
                {"locale": locale, **binding, "review_path": relative, "review_sha256": sha(path)}
            )
            documents[locale] = repository_document
            used_preservations.add(key)
        preservations_by_slug[slug] = preservations
        corrections = []
        for locale in LOCALES:
            key = (slug, locale)
            if key not in correction_inputs:
                continue
            path, review = correction_inputs[key]
            if locale in targets:
                raise ValueError(f"Source correction overlaps missing-locale job: {slug}:{locale}")
            asset_hashes = {"public" + asset["src"]: asset["sha256"] for asset in article["assets"]}
            binding = source_correction.verify_review(
                review, article, locale, documents[locale], asset_hashes
            )
            relative = f"reviews/{slug}-{locale}.json"
            corrections.append(
                {"locale": locale, **binding, "review_path": relative, "review_sha256": sha(path)}
            )
            selected.append(locale)
            used_corrections.add(key)
        corrections_by_slug[slug] = corrections
        for locale in LOCALES:
            directory = work / slug / locale
            if locale in targets:
                if not (directory / "document.json").is_file():
                    mode = (
                        "translation"
                        if locale in translation_targets
                        else "review-only publication"
                    )
                    raise ValueError(f"Missing {mode} job: {slug}:{locale}")
                doc, generated_assets = reviewed_document(directory, article, locale)
                if locale in documents:
                    if not only_image_paths_changed(documents[locale], doc):
                        raise ValueError(
                            f"Existing complete text must not be overwritten: {slug}:{locale}"
                        )
                else:
                    doc, links = localize_links(doc, locale, articles)
                    transformations.extend(
                        {"slug": slug, "locale": locale, **change} for change in links
                    )
                if (
                    locale not in documents
                    or doc != documents[locale]
                    or locale in publication_targets
                ):
                    selected.append(locale)
                documents[locale] = doc
                for asset in generated_assets:
                    for src in {asset["public_svg"], *asset["targets"]}:
                        remember_asset(
                            src,
                            inside(directory / "assets", src.lstrip("/")),
                            read(directory / "review.json")["assets"][src],
                        )
        if set(documents) != set(LOCALES):
            raise ValueError(f"Article does not have all five languages: {slug}")
        if article["database"] is None:
            selected = list(LOCALES)
        if not selected:
            raise ValueError(f"Article has no reviewed changes to import: {slug}")
        pack = ArticlePack.model_validate({**article["metadata"], "locales": documents})
        if preservations and pack.model_dump(mode="json") != repository_pack.model_dump(mode="json"):
            raise ValueError(
                f"Assembled pack differs from preservation-pinned repository pack: {slug}"
            )
        for locale in selected:
            for src in image_sources(documents[locale]):
                if src not in assets_to_copy:
                    path = inside(ROOT / "apps/web/public", src.lstrip("/"))
                    original = next((a for a in article["assets"] if a["src"] == src), None)
                    if original is None or sha(path) != original["sha256"]:
                        raise ValueError(f"Unpinned source image: {src}")
                    remember_asset(src, path, original["sha256"])
                if assets_to_copy[src][0].stat().st_size > 300_000:
                    raise ValueError(f"Image exceeds packaged-content limit: {src}")
        packs.append((article, pack, selected))
    if used_corrections != set(correction_inputs):
        raise ValueError("Source correction review is outside the selected batch")
    if used_preservations != set(preservation_inputs):
        raise ValueError("Repository preservation review is outside the selected batch")
    requirements = hub_requirements(packs, articles, prior_manifests)
    # All source/review/dependency checks finish before writing a portable bundle.
    output.mkdir(parents=True)
    manifest = {
        "schema_version": 1,
        "baseline_sha256": sha(baseline_path),
        "articles": [],
        "assets": [],
    }
    for article, pack, selected in packs:
        relative = f"packs/{article['slug']}.json"
        path = output / relative
        path.parent.mkdir(exist_ok=True)
        if preservations_by_slug[article["slug"]]:
            expected = preservations_by_slug[article["slug"]][0]["repo_pack_sha256"]
            copy_pinned_asset(ROOT / article["pack_path"], path, expected)
        else:
            write_text_lf(
                path,
                json.dumps(pack.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
            )
        manifest["articles"].append(
            {
                "slug": article["slug"],
                "pack_path": relative,
                "pack_sha256": sha(path),
                "locales": selected,
                "publish_locales": selected if article["status"] == "published" else [],
                "hub": article["slug"] in HUBS,
                **(
                    {"source_corrections": corrections_by_slug[article["slug"]]}
                    if corrections_by_slug[article["slug"]]
                    else {}
                ),
                **(
                    {"repository_preservations": preservations_by_slug[article["slug"]]}
                    if preservations_by_slug[article["slug"]]
                    else {}
                ),
                **(
                    {"requires": requirements[article["slug"]]}
                    if article["slug"] in requirements
                    else {}
                ),
            }
        )
        for correction in corrections_by_slug[article["slug"]]:
            original = correction_inputs[(article["slug"], correction["locale"])][0]
            destination = inside(output, correction["review_path"])
            destination.parent.mkdir(exist_ok=True)
            copy_pinned_asset(original, destination, correction["review_sha256"])
        for preservation in preservations_by_slug[article["slug"]]:
            original = preservation_inputs[(article["slug"], preservation["locale"])][0]
            destination = inside(output, preservation["review_path"])
            destination.parent.mkdir(exist_ok=True)
            copy_pinned_asset(original, destination, preservation["review_sha256"])
    for src, (original, expected) in sorted(assets_to_copy.items()):
        relative = "public" + src
        target = inside(output, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        copy_pinned_asset(original, target, expected)
        manifest["assets"].append({"path": relative, "sha256": expected})
    write_text_lf(output / "release-manifest.json", json.dumps(manifest, indent=2) + "\n")
    write_text_lf(
        output / "link-transformations.json",
        json.dumps(transformations, ensure_ascii=False, indent=2) + "\n",
    )
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--slug", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prior-manifest", type=Path, action="append", default=[])
    parser.add_argument("--source-correction-review", type=Path, action="append", default=[])
    parser.add_argument(
        "--repository-preservation-review", type=Path, action="append", default=[]
    )
    args = parser.parse_args()
    result = assemble(
        args.baseline,
        args.work,
        args.slug,
        args.output,
        args.prior_manifest,
        args.source_correction_review,
        args.repository_preservation_review,
    )
    print(
        json.dumps(
            {
                "articles": len(result["articles"]),
                "assets": len(result["assets"]),
                "manifest_sha256": sha(args.output / "release-manifest.json"),
            }
        )
    )


if __name__ == "__main__":
    main()
