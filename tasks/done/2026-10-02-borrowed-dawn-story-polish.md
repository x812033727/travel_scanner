---
id: 2026-10-02-borrowed-dawn-story-polish
title: Audit and improve Borrowed Dawn story delivery
status: done
priority: P2
area: docs
owner: codex-borrowed-dawn
claimed_at: 2026-10-02T13:42:07Z
created_at: 2026-10-02T13:42:04Z
completed_at: 2026-10-02T13:54:40Z
branch: codex/borrowed-dawn-story-polish
depends_on: []
scope:
  - docs/videos/series-plans/borrowed-dawn
---

# Audit and improve Borrowed Dawn story delivery

## Why

The owner requested an audit and optimization of Borrowed Dawn. Its source package is structurally sound, but repeated novice mistakes and rescue situations, abstract policy scenes and thin everyday bonds weaken the intended ensemble story. Correct the effective-rest and family-time details without changing the original length or closed ending.

## Definition of done

- [x] Key scenes show character choices through concrete actions and costs, with everyday bonds established before irreversible losses.
- [x] All 120 episodes, twelve mysteries, the 22-minute body, the 30-minute slot and the closed finale are preserved.
- [x] Source JSON, readable chapters, document bundle and manifest agree, and existing regression checks pass.
- [x] The prior independent review is preserved as history; the new author review and production limitations are explicit.

## Steps

- [x] Check branches, worktrees, remote heads, open PRs and live claims for overlapping source work.
- [x] Read the full 120-event plan and the original independent review; identify continuity and presentation weaknesses.
- [x] Improve motives, key actions, bonds, restraint, family choices and climax costs in source JSON.
- [x] Separate paused planning import support from full media production in the README and review.
- [x] Rebuild derived files and run the existing plan tests, hash checks and task validation.
- [x] Review the complete diff, record outcomes and prepare a draft PR without merging or production writes.

## How to verify

Run node docs/videos/series-plans/borrowed-dawn/build.mjs --check, node docs/videos/series-plans/borrowed-dawn/validate.mjs, node --test docs/videos/series-plans/borrowed-dawn/validate.test.mjs and npm run check:tasks. Check that irreversible outcomes, timeline, world rules, thread endpoints and episode lengths are unchanged. Inspect the derived chapters for the actual revised text.

## Notes

Started from origin/main after PR #1113 and paused-planning import PR #1125 landed. No active claim or open PR overlaps this package. Baseline build check and validator pass, and all 19 existing tests pass. This is an authored planning revision; no full screenplay, animation, audio, media acceptance, production import, worker activation or publication is implied. The prior independent PASS is historical and does not certify this new author revision.

Final source: 47 episodes contain story changes beyond punctuation/terminology cleanup. The 17 generated files rebuild consistently, validator reports zero errors, all 19 regression tests pass and check:tasks validates 1298 tickets with exit 0 (existing unrelated stale/overlap warnings). A one-time field comparison against the starting HEAD additionally confirms every episode's identity/time/cast/location/thread schedule/ending type/tension and the world, timeline, twelve mysteries, finale and runtime policies are preserved. No media files or external-host writes were created.
