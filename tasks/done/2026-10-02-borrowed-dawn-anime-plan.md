---
id: 2026-10-02-borrowed-dawn-anime-plan
title: Borrowed Dawn anime series planning package
status: done
priority: P2
area: docs
owner: codex-root
claimed_at: 2026-10-02T04:31:51Z
created_at: 2026-10-02T04:31:43Z
completed_at: 2026-10-02T05:15:46Z
branch: codex/borrowed-dawn-anime-plan
depends_on: []
scope:
  - docs/videos/series-plans/borrowed-dawn
---

# Borrowed Dawn anime series planning package

## Why

The owner asked to file the original isekai series The Borrowed Dawn under the anime category introduced by PR #1110, then explicitly requested a separate PR. The discussion has a world bible, 10 seasons / 120 episodes and two audit rounds, but no reviewable repository package. Preserve the intended long episode specification and original closed ending instead of forcing current short-drama inputs.

## Definition of done

- [x] The original setting, season outline and all 120 episode plans are saved as anime-classified source JSON with readable generated Markdown.
- [x] Every episode preserves two concrete high-tension beats, continuing consequences and traceable foreshadowing; the latest corrections appear in their actual episodes.
- [x] Local integrity checks and independent narrative review cover the complete package; production support gaps are recorded honestly.
- [x] A separate draft PR contains only the owned planning package and task records, without duplicating PR #1110's category implementation.

## Steps

- [x] Inspect PR #1110, current series document contracts and production constraints; check task/branch/PR collisions and claim this narrow scope.
- [x] Record anime category, anime-2d defaults, the world rules, cast, mysteries and original duration in plan/setting JSON.
- [x] Integrate ten seasons and both audit rounds; derive readable documents, continuity ledger and manifest.
- [x] Run source/derived validation, mutation regressions and task checks; resolve independent review findings.
- [x] File a separate draft PR with exact validation and production limitations.

## How to verify

node docs/videos/series-plans/borrowed-dawn/build.mjs --check
node docs/videos/series-plans/borrowed-dawn/validate.mjs
node --test docs/videos/series-plans/borrowed-dawn/validate.test.mjs
npm run check:tasks

## Notes

PR #1110 is an independently owned category change, still open when inspected. Anime is a video category, not a new series kind or long-duration policy. This package is local planning content, not a SeriesIn request or 120 complete 22-minute scripts. Current gaps are recorded in plan.json and the unclaimed follow-up 2026-10-02-anime-long-episode-support. No production import, activation, provider call, media generation or publication is part of this task. The existing checkout is used; no worktree was created.

All 120 episodes now have two event-based tension beats (240 total) and 46 distinct five-stage tension profiles. Cross-season chronology totals 56 months before the eight-year coda. Corrected the siege transition, flood rescue season, original-world receiver arrangements, permanent losses, true-rest accounting, separate responsibility cases and the episode 92 → 97 instrument funding consequence.

Validation: build --check reproduces all 17 generated files; complete source/derived/hash validation reports 0 errors; 19 mutation regressions and 54 existing series/schema tests pass. npm run check:tasks passes with existing stale-claim/scope-overlap warnings. The actual-worker comparison intentionally exposes custom-retention and closed-finale gaps rather than treating structural document shape as production readiness. A separate read-only tooling review found no deterministic-build or document/manifest integration blocker.

Independent narrative review read all 120 source episode plans and rechecked the corrected events in generated Markdown. Its final finding is PASS for planning/content consistency, with production and import explicitly NOT READY. Full detail and review limits are saved in review.md. Opened separate draft PR #1113: https://github.com/x812033727/travel_scanner/pull/1113. The branch was advanced to origin/main b11e01eb6 before filing; no collision or duplicate content PR was found.
