"""Deploy ``main`` on the production host without a person at the keyboard.

Nothing deploys ``main`` after a merge: every deploy is someone opening SSH and
running ``/root/deploy-travel-scanner.sh``. This module is one ``tick`` of a root
systemd timer (``travel-scanner-autodeploy.timer``, every five minutes). A tick walks a
fixed list of gates and either does nothing, waits, or runs that same script. The
script stays the only executor, so the deploy hold (``ops/release/README.md``), its
rule 1, the flock, the rollback and the logs all keep working; this file only decides
whether to run it now. The gates, in order:

1. ``/root/travel-scanner-autodeploy.paused`` exists: a previous automatic deploy
   failed. The deploy and video-ai-worker state require readback; do nothing until a
   person reconciles them and deletes the file.
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

Two more duties (docs/ops/admin-redeploy-button-and-daily-autodeploy-plan.md):

- **Admin button requests.** Before the gates, a tick looks for a ``queued``
  ``deployment_runs`` row whose ``metadata_json.executor`` is ``host_timer`` (the admin
  page inserts it; only the owner role can). It claims the row with a conditional
  ``UPDATE``, walks the same gates minus the schedule (quiet period, deploy windows, daily
  limit, blocked windows), runs the same script (``--force`` to rebuild the live commit),
  and writes stages, events and the result back to the row. A gate that holds refuses the
  request instead of waiting; the paused file refuses it too (no forced deploys).
- **Heartbeat.** Every tick ends by upserting ``deployment_host_status`` (one row) with what
  it saw, so the admin page can show the timer's decision, its last deploy and a window
  that closed without a deploy. The page is the owner's notification channel.

Both use ``psql`` in the postgres container, which a deploy never restarts. SQL is built from
fixed statements; a value is either checked against a UUID or SHA pattern or passed as a
dollar-quoted literal (``sql_literal``).

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
import secrets
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
# The systemd unit has TimeoutStartSec=2h. Leave 30 minutes for this process to
# catch a stuck warm drain, write its paused/failed receipt and notify the owner
# before systemd can kill the entire cgroup without that receipt. The RQ stage
# timeout is 20 minutes; an ordinary rebuild takes minutes.
DEPLOY_TIMEOUT = 90 * 60
TAIPEI = ZoneInfo("Asia/Taipei")

_SHA = re.compile(r"[0-9a-f]{40}")
_WINDOW = re.compile(r"^(\d{2}):(\d{2})-(\d{2}):(\d{2})$")
_TOTAL = re.compile(r"^TOTAL pass=(\d+) fail=(\d+)", re.MULTILINE)
_ONE_LINE = re.compile(r"[^\x00-\x1f\x7f]+")
_UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
REQUEST_MODES = {"latest", "rebuild"}
HOST_EXECUTOR = "host_timer"


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
    """A daily window in Asia/Taipei (a blocked or an allowed one); may wrap midnight."""

    start: int  # minutes after midnight
    end: int

    def contains(self, local: dt.datetime) -> bool:
        minute = local.hour * 60 + local.minute
        if self.start <= self.end:
            return self.start <= minute < self.end
        return minute >= self.start or minute < self.end

    def next_start(self, local: dt.datetime) -> dt.datetime:
        """The first start of this window at or after ``local`` (same time zone)."""
        start = local.replace(
            hour=self.start // 60, minute=self.start % 60, second=0, microsecond=0
        )
        if start < local.replace(second=0, microsecond=0):
            start += dt.timedelta(days=1)
        return start

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
    deploy_windows: tuple[Window, ...] = ()
    max_auto_deploys_per_day: int = 0

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
            blocked_windows=tuple(
                parse_windows(
                    env.get("AUTODEPLOY_BLOCKED_WINDOWS", ""), "AUTODEPLOY_BLOCKED_WINDOWS"
                )
            ),
            deploy_windows=tuple(
                parse_windows(env.get("AUTODEPLOY_DEPLOY_WINDOWS", ""), "AUTODEPLOY_DEPLOY_WINDOWS")
            ),
            max_auto_deploys_per_day=_int(env, "AUTODEPLOY_MAX_AUTO_DEPLOYS_PER_DAY", 0),
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


def parse_windows(raw: str, key: str = "AUTODEPLOY_BLOCKED_WINDOWS") -> list[Window]:
    windows: list[Window] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        match = _WINDOW.match(part)
        if not match:
            raise ConfigError(f"{key} entry {part!r} is not HH:MM-HH:MM")
        h1, m1, h2, m2 = (int(group) for group in match.groups())
        if h1 > 23 or h2 > 23 or m1 > 59 or m2 > 59:
            raise ConfigError(f"{key} entry {part!r} is not a time of day")
        if h1 * 60 + m1 == h2 * 60 + m2:
            raise ConfigError(f"{key} entry {part!r} is empty (start equals end)")
        windows.append(Window(h1 * 60 + m1, h2 * 60 + m2))
    return windows


def next_window_start(windows: Sequence[Window], local: dt.datetime) -> dt.datetime | None:
    """The soonest start of any window at or after ``local``; None when there are none."""
    starts = [window.next_start(local) for window in windows]
    return min(starts) if starts else None


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


def sql_literal(value: Any) -> str:
    """A PostgreSQL literal for ``value``: NULL, or dollar-quoted with a tag the text lacks."""
    if value is None:
        return "NULL"
    text = str(value).replace("\x00", "")
    tag = "ad"
    # With "$tag" nowhere in the text, the first "$tag$" after the opening one is the closing
    # one: no match can start inside the text or straddle its end.
    while f"${tag}" in text:
        tag = f"ad{secrets.token_hex(4)}"
    return f"${tag}${text}${tag}$"


def write_paused(path: Path, *, sha: str, exit_code: int, log: Path, instant: dt.datetime) -> None:
    """Two lines like the deploy hold: one for people within 600 bytes, one JSON."""
    first = one_line(
        f"autodeploy paused: the automatic deploy of {sha[:12]} exited {exit_code} at "
        f"{_iso(instant)} (log {log}); deployment and video-ai-worker state require readback. "
        "Automatic deploys stay paused until an operator reconciles the state and removes this file"
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
        # What this tick saw, for the heartbeat row the admin page reads.
        self.report: dict[str, Any] = {}

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
        self._track_window(decision, instant)
        write_state(self.paths.state, self.state)
        self._say("decision", f"{decision.action}: {decision.reason}")
        self._heartbeat()
        return decision

    def _wait(self, gate: str, reason: str, **details: Any) -> Decision:
        return self._finish(Decision("wait", reason, {"gate": gate, **details}))

    def _open_deploy_window(self, local: dt.datetime) -> Window | None:
        for window in self.config.deploy_windows:
            if window.contains(local):
                return window
        return None

    def _track_window(self, decision: Decision, instant: dt.datetime) -> None:
        """Remember why a deploy window is not deploying, so its end can say so once.

        Inside an open deploy window, a ``wait`` (CI red, paid work, a hold...) records the
        first time and the latest gate in ``window_miss``; a deploy, a failure (which notifies
        on its own) or an idle tick clears it. Outside every window a pending ``window_miss``
        is the window that ended without a deploy: notify once and keep it as
        ``last_missed_window``. ``paused`` neither records nor clears: the paused file says why.
        """
        if not self.config.deploy_windows or decision.action == "paused":
            return
        if decision.details.get("request"):
            return  # an admin button request says nothing about the automatic schedule
        local = instant.astimezone(TAIPEI)
        window = self._open_deploy_window(local)
        if window is not None:
            if decision.action == "wait" and decision.details.get("gate") != "daily_limit":
                previous = self.state.get("window_miss") or {}
                self.state["window_miss"] = {
                    "window": str(window),
                    "since": previous.get("since") or _iso(instant),
                    "gate": decision.details.get("gate"),
                    "reason": decision.reason,
                    "sha": decision.details.get("sha"),
                }
            else:
                self.state.pop("window_miss", None)
            return
        miss = self.state.pop("window_miss", None)
        if not miss:
            return
        sha = str(miss.get("sha") or "")[:12] or "main"
        self.notifier.post(
            f"mokaair autodeploy: deploy window {miss.get('window')} Asia/Taipei closed without "
            f"deploying {sha}; last gate {miss.get('gate')}: {miss.get('reason')}"
        )
        self.state["last_missed_window"] = {**miss, "notified_at": _iso(instant)}

    def _deploys_today(self, local: dt.datetime) -> int:
        record = self.state.get("auto_deploys_today") or {}
        if record.get("date") != local.date().isoformat():
            return 0
        try:
            return int(record.get("count", 0))
        except (TypeError, ValueError):
            return 0

    def _schedule(self, target: str) -> Decision | None:
        """The deploy windows and the daily limit; None when neither holds the deploy back."""
        local = self.clock().astimezone(TAIPEI)
        if self.config.deploy_windows and self._open_deploy_window(local) is None:
            upcoming = next_window_start(self.config.deploy_windows, local)
            assert upcoming is not None
            windows = ", ".join(str(window) for window in self.config.deploy_windows)
            return self._wait(
                "schedule",
                f"outside the deploy window {windows} Asia/Taipei (now {local:%H:%M}); "
                f"next opens {upcoming:%Y-%m-%d %H:%M}",
                sha=target,
            )
        limit = self.config.max_auto_deploys_per_day
        if limit and self._deploys_today(local) >= limit:
            return self._wait(
                "daily_limit",
                f"already deployed {limit} time(s) automatically on {local.date().isoformat()} "
                f"(Asia/Taipei); {target[:12]} waits for tomorrow's window",
                sha=target,
            )
        return None

    # -- what the tick saw, for the admin page ----------------------------------

    def _describe(self, live: str, target: str) -> None:
        """Live and target SHA, the target's subject and the commits between them."""
        self.report.update(live=live, target=target)
        subject = self._git("log", "-1", "--format=%s", target)
        if subject.code == 0:
            self.report["subject"] = one_line(subject.output, 255)
        if live == target:
            self.report["commits"] = []
            return
        listed = self._git("log", "--format=%H%x1f%s", "-20", f"{live}..{target}")
        commits = []
        if listed.code == 0:
            for line in listed.output.splitlines():
                sha, _, text = line.partition("\x1f")
                if _SHA.fullmatch(sha):
                    commits.append({"sha": sha, "subject": one_line(text, 255)})
        self.report["commits"] = commits

    def _ci(self, sha: str) -> tuple[str, str | None]:
        status, url = self.github.ci_status(sha)
        self._say("ci", f"{WORKFLOW_NAME} for {sha[:12]} is {status}{f' ({url})' if url else ''}")
        self.report.update(ci_sha=sha, ci_status=status[:64], ci_url=url)
        return status, url

    def _heartbeat(self) -> None:
        """Upsert ``deployment_host_status`` with this tick's view; a failure is only printed."""
        paused = read_paused(self.paths.paused)
        state = {
            key: self.state[key]
            for key in ("last_decision", "last_deploy", "auto_deploys_today", "last_missed_window")
            if key in self.state
        }
        state["deploy_windows"] = [str(window) for window in self.config.deploy_windows]
        if "commits" in self.report:
            state["commits"] = self.report["commits"]
        live = self.report.get("live")
        target = self.report.get("target")
        ci_status = self.report.get("ci_status") if self.report.get("ci_sha") == target else None
        values = ", ".join(
            [
                "1",
                "now()",
                "true" if self.dry_run else "false",
                sql_literal(live if live and _SHA.fullmatch(live) else None),
                sql_literal(target if target and _SHA.fullmatch(target) else None),
                sql_literal(self.report.get("subject")),
                sql_literal(ci_status),
                sql_literal(self.report.get("ci_url") if ci_status else None),
                sql_literal(paused[0] if paused else None),
                f"{sql_literal(json.dumps(state, sort_keys=True))}::json",
            ]
        )
        table = "deployment_host_status"
        # Fixed SQL; every value is a checked UUID or SHA, or comes from sql_literal().
        result = self._psql(
            f"insert into {table} (id, reported_at, dry_run, live_sha, target_sha, "  # noqa: S608
            "target_commit_subject, ci_status, ci_url, paused_reason, state_json) "
            f"values ({values}) on conflict (id) do update set "
            "reported_at = excluded.reported_at, dry_run = excluded.dry_run, "
            f"live_sha = coalesce(excluded.live_sha, {table}.live_sha), "
            f"target_sha = coalesce(excluded.target_sha, {table}.target_sha), "
            "target_commit_subject = coalesce(excluded.target_commit_subject, "
            f"{table}.target_commit_subject), "
            # A CI result belongs to one SHA: keep the last one only while the target is the same.
            "ci_status = case when excluded.ci_status is not null then excluded.ci_status "
            f"when excluded.target_sha is distinct from {table}.target_sha "
            f"and excluded.target_sha is not null then null else {table}.ci_status end, "
            "ci_url = case when excluded.ci_status is not null then excluded.ci_url "
            f"when excluded.target_sha is distinct from {table}.target_sha "
            f"and excluded.target_sha is not null then null else {table}.ci_url end, "
            "paused_reason = excluded.paused_reason, state_json = excluded.state_json"
        )
        if result.code != 0:
            self._say("heartbeat", f"could not write {table}: {one_line(result.output, 200)}")

    # -- admin button requests -----------------------------------------------------

    def _claim_request(self) -> tuple[str, str, bool] | None:
        """The oldest queued admin request, claimed; None when there is none or it went away."""
        # Fixed SQL; every value is a checked UUID or SHA, or comes from sql_literal().
        found = self._psql(
            "select id, coalesce(metadata_json->>'mode', 'latest'), "  # noqa: S608
            "coalesce(metadata_json->>'wait_for_paid_work', 'true') from deployment_runs "
            f"where status = 'queued' and metadata_json->>'executor' = '{HOST_EXECUTOR}' "
            "order by created_at limit 1"
        )
        if found.code != 0 or not found.output.strip():
            return None
        fields = found.output.strip().splitlines()[0].split("|")
        if len(fields) != 3 or not _UUID.fullmatch(fields[0]):
            self._say(
                "request", f"ignoring an unreadable request row: {one_line(found.output, 120)}"
            )
            return None
        run_id, mode, wait = fields
        # Fixed SQL; every value is a checked UUID or SHA, or comes from sql_literal().
        claimed = self._psql(
            "update deployment_runs set status = 'preflight', stage = 'preflight', "  # noqa: S608
            f"started_at = now(), updated_at = now() where id = '{run_id}' and status = 'queued' "
            "returning id"
        )
        if claimed.code != 0 or run_id not in claimed.output:
            return None
        self._say("request", f"claimed admin request {run_id} (mode {mode})")
        return run_id, mode, wait.strip().lower() != "false"

    def _event(self, run_id: str, stage: str, status: str, message: str) -> None:
        # Fixed SQL; every value is a checked UUID or SHA, or comes from sql_literal().
        self._psql(
            "insert into deployment_events (id, run_id, sequence, stage, status, message, "  # noqa: S608
            f"created_at) select gen_random_uuid(), '{run_id}', coalesce(max(sequence), 0) + 1, "
            f"{sql_literal(stage)}, {sql_literal(status)}, {sql_literal(one_line(message, 500))}, "
            f"now() from deployment_events where run_id = '{run_id}'"
        )

    def _update_run(self, run_id: str, *, finished: bool = False, **fields: Any) -> None:
        allowed = {
            "status",
            "stage",
            "previous_sha",
            "target_sha",
            "target_commit_subject",
            "ci_url",
            "rollback_status",
            "failure_code",
            "failure_detail",
        }
        sets = [f"{key} = {sql_literal(value)}" for key, value in fields.items() if key in allowed]
        sets.append("updated_at = now()")
        if finished:
            sets.append("finished_at = now()")
        # Columns come from the fixed set above, values from sql_literal, the id is a checked UUID.
        statement = f"update deployment_runs set {', '.join(sets)} where id = '{run_id}'"  # noqa: S608
        self._psql(statement)

    def _refuse(self, run_id: str, code: str, detail: str) -> Decision:
        detail = one_line(detail, 500)
        self._update_run(
            run_id, status="failed", failure_code=code[:64], failure_detail=detail, finished=True
        )
        self._event(run_id, "preflight", "failed", detail)
        return self._finish(
            Decision("refused", f"admin request {run_id}: {code}: {detail}", {"request": run_id})
        )

    def _serve_request(self, run_id: str, mode: str, wait_for_paid_work: bool) -> Decision:
        """An admin button request: the gates minus the schedule, then the same script.

        A gate that would make an automatic deploy wait refuses the request instead, with a
        fixed failure code the admin page shows; the person presses again later.
        """
        self._event(run_id, "preflight", "running", "主機排程器已接手，開始檢查")
        if mode not in REQUEST_MODES:
            return self._refuse(run_id, "deployment_request_invalid", f"unknown mode {mode!r}")
        paused = read_paused(self.paths.paused)
        if paused is not None:
            return self._refuse(
                run_id,
                "deployment_autodeploy_paused",
                f"上一次自動部署失敗、已暫停，先讀 log 再刪暫停檔：{paused[0]}",
            )
        fetched = self._git("fetch", "--quiet", "origin", BRANCH, timeout=120)
        if fetched.code != 0:
            return self._refuse(
                run_id, "deployment_preflight_failed", f"git fetch failed: {fetched.output}"
            )
        live = self._git("rev-parse", "HEAD").output.strip()
        latest = self._git("rev-parse", f"refs/remotes/origin/{BRANCH}").output.strip()
        if not _SHA.fullmatch(live) or not _SHA.fullmatch(latest):
            return self._refuse(
                run_id, "deployment_preflight_failed", "could not read live or main"
            )
        self._describe(live, latest)
        if mode == "rebuild":
            target = live
            self._update_run(run_id, previous_sha=live, target_sha=live)
        else:
            target = latest
            if live == target:
                return self._refuse(
                    run_id, "deployment_already_current", f"live is already {live[:12]}"
                )
            if self._git("merge-base", "--is-ancestor", live, target).code != 0:
                return self._refuse(
                    run_id,
                    "deployment_not_fast_forward",
                    f"live {live[:12]} is not an ancestor of main {target[:12]}",
                )
            status, url = self._ci(target)
            self._update_run(
                run_id,
                previous_sha=live,
                target_sha=target,
                target_commit_subject=self.report.get("subject"),
                ci_url=url,
            )
            if status != "success":
                return self._refuse(
                    run_id,
                    "deployment_ci_not_green",
                    f"{WORKFLOW_NAME} for {target[:12]} is {status}",
                )
        if self.runner.run(["flock", "-n", str(self.paths.lock), "true"]).code != 0:
            return self._refuse(
                run_id, "deployment_lock_held", "另一個部署正在執行（部署鎖被佔用）"
            )
        probe = self.runner.run([str(self.paths.deploy_script), "--dry-run"], timeout=300)
        if probe.code == REFUSED_EXIT:
            return self._refuse(run_id, "deployment_hold_active", probe.output)
        if probe.code != 0:
            return self._refuse(
                run_id,
                "deployment_preflight_failed",
                f"--dry-run exited {probe.code}: {probe.output}",
            )
        if wait_for_paid_work:
            running_job, error = self._running_paid_work()
            if error is not None:
                return self._refuse(run_id, "deployment_preflight_failed", error)
            if running_job is not None:
                return self._refuse(
                    run_id,
                    "deployment_paid_work_running",
                    f"有付費影片工作正在執行（{running_job}），部署會中斷它",
                )
        if self.dry_run:
            return self._refuse(
                run_id,
                "deployment_dry_run",
                f"排程器在乾跑模式（AUTODEPLOY_ENABLED=false）：would deploy {target[:12]}",
            )

        self._update_run(run_id, status="building", stage="building")
        self._event(run_id, "building", "running", f"開始部署 {target[:12]}（約 1 到 8 分鐘）")
        result, log, started, finished = self._run_script(
            live, target, prefix="button", force=mode == "rebuild"
        )
        record: dict[str, Any] = {
            "sha": target,
            "previous": live,
            "started_at": _iso(started),
            "finished_at": _iso(finished),
            "seconds": int((finished - started).total_seconds()),
            "exit": result.code,
            "log": str(log),
            "request": run_id,
        }
        if result.code != 0:
            # Same rule as an automatic deploy: the script rolled back or stopped midway, and
            # the timer stops until a person has read the log and removed the paused file.
            write_paused(
                self.paths.paused, sha=target, exit_code=result.code, log=log, instant=finished
            )
            self.state["last_deploy"] = record
            detail = f"部署腳本結束碼 {result.code}，已暫停自動部署；log {log}"
            self._update_run(
                run_id,
                status="failed",
                failure_code=f"deploy_script_exit_{result.code}"[:64],
                failure_detail=detail,
                finished=True,
            )
            self._event(run_id, "building", "failed", detail)
            return self._finish(
                Decision(
                    "failed", f"admin request {run_id}: deploy exited {result.code}; paused", record
                )
            )
        self._update_run(run_id, status="verifying", stage="verifying")
        self._event(run_id, "verifying", "running", "部署完成，執行 host-verify.sh")
        record["verify"] = self._verify(target)
        self.state["last_deploy"] = record
        verdict = record["verify"]["result"]
        if verdict == "FAIL":
            verify = record["verify"]
            detail = f"部署完成但驗證失敗：{verify.get('reason') or ''} {verify.get('log') or ''}"
            self._update_run(
                run_id,
                status="manual_intervention_required",
                failure_code="deployment_verify_failed",
                failure_detail=detail,
                finished=True,
            )
            self._event(run_id, "verifying", "failed", detail)
        else:
            self._update_run(run_id, status="succeeded", finished=True)
            self._event(run_id, "verifying", "succeeded", f"已部署 {target[:12]}，驗證 {verdict}")
        return self._finish(
            Decision(
                "deployed",
                f"admin request {run_id}: deployed {target[:12]}, verify {verdict}",
                record,
            )
        )

    # -- the tick -------------------------------------------------------------

    def tick(self) -> Decision:
        request = self._claim_request()
        if request is not None:
            return self._serve_request(*request)
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
        self._describe(live, target)
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

        scheduled = self._schedule(target)
        if scheduled is not None:
            return scheduled

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

        status, url = self._ci(target)
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

    def _running_paid_work(self) -> tuple[str | None, str | None]:
        """(the first running paid stage job, or None; an error reading the table, or None)."""
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
            return None, f"could not read video_stage_jobs: {one_line(stage.output, 200)}"
        running = [line for line in stage.output.splitlines() if line.startswith("running|")]
        return (running[0] if running else None), None

    def _paid_work(self) -> Decision | None:
        running_job, error = self._running_paid_work()
        if error is not None:
            return self._wait("paid_work", error)
        if running_job is None:
            return None
        running = [running_job]
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

    def _run_script(
        self, live: str, target: str, *, prefix: str, force: bool = False
    ) -> tuple[Completed, Path, dt.datetime, dt.datetime]:
        started = self.clock()
        self.paths.log_dir.mkdir(parents=True, exist_ok=True)
        log = self.paths.log_dir / f"{prefix}-{started:%Y%m%d_%H%M%S}.log"
        self._say("deploy", f"{live[:12]} -> {target[:12]}, log {log}")
        argv = [str(self.paths.deploy_script), *(["--force"] if force else [])]
        try:
            result = self.runner.run(argv, timeout=DEPLOY_TIMEOUT, log_path=log)
        except subprocess.TimeoutExpired:
            result = Completed(124, f"deploy script did not finish within {DEPLOY_TIMEOUT} s")
        return result, log, started, self.clock()

    def _deploy(self, live: str, target: str) -> Decision:
        result, log, started, finished = self._run_script(live, target, prefix="auto")
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
                f"deployment and video-ai-worker state require readback; automatic deploys are paused until "
                f"{self.paths.paused} is removed (log {log})"
            )
            return self._finish(
                Decision("failed", f"deploy of {target[:12]} exited {result.code}; paused", record)
            )
        record["verify"] = self._verify(target)
        self.state["last_deploy"] = record
        today = started.astimezone(TAIPEI).date().isoformat()
        self.state["auto_deploys_today"] = {
            "date": today,
            "count": self._deploys_today(started.astimezone(TAIPEI)) + 1,
        }
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


def status_text(paths: Paths, *, now: dt.datetime | None = None) -> str:
    lines = [f"state file: {paths.state}"]
    try:
        config: Config | None = Config.from_mapping(read_env_file(paths.env_file))
    except (ConfigError, OSError):
        config = None
    if config is not None and config.deploy_windows:
        local = (now or now_utc()).astimezone(TAIPEI)
        upcoming = next_window_start(config.deploy_windows, local)
        windows = ", ".join(str(window) for window in config.deploy_windows)
        open_now = any(window.contains(local) for window in config.deploy_windows)
        lines.append(
            f"deploy window: {windows} Asia/Taipei, "
            + ("open now" if open_now else f"next opens {upcoming:%Y-%m-%d %H:%M}")
        )
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
