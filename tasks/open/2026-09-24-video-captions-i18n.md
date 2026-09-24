---
id: 2026-09-24-video-captions-i18n
title: 影片產線 T7：五語系 CC 與中繼資料翻譯
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-24T00:41:17Z
completed_at:
branch:
depends_on:
  - 2026-09-24-video-skill-automated
scope:
  - tools/video/i18n
  - .agents/skills/youtube-video/references/prompts/caption-translate.md
  - .agents/skills/youtube-video/references/prompts/caption-review.md
---

# 影片產線 T7：五語系 CC 與中繼資料翻譯

## Why

站主要 CC 跟網站一樣五語系（zh-TW、en、ja、ko、zh-CN），標題、說明、標籤也要五語系。翻譯以句子 id 對齊（`docs/videos/<slug>/i18n/<locale>.json`，每句帶 `source_hash`），每個語系在該句的時間窗內自己分段，不強求段數一樣；zh-TW 改了哪句，只重翻那句。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

## Definition of done

- [ ] `captions --slug <slug> --workdir <dir>` 產生五條 SRT；每語系的行長與每秒字數在上限內。
- [ ] lint 列出 `source_hash` 過期的句子與缺漏的語系。
- [ ] 翻譯代理（sonnet）與逐語審稿代理（opus，只交修正清單）的提示在 skill 裡。
- [ ] 五語系的標題、說明、標籤都通過 YouTube 上限檢查。

## Steps

- [ ] `tools/video/i18n/`：翻譯檔格式與檢查、各語系分段規則（en 約 42 字元一行、ja／ko／zh 依字數）。
- [ ] `references/prompts/caption-translate.md`、`caption-review.md`。
- [ ] 用試作影片跑一次四個語系。

## How to verify

```bash
node --test tools/video/i18n/*.test.mjs
node tools/video/cli.mjs captions --slug ai-model-choice --workdir <VIDEO_WORKDIR>
```

## Notes
