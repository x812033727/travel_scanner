"""Tests for offsite.py: a temp directory stands in for the nightly root and a fake runner
for rclone, which keeps a dict of what is "on Drive". No network, Docker or root."""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import offsite  # noqa: E402
from backup import Completed, ConfigError, Paths  # noqa: E402
from offsite import Offsite, OffsiteConfig  # noqa: E402

REMOTE = "videobackup:主機/資料庫/nightly"


class FakeDrive:
    """Answers the rclone commands offsite.py sends, keeping uploaded files in ``files``."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.files: dict[str, set[str]] = {}
        self.commands: list[list[str]] = []
        self.fail: str | None = None
        self.missing_folder = True

    def run(self, args, *, timeout=60, output_path=None, input_path=None):
        rclone = list(args[args.index("rclone", args.index("-c") + 2) + 1 :])
        self.commands.append(rclone)
        verb = rclone[0]
        if verb == self.fail:
            return Completed(1, f"{verb} broke")
        if verb == "lsf" and not self.files and self.missing_folder:
            return Completed(3, "ERROR : error listing: directory not found")
        if verb == "lsf" and "--dirs-only" in rclone:
            return Completed(0, "".join(f"{name}/\n" for name in sorted(self.files)))
        if verb == "lsf":
            return Completed(
                0,
                "".join(
                    f"{name}/manifest.json\n"
                    for name, files in sorted(self.files.items())
                    if "manifest.json" in files
                ),
            )
        if verb == "copy":
            name = rclone[1].rsplit("/", 1)[1]
            local = {path.name for path in (self.root / name).iterdir()}
            if "--include" in rclone:
                chosen = {"manifest.json"}
            else:
                chosen = local - {"manifest.json"}
            self.files.setdefault(name, set()).update(chosen)
            return Completed(0, "")
        if verb == "check":
            name = rclone[1].rsplit("/", 1)[1]
            local = {path.name for path in (self.root / name).iterdir()}
            missing = local - self.files.get(name, set())
            return Completed(1 if missing else 0, f"{len(missing)} differences")
        if verb == "purge":
            self.files.pop(rclone[1].rsplit("/", 1)[1], None)
            return Completed(0, "")
        raise AssertionError(f"unexpected rclone call {rclone}")


class OffsiteCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.paths = Paths(
            root=self.tmp / "nightly",
            state_dir=self.tmp / "state",
            env_file=self.tmp / "backup.env",
        )
        self.paths.root.mkdir()
        self.drive = FakeDrive(self.paths.root)

    def make_run(self, name: str, *, manifest: bool = True) -> Path:
        run = self.paths.root / name
        run.mkdir()
        (run / f"travel-scanner-{name}-abc.dump").write_bytes(b"PGDMP" * 10)
        if manifest:
            (run / "manifest.json").write_text("{}")
        return run

    def offsite(self, **kwargs) -> Offsite:
        config = OffsiteConfig(remote=REMOTE, retention=kwargs.pop("retention", 14))
        return Offsite(self.paths, config, self.drive, out=lambda _line: None, **kwargs)

    def last(self) -> dict:
        return json.loads(self.paths.last.read_text())

    def test_uploads_missing_runs_oldest_first_manifest_last_then_checks(self) -> None:
        self.make_run("20261110T201700Z")
        self.make_run("20261111T201700Z")
        self.assertEqual(self.offsite().run(), 0)
        copies = [(c[1], "--include" in c) for c in self.drive.commands if c[0] == "copy"]
        self.assertEqual(
            copies,
            [
                ("/runs/20261110T201700Z", False),
                ("/runs/20261110T201700Z", True),
                ("/runs/20261111T201700Z", False),
                ("/runs/20261111T201700Z", True),
            ],
        )
        self.assertEqual(sum(1 for c in self.drive.commands if c[0] == "check"), 2)
        self.assertEqual(
            self.last()["offsite"]["uploaded"], ["20261110T201700Z", "20261111T201700Z"]
        )
        self.assertEqual(self.last()["offsite"]["remote"], REMOTE)

    def test_skips_runs_already_on_drive_and_partial_runs(self) -> None:
        self.make_run("20261110T201700Z")
        self.make_run("20261111T201700Z")
        self.make_run("20261112T201700Z.partial")
        self.make_run("20261112T201800Z", manifest=False)
        self.drive.files["20261110T201700Z"] = {
            "manifest.json",
            "travel-scanner-20261110T201700Z-abc.dump",
        }
        self.assertEqual(self.offsite().run(), 0)
        self.assertEqual(self.last()["offsite"]["uploaded"], ["20261111T201700Z"])

    def test_a_run_without_its_manifest_on_drive_is_uploaded_again(self) -> None:
        self.make_run("20261110T201700Z")
        self.drive.files["20261110T201700Z"] = {"travel-scanner-20261110T201700Z-abc.dump"}
        self.assertEqual(self.offsite().run(), 0)
        self.assertEqual(self.last()["offsite"]["uploaded"], ["20261110T201700Z"])

    def test_retention_purges_the_oldest_after_success(self) -> None:
        for day in range(10, 14):
            self.make_run(f"202611{day}T201700Z")
        self.assertEqual(self.offsite(retention=2).run(), 0)
        self.assertEqual(sorted(self.drive.files), ["20261112T201700Z", "20261113T201700Z"])
        self.assertEqual(self.last()["offsite"]["pruned"], ["20261110T201700Z", "20261111T201700Z"])

    def test_a_failed_check_records_a_failure_and_prunes_nothing(self) -> None:
        self.make_run("20261110T201700Z")
        self.drive.files["20261101T201700Z"] = {"manifest.json"}
        self.drive.fail = "check"
        self.assertEqual(self.offsite(retention=1).run(), 1)
        self.assertNotIn("offsite", self.last())
        self.assertEqual(self.last()["offsite_failure"]["stage"], "check")
        self.assertFalse(any(c[0] == "purge" for c in self.drive.commands))

    def test_dry_run_sends_nothing_and_writes_no_state(self) -> None:
        self.make_run("20261110T201700Z")
        self.assertEqual(self.offsite(dry_run=True).run(), 0)
        self.assertEqual({c[0] for c in self.drive.commands}, {"lsf"})
        self.assertFalse(self.paths.last.exists())

    def test_other_list_errors_still_fail(self) -> None:
        self.make_run("20261110T201700Z")
        self.drive.fail = "lsf"
        self.assertEqual(self.offsite().run(), 1)
        self.assertEqual(self.last()["offsite_failure"]["stage"], "list")

    def test_nothing_to_do_and_disabled(self) -> None:
        self.assertEqual(self.offsite().run(), 0)
        self.assertEqual(self.drive.commands, [])
        self.make_run("20261110T201700Z")
        disabled = Offsite(self.paths, OffsiteConfig(remote=""), self.drive, out=lambda _line: None)
        self.assertEqual(disabled.run(), 0)
        self.assertEqual(self.drive.commands, [])

    def test_rclone_runs_in_the_worker_image_with_the_runs_read_only(self) -> None:
        calls = []

        class Recorder:
            def run(self, args, *, timeout=60, output_path=None, input_path=None):
                calls.append(list(args))
                return Completed(0, "")

        Offsite(self.paths, OffsiteConfig(), Recorder(), out=lambda _line: None).rclone(
            ["lsf", "x:"], stage="list"
        )
        argv = calls[0]
        self.assertEqual(argv[:3], ["docker", "run", "--rm"])
        self.assertIn(f"{self.paths.root}:/runs:ro", argv)
        self.assertIn("/etc/travel-scanner/rclone-videos:/conf:ro", argv)
        self.assertIn("travel-scanner-video-worker:local", argv)
        self.assertEqual(argv[-2:], ["lsf", "x:"])

    def test_config(self) -> None:
        self.assertEqual(OffsiteConfig.from_mapping({}).remote, REMOTE)
        self.assertEqual(OffsiteConfig.from_mapping({"OFFSITE_REMOTE": ""}).remote, "")
        self.assertEqual(OffsiteConfig.from_mapping({"OFFSITE_RETENTION": "30"}).retention, 30)
        for bad in (
            {"OFFSITE_REMOTE": "no-colon"},
            {"OFFSITE_REMOTE": "videobackup:"},
            {"OFFSITE_RETENTION": "0"},
            {"OFFSITE_RETENTION": "x"},
        ):
            with self.assertRaises(ConfigError):
                OffsiteConfig.from_mapping(bad)

    def test_main_reads_the_env_file(self) -> None:
        self.paths.env_file.write_text("OFFSITE_RETENTION=nope\n")
        self.assertEqual(offsite.main(["run"], paths=self.paths, runner=self.drive), 2)
        self.paths.env_file.write_text("OFFSITE_REMOTE=\n")
        with redirect_stdout(io.StringIO()) as out:
            self.assertEqual(offsite.main(["run"], paths=self.paths, runner=self.drive), 0)
        self.assertIn("disabled", out.getvalue())


if __name__ == "__main__":
    unittest.main()
