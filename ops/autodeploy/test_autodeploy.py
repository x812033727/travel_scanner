"""Tests for the auto deploy poller. Run from the repository root:

    python -m unittest discover -s ops/autodeploy -v

A temporary directory stands in for the host, a fake runner for every command and a fake
client for GitHub, so nothing here needs the host, root, Docker or the network; the
module must keep passing on Windows.
"""

from __future__ import annotations

import datetime as dt
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import autodeploy  # noqa: E402
from autodeploy import Completed, Config, ConfigError, Decision, Paths, Poller, Window  # noqa: E402

LIVE = "a" * 40
TARGET = "b" * 40
NOW = dt.datetime(2026, 10, 7, 3, 0, tzinfo=dt.UTC)  # 11:00 in Taipei
OLD_ENOUGH = int((NOW - dt.timedelta(hours=1)).timestamp())
VERIFY_TEMPLATE = '#!/usr/bin/env bash\nEXPECTED_SHA=""\necho "== verify =="\n'


class FakeRunner:
    """Answers commands by the first matching fragment of their joined arguments."""

    def __init__(self, responses: dict[str, Completed]) -> None:
        self.responses = dict(responses)
        self.calls: list[list[str]] = []

    def run(self, args, *, timeout=60, log_path=None):
        self.calls.append(list(args))
        joined = " ".join(str(a) for a in args)
        for fragment in self.responses:
            if fragment in joined:
                break
        else:
            raise AssertionError(f"unexpected command: {joined}")
        response = self.responses[fragment]
        if log_path is not None:
            Path(log_path).write_text(response.output, encoding="utf-8")
        return response

    def ran(self, fragment: str) -> bool:
        return any(fragment in " ".join(call) for call in self.calls)


class FakeGitHub:
    def __init__(self, status: str = "success", url: str | None = "https://ci/1") -> None:
        self.status = status
        self.url = url
        self.asked: list[str] = []

    def ci_status(self, sha: str):
        self.asked.append(sha)
        return self.status, self.url


class FakeNotifier:
    def __init__(self) -> None:
        self.posts: list[str] = []

    def post(self, text: str) -> bool:
        self.posts.append(text)
        return True


def green_runner(**overrides: Completed) -> FakeRunner:
    """Every gate open: a new green commit, lock free, dry-run allows, no paid work."""
    responses = {
        "fetch": Completed(0, ""),
        "rev-parse HEAD": Completed(0, LIVE + "\n"),
        "rev-parse refs/remotes/origin/main": Completed(0, TARGET + "\n"),
        "merge-base --is-ancestor": Completed(0, ""),
        "log -1 --format=%ct": Completed(0, f"{OLD_ENOUGH}\n"),
        "flock -n": Completed(0, ""),
        "--dry-run": Completed(0, "would deploy\n"),
        "psql": Completed(0, ""),
        "bash ": Completed(0, "== verify ==\nPASS a\nPASS b\nTOTAL pass=2 fail=0\n== end ==\n"),
        "deploy-travel-scanner.sh": Completed(0, "deployed\n"),
    }
    responses.update(overrides)
    return FakeRunner(responses)


class PollerCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.paths = Paths(
            repo=root / "repo",
            deploy_script=root / "deploy-travel-scanner.sh",
            verify_script=root / "host-verify.sh",
            lock=root / "deploy.lock",
            log_dir=root / "deploy-logs",
            state_dir=root / "state",
            paused=root / "autodeploy.paused",
            env_file=root / "autodeploy.env",
        )
        self.paths.verify_script.write_text(VERIFY_TEMPLATE, encoding="utf-8")
        self.github = FakeGitHub()
        self.notifier = FakeNotifier()
        self.lines: list[str] = []

    def poller(
        self, runner: FakeRunner, *, enabled: bool = True, dry_run: bool = False, **config
    ) -> Poller:
        return Poller(
            Config(enabled=enabled, github_token="t" * 40, **config),
            self.paths,
            runner=runner,
            github=self.github,
            notifier=self.notifier,
            clock=lambda: NOW,
            dry_run=dry_run,
            out=self.lines.append,
        )

    def state(self) -> dict:
        return json.loads(self.paths.state.read_text(encoding="utf-8"))

    # -- gates -----------------------------------------------------------------

    def test_paused_file_stops_everything(self) -> None:
        autodeploy.write_paused(
            self.paths.paused, sha=TARGET, exit_code=1, log=Path("/x.log"), instant=NOW
        )
        runner = green_runner()
        decision = self.poller(runner).tick()
        self.assertEqual(decision.action, "paused")
        self.assertIn("exited 1", decision.reason)
        self.assertEqual(runner.calls, [])
        self.assertEqual(self.state()["last_decision"]["action"], "paused")

    def test_nothing_new_is_idle(self) -> None:
        runner = green_runner(**{"rev-parse refs/remotes/origin/main": Completed(0, LIVE + "\n")})
        decision = self.poller(runner).tick()
        self.assertEqual(decision.action, "idle")
        self.assertFalse(runner.ran("deploy-travel-scanner.sh"))
        self.assertEqual(self.github.asked, [])

    def test_fetch_failure_waits(self) -> None:
        runner = green_runner(fetch=Completed(128, "fatal: unable to access\n"))
        decision = self.poller(runner).tick()
        self.assertEqual((decision.action, decision.details["gate"]), ("wait", "fetch"))
        self.assertIn("unable to access", decision.reason)

    def test_diverged_live_waits_for_a_person(self) -> None:
        runner = green_runner(**{"merge-base --is-ancestor": Completed(1, "")})
        decision = self.poller(runner).tick()
        self.assertEqual((decision.action, decision.details["gate"]), ("wait", "git"))
        self.assertIn("not an ancestor", decision.reason)

    def test_quiet_period_waits(self) -> None:
        recent = int((NOW - dt.timedelta(minutes=5)).timestamp())
        runner = green_runner(**{"log -1 --format=%ct": Completed(0, f"{recent}\n")})
        decision = self.poller(runner, quiet_minutes=20).tick()
        self.assertEqual((decision.action, decision.details["gate"]), ("wait", "quiet"))
        self.assertIn("16 min to go", decision.reason)
        self.assertEqual(self.github.asked, [])

    def test_ci_pending_failed_or_missing_waits(self) -> None:
        for status in ("in_progress", "failure", "missing", "unreachable (URLError)"):
            with self.subTest(status=status):
                self.github.status = status
                runner = green_runner()
                decision = self.poller(runner).tick()
                self.assertEqual((decision.action, decision.details["gate"]), ("wait", "ci"))
                self.assertIn(status, decision.reason)
                self.assertFalse(runner.ran("--dry-run"))

    def test_blocked_window_waits(self) -> None:
        windows = autodeploy.parse_windows("10:30-12:00")
        decision = self.poller(green_runner(), blocked_windows=tuple(windows)).tick()
        self.assertEqual((decision.action, decision.details["gate"]), ("wait", "window"))
        self.assertIn("10:30-12:00", decision.reason)
        self.assertIn("now 11:00", decision.reason)

    def test_window_wrapping_midnight(self) -> None:
        window = Window(23 * 60, 1 * 60)
        self.assertTrue(window.contains(dt.datetime(2026, 1, 1, 23, 30, tzinfo=autodeploy.TAIPEI)))
        self.assertTrue(window.contains(dt.datetime(2026, 1, 1, 0, 30, tzinfo=autodeploy.TAIPEI)))
        self.assertFalse(window.contains(dt.datetime(2026, 1, 1, 1, 0, tzinfo=autodeploy.TAIPEI)))
        self.assertFalse(window.contains(dt.datetime(2026, 1, 1, 12, 0, tzinfo=autodeploy.TAIPEI)))

    def test_held_lock_waits(self) -> None:
        runner = green_runner(**{"flock -n": Completed(1, "")})
        decision = self.poller(runner).tick()
        self.assertEqual((decision.action, decision.details["gate"]), ("wait", "lock"))
        self.assertFalse(runner.ran("--dry-run"))

    def test_script_refusal_waits_with_its_reason(self) -> None:
        refusal = "NOT DEPLOYING: another release is in progress\ncodex-gemini 正在發布 3b8df68c\n"
        runner = green_runner(**{"--dry-run": Completed(3, refusal)})
        decision = self.poller(runner).tick()
        self.assertEqual((decision.action, decision.details["gate"]), ("wait", "hold"))
        self.assertIn("正在發布", decision.reason)
        self.assertFalse(runner.ran("psql"))

    def test_other_dry_run_failure_waits(self) -> None:
        runner = green_runner(**{"--dry-run": Completed(1, "cd: no such directory\n")})
        decision = self.poller(runner).tick()
        self.assertEqual((decision.action, decision.details["gate"]), ("wait", "dry-run"))

    def test_running_paid_work_waits_and_remembers_since_when(self) -> None:
        running = Completed(0, "running|1|2026-10-07 02:00:00\n")
        decision = self.poller(green_runner(psql=running)).tick()
        self.assertEqual((decision.action, decision.details["gate"]), ("wait", "paid_work"))
        self.assertEqual(self.state()["paid_work_since"], "2026-10-07T03:00:00+00:00")
        self.assertEqual(self.notifier.posts, [])
        # Three hours later the job is still running: one notification, the start time kept.
        later = NOW + dt.timedelta(hours=3)
        poller = self.poller(green_runner(psql=running), paid_work_notify_hours=2)
        poller.clock = lambda: later
        poller.tick()
        self.assertEqual(self.state()["paid_work_since"], "2026-10-07T03:00:00+00:00")
        self.assertEqual(len(self.notifier.posts), 1)
        self.assertIn("3.0 h", self.notifier.posts[0])
        poller = self.poller(green_runner(psql=running), paid_work_notify_hours=2)
        poller.clock = lambda: later + dt.timedelta(minutes=5)
        poller.tick()
        self.assertEqual(len(self.notifier.posts), 1)
        # The job settles: the deploy goes ahead and the wait is forgotten.
        decision = self.poller(green_runner()).tick()
        self.assertEqual(decision.action, "deployed")
        self.assertNotIn("paid_work_since", self.state())

    def test_submitted_media_jobs_are_printed_not_waited_for(self) -> None:
        def psql(args):
            return (
                "submitted|2|2026-10-07 01:00:00\n" if "video_media_jobs" in " ".join(args) else ""
            )

        class Runner(FakeRunner):
            def run(self, args, *, timeout=60, log_path=None):
                if "psql" in " ".join(str(a) for a in args):
                    self.calls.append(list(args))
                    return Completed(0, psql(args))
                return super().run(args, timeout=timeout, log_path=log_path)

        runner = Runner(green_runner().responses)
        decision = self.poller(runner).tick()
        self.assertEqual(decision.action, "deployed")
        self.assertTrue(any("media jobs: submitted|2" in line for line in self.lines))

    def test_paid_work_gate_can_be_switched_off(self) -> None:
        runner = green_runner(psql=Completed(0, "running|1|x\n"))
        decision = self.poller(runner, wait_for_paid_work=False).tick()
        self.assertEqual(decision.action, "deployed")
        self.assertFalse(runner.ran("psql"))

    # -- dry run ---------------------------------------------------------------

    def test_disabled_walks_every_gate_and_deploys_nothing(self) -> None:
        runner = green_runner()
        decision = self.poller(runner, enabled=False).tick()
        self.assertEqual(decision.action, "would_deploy")
        self.assertEqual(decision.details["sha"], TARGET)
        self.assertTrue(runner.ran("--dry-run"))
        self.assertTrue(runner.ran("psql"))
        self.assertEqual([c for c in runner.calls if c == [str(self.paths.deploy_script)]], [])
        self.assertTrue(self.state()["dry_run"])
        self.assertEqual(self.github.asked, [TARGET])

    def test_dry_run_flag_behaves_like_disabled(self) -> None:
        decision = self.poller(green_runner(), dry_run=True).tick()
        self.assertEqual(decision.action, "would_deploy")

    # -- deploy ----------------------------------------------------------------

    def test_deploy_success_verifies_and_records(self) -> None:
        runner = green_runner()
        decision = self.poller(runner).tick()
        self.assertEqual(decision.action, "deployed")
        self.assertIn([str(self.paths.deploy_script)], runner.calls)
        last = self.state()["last_deploy"]
        self.assertEqual((last["sha"], last["previous"], last["exit"]), (TARGET, LIVE, 0))
        self.assertEqual(
            last["verify"], {"result": "PASS", "pass": 2, "fail": 0, "log": last["verify"]["log"]}
        )
        self.assertTrue(Path(last["log"]).name.startswith("auto-20261007_030000"))
        self.assertTrue(Path(last["log"]).read_text(encoding="utf-8").startswith("deployed"))
        self.assertFalse(self.paths.paused.exists())
        self.assertEqual(len(self.notifier.posts), 1)
        self.assertIn("verify PASS", self.notifier.posts[0])
        self.assertFalse(self.state()["dry_run"])
        self.assertEqual(self.state()["last_decision"]["action"], "deployed")

    def test_verify_script_gets_the_sha_and_is_removed(self) -> None:
        seen: dict[str, str] = {}

        class Runner(FakeRunner):
            def run(self, args, *, timeout=60, log_path=None):
                if args[0] == "bash":
                    seen["script"] = Path(args[1]).read_text(encoding="utf-8")
                    seen["path"] = args[1]
                return super().run(args, timeout=timeout, log_path=log_path)

        self.poller(Runner(green_runner().responses)).tick()
        self.assertIn(f'EXPECTED_SHA="{TARGET}"', seen["script"])
        self.assertFalse(Path(seen["path"]).exists())

    def test_verify_failure_is_recorded_as_fail(self) -> None:
        runner = green_runner(**{"bash ": Completed(0, "FAIL x\nTOTAL pass=3 fail=1\n")})
        decision = self.poller(runner).tick()
        self.assertEqual(decision.action, "deployed")
        self.assertEqual(self.state()["last_deploy"]["verify"]["result"], "FAIL")
        self.assertIn("verify FAIL", decision.reason)
        self.assertFalse(self.paths.paused.exists())

    def test_missing_verify_script_is_skipped_not_fatal(self) -> None:
        self.paths.verify_script.unlink()
        decision = self.poller(green_runner()).tick()
        self.assertEqual(decision.action, "deployed")
        self.assertEqual(self.state()["last_deploy"]["verify"]["result"], "SKIPPED")

    def test_deploy_failure_writes_the_paused_file(self) -> None:
        runner = green_runner(
            **{"deploy-travel-scanner.sh": Completed(1, "health check failed\nrolled back\n")}
        )
        decision = self.poller(runner).tick()
        self.assertEqual(decision.action, "failed")
        self.assertFalse(runner.ran("bash "))
        first, record = autodeploy.read_paused(self.paths.paused)
        self.assertIn(TARGET[:12], first)
        self.assertIn("exited 1", first)
        self.assertLessEqual(len(first.encode("utf-8")), autodeploy.FIRST_LINE_LIMIT)
        self.assertEqual((record["sha"], record["exit"]), (TARGET, 1))
        self.assertEqual(record["created_at"], "2026-10-07T03:00:00+00:00")
        self.assertTrue(
            Path(record["log"]).read_text(encoding="utf-8").startswith("health check failed")
        )
        self.assertEqual(len(self.notifier.posts), 1)
        self.assertIn("FAILED", self.notifier.posts[0])
        # The next tick does nothing until a person removes the file.
        runner = green_runner()
        self.assertEqual(self.poller(runner).tick().action, "paused")
        self.assertEqual(runner.calls, [])
        self.paths.paused.unlink()
        self.assertEqual(self.poller(green_runner()).tick().action, "deployed")

    def test_paused_file_has_exactly_two_lines(self) -> None:
        autodeploy.write_paused(
            self.paths.paused, sha=TARGET, exit_code=2, log=Path("/l.log"), instant=NOW
        )
        lines = self.paths.paused.read_text(encoding="utf-8").split("\n")
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[2], "")
        json.loads(lines[1])


class ConfigCase(unittest.TestCase):
    def test_env_file_parsing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "autodeploy.env"
            path.write_text(
                "# comment\n\nAUTODEPLOY_ENABLED=true\nAUTODEPLOY_GITHUB_TOKEN='abc'\n"
                'AUTODEPLOY_BLOCKED_WINDOWS="09:00-12:00, 23:00-01:00"\n'
                "AUTODEPLOY_QUIET_MINUTES=30\n",
                encoding="utf-8",
            )
            config = Config.from_mapping(autodeploy.read_env_file(path))
        self.assertTrue(config.enabled)
        self.assertEqual(config.github_token, "abc")
        self.assertEqual(config.quiet_minutes, 30)
        self.assertEqual([str(w) for w in config.blocked_windows], ["09:00-12:00", "23:00-01:00"])
        self.assertTrue(config.wait_for_paid_work)
        self.assertEqual(config.notify_url, "")

    def test_missing_env_file(self) -> None:
        with self.assertRaises(ConfigError):
            autodeploy.read_env_file(Path("/nonexistent/autodeploy.env"))

    def test_token_is_required(self) -> None:
        with self.assertRaises(ConfigError):
            Config.from_mapping({"AUTODEPLOY_ENABLED": "true"})

    def test_bad_values_are_refused(self) -> None:
        for env in (
            {"AUTODEPLOY_QUIET_MINUTES": "soon"},
            {"AUTODEPLOY_QUIET_MINUTES": "-1"},
            {"AUTODEPLOY_BLOCKED_WINDOWS": "9-12"},
            {"AUTODEPLOY_BLOCKED_WINDOWS": "25:00-26:00"},
            {"AUTODEPLOY_PAID_WORK_NOTIFY_HOURS": "x"},
        ):
            with self.subTest(env=env), self.assertRaises(ConfigError):
                Config.from_mapping({"AUTODEPLOY_GITHUB_TOKEN": "t", **env})

    def test_ci_status_from_payload(self) -> None:
        runs = {
            "workflow_runs": [
                {"name": "pip audit", "status": "completed", "conclusion": "failure"},
                {
                    "name": "CI",
                    "status": "completed",
                    "conclusion": "success",
                    "html_url": "https://ci/9",
                },
            ]
        }
        self.assertEqual(autodeploy.ci_status_from_payload(runs), ("success", "https://ci/9"))
        pending = {"workflow_runs": [{"name": "CI", "status": "in_progress", "html_url": ""}]}
        self.assertEqual(autodeploy.ci_status_from_payload(pending), ("in_progress", None))
        self.assertEqual(
            autodeploy.ci_status_from_payload({"workflow_runs": []}), ("missing", None)
        )


class CliCase(unittest.TestCase):
    def test_status_and_config_error_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = Paths(
                state_dir=root / "state", paused=root / "paused", env_file=root / "autodeploy.env"
            )
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(autodeploy.main(["status"], paths=paths), 0)
            self.assertIn("no tick recorded yet", out.getvalue())
            self.assertIn("paused file: none", out.getvalue())
            autodeploy.write_paused(
                paths.paused, sha=TARGET, exit_code=1, log=Path("/l"), instant=NOW
            )
            out = io.StringIO()
            with redirect_stdout(out):
                autodeploy.main(["status"], paths=paths)
            self.assertIn("PAUSED", out.getvalue())
            paths.env_file.write_text("AUTODEPLOY_ENABLED=true\n", encoding="utf-8")
            self.assertEqual(autodeploy.main(["tick"], paths=paths), 2)

    def test_decision_dataclass_defaults(self) -> None:
        self.assertEqual(Decision("idle", "x").details, {})


if __name__ == "__main__":
    unittest.main()
