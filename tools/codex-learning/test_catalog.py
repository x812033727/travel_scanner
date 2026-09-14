"""A catalogue rebuild must not rewrite the independently authored hub."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class CatalogTests(unittest.TestCase):
    def test_rebuild_preserves_authored_hub_and_does_not_require_one(self):
        for has_hub in (True, False):
            with self.subTest(has_hub=has_hub), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                for relative in (
                    "tools/codex-learning/expand-catalog.py",
                    "apps/web/lib/codex-learning/catalog.json",
                    "docs/codex-learning/deep/planned.json",
                    "docs/codex-learning/depth-plan.md",
                    "docs/codex-learning/deep/sources.json",
                ):
                    destination = root / relative
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(ROOT / relative, destination)
                hub = root / "apps/api/app/guides/content/codex-learning-hub.json"
                # A legitimate two-row authored table must neither be relabelled
                # as three curriculum batches nor make a catalogue rebuild fail.
                authored = json.dumps({"locales": {locale: {
                    "description": f"Edited description: {locale}",
                    "blocks": [
                        {"type": "paragraph", "text": f"Edited introduction: {locale}"},
                        {"type": "table", "headers": ["Path", "Outcome"],
                         "rows": [["CLI", "Run a task"], ["MD", "Set project rules"]]},
                    ],
                } for locale in ("zh-TW", "zh-CN", "en", "ja", "ko")}}, indent=2).encode()
                if has_hub:
                    hub.parent.mkdir(parents=True)
                    hub.write_bytes(authored)
                script = root / "tools/codex-learning/expand-catalog.py"
                result = subprocess.run([sys.executable, str(script)], cwd=root, capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                catalog = json.loads((root / "apps/web/lib/codex-learning/catalog.json").read_text(encoding="utf-8"))
                self.assertEqual(sorted(row["id"] for row in catalog), list(range(1, 61)))
                self.assertEqual(sorted(row["order"] for row in catalog), list(range(1, 61)))
                if has_hub:
                    self.assertEqual(hub.read_bytes(), authored)
                else:
                    self.assertFalse(hub.exists())


if __name__ == "__main__":
    unittest.main()
