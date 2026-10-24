---
id: 2026-10-20-s57-r5-formal-two-reader-narrative
title: S57 R5 formal two-reader narrative merge and CLI diagnostic
status: done
priority: P2
area: docs
owner: codex-s57-r5-merge
claimed_at: 2026-10-20T23:35:47Z
created_at: 2026-10-20T23:35:45Z
completed_at: 2026-10-20T23:37:47Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s57/review/r5-merge
---

# S57 R5 formal two-reader narrative merge and CLI diagnostic

## Why

R5's independent source and written-visual review passed, but its story cannot advance until two fresh blind readers' ballots are merged under the fixed official OR rule and the exact frozen draft is run through the narrative CLI.

## Definition of done

- [x] `docs/videos/curio-s57/review/r5-merge/` preserves both raw ballots, official-shape transcriptions, an auditable OR verdict, official CLI receipt, and an exact-version PASS/HOLD summary.

## Steps

- [x] Verify both clean-room ballots used the same R5 script SHA and copy their raw bytes without edits.
- [x] Transcribe each of the 13 votes with exact scene quotes, run `panelVerdict` and `mergePanelVerdicts`, and preserve the single-reader disagreements.
- [x] Run official narrative CLI on the exact five-file freeze, archive exit/stdout/stderr/record and verify five SHA before and after.

## How to verify

Read `docs/videos/curio-s57/review/r5-merge/summary.md`, `merge-audit.json`, `cli-status.json`, and `official-narrative-record.json`; compare raw ballot hashes and `sha256sum docs/videos/curio-s57/{research.md,brief.md,claims.md,video.json,script.md}`. `npm run check:tasks` validates the board file. The exact CLI command and exit are in the summary/status receipt.

## Notes

R5 formal OR merge is **12/13 HOLD**, only shared NO `no_recap`. A: 10/13 with NO `payoffs`, `no_recap`, `no_detour`; B: 12/13 with NO `no_recap`. A's other two objections remain in the audit and summary but merge YES under fixed OR. CLI exit 1 and `passed:false`; record SHA `275ca3727588b91e264723490f5fa093b893ee8d42e9497e91c5d15104854f10`; five creative SHA matched before and after. R6 author edit clearance was sent only after this archive. R5 policy/media remain held.
