#!/usr/bin/env python3
"""Turn a manifest job into the API-format graph the pod runs (ops/runpod/workflows)."""
from __future__ import annotations

import json
import random
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pod_http import JobFailed  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
RUNPOD = ROOT / "ops" / "runpod"
SHIFT = 12.0  # H3's video flow shift; three-stage.md section 2 says why refine starts from a sigma
COMFY_INPUT = "/opt/ComfyUI/input"


def frames_for(seconds: float) -> int:
    requested = max(5, round(seconds * 24))
    return requested + (5 - requested % 17) % 17


def probe_frames(path: Path) -> int | None:
    if not shutil.which("ffprobe"):
        return None
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, timeout=300, check=True,
        ).stdout.strip()
        return int(out.split(",")[0])
    except (ValueError, subprocess.SubprocessError, OSError):
        return None


def workflow(name: str) -> dict:
    return json.loads((RUNPOD / "workflows" / f"{name}.json").read_text(encoding="utf-8"))


def profiles() -> dict:
    return json.loads((RUNPOD / "profiles.json").read_text(encoding="utf-8"))


def fill(graph: dict, values: dict) -> dict:
    """Replace every "$name" input; a placeholder without a value is a bug, so it stops the job."""
    for node_id, node in graph.items():
        for key, value in node["inputs"].items():
            if isinstance(value, str) and value.startswith("$"):
                name = value[1:]
                if name not in values:
                    raise JobFailed(f"workflow node {node_id} needs {name}")
                node["inputs"][key] = values[name]
    return graph


def resolve(base: Path, value: object) -> Path:
    path = Path(str(value)).expanduser()
    return path if path.is_absolute() else (base / path).resolve()


def text_of(job: dict, base: Path, file_key: str = "prompt_file", key: str = "prompt") -> str:
    if job.get(file_key):
        return resolve(base, job[file_key]).read_text(encoding="utf-8")
    return str(job.get(key) or "")


def pick_seed(job: dict) -> int:
    seed = job.get("seed")
    job["_seed"] = random.SystemRandom().randrange(0, 2**53) if seed in (None, "") else int(seed)
    return job["_seed"]


def clip_graph(job: dict, base: Path, pod, profile: dict, prefix: str) -> dict:
    mode = str(job.get("inference_mode") or "reference")
    width = int(job.get("width") or (1312 if mode == "first_frame" else 1344))
    height = int(job.get("height") or (736 if mode == "first_frame" else 768))
    settings = profile[mode]
    values = {
        "prompt": text_of(job, base),
        "width": width,
        "height": height,
        "frames": frames_for(float(job.get("duration_seconds", 12))),
        "seed": pick_seed(job),
        "lora": settings["lora"],
        "lora_strength": profile["lora_strength"],
        "steps": settings["steps"],
        "sampler": profile["sampler"],
        "scheduler": profile["scheduler"],
        "output_prefix": prefix,
    }
    images = [resolve(base, image) for image in job["reference_images"]]
    if mode == "first_frame":
        values["first_frame"] = pod.upload(images[0])
        values["megapixels"] = round(width * height / 1e6, 3)
        return fill(workflow("h3_fl2v"), values)
    graph = workflow("h3_r2v")
    for index, image in enumerate(images):
        node_id = str(100 + index)
        graph[node_id] = {"class_type": "LoadImage", "inputs": {"image": pod.upload(image)}}
        graph["7"]["inputs"][f"ref_images.ref_image_{index}"] = [node_id, 0]
    return fill(graph, values)


def image_graph(job: dict, base: Path, pod, prefix: str) -> dict:
    if job.get("latent", "empty") != "empty":
        raise JobFailed("latent=image1 is not on the RunPod route yet; use empty")
    graph = workflow("qwen_edit")
    for index, image in enumerate(job["reference_images"], start=1):
        node_id = str(10 + index)
        graph[node_id] = {"class_type": "LoadImage", "inputs": {"image": pod.upload(resolve(base, image))}}
        graph["20"]["inputs"][f"image{index}"] = [node_id, 0]
        graph["21"]["inputs"][f"image{index}"] = [node_id, 0]
    return fill(graph, {
        "prompt": text_of(job, base).strip(),
        "negative": text_of(job, base, "negative_file", "negative").strip(),
        "width": int(job.get("width", 1312)),
        "height": int(job.get("height", 736)),
        "seed": pick_seed(job),
        "output_prefix": prefix,
    })


def refine_sigmas(start: float, steps: int) -> str:
    base = start / (SHIFT + start * (1.0 - SHIFT))
    grid = (base * (1 - index / steps) for index in range(steps + 1))
    return ", ".join(f"{SHIFT * t / (1.0 + (SHIFT - 1.0) * t):.6f}" for t in grid)


def refine_graph(job: dict, base: Path, pod, prefix: str) -> dict:
    if job.get("guide", "none") != "none":
        raise JobFailed("guide=draft is not on the RunPod route; three-stage.md section 5 found it not worth it")
    video = resolve(base, job["input_video"])
    frames = probe_frames(video)
    if frames is None:
        raise JobFailed(f"ffprobe could not count the frames of {video.name}")
    job["_seed"] = int(job.get("seed", 0))
    return fill(workflow("h3_refine"), {
        "input_video": f"{COMFY_INPUT}/{pod.upload(video)}",
        "first_frame": pod.upload(resolve(base, job["first_frame"])),
        "prompt": text_of(job, base),
        "width": int(job.get("width", 1312)),
        "height": int(job.get("height", 736)),
        "frames": frames,
        "seed": job["_seed"],
        "sampler": job.get("sampler", "res_multistep"),
        "sigmas": job.get("sigmas") or refine_sigmas(float(job.get("sigma_start", 0.5)), int(job.get("steps", 10))),
        "output_prefix": prefix,
    })


def upscale_graph(job: dict, pod, prefix: str) -> dict:
    video = pod.upload(Path(job["input_video"]))
    return fill(workflow("upscale"), {"input_video": f"{COMFY_INPUT}/{video}", "output_prefix": prefix})
