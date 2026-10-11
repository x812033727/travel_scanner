---
id: 2026-10-11-illustrated-historical-object-judge-blindspots
title: Audit illustrated historical and object-only judge false passes
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-11T20:42:02Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - apps/api/app/video_media/judge.py
---

# Audit illustrated historical and object-only judge false passes

## Why

H02 production found selected images that passed the native judge despite clearly violating object-only or historical scene instructions. Examples include an extra child's head in `h02-find-inference-step`, two mascots and generated text in `h02-close-persons-unknown`, a cat stamp and large generated text in `h02-close-unclosed-file`, and modern equipment on `h02-close-link-life`. Historical clothing and architecture defects are recorded in the episode's visual reviews. The episode uses reviewed source cards to resolve these defects; the shared judge behavior remains unaudited.

## Definition of done

- [ ] Establish a source-bound, independently reviewed baseline of these defects and acceptable minor exceptions using retained original images and verdicts.
- [ ] Verify whether scene-specific questions can detect extra faces, main-surface generated text, modern devices and explicit historical clothing/architecture mismatches without treating generic background details as automatic failures.
- [ ] Preserve native scores, raw takes, paid receipts and manual final-review requirements; do not lower thresholds, rewrite historical `passed` values or judge repeatedly until passing.
- [ ] Bind any changed question/rubric to a new verdict identity, with focused regression checks and an honest held-out result.

## Steps

- [ ] Read `docs/videos/curio-h02/visual-review.md` and `visual-review-late.md`; distinguish selected takes from unused failed takes.
- [ ] Inspect current keyframe question construction and server interpretation before proposing a bounded change.
- [ ] Evaluate the proposed change with the retained source/image hashes and meaningful negative and acceptable-minor cases. Reconcile known paid requests before any separately authorized provider call.

## How to verify

Run the focused keyframe tests with the bundled Node runtime and relevant API tests if server code changes. Record old/new question identities, image SHA-256, unchanged native history and independent human outcomes. Do not use a stage exit code as evidence that the image is visually acceptable.

## Notes

- 2026-10-12: H02's original 86-shot batch is fully retained outside Git. Original source SHA-256 `294227a3e6ee357312f0c9faa2b23f9cbc22e72bad7e2e1edb3fa8e188eb62c2`; claims `6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`; final original manifest `d0c5901857af193f574eb7b07faf2d14fd3afc2c66267e3b5b6f94c959d484c5`. The complete-batch readback and canonical media snapshots are in the episode's external `_audit/`; no credentials belong in this task.
- A small modern storage label `1` in selected `h02-find-other-explanations-2-trim.jpg` was independently considered a minor exception. The watermark in unused seed 3 must not be attributed to selected seed 2. `farewell-newborn` selected seed 1 has closed eyes; an open-eyed unused take must not contaminate its selected-image assessment.
- This ticket is filed for later shared-tool work. H02 production does not change the judge or deploy anything.
