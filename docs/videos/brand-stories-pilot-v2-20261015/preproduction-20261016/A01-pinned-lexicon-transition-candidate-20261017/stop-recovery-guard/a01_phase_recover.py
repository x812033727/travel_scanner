#!/usr/bin/env python3
"""ExecStopPost target: stop the direct container, then restore A01 STOP.

The original auto container is never started here. On failure, both video
containers retain restart=no and the durable marker/hold need reconciliation.
"""

from __future__ import annotations

import json
import re
import stat
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/usr/local/sbin")
import a01_stop_guard  # noqa: E402


ONEOFF = (a01_stop_guard.Paths().workdir / "a01-round12-oneoff.json")


def docker(*args: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(("docker", *args), stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=10, check=False)
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f"Docker {args[0]} timed out; one-off state is uncertain") from error


def inspect(identity: str, field: str) -> tuple[int, str, str]:
    result = docker("inspect", "--format", field, identity)
    return (result.returncode, result.stdout.decode(errors="replace").strip(),
            result.stderr.decode(errors="replace").strip())


def absent(code: int, error: str, identity: str) -> bool:
    if code == 0:
        return False
    # Docker releases vary the case of this diagnostic. Accept only an exact
    # missing-object response for the full ID we inspected; a daemon error or
    # a missing different object does not prove this one-off is stopped.
    if re.fullmatch(r"(?:error:\s*)?no such (?:object|container):\s*"
                    + re.escape(identity), error.strip(), flags=re.IGNORECASE):
        return True
    raise RuntimeError(f"Docker inspect failed without a proved absent ID: {error[:160]}")


def main() -> int:
    stop_error = None
    marker_error = None
    pinned = None
    try:
        try:
            marker_info = ONEOFF.lstat()
        except FileNotFoundError:
            marker_info = None
        if marker_info is not None:
            if not stat.S_ISREG(marker_info.st_mode):
                raise RuntimeError("one-off marker is not regular")
            record = json.loads(ONEOFF.read_text())
            identity = record.get("container_id")
            if (record.get("schema_version") != 1 or
                    record.get("slug") != "story-rolling-suitcase-v2" or
                    not isinstance(identity, str) or len(identity) != 64):
                raise RuntimeError("invalid one-off marker identity")
            pinned = identity
    except (OSError, RuntimeError, ValueError, KeyError, json.JSONDecodeError) as error:
        # A truncated or corrupt marker cannot be allowed to skip the fixed
        # Docker-label route. Kill any labelled one-off, then still report the
        # marker fault and leave the phase held for manual reconciliation.
        marker_error = error
    try:
        # A missing marker must not hide a live one-off. The fixed Docker label
        # gives ExecStopPost a second route to find and stop it.
        listed = docker("ps", "--all", "--no-trunc", "--filter",
                        "label=mokaair.a01.round12", "--format", "{{.ID}}")
        if listed.returncode:
            raise RuntimeError("cannot enumerate A01 labelled one-off containers")
        identities = set(listed.stdout.decode(errors="replace").splitlines())
        if pinned is not None:
            identities.add(pinned)
        for identity in sorted(identities):
            if len(identity) != 64:
                raise RuntimeError("A01 one-off enumeration returned a non-full ID")
            format_string = ('{{.Id}} {{.State.Running}} {{.HostConfig.RestartPolicy.Name}} '
                             '{{index .Config.Labels "mokaair.a01.round12"}}')
            code, actual, error = inspect(identity, format_string)
            absent(code, error, identity)
            if code == 0:
                parts = actual.split()
                if (len(parts) != 4 or parts[0] != identity or
                        parts[3] not in ("listener", "manual", "facts", "panel", "validate", "fault-test")):
                    raise RuntimeError("one-off identity or label drift")
                if parts[2] != "no":
                    updated = docker("update", "--restart=no", identity)
                    if updated.returncode or inspect(identity, "{{.HostConfig.RestartPolicy.Name}}")[1] != "no":
                        raise RuntimeError("one-off restart=no could not be restored before kill")
                if parts[1] == "true":
                    result = docker("kill", identity)
                    if result.returncode:
                        raise RuntimeError("cannot kill pinned one-off container")
                elif parts[1] != "false":
                    raise RuntimeError("one-off running state drift")
            # --rm containers disappear after kill. A still-present stopped ID is
            # also safe; a running one is never allowed past this point.
            code, actual, error = inspect(identity, "{{.State.Running}}")
            absent(code, error, identity)
            if code == 0 and actual != "false":
                raise RuntimeError("one-off direct phase is still running")
            print(f"A01_ONEOFF_STOPPED {identity}", flush=True)
    except (OSError, RuntimeError, ValueError, KeyError) as error:
        stop_error = error
    if stop_error is None:
        stop_error = marker_error
    try:
        print(a01_stop_guard.restore(), flush=True)
        stop = a01_stop_guard.Paths().stop
        if not stat.S_ISREG(stop.lstat().st_mode):
            raise RuntimeError("A01 project STOP is not regular after restore")
        if stop_error is not None:
            raise RuntimeError(f"one-off stop unresolved: {stop_error}")
        return 0
    except (OSError, RuntimeError, ValueError, KeyError) as error:
        print(f"A01 PHASE RECOVERY FAILED: {error}", file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
