---
id: 2026-10-22-review-revised-patagonia-c09-script-sources
title: Review revised Patagonia C09 narration sources
status: done
priority: P2
area: docs
owner: codex-root-independent-review
claimed_at: 2026-10-22T14:06:58Z
created_at: 2026-10-22T14:06:50Z
completed_at: 2026-10-22T14:08:30Z
branch: codex/brand-story-patagonia-c09-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-patagonia-c09-revised-script-review
---

# Review revised Patagonia C09 narration sources

## Why

The owner adopted C09's treatment, then a cold reader held the initial script and the author rewrote the narration and matching shot plan. The old 101-line source PASS is bound to old bytes. This task independently rechecks the new 83-line version before any owner script or paid gate.

## Definition of done

- [x] A separate, input-hash-bound source review records the revised script and visual verdict with exact repair IDs and source links.

## Steps

- [x] Confirm the script, visual plan and author note hashes, and the 83/83 ID mapping.
- [x] Reopen S1, S2, S3, S4, S6 and S7 directly; review changed narration and its visual claims without importing the old PASS.

## How to verify

`Get-FileHash docs/videos/story-everyday-patagonia-c09/{script,visual-plan,script-evidence}.md -Algorithm SHA256` as explicit PowerShell paths; direct publisher URLs and cited passages in the review receipt; `git diff --check`. The script still needs a focused repair and a new hash-bound delta check.

## Notes

`c090304` asserts that a durable piton is likelier to follow *more people* to the *same route*. S2 instead documents rising climbing participation and repeated piton placement/removal on popular routes. Its causal link is unsupported and echoes the preceding line. The matching visual inherits the implication. Verdict: HOLD only this line/shot; all other 82 lines passed the bounded source check, subject to unchanged bytes. The 480-second body is unproven and is a separate production STOP.
