---
id: 2026-10-20-s50-alternate-art-paper-pilot-preflight
title: S50 alternate art paper pilot preflight
status: done
priority: P2
area: docs
owner: codex-s50-art-paper
claimed_at: 2026-10-20T22:53:05Z
created_at: 2026-10-20T22:53:02Z
completed_at: 2026-10-20T22:55:57Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s50/review/r7-alternate-art-paper-preflight.md
---

# S50 alternate art paper pilot preflight

## Why

S50's declared MiniMax three-scene art pilot failed two native-image rounds at 0/3 KEEP and stopped. A future producer needs a different, source-safe visual plan and a cumulative price/stop rule before any further paid trial; the site's image judge and music quotas are currently exhausted.

## Definition of done

- [x] Independently inspect the fixed sources, current visual prompts and both original-size rejection receipts.
- [x] Record three new paper prompts with measurable native-size acceptance conditions, a bounded stop rule and full-episode cumulative cost cap without changing frozen creative or paying media.

## Steps

- [x] Reopen fixed A and V source bytes and compare their SHA-256 against `research.md`; inspect the three second-round original JPEGs.
- [x] Read the private ledger and live dry-run/status pricing; write the preflight under `docs/videos/curio-s50/review/`.
- [x] Run docs-video tests, `check:tasks` and diff check.

## How to verify

`npm run test:docs-videos` (236 tests), `npm run check:tasks`, and `git diff --check` in `/tmp/travel_scanner_curio_preprod`. The report is `docs/videos/curio-s50/review/r7-alternate-art-paper-preflight.md`; it does not assert that the model has generated or passed any new picture.

## Notes

The two previous 0/3 pilots were not retried. The new candidate removes unsupported sleeping/porter staging from `fire001`/`fire013` and removes the pointing finger that made an isolated object the focus of `fire096`. New-pilot threshold is 3/3 KEEP, with at most one prompt-reviewed retake per failed scene; the cumulative dry-run hard-cap proposal is US$4.75 including prior US$0.081. Image judge and music remaining quota both read 0 at the 2026-10-20 check. No paid media, frozen creative edit, or permission/approval record was made.
