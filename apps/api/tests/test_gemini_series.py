"""Import the reviewed 51-page series through the real article persistence boundary."""
from __future__ import annotations

import json
from pathlib import Path

from app.guides.content_pack import apply_import, load_packs, plan_import
from tests import test_guides as guides

database = guides.database
actor = guides.actor
CATALOGUE = json.loads(
    (Path(__file__).resolve().parents[2] / "web/lib/guide-series.json").read_text(
        encoding="utf8"
    )
)


async def test_complete_series_import_preserves_documents_and_sitemap(database, actor) -> None:
    catalogue = CATALOGUE
    slugs = [a["slug"] for a in catalogue["articles"]] + [catalogue["hubSlug"]]
    packs = load_packs(slugs=set(slugs))
    assert len(packs) == 51
    by_slug = {pack.slug: pack for pack in packs}
    async with database() as session:
        plan = await plan_import(session, [by_slug[slug] for slug in slugs], locales={"zh-TW"})
        assert len(plan.articles) == 51
        report = await apply_import(session, actor, plan, publish=True)
    assert report.failed is None
    assert len(report.published) == 51
    async with guides.client(guides.make_app(database, actor)) as api:
        for slug in slugs:
            response = await api.get(f"/guides/life/{slug}", params={"locale": "zh-TW"})
            assert response.status_code == 200, slug
            document = response.json()["document"]
            expected = by_slug[slug].locales["zh-TW"].model_dump(mode="json")
            for key in ("title", "description", "hero", "blocks", "sources"):
                assert document[key] == expected[key], f"{slug}: {key} changed on import"
        response = await api.get("/guides/sitemap")
        entries = response.json()["entries"]
        assert set(slugs) <= {
            entry["slug"] for entry in entries if entry["locale"] == "zh-TW"
        }
    async with database() as session:
        again = await plan_import(session, packs, locales={"zh-TW"})
        assert all(entry.taxonomy == "unchanged" for entry in again.articles)
        assert all(not locale.publish for entry in again.articles for locale in entry.locales)
