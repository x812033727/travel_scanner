---
id: 2026-11-11-stw-pool-long-theme-review-and-new-episodes
title: 原來如此素材池：長題審視與新組 8 分鐘題案
status: done
priority: P2
area: docs
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T05:53:13Z
created_at: 2026-11-11T05:53:06Z
completed_at: 2026-11-11T06:43:21Z
branch:
depends_on: []
scope:
  - tools/video/so-thats-why/pool
---

# 原來如此素材池：長題審視與新組 8 分鐘題案

## Why

站主 2026-11-11：「原來如此也繼續擴充」「也可以審」，規則同奇聞檔案局（8 分鐘下限保留，太薄的放後備，不硬湊、不改 Shorts）。

## Definition of done

- [x] 原有長題逐題照 8 分鐘下限重算並標上結論；新組的長題經非作者覆核後進素材池。

## Steps

- [x] 審視 G01–G34 與其他 5 分鐘以上題案（39 組）：可成題 1、待合併 1、後備 34、淘汰 3。
- [x] 由短題組成新長題（看 45 組），非作者覆核後收 20 組（G576–G595）。
- [x] `themes.json` 的 `material` 欄、`render.mjs` 驗證與 THEMES.md 欄位、測試。
- [x] `reviews/material-20261111.{md,json}`、README。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`（PASS，595 組）；`node --test tools/video/so-thats-why/pool/pool.test.mjs`。

## Notes

- 給企劃的建議（G31 的 H3060／H3061 併進 P26、I3002 支持 P03 等）不在本票範圍，要改企劃另開票。
- 估時是依事實數的紙上估算；多數來源只讀到摘要或題級，寫稿前逐主張查核。
