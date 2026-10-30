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
branch:
depends_on:
  - 2026-10-30-h3-colab-three-stage
scope:
  - .agents/skills/minimax-h3-colab/references/three-stage.md
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

- [ ] Refine: Henge 3-step sigmas `0.909375, 0.857143, 0.666667, 0`; `er_sde`.
- [ ] Latent upscaler (LBH-123-AI `minimax_h3_latent_upscaler_3d`, licence to confirm) + 1 step 0.15.
- [ ] SeedVR2 7B fp16 vs 3B; `--latent_noise_scale` if skin turns too photographic.
- [ ] Ref2VA: DMAD 4-step and Pika 6-step vs `smooth` 8-step (licences to confirm).

## How to verify

The receipts (progress.json per batch, CU before and after) are linked from the reference.

## Notes

- Spend needs the owner's go-ahead per batch (skill rule 3).
