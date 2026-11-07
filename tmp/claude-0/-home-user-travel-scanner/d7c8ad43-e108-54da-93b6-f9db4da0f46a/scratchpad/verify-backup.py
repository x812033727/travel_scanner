#!/usr/bin/env python3
"""Check that every local work file is in a GitHub backup branch, byte for byte (by git blob hash).

  verify-backup.py --branch transfer/tn-all-work --root /tmp/.../scratchpad/e001 [--root …] [--exclude-dir segments-v4 --exclude-dir refs]

For every regular file under each --root (skipping the excluded directory names and *.git folders), the file must be
in the branch's tree at its absolute path minus the leading "/":
  - same blob hash -> ok;
  - stored as <path>.part00, .part01 … -> the parts' hashes must equal the local file split the same way (90 MiB);
  - a symlink must be stored as a symlink (mode 120000) to the same target.
Prints every missing or differing path and a summary; exit 1 when anything is missing or different.
Uses `git fetch --filter=blob:none` in the repository, so nothing large is downloaded.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = "/home/user/travel_scanner"
PART = 90 * 1024 * 1024


def git(*args: str, input_bytes: bytes | None = None) -> str:
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, check=True, input=input_bytes).stdout.decode()


def blob_hash(data: bytes) -> str:
    return git("hash-object", "--stdin", input_bytes=data).strip()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--branch", required=True)
    ap.add_argument("--root", action="append", required=True)
    ap.add_argument("--exclude-dir", action="append", default=["segments-v4"])
    a = ap.parse_args(argv)
    git("fetch", "-q", "--filter=blob:none", "origin", f"{a.branch}:refs/remotes/verify/{a.branch.replace('/', '_')}")
    tree: dict[str, tuple[str, str]] = {}
    for line in git("ls-tree", "-r", f"refs/remotes/verify/{a.branch.replace('/', '_')}").splitlines():
        meta, path = line.split("\t", 1)
        mode, _, sha = meta.split()
        tree[path] = (mode, sha)
    ok = missing = differ = 0
    problems: list[str] = []
    for root in a.root:
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            dirnames[:] = [d for d in dirnames if d not in a.exclude_dir and not d.endswith(".git")]
            for name in list(filenames) + [d for d in os.listdir(dirpath) if os.path.islink(os.path.join(dirpath, d)) and os.path.isdir(os.path.join(dirpath, d))]:
                full = os.path.join(dirpath, name)
                rel = full.lstrip("/")
                if os.path.islink(full):
                    entry = tree.get(rel)
                    if not entry or entry[0] != "120000":
                        missing += 1; problems.append(f"MISSING link {full}")
                    else:
                        target = git("cat-file", "-p", entry[1])
                        if target != os.readlink(full):
                            differ += 1; problems.append(f"DIFFERENT link {full}")
                        else:
                            ok += 1
                    continue
                if not os.path.isfile(full):
                    continue
                entry = tree.get(rel)
                if entry:
                    local = git("hash-object", full).strip()
                    if local == entry[1]:
                        ok += 1
                    else:
                        differ += 1; problems.append(f"DIFFERENT {full}")
                    continue
                parts = sorted(p for p in tree if p.startswith(rel + ".part"))
                if not parts:
                    missing += 1; problems.append(f"MISSING {full}")
                    continue
                with open(full, "rb") as fh:
                    k, good = 0, True
                    while True:
                        chunk = fh.read(PART)
                        if not chunk:
                            break
                        name_k = f"{rel}.part{k:02d}"
                        if name_k not in tree or tree[name_k][1] != blob_hash(chunk):
                            good = False
                            break
                        k += 1
                    good = good and k == len(parts)
                if good:
                    ok += 1
                else:
                    differ += 1; problems.append(f"DIFFERENT (parts) {full}")
    for p in problems:
        print(p)
    print(f"{a.branch}: ok {ok}, missing {missing}, different {differ}")
    return 1 if missing or differ else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
