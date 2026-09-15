"""Realistic regression cases for original materials, not Gemini/Flow execution evidence."""
import csv
import importlib.util
import json
import platform
import shutil
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

HERE = Path(__file__).resolve().parent
EX = HERE.parent / "examples"
spec = importlib.util.spec_from_file_location("checks", EX / "creative_checks.py")
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


@contextmanager
def copied(n):
    with tempfile.TemporaryDirectory(prefix="creative-fixture-") as tmp:
        folder = Path(tmp) / str(n)
        shutil.copytree(EX / str(n), folder)
        yield folder


def mutate_csv(file, callback):
    rows = checks.rows(file)
    callback(rows)
    with file.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class Materials(unittest.TestCase):
    def test_independent_sales_oracle(self):
        result = checks.sales(EX / "67")
        self.assertEqual((result["acceptedRows"], result["excludedRows"]), (43, 7))

    def test_refund_and_large_order_retained(self):
        rows = {r["source_id"]: r for r in checks.sales(EX / "67")["accepted"]}
        self.assertEqual(rows["S048"]["amount"], "-300.00")
        self.assertEqual(rows["S049"]["amount"], "30000.00")

    def test_currencies_separate(self):
        totals = checks.sales(EX / "67")["totals"]
        self.assertEqual([r["amount"] for r in totals], ["42300.00", "3040.00", "50.00"])

    def test_conflicting_id_quarantines_both(self):
        bad = {r["source_id"]: r["reason"] for r in checks.sales(EX / "67")["excluded"]}
        self.assertEqual(bad["S010"], "conflicting_order")
        self.assertEqual(bad["S050"], "conflicting_order")

    def test_exact_duplicate_only_copy_excluded(self):
        result = checks.sales(EX / "67")
        self.assertIn("S005", [r["source_id"] for r in result["accepted"]])
        self.assertIn("S041", [r["source_id"] for r in result["excluded"]])

    def test_missing_price_is_not_zero(self):
        result = checks.sales(EX / "67")
        self.assertNotIn("S042", [r["source_id"] for r in result["accepted"]])

    def test_invalid_and_ambiguous_dates_quarantined(self):
        bad = {r["source_id"]: r["reason"] for r in checks.sales(EX / "67")["excluded"]}
        self.assertEqual(bad["S043"], "invalid_date")
        self.assertEqual(bad["S045"], "ambiguous_date")

    def test_explicit_year_first_date_normalized(self):
        row = next(r for r in checks.sales(EX / "67")["accepted"] if r["source_id"] == "S044")
        self.assertEqual(row["date"], "2026-09-12")

    def test_nonfinite_price_quarantined(self):
        for price in ["NaN", "Infinity", "-1", "1.001"]:
            with self.subTest(price=price), copied(67) as folder:
                mutate_csv(folder / "sales-dirty.csv", lambda rows, price=price: rows[0].update(unit_price=price))
                result = checks.clean_sales(folder / "sales-dirty.csv")
                self.assertIn("S001", [r["source_id"] for r in result["excluded"]])

    def test_negative_sale_requires_refund_type(self):
        with copied(67) as folder:
            mutate_csv(folder / "sales-dirty.csv", lambda rows: rows[0].update(quantity="-1"))
            self.assertIn("S001", [r["source_id"] for r in checks.clean_sales(folder / "sales-dirty.csv")["excluded"]])

    def test_duplicate_source_ids_fail(self):
        with copied(67) as folder:
            mutate_csv(folder / "sales-dirty.csv", lambda rows: rows[0].update(source_id="S002"))
            with self.assertRaisesRegex(ValueError, "source_id"):
                checks.clean_sales(folder / "sales-dirty.csv")

    def test_quality_does_not_support_ingredients(self):
        with self.assertRaisesRegex(ValueError, "unsupported_mode"):
            checks.flow_request(EX / "65", "Veo 3.1 Quality", "ingredients", 8)

    def test_fast_ingredients_not_four_seconds(self):
        with self.assertRaisesRegex(ValueError, "unsupported_duration"):
            checks.flow_request(EX / "65", "Veo 3.1 Fast", "ingredients", 4)

    def test_document_compatible_not_ui_tested(self):
        r = checks.flow_request(EX / "65", "Veo 3.1 Fast", "frames_first_last", 4)
        self.assertTrue(r["documentCompatible"])
        self.assertFalse(r["actualUiVerified"])

    def test_omni_extension_still_unavailable(self):
        with self.assertRaisesRegex(ValueError, "unsupported_mode"):
            checks.flow_request(EX / "65", "Gemini Omni Flash 1.1", "extend", 8)

    def test_unknown_model_cannot_guess(self):
        with self.assertRaisesRegex(ValueError, "unknown_model"):
            checks.flow_request(EX / "65", "Future model", "ingredients", 8)

    def test_date_change_four_assets(self):
        r = checks.affected_assets(EX / "68")
        self.assertEqual(r["changedFacts"], ["F02"])
        self.assertEqual(r["affected"], ["A1", "I1", "I3", "V1"])

    def test_missing_fact_dependency_fails(self):
        with copied(68) as folder:
            mutate_csv(folder / "asset-register.csv", lambda rows: rows[0].update(fact_ids="F99"))
            with self.assertRaisesRegex(ValueError, "unknown_fact"):
                checks.affected_assets(folder)

    def test_pending_media_is_not_completion(self):
        for n, filename in [(63, "image-scorecard.csv"), (64, "edit-log.csv"), (65, "generation-log.csv")]:
            result = checks.pending(EX / str(n), filename, 3)
            self.assertEqual(result["pending"], 3)
            self.assertFalse(result["modelGenerationProved"])

    def test_review_requires_actual_output(self):
        with copied(63) as folder:
            mutate_csv(folder / "image-scorecard.csv", lambda rows: rows[0].update(status="reviewed"))
            with self.assertRaisesRegex(ValueError, "actual_output"):
                checks.pending(folder, "image-scorecard.csv", 3)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Materials))
    (HERE / "fixtures.json").write_text(json.dumps({"checkedOn": "2026-09-14", "python": platform.python_version(), "tests": result.testsRun, "success": result.wasSuccessful(), "failures": len(result.failures), "errors": len(result.errors), "modelCalls": 0}, indent=2) + "\n", encoding="utf-8", newline="\n")
    raise SystemExit(0 if result.wasSuccessful() else 1)
