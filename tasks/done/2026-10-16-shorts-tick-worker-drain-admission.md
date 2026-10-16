---
id: 2026-10-16-shorts-tick-worker-drain-admission
title: Block Shorts CLI tick while video worker STOP or drain is active
status: done
priority: P1
area: tools
owner: codex-video-worker-warm-drain
claimed_at: 2026-10-16T09:17:01Z
created_at: 2026-10-16T09:16:23Z
completed_at: 2026-10-16T09:29:53Z
branch: codex/video-worker-warm-drain-20261016
depends_on: []
scope:
  - tools/video/shorts/cli.mjs
  - tools/video/shorts/cli-drain.test.mjs
---

# Block Shorts CLI tick while video worker STOP or drain is active

## Why

The worker shell checks the shared STOP, but a supported manual
`node tools/video/shorts/cli.mjs tick` directly submits a calendar POST even
after STOP or DEPLOY_DRAIN. This can start YouTube or other remote work after
the deploy barrier has taken its idle snapshot.

## Definition of done

- [x] Shorts `tick` refuses before its first network call when shared STOP or
      DEPLOY_DRAIN exists, whether invoked by the worker or manually.
- [x] A focused offline test proves that refusal and the normal no-hold path.

## Steps

- [x] Gate the supported Shorts command against the shared work base.
- [x] Add a fake transport test and document remaining raw-exec limitations
      in the warm-drain task.

## How to verify

`node --test tools/video/shorts/cli-drain.test.mjs`, plus `npm run test:tools`.

## Notes

This narrowly scoped ticket is independent of the warm-drain task so both can
be worked and reviewed in the same stacked PR. It does not cover the general
`tools/video/cli.mjs`, currently claimed by two other active tasks; raw Docker
exec must be separately frozen by deployment operations.

2026-10-16: `node --test tools/video/shorts/cli-drain.test.mjs` passed 1/1,
showing zero POSTs under either marker and one POST without a hold. After
`npm ci`, full Windows `npm run test:tools` failed in 54 unrelated child
processes; isolated `tools/video/cli.test.mjs` exits with NTSTATUS
`3221226505` without a JS assertion. CI on Ubuntu remains the gate. No
production call was made.
