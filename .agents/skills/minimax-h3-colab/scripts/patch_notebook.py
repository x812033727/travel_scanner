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

Every replacement must match exactly once, or already be applied; anything else means the
upstream notebook changed and the script stops with exit 2 instead of guessing. bootstrap.sh
restores the pristine notebook (git checkout) before calling this, so re-running is safe.

  patch_notebook.py [--notebook PATH] [--profile smooth|hero|draft] [--dry-run]
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

UPSTREAM = {
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


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--notebook", default=None, help="path of the cloned upstream notebook")
    parser.add_argument("--profile", default=None, help="smooth (default), hero or draft; H3_PROFILE otherwise")
    parser.add_argument("--dry-run", action="store_true", help="print the diff, write nothing")
    args = parser.parse_args(argv)

    env = os.environ
    home = Path(env.get("MINIMAX_H3_COLAB_HOME") or Path.home() / ".cache" / "minimax-h3-colab-skill")
    path = Path(args.notebook) if args.notebook else home / "assets" / "MiniMax_H3_Turbo_Colab.ipynb"
    if not path.is_file():
        fail(f"notebook not found at {path}; run bootstrap.sh install first")
    profile = (args.profile or env.get("H3_PROFILE") or "smooth").strip().lower()
    chosen = settings(profile, env)

    before = path.read_text(encoding="utf-8")
    notebook = json.loads(before)
    applied, already = apply(notebook, chosen)
    after = json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"

    if args.dry_run:
        sys.stdout.writelines(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True), str(path), f"{path} ({profile})"))
    elif applied:
        path.write_text(after, encoding="utf-8")
    summary = (
        f"profile={profile} ref=({chosen['ref_repo'] or 'Comfy-Org/MiniMax-H3'} {Path(chosen['ref_file']).name}, {int(chosen['ref_steps'])} steps) "
        f"ff=({chosen['ff_repo']} {Path(chosen['ff_file']).name}, {int(chosen['ff_steps'])} steps) "
        f"lora_strength={float(chosen['strength']):g} sampler={chosen['sampler']}/{chosen['scheduler']}"
    )
    state = "dry run" if args.dry_run else ("patched " + ", ".join(applied) if applied else "already applied")
    if already and applied:
        state += f" (already: {', '.join(already)})"
    print(f"[patch_notebook] {state}: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
