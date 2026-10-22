---
id: 2026-10-22-recheck-c16-bialetti-source-repair-at
title: Recheck C16 Bialetti source repair at new hashes
status: done
priority: P2
area: docs
owner: codex-c16-independent-source-review
claimed_at: 2026-10-22T18:41:35Z
created_at: 2026-10-22T18:41:30Z
completed_at: 2026-10-22T18:44:29Z
branch: codex/brand-story-bialetti-c16-treatment
depends_on: []
scope:
  - docs/videos/brand-story-independent-reviews/C16-bialetti-20261023.md
---

# Recheck C16 Bialetti source repair at new hashes

## Why

The C16 author repaired factual-source HOLDs after an independent first-pass review on PR #1698. The author cannot certify their own correction. Recheck only the changed Treatment and M04/M05/M07/M08/M17/M18 source rows at their new hashes, append an independent verdict while preserving the first receipt, and keep the PR guarded.

## Definition of done

- [x] A second exact-hash PASS/HOLD verdict records the repaired rows, changed Treatment wording, and remaining uncertainty without altering author files.
- [x] The receipt is committed, pushed, and linked from a read-back draft PR #1698 with `no-auto-merge`.

## Steps

- [x] Compare author revision `7b5e7ada7..11a59a5e8` and freeze new SHA-256 hashes.
- [x] Reopen the complete ADI catalogue, original Navarini paper, original 1937 Gazette and ES318772A1 bibliographic record.
- [x] Append the delta verdict to the independent receipt, retaining the first HOLD verbatim.
- [x] Check the task board and staged diff, then commit/push and read back PR state.

## How to verify

`Get-FileHash` on the two author files; source PDF page extraction and Google Patents field readback; `npm run check:tasks`; `git diff --cached --check`; `gh pr view 1698 --json headRefOid,isDraft,labels,body`.

## Notes

Second receipt section: `docs/videos/brand-story-independent-reviews/C16-bialetti-20261023.md`. Frozen author SHA-256 values: Treatment `7C4D675CAD01D6A255ADF540B05131A72488E97F51E7238090CA10A8ED52F5A1`; matrix `3705477A06ED4395C44D57882951349B0D8D16DAF8D946DC86CECEC9ADF1D713`. All repaired source claims PASS within their stated limits. M16 identity and M17 invention/ownership/litigation HOLD remain. The Treatment's first line still says delta review HOLD and should be administratively synchronized before owner review; independent reviewer did not edit author files.

`npm run check:tasks` PASS: 2077 valid task files, with pre-existing stale/overlap warnings. The prior `npm run test:docs-videos` failure was missing `pinyin-pro` in this worktree; this Markdown-only delta did not change the dependency path and the suite was not rerun or its dependency installed. `git diff --cached --check` and PR readback are required before handoff.
