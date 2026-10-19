#!/usr/bin/env python3
"""One-host cutover for the one pinned legacy media job; dry-run by default.

This is an operator tool, not a deployment hook. Its --apply path must run as a
root-owned transient systemd unit after a named site-owner approval and an
independent review of the plan SHA and this source SHA. It never releases the
durable exact-job Redis nonce. It stops exactly one old API container without a
SIGKILL timeout, then lets the stock one-shot deployment do the replacement.

The plan has no secrets. The nonce stays only in a private container receipt,
the private host receipt and Redis; neither commands nor event logs print it.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import hashlib
import hmac
import json
import os
import re
import stat
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

JOB_ID = "b721a65d-8c8d-4ae8-834c-391cfc267a6f"
JOB_SLUG = "google-project-suncatcher-prototype-what-it-tests"
B25_SLUG = "story-adapt-seiko-quartz-astron"
REQUEST_HASH = "52b39c04a45f39b4101bcd7e401c31cd0e6083f3c8390b729afd2a83569379e6"
MARKER_SHA = "6d6a64a88f066ce62d3ccf2145ab59e052dee0bf76e4da7b68385d93ea6827a5"
KEY = f"video-media:lock:{JOB_ID}"
MEDIA_ROW_QUERY = (
    "select coalesce((select row_to_json(t)::text from "
    "(select id::text,slug,request_hash,kind,provider,model,status,attempts,polls,"
    "vendor_ref,submitted_at from video_media_jobs where "
    "id='b721a65d-8c8d-4ae8-834c-391cfc267a6f') t),'null');"
)
WATCH_UNIT = "a01-media-dispatch-fence-watch.service"
DRIVER_UNIT = "a01-media-cutover-driver.service"
HEARTBEAT = Path("/run/a01-media-dispatch-fence/heartbeat.json")
ROOT = Path("/root/travel_scanner")
COMPOSE = ROOT / "docker-compose.prod.yml"
HOST_DEPLOY = Path("/root/deploy-travel-scanner.sh")
HOLD_PATH = Path("/root/travel-scanner-deploy.hold")
HOLD_OWNER = "a01-media-fence"
HOLD_PHASES = ["api-drain", "nonce", "deploy", "verify"]
TIMER_UNIT = "travel-scanner-autodeploy.timer"
TICK_UNIT = "travel-scanner-autodeploy.service"
DEPLOY_GUARD_MARKER = b"A01_EXACT_MAIN_AND_ENV_GUARD_V1"
PATCHED_DEPLOY_SHA = "836b953610b4ae17eda6d2056efb1f633827db620d0eb43934312cc19d8ac9c6"
LOCKS = (
    Path("/var/lock/travel-scanner-deploy.lock"),
    Path("/root/mokaair-deploy.lock"),
    Path("/run/mokaair-manual-deploy.lock"),
    Path("/run/travel-scanner-deployer/deploy.lock"),
)
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
HEX12 = re.compile(r"[0-9a-f]{12}\Z")


class Stop(RuntimeError):
    """A failed proof. The operator must inspect the site; never retry blindly."""


def require(test: bool, reason: str) -> None:
    if not test:
        raise Stop(reason)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_b25_direct_receipt(proof: dict[str, Any], sources: dict[str, str]) -> None:
    require(
        proof.get("b25_direct_intake")
        == {"slug": B25_SLUG, "compiled_guard": True},
        "new_api_b25_direct_intake_guard_missing",
    )
    code = proof.get("code")
    require(
        isinstance(code, dict)
        and code.get("admin_api_sha256") == sources["admin_api.py"],
        "new_api_b25_direct_source_hash_drift",
    )


def verify_paid_intake_receipt(
    proof: dict[str, Any], sources: dict[str, str], plan_sha: str, target_sha: str
) -> None:
    intake = proof.get("paid_intake")
    require(
        isinstance(intake, dict)
        and intake.get("state") == "PAUSED_ALL"
        and intake.get("plan_sha256") == plan_sha
        and intake.get("target_sha") == target_sha
        and isinstance(intake.get("armed_sha256"), str)
        and bool(HEX64.fullmatch(intake["armed_sha256"]))
        and isinstance(intake.get("marker_sha256"), str)
        and bool(HEX64.fullmatch(intake["marker_sha256"])),
        "new_api_paid_intake_not_paused",
    )
    code = proof.get("code")
    require(
        isinstance(code, dict)
        and code.get("cutover_intake_sha256") == sources["cutover_intake.py"],
        "new_api_paid_intake_source_hash_drift",
    )


def safe_file(path: Path, expected: str | None = None) -> bytes:
    require(path.is_absolute(), "relative_path")
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and not path.is_symlink(), f"not_regular:{path}")
    require(info.st_size <= 2_000_000, f"oversized_file:{path}")
    content = path.read_bytes()
    if expected is not None:
        require(sha_bytes(content) == expected, f"source_hash_drift:{path.name}")
    return content


def write_all(fd: int, data: bytes) -> None:
    view = memoryview(data)
    while view:
        written = os.write(fd, view)
        require(written > 0, "short_write")
        view = view[written:]


def fsync_dir(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def parse_plan(path: Path, expected_sha: str) -> dict[str, Any]:
    require(bool(HEX64.fullmatch(expected_sha)), "invalid_plan_sha")
    plan = json.loads(safe_file(path, expected_sha))
    require(
        isinstance(plan, dict) and plan.get("schema_version") == 1,
        "invalid_plan_schema",
    )
    require(
        set(plan)
        == {
            "schema_version",
            "pr_head",
            "target_sha",
            "old_live_sha",
            "release_dir",
            "pins",
            "source_sha256",
            "require_autodeploy_absent",
        },
        "plan_keys",
    )
    for name in ("pr_head", "target_sha", "old_live_sha"):
        require(
            isinstance(plan[name], str) and bool(HEX40.fullmatch(plan[name])),
            f"invalid_{name}",
        )
    release_dir = Path(plan["release_dir"])
    require(
        release_dir.is_absolute()
        and re.fullmatch(
            r"/root/mokaair-a01-media-fence-[0-9a-f]{12}", str(release_dir)
        )
        is not None,
        "unsafe_release_dir",
    )
    require(plan["require_autodeploy_absent"] is True, "autodeploy_absence_not_pinned")
    pins = plan["pins"]
    require(
        isinstance(pins, dict)
        and set(pins)
        == {
            "old_api_id",
            "old_api_image",
            "redis_id",
            "redis_image",
            "worker_id",
            "worker_image",
            "redis_volume",
            "redis_mount",
            "video_work_mount",
            "api_redis_url_sha256",
            "host_env_sha256",
        },
        "pin_keys",
    )
    for name in (
        "old_api_id",
        "old_api_image",
        "redis_id",
        "redis_image",
        "worker_id",
        "worker_image",
        "api_redis_url_sha256",
        "host_env_sha256",
    ):
        value = pins[name]
        if name.endswith("image"):
            require(
                isinstance(value, str)
                and value.startswith("sha256:")
                and bool(HEX64.fullmatch(value[7:])),
                f"invalid_{name}",
            )
        else:
            require(
                isinstance(value, str) and bool(HEX64.fullmatch(value)),
                f"invalid_{name}",
            )
    require(plan["old_live_sha"] != plan["target_sha"], "target_already_deployed")
    require(pins["redis_volume"] == "travel_scanner_redis_data", "redis_volume_pin")
    for name in ("redis_mount", "video_work_mount"):
        value = pins[name]
        require(
            isinstance(value, str)
            and value.startswith("/var/lib/docker/volumes/")
            and "\n" not in value,
            f"unsafe_{name}",
        )
    sources = plan["source_sha256"]
    require(
        isinstance(sources, dict)
        and set(sources)
        == {
            "host-cutover-driver.py",
            "dispatch_fence_cutover.py",
            "install-marker.sh",
            "monitor-lock.sh",
            "manifest.json",
            "hold.py",
            "host-cutover-driver.deploy-wrapper.sh",
            "incoming-docker-compose.prod.yml",
            "deploy-travel-scanner.sh",
            "jobs.py",
            "admin_api.py",
            "cutover_intake.py",
            "dispatch_fence.py",
            "dispatch_fence_cli.py",
        },
        "source_hash_keys",
    )
    for name, digest in sources.items():
        require(
            isinstance(digest, str) and bool(HEX64.fullmatch(digest)),
            f"invalid_source_hash:{name}",
        )
    require(sources["manifest.json"] == MARKER_SHA, "marker_sha_pin")
    require(
        sources["deploy-travel-scanner.sh"] == PATCHED_DEPLOY_SHA,
        "patched_stock_script_sha_pin",
    )
    return plan


class Command:
    """No shell except fixed, reviewed redis-cli command; stdout is never auto-logged."""

    def run(
        self,
        argv: list[str],
        *,
        input_bytes: bytes | None = None,
        timeout: float | None = 30,
        allowed: tuple[int, ...] = (0,),
    ) -> bytes:
        result = subprocess.run(
            argv,
            input=input_bytes,
            capture_output=True,
            timeout=timeout,
            check=False,
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"} if argv[0] == "git" else None,
        )
        if result.returncode not in allowed:
            # Stderr may include secrets or DB detail; report only command class/exit.
            raise Stop(f"command_failed:{Path(argv[0]).name}:{result.returncode}")
        return result.stdout


class Driver:
    def __init__(
        self,
        plan: dict[str, Any],
        plan_sha: str,
        *,
        command: Command | None = None,
        dry_run: bool = True,
    ) -> None:
        self.plan = plan
        self.plan_sha = plan_sha
        self.command = command or Command()
        self.dry_run = dry_run
        self.release = Path(plan["release_dir"])
        self.pins = plan["pins"]
        self.sources = plan["source_sha256"]
        self.lock_fds: list[int] = []
        self.event_path = self.release / "cutover-events.jsonl"
        self.receipt_path = self.release / "nonce-receipt.json"
        self.hold_module: Any | None = None
        self.nonce_acquired = False
        self.pre_hold_owned = False
        self.hold_sha256 = ""
        self.helper_staged = False

    def cmd(
        self,
        *parts: str,
        input_bytes: bytes | None = None,
        timeout: float | None = 30,
        allowed: tuple[int, ...] = (0,),
    ) -> bytes:
        return self.command.run(
            list(parts), input_bytes=input_bytes, timeout=timeout, allowed=allowed
        )

    def event(self, phase: str, **fields: str | int | bool) -> None:
        if self.dry_run:
            return
        record = {
            "at_utc": dt.datetime.now(dt.UTC).isoformat(),
            "phase": phase,
            **fields,
        }
        data = (json.dumps(record, sort_keys=True) + "\n").encode()
        fd = os.open(
            self.event_path,
            os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_CLOEXEC | os.O_NOFOLLOW,
            0o600,
        )
        try:
            os.fchmod(fd, 0o600)
            write_all(fd, data)
            os.fsync(fd)
        finally:
            os.close(fd)

    def source_path(self, name: str) -> Path:
        if name == "deploy-travel-scanner.sh":
            return HOST_DEPLOY
        if name == "host-cutover-driver.py":
            return Path(__file__).resolve(strict=True)
        return self.release / name

    def check_host_env(self) -> None:
        path = ROOT / ".env"
        require(
            sha_bytes(safe_file(path)) == self.pins["host_env_sha256"], "host_env_drift"
        )

    def check_source_hashes(self) -> None:
        require(
            self.release.is_dir() and not self.release.is_symlink(),
            "release_dir_missing_or_symlink",
        )
        info = self.release.stat()
        require(
            info.st_uid == 0 and stat.S_IMODE(info.st_mode) == 0o700,
            "release_dir_must_be_root_0700",
        )
        for name, digest in self.sources.items():
            if name in (
                "jobs.py", "admin_api.py", "cutover_intake.py", "dispatch_fence.py",
                "dispatch_fence_cli.py",
            ):
                content = self.cmd(
                    "git",
                    "-C",
                    str(ROOT),
                    "show",
                    f"{self.plan['target_sha']}:apps/api/app/video_media/{name}",
                )
                require(
                    sha_bytes(content) == digest, f"target_source_hash_drift:{name}"
                )
            else:
                path = self.source_path(name)
                content = safe_file(path, digest)
                info = path.stat()
                require(
                    info.st_uid == 0 and not info.st_mode & 0o022,
                    f"unsafe_source_mode:{name}",
                )
                if name == "dispatch_fence_cutover.py":
                    require(
                        stat.S_IMODE(info.st_mode) == 0o644,
                        "helper_source_must_be_0644",
                    )
                if name == "deploy-travel-scanner.sh":
                    require(
                        DEPLOY_GUARD_MARKER in content
                        and b"--expected-main-sha=" in content
                        and b"--expected-env-sha256=" in content
                        and b"--expected-redis-url-sha256=" in content
                        and b"--expected-hold-sha256=" in content
                        and b"--no-rollback)" in content,
                        "stock_script_missing_exact_target_env_guard",
                    )
        target_compose = self.cmd(
            "git",
            "-C",
            str(ROOT),
            "show",
            f"{self.plan['target_sha']}:docker-compose.prod.yml",
        )
        require(
            sha_bytes(target_compose)
            == self.sources["incoming-docker-compose.prod.yml"],
            "target_compose_hash_drift",
        )

    def compose(self, *args: str) -> bytes:
        return self.cmd("docker", "compose", "-f", str(COMPOSE), *args)

    def compose_id(self, service: str) -> str:
        output = self.compose("ps", "-q", service).decode().strip()
        require(bool(HEX64.fullmatch(output)), f"compose_id_invalid:{service}")
        return output

    def inspect(self, container: str) -> dict[str, Any]:
        parsed = json.loads(self.cmd("docker", "inspect", container))
        require(isinstance(parsed, list) and len(parsed) == 1, "docker_inspect_shape")
        return parsed[0]

    def pinned_container(
        self, service: str, pin_id: str, pin_image: str, *, running: bool = True
    ) -> dict[str, Any]:
        require(self.compose_id(service) == pin_id, f"{service}_id_drift")
        info = self.inspect(pin_id)
        require(
            info.get("Id") == pin_id and info.get("Image") == pin_image,
            f"{service}_image_drift",
        )
        require(
            info.get("State", {}).get("Running") is running, f"{service}_running_drift"
        )
        labels = info.get("Config", {}).get("Labels", {})
        require(
            labels.get("com.docker.compose.project") == "travel_scanner"
            and labels.get("com.docker.compose.service") == service,
            f"{service}_compose_label_drift",
        )
        return info

    def check_live_redis_url(self, info: dict[str, Any], service: str) -> None:
        variables = info.get("Config", {}).get("Env", [])
        urls = [
            item[10:]
            for item in variables
            if isinstance(item, str) and item.startswith("REDIS_URL=")
        ]
        require(
            len(urls) == 1
            and sha_bytes(urls[0].encode()) == self.pins["api_redis_url_sha256"],
            f"{service}_live_redis_url_drift",
        )
        # A URL hash alone does not establish which Redis server or logical DB
        # the container reaches. Read the server run ID and selected DB through
        # that container's actual REDIS_URL without putting the URL in argv or
        # logs, then compare with DB0 on the pinned Redis container.
        run_ids = [
            line.removeprefix("run_id:")
            for line in self.redis_cli("INFO", "server").decode().splitlines()
            if line.startswith("run_id:")
        ]
        require(
            len(run_ids) == 1 and bool(HEX40.fullmatch(run_ids[0])),
            "pinned_redis_run_id_missing",
        )
        container_id = info.get("Id")
        require(
            isinstance(container_id, str) and bool(HEX64.fullmatch(container_id)),
            f"{service}_container_id_invalid",
        )
        proof = json.loads(
            self.cmd(
                "docker",
                "exec",
                container_id,
                "python",
                "-c",
                "import json,os; from redis import Redis; "
                "r=Redis.from_url(os.environ['REDIS_URL'],socket_timeout=5); "
                "s=r.info('server'); c=r.client_info(); "
                "print(json.dumps({'run_id':s.get('run_id'),'db':c.get('db')})); r.close()",
            )
        )
        require(
            isinstance(proof, dict)
            and proof.get("run_id") == run_ids[0]
            and proof.get("db") in (0, "0"),
            f"{service}_redis_keyspace_drift",
        )

    def redis_cli(self, *args: str) -> bytes:
        # Password is read inside Redis from its existing environment. It is not
        # interpolated into a host command, argv, receipt or event log.
        return self.cmd(
            "docker",
            "exec",
            self.pins["redis_id"],
            "sh",
            "-c",
            'REDISCLI_AUTH="$REDIS_PASSWORD" exec redis-cli --raw "$@"',
            "sh",
            *args,
        ).strip()

    def check_db(self) -> None:
        row_text = (
            self.compose(
                "exec",
                "-T",
                "postgres",
                "psql",
                "-X",
                "-q",
                "-t",
                "-A",
                "-U",
                "travel",
                "-d",
                "travel_scanner",
                "-c",
                MEDIA_ROW_QUERY,
            )
            .decode()
            .strip()
        )
        row = json.loads(row_text)
        require(isinstance(row, dict), "pinned_media_job_missing")
        for key, expected in {
            "id": JOB_ID,
            "slug": JOB_SLUG,
            "request_hash": REQUEST_HASH,
            "kind": "image",
            "provider": "minimax",
            "model": "image-01",
            "status": "queued",
            "attempts": 1,
            "polls": 0,
            "vendor_ref": None,
            "submitted_at": None,
        }.items():
            require(row.get(key) == expected, f"pinned_media_job_drift:{key}")
        count_query = "select count(*) from video_media_jobs where status in ('queued','submitted');"
        count = (
            self.compose(
                "exec",
                "-T",
                "postgres",
                "psql",
                "-X",
                "-q",
                "-t",
                "-A",
                "-U",
                "travel",
                "-d",
                "travel_scanner",
                "-c",
                count_query,
            )
            .decode()
            .strip()
        )
        require(count == "1", "other_active_media_job")
        stage_query = "select count(*) from video_stage_jobs where status in ('queued','running');"
        stage = (
            self.compose(
                "exec",
                "-T",
                "postgres",
                "psql",
                "-X",
                "-q",
                "-t",
                "-A",
                "-U",
                "travel",
                "-d",
                "travel_scanner",
                "-c",
                stage_query,
            )
            .decode()
            .strip()
        )
        require(stage == "0", "active_stage_job")

    def check_redis(self, *, locked: bool) -> None:
        self.pinned_container("redis", self.pins["redis_id"], self.pins["redis_image"])
        info = self.inspect(self.pins["redis_id"])
        mounts = [m for m in info.get("Mounts", []) if m.get("Destination") == "/data"]
        require(
            len(mounts) == 1
            and mounts[0].get("Name") == self.pins["redis_volume"]
            and mounts[0].get("Source") == self.pins["redis_mount"],
            "redis_data_volume_drift",
        )
        config = (
            self.redis_cli(
                "CONFIG", "GET", "appendonly", "appendfsync", "maxmemory-policy"
            )
            .decode()
            .splitlines()
        )
        require(len(config) == 6, "redis_config_shape")
        pairs = dict(zip(config[::2], config[1::2], strict=True))
        require(pairs.get("appendonly") == "yes", "redis_aof_disabled")
        require(
            pairs.get("appendfsync") in ("always", "everysec"), "redis_aof_fsync_weak"
        )
        require(pairs.get("maxmemory-policy") == "noeviction", "redis_eviction_policy")
        if not locked:
            require(self.redis_cli("EXISTS", KEY) == b"0", "exact_media_lock_present")
        else:
            self.check_nonce_owner()

    def check_nonce_owner(self) -> str:
        receipt = json.loads(safe_file(self.receipt_path))
        require(
            receipt.get("job_id") == JOB_ID
            and receipt.get("key") == KEY
            and receipt.get("durable") is True
            and receipt.get("waitaof_local") == 1,
            "nonce_receipt_invalid",
        )
        nonce = receipt.get("nonce")
        require(
            isinstance(nonce, str) and bool(HEX64.fullmatch(nonce)),
            "nonce_receipt_invalid",
        )
        info = self.receipt_path.stat()
        require(
            info.st_uid == 0 and stat.S_IMODE(info.st_mode) == 0o600,
            "nonce_receipt_mode",
        )
        observed = self.redis_cli("GET", KEY)
        ttl = self.redis_cli("TTL", KEY)
        require(
            hmac.compare_digest(observed, nonce.encode()) and ttl == b"-1",
            "nonce_lost_or_expiring",
        )
        return sha_bytes(nonce.encode())

    def check_compose_contract(self) -> None:
        def config(file: Path) -> dict[str, Any]:
            raw = self.cmd(
                "docker",
                "compose",
                "-f",
                str(file),
                "--project-directory",
                str(ROOT),
                "config",
                "--format",
                "json",
            )
            return json.loads(raw)

        current = config(COMPOSE)
        incoming = config(self.release / "incoming-docker-compose.prod.yml")
        # Never print config: it includes interpolated provider/database passwords.
        require(
            current.get("services", {}).get("redis")
            == incoming.get("services", {}).get("redis"),
            "incoming_redis_service_changed",
        )
        require(
            current.get("volumes", {}).get("redis_data")
            == incoming.get("volumes", {}).get("redis_data"),
            "incoming_redis_volume_changed",
        )
        for tree in (current, incoming):
            api = tree.get("services", {}).get("api", {})
            env = api.get("environment", {})
            url = env.get("REDIS_URL")
            require(
                isinstance(url, str)
                and sha_bytes(url.encode()) == self.pins["api_redis_url_sha256"],
                "api_redis_url_changed",
            )
            mounts = api.get("volumes", [])
            require(
                any(
                    m.get("source") == "video_work"
                    and m.get("target") == "/var/lib/mokaair/video-work"
                    and m.get("read_only") is True
                    for m in mounts
                ),
                "api_video_work_mount_not_ro",
            )

    def check_release_state(self) -> None:
        require(
            not HOLD_PATH.exists() and not HOLD_PATH.is_symlink(),
            "existing_deploy_hold",
        )
        require(
            not Path("/root/travel-scanner-autodeploy.paused").exists(),
            "autodeploy_paused",
        )
        self.check_autodeploy_idle()
        now = dt.datetime.now().timestamp()
        for state in Path("/root").glob("mokaair-*/state.json"):
            if now - state.stat().st_mtime > 86400:
                continue
            record = json.loads(safe_file(state))
            require(
                not (
                    "built_at" in record
                    and "activated_at" not in record
                    and "failed_at" not in record
                ),
                "unfinished_staged_release",
            )

    def unit_field(self, unit: str, field: str) -> str:
        return (
            self.cmd("systemctl", "show", unit, f"--property={field}", "--value")
            .decode()
            .strip()
        )

    def check_autodeploy_idle(self) -> None:
        self.check_tick_idle()
        require(
            self.unit_field(TIMER_UNIT, "LoadState") == "not-found",
            "autodeploy_timer_present",
        )
        require(
            self.unit_field(TIMER_UNIT, "ActiveState") == "inactive",
            "autodeploy_timer_active",
        )
        require(
            self.unit_field(TIMER_UNIT, "Job") in ("", "0"),
            "autodeploy_timer_job_pending",
        )

    def check_tick_idle(self) -> None:
        require(
            self.unit_field(TICK_UNIT, "LoadState") == "not-found",
            "autodeploy_tick_present",
        )
        require(
            self.unit_field(TICK_UNIT, "ActiveState") == "inactive",
            "autodeploy_tick_active",
        )
        require(
            self.unit_field(TICK_UNIT, "Job") in ("", "0"),
            "autodeploy_tick_job_pending",
        )

    def check_port_binding(self, info: dict[str, Any], *, stopped: bool) -> None:
        if stopped:
            listeners = self.cmd("ss", "-H", "-ltn", "sport", "=", ":8090").strip()
            require(not listeners, "api_port_still_listening")
            # curl must fail to connect. HTTP 5xx from a replacement is not absence.
            self.cmd(
                "curl",
                "-sS",
                "--connect-timeout",
                "2",
                "--max-time",
                "3",
                "http://127.0.0.1:8090/health",
                allowed=(7,),
            )
        else:
            ports = (
                info.get("NetworkSettings", {}).get("Ports", {}).get("8000/tcp") or []
            )
            require(
                any(
                    p.get("HostIp") == "127.0.0.1" and p.get("HostPort") == "8090"
                    for p in ports
                ),
                "api_port_mapping_drift",
            )

    def check_old_api_gate_bootstrap(self) -> None:
        """Necessary read-only proof that the *running* old API has the gate.

        This is not a live 423 route probe and cannot prove that admitted paid
        requests have settled. Both remain separate, blocking cutover gates.
        """
        container = self.pins["old_api_id"]
        for relative in (
            "app/main.py",
            "app/video_media/admin_api.py",
            "app/video_media/jobs.py",
            "app/video_media/cutover_intake.py",
        ):
            expected = sha_bytes(
                self.cmd(
                    "git",
                    "-C",
                    str(ROOT),
                    "show",
                    f"{self.plan['old_live_sha']}:apps/api/{relative}",
                )
            )
            observed = self.cmd(
                "docker", "exec", container, "sha256sum", f"/app/{relative}"
            ).decode().split()
            require(
                len(observed) == 2 and observed[0] == expected,
                f"old_api_gate_source_drift:{relative}",
            )
        state = json.loads(
            self.cmd(
                "docker",
                "exec",
                container,
                "python",
                "-c",
                "import json; from app.config import get_settings; "
                "from app.video_media.cutover_intake import inspect_intake; "
                "s=inspect_intake(get_settings().video_work_dir); "
                "print(json.dumps({'state':s.state,'bootstrap_id':s.bootstrap_id,"
                "'armed_sha256':s.armed_sha256,'plan_sha256':s.plan_sha256,"
                "'target_sha':s.target_sha,'nonce_sha256':s.nonce_sha256,"
                "'marker_sha256':s.marker_sha256}))",
            )
        )
        require(
            isinstance(state, dict)
            and state.get("state") == "BOOTSTRAP_ALLOW"
            and isinstance(state.get("bootstrap_id"), str)
            and bool(HEX64.fullmatch(state["bootstrap_id"]))
            and isinstance(state.get("marker_sha256"), str)
            and bool(HEX64.fullmatch(state["marker_sha256"]))
            and all(
                state.get(name) is None
                for name in ("armed_sha256", "plan_sha256", "target_sha", "nonce_sha256")
            ),
            "old_api_bootstrap_gate_not_proven",
        )

    def preflight(self, *, after_hold: bool = False) -> None:
        self.check_source_hashes()
        live = self.cmd("git", "-C", str(ROOT), "rev-parse", "HEAD").decode().strip()
        require(live == self.plan["old_live_sha"], "live_sha_drift")
        remote = (
            self.cmd("git", "-C", str(ROOT), "ls-remote", "origin", "refs/heads/main")
            .decode()
            .split()
        )
        require(
            len(remote) == 2 and remote[0] == self.plan["target_sha"], "main_sha_drift"
        )
        self.cmd(
            "git",
            "-C",
            str(ROOT),
            "merge-base",
            "--is-ancestor",
            self.plan["old_live_sha"],
            self.plan["target_sha"],
        )
        ahead = (
            self.cmd(
                "git",
                "-C",
                str(ROOT),
                "rev-list",
                "--count",
                f"{self.plan['old_live_sha']}..{self.plan['target_sha']}",
            )
            .decode()
            .strip()
        )
        require(ahead.isdecimal() and int(ahead) > 0, "target_not_a_new_fast_forward")
        require(
            not self.cmd("git", "-C", str(ROOT), "status", "--porcelain").strip(),
            "host_worktree_dirty",
        )
        if not after_hold:
            self.check_release_state()
        self.check_host_env()
        self.check_compose_contract()
        self.pinned_container("redis", self.pins["redis_id"], self.pins["redis_image"])
        api = self.pinned_container(
            "api", self.pins["old_api_id"], self.pins["old_api_image"]
        )
        worker = self.pinned_container(
            "video-ai-worker", self.pins["worker_id"], self.pins["worker_image"]
        )
        self.check_live_redis_url(api, "api")
        self.check_live_redis_url(worker, "video-ai-worker")
        require(worker.get("State", {}).get("Pid", 0) > 0, "worker_pid_invalid")
        self.check_port_binding(api, stopped=False)
        mounts = [
            m
            for m in api.get("Mounts", [])
            if m.get("Destination") == "/var/lib/mokaair/video-work"
        ]
        require(
            len(mounts) == 1
            and mounts[0].get("RW") is False
            and mounts[0].get("Source") == self.pins["video_work_mount"],
            "api_video_work_mount_drift",
        )
        self.check_old_api_gate_bootstrap()
        self.check_db()
        self.check_redis(locked=False)
        require(
            not (self.release / "nonce-receipt.json").exists(),
            "nonce_receipt_already_exists",
        )
        require(not (self.release / "handoff.json").exists(), "handoff_already_exists")
        require(
            not (self.release / "cutover-events.jsonl").exists() or after_hold,
            "prior_cutover_log_exists",
        )
        mount = Path(self.pins["video_work_mount"])
        require(mount.is_dir() and not mount.is_symlink(), "video_work_mount_missing")
        install = self.cmd(
            "bash",
            str(self.release / "install-marker.sh"),
            "--expected-mountpoint",
            str(mount),
        )
        require(
            b"mode=dry-run" in install and MARKER_SHA.encode() in install,
            "marker_dry_run_failed",
        )

    def acquire_locks(self) -> None:
        require(not self.lock_fds, "locks_already_held")
        try:
            for path in LOCKS:
                require(
                    path.parent.is_dir() and not path.parent.is_symlink(),
                    f"lock_parent_missing:{path}",
                )
                fd = os.open(
                    path, os.O_RDWR | os.O_CREAT | os.O_CLOEXEC | os.O_NOFOLLOW, 0o600
                )
                require(
                    stat.S_ISREG(os.fstat(fd).st_mode), f"lock_path_not_regular:{path}"
                )
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError as exc:
                    os.close(fd)
                    raise Stop(f"deploy_lock_held:{path}") from exc
                self.lock_fds.append(fd)
        except BaseException:
            self.release_locks()
            raise

    def release_locks(self) -> None:
        while self.lock_fds:
            fd = self.lock_fds[-1]
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)
            self.lock_fds.pop()

    def complete_recovery_locks(self) -> None:
        # Release order is reverse LOCKS order. After a partial close, the
        # remaining locked descriptors form a prefix and must stay held.
        require(len(self.lock_fds) <= len(LOCKS), "invalid_recovery_lock_count")
        if not self.lock_fds:
            self.acquire_locks()
            return
        for path in LOCKS[len(self.lock_fds) :]:
            fd = os.open(
                path, os.O_RDWR | os.O_CREAT | os.O_CLOEXEC | os.O_NOFOLLOW, 0o600
            )
            try:
                require(stat.S_ISREG(os.fstat(fd).st_mode), "recovery_lock_not_regular")
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BaseException:
                os.close(fd)
                raise
            self.lock_fds.append(fd)

    def hold(self, action: str) -> str:
        import importlib.util

        safe_file(self.release / "hold.py", self.sources["hold.py"])
        spec = importlib.util.spec_from_file_location(
            "a01_pinned_hold", self.release / "hold.py"
        )
        require(spec is not None and spec.loader is not None, "hold_import_failed")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        path = str(self.release)
        if action == "acquire":
            result = module.acquire(
                path,
                self.plan["target_sha"],
                HOLD_OWNER,
                HOLD_PHASES,
                hold_path=HOLD_PATH,
            )
            require(result == "created", "hold_not_new")
            module.verify(path, self.plan["target_sha"], hold_path=HOLD_PATH)
            descriptor = os.open(HOLD_PATH, os.O_RDONLY | os.O_NOFOLLOW)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
            fsync_dir(HOLD_PATH.parent)
            module.verify(path, self.plan["target_sha"], hold_path=HOLD_PATH)
            self.hold_sha256 = sha_bytes(safe_file(HOLD_PATH))
            self.hold_record()
            return result
        if action == "verify":
            module.verify(path, self.plan["target_sha"], hold_path=HOLD_PATH)
            require(
                self.hold_sha256
                and sha_bytes(safe_file(HOLD_PATH)) == self.hold_sha256,
                "hold_bytes_changed",
            )
            self.hold_record()
            return "verified"
        raise Stop("hold_clear_forbidden_during_a01")

    def hold_record(self) -> dict[str, Any]:
        info = HOLD_PATH.lstat()
        require(
            stat.S_ISREG(info.st_mode)
            and info.st_uid == os.geteuid()
            and stat.S_IMODE(info.st_mode) == 0o644,
            "hold_owner_or_mode_drift",
        )
        raw = safe_file(HOLD_PATH)
        require(
            self.hold_sha256 and sha_bytes(raw) == self.hold_sha256,
            "hold_bytes_changed",
        )
        lines = raw.decode("utf-8").splitlines()
        require(len(lines) == 2, "hold_record_shape_changed")
        record = json.loads(lines[1])
        require(
            isinstance(record, dict)
            and set(record)
            == {"target", "release_dir", "owner", "phases", "created_at"}
            and record["target"] == self.plan["target_sha"]
            and record["release_dir"] == str(self.release)
            and record["owner"] == HOLD_OWNER
            and record["phases"] == HOLD_PHASES
            and isinstance(record["created_at"], str)
            and dt.datetime.fromisoformat(record["created_at"]).tzinfo is not None,
            "hold_record_identity_drift",
        )
        return record

    def stop_old_api(self) -> None:
        self.event("old_api_stop_waiting", api_id=self.pins["old_api_id"])
        finished = threading.Event()

        def observer() -> None:
            while not finished.wait(30):
                self.event("old_api_stop_still_waiting", api_id=self.pins["old_api_id"])

        thread = threading.Thread(target=observer, daemon=True)
        thread.start()
        try:
            # No Python timeout and no finite Docker stop timeout: neither path
            # may escalate an in-flight vendor call to SIGKILL.
            self.cmd(
                "docker",
                "container",
                "stop",
                "--signal=SIGTERM",
                "--timeout=-1",
                self.pins["old_api_id"],
                timeout=None,
            )
        finally:
            finished.set()
            thread.join(timeout=2)
        info = self.inspect(self.pins["old_api_id"])
        state = info.get("State", {})
        require(
            state.get("Running") is False
            and state.get("Pid") == 0
            and state.get("ExitCode") == 0
            and state.get("OOMKilled") is False
            and state.get("Error") == "",
            "old_api_normal_exit_unproven",
        )
        require(
            not self.compose("ps", "-q", "api").strip(), "another_api_container_present"
        )
        self.check_port_binding(info, stopped=True)
        self.check_db()
        self.check_redis(locked=False)
        # Exit status alone cannot prove that every request which passed the
        # bootstrap gate settled its vendor result and database ledger.
        self.event("old_api_normal_exit_observed", api_id=self.pins["old_api_id"])

    def helper_paths(self) -> tuple[str, str]:
        name = self.release.name.rsplit("-", 1)[-1]
        return (
            f"/tmp/a01-media-cutover-{name}.py",
            f"/tmp/a01-media-cutover-{name}.json",
        )

    def stage_helper(self) -> None:
        # Stage and read as the worker's default UID before taking the old API
        # offline. Docker cp may otherwise leave a root-owned 0600 helper that
        # the worker cannot execute after the API has stopped.
        helper = self.release / "dispatch_fence_cutover.py"
        safe_file(helper, self.sources["dispatch_fence_cutover.py"])
        require(
            stat.S_IMODE(helper.stat().st_mode) == 0o644,
            "helper_source_must_be_0644",
        )
        container = self.pins["worker_id"]
        container_helper, container_receipt = self.helper_paths()
        self.cmd("docker", "exec", container, "test", "!", "-e", container_helper)
        self.cmd("docker", "exec", container, "test", "!", "-e", container_receipt)
        self.cmd("docker", "cp", str(helper), f"{container}:{container_helper}")
        digest = (
            self.cmd("docker", "exec", container, "sha256sum", container_helper)
            .decode()
            .split()[0]
        )
        require(
            digest == self.sources["dispatch_fence_cutover.py"],
            "container_helper_hash_drift",
        )
        self.helper_staged = True
        self.event("helper_staged_and_worker_readable", worker_id=container)

    def acquire_nonce(self) -> str:
        require(self.helper_staged, "helper_not_staged_before_api_stop")
        container = self.pins["worker_id"]
        container_helper, container_receipt = self.helper_paths()
        self.cmd("docker", "exec", container, "test", "!", "-e", container_receipt)
        digest = (
            self.cmd("docker", "exec", container, "sha256sum", container_helper)
            .decode()
            .split()[0]
        )
        require(
            digest == self.sources["dispatch_fence_cutover.py"],
            "container_helper_hash_drift_before_acquire",
        )
        # A non-zero result may still have created the key. Always recover the
        # private receipt if it exists, then stop; never acquire again blindly.
        self.event("nonce_acquire_waiting", worker_id=container)
        result = subprocess.run(
            [
                "docker",
                "exec",
                container,
                "python",
                container_helper,
                "acquire",
                "--receipt-file",
                container_receipt,
            ],
            capture_output=True,
            timeout=None,
            check=False,
        )
        receipt_exists = (
            subprocess.run(
                ["docker", "exec", container, "test", "-f", container_receipt],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10,
                check=False,
            ).returncode
            == 0
        )
        if receipt_exists:
            temporary = self.release / ".nonce-receipt.pending"
            require(
                not temporary.exists() and not self.receipt_path.exists(),
                "receipt_target_exists",
            )
            self.cmd("docker", "cp", f"{container}:{container_receipt}", str(temporary))
            content = safe_file(temporary)
            info = temporary.stat()
            require(
                info.st_uid == 0 and stat.S_IMODE(info.st_mode) == 0o600,
                "copied_receipt_not_root_0600",
            )
            fd = os.open(temporary, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
            os.replace(temporary, self.receipt_path)
            fsync_dir(self.release)
            require(content, "empty_receipt")
        require(
            result.returncode == 0 and receipt_exists, "nonce_acquire_failed_or_unknown"
        )
        proof = json.loads(result.stdout)
        require(
            proof.get("durable") is True
            and proof.get("waitaof_local") == 1
            and proof.get("job_id") == JOB_ID,
            "nonce_acquire_not_durable",
        )
        digest = self.check_nonce_owner()
        require(proof.get("nonce_sha256") == digest, "nonce_digest_drift")
        self.nonce_acquired = True
        self.event(
            "nonce_durably_acquired",
            nonce_sha256=digest,
            redis_id=self.pins["redis_id"],
        )
        return digest

    def check_watcher(self, nonce_sha: str, *, first: bool = False) -> int:
        script = self.release / "monitor-lock.sh"
        safe_file(script, self.sources["monitor-lock.sh"])
        for _ in range(16 if first else 1):
            active = (
                self.cmd("systemctl", "is-active", WATCH_UNIT, allowed=(0, 3))
                .decode()
                .strip()
            )
            try:
                heartbeat = json.loads(safe_file(HEARTBEAT))
            except (FileNotFoundError, ValueError):
                heartbeat = {}
            if active == "active" and heartbeat.get("nonce_sha256") == nonce_sha:
                break
            if not first:
                raise Stop("watcher_not_active_or_no_fresh_heartbeat")
            threading.Event().wait(1)
        require(active == "active", "watcher_not_active")
        info = HEARTBEAT.stat()
        parent = HEARTBEAT.parent.stat()
        require(
            info.st_uid == parent.st_uid == 0
            and stat.S_IMODE(info.st_mode) == 0o600
            and stat.S_IMODE(parent.st_mode) == 0o700,
            "watcher_heartbeat_permissions",
        )
        require(
            heartbeat.get("schema_version") == 1
            and heartbeat.get("job_id") == JOB_ID
            and heartbeat.get("redis_container_id") == self.pins["redis_id"]
            and heartbeat.get("nonce_sha256") == nonce_sha
            and heartbeat.get("checks", 0) > 0
            and heartbeat.get("owned") is True
            and heartbeat.get("no_expiry") is True,
            "watcher_heartbeat_mismatch",
        )
        timestamp = dt.datetime.fromisoformat(heartbeat["checked_at_utc"])
        age = (dt.datetime.now(dt.UTC) - timestamp).total_seconds()
        require(0 <= age <= 15, "watcher_heartbeat_stale")
        details = (
            self.cmd("systemctl", "show", WATCH_UNIT, "--property=MainPID", "--value")
            .decode()
            .strip()
        )
        require(details.isdecimal() and int(details) > 0, "watcher_main_pid_missing")
        self.watcher_execstart()
        return int(details)

    def watcher_execstart(self) -> str:
        value = (
            self.cmd("systemctl", "show", WATCH_UNIT, "--property=ExecStart", "--value")
            .decode()
            .strip()
        )
        expected = (
            f"argv[]=/bin/bash {self.release / 'monitor-lock.sh'} "
            f"--receipt {self.receipt_path} --redis-container-id {self.pins['redis_id']} ;"
        )
        require(
            value and expected in value and value.count("argv[]=") == 1,
            "watcher_execstart_drift",
        )
        return value

    def start_watcher(self, nonce_sha: str) -> int:
        state = (
            self.cmd("systemctl", "show", WATCH_UNIT, "--property=LoadState", "--value")
            .decode()
            .strip()
        )
        require(state == "not-found", "watcher_unit_already_exists")
        require(
            not HEARTBEAT.exists() and not HEARTBEAT.is_symlink(),
            "watcher_heartbeat_already_exists",
        )
        self.cmd(
            "systemd-run",
            f"--unit={WATCH_UNIT.removesuffix('.service')}",
            "--property=Type=exec",
            "--property=Restart=no",
            "--property=KillMode=process",
            "/bin/bash",
            str(self.release / "monitor-lock.sh"),
            "--receipt",
            str(self.receipt_path),
            "--redis-container-id",
            self.pins["redis_id"],
        )
        pid = self.check_watcher(nonce_sha, first=True)
        self.event("watcher_supervised", watcher_pid=pid, nonce_sha256=nonce_sha)
        return pid

    def install_marker(self, nonce_sha: str) -> None:
        safe_file(self.release / "install-marker.sh", self.sources["install-marker.sh"])
        self.check_nonce_owner()
        self.check_watcher(nonce_sha)
        output = self.cmd(
            "bash",
            str(self.release / "install-marker.sh"),
            "--expected-mountpoint",
            self.pins["video_work_mount"],
            "--apply",
        )
        require(
            b"installed marker O_NOFOLLOW/regular-file/SHA-256 readback PASS" in output,
            "marker_install_readback_failed",
        )
        self.check_db()
        self.check_nonce_owner()
        self.check_watcher(nonce_sha)
        self.event("marker_installed", manifest_sha256=MARKER_SHA)

    def timer_pause(self) -> None:
        # This exact-host release rejects loaded autodeploy units. Stopping a
        # timer only here would leave a merge-to-cutover firing window.
        self.check_autodeploy_idle()

    def timer_restore(self) -> None:
        self.check_autodeploy_idle()

    def stock_deploy(self) -> None:
        safe_file(
            self.release / "host-cutover-driver.deploy-wrapper.sh",
            self.sources["host-cutover-driver.deploy-wrapper.sh"],
        )
        safe_file(HOST_DEPLOY, self.sources["deploy-travel-scanner.sh"])
        self.check_host_env()
        self.check_autodeploy_idle()
        self.hold("verify")
        self.event(
            "cutover_hold_retained_for_stock_deploy", hold_sha256=self.hold_sha256
        )
        self.release_locks()
        self.event("stock_deploy_started", target_sha=self.plan["target_sha"])
        # Wrapper itself starts the stock script with nohup and waits for its
        # terminal result. The driver remains in its own systemd service.
        result = subprocess.run(
            [
                "/bin/bash",
                str(self.release / "host-cutover-driver.deploy-wrapper.sh"),
                "--ignore-hold",
                "--no-rollback",
                f"--expected-main-sha={self.plan['target_sha']}",
                f"--expected-env-sha256={self.pins['host_env_sha256']}",
                f"--expected-redis-url-sha256={self.pins['api_redis_url_sha256']}",
                f"--expected-hold-sha256={self.hold_sha256}",
            ],
            capture_output=True,
            timeout=None,
            check=False,
        )
        self.event("stock_deploy_terminal", exit_code=result.returncode)
        require(
            result.returncode == 0 and b"DEPLOY_EXIT=0" in result.stdout,
            "stock_deploy_failed_or_rolled_back",
        )

    def post_hold(self) -> None:
        self.complete_recovery_locks()
        self.hold("verify")
        self.event("post_deploy_hold_verified")

    def verify_new_api(self, nonce_sha: str, watcher_pid: int) -> dict[str, Any]:
        self.hold("verify")
        require(
            self.cmd("git", "-C", str(ROOT), "rev-parse", "HEAD").decode().strip()
            == self.plan["target_sha"],
            "deployed_sha_drift",
        )
        remote = (
            self.cmd("git", "-C", str(ROOT), "ls-remote", "origin", "refs/heads/main")
            .decode()
            .split()
        )
        require(
            len(remote) == 2 and remote[0] == self.plan["target_sha"],
            "main_moved_during_cutover",
        )
        self.check_db()
        self.check_redis(locked=True)
        require(self.check_nonce_owner() == nonce_sha, "nonce_digest_changed")
        require(self.check_watcher(nonce_sha) == watcher_pid, "watcher_pid_changed")
        api_id = self.compose_id("api")
        api = self.inspect(api_id)
        require(
            api.get("State", {}).get("Running") is True
            and api.get("Config", {})
            .get("Labels", {})
            .get("com.docker.compose.service")
            == "api",
            "new_api_not_running",
        )
        api_image = api.get("Image")
        require(
            isinstance(api_image, str) and api_image.startswith("sha256:"),
            "new_api_image_invalid",
        )
        self.check_port_binding(api, stopped=False)
        self.check_live_redis_url(api, "new_api")
        mounts = [
            mount
            for mount in api.get("Mounts", [])
            if mount.get("Destination") == "/var/lib/mokaair/video-work"
        ]
        require(
            len(mounts) == 1
            and mounts[0].get("RW") is False
            and mounts[0].get("Source") == self.pins["video_work_mount"],
            "new_api_video_work_mount_drift",
        )
        self.check_host_env()
        self.check_autodeploy_idle()
        # API health is a separate proof from the CLI's fence behavior.
        health = self.cmd(
            "curl",
            "-fsS",
            "--connect-timeout",
            "3",
            "--max-time",
            "10",
            "http://127.0.0.1:8090/health",
        )
        require(health, "new_api_health_empty")
        output = self.cmd(
            "docker",
            "exec",
            api_id,
            "python",
            "-m",
            "app.video_media.dispatch_fence_cli",
            "check",
            "--job-id",
            JOB_ID,
            "--expect-operator-lock",
        )
        proof = json.loads(output)
        require(
            proof.get("schema_version") == 1
            and proof.get("enforced") is True
            and proof.get("fence_sha256") == MARKER_SHA
            and proof.get("media_lock_absent") is False
            and proof.get("operator_lock_expected") is True
            and proof.get("active_media_count") == 1,
            "new_api_held_mode_fence_failed",
        )
        verify_b25_direct_receipt(proof, self.sources)
        verify_paid_intake_receipt(
            proof, self.sources, self.plan_sha, self.plan["target_sha"]
        )
        job = proof.get("job", {})
        for key, expected in {
            "id": JOB_ID,
            "slug": JOB_SLUG,
            "request_hash": REQUEST_HASH,
            "kind": "image",
            "provider": "minimax",
            "model": "image-01",
            "status": "queued",
            "vendor_ref": None,
            "submitted_at": None,
        }.items():
            require(job.get(key) == expected, f"new_api_job_drift:{key}")
        code = proof.get("code", {})
        require(
            code.get("jobs_sha256") == self.sources["jobs.py"]
            and code.get("dispatch_fence_sha256") == self.sources["dispatch_fence.py"],
            "new_api_source_hash_drift",
        )
        cli_sha = (
            self.cmd(
                "docker",
                "exec",
                api_id,
                "sha256sum",
                "/app/app/video_media/dispatch_fence_cli.py",
            )
            .decode()
            .split()[0]
        )
        require(
            cli_sha == self.sources["dispatch_fence_cli.py"],
            "new_api_cli_source_hash_drift",
        )
        require(
            self.compose_id("api") == api_id
            and self.check_watcher(nonce_sha) == watcher_pid,
            "api_or_watcher_changed_during_proof",
        )
        return {"api_id": api_id, "api_image": api_image, "proof": proof}

    def write_handoff(
        self, nonce_sha: str, watcher_pid: int, new_api: dict[str, Any]
    ) -> None:
        hold_record = self.hold_record()
        payload = {
            "schema_version": 1,
            "target_sha": self.plan["target_sha"],
            "plan_sha256": self.plan_sha,
            "job_id": JOB_ID,
            "redis_id": self.pins["redis_id"],
            "redis_image": self.pins["redis_image"],
            "api_id": new_api["api_id"],
            "api_image": new_api["api_image"],
            "watcher_unit": WATCH_UNIT,
            "watcher_main_pid": watcher_pid,
            "nonce_watcher_script_path": str(self.release / "monitor-lock.sh"),
            "nonce_watcher_script_sha256": self.sources["monitor-lock.sh"],
            "nonce_watcher_execstart_sha256": sha_bytes(
                self.watcher_execstart().encode("utf-8")
            ),
            "nonce_sha256": nonce_sha,
            "nonce_receipt_sha256": sha_bytes(safe_file(self.receipt_path)),
            "nonce_receipt_path": str(self.receipt_path),
            "nonce_heartbeat_path": str(HEARTBEAT),
            "nonce_retained": True,
            "hold_path": str(HOLD_PATH),
            "hold_release_dir": str(self.release),
            "hold_sha256": self.hold_sha256,
            "hold_owner": hold_record["owner"],
            "hold_phases": hold_record["phases"],
            "hold_created_at": hold_record["created_at"],
            "marker_sha256": MARKER_SHA,
            "api_held_mode_receipt": new_api["proof"],
            "dispatch_fence_cli_sha256": self.sources["dispatch_fence_cli.py"],
            "checked_at_utc": dt.datetime.now(dt.UTC).isoformat(),
        }
        target = self.release / "handoff.json"
        require(not target.exists(), "handoff_already_exists")
        data = (json.dumps(payload, sort_keys=True) + "\n").encode()
        fd = os.open(
            target,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | os.O_NOFOLLOW,
            0o600,
        )
        try:
            os.fchmod(fd, 0o600)
            write_all(fd, data)
            os.fsync(fd)
        finally:
            os.close(fd)
        fsync_dir(self.release)
        require(safe_file(target) == data, "handoff_readback_failed")

    def run(self) -> None:
        self.preflight()
        if self.dry_run:
            print(
                json.dumps(
                    {
                        "dry_run": True,
                        "preflight_passed": True,
                        "production_ready": False,
                        "blocking_reason": "b25_producer_proof_missing",
                        "additional_blocking_reason": "global_paid_intake_cutover_proof_missing",
                        "plan_sha256": self.plan_sha,
                        "target_sha": self.plan["target_sha"],
                        "job_id": JOB_ID,
                    },
                    sort_keys=True,
                )
            )
            return
        self.verify_b25_producer_quiescence()
        self.verify_global_pause_cutover_ready()
        require(os.geteuid() == 0, "apply_requires_root")
        # A transient systemd service survives SSH loss. A shell invocation is
        # refused, because SIGINT/HUP could orphan the stop/cutover midway.
        cgroup = Path("/proc/self/cgroup").read_text()
        require(DRIVER_UNIT in cgroup, "apply_requires_named_systemd_unit")
        nonce_sha = ""
        watcher_pid = 0
        try:
            self.acquire_locks()
            # The first read-only survey occurred without locks. Repeat its
            # full release-state checks while all four flocks are held and
            # before this driver creates its own hold.
            self.preflight()
            self.hold("acquire")
            self.pre_hold_owned = True
            self.event("cutover_hold_acquired", plan_sha256=self.plan_sha)
            self.timer_pause()
            self.stage_helper()
            self.stop_old_api()
            nonce_sha = self.acquire_nonce()
            watcher_pid = self.start_watcher(nonce_sha)
            self.install_marker(nonce_sha)
            self.check_nonce_owner()
            self.check_watcher(nonce_sha)
            self.stock_deploy()
        except BaseException:
            # The exact hold stays intact across the stock deploy and all
            # failure paths. Redis nonce, if acquired, also stays intact.
            if self.pre_hold_owned:
                try:
                    self.post_hold()
                    self.event("recovery_hold_verified_after_failure")
                except BaseException:  # noqa: BLE001 - retain nonce on any interrupted recovery
                    self.event("recovery_hold_unverified_nonce_retained")
            if self.nonce_acquired:
                self.event("cutover_stopped_nonce_retained")
            self.release_locks()
            raise
        # The stock script has exited. Reacquire four locks and verify the same
        # original hold before trusting any post-deploy receipts.
        try:
            self.post_hold()
            new_api = self.verify_new_api(nonce_sha, watcher_pid)
            self.write_handoff(nonce_sha, watcher_pid, new_api)
            self.timer_restore()
            self.check_autodeploy_idle()
            require(
                safe_file(self.release / "handoff.json"), "handoff_missing_before_clear"
            )
            self.hold("verify")
            self.event(
                "handoff_complete_hold_and_nonce_retained", api_id=new_api["api_id"]
            )
        finally:
            self.release_locks()

    def verify_b25_producer_quiescence(self) -> None:
        # The B25 producer can queue another paid image job after a brief empty
        # interval. A single DB count is not a durable proof. Keep apply closed
        # until an authoritative producer completion/pause receipt is designed,
        # implemented and independently reviewed.
        raise Stop("b25_producer_proof_missing")

    def verify_global_pause_cutover_ready(self) -> None:
        # A bootstrap-state source check is necessary but not sufficient. There
        # is no reviewed root-owned armed/PAUSED_ALL transition, authenticated
        # live 423 probe, settled-in-flight proof, or new-image pre-exposure
        # barrier. The API's out-of-band second paid-intake check is not an
        # atomic barrier for a request already past that check. Do not enter
        # the host-writing path until all are integrated and proven live.
        raise Stop("global_paid_intake_cutover_proof_missing")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--expected-plan-sha256", required=True)
    parser.add_argument(
        "--apply", action="store_true", help="owner-approved production write"
    )
    args = parser.parse_args(argv)
    try:
        plan = parse_plan(args.plan, args.expected_plan_sha256)
        Driver(plan, args.expected_plan_sha256, dry_run=not args.apply).run()
    except (
        Stop,
        FileNotFoundError,
        PermissionError,
        json.JSONDecodeError,
        subprocess.TimeoutExpired,
        OSError,
        ValueError,
        KeyError,
    ) as error:
        # Avoid printing subprocess stderr, interpolated Compose config or nonce.
        print(
            json.dumps(
                {
                    "status": "STOP",
                    "production_ready": False,
                    "reason": type(error).__name__
                    if not isinstance(error, Stop)
                    else str(error),
                }
            ),
            file=sys.stderr,
        )
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
