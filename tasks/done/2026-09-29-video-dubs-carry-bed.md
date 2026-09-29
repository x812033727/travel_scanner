---
id: 2026-09-29-video-dubs-carry-bed
title: Dub tracks carry the music bed and sound effects of an illustrated video
status: done
priority: P2
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-29T10:45:14Z
created_at: 2026-09-29T09:14:23Z
completed_at: 2026-09-29T10:53:03Z
branch: claude/sharp-brown-dh2x95
depends_on:
  - 2026-09-29-video-illustrated-slides-assemble
scope:
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/plan.mjs
  - tools/video/dubs/dubs.test.mjs
  - tools/video/dubs/encode.mjs
  - tools/video/assemble/sound.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/assemble/drama.mjs
  - tools/video/core/state.mjs
  - docs/videos/ILLUSTRATED.md
---

# Dub tracks carry the music bed and sound effects of an illustrated video

## Why

`dubs/cli.mjs:207-213` 只用 `measureLoudnessArgs`＋`encodeArgs` 編旁白，插圖投影片的 zh-TW 有配樂與音效之後，en／ja／ko／zh-CN 的音軌會是乾的。

## Definition of done

- [x] 有 `music`／`sfx` 的影片，dub 走 `measureMixArgs`／`mixArgs`（＋sfx 軌），床與壓低跟成片一樣；`mixArgs` 多一個 `codec` 參數，dub 用自己的上傳格式（m4a／mp3／wav）。
- [x] dub 的 timeline 記 `mix_hash`／`sfx_hash`；`dubsStatus` 不符就標 stale（註明「made without the video's music or sound effects; run dub again」）。
- [x] 沒有配樂的影片行為不變（既有測試的 ffmpeg 參數不動）。

## Steps

- [x] `dubs/cli.mjs` 混音路徑（`dubSound()`）。
- [x] 測試（`dubs.test.mjs` 插圖 fixture 走查）；`plan.mjs` 不用改。

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs dub --slug <插圖投影片> --locale en --workdir <tmp>；聽 upload 的音軌有配樂
```

## Notes

依賴 `2026-09-29-video-illustrated-slides-assemble` 的 `mediaInputs` 與 sfx 軌。

做完學到的：

- `musicInputs`／`sfxInputs` 從 `assemble/cli.mjs` 搬到新的 `assemble/sound.mjs`，assemble 與 dub 共用；dub 不重算音效軌（要 layout 與 frames），直接重用成片的 `build/sfx.wav`，條件是 `checks.json` 的 `sfx_hash` 等於劇本的、`speech_hash` 等於 timeline 的：配音的句子放在 zh-TW 時間軸的視窗裡，成片的節拍位置對配音仍成立。成片還沒合成時只帶配樂、`sfx_hash` 記 null，status 標 stale，工人在 languages 階段（成片核准後）跑 dub 時成片一定在。
- 配樂檔不在 `_music/` 是站主要補的，dub 直接拒絕（exit usage），不做乾的音軌。
- scope 加了 `encode.mjs`（匯出 CODECS）、`assemble/sound.mjs`、`assemble/cli.mjs`、`assemble/drama.mjs`、`core/state.mjs`、`ILLUSTRATED.md`。
