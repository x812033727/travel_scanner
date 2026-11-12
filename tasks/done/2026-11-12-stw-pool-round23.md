---
id: 2026-11-12-stw-pool-round23
title: 原來如此素材池第二十三輪
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T15:21:36Z
created_at: 2026-11-12T15:21:36Z
completed_at: 2026-11-12T15:50:38Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第二十三輪

## Why

站主 2026-11-12：「原來如此就一直持續審下去」。挑第二十一、二十二輪覆核寫明「點名原文全補到就能過線」的題，只照覆核點名的清單補讀。

## Definition of done

- [x] 新核心批次與 `reviews/material-20261111-round23.{json,md}` 入庫，快照照前例，`cli.mjs check` PASS，pool 與 catalog 測試全過。

## Steps

- [x] 二十位作者（F62–F81）各補一題第二十到二十二輪留下的後備題（C9-01～C19-02），只讀覆核點名的原文。
- [x] 非作者覆核 V65–V84（無提案的作者 F65、F69、F70、F75、F76、F80 記為無變更）。
- [x] 整合、更新 README 與報告。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`；`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`。

## Notes

第七十三批 28 個新核心（4,321 → 4,349），二十題都仍後備；最接近的是 C12-01 冷凍肉（8.43 分，差 0.25 條）。多數覆核建議不再單獨補讀、改合併或淘汰（C16-02、C18-02、C19-01、C14-02、C15-02、C12-02），等站主決定，見 round23.json 的 policies.drop_or_merge。第二十四輪（從零研究新長題，F82 起）等本輪入庫後另開票。
