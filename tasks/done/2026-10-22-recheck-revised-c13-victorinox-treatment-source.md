---
id: 2026-10-22-recheck-revised-c13-victorinox-treatment-source
title: Recheck revised C13 Victorinox treatment source delta
status: done
priority: P2
area: docs
owner: codex-c13-independent-review
claimed_at: 2026-10-22T16:33:44Z
created_at: 2026-10-22T16:32:35Z
completed_at: 2026-10-22T16:38:02Z
branch: codex/brand-story-victorinox-c13-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-victorinox-c13/reviews/independent-treatment-delta-review.md
---

# Recheck revised C13 Victorinox treatment source delta

## Why

The first independent source review held C13 because a January 29 Swissinfo agency article placed a near-third sales fall in Q4 2001, while a January 25 direct Victorinox-manager interview limited the similar figure to October. The author revised the Treatment and source matrix twice. Recheck the exact final pair without editing author-owned files; sign a separate hash-bound delta receipt.

## Definition of done

- [x] A new independent PASS/HOLD receipt binds the revised Treatment and source matrix SHA-256 values and covers M01–M13, S1–S10, chronology, denominators, causal limits, narrative and visual gates.
- [x] Only this task and the delta receipt are committed to the C13 draft PR branch.

## Steps

- [x] Reopen changed Swissinfo S5/S10 wording and verify the author revision against original sources.
- [x] Recheck chronology, SEC entity boundaries, CEO recollection and production claims against the existing independent review and original sources.
- [x] Record the exact new hashes, verdict, limitations and signature in the delta receipt.
- [x] Run targeted checks, commit and push the receipt and this task only.

## How to verify

`Get-FileHash -Algorithm SHA256` on Treatment and source matrix; `git diff --check`; `npm run test:docs-videos`; `npm run check:tasks`; `git show --check --stat HEAD` after commit. Inspect the draft PR branch status. A task-board ghost left by the prior review is policy-blocked; report that check accurately and do not stage or delete the ghost.

## Notes

Separate reviewer `codex-c13-independent-review`; same C13 branch as author because the receipt is for draft PR #1693. The author task has a broader docs scope, so claim used `--force` for this narrow review-only scope. Earlier signed HOLD is preserved unchanged. Author's final candidate is head `bdf4feaa1` with Treatment SHA `A4A47F06F52490B4044267405445F31AC31EF7FB2C19575D59511D5BE0C57F20` and matrix SHA `295A7793DE618FEF714FA530F78592527EF77E82BAA38EE5594745B8386641D1`.

The new delta receipt gives a planning-gate PASS with explicit caveats on S5/S10's Q4-versus-October conflict, the Spanish/Portuguese 7.5% wording, SABI/AG denominators, M09 product statuses, and unmeasured duration/visual ratios. `npm run test:docs-videos` ran: 131/137 passed; six unrelated tests failed because this worktree lacks the `pinyin-pro` package required by `tools/video/tts/check.mjs`. The two reviewed Markdown files were unchanged throughout review.

`npm run tasks -- done ...` wrote this done copy but exited 1 because its open copy remained. `npm run check:tasks` exited 1 only on duplicate open/done IDs for this task and the prior independent review task; the many old stale-owner/scope warnings are warnings. Both open copies are untracked ghosts. The prior ghost was already blocked by policy on an exact-path removal attempt, so neither copy was deleted or staged.
