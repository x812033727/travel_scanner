"""Tests for the nightly backup. Run from the repository root:

    python -m unittest discover -s ops/backup -v

A temporary directory stands in for the host and a fake runner for every command, so
nothing here needs the host, root, Docker or age; the module must keep passing on Windows.
"""

from __future__ import annotations

import datetime as dt
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import backup
from backup import Backup, Completed, Config, ConfigError, Paths

SHA = "c" * 40
NOW = dt.datetime(2026, 10, 7, 20, 17, tzinfo=dt.UTC)
STAMP = "20261007T201700Z"


class FakeRunner:
    """Answers commands by the first matching fragment; `output_path` gets the output bytes."""

    def __init__(self, responses: dict[str, Completed]) -> None:
        self.responses = dict(responses)
        self.calls: list[list[str]] = []
        self.inputs: list[Path] = []

    def run(self, args, *, timeout=60, output_path=None, input_path=None):
        self.calls.append(list(args))
        joined = " ".join(str(a) for a in args)
        for fragment in self.responses:
            if fragment in joined:
                break
        else:
            raise AssertionError(f"unexpected command: {joined}")
        response = self.responses[fragment]
        if input_path is not None:
            self.inputs.append(Path(input_path))
        if output_path is not None:
            Path(output_path).write_bytes(response.output.encode("utf-8"))
            return Completed(response.code, "")
        if joined.startswith("age "):
            Path(args[args.index("-o") + 1]).write_bytes(
                b"AGE-ENCRYPTED\n" + response.output.encode()
            )
        return response

    def ran(self, fragment: str) -> bool:
        return any(fragment in " ".join(map(str, call)) for call in self.calls)


def good_runner(**overrides: Completed) -> FakeRunner:
    responses = {
        "flock -n": Completed(0, ""),
        "rev-parse HEAD": Completed(0, SHA + "\n"),
        "alembic_version": Completed(0, "0071_video_media\n"),
        "SELECT version()": Completed(0, "PostgreSQL 17.6 on x86_64\n"),
        "pg_dump": Completed(0, "PGDMP-fake-dump-bytes"),
        "pg_restore --list": Completed(0, ";\n; Archive created\n"),
        "redis-cli SAVE": Completed(0, "REDIS0011fake"),
        "age -r": Completed(0, ""),
    }
    responses.update(overrides)
    return FakeRunner(responses)


class BackupCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.paths = Paths(
            repo=root / "repo",
            root=root / "nightly",
            state_dir=root / "state",
            env_file=root / "backup.env",
            lock=root / "deploy.lock",
            predeploy_dir=root / "rootdir",
            manifest_paths=root / "manifest-paths.txt",
        )
        self.paths.predeploy_dir.mkdir()
        self.secrets = root / "etc"
        self.secrets.mkdir()
        (self.secrets / "runtime.env").write_text("SECRET=1\n", encoding="utf-8")
        self.paths.manifest_paths.write_text(
            f"# host files\n{self.secrets / 'runtime.env'}\n{root / 'missing.env'}\n",
            encoding="utf-8",
        )
        self.lines: list[str] = []

    def backup(self, runner: FakeRunner, *, dry_run: bool = False, **config) -> Backup:
        return Backup(
            Config(**config),
            self.paths,
            runner=runner,
            clock=lambda: NOW,
            dry_run=dry_run,
            out=self.lines.append,
        )

    def last(self) -> dict:
        return json.loads(self.paths.last.read_text(encoding="utf-8"))

    def manifest(self) -> dict:
        return json.loads((self.paths.root / STAMP / "manifest.json").read_text(encoding="utf-8"))

    # -- the happy path --------------------------------------------------------

    def test_run_dumps_verifies_and_records(self) -> None:
        runner = good_runner()
        self.assertEqual(self.backup(runner, age_recipient="age1" + "q" * 58).run(), 0)
        run_dir = self.paths.root / STAMP
        self.assertTrue(run_dir.is_dir())
        self.assertFalse((self.paths.root / f"{STAMP}.partial").exists())
        dump = run_dir / f"travel-scanner-{STAMP}-{SHA[:12]}.dump"
        self.assertEqual(dump.read_bytes(), b"PGDMP-fake-dump-bytes")
        self.assertEqual(
            [p.name for p in runner.inputs], [dump.name]
        )  # pg_restore --list read the dump
        manifest = self.manifest()
        self.assertEqual(manifest["git_sha"], SHA)
        self.assertEqual(manifest["alembic_revision"], "0071_video_media")
        self.assertIn("PostgreSQL 17.6", manifest["postgres_version"])
        names = {item["name"]: item for item in manifest["files"]}
        self.assertEqual(names[dump.name]["sha256"], backup.sha256_of(dump))
        self.assertEqual(names[dump.name]["kind"], "database")
        self.assertIn("config.tar.age", names)
        self.assertTrue(manifest["config"]["encrypted"])
        self.assertEqual(manifest["config"]["included"], [str(self.secrets / "runtime.env")])
        self.assertEqual(len(manifest["config"]["missing"]), 1)
        self.assertNotIn("redis.rdb", names)
        last = self.last()["last_success"]
        self.assertEqual(last["path"], str(run_dir))
        self.assertEqual(last["at"], "2026-10-07T20:17:00+00:00")
        self.assertEqual(sorted(last["files"]), sorted(names))
        self.assertNotIn("SECRET", json.dumps(self.last()) + json.dumps(manifest))

    def test_plain_config_tar_never_lands_in_the_run_directory(self) -> None:
        seen: dict[str, object] = {}

        class Runner(FakeRunner):
            def run(self, args, *, timeout=60, output_path=None, input_path=None):
                if args and args[0] == "age":
                    plain = Path(args[-1])
                    seen["plain"] = plain
                    seen["mode"] = oct(plain.parent.stat().st_mode & 0o777)
                    seen["inside_run_dir"] = str(plain).startswith(str(self.paths_root))
                return super().run(
                    args, timeout=timeout, output_path=output_path, input_path=input_path
                )

        runner = Runner(good_runner().responses)
        runner.paths_root = self.paths.root  # type: ignore[attr-defined]
        self.backup(runner, age_recipient="age1" + "q" * 58).run()
        self.assertFalse(seen["inside_run_dir"])
        self.assertFalse(Path(seen["plain"]).exists())  # removed in finally
        if os.name == "posix":
            self.assertEqual(seen["mode"], "0o700")
        self.assertEqual(list((self.paths.root / STAMP).glob("config.tar")), [])

    def test_without_recipient_the_bundle_is_not_kept(self) -> None:
        runner = good_runner()
        self.assertEqual(self.backup(runner).run(), 0)
        self.assertFalse(runner.ran("age -r"))
        self.assertEqual(list((self.paths.root / STAMP).glob("config.*")), [])
        self.assertFalse(self.manifest()["config"]["kept"])

    def test_redis_is_optional(self) -> None:
        runner = good_runner()
        self.assertEqual(self.backup(runner, include_redis=True).run(), 0)
        self.assertEqual((self.paths.root / STAMP / "redis.rdb").read_bytes(), b"REDIS0011fake")
        self.assertIn("redis.rdb", self.last()["last_success"]["files"])

    # -- failures --------------------------------------------------------------

    def test_empty_dump_fails_and_removes_the_partial_run(self) -> None:
        runner = good_runner(pg_dump=Completed(0, ""))
        self.assertEqual(self.backup(runner).run(), 1)
        self.assertEqual(list(self.paths.root.iterdir()), [])
        failure = self.last()["last_failure"]
        self.assertEqual(failure["stage"], "database")
        self.assertIn("empty", failure["reason"])
        self.assertNotIn("last_success", self.last())

    def test_unlistable_dump_fails(self) -> None:
        runner = good_runner(
            **{
                "pg_restore --list": Completed(
                    1, "pg_restore: error: input file does not appear to be a valid archive"
                )
            }
        )
        self.assertEqual(self.backup(runner).run(), 1)
        self.assertIn("valid archive", self.last()["last_failure"]["reason"])
        self.assertEqual(list(self.paths.root.iterdir()), [])

    def test_age_failure_fails_the_run(self) -> None:
        runner = good_runner(**{"age -r": Completed(1, "age: error: no such recipient")})

        class Runner(FakeRunner):
            def run(self, args, *, timeout=60, output_path=None, input_path=None):
                if args and args[0] == "age":
                    self.calls.append(list(args))
                    return Completed(1, "age: error")
                return super().run(
                    args, timeout=timeout, output_path=output_path, input_path=input_path
                )

        self.assertEqual(
            self.backup(Runner(runner.responses), age_recipient="age1" + "q" * 58).run(), 1
        )
        self.assertEqual(self.last()["last_failure"]["stage"], "config")
        self.assertEqual(list(self.paths.root.iterdir()), [])

    def test_held_deploy_lock_skips(self) -> None:
        runner = good_runner(**{"flock -n": Completed(1, "")})
        self.assertEqual(self.backup(runner).run(), backup.SKIPPED_EXIT)
        self.assertFalse(runner.ran("pg_dump"))
        self.assertEqual(self.last()["last_skipped"]["reason"], "deploy lock held")
        self.assertFalse(self.paths.root.exists())

    # -- predeploy sweep -------------------------------------------------------

    def test_predeploy_dumps_newer_than_the_last_success_are_swept(self) -> None:
        old = self.paths.predeploy_dir / "travel_scanner_predeploy_20261001.dump"
        new = self.paths.predeploy_dir / "travel_scanner_predeploy_20261007.dump"
        old.write_bytes(b"PGDMP-old")
        new.write_bytes(b"PGDMP-new")
        old_time = (NOW - dt.timedelta(days=6)).timestamp()
        os.utime(old, (old_time, old_time))
        backup.write_json(
            self.paths.last, {"last_success": {"at": _iso(NOW - dt.timedelta(days=1))}}
        )
        runner = good_runner()
        self.assertEqual(self.backup(runner).run(), 0)
        files = {item["name"]: item for item in self.manifest()["files"]}
        self.assertIn(new.name, files)
        self.assertEqual(files[new.name]["kind"], "predeploy")
        self.assertNotIn(old.name, files)
        self.assertEqual(len(runner.inputs), 2)  # both dumps were listed
        self.assertTrue(new.exists())  # the original stays where the deploy script put it

    def test_first_run_sweeps_every_predeploy_dump(self) -> None:
        (self.paths.predeploy_dir / "travel_scanner_predeploy_1.dump").write_bytes(b"PGDMP-1")
        self.assertEqual(self.backup(good_runner()).run(), 0)
        self.assertIn("travel_scanner_predeploy_1.dump", self.last()["last_success"]["files"])

    # -- retention -------------------------------------------------------------

    def test_retention_keeps_the_newest_complete_runs_only(self) -> None:
        self.paths.root.mkdir(parents=True)
        for day in range(1, 9):
            (self.paths.root / f"202609{day:02d}T201700Z").mkdir()
        (self.paths.root / "20260901T000000Z.partial").mkdir()
        stale = self.paths.root / "20260901T000000Z.partial"
        old_time = (NOW - dt.timedelta(days=3)).timestamp()
        os.utime(stale, (old_time, old_time))
        (self.paths.root / "notes.txt").write_text("keep me", encoding="utf-8")
        self.assertEqual(self.backup(good_runner(), local_retention=3).run(), 0)
        remaining = sorted(p.name for p in self.paths.root.iterdir())
        self.assertEqual(remaining, ["20260907T201700Z", "20260908T201700Z", STAMP, "notes.txt"])

    def test_retention_is_not_applied_after_a_failure(self) -> None:
        self.paths.root.mkdir(parents=True)
        for day in range(1, 9):
            (self.paths.root / f"202609{day:02d}T201700Z").mkdir()
        self.assertEqual(
            self.backup(good_runner(pg_dump=Completed(0, "")), local_retention=3).run(), 1
        )
        self.assertEqual(len(list(self.paths.root.iterdir())), 8)

    # -- dry run ---------------------------------------------------------------

    def test_dry_run_writes_nothing(self) -> None:
        (self.paths.predeploy_dir / "travel_scanner_predeploy_2.dump").write_bytes(b"x")
        runner = good_runner()
        self.assertEqual(self.backup(runner, dry_run=True).run(), 0)
        self.assertEqual([c for c in runner.calls if c[0] != "flock"], [])
        self.assertFalse(self.paths.root.exists())
        self.assertFalse(self.paths.last.exists())
        joined = "\n".join(self.lines)
        self.assertIn("travel_scanner_predeploy_2.dump", joined)
        self.assertIn("1 path(s) present, 1 missing", joined)
        self.assertIn("would not be kept", joined)


class ConfigCase(unittest.TestCase):
    def test_env_parsing_and_validation(self) -> None:
        config = Config.from_mapping(
            {
                "BACKUP_INCLUDE_REDIS": "true",
                "BACKUP_LOCAL_RETENTION": "10",
                "BACKUP_AGE_RECIPIENT": "age1abc",
            }
        )
        self.assertEqual(
            (config.include_redis, config.local_retention, config.age_recipient),
            (True, 10, "age1abc"),
        )
        self.assertEqual(Config.from_mapping({}), Config())
        for env in (
            {"BACKUP_LOCAL_RETENTION": "0"},
            {"BACKUP_LOCAL_RETENTION": "seven"},
            {"BACKUP_AGE_RECIPIENT": "ssh-ed25519 AAAA"},
        ):
            with self.subTest(env=env), self.assertRaises(ConfigError):
                Config.from_mapping(env)

    def test_manifest_paths_must_be_absolute(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest-paths.txt"
            path.write_text("# c\n/etc/a\n\n/root/b\n", encoding="utf-8")
            self.assertEqual(backup.read_manifest_paths(path), [Path("/etc/a"), Path("/root/b")])
            path.write_text("etc/a\n", encoding="utf-8")
            with self.assertRaises(ConfigError):
                backup.read_manifest_paths(path)
            self.assertEqual(backup.read_manifest_paths(Path(tmp) / "none.txt"), [])


class StatusCase(unittest.TestCase):
    def test_status_verdicts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = Paths(state_dir=Path(tmp))
            text, code = backup.status_text(paths, now=NOW)
            self.assertEqual(code, 1)
            self.assertIn("last success: never", text)
            backup.write_json(
                paths.last,
                {
                    "last_success": {
                        "at": _iso(NOW - dt.timedelta(hours=5)),
                        "bytes": 10,
                        "files": ["a"],
                        "path": "/p",
                    }
                },
            )
            text, code = backup.status_text(paths, now=NOW)
            self.assertEqual(code, 0)
            self.assertIn("5.0 h ago", text)
            backup.write_json(
                paths.last,
                {"last_success": {"at": _iso(NOW - dt.timedelta(hours=40)), "files": []}},
            )
            text, code = backup.status_text(paths, now=NOW)
            self.assertEqual(code, 1)
            self.assertIn("BACKUP STALE", text)
            backup.write_json(
                paths.last,
                {
                    "last_success": {"at": _iso(NOW - dt.timedelta(hours=30)), "files": []},
                    "last_failure": {
                        "at": _iso(NOW - dt.timedelta(hours=6)),
                        "stage": "dump",
                        "reason": "boom",
                    },
                },
            )
            text, code = backup.status_text(paths, now=NOW)
            self.assertEqual(code, 1)
            self.assertIn("BACKUP FAILED: dump: boom", text)
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(backup.main(["status"], paths=paths), 1)
            self.assertIn("BACKUP FAILED", out.getvalue())
            self.assertEqual(backup.main(["run"], paths=paths), 2)  # no env file
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(backup.main(["status", "--state-dir", tmp]), 1)
            self.assertIn("BACKUP FAILED", out.getvalue())


def _iso(instant: dt.datetime) -> str:
    return instant.replace(microsecond=0).isoformat()


if __name__ == "__main__":
    unittest.main()
