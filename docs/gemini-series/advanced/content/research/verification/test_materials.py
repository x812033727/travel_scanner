"""Meaningful negative cases for the local research exercises, no model calls."""
import csv
import hashlib
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
spec = importlib.util.spec_from_file_location("checks", EX / "research_checks.py")
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


@contextmanager
def copied(number):
    with tempfile.TemporaryDirectory(prefix="gemini-research-test-") as temp:
        root = Path(temp) / str(number)
        shutil.copytree(EX / str(number), root, ignore=shutil.ignore_patterns("__pycache__"))
        yield root


def save_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def change_transit(root, callback):
    path = root / "youbike-snapshot.json"
    data = json.loads(path.read_bytes())
    callback(data)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8", newline="\n")
    provenance = json.loads((root / "snapshot-provenance.json").read_text(encoding="utf-8"))
    provenance["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    (root / "snapshot-provenance.json").write_text(json.dumps(provenance), encoding="utf-8", newline="\n")


class Materials(unittest.TestCase):
    def test_versions_select_one_of_each(self):
        self.assertEqual(checks.versions(EX / "57", "phase1")["selectedS01"], "v1")
        self.assertEqual(checks.versions(EX / "57")["selectedS01"], "v2")

    def test_two_active_versions_fail(self):
        with copied(57) as root:
            rows = checks.rows(root / "sources-v1-v2.csv")
            rows[0]["phase2"] = "yes"
            save_csv(root / "sources-v1-v2.csv", rows)
            with self.assertRaisesRegex(ValueError, "unique_active"):
                checks.versions(root)

    def test_source_changed_fails_hash(self):
        with copied(57) as root:
            (root / "sources/S01-v2.md").write_text("名額54人", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "bytes_changed"):
                checks.versions(root)

    def test_path_scope(self):
        with self.assertRaisesRegex(ValueError, "outside_exercise"):
            checks.local(EX / "57", "../58/prompt.txt")

    def test_five_claims_are_traceable(self):
        result = checks.evidence(EX / "58")
        self.assertEqual(result["claims"], 5)
        self.assertTrue(result["humanSemanticReviewRequired"])

    def test_fabricated_quote_fails(self):
        with copied(58) as root:
            data = checks.rows(root / "evidence-matrix.csv")
            data[0]["quotes"] = json.dumps({"E1": "名額為24人。", "E2": "名額為54人。"})
            save_csv(root / "evidence-matrix.csv", data)
            with self.assertRaisesRegex(ValueError, "fabricated_quote"):
                checks.evidence(root)

    def test_unknown_can_record_search_without_fake_quote(self):
        with copied(58) as root:
            data = checks.rows(root / "evidence-matrix.csv")
            data[4].update(claim="是否有餐點", source_ids="E1|E2|E3", quotes="{}", judgment="三份資料均未提及")
            save_csv(root / "evidence-matrix.csv", data)
            self.assertEqual(checks.evidence(root)["claims"], 5)

    def test_conflict_needs_both_sources(self):
        with copied(58) as root:
            data = checks.rows(root / "evidence-matrix.csv")
            data[1].update(source_ids="E1", quotes=json.dumps({"E1": "預定活動日期為 2026-10-03。"}))
            save_csv(root / "evidence-matrix.csv", data)
            with self.assertRaisesRegex(ValueError, "two_sources"):
                checks.evidence(root)

    def test_twelve_questions(self):
        self.assertEqual(checks.quiz(EX / "59")["questions"], 12)

    def test_duplicate_options_are_invalid(self):
        with copied(59) as root:
            data = checks.rows(root / "questions.csv")
            data[0]["B"] = data[0]["A"]
            save_csv(root / "questions.csv", data)
            with self.assertRaisesRegex(ValueError, "invalid_options"):
                checks.quiz(root)

    def test_wrong_concept_quote_is_invalid(self):
        with copied(59) as root:
            data = checks.rows(root / "questions.csv")
            data[0]["quote"] = data[1]["quote"]
            save_csv(root / "questions.csv", data)
            with self.assertRaisesRegex(ValueError, "not_supported"):
                checks.quiz(root)

    def test_three_original_pdf_bytes(self):
        result = checks.papers(EX / "60")
        self.assertTrue(result["bytesMatch"])
        self.assertFalse(result["comparableAsSingleRanking"])

    def test_damaged_pdf_rejected(self):
        with copied(60) as root:
            (root / "papers/dpr-2020.pdf").write_bytes(b"%PDF damaged")
            with self.assertRaisesRegex(ValueError, "bytes_changed"):
                checks.papers(root)

    def test_media_not_run_is_pending(self):
        result = checks.media(EX / "61")
        self.assertEqual(result["pending"], 30)
        self.assertEqual(result["reviewed"], 0)
        self.assertFalse(result["modelMediaGenerationVerified"])

    def test_media_review_needs_evidence(self):
        with copied(61) as root:
            data = checks.rows(root / "consistency-log.csv")
            data[0]["status"] = "reviewed"
            save_csv(root / "consistency-log.csv", data)
            with self.assertRaisesRegex(ValueError, "evidence_required"):
                checks.media(root)

    def test_media_cannot_drop_one_fact(self):
        with copied(61) as root:
            data = checks.rows(root / "consistency-log.csv")
            save_csv(root / "consistency-log.csv", data[:-1])
            with self.assertRaisesRegex(ValueError, "thirty_observations"):
                checks.media(root)

    def test_snapshot_reproduces_counts_and_field_drift(self):
        result = checks.transit(EX / "62")
        self.assertEqual(result["stations"], 1800)
        self.assertEqual(sum(result["areaCounts"].values()), 1800)
        self.assertEqual(len(result["areaCounts"]), 13)
        self.assertEqual(result["areaCounts"]["臺大公館校區"], 65)
        self.assertEqual(result["actValues"], {"0": 32, "1": 1768})
        self.assertIn("tot", result["declaredButAbsent"])
        self.assertIn("Quantity", result["presentButNotDeclared"])
        self.assertFalse(result["annualUsageInferable"])

    def test_duplicate_station_rejected(self):
        with copied(62) as root:
            change_transit(root, lambda data: data.append(data[0].copy()))
            with self.assertRaisesRegex(ValueError, "duplicate_or_invalid"):
                checks.transit(root)

    def test_missing_field_is_not_zero(self):
        with copied(62) as root:
            change_transit(root, lambda data: data[0].pop("available_rent_bikes"))
            with self.assertRaisesRegex(ValueError, "missing_required"):
                checks.transit(root)

    def test_invalid_count_not_silently_coerced(self):
        for value in [-1, "5", True]:
            with self.subTest(value=value), copied(62) as root:
                change_transit(root, lambda data, value=value: data[0].update(available_rent_bikes=value))
                with self.assertRaisesRegex(ValueError, "invalid_station_count"):
                    checks.transit(root)

    def test_future_station_timestamp_rejected(self):
        with copied(62) as root:
            change_transit(root, lambda data: data[0].update(infoTime="2099-01-01 00:00:00"))
            with self.assertRaisesRegex(ValueError, "after_capture"):
                checks.transit(root)

    def test_snapshot_changed_without_provenance_rejected(self):
        with copied(62) as root:
            with (root / "youbike-snapshot.json").open("ab") as file:
                file.write(b" ")
            with self.assertRaisesRegex(ValueError, "hash_mismatch"):
                checks.transit(root)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Materials))
    receipt = {"checkedOn": "2026-09-14", "python": platform.python_version(), "platform": platform.system(), "kind": "original-fixtures-and-frozen-public-data", "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "success": result.wasSuccessful(), "modelCalls": 0, "mediaGenerated": 0}
    (HERE / "fixtures.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    raise SystemExit(0 if result.wasSuccessful() else 1)
