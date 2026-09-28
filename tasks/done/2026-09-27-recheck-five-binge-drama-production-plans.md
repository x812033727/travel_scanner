---
id: 2026-09-27-recheck-five-binge-drama-production-plans
title: Recheck five binge drama production plans
status: done
priority: P1
area: docs
owner: codex-five-binge-recheck
claimed_at: 2026-09-27T18:17:29Z
created_at: 2026-09-27T18:17:19Z
completed_at: 2026-09-27T18:35:12Z
branch: codex/five-binge-story-plans
depends_on: []
scope:
  - docs/videos/series-plans/binge-five-20260928
---

# Recheck five binge drama production plans

## Why

The owner requested a second check of the five completed drama planning packs. Re-read the stories independently, verify the production handoff and validators, fix concrete defects, and record a source-bound second review without generating media or creating backend work.

## Definition of done

- [x] All five stories receive a second substantive continuity and packaging review.
- [x] Concrete findings are fixed and affected files rebuilt; previous review evidence is preserved.
- [x] Current source-bound reviews, production checks and relevant regression tests pass.
- [x] A readable second-check report clearly states remaining production-stage limitations.

## Steps

- [x] Re-run the existing validators and check scope collisions; reuse the current task-owned branch.
- [x] Independently read all five stories and audit the handoff renderer.
- [x] Correct findings, obtain re-review, rebuild and validate.
- [x] Deliver the recheck report and close this task.

## How to verify

`node docs/videos/series-plans/binge-five-20260928/validate.mjs --require-reviews --write-report`

`node --test docs/videos/series-plans/binge-five-20260928/validate.test.mjs`

`npm run check:tasks`

## Notes

- Initial recheck: five packs and 14 validator tests pass; no active task or open PR touches the scope. Existing untracked .codex/environments/ is unrelated.
- Second reviewers rotate: xianxia_author reads wedding/train; empress_author reads city/xianxia; train_author independently reads empress; root also reads empress and audits shared tooling. No media/backend/upload operations are authorized or performed.

- Completed: all five second-round readers reviewed all 200 episodes and their settings/mysteries/packaging; current receipts are review_round=2 and bound to final hashes. First-round receipts and exact source snapshots are archived under reviews/round-01.
- Fixed wedding past-life rescue setup/payoff, fixed-intercom continuity, villain evidence knowledge and offscreen speaking roles; train voice registration, ticket-sound rule and verify-before-exit staging; empress premature knowledge and context-specific traditional Chinese wording; city scene/timeline mismatch; xianxia memory wording and tags.
- Fixed structured narrator omission in generated setting Markdown and required compilation-tag validation. All 100 generated files rebuilt; validation with required reviews passes, 16 regression tests pass, 61 JSON files parse, 82 local Markdown links resolve, and all 5 archived receipts match historical source hashes.
- npm run check:tasks passes (941 tasks before closure); existing unrelated stale-claim/scope warnings remain. No app code, paid/media generation, backend creation, upload, PR or production operation was performed.
- Handoff: docs/videos/series-plans/binge-five-20260928/RECHECK.md with actual fixes and the remaining script/audio/film measurement boundary.
