---
id: 2026-11-12-stw-pool-round9
title: 原來如此素材池第九輪：補組題缺口與第二輪新組長題
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round9
claimed_at: 2026-11-12T02:29:46Z
created_at: 2026-11-12T02:29:44Z
completed_at: 2026-11-12T03:20:23Z
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第九輪：補組題缺口與第二輪新組長題

## Why

站主 2026-11-12：「繼續擴充」。照上一輪覆核開的翻案條件補後備組題的缺口，並再做一輪新組長題；夠成一集的才成題，不為片長硬湊。

## Definition of done

- [x] wave59 批次、checkpoint-3859、reviews/material-20261111-round9.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 作者 F13 補 C4-07、C4-08、C4-03、C4-04、C4-02、G38、G35；作者 F14 新組 3 組長題提案。
- [x] 兩位非作者覆核（V16、V17）重抓來源、重算片長。
- [x] 組進素材池：新增 G613–G616，其餘留後備。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 3,859→3,885，可成題長題 71→75。第二輪新組長題三組全數後備：讀過全文的核心已被現有可成題長題用完，下一輪不要再派「新組長題」，改派補讀新來源（C5-01 食品驗真最接近，差 1–1.5 條）。作者曾猜測未公開連結的檔名取得一篇論文，覆核找到公開連結才收：之後的說明檔要寫明「來源必須循公開連結取得，不得猜測網址」。等站主決定：G35 是否升長片（紀錄裡有 9 分鐘大綱）、行人組的事故案例、食品驗真組怎麼用三聚氰胺事件。
