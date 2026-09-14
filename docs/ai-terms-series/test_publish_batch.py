"""Local-only tests for the release driver's state machine and source pinning.

Run from repo root:
  set PYTHONPATH=apps/api
  apps/api/.venv/Scripts/python.exe -m pytest -c apps/api/pyproject.toml \
    docs/ai-terms-series/test_publish_batch.py
Uses the existing disposable guide fixtures; production CLI is never invoked.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from app.guides import admin_service
from app.guides.content_pack import apply_import, load_packs, plan_import
from app.guides.models import GuideArticle, GuideArticleLocale
from app.guides.schemas import DraftWrite
from sqlalchemy import select
from tests import test_guides as guides

spec = importlib.util.spec_from_file_location(
    "ai_terms_publish_batch", Path(__file__).with_name("publish_batch.py")
)
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)

database = guides.database
actor = guides.actor


@pytest.fixture
def packs():
    return {pack.slug: pack for pack in load_packs(slugs=set(driver.SLUGS))}


async def seed_existing(database, actor, packs):
    prior = []
    for slug in driver.UPDATED:
        pack = packs[slug].model_copy(deep=True)
        pack.locales["zh-TW"].title = "舊公開版本：" + pack.locales["zh-TW"].title[:40]
        prior.append(pack)
    async with database() as session:
        plan = await plan_import(session, prior, locales={"zh-TW"})
        report = await apply_import(session, actor, plan, publish=True)
        assert report.failed is None


def args(tmp_path, phase):
    return SimpleNamespace(
        phase=phase,
        manifest_sha256="0" * 64,
        manifest=tmp_path / "manifest.json",
        public_dir=tmp_path / "public",
    )


@pytest.mark.parametrize("uncertain_commit", [False, True])
async def test_resume_preserves_publications_and_publishes_index_last(
    database,
    actor,
    packs,
    tmp_path,
    monkeypatch,
    uncertain_commit,
):
    await seed_existing(database, actor, packs)
    monkeypatch.setattr(driver, "verify_bundle", lambda *a: packs)

    async def active(_session):
        return actor

    monkeypatch.setattr(driver, "active_actor", active)
    journal = tmp_path / "journal.json"
    db_engine = database.kw["bind"]
    await driver.execute_phase(args(tmp_path, "dry-run"), packs, journal, db_engine)
    baseline = json.loads(journal.read_text())["expected"]
    original_apply = driver.apply_import
    interrupted = driver.SLUGS[2]

    async def fail_once(session, user, plan, *, publish):
        if plan.articles[0].pack.slug == interrupted:
            if uncertain_commit:
                await original_apply(session, user, plan, publish=publish)
            raise OSError("simulated interruption")
        return await original_apply(session, user, plan, publish=publish)

    monkeypatch.setattr(driver, "apply_import", fail_once)
    with pytest.raises(OSError, match="simulated"):
        await driver.execute_phase(args(tmp_path, "drafts"), packs, journal, db_engine)
    stopped = json.loads(journal.read_text())
    assert stopped["done"]["drafts"] == list(driver.SLUGS[:2])
    assert stopped["pending"]["slug"] == interrupted
    monkeypatch.setattr(driver, "apply_import", original_apply)
    await driver.execute_phase(args(tmp_path, "drafts"), packs, journal, db_engine)
    staged = json.loads(journal.read_text())["expected"]
    for slug in driver.NEW:
        assert staged[slug]["locales"]["zh-TW"]["published_version"] is None
        assert staged[slug]["locales"]["zh-TW"]["version"] == 1
    for slug in driver.UPDATED:
        assert (
            staged[slug]["locales"]["zh-TW"]["published_sha256"]
            == baseline[slug]["locales"]["zh-TW"]["published_sha256"]
        )
    with pytest.raises(driver.Refused, match="Complete publish-articles"):
        await driver.execute_phase(
            args(tmp_path, "publish-index"), packs, journal, db_engine
        )
    await driver.execute_phase(
        args(tmp_path, "publish-articles"), packs, journal, db_engine
    )
    published = json.loads(journal.read_text())["expected"]
    driver.require_public(
        published, packs, [s for s in driver.SLUGS if s != driver.INDEX]
    )
    assert published[driver.INDEX]["locales"]["zh-TW"]["published_version"] is None
    await driver.execute_phase(
        args(tmp_path, "publish-index"), packs, journal, db_engine
    )
    final = json.loads(journal.read_text())["expected"]
    driver.require_public(final, packs, driver.SLUGS)
    await driver.execute_phase(
        args(tmp_path, "publish-index"), packs, journal, db_engine
    )
    assert json.loads(journal.read_text())["expected"] == final


async def test_unexpected_old_draft_and_later_change_stop(
    database,
    actor,
    packs,
    tmp_path,
    monkeypatch,
):
    await seed_existing(database, actor, packs)
    monkeypatch.setattr(driver, "verify_bundle", lambda *a: packs)
    db_engine = database.kw["bind"]
    journal = tmp_path / "journal.json"
    await driver.execute_phase(args(tmp_path, "dry-run"), packs, journal, db_engine)
    slug = next(iter(driver.UPDATED))
    async with database() as session:
        article = await session.scalar(
            select(GuideArticle).where(GuideArticle.slug == slug)
        )
        row = await session.scalar(
            select(GuideArticleLocale).where(
                GuideArticleLocale.article_id == article.id,
                GuideArticleLocale.locale == "zh-TW",
            )
        )
        await admin_service.save_draft(
            session,
            actor,
            article.id,
            "zh-TW",
            DraftWrite(
                expected_version=row.version, document=packs[slug].locales["zh-TW"]
            ),
        )
    with pytest.raises(driver.Refused, match="Concurrent/unexpected"):
        await driver.execute_phase(args(tmp_path, "drafts"), packs, journal, db_engine)
    with pytest.raises(driver.Refused, match="unexpected unpublished draft"):
        await driver.execute_phase(
            args(tmp_path, "dry-run"), packs, tmp_path / "new.json", db_engine
        )


def test_hash_and_exact_scope_guards(packs, tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[2]
    public = root / "apps/web/public"
    directory = tmp_path / "content"
    directory.mkdir()
    files = {}
    for slug, pack in packs.items():
        data = (driver.default_directory() / (slug + ".json")).read_bytes()
        (directory / (slug + ".json")).write_bytes(data)
        files[driver.PACK_PREFIX + slug + ".json"] = driver.sha(data)
        doc = pack.locales["zh-TW"]
        for src in [doc.hero.src] + [b.src for b in doc.blocks if b.type == "image"]:
            files[driver.ASSET_PREFIX + src.lstrip("/")] = driver.sha(
                (public / src.lstrip("/")).read_bytes()
            )
    manifest = {
        "slugs": list(driver.SLUGS),
        "locale": "zh-TW",
        "index_last": driver.INDEX,
        "new_slugs": sorted(driver.NEW),
        "updated_slugs": sorted(driver.UPDATED),
        "files": files,
    }
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    digest = driver.sha(path.read_bytes())
    monkeypatch.setattr(driver, "default_directory", lambda: directory)
    assert len(driver.verify_bundle(path, digest, public)) == 83
    target = directory / (driver.SLUGS[0] + ".json")
    target.write_bytes(target.read_bytes() + b" ")
    with pytest.raises(driver.Refused, match="pack SHA256 mismatch"):
        driver.verify_bundle(path, digest, public)
    with pytest.raises(driver.Refused, match="Manifest SHA256"):
        driver.verify_bundle(path, "0" * 64, public)
    manifest["slugs"][-1] = "unrelated"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(driver.Refused, match="exactly"):
        driver.verify_bundle(path, driver.sha(path.read_bytes()), public)
