"""Disposable Linux tests for the host cutover driver's safety ordering."""

from __future__ import annotations

import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "host_cutover_driver", HERE / "host-cutover-driver.py"
)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def plan(release_dir: str = "/root/mokaair-a01-media-fence-123456abcdef") -> dict:
    digest = "a" * 64
    return {
        "schema_version": 1,
        "pr_head": "1" * 40,
        "target_sha": "2" * 40,
        "old_live_sha": "3" * 40,
        "release_dir": release_dir,
        "require_autodeploy_absent": True,
        "pins": {
            "old_api_id": "4" * 64,
            "old_api_image": "sha256:" + "5" * 64,
            "redis_id": "6" * 64,
            "redis_image": "sha256:" + "7" * 64,
            "worker_id": "8" * 64,
            "worker_image": "sha256:" + "9" * 64,
            "redis_volume": "travel_scanner_redis_data",
            "redis_mount": "/var/lib/docker/volumes/travel_scanner_redis_data/_data",
            "video_work_mount": "/var/lib/docker/volumes/travel_scanner_video_work/_data",
            "api_redis_url_sha256": digest,
            "host_env_sha256": digest,
        },
        "source_sha256": {
            "host-cutover-driver.py": digest,
            "dispatch_fence_cutover.py": digest,
            "install-marker.sh": digest,
            "monitor-lock.sh": digest,
            "manifest.json": module.MARKER_SHA,
            "hold.py": digest,
            "host-cutover-driver.deploy-wrapper.sh": digest,
            "incoming-docker-compose.prod.yml": digest,
            "deploy-travel-scanner.sh": module.PATCHED_DEPLOY_SHA,
            "jobs.py": digest,
            "admin_api.py": digest,
            "cutover_intake.py": digest,
            "dispatch_fence.py": digest,
            "dispatch_fence_cli.py": digest,
        },
    }


class CutoverTest(unittest.TestCase):
    def test_git_preflight_disables_optional_index_locks(self) -> None:
        with patch.object(module.subprocess, "run") as run:
            run.return_value.returncode = 0
            run.return_value.stdout = b""
            module.Command().run(["git", "status", "--porcelain"])
        self.assertEqual(run.call_args.kwargs["env"]["GIT_OPTIONAL_LOCKS"], "0")

    def test_plan_hash_and_exact_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "plan.json"
            data = json.dumps(plan(), sort_keys=True).encode()
            path.write_bytes(data)
            self.assertEqual(
                module.parse_plan(path, module.sha_bytes(data))["target_sha"], "2" * 40
            )
            with self.assertRaisesRegex(module.Stop, "source_hash_drift"):
                module.parse_plan(path, "b" * 64)
            altered = plan()
            altered["pins"]["old_api_id"] = "not-a-container"
            data = json.dumps(altered).encode()
            path.write_bytes(data)
            with self.assertRaisesRegex(module.Stop, "invalid_old_api_id"):
                module.parse_plan(path, module.sha_bytes(data))
            missing_admin_hash = plan()
            del missing_admin_hash["source_sha256"]["admin_api.py"]
            data = json.dumps(missing_admin_hash).encode()
            path.write_bytes(data)
            with self.assertRaisesRegex(module.Stop, "source_hash_keys"):
                module.parse_plan(path, module.sha_bytes(data))

    def test_new_api_b25_receipt_requires_exact_slug_and_route_source(self) -> None:
        sources = {"admin_api.py": "a" * 64}
        proof = {
            "b25_direct_intake": {
                "slug": module.B25_SLUG,
                "compiled_guard": True,
            },
            "code": {"admin_api_sha256": "a" * 64},
        }
        module.verify_b25_direct_receipt(proof, sources)
        with self.assertRaisesRegex(module.Stop, "new_api_b25_direct_intake_guard_missing"):
            module.verify_b25_direct_receipt({**proof, "b25_direct_intake": {}}, sources)
        with self.assertRaisesRegex(module.Stop, "new_api_b25_direct_source_hash_drift"):
            module.verify_b25_direct_receipt({**proof, "code": {}}, sources)

    def test_new_api_paid_intake_receipt_requires_exact_pause_and_source(self) -> None:
        sources = {"cutover_intake.py": "a" * 64}
        proof = {
            "paid_intake": {
                "state": "PAUSED_ALL",
                "plan_sha256": "b" * 64,
                "target_sha": "c" * 40,
                "marker_sha256": "d" * 64,
                "armed_sha256": "e" * 64,
            },
            "code": {"cutover_intake_sha256": "a" * 64},
        }
        module.verify_paid_intake_receipt(proof, sources, "b" * 64, "c" * 40)
        with self.assertRaisesRegex(module.Stop, "new_api_paid_intake_not_paused"):
            module.verify_paid_intake_receipt(
                {**proof, "paid_intake": {**proof["paid_intake"], "state": "BOOTSTRAP_ALLOW"}},
                sources,
                "b" * 64,
                "c" * 40,
            )
        with self.assertRaisesRegex(module.Stop, "new_api_paid_intake_source_hash_drift"):
            module.verify_paid_intake_receipt({**proof, "code": {}}, sources, "b" * 64, "c" * 40)

    def test_dry_run_cannot_enter_apply_path(self) -> None:
        class DryDriver(module.Driver):
            def preflight(self, *, after_hold: bool = False) -> None:
                self.preflight_seen = True

            def acquire_locks(self) -> None:
                raise AssertionError("dry-run acquired locks")

        driver = DryDriver(plan(), "a" * 64, dry_run=True)
        output = io.StringIO()
        with redirect_stdout(output):
            driver.run()
        self.assertTrue(driver.preflight_seen)
        self.assertFalse(json.loads(output.getvalue())["production_ready"])

    def test_apply_stops_before_any_write_without_b25_producer_proof(self) -> None:
        class BlockedDriver(module.Driver):
            def preflight(self, *, after_hold: bool = False) -> None:
                pass

            def acquire_locks(self) -> None:
                raise AssertionError("apply reached host write")

        driver = BlockedDriver(plan(), "a" * 64, dry_run=False)
        with self.assertRaisesRegex(module.Stop, "b25_producer_proof_missing"):
            driver.run()

    def test_global_cutover_missing_proof_stops_before_write(self) -> None:
        class BlockedDriver(module.Driver):
            def preflight(self, *, after_hold: bool = False) -> None:
                pass

            def verify_b25_producer_quiescence(self) -> None:
                pass

            def acquire_locks(self) -> None:
                raise AssertionError("apply reached host write")

        driver = BlockedDriver(plan(), "a" * 64, dry_run=False)
        with self.assertRaisesRegex(
            module.Stop, "global_paid_intake_cutover_proof_missing"
        ):
            driver.run()

    def test_old_api_bootstrap_source_and_marker_proof_is_read_only(self) -> None:
        state = {
            "state": "BOOTSTRAP_ALLOW",
            "bootstrap_id": "b" * 64,
            "marker_sha256": "c" * 64,
            "armed_sha256": None,
            "plan_sha256": None,
            "target_sha": None,
            "nonce_sha256": None,
        }

        class BootstrapDriver(module.Driver):
            def __init__(self) -> None:
                super().__init__(plan(), "a" * 64)
                self.source_drift = False

            def cmd(self, *parts: str, **kwargs: object) -> bytes:
                if parts[:3] == ("git", "-C", str(module.ROOT)):
                    return b"pinned old API bytes"
                if parts[:3] == ("docker", "exec", self.pins["old_api_id"]):
                    if parts[3] == "sha256sum":
                        digest = "0" * 64 if self.source_drift else module.sha_bytes(
                            b"pinned old API bytes"
                        )
                        return f"{digest}  {parts[4]}\n".encode()
                    if parts[3] == "python":
                        return json.dumps(state).encode()
                raise AssertionError(f"unexpected command: {parts}")

        driver = BootstrapDriver()
        driver.check_old_api_gate_bootstrap()
        driver.source_drift = True
        with self.assertRaisesRegex(module.Stop, "old_api_gate_source_drift"):
            driver.check_old_api_gate_bootstrap()
        driver.source_drift = False
        state["state"] = "PAUSED_ALL"
        with self.assertRaisesRegex(module.Stop, "old_api_bootstrap_gate_not_proven"):
            driver.check_old_api_gate_bootstrap()

    def test_locked_preflight_rechecks_full_release_state_before_hold(self) -> None:
        class DriftDriver(module.Driver):
            def __init__(self) -> None:
                super().__init__(plan(), "a" * 64, dry_run=False)
                self.locked = False
                self.surveys: list[tuple[bool, bool]] = []

            def verify_b25_producer_quiescence(self) -> None:
                pass

            def verify_global_pause_cutover_ready(self) -> None:
                pass

            def preflight(self, *, after_hold: bool = False) -> None:
                self.surveys.append((after_hold, self.locked))
                if self.locked:
                    raise module.Stop("locked_release_state_drift")

            def acquire_locks(self) -> None:
                self.locked = True

            def release_locks(self) -> None:
                self.locked = False

        driver = DriftDriver()
        with (
            patch.object(module.os, "geteuid", return_value=0),
            patch.object(module.Path, "read_text", return_value=module.DRIVER_UNIT),
            self.assertRaisesRegex(module.Stop, "locked_release_state_drift"),
        ):
            driver.run()
        self.assertEqual(driver.surveys, [(False, False), (False, True)])

    def test_old_api_stop_is_indefinite_and_rechecks_row(self) -> None:
        class StopDriver(module.Driver):
            def __init__(self, state: dict | None = None) -> None:
                super().__init__(plan(), "a" * 64, dry_run=False)
                self.calls: list[str] = []
                self.stop_state = state or {
                    "Running": False,
                    "Pid": 0,
                    "ExitCode": 0,
                    "OOMKilled": False,
                    "Error": "",
                }

            def event(self, phase: str, **fields: object) -> None:
                self.calls.append(phase)

            def cmd(self, *parts: str, **kwargs: object) -> bytes:
                self.calls.append(" ".join(parts))
                if parts[:3] == ("docker", "container", "stop"):
                    self.assert_timeout_none(kwargs)
                return b""

            @staticmethod
            def assert_timeout_none(kwargs: dict) -> None:
                assert kwargs.get("timeout") is None

            def inspect(self, container: str) -> dict:
                return {"State": self.stop_state}

            def compose(self, *parts: str) -> bytes:
                return b""

            def check_port_binding(self, info: dict, *, stopped: bool) -> None:
                assert stopped

            def check_db(self) -> None:
                self.calls.append("db_rechecked")

            def check_redis(self, *, locked: bool) -> None:
                assert not locked
                self.calls.append("redis_rechecked")

        driver = StopDriver()
        driver.stop_old_api()
        stop = [
            call for call in driver.calls if call.startswith("docker container stop")
        ]
        self.assertEqual(
            stop, [f"docker container stop --signal=SIGTERM --timeout=-1 {'4' * 64}"]
        )
        self.assertLess(driver.calls.index(stop[0]), driver.calls.index("db_rechecked"))
        self.assertLess(
            driver.calls.index("db_rechecked"), driver.calls.index("redis_rechecked")
        )
        for abnormal in ({"ExitCode": 137}, {"OOMKilled": True}, {"Error": "crash"}):
            bad_state = {**driver.stop_state, **abnormal}
            failed = StopDriver(bad_state)
            with self.assertRaisesRegex(module.Stop, "old_api_normal_exit_unproven"):
                failed.stop_old_api()
            self.assertNotIn("db_rechecked", failed.calls)

    def test_watcher_execstart_requires_exact_command(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            driver = module.Driver(plan(temporary), "a" * 64)
            expected = (
                f"argv[]=/bin/bash {temporary}/monitor-lock.sh --receipt "
                f"{temporary}/nonce-receipt.json --redis-container-id {'6' * 64} ;"
            )
            with patch.object(
                driver,
                "cmd",
                return_value=(
                    "{ path=/bin/bash ; " + expected + " ignore_errors=no ; }\n"
                ).encode(),
            ):
                self.assertIn(expected, driver.watcher_execstart())
            with (
                patch.object(
                    driver, "cmd", return_value=b"{ argv[]=/bin/bash /tmp/wrong.sh ; }"
                ),
                self.assertRaisesRegex(module.Stop, "watcher_execstart_drift"),
            ):
                driver.watcher_execstart()

    def test_no_code_path_releases_nonce(self) -> None:
        source = (HERE / "host-cutover-driver.py").read_text(encoding="utf-8")
        self.assertNotIn('"release", input_bytes=', source)
        self.assertNotIn("dispatch_fence_cutover.py release", source)
        self.assertIn('"nonce_retained": True', source)

    def test_stock_guard_candidate_is_exact_and_lf_only(self) -> None:
        candidate = (HERE / "host-cutover-driver.deploy-patched.sh").read_bytes()
        self.assertEqual(module.sha_bytes(candidate), module.PATCHED_DEPLOY_SHA)
        self.assertNotIn(b"\r", candidate)
        self.assertIn(module.DEPLOY_GUARD_MARKER, candidate)
        self.assertIn(b'git merge --ff-only "$REMOTE_SHA"', candidate)
        self.assertIn(b'export RUNTIME_ENV_FILE="$PINNED_ENV_FILE"', candidate)
        self.assertIn(b"assert_pinned_env\n    docker compose --env-file", candidate)
        self.assertIn(b'"${actual_hold%% *}" == "$EXPECTED_HOLD_SHA256"', candidate)

    def test_release_state_requires_autodeploy_units_absent(self) -> None:
        driver = module.Driver(plan(), "a" * 64)
        # CI cannot traverse /root; only the unit-state callback is under test.
        with (
            patch.object(module, "HOLD_PATH", Path("/nonexistent/hold")),
            patch.object(driver, "check_autodeploy_idle") as idle,
            patch.object(module.Path, "exists", return_value=False),
            patch.object(module.Path, "glob", return_value=[]),
        ):
            driver.check_release_state()
        idle.assert_called_once()

    def test_effective_redis_url_must_reach_pinned_server_db_zero(self) -> None:
        url = "redis://:private-pass@redis:6379/0"
        candidate = plan()
        candidate["pins"]["api_redis_url_sha256"] = module.sha_bytes(url.encode())
        driver = module.Driver(candidate, "a" * 64)
        api = {"Id": "4" * 64, "Config": {"Env": [f"REDIS_URL={url}"]}}
        for run_id, database, valid in (
            ("a" * 40, 0, True),
            ("b" * 40, 0, False),
            ("a" * 40, 1, False),
        ):
            with self.subTest(run_id=run_id, database=database):
                proof = json.dumps({"run_id": run_id, "db": database}).encode()
                with (
                    patch.object(
                        driver, "redis_cli", return_value=b"run_id:" + b"a" * 40
                    ),
                    patch.object(driver, "cmd", return_value=proof) as command,
                ):
                    if valid:
                        driver.check_live_redis_url(api, "api")
                    else:
                        with self.assertRaisesRegex(
                            module.Stop, "redis_keyspace_drift"
                        ):
                            driver.check_live_redis_url(api, "api")
                self.assertNotIn("private-pass", repr(command.call_args))

    def test_four_real_flocks_and_exact_hold(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            release = root / "release"
            release.mkdir()
            source = HERE.parents[4] / "ops" / "release" / "hold.py"
            self.assertTrue(source.is_file())
            shutil.copyfile(source, release / "hold.py")
            candidate = plan(str(release))
            candidate["source_sha256"]["hold.py"] = module.sha_bytes(
                source.read_bytes()
            )
            locks = tuple(root / f"lock-{index}" for index in range(4))
            hold_file = root / "deploy.hold"
            with (
                patch.object(module, "LOCKS", locks),
                patch.object(module, "HOLD_PATH", hold_file),
            ):
                driver = module.Driver(candidate, "a" * 64, dry_run=False)
                other = module.Driver(candidate, "a" * 64, dry_run=False)
                driver.acquire_locks()
                self.assertEqual(len(driver.lock_fds), 4)
                self.assertEqual(driver.hold("acquire"), "created")
                self.assertEqual(driver.hold("verify"), "verified")
                with self.assertRaisesRegex(module.Stop, "deploy_lock_held"):
                    other.acquire_locks()
                self.assertTrue(hold_file.exists())
                with self.assertRaisesRegex(
                    module.Stop, "hold_clear_forbidden_during_a01"
                ):
                    driver.hold("clear")
                driver.release_locks()
                other.acquire_locks()
                other.release_locks()
                self.assertTrue(hold_file.exists())

    def test_failed_old_api_stop_keeps_hold(self) -> None:
        class FailureDriver(module.Driver):
            def __init__(self) -> None:
                super().__init__(plan(), "a" * 64, dry_run=False)
                self.steps: list[str] = []

            def preflight(self, *, after_hold: bool = False) -> None:
                pass

            def verify_b25_producer_quiescence(self) -> None:
                pass

            def verify_global_pause_cutover_ready(self) -> None:
                pass

            def acquire_locks(self) -> None:
                self.steps.append("locks")

            def release_locks(self) -> None:
                self.steps.append("unlock")

            def hold(self, action: str) -> str:
                self.steps.append(f"hold_{action}")
                return "created"

            def event(self, phase: str, **fields: object) -> None:
                self.steps.append(phase)

            def stop_old_api(self) -> None:
                raise module.Stop("graceful_stop_not_proven")

            def timer_pause(self) -> None:
                self.steps.append("timer_paused")

            def stage_helper(self) -> None:
                self.steps.append("helper_staged")

        driver = FailureDriver()
        with (
            patch.object(module.os, "geteuid", return_value=0),
            patch.object(module.Path, "read_text", return_value=module.DRIVER_UNIT),
            self.assertRaisesRegex(module.Stop, "graceful_stop_not_proven"),
        ):
            driver.run()
        self.assertIn("hold_acquire", driver.steps)
        self.assertLess(
            driver.steps.index("timer_paused"), driver.steps.index("unlock")
        )
        self.assertLess(
            driver.steps.index("helper_staged"), driver.steps.index("unlock")
        )
        self.assertNotIn("hold_clear", driver.steps)

    def test_unreadable_staged_helper_stops_before_old_api(self) -> None:
        class UnreadableHelperDriver(module.Driver):
            def __init__(self) -> None:
                super().__init__(plan(), "a" * 64, dry_run=False)
                self.steps: list[str] = []

            def preflight(self, *, after_hold: bool = False) -> None:
                pass

            def verify_b25_producer_quiescence(self) -> None:
                pass

            def verify_global_pause_cutover_ready(self) -> None:
                pass

            def acquire_locks(self) -> None:
                self.steps.append("locks")

            def release_locks(self) -> None:
                self.steps.append("unlock")

            def hold(self, action: str) -> str:
                self.steps.append(f"hold_{action}")
                return "created"

            def event(self, phase: str, **fields: object) -> None:
                self.steps.append(phase)

            def timer_pause(self) -> None:
                pass

            def stage_helper(self) -> None:
                self.steps.append("helper_unreadable")
                raise module.Stop("container_helper_unreadable")

            def stop_old_api(self) -> None:
                raise AssertionError("old API stopped before helper proof")

            def post_hold(self) -> None:
                self.steps.append("same_hold_verified")

        driver = UnreadableHelperDriver()
        with (
            patch.object(module.os, "geteuid", return_value=0),
            patch.object(module.Path, "read_text", return_value=module.DRIVER_UNIT),
            self.assertRaisesRegex(module.Stop, "container_helper_unreadable"),
        ):
            driver.run()
        self.assertIn("same_hold_verified", driver.steps)
        self.assertNotIn("old_api_stop_waiting", driver.steps)

    def test_helper_copy_must_be_readable_by_worker_default_user(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            release = Path(temporary)
            helper = release / "dispatch_fence_cutover.py"
            helper.write_bytes(b"# disposable helper\n")
            candidate = plan(str(release))
            candidate["source_sha256"][helper.name] = module.sha_bytes(
                helper.read_bytes()
            )
            driver = module.Driver(candidate, "a" * 64, dry_run=False)
            helper.chmod(0o600)
            with self.assertRaisesRegex(module.Stop, "helper_source_must_be_0644"):
                driver.stage_helper()
            helper.chmod(0o644)

            def response(*args: str, **kwargs: object) -> bytes:
                if (
                    args[:3] == ("docker", "exec", candidate["pins"]["worker_id"])
                    and "sha256sum" in args
                ):
                    return (
                        candidate["source_sha256"][helper.name].encode() + b"  helper"
                    )
                return b""

            with (
                patch.object(driver, "cmd", side_effect=response) as command,
                patch.object(driver, "event"),
            ):
                driver.stage_helper()
            self.assertTrue(driver.helper_staged)
            self.assertTrue(
                any("sha256sum" in call.args for call in command.call_args_list)
            )

    def test_event_failure_before_stock_deploy_keeps_same_hold_and_four_locks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            release = root / "release"
            release.mkdir()
            hold_source = HERE.parents[4] / "ops" / "release" / "hold.py"
            shutil.copyfile(hold_source, release / "hold.py")
            wrapper = HERE / "host-cutover-driver.deploy-wrapper.sh"
            shutil.copyfile(wrapper, release / wrapper.name)
            candidate = plan(str(release))
            candidate["source_sha256"]["hold.py"] = module.sha_bytes(
                hold_source.read_bytes()
            )
            candidate["source_sha256"][wrapper.name] = module.sha_bytes(
                wrapper.read_bytes()
            )
            lock_paths = tuple(root / f"lock-{index}" for index in range(4))
            hold_path = root / "deploy.hold"

            class FaultDriver(module.Driver):
                def check_host_env(self) -> None:
                    pass

                def check_autodeploy_idle(self) -> None:
                    pass

                def event(self, phase: str, **fields: object) -> None:
                    if phase == "cutover_hold_retained_for_stock_deploy":
                        raise OSError("injected event fsync fault")

            with (
                patch.object(module, "LOCKS", lock_paths),
                patch.object(module, "HOLD_PATH", hold_path),
                patch.object(
                    module,
                    "HOST_DEPLOY",
                    HERE / "host-cutover-driver.deploy-patched.sh",
                ),
            ):
                driver = FaultDriver(candidate, "a" * 64, dry_run=False)
                driver.acquire_locks()
                driver.hold("acquire")
                driver.pre_hold_owned = True
                with self.assertRaisesRegex(OSError, "injected event"):
                    driver.stock_deploy()
                self.assertTrue(driver.pre_hold_owned)
                self.assertEqual(len(driver.lock_fds), 4)
                self.assertTrue(hold_path.exists())
                driver.post_hold()
                self.assertEqual(len(driver.lock_fds), 4)
                self.assertTrue(hold_path.exists())
                self.assertEqual(driver.hold("verify"), "verified")
                driver.release_locks()

    def test_stock_deploy_uses_exact_hold_entitlement_and_retains_hold(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            release = root / "release"
            release.mkdir()
            hold_source = HERE.parents[4] / "ops" / "release" / "hold.py"
            shutil.copyfile(hold_source, release / "hold.py")
            wrapper = HERE / "host-cutover-driver.deploy-wrapper.sh"
            shutil.copyfile(wrapper, release / wrapper.name)
            candidate = plan(str(release))
            candidate["source_sha256"]["hold.py"] = module.sha_bytes(
                hold_source.read_bytes()
            )
            candidate["source_sha256"][wrapper.name] = module.sha_bytes(
                wrapper.read_bytes()
            )
            lock_paths = tuple(root / f"lock-{index}" for index in range(4))
            hold_path = root / "deploy.hold"
            with (
                patch.object(module, "LOCKS", lock_paths),
                patch.object(module, "HOLD_PATH", hold_path),
                patch.object(
                    module,
                    "HOST_DEPLOY",
                    HERE / "host-cutover-driver.deploy-patched.sh",
                ),
            ):
                driver = module.Driver(candidate, "a" * 64, dry_run=False)
                driver.acquire_locks()
                driver.hold("acquire")
                with (
                    patch.object(driver, "check_host_env"),
                    patch.object(driver, "check_autodeploy_idle"),
                    patch.object(module.subprocess, "run") as run,
                ):
                    run.return_value.returncode = 0
                    run.return_value.stdout = b"DEPLOY_EXIT=0\n"
                    driver.stock_deploy()
                arguments = run.call_args.args[0]
                self.assertIn("--ignore-hold", arguments)
                self.assertIn("--no-rollback", arguments)
                self.assertIn(f"--expected-hold-sha256={driver.hold_sha256}", arguments)
                self.assertTrue(hold_path.exists())
                self.assertFalse(driver.lock_fds)

    def test_nonce_handoff_keeps_receipt_private(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            candidate = plan(str(root))
            driver = module.Driver(candidate, "a" * 64, dry_run=False)
            nonce = "b" * 64
            receipt = {
                "schema_version": 1,
                "job_id": module.JOB_ID,
                "key": module.KEY,
                "nonce": nonce,
                "waitaof_local": 1,
                "durable": True,
            }
            driver.receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            driver.hold_sha256 = "f" * 64
            systemd_output = (
                "{ path=/bin/bash ; argv[]=/bin/bash "
                f"{temporary}/monitor-lock.sh --receipt {temporary}/nonce-receipt.json "
                f"--redis-container-id {'6' * 64} ; ignore_errors=no ; }}"
            )
            hold_record = {
                "owner": module.HOLD_OWNER,
                "phases": module.HOLD_PHASES,
                "created_at": "2026-10-18T00:00:00+00:00",
            }
            with (
                patch.object(driver, "watcher_execstart", return_value=systemd_output),
                patch.object(driver, "hold_record", return_value=hold_record),
            ):
                driver.write_handoff(
                    "c" * 64,
                    123,
                    {
                        "api_id": "d" * 64,
                        "api_image": "sha256:" + "e" * 64,
                        "proof": {"enforced": True},
                    },
                )
            raw = (root / "handoff.json").read_text(encoding="utf-8")
            self.assertNotIn(nonce, raw)
            self.assertIn('"nonce_retained": true', raw)
            self.assertIn('"nonce_watcher_execstart_sha256"', raw)
            self.assertIn('"hold_sha256": "' + "f" * 64 + '"', raw)
            handoff = json.loads(raw)
            self.assertEqual(
                handoff["nonce_watcher_execstart_sha256"],
                module.sha_bytes(systemd_output.strip().encode("utf-8")),
            )

    def test_deploy_failure_verifies_continuous_hold(self) -> None:
        class FailureDriver(module.Driver):
            def __init__(self) -> None:
                super().__init__(plan(), "a" * 64, dry_run=False)
                self.steps: list[str] = []

            def preflight(self, *, after_hold: bool = False) -> None:
                self.steps.append("preflight")

            def verify_b25_producer_quiescence(self) -> None:
                pass

            def verify_global_pause_cutover_ready(self) -> None:
                pass

            def acquire_locks(self) -> None:
                self.steps.append("locks")

            def release_locks(self) -> None:
                self.steps.append("unlock")

            def hold(self, action: str) -> str:
                self.steps.append(f"hold_{action}")
                return "created"

            def event(self, phase: str, **fields: object) -> None:
                self.steps.append(phase)

            def stop_old_api(self) -> None:
                self.steps.append("stop")

            def stage_helper(self) -> None:
                self.steps.append("helper_staged")

            def acquire_nonce(self) -> str:
                self.nonce_acquired = True
                return "a" * 64

            def start_watcher(self, nonce_sha: str) -> int:
                return 123

            def install_marker(self, nonce_sha: str) -> None:
                pass

            def timer_pause(self) -> None:
                pass

            def check_nonce_owner(self) -> str:
                return "a" * 64

            def check_watcher(self, nonce_sha: str, *, first: bool = False) -> int:
                return 123

            def stock_deploy(self) -> None:
                self.steps.append("stock_terminal_failure")
                raise module.Stop("stock_deploy_failed_or_rolled_back")

            def post_hold(self) -> None:
                self.steps.append("recovery_post_hold")

        driver = FailureDriver()
        with (
            patch.object(module.os, "geteuid", return_value=0),
            patch.object(module.Path, "read_text", return_value=module.DRIVER_UNIT),
            self.assertRaisesRegex(module.Stop, "stock_deploy_failed_or_rolled_back"),
        ):
            driver.run()
        self.assertIn("recovery_post_hold", driver.steps)
        self.assertLess(
            driver.steps.index("stock_terminal_failure"),
            driver.steps.index("recovery_post_hold"),
        )


if __name__ == "__main__":
    unittest.main()
