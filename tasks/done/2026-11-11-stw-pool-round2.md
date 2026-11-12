---
id: 2026-11-11-stw-pool-round2
title: 原來如此素材池第二輪：再組長題與補後備來源
status: done
priority: P2
area: docs
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T10:17:13Z
created_at: 2026-11-11T09:11:42Z
completed_at: 2026-11-11T10:17:14Z
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

# 原來如此素材池第二輪：再組長題與補後備來源

## Why

站主 2026-11-11 再次：「繼續擴充素材池，一樣做好去重和來源整理，太薄或無聊的題目就合併或淘汰，影片不要為了片長硬湊」，並說「做完就合併部署」。

## Definition of done

- [x] 從剩下的短題再組長題，替最接近門檻的後備題補讀來源；都經非作者覆核，不為片長硬湊。

## Steps

- [x] 再組長題（看 24 組，覆核後收 8 組：G596–G603）。
- [x] 補來源研究（wave52，26 個新題目；自製 QR 測試只當示範），G13、G15、G17、G24、G27、G29 刪掉指定章節後升為可成題。
- [x] 企劃 P04、P12 補來源後改成可成題並縮短片長（POOL_SUPPORT、MATERIAL_REVIEW）。
- [x] checkpoint-3558、reviews/material-20261111-round2、README、VALIDATION。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node tools/video/so-thats-why/cli.mjs check`、`node --test tools/video/so-thats-why/*.test.mjs tools/video/so-thats-why/pool/pool.test.mjs`、`node tools/video/long-form/cli.mjs check`。

## Notes

- 入選 3,558 → 3,584，題案 595 → 603，可成題長題 21 → 35；企劃可成題 9 → 11。
- E2282 不能改原紀錄（會破壞基線），在 G17 的 evidence_gaps 註明只引 Tektronix。
- refresh-20261101、catalog.test.mjs 與 11/01 的 codex 舊票（review、超過 10 天沒動）重疊，照站主先前同意的做法以 --force 認領。
