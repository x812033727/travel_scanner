---
id: 2026-09-29-bind-shared-shorts-narration-and-qa
title: Bind shared Shorts narration and QA receipts to current script inputs
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-29T02:00:49Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts/check.mjs
  - tools/video/shorts/qa.mjs
  - tools/video/shorts/push.mjs
---

# Bind shared Shorts narration and QA receipts to current script inputs

## Why

The shared Shorts CLI can reuse stale evidence when a build directory is edited in place. `audioHash` covers ordered WAV bytes, while `narrationItem` checks only that hash and phrase counts; changed narration text with the same count is not compared with `check.results`. `push` binds QA to the final video hash but not the script or other QA inputs, so a metadata-only script edit can carry an older policy/metadata verdict. The dated 2026-09-29 correction helper rejects both cases for that release; the shared commands still need equivalent protection.

## Definition of done

- [ ] Changing a phrase while retaining the same WAV bytes and phrase count invalidates its narration check.
- [ ] Changing the script, facts receipt, narration check or layout measurement invalidates QA at push time, even when the MP4 is unchanged.
- [ ] Existing valid builds have a documented regeneration/migration path, and actual failed checks remain failed.

## Steps

- [ ] Recheck active Shorts tool branches and PRs before claiming this scope; coordinate with their owners.
- [ ] Add explicit input bindings to the shared check/QA/push flow without relaxing any gates.
- [ ] Add regression tests for same-count text edits, metadata-only edits and changed check/verify inputs.

## How to verify

Create a valid build fixture, change only narration words while leaving WAV bytes and count fixed, and require narration failure. Separately change only description text after successful QA and require push to reject the stale report before any API write. Run the focused Shorts tests and relevant tools checks.

## Notes

- Found by independent review during the owner-authorized correction of 15 live Shorts on 2026-09-29.
- See `docs/videos/ai-shorts/corrections-20260929/operations/review.mjs` for a dated guard: it compares exact phrase text and binds script/final/QA/check/verify/checks hashes. This is evidence of the desired behavior, not a reason to duplicate that helper wholesale.
- Not claimed: shared Shorts tool work was active in another worktree/PR. The current correction used isolated dated tooling and did not edit those shared files.
