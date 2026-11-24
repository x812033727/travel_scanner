---
id: 2026-11-24-produce-curio-w30-monde-selection-n9070
title: Produce curio-w30-monde-selection (N9070, #9 pool core)
status: in-progress
priority: P2
area: docs
owner: antigravity-gemini-curio
claimed_at: 2026-11-24T05:18:57Z
created_at: 2026-11-24T05:18:10Z
completed_at:
branch: antigravity/curio-w30-monde-selection
depends_on: []
scope:
  - docs/videos/curio-w30-monde-selection
  - docs/videos/lexicon.json
  - tasks/open/2026-11-24-produce-curio-w30-monde-selection-n9070.md
---

# Produce curio-w30-monde-selection (N9070, #9 pool core)

## Why

Produce 奇聞檔案局 `W30` (`curio-w30-monde-selection`, pool `N9070`): why Belgian Monde Selection gold award stickers appear across Asian convenience stores despite Belgium having 0 entries in the 2026 Nominee Label directory.

## Definition of done

- [x] Brief, claims, independent fact-check (`verify-2.md` PASS), and `video.json` v20 (`lint: 0 errors, 0 warnings`).
- [x] Opening review (`newcomer 9.1`, `scroller 9.0`, `stickler 9.1`, `problems: []`) and Blind Narrative Panel (`28/28 ALL YES`) officially recorded.
- [x] All 56/56 theatrical-light rich-gouache keyframes generated (`$0`), passed 2x-zoom 4-quadrant independent visual audit (`56/56`), and imported (`--provider external --usd 0`).
- [x] All 8 locales (`en, ja, ko, es, pt, id, vi, th`) translated, independently audited (`en`/`ja` + `ko`/`es`/`pt`/`id`/`vi`/`th` fixes applied, `lint: 0 errors, 0 warnings`), merged, and 9 thumbnails rendered & visually inspected.
- [x] `script` + `storyboard` gates pushed to `/admin/videos` and full zero-diff Google Drive backup verified.
- [ ] Post-TTS completion (`tts`, `check-audio --second-opinion`, `music`, 8 MiniMax `dub`s, `clips`, `assemble`, `captions`, `qa` 11/11, independent `audience-review.md`, `package` 4/4, Drive backup, `review-push --gate final`).

## How to verify

```bash
node tools/video/cli.mjs lint --slug curio-w30-monde-selection
node tools/video/cli.mjs opening-review --slug curio-w30-monde-selection --check
node tools/video/cli.mjs status --slug curio-w30-monde-selection
npm run check:tasks && npm run test:docs-videos
```

## Notes

- All 56 keyframes generated with built-in `generate_image` (`$0`), 0 border flags, 3-round 2x-zoom audit `56/56 PASS`.
- Waiting on upstream Gemini TTS daily RPD quota after W25–W29 before running W30 `tts`.
