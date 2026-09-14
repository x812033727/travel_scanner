"""Tutorial blocks remain inert, and the series is a complete navigable content pack."""

import json
import subprocess
import sys
from hashlib import sha256
from pathlib import Path
from shutil import copyfile
from zipfile import ZipFile

import pytest
from pydantic import ValidationError
from sqlalchemy import func, select

from app.guides.content_pack import ArticlePack, apply_import, load_packs, plan_import
from app.guides.models import GuideArticle, GuideArticleLocale, GuideArticleRevision
from app.guides.schemas import GuideDocument
from app.models import AdminAuditLog
from tests import test_guides as guides

ROOT = Path(__file__).resolve().parents[3]
database = guides.database
actor = guides.actor


def test_practice_download_contains_current_exercise_files_and_manifest():
    practice = ROOT / "docs/codex-learning/practice"
    sources = {
        path.relative_to(practice).as_posix(): path
        for path in practice.rglob("*")
        if path.is_file() and path.suffix in {".html", ".css", ".js", ".mjs", ".md"}
    }
    with ZipFile(ROOT / "apps/web/public/guides/codex-first-project/todo-practice.zip") as archive:
        expected_names = {f"codex-practice/{name}" for name in sources}
        assert set(archive.namelist()) == expected_names
        assert archive.namelist() == sorted(expected_names)
        assert archive.testzip() is None
        for name, path in sources.items():
            # Git stores these text files as LF; the downloaded bytes must also
            # be LF even when an authoring tool wrote CRLF in the checkout.
            expected = path.read_bytes().replace(b"\r\n", b"\n")
            assert archive.read(f"codex-practice/{name}") == expected
    manifest = json.loads((practice / "manifest.json").read_text(encoding="utf-8"))
    expected_hashes = {
        name: sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        for name, path in sources.items()
    }
    assert manifest == expected_hashes


@pytest.mark.parametrize("line_ending", [b"\n", b"\r\n"], ids=["lf", "crlf"])
def test_practice_packaging_is_reproducible_across_checkouts(tmp_path, line_ending):
    practice = ROOT / "docs/codex-learning/practice"
    source = tmp_path / "source"
    before = {}
    for path in practice.rglob("*"):
        if not path.is_file() or path.suffix not in {".html", ".css", ".js", ".mjs", ".md"}:
            continue
        target = source / path.relative_to(practice)
        target.parent.mkdir(parents=True, exist_ok=True)
        content = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", line_ending)
        target.write_bytes(content)
        before[target] = content
    archive = tmp_path / "practice.zip"
    manifest = tmp_path / "manifest.json"
    subprocess.run(
        [sys.executable, str(ROOT / "tools/codex-learning/practice_archive.py"),
         "--source", str(source), "--archive", str(archive), "--manifest", str(manifest)],
        check=True, capture_output=True, text=True,
    )
    assert archive.read_bytes() == (
        ROOT / "apps/web/public/guides/codex-first-project/todo-practice.zip"
    ).read_bytes()
    assert manifest.read_bytes() == (practice / "manifest.json").read_bytes()
    assert all(path.read_bytes() == content for path, content in before.items())


@pytest.mark.parametrize("database", ["sqlite"], indirect=True)
async def test_complete_series_import_preserves_identity_and_publication(database, actor, tmp_path):
    """Exercise all real packs in temporary SQLite, never the configured database."""
    catalog = json.loads(
        (ROOT / "apps/web/lib/codex-learning/catalog.json").read_text(encoding="utf-8")
    )
    slugs = {row["slug"] for row in catalog} | {"codex-learning-hub"}
    directory = tmp_path / "codex-only"
    directory.mkdir()
    for slug in slugs:
        copyfile(ROOT / f"apps/api/app/guides/content/{slug}.json", directory / f"{slug}.json")
    packs = load_packs(directory)
    assert len(packs) == 61 and sum(len(pack.locales) for pack in packs) == 305

    # These three routes already existed before the expanded series. A new draft
    # must keep their identities and leave the old public revision available.
    existing = {"codex-beginner-guide", "codex-cli-getting-started", "codex-cloud-tasks-github"}
    seeds = []
    for pack in packs:
        if pack.slug in existing:
            seed = pack.model_copy(deep=True)
            seed.locales = {"zh-TW": seed.locales["zh-TW"]}
            seed.locales["zh-TW"].title = f"Existing {pack.slug}"
            seeds.append(seed)
    seeds.append(
        ArticlePack(
            slug="unrelated-local-article",
            kind="life",
            topics=["ai"],
            locales={
                "en": GuideDocument.model_validate(guides.document(title="Unrelated fixture"))
            },
        )
    )

    async def counts(session):
        return tuple(
            [
                await session.scalar(select(func.count()).select_from(model))
                for model in [GuideArticle, GuideArticleLocale, GuideArticleRevision, AdminAuditLog]
            ]
        )

    async with database() as session:
        seeded = await apply_import(session, actor, await plan_import(session, seeds), publish=True)
        assert seeded.failed is None and len(seeded.published) == 4
        identities = dict((await session.execute(select(GuideArticle.slug, GuideArticle.id))).all())
        control = (
            await session.execute(
                select(
                    GuideArticleLocale.id,
                    GuideArticleLocale.version,
                    GuideArticleLocale.published_version,
                    GuideArticleLocale.draft_json,
                ).where(GuideArticleLocale.article_id == identities["unrelated-local-article"])
            )
        ).one()
        before_plan = await counts(session)
        plan = await plan_import(session, packs)
        assert await counts(session) == before_plan
        drafted = await apply_import(session, actor, plan, publish=False)
        assert drafted.failed is None and drafted.published == []
        assert len(drafted.created) == 302 and len(drafted.updated) == 3
        assert (await counts(session))[:2] == (62, 306)

    async with guides.client(guides.make_app(database)) as api:
        for slug in existing:
            response = await api.get(f"/guides/life/{slug}", params={"locale": "zh-TW"})
            assert response.json()["document"]["title"] == f"Existing {slug}"
        for locale in ["zh-TW", "zh-CN", "en", "ja", "ko"]:
            response = await api.get("/guides/life/codex-learning-hub", params={"locale": locale})
            assert response.json()["status"] == "unpublished"
            assert response.json()["document"] is None
            assert (
                await api.get("/guides/series/codex", params={"locale": locale})
            ).status_code == 404

    # Publishing is simulated only inside the isolated test database. A second
    # identical import must neither duplicate articles nor append revisions.
    async with database() as session:
        published = await apply_import(
            session, actor, await plan_import(session, packs), publish=True
        )
        assert published.failed is None and len(published.published) == 305
        assert len(published.unchanged) == 305
        before_repeat = await counts(session)
        repeated = await apply_import(
            session, actor, await plan_import(session, packs), publish=True
        )
        assert repeated.failed is None and len(repeated.unchanged) == 305
        assert repeated.created == repeated.updated == repeated.published == []
        assert await counts(session) == before_repeat
        final_ids = dict((await session.execute(select(GuideArticle.slug, GuideArticle.id))).all())
        assert all(final_ids[slug] == id_ for slug, id_ in identities.items())
        assert (
            await session.execute(
                select(
                    GuideArticleLocale.id,
                    GuideArticleLocale.version,
                    GuideArticleLocale.published_version,
                    GuideArticleLocale.draft_json,
                ).where(GuideArticleLocale.article_id == identities["unrelated-local-article"])
            )
        ).one() == control

    async with guides.client(guides.make_app(database)) as api:
        for locale in ["zh-TW", "zh-CN", "en", "ja", "ko"]:
            directory_response = await api.get("/guides/series/codex", params={"locale": locale})
            assert directory_response.status_code == 200
            assert {entry["slug"] for entry in directory_response.json()["entries"]} == (
                slugs - {"codex-learning-hub"}
            )
            for pack in packs:
                response = await api.get(f"/guides/life/{pack.slug}", params={"locale": locale})
                assert response.status_code == 200
                body = response.json()
                assert body["status"] == "published"
                assert set(body["published_locales"]) == set(pack.locales)
                assert body["document"]["title"] == pack.locales[locale].title
                assert [
                    (block["language"], block["code"])
                    for block in body["document"]["blocks"]
                    if block["type"] == "code"
                ] == [
                    (block.language, block.code)
                    for block in pack.locales[locale].blocks
                    if block.type == "code"
                ]


def document(block):
    return GuideDocument.model_validate({"title": "Test", "description": "Test", "blocks": [block]})


def test_code_preserves_markup_whitespace_and_line_endings():
    code = "<script>alert(1)</script>\r\n\tvalue = 1\n"
    parsed = document({"type": "code", "language": "html", "label": "HTML", "code": code})
    assert parsed.blocks[0].code == code


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "data:text/html,test",
        "https://u:p@example.com",
        "//example.com",
        "https://example.com/\n",
    ],
)
def test_inline_links_reject_unsafe_destinations(url):
    with pytest.raises(ValidationError):
        document(
            {"type": "rich_paragraph", "inlines": [{"type": "link", "text": "Read", "url": url}]}
        )


def test_inline_spacing_and_legacy_paragraphs():
    block = {
        "type": "rich_paragraph",
        "inlines": [
            {"type": "text", "text": "Read "},
            {"type": "link", "text": "more", "url": "https://example.com"},
            {"type": "text", "text": " here."},
        ],
    }
    assert "".join(span.text for span in document(block).blocks[0].inlines) == "Read more here."
    assert (
        document({"type": "paragraph", "text": "[literal](url)"}).blocks[0].text == "[literal](url)"
    )


def test_ready_lessons_have_five_locales_valid_images_and_existing_links():
    catalog = json.loads(
        (ROOT / "apps/web/lib/codex-learning/catalog.json").read_text(encoding="utf-8")
    )
    assert len(catalog) == 60
    assert [row["id"] for row in catalog] == list(range(1, 61))
    assert sorted(row["order"] for row in catalog) == list(range(1, 61))
    assert all(sum(row["unit"] == unit for row in catalog) == 6 for unit in "ABCDEFGHIJ")
    # Platform alternatives must be usable without completing a different OS.
    by_id = {row["id"]: row for row in catalog}
    assert all(by_id[id_]["prerequisites"] == [5] for id_ in [35, 36, 37])
    assert all(by_id[id_]["prerequisites"] == [4] for id_ in [38, 39])
    assert 40 not in by_id[15]["prerequisites"]  # Cloud does not require mobile pairing.
    known = {row["slug"] for row in catalog} | {"codex-learning-hub"}
    for row in catalog:
        if not row["ready"]:
            assert not (ROOT / f"apps/api/app/guides/content/{row['slug']}.json").exists()
        assert all(
            any(prereq["id"] == id_ and prereq["order"] < row["order"] for prereq in catalog)
            for id_ in row["prerequisites"]
        )
    ready = {row["slug"] for row in catalog if row["ready"]} | {"codex-learning-hub"}
    locales = {"zh-TW", "zh-CN", "en", "ja", "ko"}
    for slug in ready:
        path = ROOT / f"apps/api/app/guides/content/{slug}.json"
        pack = ArticlePack.model_validate_json(path.read_text(encoding="utf-8"))
        assert set(pack.locales) == locales
        for locale, doc in pack.locales.items():
            assert doc.sources and all(source.checked_on for source in doc.sources)
            assert doc.hero and (ROOT / "apps/web/public" / doc.hero.src.lstrip("/")).is_file()
            assert len([block for block in doc.blocks if block.type == "heading"]) >= 3
            for block in doc.blocks:
                if block.type == "image":
                    assert (ROOT / "apps/web/public" / block.src.lstrip("/")).is_file()
                if block.type == "rich_paragraph":
                    assert all(
                        node.slug in known for node in block.inlines if node.type == "article"
                    )
                links = (
                    [block.url]
                    if block.type == "link"
                    else [span.url for span in block.inlines if span.type == "link"]
                    if block.type == "rich_paragraph"
                    else []
                )
                for url in links:
                    if url.startswith("https://mokaair.com/"):
                        if url.startswith("https://mokaair.com/guides/"):
                            asset = url.removeprefix("https://mokaair.com/")
                            assert asset in {
                                "guides/codex-first-project/todo-practice.zip",
                                "guides/codex-skills/todo-acceptance.zip",
                                "guides/codex-skill-resources/todo-summary-practice.zip",
                                "guides/codex-csv-workshop/contacts-practice.zip",
                            }
                            assert (ROOT / "apps/web/public" / asset).is_file()
                            continue
                        assert url.startswith(f"https://mokaair.com/{locale}/life/")
                        # References may name planned lessons; the publication-aware
                        # renderer makes those references inert until actually public.
                        assert url.rsplit("/", 1)[-1] in known


def test_deep_drafts_preserve_code_sources_and_structures_across_locales():
    catalog = json.loads(
        (ROOT / "apps/web/lib/codex-learning/catalog.json").read_text(encoding="utf-8")
    )
    for slug in [row["slug"] for row in catalog if row["deepDraft"]]:
        pack = ArticlePack.model_validate_json(
            (ROOT / f"apps/api/app/guides/content/{slug}.json").read_text(encoding="utf-8")
        )
        reference = pack.locales["zh-TW"]
        for document in pack.locales.values():
            assert [
                "prose" if block.type in {"paragraph", "rich_paragraph"} else block.type
                for block in document.blocks
            ] == [
                "prose" if block.type in {"paragraph", "rich_paragraph"} else block.type
                for block in reference.blocks
            ]
            assert [
                (block.language, block.code) for block in document.blocks if block.type == "code"
            ] == [
                (block.language, block.code) for block in reference.blocks if block.type == "code"
            ]
            assert document.sources == reference.sources
            body = [block for block in document.blocks if block.type != "image"]
            assert body[0].type == body[-1].type == "rich_paragraph"
            assert body[0].inlines[0].slug == body[-1].inlines[0].slug == "codex-learning-hub"
        if slug == "codex-skills":
            sample = (
                ROOT / "docs/codex-learning/practice/skills/todo-acceptance/SKILL.md"
            ).read_text(encoding="utf-8")
            assert (
                next(
                    block.code
                    for block in reference.blocks
                    if block.type == "code" and block.language == "markdown"
                )
                == sample
            )
