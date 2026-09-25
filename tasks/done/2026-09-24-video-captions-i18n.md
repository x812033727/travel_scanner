---
id: 2026-09-24-video-captions-i18n
title: 影片產線 T7：五語系 CC 與中繼資料翻譯
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-25T05:48:52Z
created_at: 2026-09-24T00:41:17Z
completed_at: 2026-09-25T05:51:42Z
branch: claude/video-captions-i18n
depends_on:
  - 2026-09-24-video-skill-automated
scope:
  - tools/video/i18n
  - .agents/skills/youtube-video/references/prompts/caption-translate.md
  - .agents/skills/youtube-video/references/prompts/caption-review.md
  - .agents/skills/youtube-video/SKILL.md
  - .agents/skills/youtube-video/references/automated.md
  - .claude/skills/youtube-video/SKILL.md
  - tools/video/cli.mjs
---

# 影片產線 T7：五語系 CC 與中繼資料翻譯

## Why

站主要 CC 跟網站一樣五語系（zh-TW、en、ja、ko、zh-CN），標題、說明、標籤也要五語系。翻譯以句子 id 對齊（`docs/videos/<slug>/i18n/<locale>.json`，每句帶 `source_hash`），每個語系在該句的時間窗內自己分段，不強求段數一樣；zh-TW 改了哪句，只重翻那句。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

## Definition of done

- [x] `captions --slug <slug> --workdir <dir>` 產生五條 SRT；每語系的行長與每秒字數在上限內（T1 的 `core/captions.mjs` 早已做好，這張不用動）。
- [x] lint 列出 `source_hash` 過期的句子與缺漏的語系（T1 的 `core/lint.mjs` 早已做好）。
- [x] 翻譯代理（sonnet）與逐語審稿代理（opus，只交修正清單）的提示在 skill 裡。
- [x] 五語系的標題、說明、標籤都通過 YouTube 上限檢查（`i18n-merge` 擋標題長度與角括號，`package` 的 `composeMetadata` 再檢查組好的說明欄）。

## Steps

- [x] `tools/video/i18n/`：`i18n-sheet` 出底稿、`i18n-merge` 寫回並算雜湊；分段規則沿用 `core/captions.mjs`。
- [x] `references/prompts/caption-translate.md`、`caption-review.md`；SKILL.md 與 `automated.md` 第 9 步改寫。
- [ ] 用試作影片跑一次四個語系 → 移到試作片的票 `2026-09-24-video-pilot-ai-model-choice`（分支 `claude/video-pilot-audio`）做，結果記在那裡。

## How to verify

```bash
node --test tools/video/i18n/*.test.mjs
node tools/video/cli.mjs captions --slug ai-model-choice --workdir <VIDEO_WORKDIR>
```

## Notes

- 為什麼要底稿：lint 與 `captions` 把「有這一筆、雜湊對」當成已翻譯，所以讓代理先填空白佔位會把空字串寫成字幕；代理也不該自己算雜湊。底稿（`<VIDEO_WORKDIR>/<slug>/i18n/<locale>.todo.json`）列出每一句的中文原文與目前的譯文，`todo` 標出要翻的；`i18n-merge` 驗證原文沒變、譯文不空，才寫進 repo 的 `i18n/<locale>.json` 並算雜湊。
- 原文在做底稿之後被改過的句子不會被合併，會列成問題，要重做底稿，避免譯文對到舊句子。
