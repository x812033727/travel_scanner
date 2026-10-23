---
id: 2026-10-23-c19-seven-bank-v4-blind-a
title: C19 Seven Bank v4 context-exposed narrator-only narrative review
status: review
priority: P2
area: docs
owner: codex-c19-v4-blind-a
claimed_at: 2026-10-23T07:25:15Z
created_at: 2026-10-23T07:25:11Z
completed_at:
branch: codex/c19-seven-bank-v4-blind-a
depends_on: []
scope:
  - docs/videos/story-everyday-seven-bank-c19/reviews/context-exposed-narrative-review-v4.md
  - tasks/open/2026-10-23-c19-seven-bank-v4-blind-a.md
---

# C19 Seven Bank v4 context-exposed narrator-only narrative review

## Why

The latest C19 script requires editorial readback after two source-scope repairs. The reviewer inherited the parent conversation, which already exposed earlier C19 review outcomes, so this review does not satisfy an independent blind gate.

## Definition of done

- [x] Twelve required narrative checks are locked on the exact v4 narrator-only projection before inspecting the author files in this subtask.
- [x] A hash-bound, context-exposed receipt identifies each PASS/HOLD and the exact repair target without claiming independent blind status.

## Steps

- [x] Hash and read only the 79-line projection; write an external lock.
- [x] Verify author HEAD, Git blob, file SHA-256, and all 79 `(ID, narration)` pairs after locking.
- [x] Commit the receipt on a separate branch and open a draft review PR.

## How to verify

`Get-FileHash -Algorithm SHA256` on projection, external lock and author script; 79-row parser and `Compare-Object` reported zero mismatches; `git diff --check`; `npm run check:tasks`. Source and visual verification remain a separate independent review.

## Notes

Locked projection SHA-256 `99D990690BE8E5757CB7C9580CF7DCAD7D26CCC6E4B7FC0B7F2C5ADBA7CE0590`; external lock SHA-256 `51B15B1A81F3490D6982526DA0E963B15CD014AC395ED30CC2833F24FC9B13FF`; author head `c1fe8f9daa667712f9be9e6746148f05ad39f89f`. Context-exposed reviewer HOLD: `no_recap` at `c190610`, which restates `c190301`–`c190313`. Eleven other required checks PASS. This receipt does not count toward either required independent blind read; two fresh readers without inherited C19 context are needed on the final narration.

Draft review PR: https://github.com/x812033727/travel_scanner/pull/1762 (`no-auto-merge`).
