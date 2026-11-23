---
id: 2026-11-21-adopt-heimao-signature-emblem-and-subject
title: Adopt Heimao signature-emblem and subject-named headline thumbnail rules across Curio and So-Thats-Why
status: done
priority: P2
area: docs
owner: antigravity
claimed_at: 2026-11-21T07:07:04Z
created_at: 2026-11-21T07:05:47Z
completed_at: 2026-11-21T08:08:14Z
branch: antigravity/heimao-emblem-thumbnail-rules
depends_on: []
scope:
  - AGENTS.md
  - CLAUDE.md
  - GEMINI.md
  - docs/videos/so-thats-why/thumbnails.md
  - docs/videos/so-thats-why/dialogue-pilot-20261103/README.md
  - docs/videos/explainer-series/README.md
  - docs/videos/history-curiosity/README.md
  - tools/video/core/curio.mjs
  - tools/video/core/curio.test.mjs
  - docs/videos/curio-s10-v2
  - docs/videos/curio-s23-v2
  - docs/videos/curio-s24-v2
  - docs/videos/curio-s26-v2
  - docs/videos/curio-w01-dolby-licensing
---

# Adopt Heimao signature-emblem and subject-named headline thumbnail rules across Curio and So-Thats-Why

## Why

`curio-s10-v2` (Honno-ji) recorded `1.8%` organic CTR because its initial Heimao thumbnail hid the episode's subject behind a nameless demonstrative (`"這句話根本沒寫？"`) without an iconic emblem on the right. After reviewing 81 nine-locale (`zh-TW` + `en, ja, ko, es, pt, id, vi, th`) emblem-and-subject-named thumbnails across 9 episodes (`curio-s24-v2`, `curio-s25-v2`, `curio-s26-v2`, `curio-s13-v2`, `curio-w01-dolby-licensing`, `curio-s10-v2`, `curio-s23-v2`, `sothatswhy-p12-qr-code`, `curio-s14`), the owner approved updating all 9 episodes on `/admin/videos` and Google Drive and codifying the **Signature-Object (`特徵物` / 家徽 / 去文字卡通抽象標誌) + Subject-Named `headline` (`layout: "heimao-left"`)** standard permanently across both `奇聞檔案局` (`curio-*`) and `原來如此事務所` (`sothatswhy-*`).

## Definition of done

- [x] `tools/video/core/curio.mjs` (`heimaoSubjectWarnings` + `pacingWarnings`) warns when a `curio-*`, `sothatswhy-*`, or `story-*` Heimao thumbnail opens `headline` with a nameless pronoun/demonstrative (`這句話`, `這兩字`, `它`, `他`, `她`, etc.) instead of naming the subject up front, covered by unit tests in `tools/video/core/curio.test.mjs`.
- [x] `AGENTS.md` (and byte-identical `CLAUDE.md` + `GEMINI.md`), `docs/videos/so-thats-why/thumbnails.md`, `docs/videos/explainer-series/README.md`, `docs/videos/so-thats-why/dialogue-pilot-20261103/README.md`, and `docs/videos/history-curiosity/README.md` codify the 2026-11-20 rules: default `layout: "heimao-left"`, mandatory subject name in `headline` across all 9 locales, the 4-tier signature-object funnel (including green-light wordless cartoonized/abstract brand geometry & trade-dress colors vs red-light ban on copyrighted IP mascots/characters), and the hybrid `generate_image` base + precision vector SVG `<workdir>/stock/<sha256>.jpg` + `thumbnail.replaces` workflow.
- [x] Collision-free episode manifests (`curio-s10-v2`, `curio-s23-v2`, `curio-s24-v2`, `curio-s26-v2`, `curio-w01-dolby-licensing`) carry the approved 9-locale `heimao-left` emblem `video.json` (`thumbnail.replaces` + `stock/<sha256>.jpg`) and `i18n/*.json` (`thumbnail` + `source_hashes.thumbnail`), while all 9 episodes are backed up to Google Drive (`epDir` + `workDir`, archiving replaced thumbnails under `_舊版/20261120_pre_emblem/`) and synced to `/admin/videos` (`publish` + `languages`).
- [x] `npm run test:tools && npm run test:docs-videos && npm run check:tasks` pass.

## Steps

- [x] Implement `heimaoSubjectWarnings` in `tools/video/core/curio.mjs` and unit tests in `tools/video/core/curio.test.mjs`.
- [x] Codify the 2026-11-20 emblem & subject-named headline specification across `docs/videos/so-thats-why/thumbnails.md`, `docs/videos/explainer-series/README.md`, `docs/videos/so-thats-why/dialogue-pilot-20261103/README.md`, `docs/videos/history-curiosity/README.md`, and byte-identical `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`.
- [x] Sync the 5 collision-free episode directories in git (`curio-s10-v2`, `curio-s23-v2`, `curio-s24-v2`, `curio-s26-v2`, `curio-w01-dolby-licensing`), back up all 9 episodes to Google Drive, and push `publish` + `languages` reviews for all 9 episodes to `/admin/videos`.
- [x] Verify `npm run test:tools && npm run test:docs-videos && npm run check:tasks`.

## How to verify

```bash
npm run test:tools && npm run test:docs-videos && npm run check:tasks
```

## Notes

- Claimed with `--force` over 5 verified stale (`> 24h`, 45h–904h old, zero active worktrees or open PRs) claims: `2026-10-14-curio-episodes-keep-the-series-look`, `2026-10-30-three-brand-stories-move-to-curio`, `2026-10-31-curio-burns-zh-tw-subtitles-in`, `2026-11-03-sothatswhy-dialogue-pilot-p02`, and `2026-11-19-heimao-titles-and-retitle-batch`.
- Scoped carefully to avoid any file overlap with active open PRs `#2186` (`curio-s13-v2`, `curio-s14`, `curio-episode/SKILL.md`, `lessons/{curio,explainer}.md`), `#2191` (`sothatswhy-{g653,g712,p25}`), `#2183` (`shorts-drama`, `rules-sync`), and `#2117` (`curio-s25-v2/i18n/{es,vi}.json`). All 9 episodes (`curio-s14`, `curio-s24-v2`, `curio-s25-v2`, `curio-s26-v2`, `curio-s13-v2`, `curio-w01-dolby-licensing`, `curio-s10-v2`, `curio-s23-v2`, `sothatswhy-p12-qr-code`) have their updated `video.json`, `i18n/*.json`, `<workdir>/stock/<sha256>.jpg`, and 9-locale JPEGs backed up on Google Drive and pushed to `/admin/videos`.
