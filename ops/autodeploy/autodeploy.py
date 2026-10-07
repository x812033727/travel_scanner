"""Deploy ``main`` on the production host without a person at the keyboard.

Nothing deploys ``main`` after a merge: every deploy is someone opening SSH and
running ``/root/deploy-travel-scanner.sh``. This module is one ``tick`` of a root
systemd timer (``travel-scanner-autodeploy.timer``, every five minutes). A tick walks a
fixed list of gates and either does nothing, waits, or runs that same script. The
script stays the only executor, so the deploy hold (``ops/release/README.md``), its
rule 1, the flock, the rollback and the logs all keep working; this file only decides
whether to run it now. The gates, in order:

1. ``/root/travel-scanner-autodeploy.paused`` exists: a previous automatic deploy
   failed (the script rolled back on its own). Print the reason, do nothing, until a
   person deletes the file.
2. ``origin/main`` is not ahead of the live ``HEAD``: nothing to do.
3. The newest commit is younger than the quiet period: wait, so a run of merges
   becomes one rebuild (every deploy restarts every container, skill ``deploy``).
4. The ``CI`` workflow for that commit is not ``success``: wait (pending or red; red
   on main already opens an issue through ``.github/workflows/ci-red-main.yml``).
5. A configured blocked window (``Asia/Taipei``) is open: wait.
6. The deploy lock is held, or ``deploy-travel-scanner.sh --dry-run`` refuses (exit 3:
   the hold file, or a staged release that is prepared but not activated): wait.
7. A ``running`` paid video stage job (the same two selects as
   ``host-preflight.sh``): wait, and say so once after a configurable number of hours.
8. Otherwise run the script. Exit 0: run ``host-verify.sh`` for the new SHA and record
   PASS or FAIL. Any other exit: write the paused file and stop deploying.

``AUTODEPLOY_ENABLED=false`` and ``tick --dry-run`` walk every gate and print what
would happen, which is how the timer is watched for a week before it is enabled.

Standard library only and no ``fcntl`` (the host runs Python 3.14; the tests also run
on Windows). Every host command goes through ``CommandRunner`` and every GitHub call
through ``GitHubClient`` so the tests need neither the host nor the network. The state
file and the paused file never carry a secret.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

GITHUB_REPO = "x812033727/travel_scanner"
BRANCH = "main"
WORKFLOW_NAME = "CI"
REFUSED_EXIT = 3  # the deploy script's "NOT DEPLOYING: another release is in progress"
FIRST_LINE_LIMIT = 600  # bytes; same convention as the deploy hold
DEPLOY_TIMEOUT = 2 * 60 * 60  # a cold build is minutes, not hours; this is the safety net
TAIPEI = ZoneInfo("Asia/Taipei")

_SHA = re.compile(r"[0-9a-f]{40}")
_WINDOW = re.compile(r"^(\d{2}):(\d{2})-(\d{2}):(\d{2})$")
_TOTAL = re.compile(r"^TOTAL pass=(\d+) fail=(\d+)", re.MULTILINE)
_ONE_LINE = re.compile(r"[^\x00-\x1f\x7f]+")


# --------------------------------------------------------------------------- paths


@dataclass(frozen=True)
class Paths:
    """Everything on the host the poller reads or writes. Tests point these at a temp dir."""

    repo: Path = Path("/root/travel_scanner")
    deploy_script: Path = Path("/root/deploy-travel-scanner.sh")
    verify_script: Path = Path("/opt/travel-scanner-autodeploy/host-verify.sh")
    lock: Path = Path("/var/lock/travel-scanner-deploy.lock")
    log_dir: Path = Path("/root/deploy-logs")
    state_dir: Path = Path("/var/lib/travel-scanner-autodeploy")
    paused: Path = Path("/root/travel-scanner-autodeploy.paused")
    env_file: Path = Path("/etc/travel-scanner/autodeploy.env")

    @property
    def state(self) -> Path:
        return self.state_dir / "state.json"


# -------------------------------------------------------------------------- config


class ConfigError(RuntimeError):
    """The env file is missing something the poller cannot run without."""


@dataclass(frozen=True)
class Window:
    """A daily window in Asia/Taipei during which no deploy starts; may wrap midnight."""

    start: int  # minutes after midnight
    end: int

    def contains(self, local: dt.datetime) -> bool:
        minute = local.hour * 60 + local.minute
        if self.start <= self.end:
            return self.start <= minute < self.end
        return minute >= self.start or minute < self.end

    def __str__(self) -> str:
        return (
            f"{self.start // 60:02d}:{self.start % 60:02d}-{self.end // 60:02d}:{self.end % 60:02d}"
        )


@dataclass(frozen=True)
class Config:
    enabled: bool
    github_token: str
    quiet_minutes: int = 20
    wait_for_paid_work: bool = True
    blocked_windows: tuple[Window, ...] = ()
    notify_url: str = ""
    paid_work_notify_hours: float = 2.0

    @classmethod
    def from_mapping(cls, env: Mapping[str, str]) -> Config:
        token = env.get("AUTODEPLOY_GITHUB_TOKEN", "").strip()
        if not token:
            raise ConfigError(
                "AUTODEPLOY_GITHUB_TOKEN is empty: a fine-grained token with Actions: Read on "
                f"{GITHUB_REPO} is required to see whether CI is green"
            )
        return cls(
            enabled=_truthy(env.get("AUTODEPLOY_ENABLED", "false")),
            github_token=token,
            quiet_minutes=_int(env, "AUTODEPLOY_QUIET_MINUTES", 20),
            wait_for_paid_work=_truthy(env.get("AUTODEPLOY_WAIT_FOR_PAID_WORK", "true")),
            blocked_windows=tuple(parse_windows(env.get("AUTODEPLOY_BLOCKED_WINDOWS", ""))),
            notify_url=env.get("AUTODEPLOY_NOTIFY_URL", "").strip(),
            paid_work_notify_hours=_float(env, "AUTODEPLOY_PAID_WORK_NOTIFY_HOURS", 2.0),
        )


def _truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int(env: Mapping[str, str], key: str, default: int) -> int:
    raw = env.get(key, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ConfigError(f"{key} must be an integer, got {raw!r}") from exc
    if value < 0:
        raise ConfigError(f"{key} must not be negative")
    return value


def _float(env: Mapping[str, str], key: str, default: float) -> float:
    raw = env.get(key, "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError as exc:
        raise ConfigError(f"{key} must be a number, got {raw!r}") from exc
    if value < 0:
        raise ConfigError(f"{key} must not be negative")
    return value


def parse_windows(raw: str) -> list[Window]:
    windows: list[Window] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        match = _WINDOW.match(part)
        if not match:
            raise ConfigError(f"AUTODEPLOY_BLOCKED_WINDOWS entry {part!r} is not HH:MM-HH:MM")
        h1, m1, h2, m2 = (int(group) for group in match.groups())
        if h1 > 23 or h2 > 23 or m1 > 59 or m2 > 59:
            raise ConfigError(f"AUTODEPLOY_BLOCKED_WINDOWS entry {part!r} is not a time of day")
        windows.append(Window(h1 * 60 + m1, h2 * 60 + m2))
    return windows


def read_env_file(path: Path) -> dict[str, str]:
    """KEY=VALUE lines; blank lines and ``#`` comments skipped; matching quotes stripped."""
    values: dict[str, str] = {}
    if not path.exists():
        raise ConfigError(f"{path} does not exist; copy autodeploy.env.example there")
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


# --------------------------------------------------------------------------- seams


@dataclass(frozen=True)
class Completed:
    code: int
    output: str


class CommandRunner:
    """Runs host commands. ``log_path`` streams a long command's output to a file."""

    def run(
        self, args: Sequence[str], *, timeout: int = 60, log_path: Path | None = None
    ) -> Completed:
        # Every argv is built here from compiled paths and fixed words; nothing from a request.
        if log_path is None:
            result = subprocess.run(  # noqa: S603
                list(args),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                check=False,
            )
            return Completed(result.returncode, (result.stdout or "") + (result.stderr or ""))
        with log_path.open("ab") as handle:
            result = subprocess.run(  # noqa: S603
                list(args), stdout=handle, stderr=subprocess.STDOUT, timeout=timeout, check=False
            )
        return Completed(result.returncode, log_path.read_text(encoding="utf-8", errors="replace"))


class GitHubClient:
    """The same lookup ``apps/api/deployment_agent`` makes: the ``CI`` run for one SHA."""

    def __init__(self, token: str) -> None:
        self.token = token

    def ci_status(self, sha: str) -> tuple[str, str | None]:
        url = (
            f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs"
            f"?head_sha={sha}&branch={BRANCH}&event=push&per_page=30"
        )
        request = Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "User-Agent": "travel-scanner-autodeploy/1",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        try:
            with urlopen(request, timeout=15) as response:  # noqa: S310 (https, fixed host)
                payload = json.load(response)
        except (HTTPError, URLError, TimeoutError, ValueError) as exc:
            return f"unreachable ({exc.__class__.__name__})", None
        return ci_status_from_payload(payload)


def ci_status_from_payload(payload: Mapping[str, Any]) -> tuple[str, str | None]:
    for run in payload.get("workflow_runs", []):
        if run.get("name") != WORKFLOW_NAME:
            continue
        if run.get("status") == "completed":
            status = str(run.get("conclusion") or "unknown")
        else:
            status = str(run.get("status") or "unknown")
        return status, str(run.get("html_url") or "") or None
    return "missing", None


class Notifier:
    """One JSON POST per event. ``text`` for Slack and Telegram (chat_id in the URL),
    ``content`` for Discord. A failed post is printed and otherwise ignored."""

    def __init__(self, url: str) -> None:
        self.url = url

    def post(self, text: str) -> bool:
        if not self.url:
            return False
        body = json.dumps({"text": text, "content": text}).encode("utf-8")
        if not self.url.startswith("https://"):
            print("notify skipped: AUTODEPLOY_NOTIFY_URL is not https")
            return False
        request = Request(  # noqa: S310
            self.url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "travel-scanner-autodeploy/1",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=10):  # noqa: S310
                return True
        except (HTTPError, URLError, TimeoutError) as exc:
            print(f"notify failed: {exc.__class__.__name__}")
            return False


# --------------------------------------------------------------------------- state


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


def read_state(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


def write_state(path: Path, state: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix="state.", suffix=".json", dir=path.parent)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(tmp, path)


def one_line(text: str, limit: int = FIRST_LINE_LIMIT) -> str:
    joined = " ".join(_ONE_LINE.findall(text)).strip()
    encoded = joined.encode("utf-8")[:limit]
    return encoded.decode("utf-8", errors="ignore")


def write_paused(path: Path, *, sha: str, exit_code: int, log: Path, instant: dt.datetime) -> None:
    """Two lines like the deploy hold: one for people within 600 bytes, one JSON."""
    first = one_line(
        f"autodeploy paused: the automatic deploy of {sha[:12]} exited {exit_code} at "
        f"{_iso(instant)} and the deploy script rolled back on its own (log {log}); read the "
        "log, fix forward on main, then delete this file to let the timer deploy again"
    )
    record = {"sha": sha, "exit": exit_code, "log": str(log), "created_at": _iso(instant)}
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(first + "\n")
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def read_paused(path: Path) -> tuple[str, dict[str, Any]] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    lines = text.splitlines()
    first = one_line(lines[0]) if lines else ""
    record: dict[str, Any] = {}
    if len(lines) > 1:
        try:
            loaded = json.loads(lines[1])
        except ValueError:
            loaded = None
        if isinstance(loaded, dict):
            record = loaded
    return first, record


# ---------------------------------------------------------------------------- tick


@dataclass
class Decision:
    """What one tick concluded. ``action`` is one of paused, idle, wait, would_deploy,
    deployed, failed; ``reason`` is the one line a person reads in the state file."""

    action: str
    reason: str
    details: dict[str, Any] = field(default_factory=dict)


class Poller:
    def __init__(
        self,
        config: Config,
        paths: Paths,
        *,
        runner: CommandRunner | None = None,
        github: GitHubClient | None = None,
        notifier: Notifier | None = None,
        clock: Callable[[], dt.datetime] = now_utc,
        dry_run: bool = False,
        out: Callable[[str], None] = print,
    ) -> None:
        self.config = config
        self.paths = paths
        self.runner = runner or CommandRunner()
        self.github = github or GitHubClient(config.github_token)
        self.notifier = notifier or Notifier(config.notify_url)
        self.clock = clock
        self.dry_run = dry_run or not config.enabled
        self.out = out
        self.state = read_state(paths.state)

    # -- helpers --------------------------------------------------------------

    def _say(self, step: str, message: str) -> None:
        self.out(f"{_iso(self.clock())} {step}: {message}")

    def _git(self, *args: str, timeout: int = 60) -> Completed:
        return self.runner.run(["git", "-C", str(self.paths.repo), *args], timeout=timeout)

    def _psql(self, sql: str) -> Completed:
        return self.runner.run(
            [
                "docker",
                "compose",
                "-f",
                str(self.paths.repo / "docker-compose.prod.yml"),
                "exec",
                "-T",
                "postgres",
                "psql",
                "-U",
                "travel",
                "-d",
                "travel_scanner",
                "-Atc",
                sql,
            ],
            timeout=60,
        )

    def _finish(self, decision: Decision) -> Decision:
        instant = self.clock()
        self.state["last_tick"] = _iso(instant)
        self.state["last_decision"] = {
            "action": decision.action,
            "reason": decision.reason,
            **{k: v for k, v in decision.details.items() if k not in {"action", "reason"}},
        }
        self.state["dry_run"] = self.dry_run
        if decision.action not in {"wait"} or decision.details.get("gate") != "paid_work":
            self.state.pop("paid_work_since", None)
            self.state.pop("paid_work_notified_at", None)
        write_state(self.paths.state, self.state)
        self._say("decision", f"{decision.action}: {decision.reason}")
        return decision

    def _wait(self, gate: str, reason: str, **details: Any) -> Decision:
        return self._finish(Decision("wait", reason, {"gate": gate, **details}))

    # -- the tick -------------------------------------------------------------

    def tick(self) -> Decision:
        paused = read_paused(self.paths.paused)
        if paused is not None:
            first, _ = paused
            self._say("paused", f"{self.paths.paused} exists: {first or '(empty file)'}")
            return self._finish(
                Decision("paused", first or "paused file present", {"gate": "paused"})
            )
        if self.dry_run:
            self._say("mode", "dry run: every gate is evaluated, nothing is deployed")

        fetched = self._git("fetch", "--quiet", "origin", BRANCH, timeout=120)
        if fetched.code != 0:
            return self._wait(
                "fetch", f"git fetch origin {BRANCH} failed: {one_line(fetched.output, 200)}"
            )
        live = self._git("rev-parse", "HEAD").output.strip()
        target = self._git("rev-parse", f"refs/remotes/origin/{BRANCH}").output.strip()
        if not _SHA.fullmatch(live) or not _SHA.fullmatch(target):
            return self._wait(
                "git", f"could not read live ({live[:12]!r}) or origin/{BRANCH} ({target[:12]!r})"
            )
        self._say("git", f"live {live[:12]}, origin/{BRANCH} {target[:12]}")
        if live == target:
            return self._finish(
                Decision("idle", f"live is origin/{BRANCH} ({live[:12]})", {"sha": live})
            )
        if self._git("merge-base", "--is-ancestor", live, target).code != 0:
            return self._wait(
                "git",
                f"live {live[:12]} is not an ancestor of origin/{BRANCH} {target[:12]}; the deploy "
                "script's fast-forward would refuse, a person has to look",
                sha=target,
            )

        committed = self._git("log", "-1", "--format=%ct", target).output.strip()
        try:
            commit_time = dt.datetime.fromtimestamp(int(committed), tz=dt.UTC)
        except ValueError:
            return self._wait("git", f"could not read the commit time of {target[:12]}", sha=target)
        age = self.clock() - commit_time
        quiet = dt.timedelta(minutes=self.config.quiet_minutes)
        if age < quiet:
            left = int((quiet - age).total_seconds() // 60) + 1
            return self._wait(
                "quiet",
                f"{target[:12]} is {int(age.total_seconds() // 60)} min old; quiet period "
                f"is {self.config.quiet_minutes} min, {left} min to go",
                sha=target,
            )

        status, url = self.github.ci_status(target)
        self._say(
            "ci", f"{WORKFLOW_NAME} for {target[:12]} is {status}{f' ({url})' if url else ''}"
        )
        if status != "success":
            return self._wait(
                "ci", f"{WORKFLOW_NAME} for {target[:12]} is {status}", sha=target, ci_url=url
            )

        local = self.clock().astimezone(TAIPEI)
        for window in self.config.blocked_windows:
            if window.contains(local):
                return self._wait(
                    "window",
                    f"blocked window {window} Asia/Taipei is open (now {local:%H:%M})",
                    sha=target,
                )

        if self.runner.run(["flock", "-n", str(self.paths.lock), "true"]).code != 0:
            return self._wait("lock", f"deploy lock {self.paths.lock} is held", sha=target)
        probe = self.runner.run([str(self.paths.deploy_script), "--dry-run"], timeout=300)
        if probe.code == REFUSED_EXIT:
            return self._wait(
                "hold", f"deploy script refuses: {one_line(probe.output, 300)}", sha=target
            )
        if probe.code != 0:
            return self._wait(
                "dry-run",
                f"deploy script --dry-run exited {probe.code}: {one_line(probe.output, 300)}",
                sha=target,
            )

        if self.config.wait_for_paid_work:
            paid = self._paid_work()
            if paid is not None:
                return paid

        if self.dry_run:
            return self._finish(
                Decision("would_deploy", f"would deploy {target[:12]} now", {"sha": target})
            )
        return self._deploy(live, target)

    def _paid_work(self) -> Decision | None:
        stage = self._psql(
            "select status, count(*), min(created_at) from video_stage_jobs "
            "where status in ('queued', 'running', 'uncertain') group by status"
        )
        media = self._psql(
            "select status, count(*), min(created_at) from video_media_jobs "
            "where status in ('queued', 'submitted') group by status"
        )
        self._say("paid work", f"stage jobs: {one_line(stage.output, 200) or 'none'}")
        self._say("paid work", f"media jobs: {one_line(media.output, 200) or 'none'}")
        if stage.code != 0:
            return self._wait(
                "paid_work", f"could not read video_stage_jobs: {one_line(stage.output, 200)}"
            )
        running = [line for line in stage.output.splitlines() if line.startswith("running|")]
        if not running:
            return None
        instant = self.clock()
        since = _parse_iso(self.state.get("paid_work_since")) or instant
        self.state["paid_work_since"] = _iso(since)
        held_for = instant - since
        hours = held_for.total_seconds() / 3600
        if (
            self.config.paid_work_notify_hours
            and hours >= self.config.paid_work_notify_hours
            and not self.state.get("paid_work_notified_at")
        ):
            self.notifier.post(
                f"mokaair autodeploy: a running paid video stage job has held the deploy back for "
                f"{hours:.1f} h ({running[0]}); it deploys when the job settles"
            )
            self.state["paid_work_notified_at"] = _iso(instant)
        return self._wait(
            "paid_work",
            f"a running paid video stage job ({running[0]}) would turn uncertain if its "
            f"worker restarted; waiting since {_iso(since)}",
        )

    def _deploy(self, live: str, target: str) -> Decision:
        started = self.clock()
        self.paths.log_dir.mkdir(parents=True, exist_ok=True)
        log = self.paths.log_dir / f"auto-{started:%Y%m%d_%H%M%S}.log"
        self._say("deploy", f"{live[:12]} -> {target[:12]}, log {log}")
        try:
            result = self.runner.run(
                [str(self.paths.deploy_script)], timeout=DEPLOY_TIMEOUT, log_path=log
            )
        except subprocess.TimeoutExpired:
            result = Completed(124, f"deploy script did not finish within {DEPLOY_TIMEOUT} s")
        finished = self.clock()
        record: dict[str, Any] = {
            "sha": target,
            "previous": live,
            "started_at": _iso(started),
            "finished_at": _iso(finished),
            "seconds": int((finished - started).total_seconds()),
            "exit": result.code,
            "log": str(log),
        }
        if result.code != 0:
            write_paused(
                self.paths.paused, sha=target, exit_code=result.code, log=log, instant=finished
            )
            record["paused"] = str(self.paths.paused)
            self.state["last_deploy"] = record
            self.notifier.post(
                f"mokaair autodeploy FAILED: deploy of {target[:12]} exited {result.code}; "
                f"the script rolled back; automatic deploys are paused until "
                f"{self.paths.paused} is removed (log {log})"
            )
            return self._finish(
                Decision("failed", f"deploy of {target[:12]} exited {result.code}; paused", record)
            )
        record["verify"] = self._verify(target)
        self.state["last_deploy"] = record
        verdict = record["verify"]["result"]
        self.notifier.post(
            f"mokaair autodeploy: deployed {target[:12]} in {record['seconds']} s, verify {verdict}"
        )
        return self._finish(
            Decision("deployed", f"deployed {target[:12]}, verify {verdict}", record)
        )

    def _verify(self, sha: str) -> dict[str, Any]:
        """``host-verify.sh`` with ``EXPECTED_SHA`` filled in, as the skill does with sed."""
        try:
            template = self.paths.verify_script.read_text(encoding="utf-8")
        except OSError as exc:
            return {
                "result": "SKIPPED",
                "reason": f"{self.paths.verify_script}: {exc.__class__.__name__}",
            }
        filled, count = re.subn(
            r'^EXPECTED_SHA=""$', f'EXPECTED_SHA="{sha}"', template, count=1, flags=re.M
        )
        if count != 1:
            return {"result": "SKIPPED", "reason": "verify script has no EXPECTED_SHA line to fill"}
        log = self.paths.log_dir / f"auto-verify-{self.clock():%Y%m%d_%H%M%S}.log"
        self.paths.state_dir.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix="verify.", suffix=".sh", dir=self.paths.state_dir)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(filled)
        try:
            result = self.runner.run(["bash", tmp], timeout=600, log_path=log)
        finally:
            try:
                os.unlink(tmp)
            except OSError:
                pass
        match = _TOTAL.search(result.output)
        if match is None:
            return {
                "result": "FAIL",
                "reason": f"no TOTAL line (exit {result.code})",
                "log": str(log),
            }
        passed, failed = int(match.group(1)), int(match.group(2))
        self._say("verify", f"pass={passed} fail={failed} ({log})")
        return {
            "result": "PASS" if failed == 0 else "FAIL",
            "pass": passed,
            "fail": failed,
            "log": str(log),
        }


# ----------------------------------------------------------------------------- cli


def status_text(paths: Paths) -> str:
    lines = [f"state file: {paths.state}"]
    state = read_state(paths.state)
    if not state:
        lines.append("  (no tick recorded yet)")
    else:
        lines.append(json.dumps(state, indent=2, sort_keys=True))
    paused = read_paused(paths.paused)
    if paused is None:
        lines.append(f"paused file: none ({paths.paused})")
    else:
        lines.append(f"PAUSED ({paths.paused}): {paused[0] or '(empty file)'}")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None, *, paths: Paths | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deploy main on the production host when it is green."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    tick = sub.add_parser("tick", help="walk the gates once; deploy when they all pass")
    tick.add_argument(
        "--dry-run", action="store_true", help="print what would happen, deploy nothing"
    )
    sub.add_parser("status", help="print the state file and the paused file")
    args = parser.parse_args(argv)
    paths = paths or Paths()
    if args.command == "status":
        print(status_text(paths))
        return 0
    try:
        config = Config.from_mapping(read_env_file(paths.env_file))
    except ConfigError as exc:
        print(f"config error: {exc}", file=sys.stderr)
        return 2
    decision = Poller(config, paths, dry_run=args.dry_run).tick()
    return 1 if decision.action == "failed" else 0


if __name__ == "__main__":
    sys.exit(main())
