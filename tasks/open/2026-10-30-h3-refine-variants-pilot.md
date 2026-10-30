---
id: 2026-10-30-h3-refine-variants-pilot
title: Pilot H3 refine and upscale variants and Ref2VA speed LoRAs on Colab G4
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-30T06:28:37Z
completed_at:
branch: claude/h3-colab-three-stage
depends_on:
  - 2026-10-30-h3-colab-three-stage
scope:
  - .agents/skills/minimax-h3-colab/references/three-stage.md
  - .agents/skills/minimax-h3-colab/scripts/refine.py
  - .agents/skills/minimax-h3-colab/assets/h3_refine.ipynb
  - tools/minimax-h3-colab.test.mjs
---

# Pilot H3 refine and upscale variants and Ref2VA speed LoRAs on Colab G4

## Why

The three-stage pilot (2026-10-30) settled on a 10-step refine from sigma 0.5 and SeedVR2 3B. Henge
and the H3 community offer cheaper or better alternatives nobody here has measured: a 3-step refine
schedule, a learned H3 latent upscaler with one 0.15-denoise step, the `er_sde` sampler, SeedVR2 7B,
and the Ref2VA speed LoRAs (Kijai DMAD 4-step, Pika 6-step).

## Definition of done

- [ ] On the same three e030 shots and seeds, each variant's seconds, CU, frame-0 PSNR and a blind
      pick against the current default are recorded in `references/three-stage.md` §5.
- [ ] The default changes only if a variant wins; the owner sees the side-by-side first.

## Steps

- [ ] First: the whole stage-1 draft as a guide. Chain `MiniMaxH3AddGuide` (core ComfyUI,
      `comfy_extras/nodes_minimax_h3.py`; no extra model) after `MiniMaxH3ImageToVideo` in
      `h3_refine.ipynb` with the stretched draft frames as `image` at `frame_idx` 0, the way Henge
      anchors its refine to the source (`backend/workflows.py`, node 76). Today only frame 0 is
      anchored, which is why sigma 0.7 changed the faces; with every frame guided, try sigma 0.5 and
      0.7 again and see whether the higher start adds detail without the drift.
- [ ] Refine: Henge 3-step sigmas `0.909375, 0.857143, 0.666667, 0`; `er_sde`.
- [ ] Latent upscaler (LBH-123-AI `minimax_h3_latent_upscaler_3d`, licence to confirm) + 1 step 0.15.
- [ ] SeedVR2 7B fp16 vs 3B; `--latent_noise_scale` if skin turns too photographic.
- [ ] Ref2VA: DMAD 4-step and Pika 6-step vs `smooth` 8-step (licences to confirm).

## How to verify

The receipts (progress.json per batch, CU before and after) are linked from the reference.

## Notes

- 2026-10-30 first batch (owner asked to run it): whole-draft guide at sigma 0.5 and 0.7, Henge
  3-step + `er_sde` + guide, and SeedVR2 7B. 9.92 CU in all; table in `references/three-stage.md` §5.
  The guide is 3x slower for little, so the refine default stays. 7B looks better than 3B for
  donghua skin at about the same cost; the owner saw the side-by-side and made 7B the default.
  Not run: the latent upscaler and the Ref2VA speed LoRAs (licences unconfirmed; the LoRAs do not
  apply to our first-frame route).
- Released 2026-10-30: the steps left are the latent upscaler and the Ref2VA speed LoRAs, both waiting on licences.
- Spend needs the owner's go-ahead per batch (skill rule 3).
- Henge's LMS sharpening LoRA uses a fixed "photorealistic" caption and has no stated licence;
  leave it and its refiner LoRA out until both are cleared and checked not to push donghua toward
  live action (the owner agreed, 2026-10-30).
- `MiniMaxH3AddGuide` crops multi-frame guides to 17k+5 frames, so the draft's 124/158 frames fit
  as they are; it may need `vae` (video VAE) connected.
