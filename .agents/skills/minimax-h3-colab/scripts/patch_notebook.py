#!/usr/bin/env python3
"""Apply a sampling profile to the upstream MiniMax H3 Colab notebook.

The upstream notebook (killkli/minimax-h3-colab-skill, pinned in bootstrap.sh) hard-codes the
Turbo LoRAs and step counts: Ref2VA runs the 4-step `ref2v_turbo_4step_v0.1` LoRA, which the
ComfyUI H3 guide says can barely apply the references (pose and face drift), and both modes
sample with euler + beta. This script rewrites those constants in place, by exact string
replacement, so the graph itself stays upstream's:

  smooth  (default) Ref2VA: lightx2v 8-step 768p Ref2V v1.0 LoRA, 8 steps; FL2VA: the official
                    Comfy-Org 8-step FL2V v1.0 LoRA, 8 steps; euler + simple (the LoRA cards'
                    recommendation). Motion and reference adherence over speed.
  hero              no LoRA effect (strength 0), 20 steps, res_multistep + simple: the official
                    ComfyUI template's base-model settings. About three times slower; for the
                    identity and beauty shots.
  draft             upstream unchanged (4-step Ref2VA, drbaph v4 FL2VA, euler + beta).

Two more replacements apply for every profile: the canvas cap. Upstream asserts
WIDTH * HEIGHT <= 1344 * 768 (the official canvas), but a 2026-10-28 run on an A100 proved
ComfyUI takes 1920x1088 in both modes (sharper, faces kept), so the notebook's assert and the
runner's MAX_PIXELS become 1920 * 1088 (CANVAS below), the runner's error text names it, and
the runner passes each job's area to the notebook as H3_FIRST_FRAME_MEGAPIXELS so a
first_frame job scales its frame to its own canvas instead of the hard-coded 0.98 MP.

Every replacement must match exactly once, or already be applied; anything else means the
upstream notebook or runner changed and the script stops with exit 2 instead of guessing.
bootstrap.sh restores the pristine files (git checkout) before calling this, so re-running is
safe, and a second run on patched files reports "already applied".

  patch_notebook.py [--notebook PATH] [--runner PATH] [--profile smooth|hero|draft] [--dry-run]
  environment: H3_PROFILE, H3_REF_LORA_REPO, H3_REF_LORA_FILE, H3_FF_LORA_REPO, H3_FF_LORA_FILE,
               H3_REF_STEPS, H3_FF_STEPS, H3_SAMPLER, H3_SCHEDULER, H3_LORA_STRENGTH,
               MINIMAX_H3_COLAB_HOME (default ~/.cache/minimax-h3-colab-skill)
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import sys
from pathlib import Path


def fail(message: str, code: int = 2) -> None:
    print(f"[patch_notebook] {message}", file=sys.stderr)
    sys.exit(code)

# Width x height both modes accept on an A100 (2026-10-28); multiples of 32 as H3 wants.
CANVAS = (1920, 1088)

UPSTREAM = {
    "canvas": 'assert WIDTH * HEIGHT <= 1344 * 768, "輸出尺寸總面積不可超過官方 1344×768 畫布上限。"',
    "first_frame_mp": "FIRST_FRAME_MEGAPIXELS = 0.98",
    "steps": 'STEPS = 4 if INFERENCE_MODE == "reference" else 8',
    "ref_repo": "LORA_REPO = BASE_REPO",
    "ref_file": 'LORA_REMOTE = "loras/minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors"',
    "ff_repo": 'LORA_REPO = "drbaph/MiniMax-H3-Turbo-Lora-ComfyUI"',
    "ff_file": 'LORA_REMOTE = "minimax_h3_turbo_v4_step600_ema_pruned_comfyui.safetensors"',
    "strength": "LORA_STRENGTH = 1.0",
    "sampler": 'SAMPLER_NAME = "euler"',
    "scheduler": 'SCHEDULER_NAME = "beta"',
}

PROFILES = {
    "smooth": {
        "ref_steps": 8,
        "ff_steps": 8,
        "ref_repo": "lightx2v/Minimax-h3-Turbo",
        "ref_file": "minimax_h3_ref2v_turbo_8step_v1.0_768p_comfyui_bf16.safetensors",
        "ff_repo": "Comfy-Org/MiniMax-H3",
        "ff_file": "loras/minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors",
        "strength": 1.0,
        "sampler": "euler",
        "scheduler": "simple",
    },
    "hero": {
        "ref_steps": 20,
        "ff_steps": 20,
        "ref_repo": "lightx2v/Minimax-h3-Turbo",
        "ref_file": "minimax_h3_ref2v_turbo_8step_v1.0_768p_comfyui_bf16.safetensors",
        "ff_repo": "Comfy-Org/MiniMax-H3",
        "ff_file": "loras/minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors",
        "strength": 0.0,
        "sampler": "res_multistep",
        "scheduler": "simple",
    },
    "draft": {
        "ref_steps": 4,
        "ff_steps": 8,
        "ref_repo": None,  # keep upstream's `LORA_REPO = BASE_REPO`
        "ref_file": "loras/minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors",
        "ff_repo": "drbaph/MiniMax-H3-Turbo-Lora-ComfyUI",
        "ff_file": "minimax_h3_turbo_v4_step600_ema_pruned_comfyui.safetensors",
        "strength": 1.0,
        "sampler": "euler",
        "scheduler": "beta",
    },
}

ENV_OVERRIDES = {
    "H3_REF_LORA_REPO": ("ref_repo", str),
    "H3_REF_LORA_FILE": ("ref_file", str),
    "H3_FF_LORA_REPO": ("ff_repo", str),
    "H3_FF_LORA_FILE": ("ff_file", str),
    "H3_REF_STEPS": ("ref_steps", int),
    "H3_FF_STEPS": ("ff_steps", int),
    "H3_SAMPLER": ("sampler", str),
    "H3_SCHEDULER": ("scheduler", str),
    "H3_LORA_STRENGTH": ("strength", float),
}


def settings(profile: str, env: dict[str, str]) -> dict:
    if profile not in PROFILES:
        fail(f"unknown profile {profile!r}; use one of {', '.join(PROFILES)}")
    chosen = dict(PROFILES[profile])
    for name, (key, kind) in ENV_OVERRIDES.items():
        raw = env.get(name, "").strip()
        if not raw:
            continue
        try:
            chosen[key] = kind(raw)
        except ValueError:
            fail(f"{name}={raw!r} is not a {kind.__name__}")
    for key in ("ref_steps", "ff_steps"):
        if not 1 <= int(chosen[key]) <= 100:
            fail(f"{key} must be 1..100, got {chosen[key]}")
    if not 0.0 <= float(chosen["strength"]) <= 2.0:
        fail(f"LoRA strength must be 0..2, got {chosen['strength']}")
    for key in ("sampler", "scheduler", "ref_file", "ff_file", "ff_repo"):
        value = chosen[key]
        if not isinstance(value, str) or not value or '"' in value or "\n" in value:
            fail(f"{key} must be a plain non-empty string, got {value!r}")
    if chosen["ref_repo"] is not None and ('"' in chosen["ref_repo"] or not chosen["ref_repo"]):
        fail(f"ref_repo must be a plain non-empty string, got {chosen['ref_repo']!r}")
    return chosen


def replacements(chosen: dict) -> list[tuple[str, str, str]]:
    """(key, upstream text, replacement text); a replacement equal to upstream is a no-op."""
    ref_repo = "LORA_REPO = BASE_REPO" if chosen["ref_repo"] is None else f'LORA_REPO = "{chosen["ref_repo"]}"'
    return [
        ("steps", UPSTREAM["steps"], f'STEPS = {int(chosen["ref_steps"])} if INFERENCE_MODE == "reference" else {int(chosen["ff_steps"])}'),
        ("ref_repo", UPSTREAM["ref_repo"], ref_repo),
        ("ref_file", UPSTREAM["ref_file"], f'LORA_REMOTE = "{chosen["ref_file"]}"'),
        ("ff_repo", UPSTREAM["ff_repo"], f'LORA_REPO = "{chosen["ff_repo"]}"'),
        ("ff_file", UPSTREAM["ff_file"], f'LORA_REMOTE = "{chosen["ff_file"]}"'),
        ("strength", UPSTREAM["strength"], f'LORA_STRENGTH = {float(chosen["strength"]):g}'),
        ("sampler", UPSTREAM["sampler"], f'SAMPLER_NAME = "{chosen["sampler"]}"'),
        ("scheduler", UPSTREAM["scheduler"], f'SCHEDULER_NAME = "{chosen["scheduler"]}"'),
        # profile-independent: the canvas cap and the first-frame scale that follows the job's canvas
        ("canvas", UPSTREAM["canvas"], f'assert WIDTH * HEIGHT <= {CANVAS[0]} * {CANVAS[1]}, "輸出尺寸總面積不可超過 {CANVAS[0]}×{CANVAS[1]}（實測 A100 可跑；官方建議畫布 1344×768）。"'),
        ("first_frame_mp", UPSTREAM["first_frame_mp"], 'FIRST_FRAME_MEGAPIXELS = float(os.environ.get("H3_FIRST_FRAME_MEGAPIXELS", "0.98"))'),
    ]


# The upstream runner (scripts/runner.py) checks the same cap before uploading anything and
# does not tell the notebook how large the first frame should be; exact lines, same rule.
RUNNER_TIMEOUT_LINE = '                "H3_JOB_TIMEOUT_SECONDS=" + str(min(exec_timeout, 7200)),\n'
RUNNER_REPLACEMENTS: list[tuple[str, str, str]] = [
    ("max_pixels", "MAX_PIXELS = DEFAULT_WIDTH * DEFAULT_HEIGHT", f"MAX_PIXELS = {CANVAS[0]} * {CANVAS[1]}"),
    (
        "max_pixels_message",
        'f"{label} dimensions may not exceed {MAX_PIXELS:,} pixels (1344×768)."',
        f'f"{{label}} dimensions may not exceed {{MAX_PIXELS:,}} pixels ({CANVAS[0]}×{CANVAS[1]})."',
    ),
    (
        "first_frame_env",
        RUNNER_TIMEOUT_LINE,
        RUNNER_TIMEOUT_LINE + '                "H3_FIRST_FRAME_MEGAPIXELS=" + str(round(job["width"] * job["height"] / 1e6, 3)),\n',
    ),
]


def cell_text(cell: dict) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else str(source)


def set_cell_text(cell: dict, text: str) -> None:
    cell["source"] = text.splitlines(keepends=True)


def apply(notebook: dict, chosen: dict) -> tuple[list[str], list[str]]:
    """Patch in place; return (applied keys, already-applied keys). Exit 2 on anything odd."""
    code_cells = [c for c in notebook.get("cells", []) if c.get("cell_type") == "code"]
    if not code_cells:
        fail("the notebook has no code cells; is this the upstream MiniMax_H3_Turbo_Colab.ipynb?")
    applied, already = [], []
    for key, old, new in replacements(chosen):
        if old == new:
            continue
        hits = [(i, cell_text(c).count(old)) for i, c in enumerate(code_cells)]
        total = sum(n for _, n in hits)
        if total == 1:
            index = next(i for i, n in hits if n == 1)
            set_cell_text(code_cells[index], cell_text(code_cells[index]).replace(old, new, 1))
            applied.append(key)
        elif total == 0 and sum(cell_text(c).count(new) for c in code_cells) >= 1:
            already.append(key)
        else:
            fail(
                f"expected exactly one `{old}` in the notebook, found {total}: the upstream "
                "notebook changed. Re-pin MINIMAX_H3_UPSTREAM_COMMIT and update UPSTREAM in this script, "
                "or set H3_NOTEBOOK_PATCH=off to run upstream's settings unchanged."
            )
    return applied, already


def apply_runner(text: str) -> tuple[str, list[str], list[str]]:
    """Patch the runner's source; return (text, applied keys, already-applied keys). Exit 2 on drift.

    The env replacement keeps upstream's line and adds one after it, so the replaced text is
    checked for before the upstream text: finding it means the edit is already there.
    """
    applied, already = [], []
    for key, old, new in RUNNER_REPLACEMENTS:
        if text.count(new) == 1:
            already.append(key)
        elif text.count(old) == 1:
            text = text.replace(old, new, 1)
            applied.append(key)
        else:
            fail(
                f"expected exactly one `{old.strip()}` in runner.py, found {text.count(old)}: the upstream "
                "runner changed. Re-pin MINIMAX_H3_UPSTREAM_COMMIT and update RUNNER_REPLACEMENTS in this script, "
                "or set H3_NOTEBOOK_PATCH=off to run upstream unchanged."
            )
    return text, applied, already


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--notebook", default=None, help="path of the cloned upstream notebook")
    parser.add_argument("--runner", default=None, help="path of the cloned upstream runner.py")
    parser.add_argument("--profile", default=None, help="smooth (default), hero or draft; H3_PROFILE otherwise")
    parser.add_argument("--dry-run", action="store_true", help="print the diff, write nothing")
    args = parser.parse_args(argv)

    env = os.environ
    home = Path(env.get("MINIMAX_H3_COLAB_HOME") or Path.home() / ".cache" / "minimax-h3-colab-skill")
    path = Path(args.notebook) if args.notebook else home / "assets" / "MiniMax_H3_Turbo_Colab.ipynb"
    if not path.is_file():
        fail(f"notebook not found at {path}; run bootstrap.sh install first")
    runner_path = Path(args.runner) if args.runner else home / "scripts" / "runner.py"
    if not runner_path.is_file():
        fail(f"runner not found at {runner_path}; run bootstrap.sh install first")
    profile = (args.profile or env.get("H3_PROFILE") or "smooth").strip().lower()
    chosen = settings(profile, env)

    before = path.read_text(encoding="utf-8")
    notebook = json.loads(before)
    applied, already = apply(notebook, chosen)
    after = json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"
    runner_before = runner_path.read_text(encoding="utf-8")
    runner_after, runner_applied, runner_already = apply_runner(runner_before)

    if args.dry_run:
        sys.stdout.writelines(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True), str(path), f"{path} ({profile})"))
        sys.stdout.writelines(difflib.unified_diff(runner_before.splitlines(keepends=True), runner_after.splitlines(keepends=True), str(runner_path), f"{runner_path} (canvas {CANVAS[0]}x{CANVAS[1]})"))
    else:
        if applied:
            path.write_text(after, encoding="utf-8")
        if runner_applied:
            runner_path.write_text(runner_after, encoding="utf-8")
    summary = (
        f"profile={profile} ref=({chosen['ref_repo'] or 'Comfy-Org/MiniMax-H3'} {Path(chosen['ref_file']).name}, {int(chosen['ref_steps'])} steps) "
        f"ff=({chosen['ff_repo']} {Path(chosen['ff_file']).name}, {int(chosen['ff_steps'])} steps) "
        f"lora_strength={float(chosen['strength']):g} sampler={chosen['sampler']}/{chosen['scheduler']} "
        f"canvas={CANVAS[0]}x{CANVAS[1]}"
    )
    if args.dry_run:
        state = "dry run"
    elif not applied and not runner_applied:
        state = "already applied"
    else:
        state = "patched " + ", ".join(applied) if applied else "notebook already applied"
        if already and applied:
            state += f" (already: {', '.join(already)})"
        state += "; runner " + ("patched " + ", ".join(runner_applied) if runner_applied else "already applied")
    print(f"[patch_notebook] {state}: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
