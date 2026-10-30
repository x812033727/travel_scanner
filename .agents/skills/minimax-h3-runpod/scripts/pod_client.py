#!/usr/bin/env python3
"""One pod: its heartbeat, its gate, and starting or stopping it through the site's broker."""
from __future__ import annotations

import json
import os
import sys
import threading
import time
import urllib.parse
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pod_http import Http, JobFailed, RunnerError, broker, clear_state, detail, read_state, write_state  # noqa: E402

HEARTBEAT_SECONDS = float(os.environ.get("H3R_HEARTBEAT_SECONDS", "60"))
POLL_SECONDS = float(os.environ.get("H3R_POLL_SECONDS", "5"))
READY_TIMEOUT_SECONDS = float(os.environ.get("H3R_READY_TIMEOUT", "5400"))  # the first pod fetches 110 GiB
JOB_TIMEOUT_SECONDS = float(os.environ.get("H3R_JOB_TIMEOUT", "3600"))
TRANSFER_TIMEOUT_SECONDS = 900
TRANSIENT_POLLS = 12
CRLF = "\r\n"


class Pod:
    def __init__(self, site: Http, state: dict) -> None:
        self.site = site
        self.state = state
        self.gate = Http(state["base_url"], state["gate_token"])
        self.stopped = threading.Event()
        self.stop_reason = ""
        self._beat_stop = threading.Event()
        self._beat = threading.Thread(target=self._heartbeat, daemon=True)

    def _heartbeat(self) -> None:
        path = f"/api/video/runpod/pods/{self.state['session_id']}/heartbeat"
        while not self._beat_stop.wait(HEARTBEAT_SECONDS):
            try:
                status, body = self.site.json("POST", path, {})
            except OSError:
                continue  # a missed beat is fine; the reaper allows for it
            if status == 409:
                self.stop_reason = detail(body)
                self.stopped.set()
                return

    def start_beating(self) -> None:
        self._beat.start()

    def stop_beating(self) -> None:
        self._beat_stop.set()

    def check_alive(self) -> None:
        if self.stopped.is_set():
            raise RunnerError(f"the pod was stopped: {self.stop_reason}")

    def wait_ready(self) -> None:
        deadline = time.monotonic() + READY_TIMEOUT_SECONDS
        last = ""
        while time.monotonic() < deadline:
            self.check_alive()
            try:
                status, body = self.gate.json("GET", "/health", timeout=30)
            except OSError:
                status, body = 0, {"status": "booting"}
            body = body if isinstance(body, dict) else {}
            if status == 200 and body.get("status") == "ready":
                print("[h3r] pod ready", flush=True)
                return
            if status == 401:
                raise RunnerError("the pod's gate refused this gate token")
            if body.get("status") == "failed":
                raise RunnerError(f"the pod could not get ready: {body.get('error')}")
            line = f"{body.get('status', status)} {body.get('index', '')}/{body.get('total', '')} {body.get('file', '')}".strip(" /")
            if line != last:
                print(f"[h3r] pod: {line}", flush=True)
                last = line
            time.sleep(POLL_SECONDS)
        raise RunnerError(f"the pod was not ready after {READY_TIMEOUT_SECONDS:.0f} s")

    def upload(self, path: Path) -> str:
        boundary = uuid.uuid4().hex
        name = f"{uuid.uuid4().hex[:12]}{path.suffix.lower()}"
        head = CRLF.join([
            f"--{boundary}",
            f'Content-Disposition: form-data; name="image"; filename="{name}"',
            "Content-Type: application/octet-stream", "", "",
        ]).encode()
        tail = CRLF.join([
            "", f"--{boundary}", 'Content-Disposition: form-data; name="overwrite"', "", "true", f"--{boundary}--", "",
        ]).encode()
        status, raw = self.gate.request(
            "POST", "/upload/image", head + path.read_bytes() + tail, f"multipart/form-data; boundary={boundary}", TRANSFER_TIMEOUT_SECONDS
        )
        if status != 200:
            raise JobFailed(f"upload of {path.name} failed: HTTP {status} {raw[:200]!r}")
        return json.loads(raw)["name"]

    def submit(self, graph: dict) -> str:
        status, body = self.gate.json("POST", "/prompt", {"prompt": graph, "client_id": "h3r"})
        if status != 200 or body.get("node_errors"):
            raise JobFailed(f"ComfyUI refused the graph: HTTP {status} {json.dumps(body, ensure_ascii=False)[:1500]}")
        return body["prompt_id"]

    def wait(self, prompt_id: str) -> dict:
        deadline = time.monotonic() + JOB_TIMEOUT_SECONDS
        misses = 0
        while time.monotonic() < deadline:
            self.check_alive()
            try:
                status, history = self.gate.json("GET", f"/history/{prompt_id}", timeout=60)
                misses = 0 if status == 200 else misses + 1
            except OSError:
                status, history = 0, {}
                misses += 1
            if misses > TRANSIENT_POLLS:
                raise RunnerError(f"the pod stopped answering (HTTP {status})")
            run = history.get(prompt_id) if isinstance(history, dict) else None
            if run:
                run_status = run.get("status", {})
                if run_status.get("status_str") == "error":
                    raise JobFailed("ComfyUI failed: " + json.dumps(run_status, ensure_ascii=False)[:1500])
                if run.get("outputs") and (run_status.get("completed") or run_status.get("status_str") == "success"):
                    return run["outputs"]
            time.sleep(POLL_SECONDS)
        raise JobFailed(f"no result after {JOB_TIMEOUT_SECONDS:.0f} s; the pod may still be working on {prompt_id}")

    def download(self, info: dict, target: Path) -> None:
        query = urllib.parse.urlencode({"filename": info["filename"], "subfolder": info.get("subfolder", ""), "type": info.get("type", "output")})
        status, raw = self.gate.request("GET", f"/view?{query}", timeout=TRANSFER_TIMEOUT_SECONDS)
        if status != 200 or not raw:
            raise JobFailed(f"download of {info['filename']} failed: HTTP {status}")
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(target.name + ".part")
        temporary.write_bytes(raw)
        temporary.replace(target)


def open_pod(label: str, slug: str | None) -> tuple[Pod, bool]:
    """A pod to work on, and whether this run started it."""
    site = broker()
    state = read_state()
    if state:
        status, view = site.json("GET", f"/api/video/runpod/pods/{state['session_id']}")
        if status == 200 and not view.get("stopped_at"):
            print(f"[h3r] reusing pod {state['pod_id']}", flush=True)
            return Pod(site, state), False
        clear_state()
    status, running = site.json("GET", "/api/video/runpod/pods")
    if status == 403:
        raise RunnerError(detail(running))
    if status == 200 and running:
        raise RunnerError(
            f"pod session {running[0]['session_id']} is running but its gate token is not on this computer "
            "(a start whose answer was lost). Run `stop --session <id>`, then run again."
        )
    status, body = site.json("POST", "/api/video/runpod/pods", {"label": label, **({"slug": slug} if slug else {})})
    if status != 201:
        raise RunnerError(f"the site would not start a pod: HTTP {status} {detail(body)}")
    state = {key: body[key] for key in ("session_id", "pod_id", "base_url", "gate_token")}
    write_state(state)
    print(f"[h3r] started pod {state['pod_id']} at US${body.get('cost_per_hr')}/h; idle stop {body.get('idle_stop_minutes')} min", flush=True)
    return Pod(site, state), True


def stop_pod(site: Http, session_id: str) -> dict:
    status, body = site.json("POST", f"/api/video/runpod/pods/{session_id}/stop", {})
    if status != 200:
        raise RunnerError(f"stop failed: HTTP {status} {detail(body)}. It is still billing: stop it on the admin RunPod card.")
    return body
