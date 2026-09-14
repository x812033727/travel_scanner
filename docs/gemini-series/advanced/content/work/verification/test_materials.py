"""Exercise actual local validators; never claim to have run Gemini or Spark."""
import copy
import csv
import importlib.util
import json
import platform
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
EX = HERE.parent / "examples"


def module(number, filename):
    spec = importlib.util.spec_from_file_location(f"lesson{number}", EX / str(number) / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


score = module(51, "score.py")
handoff = module(54, "check_handoff.py")
digest = module(56, "check_digest.py")


class Materials(unittest.TestCase):
    def setUp(self):
        self.cases = rows(EX / "51/cases.csv")
        self.ratings = rows(EX / "51/ratings-template.csv")
        self.mails = json.loads((EX / "54/mail-samples.json").read_text(encoding="utf-8"))
        self.items = rows(EX / "54/action-items.csv")
        self.news = json.loads((EX / "56/authored-digest-fixture.json").read_text(encoding="utf-8"))

    def test_unrun_is_not_success(self):
        result = score.audit(self.cases, self.ratings, EX)
        self.assertFalse(result["modelTestingComplete"])
        self.assertEqual(result["required"], 20)
        self.assertEqual(result["completed"], 0)
        self.assertIsNone(result["totals"])

    def completed(self, root):
        (root / "author.txt").write_text("Author fixture only, not a model output.", encoding="utf-8")
        data = copy.deepcopy(self.ratings)
        for row in data:
            row.update(status="complete", raw_file="author.txt", evidence="Fixture for validator only")
            row.update({key: "2" for key in score.CRITERIA})
        return data

    def test_complete_records_still_need_semantic_review(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = score.audit(self.cases, self.completed(root), root)
            self.assertTrue(result["modelTestingComplete"])
            self.assertFalse(result["semanticQualityApproved"])
            self.assertEqual(result["totals"], {"A": 80, "B": 80})

    def test_raw_output_and_rating_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            valid = self.completed(root)
            for key, value in (("raw_file", "missing.txt"), ("raw_file", "../outside.txt"), ("raw_file", str(root / "author.txt")), ("accuracy", "3"), ("accuracy", "1.5"), ("evidence", ""), ("status", "approved")):
                with self.subTest(key=key, value=value):
                    data = copy.deepcopy(valid)
                    data[0][key] = value
                    result = score.audit(self.cases, data, root)
                    self.assertTrue(result["errors"])
                    self.assertFalse(result["modelTestingComplete"])

    def test_empty_raw(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = self.completed(root)
            (root / "author.txt").write_text(" ", encoding="utf-8")
            self.assertTrue(score.audit(self.cases, data, root)["errors"])

    def test_missing_duplicate_and_unknown_cases(self):
        self.assertTrue(score.audit(self.cases, self.ratings[1:], EX)["missingRows"])
        self.assertTrue(score.audit(self.cases, self.ratings + self.ratings[:1], EX)["errors"])
        self.ratings[0]["case_id"] = "unknown"
        self.assertTrue(score.audit(self.cases, self.ratings, EX)["errors"])

    def test_ten_distinct_cases_and_no_scores(self):
        self.assertEqual(len({row["kind"] for row in self.cases}), 10)
        self.assertTrue(all(not row["accuracy"] for row in self.ratings))

    def test_gem_change_and_regression(self):
        cases = rows(EX / "52/regression-cases.csv")
        self.assertEqual(len(cases), 12)
        changed = [r["id"] for r in cases if r["expected_v1"] != r["expected_v2"]]
        self.assertEqual(changed, ["G03", "G11"])
        log = rows(EX / "52/regression-log.csv")
        self.assertEqual(len(log), 24)
        self.assertTrue(all(r["status"] == "not_run" for r in log))

    def test_handoff_retains_conflict_and_unknown_owner(self):
        result = handoff.check(self.mails, self.items)
        self.assertTrue(result["evidenceFieldsValid"])
        self.assertTrue(result["semanticReviewRequired"])
        self.assertEqual(result["sentEmails"], 0)
        self.assertEqual(self.items[0]["due"], "2026-09-20|2026-09-21")
        self.assertEqual(self.items[3]["owner"], "")

    def test_fabricated_or_wrong_source_quote_rejected(self):
        for quotes in ({"M2": "已寄出"}, {"M99": "不存在"}, [], {"M2": ""}):
            with self.subTest(quotes=quotes):
                self.items[1]["source_quotes"] = json.dumps(quotes)
                self.assertFalse(handoff.check(self.mails, self.items)["evidenceFieldsValid"])

    def test_unresolved_handoff_not_confirmed(self):
        self.items[0]["status"] = "confirmed"
        self.assertFalse(handoff.check(self.mails, self.items)["evidenceFieldsValid"])

    def test_missing_date_and_invented_owner(self):
        self.items[1]["due"] = ""
        self.items[3]["owner"] = "模型指定"
        self.assertEqual(len(handoff.check(self.mails, self.items)["errors"]), 2)

    def test_conflict_requires_both_dates(self):
        self.items[0]["due"] = "2026-09-21"
        self.assertFalse(handoff.check(self.mails, self.items)["evidenceFieldsValid"])

    def test_duplicate_handoff(self):
        self.assertFalse(handoff.check(self.mails, self.items + self.items[:1])["evidenceFieldsValid"])

    def test_digest_reports_unread_source_without_claiming_schedule(self):
        result = digest.check(self.news)
        self.assertEqual(result["missingSources"], ["https://example.invalid/source-c"])
        self.assertTrue(result["authoredFixture"])
        self.assertFalse(result["actualScheduledRunVerified"])
        self.assertFalse(result["scheduleCreated"])

    def test_digest_date_boundaries(self):
        for date in (self.news["end"], "2026-09-06T23:59:59+08:00"):
            with self.subTest(date=date):
                self.news["items"][0]["published"] = date
                with self.assertRaisesRegex(ValueError, "outside_period"):
                    digest.check(self.news)
        self.news["items"][0]["published"] = self.news["start"]
        self.assertEqual(digest.check(self.news)["dateAndCoverageCheck"], "passed")

    def test_digest_timezone_and_reversed_period(self):
        self.news["start"] = "2026-09-07T00:00:00"
        with self.assertRaisesRegex(ValueError, "timezone_required"):
            digest.check(self.news)
        self.news["start"] = self.news["end"]
        with self.assertRaisesRegex(ValueError, "invalid_period"):
            digest.check(self.news)

    def test_digest_requires_full_source_accounting(self):
        self.news["sources"].pop()
        with self.assertRaisesRegex(ValueError, "accounted_for"):
            digest.check(self.news)

    def test_digest_cannot_cite_unread_source(self):
        self.news["items"][0]["source"] = "https://example.invalid/source-c"
        with self.assertRaisesRegex(ValueError, "no_read_source"):
            digest.check(self.news)

    def test_digest_requires_quote(self):
        self.news["items"][0]["quote"] = ""
        with self.assertRaisesRegex(ValueError, "missing_item_evidence"):
            digest.check(self.news)

    def test_schedule_log_is_unrun(self):
        log = rows(EX / "56/schedule-log.csv")
        self.assertEqual(len(log), 6)
        self.assertTrue(all(r["status"] == "not_run" and not r["output_file"] for r in log))


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Materials))
    receipt = {"checkedOn": "2026-09-14", "python": platform.python_version(), "platform": platform.system(), "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "success": result.wasSuccessful(), "kind": "authored-fixture-validator-tests", "modelCalls": 0, "actualScheduledRuns": 0}
    (HERE / "fixtures.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    raise SystemExit(0 if result.wasSuccessful() else 1)
