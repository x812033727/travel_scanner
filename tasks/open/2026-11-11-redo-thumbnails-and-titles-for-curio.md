---
id: 2026-11-11-redo-thumbnails-and-titles-for-curio
title: Redo thumbnails and titles for curio v2 videos with high impressions and sub-1% CTR
status: review
priority: P2
area: docs
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T02:17:13Z
created_at: 2026-11-11T00:03:53Z
completed_at:
branch: claude/youthful-albattani-m1ih5z
depends_on: []
scope:
  - docs/videos/curio-s01
  - docs/videos/curio-s11
---

# Redo thumbnails and titles for curio v2 videos with high impressions and sub-1% CTR

## Why

The 2026-11-11 promotion review (`docs/videos/channel-review-20261111-promotion/README.md`)
found that YouTube is already showing some 奇聞檔案局 v2 videos and few people click. These
figures are self-computed from the site's YouTube report rows for 2026-10-04 to 2026-11-07:

- curio-s01-v2 `gkl0vABh1_c`: 8,656 thumbnail impressions, 0.68% CTR
- curio-s11-v2 `OzUv1Dd2XBk`: 6,151 impressions, 1.01% CTR
- curio-s04-v2: 4,530 impressions, 0.55% CTR (no `docs/videos/curio-s04*` project in the repo,
  so it is not in scope. Find where its package lives before you widen the scope.)

Buying ads for them first would only cover up the packaging problem.

## Definition of done

- [x] Each video has a new thumbnail and title that follow the series look (`curio-episode` skill) and the
      title pattern from `docs/videos/channel-review-20261025-story-series/README.md`.
- [ ] The owner has approved and changed them in Studio (changing public videos is the owner's call).
- [ ] 7 and 14 days later, the CTR is compared with the numbers above and written in Notes.

## Steps

- [x] Read `curio-episode` and `youtube-video` (thumbnail rules).
- [x] Draft two title and thumbnail options per video and hand them to the owner (`docs/videos/curio-s01/thumbnail-redo-20261111.md`, `docs/videos/curio-s11/thumbnail-redo-20261111.md`; JPGs in each episode's Drive backup under `thumbnails-redo-20261111/`).
- [ ] After the change, re-read `channel_reach_basic` with `tools/video/youtube-reports/cli.mjs`.

## How to verify

`node tools/video/youtube-reports/cli.mjs rows --report channel_reach_basic --video <id> --from <change date>`
then weight CTR by impressions.

## Notes

Never publish the computed CTRs (YouTube developer policy on derived metrics, `docs/videos/YOUTUBE-REPORTS.md`).

- 2026-11-11: the review store had already purged the v2 finals, so the cuts came from the Drive backup (`rclone backend copyid`). Frames were cropped to remove the burned-in subtitles and the top-right watermark, then drawn with `thumbnailHtml` layout e in a local Chromium. Upload and the 14-day readback are still the owner's (status: review).
