---
id: 2026-10-02-wedding-competition-pilot-four-languages
title: Produce wedding competition pilot and four-language cast delivery
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-02T15:04:17Z
completed_at:
branch:
depends_on:
  - 2026-10-02-drama-competition-wedding-final
scope:
  - docs/videos/series-plans/competition-20261002
  - tools/video/dubs
  - tools/video/compile
  - apps/api/app/video_reviews/admin_service.py
---

# Produce wedding competition pilot and four-language cast delivery

## Why

The competition film needs four distinct character/narrator audio mixes and CC
under one YouTube video ID. Current drama dub CLI and backend reject cast dubs;
compilation does not deliver all foreign cast tracks. Planning cannot count as
media completion. The owner authorized USD 3,000 target plus USD 1,000 reserve;
views and actual production cost are evaluated separately after three months.

## Definition of done

- [ ] Pair the video tool without exposing keys; verify provider status and quota.
- [ ] Author and verify an executable pilot from the source-bound competition package.
- [ ] Produce/listen/revise Chinese cast auditions and a timed animatic; record actual cost.
- [ ] Render and review a representative 60-second pilot within USD 100, then E1-3 within cumulative USD 350 if accepted.
- [ ] Support locale x speaker casting, stable line IDs, translation revisions, measured per-line TTS timing and separate music/effects mix.
- [ ] Produce ja/ko/en pilot voice tracks and CC timed to each accepted track; get native listening.
- [ ] Compile matched-duration multi-language cast tracks and captions with stale-input invalidation and no Chinese speech underneath.
- [ ] Prove the target channel can attach four tracks to one video before scheduling the competition release.
- [ ] Continue full-film screenplay/production only with measured costs and bounded retakes; four languages complete before public launch.

## Steps

- [ ] Read `docs/videos/series-plans/competition-20261002/README.md`, handoff.json and production-readiness.md.
- [ ] Check current main, open PR #1132 and other active work before claiming code paths.
- [ ] Keep all media and live receipts outside Git; use the cost ledger for accepted and rejected paid outputs.
- [ ] Integrate multilingual drama capabilities rather than merely deleting rejection guards.
- [ ] Run focused tests for character voice routing, own-audio CC timing, stale sources, mix isolation and compilation joins.

## How to verify

Use the selected drama's source-bound review bundle and real pilot artifacts.
Document production-check, lint, real clip/voice measurements, human listening,
CC toggle/sync, identity/prop continuity, ledger receipts and player track switching
as separate outcomes. Text reviews or a passing JSON check cannot approve media.

## Notes

This task is filed, unclaimed and not executed by the preparation PR. Original
40-episode source and existing reviews remain intact. No global drama worker
activation or other-series generation is authorized by a pilot run. The owner has
already accepted the budget; only missing account pairing needs owner action.
Do not treat three months as ninety days, count Shorts views toward the main video,
or apply an unagreed weighted views/cost score.
