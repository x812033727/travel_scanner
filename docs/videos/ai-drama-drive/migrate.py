#!/usr/bin/env python3
"""Move the old transfer/* branches into Drive, once (docs/videos/AI-DRAMA-DRIVE.md §舊的 transfer/* 分支).

    python3 -I docs/videos/ai-drama-drive/migrate.py [--only BRANCH ...] [--dry-run]

Runs on the production host as root: `gh` reads the four private backup repositories, and rclone
runs inside the video worker's image (the host has no rclone of its own) with the host's backup
config, read-only, copied to /tmp first so a token refresh never writes the host's file.

For every row of legacy-branches.tsv, one branch at a time:
  1. fetch only the branch's head (for a copy of the whole repository, its commits past main) into
     a throwaway bare repository, and write its tree out under the staging folder;
  2. a copy of the whole repository keeps only the files its own commits added or changed;
  3. X.part00, X.part01… are joined back into X (against the sha256 in X.SPLIT when there is one);
  4. the files are laid out as Drive will hold them: <drive_folder>/…, or, for a branch that holds
     several episodes, each file under the episode its path names (shared files under _共用/);
  5. `rclone copy --checksum` into the remote (never sync: nothing in Drive is deleted; a file
     Drive already has with other content goes to AI劇/_舊版-搬家/<time>/), then `rclone check
     --one-way`; only 0 differences records the branch as done in the ledger.
The staging folder is emptied after each branch. A branch already in the ledger at the same commit
is skipped, so the run can stop and start again.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
TABLE = HERE / "legacy-branches.tsv"
WORK = Path(os.environ.get("MIGRATE_WORK", "/root/drive-migration"))
LEDGER = WORK / "ledger.json"
OWNER = "x812033727"
REMOTE = "videobackup"
CONF_DIR = "/etc/travel-scanner/rclone-videos"
IMAGE = os.environ.get("MIGRATE_IMAGE", "travel-scanner-video-worker:local")
OLD = "AI劇/_舊版-搬家"
SPLIT_NOTE = "（依路徑拆到各集）"
PART = re.compile(r"^(?P<base>.+)\.part(?P<n>\d+)$")
CREDENTIAL = ["-c", "credential.helper=", "-c", "credential.helper=!gh auth git-credential"]


def log(message: str) -> None:
    print(f"{datetime.now(UTC):%H:%M:%S} {message}", flush=True)


def run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, capture_output=True, **kwargs)  # type: ignore[call-overload]


def rclone(args: list[str], stage: Path) -> subprocess.CompletedProcess[str]:
    inner = "cp /conf/rclone.conf /tmp/rclone.conf && exec rclone --config /tmp/rclone.conf " + " ".join(
        "'" + arg.replace("'", "'\\''") + "'" for arg in args
    )
    return subprocess.run(
        ["docker", "run", "--rm", "-u", "0", "--network", "host", "-v", f"{CONF_DIR}:/conf:ro",
         "-v", f"{stage}:/stage:ro", "--entrypoint", "sh", IMAGE, "-c", inner],
        text=True, capture_output=True, check=False,
    )


def ahead_of_main(branch: str) -> int | None:
    """How many commits a copy of the whole repository has past main (its own), from travel_scanner,
    which still has these branches at the same commits."""
    out = run(["gh", "api", f"repos/{OWNER}/travel_scanner/compare/main...{branch}", "--jq", ".ahead_by"])
    return int(out.stdout.strip())


def fetch(repo: str, branch: str, depth: int, into: Path) -> str:
    git = into / "repo.git"
    run(["git", "init", "-q", "--bare", str(git)])
    url = f"https://github.com/{OWNER}/{repo}.git"
    run(["git", *CREDENTIAL, "-C", str(git), "fetch", "-q", "--depth", str(depth), url, f"refs/heads/{branch}"])
    return run(["git", "-C", str(git), "rev-parse", "FETCH_HEAD"]).stdout.strip()


def export(into: Path, commit: str, tree: Path) -> None:
    git = into / "repo.git"
    tree.mkdir(parents=True)
    archive = subprocess.Popen(["git", "-C", str(git), "archive", commit], stdout=subprocess.PIPE)
    subprocess.run(["tar", "-x", "-C", str(tree)], stdin=archive.stdout, check=True)
    if archive.wait() != 0:
        raise RuntimeError("git archive failed")


def own_files(into: Path, commit: str, ahead: int) -> set[str]:
    git = into / "repo.git"
    out = run(["git", "-C", str(git), "diff", "--name-only", "--no-renames", "--diff-filter=AM",
               f"{commit}~{ahead}", commit])
    return {line for line in out.stdout.splitlines() if line}


def files_under(root: Path) -> list[str]:
    return sorted(
        str(path.relative_to(root)) for path in root.rglob("*") if path.is_file() or path.is_symlink()
    )


def keep_only(tree: Path, keep: set[str]) -> None:
    for relative in files_under(tree):
        if relative not in keep:
            (tree / relative).unlink()
    for path in sorted(tree.rglob("*"), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()


def join_parts(tree: Path) -> int:
    """X.part00… back into X; returns how many were joined. Refuses a gap or a wrong sha256."""
    groups: dict[Path, list[tuple[int, Path]]] = {}
    for relative in files_under(tree):
        match = PART.match(relative)
        if match:
            groups.setdefault(tree / match["base"], []).append((int(match["n"]), tree / relative))
    for base, pieces in groups.items():
        if base.exists():
            continue  # the branch has both: kept as it is
        pieces.sort()
        if [n for n, _ in pieces] != list(range(pieces[0][0], pieces[0][0] + len(pieces))):
            raise RuntimeError(f"parts of {base.name} are not numbered without a gap")
        digest = hashlib.sha256()
        with base.open("wb") as out:
            for _, piece in pieces:
                with piece.open("rb") as handle:
                    while chunk := handle.read(1 << 20):
                        digest.update(chunk)
                        out.write(chunk)
        note = base.with_name(base.name + ".SPLIT")
        if note.exists():
            wanted = re.findall(r"\b[0-9a-f]{64}\b", note.read_text(errors="replace"))
            if wanted and digest.hexdigest() not in wanted:
                raise RuntimeError(f"{base.name}: joined sha256 does not match {note.name}")
        for _, piece in pieces:
            piece.unlink()
    return len(groups)


def episode_of(relative: str, drama: str, low: int, high: int) -> str | None:
    """The episode folder a file of a several-episode branch belongs to, from its path."""
    if "原來如此" in drama:
        found = [int(n) for n in re.findall(r"(?:^|[^a-z0-9])p(\d{2})(?=[^0-9]|$)", relative)]
        hits = [n for n in found if low <= n <= high]
        return f"P{hits[0]:02d}" if hits else None
    found = [int(n) for n in re.findall(r"(?:^|[^a-z0-9])e(\d{3})(?=[^0-9]|$)", relative)]
    hits = [n for n in found if low <= n <= high]
    return f"第{hits[0]:03d}集" if hits else None


def lay_out(tree: Path, stage: Path, row: dict[str, str]) -> dict[str, int]:
    """Move the branch's files under stage/<Drive path>; returns files per Drive folder."""
    branch_name = row["branch"].split("/", 1)[1]
    folder = row["drive_folder"].rstrip("/")
    counts: dict[str, int] = {}
    if SPLIT_NOTE not in folder:
        destination = stage / folder
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(tree), str(destination))
        counts[folder] = len(files_under(destination))
        return counts
    head, rest = folder.split(SPLIT_NOTE, 1)
    drama, span = head.rsplit("/", 1)
    numbers = [int(n) for n in re.findall(r"\d+", span)]
    low, high = numbers[0], numbers[-1]
    for relative in files_under(tree):
        episode = episode_of(relative.lower(), drama, low, high) or "_共用"
        target = f"{drama}/{episode}/製作檔/{branch_name}"
        destination = stage / target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(tree / relative), str(destination))
        counts[target] = counts.get(target, 0) + 1
    shutil.rmtree(tree)
    return counts


def load_ledger() -> dict[str, dict[str, object]]:
    return json.loads(LEDGER.read_text()) if LEDGER.exists() else {}


def save_ledger(ledger: dict[str, dict[str, object]]) -> None:
    tmp = LEDGER.with_suffix(".tmp")
    tmp.write_text(json.dumps(ledger, ensure_ascii=False, indent=1, sort_keys=True))
    tmp.replace(LEDGER)


def head_of(repo: str, branch: str) -> str:
    out = run(["gh", "api", f"repos/{OWNER}/{repo}/branches/{branch}", "--jq", ".commit.sha"])
    return out.stdout.strip()


def migrate(row: dict[str, str], ledger: dict[str, dict[str, object]], dry_run: bool) -> bool:
    key = f"{row['repo']}:{row['branch']}"
    commit = head_of(row["repo"], row["branch"])
    done = ledger.get(key, {})
    if done.get("commit") == commit and done.get("differences") == 0:
        log(f"skip {key}: done at {commit[:12]}")
        return True
    whole_repo = "只取比 main 多的檔" in row.get("note", "")
    ahead = ahead_of_main(row["branch"]) if whole_repo else None
    scratch = WORK / "scratch"
    stage = WORK / "stage"
    for path in (scratch, stage):
        shutil.rmtree(path, ignore_errors=True)
        path.mkdir(parents=True)
    started = time.time()
    try:
        fetched = fetch(row["repo"], row["branch"], (ahead or 0) + 1, scratch)
        if fetched != commit:
            raise RuntimeError(f"fetched {fetched[:12]}, the branch is at {commit[:12]}")
        tree = scratch / "tree"
        export(scratch, commit, tree)
        if ahead:
            keep_only(tree, own_files(scratch, commit, ahead))
        shutil.rmtree(scratch / "repo.git")
        joined = join_parts(tree)
        counts = lay_out(tree, stage, row)
        files = sum(counts.values())
        size = sum(path.stat().st_size for path in stage.rglob("*") if path.is_file())
        log(f"{key} {commit[:12]}: {files} files, {size / 1e9:.2f} GB, {joined} joined → {', '.join(counts)}")
        if dry_run:
            return True
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        flags = ["--links", "--tpslimit", "5", "--retries", "5", "--exclude", f"/{OLD}/**"]
        copied = rclone(["copy", "/stage", f"{REMOTE}:", "--checksum", "--drive-chunk-size", "64M",
                         "--transfers", "4", "--backup-dir", f"{REMOTE}:{OLD}/{stamp}", *flags], stage)
        if copied.returncode != 0:
            raise RuntimeError(f"rclone copy: {copied.stderr.strip()[-400:]}")
        checked = rclone(["check", "/stage", f"{REMOTE}:", "--one-way", *flags], stage)
        found = re.findall(r"(\d+) differences found", checked.stderr)
        differences = int(found[-1]) if found else (0 if checked.returncode == 0 else -1)
        ledger[key] = {
            "commit": commit, "files": files, "bytes": size, "folders": counts, "joined": joined,
            "differences": differences, "at": datetime.now(UTC).isoformat(),
            "seconds": round(time.time() - started),
        }
        save_ledger(ledger)
        log(f"{key}: rclone check {differences} differences")
        return differences == 0
    except (RuntimeError, subprocess.CalledProcessError, OSError) as error:
        detail = getattr(error, "stderr", "") or ""
        log(f"FAILED {key}: {error} {str(detail).strip()[-300:]}")
        ledger[key] = {"commit": commit, "error": str(error), "at": datetime.now(UTC).isoformat()}
        save_ledger(ledger)
        return False
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
        shutil.rmtree(stage, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="*", help="branch names (transfer/…) to do")
    parser.add_argument("--dry-run", action="store_true", help="fetch and lay out, copy nothing")
    options = parser.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    with TABLE.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if options.only:
        rows = [row for row in rows if row["branch"] in options.only]
    rows.sort(key=lambda row: float(row["GB"]))  # small ones first: early failures are cheap
    ledger = load_ledger()
    failed = [row["branch"] for row in rows if not migrate(row, ledger, options.dry_run)]
    log(f"done: {len(rows) - len(failed)} of {len(rows)} branches; failed: {failed or 'none'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
