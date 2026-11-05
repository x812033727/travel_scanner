#!/usr/bin/env python3
"""Regenerate models.lock: every model the pod may load, at a fixed Hugging Face revision.

Reads the revision, size and LFS sha256 from the Hub's own API, so a re-pin is one command and a
reviewed diff. The weights chosen are the ones the Colab route measured (three-stage.md): INT8
ConvRot H3 on CUDA 13, the four LoRAs the three sampling profiles name, Qwen-Image-Edit-2509,
and SeedVR2 7B with its VAE.

  make_lock.py > models.lock
"""
from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request

WANTED = {
    "Comfy-Org/MiniMax-H3": [
        ("diffusion_models", "diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors"),
        ("diffusion_models", "diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors"),
        ("text_encoders", "text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors"),
        ("vae", "vae/minimax_h3_video_vae_fp16.safetensors"),
        ("vae", "vae/minimax_h3_video_vae_int8_convrot.safetensors"),
        ("vae", "vae/minimax_h3_audio_vae_fp32.safetensors"),
        ("loras", "loras/minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors"),
        ("loras", "loras/minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors"),
    ],
    "lightx2v/Minimax-h3-Turbo": [
        ("loras", "minimax_h3_ref2v_turbo_8step_v1.0_768p_comfyui_bf16.safetensors"),
    ],
    "drbaph/MiniMax-H3-Turbo-Lora-ComfyUI": [
        ("loras", "minimax_h3_turbo_v4_step600_ema_pruned_comfyui.safetensors"),
    ],
    "Comfy-Org/Qwen-Image-Edit": [
        ("diffusion_models", "split_files/diffusion_models/qwen_image_edit_2509_fp8_e4m3fn.safetensors"),
    ],
    "Comfy-Org/Qwen-Image": [
        ("text_encoders", "split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors"),
        ("vae", "split_files/vae/qwen_image_vae.safetensors"),
    ],
    "lightx2v/Qwen-Image-Lightning": [
        ("loras", "Qwen-Image-Edit-2509/Qwen-Image-Edit-2509-Lightning-8steps-V1.0-bf16.safetensors"),
    ],
    "numz/SeedVR2_comfyUI": [
        ("SEEDVR2", "seedvr2_ema_7b_fp16.safetensors"),
        ("SEEDVR2", "ema_vae_fp16.safetensors"),
    ],
}
TIMEOUT_SECONDS = 60
USER_AGENT = "mokaair-runpod-lock/1.0 (support@mokaair.com)"


def api(url: str, data: bytes | None = None) -> object:
    headers = {"User-Agent": USER_AGENT}
    if data is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    request = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return json.load(response)


def entries(repo: str, files: list[tuple[str, str]]) -> list[dict]:
    revision = api(f"https://huggingface.co/api/models/{repo}")["sha"]
    body = urllib.parse.urlencode([("paths", path) for _, path in files] + [("expand", "true")]).encode()
    found = {item["path"]: item for item in api(f"https://huggingface.co/api/models/{repo}/paths-info/{revision}", body)}
    result = []
    for folder, path in files:
        item = found.get(path)
        if item is None or not item.get("lfs"):
            raise SystemExit(f"{repo}: {path} is not an LFS file at {revision}")
        lfs = item["lfs"]
        result.append({
            "repo": repo,
            "revision": revision,
            "path": path,
            "folder": folder,
            "size": item["size"],
            "sha256": lfs.get("oid") or lfs["sha256"],
        })
    return result


def main() -> int:
    files = [entry for repo, wanted in WANTED.items() for entry in entries(repo, wanted)]
    json.dump({"files": files}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
