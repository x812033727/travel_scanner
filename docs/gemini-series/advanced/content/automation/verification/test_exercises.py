"""Behavioral regression cases for authored fixtures; no model or remote Actions job."""
import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
EX = HERE / "examples"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


pipeline = module("pipeline", EX / "78/pipeline.py")
sys.modules["pipeline"] = pipeline
merger = module("merger", EX / "77/merge_reviews.py")
workflow = module("workflow", EX / "79/runner.py")
maintenance = module("maintenance", EX / "80/prepare_review.py")


class Exercises(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="gemini-automation-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.documents = self.root / "documents"
        shutil.copytree(EX / "78/documents", self.documents)
        self.output = self.root / "output"

    def test_twenty_documents_interrupt_resume_and_no_duplicate(self):
        first = pipeline.run_batch(self.documents, self.output, fixture=True, stop_after=5)
        self.assertEqual((first["processed"], first["interrupted"]), (5, True))
        second = pipeline.run_batch(self.documents, self.output, fixture=True)
        self.assertEqual((second["processed"], second["skipped"]), (15, 5))
        third = pipeline.run_batch(self.documents, self.output, fixture=True)
        self.assertEqual((third["processed"], third["skipped"]), (0, 20))
        self.assertEqual(len(list((self.output / "results").glob("*.json"))), 20)
        self.assertEqual(len((self.output / "journal.jsonl").read_text().splitlines()), 20)

    def test_one_changed_input_reprocesses_one_document(self):
        pipeline.run_batch(self.documents, self.output, fixture=True)
        with (self.documents / "doc07.md").open("a", encoding="utf-8") as stream:
            stream.write("\n更正人數。\n")
        result = pipeline.run_batch(self.documents, self.output, fixture=True)
        self.assertEqual((result["processed"], result["skipped"]), (1, 19))

    def test_tampered_output_is_not_reused(self):
        initial = pipeline.run_batch(self.documents, self.output, fixture=True)
        self.assertFalse(initial["failed"], initial)
        (self.output / "results/doc03.json").write_text("{}")
        self.assertEqual(pipeline.run_batch(self.documents, self.output, fixture=True)["processed"], 1)

    def test_lock_prevents_another_writer(self):
        self.output.mkdir()
        (self.output / ".pipeline.lock").write_text("authored-other-process")
        with self.assertRaises(FileExistsError):
            pipeline.run_batch(self.documents, self.output, fixture=True)

    def test_provider_failure_stops_and_does_not_mark_done(self):
        def fail(document_id, text):
            raise ValueError("authored_provider_failure")
        result = pipeline.run_batch(self.documents, self.output, fixture=True, provider=fail)
        self.assertEqual(result["processed"], 0)
        self.assertEqual(len(result["failed"]), 1)
        self.assertFalse((self.output / "checkpoint.json").exists())

    def test_output_contract_rejects_fabricated_quote(self):
        bad = {"id": "doc01", "title": "標題", "summary": "摘要", "quote": "資料沒有這句"}
        with self.assertRaisesRegex(ValueError, "quote_not_in_input"):
            pipeline.validate(bad, "doc01", "實際原文")

    def test_zero_exit_does_not_make_invalid_json_successful(self):
        for stdout in ('not json', '{}', '{"response":"not json"}', '{"error":{"message":"failed"},"response":"{}"}'):
            with self.subTest(stdout=stdout), self.assertRaises(ValueError):
                pipeline.parse_cli(stdout, 0, "doc01", "原文")

    def test_nonzero_exit_rejects_even_valid_response(self):
        with self.assertRaisesRegex(ValueError, "cli_exit_53"):
            pipeline.parse_cli('{}', 53, "doc01", "原文")

    def test_stream_tool_result_does_not_mean_finished(self):
        with self.assertRaises(ValueError):
            pipeline.classify_stream('{"type":"tool_result","result":"done"}\n')
        result = pipeline.classify_stream('{"type":"message","content":"text"}\n{"type":"result","status":"success"}\n')
        self.assertFalse(result["content_contract_verified"])

    def test_live_mode_missing_model_fails_without_request(self):
        result = pipeline.run_batch(self.documents, self.output, fixture=False, config={"command": ["unused-executable"]})
        self.assertEqual(result["processed"], 0)
        self.assertEqual(len(result["failed"]), 1)

    def reports(self):
        return [json.loads((EX / "77" / name).read_text(encoding="utf-8")) for name in ("fixture-code-report.json", "fixture-docs-report.json")]

    def test_reviews_require_real_evidence(self):
        result = merger.merge(EX / "77/review-project", self.reports())
        self.assertEqual(len(result["accepted"]), 2)
        self.assertFalse(result["automatically_applied"])

    def test_duplicate_reviews_merge(self):
        report = self.reports()[0]
        duplicate = copy.deepcopy(report)
        duplicate["agent"] = "second-authored-fixture"
        result = merger.merge(EX / "77/review-project", [report, duplicate])
        self.assertEqual(len(result["accepted"]), 1)
        self.assertEqual(len(result["accepted"][0]["agents"]), 2)

    def test_opposite_recommendations_wait_for_review(self):
        first = self.reports()[0]
        second = copy.deepcopy(first)
        second["findings"][0]["recommendation"] = "Keep negative inputs unchanged."
        result = merger.merge(EX / "77/review-project", [first, second])
        self.assertEqual(len(result["accepted"]), 0)
        self.assertEqual(len(result["conflicts"]), 1)

    def test_bad_line_quote_or_path_is_rejected(self):
        for key, value in [("line", 0), ("line", True), ("quote", "fabricated"), ("file", "../private.txt")]:
            report = self.reports()[0]
            report["findings"][0][key] = value
            with self.subTest(key=key):
                self.assertEqual(len(merger.merge(EX / "77/review-project", [report])["rejected"]), 1)

    def test_failed_agent_cannot_offer_accepted_findings(self):
        report = self.reports()[0]
        report["status"] = "failed"
        self.assertEqual(len(merger.merge(EX / "77/review-project", [report])["accepted"]), 0)

    def workflow_root(self):
        target = self.root / "workflow"
        shutil.copytree(EX / "79", target, ignore=shutil.ignore_patterns("__pycache__"))
        return target

    def test_workflow_fixture_runs_without_secret(self):
        result = workflow.run(self.workflow_root(), {"LESSON_MODE": "fixture", "LESSON_DOCUMENT": "doc02.md"})
        self.assertEqual(result["status"], "complete")
        self.assertFalse(result["remote_actions_run"])
        self.assertEqual(result["batch"]["processed"], 1)

    def test_workflow_missing_secret_and_path_injection_fail(self):
        target = self.workflow_root()
        for env in [{"LESSON_MODE": "live", "LESSON_MODEL": "placeholder"}, {"LESSON_DOCUMENT": "../private.txt"}, {"LESSON_MODE": "other"}]:
            result = workflow.run(target, env)
            self.assertEqual(result["status"], "failed")

    def test_workflow_has_only_manual_trigger_and_pinned_actions(self):
        import yaml
        value = yaml.load((EX / "79/review.yml").read_text(), Loader=yaml.BaseLoader)
        self.assertEqual(set(value["on"]), {"workflow_dispatch"})
        self.assertEqual(value["permissions"], {"contents": "read"})
        self.assertEqual(value["jobs"]["report"]["environment"], "gemini-tutorial")
        for step in value["jobs"]["report"]["steps"]:
            if "uses" in step:
                self.assertRegex(step["uses"], r"^actions/[a-z-]+@[a-f0-9]{40}$")
            self.assertNotIn("${{", step.get("run", ""))

    def test_maintenance_finds_known_broken_link(self):
        tree = {file.name: file.read_text(encoding="utf-8") for file in (EX / "80/documents").glob("*.md")}
        problems = maintenance.check(tree)
        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0]["file"], "doc03.md")

    def test_maintenance_produces_patch_without_source_write(self):
        proposals = json.loads((EX / "80/reference-proposals.json").read_text(encoding="utf-8"))
        source = EX / "80/documents"
        before = (source / "doc03.md").read_bytes()
        result = maintenance.prepare(source, proposals, self.output)
        self.assertTrue(result["ready_for_human_review"])
        self.assertFalse(result["publishable"])
        self.assertEqual(len(result["changes"]), 1)
        self.assertEqual((source / "doc03.md").read_bytes(), before)
        self.assertIn('+[下一份](doc04.md#details)', (self.output / "changes.patch").read_text(encoding="utf-8"))

    def test_invented_target_does_not_create_reviewable_patch(self):
        proposals = json.loads((EX / "80/bad-proposals.json").read_text(encoding="utf-8"))
        result = maintenance.prepare(EX / "80/documents", proposals, self.output)
        self.assertFalse(result["ready_for_human_review"])
        self.assertFalse((self.output / "changes.patch").exists())

    def test_maintenance_outside_path_is_rejected(self):
        result = maintenance.prepare(EX / "80/documents", {"../outside.md": "bad"}, self.output)
        self.assertEqual(result["reason"], "proposal_outside_scope")

    def test_patch_passes_git_check_with_document_directory(self):
        source = self.root / "project/documents"
        shutil.copytree(EX / "80/documents", source)
        proposals = json.loads((EX / "80/reference-proposals.json").read_text(encoding="utf-8"))
        maintenance.prepare(source, proposals, source.parent / "review")
        result = subprocess.run(["git", "apply", "--check", "--directory=documents", "review/changes.patch"],
                                cwd=source.parent, capture_output=True, text=True, check=False, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("missing.md", (source / "doc03.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Exercises)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    receipt = {"checkedOn": "2026-09-14", "platform": os.name, "python": sys.version.split()[0],
               "method": "authored fixtures and local subprocess adapters; no cloud model or remote Actions run",
               "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped)}
    (HERE / "verification/fixtures.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    raise SystemExit(0 if result.wasSuccessful() else 1)
