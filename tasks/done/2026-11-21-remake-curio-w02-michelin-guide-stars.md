---
id: 2026-11-21-remake-curio-w02-michelin-guide-stars
title: Remake curio-w02-michelin-guide-stars under full 2026-11-20 Curio and Heimao emblem rules
status: done
priority: P1
area: docs
owner: antigravity
claimed_at: 2026-11-21T10:53:27Z
created_at: 2026-11-21T10:53:05Z
completed_at: 2026-11-22T06:32:09Z
branch: antigravity/curio-w02-remake
depends_on: []
scope:
  - docs/videos/curio-w02-michelin-guide-stars
  - docs/videos/lexicon.json
---

# Remake curio-w02-michelin-guide-stars under full 2026-11-20 Curio and Heimao emblem rules

## Why

The owner requested remaking `curio-w02-michelin-guide-stars` (`米其林指南`) end-to-end under all current 2026-11-14 through 2026-11-20 `奇聞檔案局` rules: eliminating all 33 `lint` warnings (29 scenes > 10s, missing first-15s thumbnail/title echo, excess `「還記得…」`, 7 generic purse/wallet stand-ins, and internal engineering notes in `youtube.description`), passing the 3-persona first-300s `opening-review` and 2-reader blind `narrative` gates, synthesizing `>= 4.4 chars/s` `zh-TW` `Sulafat` narration and 8-locale MiniMax dubs (`0 flagged`), replacing the mixed 71 MiniMax `.jpg` + 15 PNG visuals with 100% unified theatrical-light rich-gouache `generate_image` keyframes (`ada-canon-v2.png` + ~55% `nobody: true`), adopting `intro_at: "none"` (`0:00` hook) + 9-locale `heimao-left` Michelin signature-emblem thumbnails, and passing `qa` (`11/11`) + independent `review/audience-review.md` before Google Drive backup and `/admin/videos` submission.

## Definition of done

- [x] `node tools/video/cli.mjs lint --slug curio-w02-michelin-guide-stars` passes with `0 errors, 0 warnings`, independent `verify-2.md` confirms 100% factual fidelity to `topic-checks/W02.md`, 3-persona `opening-review` (`>= 8.5`, `would_stay_300: true`) passes, and 2-reader blind `narrative` (`14/14`) passes.
- [x] `zh-TW` `Sulafat` narration (`>= 4.4 chars/s`, `4.58 chars/s` measured) + looped music + 8-locale MiniMax dubs (`en, ja, ko, es, pt, id, vi, th`, `0` fit overflows, pronunciation-verified) synthesized and verified.
- [x] 100% of scenes drawn in unified theatrical-light rich-gouache style via `generate_image` (`ada-canon-v2.png` + `andre-1920` character sheets, `63%` `nobody: true`), verified by 4-edge full-bleed check + independent 4-quadrant 2x zoom audit (`81/81` PASS), and imported via `keyframes import --provider external --usd 0`.
- [x] 9-locale `heimao-left` Michelin signature-emblem thumbnails (`stock/<sha256>.jpg` with wordless crimson guide book + precision vector SVG 6-petal gastronomy stars + black radial tire + gold coins, zero Bibendum IP mascot and zero letters) pass `thumbnailChecks`.
- [x] `assemble` (`intro_at: "none"` + `v4-endscreen`), `captions`, `qa` (`11/11`), independent `review/audience-review.md` (`>= 8.0/10`), `package` (`4/4`), Google Drive backup (`W02` `epDir` + `workDir`), and `/admin/videos` review pushes completed.

## Steps

- [x] Phase 1: Upgrade `video.json` + `script.md` + `claims.md` (`0 errors, 0 warnings`), generate Michelin emblem hero + `andre-1920` character sheet, pass `verify-2.md`, `opening-review`, and `narrative`.
- [x] Phase 2: Synthesize & check `zh-TW` narration (`Sulafat` >= 4.4 chars/s) + music + 8-locale translations & MiniMax dubs (`en, ja, ko, es, pt, id, vi, th`).
- [x] Phase 3: Generate all theatrical-gouache keyframes, pass 4-quadrant 2x independent audit, and `keyframes import`.
- [x] Phase 4: Render 9 thumbnails, obtain owner approvals (`script`, `audio`, `storyboard`, `final`) on `/admin/videos`, assemble `final.mp4`, pass `qa` (`11/11`) + independent `audience-review.md` (`9.12/10` PASS), run `package` (`4/4`), back up to Google Drive `W02`, push `publish` & `languages` to `/admin/videos`, and open PR.

## How to verify

```bash
node tools/video/cli.mjs lint --slug curio-w02-michelin-guide-stars
npm run test:docs-videos && npm run check:tasks
```

## Notes

- Claimed with `--force` over stale (`22d` old, no open PR) `2026-10-30-three-brand-stories-move-to-curio`.
- Completed `assemble --adopt-branding` (`17,487` frames, `-14 LUFS`, `final.mp4` sha256 `99fe8242330db5aae66ec01cef96e64b6e16fba8cbc9506287fa69f769629f50`), 8 branded MiniMax `.m4a` dubs, 9 `.srt` captions, `qa` (`11/11` checks passed), independent post-assembly `review/audience-review.md` (`9.12/10` PASS, `blocking_fixes: []`), `package` (`4/4`, `metadata.json` sha256 `3ad7809d75b6`), complete Google Drive `W02` (`12XnJcan_DZ-LVc7Dc4afeWgSut7RuZqp`) backup, and `/admin/videos` `final` + `publish` + `languages` pushes.
