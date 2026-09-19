"""Tests for the shared deploy hold. Run from the repository root:

    python -m unittest discover -s ops/release -v

A temporary directory stands in for /root, so nothing here needs the host, root, or
Linux; the module must keep passing on Windows.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import stat
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hold  # noqa: E402

TARGET_A = "3b8df68c693e" + "0" * 28
TARGET_B = "f" * 40
PHASES = ["prepare", "activate", "dry-run", "drafts", "publish-articles", "publish-index"]
STARTED = datetime(2026, 9, 14, 6, 54, tzinfo=UTC)


class HoldTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(self._remove_tree, root)
        self.hold_path = root / "travel-scanner-deploy.hold"
        self.release_a = root / "mokaair-ai-terms-3b8df68c693e"
        self.release_b = root / "mokaair-gemini-ffffffffffff"

    @staticmethod
    def _remove_tree(root: Path) -> None:
        for child in root.iterdir():
            child.unlink()
        root.rmdir()

    def acquire(
        self, release_dir: Path | None = None, target: str = TARGET_A, **extra: object
    ) -> str:
        owner = str(extra.pop("owner", "codex-ai-terms"))
        phases = extra.pop("phases", PHASES)
        return hold.acquire(
            release_dir or self.release_a,
            target,
            owner,
            phases,  # type: ignore[arg-type]
            hold_path=self.hold_path,
            now=STARTED,
        )

    def test_acquire_writes_a_reason_line_and_a_record(self) -> None:
        self.assertEqual(self.acquire(), "created")
        first_line, second_line = self.hold_path.read_text(encoding="utf-8").splitlines()
        # The deploy script prints this line; it must say who, which release, and what to do.
        self.assertIn("codex-ai-terms", first_line)
        self.assertIn(TARGET_A[:12], first_line)
        self.assertIn(str(self.release_a), first_line)
        self.assertIn("prepare→…→publish-index", first_line)
        self.assertIn("2026-09-14T06:54:00+00:00", first_line)
        self.assertIn("檢查該目錄後才能刪除本檔", first_line)
        self.assertEqual(
            json.loads(second_line),
            {
                "created_at": "2026-09-14T06:54:00+00:00",
                "owner": "codex-ai-terms",
                "phases": PHASES,
                "release_dir": str(self.release_a),
                "target": TARGET_A,
            },
        )
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(self.hold_path.stat().st_mode), 0o644)

    def test_the_same_release_resumes_and_any_other_is_refused(self) -> None:
        self.acquire()
        before = self.hold_path.read_bytes()
        # A driver run again after an interrupted phase keeps its own hold, unchanged.
        self.assertEqual(self.acquire(), "resumed")
        self.assertEqual(self.acquire(owner="someone-resuming-the-same-release"), "resumed")
        self.assertEqual(self.hold_path.read_bytes(), before)
        # Another release, another target in the same directory, or the same target in
        # another directory: all refused, and the file is never overwritten.
        for release_dir, target in (
            (self.release_b, TARGET_B),
            (self.release_a, TARGET_B),
            (self.release_b, TARGET_A),
        ):
            with self.assertRaises(hold.HeldByAnother) as refused:
                self.acquire(release_dir, target)
            self.assertIn("codex-ai-terms", refused.exception.first_line)
        self.assertEqual(self.hold_path.read_bytes(), before)

    def test_a_hold_written_by_hand_is_respected(self) -> None:
        # The owner can stop deploys with a one-line file; no driver may displace it.
        self.hold_path.write_text("站主暫停部署，勿動\n", encoding="utf-8")
        with self.assertRaises(hold.HeldByAnother):
            self.acquire()
        with self.assertRaises(hold.HeldByAnother):
            hold.verify(self.release_a, TARGET_A, hold_path=self.hold_path)
        with self.assertRaises(hold.HeldByAnother):
            hold.clear(self.release_a, TARGET_A, hold_path=self.hold_path)
        self.assertEqual(self.hold_path.read_text(encoding="utf-8"), "站主暫停部署，勿動\n")
        # So is an empty one, and one whose second line is not JSON.
        for content in ("", "reason only\nnot json\n"):
            self.hold_path.write_text(content, encoding="utf-8")
            with self.assertRaises(hold.HeldByAnother):
                self.acquire()

    def test_verify_refuses_when_the_hold_is_gone_or_someone_elses(self) -> None:
        self.acquire()
        record = hold.verify(self.release_a, TARGET_A, hold_path=self.hold_path)
        self.assertEqual((record["target"], record["release_dir"]), (TARGET_A, str(self.release_a)))
        self.hold_path.unlink()
        with self.assertRaises(hold.HoldMissing):
            hold.verify(self.release_a, TARGET_A, hold_path=self.hold_path)
        # Replaced by another release between two phases.
        self.acquire(self.release_b, TARGET_B, owner="codex-gemini")
        with self.assertRaises(hold.HeldByAnother) as refused:
            hold.verify(self.release_a, TARGET_A, hold_path=self.hold_path)
        self.assertIn("codex-gemini", refused.exception.first_line)
        self.assertTrue(self.hold_path.exists())

    def test_clear_removes_only_its_own_hold(self) -> None:
        self.acquire()
        with self.assertRaises(hold.HeldByAnother):
            hold.clear(self.release_b, TARGET_B, hold_path=self.hold_path)
        self.assertTrue(self.hold_path.exists())
        self.assertEqual(hold.clear(self.release_a, TARGET_A, hold_path=self.hold_path), "cleared")
        self.assertFalse(self.hold_path.exists())
        # Nothing left to remove is reported, not raised: the release already succeeded.
        self.assertEqual(hold.clear(self.release_a, TARGET_A, hold_path=self.hold_path), "missing")

    def test_a_hold_from_an_earlier_driver_is_recognised_by_its_two_keys(self) -> None:
        # docs/ai-news-2026-ytd/release_hold.py wrote the same two-line shape; only
        # target and release_dir decide ownership, so its holds and ours interoperate.
        record = {
            "target": TARGET_A,
            "release_dir": str(self.release_a),
            "owner": "codex-ai-news-ytd",
            "phases": ["prepare", "activate", "dry-run", "publish", "public-qa"],
            "created_at": "2026-09-18T01:02:03+00:00",
        }
        self.hold_path.write_text(
            "codex-ai-news-ytd publishing 3b8df68c693e; inspect before removal.\n"
            + json.dumps(record)
            + "\n",
            encoding="utf-8",
        )
        self.assertEqual(self.acquire(), "resumed")
        self.assertEqual(hold.verify(self.release_a, TARGET_A, hold_path=self.hold_path), record)
        with self.assertRaises(hold.HeldByAnother):
            self.acquire(self.release_b, TARGET_B)

    def test_the_reason_line_stays_within_what_the_script_prints(self) -> None:
        long_phases = [f"phase-{index:02d}" for index in range(40)]
        self.acquire(owner="x" * hold.OWNER_LIMIT, phases=long_phases)
        first_line = self.hold_path.read_bytes().splitlines()[0]
        self.assertLessEqual(len(first_line), hold.FIRST_LINE_LIMIT)
        self.assertIn("phase-00→…→phase-39".encode(), first_line)
        self.hold_path.unlink()
        # A release directory long enough to push the line past the limit is refused
        # before anything is written, rather than truncated on the host.
        too_long = self.release_a.parent / ("m" * 600)
        with self.assertRaises(ValueError):
            self.acquire(too_long)
        self.assertFalse(self.hold_path.exists())

    def test_inputs_are_validated_before_anything_is_written(self) -> None:
        cases = [
            dict(target="3B8DF68C693E" + "0" * 28),  # uppercase
            dict(target=TARGET_A[:12]),  # short
            dict(release_dir=Path("relative/dir")),
            dict(owner=""),
            dict(owner="two\nlines"),
            dict(owner="o" * (hold.OWNER_LIMIT + 1)),
            dict(phases=[]),
            dict(phases=["prepare", "bad\nphase"]),
        ]
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    self.acquire(**case)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            hold.acquire(
                self.release_a,
                TARGET_A,
                "owner",
                PHASES,
                hold_path=self.hold_path,
                now=datetime(2026, 9, 14),
            )
        self.assertFalse(self.hold_path.exists())

    def test_read_reports_absent_hand_written_and_driver_holds(self) -> None:
        self.assertEqual(hold.read(self.hold_path), ("", None))
        self.hold_path.write_text("by hand\n", encoding="utf-8")
        self.assertEqual(hold.read(self.hold_path), ("by hand", None))
        self.hold_path.unlink()
        self.acquire()
        first_line, record = hold.read(self.hold_path)
        self.assertIn("codex-ai-terms", first_line)
        self.assertEqual(record["owner"], "codex-ai-terms")  # type: ignore[index]

    def test_the_command_line_refuses_with_the_scripts_exit_code(self) -> None:
        def run(*args: str) -> tuple[int, str, str]:
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = hold.main(["--hold-path", str(self.hold_path), *args])
            return code, out.getvalue().strip(), err.getvalue().strip()

        self.assertEqual(run("show"), (0, f"no hold at {self.hold_path}", ""))
        code, out, err = run("acquire", str(self.release_a), TARGET_A, "codex-ai-terms", *PHASES)
        self.assertEqual((code, out, err), (0, "created", ""))
        code, out, _ = run("verify", str(self.release_a), TARGET_A)
        self.assertEqual((code, json.loads(out)["owner"]), (0, "codex-ai-terms"))
        code, out, err = run("acquire", str(self.release_b), TARGET_B, "codex-gemini", *PHASES)
        self.assertEqual((code, out), (hold.REFUSED_EXIT, ""))
        self.assertIn("held by someone else", err)
        code, out, _ = run("show")
        self.assertEqual(code, 0)
        self.assertIn("codex-ai-terms 正在發布", out)
        self.assertEqual(run("clear", str(self.release_a), TARGET_A)[:2], (0, "cleared"))
        code, _, err = run("verify", str(self.release_a), TARGET_A)
        self.assertEqual(code, hold.REFUSED_EXIT)
        self.assertIn("does not exist", err)
        code, _, err = run("acquire", str(self.release_a), "not-a-sha", "codex-ai-terms", *PHASES)
        self.assertEqual(code, hold.REFUSED_EXIT)
        self.assertIn("40-character", err)


if __name__ == "__main__":
    unittest.main()
