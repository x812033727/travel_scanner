---
id: 2026-10-02-borrowed-dawn-continuity-followup
title: Audit Borrowed Dawn travel handoffs and permanent injury continuity
status: done
priority: P2
area: docs
owner: codex-borrowed-dawn
claimed_at: 2026-10-02T14:09:20Z
created_at: 2026-10-02T14:07:08Z
completed_at: 2026-10-02T14:15:06Z
branch: codex/borrowed-dawn-story-polish
depends_on: []
scope:
  - docs/videos/series-plans/borrowed-dawn
---

# Audit Borrowed Dawn travel handoffs and permanent injury continuity

## Why

The owner requested a second audit of the revised Borrowed Dawn plan. Several returning characters need ordinary travel and handover details; some post-injury rescue descriptions leave Oren's load-bearing limits ambiguous, and episode 84 wrongly suggests that resumed work cancels previously earned debt repayment.

## Definition of done

- [x] Care and craft duties have verified successors before Lyne, Nale and Tara travel; gate-window handover and later arrival are planned rather than instantaneous.
- [x] Oren's later actions preserve mobility and grip limits, ordinary assistance and legal supervision.
- [x] Episode 84 preserves already-earned effective-rest repayment and describes remaining debt and new load correctly.
- [x] Generated files, existing regression tests and task validation pass; include the revision in the same draft PR.

## Steps

- [x] Check live claims, local/worktree branches, remote heads and open PRs for collisions.
- [x] Read the revised character arcs and the affected episodes with their before/after states.
- [x] Revise source and append an accurately scoped author review without claiming independent acceptance.
- [x] Rebuild, validate, inspect the diff and record checks before closing within PR #1131.

## How to verify

Run node docs/videos/series-plans/borrowed-dawn/build.mjs --check, node docs/videos/series-plans/borrowed-dawn/validate.mjs, node --test docs/videos/series-plans/borrowed-dawn/validate.test.mjs and npm run check:tasks. Compare episode identities, times, casts, locations, threads, tension/ending types and core world/runtime/finale policies with the starting HEAD.

## Notes

The only open PR touching this package is our existing draft #1131; no active claim overlaps it. Ten episodes are revised: 73, 75, 77, 81, 84, 85, 96, 98, 106 and 112. A one-time preservation comparison passes for all 120 episodes and unchanged core policies. Reko's episode 78 already describes long-term ship repair before sailing, so it is not treated as a missing repair. Geographic staging and exact journey durations remain screenplay work; no new transport magic or medical cure is introduced. No production readback, imports, worker activation, paid media or publishing is involved.

All 19 existing tests pass, build --check confirms 17 generated files, the validator reports zero errors across 120 episodes, and check:tasks validates 1299 files with exit 0 and existing unrelated warnings. The complete source diff was reviewed. README now distinguishes historical independent review from subsequent author checks. Review/README hash changes are rebuilt and checked again before committing.
