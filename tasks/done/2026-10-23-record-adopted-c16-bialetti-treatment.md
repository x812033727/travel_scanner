---
id: 2026-10-23-record-adopted-c16-bialetti-treatment
title: Record adopted C16 Bialetti Treatment
status: done
priority: P2
area: docs
owner: codex-c16-adoption
claimed_at: 2026-10-23T03:20:03Z
created_at: 2026-10-23T03:19:58Z
completed_at: 2026-10-23T03:20:43Z
branch: codex/brand-story-bialetti-c16-treatment
depends_on: []
scope:
  - docs/videos/brand-story-owner-approvals/C16-bialetti-treatment-20261023.md
---

# Record adopted C16 Bialetti Treatment

## Why

The owner adopted the reviewed C16 Bialetti direction on 2026-10-23. Record the decision against the exact Treatment, source matrix, and independent review inputs so subsequent script work cannot mistake a plan decision for script or paid-production approval. The original Treatment task still has an active broad claim on the C16 episode directory, so this receipt lives in a separate exact path.

## Definition of done

- [x] One owner-decision receipt identifies PR #1698, current Treatment and matrix SHA-256, independent review receipt SHA-256, the adopted causal direction, and unresolved M16/M17 limits.
- [x] No script, source Treatment, matrix, or paid-production file is edited under another task's active scope.

## Steps

- [x] Read back PR head, hashes, independent PASS, and active task ownership.
- [x] Record the owner's adoption in `docs/videos/brand-story-owner-approvals/C16-bialetti-treatment-20261023.md`.

## How to verify

Compare `Get-FileHash` of the Treatment, matrix and independent receipt with the receipt table; inspect `gh pr view 1698 --json headRefOid,isDraft,labels`; run `git diff --check` and `npm run check:tasks`.

## Notes

`tasks/open/2026-10-22-c16-bialetti-treatment-and-primary-source.md` remains `status: review`, owner `codex-bialetti-c16`, scope the entire `docs/videos/story-everyday-bialetti-c16` directory. The task-board scope audit confirms that a new `script.md` claim overlaps it. This receipt does not release, narrow, or override that active task. Script authoring waits for clean ownership coordination; it is not a content or budget HOLD.

After `npm run tasks -- done` wrote this completed copy, it failed to remove the local `tasks/open/2026-10-23-record-adopted-c16-bialetti-treatment.md` copy. One exact-file `Remove-Item -LiteralPath` attempt was rejected by automatic approval review as `blocked by policy`. The local open copy remains **untracked** and untouched; it is not staged in the PR. Local `check:tasks` therefore needs a readback after the copy is manually removed. No alternate deletion route was attempted.
