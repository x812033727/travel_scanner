"""Recording packages use the existing helper without pretending media exists."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from authoring_kit import KIT_PATH, ROOT, authoring_kit
from files import digest


class AuthoringKitTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        base = Path(self.temporary.name)
        self.workspace, self.repo = base / "author", base / "checkout"
        self.workspace.mkdir()
        helper = self.repo / KIT_PATH
        helper.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / KIT_PATH, helper)
        catalogue = self.repo / "apps/api/app/guides/series_data/dots.json"
        catalogue.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / "apps/api/app/guides/series_data/dots.json", catalogue)
        content = self.repo / "apps/api/app/guides/content"
        content.mkdir()
        for directory in ("lessons", "videos", "examples"):
            (self.workspace / directory).mkdir()
        for number in range(17):
            (self.workspace / "lessons" / f"{number:02}.md").write_text(f"# 第{number}課\n\n作者原稿。\n", encoding="utf-8")
        for number in range(1, 17):
            (content / f"dots-lesson-{number:02}.json").write_text('{"kind":"life"}', encoding="utf-8")
            script = (f"---\ntitle: 第{number}課示範\nformat: screenshot-tutorial\nrecorded_on: null\n"
                      f"article: dots-lesson-{number:02}\nsummary: 看懂步驟。\n---\n"
                      "\n## 開場\n[截圖] 真實介面待擷取\n" + "請核對資料來源與限制。\n" * 5 +
                      "\n## 操作\n[截圖] 真實輸入待擷取\n" + "請核對資料來源與限制。\n" * 10 +
                      "\n## 完成\n[截圖] 真實結果待擷取\n" + "請核對資料來源與限制。\n" * 10 +
                      "\n## 來源\n- 官方文件 https://learn.chatgpt.com/docs/dots（2026-10-03確認）\n")
            (self.workspace / "videos" / f"{number:02}.md").write_text(script, encoding="utf-8")
        for number in range(11, 17):
            directory = self.workspace / "examples" / str(number)
            directory.mkdir()
            for filename in ("input-v1.md", "changed-v2.md"):
                (directory / filename).write_text("合成練習輸入。\n", encoding="utf-8")
        # Explicit Windows originals exercise normalization on Linux CI too.
        self.source_bytes = {}
        for path in self.workspace.rglob("*.md"):
            raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
            path.write_bytes(raw)
            self.source_bytes[path] = raw

    def test_real_helper_packages_are_estimated_and_bind_original_and_normalized_script(self):
        result = authoring_kit(self.workspace, repo=self.repo, install=True)
        self.assertEqual(len(result["entries"]), 16)
        self.assertFalse(result["published"])
        self.assertFalse(result["media_generated"])
        entry = result["entries"][2]
        directory = self.repo / "docs/videos/dots-lesson-03"
        self.assertEqual(entry["source_script_sha256"], digest(self.workspace / "videos/03.md"))
        self.assertEqual(entry["normalized_script_sha256"], digest(directory / "script.md"))
        self.assertNotEqual(entry["source_script_sha256"], entry["normalized_script_sha256"])
        normalized = (directory / "script.md").read_text(encoding="utf-8")
        self.assertIn("recorded_on:\n", normalized)
        self.assertNotIn("recorded_on: \n", normalized)
        self.assertIn("recorded_on: null\n", (self.workspace / "videos/03.md").read_text(encoding="utf-8"))
        self.assertIsNone(entry["video_url"])
        self.assertIsNone(entry["measured_final_seconds"])
        upload = (directory / "upload-draft.md").read_text(encoding="utf-8")
        self.assertIn("所有時間均為口播估計", upload)
        self.assertIn("預定網址（尚未公開）", upload)
        self.assertNotIn("錄製日期：null", upload)
        self.assertNotIn("[截圖]", (directory / "teleprompter.txt").read_text(encoding="utf-8"))
        self.assertEqual((self.repo / "docs/dots-series/lessons/00.md").read_bytes(),
                         (self.workspace / "lessons/00.md").read_bytes().replace(b"\r\n", b"\n"))
        self.assertFalse(list(directory.glob("*.srt")))
        self.assertFalse((directory / "chapters.txt").exists())
        manifest = json.loads((self.repo / "docs/dots-series/production-manifest.json").read_text(encoding="utf-8"))
        self.assertTrue(all(item["script_check_exit_code"] == 0 for item in manifest["entries"]))
        for path, raw in self.source_bytes.items():
            self.assertEqual(path.read_bytes(), raw, "external originals must retain their reviewed bytes")
        for item in manifest["files"]:
            output = self.repo / item["path"]
            self.assertNotIn(b"\r", output.read_bytes(), item["path"])
            self.assertEqual(digest(output), item["sha256"])
        for item in manifest["sources"]:
            self.assertEqual(digest(self.workspace / item["path"]), item["sha256"])
            if "output_path" in item:
                self.assertEqual(digest(self.repo / item["output_path"]), item["output_sha256"])
        self.assertEqual(entry["article_output_sha256"], digest(self.repo / "docs/dots-series/lessons/03.md"))
        self.assertNotEqual(entry["source_article_sha256"], entry["article_output_sha256"])
        self.assertNotIn(b"\r", (self.repo / "docs/dots-series/production-manifest.json").read_bytes())

        # Check actual index bytes under the real repository's LF attribute,
        # rather than just asserting that the same hashing helper agrees.
        git = shutil.which("git")
        if git is None:
            self.skipTest("Git is required to compare the staged representation")
        subprocess.run([git, "init", "--quiet", str(self.repo)], check=True, capture_output=True)
        (self.repo / ".gitattributes").write_bytes(b"* text=auto eol=lf\n")
        subprocess.run([git, "add", "docs"], cwd=self.repo, check=True, capture_output=True)
        indexed = ["docs/videos/dots-lesson-03/script.md", "docs/dots-series/lessons/03.md",
                   "docs/dots-series/examples/11/input-v1.md", "docs/dots-series/production-manifest.json"]
        for relative in indexed:
            staged = subprocess.run([git, "show", ":" + relative], cwd=self.repo, check=True, capture_output=True).stdout
            self.assertEqual(staged, (self.repo / relative).read_bytes(), relative)
            self.assertEqual(hashlib.sha256(staged).hexdigest(), digest(self.repo / relative))

    def test_missing_source_prevents_repo_installation(self):
        (self.workspace / "videos/16.md").unlink()
        with self.assertRaisesRegex(ValueError, "Missing or non-text"):
            authoring_kit(self.workspace, repo=self.repo, install=True)
        self.assertFalse((self.repo / "docs").exists())

    def test_bad_recording_script_blocks_all_repo_outputs(self):
        path = self.workspace / "videos/16.md"
        path.write_text(path.read_text(encoding="utf-8").split("## 操作")[0], encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "video_kit check failed"):
            authoring_kit(self.workspace, repo=self.repo, install=True)
        self.assertFalse((self.repo / "docs").exists())


if __name__ == "__main__":
    unittest.main()
