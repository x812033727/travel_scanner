---
id: 2026-09-28-make-five-drama-plans-reproducible-after
title: Make five drama plans reproducible after Git checkout
status: done
priority: P1
area: docs
owner: codex-five-binge-pr
claimed_at: 2026-09-28T01:52:08Z
created_at: 2026-09-28T01:51:57Z
completed_at: 2026-09-28T01:57:02Z
branch: codex/five-binge-story-plans
depends_on: []
scope:
  - docs/videos/series-plans/binge-five-20260928
---

# Make five drama plans reproducible after Git checkout

## Why

The owner authorized a draft PR for the completed five drama planning packs. Pre-push inspection found continuity CSVs use CRLF while repository attributes require LF. Git would normalize these bytes and invalidate the generated manifest and exact file checks on a fresh checkout.

## Definition of done

- [x] Generated artifacts and manifests survive Git normalization with unchanged story source and review hashes.
- [x] The regression fails before the fix and passes afterward; all five plans and required reviews validate.
- [x] The staged draft-PR package contains only the completed planning scope and task records.

## Steps

- [x] Check live local/remote branch and PR collisions; fast-forward the existing branch to origin/main.
- [x] Reproduce the CSV normalization defect with a regression test.
- [x] Use LF output for CSV, rebuild, and preserve UTF-8 BOM and data.
- [x] Verify all 100 staged generated blobs against compile(source) and prepare the scoped commit for the authorized draft PR.

## How to verify

- node docs/videos/series-plans/binge-five-20260928/validate.mjs --require-reviews
- node --test docs/videos/series-plans/binge-five-20260928/validate.test.mjs
- npm run test:tools
- npm run check:tasks
- Compare all staged generated file blobs to compile(source); inspect draft flag, PR file scope and CI on the pushed SHA.

## Notes

- Existing untracked .codex/environments/ remains excluded. No runtime app, workflow or production files are changed.
- The regression failed specifically on continuity.csv before the fix. No story source changed, so the second-round editorial receipts retain their exact source hashes.
- This task follows the owner's draft-PR approval; merger, backend creation, media generation, deployment and publishing are outside its scope.

- Validation passed: five plans with current independent receipts; all 17 regression tests; all 100 staged generated blobs match compile(source); git diff --cached --check. The archived empress source had one surplus EOF blank line removed; parsed historical source hash is unchanged.
- npm ci completed (Node engine advisories for existing dependencies). Full npm run test:tools encountered 20 existing video test-file native crashes on Windows; recorded separately in tasks/open/2026-09-28-investigate-windows-native-crash-in-video.md with reproduction, instead of claiming a green full suite.
- The original authoring and second-review task notes describe their earlier local delivery state. This follow-up prepares their commit/push/PR without reopening or rewriting story reviews.
