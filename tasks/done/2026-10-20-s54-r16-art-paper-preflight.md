---
id: 2026-10-20-s54-r16-art-paper-preflight
title: S54 R16 art paper preflight
status: done
priority: P2
area: docs
owner: s54_art_paper_preflight
claimed_at: 2026-10-20T23:35:29Z
created_at: 2026-10-20T23:35:27Z
completed_at: 2026-10-20T23:37:38Z
branch: codex/curio-preproduction-s46-s56-20261020
depends_on: []
scope:
  - docs/videos/curio-s54/review/r16-art-paper-preflight.md
---

# S54 R16 art paper preflight

## Why

S54 R16 has verified narration but no generated illustrations. Three historically sensitive scenes need a bounded, source-aware image plan and a full-episode price before any paid call.

## Definition of done

- [x] A written three-scene MiniMax pilot with exact R16 visual binding, native-image acceptance rules, STOP condition and cumulative episode cap exists without modifying frozen creative files.

## Steps

- [x] Read the Curio workflow, R16 source and audio receipts, prior paper preflights and current media quote.
- [x] Draft source-safe candidate prompts and staged pilot rules for independent written review.
- [x] Verify lint, video docs, tasks and diff checks.

## How to verify

`node tools/video/cli.mjs lint --slug curio-s54 --json`; `npm run test:docs-videos`; `npm run check:tasks`; `git diff --check`; `git diff --no-index --check /dev/null docs/videos/curio-s54/review/r16-art-paper-preflight.md`.

## Notes

Current `visualHash` `ba9a43292268b35b`; 138 shots. 2026-10-20 23:35 UTC server dry-runs quote up to US$5.59 for three takes per shot plus about US$0.08 music; zero S54 ledger spend. Live quotas are judge 20,059/30,000 and music 62/100, higher than the older exhausted snapshot. Site outline/script/audio cards remain pending. No paid media generated or site approval asserted. Written candidate needs independent review before adoption.
