---
id: 2026-10-26-make-a01-capture-fixtures-work-in
title: Make a01 capture fixtures work in managed sandboxes
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-26T02:59:36Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/a01-capture/capture.test.mjs
  - tools/video/a01-capture/verify-archive.test.mjs
---

# Make a01 capture fixtures work in managed sandboxes

## Why

The managed sandbox exposes synthetic empty /tmp/.git and /workspace/.git ancestors. Six existing outside-Git capture fixtures fail with OUT_INSIDE_REPOSITORY or CAPTURE_INSIDE_REPOSITORY before reaching their intended assertions. The new renewal source checks exposed this execution-environment limitation; production capture guards must stay intact.

## Definition of done

- [ ] Preserve genuine outside-Git/path/link/runtime-pin protections and exercise the six cases on a supported fixture filesystem.
- [ ] Clearly report unsupported environment prerequisites; do not use path aliases or weaken guards merely to obtain green results.

## Steps

- [ ] Reproduce capture.test.mjs and verify-archive.test.mjs failures under the managed profile.
- [ ] Choose a supported fixture/runtime setup while retaining meaningful checks in ordinary CI.

## How to verify

Run the two targeted capture test files and npm run test:tools; report actual pass/fail/skip counts.

## Notes

Observed full suite on final renewal source: 2747 total,2736passed,6failed,5skipped. Exact failure names and log SHA are saved in docs/videos/ai-editable-explainer-animation/research/media-checkpoints/bookends-final-source-checks-20261026.json. Actual new video QA11/11 and renewal114/114 passed; this task is separate from film media quality. No capture source or environment protection was changed.
