---
id: 2026-10-20-curio-s49-selected-art-second-look
title: Curio S49 selected art second look
status: done
priority: P2
area: docs
owner: codex-s49-native-art-second-look
claimed_at: 2026-10-20T20:34:53Z
created_at: 2026-10-20T20:34:50Z
completed_at: 2026-10-20T20:36:37Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s49/review/r15-native-art-second-look.md
---

# Curio S49 selected art second look

## Why

The first 14 S49 Moon Hoax keyframes have selected takes, but machine ratings and prior visual notes cover earlier prompts or earlier selected files. A fresh human check must identify which exact current images are safe to use before further paid art work.

## Definition of done

- [x] Independent scene-by-scene visual review of the 14 exact selected JPEGs against current prompt and narration, saved in `docs/videos/curio-s49/review/r15-native-art-second-look.md`.

## Steps

- [x] Inspect every selected image and verify its SHA against the selection manifest.
- [x] Distinguish stale takes and real child/modern artifacts from chibi adult proportions; record accept/hold and actionable corrections.

## How to verify

Read the review and compare its 14 file paths with `/workspace/.video-work/curio-s49/keyframes/manifest.json`. `git diff --check` and `npm run check:tasks` should pass.

## Notes

Nine selected scenes are visually acceptable. `moon007/013/014` are stale images generated against prior prompts and require redraw; `moon010/012` need zero-cost bottom-edge cleanup and rejudging before a final pass. Current `video.json` SHA-256: `6ccd5b19ae2e0eb0548f5647fdf631f35b983d160027eb6c401832fe2a55476e`; current selection manifest SHA-256: `d01bd6cd544148bde80bc7d037123e7f1af02805bcc6d4827087445c61d1a49c`.
