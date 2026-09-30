---
id: 2026-09-29-bind-shared-shorts-narration-and-qa
title: Bind shared Shorts narration and QA receipts to current script inputs
status: done
priority: P2
area: tools
owner: codex-shorts-evidence
claimed_at: 2026-09-30T00:01:58Z
created_at: 2026-09-29T02:00:49Z
completed_at: 2026-09-30T00:12:26Z
branch: codex/shorts-evidence-bindings
depends_on: []
scope:
  - tools/video/shorts/check.mjs
  - tools/video/shorts/qa.mjs
  - tools/video/shorts/push.mjs
  - tools/video/shorts/pipeline.test.mjs
  - tools/video/shorts/bindings.test.mjs
  - docs/videos/SHORTS.md
---

# Bind shared Shorts narration and QA receipts to current script inputs

## Why

The shared Shorts CLI can reuse stale evidence when a build directory is edited in place. `audioHash` covers ordered WAV bytes, while `narrationItem` checks only that hash and phrase counts; changed narration text with the same count is not compared with `check.results`. `push` binds QA to the final video hash but not the script or other QA inputs, so a metadata-only script edit can carry an older policy/metadata verdict. The dated 2026-09-29 correction helper rejects both cases for that release; the shared commands still need equivalent protection.

## Definition of done

- [x] Changing a phrase while retaining the same WAV bytes and phrase count invalidates its narration check.
- [x] Changing the script, facts receipt, narration check or layout measurement invalidates QA at push time, even when the MP4 is unchanged.
- [x] Existing valid builds have a documented regeneration/migration path, and actual failed checks remain failed.

## Steps

- [x] Recheck active Shorts tool branches and PRs before claiming this scope; coordinate with their owners.
- [x] Add explicit input bindings to the shared check/QA/push flow without relaxing any gates.
- [x] Add regression tests for same-count text edits, metadata-only edits and changed check/verify inputs.

## How to verify

Create a valid build fixture, change only narration words while leaving WAV bytes and count fixed, and require narration failure. Separately change only description text after successful QA and require push to reject the stale report before any API write. Run the focused Shorts tests and relevant tools checks.

## Notes

- 2026-09-30: Claimed by codex-shorts-evidence from main cb4d0b44.
  `--force` bypasses only the stale broad scope of
  `2026-09-28-sothatswhy-shorts-from-episode`: its implementation merged in
  PR #904 and its remaining step is the separately tracked real pilot render.
  Local and remote branches have no unmerged implementation on check/qa/push;
  open PRs #990 and #991 cover unrelated documents. The other ticket is unchanged.
  Scope includes focused regression tests and the existing Shorts migration docs.
- Completed: narration receipts bind exact ordered text and WAVs; QA records a
  versioned map of local input hashes (including explicit missing files), rejects
  edits during its async work, and push rechecks before writes and review submits.
  A returned approval must carry the exact submitted QA report, preserving both
  fresh failures and explicit owner approval of that current report.
- Validation with the bundled Node 24.19.0: pipeline suite 35 passed; binding suite
  30 passed; full `npm run test:tools` 876 passed, 2 skipped, 0 failed (878 total).
  `npm run check:tasks` and `git diff --check` passed. The default Node 24.13.0
  full run had 26 test-file failures; no tests were weakened or
  excluded to obtain the successful supported-runtime result.
- Independent code review identified the API's existing reuse of a decided
  MP4 review despite new QA evidence. The client now stops that stale approval
  before publish; server renewal is explicitly tracked in
  `2026-09-30-shorts-renew-decided-qa-review`. Migration caveats are documented
  in docs/videos/SHORTS.md. No service credentials or production writes were used.
- Pre-PR collision recheck: open PRs #990/#991 remain unrelated docs work;
  matching local/remote Shorts branches contain no competing unmerged change
  to these shared check/QA/push files.

- Found by independent review during the owner-authorized correction of 15 live Shorts on 2026-09-29.
- See `docs/videos/ai-shorts/corrections-20260929/operations/review.mjs` for a dated guard: it compares exact phrase text and binds script/final/QA/check/verify/checks hashes. This is evidence of the desired behavior, not a reason to duplicate that helper wholesale.
- Not claimed: shared Shorts tool work was active in another worktree/PR. The current correction used isolated dated tooling and did not edit those shared files.
