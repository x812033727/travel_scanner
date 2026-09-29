---
id: 2026-09-29-video-dubs-carry-bed
title: Dub tracks carry the music bed and sound effects of an illustrated video
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-29T09:14:23Z
completed_at:
branch:
depends_on:
  - 2026-09-29-video-illustrated-slides-assemble
scope:
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/plan.mjs
  - tools/video/dubs/dubs.test.mjs
---

# Dub tracks carry the music bed and sound effects of an illustrated video

## Why

`dubs/cli.mjs:207-213` 只用 `measureLoudnessArgs`＋`encodeArgs` 編旁白，插圖投影片的 zh-TW 有配樂與音效之後，en／ja／ko／zh-CN 的音軌會是乾的。

## Definition of done

- [ ] 有 `music`／`sfx` 的影片，dub 走 `measureMixArgs`／`mixArgs`（＋sfx 軌），床與壓低跟成片一樣。
- [ ] dub 的 timeline 記 `mix_hash`／`sfx_hash`；`dubsStatus`（`state.mjs:243-267`）不符就標 stale。
- [ ] 沒有配樂的影片行為不變。

## Steps

- [ ] `dubs/cli.mjs` 混音路徑。
- [ ] `dubs/plan.mjs`／測試。

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs dub --slug <插圖投影片> --locale en --workdir <tmp>；聽 upload 的音軌有配樂
```

## Notes

依賴 `2026-09-29-video-illustrated-slides-assemble` 的 `mediaInputs` 與 sfx 軌。
