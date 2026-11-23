---
id: 2026-11-12-stw-pool-round17
title: 原來如此素材池第十七輪：補讀最接近門檻的後備組題
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round17
claimed_at: 2026-11-12T10:33:23Z
created_at: 2026-11-12T10:33:22Z
completed_at: 2026-11-12T11:05:24Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第十七輪：補讀最接近門檻的後備組題

## Why

站主 2026-11-12：「持續擴充」。第十四到十六輪從零研究的 8 個新長題都沒成題，這一輪改以補讀最接近門檻的後備組題為主；夠成一集的才成題，不為片長硬湊。

## Definition of done

- [x] wave67 批次、checkpoint-4074、reviews/material-20261111-round17.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 作者 F29 補 C9-02 濕沙、C12-01 冷凍肉；作者 F30 補 C7-01 交叉雙手、C13-01 鳥蛋。
- [x] 兩位非作者覆核（V32、V33）重抓來源、逐筆讀工具紀錄、重算片長。
- [x] 組進素材池：新增 G626、G627，其餘留後備。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 4,074→4,089，可成題長題 84→86。補讀比從零研究有效：四題成了兩題。G626 只比門檻多 0.06 分（靠 Herminghaus 2003 預印本 0.25 條），寫稿重讀時站不住就退回後備。後備：C12-01 約 7.91 分、差約 1.25 條（Martino & Zaritzky 1986、Zhang & Ertbjerg 的原論文數字）；C13-01 約 7.26 分、差約 2.4 條（Hays & Hauber 2018 被 403、Shatkovska 2018 無開放全文）。其他仍後備、可再補的：C10-01 冰（約 7.3 分）、C11-01 迷路繞圈（約 5.8 分）、C13-02 蝸牛（約 5.7 分）。
