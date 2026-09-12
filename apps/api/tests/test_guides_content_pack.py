"""Content packs: articles authored in the repository, imported through the admin write path.

Reuses the guides fixtures (SQLite plus the optional PostgreSQL leg) so an import is proven
against the same tables and endpoints the editor uses.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.guides.content_pack import (
    ContentPackError,
    apply_import,
    default_directory,
    load_packs,
    plan_import,
)
from app.guides.schemas import ImageBlock
from tests import test_guides as guides

# The guides fixtures, registered here under their own names. Bound by assignment rather
# than imported, so a test parameter of the same name is not a redefinition to the linter.
database = guides.database
actor = guides.actor
client = guides.client
make_app = guides.make_app
document = guides.document
publish = guides.publish


def write_pack(directory: Path, slug: str, **overrides) -> Path:
    pack = {
        "slug": slug,
        "kind": "howto",
        "destination_id": "tokyo",
        "topics": ["transport"],
        "featured": True,
        "display_order": 10,
        "locales": {
            "zh-TW": document(),
            "en": document(title="Narita to Tokyo", description="Three ways, compared"),
        },
        **overrides,
    }
    path = directory / f"{slug}.json"
    path.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
    return path


async def test_an_import_creates_publishes_and_is_idempotent(database, actor, tmp_path) -> None:
    write_pack(tmp_path, "narita-to-tokyo")

    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        assert [entry.taxonomy for entry in plan.articles] == ["create"]
        report = await apply_import(session, actor, plan, publish=True)
    assert report.failed is None
    assert report.created == ["narita-to-tokyo:zh-TW", "narita-to-tokyo:en"]
    assert report.published == ["narita-to-tokyo:zh-TW", "narita-to-tokyo:en"]

    async with client(make_app(database)) as api:
        english = (await api.get("/guides/howto/narita-to-tokyo", params={"locale": "en"})).json()
        assert english["status"] == "published"
        assert english["document"]["title"] == "Narita to Tokyo"
        assert english["published_locales"] == ["en", "zh-TW"]
        listed = (await api.get("/guides", params={"locale": "zh-TW"})).json()["articles"]
        # The flags ArticleCreate cannot carry were applied right after creation.
        assert listed[0]["featured"] is True

    # A second run finds nothing to do and publishes nothing again.
    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        assert [entry.taxonomy for entry in plan.articles] == ["unchanged"]
        report = await apply_import(session, actor, plan, publish=True)
    assert report.unchanged == ["narita-to-tokyo:zh-TW", "narita-to-tokyo:en"]
    assert report.created == [] and report.updated == [] and report.published == []

    # Editing one locale in the pack updates and republishes only that locale.
    write_pack(
        tmp_path,
        "narita-to-tokyo",
        locales={
            "zh-TW": document(title="票價已更新"),
            "en": document(title="Narita to Tokyo", description="Three ways, compared"),
        },
    )
    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        report = await apply_import(session, actor, plan, publish=True)
    assert report.updated == ["narita-to-tokyo:zh-TW"]
    assert report.published == ["narita-to-tokyo:zh-TW"]
    assert report.unchanged == ["narita-to-tokyo:en"]
    async with client(make_app(database)) as api:
        body = (await api.get("/guides/howto/narita-to-tokyo", params={"locale": "zh-TW"})).json()
        assert body["document"]["title"] == "票價已更新"
        assert body["document"]["modified_at"] > body["document"]["published_at"]


async def test_taxonomy_changes_are_applied_without_touching_the_text(
    database, actor, tmp_path
) -> None:
    write_pack(tmp_path, "narita-to-tokyo")
    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        await apply_import(session, actor, plan, publish=False)

    write_pack(tmp_path, "narita-to-tokyo", topics=["transport", "budget"], featured=False)
    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        assert plan.articles[0].taxonomy == "update"
        report = await apply_import(session, actor, plan, publish=False)
    assert report.taxonomy_updated == ["narita-to-tokyo"]
    assert report.unchanged == ["narita-to-tokyo:zh-TW", "narita-to-tokyo:en"]

    async with client(make_app(database, actor)) as api:
        rows = (await api.get("/admin/guides", params={"locale": "zh-TW"})).json()["articles"]
        assert sorted(topic["slug"] for topic in rows[0]["topics"]) == ["budget", "transport"]
        assert rows[0]["featured"] is False


async def test_a_bad_pack_stops_the_run_before_anything_is_written(
    database, actor, tmp_path
) -> None:
    write_pack(tmp_path, "good-one")
    write_pack(tmp_path, "bad-one", destination_id="atlantis")
    async with database() as session:
        with pytest.raises(ContentPackError, match="guide_destination_unknown"):
            await plan_import(session, load_packs(tmp_path))
    async with client(make_app(database)) as api:
        assert (await api.get("/guides", params={"locale": "zh-TW"})).json()["articles"] == []


def test_a_pack_must_be_named_after_its_slug_and_parse(tmp_path) -> None:
    path = write_pack(tmp_path, "narita-to-tokyo")
    path.rename(tmp_path / "other-name.json")
    with pytest.raises(ContentPackError, match="must match the file name"):
        load_packs(tmp_path)
    (tmp_path / "other-name.json").unlink()

    (tmp_path / "broken.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(ContentPackError, match="broken.json"):
        load_packs(tmp_path)


async def test_a_refusal_mid_run_is_reported_and_the_rest_waits(database, actor, tmp_path) -> None:
    """A write-time refusal (the API's own rules) stops the run and names the rule."""
    async with client(make_app(database, actor)) as api:
        response = await api.post(
            "/admin/guides",
            json={
                "slug": "moved-article",
                "kind": "howto",
                "destination_id": "tokyo",
                "topics": [],
                "document": document(),
            },
        )
        created = response.json()
        await publish(api, created["id"], "zh-TW", created["version"])

    # The pack now says this published article is a lifestyle piece: a cross-section move
    # the API refuses with 409 while any locale is public.
    write_pack(tmp_path, "moved-article", kind="life", topics=["ai"], destination_id=None)
    write_pack(tmp_path, "zzz-later", destination_id="seoul")
    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        report = await apply_import(session, actor, plan, publish=False)
    assert report.failed is not None
    assert "guide_kind_locked" in report.failed
    # The run stopped there: the later pack was never written.
    async with client(make_app(database, actor)) as api:
        rows = (await api.get("/admin/guides", params={"locale": "zh-TW"})).json()["articles"]
        assert [row["slug"] for row in rows] == ["moved-article"]


async def test_only_the_requested_locales_are_planned(database, actor, tmp_path) -> None:
    write_pack(tmp_path, "narita-to-tokyo")
    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path), locales={"en"})
        assert [item.locale for item in plan.articles[0].locales] == ["en"]
        report = await apply_import(session, actor, plan, publish=True)
    assert report.created == ["narita-to-tokyo:en"]


def test_the_packaged_content_validates_and_its_images_exist() -> None:
    """Every pack that ships in the repository must import cleanly and every picture it
    names must be a real file under the web app's public folder, small enough to serve."""
    packs = load_packs()
    web_public = Path(__file__).resolve().parents[2] / "web" / "public"
    if packs and not web_public.is_dir():
        pytest.skip("the web app is not checked out next to the API")
    assert all(pack.slug == pack.slug.casefold() for pack in packs)
    for pack in packs:
        for locale, doc in pack.locales.items():
            sources = [doc.hero.src] if doc.hero else []
            sources += [block.src for block in doc.blocks if isinstance(block, ImageBlock)]
            for src in sources:
                file = web_public / src.lstrip("/")
                assert file.is_file(), f"{pack.slug} ({locale}): missing {src}"
                assert file.stat().st_size <= 300_000, f"{pack.slug} ({locale}): {src} is too large"
            assert doc.sources, f"{pack.slug} ({locale}): an article must cite its sources"


def test_the_default_directory_is_inside_the_package() -> None:
    assert default_directory().name == "content"
    assert default_directory().parent.name == "guides"
