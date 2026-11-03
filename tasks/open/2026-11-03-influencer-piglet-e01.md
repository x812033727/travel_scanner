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
- [ ] 粉粉、水豚男友的寫實定裝照（站主選定）。
- [ ] Colab 首格、H3 直式片段、剪接、`shorts import`。

## How to verify

```bash
node tools/video/cli.mjs lint --file docs/videos/influencer-piglet-e01/video.json
```

## Notes

- 音效組 `piglet-comedy`：shutter、recordscratch、crack（ffmpeg 自己合成）。
- 一鏡一個主角；成品照裡的水豚臉是照片內容，首格要特別驗。
