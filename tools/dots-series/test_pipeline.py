"""API-dependent compile/publication tests. Run with the API virtual environment."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.guides.schemas import ArticleReference, GuideDocument
from app.guides.series import article_navigation, catalogues, public_series
from build import build, compile_course
from files import contained, digest
from package import package
from PIL import Image
from test_paths import directory_link, forbid_outside_reads, remove_directory_link


class CompileTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="dots-compile-")
        self.addCleanup(self.directory.cleanup)
        self.workspace = Path(self.directory.name)
        for number in range(1, 17):
            lesson = self.workspace / "lessons" / f"{number:02}.md"
            lesson.parent.mkdir(parents=True, exist_ok=True)
            lesson.write_text(f"# 教學 {number}\n\n這是編譯測試資料，不能當作實機操作證據。\n\n## 準備\n\n> 本段是測試。\n\n## 操作\n\n```text 在 dots 對話輸入\n請整理待辦。\n```\n\n| 項目 | 結果 |\n| --- | --- |\n| 測試 | 合成資料 |\n\n## 完成檢查\n\n- 開啟結果\n\n## 官方來源\n\n- [Dots](https://learn.chatgpt.com/docs/dots)\n\n查核日期：2026-10-03。\n", encoding="utf-8")
        for slug in [f"dots-lesson-{number:02}" for number in range(1, 17)] + ["dots-guide"]:
            path = self.workspace / "assets/guides" / slug / "hero.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (1600, 900), "#faf5eb").save(path)
        for number in range(11, 17):
            example = self.workspace / "examples" / str(number)
            example.mkdir(parents=True)
            (example / "input-v1.txt").write_text("test input", encoding="utf-8")
            (example / "change-v2.txt").write_text("test change", encoding="utf-8")
        package(self.workspace)

    def test_existing_schema_and_lint_compile_exactly_seventeen_drafts(self):
        packs, assets, warnings = compile_course(self.workspace)
        self.assertEqual(len(packs), 17)
        self.assertTrue(len(assets) >= 17)
        self.assertTrue(warnings)  # Warnings are reported rather than called publication.
        self.assertTrue(all(pack["kind"] == "life" and list(pack["locales"]) == ["zh-TW"] for pack in packs.values()))
        self.assertEqual(packs["dots-lesson-03"]["display_order"], 603)
        self.assertEqual(packs["dots-guide"]["display_order"], 599)
        report = build(self.workspace)
        self.assertFalse(report["installed"])
        self.assertFalse(report["published"])
        self.assertEqual(report["state"], "draft")
        manifest_path = self.workspace / "build/build-manifest.json"
        self.assertNotIn(b"\r", manifest_path.read_bytes())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for entry in manifest["files"]:
            output = self.workspace / "build" / entry["path"]
            self.assertEqual(digest(output), entry["sha256"])
            if output.suffix in {".json", ".svg"}:
                self.assertNotIn(b"\r", output.read_bytes())

    def test_missing_authored_lesson_and_bad_schema_fail_before_output(self):
        source = self.workspace / "lessons/16.md"
        original = source.read_text(encoding="utf-8")
        source.unlink()
        with self.assertRaisesRegex(ValueError, "Missing authored lesson"):
            build(self.workspace)
        self.assertFalse((self.workspace / "build").exists())
        source.write_text(original.replace("text 在 dots", "invalid-language 在 dots"), encoding="utf-8")
        with self.assertRaises(ValueError):
            build(self.workspace)
        self.assertFalse((self.workspace / "build").exists())

    def test_pilot_build_reads_only_selected_lessons_without_creating_a_full_release(self):
        (self.workspace / "lessons/16.md").unlink()
        report = build(self.workspace, selected=[2, 3])
        self.assertEqual(report["articles"], 2)
        self.assertEqual(Path(report["output"]).name, "build-pilot")
        self.assertFalse((self.workspace / "build").exists())

    def test_practice_archive_is_deterministic_and_distinct_from_media(self):
        original = (self.workspace / "assets/dots-course/downloads/lesson-11.zip").read_bytes()
        report = package(self.workspace)
        self.assertEqual(original, (self.workspace / "assets/dots-course/downloads/lesson-11.zip").read_bytes())
        self.assertFalse(report["media_generated"])
        self.assertTrue(all(item["state"] == "synthetic-practice-input" for item in report["downloads"]))
    def test_missing_download_and_unknown_article_links_fail(self):
        path = self.workspace / "lessons/11.md"
        original = path.read_text(encoding="utf-8")
        path.write_text(original.replace("## 完成檢查", "[下載](https://mokaair.com/dots-course/downloads/missing.zip)\n\n## 完成檢查"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Missing public asset"):
            compile_course(self.workspace)
        path.write_text(original.replace("## 完成檢查", "[缺失文章](article:unknown-dots-course-target)\n\n## 完成檢查"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unknown course article"):
            compile_course(self.workspace)


class PublicationTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_series_join_excludes_withdrawn_lesson_hub_and_other_locale(self):
        catalogue = next(item for item in catalogues() if item.slug == "dots")
        visible = {catalogue.hub, *[entry.slug for entry in catalogue.entries]}

        async def published(_session, locale, targets):
            return {slug: (ArticleReference(kind="life", slug=slug, title="Published " + slug),
                           GuideDocument(title="Published " + slug, description="Live title and body", blocks=[{"type": "paragraph", "text": "Published body"}]))
                    for _kind, slug in targets if slug in visible and locale == "zh-TW"}

        with patch("app.guides.series.published_documents", published):
            series = await public_series(None, "dots", "zh-TW")
            self.assertEqual(len(series.entries), 16)
            self.assertTrue(all(entry.title.startswith("Published ") for entry in series.entries))
            visible.remove("dots-lesson-03")
            series = await public_series(None, "dots", "zh-TW")
            self.assertNotIn("dots-lesson-03", [entry.slug for entry in series.entries])
            self.assertTrue(all("dots-lesson-03" not in route.slugs for route in series.paths))
            navigation = await article_navigation(None, "life", "dots-lesson-02", "zh-TW")
            self.assertEqual(navigation.next.slug, "dots-lesson-04")
            self.assertIsNone(await article_navigation(None, "life", "dots-lesson-03", "zh-TW"))
            self.assertIsNone(await public_series(None, "dots", "en"))
            visible.remove(catalogue.hub)
            self.assertIsNone(await public_series(None, "dots", "zh-TW"))
            self.assertIsNone(await article_navigation(None, "life", "dots-lesson-02", "zh-TW"))


class CompilerBoundaryTests(unittest.TestCase):
    def setUp(self):
        fixture = CompileTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.workspace = fixture.workspace
        separate = tempfile.TemporaryDirectory(prefix="dots-compile-boundary-")
        self.addCleanup(separate.cleanup)
        self.base = Path(separate.name)
        self.repo, self.outside = self.base / "repo", self.base / "outside"
        self.outside.mkdir()
        catalogue = self.repo / "apps/api/app/guides/series_data/dots.json"
        catalogue.parent.mkdir(parents=True)
        shutil.copyfile(Path(__file__).resolve().parents[2] / "apps/api/app/guides/series_data/dots.json", catalogue)

    def test_linked_authoring_root_is_rejected_without_reading_outside_sources(self):
        (self.outside / "01.md").write_text("outside source must not be read", encoding="utf-8")
        original = self.workspace / "lessons"
        contained(original, self.workspace)
        shutil.rmtree(original)
        directory_link(self, self.outside, original)
        with forbid_outside_reads(self.outside), self.assertRaisesRegex(ValueError, "escapes allowed workspace"):
            build(self.workspace, repo=self.repo, install=True)
        self.assertFalse((self.workspace / "build").exists())
        self.assertFalse((self.repo / "apps/api/app/guides/content").exists())

    def test_build_pilot_assets_and_repo_install_roots_are_checked_before_any_output(self):
        roots = [self.workspace / "build", self.workspace / "build-pilot", self.workspace / "build/content",
                 self.workspace / "build/web-public", self.repo / "apps/api/app/guides/content", self.repo / "apps/web/public"]
        for index, link in enumerate(roots):
            with self.subTest(link=link):
                external = self.outside / str(index)
                external.mkdir()
                directory_link(self, external, link)
                try:
                    selected = [2, 3] if link.name == "build-pilot" else None
                    with self.assertRaisesRegex(ValueError, "escapes allowed workspace"):
                        build(self.workspace, repo=self.repo, install=True, selected=selected)
                    self.assertFalse(list(external.rglob("*")))
                    self.assertFalse(list((self.workspace / "build").rglob("*.json")))
                    self.assertFalse(list((self.repo / "apps/api/app/guides/content").rglob("*.json")))
                finally:
                    remove_directory_link(link)

    def test_external_asset_root_cannot_be_read_or_silently_fall_back(self):
        original = self.workspace / "assets"
        contained(original, self.workspace)
        shutil.rmtree(original)
        directory_link(self, self.outside, original)
        with forbid_outside_reads(self.outside), self.assertRaisesRegex(ValueError, "escapes allowed workspace"):
            build(self.workspace, repo=self.repo)
        self.assertFalse((self.workspace / "build").exists())

    def test_late_install_file_symlink_prevents_all_prior_pack_and_install_writes(self):
        destination = self.repo / "apps/api/app/guides/content/dots-lesson-16.json"
        destination.parent.mkdir(parents=True)
        target = self.outside / "escaped.json"
        try:
            destination.symlink_to(target)
        except OSError as error:
            self.skipTest(f"File symlink creation unavailable: {error}")
        with self.assertRaisesRegex(ValueError, "escapes allowed workspace"):
            build(self.workspace, repo=self.repo, install=True)
        self.assertFalse(target.exists())
        self.assertFalse((self.workspace / "build").exists())
        self.assertFalse((destination.parent / "dots-lesson-01.json").exists())


if __name__ == "__main__":
    unittest.main()
