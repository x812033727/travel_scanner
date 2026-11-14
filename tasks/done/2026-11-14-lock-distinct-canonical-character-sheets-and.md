---
id: 2026-11-14-lock-distinct-canonical-character-sheets-and
title: Lock distinct canonical character sheets and object-shot balance for sothatswhy and curio
status: done
priority: P2
area: docs
owner: antigravity-explainer-canon
claimed_at: 2026-11-14T15:56:35Z
created_at: 2026-11-14T15:56:10Z
completed_at: 2026-11-14T16:12:01Z
branch: antigravity/explainer-series-character-canon-shot-mix
depends_on: []
scope:
  - AGENTS.md
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - docs/videos/explainer-series/README.md
  - docs/videos/history-curiosity/look.md
  - docs/videos/history-curiosity/series-sheets
  - docs/videos/lessons/explainer.md
  - docs/videos/lessons/sothatswhy.md
  - docs/videos/rules-sync/manifest.tsv
  - docs/videos/rules-sync/watch.txt
  - docs/videos/so-thats-why/CURRENT.md
  - docs/videos/so-thats-why/dialogue-pilot-20261103/HANDOFF.md
  - docs/videos/so-thats-why/dialogue-pilot-20261103/README.md
  - docs/videos/so-thats-why/dialogue-pilot-20261103/SCORECARD.md
  - docs/videos/so-thats-why/look.md
  - docs/videos/so-thats-why/series-sheets
---

# Lock distinct canonical character sheets and object-shot balance for sothatswhy and curio

## Why

Other sessions producing `原來如此事務所` (`sothatswhy-*`) and `奇聞檔案局` (`curio-*`) episodes drew inconsistent or awkward character designs ("別的對話畫得怪怪的") and overstuffed characters into nearly every shot ("也不一定每一個畫面要都有人"):

1. `docs/videos/so-thats-why/series-sheets/characters/` previously only contained two legacy MiniMax `image-01` sheets marked `judge.passed: false` (`0c3a400c8e981d84.png` where Chief's ear-pencil looked like a dangling earring, and `f8dac008f296a6a3.png` where Kid had half-closed eyes and fingerless nubs), while `奇聞檔案局` had zero canonical reference sheet committed in git. Under the upgraded theatrical-gouache `generate_image` workflow, sessions without clean canonical PNGs in `ImagePaths` or explicit head-to-body ratios drifted into 6–7-head realistic adults or mixed up the two series ("奇聞就是另外一個造型的人，兩系列不同").
2. Legacy MiniMax `image-01` guidance discouraged empty/object-only scenes (because MiniMax hallucinated faces onto objects), causing episodes to put talking-head characters in 65%–80% of frames instead of letting mechanisms and props fill the screen.

## Definition of done

- [x] Commit clean `1376x768` theatrical-gouache canonical character reference PNGs in git for both series with unmistakably distinct proportions and silhouettes:
  - `原來如此事務所` (**2.5-head chibi**): `docs/videos/so-thats-why/series-sheets/characters/chief/chief-canon-v2.png` (clean bare ears with legacy ear-pencil removed, silver-streaked low side ponytail, bold round black glasses, mustard knitted cardigan over white shirt) and `docs/videos/so-thats-why/series-sheets/characters/kid/kid-canon-v2.png` (glossy black bob with cowlick, wide-open bright round dark brown eyes, ink-navy toggle raincoat with bright yellow hood down, empty hands).
  - `奇聞檔案局` (**3.5-head slender theatrical anime**): `docs/videos/history-curiosity/series-sheets/characters/ada/ada-canon-v2.png` (silent archive investigator Ada with wavy black chin-length bob + side-parted fringe, thin crimson-red round glasses, muted-teal double-breasted trench coat over parchment-cream turtleneck).
- [x] Document mandatory `ImagePaths` canonical PNG paths, exact English character prompt locks, and strict cross-series separation across `series-sheets/README.md`, `look.md`, `dialogue-pilot-20261103/{README.md,SCORECARD.md,HANDOFF.md}`, `CURRENT.md`, `explainer-series/README.md`, `.agents/skills/curio-episode/SKILL.md` (and byte-identical `.claude/skills/curio-episode/SKILL.md`), and `AGENTS.md`.
- [x] Lock the shot-mix rule across both explainer series: ~**45%–65% `nobody: true` pure mechanism / object / prop / environment shots** vs ~**35%–55% character shots** reserved for opening hooks, questions, discoveries, turns, and closing beats.
- [x] Register `docs/videos/history-curiosity/series-sheets/*.md` in `docs/videos/rules-sync/{watch.txt,manifest.tsv}`, record root causes in `docs/videos/lessons/{explainer.md,sothatswhy.md}`, and pass `npm run test:tools`, `npm run test:docs-videos`, and `npm run check:tasks`.

## Steps

- [x] Generate and visually audit 2×-zoom details (eyes, ears, glasses, fingers, proportions) of `chief-canon-v2.png`, `kid-canon-v2.png`, and `ada-canon-v2.png`.
- [x] Create `docs/videos/history-curiosity/series-sheets/README.md`, update `docs/videos/so-thats-why/series-sheets/README.md`, and register the new rules-sync entry in `watch.txt` and `manifest.tsv`.
- [x] Update `look.md`, `explainer-series/README.md`, `dialogue-pilot-20261103/{README.md,SCORECARD.md,HANDOFF.md}`, `CURRENT.md`, `.agents/skills/curio-episode/SKILL.md`, `.claude/skills/curio-episode/SKILL.md`, `AGENTS.md`, and `docs/videos/lessons/{explainer.md,sothatswhy.md}`.
- [x] Run `npm run test:tools`, `npm run test:docs-videos`, and `npm run check:tasks`, then close task in PR with `npm run tasks -- done`.

## How to verify

```bash
npm run test:tools && npm run test:docs-videos && npm run check:tasks
```

## Notes

- Claimed with `--force` per `task-board` Rule 2 because `AGENTS.md` and `.agents/skills/curio-episode/SKILL.md` overlapped only with 7 stale tasks from `2026-10-10` through `2026-11-03` (>260h stale, `[not found anywhere]` in `who-is-on-it.mjs`). Active open PR `#2107` carries `no-auto-merge` and is `DIRTY`.
- Legacy `0c3a400c8e981d84.png`, `f8dac008f296a6a3.png`, and `characters/index.json` are intentionally preserved alongside `chief-canon-v2.png` / `kid-canon-v2.png` so historical episodes using `tools/video/media/series-store.mjs` hash lookups remain backwards-compatible while all new generations pass the `-canon-v2.png` sheets via `ImagePaths`.
- Verified zero overlap with files hash-pinned in `docs/videos/long-form/review.json`.
