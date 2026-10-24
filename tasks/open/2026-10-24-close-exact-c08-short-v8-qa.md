---
id: 2026-10-24-close-exact-c08-short-v8-qa
title: Close exact C08 short-v8 QA CLI duration bypass
status: review
priority: P1
area: tools
owner: codex-c08-short-backend
claimed_at: 2026-10-24T05:48:00Z
created_at: 2026-10-24T05:47:43Z
completed_at:
branch: codex/c08-kikkoman-canonical-preflight-20261024
depends_on: []
scope:
  - tools/video/qa/cli.mjs
  - tools/video/qa/duration.test.mjs
  - tasks/open/2026-10-24-close-exact-c08-short-v8-qa.md
  - tasks/done/2026-10-24-c08-short-v8-safe-promotion.md
---

# Close exact C08 short-v8 QA CLI duration bypass

## Why

The approved C08 short-v8 carries an exact, frozen four-to-five-minute duration policy. The final QA CLI nevertheless passes the ordinary eight-minute floor to `assembleItem` because C08 has category `explainer`; a valid five-minute cut is then rejected after the narrower 240-second body and 300-second final checks pass. The direct `assembleItem` tests did not cover the CLI argument.

## Definition of done

- [x] Real QA CLI accepts only the exact approved C08 short-v8 within measured body >=240 seconds and final cut <=300 seconds, while one-frame violations and nearby identities remain held.
- [x] `assembleItem` retains the explicit `minMinutes` contract and other videos retain the ordinary eight-minute QA parameter.
- [ ] Existing C08 independent review receipt is re-bound by a non-author reviewer before treating QA as cleared.

## Steps

- [x] Exclude only `isC08ApprovedShortStory(doc)` from the CLI's duplicate eight-minute `minMinutes` argument.
- [x] Add real QA CLI regression using the approved 36-line project, synthetic local timing evidence and final bytes; cover exact and neighboring identities plus one-frame boundaries.
- [x] Run focused tests and report exact source hashes to the independent reviewer.

## How to verify

Run `node --test tools/video/qa/duration.test.mjs tools/video/qa/qa.test.mjs tools/video/core/duration.test.mjs`, `git diff --check` and `npm run check:tasks`. No paid media, provider calls, production import, or upload.

## Notes

Parent independently reproduced: approved C08 with 9000 checked final frames fails QA CLI as 05:00 under the eight-minute floor, while `assembleItem` with `minMinutes: 0` passes. The existing independent DURATION_ONLY receipt at d9adb5b4b predates this CLI correction and must be reviewed again by a different author. Three older C08 open task copies are duplicated with their done copies because automatic policy blocked their deletion; do not attempt an alternate removal.

The real CLI regression sets the test-only episode minimum explicitly to 8 and restores its prior environment. It copies the approved 36-line short project into a temporary fixture, binds silent WAVs and checked fake final bytes, and checks 7199 and 7200 body frames, 8220 body + 780 selected bookend = 9000 final frames, and 8221 + 780 = 9001 final frames. It also copies the historical 84-line C08 into a temporary fixture, adjusts that copy's pre-existing outro lint issue, and verifies a short measured cut remains held. The fixture is not production duration or media evidence. Bundled Node 24.19: 42/42 focused core/QA tests passed. `git diff --check` passed. `npm run check:tasks` is blocked by exactly the three pre-existing duplicate open/done C08 IDs; `long-form check` reports the expected stale `qa/cli.mjs` and `qa/duration.test.mjs` bindings pending independent review.

Source SHA-256 after the fix: `tools/video/qa/cli.mjs` = `3f88cb712d7658e0ac2659e79ea67b673f4201b50d04b330265d4b620dcd2c32`; `tools/video/qa/duration.test.mjs` = `0dd86e17c7048f1873d86abf4c07219eed41ca756c0e1bf30288527635ceb3d8`.
