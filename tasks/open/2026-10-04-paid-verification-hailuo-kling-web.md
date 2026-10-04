---
id: 2026-10-04-paid-verification-hailuo-kling-web
title: Paid verification of the Hailuo and Kling web numbers the animation skills still mark unverified
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-04T15:44:03Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/animation-preproduction/references/route-decisions.md
  - .agents/skills/animation-production/references/providers-and-plans.md
---

# Paid verification of the Hailuo and Kling web numbers the animation skills still mark unverified

## Why

The animation skills plan every shot's route, seconds and credits from official prices read on
2026-10-04, but several numbers were never charged on the owner's accounts, and image-to-video
from a pipeline keyframe has never been sent on either service. A three-shot pilot on each
service would settle them for a few hundred credits. This needs the owner's approval: it spends
credits on the owner's Hailuo (Max) and Kling accounts.

## Definition of done

- [ ] Each item below is measured on the owner's account (credits shown, balance before and after, output size, fps, time) and written into `.agents/skills/animation-preproduction/references/route-decisions.md` and `.agents/skills/animation-production/references/providers-and-plans.md` with the date, replacing "官方、未實扣" or "未驗".
- [ ] The two pilots' clips are imported with `clips import` and watched at speed (first-frame PSNR, cuts, watermark).

## Steps

Estimated cost (credits; official per-second prices, 2026-10-04):

- [ ] Kling VIDEO 3.0, 1080p, audio off, outputs 1, three shots of 4 s from approved keyframes: about 3 × 32 = 96 credits. Measure the real deduction, output size and fps, whether the web panel has a negative field, AI Prompter's default.
- [ ] Hailuo H3 768P, one 4 s image-to-video shot: 28 credits. Measure credits per second (about 7 is inferred, not an official price), the output size (1344×768 per the self-host guide), and whether 768P upscaled to 1080p is acceptable.
- [ ] Hailuo H3 2K, the same three shots as Kling: about 3 × 48 = 144 credits, for a side-by-side on the same keyframes.
- [ ] Hailuo 2.3 1080p 6 s, one shot: 80 credits (or free in the Max relax queue once credits are used up; measure the wait).
- [ ] A master shot cut three times (`data.source`) on one route: does each cut's frame match and read right.
- [ ] Hailuo H3 with an end frame on the web (whether it is offered for H3).

Total about 350 credits plus retakes.

## How to verify

`clips import` exit 0 for each accepted clip; `run_report.mjs --markdown` lists them with their credits.

## Notes

- Filed from `2026-10-04-animation-preproduction-skill`. Run it through the animation-preproduction lock package and the pilot procedure in `.agents/skills/animation-production/references/browser-production.md`; uploading a local keyframe needs Claude in Chrome's file upload (the in-app browser cannot), with the owner's consent.
