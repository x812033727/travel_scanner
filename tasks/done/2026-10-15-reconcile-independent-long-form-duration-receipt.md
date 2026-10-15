---
id: 2026-10-15-reconcile-independent-long-form-duration-receipt
title: Reconcile independent long-form duration receipt after H09 main sync
status: done
priority: P2
area: docs
owner: codex-gpt6-h09-independent-duration-review
claimed_at: 2026-10-15T08:36:29Z
created_at: 2026-10-15T08:35:46Z
completed_at: 2026-10-15T09:46:55Z
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Reconcile independent long-form duration receipt after H09 main sync

## Why

Draft PR #1503 for Curio H09 and the newer main branch both changed the SHA-256-bound long-form duration receipt. Their `review.md` and `review.json` conflict even though the reviewed source changes are disjoint. A receipt that chooses one side or changes a hash without independent review would discard review evidence or fail the duration gate.

## Definition of done

- [x] The merged report retains both branches' review history, its 108 table rows match the merged source bytes, and `review.json` binds that exact report with an independent reviewer identity. The duration CLI and review regression test pass.

## Steps

- [x] Claim only `review.md` and `review.json`; inspect both parents' sections, receipt maps, and review rules without editing the receipts.
- [x] Wait for the H09 code author to finish the main sync and signal that the implementation tree is stable.
- [x] Independently verify both parents' report hashes and all 108 source bindings against the merged tree; inspect the code delta for duration-rule changes.
- [x] Preserve both parents' review sections, add a merge follow-up with provenance and non-claims, and update the 108-row table and JSON hashes from actual bytes; hand only the two receipt files to the H09 author for the single merge commit.
- [x] Run the duration CLI, its regression test, and the relevant repository checks; hand the result and exact file hashes to the H09 author.

## How to verify

`node tools/video/long-form/cli.mjs check`; `node --test tools/video/long-form/review.test.mjs`; `npm run check:tasks`; `git diff --check`; compare all 108 working-tree SHA-256 values with `review.json` and check the report bytes against `report_sha256`.

## Notes

The H09 and main receipts each list the same 108 paths. Seven hashes differ: main owns reviewed changes in `apps/api/app/video_automation/judge.py`, `schemas.py`, `series.py`, `docs/videos/long-form/plans.json`, `tools/video/automation/flow.mjs`, and `tools/video/core/drama.mjs`; H09 owns the reviewed `tools/video/media/clips.test.mjs` change. Main adds eight review sections; H09 adds two. On 2026-10-15, an independent `git show` blob SHA-256 pass confirmed both parents' own report hashes and all 108 bindings (`bad=[]` for both). Keep those sections byte-identical and reconcile the table only after the code merge. The reviewer did not write the media implementation and must not update the receipt until the final source tree is ready. Git cannot make a partial receipt commit during the unresolved merge, so the H09 author will stage the two independently edited receipt files in the single merge commit.

After the H09 author stabilized the media conflict, the merged source tree contained 101 bindings shared by both parents, six main-only reviewed hashes and one H09-only reviewed hash; no bound file had novel bytes. The main preset sets a 10-minute story target while its earlier duration review retains the measured 480-second narration and final-video floors. The H09-only clips test changes paid-failure and fresh-seed expectations, not clip-duration implementation. The new report preserves all ten side-specific sections, adds a DURATION_ONLY merge follow-up and has SHA-256 `72553bd4a18ef5f0d3991f99da91670d9e3f9afeb3dee1d99eadaaacbc99a950`; `review.json` has SHA-256 `dcd26fd9440106ce68aa8f96d49cf6431f002d4929578e5b944cac952a6c094b`. Both files have LF with no CR.

Verification in the unresolved merge tree: `node tools/video/long-form/cli.mjs check` passed all 473 plans; `node --test tools/video/long-form/review.test.mjs` passed 2/2; `git diff --check -- docs/videos/long-form/review.md docs/videos/long-form/review.json` passed; `npm run check:tasks` exited 0 with warnings about unrelated and inherited main-branch active scope overlaps. The H09 author staged the reviewed files in merge commit `9a48a8c0f` and subsequently pushed CI fix `ce0ed5c83`; the author reported 23/23 checks green at the exact head. The independent receipt hashes remained unchanged.
