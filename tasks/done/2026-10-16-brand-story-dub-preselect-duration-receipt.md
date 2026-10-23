---
id: 2026-10-16-brand-story-dub-preselect-duration-receipt
title: Independently bind brand story dub preselection to long-form duration review
status: done
priority: P2
area: docs
owner: codex-story-dub-independent-review-8a78
claimed_at: 2026-10-16T14:31:02Z
created_at: 2026-10-16T14:28:12Z
completed_at: 2026-10-16T14:39:25Z
branch: codex/story-dub-preselect-20261016
depends_on: []
scope:
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
  - tasks/open/2026-10-16-brand-story-dub-preselect-duration-receipt.md
  - tasks/done/2026-10-16-brand-story-dub-preselect-duration-receipt.md
---

# Independently bind brand story dub preselection to long-form duration review

## Why

The brand story dub preselection changes 11 files registered in the mandatory long-form
duration review. An independent reviewer must assess whether those changes alter duration
policy and bind the exact file bytes to the review receipt before CI can pass.

## Definition of done

- [x] An independent `DURATION_ONLY` review records the exact changed file hashes and
      confirms the existing long-form duration targets, floor and checks remain intact.
- [x] `node tools/video/long-form/cli.mjs check` and the receipt tests pass.

## Steps

- [x] Independently inspect the brand story dub preselection API, worker and UI diff.
- [x] Audit other active receipt owners and claim this narrow review task.
- [x] After implementation freeze, hash the 11 changed registered files and verify all
      unchanged bindings against disk.
- [x] Update the review report and machine receipt, then run the checks.

## How to verify

`node tools/video/long-form/cli.mjs check`
`node --test tools/video/long-form/review.test.mjs`
`npm run check:tasks`

## Notes

Claimed with `--force` only after checking the apparent scope conflicts: older A21,
Curio-look, brand-story route/budget and the merged video-topic PR #1520 retain stale
claim metadata, but no owner is currently editing this receipt in this branch. Draft PR
#1503 remains open and also edits this receipt; its `curio-h09` worktree was clean at the
ownership audit. This branch may sign its own bytes independently. Whichever PR merges
second must rebase, review the combined diff, and rebind all changed registered files.
The old draft PR #1387 is also open but idle. If either active PR changes before this
receipt is signed, repeat the overlap and SHA audit.

Independent review rebound exactly 11 of 108 registered source paths; the other 97
match the prior receipt. Pre-rebase report SHA-256:
`931800b854fe2542ae96b9b65cf241758a60bb086c47326a4ee4f3e65cebcba2`.
The API, worker and UI diffs change review/production timing, not the 600/780-second
targets or 480-second measured floor. `node tools/video/long-form/cli.mjs check` passed
473 plans; `node --test tools/video/long-form/review.test.mjs` passed 2/2; and
`npm run check:tasks` exited 0 with stale-claim overlap warnings. If implementation
bytes change after this signature, independently re-review and rebind before merging.

After the first signature, the web test author updated two shared fixtures to declare
the already approved final explicitly in their checklists. Independently reviewed that
fixture-only delta; `apps/web/components/admin-video-reviews.test.tsx` now hashes to
`231f41dc4e3b390b19b7d2bdab55e336891602315554b99b9715803023974286`.
Rebound this one registered row and the report hash. The long-form check again passed
473 plans, the receipt test again passed 2/2, and `git diff --check` passed.

The rebase from `9b8bcf6b2` to `974ad0d39` normalized seven web worktree files from
CRLF to LF while retaining identical Git blobs. For each, converting current LF bytes
back to CRLF reproduces its previously reviewed SHA-256 exactly. An independent
duration-only increment rebound those seven raw hashes; all other 101 registry paths
remain unchanged. Current report SHA-256:
`cdf01bf334aff629b4fc362267edc58810b1f8ecb4121ce45bc01e2069036127`.
After rebinding, long-form check passed 473 plans, receipt tests passed 2/2, and
`git diff --check` passed.
