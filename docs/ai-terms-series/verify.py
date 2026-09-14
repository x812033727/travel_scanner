"""Validate this editorial series. Production is never contacted or written.

Run apps/api/.venv/Scripts/python.exe docs/ai-terms-series/verify.py --partial
while authoring; omit --partial for the completeness gate. --database exercises
draft/publication/idempotence in a disposable SQLite database after ingestion.
"""
from __future__ import annotations

import argparse
import asyncio
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse
from uuid import uuid4

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / "apps/api"), str(ROOT / "apps/api/tests")]

from app.guides.content_pack import ArticlePack, apply_import, load_packs, plan_import
from app.guides.pack_ingest import check_svg, lint_document, missing_diagram_numbers


def prose(document: dict) -> str:
    result = []
    for block in document["blocks"]:
        if block["type"] == "paragraph":
            result.append(block["text"])
        elif block["type"] == "list":
            result.extend(block["items"])
    return "\n".join(result)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def validate(partial: bool) -> dict:
    catalogue = read_json(HERE / "catalogue.json")
    terms = catalogue["terms"] + [{"slug": "ai-terms-index", "action": "new-index"}]
    assert len({t["slug"] for t in terms}) == len(terms)
    errors, warnings, results, missing = [], [], [], []
    titles, bodies, repeated, visuals = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    all_slugs = {t["slug"] for t in terms} | {"ai-terms-index"}
    all_slugs |= {p.stem for p in (ROOT / "apps/api/app/guides/content").glob("*.json")}
    for term in terms:
        slug = term["slug"]
        folder = HERE / "staging" / slug
        required = [folder / f for f in ["pack.json", "hero.svg", "diagram-1.svg", "research.json", "notes.md"]]
        if not all(p.is_file() for p in required):
            missing.append(slug)
            continue
        try:
            raw = read_json(folder / "pack.json")
            pack = ArticlePack.model_validate(raw)
            research = read_json(folder / "research.json")
            document = raw["locales"]["zh-TW"]
            doc = pack.locales["zh-TW"]
            text = prose(document)
            count = len(re.sub(r"\s", "", text))
            issue = lambda message: errors.append({"slug": slug, "message": message})
            if pack.slug != slug or pack.kind != "life" or set(pack.locales) != {"zh-TW"}:
                issue("Wrong slug, kind or locale")
            if pack.destination_id is not None or set(pack.topics) - {"ai", "tutorial"}:
                issue("Wrong destination/topics")
            if not 1800 <= count <= 3000:
                issue(f"Running prose must be 1800–3000 non-whitespace characters, found {count}")
            if len(document["title"]) > 60 or not 120 <= len(document["description"]) <= 200:
                issue("Title/description outside editorial range")
            if research.get("status") != "verified" or not research.get("sources"):
                issue("Research not verified")
            if len(doc.sources) < 2 or any(not s.checked_on for s in doc.sources):
                issue("Need checked primary sources")
            links = [b["url"] for b in document["blocks"] if b["type"] == "link"]
            if slug != "ai-terms-index" and "https://mokaair.com/zh-TW/life/ai-terms-index" not in links:
                issue("Missing index backlink")
            if slug == "ai-terms-index":
                linked = {url.rstrip("/").split("/")[-1] for url in links}
                absent = {t["slug"] for t in catalogue["terms"]} - linked
                if absent:
                    issue(f"Index missing terms: {sorted(absent)}")
            for url in links:
                if url.startswith("https://mokaair.com/zh-TW/life/") and url.rstrip("/").split("/")[-1] not in all_slugs:
                    issue(f"Unknown internal article: {url}")
            for p in lint_document(doc, "life"):
                (errors if p.level == "error" else warnings).append({"slug": slug, "message": str(p)})
            for name in ["hero.svg", "diagram-1.svg"]:
                svg = (folder / name).read_text(encoding="utf-8")
                visuals[hashlib.sha256(svg.encode()).hexdigest()].append(f"{slug}/{name}")
                for p in check_svg(svg):
                    (errors if p.level == "error" else warnings).append({"slug": slug, "message": f"{name}: {p}"})
                if name.startswith("diagram"):
                    numbers = missing_diagram_numbers(svg, doc)
                    if numbers:
                        issue(f"Diagram numbers missing from prose: {numbers}")
            normalized = re.sub(r"\s", "", text)
            bodies[hashlib.sha256(normalized.encode()).hexdigest()].append(slug)
            titles[document["title"]].append(slug)
            for b in document["blocks"]:
                if b["type"] == "paragraph" and len(b["text"]) >= 100:
                    repeated[b["text"]].append(slug)
            results.append({"slug": slug, "title": document["title"], "running_characters": count,
                            "source_count": len(doc.sources), "source_domains": sorted({urlparse(s.url).netloc for s in doc.sources}),
                            "action": term["action"]})
        except Exception as exc:
            errors.append({"slug": slug, "message": str(exc)})
    for label, groups in [("identical title", titles), ("identical article", bodies), ("reused long paragraph", repeated), ("identical SVG", visuals)]:
        for key, members in groups.items():
            if len(set(members)) > 1:
                errors.append({"slug": members, "message": label, "sample": key[:100]})
    if missing and not partial:
        errors.append({"slug": missing, "message": "Incomplete series; publication forbidden"})
    glossary = read_json(ROOT / "apps/api/app/guides/content/ai-glossary-50-terms.json")
    glossary_doc = ArticlePack.model_validate(glossary).locales["zh-TW"]
    for p in lint_document(glossary_doc, "life"):
        (errors if p.level == "error" else warnings).append({"slug": glossary["slug"], "message": str(p)})
    if not any(b["type"] == "link" and b["url"] == "https://mokaair.com/zh-TW/life/ai-terms-index" for b in glossary["locales"]["zh-TW"]["blocks"]):
        errors.append({"slug": glossary["slug"], "message": "Missing index link"})
    return {"candidate_terms": len(catalogue["terms"]), "complete_staging": len(results), "missing": missing,
            "errors": errors, "warnings": warnings, "articles": results, "production_writes": 0}


async def database_check() -> dict:
    from sqlalchemy import event
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
    from app.db import Base
    from app.guides.models import GuideTopic
    from app.guides.taxonomy import LIFE_SEED_TOPICS, SEED_TOPICS, seed_names
    from app.models import User
    from test_guides import TABLES, client, make_app
    terms = read_json(HERE / "catalogue.json")["terms"]
    slugs = {t["slug"] for t in terms} | {"ai-terms-index", "ai-glossary-50-terms"}
    packs = load_packs(slugs=slugs)
    assert {p.slug for p in packs} == slugs, "Ingest complete series and index first"
    reused = {t["slug"] for t in terms if t["action"] != "new"} | {"ai-glossary-50-terms"}
    baseline = []
    for pack in packs:
        if pack.slug in reused:
            old = pack.model_copy(deep=True)
            old.locales["zh-TW"].title = "驗證用舊版：" + old.locales["zh-TW"].title
            baseline.append(old)
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    @event.listens_for(engine.sync_engine, "connect")
    def fk(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")
    try:
        async with engine.begin() as connection:
            await connection.run_sync(lambda c: Base.metadata.create_all(c, tables=TABLES))
        factory = async_sessionmaker(engine, expire_on_commit=False)
        actor = User(id=uuid4(), email="ai-terms-validation@example.com", password_hash="local-only", is_admin=True, is_active=True)
        async with factory() as session:
            for section, topics in [("travel", SEED_TOPICS), ("life", LIFE_SEED_TOPICS)]:
                for order, (slug, labels) in enumerate(topics):
                    session.add(GuideTopic(slug=slug, names_json=seed_names(labels), display_order=order * 10, section=section, source="seed"))
            session.add(actor)
            await session.commit()
            before = await apply_import(session, actor, await plan_import(session, baseline), publish=True)
            assert before.failed is None and len(before.published) == len(reused)
            draft = await apply_import(session, actor, await plan_import(session, packs), publish=False)
            assert draft.failed is None and len(draft.created) == len(packs) - len(reused) and not draft.published
        async with client(make_app(factory)) as api:
            for pack in packs:
                data = (await api.get(f"/guides/life/{pack.slug}", params={"locale": "zh-TW"})).json()
                if pack.slug in reused:
                    assert data["status"] == "published" and data["document"]["title"].startswith("驗證用舊版："), pack.slug
                else:
                    assert data["status"] == "unpublished", pack.slug
        async with factory() as session:
            published = await apply_import(session, actor, await plan_import(session, packs), publish=True)
            assert published.failed is None and len(published.published) == len(packs)
            again = await apply_import(session, actor, await plan_import(session, packs), publish=True)
            assert again.failed is None and len(again.unchanged) == len(packs)
            assert not again.created and not again.updated and not again.published
        async with client(make_app(factory)) as api:
            for pack in packs:
                data = (await api.get(f"/guides/life/{pack.slug}", params={"locale": "zh-TW"})).json()
                assert data["status"] == "published" and data["document"]["title"] == pack.locales["zh-TW"].title
                foreign = (await api.get(f"/guides/life/{pack.slug}", params={"locale": "en"})).json()
                assert foreign["status"] == "unpublished"
        return {"engine": "SQLite memory", "drafts_hidden": len(packs) - len(reused),
                "draft_updates_preserve_public": len(reused), "published_reads": len(packs),
                "untranslated_hidden": len(packs), "idempotent_unchanged": len(packs), "production_writes": 0}
    finally:
        await engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--partial", action="store_true")
    parser.add_argument("--database", action="store_true")
    args = parser.parse_args()
    report = validate(args.partial)
    if args.database and not report["errors"] and not report["missing"]:
        report["database"] = asyncio.run(database_check())
    (HERE / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "articles"}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(report["errors"]))
