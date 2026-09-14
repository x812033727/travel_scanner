"""Run one reviewed publication phase with existing Compose API configuration.

Linux host only. Usage: python publish_host.py <deployed SHA> <manifest SHA256> <phase>
No services are replaced; a temporary API-image CLI container uses durable host journal storage.
"""
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


TARGET, MANIFEST_SHA, PHASE = sys.argv[1:4]
require(bool(re.fullmatch(r"[a-f0-9]{40}", TARGET)), "Invalid release SHA")
require(bool(re.fullmatch(r"[a-f0-9]{64}", MANIFEST_SHA)), "Invalid manifest SHA256")
require(PHASE in {"dry-run", "drafts", "publish-articles", "publish-index"}, "Unknown phase")
BASE = Path("/root/mokaair-ai-terms-" + TARGET[:12])
SOURCE = BASE / "source"
ENV = BASE / "runtime.env"
environment = {"PATH": os.environ.get("PATH", "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"),
               "HOME": "/root", "RELEASE_SHA": TARGET, "RUNTIME_ENV_FILE": str(ENV)}
ONEOFF_NAME = "travel-scanner-ai-terms-" + TARGET[:12] + "-" + PHASE
MANIFEST_LABEL = "io.mokaair.ai-terms.manifest-sha256"
os.umask(0o077)
locks = []
for path in ["/var/lock/travel-scanner-deploy.lock", "/root/mokaair-deploy.lock",
             "/run/mokaair-manual-deploy.lock", "/run/travel-scanner-deployer/deploy.lock"]:
    handle = open(path, "r+")
    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    locks.append(handle)
log = (BASE / ("publish-" + PHASE + ".log")).open("a")


def run(args, *, capture=False, stdin=None, timeout=1800):
    result = subprocess.run(args, stdin=stdin, stdout=subprocess.PIPE if capture else log,
                            stderr=log, text=capture, env=environment, timeout=timeout)
    require(result.returncode == 0, "Command failed; inspect private publication log and journal")
    return result.stdout if capture else None


def digest(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def inspect_oneoff():
    # Filter may match substrings, so inspect and compare the complete Docker name.
    ids = run(["docker", "container", "ls", "--all", "--filter", "name=" + ONEOFF_NAME,
               "--format", "{{.ID}}"], capture=True, timeout=60).splitlines()
    for container_id in ids:
        row = json.loads(run(["docker", "inspect", container_id], capture=True, timeout=60))[0]
        if row["Name"] == "/" + ONEOFF_NAME:
            return row
    return None


def require_owned_oneoff(row, container_id=None):
    require(row["Name"] == "/" + ONEOFF_NAME, "Publisher name does not match")
    require(container_id is None or row["Id"] == container_id, "Publisher container identity changed")
    require(row["Image"] == release["api_image"], "Refusing to stop an unexpected publisher image")
    require((row["Config"].get("Labels") or {}).get(MANIFEST_LABEL) == MANIFEST_SHA,
            "Refusing to stop a publisher with an unexpected manifest label")


def stop_owned_oneoff():
    """Called with all host locks still held; never addresses normal service containers."""
    row = inspect_oneoff()
    if row is None:
        return
    require_owned_oneoff(row)
    container_id = row["Id"]
    if row["State"]["Running"]:
        try:
            run(["docker", "stop", "--time", "20", container_id], timeout=45)
        except (RuntimeError, subprocess.TimeoutExpired):
            pass  # Reinspect before deciding whether the exact same container needs kill.
    row = inspect_oneoff()
    if row is None:
        return
    require_owned_oneoff(row, container_id)
    if row["State"]["Running"]:
        try:
            run(["docker", "kill", container_id], timeout=30)
        except (RuntimeError, subprocess.TimeoutExpired):
            pass
    row = inspect_oneoff()
    if row is None:
        return
    require_owned_oneoff(row, container_id)
    require(not row["State"]["Running"], "Publisher did not stop; manual intervention required")


release = json.loads((BASE / "state.json").read_text())
require(release["target"] == TARGET and release.get("activated_at") and not release.get("failed_at"), "Release is not successfully active")
require(run(["git", "-C", "/root/travel_scanner", "rev-parse", "HEAD"], capture=True).strip() == TARGET, "Host checkout changed")
require(digest(ENV) == release["env_hash"] == digest(Path("/root/travel_scanner/.env")), "Runtime changed")
require(ENV.stat().st_mode & 0o777 == 0o600, "Runtime snapshot mode changed")
manifest = SOURCE / "docs/ai-terms-series/release-manifest.json"
require(digest(manifest) == MANIFEST_SHA, "Reviewed manifest changed")
for service in release["after"]:
    current = json.loads(run(["docker", "inspect", "travel_scanner-" + service + "-1"], capture=True))[0]
    require(current["State"]["Status"] == "running" and current["Image"] == release["after"][service]["image"], "Running release changed: " + service)
    require(hashlib.sha256(json.dumps(sorted(current["Config"]["Env"])).encode()).hexdigest() == release["after"][service]["env_hash"], "Service environment changed: " + service)
image = json.loads(run(["docker", "image", "inspect", "travel-scanner-api:" + TARGET], capture=True))[0]
require(image["Id"] == release["api_image"], "Publisher image tag changed")
require(inspect_oneoff() is None, "Existing publisher container requires inspection before rerun")

state_dir = BASE / "publication-state"
state_dir.mkdir(mode=0o700, exist_ok=True)
os.chown(state_dir, 10001, 10001)
os.chmod(state_dir, 0o700)
if PHASE == "drafts":
    backup_receipt = BASE / "prepublish-backup.json"
    if backup_receipt.exists():
        receipt = json.loads(backup_receipt.read_text())
        require(digest(Path(receipt["path"])) == receipt["sha256"], "Publication backup changed")
    else:
        dump = BASE / "prepublish.dump"
        with dump.open("xb") as output:
            result = subprocess.run(["docker", "exec", "travel_scanner-postgres-1", "pg_dump", "-U", "travel", "-d", "travel_scanner", "-Fc"], stdout=output, stderr=log, timeout=600, env=environment)
        require(result.returncode == 0 and dump.stat().st_size > 0, "Publication backup failed")
        with dump.open("rb") as input_file:
            run(["docker", "exec", "-i", "travel_scanner-postgres-1", "pg_restore", "--list"], stdin=input_file)
        receipt = {"created_at": datetime.now(timezone.utc).isoformat(), "path": str(dump),
                   "bytes": dump.stat().st_size, "sha256": digest(dump), "index_verified": True}
        backup_receipt.write_text(json.dumps(receipt, indent=2))

command = ["docker", "compose", "-p", "travel_scanner", "--env-file", str(ENV),
           "-f", str(SOURCE / "docker-compose.prod.yml"), "--profile", "hotspots",
           "run", "--rm", "--no-deps", "-T", "--name", ONEOFF_NAME,
           "--label", MANIFEST_LABEL + "=" + MANIFEST_SHA,
           "--volume", str(SOURCE / "docs/ai-terms-series") + ":/batch:ro",
           "--volume", str(SOURCE / "apps/web/public") + ":/public:ro",
           "--volume", str(state_dir) + ":/publication-state",
           "api", "python", "/batch/publish_batch.py", "--manifest", "/batch/release-manifest.json",
           "--manifest-sha256", MANIFEST_SHA, "--public-dir", "/public",
           "--state-dir", "/publication-state", PHASE]
try:
    output = run(command, capture=True)
    result = json.loads(output)
    require(result["phase"] == PHASE and result["status"] in {"read_only", "complete"}, "Unexpected publication result")
except BaseException:
    # Killing the Compose client on timeout does not prove its server-side job stopped.
    # Preserve the durable journal so publish_batch can reconcile an uncertain commit.
    stop_owned_oneoff()
    raise
(BASE / ("publication-" + PHASE + ".json")).write_text(json.dumps(result, indent=2))
print(json.dumps(result))
