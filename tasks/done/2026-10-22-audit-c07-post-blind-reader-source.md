---
id: 2026-10-22-audit-c07-post-blind-reader-source
title: Audit C07 post blind reader source delta v10
status: done
priority: P2
area: docs
owner: codex-c07-v10-source-delta
claimed_at: 2026-10-22T14:02:29Z
created_at: 2026-10-22T14:02:23Z
completed_at: 2026-10-22T14:08:32Z
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review-v10.md
---

# Audit C07 post blind reader source delta v10

## Why

The C07 author rewrote the 77-row script and visual plan after a blind-reader HOLD. The preceding v9 source PASS binds only the prior three SHA-256 values. The 73-row revision needs its own independent source and ID-alignment receipt before script approval or paid production.

## Definition of done

- [x] Directly read the company product/history pages, museum object record, and scholar article against every changed narration and visual assertion.
- [x] Save a PASS/HOLD receipt bound to all three current SHA-256 values, with exact IDs and bounded repairs.
- [x] Commit and push only this task and its review receipt to draft PR #1680, without modifying the author's three files.

## Steps

- [x] Compare `5ab7d1566` with `651bbb4a3`, including renamed ID uses and deleted rows.
- [x] Check 73 unique script IDs against 73 visual IDs, shot/card totals and card run length.
- [x] Review factual source boundaries and write `script-source-review-v10.md`.
- [x] Run local checks, then push the bounded HOLD to the existing draft branch.

## How to verify

Recompute SHA-256 of `script.md`, `visual-plan.md` and `script-source-notes.md`; compare all three full hashes with the v10 review. Compare rows against `git show 5ab7d1566:<path>`. Run `npm run test:docs-videos`, `npm run check:tasks`, and `git diff --check`. Inspect draft PR #1680 head after push.

## Notes

Review result: bounded HOLD at `c070606–607` because the company's floral customization account does not establish painting or a brush, and at `c070609` because London Museum's 1995 is the boot's production date, not a stated cataloguing/acquisition date. All 22 rewritten narration rows and 10 rewritten visual rows, plus the four corresponding deleted IDs, are covered in the v10 receipt. A1's trouser/boot juxtaposition at `c070407` is acceptable only as anonymous conceptual illustration, not an exact documented hem position. Current hashes: script `D73A820B0A426F8EDDE35F94718A9C440496D90867EB1AA1893B98D3E9B6BE99`; visual `98A8F2A59DEADBF81D323852D6D643985207D5DAC564D43A7AE0463B800E60CC`; notes `95B272D6B1AF9A485419E704F9001E2180CC227919592B616159B45763F9C5EE`. `git diff --cached --check` passed. `npm run check:tasks` failed only because seven unrelated pre-existing untracked `tasks/open` copies duplicate committed `tasks/done` IDs; they were not changed under this scope. `npm run test:docs-videos` progressed through unrelated media tests without a failure, then was stopped because the long suite did not exercise this Markdown-only receipt. No paid generation, author-file edits, owner approval, merge, upload or publication.
