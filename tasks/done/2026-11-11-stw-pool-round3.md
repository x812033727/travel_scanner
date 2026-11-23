---
id: 2026-11-11-stw-pool-round3
title: 原來如此素材池第三輪：補後備企劃與長題來源
status: done
priority: P2
area: docs
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T11:58:53Z
created_at: 2026-11-11T10:56:37Z
completed_at: 2026-11-11T11:58:54Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
  - tools/video/so-thats-why/pool
  - tools/video/so-thats-why/episode-plan.mjs
  - tools/video/so-thats-why/catalog.test.mjs
  - docs/videos/so-thats-why/refresh-20261101/EPISODES.md
  - docs/videos/so-thats-why/refresh-20261101/episodes.json
  - docs/videos/so-thats-why/material-20261111/README.md
---

# 原來如此素材池第三輪：補後備企劃與長題來源

## Why

站主 2026-11-11：「繼續擴充素材池」（規則同前）。

## Definition of done

- [x] 替最接近門檻的後備企劃與長題補讀來源，經非作者覆核；補不上的照實留後備。

## Steps

- [x] 補來源研究（wave53，31 個新題目；三份既有來源的新讀記錄併回原 id）。
- [x] 紙怎麼摺成為長題 G604（9 分）。
- [x] 企劃 P13、P29 改可成題並縮短（11、12 分），POOL_SUPPORT／MATERIAL_REVIEW。
- [x] checkpoint-3584、reviews/material-20261111-round3、README、VALIDATION。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node tools/video/so-thats-why/cli.mjs check`、`node --test tools/video/so-thats-why/*.test.mjs tools/video/so-thats-why/pool/pool.test.mjs`、`node tools/video/long-form/cli.mjs check`。

## Notes

- 入選 3,584 → 3,615，題案 603 → 604；企劃可成題 11 → 13。
- P30 兩半不是同一個問題（覆核 V5），C2-11 沙漏缺直接量測，P19 缺主動降噪教材，P22 沒補：都留後備。
- refresh-20261101、catalog.test.mjs 與 11/01 的 codex 舊票重疊，照站主先前同意的做法以 --force 認領。
