---
id: 2026-11-03-influencer-piglet-e01
title: 網美小豬 EP1〈夕陽海邊〉零台詞短劇：系列規則與分鏡
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-wangwang
claimed_at: 2026-11-03T13:41:08Z
created_at: 2026-11-03T13:41:07Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/influencer-piglet
  - docs/videos/influencer-piglet-e01
---

# 網美小豬 EP1〈夕陽海邊〉零台詞短劇：系列規則與分鏡

## Why

站主 2026-11-03 從第二批零台詞系列企劃選了《網美小豬》。

## Definition of done

- [x] 系列規則 `docs/videos/influencer-piglet/README.md`；EP1 `video.json`（lint 0 錯誤）、`brief.md`。
- [x] 粉粉、水豚男友的寫實定裝照（依站主授權由 Claude 選定）。
- [x] Colab 首格、H3 直式片段、剪接：成片 18.0 s、-14.4 LUFS（`<VIDEO_WORKDIR>/influencer-piglet-e01/edit/final.mp4`）。
- [ ] `shorts import`：等 `2026-11-03-shorts-import-zero-dialogue`。

## How to verify

```bash
node tools/video/cli.mjs lint --file docs/videos/influencer-piglet-e01/video.json
```

## Notes

- 音效組 `piglet-comedy`：shutter、recordscratch、crack（ffmpeg 自己合成）。
- 一鏡一個主角；成品照裡的水豚臉是照片內容，首格要特別驗。
- s05 成品照的「水豚臉太陽」首格模型畫不出來（只畫了普通太陽），改用 ffmpeg 從定裝照裁臉、染橘、圓形羽化疊進太陽（原圖留 `s05-photo-orig.png`）。
- `colab exec` 跑首格常卡死且不會自己逾時：改成一張一張跑、每張 5 分鐘強制重試（scratchpad 的 run_episode.sh 做法），之後每張約 1 分鐘。
