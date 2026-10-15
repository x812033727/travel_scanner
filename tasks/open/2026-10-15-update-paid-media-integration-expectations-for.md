---
id: 2026-10-15-update-paid-media-integration-expectations-for
title: Update paid media integration expectations for reserved judge cost
status: in-progress
priority: P1
area: tools
owner: codex-gpt6-h09-ci
claimed_at: 2026-10-15T01:34:17Z
created_at: 2026-10-15T01:33:36Z
completed_at:
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - tools/video/media/clips.test.mjs
  - tools/video/media/look-keyframes.test.mjs
---

# Update paid media integration expectations for reserved judge cost

## Why

H09 PR #1503 added a reservation for each paid media judge call. Linux CI on commit 5800dd6c2 found six media integration failures. The stage code must still support a fresh paid rejudge after a source change and release a request rejected before it reaches the provider. Once those behaviors are fixed, the clip tests also need to count provider-reported failed-job charges and the judge's simultaneous reservation during a paid import.

## Definition of done

- [ ] The existing look/keyframes rerun tests pass without relaxing their rejudge counts, and the clip tests prove failed provider jobs and concurrent import/judge reservations are accounted for.

## Steps

- [x] Check that no active task or PR owns either integration test file, then claim this narrow task.
- [x] Update only stale clip ledger expectations; preserve the look/keyframes behavior assertions.
- [ ] Rerun the affected tests on Linux CI after the production fix, and resolve any remaining real regression.

## How to verify

`node --test tools/video/media/clips.test.mjs tools/video/media/look-keyframes.test.mjs`; `npm run test:tools`; `npm run check:tasks`; read the exact head SHA and video-test checks on PR #1503.

## Notes

The initial 5800dd6c2 Linux `web-checks`, `smoke`, and `video-tests` failures reproduced the same six assertions. `clips.test.mjs:637` assumed a provider job that later failed had zero cost, although its status response supplied a positive `usd_estimate`. `clips.test.mjs:1082` assumed only the imported clip was reserved while judging, but the new judge reservation is also live during that call. The original look/keyframes assertions were retained; the paired stage fix allows a fresh paid rejudge with a distinct repeat key and keeps uncertain reservations blocked. The local Windows Node test runner exits at the file level without assertion diagnostics, so Linux CI is the decisive check.
