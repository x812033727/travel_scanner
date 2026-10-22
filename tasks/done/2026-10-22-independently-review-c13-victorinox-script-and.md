---
id: 2026-10-22-independently-review-c13-victorinox-script-and
title: Independently review C13 Victorinox script and visuals
status: done
priority: P2
area: docs
owner: codex-c13-script-independent-review
claimed_at: 2026-10-22T17:35:51Z
created_at: 2026-10-22T17:35:41Z
completed_at: 2026-10-22T17:40:24Z
branch: codex/brand-story-victorinox-c13-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-victorinox-c13/reviews/independent-script-visual-review.md
---

# Independently review C13 Victorinox script and visuals

## Why

The adopted C13 Victorinox Treatment has an author-written 75-line narration and 75-shot visual plan on draft PR #1693. A separate reviewer must reopen the original sources, check every line and prompt, and leave a hash-bound PASS/HOLD receipt before any script adoption or paid media work.

## Definition of done

- [x] An independent receipt binds the exact Treatment, source matrix, script, source notes, visual MD/JSON hashes and reviewed PR head.
- [x] The receipt audits all 75 narration lines and paired shots, identifies corrections and makes its production boundary explicit.

## Steps

- [x] Read the repository and matching brand-story, story-writing, visual and task-board rules; claim only this review receipt path.
- [x] Reopen official Victorinox history, SABI SEC filings, Swissinfo reports and CEO interviews; record TSA direct-fetch limit for unused S8.
- [x] Independently compare all 75 source-tagged lines with all 75 visual entries and recompute mechanical counts.
- [x] Write a separate HOLD receipt and leave author content untouched.

## How to verify

`Get-FileHash` on the six authored files must match the receipt; parse `visual-plan.json` and compare its ordered IDs to `script.md` IDs; `git diff --cached --check` must pass after staging only this task and receipt. Read back draft PR #1693 after push. `npm run check:tasks` is expected to report two pre-existing untracked duplicate open/done C13 treatment task IDs; do not alter those ghost files.

## Notes

Reviewer `codex-c13-script-independent-review`, same draft branch as author but exact receipt-file scope. Claim used `--force` only because the author task claims the parent C13 directory. The two pre-existing untracked open/done treatment task files existed before this review and were not staged or edited.

2026-10-22: **HOLD**. T03 cites only S6 for a claim that two CEO interviews disagree on an employee count. S6 says up to 80; a newly reopened 2025 first-person interview says 60 and should be cited in the authored chain, or T03 should drop the comparison. Every one of 61 illustration prompts includes `cute-mystery` despite the exact `look` already containing that preset and the skill saying style belongs only in `look`. E03 and T03 cards include internal/editorial wording unsuitable for viewers. Other 74 lines were source-consistent; no media generation, TTS, blind-read signoff, owner adoption, import, upload, merge or publication was done. Exact hashes, primary URLs, individual line/shot results and corrections are in `docs/videos/story-everyday-victorinox-c13/reviews/independent-script-visual-review.md`.
