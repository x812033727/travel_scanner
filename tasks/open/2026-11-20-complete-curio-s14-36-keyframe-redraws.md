---
id: 2026-11-20-complete-curio-s14-36-keyframe-redraws
title: Complete curio-s14 36 keyframe redraws, final cut, audience review, and publish
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-11-20T13:29:19Z
completed_at:
branch: antigravity/curio-s13-v2-s14-remake
depends_on: []
scope:
  - docs/videos/curio-s14
---

# Complete curio-s14 36 keyframe redraws, final cut, audience review, and publish

## Why

`curio-s14` ("宮本武藏故意遲到 2 小時？死後 9 年石碑竟隻字未提｜奇聞檔案局") has completed its R20 script, `lint` (`0/0`), independent `verify-2` fact & i18n check (`PASS`), 3-persona `opening-review` (`9.2` each), 2-reader blind `narrative` panel (`14/14`), 9-locale `heimao` thumbnails, `zh-TW` `Sulafat` narration (`4.60` chars/s, `70/70` `0 flagged`), `music`, all 8 MiniMax dubs (`en,ja,ko,es,pt,id,vi,th`, all `70/70` `0 flagged`), `captions`, `/admin/videos` `script` + `audio` review-pushes, and full Google Drive backup (`1trNpPEUq_Cg3b1I1bQW6vyf5sj2Yemme` / `14UMzKO6kx3o6L9_MIifFd0Mbkql-G-gN`, `0 differences`).

During keyframe redrawing, `gemini-3.1-flash-image` entered quota cooldown (expected reset around `2026-11-20T18:25Z`). Per `curio-episode` SKILL.md, MiniMax image generation is strictly forbidden. Once `gemini-3.1-flash-image` quota resets, the 36 failed keyframes identified in the 71-shot 2x quadrant audit (`docs/videos/curio-s14/NOTES.md` §2) need to be redrawn via built-in `generate_image` (`16:9`) + `keyframes import --provider external --usd 0`, followed by `assemble` + `qa` (`11/11`) + independent `review/audience-review.md` + `package` (`4/4`) + Google Drive backup (`0 differences`) + `/admin/videos` `storyboard`/`final`/`publish`(/`languages` after `publish` approval) pushes.

## Definition of done

- [x] Restore `curio-s14` workdir from Google Drive `1trNpPEUq_Cg3b1I1bQW6vyf5sj2Yemme`, generate the single-figure character sheets (`musashi-29`, `kojiro`, `musashi-60`, `meiji-editor` matching `ada-canon-v2.png`) and redraw all 36 failed keyframes listed in `docs/videos/curio-s14/NOTES.md` §2 via owner-authorized Mokaair Gemini API (`image_model: "gemini-3.1-flash-image"`, `size: "2K"`, `16:9`, **never MiniMax**).
- [x] Pass 2x-zoom 4-quadrant independent subagent visual audit across all 71 images (`00-hero` + `01`–`70`, checking right-over-left kimono wrap `右衽`, flat center-stitched `wahon` books, guardless `suburito` wooden oar sword with no `tsuba` or scabbard, 5 fingers, full-bleed zero white borders, zero text/garbled marks), import all 70 shots into `keyframes/manifest.json` (`[x] keyframes drawn`), run `render` (`[x] frames rendered`), and submit `review-push --slug curio-s14 --gate storyboard` on `/admin/videos`.
- [x] Once the owner approves `storyboard` on `/admin/videos`, run `review-pull --slug curio-s14` -> `clips` -> `assemble` (`final.mp4` `sha256: 06530d2067da`, `16,835` frames, `-14.0 LUFS`) -> `dub` remix -> `captions` -> `qa` (`11/11` checks passed).
- [x] Run an independent post-assembly audience review subagent (`review/audience-review.md`, scores `8.2–8.9`, overall average `8.60/10 >= 8.0`, `0` blocking defects, 100% promise-payoff alignment `PASS`), sync workdir + `final.mp4` to Google Drive (`1trNpPEUq_Cg3b1I1bQW6vyf5sj2Yemme` & `14UMzKO6kx3o6L9_MIifFd0Mbkql-G-gN`, `0 differences`), and submit `review-push --slug curio-s14 --gate final` (`pending` on `/admin/videos`).
- [ ] Once the owner approves `final` on `/admin/videos`: run `review-pull --slug curio-s14` -> `package --slug curio-s14` (`4/4`) -> `review-push --slug curio-s14 --gate publish` (and once `publish` is approved, `review-push --slug curio-s14 --gate languages`) -> sync `upload/` & `review/` to Google Drive (`0 differences`).

## Steps

- [x] Pull `curio-s14` workdir and run `review-pull --slug curio-s14` (`script`, `audio`, and `storyboard` approvals recorded).
- [x] Generate the 4 character sheets + 36 keyframe redraws via `gemini-3.1-flash-image` 2K API, pass independent 2x quadrant audit (`71/71` PASS), import all 70 shots into `keyframes/manifest.json`, run `render`, `clips`, `assemble --adopt-branding`, `dub` remix, `captions`, `qa` (`11/11`), independent `audience-review.md` (`8.60/10` PASS), Google Drive sync (`0 differences`), and `review-push --gate final`.
- [ ] After owner approves `final` on `/admin/videos`: run `review-pull`, `package` (`4/4`), `review-push --gate publish` (then `--gate languages` after `publish` approval), and final Google Drive sync (`0 differences`).

## How to verify

```bash
VIDEO_WORKDIR=/home/antigravity/mokaair-work/videos node tools/video/cli.mjs qa --slug curio-s14
VIDEO_WORKDIR=/home/antigravity/mokaair-work/videos node tools/video/cli.mjs package --slug curio-s14
npm run test:tools && npm run test:docs-videos && npm run check:tasks
```

## Notes

- `final.mp4` (`sha256: 06530d2067da`, `9m21.21s`), `review/qa.json` (`11/11`), `review/audience-review.md` (`8.60/10` PASS), and all 8 remixed MiniMax dubs (`en,ja,ko,es,pt,id,vi,th`) + 9 captions/thumbnails are backed up on Google Drive (`1trNpPEUq_Cg3b1I1bQW6vyf5sj2Yemme` & `14UMzKO6kx3o6L9_MIifFd0Mbkql-G-gN`, `0 differences`), and `final` is pending owner approval on `/admin/videos` (`package` requires `final` approval first).
- Yoshikawa Eiji died in 1962 (<70 years ago) and is depicted in zero frames.
