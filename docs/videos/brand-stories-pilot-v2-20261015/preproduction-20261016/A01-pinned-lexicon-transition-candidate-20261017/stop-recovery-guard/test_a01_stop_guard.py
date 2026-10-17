"""Local, disposable tests for the host-only STOP guard candidate."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from a01_stop_guard import Paths, arm, finish, lift, restore, status


class StopGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.paths = Paths(root / "video-work" / "story-rolling-suitcase-v2", root / "release")
        self.paths.workdir.mkdir(parents=True)
        self.paths.release_dir.mkdir()
        self.original = b"owner A01 hold; no paid media yet\n"
        self.paths.stop.write_bytes(self.original)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_arm_lift_restore_finish_keeps_original_stop(self) -> None:
        arm(self.paths)
        self.assertEqual(self.paths.stop.read_bytes(), self.original)
        self.assertEqual(self.paths.held.read_bytes(), self.original)
        lift(self.paths)
        self.assertFalse(self.paths.stop.exists())
        self.assertTrue(self.paths.marker.exists())
        self.assertEqual(restore(self.paths), "A01 original STOP restored")
        self.assertEqual(self.paths.stop.read_bytes(), self.original)
        self.assertEqual(restore(self.paths), "A01 STOP already present")
        finish(self.paths)
        self.assertTrue(self.paths.stop.exists())
        self.assertFalse(self.paths.marker.exists())
        self.assertFalse(self.paths.held.exists())

    def test_interruption_before_lift_keeps_stop_and_refuses_second_arm(self) -> None:
        arm(self.paths)
        with self.assertRaisesRegex(RuntimeError, "already armed"):
            arm(self.paths)
        self.assertEqual(restore(self.paths), "A01 STOP already present")
        self.assertTrue(self.paths.stop.exists())

    def test_missing_held_link_recovers_conservative_stop(self) -> None:
        arm(self.paths)
        lift(self.paths)
        self.paths.held.unlink()
        self.assertIn("conservative STOP restored", restore(self.paths))
        self.assertIn(b"manual review interrupted", self.paths.stop.read_bytes())
        self.assertTrue(self.paths.marker.exists())

    def test_existing_new_stop_is_not_overwritten(self) -> None:
        arm(self.paths)
        lift(self.paths)
        self.paths.stop.write_bytes(b"new owner STOP\n")
        self.assertEqual(restore(self.paths), "A01 STOP already present")
        self.assertEqual(self.paths.stop.read_bytes(), b"new owner STOP\n")

    def test_unarmed_guard_requires_stop(self) -> None:
        self.assertEqual(restore(self.paths), "A01 STOP already present")
        self.paths.stop.unlink()
        with self.assertRaisesRegex(RuntimeError, "STOP and held link absent"):
            restore(self.paths)
        self.assertIn('"armed": false', status(self.paths))

    def test_lost_marker_restores_from_held_link(self) -> None:
        arm(self.paths)
        lift(self.paths)
        self.paths.marker.unlink()
        self.assertEqual(restore(self.paths), "A01 original STOP restored")
        self.assertEqual(self.paths.stop.read_bytes(), self.original)

    @unittest.skipIf(os.name == "nt", "Windows symlink privileges vary")
    def test_symlink_stop_is_rejected(self) -> None:
        self.paths.stop.unlink()
        target = self.paths.workdir / "other"
        target.write_text("x")
        self.paths.stop.symlink_to(target)
        with self.assertRaisesRegex(RuntimeError, "not a symlink"):
            arm(self.paths)


if __name__ == "__main__":
    unittest.main()
