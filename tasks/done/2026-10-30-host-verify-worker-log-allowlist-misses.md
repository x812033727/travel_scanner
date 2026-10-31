---
id: 2026-10-30-host-verify-worker-log-allowlist-misses
title: host-verify: worker log allowlist misses normal lane progress after the draft cap
status: done
priority: P2
area: ops
owner: claude-opus-5-5-redeploy
claimed_at: 2026-10-30T19:14:18Z
created_at: 2026-10-30T19:13:43Z
completed_at: 2026-10-31T01:57:33Z
branch:
depends_on: []
scope:
  - .agents/skills/deploy/scripts/host-verify.sh
  - tools/deploy-host-verify.test.mjs
---

# host-verify: worker log allowlist misses normal lane progress after the draft cap

## Why

The deploy of `c58d79510` on 2026-10-30 reported `FAIL video-worker-started context_errors=1`
while the worker was healthy: it was running with no restarts and took `daily-ai-20261029` from
the approved final to the confirmed upload. The verifier from #1929 accepts only exact progress
lines after a policy message, and these normal ones were not on its list, so with the monthly
draft cap in force any video reaching upload made a good deploy read as failed.

## Definition of done

- [x] A brief moving from approval to upload under the draft cap passes `video-worker-started`.
- [x] Unknown lines, free-text notes and the same lines with an error suffix still fail.

## Steps

- [x] Add the auto-approved final, upload package, publish confirmation and auto-confirmed upload
      lines, the durable stages' "still running" line, and the translator and caption reviewer
      token lines, to `benign` in `host-verify.sh`.
- [x] Add the worker's actual log to `tools/deploy-host-verify.test.mjs`, with near-misses.

## How to verify

```bash
node --test tools/deploy-host-verify.test.mjs
```

## Notes

- Only the auto-approval notes are accepted (`judge.py`: `QA_AUTO_APPROVED_NOTE`,
  `PACKAGE_AUTO_APPROVED_NOTE`). An owner's note is free text, so it stays unknown and fails closed.
- `is still running` covers `DURABLE_STAGES` in `tools/video/automation/client.mjs`. That is a
  second list to keep in step with the worker's messages: a new progress line fails the check until
  it is added here. The check fails closed on purpose; read the log before treating it as a fault.
- `npm run tasks -- new` kept only the last of two `--scope` flags; the first was added by hand.
