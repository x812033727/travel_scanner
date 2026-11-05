#!/usr/bin/env python3
"""Put every file in models.lock on the network volume, verified, once.

A file is fetched at its pinned revision into `<name>.part` (curl resumes it after a restart),
hashed against the lock and only then renamed; `<dest>/.verified/<sha256>` records the hash so a
later pod does not re-read 110 GiB. A model file the lock no longer names is removed first, so a
re-pin fits on the volume. Writes its state to --status for the gate to report.

  fetch_models.py --lock models.lock --dest /workspace/models --status /tmp/gate-status.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

CHUNK = 16 * 2**20
CURL_ATTEMPTS = 5
BASE_URL = os.environ.get("HF_BASE_URL", "https://huggingface.co")


def write_status(path: Path, **state: object) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps({**state, "updated_at": time.time()}), encoding="utf-8")
    temporary.replace(path)


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(CHUNK):
            digest.update(chunk)
    return digest.hexdigest()


def fetch(entry: dict, target: Path) -> None:
    part = target.with_name(target.name + ".part")
    url = f"{BASE_URL}/{entry['repo']}/resolve/{entry['revision']}/{entry['path']}"
    for attempt in range(1, CURL_ATTEMPTS + 1):
        done = subprocess.run(["curl", "-fsSL", "--retry", "3", "-C", "-", "-o", str(part), url], check=False)
        if done.returncode == 0 and part.stat().st_size == entry["size"]:
            break
        if part.exists() and part.stat().st_size > entry["size"]:
            part.unlink()
        if attempt == CURL_ATTEMPTS:
            raise RuntimeError(f"{target.name}: download failed (curl exit {done.returncode})")
        time.sleep(5 * attempt)
    actual = sha256_of(part)
    if actual != entry["sha256"]:
        part.unlink()
        raise RuntimeError(f"{target.name}: sha256 {actual} does not match the lock")
    part.replace(target)


def run(lock: Path, dest: Path, status: Path) -> None:
    files = json.loads(lock.read_text(encoding="utf-8"))["files"]
    verified = dest / ".verified"
    verified.mkdir(parents=True, exist_ok=True)
    wanted = {dest / entry["folder"] / Path(entry["path"]).name for entry in files}
    hashes = {entry["sha256"] for entry in files}
    for folder in {entry["folder"] for entry in files}:
        for path in (dest / folder).glob("*"):
            if path.is_file() and path not in wanted and path.with_name(path.name.removesuffix(".part")) not in wanted:
                print(f"[fetch_models] removing {path.name}, no longer in the lock", flush=True)
                path.unlink()
    for marker in verified.glob("*"):
        if marker.name not in hashes:
            marker.unlink()
    missing = []
    for entry in files:
        target = dest / entry["folder"] / Path(entry["path"]).name
        marker = verified / entry["sha256"]
        if not (marker.exists() and target.is_file() and target.stat().st_size == entry["size"]):
            missing.append((entry, target, marker))
    needed = sum(entry["size"] for entry, _, _ in missing)
    free = shutil.disk_usage(dest).free
    if needed > free:
        raise RuntimeError(f"the volume has {free / 2**30:.1f} GiB free; the models need {needed / 2**30:.1f} GiB more")
    for index, (entry, target, marker) in enumerate(missing, start=1):
        name = target.name
        write_status(status, status="fetching", file=name, index=index, total=len(missing))
        print(f"[fetch_models] {index}/{len(missing)} {name}", flush=True)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_file() and target.stat().st_size == entry["size"] and sha256_of(target) == entry["sha256"]:
            marker.touch()
            continue
        fetch(entry, target)
        marker.touch()
    write_status(status, status="starting")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--dest", type=Path, required=True)
    parser.add_argument("--status", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        run(args.lock, args.dest, args.status)
    except (OSError, RuntimeError, ValueError, KeyError) as exc:
        write_status(args.status, status="failed", error=str(exc))
        print(f"[fetch_models] {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
