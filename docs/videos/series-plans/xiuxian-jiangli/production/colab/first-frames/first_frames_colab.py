"""Draw first frames on a Colab GPU with Qwen-Image-Edit-2509 (Apache-2.0), one picture per job.

Runs inside the Colab kernel (`colab exec --file`), everything it needs comes through the
environment: FF_BUNDLE (a tar with manifest.json and the reference pictures, uploaded by
ff_runner.py), FF_OUT (the tar to write the pictures into), FF_PROFILE (lightning: the 8-step
Lightning LoRA when Hugging Face has it, else 40 steps; base: 40 steps, true CFG 4.0).

Memory: the transformer alone is ~41 GB in bf16, more than an A100 40 GB holds, so it is loaded
in 8-bit (bitsandbytes) and the pipeline offloads the text encoder and VAE to the CPU between
uses. The first run downloads ~45 GB from Hugging Face; a session keeps it in its cache.
"""
import json
import os
import subprocess
import sys
import tarfile
import time
from pathlib import Path

BUNDLE = Path(os.environ.get("FF_BUNDLE", "/content/ff_bundle.tar"))
OUT_TAR = Path(os.environ.get("FF_OUT", "/content/ff_out.tar"))
PROFILE = os.environ.get("FF_PROFILE", "lightning").strip().lower()
MODEL = os.environ.get("FF_MODEL", "Qwen/Qwen-Image-Edit-2509")
# The Lightning LoRAs for Qwen-Image-Edit-2509 live in the lightx2v/Qwen-Image-Lightning repo, in its
# Qwen-Image-Edit-2509 folder (comfy.org's model page points at the 8-step V1.0 bf16 file there);
# the first run asked a repo of a similar name that answers 401.
LORA_REPO = os.environ.get("FF_LORA_REPO", "lightx2v/Qwen-Image-Lightning")
LORA_FILE = os.environ.get("FF_LORA_FILE", "Qwen-Image-Edit-2509/Qwen-Image-Edit-2509-Lightning-8steps-V1.0-bf16.safetensors")
WORK = Path("/content/ff_work")
OUT_DIR = Path("/content/ff_out")


def log(*parts):
    print("[ff]", *parts, flush=True)


def pip(*packages):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *packages], check=True)


started = time.time()
log("python", sys.version.split()[0], "profile", PROFILE)
pip("diffusers>=0.36.0", "transformers>=4.51", "accelerate>=1.0", "bitsandbytes>=0.45", "huggingface_hub>=0.30", "pillow")

import torch  # noqa: E402
from PIL import Image  # noqa: E402
from diffusers import BitsAndBytesConfig, QwenImageEditPlusPipeline, QwenImageTransformer2DModel  # noqa: E402
from huggingface_hub import list_repo_files  # noqa: E402

log("torch", torch.__version__, "cuda", torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else "-")
WORK.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)
with tarfile.open(BUNDLE) as tar:
    tar.extractall(WORK, filter="data")
manifest = json.loads((WORK / "manifest.json").read_text(encoding="utf-8"))
jobs = manifest["jobs"]
log(len(jobs), "jobs in", BUNDLE)

t0 = time.time()
# An 80 GB card (Colab's A100-SXM4-80GB) holds the whole pipeline in bf16 (~58 GB) and runs it
# on the GPU; a 40 GB card gets the transformer in 8-bit and the rest offloaded to the CPU
# (first run 2026-10-28: 8-bit + offload took 416 s a picture at 40 steps, the slow path).
vram_gb = torch.cuda.get_device_properties(0).total_memory / 2**30 if torch.cuda.is_available() else 0
EIGHT_BIT = os.environ.get("FF_8BIT", "auto").lower()
eight_bit = EIGHT_BIT == "on" or (EIGHT_BIT == "auto" and vram_gb < 70)
if eight_bit:
    transformer = QwenImageTransformer2DModel.from_pretrained(
        MODEL, subfolder="transformer", quantization_config=BitsAndBytesConfig(load_in_8bit=True), torch_dtype=torch.bfloat16
    )
    pipe = QwenImageEditPlusPipeline.from_pretrained(MODEL, transformer=transformer, torch_dtype=torch.bfloat16)
    pipe.enable_model_cpu_offload()
else:
    pipe = QwenImageEditPlusPipeline.from_pretrained(MODEL, torch_dtype=torch.bfloat16)
    pipe.to("cuda")
log("vram", round(vram_gb), "GB", "8-bit" if eight_bit else "bf16 on gpu")
pipe.set_progress_bar_config(disable=True)
log("pipeline loaded in", round(time.time() - t0), "s")

steps, true_cfg, lora = 40, 4.0, None
if PROFILE == "lightning":
    try:
        files = list_repo_files(LORA_REPO)
        edit = [f for f in files if f.endswith(".safetensors") and "edit-2509" in f.lower() and "8step" in f.lower()]
        candidates = [LORA_FILE] if LORA_FILE in files else ([f for f in edit if "bf16" in f.lower()] or edit)
        if candidates:
            lora = sorted(candidates)[-1]
            pipe.load_lora_weights(LORA_REPO, weight_name=lora)
            steps, true_cfg = 8, 1.0
            log("lightning lora", lora)
        else:
            log("no 8-step lora in", LORA_REPO, "- falling back to 40 steps")
    except Exception as exc:  # noqa: BLE001
        log("lora unavailable:", exc, "- falling back to 40 steps")

results = []
for job in jobs:
    t1 = time.time()
    refs = []
    for ref in job.get("references", []):
        img = Image.open(WORK / ref["file"]).convert("RGB")
        refs.append(img)
    if not refs:
        refs = [Image.new("RGB", (job["width"], job["height"]), (90, 96, 104))]
    generator = torch.Generator(device="cpu").manual_seed(int(job.get("seed", 1)))
    try:
        with torch.inference_mode():
            image = pipe(
                image=refs,
                prompt=job["prompt"],
                negative_prompt=job.get("negative") or " ",
                true_cfg_scale=true_cfg,
                num_inference_steps=steps,
                guidance_scale=1.0,
                num_images_per_prompt=1,
                width=job["width"],
                height=job["height"],
                generator=generator,
            ).images[0]
        out = OUT_DIR / job["output_name"]
        image.save(out)
        results.append({"id": job["id"], "status": "completed", "file": job["output_name"], "seconds": round(time.time() - t1, 1), "steps": steps, "true_cfg": true_cfg, "lora": lora, "seed": job.get("seed", 1), "references": len(refs)})
        log(job["id"], "done in", round(time.time() - t1, 1), "s")
    except Exception as exc:  # noqa: BLE001
        results.append({"id": job["id"], "status": "failed", "error": str(exc)[:500], "seconds": round(time.time() - t1, 1)})
        log(job["id"], "FAILED", exc)
        torch.cuda.empty_cache()

(OUT_DIR / "results.json").write_text(json.dumps({"model": MODEL, "profile": PROFILE, "lora": lora, "steps": steps, "eight_bit": eight_bit, "vram_gb": round(vram_gb), "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None, "total_seconds": round(time.time() - started), "results": results}, ensure_ascii=False, indent=1), encoding="utf-8")
with tarfile.open(OUT_TAR, "w") as tar:
    for file in sorted(OUT_DIR.iterdir()):
        tar.add(file, arcname=file.name)
log("wrote", OUT_TAR, "total", round(time.time() - started), "s")
print("COLAB_CLI_OUTPUT_PATH:", OUT_TAR, flush=True)
