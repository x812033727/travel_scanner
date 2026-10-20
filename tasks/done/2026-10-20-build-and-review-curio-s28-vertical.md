---
id: 2026-10-20-build-and-review-curio-s28-vertical
title: Build and review Curio S28 vertical Short
status: done
priority: P2
area: docs
owner: codex-s07-shorts
claimed_at: 2026-10-20T05:42:06Z
created_at: 2026-10-20T05:42:03Z
completed_at: 2026-10-20T06:09:04Z
branch: codex/curio-s34-endurance-20261019
depends_on:
  - 2026-10-20-curio-s28-one-sourced-short-script
scope:
  - docs/videos/curio-s28/shorts.json
  - docs/videos/curio-s28/short-verify-1.md
  - docs/videos/curio-s28/short-verify-2.md
---

# Build and review Curio S28 vertical Short

## Why

S28 has an approved long film and a source-checked one-Short script, but its
vertical film has not been built. Reuse the long film's approved pictures,
synthesize the channel voice after S34 releases its voice/ASR window, and
separate a locally complete cut from any site/YouTube gate still pending.

## Definition of done

- [x] The one-Short cut has measured 1080×1920/30 fps and 25–55 seconds,
      correct spoken text, safe captions, a source check bound to exact script
      hash, and visible opening/loop frames.
- [x] Local QA/package results and any site or full-film URL blockers are
      recorded without claiming a private/public upload that has not happened.

## Steps

- [x] Wait for S34 producer to release the voice/ASR call window.
- [x] Run `from-episode` server build against S28's existing keyframes, then
      `check-audio`; repair only flagged phrases if needed.
- [x] Bind an independent factual `verify.json` to the resolved script, run
      QA, inspect source/ending frames, and package or record exact blockers.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/shorts/cli.mjs from-episode --slug curio-s28 --check`;
`node tools/video/shorts/cli.mjs from-episode --slug curio-s28 --workdir /workspace/.video-work/shorts --speech server`;
`node tools/video/shorts/cli.mjs check-audio --dir <build>`;
`node tools/video/shorts/cli.mjs qa --dir <build> --verify <verify.json>`;
`node tools/video/shorts/cli.mjs package --dir <build>`.

## Notes

Preflight `short-verify-1.md` and script commit `d60b3c03` pass one-Short
validation, sourced claims, and five unique keyframe hashes. The long film
has no YouTube video ID at this point, so a package may rightly fail the
full-film-link item; keep that explicit until a real ID is linked.
`VIDEO_WORKDIR=/workspace/.video-work` resolves the source episode, while
`--workdir /workspace/.video-work/shorts` keeps the build and shared speech
cache with the other completed Shorts.

2026-10-20：S34 製作者已釋出語音時窗；S28 修鏡版 first build 30.10 秒／8 句，初檢兩句辨音被標，只定點重錄 2 句後第二版 30.233 秒，仍是同兩句被標。直式六幕與首尾抽格通過；沒有把 6/8 核音說成全過。只改 #4 與 #7 兩句更自然同義文字，現行 `shorts.json` SHA `586e971e165583f43185794ac504c31d7a6ea1aaa1ac532dd6acce0380b2a753`，來源與 5 張影格重新檢查通過；詳 `short-verify-2.md`。語音／ASR 時窗已交 S05 Short，等其明確放行才重建新版。舊兩支成片的 `verify.json`／核音不沿用。

2026-10-20：S05 釋出後再建兩版，最終版補錄唯一被誤聽的 CTA 句，31.00 秒／930 格，8/8 語音 0 flags，四語字幕各 8 cue 零時碼問題且經獨立語義覆看；QA 11/13、package 3/4。後台只建 `cut` 草稿（0 reviews、無 YouTube ID），未送審或發布。餘下 QA `metadata`／`links` 和 package `descriptions` 都是來源長片沒有真實 YouTube URL；後續取得 ID 後須重跑，見 `short-verify-2.md`。現行 `shorts.json` SHA `49cced53588315c1ac3bc2a94dc9337858cda521a4bf11f9540e6ca9708aed60`。
