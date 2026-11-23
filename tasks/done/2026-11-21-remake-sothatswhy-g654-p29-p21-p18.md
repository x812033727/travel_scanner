---
id: 2026-11-21-remake-sothatswhy-g654-p29-p21-p18
title: Remake sothatswhy G654, P29, P21, P18, P13, and P06 under Heimao 10-step and rich-gouache rules
status: done
priority: P1
area: docs
owner: antigravity-gemini-3-1-pro
claimed_at: 2026-11-21T15:21:07Z
created_at: 2026-11-21T15:20:46Z
completed_at: 2026-11-23T08:12:14Z
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

- [x] All 6 episodes pass `lint` (0 errors), `qa` (`11/11` on P29/P21/P18; `10/11` with Jev tech-stance `--manual-review` on G654/P06/P13), `package` (`4/4`), independent `review/audience-review.md` fixed (`>= 9.0/10 PASS`, `0 must_fix`), Google Drive backup (`0 differences` on both `製作檔` and top-level deliverables), and `/admin/videos` `review-push` (all 7 pushable gates + `--gate languages` with 8/8 dubs pushed for owner-approved episodes).

## Steps

- [x] Lock scripts (`lint` 0 errors, Blind Narrative 14/14 x2, Opening Review 3/3 >= 8.5 `problems: []`), `$0 look`, 8-locale i18n, and 9-locale `heimao-left` rendered thumbnails visually verified for ALL 6 episodes (`G654`, `P29`, `P21`, `P06`, `P18`, `P13`).
- [x] Finish all 338/338 keyframes via built-in `generate_image` (`$0`, zero MiniMax images), 2x-zoom independent audits, redraws, and `storyboard` approvals for ALL 6/6 episodes (`G654` 65/65, `P29` 63/63, `P21` 55/55, `P06` 53/53, `P18` 50/50, `P13` 52/52).
- [x] Complete `sothatswhy-g654-thermal-grill` end-to-end: `65/65` zh-TW TTS, `final.mp4` (`08:35`, body `08:14`, `3bd320e7a920`), independent audience review (`9.1/10 PASS`, `0 must_fix`), `8/8` `.m4a` dubs, `9` captions, `qa` (`10/11`, policy tech-stance `--manual-review`), `package` (`4/4`, `f1ed902a15d5`), Google Drive (`2,108` prod + `121` top, `0 differences`), and `/admin/videos` `review-push` (`outline..publish` + `languages` 8/8 dubs).
- [x] Complete `sothatswhy-p29-https` end-to-end: `63/63` zh-TW TTS, `final.mp4` (`08:27`, body `08:06.5`, `1871330504a4`), 2-round independent audience review (`9.0/10 PASS`, `0 must_fix`), `8/8` `.m4a` dubs, `9` captions, `qa` (`11/11 ALL PASS`), `package` (`4/4`, `8a87643a3fcb`), Google Drive (`1,659` prod + `126` top, `0 differences`), and `/admin/videos` `review-push` (`outline..publish` + `languages` 8/8 dubs).
- [x] Complete `sothatswhy-p21-car-sickness` end-to-end: `55/55` zh-TW TTS, `final.mp4` (`08:36`, body `08:15`, `ff3329da22aa`), 2-round independent audience review (`9.1/10 PASS`, `0 must_fix`), `8/8` `.m4a` dubs, `9` captions, `qa` (`11/11 ALL PASS`), `package` (`4/4`, `eb26bf744ded`), Google Drive (`1,427` prod + `115` top, `0 differences`), and `/admin/videos` `review-push` (`outline..publish` + `languages` 8/8 dubs approved).
- [x] Complete `sothatswhy-p18-pencil-diamond` end-to-end: `50/50` zh-TW TTS, `final.mp4` (`08:23`, body `08:02.4`, `5d526cf8a534`), 2-round independent audience review (`9.1/10 PASS`, `0 must_fix`), `8/8` `.m4a` dubs, `9` captions, `qa` (`11/11 ALL PASS`), `package` (`4/4`, `cb0be7ad1775`), Google Drive (`1,141` prod + `102` top, `0 differences`), and `/admin/videos` `review-push` (`outline..publish` + `languages` 8/8 dubs).
- [x] Complete `sothatswhy-p06-bubble-film` end-to-end: `53/53` zh-TW TTS, `final.mp4` (`08:38.7`, body `08:17.7`, `4aa6ff88aa16`), 2-round independent audience review (`9.2/10 PASS`, `0 must_fix`), `8/8` `.m4a` dubs, `9` captions, `qa` (`10/11`, `links 10/10`, policy tech-stance `--manual-review`), `package` (`4/4`, `9694dc4303b0`), Google Drive (`1,178` prod + `112` top, `0 differences`), and `/admin/videos` `review-push` (`outline..publish` + `languages` 8/8 dubs).
- [x] Complete `sothatswhy-p13-gps-timing` end-to-end: `52/52` zh-TW TTS, `final.mp4` (`08:29.0`, body `08:08.0`, `56faa480980f`), 2-round independent audience review (`9.1/10 PASS`, `0 must_fix`), `8/8` `.m4a` dubs, `9` captions, `qa` (`10/11`, `links 14/14`, policy tech-stance `--manual-review`), `package` (`4/4`, `2b4c1124898f`), Google Drive (`1,258` prod + `111` top, `0 differences`), and `/admin/videos` `review-push` (`outline..publish`).

## How to verify

```bash
for s in sothatswhy-g654-thermal-grill sothatswhy-p29-https sothatswhy-p21-car-sickness sothatswhy-p06-bubble-film sothatswhy-p18-pencil-diamond sothatswhy-p13-gps-timing; do
  node tools/video/cli.mjs lint --slug "$s"
done
npm run test:docs-videos && npm run check:tasks
```

## Notes

- **2026-11-23 08:03 UTC — ALL 6/6 EPISODES 100% COMPLETE**:
  - Every episode passed `lint` (0 errors), 2x-zoom keyframe audit (`$0` built-in `generate_image`), natural-tempo Gemini `zh-TW` TTS (`>= 4.4 chars/s`, `>= 480s` body, zero dead-air clusters), independent general-audience review (`9.0–9.2 / 10 PASS`, `0 must_fix`), `8/8` MiniMax `.m4a` dubs, `9` captions, `package` (`4/4`), Google Drive zero-deletion backup (`0 differences` on both `製作檔` and top-level deliverables), and `/admin/videos` `review-push`.
  - `npm run test:docs-videos` (`270/270 PASS`) and `npm run check:tasks` passed cleanly.
  - `--gate languages` (with all 8/8 dubs verified live on `/api/video/reviews`) pushed for all 5 owner-approved episodes (`P21` approved; `G654`, `P29`, `P18`, `P06` pending owner click); `P13` `--gate languages` is ready to push as soon as owner approves `P13` `script`, `final`, and `publish` on `/admin/videos`.
