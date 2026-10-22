---
id: 2026-10-22-c07-revised-script-source-review
title: Independently review C07 revised script sources
status: done
priority: P2
area: docs
owner: codex-c07-source-reviewer
claimed_at: 2026-10-22T11:44:41Z
created_at: 2026-10-22T11:44:35Z
completed_at: 2026-10-22T11:48:12Z
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review-v2.md
  - tasks/open/2026-10-22-c07-revised-script-source-review.md
  - tasks/done/2026-10-22-c07-revised-script-source-review.md
---

# Independently review C07 revised script sources

## Why

The author revised the 77-sentence C07 script and 77-shot visual plan after an earlier HOLD. A second agent must recheck the actual current files against direct sources and bind the result to both hashes before script approval or any paid step.

## Definition of done

- [x] Reopen the current company, museum and academic sources and assess claim scope independently.
- [x] Record PASS/HOLD for every narration and matching visual ID, plus the exact two SHA-256 hashes and bounded repairs.
- [x] Commit and push the review receipt to the existing draft PR #1680.

## Steps

- [x] Verify date, 1460 versus broad Dr. Martens, workwear, cultural and political claims.
- [x] Check all 77 IDs, visual alignment and non-paid visual constraints.
- [x] Write docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review-v2.md.
- [x] Run task check and diff check, then commit and push.

## How to verify

Recompute SHA-256 of script.md and visual-plan.md; compare to the review receipt. Count the 77 unique narration IDs and their 77 matching visual IDs. Run npm run check:tasks and git diff --check. Read the receipt for each ID and confirm the overall HOLD agrees with the three row-level holds.

## Notes

2026-10-22: Independent direct source reread found no wholesale 1460-versus-brand or political-chronology collapse. The bounded HOLD items are c070105 (design intent for prolonged standing unproven), c070310 (later brand archive could sound like contemporaneous factory ledger), and c070609 (B4 currently links a page without the individual-expression statement; the directly readable company parent page has it). The 77 text visual plans passed source-consistency review; they are not generated images or time-based validation. Script SHA A1BE5CFC53CE24EDEFA95094E4D442F6E86FE6B0B4F8D0E0D7E5BE7CEE510A14; visual SHA 32B854AE849421F14B39B81CC612745B522E9EBFDFEC1FF62AA09EEAE43984CA. No script/visual edit, paid work, merge, upload or publication.
