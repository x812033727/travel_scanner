---
id: 2026-10-08-use-normal-caption-warnings-and-local
title: Use normal caption warnings and local bindings in imported language submission
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-08T07:53:24Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/imported-long-languages/runner.mjs
  - docs/videos/imported-long-languages/runner.test.mjs
---

# Use normal caption warnings and local bindings in imported language submission

## Why

The imported-language production sibling translated and reviewed Japanese text,
generated129 current caption cues and passed ordinary captionsItem with three
reading-speed warnings. Its private localAdditions classification nevertheless
reported the captions missing. An earlier native submitSnapshot caller supplied
the remote backend project where the renewal binder requires a loaded local
project, blocking a fully completed English stage without further model work.
These deterministic compatibility defects were reproduced during2026-10-08
stalled-video recovery. Private guarded corrections preserve every paid result;
the shared implementation still needs regression coverage.

## Definition of done

- [ ] Ordinary reading-speed warnings stay visible and do not become hard missing
      captions when normal source/timing/file checks pass.
- [ ] Missing, stale, overlapping or otherwise invalid captions still block.
- [ ] Renewal submission receives a source-bound local project; backend owner
      choices and approved-final authority stay separate and enforced.

## Steps

- [ ] Coordinate with the active imported-language runner PR1359 before editing.
- [ ] Add regressions for the actual warning and local/remote binding mismatch.
- [ ] Verify zero model calls when only existing caption delivery remains.

## How to verify

Run the runner's focused tests and renewal binding tests, using actual local
project fixtures plus mocked backend decisions. Inspect preserved warning output
and rejected invalid-caption cases; never relax unknown-paid-request guards.

## Notes

Detailed frozen candidates and proofs remain outside Git at
<home>/mokaair-work/handoff/branding-peak-20261008/continuation/.
The operational checkpoint is docs/videos/recovery/2026-10-08-stalled-production.md.
Do not replay the free-versus-paid request interrupted by the unrelated15:51
deployment. This follow-up files a code defect, not permission to restart paid work.
