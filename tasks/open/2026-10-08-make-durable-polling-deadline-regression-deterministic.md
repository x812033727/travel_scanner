---
id: 2026-10-08-make-durable-polling-deadline-regression-deterministic
title: Make durable polling deadline regression deterministic
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-08T07:52:32Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/client.test.mjs
---

# Make durable polling deadline regression deterministic

## Why

The Windows tools suite's durable poll regression expected two completed lookups
but observed one under concurrent load. The case uses a real wall-clock deadline
and took224ms. A slow test scheduling interval can consume its polling window
before the second mock response, obscuring the intended distinction between
an answered lookup and a transport error. This was one of eight failures in the
2026-10-08 broad tools run; the suite is not reported as green.

## Definition of done

- [ ] The test deterministically covers answered, unanswered, refused and lost
      transport outcomes without depending on machine load.
- [ ] Production polling, request receipts and uncertain-paid-request semantics
      remain unchanged.

## Steps

- [ ] Reproduce the assertion under concurrent Windows load and inspect its clock.
- [ ] Use the existing injected clock/sleep facilities or a controlled test clock.
- [ ] Run the focused client suite on Windows and Linux.

## How to verify

`node --test tools/video/automation/client.test.mjs`; verify the same real outcome
assertions, not only that a timeout was lengthened.

## Notes

Outside-Git evidence: C:/Users/x8120/mokaair-work/stalled-video-audit-20261008/test-tools.log,
test beginning at571 and final assertion at2240. No change to the implementation
or any provider retry was made while filing this follow-up.
