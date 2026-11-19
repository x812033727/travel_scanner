---
id: 2026-11-18-heimao-thumbnails-s14-p25
title: Upgrade 16 curio/sothatswhy episodes to heimao thumbnails, restore full packages/backups, and produce sothatswhy-p25-train-tunnel
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-11-18T13:56:11Z
completed_at:
branch: antigravity/heimao-thumbnails-s14-p25
depends_on: []
scope:
  - docs/videos/curio-s14
  - docs/videos/curio-w01-dolby-licensing
  - docs/videos/curio-s23-v2
  - docs/videos/curio-s10-v2
  - docs/videos/curio-s25-v2
  - docs/videos/curio-s24-v2
  - docs/videos/curio-s13-v2
  - docs/videos/curio-s26-v2
  - docs/videos/curio-w02-michelin-guide-stars
  - docs/videos/sothatswhy-p25-train-tunnel
---

# Upgrade 16 curio/sothatswhy episodes to heimao thumbnails, restore full packages/backups, and produce sothatswhy-p25-train-tunnel

## Why

1. `curio-s14` was left with superseded foreign dub tracks on `/admin/videos` and an incomplete `S14/製作檔` folder on Google Drive (missing `curio-s14` full workdir, keyframes, recordings, and 8-locale dub timelines).
2. Following PR #2164 (`layout: "heimao"` / `"heimao-left"`), 16 existing episodes across `奇聞檔案局` (`curio-s14`, `curio-w01-dolby-licensing`, `curio-s23-v2`, `curio-s10-v2`, `curio-s25-v2`, `curio-s24-v2`, `curio-s13-v2`, `curio-s26-v2`, `curio-h18-flight-19`, `curio-w02-michelin-guide-stars`) and `原來如此事務所` (`sothatswhy-p21-car-sickness`, `sothatswhy-p13-gps-timing`, `sothatswhy-p06-bubble-film`, `sothatswhy-p29-https`, `sothatswhy-p12-qr-code`, `sothatswhy-p18-pencil-diamond`) need dedicated full-bleed `heimao` 9-locale thumbnails, full-tier `publish` + `languages` (`dubs=8`) package sync on `/admin/videos`, and verified Google Drive backups (`0 differences`).
3. `sothatswhy-p25-train-tunnel` (作品 `sothatswhy` 第 25 集, `"高鐵車頭變長，為什麼跟隧道有關？"`) needs complete end-to-end production in the theatrical-light rich-gouache series look with `heimao` 9-locale thumbnails, independent fact-check, 2x quadrant keyframe audit, post-assembly independent audience review, full Google Drive backup, and `/admin/videos` review push.

## Definition of done

- [x] `curio-s14` has all 8 foreign dubs (`en,ja,ko,es,pt,id,vi,th`), 85 keyframes, `recordings`, `narration.wav`, `timeline.json`, and 9-locale `heimao` thumbnails backed up to both `S14` root and `S14/製作檔/curio-s14` (`0 differences`) and pushed to `/admin/videos` (`publish` full-tier + `languages` `dubs=8`).
- [x] All 9 remaining `curio-*` episodes (`w01`, `s23-v2`, `s10-v2`, `s25-v2`, `s24-v2`, `s13-v2`, `s26-v2`, `h18`, `w02`) pass PR #2164 `thumbnailChecks` across all 9 locales with audited `heimao` hero illustrations, have full Google Drive backups (`0 differences`), and have complete `publish` + `languages` packages on `/admin/videos`.
- [x] All 6 existing `sothatswhy-*` episodes (`p21`, `p13`, `p06`, `p29`, `p12`, `p18`) pass PR #2164 `thumbnailChecks` across all 9 locales with audited `heimao` hero illustrations, have full Google Drive backups (`0 differences`), and have complete `/admin/videos` packages (`p18` `final`+`publish` pushed, `--gate languages` awaits owner approval of `final`; `p29` `final` pushed with `11/11` `qa.json`, `dubs=8`, `thumbnail` `df7ab6139fa6...`, and full `upload/` backed up on Drive while `--gate publish` awaits `/admin/videos` `HTTP 507 video_review_store_full` clearance).
- [ ] `sothatswhy-p25-train-tunnel` passes `lint` (`0` errors, `0` i18n warnings), independent fact-check (`verify-3.md` `PASS`), blind panel (`review/narrative.json` `passed`), `look` (`chief-canon-v2.png` + `kid-canon-v2.png`), `tts` (`5.15` chars/s) + `recordings/` + `music/` + 8-locale `i18n/*.json` + full Google Drive backup (`0 differences`) + `/admin/videos` `outline` & `script` push (**DONE**); remaining after `gemini-3.1-flash-image` ~48h quota reset: 106 rich-gouache keyframes + `heimao` hero + 2x quadrant audit, `render`, `assemble`, `captions`, 8-locale MiniMax `dub` + `check-audio`, `qa` (`11/11`), independent `review/audience-review.md`, `package`, Drive sync, and `review-push --gate final/publish/languages` (full copy-paste commands in `docs/videos/sothatswhy-p25-train-tunnel/NOTES.md`).
- [x] `npm run test:tools`, `npm run test:docs-videos`, and `npm run check:tasks` pass cleanly.

## Steps

- [x] Reconstruct `curio-s14`, generate & audit `heimao` hero illustration, render 9-locale thumbnails, push `publish` + `languages` to `/admin/videos`, and sync Google Drive (`S14` + `S14/製作檔/curio-s14`).
- [x] Audit, upgrade/fix, back up, and sync Batch 3A (`curio-s23-v2`, `curio-s10-v2`, `curio-s25-v2`, `curio-s24-v2`, `curio-s13-v2`) and Batch 3B (`curio-w01-dolby-licensing`, `curio-s26-v2`, `curio-h18-flight-19`, `curio-w02-michelin-guide-stars`).
- [x] Upgrade, audit, back up, and sync the 6 existing `sothatswhy-*` episodes (`p21`, `p13`, `p06`, `p29`, `p12`, `p18`) from staged `workDir` docs without colliding with open PRs `#2060` / `#2111`.
- [x] Complete `sothatswhy-p25-train-tunnel` pre-keyframe production (`brief.md`, `claims.md`, `video.json`, `verify-3.md`, blind `panel`, `look`, `tts`, `recordings/`, `music/`, 8-locale `i18n/*.json`, `/admin/videos` `outline` + `script` push, `NOTES.md`, and Drive backup `0 differences`).
- [ ] After `gemini-3.1-flash-image` ~48h quota reset, generate `sothatswhy-p25-train-tunnel` keyframes + `heimao` hero via built-in `generate_image` (never MiniMax `image-01`), run 2x audit, `render`, `assemble`, `captions`, 8-locale MiniMax `dub`, `qa`, `audience-review.md`, `package`, Drive sync, and `review-push`.

## How to verify

```bash
npm run test:tools && npm run test:docs-videos && npm run check:tasks
```

Also verify via `/api/video/reviews/<slug>` and independent `gdrive readonly` checks that all 17 episodes' Google Drive `epDir` and `製作檔/<slug>` (`workDir`) stand at `0 differences`.

## Notes

- Claimed with `--force` over three stale Oct 19–30 claims (`2026-10-19-curio-s-axis-third-batch-s29`, `2026-10-20-remake-ten-curio-episodes-in-the`, `2026-10-30-three-brand-stories-move-to-curio`) that have no active branches or open PRs.
- Episodes whose text docs are not yet merged to `main` (`curio-h18-flight-19` in PR `#2111`; `sothatswhy-p06/p12/p13/p18/p21/p29` in PR `#2060` / Drive `製作檔`) were staged in `/tmp/mokaair-work/shelf/<slug>/` and backed up to `製作檔/<slug>/repo-docs/` on Google Drive + pushed to `/admin/videos` so this PR stays conflict-free.
- **Independent Google Drive Verification (`17 / 17 PASS — 0 differences`)**:
  1. `curio-s14` (`epDir`: `14UMzKO6kx3o6L9_MIifFd0Mbkql-G-gN`, `workDir`: `1trNpPEUq_Cg3b1I1bQW6vyf5sj2Yemme`, `work=318`, `ep=134`) — `0 diffs`
  2. `curio-s23-v2` (`epDir`: `1LSovmL-k0u6sYhlliXgNVIPSZSqzvHCl`, `workDir`: `1selr2LIdZ1FOw9ocBZb-SeJADFfAb0Sd`, `work=329`, `ep=129`) — `0 diffs`
  3. `curio-s10-v2` (`epDir`: `1KPVINm5Y063cF0gRgJyAqDFzt9DVoxcS`, `workDir`: `1e_tOkpom8rMV42qskDwHOcowTsKbqEtv`, `work=345`, `ep=138`) — `0 diffs`
  4. `curio-s24-v2` (`epDir`: `1EfmKwl6XnUnJtBVxvTEPAPTPo_U09IgQ`, `workDir`: `17SwD9W8xZs_ytJP5IZwwjSWtH7FID6rL`, `work=347`, `ep=135`) — `0 diffs`
  5. `curio-s13-v2` (`epDir`: `17JPN_rnEskQiPaTBgfGKGZnJvE2QYyqY`, `workDir`: `1pOPQLLhXyMuT4XGbIhAhbJf7C1q26ADi`, `work=373`, `ep=165`) — `0 diffs`
  6. `curio-s26-v2` (`epDir`: `1NX3v6pvZZiM2OWELXm1R9lRTIc-47OTu`, `workDir`: `1cBsiZ8X1fWdrwZS8Q-ujJA2_eJcEvXv3`, `work=359`, `ep=138`) — `0 diffs`
  7. `curio-s25-v2` (`epDir`: `1_m3qSNf4c-X3qbQTSe-6WhzdsxNKhCey`, `workDir`: `1gAajKp8AO-WGKOaN-6u0w5n08fK3Sql4`, `work=336`, `ep=136`) — `0 diffs`
  8. `curio-w02-michelin-guide-stars` (`epDir`: `12XnJcan_DZ-LVc7Dc4afeWgSut7RuZqp`, `workDir`: `1P_F-1AV_0JPVWVw7bOZAbfUuNjZcJx6u`, `work=360`, `ep=135`) — `0 diffs`
  9. `curio-w01-dolby-licensing` (`epDir`: `1uGYOq5aYvRn1HXwb0dCune09uTw1QVCl`, `workDir`: `1-3rDkXTcfW-K2fakNZfsIcQyWy_xW2cd`, `work=381`, `ep=149`) — `0 diffs`
  10. `curio-h18-flight-19` (`epDir`: `1fBpM1QyrKVIPfnpw8BrNNcfFFa9Efqht`, `workDir`: `1dGjoosUoNX5N_OJC6IgP2lQQp_JF6bYy`, `work=285`, `ep=125`) — `0 diffs`
  11. `sothatswhy-p12-qr-code` (`epDir`: `1ZO4236C3SIr6noBAhEgpbqAVV0Ms3iF5`, `workDir`: `1kMdSO7TbqNqoTayAhSlB5c7Xo_Kln7EO`, `work=370`, `ep=129`) — `0 diffs`
  12. `sothatswhy-p06-bubble-film` (`epDir`: `1I9ZqDj35TqviYPWM8aoRExPFbIORSjSh`, `workDir`: `1oO0H2ATrN6Y4VGHNNzGM3pJMRe5UQs6v`, `work=410`, `ep=165`) — `0 diffs`
  13. `sothatswhy-p13-gps-timing` (`epDir`: `1ujihXrU3uzqJaCRf-gip-EVxu-1kif50`, `workDir`: `1Rx_kIBjXI5Z0SxVf9SNf_2ksWsnKFkXz`, `work=397`, `ep=138`) — `0 diffs`
  14. `sothatswhy-p21-car-sickness` (`epDir`: `1yopwkCx1lwvIDXLDGebbXnWkWk4QKhch`, `workDir`: `1eYk0JY-hPftpPpCEgt8XEBiaTaPW72vu`, `work=405`, `ep=164`) — `0 diffs`
  15. `sothatswhy-p18-pencil-diamond` (`epDir`: `1gYSFL8Alp5WsdYGwoQRi9rV2-2j-bkT2`, `workDir`: `19q7SP-psjEpgTUKneYLa-JuO9Z3itmZr`, `work=453`, `ep=181`) — `0 diffs`
  16. `sothatswhy-p29-https` (`epDir`: `17wKEo-6PvkA1_0LflpKiUHUCmB7XCOBT`, `workDir`: `1zi1PMCGElzLKAXhIO1HrnANAoJfh9f1E`, `work=393`, `ep=138`) — `0 diffs`
  17. `sothatswhy-p25-train-tunnel` (`epDir`: `1TxaxA5sx5Ksw5kdAJTYQv1CR8Dz6aKNZ`, `workDir`: `1llYIMZ5x9S9xcoa0aAXlx9_9WcpCWBnd`, `work=176`, `ep=6`, pre-keyframe handoff) — `0 diffs`
- Released after pushing this PR so the next session after `gemini-3.1-flash-image` ~48h quota reset can claim and complete `sothatswhy-p25-train-tunnel`'s keyframes, assembly, dubs, QA, and final package cleanly.
