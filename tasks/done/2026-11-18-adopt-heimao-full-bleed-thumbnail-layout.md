---
id: 2026-11-18-adopt-heimao-full-bleed-thumbnail-layout
title: Adopt Heimao full-bleed thumbnail layout and rules for Curio and So-Thats-Why
status: done
priority: P2
area: tools
owner: antigravity-heimao-thumbs
claimed_at: 2026-11-18T11:42:32Z
created_at: 2026-11-18T11:42:06Z
completed_at: 2026-11-18T12:00:01Z
branch: claude/explainer-heimao-thumbnail-rules
depends_on: []
scope:
  - AGENTS.md
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
  - tools/video/qa/thumbnail.mjs
  - tools/video/qa/thumbnail.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/explainer-cute.test.mjs
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - docs/videos/so-thats-why/thumbnails.md
  - docs/videos/so-thats-why/dialogue-pilot-20261103/README.md
  - docs/videos/explainer-series/README.md
  - docs/videos/lessons/explainer.md
---

# Adopt Heimao full-bleed thumbnail layout and rules for Curio and So-Thats-Why

## Why

Recent `奇聞檔案局` (`curio-*`) and `原來如此事務所` (`sothatswhy-*`) thumbnails used narrow split panels (`layout: "e"` and `subject: "right"`) that repeatedly defaulted to a standing portrait of `Ada` or `Kid`, making episodes look nearly identical in YouTube mobile feeds and giving iconic subject objects too little room. After studying authentic high-CTR `黑猫研究院` (`@qiqiqushi0`) thumbnails and reviewing full-bleed prototypes, the owner approved adopting the full-bleed bright top-headline + "giant iconic object/symbol + dramatic conflict or character reaction" formula (`thumbnail.data.layout: "heimao"` / `"heimao-left"`) across both explainer series.

## Definition of done

- [x] `tools/video/templates/templates.mjs` supports `thumbnail.data.layout: "heimao"` (top-center) and `"heimao-left"` (top-left) for both `curio-*` and `sothatswhy-*`, rendering full-bleed `1280x720` thumbnails with 1-line `#FFE600` yellow bold black-stroked `headline` + 1-line `#FFFFFF` white bold black-stroked `sub`, rejecting `subject` narrowing, and omitting stamps, pills, and bottom dark scrims while leaving all existing layouts byte-for-byte unchanged.
- [x] `tools/video/qa/thumbnail.mjs` and `tools/video/core/lint.mjs` validate `heimao` / `heimao-left` headlines against the 1-line `<= 10` unit rule (`zh-TW`) and `>= 24 px` phone-width readability across all locales.
- [x] Thumbnail rules and lessons are updated across `AGENTS.md`, `.agents/skills/curio-episode/SKILL.md` (and mirrored byte-for-byte to `.claude/skills/curio-episode/SKILL.md`), `docs/videos/so-thats-why/thumbnails.md`, `docs/videos/so-thats-why/dialogue-pilot-20261103/README.md`, `docs/videos/explainer-series/README.md`, and `docs/videos/lessons/explainer.md`.
- [x] `npm run test:tools` and `npm run check:tasks` pass.

## Steps

- [x] Implement `THUMB_HEIMAO_LAYOUT` (`"heimao"`) and `THUMB_HEIMAO_LEFT_LAYOUT` (`"heimao-left"`) in `tools/video/templates/templates.mjs` with unit tests in `templates.test.mjs` and `explainer-cute.test.mjs`.
- [x] Update `headlineRule` / `thumbnailChecks` in `tools/video/qa/thumbnail.mjs` and `thumbnailHeadlineProblems` in `tools/video/core/lint.mjs` with unit tests in `qa/thumbnail.test.mjs` and `core/lint.test.mjs`.
- [x] Update repository rules, skills (`.agents` + `.claude` mirror), series specs, and lessons for the 2026-11-18 `黑猫研究院` full-bleed thumbnail standard.
- [x] Verify with `npm run test:tools`, `npm run check:tasks`, and Playwright `openRenderer` smoke render across `zh-TW`, `en`, and `th`.

## How to verify

```bash
npm run test:tools && npm run check:tasks
```

## Notes

- Claimed with `--force` because 8 stale tickets from `2026-10-14` to `2026-11-03` (15–35 days old, verified via `who-is-on-it.mjs` and `gh pr list` to have zero active sessions or open PRs) still listed `templates.mjs` or `SKILL.md` in `review` / stale `in-progress` state.
- Existing videos without `layout: "heimao"` / `"heimao-left"` keep their exact HTML, CSS, and frame hashes byte-for-byte.
- At `fontSize: 120` (`leftFontSize: 110`) across `1200 px`, `zh-TW` headlines up to 10 CJK characters stay at `120 px` (`30 px` on a `320 px` phone tile), while foreign (`en, es, pt, id, vi, th`) single-line headlines should stay within ~18–20 Latin characters so `.fit` keeps phone height `>= 24 px`.
