---
id: 2026-11-24-plan-10-season-western-sci-fi
title: Plan 10-season Western sci-fi AI drama series Glass Meridian (120 episodes)
status: done
priority: P2
area: docs
owner: antigravity
claimed_at: 2026-11-24T08:45:21Z
created_at: 2026-11-24T08:45:08Z
completed_at: 2026-11-24T09:16:23Z
branch: antigravity/glass-meridian-10-season-plan
depends_on: []
scope:
  - docs/videos/series-plans/glass-meridian
---

# Plan 10-season Western sci-fi AI drama series Glass Meridian (120 episodes)

## Why

The owner requested an original Western Netflix-style photorealistic live-action AI sci-fi drama targeting 10 seasons with relentless binge hooks, structured in YouTube/streaming high-density format (12 episodes per season × ~8 min, compiling cleanly into ~96-min season movies) with English-primary multi-accent audio and 8-language subtitles/dubs.

## Definition of done

- [x] Complete 10-season, 120-episode planning package exists under `docs/videos/series-plans/glass-meridian/` with `plan.json`, `authoring-contract.json`, `setting.json`, `season-01.json`–`season-10.json`, generated Markdown/CSV/JSON/manifest deliverables, and `README.md`.
- [x] Automated build parity (`build.mjs --check`), structural & continuity validator (`validate.mjs`), and unit tests (`validate.test.mjs`) all pass offline with zero errors.
- [x] `npm run check:tasks` passes.

## Steps

- [x] Lock owner-approved creative & format spec (`Glass Meridian`, live-action cinematic, 10 seasons × 12 episodes × ~8 min, English primary + 8 languages).
- [x] Author `plan.json`, `authoring-contract.json`, `setting.json` (world rules, 5 factions, 12 cast profiles with AI visual/accent anchors, 12 mystery threads, closed finale).
- [x] Author all 10 seasons (`season-01.json` through `season-10.json`, E001–E120) with strict cliffhanger alternation, two high-tension beats per episode, mystery ledger continuity, and irreversible death enforcement.
- [x] Implement `build.mjs`, `validate.mjs`, `validate.test.mjs`, and `README.md`, generate derived files, and verify all checks pass.

## How to verify

```bash
node docs/videos/series-plans/glass-meridian/build.mjs --check
node docs/videos/series-plans/glass-meridian/validate.mjs
node --test docs/videos/series-plans/glass-meridian/validate.test.mjs
npm run check:tasks
```

## Notes

- Zero media generated, zero paid API calls, and `production_support.ready_for_import` remains `false`.
- Next production gate (separate ticket/phase): `animation-preproduction` lock for S1E01 (`180 Seconds`) with 6 cast reference sheets, 4 Season 1 master location sheets, and a 3-shot pilot before spending credits on full Season 1 production.
