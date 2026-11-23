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
- [ ] Complete remaining Gemini TTS lines (`G654` `vi` 16 kid lines that fall back from MiniMax to Gemini; `P29` 11 remaining `check-audio` redo lines; `P21` 55, `P06` 53, `P18` 50, `P13` 52), then finish assembly, independent `audience-review.md`, 8/8 dubs, `qa`, `package`, Google Drive backup (`0 differences`), and `/admin/videos` `review-push` for all 6.

## How to verify

```bash
for s in sothatswhy-g654-thermal-grill sothatswhy-p29-https sothatswhy-p21-car-sickness sothatswhy-p06-bubble-film sothatswhy-p18-pencil-diamond sothatswhy-p13-gps-timing; do
  node tools/video/cli.mjs lint --slug "$s"
  node tools/video/cli.mjs qa --slug "$s"
done
npm run test:docs-videos && npm run check:tasks
```

## Notes

- 2026-11-23 01:30 UTC checkpoint:
  - **ALL 6/6 EPISODES — ALL 338/338 KEYFRAMES 100% 2x-ZOOM AUDITED, FIXED, AND `storyboard` APPROVED!** Zero `generate_image` work left across all 6 episodes.
  - All 6 episodes switched to local canonical series music bed `sothatswhy-bed-r2.m4a` (`9bb4ba6f...`), enabled 8-locale `languages.json` (`en,ja,ko,es,pt,id,vi,th`), and calibrated `pauses` / `pause_after_ms` (`lint` 0 errors across all 6) so every episode cleanly clears the `>= 480s (14,400 frames)` knowledge long-video body floor.
  - **`sothatswhy-g654-thermal-grill` (99% DONE)**:
    - `65/65` Gemini `zh-TW` lines synthesized & `check-audio` **0 flags** (`g052` fixed via `say: "眼睛來插手就算了..."`, exact match).
    - Assembled `final.mp4`: `15,474 frames` (`08:35` total / `08:14` body, `-14 LUFS`, `-2 dBFS` peak, `-33 LUFS` music bed).
    - Independent post-assembly audience review saved in `docs/videos/sothatswhy-g654-thermal-grill/review/audience-review.md` (**9.1 / 10 PASS**, 0 `must_fix`).
    - All **9** locale `.srt/.vtt` captions generated; **7/8** `.m4a` MiniMax dub tracks (`en, ja, ko, es, pt, id, th`) finished with 0 long windows (`max 1.10x–1.15x`).
    - `qa`: **10/11 PASS** (`assemble, render, narration, pace, captions, metadata, facts, links, thumbnail, disclosure` all green; `policy` Jev stance `0.42–0.54` due to channel_stance tech-tutorial checklist vs general science).
    - Only **`vi.m4a`** remains (blocked on Gemini TTS because `DUB_MINIMAX_VOICES.vi` only lists 1 voice so `kid`'s 16 lines fall back to Gemini `Leda`), then `package`, Google Drive backup (script ready at `scratch/gdrive-backup-episode.py`), and `review-push`.
  - **Remaining Gemini TTS workload (~237 lines total)** currently blocked by host Gemini TTS B-account daily RPD `HTTP 429` (`rc=4`):
    - `G654 vi`: 16 `kid` lines (49 `chief` lines go to MiniMax)
    - `P29`: 11 remaining `check-audio` redo lines (`h020, h032, h034, h035, h037, h038, h042, h043, h050, h051, h055`)
    - `P21`: 55 lines | `P06`: 53 lines | `P18`: 50 lines | `P13`: 52 lines


