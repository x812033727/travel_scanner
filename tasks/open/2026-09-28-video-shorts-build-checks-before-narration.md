---
id: 2026-09-28-video-shorts-build-checks-before-narration
title: Shorts build 先查 STOP 與 ffmpeg 再付費合成旁白
status: in-progress
priority: P3
area: tools
owner: claude-fable-5-1-shorts-build
claimed_at: 2026-09-30T03:40:23Z
created_at: 2026-09-28T15:33:40Z
completed_at:
branch: claude/shorts-build-stop-before-narration
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

- [x] `build` 在任何付費合成之前，先檢查 `stopRequested(base/slug)`（它也涵蓋 `base/STOP`，`tools/video/core/paths.mjs:84-86`）並找到 ffmpeg；兩者任一不過就停，一句都不合成。
- [x] 其餘行為不變。

## Steps

- [x] 把 STOP 檢查與 `locateFfmpeg` 移到 `narrate()` 之前（新的時間戳目錄不可能有 STOP 檔，所以不依賴 buildId）。
- [x] 測試：有 STOP 檔時 `narrate` 的替身一次都沒被呼叫。

## How to verify

```bash
node --test "tools/video/shorts/*.test.mjs"
```

## Notes

同一次稽核也看了 `qa.mjs:223` 每次都呼叫網站的政策評審，判定為設計如此（長影片的 qa 也一樣），不算缺陷。

### 2026-09-30 claude-fable-5-1-shorts-build

- 認領用了 `--force`：`2026-09-28-sothatswhy-shorts-from-episode`（claude-opus）的 scope 是整個 `tools/video/shorts/`，認領已超過 24 小時，本機、遠端都找不到它的分支，也沒有開著的 PR，屬過期認領；本票只動 `build.mjs` 與 `pipeline.test.mjs` 兩個檔。
- `build.mjs`：解析出 work base 之後、讀網站設定與 `narrate()` 之前，先 `stopRequested(base/slug)`（同時涵蓋 `base/STOP`），再找 ffmpeg；任一不過就丟錯，一句都不合成、也不建立時間戳目錄。原本旁白之後的 STOP 檢查保留（合成途中放的 STOP 仍在建目錄前生效），ffmpeg 的結果沿用給後面的步驟，其餘不變。
- 為了測「沒有 ffmpeg」，`build` 多了一個可注入的 `locateFfmpegImpl`（預設就是 `locateFfmpeg`），與既有的 `synthesizeImpl` 同樣是替身用的參數；CLI 的呼叫不必改。
- 測試 `a STOP file or a missing ffmpeg ends a build before a single phrase is paid for`：slug 目錄有 STOP、base 有 STOP、ffmpeg 找不到三種情況，合成替身都是 0 次；對照組（兩者都過）證明替身確實接上了——11 句全數合成，停在假的 ffmpeg。把 `build.mjs` 換回 main 的版本時這個測試會紅（STOP 情況合成了 11 次）。
- 驗證：`node --test tools/video/shorts/pipeline.test.mjs` 36/36 過；`npm run test:tools` 932 項中 930 過、1 跳過、1 失敗——失敗的是 `tools/video/tts/check.test.mjs` 的「a second transcript clears a line only Gemini misheard…」，與本票無關（單獨跑也失敗，該檔不引用 shorts）。
