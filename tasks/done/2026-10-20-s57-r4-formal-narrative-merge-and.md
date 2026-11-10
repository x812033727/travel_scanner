---
id: 2026-10-20-s57-r4-formal-narrative-merge-and
title: S57 R4 formal narrative merge and diagnostic
status: done
priority: P2
area: docs
owner: codex-s57-r4-merge
claimed_at: 2026-10-20T23:25:08Z
created_at: 2026-10-20T23:25:06Z
completed_at: 2026-10-20T23:28:09Z
branch:
depends_on:
  - 2026-10-20-s57-r4-independent-source-and-written
scope:
  - docs/videos/curio-s57/review/r4-merge
---

# S57 R4 formal narrative merge and diagnostic

## Why

R4 has a source PASS and two new blind narrative ballots. The author needs a formal, auditable fixed-OR verdict bound to the R4 creative freeze before any R5 edit.

## Definition of done

- [x] `review/r4-merge/` contains exact raw ballots, faithful 13-item answer transcriptions, fixed-OR audit, merged answers, official CLI output and record, and an R4 HOLD summary.

## Steps

- [x] Verify all five R4 SHA-256 values and both raw ballot hashes; retain each ballot's vote and reason.
- [x] Apply `panelVerdict` and `mergePanelVerdicts`, preserving the A-YES/B-NO `one_line` split.
- [x] Run formal `narrative --answers` against the exact R4 freeze and archive the exit, output, record, and before/after hashes before R5 edit clearance.
- [x] Write the diagnostic and hand off the four shared NO items without running policy or paid media.

## How to verify

See `docs/videos/curio-s57/review/r4-merge/cli-status.json` for the exact formal CLI command and five-file pre/post hashes; `merge-audit.json` stores both `panelVerdict` results and `mergePanelVerdicts`. The CLI exited 1 with the expected narrative HOLD and wrote `official-narrative-record.json`.

## Notes

R4 fixed OR: 9/13 YES, four shared required NO (`chapters_link`, `payoffs`, `no_recap`, `no_detour`). Reader A 9/13, B 8/13; `one_line` A YES/B NO, merged YES. CLI record SHA-256 `ff0c11b17c09aa5f016981a0582182e2a469c10c0a5f8fa6dd989c8bcee37804`; panel narration SHA-256 `44f05cb06f452a3d7fcf987b2895f05ea9c495db776667de43d755e924f557a8`. Root and S57 preproduction agent received R5 edit clearance only after archive was complete. Source PASS remains separate; no policy or paid-media gate was run.

Post-archive integrity check passed. `npm run test:docs-videos`: 236 pass, 0 fail. `npm run check:tasks`: exit 0 with unrelated stale/scope warnings.
