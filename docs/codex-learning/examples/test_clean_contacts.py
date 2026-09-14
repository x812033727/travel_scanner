import csv
import tempfile
import unittest
from pathlib import Path

from clean_contacts import clean


class CleanupTests(unittest.TestCase):
    def test_contract_and_input_preservation(self):
        original = (Path(__file__).parent / "contacts.csv").read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            target = Path(directory) / "output.csv"
            source.write_bytes(original)
            self.assertEqual(clean(source, target), {"kept": 2, "duplicate": 1, "invalid": 1})
            self.assertEqual(source.read_bytes(), original)
            with target.open(encoding="utf-8", newline="") as stream:
                self.assertEqual(list(csv.DictReader(stream)), [{"name": "Alice", "email": "alice@example.test"}, {"name": "Bob", "email": "bob@example.test"}])
            with self.assertRaises(FileExistsError):
                clean(source, target)
            with self.assertRaises(ValueError):
                clean(source, source)

    def test_unicode_and_quoted_comma(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / "in.csv", Path(directory) / "out.csv"
            source.write_text('name,email\n"林, Alex",alex@example.test\n', encoding="utf-8")
            self.assertEqual(clean(source, target)["kept"], 1)
            self.assertIn('"林, Alex"', target.read_text(encoding="utf-8"))

    def test_bad_header_and_malformed_rows_create_no_output(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / "in.csv", Path(directory) / "out.csv"
            for value in ["email,name\na@b.test,A\n", "name,email\nAlice\n", "name,email\nA,a@b.test,extra\n"]:
                source.write_text(value, encoding="utf-8")
                with self.assertRaises(ValueError):
                    clean(source, target)
                self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
