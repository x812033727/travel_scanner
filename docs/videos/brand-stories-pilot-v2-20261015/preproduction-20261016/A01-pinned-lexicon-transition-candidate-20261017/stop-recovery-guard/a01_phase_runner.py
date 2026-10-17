#!/usr/bin/env python3
"""Candidate systemd ExecStart for one A01 round-12 phase in an isolated container.

No phase can run with the deliberately incomplete manifest distributed here.
The installed service, source hashes, host, jobs and budget must all be pinned
and read back at action time. Do not run until independently reviewed.
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tarfile
import time
from contextlib import ExitStack
from decimal import Decimal
from pathlib import Path, PurePosixPath

sys.path.insert(0, "/root/travel_scanner/ops/release")
sys.path.insert(0, "/usr/local/sbin")
import hold  # noqa: E402
import a01_stop_guard  # noqa: E402
import a01_phase_recover  # noqa: E402


ROOT = Path("/root/travel_scanner")
RELEASE = Path("/root/mokaair-a01-round12-20261017-fe35369c")
MANIFEST = RELEASE / "a01-phase-manifest.json"
WORK = a01_stop_guard.Paths().workdir
PENDING = WORK / "round12-restore-stop.pending.json"
ONEOFF = WORK / "a01-round12-oneoff.json"
GLOBAL_STOP = WORK.parent / "STOP"
GLOBAL_STOP_BYTES = b"A01 round12 isolated manual review: drain original video worker.\n"
HOST_PAYLOAD = RELEASE / "payload"
CONTAINER_PAYLOAD = Path("/tmp/a01-round12-20261017-fe35369c/payload")
PHASES = {"listener": (104, "--listener"), "manual": (105, "--manual"),
          "facts": (106, "--facts"), "panel": (107, "--panel")}
LOCKS = [Path("/var/lock/travel-scanner-deploy.lock"), Path("/root/mokaair-deploy.lock"),
         Path("/run/mokaair-manual-deploy.lock"), Path("/run/travel-scanner-deployer/deploy.lock")]
SHA = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA = re.compile(r"^[0-9a-f]{40}$")
EXPECTED_PAYLOAD_MEMBERS = 1351
EXPECTED_PAYLOAD_FILES = 979
EXPECTED_PAYLOAD_SUBDIRS = 371


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def command(*args: str, input_bytes: bytes | None = None,
            timeout_seconds: int = 120) -> str:
    try:
        result = subprocess.run(args, input=input_bytes, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=timeout_seconds,
                                check=False)
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f"{args[0]} {args[1] if len(args)>1 else ''} timed out after "
                           f"{timeout_seconds}s; result is uncertain") from error
    if result.returncode:
        raise RuntimeError(f"{args[0]} {args[1] if len(args)>1 else ''} exited "
                           f"{result.returncode}: {result.stderr.decode(errors='replace')[:400]}")
    return result.stdout.decode(errors="replace").strip()


def compose(service: str, *argv: str, input_bytes: bytes | None = None) -> str:
    return command("docker", "compose", "-f", str(ROOT / "docker-compose.prod.yml"),
                   "exec", "-T", service, *argv, input_bytes=input_bytes)


def digest(path: Path) -> str:
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), f"expected regular file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pinned(value: object, label: str) -> str:
    need(isinstance(value, str) and bool(SHA.fullmatch(value)), f"unfilled SHA pin: {label}")
    return value


def reviewed_payload_tree(archive_path: Path) -> dict:
    """Derive every expected byte from the pinned archive, then inspect host extraction."""
    files: dict[str, str] = {}
    dirs: set[str] = set()
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        need(len(members) == EXPECTED_PAYLOAD_MEMBERS, "reviewed archive member count drift")
        for member in members:
            path = PurePosixPath(member.name)
            need(not path.is_absolute() and ".." not in path.parts and path.parts[0] == "payload",
                 "reviewed archive contains unsafe path")
            relative = path.relative_to("payload").as_posix()
            if member.isdir():
                if relative != ".":
                    need(relative not in dirs and relative not in files, "duplicate archive directory")
                    dirs.add(relative)
            elif member.isfile():
                need(relative != "." and relative not in files and relative not in dirs,
                     "duplicate archive file")
                source = archive.extractfile(member)
                need(source is not None, "archive file unreadable")
                files[relative] = hashlib.sha256(source.read()).hexdigest()
            else:
                raise RuntimeError("reviewed archive contains link or special entry")
    need(len(files) == EXPECTED_PAYLOAD_FILES and len(dirs) == EXPECTED_PAYLOAD_SUBDIRS,
         "reviewed archive file/directory count drift")
    need(HOST_PAYLOAD.is_dir() and not HOST_PAYLOAD.is_symlink(), "host payload missing or linked")
    host_files: set[str] = set()
    host_dirs: set[str] = set()
    for path in HOST_PAYLOAD.rglob("*"):
        relative = path.relative_to(HOST_PAYLOAD).as_posix()
        info = path.lstat()
        if stat.S_ISREG(info.st_mode):
            host_files.add(relative)
        elif stat.S_ISDIR(info.st_mode):
            host_dirs.add(relative)
        else:
            raise RuntimeError(f"host payload contains link or special entry: {relative}")
    need(host_files == set(files) and host_dirs == dirs, "host payload tree differs from archive")
    for relative, expected in files.items():
        need(digest(HOST_PAYLOAD / relative) == expected,
             f"host payload byte drift: {relative}")
    return {"files": files, "dirs": sorted(dirs)}


def config() -> dict:
    need(digest(MANIFEST), "manifest is required")
    m = json.loads(MANIFEST.read_text())
    need(m.get("schema_version") == 1 and m.get("slug") == "story-rolling-suitcase-v2",
         "invalid A01 manifest identity")
    need(isinstance(m.get("expected_head"), str) and bool(GIT_SHA.fullmatch(m["expected_head"])),
         "unfilled target git SHA")
    image_ref = m.get("video_worker_image_ref")
    need(isinstance(image_ref, str) and image_ref.startswith("travel-scanner-video-worker:"),
         "pinned video worker image reference missing")
    image_tag = image_ref.split(":", 1)[1]
    need(image_tag == "local", "production Compose image tag drift")
    image_id = m.get("video_worker_image_id")
    need(isinstance(image_id, str) and image_id.startswith("sha256:")
         and bool(SHA.fullmatch(image_id[7:])), "pinned video worker image ID missing")
    for key in ("expected_stop_sha256", "video_worker_id", "video_ai_worker_id"):
        pinned(m.get(key), key)
    need(m.get("next_phase") in PHASES, "next_phase is not pinned")
    need(isinstance(m.get("owner_approval_ref"), str) and len(m["owner_approval_ref"]) >= 16,
         "owner approval reference is missing")
    need(isinstance(m.get("driver_container_path"), str)
         and m["driver_container_path"].startswith("/tmp/a01-round12-20261017-fe35369c/payload/"),
         "driver path is not the isolated payload")
    archive = m.get("host_payload_archive_path")
    need(isinstance(archive, str) and archive.startswith(str(RELEASE) + "/")
         and archive.endswith(".tar.gz") and ".." not in Path(archive).parts,
         "host archive path is not pinned inside release")
    need(digest(Path(archive)) == pinned(m.get("host_payload_archive_sha256"), "host archive"),
         "reviewed host archive SHA drift")
    m["_payload_tree"] = reviewed_payload_tree(Path(archive))
    files = m.get("container_files")
    need(isinstance(files, dict) and len(files) >= 5, "container file pins are incomplete")
    need(m["driver_container_path"] in files, "driver SHA is not pinned")
    for path, value in files.items():
        need(path.startswith("/tmp/a01-round12-20261017-fe35369c/payload/") and ".." not in Path(path).parts,
             "container file path outside isolated payload")
        pinned(value, path)
        relative = Path(path).relative_to(CONTAINER_PAYLOAD)
        need(digest(HOST_PAYLOAD / relative) == value,
             f"host extracted payload hash drift: {relative}")
    pinned(m.get("phase_sources", {}).get(m["next_phase"]), "next phase source")
    for filename in ("a01_stop_guard.py", "a01_phase_runner.py",
                     "a01_phase_recover.py", "mokaair-a01-review@.service"):
        expected = pinned(m.get("installed_files", {}).get(filename), filename)
        actual = Path("/etc/systemd/system" if filename.endswith(".service") else "/usr/local/sbin") / filename
        need(digest(actual) == expected, f"installed file hash drift: {filename}")
    return m


def acquire_locks(stack: ExitStack) -> None:
    for path in LOCKS:
        if path.parent == Path("/run/travel-scanner-deployer"):
            path.parent.mkdir(mode=0o700, exist_ok=True)
        fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
        stack.callback(os.close, fd)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)


def check_unit() -> None:
    command("systemd-analyze", "verify", "/etc/systemd/system/mokaair-a01-review@.service")


def container_id(service: str) -> str:
    result = command("docker", "ps", "--all", "--no-trunc",
                     "--filter", "label=com.docker.compose.project=travel_scanner",
                     "--filter", f"label=com.docker.compose.service={service}",
                     "--filter", "label=com.docker.compose.oneoff=False",
                     "--format", "{{.ID}}")
    candidates = [line.strip() for line in result.splitlines() if line.strip()]
    need(len(candidates) == 1 and bool(SHA.fullmatch(candidates[0])),
         f"{service} has no unique original container")
    original = candidates[0]
    labels = json.loads(command("docker", "inspect", "--format",
                                "{{json .Config.Labels}}", original))
    need(isinstance(labels, dict)
         and labels.get("com.docker.compose.project") == "travel_scanner"
         and labels.get("com.docker.compose.service") == service
         and labels.get("com.docker.compose.oneoff") == "False",
         f"{service} original Compose label drift")
    need(command("docker", "inspect", "--format", "{{.Id}}", original) == original,
         f"{service} original Docker ID drift")
    return original


def restart_policy(container: str) -> str:
    return command("docker", "inspect", "--format", "{{.HostConfig.RestartPolicy.Name}}", container)


def running(container: str) -> bool:
    return command("docker", "inspect", "--format", "{{.State.Running}}", container) == "true"


def sql(query: str) -> str:
    return compose("postgres", "psql", "-X", "-q", "-t", "-A", "-U", "travel", "-d",
                   "travel_scanner", "-v", "ON_ERROR_STOP=1", "-c", query)


def site_row(*, require_blocked: bool = True) -> dict:
    raw = sql("SELECT json_build_object('slug',slug,'stage',stage,"
              "'request',retry_request_id,'ack',retry_acknowledged_id)::text "
              "FROM video_projects WHERE slug='story-rolling-suitcase-v2'")
    row = json.loads(raw)
    need(row.get("slug") == "story-rolling-suitcase-v2", "A01 site row is absent")
    if require_blocked:
        need(row.get("stage") == "blocked", "A01 site row is no longer blocked")
    need(row.get("request") == row.get("ack"), "A01 owner Retry is pending")
    return row


def jobs() -> dict:
    raw = sql("SELECT json_build_object("
              "'stage',(SELECT count(*) FROM video_stage_jobs WHERE status IN ('queued','running')) ,"
              "'media',(SELECT count(*) FROM video_media_jobs WHERE status IN ('queued','submitted')) ,"
              "'a01',(SELECT count(*) FROM video_stage_jobs WHERE request_json->>'slug'="
              "'story-rolling-suitcase-v2' AND status IN ('queued','running')))::text")
    row = json.loads(raw)
    need(row == {"stage": 0, "media": 0, "a01": 0}, f"paid job not settled: {row}")
    return row


def budget() -> dict:
    row = json.loads(compose("api", "python", "-m", "app.video_budget.reconcile_cli",
                             "--slug", "story-rolling-suitcase-v2"))
    need(row.get("slug") == "story-rolling-suitcase-v2" and Decimal(row["limit_usd"]) == 25,
         "A01 budget cap changed")
    need(Decimal(row["reserved_usd"]) == 0 and Decimal(row["remaining_usd"]) > 0
         and int(row["uncertain_operations"]) == 0 and row["total_over_limit"] is False,
         "A01 budget has reservation, uncertainty or no room")
    return row


def no_leases() -> None:
    try:
        (WORK / "LEASE").lstat()
    except FileNotFoundError:
        pass
    else:
        raise RuntimeError("A01 project LEASE exists")
    # A foreign direct producer could be active without an API job yet. Refuse a
    # concurrent phase rather than freeze its worker process halfway through.
    live = []
    for path in WORK.parent.iterdir():
        info = path.lstat()
        need(not stat.S_ISLNK(info.st_mode), f"unexpected video work symlink: {path}")
        if stat.S_ISDIR(info.st_mode) and (path / "LEASE").exists():
            live.append(str(path))
    need(not live, f"video project LEASE exists: {live[:3]}")


def supervised(phase: str) -> None:
    # A direct shell invocation would lack systemd ExecStopPost after SIGKILL.
    # The phase and invocation must be the installed, distinct supervised unit.
    expected = f"mokaair-a01-review@{phase}.service"
    groups = Path("/proc/self/cgroup").read_text().splitlines()
    need(any(row.split(":", 2)[-1].endswith("/" + expected) for row in groups),
         f"not running inside {expected}; direct invocation is forbidden")
    need(bool(os.environ.get("INVOCATION_ID")), "systemd invocation ID is missing")


def worker_file(path: str, oneoff: str) -> str:
    return command("docker", "exec", oneoff, "sha256sum", path).split()[0]


def pinned_site_env(identity: str) -> None:
    values = json.loads(command("docker", "inspect", "--format", "{{json .Config.Env}}", identity))
    need("VIDEO_INTERNAL_SITE=http://web:3000" in values, "worker site environment drift")


def direct_node(identity: str, driver: str, argument: str,
                *, timeout_seconds: int = 120) -> str:
    pinned_site_env(identity)
    return command("docker", "exec", "-e", "MOKAAIR_SITE=http://web:3000",
                   identity, "node", driver, argument, timeout_seconds=timeout_seconds)


def driver_preflight(m: dict, phase: str, oneoff: str) -> dict:
    result = direct_node(oneoff, m["driver_container_path"], "--preflight")
    rows = [json.loads(line) for line in result.splitlines() if line.startswith("{")]
    match = [row for row in rows if row.get("event") == "A01_ROUND12_PREFLIGHT_PASS"]
    need(len(match) == 1, "driver preflight has no exact PASS event")
    row = match[0]
    need(row.get("links") == PHASES[phase][0]
         and row.get("source_sha256") == m["phase_sources"][phase]
         and row.get("stop_preserved") is True and row.get("model_calls") == 0,
         "driver source, link count or no-model receipt drift")
    return row


ONEOFF_TREE_VERIFY = r'''
import hashlib, json, stat, sys
from pathlib import Path
base = Path('/tmp/a01-round12-20261017-fe35369c/payload')
if not stat.S_ISDIR(base.lstat().st_mode):
    raise SystemExit('payload root is not a real directory')
expected = json.load(sys.stdin)
files, dirs = {}, set()
for path in base.rglob('*'):
    relative = path.relative_to(base).as_posix()
    info = path.lstat()
    if stat.S_ISREG(info.st_mode):
        files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    elif stat.S_ISDIR(info.st_mode):
        dirs.add(relative)
    else:
        raise SystemExit('payload link or special entry: ' + relative)
if files != expected['files'] or dirs != set(expected['dirs']):
    raise SystemExit('payload tree or bytes differ from reviewed archive')
print('A01_ONEOFF_PAYLOAD_TREE_VERIFIED files=' + str(len(files)))
'''


def created_oneoff_id(name: str, phase: str) -> str:
    # Resolve the exact Docker object by fixed phase label and name, independent
    # of CLI stdout formatting or caller capture behavior.
    listed = command("docker", "ps", "--all", "--no-trunc", "--filter",
                     f"label=mokaair.a01.round12={phase}", "--format", "{{.ID}}")
    identities = [line.strip() for line in listed.splitlines() if line.strip()]
    need(len(identities) == 1 and bool(SHA.fullmatch(identities[0])),
         "created A01 one-off has no unique full Docker ID")
    identity = identities[0]
    labels = json.loads(command("docker", "inspect", "--format", "{{json .Config.Labels}}", identity))
    need(command("docker", "inspect", "--format", "{{.Id}}", identity) == identity
         and command("docker", "inspect", "--format", "{{.Name}}", identity) == "/" + name
         and isinstance(labels, dict)
         and labels.get("mokaair.a01.round12") == phase
         and labels.get("com.docker.compose.project") == "travel_scanner"
         and labels.get("com.docker.compose.service") == "video-worker"
         and labels.get("com.docker.compose.oneoff") == "True",
         "created A01 one-off name, ID or Compose label drift")
    return identity


def create_oneoff(m: dict, phase: str, original_id: str) -> str:
    need(not ONEOFF.exists(), "prior one-off marker requires reconciliation")
    need(not command("docker", "ps", "--all", "--no-trunc", "--filter",
                     "label=mokaair.a01.round12", "--format", "{{.ID}}"),
         "prior labelled A01 one-off requires reconciliation")
    original_image = command("docker", "inspect", "--format", "{{.Image}}", original_id)
    need(original_image == m["video_worker_image_id"], "original worker image ID drift")
    need(command("docker", "inspect", "--format", "{{.Config.Image}}", original_id)
         == m["video_worker_image_ref"], "original worker image reference drift")
    need(command("docker", "image", "inspect", "--format", "{{.Id}}", m["video_worker_image_ref"])
         == m["video_worker_image_id"], "pinned image tag resolves to another image")
    compose_images = command("docker", "compose", "-f", str(ROOT / "docker-compose.prod.yml"),
                             "--profile", "video", "config", "--images").splitlines()
    need(m["video_worker_image_ref"] in compose_images, "Compose video image tag drift")
    name = f"mokaair-a01-round12-{phase}"
    command("docker", "compose", "-f", str(ROOT / "docker-compose.prod.yml"),
            "--profile", "video", "run", "--rm", "--detach", "--no-deps", "--pull", "never",
            "--name", name, "--label", f"mokaair.a01.round12={phase}",
            "video-worker", "sleep", "infinity")
    oneoff = created_oneoff_id(name, phase)
    # The one-off never runs worker.sh. No phase can start before this durable
    # marker is saved; a crash in this narrow interval leaves only sleeping.
    data = {"schema_version": 1, "slug": "story-rolling-suitcase-v2",
            "phase": phase, "container_id": oneoff, "original_worker_id": original_id}
    fd = os.open(ONEOFF, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        os.write(fd, (json.dumps(data, sort_keys=True) + "\n").encode())
        os.fsync(fd)
    finally:
        os.close(fd)
    parent = os.open(WORK, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(parent)
    finally:
        os.close(parent)
    need(running(oneoff) and restart_policy(oneoff) == "no", "one-off is not running with restart=no")
    need(command("docker", "inspect", "--format", "{{.HostConfig.AutoRemove}}", oneoff) == "true",
         "one-off auto-remove drift")
    need(command("docker", "inspect", "--format", "{{.Image}}", oneoff)
         == command("docker", "inspect", "--format", "{{.Image}}", original_id),
         "one-off image differs from pinned video-worker")
    need(command("docker", "inspect", "--format", "{{.Config.Hostname}}", oneoff) == "video-worker",
         "one-off hostname drift")
    pinned_site_env(oneoff)
    need(command("docker", "inspect", "--format", "{{index .Config.Labels \"mokaair.a01.round12\"}}", oneoff)
         == phase, "one-off label drift")
    mounts = json.loads(command("docker", "inspect", "--format", "{{json .Mounts}}", oneoff))
    actual = {(row.get("Name"), row.get("Destination")) for row in mounts}
    expected = {("travel_scanner_video_work", "/var/lib/mokaair/video-work"),
                ("travel_scanner_video_home", "/var/lib/mokaair/video-home"),
                ("travel_scanner_video_docs", "/opt/mokaair/docs/videos")}
    need(expected <= actual, "one-off named volumes drift")
    network = json.loads(command("docker", "inspect", "--format", "{{json .NetworkSettings.Networks}}", oneoff))
    need("travel_scanner_default" in network, "one-off site network drift")
    need(reviewed_payload_tree(Path(m["host_payload_archive_path"])) == m["_payload_tree"],
         "host payload changed after the initial full-tree check")
    command("docker", "exec", oneoff, "mkdir", "-p", str(CONTAINER_PAYLOAD))
    command("docker", "cp", str(HOST_PAYLOAD) + "/.", f"{oneoff}:{CONTAINER_PAYLOAD}/")
    # docker cp creates root-owned files. Only this one-off's private /tmp is
    # changed; make the reviewed archive readable by the pwuser direct driver.
    command("docker", "exec", "--user", "0", oneoff,
            "chmod", "-R", "a+rX", str(CONTAINER_PAYLOAD))
    need(command("docker", "exec", "-i", oneoff, "python3", "-c", ONEOFF_TREE_VERIFY,
                 input_bytes=json.dumps(m["_payload_tree"], sort_keys=True).encode())
         == "A01_ONEOFF_PAYLOAD_TREE_VERIFIED files=979", "one-off payload full-tree verification failed")
    for path, expected_hash in m["container_files"].items():
        need(worker_file(path, oneoff) == expected_hash, f"one-off payload hash drift: {path}")
    print(json.dumps({"event": "A01_ONEOFF_PINNED", "container_id": oneoff,
                      "phase": phase}), flush=True)
    return oneoff


def oneoff_stopped() -> None:
    record = json.loads(ONEOFF.read_text())
    identity = record["container_id"]
    result = subprocess.run(("docker", "inspect", "--format", "{{.State.Running}}", identity),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15,
                            check=False)
    if result.returncode:
        error = result.stderr.decode(errors="replace")
        a01_phase_recover.absent(result.returncode, error, identity)
    else:
        need(result.stdout.decode().strip() == "false",
             "one-off direct phase container still running")


WORKER_PROCESSES = r'''
import json, os
from pathlib import Path
rows = []
for entry in Path('/proc').iterdir():
    if not entry.name.isdigit() or int(entry.name) == os.getpid():
        continue
    try:
        stat = (entry / 'stat').read_text()
        state = stat[stat.rfind(')') + 2:].split()[0]
        argv = [part.decode(errors='replace') for part in (entry / 'cmdline').read_bytes().split(b'\0') if part]
    except (FileNotFoundError, ProcessLookupError):
        continue
    if state in ('Z', 'X', 'x') or not argv:
        continue
    rows.append(argv)
print(json.dumps(rows))
'''


def worker_quiet(identity: str) -> bool:
    rows = json.loads(command("docker", "exec", identity, "python3", "-c", WORKER_PROCESSES))
    need(isinstance(rows, list), "worker process inventory malformed")
    unexpected = []
    for argv in rows:
        name = Path(argv[0]).name
        if name == "docker-init":
            continue
        if name == "sh" and argv[1:] == ["/usr/local/bin/video-worker"]:
            continue
        if name == "sleep" and len(argv) == 2 and argv[1].isdigit():
            continue
        unexpected.append(argv[:3])
    if unexpected:
        print(json.dumps({"event": "A01_WAIT_WORKER_DRAIN", "unexpected": unexpected[:3]}), flush=True)
    return not unexpected


def global_stop_create() -> None:
    need(not GLOBAL_STOP.exists() and not GLOBAL_STOP.is_symlink(), "global STOP already exists")
    fd = os.open(GLOBAL_STOP, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        os.write(fd, GLOBAL_STOP_BYTES)
        os.fsync(fd)
    finally:
        os.close(fd)
    parent = os.open(WORK.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(parent)
    finally:
        os.close(parent)


def global_stop_clear() -> None:
    need(digest(GLOBAL_STOP) == hashlib.sha256(GLOBAL_STOP_BYTES).hexdigest(),
         "global STOP differs from this round's drain marker")
    GLOBAL_STOP.unlink()
    parent = os.open(WORK.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(parent)
    finally:
        os.close(parent)


def durable_pending(phase: str, source: str, stop_sha: str) -> None:
    need(not PENDING.exists(), "prior round12 pending guard exists; inspect before reuse")
    data = {"schema_version": 1, "slug": "story-rolling-suitcase-v2",
            "phase": PHASES[phase][1], "source_sha256": source,
            "stop_sha256": stop_sha, "host_startup_guard_verified": True}
    fd = os.open(PENDING, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        os.write(fd, (json.dumps(data, sort_keys=True) + "\n").encode())
        os.fsync(fd)
    finally:
        os.close(fd)
    parent = os.open(WORK, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(parent)
    finally:
        os.close(parent)


def phase_main(phase: str) -> int:
    supervised(phase)
    m = config()
    os.environ["RELEASE_SHA"] = m["video_worker_image_ref"].split(":", 1)[1]
    chosen = m["next_phase"] if phase in ("validate", "fault-test") else phase
    need(chosen == m["next_phase"], "service instance is not manifest's next phase")
    with ExitStack() as stack:
        acquire_locks(stack)
        need(command("git", "-C", str(ROOT), "rev-parse", "HEAD") == m["expected_head"],
             "live HEAD drift")
        need(not command("git", "-C", str(ROOT), "status", "--porcelain"), "live repo dirty")
        check_unit()
        need(digest(a01_stop_guard.Paths().stop) == m["expected_stop_sha256"], "A01 STOP hash drift")
        need(not a01_stop_guard.Paths().marker.exists() and not a01_stop_guard.Paths().held.exists()
             and not ONEOFF.exists() and not PENDING.exists(), "prior guard/phase needs recovery")
        ids = {"video-worker": m["video_worker_id"], "video-ai-worker": m["video_ai_worker_id"]}
        for service, identity in ids.items():
            need(container_id(service) == identity and running(identity)
                 and restart_policy(identity) == "unless-stopped", f"{service} ID/state/policy drift")
        site_before = site_row()
        jobs()
        budget()
        no_leases()
        if phase == "fault-test":
            # Disposable Linux/systemd/Docker test only. It creates a labelled,
            # sleeping container and blocks until the unit MainPID is killed.
            # No driver, LEASE, STOP lift, model or worker policy change occurs.
            need(m.get("fault_test_allowed") is True, "fault-test is not enabled in this manifest")
            test_id = create_oneoff(m, "fault-test", ids["video-worker"])
            print(json.dumps({"event": "A01_FAULT_TEST_READY", "oneoff": test_id,
                              "original_worker": ids["video-worker"],
                              "original_ai_worker": ids["video-ai-worker"]}), flush=True)
            while True:
                time.sleep(30)
        if phase == "validate":
            # This is a bounded host write: create/kill an inert one-off and
            # write its private /tmp capture. The original worker's /tmp may
            # hold an older driver; it is never read or overwritten here.
            # Project STOP remains present. No model is called.
            test_id = create_oneoff(m, "validate", ids["video-worker"])
            progress = driver_preflight(m, chosen, test_id)
            command("python3", "/usr/local/sbin/a01_phase_recover.py")
            oneoff_stopped()
            ONEOFF.unlink()
            print(json.dumps({"event": "A01_NO_MODEL_VALIDATION_PASS", "source": progress["source_sha256"],
                              "bounded_host_write": True}), flush=True)
            return 0
        hold_file = Path("/root/travel-scanner-deploy.hold")
        if chosen == "listener":
            need(not hold_file.exists(), "another release hold exists")
            need(hold.acquire(str(RELEASE), m["expected_head"], "codex-a01-round12-review",
                              ["listener", "manual", "facts", "panel"]) == "created", "hold not newly acquired")
        else:
            hold.verify(str(RELEASE), m["expected_head"])
        # STOP stays present until both video containers cannot auto restart.
        # A short-lived global STOP prevents a new Shorts tick or auto unit
        # while we wait for any in-flight child to finish before docker stop.
        for identity in ids.values():
            command("docker", "update", "--restart=no", identity)
        for service, identity in ids.items():
            need(container_id(service) == identity and restart_policy(identity) == "no",
                 f"{service} restart=no not read back")
        global_stop_create()
        deadline = time.monotonic() + 120
        while True:
            jobs(); no_leases()
            need(site_row() == site_before, "site Retry/stage changed during global drain")
            if worker_quiet(ids["video-worker"]):
                break
            need(time.monotonic() < deadline, "video/Shorts process did not drain within 120 s")
            time.sleep(2)
        command("docker", "stop", "--time", "20", ids["video-worker"])
        need(not running(ids["video-worker"]), "original auto worker still running")
        jobs(); no_leases()
        need(site_row() == site_before, "site Retry/stage changed after auto stop")
        global_stop_clear()
        oneoff = create_oneoff(m, chosen, ids["video-worker"])
        progress = driver_preflight(m, chosen, oneoff)
        need(digest(a01_stop_guard.Paths().stop) == m["expected_stop_sha256"], "STOP changed before arm")
        print(a01_stop_guard.arm(), flush=True)
        need(a01_stop_guard.Paths().marker.is_file() and a01_stop_guard.Paths().held.is_file(),
             "durable STOP recovery marker not read back")
        # Docker's persisted `restart=no` on both exact IDs is the reboot gate.
        # After reboot neither worker may be started before manual STOP recovery.
        for service, identity in ids.items():
            need(container_id(service) == identity and running(identity) == (service == "video-ai-worker")
                 and restart_policy(identity) == "no", f"{service} reboot gate drift")
        need(running(oneoff) and restart_policy(oneoff) == "no", "one-off reboot gate drift")
        durable_pending(chosen, progress["source_sha256"], m["expected_stop_sha256"])
        need(site_row() == site_before, "site Retry/stage changed before phase")
        # Exact direct phase only. This is the sole possible model dispatch here.
        print(direct_node(oneoff, m["driver_container_path"], PHASES[chosen][1],
                          timeout_seconds=3600), flush=True)
        # The original worker's /tmp is cleared by docker stop, so inspect the
        # next audit link in the same pinned one-off before killing it.
        after = direct_node(oneoff, m["driver_container_path"], "--preflight")
        rows = [json.loads(line) for line in after.splitlines() if line.startswith("{")]
        need(any(row.get("event") == "A01_ROUND12_PREFLIGHT_PASS"
                 and row.get("links") == PHASES[chosen][0] + 1
                 and row.get("stop_preserved") is True and row.get("model_calls") == 0
                 for row in rows), "phase did not append exactly one verified link")
        command("python3", "/usr/local/sbin/a01_phase_recover.py")
        oneoff_stopped()
        need(digest(a01_stop_guard.Paths().stop) == m["expected_stop_sha256"], "restored STOP differs")
        jobs(); budget(); no_leases()
        site_after = site_row(require_blocked=False)
        need(site_after.get("request") == site_before.get("request")
             and site_after.get("ack") == site_before.get("ack"), "A01 owner Retry changed during phase")
        command("docker", "start", ids["video-worker"])
        need(running(ids["video-worker"]) and restart_policy(ids["video-worker"]) == "no",
             "original worker did not restart safely under A01 STOP")
        for service, identity in ids.items():
            need(container_id(service) == identity and running(identity), f"{service} stopped or replaced")
            command("docker", "update", "--restart=unless-stopped", identity)
            need(restart_policy(identity) == "unless-stopped", f"{service} restart policy restore failed")
        print(a01_stop_guard.finish(), flush=True)
        PENDING.unlink()
        ONEOFF.unlink()
        print(json.dumps({"event": "A01_PHASE_SETTLED_STOP_PRESENT", "phase": chosen,
                          "source": progress["source_sha256"]}), flush=True)
        return 0


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in (*PHASES, "validate", "fault-test"):
        print("usage: a01_phase_runner.py validate|fault-test|listener|manual|facts|panel", file=sys.stderr)
        return 2
    try:
        phase = sys.argv[1]
        return phase_main(phase)
    except (OSError, RuntimeError, ValueError, KeyError, json.JSONDecodeError,
            tarfile.TarError, subprocess.TimeoutExpired) as error:
        print(f"A01 PHASE HELD: {error}", file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
