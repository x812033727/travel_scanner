"""Regression checks for evidence drift, missing files and unsafe evidence paths."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "audit_readiness", Path(__file__).with_name("audit-readiness.py")
)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class EvidenceChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.file = self.root / "example.md"
        self.file.write_bytes(b"reviewed\n")
        self.expected = audit.digest(self.file)

    def test_nested_and_duplicate_receipt_entries(self):
        receipt = {"articles": [{"files": [{"path": "example.md", "sha256": self.expected}]}],
                   "followup": {"file": "example.md", "sha256": self.expected}}
        rows = audit.verify_references(self.root, audit.references(receipt))
        self.assertEqual(len(rows), 1)

    def test_modified_bytes_fail(self):
        self.file.write_bytes(b"changed\n")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            audit.verify_references(self.root, [("example.md", self.expected)])

    def test_line_endings_are_not_silently_normalized(self):
        self.file.write_bytes(b"reviewed\r\n")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            audit.verify_references(self.root, [("example.md", self.expected)])

    def test_missing_file_fails(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            audit.verify_references(self.root, [("missing.md", self.expected)])

    def test_escape_and_absolute_paths_fail(self):
        for name in ["../outside.md", str(self.file.resolve()), "folder\\file.md"]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                audit.safe_file(self.root, name)

    def test_empty_receipt_is_not_passed(self):
        with self.assertRaisesRegex(ValueError, "no hashed files"):
            audit.verify_references(self.root, [])

    def test_visual_receipt_source_hash(self):
        rows = list(audit.references({"source": "example.md", "sourceSha256": self.expected}))
        self.assertEqual(audit.verify_references(self.root, rows)[0]["sha256"], self.expected)


if __name__ == "__main__":
    unittest.main()
