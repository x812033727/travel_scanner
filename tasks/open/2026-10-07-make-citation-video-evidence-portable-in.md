---
id: 2026-10-07-make-citation-video-evidence-portable-in
title: Make citation video evidence portable in public repository
status: review
priority: P2
area: docs
owner: codex-citation-evidence-hygiene
claimed_at: 2026-10-07T10:45:17Z
created_at: 2026-10-07T10:45:05Z
completed_at:
branch: codex/ai-citation-completion-20261007
depends_on: []
scope:
  - docs/videos/ai-citation-check/archive-inventory-20261007.md
  - docs/videos/ai-citation-check/continuation-receipt-20261007.md
  - docs/videos/ai-citation-check/offline-audio-review-20261007.md
  - docs/videos/ai-citation-check/visual-review-20261007.md
  - tasks/open/2026-09-27-general-audience-ai-citation-checking-video.md
  - tasks/open/2026-10-07-audio-review-distinguishes-transcripts-awaiting-a.md
  - tools/repo-hygiene.test.mjs
---

# Make citation video evidence portable in public repository

## Why

PR #1369 fails the repository hygiene check because six public evidence files contain personal Windows paths. Those paths prevent readers from using the records on their own machines. The citation ticket also carries an older tolerated path that can now be removed.

## Definition of done

- [x] Public evidence paths use visible portable placeholders and the citation ticket no longer needs its tolerated host-detail entry.
- [x] Repository hygiene and task checks pass; a second reviewer confirms source bindings and the paid-work hold remain unchanged.
- [ ] Linux CI completes its full tools check on the repair commit.

## Steps

- [x] Replace local profile paths in the six declared files and delete only the citation ticket's KNOWN row.
- [ ] Run the relevant checks, record independent review, and update the existing draft PR.

## How to verify

`node --test tools/repo-hygiene.test.mjs`; `npm run test:tools`; `npm run check:tasks`; `git diff --check`.

## Notes

CI job `112746240720` on commit `8cd839e58763edc9c20cbf672025b238a270b5e6` identifies the public user-path regression. Real paths remain in the outside-Git operator receipts under `<home>/mokaair-work/ai-teaching-continuation-20261007/`. This repair changes document path text and removes an obsolete allowance; it does not change video sources, media, the unknown `ci037` request, STOP, review state, or approval. The production task stays blocked.

2026-10-07: the native repository hygiene test passes all 3 cases and task validation passes 1,616 files. Independent normalized-diff comparison confirms 35 personal path occurrences become zero while every evidence SHA string, all 18 language bindings, source, metadata, four translations, STOP, sent journal, cache, timeline and approvals remain unchanged. Full independent receipt: `<home>/mokaair-work/ai-teaching-continuation-20261007/portable-evidence-review-20261007.json`, SHA-256 `4ea906173ec36088359293b09807bdfb87fa7c399672ca804776d205675ab75d`. The initial full Windows tools run was stopped after verifying its process identity; its exit 1 is not a pass. A second run with concurrency limited to 2 is still running and has exposed unrelated Windows tools test errors, including `ERR_UNSUPPORTED_ESM_URL_SCHEME`; full tools success is not claimed. Linux CI remains the pending full-suite check.
