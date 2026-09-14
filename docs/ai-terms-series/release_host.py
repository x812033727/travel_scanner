"""Guarded host release driver. Run only after full editorial acceptance and green CI.

Requires Linux host, existing PuTTY-authorized production and a reviewed main SHA.
No content publication, nginx edits, runtime edits, or database migrations occur here.
Usage: python release_host.py <40-char reviewed main SHA> prepare|activate
"""
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.request

if sys.flags.optimize:
    raise RuntimeError("Optimized Python disables required release guards; run without -O/PYTHONOPTIMIZE")

TARGET, PHASE = sys.argv[1:3]
assert re.fullmatch(r"[0-9a-f]{40}", TARGET) and PHASE in {"prepare", "activate"}
ROOT = Path("/root/travel_scanner")
BASE = Path("/root/mokaair-ai-terms-" + TARGET[:12])
SOURCE = BASE / "source"
ORIGINAL_ENV = ROOT / ".env"
ENV = BASE / "runtime.env"
SERVICES = ["api", "web", "worker", "alert-worker", "alert-scheduler",
            "hotspot-collector", "analytics-scheduler", "community-sweeper"]
os.umask(0o077)
BASE.mkdir(mode=0o700, exist_ok=True)
locks = []
for name in ["/var/lock/travel-scanner-deploy.lock", "/root/mokaair-deploy.lock",
             "/run/mokaair-manual-deploy.lock", "/run/travel-scanner-deployer/deploy.lock"]:
    assert Path(name).is_file(), "Existing shared lock missing; inspect ownership before creating"
    handle = open(name, "r+")
    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    locks.append(handle)
log = open(BASE / (PHASE + ".log"), "a", buffering=1)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def say(value):
    print(now(), value, flush=True)
    print(now(), value, file=log)


def run(args, capture=False, stdin=None, timeout=2400, env=None):
    result = subprocess.run(args, stdin=stdin, stdout=subprocess.PIPE if capture else log,
                            stderr=log, text=capture, timeout=timeout, env=env)
    if result.returncode:
        raise RuntimeError(f"{args[0]} {args[1]} failed ({result.returncode}); see private log")
    return result.stdout.strip() if capture else None


def git(*args):
    return run(["git", "-C", str(ROOT), *args], capture=True)


def digest(path):
    return hashlib.file_digest(open(path, "rb"), "sha256").hexdigest()


def inspect(name):
    return json.loads(run(["docker", "inspect", name], capture=True))[0]


def containers():
    state = {}
    for service in SERVICES + ["postgres", "redis"]:
        row = inspect("travel_scanner-" + service + "-1")
        state[service] = {
            "id": row["Id"], "image": row["Image"], "image_tag": row["Config"]["Image"],
            "status": row["State"]["Status"], "restarts": row["RestartCount"],
            "env_hash": hashlib.sha256(json.dumps(sorted(row["Config"]["Env"])).encode()).hexdigest(),
            "mounts": row["Mounts"],
        }
    return state


def compose(*args, tag=TARGET, capture=False):
    # Interpolation must come from the pinned runtime file, never the caller's shell.
    env = {"PATH": os.environ.get("PATH", "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"),
           "HOME": "/root", "RELEASE_SHA": tag, "RUNTIME_ENV_FILE": str(ENV)}
    return run(["docker", "compose", "-p", "travel_scanner", "--env-file", str(ENV),
                "-f", str(SOURCE / "docker-compose.prod.yml"), "--profile", "hotspots", *args], env=env, capture=capture)


def effective_environment_hash(image_environment, service_environment):
    values = dict(item.split("=", 1) for item in (image_environment or []))
    for name, value in service_environment.items():
        if value is None:
            values.pop(name, None)
        else:
            values[name] = str(value)
    return hashlib.sha256(json.dumps(sorted(f"{name}={value}" for name, value in values.items())).encode()).hexdigest()


def verify_effective_environment(state, images):
    # Capture the resolved model privately in memory; it contains runtime secrets.
    model = json.loads(compose("config", "--format", "json", capture=True))
    for service in SERVICES:
        environment = model["services"][service].get("environment", {})
        if not isinstance(environment, dict):
            raise RuntimeError(f"Compose environment is not normalized for {service}")
        image_environment = inspect(images[service])["Config"].get("Env")
        actual = effective_environment_hash(image_environment, environment)
        if actual != state["before"][service]["env_hash"]:
            raise RuntimeError(f"Effective environment differs for {service}; activation refused")


def verify_runtime_snapshot(state):
    if digest(ORIGINAL_ENV) != state["env_hash"] or digest(ENV) != state["env_hash"]:
        raise RuntimeError("Original runtime or release snapshot changed; activation refused")
    if ENV.stat().st_mode & 0o777 != 0o600:
        raise RuntimeError("Release runtime snapshot must have mode 0600")


def save(state):
    temporary = BASE / "state.json.next"
    with temporary.open("w") as handle:
        json.dump(state, handle, indent=2)
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(BASE / "state.json")


def ready():
    with urllib.request.urlopen("http://127.0.0.1:8090/ready", timeout=15) as response:
        result = json.load(response)
        assert result["status"] == "ready" and result["database"] == result["redis"] == "ok"
        return result


def healthy(schema):
    streak = 0
    for _ in range(40):
        try:
            assert ready()["schema"] == schema
            for url in ["http://127.0.0.1:8090/health", "http://127.0.0.1:8091/zh-TW/life"]:
                with urllib.request.urlopen(url, timeout=15) as response:
                    assert response.status == 200
            streak += 1
            if streak == 3:
                return
        except Exception:
            streak = 0
        time.sleep(3)
    raise RuntimeError("Health verification failed")


if PHASE == "prepare":
    assert not (BASE / "state.json").exists(), "Existing release must be inspected, not overwritten"
    git("fetch", "origin", "main")
    assert git("rev-parse", "origin/main") == TARGET
    previous = git("rev-parse", "HEAD")
    assert not git("status", "--porcelain")
    assert not git("diff", "--name-only", previous, TARGET, "--",
                   "apps/api/migrations", "docker-compose.prod.yml", ".env.example"), "Infrastructure changed; needs separate review"
    before = containers()
    assert all(x["status"] == "running" for x in before.values())
    assert all(before[s]["image_tag"].endswith(":" + previous) for s in SERVICES), "Checkout and running release differ"
    state = {"target": TARGET, "previous": previous, "before": before, "env_hash": digest(ORIGINAL_ENV),
             "schema": ready()["schema"], "started_at": now(), "rollback_tag": "rollback-ai-terms-" + TARGET[:12]}
    runtime_bytes = ORIGINAL_ENV.read_bytes()
    if hashlib.sha256(runtime_bytes).hexdigest() != state["env_hash"]:
        raise RuntimeError("Runtime changed while taking release snapshot")
    with ENV.open("xb") as handle:
        handle.write(runtime_bytes)
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(ENV, 0o600)
    verify_runtime_snapshot(state)
    SOURCE.mkdir(mode=0o755)
    run(["git", "-C", str(ROOT), "archive", "--format=tar", "--output", str(BASE / "source.tar"), TARGET])
    previous_mask = os.umask(0o022)
    try:
        run(["tar", "-xf", str(BASE / "source.tar"), "-C", str(SOURCE)])
    finally:
        os.umask(previous_mask)
    assert not (SOURCE / ".env").exists()
    catalogue = json.loads((SOURCE / "docs/ai-terms-series/catalogue.json").read_text())
    validation = json.loads((SOURCE / "docs/ai-terms-series/validation.json").read_text())
    assert len(catalogue["terms"]) == 81 and all(t["status"] == "verified" for t in catalogue["terms"])
    assert not validation["missing"] and not validation["errors"] and validation["database"]["published_reads"] == 83
    for service in ["api", "web"]:
        run(["docker", "image", "tag", before[service]["image"], "travel-scanner-" + service + ":" + state["rollback_tag"]])
    save(state)
    compose("config", "--quiet")
    verify_effective_environment(state, {service: before[service]["image"] for service in SERVICES})
    say("Building reviewed content and assets while current services remain live")
    compose("build", "api", "web")
    for service in ["api", "web"]:
        state[service + "_image"] = inspect("travel-scanner-" + service + ":" + TARGET)["Id"]
    verify_runtime_snapshot(state)
    verify_effective_environment(state, {
        service: state["web_image" if service == "web" else "api_image"] for service in SERVICES
    })
    state["built_at"] = now()
    save(state)
    say("BUILD_READY " + TARGET)
else:
    state = json.loads((BASE / "state.json").read_text())
    assert state["target"] == TARGET and state.get("built_at") and not state.get("activated_at")
    assert not state.get("failed_at"), "Failed release requires explicit inspection before another attempt"
    ci = json.loads((BASE / "ci.json").read_text())
    assert ci["headSha"] == TARGET and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["workflowName"] == "CI" and ci["event"] == "push" and ci["headBranch"] == "main"
    assert re.fullmatch(r"https://github.com/x812033727/travel_scanner/actions/runs/[0-9]+", ci["url"])
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    git("fetch", "origin", "main")
    assert git("rev-parse", "origin/main") == TARGET, "Main advanced; refresh reviewed release"
    assert git("rev-parse", "HEAD") == state["previous"] and not git("status", "--porcelain")
    verify_runtime_snapshot(state)
    assert containers() == state["before"], "Live baseline changed"
    verify_effective_environment(state, {
        service: state["web_image" if service == "web" else "api_image"] for service in SERVICES
    })
    stopped = False
    checkout_advanced = False
    try:
        stopped = True
        run(["docker", "stop", "--time", "45", *["travel_scanner-" + s + "-1" for s in SERVICES]])
        dump = BASE / "predeploy.dump"
        with dump.open("wb") as output:
            result = subprocess.run(["docker", "exec", "travel_scanner-postgres-1", "pg_dump",
                                     "-U", "travel", "-d", "travel_scanner", "-Fc"],
                                    stdout=output, stderr=log, timeout=600)
        assert result.returncode == 0 and dump.stat().st_size > 0
        with dump.open("rb") as input_file:
            run(["docker", "exec", "-i", "travel_scanner-postgres-1", "pg_restore", "--list"], stdin=input_file)
        state["backup"] = {"path": str(dump), "bytes": dump.stat().st_size, "sha256": digest(dump),
                           "index_verified": True, "mode": oct(dump.stat().st_mode & 0o777)}
        save(state)
        say("BACKUP_VERIFIED " + json.dumps(state["backup"]))
        compose("up", "-d", "--no-build", "--no-deps", *SERVICES)
        healthy(state["schema"])
        after = containers()
        for service in SERVICES:
            assert after[service]["image"] == state["web_image" if service == "web" else "api_image"]
            assert after[service]["status"] == "running" and after[service]["restarts"] == 0
            assert after[service]["env_hash"] == state["before"][service]["env_hash"]
        for service in ["postgres", "redis"]:
            assert after[service] == state["before"][service]
        verify_runtime_snapshot(state)
        previous_mask = os.umask(0o022)
        try:
            git("merge", "--ff-only", TARGET)
            checkout_advanced = True
        finally:
            os.umask(previous_mask)
        for service in ["api", "web"]:
            run(["docker", "image", "tag", state[service + "_image"], "travel-scanner-" + service + ":local"])
        state.update(after=after, activated_at=now(), ci_run=ci["url"])
        save(state)
        say("DEPLOY_SUCCESS " + TARGET + "; no content import or publication performed")
    except BaseException as exc:
        state.pop("activated_at", None)
        state.pop("after", None)
        state.update(failed_at=now(), error=str(exc), status="rolling_back")
        try:
            save(state)
        except OSError:
            pass  # A full filesystem must not prevent restoring the applications.
        try:
            say("Activation failed; restoring retained application images")
        except OSError:
            pass  # A lost output connection must not prevent rollback.
        try:
            if stopped:
                compose("up", "-d", "--no-build", "--no-deps", *SERVICES, tag=state["rollback_tag"])
                healthy(state["schema"])
                restored = containers()
                for service in SERVICES:
                    assert restored[service]["image"] == state["before"][service]["image"]
                    assert restored[service]["env_hash"] == state["before"][service]["env_hash"]
                if checkout_advanced:
                    assert git("rev-parse", "HEAD") == TARGET and not git("status", "--porcelain")
                    # This checkout was verified clean immediately before our own fast-forward.
                    git("reset", "--hard", state["previous"])
                for service in ["api", "web"]:
                    run(["docker", "image", "tag", state["before"][service]["image"], "travel-scanner-" + service + ":local"])
            state.update(status="rolled_back", rollback_status="succeeded")
        except BaseException as rollback_error:
            state.update(status="manual_intervention_required", rollback_status="failed", rollback_error=str(rollback_error))
            try:
                save(state)
            except OSError:
                pass
            raise RuntimeError("Activation and rollback failed; manual intervention required") from rollback_error
        save(state)
        raise
