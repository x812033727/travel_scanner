---
id: 2026-09-28-video-shorts-build-checks-before-narration
title: Shorts build 先查 STOP 與 ffmpeg 再付費合成旁白
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-28T15:33:40Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts/build.mjs
  - tools/video/shorts/pipeline.test.mjs
---

# Shorts build 先查 STOP 與 ffmpeg 再付費合成旁白

## Why

#925（`f67b83715`）讓 `node tools/video/shorts/cli.mjs build --speech server` 改用網站的付費旁白（Gemini／Azure 的字元額度）。現在 `build.mjs:201-203` 一開始就讀設定、呼叫 `narrate()`，對每一句沒快取的旁白付費合成，然後才在 :209 檢查 STOP 檔、在 :219 找 ffmpeg。#925 之前順序相反（STOP 與 ffmpeg 在前），而且當時合成的是免費的 Windows 語音。

所以放了 STOP 檔，或機器上沒有 ffmpeg，都要等錢花完才發現。每句有快取（`speech.mjs:50-51`），重跑不會再付一次，而且 build 目前沒有自動呼叫者，所以現在影響很小；但工人的 `shortsStep`（票 `2026-09-28-video-shorts-worker-lab`）一旦自動呼叫 build，就會變成實際的花費問題。

2026-09-28 部署 `50b3cb55` 後的稽核找到的（兩個代理獨立確認）。

## Definition of done

- [ ] `build` 在任何付費合成之前，先檢查 `stopRequested(base/slug)`（它也涵蓋 `base/STOP`，`tools/video/core/paths.mjs:84-86`）並找到 ffmpeg；兩者任一不過就停，一句都不合成。
- [ ] 其餘行為不變。

## Steps

- [ ] 把 STOP 檢查與 `locateFfmpeg` 移到 `narrate()` 之前（新的時間戳目錄不可能有 STOP 檔，所以不依賴 buildId）。
- [ ] 測試：有 STOP 檔時 `narrate` 的替身一次都沒被呼叫。

## How to verify

```bash
node --test "tools/video/shorts/*.test.mjs"
```

## Notes

同一次稽核也看了 `qa.mjs:223` 每次都呼叫網站的政策評審，判定為設計如此（長影片的 qa 也一樣），不算缺陷。
