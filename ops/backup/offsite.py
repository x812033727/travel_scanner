"""Copy the nightly backup runs to the owner's Google Drive.

``backup.py`` leaves one complete directory per night under
``/var/backups/travel-scanner/nightly/<UTC timestamp>/`` on the same disk as the database.
One ``run`` of this module, started by ``travel-scanner-offsite.timer`` an hour and a half
after the backup, copies every complete run that is not on Drive yet to
``<OFFSITE_REMOTE>/<timestamp>/`` (oldest first, so a missed night catches up), then:

1. ``rclone copy`` the run without ``manifest.json``, then ``manifest.json`` on its own, so a
   run on Drive that has a manifest is a run whose dumps all arrived;
2. ``rclone check --one-way`` the local run against Drive, file by file (MD5 on Drive); any
   difference fails the run and nothing is recorded as uploaded;
3. only after the newest run is verified, keep the newest ``OFFSITE_RETENTION`` run
   directories on Drive and ``purge`` older ones (Drive keeps a purged folder in its trash
   for 30 days).

Owner decision 2026-11-11: the dumps go to Drive **unencrypted**, with the same rclone remote
the video backups use (``videobackup``, rooted at ``AI/備份``), under ``主機/資料庫/nightly``.
The encrypted config bundle (``config.tar.age``) goes along when ``backup.py`` kept one.

rclone is not installed on the host; it runs from the video worker image, the same way
``docs/videos/rules-sync/sync.mjs`` does: the config directory is mounted read-only and copied
inside the container, because rclone rewrites the token when it refreshes it.

``/var/lib/travel-scanner-backup/last.json`` gains ``offsite`` (last success: time, remote,
runs, bytes) and ``offsite_failure``. Exit codes: 0 success (also: nothing to do), 1 failure,
2 configuration error. Standard library only; every command goes through ``CommandRunner``.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from backup import (  # noqa: E402 (the module sits next to this file on the host)
    RUN_DIR,
    CommandRunner,
    ConfigError,
    Paths,
    _iso,
    now_utc,
    one_line,
    read_env_file,
    read_json,
    write_json,
)

UPLOAD_TIMEOUT = 4 * 3600
RCLONE_FLAGS = [
    "--retries",
    "5",
    "--low-level-retries",
    "20",
    "--drive-chunk-size",
    "64M",
    "--stats",
    "0",
]


class OffsiteError(RuntimeError):
    def __init__(self, stage: str, reason: str) -> None:
        super().__init__(f"{stage}: {reason}")
        self.stage = stage
        self.reason = reason


@dataclass(frozen=True)
class OffsiteConfig:
    remote: str = "videobackup:主機/資料庫/nightly"
    retention: int = 14
    docker_image: str = "travel-scanner-video-worker:local"
    rclone_conf_dir: str = "/etc/travel-scanner/rclone-videos"

    @classmethod
    def from_mapping(cls, env: Mapping[str, str]) -> OffsiteConfig:
        defaults = cls()
        remote = env.get("OFFSITE_REMOTE", defaults.remote).strip().rstrip("/")
        if remote and ":" not in remote:
            raise ConfigError(f"OFFSITE_REMOTE must be <remote>:<path>, got {remote!r}")
        if remote.endswith(":"):
            raise ConfigError("OFFSITE_REMOTE must name a folder, not the root of the remote")
        raw = env.get("OFFSITE_RETENTION", "").strip()
        retention = defaults.retention
        if raw:
            try:
                retention = int(raw)
            except ValueError as exc:
                raise ConfigError(f"OFFSITE_RETENTION must be an integer, got {raw!r}") from exc
            if retention < 1:
                raise ConfigError("OFFSITE_RETENTION must keep at least one run")
        return cls(
            remote=remote,
            retention=retention,
            docker_image=env.get("OFFSITE_DOCKER_IMAGE", defaults.docker_image).strip(),
            rclone_conf_dir=env.get("OFFSITE_RCLONE_CONF_DIR", defaults.rclone_conf_dir).strip(),
        )


class Offsite:
    def __init__(
        self,
        paths: Paths,
        config: OffsiteConfig,
        runner: CommandRunner,
        *,
        dry_run: bool = False,
        now: Any = now_utc,
        out: Any = print,
    ) -> None:
        self.paths = paths
        self.config = config
        self.runner = runner
        self.dry_run = dry_run
        self.now = now
        self.out = out

    def _say(self, stage: str, message: str) -> None:
        self.out(f"{_iso(self.now())} {stage}: {message}")

    def rclone(
        self, args: Sequence[str], *, stage: str, timeout: int = 600, missing_ok: bool = False
    ) -> str:
        """One rclone command in the worker image; the nightly root is read-only at /runs."""
        argv = [
            "docker",
            "run",
            "--rm",
            "-u",
            "0",
            "--network",
            "host",
            "-v",
            f"{self.config.rclone_conf_dir}:/conf:ro",
            "-v",
            f"{self.paths.root}:/runs:ro",
            "--entrypoint",
            "sh",
            self.config.docker_image,
            "-c",
            'cp /conf/rclone.conf /tmp/rclone.conf && exec rclone --config /tmp/rclone.conf "$@"',
            "rclone",
            *args,
        ]
        result = self.runner.run(argv, timeout=timeout)
        if missing_ok and result.code == 3 and "directory not found" in result.output:
            return ""  # the first run: the folder on Drive does not exist yet
        if result.code != 0:
            raise OffsiteError(
                stage, f"rclone {args[0]} exited {result.code}: {one_line(result.output)}"
            )
        return result.output

    def local_runs(self) -> list[Path]:
        if not self.paths.root.is_dir():
            return []
        return sorted(
            path
            for path in self.paths.root.iterdir()
            if path.is_dir() and RUN_DIR.match(path.name) and (path / "manifest.json").is_file()
        )

    def remote_runs(self) -> list[str]:
        """Run directories on Drive that have their manifest (the last file of an upload)."""
        listing = self.rclone(
            ["lsf", "-R", "--files-only", "--include", "/*/manifest.json", self.config.remote],
            stage="list",
            missing_ok=True,
        )
        names = {
            line.split("/", 1)[0]
            for line in listing.splitlines()
            if line.endswith("/manifest.json")
        }
        return sorted(name for name in names if RUN_DIR.match(name))

    def remote_dirs(self) -> list[str]:
        listing = self.rclone(
            ["lsf", "--dirs-only", self.config.remote], stage="list", missing_ok=True
        )
        return sorted(
            line.rstrip("/") for line in listing.splitlines() if RUN_DIR.match(line.rstrip("/"))
        )

    def upload(self, run: Path) -> int:
        target = f"{self.config.remote}/{run.name}"
        source = f"/runs/{run.name}"
        size = sum(path.stat().st_size for path in run.iterdir() if path.is_file())
        self._say("upload", f"{run.name} ({size} bytes) -> {target}")
        if self.dry_run:
            return size
        self.rclone(
            ["copy", source, target, "--exclude", "/manifest.json", *RCLONE_FLAGS],
            stage="upload",
            timeout=UPLOAD_TIMEOUT,
        )
        self.rclone(
            ["copy", source, target, "--include", "/manifest.json", *RCLONE_FLAGS],
            stage="upload",
            timeout=600,
        )
        self.rclone(
            ["check", source, target, "--one-way", "--retries", "3"], stage="check", timeout=1800
        )
        self._say("check", f"{run.name}: 0 differences")
        return size

    def prune(self) -> list[str]:
        dirs = self.remote_dirs()
        old = dirs[: max(0, len(dirs) - self.config.retention)]
        for name in old:
            self._say(
                "retention",
                f"{'would purge' if self.dry_run else 'purge'} {self.config.remote}/{name}",
            )
            if not self.dry_run:
                self.rclone(["purge", f"{self.config.remote}/{name}"], stage="retention")
        return old

    def _record(self, key: str, payload: Mapping[str, Any]) -> None:
        if self.dry_run:
            return
        state = read_json(self.paths.last)
        state[key] = dict(payload)
        write_json(self.paths.last, state)

    def run(self) -> int:
        if not self.config.remote:
            self._say("config", "OFFSITE_REMOTE is empty: the offsite copy is disabled")
            return 0
        try:
            local = self.local_runs()
            if not local:
                self._say("list", f"no complete run under {self.paths.root}")
                return 0
            done = set(self.remote_runs())
            todo = [run for run in local if run.name not in done]
            self._say(
                "list", f"{len(local)} local run(s), {len(done)} on Drive, {len(todo)} to upload"
            )
            sent = [(run.name, self.upload(run)) for run in todo]
            pruned = self.prune()
        except OffsiteError as error:
            self._say("failed", str(error))
            self._record(
                "offsite_failure",
                {"at": _iso(self.now()), "stage": error.stage, "reason": error.reason},
            )
            return 1
        self._record(
            "offsite",
            {
                "at": _iso(self.now()),
                "remote": self.config.remote,
                "newest": local[-1].name,
                "uploaded": [name for name, _ in sent],
                "bytes": sum(size for _, size in sent),
                "pruned": pruned,
            },
        )
        self._say(
            "done",
            f"{len(sent)} run(s) uploaded, newest on Drive {local[-1].name}, {len(pruned)} pruned",
        )
        return 0


def main(
    argv: Sequence[str] | None = None,
    *,
    paths: Paths | None = None,
    runner: CommandRunner | None = None,
) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("command", choices=["run"])
    parser.add_argument(
        "--dry-run", action="store_true", help="list what would be uploaded and pruned"
    )
    args = parser.parse_args(argv)
    paths = paths or Paths()
    try:
        config = OffsiteConfig.from_mapping(read_env_file(paths.env_file))
    except ConfigError as error:
        print(f"config: {error}", file=sys.stderr)
        return 2
    return Offsite(paths, config, runner or CommandRunner(), dry_run=args.dry_run).run()


if __name__ == "__main__":
    sys.exit(main())
