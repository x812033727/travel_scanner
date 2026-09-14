"""Real compiler tests with synthetic, temporary authoring inputs; no published content."""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
HERE = ROOT / "docs/gemini-series"
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location("gemini_build", HERE / "build.py")
assert spec and spec.loader
compiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)

SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900"><title>合成測試圖</title><desc>只供建置測試</desc><rect width="1600" height="900" fill="#fff"/><text x="100" y="150" font-size="60">合成測試圖</text></svg>'
LONG_TEXT = "這是隔離環境的合成測試資料，只用來驗證文字長度與格式，不是正式教學內容。" * 55


class AuthoringTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="gemini-build-test-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.content = self.directory / "content"
        self.track = self.content / "md"
        self.output = self.directory / "output"
        examples = self.track / "examples"
        examples.mkdir(parents=True)
        (examples / "rules.toml").write_text('prompt = """保留中文字與 <script>literal</script>"""\n', encoding="utf-8")
        with zipfile.ZipFile(examples / "exercise.zip", "w") as archive:
            archive.writestr("README.md", "Synthetic exercise fixture.")
        self.create_lesson(69)

    def create_lesson(self, number):
        lesson = self.track / str(number)
        lesson.mkdir(parents=True)
        sections = [
            "這是隔離的編譯測試，所有內容與素材都只供測試。",
            "## 學完成果", LONG_TEXT,
            "## 操作步驟", "先讀 [[36#section-3|GEMINI.md 指示]] 再建立範例。",
            "!include-code examples/rules.toml",
            "| 案例 | 結果 |\n| --- | --- |\n| 合成輸入 | 文字不執行 |",
            "> 這是故意製作的測試資料。",
            "## 常見問題", "### 第一題", "合成答案一。", "### 第二題", "合成答案二。", "### 第三題", "合成答案三。",
        ]
        manuscript = "\n\n".join(sections) + "\n"
        (lesson / "lesson.md").write_text(manuscript, encoding="utf-8")
        meta = {"hero_alt": "測試封面", "diagram_alt": "測試流程", "diagram_caption": "合成圖，只供測試",
                "sources": [{"title": "Gemini CLI", "url": "https://geminicli.com/docs/cli/gemini-md/", "checked_on": "2026-09-14"}],
                "downloads": [{"source": "examples/exercise.zip", "filename": "practice.zip", "text": "下載合成練習"}]}
        (lesson / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
        for name in ["hero.svg", "diagram-1.svg"]:
            (lesson / name).write_text(SVG, encoding="utf-8")
        Image.new("RGB", (1600, 900), "white").save(lesson / "hero.jpg", "JPEG")

    def build(self, numbers=None):
        return compiler.build_advanced("md", numbers or [69], self.content, self.output, False)

    def test_selected_build_preserves_runtime_and_embeds_literal_toml(self):
        original = compiler.CATALOGUE_PATH.read_bytes()
        result = self.build()
        self.assertEqual(result[0]["status"], "built-unpublished")
        slug = result[0]["slug"]
        pack = json.loads((self.output / "apps/api/app/guides/content" / (slug + ".json")).read_text(encoding="utf-8"))
        blocks = pack["locales"]["zh-TW"]["blocks"]
        literal = next(b for b in blocks if b["type"] == "code")
        self.assertEqual(literal["language"], "toml")
        self.assertIn("<script>literal</script>", literal["code"])
        linked = next(b for b in blocks if b["type"] == "rich_paragraph")
        self.assertTrue(any(n.get("url", "").endswith("#section-3") for n in linked["inlines"]))
        self.assertEqual(next(b for b in blocks if b["type"] == "table")["rows"], [["合成輸入", "文字不執行"]])
        download = self.output / "apps/web/public/guides" / slug / "practice.zip"
        self.assertEqual(download.read_bytes(), (self.track / "examples/exercise.zip").read_bytes())
        self.assertEqual(compiler.CATALOGUE_PATH.read_bytes(), original)
        self.assertFalse((self.output / "apps/web/lib/guide-series.json").exists())

    def test_bad_second_lesson_does_not_write_first(self):
        self.create_lesson(70)
        (self.track / "70/lesson.md").write_text("不完整。", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.build([69, 70])
        self.assertFalse(self.output.exists())

    def test_numbers_cannot_escape_track_or_repeat(self):
        for numbers in [[51], [69, 69]]:
            with self.assertRaises(ValueError):
                self.build(numbers)
        self.assertFalse(self.output.exists())

    def test_includes_and_downloads_cannot_escape_examples(self):
        with self.assertRaisesRegex(ValueError, "inside examples"):
            compiler.parse("!include-code ../outside.py", base_dir=self.track)
        meta_file = self.track / "69/meta.json"
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        meta["downloads"][0]["filename"] = "../../outside.zip"
        meta_file.write_text(json.dumps(meta), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "filenames"):
            self.build()
        self.assertFalse(self.output.exists())

    def test_active_svg_is_rejected_before_rendering(self):
        (self.track / "69/hero.svg").write_text(SVG.replace("<svg ", '<svg onload="alert(1)" '), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "active SVG"):
            self.build()
        self.assertFalse(self.output.exists())

    def test_three_faqs_and_body_length_are_enforced(self):
        file = self.track / "69/lesson.md"
        original = file.read_text(encoding="utf-8")
        file.write_text(original.replace("### 第三題", "第三題"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "three FAQ"):
            self.build()
        file.write_text(original.replace(LONG_TEXT, "太短。"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "body characters"):
            self.build()
        self.assertFalse(self.output.exists())

    def test_missing_or_wrong_hero_does_not_write_pack(self):
        hero = self.track / "69/hero.jpg"
        hero.unlink()
        with self.assertRaisesRegex(ValueError, "--render"):
            self.build()
        Image.new("RGB", (80, 80), "white").save(hero, "JPEG")
        with self.assertRaisesRegex(ValueError, "1600"):
            self.build()
        self.assertFalse(self.output.exists())

    def test_original_lesson_rebuild_matches_reviewed_pack(self):
        original = compiler.CATALOGUE_PATH.read_bytes()
        result = compiler.build(36, False, self.output)
        expected = json.loads((ROOT / "apps/api/app/guides/content" / (result["slug"] + ".json")).read_text(encoding="utf-8"))
        rebuilt = json.loads((self.output / "apps/api/app/guides/content" / (result["slug"] + ".json")).read_text(encoding="utf-8"))
        self.assertEqual(rebuilt, expected)
        self.assertEqual(compiler.CATALOGUE_PATH.read_bytes(), original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
