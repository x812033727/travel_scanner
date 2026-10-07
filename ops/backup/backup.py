"""Nightly verified backups on the production host.

The production database holds every article, merchant, hotspot, community post, video
job and admin setting, and until this module the only dumps of it were the ones the
deploy script takes before a migration, on the same disk. One ``run`` of this module,
started by ``travel-scanner-backup.timer`` every night, writes a directory under
``/var/backups/travel-scanner/nightly/<UTC timestamp>/``:

1. ``travel-scanner-<ts>-<sha12>.dump``: ``pg_dump -Fc`` through
   ``docker compose exec -T postgres``, verified with ``pg_restore --list`` and hashed
   with SHA-256. An empty dump or one that does not list fails the run and is deleted.
2. Any ``/root/travel_scanner_predeploy_*.dump`` newer than the previous successful run
   (the dumps the deploy script takes right before a migration), copied in, verified
   and hashed the same way.
3. ``config.tar.age``: the host files that are not in git (``manifest-paths.txt``),
   built as a tar in a private temporary directory and encrypted with ``age`` to
   ``BACKUP_AGE_RECIPIENT`` before it is written under the run directory. The plain
   tar never lands in ``/var/backups``; without a recipient the bundle is not kept.
4. ``redis.rdb`` when ``BACKUP_INCLUDE_REDIS=true`` (default false; the queue is
   rebuilt, not restored).
5. ``manifest.json``: host, times, live git SHA, alembic revision, PostgreSQL version,
   and every file's name, size and SHA-256.

The run directory is ``<ts>.partial`` until everything above succeeded, so retention
(``BACKUP_LOCAL_RETENTION`` newest complete runs, applied only after a success) and the
offsite copy (``offsite.py``, a later task) only ever see complete runs.
``/var/lib/travel-scanner-backup/last.json`` records the last success, failure and skip
and never holds a secret. A run refuses to start while the deploy lock is held (a
deploy may be restarting postgres) and leaves it to the next timer firing.

Standard library only and no ``fcntl`` (the host runs Python 3.14; the tests also run
on Windows). Every host command goes through ``CommandRunner`` so the tests need neither
the host, root, Docker nor ``age``.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tarfile
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SKIPPED_EXIT = 3  # same code the deploy script uses for "not now"
RUN_DIR = re.compile(r"^\d{8}T\d{6}Z$")
_SHA = re.compile(r"[0-9a-f]{40}")
_REVISION = re.compile(r"[A-Za-z0-9_.-]{1,64}")


# --------------------------------------------------------------------------- paths


@dataclass(frozen=True)
class Paths:
    """Everything on the host the backup reads or writes. Tests point these at a temp dir."""

    repo: Path = Path("/root/travel_scanner")
    root: Path = Path("/var/backups/travel-scanner/nightly")
    state_dir: Path = Path("/var/lib/travel-scanner-backup")
    env_file: Path = Path("/etc/travel-scanner/backup.env")
    lock: Path = Path("/var/lock/travel-scanner-deploy.lock")
    predeploy_dir: Path = Path("/root")
    manifest_paths: Path = Path("/opt/travel-scanner-backup/manifest-paths.txt")

    @property
    def last(self) -> Path:
        return self.state_dir / "last.json"


# -------------------------------------------------------------------------- config


class ConfigError(RuntimeError):
    """The env file holds something the backup cannot run with."""


@dataclass(frozen=True)
class Config:
    include_redis: bool = False
    local_retention: int = 7
    age_recipient: str = ""

    @classmethod
    def from_mapping(cls, env: Mapping[str, str]) -> Config:
        raw = env.get("BACKUP_LOCAL_RETENTION", "").strip()
        retention = 7
        if raw:
            try:
                retention = int(raw)
            except ValueError as exc:
                raise ConfigError(
                    f"BACKUP_LOCAL_RETENTION must be an integer, got {raw!r}"
                ) from exc
            if retention < 1:
                raise ConfigError("BACKUP_LOCAL_RETENTION must keep at least one run")
        recipient = env.get("BACKUP_AGE_RECIPIENT", "").strip()
        if recipient and not re.fullmatch(r"age1[0-9a-z]+", recipient):
            raise ConfigError("BACKUP_AGE_RECIPIENT is not an age public key (age1...)")
        return cls(
            include_redis=env.get("BACKUP_INCLUDE_REDIS", "false").strip().lower()
            in {"1", "true", "yes", "on"},
            local_retention=retention,
            age_recipient=recipient,
        )


def read_env_file(path: Path) -> dict[str, str]:
    """KEY=VALUE lines; blank lines and ``#`` comments skipped; matching quotes stripped."""
    values: dict[str, str] = {}
    if not path.exists():
        raise ConfigError(f"{path} does not exist; copy backup.env.example there")
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key.strip()] = value
    return values


def read_manifest_paths(path: Path) -> list[Path]:
    """One absolute path per line; blank lines and ``#`` comments skipped."""
    paths: list[Path] = []
    if not path.exists():
        return paths
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith("/"):
            raise ConfigError(f"{path}: {line!r} is not an absolute path")
        paths.append(Path(line))
    return paths


# --------------------------------------------------------------------------- seams


@dataclass(frozen=True)
class Completed:
    code: int
    output: str


class CommandRunner:
    """Runs host commands. ``output_path`` streams stdout to a file (a dump is large);
    ``input_path`` feeds a file to stdin (``pg_restore --list`` reads the dump)."""

    def run(
        self,
        args: Sequence[str],
        *,
        timeout: int = 60,
        output_path: Path | None = None,
        input_path: Path | None = None,
    ) -> Completed:
        stdin = input_path.open("rb") if input_path is not None else None
        try:
            if output_path is None:
                result = subprocess.run(  # noqa: S603 (fixed argv, nothing from a request)
                    list(args),
                    stdin=stdin,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=timeout,
                    check=False,
                )
                return Completed(result.returncode, (result.stdout or "") + (result.stderr or ""))
            with output_path.open("wb") as out:
                result = subprocess.run(  # noqa: S603
                    list(args),
                    stdin=stdin,
                    stdout=out,
                    stderr=subprocess.PIPE,
                    timeout=timeout,
                    check=False,
                )
            return Completed(
                result.returncode, (result.stderr or b"").decode("utf-8", errors="replace")
            )
        finally:
            if stdin is not None:
                stdin.close()


# --------------------------------------------------------------------------- state


class BackupError(RuntimeError):
    def __init__(self, stage: str, reason: str) -> None:
        self.stage = stage
        self.reason = reason
        super().__init__(f"{stage}: {reason}")


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.UTC)


def _iso(instant: dt.datetime) -> str:
    return instant.astimezone(dt.UTC).replace(microsecond=0).isoformat()


def _parse_iso(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.UTC)


def read_json(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(tmp, path)


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def one_line(text: str, limit: int = 300) -> str:
    return " ".join(text.split())[:limit]


# ----------------------------------------------------------------------------- run


class Backup:
    def __init__(
        self,
        config: Config,
        paths: Paths,
        *,
        runner: CommandRunner | None = None,
        clock=now_utc,
        dry_run: bool = False,
        out=print,
    ) -> None:
        self.config = config
        self.paths = paths
        self.runner = runner or CommandRunner()
        self.clock = clock
        self.dry_run = dry_run
        self.out = out
        self.last = read_json(paths.last)

    # -- helpers --------------------------------------------------------------

    def _say(self, step: str, message: str) -> None:
        self.out(f"{_iso(self.clock())} {step}: {message}")

    def _compose(self, *args: str) -> list[str]:
        return [
            "docker",
            "compose",
            "-f",
            str(self.paths.repo / "docker-compose.prod.yml"),
            *args,
        ]

    def _psql(self, sql: str) -> Completed:
        return self.runner.run(
            self._compose(
                "exec",
                "-T",
                "postgres",
                "sh",
                "-c",
                'exec psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1 -Atqc '
                + _sh(sql),
            ),
            timeout=60,
        )

    def _record(self, key: str, payload: Mapping[str, Any]) -> None:
        self.last[key] = dict(payload)
        write_json(self.paths.last, self.last)

    # -- the run --------------------------------------------------------------

    def run(self) -> int:
        started = self.clock()
        if self.runner.run(["flock", "-n", str(self.paths.lock), "true"]).code != 0:
            self._say(
                "skip",
                f"deploy lock {self.paths.lock} is held; a deploy may be restarting postgres",
            )
            if not self.dry_run:
                self._record("last_skipped", {"at": _iso(started), "reason": "deploy lock held"})
            return SKIPPED_EXIT
        stamp = f"{started:%Y%m%dT%H%M%SZ}"
        final = self.paths.root / stamp
        partial = self.paths.root / f"{stamp}.partial"
        if self.dry_run:
            return self._plan(started)
        self.paths.root.mkdir(parents=True, exist_ok=True)
        partial.mkdir()
        files: list[dict[str, Any]] = []
        manifest: dict[str, Any] = {
            "host": socket.gethostname(),
            "started_at": _iso(started),
            "run": stamp,
            "files": files,
        }
        try:
            manifest["git_sha"] = self._git_sha()
            manifest["alembic_revision"] = self._alembic_revision()
            manifest["postgres_version"] = self._postgres_version()
            files.append(self._dump_database(partial, stamp, manifest["git_sha"]))
            files.extend(self._sweep_predeploy(partial))
            bundle = self._config_bundle(partial)
            manifest["config"] = bundle["summary"]
            if bundle["file"] is not None:
                files.append(bundle["file"])
            if self.config.include_redis:
                files.append(self._dump_redis(partial))
            manifest["finished_at"] = _iso(self.clock())
            manifest["seconds"] = int((self.clock() - started).total_seconds())
            write_json(partial / "manifest.json", manifest)
            partial.rename(final)
        except BackupError as exc:
            self._say("failed", f"{exc.stage}: {exc.reason}")
            shutil.rmtree(partial, ignore_errors=True)
            self._record(
                "last_failure",
                {"at": _iso(self.clock()), "stage": exc.stage, "reason": exc.reason},
            )
            return 1
        total = sum(int(item["size"]) for item in files)
        self._record(
            "last_success",
            {
                "at": manifest["finished_at"],
                "path": str(final),
                "seconds": manifest["seconds"],
                "bytes": total,
                "files": [item["name"] for item in files],
                "git_sha": manifest["git_sha"],
                "alembic_revision": manifest["alembic_revision"],
            },
        )
        removed = self._retain()
        self._say(
            "done",
            f"{final} ({len(files)} files, {total} bytes, {manifest['seconds']} s); "
            f"removed {len(removed)} old run(s)",
        )
        return 0

    def _plan(self, started: dt.datetime) -> int:
        self._say("dry run", "nothing is written; this is what a run would do")
        self._say("dump", f"pg_dump -Fc through compose at {self.paths.repo}")
        since = _parse_iso((self.last.get("last_success") or {}).get("at"))
        candidates = self._predeploy_candidates(since)
        self._say(
            "predeploy",
            f"{len(candidates)} dump(s) newer than {_iso(since) if since else 'ever'} "
            "would be swept: " + (", ".join(p.name for p in candidates) or "none"),
        )
        present, missing = self._split_manifest_paths()
        self._say(
            "config",
            f"{len(present)} path(s) present, {len(missing)} missing: "
            + (", ".join(map(str, missing)) or "none"),
        )
        if self.config.age_recipient:
            self._say("config", f"bundle would be encrypted to {self.config.age_recipient[:12]}...")
        else:
            self._say("config", "no BACKUP_AGE_RECIPIENT: the bundle would not be kept")
        self._say("redis", "included" if self.config.include_redis else "not included")
        old = self._retention_candidates(extra=1)
        self._say(
            "retention",
            f"keep {self.config.local_retention}; would remove: "
            + (", ".join(p.name for p in old) or "none"),
        )
        return 0

    # -- steps ----------------------------------------------------------------

    def _git_sha(self) -> str:
        result = self.runner.run(["git", "-C", str(self.paths.repo), "rev-parse", "HEAD"])
        sha = result.output.strip()
        if result.code != 0 or not _SHA.fullmatch(sha):
            raise BackupError("git", f"could not read live HEAD: {one_line(result.output)}")
        return sha

    def _alembic_revision(self) -> str:
        result = self._psql("SELECT version_num FROM alembic_version LIMIT 1")
        revision = result.output.strip()
        if result.code != 0 or not _REVISION.fullmatch(revision):
            raise BackupError(
                "alembic", f"could not read alembic_version: {one_line(result.output)}"
            )
        return revision

    def _postgres_version(self) -> str:
        result = self._psql("SELECT version()")
        if result.code != 0:
            raise BackupError("postgres", f"could not read version(): {one_line(result.output)}")
        return one_line(result.output, 120)

    def _verify_and_hash(self, path: Path, kind: str) -> dict[str, Any]:
        if not path.is_file() or path.stat().st_size == 0:
            raise BackupError(kind, f"{path.name} is empty")
        listed = self.runner.run(
            self._compose("exec", "-T", "postgres", "pg_restore", "--list"),
            timeout=600,
            input_path=path,
        )
        if listed.code != 0:
            raise BackupError(
                kind, f"pg_restore --list rejected {path.name}: {one_line(listed.output)}"
            )
        return {
            "name": path.name,
            "kind": kind,
            "size": path.stat().st_size,
            "sha256": sha256_of(path),
        }

    def _dump_database(self, run_dir: Path, stamp: str, sha: str) -> dict[str, Any]:
        target = run_dir / f"travel-scanner-{stamp}-{sha[:12]}.dump"
        self._say("dump", f"pg_dump -Fc -> {target.name}")
        result = self.runner.run(
            self._compose(
                "exec",
                "-T",
                "postgres",
                "sh",
                "-c",
                'exec pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc',
            ),
            timeout=3600,
            output_path=target,
        )
        if result.code != 0:
            raise BackupError("dump", f"pg_dump exited {result.code}: {one_line(result.output)}")
        entry = self._verify_and_hash(target, "database")
        self._say("dump", f"verified, {entry['size']} bytes, sha256 {entry['sha256'][:12]}")
        return entry

    def _predeploy_candidates(self, since: dt.datetime | None) -> list[Path]:
        found = []
        for path in sorted(self.paths.predeploy_dir.glob("travel_scanner_predeploy_*.dump")):
            if not path.is_file():
                continue
            modified = dt.datetime.fromtimestamp(path.stat().st_mtime, tz=dt.UTC)
            if since is None or modified > since:
                found.append(path)
        return found

    def _sweep_predeploy(self, run_dir: Path) -> list[dict[str, Any]]:
        since = _parse_iso((self.last.get("last_success") or {}).get("at"))
        entries = []
        for source in self._predeploy_candidates(since):
            target = run_dir / source.name
            self._say("predeploy", f"sweeping {source}")
            shutil.copyfile(source, target)
            entries.append(self._verify_and_hash(target, "predeploy"))
        return entries

    def _split_manifest_paths(self) -> tuple[list[Path], list[Path]]:
        present, missing = [], []
        for path in read_manifest_paths(self.paths.manifest_paths):
            (present if path.exists() else missing).append(path)
        return present, missing

    def _config_bundle(self, run_dir: Path) -> dict[str, Any]:
        present, missing = self._split_manifest_paths()
        summary: dict[str, Any] = {
            "included": [str(p) for p in present],
            "missing": [str(p) for p in missing],
            "encrypted": False,
        }
        if not present:
            self._say("config", "no manifest path exists on this host; no bundle")
            return {"summary": summary, "file": None}
        if not self.config.age_recipient:
            self._say(
                "config",
                f"{len(present)} path(s) present but no BACKUP_AGE_RECIPIENT; bundle not kept",
            )
            summary["kept"] = False
            return {"summary": summary, "file": None}
        # The plain tar holds secrets: a private temporary directory, removed in `finally`.
        tmp = Path(tempfile.mkdtemp(prefix="travel-scanner-backup."))
        try:
            os.chmod(tmp, 0o700)
            plain = tmp / "config.tar"
            with tarfile.open(plain, "w") as archive:
                for path in present:
                    archive.add(str(path), arcname=str(path).lstrip("/"))
            summary["plain_sha256"] = sha256_of(plain)
            target = run_dir / "config.tar.age"
            result = self.runner.run(
                ["age", "-r", self.config.age_recipient, "-o", str(target), str(plain)],
                timeout=300,
            )
            if result.code != 0 or not target.is_file() or target.stat().st_size == 0:
                raise BackupError("config", f"age exited {result.code}: {one_line(result.output)}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        summary["encrypted"] = True
        summary["kept"] = True
        self._say("config", f"{len(present)} path(s) -> {target.name}")
        return {
            "summary": summary,
            "file": {
                "name": target.name,
                "kind": "config",
                "size": target.stat().st_size,
                "sha256": sha256_of(target),
            },
        }

    def _dump_redis(self, run_dir: Path) -> dict[str, Any]:
        target = run_dir / "redis.rdb"
        self._say("redis", f"SAVE and copy dump.rdb -> {target.name}")
        result = self.runner.run(
            self._compose(
                "exec", "-T", "redis", "sh", "-c", "redis-cli SAVE >/dev/null && cat /data/dump.rdb"
            ),
            timeout=600,
            output_path=target,
        )
        if result.code != 0 or not target.is_file() or target.stat().st_size == 0:
            raise BackupError(
                "redis", f"redis dump failed ({result.code}): {one_line(result.output)}"
            )
        return {
            "name": target.name,
            "kind": "redis",
            "size": target.stat().st_size,
            "sha256": sha256_of(target),
        }

    # -- retention ------------------------------------------------------------

    def _complete_runs(self) -> list[Path]:
        if not self.paths.root.exists():
            return []
        return sorted(
            (p for p in self.paths.root.iterdir() if p.is_dir() and RUN_DIR.match(p.name)),
            key=lambda p: p.name,
            reverse=True,
        )

    def _retention_candidates(self, *, extra: int = 0) -> list[Path]:
        keep = max(self.config.local_retention - extra, 0)
        return self._complete_runs()[keep:]

    def _retain(self) -> list[Path]:
        removed = []
        for old in self._retention_candidates():
            shutil.rmtree(old, ignore_errors=True)
            removed.append(old)
        cutoff = self.clock() - dt.timedelta(days=1)
        for stale in self.paths.root.glob("*.partial"):
            if (
                stale.is_dir()
                and dt.datetime.fromtimestamp(stale.stat().st_mtime, tz=dt.UTC) < cutoff
            ):
                shutil.rmtree(stale, ignore_errors=True)
        return removed


def _sh(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


# ----------------------------------------------------------------------------- cli


def status_text(paths: Paths, *, now: dt.datetime | None = None) -> tuple[str, int]:
    """One line per record plus a verdict; exit 1 when the last run failed or is stale."""
    now = now or now_utc()
    last = read_json(paths.last)
    lines = [f"state file: {paths.last}"]
    success = last.get("last_success") or {}
    failure = last.get("last_failure") or {}
    skipped = last.get("last_skipped") or {}
    code = 0
    at = _parse_iso(success.get("at"))
    if at is None:
        lines.append("last success: never")
        code = 1
    else:
        hours = (now - at).total_seconds() / 3600
        lines.append(
            f"last success: {success.get('at')} ({hours:.1f} h ago) "
            f"{success.get('bytes', '?')} bytes "
            f"{len(success.get('files') or [])} file(s) at {success.get('path', '?')}"
        )
        if hours > 36:
            lines.append(f"BACKUP STALE: last success is {hours:.1f} h old (limit 36 h)")
            code = 1
    if failure:
        lines.append(
            f"last failure: {failure.get('at')} {failure.get('stage')}: {failure.get('reason')}"
        )
        failed_at = _parse_iso(failure.get("at"))
        if at is None or (failed_at is not None and failed_at > at):
            lines.append(f"BACKUP FAILED: {failure.get('stage')}: {failure.get('reason')}")
            code = 1
    if skipped:
        lines.append(f"last skipped: {skipped.get('at')} {skipped.get('reason')}")
    return "\n".join(lines), code


def main(argv: Sequence[str] | None = None, *, paths: Paths | None = None) -> int:
    parser = argparse.ArgumentParser(description="Nightly verified backups of the production host.")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="take, verify and record one backup")
    run.add_argument(
        "--dry-run", action="store_true", help="print what a run would do, write nothing"
    )
    status = sub.add_parser(
        "status", help="print last.json; exit 1 when the last run failed or is stale"
    )
    status.add_argument("--state-dir", help="read last.json from this directory instead")
    args = parser.parse_args(argv)
    paths = paths or Paths()
    if args.command == "status":
        if args.state_dir:
            paths = Paths(state_dir=Path(args.state_dir))
        text, code = status_text(paths)
        print(text)
        return code
    try:
        config = Config.from_mapping(read_env_file(paths.env_file))
    except ConfigError as exc:
        print(f"config error: {exc}", file=sys.stderr)
        return 2
    return Backup(config, paths, dry_run=args.dry_run).run()


if __name__ == "__main__":
    sys.exit(main())
