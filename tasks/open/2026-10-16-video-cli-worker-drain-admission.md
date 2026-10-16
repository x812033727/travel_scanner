---
id: 2026-10-16-video-cli-worker-drain-admission
title: Gate manual video CLI paid commands during worker drain
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-16T09:22:29Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/cli.mjs
  - tools/video/cli-drain.test.mjs
---

# Gate manual video CLI paid commands during worker drain

## Why

The worker's shared STOP/DEPLOY_DRAIN cannot stop a separately invoked
`node tools/video/cli.mjs` from starting a new paid or remote unit after the
deployment helper's idle snapshot. The Shorts `tick` has a separate narrow
gate; this is the main video's manual command entry point.

## Definition of done

- [ ] Supported manual video CLI commands that can start remote/paid work
      refuse at entry under shared STOP or DEPLOY_DRAIN, before sending.
- [ ] Offline tests cover refusal and legitimate read-only behavior.

## Steps

- [ ] Recheck all active scopes and PRs for `tools/video/cli.mjs`; claim only
      after conflicts are resolved, without forcing another owner's claim.
- [ ] Implement and test the bounded supported CLI admission gate.

## How to verify

Run `node --test tools/video/cli-drain.test.mjs` and the full video tools test
suite. This does not prove that arbitrary raw `docker exec` is blocked.

## Notes

2026-10-16 HOLD: `2026-10-12-play-the-channel-intro-bumper-after`
(claude-opus-5-5-bumper, review), `2026-10-14-enforce-usd-25-all-in-cap`
(codex-story-budget-cap, in progress) and open PR #1454 touch
`tools/video/cli.mjs`. This task is intentionally unclaimed and no file edit
was made. A host-level manual exec freeze and post-request receipt checks
remain separate deployment gates even after this supported CLI is updated.
