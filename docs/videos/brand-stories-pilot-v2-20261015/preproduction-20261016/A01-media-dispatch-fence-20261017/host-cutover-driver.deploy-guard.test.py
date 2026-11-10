"""Disposable tests of the exact captured deploy guard candidate."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "host-cutover-driver.deploy-patched.sh"
BUILDER = HERE / "host-cutover-driver.deploy-guard.py"
EXPECTED_SHA = "836b953610b4ae17eda6d2056efb1f633827db620d0eb43934312cc19d8ac9c6"


def bash_binary() -> str:
    if os.name == "nt":
        git_bash = Path(r"C:\Program Files\Git\bin\bash.exe")
        if git_bash.exists():
            return str(git_bash)
    binary = shutil.which("bash")
    if not binary:
        raise unittest.SkipTest("bash is unavailable")
    return binary


def extract_function(source: str, name: str) -> str:
    start = source.index(f"{name}() {{\n")
    end = source.index("\n}\n", start) + 3
    return source[start:end]


class DeployGuardTest(unittest.TestCase):
    @unittest.skipIf(os.name == "nt", "POSIX shell path semantics")
    def test_expected_hold_digest_rejects_missing_or_changed_hold(self) -> None:
        source = CANDIDATE.read_text(encoding="utf-8")
        fragment = (
            'if [[ -n "$EXPECTED_HOLD_SHA256" ]]; then\n'
            + source.split('if [[ -n "$EXPECTED_HOLD_SHA256" ]]; then\n', 1)[1].split(
                '\nHOLD=""', 1
            )[0]
            + "\n"
        )
        with tempfile.TemporaryDirectory() as temporary:
            hold = Path(temporary) / "a01.hold"
            hold.write_bytes(b"owned hold\n")
            expected = hashlib.sha256(hold.read_bytes()).hexdigest()
            for state in ("same", "changed", "missing"):
                with self.subTest(state=state):
                    if state == "changed":
                        hold.write_bytes(b"different hold\n")
                    elif state == "missing":
                        hold.unlink()
                    script = (
                        "set -euo pipefail\n"
                        f"HOLD_FILE={str(hold)!r}\n"
                        f"EXPECTED_HOLD_SHA256={expected}\n"
                        "fail() { exit 73; }\n" + fragment
                    )
                    result = subprocess.run(
                        [bash_binary(), "-c", script], capture_output=True, check=False
                    )
                    self.assertEqual(result.returncode, 0 if state == "same" else 73)

    def test_exact_lf_candidate_and_bash_syntax(self) -> None:
        raw = CANDIDATE.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), EXPECTED_SHA)
        self.assertNotIn(b"\r", raw)
        completed = subprocess.run(
            [bash_binary(), "-n"], input=raw, capture_output=True, check=False
        )
        self.assertEqual(
            completed.returncode, 0, completed.stderr.decode(errors="replace")
        )

    def test_builder_rejects_any_changed_capture(self) -> None:
        spec = importlib.util.spec_from_file_location("a01_deploy_guard", BUILDER)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with self.assertRaisesRegex(ValueError, "capture.*drift"):
            module.build(b"#!/bin/bash\n")

    def test_no_rollback_never_restarts_old_api_on_compose_or_health_failure(
        self,
    ) -> None:
        source = CANDIDATE.read_text(encoding="utf-8")
        rollback = extract_function(source, "rollback")
        for reason in ("compose up failed", "health checks failed"):
            with self.subTest(reason=reason):
                script = (
                    "set -euo pipefail\n"
                    "NO_ROLLBACK=1\nLOG_FILE=/tmp/fake-deploy.log\n"
                    "fail() { printf 'HALTED:%s\\n' \"$1\"; exit 77; }\n"
                    "git() { echo UNSAFE_GIT; exit 99; }\n"
                    "compose() { echo UNSAFE_COMPOSE; exit 99; }\n"
                    "ensure_readable() { echo UNSAFE_PERMISSIONS; exit 99; }\n"
                    "assert_pinned_redis_config() { echo UNSAFE_CONFIG; exit 99; }\n"
                    + rollback
                    + f"\nrollback {json.dumps(reason)}\n"
                )
                result = subprocess.run(
                    [bash_binary(), "-c", script], capture_output=True, check=False
                )
                self.assertEqual(
                    result.returncode, 77, result.stderr.decode(errors="replace")
                )
                self.assertIn(b"HALTED:", result.stdout)
                self.assertNotIn(b"UNSAFE_", result.stdout)

    def test_rendered_redis_guard_checks_required_services(self) -> None:
        source = CANDIDATE.read_text(encoding="utf-8")
        guard = extract_function(source, "assert_pinned_redis_config")
        url = "redis://private-redis/0"
        expected = hashlib.sha256(url.encode()).hexdigest()
        snapshot = "/run/mokaair-a01-deploy-env.fake"
        configuration = {
            "services": {
                "api": {
                    "environment": {"REDIS_URL": url},
                    "env_file": [{"path": snapshot}],
                },
                "video-ai-worker": {
                    "environment": {"REDIS_URL": url},
                    "env_file": [{"path": snapshot}],
                },
            }
        }
        for tamper in (None, "url", "path", "missing_service"):
            with self.subTest(tamper=tamper):
                tree = json.loads(json.dumps(configuration))
                if tamper == "url":
                    tree["services"]["video-ai-worker"]["environment"]["REDIS_URL"] = (
                        "redis://other/0"
                    )
                elif tamper == "path":
                    tree["services"]["api"]["env_file"][0]["path"] = "/run/other"
                elif tamper == "missing_service":
                    del tree["services"]["video-ai-worker"]
                payload = json.dumps(tree)
                # Git Bash invokes the Windows Store Python shim across a pipe
                # differently from Linux. Test the exact embedded predicate
                # directly there; POSIX CI exercises the full shell function.
                if os.name == "nt":
                    program = guard.split("python3 -c '", 1)[1].split(
                        '\' "$EXPECTED_REDIS_URL_SHA256"', 1
                    )[0]
                    direct = subprocess.run(
                        [sys.executable, "-c", program, expected, snapshot],
                        input=payload.encode(),
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(
                        direct.returncode,
                        0 if tamper is None else 1,
                        direct.stderr.decode(errors="replace"),
                    )
                    continue
                script = (
                    "set -euo pipefail\n"
                    f"EXPECTED_REDIS_URL_SHA256={expected}\n"
                    f"PINNED_ENV_FILE={snapshot}\n"
                    "compose() {\n"
                    "  cat <<'JSON'\n"
                    f"{payload}\n"
                    "JSON\n"
                    "}\n"
                    "fail() { exit 73; }\n" + guard + "\nassert_pinned_redis_config\n"
                )
                result = subprocess.run(
                    [bash_binary(), "-c", script], capture_output=True, check=False
                )
                self.assertEqual(
                    result.returncode,
                    0 if tamper is None else 73,
                    result.stdout.decode(errors="replace")
                    + result.stderr.decode(errors="replace"),
                )


if __name__ == "__main__":
    unittest.main()
