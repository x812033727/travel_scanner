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
- [x] 站主授權直接做完（2026-11-03）。
- [x] 定裝照（`docs/videos/raccoon-mischief-e01/reference/`）。
- [x] Colab 首格、H3 直式片段、剪接：成片 13.0 s、-14.8 LUFS（`<VIDEO_WORKDIR>/raccoon-mischief-e01/edit/final.mp4`）。
- [ ] `shorts import`：等 `2026-11-03-shorts-import-zero-dialogue`。

## How to verify

```bash
node tools/video/cli.mjs lint --file docs/videos/raccoon-mischief-e01/video.json
```

## Notes

- 音效組 `raccoon-comedy`：shatter、keys、crunch、sting，要有授權的檔案。
- 首格：兩個角色加複雜動作會被畫錯（媽媽叼花、多一個真花瓶），改成一鏡一個角色才對；s05（青蔥）三次都沒畫出笑點，成片停在爸爸假裝落地燈。
- s03 片段從第 1 秒起畫面前方晃進一扇門板，只用第一格做 3.2 s 的慢推。
