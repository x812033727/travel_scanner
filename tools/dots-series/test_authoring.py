"""Dependency-free authoring contract tests; these are not dots demonstration proof."""
import unittest

from authoring import parse_markdown

FOOTER = "\n## 官方來源\n- [Dots](https://learn.chatgpt.com/docs/dots)\n查核日期：2026-10-03。\n"
BASE = "# Dots 教學\n\n本課說明完成工作的操作。\n\n"


class AuthoringTests(unittest.TestCase):
    def test_copy_label_preserves_multiline_prompt_and_source_is_metadata(self):
        document = parse_markdown(BASE + "## 實作\n\n```text 在 dots 對話輸入\n請整理待辦。\n先不要傳送。\n```\n" + FOOTER)
        code = next(block for block in document["blocks"] if block["type"] == "code")
        self.assertEqual(code, {"type": "code", "language": "text", "label": "在 dots 對話輸入", "code": "請整理待辦。\n先不要傳送。\n"})
        self.assertEqual(document["sources"], [{"title": "Dots", "url": "https://learn.chatgpt.com/docs/dots", "checked_on": "2026-10-03"}])
        self.assertFalse(any("官方來源" == block.get("text") for block in document["blocks"]))

    def test_article_reference_uses_publication_aware_inline(self):
        document = parse_markdown(BASE + "閱讀 [第三課](https://mokaair.com/zh-TW/life/dots-lesson-03)，查看 `Activity`。\n" + FOOTER)
        block = document["blocks"][1]
        self.assertEqual([node["type"] for node in block["inlines"]], ["text", "article", "text", "code", "text"])
        self.assertEqual(block["inlines"][1]["slug"], "dots-lesson-03")

    def test_tables_lists_and_callouts_preserve_authored_values(self):
        document = parse_markdown(BASE + "## 檢查\n\n| 項目 | 結果 |\n| --- | --- |\n| 數量 | 2 |\n\n1. **開啟工作。**\n2. 檢查結果。\n\n> 不要傳送。\n" + FOOTER)
        table = next(block for block in document["blocks"] if block["type"] == "table")
        self.assertEqual(table["rows"], [["數量", "2"]])
        self.assertEqual(next(block for block in document["blocks"] if block["type"] == "list")["items"][0], "開啟工作。")

    def test_table_cells_are_plain_labels_and_relative_article_links_are_resolvable(self):
        document = parse_markdown(BASE + "## 目錄\n\n| 課次 | 名稱 |\n| --- | --- |\n| [01](/zh-TW/life/dots-lesson-01) | `Activity` |\n\n[第一課](/zh-TW/life/dots-lesson-01)\n" + FOOTER)
        table = next(block for block in document["blocks"] if block["type"] == "table")
        self.assertEqual(table["rows"], [["01", "Activity"]])
        paragraph = next(block for block in document["blocks"] if block["type"] == "rich_paragraph")
        self.assertEqual(paragraph["inlines"], [{"type": "article", "kind": "life", "slug": "dots-lesson-01", "text": "第一課"}])

    def test_missing_ambiguous_duplicate_source_dates_fail(self):
        bad = ["## 官方來源\n- [Dots](https://learn.chatgpt.com/docs/dots)\n",
               "## 官方來源\n- [Dots](https://learn.chatgpt.com/docs/dots)\n2026-10-03\n2026-10-04\n",
               "## 官方來源\n- [Dots](https://learn.chatgpt.com/docs/dots) 2026-10-03\n- [Dots](https://learn.chatgpt.com/docs/dots) 2026-10-03\n"]
        for footer in bad:
            with self.subTest(footer=footer), self.assertRaises(ValueError):
                parse_markdown(BASE + footer)

    def test_unlabelled_unclosed_and_unsupported_constructs_fail(self):
        for body in ("```text\n請整理\n```", "```text 在 dots 輸入\n請整理", "<script>alert(1)</script>", "![截圖](/bad.png)"):
            with self.subTest(body=body), self.assertRaises(ValueError):
                parse_markdown(BASE + body + FOOTER)

    def test_source_section_must_be_last(self):
        with self.assertRaisesRegex(ValueError, "final section"):
            parse_markdown(BASE + FOOTER + "## 還有一段\n錯置內容。\n")

    def test_instruction_heading_mentioning_sources_is_not_a_source_footer(self):
        document = parse_markdown(BASE + "## 教學期待結果：用來源驗收第一版\n\n請核對來源。\n" + FOOTER)
        self.assertTrue(any(block.get("text") == "教學期待結果：用來源驗收第一版" for block in document["blocks"]))

    def test_only_explicit_authored_summary_is_converted(self):
        document = parse_markdown(BASE + ":::summary\n- 本課整理工作。\n- 逐步核對結果。\n:::\n\n## 操作\n完成練習。\n" + FOOTER)
        self.assertEqual(document["blocks"][0]["type"], "paragraph")
        self.assertEqual(document["blocks"][1], {"type": "summary", "items": ["本課整理工作。", "逐步核對結果。"]})


if __name__ == "__main__":
    unittest.main()
