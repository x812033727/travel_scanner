"""Compile synthetic Route B inputs, then hand the real output to the guarded publisher.

Run from the repository root with the API environment:
  uv run --project apps/api pytest -q -o asyncio_mode=auto
    docs/article-localization/test_prepare_route_b_bundle.py
With RUN_INTEGRATION_TESTS=1 the shared guides fixture runs every database case on an
isolated PostgreSQL schema too, including the two-session lock cases, which skip on
SQLite. Every input is synthetic: nothing reads production or the repository's packs.
"""

from __future__ import annotations

import ast
import copy
import importlib.util
import json
import os
import sys
from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest
from app.auth import service as auth_service
from app.guides import admin_service
from app.guides.content_pack import ArticlePack, load_publish_holds
from app.guides.models import GuideArticle, GuideArticleRevision
from app.guides.publication import today
from app.guides.schemas import ArticleCreate, DraftWrite, GuideDocument, PublishWrite
from sqlalchemy import func, select, text
from sqlalchemy.exc import DBAPIError
from tests import test_guides as guides

spec = importlib.util.spec_from_file_location(
    "route_b_bundle_compiler", Path(__file__).with_name("prepare_route_b_bundle.py")
)
compiler = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = compiler
spec.loader.exec_module(compiler)
driver = compiler.publish_bundle

database = guides.database
actor = guides.actor

SLUG = "route-b-guide"
OTHER = "route-b-second"
TARGETS = ["en", "ja", "ko", "zh-CN"]
LOCALES = list(compiler.LOCALES)
FIELDS = ("id", "version", "published_version", "published_sha256", "draft_sha256")


def write_json(path, value, **options):
    path.parent.mkdir(parents=True, exist_ok=True)
    options = options or {"ensure_ascii": False, "indent": 2}
    raw = (json.dumps(value, **options) + "\n").encode()
    path.write_bytes(raw)
    return driver.sha(raw)


def metadata(slug):
    return {
        "slug": slug,
        "kind": "howto",
        "destination_id": "tokyo",
        "topics": ["transport"],
        "valid_until": None,
        "featured": False,
        "display_order": 100,
    }


def source_document(slug):
    document = guides.document(title="原文標題", description="原文說明")
    document["hero"] = {
        "src": f"/guides/{slug}/hero.jpg",
        "alt": "原文主圖",
        "width": 1600,
        "height": 900,
        "credit": None,
    }
    document["blocks"].append(
        {
            "type": "image",
            "src": f"/guides/{slug}/diagram-1.svg",
            "alt": "原文圖解",
            "caption": "原文圖說",
            "width": 1600,
            "height": 900,
            "credit": None,
        }
    )
    return driver.normalized(document)


def translated(slug, source, locale):
    document = copy.deepcopy(source)
    document["title"] = f"Reviewed title {locale}"
    document["description"] = f"Reviewed description {locale}"
    # en has a localized raster hero with its editable SVG master; the rest reuse the
    # source hero, which therefore ships with them while the source diagram does not.
    if locale == "en":
        document["hero"]["src"] = f"/guides/{slug}/hero-en.jpg"
    document["blocks"][-1]["src"] = f"/guides/{slug}/diagram-1-{locale.lower()}.svg"
    document["blocks"][-1]["alt"] = f"Reviewed diagram {locale}"
    return driver.normalized(document)


def synthetic_database(document):
    digest = driver.document_hash(document)
    return {
        "id": str(uuid4()),
        "version": 1,
        "locales": {
            "zh-TW": {
                "id": str(uuid4()),
                "version": 2,
                "published_version": 2,
                "published_sha256": digest,
                "draft_sha256": digest,
            }
        },
    }


def pinned(state):
    return {
        "id": state["id"],
        "version": state["version"],
        "locales": {
            locale: {key: row[key] for key in FIELDS} for locale, row in state["locales"].items()
        },
    }


def image_sources(document):
    sources = [document["hero"]["src"]] if document.get("hero") else []
    return sources + [block["src"] for block in document["blocks"] if block["type"] == "image"]


def baseline_article(inputs, slug, database_block, repository=()):
    """A full build_baseline row: identity, versions, documents, targets and visibility."""
    pack = inputs.packs[slug]
    documents = {
        locale: copy.deepcopy(pack["locales"][locale])
        for locale in LOCALES
        if locale in database_block["locales"] or locale in repository
    }
    published = [
        locale
        for locale in LOCALES
        if locale in database_block["locales"]
        and database_block["locales"][locale]["published_version"] is not None
    ]
    provenance = compiler.build_baseline.locale_provenance(
        list(documents), database_block["locales"]
    )
    sources = sorted({src for document in documents.values() for src in image_sources(document)})
    return {
        "slug": slug,
        "kind": "howto",
        "status": "published",
        "pack_path": f"apps/api/app/guides/content/{slug}.json",
        "pack_sha256": "a" * 64,
        "metadata": metadata(slug),
        "source_locale": "zh-TW",
        "source_document": documents["zh-TW"],
        "source_sha256": driver.document_hash(documents["zh-TW"]),
        "existing_locales": list(documents),
        **compiler.build_baseline.locale_work(documents, published, "published"),
        "locale_provenance": {locale: provenance[locale] for locale in LOCALES if locale in provenance},
        "published_locales": published,
        "locale_documents": documents,
        "database": database_block,
        "assets": [
            {"src": src, "sha256": driver.sha(inputs.files["public" + src])} for src in sources
        ],
    }


def build(tmp_path, live=None, slugs=(SLUG,)):
    """Write a frozen candidate, an independent review, a full baseline and a hold list."""
    inputs = SimpleNamespace(
        work=tmp_path / "work",
        root=tmp_path / "candidate",
        packs={},
        files={},
        holds=tmp_path / "publish_holds.json",
    )
    inputs.work.mkdir(parents=True)
    write_json(inputs.holds, {})
    targets = []
    for slug in slugs:
        source = source_document(slug)
        pack = {**metadata(slug), "locales": {"zh-TW": source}}
        for locale in TARGETS:
            pack["locales"][locale] = translated(slug, source, locale)
        inputs.packs[slug] = pack
        names = ["hero.jpg", "hero.svg", "diagram-1.svg", "hero-en.jpg", "hero-en.svg"]
        names += [f"diagram-1-{locale.lower()}.svg" for locale in TARGETS]
        for name in names:
            inputs.files[f"public/guides/{slug}/{name}"] = f"{slug} {name} reviewed\n".encode()
        for locale in TARGETS:
            document = pack["locales"][locale]
            assets = {src: driver.sha(inputs.files["public" + src]) for src in image_sources(document)}
            if locale == "en":
                master = f"/guides/{slug}/hero-en.svg"
                assets[master] = driver.sha(inputs.files["public" + master])
            targets.append(
                {
                    "slug": slug,
                    "locale": locale,
                    "status": "PASS",
                    "translator": f"translator-{locale}",
                    "reviewer": f"reviewer-{locale}",
                    "reviewed_at": "2026-09-29T05:00:00+00:00",
                    "source_sha256": driver.document_hash(source),
                    "document_sha256": driver.document_hash(document),
                    "assets": assets,
                    "checks": {name: True for name in compiler.CHECKS},
                    "open_findings": 0,
                }
            )
    for relative, data in inputs.files.items():
        (inputs.root / relative).parent.mkdir(parents=True, exist_ok=True)
        (inputs.root / relative).write_bytes(data)
    inputs.candidate_doc = {
        "schema": compiler.CANDIDATE_SCHEMA,
        "source_git_commit": "2" * 40,
        "articles": [],
        "assets": [
            {"path": path, "sha256": driver.sha(data)} for path, data in sorted(inputs.files.items())
        ],
    }
    for slug, pack in inputs.packs.items():
        # Frozen Git bytes need not match the native serialization the compiler writes.
        pack_sha = write_json(
            inputs.root / f"packs/{slug}.json", pack, ensure_ascii=False, sort_keys=True
        )
        inputs.candidate_doc["articles"].append(
            {"slug": slug, "pack_path": f"packs/{slug}.json", "pack_sha256": pack_sha}
        )
    inputs.review_doc = {
        "schema": compiler.REVIEW_SCHEMA,
        "evidence_sha256": "e" * 64,
        "targets": targets,
    }
    inputs.baseline_doc = {
        "schema_version": 1,
        "repo_commit": "1" * 40,
        "captured_at": "2026-10-05T00:00:00+00:00",
        "locales": LOCALES,
        "articles": [
            baseline_article(
                inputs,
                slug,
                (live or {}).get(slug) or synthetic_database(inputs.packs[slug]["locales"]["zh-TW"]),
            )
            for slug in slugs
        ],
        "batches": [],
    }
    inputs.candidate = inputs.root / "candidate-manifest.json"
    inputs.review = tmp_path / "review.json"
    inputs.baseline = tmp_path / "baseline.json"
    repin(inputs)
    return inputs


def repin(inputs):
    inputs.candidate_sha = write_json(inputs.candidate, inputs.candidate_doc)
    inputs.review_sha = write_json(inputs.review, inputs.review_doc)
    inputs.baseline_sha = write_json(inputs.baseline, inputs.baseline_doc)


def rewrite_pack(inputs, slug=SLUG):
    entry = next(row for row in inputs.candidate_doc["articles"] if row["slug"] == slug)
    entry["pack_sha256"] = write_json(inputs.root / entry["pack_path"], inputs.packs[slug])
    repin(inputs)


def rewrite_asset(inputs, path, data):
    (inputs.root / path).write_bytes(data)
    entry = next(row for row in inputs.candidate_doc["assets"] if row["path"] == path)
    entry["sha256"] = driver.sha(data)
    repin(inputs)


def review_target(inputs, slug, locale):
    return next(
        row
        for row in inputs.review_doc["targets"]
        if row["slug"] == slug and row["locale"] == locale
    )


def compile_inputs(inputs, *, slugs=(SLUG,), locales=TARGETS, output=None, **pins):
    return compiler.compile_bundle(
        candidate=inputs.candidate,
        candidate_sha256=pins.get("candidate_sha256", inputs.candidate_sha),
        review=inputs.review,
        review_sha256=pins.get("review_sha256", inputs.review_sha),
        baseline=inputs.baseline,
        baseline_sha256=pins.get("baseline_sha256", inputs.baseline_sha),
        slugs=list(slugs),
        locales=list(locales),
        output=output or inputs.work / "bundle",
        holds_path=inputs.holds,
    )


def tree(root):
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def leftovers(inputs):
    return sorted(path.name for path in inputs.work.iterdir() if ".partial-" in path.name)


def deploy(inputs):
    """The deployed repository: candidate pack bytes and every candidate image."""
    deployed = inputs.work / "deployed"
    for slug in inputs.packs:
        destination = deployed / f"apps/api/app/guides/content/{slug}.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((inputs.root / f"packs/{slug}.json").read_bytes())
    for relative, data in inputs.files.items():
        destination = deployed / "apps/web" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    return deployed


@pytest.fixture
def owner(monkeypatch, actor):
    settings = SimpleNamespace(admin_email_set={actor.email.lower()})
    monkeypatch.setattr(driver, "get_settings", lambda: settings)
    monkeypatch.setattr(auth_service, "get_settings", lambda: settings)
    return actor


@pytest.fixture
def publisher_holds(monkeypatch):
    """Point the publisher at the same hold list each case gives the compiler."""
    paths = {}

    def bind(inputs):
        paths["holds"] = inputs.holds

    monkeypatch.setattr(driver, "load_publish_holds", lambda: load_publish_holds(paths["holds"]))
    return bind


async def publish_source(database, owner, slug=SLUG):
    document = source_document(slug)
    async with database() as session:
        created = await admin_service.create_article(
            session,
            owner,
            ArticleCreate(
                slug=slug,
                kind="howto",
                destination_id="tokyo",
                topics=["transport"],
                locale="zh-TW",
                document=GuideDocument.model_validate(document),
            ),
        )
        await admin_service.publish_locale(
            session,
            owner,
            created.id,
            "zh-TW",
            PublishWrite(expected_version=1, confirmed=True, reason="Synthetic source"),
        )
    return await state(database, slug)


async def state(database, slug=SLUG):
    async with database() as session:
        return (await driver.snapshot(session, [slug]))[slug]


async def revision_count(database):
    async with database() as session:
        return await session.scalar(select(func.count()).select_from(GuideArticleRevision))


async def run(bundle, database, phase, deployed):
    path = bundle.root.parent / "state" / "journal.json"
    with driver.journal_lock(path.parent):
        return await driver.execute_phase(
            bundle, phase, path, deployed_root=deployed, db_engine=database.kw["bind"]
        )


async def compiled_live(tmp_path, database, owner, publisher_holds, locales=("en", "ja")):
    before = await publish_source(database, owner)
    inputs = build(tmp_path, live={SLUG: pinned(before)})
    publisher_holds(inputs)
    result = compile_inputs(inputs, locales=locales)
    bundle = driver.verify_bundle(inputs.work / "bundle", inputs.baseline, result["manifest_sha256"])
    return inputs, bundle, deploy(inputs), before


def test_compiles_exact_selection_deterministically_for_the_publisher(tmp_path):
    inputs = build(tmp_path)
    holds = inputs.holds.read_bytes()
    first = compile_inputs(inputs, output=inputs.work / "first")
    second = compile_inputs(inputs, output=inputs.work / "second")
    assert first["manifest_sha256"] == second["manifest_sha256"]
    assert tree(inputs.work / "first") == tree(inputs.work / "second")
    files = tree(inputs.work / "first")
    manifest = json.loads(files["release-manifest.json"])
    assert manifest["articles"] == [
        {
            "slug": SLUG,
            "pack_path": f"packs/{SLUG}.json",
            "pack_sha256": driver.sha(files[f"packs/{SLUG}.json"]),
            "locales": TARGETS,
            "publish_locales": TARGETS,
            "hub": False,
        }
    ]
    expected = {f"public/guides/{SLUG}/{name}" for name in ["hero.jpg", "hero-en.jpg", "hero-en.svg"]}
    expected |= {f"public/guides/{SLUG}/diagram-1-{locale.lower()}.svg" for locale in TARGETS}
    assert {row["path"] for row in manifest["assets"]} == expected
    assert set(files) == expected | {
        "release-manifest.json",
        compiler.PROVENANCE_FILE,
        f"packs/{SLUG}.json",
    }
    # Native schema: the publisher's own contract accepts it, and the pack is the
    # reviewed candidate re-serialized, not its frozen bytes.
    bundle = driver.verify_bundle(inputs.work / "first", inputs.baseline, first["manifest_sha256"])
    assert bundle.slugs == [SLUG]
    native = files[f"packs/{SLUG}.json"]
    frozen = (inputs.root / f"packs/{SLUG}.json").read_bytes()
    assert native != frozen
    assert ArticlePack.model_validate_json(native) == ArticlePack.model_validate_json(frozen)
    provenance = json.loads(files[compiler.PROVENANCE_FILE])
    assert provenance["authorizes_production"] is False
    assert provenance["manifest_sha256"] == first["manifest_sha256"]
    assert provenance["candidate"]["sha256"] == inputs.candidate_sha
    assert provenance["review"]["sha256"] == inputs.review_sha
    assert provenance["baseline"]["sha256"] == inputs.baseline_sha
    assert [(row["slug"], row["locale"]) for row in provenance["targets"]] == [
        (SLUG, locale) for locale in TARGETS
    ]
    assert leftovers(inputs) == []
    assert inputs.holds.read_bytes() == holds


def test_wave_selection_copies_only_that_waves_documents_and_images(tmp_path):
    inputs = build(tmp_path, slugs=(SLUG, OTHER))
    result = compile_inputs(inputs, slugs=[OTHER], locales=["en"])
    files = tree(inputs.work / "bundle")
    manifest = json.loads(files["release-manifest.json"])
    assert [(row["slug"], row["locales"]) for row in manifest["articles"]] == [(OTHER, ["en"])]
    assert {row["path"] for row in manifest["assets"]} == {
        f"public/guides/{OTHER}/{name}" for name in ["hero-en.jpg", "hero-en.svg", "diagram-1-en.svg"]
    }
    assert not any(SLUG + "/" in path or path.endswith(f"{SLUG}.json") for path in files)
    assert result == {
        "status": "compiled",
        "authorizes_production": False,
        "articles": 1,
        "documents": 1,
        "assets": 3,
        "manifest_sha256": driver.sha(files["release-manifest.json"]),
        "output": str((inputs.work / "bundle").resolve()),
    }


def change_review(field, value, locale="en"):
    def apply(inputs):
        review_target(inputs, SLUG, locale)[field] = value
        repin(inputs)

    return apply


def change_baseline(update):
    def apply(inputs):
        update(inputs.baseline_doc["articles"][0])
        repin(inputs)

    return apply


def change_pack(update):
    def apply(inputs):
        update(inputs.packs[SLUG])
        rewrite_pack(inputs)

    return apply


def existing_target(article):
    document = article["locale_documents"]["zh-TW"]
    en = copy.deepcopy(document)
    en["title"] = "Someone else's draft"
    article["database"]["locales"]["en"] = {
        "id": str(uuid4()),
        "version": 1,
        "published_version": None,
        "published_sha256": None,
        "draft_sha256": driver.document_hash(en),
    }
    article["locale_documents"]["en"] = en
    article["existing_locales"] = ["zh-TW", "en"]
    article.update(
        compiler.build_baseline.locale_work(article["locale_documents"], ["zh-TW"], "published")
    )
    article["locale_provenance"]["en"] = "database-draft"


def repository_target(article):
    article["locale_documents"]["en"] = article["locale_documents"]["zh-TW"]
    article["existing_locales"] = ["zh-TW", "en"]
    article.update(
        compiler.build_baseline.locale_work(article["locale_documents"], ["zh-TW"], "published")
    )
    article["locale_provenance"]["en"] = "repository-only"


def expire(article):
    article["metadata"]["valid_until"] = str(today() - timedelta(days=1))


def unsafe_asset(path):
    def apply(inputs):
        inputs.candidate_doc["assets"][0]["path"] = path
        repin(inputs)

    return apply


def repeated_key(inputs):
    raw = inputs.review.read_bytes().replace(
        b'"schema": "route-b-review-v1",',
        b'"schema": "route-b-review-v1",\n  "schema": "route-b-review-v1",',
    )
    inputs.review.write_bytes(raw)
    inputs.review_sha = driver.sha(raw)


def hold(inputs):
    write_json(inputs.holds, {SLUG: "Source summary review pending"})


def extra_review_image(inputs):
    source = f"/guides/{SLUG}/diagram-1.svg"
    review_target(inputs, SLUG, "en")["assets"][source] = driver.sha(inputs.files["public" + source])
    repin(inputs)


TAMPERS = {
    "candidate-pin": ({"candidate_sha256": "0" * 64}, None, "Candidate manifest SHA256 mismatch"),
    "review-pin": ({"review_sha256": "0" * 64}, None, "Review SHA256 mismatch"),
    "baseline-pin": ({"baseline_sha256": "0" * 64}, None, "Baseline SHA256 mismatch"),
    "absent-pin": ({"review_sha256": "REVIEWED"}, None, "Supply the external Review SHA256"),
    "pack-bytes": (
        {},
        lambda inputs: (inputs.root / f"packs/{SLUG}.json").write_bytes(b"{}"),
        "candidate pack SHA256 mismatch",
    ),
    "asset-bytes": (
        {},
        lambda inputs: (inputs.root / f"public/guides/{SLUG}/hero.svg").write_bytes(b"x"),
        "candidate asset SHA256 mismatch",
    ),
    "changed-document": (
        {},
        change_pack(lambda pack: pack["locales"]["ja"].update(title="Unreviewed title")),
        "ja: reviewed document changed",
    ),
    "changed-image": (
        {},
        lambda inputs: rewrite_asset(
            inputs, f"public/guides/{SLUG}/diagram-1-ko.svg", b"unreviewed\n"
        ),
        "ko: reviewed image changed",
    ),
    "changed-master": (
        {},
        lambda inputs: rewrite_asset(inputs, f"public/guides/{SLUG}/hero-en.svg", b"other\n"),
        "SVG master changed",
    ),
    "stale-review": ({}, change_review("source_sha256", "f" * 64), "review is stale"),
    "unapproved": ({}, change_review("status", "CHANGES_REQUESTED"), "independent PASS"),
    "self-review": ({}, change_review("reviewer", "Translator-EN "), "independent of the"),
    "open-findings": ({}, change_review("open_findings", 1), "unresolved findings"),
    "unchecked-glyphs": (
        {},
        change_review("checks", {"text": True, "visual": True, "glyph": False, "links": True}),
        "must all pass",
    ),
    "unrelated-image": ({}, extra_review_image, "does not use"),
    "unreviewed-locale": (
        {},
        lambda inputs: (
            inputs.review_doc["targets"].remove(review_target(inputs, SLUG, "ko")),
            repin(inputs),
        ),
        "ko: selection exceeds the independent review",
    ),
    "repeated-key": ({}, repeated_key, "repeats a JSON key"),
    "unsafe-pack-path": (
        {},
        lambda inputs: (
            inputs.candidate_doc["articles"][0].update(pack_path=f"../packs/{SLUG}.json"),
            repin(inputs),
        ),
        "unsafe candidate pack path",
    ),
    "parent-asset-path": ({}, unsafe_asset("public/guides/../../outside.svg"), "Unsafe candidate"),
    "absolute-asset-path": ({}, unsafe_asset("/etc/guides/x.svg"), "Unsafe candidate"),
    "backslash-asset-path": ({}, unsafe_asset("public\\guides\\x\\y.svg"), "Unsafe candidate"),
    "duplicate-slug": ({"slugs": [SLUG, SLUG]}, None, "distinct slugs"),
    "duplicate-locale": ({"locales": ["en", "ja", "en"]}, None, "distinct supported locales"),
    "unknown-locale": ({"locales": ["fr"]}, None, "distinct supported locales"),
    "source-locale": ({"locales": ["zh-TW", "en"]}, None, "source locale cannot be selected"),
    "widened-slug": ({"slugs": [SLUG, OTHER]}, None, "outside the candidate"),
    "present-target": ({}, change_baseline(existing_target), "already exists in the baseline"),
    "repository-differs": (
        {},
        change_baseline(repository_target),
        "repository document differs from the reviewed candidate",
    ),
    "public-projection": (
        {},
        change_baseline(lambda article: article.update(database=None)),
        "public projection",
    ),
    "incomplete-baseline": (
        {},
        change_baseline(lambda article: article.pop("locale_provenance")),
        "incomplete baseline article",
    ),
    "unversioned-baseline": (
        {},
        change_baseline(lambda article: article["database"]["locales"]["zh-TW"].pop("version")),
        "incomplete baseline locale version",
    ),
    "inconsistent-targets": (
        {},
        change_baseline(lambda article: article.update(publication_locales=[])),
        "inconsistent",
    ),
    "hidden-source": (
        {},
        change_baseline(lambda article: article.update(status="hidden")),
        "not public",
    ),
    "expired-source": ({}, change_baseline(expire), "expired"),
    "unclean-source": (
        {},
        change_baseline(
            lambda article: article["database"]["locales"]["zh-TW"].update(version=3)
        ),
        "not cleanly published",
    ),
    "source-text": (
        {},
        change_pack(lambda pack: pack["locales"]["zh-TW"].update(title="Silent source fix")),
        "unselected or source text differs",
    ),
    "classification": (
        {},
        change_pack(lambda pack: pack.update(featured=True)),
        "classification/order differs",
    ),
    "aliases": (
        {},
        change_pack(lambda pack: pack.update(aliases={"en": ["route b"]})),
        "not aliases",
    ),
    "held": ({}, hold, "publication held: Source summary review pending"),
}


@pytest.mark.parametrize("case", sorted(TAMPERS))
def test_tampered_stale_widened_or_unsafe_inputs_refuse_without_output(tmp_path, case):
    inputs = build(tmp_path)
    options, tamper, message = TAMPERS[case]
    if tamper:
        tamper(inputs)
    pins = {key: value for key, value in options.items() if key.endswith("sha256")}
    selection = {key: value for key, value in options.items() if key in {"slugs", "locales"}}
    holds = inputs.holds.read_bytes()
    with pytest.raises(driver.Refused, match=message):
        compile_inputs(inputs, **selection, **pins)
    assert not (inputs.work / "bundle").exists()
    assert leftovers(inputs) == []
    assert inputs.holds.read_bytes() == holds


@pytest.mark.parametrize("place", ["existing", "candidate", "repository"])
def test_output_must_be_a_new_directory_outside_sources(tmp_path, place):
    inputs = build(tmp_path)
    if place == "existing":
        output = inputs.work / "bundle"
        output.mkdir()
        message = "already exists"
    elif place == "candidate":
        output = inputs.root / "bundle"
        message = "outside the candidate"
    else:
        output = compiler.ROOT / f"route-b-bundle-{uuid4().hex}"
        message = "outside the repository"
    with pytest.raises(driver.Refused, match=message):
        compile_inputs(inputs, output=output)
    if place != "existing":
        assert not output.exists()


@pytest.mark.parametrize("points", ["outside", "inside"])
def test_linked_candidate_file_is_refused(tmp_path, points):
    # A link is refused as a link before anything resolves it, wherever it points.
    inputs = build(tmp_path)
    target = inputs.root / f"public/guides/{SLUG}/hero.svg"
    real = tmp_path / "outside.svg" if points == "outside" else inputs.root / "unlisted.svg"
    real.write_bytes(target.read_bytes())
    target.unlink()
    try:
        os.symlink(real, target)
    except OSError:
        pytest.skip("this platform cannot create a symbolic link without privileges")
    with pytest.raises(driver.Refused, match="linked candidate path"):
        compile_inputs(inputs)
    assert not (inputs.work / "bundle").exists()


def test_hub_articles_are_refused(tmp_path):
    inputs = build(tmp_path, slugs=("gemini-guide",))
    with pytest.raises(driver.Refused, match="hub needs Route A dependency pins"):
        compile_inputs(inputs, slugs=["gemini-guide"])


def test_hub_list_matches_the_route_a_assembler():
    source = Path(__file__).with_name("assemble_bundle.py").read_text(encoding="utf-8")
    declared = next(line for line in source.splitlines() if line.startswith("HUBS = "))
    assert ast.literal_eval(declared.split("=", 1)[1].strip()) == set(compiler.HUBS)


def test_failure_after_writing_leaves_no_manifest_or_partial_directory(tmp_path, monkeypatch):
    inputs = build(tmp_path)

    def refuse(*args, **kwargs):
        raise driver.Refused("Simulated publisher contract failure")

    monkeypatch.setattr(compiler.publish_bundle, "verify_bundle", refuse)
    with pytest.raises(driver.Refused, match="Simulated publisher contract failure"):
        compile_inputs(inputs)
    assert not (inputs.work / "bundle").exists()
    assert leftovers(inputs) == []


def test_cli_prints_hashes_only_and_refuses_without_document_text(tmp_path, capsys, monkeypatch):
    inputs = build(tmp_path)
    monkeypatch.setattr(compiler, "publish_holds_path", lambda: inputs.holds)
    arguments = [
        "--candidate",
        str(inputs.candidate),
        "--candidate-sha256",
        inputs.candidate_sha,
        "--review",
        str(inputs.review),
        "--review-sha256",
        inputs.review_sha,
        "--baseline",
        str(inputs.baseline),
        "--baseline-sha256",
        inputs.baseline_sha,
        "--slug",
        SLUG,
        "--locale",
        "en",
    ]
    assert compiler.main([*arguments, "--output", str(inputs.work / "cli")]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["status"] == "compiled" and printed["documents"] == 1
    change_review("source_sha256", "f" * 64)(inputs)
    arguments[arguments.index("--review-sha256") + 1] = inputs.review_sha
    assert compiler.main([*arguments, "--output", str(inputs.work / "stale")]) == 1
    refusal = capsys.readouterr().err
    assert json.loads(refusal)["status"] == "refused"
    assert "review is stale" in refusal
    assert "Reviewed title" not in refusal
    assert not (inputs.work / "stale").exists()


async def test_publisher_writes_only_selected_locales_and_replays_unchanged(
    tmp_path, database, owner, publisher_holds
):
    inputs, bundle, deployed, before = await compiled_live(
        tmp_path, database, owner, publisher_holds
    )
    candidate = tree(inputs.root)
    revisions = await revision_count(database)
    assert (await run(bundle, database, "dry-run", deployed))["status"] == "read_only"
    assert await state(database) == before
    for phase in driver.PHASES[1:]:
        await run(bundle, database, phase, deployed)
    after = await state(database)
    assert after["locales"]["zh-TW"] == before["locales"]["zh-TW"]
    assert {k: v for k, v in after.items() if k != "locales"} == {
        k: v for k, v in before.items() if k != "locales"
    }
    assert set(after["locales"]) == {"zh-TW", "en", "ja"}
    for locale in ("en", "ja"):
        row = after["locales"][locale]
        assert row["published_version"] == row["version"] == 2
        assert row["published_sha256"] == driver.document_hash(inputs.packs[SLUG]["locales"][locale])
    assert await revision_count(database) == revisions + 4
    for phase in driver.PHASES:
        await run(bundle, database, phase, deployed)
    assert await state(database) == after
    assert await revision_count(database) == revisions + 4
    assert tree(inputs.root) == candidate
    # Missing-locales only: a fresh baseline of the new live state refuses the same targets.
    refreshed = build(tmp_path / "refresh", live={SLUG: pinned(after)})
    with pytest.raises(driver.Refused, match="already exists in the baseline"):
        compile_inputs(refreshed, locales=["en"])


@pytest.mark.parametrize("timing", ["before-dry-run", "after-dry-run"])
async def test_source_drift_after_compilation_stops_the_publisher(
    tmp_path, database, owner, publisher_holds, timing
):
    inputs, bundle, deployed, before = await compiled_live(
        tmp_path, database, owner, publisher_holds
    )
    if timing == "after-dry-run":
        await run(bundle, database, "dry-run", deployed)
    changed = copy.deepcopy(inputs.packs[SLUG]["locales"]["zh-TW"])
    changed["title"] = "An editor's newer source"
    async with database() as session:
        await admin_service.save_draft(
            session,
            owner,
            UUID(before["id"]),
            "zh-TW",
            DraftWrite(
                expected_version=before["locales"]["zh-TW"]["version"],
                document=GuideDocument.model_validate(changed),
            ),
        )
    with pytest.raises(driver.Refused):
        await run(bundle, database, "drafts" if timing == "after-dry-run" else "dry-run", deployed)
    assert set((await state(database))["locales"]) == {"zh-TW"}


@pytest.mark.parametrize("failure", ["lost-response", "before-commit"])
async def test_interrupted_write_resumes_with_the_same_intent_exactly_once(
    tmp_path, database, owner, publisher_holds, monkeypatch, failure
):
    _, bundle, deployed, _ = await compiled_live(tmp_path, database, owner, publisher_holds)
    revisions = await revision_count(database)
    await run(bundle, database, "dry-run", deployed)
    original = admin_service.start_translation
    calls = 0

    async def interrupted(*args, **kwargs):
        nonlocal calls
        calls += 1
        if failure == "lost-response":
            await original(*args, **kwargs)
        raise ConnectionError("Interrupted")

    monkeypatch.setattr(admin_service, "start_translation", interrupted)
    with pytest.raises(ConnectionError):
        await run(bundle, database, "drafts", deployed)
    journal = json.loads((bundle.root.parent / "state/journal.json").read_text("utf-8"))
    assert journal["pending"]["action"] == "start_translation"
    monkeypatch.setattr(admin_service, "start_translation", original)
    await run(bundle, database, "drafts", deployed)
    journal = json.loads((bundle.root.parent / "state/journal.json").read_text("utf-8"))
    assert journal["pending"] is None
    status = "committed_reconciled" if failure == "lost-response" else "not_written_reconciled"
    assert any(row.get("status") == status for row in journal["history"])
    assert calls == 1
    assert await revision_count(database) == revisions + 2
    drafts = await state(database)
    assert all(drafts["locales"][locale]["published_version"] is None for locale in ("en", "ja"))


async def test_compiler_success_does_not_lift_a_later_hold(
    tmp_path, database, owner, publisher_holds
):
    inputs, bundle, deployed, _ = await compiled_live(tmp_path, database, owner, publisher_holds)
    await run(bundle, database, "dry-run", deployed)
    await run(bundle, database, "drafts", deployed)
    drafts = await state(database)
    hold(inputs)
    with pytest.raises(driver.Refused, match="Source summary review pending"):
        await run(bundle, database, "publish-articles", deployed)
    assert await state(database) == drafts
    assert all(drafts["locales"][locale]["published_version"] is None for locale in ("en", "ja"))
    assert json.loads(inputs.holds.read_text("utf-8")) == {SLUG: "Source summary review pending"}


@pytest.mark.parametrize("lock", ["advisory", "row"])
async def test_postgresql_second_session_lock_stops_the_publisher_without_writes(
    tmp_path, database, owner, publisher_holds, lock
):
    engine = database.kw["bind"]
    if engine.dialect.name != "postgresql":
        pytest.skip("two-session advisory and row locks need PostgreSQL")
    _, bundle, deployed, before = await compiled_live(
        tmp_path, database, owner, publisher_holds
    )
    await run(bundle, database, "dry-run", deployed)
    revisions = await revision_count(database)
    if lock == "advisory":
        async with engine.connect() as other:
            key = {"key": driver.LOCK_KEY}
            assert await other.scalar(text("SELECT pg_try_advisory_lock(:key)"), key)
            await other.commit()
            try:
                with pytest.raises(driver.Refused, match="Another editorial publisher"):
                    await run(bundle, database, "drafts", deployed)
            finally:
                await other.execute(text("SELECT pg_advisory_unlock(:key)"), key)
                await other.commit()
    else:
        async with database() as other:
            await other.execute(
                select(GuideArticle.id).where(GuideArticle.slug == SLUG).with_for_update()
            )
            with pytest.raises(DBAPIError):
                await run(bundle, database, "drafts", deployed)
            assert await state(database) == before
            await other.rollback()
        journal = json.loads((bundle.root.parent / "state/journal.json").read_text("utf-8"))
        assert journal["pending"] is None
        assert journal["history"][-1]["status"] == "stopped"
    assert await state(database) == before
    assert await revision_count(database) == revisions
    await run(bundle, database, "drafts", deployed)
    assert set((await state(database))["locales"]) == {"zh-TW", "en", "ja"}
