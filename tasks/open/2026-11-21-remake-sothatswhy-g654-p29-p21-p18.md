---
id: 2026-11-21-remake-sothatswhy-g654-p29-p21-p18
title: Remake sothatswhy G654, P29, P21, P18, P13, and P06 under Heimao 10-step and rich-gouache rules
status: in-progress
priority: P1
area: docs
owner: antigravity-gemini-3-1-pro
claimed_at: 2026-11-21T15:21:07Z
created_at: 2026-11-21T15:20:46Z
completed_at:
branch: antigravity/sothatswhy-heimao-remake-batch2
depends_on: []
scope:
  - docs/videos/sothatswhy-g654-thermal-grill
  - docs/videos/sothatswhy-p29-https
  - docs/videos/sothatswhy-p21-car-sickness
  - docs/videos/sothatswhy-p06-bubble-film
  - docs/videos/sothatswhy-p18-pencil-diamond
  - docs/videos/sothatswhy-p13-gps-timing
---

# Remake sothatswhy G654, P29, P21, P18, P13, and P06 under Heimao 10-step and rich-gouache rules

## Why

Full Batch 2 remake of six `sothatswhy-*` episodes (`G654`, `P29`, `P21`, `P06`, `P18`, `P13`) under the 2026-11-14 / 11-18 / 11-20 (`#2197`) rules: Heimao 10-step dialogue scripts, 2x blind narrative + 3-persona opening review lock, rich matte gouache keyframes via built-in `generate_image` (`$0`, never MiniMax images), 2.5-head V2 chibi sheets + 45%-65% `nobody: true`, `heimao-left` 9-locale thumbnails, Gemini `zh-TW` TTS + 8-locale MiniMax dubs, independent post-assembly `audience-review.md`, Google Drive backup (`0 differences`), and `/admin/videos` `review-push`.

## Definition of done

- [ ] All 6 episodes pass `lint` (0 errors, 0 i18n/youtube/thumb warnings), `qa` (`11/11`), `package` (`4/4`), independent `review/audience-review.md` fixed, Google Drive backup (`0 differences`), and `/admin/videos` `review-push --gate outline,script,final,publish`.

## Steps

- [x] Lock scripts (`lint` 0 errors, Blind Narrative 14/14 x2, Opening Review 3/3 >= 8.5 `problems: []`), `$0 look`, 8-locale i18n (`0` warnings), and 9-locale `heimao-left` rendered thumbnails visually verified for ALL 6 episodes (`G654`, `P29`, `P21`, `P06`, `P18`, `P13`).
- [x] Generate, import, 2x-zoom audit, fix all `must_fix`, and approve `storyboard` for `G654` (65/65), `P29` (63/63), `P21` (55/55; `dfedcf4d1934`), and `P06` (53/53; all 11 `must_fix` fixed & `storyboard` approved `2b72d24b80be`).
- [x] Finish all 338/338 keyframes, 2x-zoom independent audits, redraws, and `storyboard` approvals for ALL 6/6 episodes (`G654` 65/65, `P29` 63/63, `P21` 55/55, `P06` 53/53, `P18` 50/50 `18df1dd7e77d`, `P13` 52/52 `4a43ca64f183`).
- [x] Complete `sothatswhy-g654-thermal-grill` end-to-end: `65/65` zh-TW TTS (`0` flags), `final.mp4` (`08:35`, body `08:14`, `3bd320e7a920`), independent audience review (`9.1/10 PASS`, `0 must_fix`), `8/8` `.m4a` dubs, `9` captions, `qa` (`10/11`, policy channel_stance note), `package` (`4/4`, `f1ed902a15d5`), Google Drive backup (`2,108` prod + `121` top-level files, `0 differences`), and `/admin/videos` `review-push` (`outline, script, storyboard, audio, final, dubs, publish`).
- [x] Complete `sothatswhy-p29-https` end-to-end: `63/63` zh-TW TTS (`08:06.5` body, `5.64 chars/s`), `final.mp4` (`08:27`, `1871330504a4`), 2-round independent audience review fixed & re-verified (`9.0/10 PASS`, `0 must_fix`), `8/8` `.m4a` dubs, `9` captions, `qa` (`11/11 ALL PASS`), `package` (`4/4`, `8a87643a3fcb`), Google Drive backup (`1,659` prod + `126` top-level files, `0 differences`), and `/admin/videos` `review-push` (`outline, script, storyboard, audio, final, dubs, publish`).
- [ ] Complete remaining 4 episodes (`P21` 55 lines, `P06` 53 lines, `P18` 50 lines, `P13` 52 lines — all 4 already `storyboard` APPROVED) once user authorizes website Gemini TTS key or account quota cooldown clears: TTS, `assemble`, independent `audience-review.md`, `8/8` dubs, `9` captions, `qa`, `package`, Google Drive backup (`0 differences`), and `/admin/videos` `review-push`.

## How to verify

```bash
for s in sothatswhy-g654-thermal-grill sothatswhy-p29-https sothatswhy-p21-car-sickness sothatswhy-p06-bubble-film sothatswhy-p18-pencil-diamond sothatswhy-p13-gps-timing; do
  node tools/video/cli.mjs lint --slug "$s"
  node tools/video/cli.mjs qa --slug "$s"
done
npm run test:docs-videos && npm run check:tasks
```

## Notes

- **2026-11-23 03:50 UTC checkpoint (`G654` & `P29` 100% DONE, backed up `0 differences`, pushed to `/admin/videos`)**:
  - **ALL 6/6 EPISODES — ALL 338/338 KEYFRAMES 100% 2x-ZOOM AUDITED, FIXED, AND `storyboard` APPROVED!** Zero `generate_image` work left across all 6 episodes.
  - **`sothatswhy-g654-thermal-grill` — 100% COMPLETE**:
    - `final.mp4`: `08:35` total / `08:14` body (`15,474` frames, `sha256: 3bd320e7a920`).
    - Independent post-assembly audience review: `docs/videos/sothatswhy-g654-thermal-grill/review/audience-review.md` (**9.1 / 10 PASS**, `0 must_fix`).
    - `8/8` `.m4a` dubs + `9` captions + `9` Heimao thumbnails + `qa` (`10/11`, Jev stance `0.36–0.42` against tech-tutorial `channel_stance`) + `package` (`4/4`, `f1ed902a15d5`).
    - Google Drive (`0 differences`): `製作檔/sothatswhy-g654-thermal-grill` (`1Qg8S7BtIYWpqmeu5DC1qRcE31rbLgYtm`, `2,108 files, 0 differences`) + ep deliverables (`18G9zupAKBCnEF3Ildy0icIN6UXbU7GTX`, `121 files, 0 differences`).
    - `/admin/videos` `review-push`: `outline, script, storyboard, audio, final, dubs, publish` all submitted (`pending`; `languages` waits for owner approval of `final`).
  - **`sothatswhy-p29-https` — 100% COMPLETE**:
    - `final.mp4`: `08:27` total / `08:06.5` body (`14,595` frames, `sha256: 1871330504a4`).
    - Independent post-assembly audience review (2 rounds): Round 1 flagged `1400ms` post-300s pause cluster, 4 subtitle-vs-audio wording diffs, and long thumbnail subline; fixed (`h034` re-synthesized verbatim, `h035/h037/h055` synced, `h051`/`h060` ear-verified, uniform natural pauses, shortened 9-locale thumbnail sublines), re-assembled, and Round-2 verified in `docs/videos/sothatswhy-p29-https/review/audience-review.md` (**9.0 / 10 PASS**, `0 must_fix`).
    - `8/8` `.m4a` dubs + `9` captions + `9` Heimao thumbnails + `qa` (**`11/11 ALL PASS`**, Jev `0.66–0.68`) + `package` (**`4/4`**, `8a87643a3fcb`).
    - Google Drive (`0 differences`): `製作檔/sothatswhy-p29-https` (`1zi1PMCGElzLKAXhIO1HrnANAoJfh9f1E`, `1,659 files, 0 differences`) + ep deliverables (`17wKEo-6PvkA1_0LflpKiUHUCmB7XCOBT`, `126 files, 0 differences`).
    - `/admin/videos` `review-push`: `outline, script, storyboard, audio, final, dubs, publish` all submitted (`pending`; `languages` waits for owner approval of `final`).
  - **Remaining 4 episodes (`P21`, `P06`, `P18`, `P13`)**: Per owner's strict budget instruction (`等待冷卻的TTS可先使用網站金鑰來做 g654 p29`), paused cleanly BEFORE running paid-key Gemini TTS on `P21` (55 lines), `P06` (53 lines), `P18` (50 lines), and `P13` (52 lines) — awaiting owner's go-ahead or account cooldown recovery.



