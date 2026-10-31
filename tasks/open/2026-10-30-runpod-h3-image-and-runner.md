---
id: 2026-10-30-runpod-h3-image-and-runner
title: MiniMax H3 on a RunPod RTX 6000 Ada pod: image, models volume, workflows and runner skill
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-30T00:37:21Z
completed_at:
branch:
depends_on:
  - 2026-10-30-runpod-pod-broker
scope:
  - ops/runpod
  - .agents/skills/minimax-h3-runpod
  - .claude/skills/minimax-h3-runpod
  - tools/minimax-h3-runpod.test.mjs
  - .github/workflows/runpod-h3-image.yml
  - tools/video/tts/cli.mjs
  - tools/video/tts/pairing.mjs
  - tools/video/cli.mjs
---

# MiniMax H3 on a RunPod RTX 6000 Ada pod: image, models volume, workflows and runner skill

## Why

The Colab route runs an unlicensed upstream notebook we can only string-patch, downloads ~70 GiB
of models on every cold start, and caps output at 1344×768. On RunPod the repo can own the
ComfyUI image, keep the models on a network volume, and reach 1920×1080.

## Definition of done

- [ ] `ops/runpod/`: a Dockerfile with pinned ComfyUI, the H3 nodes, an upscaler node, and a small
      bearer-token gate (`gate.py`, only `/prompt`, `/history`, `/upload/image`, `/view`, `/health`);
      `fetch_models.sh` + `models.lock` (HF revisions and sha256 for H3, the four LoRAs,
      Qwen-Image-Edit-2509, the upscaler); API-format workflows from Comfy-Org `workflow_templates`
      (`h3_fl2v.json`, `h3_r2v.json`, `qwen_edit.json`, `upscale.json`) and `profiles.json`
      (smooth/hero/draft as node overrides, from `patch_notebook.py`).
- [ ] Shared skill `minimax-h3-runpod` with `scripts/runpod_runner.py` and `scripts/h3r.sh`
      (usage, check, single, batch, images, upscale, start, stop) that starts pods through the
      site broker, keeps a heartbeat, writes `progress.json` like the Colab runner, and always
      stops the pod at the end unless `--keep`.
- [ ] It reuses `check_manifest.py`, `check_images_manifest.py`, `fit_first_frame.sh` and links
      `motion-quality.md` instead of copying them.
- [ ] Offline tests with a fake broker and a fake ComfyUI.
- [ ] Pilot (owner approves spend): three shots (speaking MCU, walking MS, two-person Ref2VA) ×
      {736p smooth + upscale, native 1920×1088 smooth}; record cold start, seconds per clip, VRAM
      peak, USD per clip, frame-0 PSNR, and a blind pick. The result sets `runpod_default_canvas`.

## Steps

- [ ] Image and gate; publish with a digest.
- [ ] Models volume script and lock file.
- [ ] Workflows and profiles.
- [ ] Runner, wrapper, SKILL.md and its `.claude/skills` copy.
- [ ] Tests; pilot; write the measured numbers into the skill.

## How to verify

```bash
node --test tools/minimax-h3-runpod.test.mjs tools/minimax-h3-colab.test.mjs tools/skills.test.mjs
```

## Notes

- First real run 2026-10-31: e033 s08 Ref2VA 960x544 hero on WK, EU-RO-1. Models 19 min, first clip 278.6 s with model load, pod 23.5 min, US$1.01, stopped itself. refine, SeedVR2, Qwen and a cloud-session run are not verified. The owner keeps production on Colab for now (RunPod about 3x the hourly cost on the same card), so this waits; the pilot row above is still open.
- Speed 2026-10-31: e040 Ref2VA hero drafts took 31.65 s a step (633-706 s a clip) at 600 W, against about 5 s a step on Colab G4. Colab uses CUDA 13 and INT8 ConvRot; the first image used CUDA 12.8 and FP8. The image now matches Colab; the measured result goes here.

- Progress 2026-10-31 (uncommitted in worktree `rtx-pro-6000-wl-setup-faf816`): `ops/runpod` image,
  gate, model fetch, lock (15 files, 109.7 GiB) and workflows are written, none of it run yet;
  `runpod_runner.py`, SKILL.md, README and tests are written with offline tests; not run on a real pod. The image workflow
  `.github/workflows/runpod-h3-image.yml` and `login --runpod` were added to the scope. Left: merge, public package, admin card, pilot.
- Feasibility (2026-10-30): only the open-weights H3 runs here, not the MiniMax API or Hailuo web
  H3. 736p fits easily (Colab's 40 GB A100 runs it; Ada has FP8). Native 1088p is unmeasured:
  ~2.1 MP against the 0.97 MP training size, roughly 4–5× the time, possible artefacts.
- Estimated RTX 6000 Ada speed ~0.6× A100: a 6-second 736p clip ~3.5–4 minutes (unmeasured).
- Do not enable Sage Attention (INT8 artefacts, motion-quality.md §5).
- Add the skill to the list in `AGENTS.md` when its scope is free.
