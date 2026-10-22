---
id: 2026-10-22-mechanically-recheck-c16-treatment-status-line
title: Mechanically recheck C16 Treatment status line
status: done
priority: P2
area: docs
owner: codex-c16-independent-source-review
claimed_at: 2026-10-22T18:47:45Z
created_at: 2026-10-22T18:47:41Z
completed_at: 2026-10-22T18:48:33Z
branch: codex/brand-story-bialetti-c16-treatment
depends_on: []
scope:
  - docs/videos/brand-story-independent-reviews/C16-bialetti-20261023.md
---

# Mechanically recheck C16 Treatment status line

## Why

After independent source-delta PASS, the C16 Treatment still carried a stale HOLD status line. Its author synchronized the status line on PR #1698 and requested a separate exact-hash mechanical review. The independent reviewer may update only the existing review receipt.

## Definition of done

- [x] A hash-bound third receipt confirms whether the author changed only the Treatment status line, left matrix bytes unchanged, and retained M16/M17 HOLD.
- [x] PR #1698 links the receipt and remains draft with `no-auto-merge` after readback.

## Steps

- [x] Compare prior source-PASS head `ac6e1410b` with author sync head `ade850163`, including raw-byte hashes.
- [x] Confirm author-only status change and unchanged M16/M17 HOLD wording.
- [x] Append the third exact-hash PASS/HOLD receipt without touching author files.
- [x] Check, close task, commit, push, and read back PR.

## How to verify

Python byte comparison of `git show ac6e1410b:treatment.md` against current file, excluding line 3; byte comparison of old and new `source-matrix.md`; `npm run check:tasks`; `git diff --cached --check`; `gh pr view 1698 --json headRefOid,isDraft,labels,body`.

## Notes

Old Treatment SHA-256 `7C4D675CAD01D6A255ADF540B05131A72488E97F51E7238090CA10A8ED52F5A1`; new `1B82057CE1CA064C84829F64F2D5B4679CC2E9CCA74F14F24964650636282EEE`. Both versions have 44 lines; only line 3 differs and all other bytes are identical. Matrix is byte-identical at `3705477A06ED4395C44D57882951349B0D8D16DAF8D946DC86CECEC9ADF1D713`. New status line and matrix still explicitly HOLD M16/M17 factual uncertainty. Third verdict: PASS for administrative status sync, owner approval and production not passed. Broad docs-videos tests are not rerun for this single-line Markdown change; prior worktree failure was missing `pinyin-pro`.
