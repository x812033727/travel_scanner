---
id: 2026-10-22-verify-c07-corrected-trouser-hem-attribution
title: Verify C07 corrected trouser hem attribution
status: done
priority: P2
area: docs
owner: codex-c07-v9-source-review
claimed_at: 2026-10-22T13:49:44Z
created_at: 2026-10-22T13:49:41Z
completed_at: 2026-10-22T13:50:28Z
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review-v9.md
  - tasks/open/2026-10-22-verify-c07-corrected-trouser-hem-attribution.md
  - tasks/done/2026-10-22-verify-c07-corrected-trouser-hem-attribution.md
---

# Verify C07 corrected trouser hem attribution

## Why

The independent v8 source review held a precise attribution error: A1 describes jeans with cut-off legs, while the script and visual plan depicted turned-up hems. The author corrected three script rows, four visual rows, and one source-note paragraph. This new-hash delta needs independent review before the source gate can pass.

## Definition of done

- [x] Check every changed claim and image instruction against Crucq A1 and adjacent chronology.
- [x] Record a PASS/HOLD decision tied to exact hashes in a separate review receipt.
- [x] Confirm the 77/77 alignment and 64-shot/13-card counts.

## Steps

- [x] Diff the corrected author files against the v8 HOLD version and read the A1 article directly.
- [x] Recheck adjacent `c070102`, `c070103`, `c070404`, and `c070612` narration and visual pairs; verify no turned-up hem remains.
- [x] Save the new-hash receipt without editing author files.

## How to verify

`git diff 984654f10 44d0b9715 -- docs/videos/story-everyday-dr-martens-c07/{script.md,visual-plan.md,script-source-notes.md}`; `Get-FileHash` on those three files; enumerate `c######` table IDs and `shot`/`stats` rows; search the three files for `反摺`; read A1 directly at the URL cited in the receipt.

## Notes

PASS on the narrow correction. A1's direct wording is “jeans with cut-off legs or starched trousers” and “carefully polished Dr. Martens boots,” in its account of late-1960s skinheads. The new wording says 裁短 and depicts anonymous wearers with model-unspecified boots. The prior v8 PASS rows are unchanged; the review receipt defines the resulting scope and limits. No paid generation, merge, or upload was performed.
