---
id: 2026-11-03-raccoon-mischief-e01-vase
title: 闖禍小浣熊 EP1〈花瓶〉零台詞短劇：系列規則與分鏡
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-wangwang
claimed_at: 2026-11-03T11:38:01Z
created_at: 2026-11-03T11:38:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/raccoon-mischief
  - docs/videos/raccoon-mischief-e01
---

# 闖禍小浣熊 EP1〈花瓶〉零台詞短劇：系列規則與分鏡

## Why

站主 2026-11-03 從零台詞系列企劃選了《闖禍小浣熊》（盲評第 1 名）。

## Definition of done

- [x] 系列規則 `docs/videos/raccoon-mischief/README.md`；EP1 `video.json`（lint 0 錯誤）、`brief.md`。
- [ ] 站主看 EP1 分鏡、核准劇本。
- [ ] 三隻浣熊的寫實設定圖（`sheet_prompt` 已寫成單張全身照，避免卡通三視圖，見《汪家夫妻》的經驗）。
- [ ] Colab 首格與小樣、剪接、`shorts import`。

## How to verify

```bash
node tools/video/cli.mjs lint --file docs/videos/raccoon-mischief-e01/video.json
```

## Notes

- 音效組 `raccoon-comedy`：shatter、keys、crunch、sting，要有授權的檔案。
