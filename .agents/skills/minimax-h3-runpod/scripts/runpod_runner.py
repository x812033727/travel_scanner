#!/usr/bin/env python3
"""Run H3 clips, Qwen first frames, refines and upscales on a RunPod pod the site starts.

The RunPod key stays on the site: this asks the broker for a pod, beats its heartbeat so the reaper
leaves it alone, talks to the pod's gate with the one-time gate token, and stops the pod when the
work is done unless --keep. A job whose output file exists is skipped, so a rerun pays only for
what is left. Exit codes: 0 done, 1 a job failed or the manifest has errors, 2 usage, 3 refused.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pod_client import open_pod, stop_pod  # noqa: E402
from pod_graphs import clip_graph, image_graph, probe_frames, profiles, refine_graph, upscale_graph  # noqa: E402
from pod_http import JobFailed, RunnerError, broker, clear_state, detail, read_state  # noqa: E402

COLAB_SCRIPTS = Path(__file__).resolve().parents[2] / "minimax-h3-colab" / "scripts"
MAX_CLIPS = 20


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def write_progress(path: Path | None, progress: dict) -> None:
    if path is None:
        return
    progress["updated_at"] = now_iso()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def video_info(outputs: dict) -> dict:
    items = outputs.get("15", {}).get("gifs", [])
    found = next((item for item in items if item["filename"].endswith(".mp4")), None)
    if found is None:
        raise JobFailed(f"ComfyUI returned no MP4: {json.dumps(outputs, ensure_ascii=False)[:500]}")
    return found


def image_info(outputs: dict) -> dict:
    items = outputs.get("42", {}).get("images", [])
    if not items:
        raise JobFailed(f"ComfyUI returned no image: {json.dumps(outputs, ensure_ascii=False)[:500]}")
    return items[0]


def run_one(job, entry, pod, make_graph, pick_output, verify, args, progress) -> None:
    began = time.monotonic()
    entry.update({"status": "uploading", "started_at": now_iso()})
    write_progress(args.progress, progress)
    graph = make_graph(job, pod, f"h3r_{uuid.uuid4().hex[:10]}")
    entry["status"] = "generating"
    write_progress(args.progress, progress)
    outputs = pod.wait(pod.submit(graph))
    entry["status"] = "downloading"
    write_progress(args.progress, progress)
    pod.download(pick_output(outputs), job["_output"])
    if verify:
        verify(job)
    entry.update({"status": "completed", "finished_at": now_iso(), "seconds": round(time.monotonic() - began, 1), "bytes": job["_output"].stat().st_size})
    if "_seed" in job:
        entry["seed"] = job["_seed"]
    if "_profile" in job:
        entry["profile"] = job["_profile"]
    print(f"[h3r] {job['id']}: done in {entry['seconds']} s", flush=True)


def run_jobs(args, task: str, jobs: list[dict], make_graph, pick_output, verify=None) -> int:
    entries = [{"id": job["id"], "status": "queued", "output": str(job["_output"])} for job in jobs]
    progress = {"task": task, "status": "starting", "started_at": now_iso(), "jobs": entries}
    todo = []
    for job, entry in zip(jobs, entries):
        if job["_output"].is_file() and job["_output"].stat().st_size > 0:
            entry["status"] = "skipped_exists"
        else:
            todo.append((job, entry))
    write_progress(args.progress, progress)
    if not todo:
        progress["status"] = "completed"
        write_progress(args.progress, progress)
        print("[h3r] every output already exists; no pod started", flush=True)
        return 0
    pod, started = open_pod(args.label, args.slug)
    pod.start_beating()
    failed = 0
    fatal = None
    try:
        progress.update({"status": "waiting_for_pod", "pod_id": pod.state["pod_id"], "session_id": pod.state["session_id"]})
        write_progress(args.progress, progress)
        pod.wait_ready()
        progress["status"] = "running"
        for job, entry in todo:
            try:
                run_one(job, entry, pod, make_graph, pick_output, verify, args, progress)
            except JobFailed as exc:
                failed += 1
                entry.update({"status": "failed", "finished_at": now_iso(), "error": str(exc)})
                print(f"[h3r] {job['id']}: {exc}", file=sys.stderr, flush=True)
            write_progress(args.progress, progress)
    except RunnerError as exc:
        fatal = exc
    finally:
        pod.stop_beating()
        if args.keep or not started:
            print(f"[h3r] pod {pod.state['pod_id']} left running: it is billing until `stop`", flush=True)
        else:
            try:
                view = stop_pod(pod.site, pod.state["session_id"])
                clear_state()
                progress["usd"] = view.get("usd")
                print(f"[h3r] pod stopped; cost US${view.get('usd')}", flush=True)
            except (RunnerError, OSError) as exc:
                fatal = fatal or RunnerError(str(exc))
        progress["status"] = "failed" if fatal or failed else "completed"
        if fatal:
            progress["error"] = str(fatal)
        write_progress(args.progress, progress)
    if fatal:
        raise fatal
    return 1 if failed else 0


def run_checker(script: str, *arguments: str) -> int:
    return subprocess.run([sys.executable, "-I", str(COLAB_SCRIPTS / script), *arguments], check=False).returncode


def load_jobs(manifest: Path, output_dir: Path, suffix: str) -> list[dict]:
    jobs = json.loads(manifest.read_text(encoding="utf-8"))["jobs"]
    for job in jobs:
        job["_output"] = output_dir / str(job.get("output_name") or f"{job['id']}{suffix}")
    return jobs


def cmd_batch(args) -> int:
    if not args.no_check and run_checker("check_manifest.py", str(args.manifest)) != 0:
        return 1
    known = profiles()
    asked = (args.profile or os.environ.get("H3_PROFILE") or "").strip().lower()
    if asked and asked not in known:
        print(f"[h3r] unknown profile {asked!r}; use one of {', '.join(known)}", file=sys.stderr)
        return 2
    base = args.manifest.resolve().parent
    jobs = load_jobs(args.manifest, args.output_dir, ".mp4")

    def make_graph(job: dict, pod, prefix: str) -> dict:
        # Asked for by name, else the admin card's default, which the site sends with the pod.
        name = asked or pod.state.get("default_profile") or "smooth"
        if name not in known:
            raise RunnerError(f"the site's default profile {name!r} is not one of {', '.join(known)}")
        job["_profile"] = name
        return clip_graph(job, base, pod, known[name], prefix)

    return run_jobs(args, "batch", jobs, make_graph, video_info)


def cmd_single(args) -> int:
    job = {
        "id": args.output.stem,
        "inference_mode": args.mode,
        "reference_images": [str(Path(image).resolve()) for image in args.image],
        "prompt_file": str(args.prompt.resolve()),
        "duration_seconds": args.seconds,
        "output_name": args.output.name,
    }
    if args.seed is not None:
        job["seed"] = args.seed
    if args.width and args.height:
        job.update({"width": args.width, "height": args.height})
    with tempfile.TemporaryDirectory(prefix="h3r-") as folder:
        manifest = Path(folder) / "jobs.json"
        manifest.write_text(json.dumps({"jobs": [job]}), encoding="utf-8")
        args.manifest, args.output_dir, args.no_check = manifest, args.output.parent, False
        return cmd_batch(args)


def cmd_images(args) -> int:
    if run_checker("check_images_manifest.py", str(args.manifest)) != 0:
        return 1
    base = args.manifest.resolve().parent
    jobs = load_jobs(args.manifest, args.output_dir, ".png")
    return run_jobs(args, "images", jobs, lambda job, pod, prefix: image_graph(job, base, pod, prefix), image_info)


def cmd_refine(args) -> int:
    if run_checker("refine.py", "--manifest", str(args.manifest), "--check") != 0:
        return 1
    base = args.manifest.resolve().parent
    jobs = load_jobs(args.manifest, args.output_dir, ".mp4")
    return run_jobs(args, "refine", jobs, lambda job, pod, prefix: refine_graph(job, base, pod, prefix), video_info)


def cmd_upscale(args) -> int:
    clips = [Path(path).resolve() for path in args.inputs]
    if args.input_dir:
        clips += sorted(path.resolve() for path in args.input_dir.glob("*.mp4"))
    if not 1 <= len(clips) <= MAX_CLIPS:
        print(f"[h3r] upscale takes 1-{MAX_CLIPS} clips, got {len(clips)}", file=sys.stderr)
        return 1
    jobs = [{"id": clip.stem, "input_video": str(clip), "_output": args.output_dir / f"{clip.stem}_1080.mp4"} for clip in clips]

    def verify(job: dict) -> None:
        expected, produced = probe_frames(Path(job["input_video"])), probe_frames(job["_output"])
        if expected is not None and produced != expected:
            job["_output"].unlink(missing_ok=True)
            raise JobFailed(f"{expected} frames in, {produced} out; SeedVR2 must keep the frame count")

    return run_jobs(args, "upscale", jobs, lambda job, pod, prefix: upscale_graph(job, pod, prefix), video_info, verify)


def cmd_check(args) -> int:
    return run_checker("check_manifest.py", str(args.manifest))


def cmd_usage(args) -> int:
    site = broker()
    status, routes = site.json("GET", "/api/video/gpu-routes?canvas=1088p&upscale=true")
    print(json.dumps(routes, ensure_ascii=False, indent=2))
    if status != 200:
        return 3
    status, running = site.json("GET", "/api/video/runpod/pods")
    print(json.dumps({"running": running if status == 200 else detail(running)}, ensure_ascii=False, indent=2))
    return 0


def cmd_start(args) -> int:
    pod, _ = open_pod(args.label, args.slug)
    pod.start_beating()
    try:
        pod.wait_ready()
    finally:
        pod.stop_beating()
    print(f"[h3r] pod {pod.state['pod_id']} is up and billing; without a heartbeat the reaper stops it when idle")
    return 0


def cmd_stop(args) -> int:
    state = read_state()
    session = args.session or (state or {}).get("session_id")
    if not session:
        print("[h3r] no session on this computer; pass --session <id>", file=sys.stderr)
        return 2
    view = stop_pod(broker(), session)
    if state and state.get("session_id") == session:
        clear_state()
    print(f"[h3r] stopped ({view.get('stop_reason')}); cost US${view.get('usd')}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    top = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    commands = top.add_subparsers(dest="command", required=True)

    def add(name: str, handler, work: bool = False) -> argparse.ArgumentParser:
        sub = commands.add_parser(name)
        sub.set_defaults(handler=handler)
        if work:
            sub.add_argument("--label", default=f"h3r {name}")
            sub.add_argument("--slug")
            sub.add_argument("--keep", action="store_true", help="leave the pod running afterwards")
            sub.add_argument("--progress", type=Path)
        return sub

    add("usage", cmd_usage)
    add("check", cmd_check).add_argument("--manifest", type=Path, required=True)
    batch = add("batch", cmd_batch, True)
    batch.add_argument("--manifest", type=Path, required=True)
    batch.add_argument("--output-dir", type=Path, required=True)
    batch.add_argument("--profile")
    batch.add_argument("--no-check", action="store_true")
    single = add("single", cmd_single, True)
    single.add_argument("--mode", choices=["first_frame", "reference"], default="first_frame")
    single.add_argument("--image", action="append", required=True)
    single.add_argument("--prompt", type=Path, required=True)
    single.add_argument("--output", type=Path, required=True)
    single.add_argument("--seconds", type=float, default=6.0)
    single.add_argument("--width", type=int)
    single.add_argument("--height", type=int)
    single.add_argument("--seed", type=int)
    single.add_argument("--profile")
    for name, handler in (("images", cmd_images), ("refine", cmd_refine)):
        sub = add(name, handler, True)
        sub.add_argument("--manifest", type=Path, required=True)
        sub.add_argument("--output-dir", type=Path, required=True)
    upscale = add("upscale", cmd_upscale, True)
    upscale.add_argument("inputs", nargs="*")
    upscale.add_argument("--input-dir", type=Path)
    upscale.add_argument("--output-dir", type=Path, required=True)
    start = add("start", cmd_start)
    start.add_argument("--label", default="h3r start")
    start.add_argument("--slug")
    add("stop", cmd_stop).add_argument("--session")
    return top


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.handler(args)
    except RunnerError as exc:
        print(f"[h3r] {exc}", file=sys.stderr)
        return 3
    except (OSError, ValueError, KeyError) as exc:
        print(f"[h3r] {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
