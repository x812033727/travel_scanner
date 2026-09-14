"""Reconcile one explicitly observed external deployment with a prepared release.

Linux host only. This incident-specific tool retains the original state and rollback
tags, pins the observed images under new rollback tags, and updates only the next
deployment's baseline. It never stops/restarts services, builds images, imports
content, creates a database backup, or marks a release activated.

Run with --target, --manifest-sha256, --observed-api-image and --observed-web-image.
All four must match the reviewed incident pins below. Existing shared host locks
are held throughout. A partial tag operation can be resumed only if every live
guard and the retained original-state bytes still match. A reconciled state is
never silently reconciled again.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import urllib.request
from contextlib import ExitStack, contextmanager
from datetime import UTC, datetime
from pathlib import Path

TARGET = "3b8df68c693eb81ccde7793a2f89d71999dbb2c2"
DOCUMENTATION_MAIN = "50591be5fc402fd4dd4ad55fb1af92cf0606f674"
ORIGINAL_PREVIOUS = "2123edbd2e1fc53adef0b89952ead60deef31feb"
MANIFEST_SHA256 = "96ad2cb050c0b31a678e446c08e428746d1e3e873343a9a72ae0353f48ca7d59"
PREPARED_IMAGES = {
    "api": "sha256:0c8466ae242ef94e18f2dcf4979cabc7d51aab1f2d06fa96c9f5bf54988a8e7a",
    "web": "sha256:65cf8f61552e84ea0ef0f80a51fbe38adba624d059b96c2628410007d6ca5745",
}
OBSERVED_IMAGES = {
    "api": "sha256:7b5e56291f498ab952601db4f272be2526af50dc109872a6899ce8b98aa848ea",
    "web": "sha256:d814fec0b47cd985f36cb002fdff1a669e807665e258060c08f1b1709f08598a",
}
SERVICES = (
    "api",
    "web",
    "worker",
    "alert-worker",
    "alert-scheduler",
    "hotspot-collector",
    "analytics-scheduler",
    "community-sweeper",
)
ALL_SERVICES = SERVICES + ("postgres", "redis")
ROOT = Path("/root/travel_scanner")
BASE = Path("/root/mokaair-ai-terms-" + TARGET[:12])
ORIGINAL_ROLLBACK_TAG = "rollback-ai-terms-" + TARGET[:12]
OBSERVED_ROLLBACK_TAG = ORIGINAL_ROLLBACK_TAG + "-observed"
LOCKS = (
    "/var/lock/travel-scanner-deploy.lock",
    "/root/mokaair-deploy.lock",
    "/run/mokaair-manual-deploy.lock",
    "/run/travel-scanner-deployer/deploy.lock",
)


class Refused(RuntimeError):
    """Safe diagnostic which excludes private file contents and subprocess output."""


def require(condition, message):
    if not condition:
        raise Refused(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(UTC).isoformat()


def image_sha(value):
    return (
        isinstance(value, str)
        and re.fullmatch(r"sha256:[a-f0-9]{64}", value) is not None
    )


def read_regular(path, *, mode=None):
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(descriptor, "rb") as handle:
        info = os.fstat(handle.fileno())
        require(stat.S_ISREG(info.st_mode), "Expected a regular private/source file")
        if mode is not None:
            require(
                stat.S_IMODE(info.st_mode) == mode, "Private file permissions differ"
            )
        return handle.read()


def fsync_directory(directory):
    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def preserve_original(path, raw):
    """Exclusive first save; an identical durable archive permits a partial-tag retry."""
    try:
        descriptor = os.open(
            path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600
        )
    except FileExistsError:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(descriptor, "rb") as handle:
            info = os.fstat(handle.fileno())
            require(
                stat.S_ISREG(info.st_mode)
                and stat.S_IMODE(info.st_mode) == 0o600
                and handle.read() == raw,
                "Retained original state differs; manual inspection required",
            )
            # A previous file fsync may have failed despite complete readable bytes.
            os.fsync(handle.fileno())
        fsync_directory(path.parent)
        return
    with os.fdopen(descriptor, "wb") as handle:
        require(
            handle.write(raw) == len(raw), "Original-state archive write was incomplete"
        )
        handle.flush()
        os.fsync(handle.fileno())
    fsync_directory(path.parent)


def atomic_state(path, original, replacement):
    """Replace only the unchanged original; a post-replace fsync error is explicit."""
    require(
        read_regular(path, mode=0o600) == original,
        "State changed before baseline write",
    )
    descriptor, name = tempfile.mkstemp(
        prefix=".external-baseline-", suffix=".json.next", dir=path.parent
    )
    temporary = Path(name)
    replaced = False
    try:
        with os.fdopen(descriptor, "wb") as handle:
            data = (json.dumps(replacement, indent=2) + "\n").encode()
            require(
                handle.write(data) == len(data),
                "Replacement-state write was incomplete",
            )
            handle.flush()
            os.fsync(handle.fileno())
        require(
            read_regular(path, mode=0o600) == original,
            "State changed during baseline write",
        )
        os.replace(temporary, path)
        replaced = True
        fsync_directory(path.parent)
    except BaseException:
        if replaced:
            raise Refused(
                "State was replaced but directory durability is uncertain; inspect state before any next action"
            ) from None
        if temporary.exists():
            temporary.unlink()
        raise


@contextmanager
def shared_locks():
    # Import lazily so --help works on the reviewer's non-Linux workstation.
    import fcntl

    with ExitStack() as stack:
        for name in LOCKS:
            handle = stack.enter_context(open(name, "r+"))
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Host:
    def __init__(self):
        self.state_path = BASE / "state.json"
        self.archive_path = BASE / "state-before-external-baseline.json"
        self.source = BASE / "source"
        self.runtime = BASE / "runtime.env"
        self.environment = {
            "PATH": os.environ.get(
                "PATH", "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ),
            "HOME": "/root",
            "RELEASE_SHA": TARGET,
            "RUNTIME_ENV_FILE": str(self.runtime),
        }

    def command(self, arguments):
        completed = subprocess.run(
            arguments,
            capture_output=True,
            env=self.environment,
            timeout=90,
            check=False,
        )
        require(
            completed.returncode == 0,
            "Host command failed; no command output is exposed",
        )
        return completed.stdout

    def git(self, *arguments):
        return (
            self.command(["git", "-C", str(ROOT), *arguments]).decode("utf-8").strip()
        )

    def image_id(self, reference, *, optional=False):
        if optional:
            rows = self.command(
                [
                    "docker",
                    "image",
                    "ls",
                    "--no-trunc",
                    "--filter",
                    "reference=" + reference,
                    "--format",
                    "{{.Repository}}:{{.Tag}} {{.ID}}",
                ]
            )
            matches = [
                line.split(" ", 1)[1]
                for line in rows.decode().splitlines()
                if line.startswith(reference + " ")
            ]
            require(len(matches) <= 1, "Ambiguous rollback image tag")
            if not matches:
                return None
        result = json.loads(self.command(["docker", "image", "inspect", reference]))
        require(
            isinstance(result, list)
            and len(result) == 1
            and image_sha(result[0].get("Id")),
            "Invalid immutable image identity",
        )
        return result[0]["Id"]

    def snapshot(self):
        current = {}
        for service in ALL_SERVICES:
            name = "travel_scanner-" + service + "-1"
            result = json.loads(self.command(["docker", "inspect", name]))
            require(
                isinstance(result, list) and len(result) == 1,
                "Ambiguous service container",
            )
            row = result[0]
            require(row.get("Name") == "/" + name, "Service container name differs")
            labels = row["Config"].get("Labels") or {}
            require(
                labels.get("com.docker.compose.project") == "travel_scanner"
                and labels.get("com.docker.compose.service") == service,
                "Service Compose labels differ",
            )
            current[service] = {
                "id": row["Id"],
                "image": row["Image"],
                "image_tag": row["Config"]["Image"],
                "status": row["State"]["Status"],
                "restarts": row["RestartCount"],
                "env_hash": sha(json.dumps(sorted(row["Config"]["Env"])).encode()),
                "mounts": row["Mounts"],
            }
        return current

    def healthy(self, schema):
        # Loopback readiness must never inherit a shell proxy or follow a redirect.
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}), NoRedirect()
        )
        for url in (
            "http://127.0.0.1:8090/ready",
            "http://127.0.0.1:8090/health",
            "http://127.0.0.1:8091/zh-TW/life",
        ):
            with opener.open(
                urllib.request.Request(url, method="GET"), timeout=15
            ) as response:
                require(
                    response.status == 200 and response.geturl() == url,
                    "Local readiness/health failed",
                )
                if url.endswith("/ready"):
                    result = json.load(response)
                    require(
                        result.get("status") == "ready"
                        and result.get("database") == result.get("redis") == "ok"
                        and result.get("schema") == schema,
                        "Readiness/schema baseline differs",
                    )

    def verify_source_runtime(self, state):
        require(
            sha(read_regular(ROOT / ".env"))
            == sha(read_regular(self.runtime, mode=0o600))
            == state["env_hash"],
            "Original runtime or prepared snapshot changed",
        )
        relative = "docs/ai-terms-series/release-manifest.json"
        manifest = read_regular(self.source / relative)
        require(sha(manifest) == MANIFEST_SHA256, "Prepared source manifest changed")
        committed = self.command(
            ["git", "-C", str(ROOT), "show", TARGET + ":" + relative]
        )
        require(
            committed == manifest,
            "Prepared manifest differs from the reviewed Git release",
        )
        for kind in ("api", "web"):
            require(
                state.get(kind + "_image") == PREPARED_IMAGES[kind]
                and self.image_id("travel-scanner-" + kind + ":" + TARGET)
                == PREPARED_IMAGES[kind],
                "Prepared immutable release image changed",
            )
            require(
                self.image_id("travel-scanner-" + kind + ":local")
                == OBSERVED_IMAGES[kind],
                "Observed local image tag changed",
            )
            require(
                self.image_id("travel-scanner-" + kind + ":" + ORIGINAL_ROLLBACK_TAG)
                == state["before"][kind]["image"],
                "Original rollback image is no longer retained",
            )

    def verify_checkout(self, *, fetch):
        if fetch:
            self.git("fetch", "origin", "main")
        main = self.git("rev-parse", "origin/main")
        require(main in {TARGET, DOCUMENTATION_MAIN}, "Main advanced beyond reviewed documentation")
        if main != TARGET:
            changed = self.git("diff", "--name-only", TARGET, main).splitlines()
            require(all(path.startswith("docs/ai-news-2026-09/") or path == "tasks/done/2026-09-14-ai-news-july-september.md" for path in changed), "Main has changes beyond reviewed publication receipts")
        require(
            self.git("rev-parse", "HEAD")
            == TARGET
            and not self.git("status", "--porcelain"),
            "Checkout/main must remain clean at the reviewed release",
        )

    def preserve(self, raw):
        preserve_original(self.archive_path, raw)

    def install_state(self, original, replacement):
        atomic_state(self.state_path, original, replacement)

    def tag_observed(self, kind):
        reference = "travel-scanner-" + kind + ":" + OBSERVED_ROLLBACK_TAG
        present = self.image_id(reference, optional=True)
        require(
            present in {None, OBSERVED_IMAGES[kind]},
            "Observed rollback tag belongs to a different image",
        )
        if present is None:
            self.command(["docker", "image", "tag", OBSERVED_IMAGES[kind], reference])
        require(
            self.image_id(reference) == OBSERVED_IMAGES[kind],
            "Observed rollback tag could not be verified",
        )


def validate_arguments(args):
    require(
        args.target == TARGET and args.manifest_sha256 == MANIFEST_SHA256,
        "This helper is restricted to the reviewed incident release and manifest",
    )
    require(
        args.observed_api_image == OBSERVED_IMAGES["api"]
        and args.observed_web_image == OBSERVED_IMAGES["web"],
        "Observed image arguments differ from reviewed incident pins",
    )


def validate_original(state):
    require(
        state.get("target") == TARGET
        and state.get("previous") == ORIGINAL_PREVIOUS
        and state.get("rollback_tag") == ORIGINAL_ROLLBACK_TAG,
        "Original prepared state identity differs",
    )
    require(
        not any(
            key in state
            for key in (
                "activated_at",
                "failed_at",
                "backup",
                "after",
                "external_baseline",
                "status",
                "rollback_status",
            )
        ),
        "State is activated, failed, backed up, or already reconciled",
    )
    require(
        isinstance(state.get("built_at"), str), "Release has not completed preparation"
    )
    try:
        built = datetime.fromisoformat(state["built_at"].replace("Z", "+00:00"))
    except ValueError:
        raise Refused("Invalid prepared build timestamp") from None
    require(
        built.utcoffset() is not None and built <= datetime.now(UTC),
        "Invalid/future prepared build timestamp",
    )
    require(
        isinstance(state.get("env_hash"), str)
        and re.fullmatch(r"[a-f0-9]{64}", state["env_hash"]),
        "Missing prepared environment fingerprint",
    )
    before = state.get("before")
    require(
        isinstance(before, dict) and set(before) == set(ALL_SERVICES),
        "Original service snapshot scope differs",
    )
    for service in SERVICES:
        require(
            before[service].get("status") == "running"
            and image_sha(before[service].get("image"))
            and before[service].get("image_tag")
            == "travel-scanner-"
            + ("web" if service == "web" else "api")
            + ":"
            + ORIGINAL_PREVIOUS,
            "Original application baseline differs",
        )


def validate_current(state, current):
    require(
        set(current) == set(ALL_SERVICES), "Observed service snapshot scope differs"
    )
    for service in SERVICES:
        kind = "web" if service == "web" else "api"
        row = current[service]
        require(
            row.get("image") == OBSERVED_IMAGES[kind]
            and row.get("image_tag") == "travel-scanner-" + kind + ":local"
            and row.get("status") == "running"
            and row.get("restarts") == 0,
            "Observed application image/tag/health differs",
        )
        require(
            row.get("env_hash") == state["before"][service].get("env_hash"),
            "Observed application environment differs from original baseline",
        )
    require(
        all(
            current[service] == state["before"][service]
            and current[service].get("status") == "running"
            for service in ("postgres", "redis")
        ),
        "Database/cache containers changed from the original snapshot",
    )


def reconcile(args, host):
    validate_arguments(args)
    original = read_regular(host.state_path, mode=0o600)
    state = json.loads(original)
    validate_original(state)
    host.verify_checkout(fetch=True)
    host.verify_source_runtime(state)
    current = host.snapshot()
    validate_current(state, current)
    host.healthy(state["schema"])
    # Refuse a conflict in either new tag before creating either tag or the archive.
    for kind in ("api", "web"):
        present = host.image_id(
            "travel-scanner-" + kind + ":" + OBSERVED_ROLLBACK_TAG, optional=True
        )
        require(
            present in {None, OBSERVED_IMAGES[kind]},
            "Observed rollback tag already belongs to a different image",
        )
    require(
        read_regular(host.state_path, mode=0o600) == original,
        "State changed during preflight",
    )
    host.preserve(original)
    for kind in ("api", "web"):
        host.tag_observed(kind)
    # Competing clients ignoring the locks cannot turn a stale snapshot into activation.
    host.verify_checkout(fetch=True)
    host.verify_source_runtime(state)
    final_current = host.snapshot()
    validate_current(state, final_current)
    require(
        final_current == current,
        "Service baseline changed while retaining rollback images",
    )
    host.healthy(state["schema"])
    replacement = copy.deepcopy(state)
    replacement.update(
        previous=TARGET,
        before=current,
        rollback_tag=OBSERVED_ROLLBACK_TAG,
        external_baseline={
            "reconciled_at": now(),
            "original_previous": ORIGINAL_PREVIOUS,
            "original_rollback_tag": ORIGINAL_ROLLBACK_TAG,
            "original_images": {
                kind: state["before"][kind]["image"] for kind in ("api", "web")
            },
            "observed_images": dict(OBSERVED_IMAGES),
            "manifest_sha256": MANIFEST_SHA256,
            "original_state_sha256": sha(original),
            "reason": "External application replacement at the same reviewed Git release; this records a baseline only.",
        },
    )
    require(
        all(
            replacement[key] == value
            for key, value in state.items()
            if key not in {"previous", "before", "rollback_tag"}
        ),
        "Prepared/source/build state must remain unchanged",
    )
    host.install_state(original, replacement)
    return {
        "status": "baseline_reconciled",
        "target": TARGET,
        "reconciled_at": replacement["external_baseline"]["reconciled_at"],
        "prepared_images": PREPARED_IMAGES,
        "rollback_images": OBSERVED_IMAGES,
        "activated": False,
        "backup_created": False,
        "services_restarted": False,
        "next_step": "The separately guarded release activate phase must take a fresh backup and verify the prepared images.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--observed-api-image", required=True)
    parser.add_argument("--observed-web-image", required=True)
    args = parser.parse_args(argv)
    try:
        require(sys.platform.startswith("linux"), "This host helper only runs on Linux")
        validate_arguments(args)
        os.umask(0o077)
        with shared_locks():
            result = reconcile(args, Host())
    except Exception as error:  # noqa: BLE001 - no private state or command output in diagnostics
        print(
            json.dumps(
                {
                    "status": "refused",
                    "reason": str(error)
                    if isinstance(error, Refused)
                    else "Baseline reconciliation stopped; inspect the retained state and image tags",
                    "activated": False,
                    "backup_created": False,
                }
            )
        )
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
