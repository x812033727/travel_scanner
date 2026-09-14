"""Focused authoring guarantees, separate from the API's runtime dependencies."""
import importlib.util
from pathlib import Path
import unittest
import json
import tempfile
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("depth", Path(__file__).with_name("build-depth.py"))
depth = importlib.util.module_from_spec(spec)
spec.loader.exec_module(depth)


class CompilerTests(unittest.TestCase):
    def test_nested_markdown_fences_preserve_literal_code_in_all_locales(self):
        author_spec = importlib.util.spec_from_file_location("authors", Path(__file__).with_name("render-authors.py"))
        authors = importlib.util.module_from_spec(author_spec)
        author_spec.loader.exec_module(authors)
        sample = "## 專案規則\n\n```text\n繁體內容不得翻譯\n```\n"
        bodies = authors.render({"id": 9, "blocks": [{"type": "code", "language": "markdown", "code": sample}]})
        for locale, body in bodies.items():
            code = [block for block in depth.compile_body(body, locale) if block["type"] == "code"]
            self.assertEqual(code, [{"type": "code", "language": "markdown", "code": sample}])
        simplified = depth.compile_body(depth.simplified(bodies["zh-TW"]), "zh-CN")
        self.assertEqual(next(block["code"] for block in simplified if block["type"] == "code"), sample)
        self.assertIn("繁體", depth.simplified("~~~text\n繁體\n~~~\n"))
        with self.assertRaisesRegex(ValueError, "Unclosed"):
            depth.simplified("```text\n未結束\n")

    def test_check_rejects_stale_pack_without_replacing_it(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            authors, packs = root / "authors", root / "packs"
            authors.mkdir()
            packs.mkdir()
            catalog = root / "catalog.json"
            catalog.write_text(json.dumps([{"id": 1, "slug": "codex-example"}]), encoding="utf-8")
            (authors / "sources.json").write_text('{"01": []}', encoding="utf-8")
            original = json.dumps({"locales": {locale: {"blocks": []} for locale in ["zh-TW", "zh-CN", "en", "ja", "ko"]}})
            pack = packs / "codex-example.json"
            pack.write_text(original, encoding="utf-8")
            for locale in ["zh-TW", "en", "ja", "ko"]:
                (authors / locale).mkdir()
                (authors / locale / "01.md").write_text("## Updated\n\nA changed instruction.\n", encoding="utf-8")
            with patch.multiple(depth, ROOT=root, AUTHORS=authors, PACKS=packs, CATALOG=catalog), patch("sys.argv", ["build-depth.py", "--check"]):
                with self.assertRaisesRegex(ValueError, "Stale compiled packs"):
                    depth.main()
            self.assertEqual(pack.read_text(encoding="utf-8"), original)
            self.assertFalse((authors / "build-report.json").exists())

    def test_late_invalid_article_does_not_replace_earlier_pack(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            authors, packs = root / "authors", root / "packs"
            authors.mkdir()
            packs.mkdir()
            rows = [{"id": id_, "slug": f"codex-example-{id_}"} for id_ in [1, 2]]
            catalog = root / "catalog.json"
            catalog.write_text(json.dumps(rows), encoding="utf-8")
            (authors / "sources.json").write_text(json.dumps({"01": [], "02": []}), encoding="utf-8")
            originals = {}
            for row in rows:
                originals[row["slug"]] = json.dumps({"locales": {locale: {"blocks": []} for locale in ["zh-TW", "zh-CN", "en", "ja", "ko"]}})
                (packs / f'{row["slug"]}.json').write_text(originals[row["slug"]], encoding="utf-8")
            for locale in ["zh-TW", "en", "ja", "ko"]:
                (authors / locale).mkdir()
                (authors / locale / "01.md").write_text("## Valid\n\nA complete draft.\n", encoding="utf-8")
                (authors / locale / "02.md").write_text("<script>not allowed</script>\n", encoding="utf-8")
            with patch.multiple(depth, ROOT=root, AUTHORS=authors, PACKS=packs, CATALOG=catalog), patch("sys.argv", ["build-depth.py"]):
                with self.assertRaises(ValueError):
                    depth.main()
            for slug, original in originals.items():
                self.assertEqual((packs / f"{slug}.json").read_text(encoding="utf-8"), original)
            self.assertFalse((authors / "build-report.json").exists())

    def test_locale_links_and_spaces(self):
        blocks = depth.compile_body("Read [plan](article:codex-plan-mode) now.\n\n[Back](article:codex-learning-hub)\n", "ja")
        self.assertEqual(blocks[0]["spans"], [
            {"type": "text", "text": "Read "},
            {"type": "link", "text": "plan", "url": "https://mokaair.com/ja/life/codex-plan-mode"},
            {"type": "text", "text": " now."},
        ])
        self.assertEqual(blocks[1]["type"], "link")

    def test_translation_preserves_exact_code(self):
        body = "## 設定\n\n```markdown 寫入規則\n\t繁體檔案 `x`\n\n$HOME\n```\n"
        translated = depth.simplified(body)
        self.assertIn("写入规则", translated)
        self.assertEqual(depth.compile_body(body, "zh-TW")[-1], depth.compile_body(translated, "zh-CN")[-1])
        self.assertEqual(depth.compile_body(body, "en")[-1]["code"], "\t繁體檔案 `x`\n\n$HOME\n")

    def test_rejects_unsupported_content_instead_of_silently_dropping_it(self):
        for body in ["<script>alert(1)</script>\n", "# A second page title\n", "- Parent\n  - Nested\n", "[Bad](article:../../admin)"]:
            with self.subTest(body=body), self.assertRaises(ValueError):
                depth.compile_body(body, "en")

    def test_table_callout_and_inert_code(self):
        blocks = depth.compile_body("| A | B |\n| --- | --- |\n| 1 | 2 |\n\n> Note\n\n```html\n<script>x()</script>\n```\n", "en")
        self.assertEqual(blocks[0]["rows"], [["1", "2"]])
        self.assertEqual(blocks[1]["type"], "callout")
        self.assertEqual(blocks[2]["code"], "<script>x()</script>\n")


if __name__ == "__main__":
    unittest.main()
