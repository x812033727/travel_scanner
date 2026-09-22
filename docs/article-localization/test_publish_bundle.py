"""Exercise real admin-service commits, private drafts and crash reconciliation.

Run from apps/api: .venv/Scripts/python.exe -m pytest
  ../../docs/article-localization/test_publish_bundle.py -q -o asyncio_mode=auto
The shared guides fixture also runs isolated PostgreSQL when RUN_INTEGRATION_TESTS=1.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select, update

from app.auth import service as auth_service
from app.guides import admin_service
from app.guides.models import GuideArticle, GuideArticleLocale, GuideArticleRevision
from app.guides.publication import today
from app.guides.schemas import (
    ArticleCreate,
    DraftWrite,
    GuideDocument,
    PublishWrite,
    VisibilityWrite,
)
from app.models import User
from tests import test_guides as guides

spec = importlib.util.spec_from_file_location(
    "localization_publish_bundle", Path(__file__).with_name("publish_bundle.py")
)
driver = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = driver
spec.loader.exec_module(driver)

database = guides.database
actor = guides.actor


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
    path.write_bytes(raw)
    return driver.sha(raw)


@pytest.fixture
def owner(monkeypatch, actor):
    settings = SimpleNamespace(admin_email_set={actor.email.lower()})
    monkeypatch.setattr(driver, "get_settings", lambda: settings)
    monkeypatch.setattr(auth_service, "get_settings", lambda: settings)
    return actor


async def case(tmp_path, database, owner, *, new=False, images=False, order=100, slug="test-guide"):
    document = driver.normalized(
        guides.document(title="Original title", description="Original description")
    )
    if images:
        document["hero"] = {
            "src": f"/guides/{slug}/hero.jpg",
            "alt": "Original alternative text",
            "width": 1600,
            "height": 900,
            "credit": None,
        }
        document["blocks"].append(
            {
                "type": "image",
                "src": f"/guides/{slug}/diagram.svg",
                "alt": "Original diagram",
                "caption": "Original caption",
                "width": 1600,
                "height": 900,
                "credit": None,
            }
        )
        document = driver.normalized(document)
    if not new:
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
                PublishWrite(
                    expected_version=1,
                    confirmed=True,
                    reason="Initial fixture publication",
                ),
            )
    async with database() as session:
        states = await driver.snapshot(session, [slug])
    state = states[slug]
    metadata = {
        "slug": slug,
        "kind": "howto",
        "destination_id": "tokyo",
        "topics": ["transport"],
        "valid_until": None,
        "featured": False,
        "display_order": order,
    }
    pinned = (
        None
        if new
        else {
            "id": state["id"],
            "version": state["version"],
            "locales": {
                locale: {
                    key: row[key]
                    for key in (
                        "id",
                        "version",
                        "published_version",
                        "draft_sha256",
                        "published_sha256",
                    )
                }
                for locale, row in state["locales"].items()
            },
        }
    )
    baseline = {
        "schema_version": 1,
        "articles": [
            {
                "slug": slug,
                "metadata": metadata,
                "status": "draft" if new else "published",
                "database": pinned,
                "source_locale": "zh-TW",
                "source_document": document,
                "source_sha256": driver.document_hash(document),
                "pack_path": f"apps/api/app/guides/content/{slug}.json",
                "locale_documents": {"zh-TW": document},
                "existing_locales": ["zh-TW"],
                "missing_locales": [x for x in driver.LOCALES if x != "zh-TW"],
                "published_locales": [] if new else ["zh-TW"],
                "publication_locales": [] if new else [x for x in driver.LOCALES if x != "zh-TW"],
            }
        ],
    }
    pack = {**metadata, "locales": {}}
    for locale in driver.LOCALES:
        translated = copy.deepcopy(document)
        if locale != "zh-TW":
            translated["title"] = f"Translated title {locale}"
            translated["description"] = f"Translated description {locale}"
        pack["locales"][locale] = translated
    selected = list(driver.LOCALES) if new else ["en"]
    root = tmp_path / slug
    baseline_path = root / "baseline.json"
    baseline_sha = write_json(baseline_path, baseline)
    pack_path = f"packs/{slug}.json"
    pack_sha = write_json(root / pack_path, pack)
    assets = []
    if images:
        for name in ["hero.jpg", "diagram.svg"]:
            asset = f"public/guides/{slug}/{name}"
            (root / asset).parent.mkdir(parents=True, exist_ok=True)
            (root / asset).write_bytes(b"Reviewed image fixture")
            assets.append({"path": asset, "sha256": driver.sha((root / asset).read_bytes())})
    manifest = {
        "schema_version": 1,
        "baseline_sha256": baseline_sha,
        "articles": [
            {
                "slug": slug,
                "pack_path": pack_path,
                "pack_sha256": pack_sha,
                "locales": selected,
                "publish_locales": [] if new else ["en"],
                "hub": False,
            }
        ],
        "assets": assets,
    }
    pinned_sha = write_json(root / "release-manifest.json", manifest)
    bundle = driver.verify_bundle(root, baseline_path, pinned_sha)
    deploy_bundle(bundle)
    return bundle, root / "state" / "journal.json", states


def deploy_bundle(bundle):
    deployed = bundle.root / "deployed"
    for entry in bundle.entries:
        destination = deployed / f"apps/api/app/guides/content/{entry['slug']}.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((bundle.root / entry["pack_path"]).read_bytes())
    for asset in bundle.manifest["assets"]:
        destination = deployed / "apps/web" / asset["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((bundle.root / asset["path"]).read_bytes())
    return deployed


def replace_bundle(bundle, *, manifest=None, baseline=None, pack=None):
    manifest = copy.deepcopy(manifest or bundle.manifest)
    if baseline is not None:
        manifest["baseline_sha256"] = write_json(bundle.baseline_path, baseline)
    if pack is not None:
        entry = manifest["articles"][0]
        entry["pack_sha256"] = write_json(bundle.root / entry["pack_path"], pack)
    pinned = write_json(bundle.root / "release-manifest.json", manifest)
    replaced = driver.verify_bundle(bundle.root, bundle.baseline_path, pinned)
    deploy_bundle(replaced)
    return replaced


def reviewed_source_correction(bundle, *, approved=True, draft_hash=None):
    """Build one exact, portable old-to-new zh-TW correction fixture."""
    baseline = copy.deepcopy(bundle.baseline_path.read_text("utf-8"))
    baseline = json.loads(baseline)
    article = baseline["articles"][0]
    original = article["locale_documents"]["zh-TW"]
    corrected = copy.deepcopy(original)
    corrected["title"] = "Corrected, independently reviewed source title"
    article["source_document"] = corrected
    article["source_sha256"] = driver.document_hash(corrected)
    article["locale_documents"]["zh-TW"] = corrected
    if draft_hash is not None:
        article["database"]["locales"]["zh-TW"]["draft_sha256"] = draft_hash
    pack = json.loads((bundle.root / bundle.entries[0]["pack_path"]).read_text("utf-8"))
    pack["locales"]["zh-TW"] = corrected
    pinned = article["database"]
    old = pinned["locales"]["zh-TW"]
    review = {
        "schema_version": 1,
        "approved": approved,
        "reviewer": "independent-editor",
        "reason": "Verified exact original title correction",
        "evidence_sha256": "e" * 64,
        "slug": article["slug"],
        "article_id": pinned["id"],
        "article_version": pinned["version"],
        "locale": "zh-TW",
        "locale_version": old["version"],
        "published_version": old["published_version"],
        "published_sha256": old["published_sha256"],
        "draft_sha256": old["draft_sha256"],
        "corrected_sha256": driver.document_hash(corrected),
        "old_document": original,
        "changes": [
            {"pointer": "/title", "before": original["title"], "after": corrected["title"]}
        ],
        "assets": [],
    }
    manifest = copy.deepcopy(bundle.manifest)
    entry = manifest["articles"][0]
    entry["locales"] = ["zh-TW", "en"]
    entry["publish_locales"] = ["zh-TW", "en"]
    review_path = f"reviews/{article['slug']}-zh-TW.json"
    review_sha = write_json(bundle.root / review_path, review)
    entry["source_corrections"] = [
        {
            "locale": "zh-TW",
            "from_published_sha256": old["published_sha256"],
            "to_document_sha256": review["corrected_sha256"],
            "review_path": review_path,
            "review_sha256": review_sha,
        }
    ]
    manifest["baseline_sha256"] = write_json(bundle.baseline_path, baseline)
    entry["pack_sha256"] = write_json(bundle.root / entry["pack_path"], pack)
    manifest_sha = write_json(bundle.root / "release-manifest.json", manifest)
    return baseline, pack, review, manifest, manifest_sha


async def run(bundle, path, database, phase, actor_id=None):
    with driver.journal_lock(path.parent):
        return await driver.execute_phase(
            bundle,
            phase,
            path,
            deployed_root=bundle.root / "deployed",
            actor_id=actor_id,
            db_engine=database.kw["bind"],
        )


async def state(database, slug="test-guide"):
    async with database() as session:
        return (await driver.snapshot(session, [slug]))[slug]


async def revision_count(database):
    async with database() as session:
        return await session.scalar(select(func.count()).select_from(GuideArticleRevision))


async def test_repository_only_five_drafts_never_become_public_and_order_survives(
    tmp_path, database, owner
):
    bundle, path, _ = await case(tmp_path, database, owner, new=True, order=142)
    assert (await run(bundle, path, database, "dry-run"))["status"] == "read_only"
    assert await state(database) is None
    await run(bundle, path, database, "drafts")
    after = await state(database)
    assert after["display_order"] == 142
    assert after["version"] == 2
    assert set(after["locales"]) == set(driver.LOCALES)
    assert all(row["published_version"] is None for row in after["locales"].values())
    for phase in ("publish-articles", "publish-hubs", "drafts"):
        await run(bundle, path, database, phase)
    assert await state(database) == after
    assert await revision_count(database) == 5


async def test_only_authorized_missing_language_publishes_existing_text_is_untouched(
    tmp_path, database, owner
):
    bundle, path, before = await case(tmp_path, database, owner)
    await run(bundle, path, database, "dry-run")
    await run(bundle, path, database, "drafts")
    drafts = await state(database)
    assert drafts["locales"]["en"]["published_version"] is None
    assert drafts["locales"]["zh-TW"] == before["test-guide"]["locales"]["zh-TW"]
    await run(bundle, path, database, "publish-articles")
    after = await state(database)
    assert set(after["locales"]) == {"zh-TW", "en"}
    assert after["locales"]["en"]["version"] == after["locales"]["en"]["published_version"] == 2
    assert after["locales"]["zh-TW"] == before["test-guide"]["locales"]["zh-TW"]
    assert {k: v for k, v in after.items() if k != "locales"} == {
        k: v for k, v in before["test-guide"].items() if k != "locales"
    }
    await run(bundle, path, database, "publish-articles")
    assert await state(database) == after
    assert await revision_count(database) == 4


async def test_reviewed_source_correction_publishes_once_with_missing_translation(
    tmp_path, database, owner
):
    original, path, before = await case(tmp_path, database, owner)
    _, _, review, _, manifest_sha = reviewed_source_correction(original)
    bundle = driver.verify_bundle(original.root, original.baseline_path, manifest_sha)
    deploy_bundle(bundle)
    assert (await run(bundle, path, database, "dry-run"))["status"] == "read_only"
    await run(bundle, path, database, "drafts")
    mid = await state(database)
    assert (
        mid["locales"]["zh-TW"]["published_sha256"]
        == before["test-guide"]["locales"]["zh-TW"]["published_sha256"]
    )
    assert mid["locales"]["zh-TW"]["draft_sha256"] == review["corrected_sha256"]
    await run(bundle, path, database, "publish-articles")
    after = await state(database)
    assert after["locales"]["zh-TW"]["published_sha256"] == review["corrected_sha256"]
    assert after["locales"]["en"]["published_version"] is not None
    revisions = await revision_count(database)
    await run(bundle, path, database, "drafts")
    await run(bundle, path, database, "publish-articles")
    assert await state(database) == after
    assert await revision_count(database) == revisions


@pytest.mark.parametrize("tamper", ["absent", "unapproved", "unlisted_text", "draft"])
async def test_source_correction_requires_exact_clean_review(tmp_path, database, owner, tamper):
    original, _, before = await case(tmp_path, database, owner)
    _, pack, _, manifest, _ = reviewed_source_correction(
        original,
        approved=tamper != "unapproved",
        draft_hash="f" * 64 if tamper == "draft" else None,
    )
    entry = manifest["articles"][0]
    if tamper == "absent":
        del entry["source_corrections"]
    elif tamper == "unlisted_text":
        pack["locales"]["zh-TW"]["description"] = "Unreviewed description"
        entry["pack_sha256"] = write_json(original.root / entry["pack_path"], pack)
    manifest_sha = write_json(original.root / "release-manifest.json", manifest)
    with pytest.raises((driver.Refused, ValueError)):
        driver.verify_bundle(original.root, original.baseline_path, manifest_sha)
    assert await state(database) == before["test-guide"]


async def test_reviewed_source_correction_stops_on_intervening_editor_draft(
    tmp_path, database, owner
):
    original, path, before = await case(tmp_path, database, owner)
    _, _, _, _, manifest_sha = reviewed_source_correction(original)
    bundle = driver.verify_bundle(original.root, original.baseline_path, manifest_sha)
    deploy_bundle(bundle)
    await run(bundle, path, database, "dry-run")
    article_id = UUID(before["test-guide"]["id"])
    async with database() as session:
        changed = bundle.packs["test-guide"].locales["zh-TW"].model_copy(deep=True)
        changed.title = "Another editor's draft"
        await admin_service.save_draft(
            session,
            owner,
            article_id,
            "zh-TW",
            DraftWrite(expected_version=2, document=changed),
        )
    with pytest.raises(driver.Refused, match="Concurrent/unexpected change"):
        await run(bundle, path, database, "drafts")
    after = await state(database)
    assert (
        after["locales"]["zh-TW"]["draft_sha256"]
        != before["test-guide"]["locales"]["zh-TW"]["draft_sha256"]
    )
    assert "en" not in after["locales"]


async def test_exact_reviewed_existing_unpublished_draft_is_published_without_overwrite(
    tmp_path, database, owner
):
    bundle, path, before = await case(tmp_path, database, owner)
    article_id = UUID(before["test-guide"]["id"])
    reviewed = bundle.packs["test-guide"].locales["en"]
    async with database() as session:
        await admin_service.start_translation(session, owner, article_id, "en", reviewed)
    actual = await state(database)
    baseline = json.loads(bundle.baseline_path.read_text("utf-8"))
    article = baseline["articles"][0]
    article["database"]["locales"]["en"] = {
        key: actual["locales"]["en"][key]
        for key in (
            "id",
            "version",
            "published_version",
            "draft_sha256",
            "published_sha256",
        )
    }
    article["locale_documents"]["en"] = reviewed.model_dump(mode="json")
    article["existing_locales"].append("en")
    article["missing_locales"].remove("en")
    bundle = replace_bundle(bundle, baseline=baseline)

    before_drafts = await revision_count(database)
    await run(bundle, path, database, "dry-run")
    await run(bundle, path, database, "drafts")
    assert await revision_count(database) == before_drafts
    await run(bundle, path, database, "publish-articles")
    published = (await state(database))["locales"]["en"]
    assert published["published_sha256"] == published["draft_sha256"]
    assert published["published_version"] == 2
    assert await revision_count(database) == before_drafts + 1


@pytest.mark.parametrize("target", ["pack", "asset"])
@pytest.mark.parametrize("timing", ["dry-run", "before-write"])
async def test_deployed_hash_mismatch_stops_before_database_write(
    tmp_path, database, owner, target, timing
):
    bundle, path, before = await case(tmp_path, database, owner, images=True)
    if timing == "before-write":
        await run(bundle, path, database, "dry-run")
    deployed = bundle.root / "deployed"
    if target == "pack":
        changed = deployed / "apps/api/app/guides/content/test-guide.json"
    else:
        changed = deployed / "apps/web" / bundle.manifest["assets"][0]["path"]
    changed.write_bytes(b"unreviewed deployed bytes")
    with pytest.raises(driver.Refused, match="deployed .*mismatch"):
        await run(bundle, path, database, "drafts" if timing == "before-write" else "dry-run")
    assert await state(database) == before["test-guide"]


async def test_deployed_pack_with_equivalent_serialization_passes(tmp_path, database, owner):
    bundle, path, _ = await case(tmp_path, database, owner)
    deployed = bundle.root / "deployed/apps/api/app/guides/content/test-guide.json"
    # The repository pack includes explicit defaults and a different field order,
    # while the manifest still pins the original reviewed bundle bytes.
    deployed.write_bytes(
        json.dumps(
            bundle.packs["test-guide"].model_dump(mode="json"),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    assert driver.sha(deployed.read_bytes()) != bundle.entries[0]["pack_sha256"]
    assert (await run(bundle, path, database, "dry-run"))["status"] == "read_only"
    await run(bundle, path, database, "drafts")
    assert "en" in (await state(database))["locales"]


@pytest.mark.parametrize("change", ["metadata", "document"])
async def test_deployed_pack_semantic_change_stops_before_database_write(
    tmp_path, database, owner, change
):
    bundle, path, before = await case(tmp_path, database, owner)
    deployed = bundle.root / "deployed/apps/api/app/guides/content/test-guide.json"
    pack = json.loads(deployed.read_text("utf-8"))
    if change == "metadata":
        pack["featured"] = True
    else:
        pack["locales"]["en"]["title"] = "Unreviewed title"
    write_json(deployed, pack)
    with pytest.raises(driver.Refused, match="deployed content pack mismatch"):
        await run(bundle, path, database, "dry-run")
    assert await state(database) == before["test-guide"]


@pytest.mark.parametrize("forgery", ["phase", "action", "done", "pending", "dry-run"])
async def test_forged_journal_cannot_authorize_work(tmp_path, database, owner, forgery):
    bundle, path, before = await case(tmp_path, database, owner)
    await run(bundle, path, database, "dry-run")
    journal = json.loads(path.read_text("utf-8"))
    operation = journal["operations"]["drafts"][0]
    if forgery == "phase":
        operation["phase"] = "publish-articles"
    elif forgery == "action":
        operation["action"] = "publish"
    elif forgery == "done":
        journal["done"]["drafts"] = [operation["id"]]
    elif forgery == "pending":
        journal["pending"] = {
            **operation,
            "action": "publish",
            "actor_id": journal["actor_id"],
            "at": driver.stamp(),
        }
    else:
        journal["dry_run"] = "yes"
    journal["authorization_sha256"] = driver.journal_authorization(
        bundle, journal["initial"], journal["operations"]
    )
    driver.seal_journal(journal)
    driver.persist(path, journal)
    with pytest.raises(driver.Refused):
        await run(bundle, path, database, "drafts")
    assert await state(database) == before["test-guide"]


async def test_forged_journal_cannot_publish_repository_only_article(tmp_path, database, owner):
    bundle, path, _ = await case(tmp_path, database, owner, new=True)
    await run(bundle, path, database, "dry-run")
    journal = json.loads(path.read_text("utf-8"))
    fake = {
        "slug": "test-guide",
        "locale": "en",
        "action": "publish",
        "id": "publish-articles:0:test-guide:en",
        "phase": "publish-articles",
    }
    journal["operations"]["publish-articles"].append(fake)
    # Even a recomputed self-seal cannot expand manifest/baseline authorization.
    journal["authorization_sha256"] = driver.journal_authorization(
        bundle, journal["initial"], journal["operations"]
    )
    driver.seal_journal(journal)
    driver.persist(path, journal)
    with pytest.raises(driver.Refused, match="operation plan was forged"):
        await run(bundle, path, database, "drafts")
    assert await state(database) is None


async def test_deployed_pack_is_rechecked_before_each_database_write(
    tmp_path, database, owner, monkeypatch
):
    bundle, path, _ = await case(tmp_path, database, owner, new=True)
    await run(bundle, path, database, "dry-run")
    original = driver.write_operation
    calls = 0

    async def change_install_after_first_write(*args, **kwargs):
        nonlocal calls
        await original(*args, **kwargs)
        calls += 1
        if calls == 1:
            deployed = bundle.root / "deployed/apps/api/app/guides/content/test-guide.json"
            deployed.write_bytes(b"changed between writes")

    monkeypatch.setattr(driver, "write_operation", change_install_after_first_write)
    with pytest.raises(driver.Refused, match="deployed content pack mismatch"):
        await run(bundle, path, database, "drafts")
    assert calls == 1
    after = await state(database)
    assert after is not None
    assert len(after["locales"]) == 1
    assert all(item["published_version"] is None for item in after["locales"].values())


def test_cli_requires_explicit_deployed_root(tmp_path, capsys):
    with pytest.raises(SystemExit):
        driver.main(
            [
                "--bundle",
                str(tmp_path),
                "--baseline",
                str(tmp_path / "baseline.json"),
                "--manifest-sha256",
                "0" * 64,
                "--state-dir",
                str(tmp_path / "state"),
                "dry-run",
            ]
        )
    assert "--deployed-root" in capsys.readouterr().err


@pytest.mark.parametrize("timing", ["before_dry_run", "between_phases"])
@pytest.mark.parametrize("change", ["version", "source_hash", "hidden", "expired", "locale_added"])
async def test_source_version_visibility_drift_refuses_without_partial_language_creation(
    tmp_path,
    database,
    owner,
    timing,
    change,
):
    bundle, path, before = await case(tmp_path, database, owner)
    if timing == "between_phases":
        await run(bundle, path, database, "dry-run")
    async with database() as session:
        article_id = UUID(before["test-guide"]["id"])
        if change == "version":
            await admin_service.save_draft(
                session,
                owner,
                article_id,
                "zh-TW",
                DraftWrite(
                    expected_version=2,
                    document=bundle.packs["test-guide"].locales["zh-TW"],
                ),
            )
        elif change == "source_hash":
            # Simulate corruption/legacy writes which did not advance the optimistic version.
            changed = bundle.packs["test-guide"].locales["zh-TW"].model_dump(mode="json")
            changed["title"] = "Changed source at same version"
            await session.execute(update(GuideArticleLocale).values(draft_json=changed))
            await session.commit()
        elif change == "hidden":
            await admin_service.set_visibility(
                session,
                owner,
                article_id,
                hidden=True,
                locale="zh-TW",
                payload=VisibilityWrite(
                    expected_version=1,
                    confirmed=True,
                    reason="Editorial withdrawal",
                ),
            )
        elif change == "expired":
            await session.execute(
                update(GuideArticle).values(valid_until=today() - timedelta(days=1))
            )
            await session.commit()
        else:
            await admin_service.start_translation(
                session,
                owner,
                article_id,
                "ja",
                bundle.packs["test-guide"].locales["ja"],
            )
    with pytest.raises(driver.Refused):
        await run(
            bundle,
            path,
            database,
            "drafts" if timing == "between_phases" else "dry-run",
        )
    assert "en" not in (await state(database))["locales"]


@pytest.mark.parametrize(
    "action",
    ["start_translation", "publish_locale", "create_article", "update_article"],
)
async def test_lost_response_after_commit_reconciles_without_a_second_revision(
    tmp_path,
    database,
    owner,
    monkeypatch,
    action,
):
    new = action in {"create_article", "update_article"}
    bundle, path, _ = await case(
        tmp_path,
        database,
        owner,
        new=new,
        order=142 if action == "update_article" else 100,
    )
    await run(bundle, path, database, "dry-run")
    phase = "publish-articles" if action == "publish_locale" else "drafts"
    if phase == "publish-articles":
        await run(bundle, path, database, "drafts")
    original = getattr(admin_service, action)
    calls = 0

    async def commit_then_lose_response(*args, **kwargs):
        nonlocal calls
        calls += 1
        await original(*args, **kwargs)
        raise ConnectionError("Response lost after commit")

    monkeypatch.setattr(admin_service, action, commit_then_lose_response)
    with pytest.raises(ConnectionError):
        await run(bundle, path, database, phase)
    journal = json.loads(path.read_text("utf-8"))
    assert journal["pending"] is not None
    written = await state(database)
    monkeypatch.setattr(admin_service, action, original)
    await run(bundle, path, database, phase)
    assert calls == 1
    journal = json.loads(path.read_text("utf-8"))
    assert journal["pending"] is None
    assert any(row["status"] == "committed_reconciled" for row in journal["history"])
    after = await state(database)
    for locale, row in written["locales"].items():
        assert after["locales"][locale] == row
    assert await revision_count(database) == (5 if new else 4 if action == "publish_locale" else 3)


async def test_failure_before_commit_retries_once_with_the_same_durable_intent(
    tmp_path, database, owner, monkeypatch
):
    bundle, path, _ = await case(tmp_path, database, owner)
    await run(bundle, path, database, "dry-run")
    original = admin_service.start_translation

    async def unavailable(*args, **kwargs):
        raise ConnectionError("No transaction was committed")

    monkeypatch.setattr(admin_service, "start_translation", unavailable)
    with pytest.raises(ConnectionError):
        await run(bundle, path, database, "drafts")
    monkeypatch.setattr(admin_service, "start_translation", original)
    await run(bundle, path, database, "drafts")
    assert await revision_count(database) == 3
    assert any(
        row["status"] == "not_written_reconciled"
        for row in json.loads(path.read_text("utf-8"))["history"]
    )


async def test_uncertain_commit_from_a_different_actor_is_not_adopted(
    tmp_path, database, owner, monkeypatch
):
    bundle, path, _ = await case(tmp_path, database, owner)
    await run(bundle, path, database, "dry-run")
    other = User(
        id=uuid4(),
        email="other-editor@example.com",
        password_hash=owner.password_hash,
        is_active=True,
    )
    async with database() as session:
        session.add(other)
        await session.commit()
    original = admin_service.start_translation

    async def unexpected_editor(session, actor, *args, **kwargs):
        await original(session, other, *args, **kwargs)
        raise ConnectionError("Different editor wrote the same document")

    monkeypatch.setattr(admin_service, "start_translation", unexpected_editor)
    with pytest.raises(ConnectionError):
        await run(bundle, path, database, "drafts")
    monkeypatch.setattr(admin_service, "start_translation", original)
    with pytest.raises(driver.Refused, match="actor mismatch"):
        await run(bundle, path, database, "drafts")
    assert json.loads(path.read_text("utf-8"))["pending"] is not None


async def test_existing_image_src_only_update_preserves_text_and_public_body_until_publish(
    tmp_path, database, owner
):
    bundle, path, before = await case(tmp_path, database, owner, images=True)
    manifest = copy.deepcopy(bundle.manifest)
    manifest["articles"][0]["locales"] = ["zh-TW"]
    manifest["articles"][0]["publish_locales"] = ["zh-TW"]
    pack = bundle.packs["test-guide"].model_dump(mode="json")
    pack["locales"]["zh-TW"]["hero"]["src"] = "/guides/test-guide/hero-zh-tw.jpg"
    asset = "public/guides/test-guide/hero-zh-tw.jpg"
    (bundle.root / asset).write_bytes(b"Reviewed localized hero")
    manifest["assets"] = [row for row in manifest["assets"] if not row["path"].endswith("hero.jpg")]
    manifest["assets"].append(
        {"path": asset, "sha256": driver.sha((bundle.root / asset).read_bytes())}
    )
    bundle = replace_bundle(bundle, manifest=manifest, pack=pack)
    await run(bundle, path, database, "dry-run")
    await run(bundle, path, database, "drafts")
    draft = (await state(database))["locales"]["zh-TW"]
    assert draft["published_sha256"] == before["test-guide"]["locales"]["zh-TW"]["published_sha256"]
    assert draft["draft_sha256"] != draft["published_sha256"]
    await run(bundle, path, database, "publish-articles")
    after = (await state(database))["locales"]["zh-TW"]
    assert after["published_sha256"] == after["draft_sha256"]
    assert after["published_at"] == before["test-guide"]["locales"]["zh-TW"]["published_at"]


async def test_existing_unpublished_edits_are_preserved_even_when_the_baseline_knows_them(
    tmp_path, database, owner
):
    bundle, path, before = await case(tmp_path, database, owner)
    async with database() as session:
        changed = bundle.packs["test-guide"].locales["zh-TW"].model_dump(mode="json")
        changed["title"] = "Unsaved editorial work"
        await admin_service.save_draft(
            session,
            owner,
            UUID(before["test-guide"]["id"]),
            "zh-TW",
            DraftWrite(expected_version=2, document=GuideDocument.model_validate(changed)),
        )
    actual = await state(database)
    baseline = json.loads(bundle.baseline_path.read_text("utf-8"))
    pinned = baseline["articles"][0]["database"]["locales"]["zh-TW"]
    pinned.update({key: actual["locales"]["zh-TW"][key] for key in pinned})
    manifest = copy.deepcopy(bundle.manifest)
    manifest["articles"][0]["locales"] = ["zh-TW"]
    manifest["articles"][0]["publish_locales"] = ["zh-TW"]
    bundle = replace_bundle(bundle, manifest=manifest, baseline=baseline)
    with pytest.raises(driver.Refused, match="unpublished edits"):
        await run(bundle, path, database, "dry-run")
    assert await state(database) == actual


async def test_publish_phase_order_actor_pin_and_changed_bundle_are_enforced(
    tmp_path, database, owner
):
    bundle, path, _ = await case(tmp_path, database, owner)
    with pytest.raises(driver.Refused, match="dry-run first"):
        await run(bundle, path, database, "drafts")
    await run(bundle, path, database, "dry-run")
    with pytest.raises(driver.Refused, match="Complete drafts"):
        await run(bundle, path, database, "publish-articles")
    with pytest.raises(driver.Refused, match="actor is pinned"):
        await run(bundle, path, database, "drafts", actor_id=uuid4())
    (bundle.root / bundle.manifest["articles"][0]["pack_path"]).write_text("{}", encoding="utf-8")
    with pytest.raises(driver.Refused, match="pack SHA256"):
        await run(bundle, path, database, "drafts")


async def test_unchanged_existing_publication_never_creates_a_redundant_revision(
    tmp_path,
    database,
    owner,
):
    bundle, path, before = await case(tmp_path, database, owner)
    manifest = copy.deepcopy(bundle.manifest)
    manifest["articles"][0]["locales"] = ["zh-TW"]
    manifest["articles"][0]["publish_locales"] = ["zh-TW"]
    bundle = replace_bundle(bundle, manifest=manifest)
    for phase in ["dry-run", "drafts", "publish-articles", "publish-hubs"]:
        await run(bundle, path, database, phase)
    assert await state(database) == before["test-guide"]
    assert await revision_count(database) == 2


async def test_same_stem_svg_source_is_allowed_but_unrelated_asset_is_refused(
    tmp_path,
    database,
    owner,
):
    bundle, _, _ = await case(tmp_path, database, owner, images=True)
    manifest = copy.deepcopy(bundle.manifest)
    companion = "public/guides/test-guide/hero.svg"
    (bundle.root / companion).write_bytes(b"Editable hero vector")
    manifest["assets"].append(
        {
            "path": companion,
            "sha256": driver.sha((bundle.root / companion).read_bytes()),
        }
    )
    bundle = replace_bundle(bundle, manifest=manifest)
    unrelated = "public/guides/test-guide/unrelated.svg"
    (bundle.root / unrelated).write_bytes(b"Not referenced and not a raster source")
    manifest["assets"].append(
        {
            "path": unrelated,
            "sha256": driver.sha((bundle.root / unrelated).read_bytes()),
        }
    )
    with pytest.raises(driver.Refused, match="unrelated or unused"):
        replace_bundle(bundle, manifest=manifest)


async def test_deactivated_owner_stops_resume_without_exposing_identity(tmp_path, database, owner):
    bundle, path, _ = await case(tmp_path, database, owner)
    await run(bundle, path, database, "dry-run")
    async with database() as session:
        await session.execute(update(User).where(User.id == owner.id).values(is_active=False))
        await session.commit()
    with pytest.raises(driver.Refused, match="No active configured owner") as failure:
        await run(bundle, path, database, "drafts")
    assert owner.email not in str(failure.value)


async def test_hub_waits_for_exact_public_dependency_across_bundles(tmp_path, database, owner):
    dependency, dep_path, _ = await case(tmp_path, database, owner, slug="part-one")
    bundle, path, _ = await case(tmp_path, database, owner, slug="series-hub")
    baseline = json.loads(bundle.baseline_path.read_text("utf-8"))
    baseline["articles"].extend(json.loads(dependency.baseline_path.read_text("utf-8"))["articles"])
    manifest = copy.deepcopy(bundle.manifest)
    manifest["articles"][0].update(
        {
            "hub": True,
            "requires": [
                {
                    "slug": "part-one",
                    "locale": "en",
                    "document_sha256": driver.document_hash(
                        dependency.packs["part-one"].locales["en"].model_dump(mode="json")
                    ),
                }
            ],
        }
    )
    bundle = replace_bundle(bundle, manifest=manifest, baseline=baseline)
    for phase in ["dry-run", "drafts", "publish-articles"]:
        await run(bundle, path, database, phase)
    with pytest.raises(driver.Refused, match="dependency is not published"):
        await run(bundle, path, database, "publish-hubs")
    assert (await state(database, "series-hub"))["locales"]["en"]["published_version"] is None
    for phase in ["dry-run", "drafts", "publish-articles"]:
        await run(dependency, dep_path, database, phase)
    await run(bundle, path, database, "publish-hubs")
    assert (await state(database, "series-hub"))["locales"]["en"]["published_version"] == 2


@pytest.mark.parametrize(
    "violation",
    ["new_publish", "old_text", "unselected_text", "unsafe_path", "over_twenty"],
)
async def test_manifest_refuses_unapproved_scope_before_any_write(
    tmp_path, database, owner, violation
):
    bundle, _, _ = await case(tmp_path, database, owner, new=violation == "new_publish")
    manifest = copy.deepcopy(bundle.manifest)
    pack = bundle.packs["test-guide"].model_dump(mode="json")
    if violation == "new_publish":
        manifest["articles"][0]["publish_locales"] = ["en"]
    elif violation == "old_text":
        manifest["articles"][0]["locales"] = ["zh-TW"]
        manifest["articles"][0]["publish_locales"] = []
        pack["locales"]["zh-TW"]["blocks"][1]["text"] = "Unapproved original rewrite"
    elif violation == "unselected_text":
        pack["locales"]["zh-TW"]["title"] = "Unapproved unselected rewrite"
    elif violation == "unsafe_path":
        manifest["articles"][0]["pack_path"] = "../unapproved.json"
    else:
        manifest["articles"] *= 21
    with pytest.raises(driver.Refused):
        replace_bundle(bundle, manifest=manifest, pack=None if violation == "unsafe_path" else pack)
