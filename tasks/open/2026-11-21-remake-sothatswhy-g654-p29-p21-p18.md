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
- [x] Generate, import, 2x-zoom audit, fix all `must_fix`, and approve `storyboard` for `G654` (65/65) and `P29` (63/63).
- [ ] Finish remaining keyframes + 2x-zoom audit + `storyboard` approve for `P21` (39/55 imported; redraw `#27, #32, #36, #37` for canon outfits + generate `#40..#55`), `P06` (0/53), `P18` (0/50), and `P13` (0/52) once `generate_image` quota resets.
- [ ] Complete `zh-TW` Gemini TTS (`G654` 14/65 cached; others 0 done) once host Gemini TTS quota recovers, then `check-audio`, `clips`, `music`, `assemble`, `captions`, independent `audience-review.md`, 8/8 MiniMax `.m4a` dubs, `qa 11/11`, `package 4/4`, Google Drive backup, and `/admin/videos` `review-push` for all 6.

## How to verify

```bash
for s in sothatswhy-g654-thermal-grill sothatswhy-p29-https sothatswhy-p21-car-sickness sothatswhy-p06-bubble-film sothatswhy-p18-pencil-diamond sothatswhy-p13-gps-timing; do
  node tools/video/cli.mjs lint --slug "$s"
  node tools/video/cli.mjs qa --slug "$s"
done
npm run test:docs-videos && npm run check:tasks
```

## Notes

- 2026-11-21 20:10 UTC checkpoint:
  - All 6 scripts, 48 i18n JSONs, `$0 look` approvals, and 54 rendered thumbnails (9 locales x 6) are complete and verified (`0` lint errors, `0` i18n/youtube/thumb warnings).
  - `G654` (65/65 KFs, `storyboard` approved, 14/65 Gemini TTS cached) and `P29` (63/63 KFs, `storyboard` approved) are 100% ready for Gemini TTS -> assembly -> audience review -> 8-locale MiniMax dubs -> Drive backup -> `review-push`.
  - Two external quota cooldowns currently active:
    1. Built-in `generate_image` (`gemini-3.1-flash-image`) hit 4h rolling quota at `2026-11-21T19:37:52Z` (resets ~`2026-11-21T23:38Z`).
    2. Host Gemini TTS returning `Gemini 語音暫時忙碌或達到用量上限` (stopped polling cleanly at `20:09Z` so bucket recovers).
  - For `P21`, remember to redraw KFs `#27` (`kid-reverse-sofa-hook`), `#32` (`kid-dashcam-screen-idea`), `#36` (`chief-theory-boundary-honest`), `#37` (`kid-ten-thousand-gap-hook`) with exact canon outfits (Chief: mustard-yellow cardigan + dark navy trousers + side ponytail with silver-grey streak; Kid: 8yo girl black bob + ink-navy toggle raincoat with mustard hood) alongside `#40..#55`.

