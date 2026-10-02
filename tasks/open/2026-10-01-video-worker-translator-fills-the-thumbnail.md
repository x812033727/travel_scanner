---
id: 2026-10-01-video-worker-translator-fills-the-thumbnail
title: Video worker translator fills the thumbnail words on the metadata sheet
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-01T15:22:53Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-localized-thumbnails
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/flow.mjs
  - .agents/skills/youtube-video/references/prompts/caption-translate.md
  - .agents/skills/youtube-video/references/prompts/caption-review.md
---

# Video worker translator fills the thumbnail words on the metadata sheet

## Why

`2026-09-28-video-localized-thumbnails` 讓 `i18n-sheet` 的 metadata 部件多一個 `thumbnail`（`source` 是影片縮圖的 tag／headline／sub，`text` 要填該語言的字），`i18n-merge` 寫進 `i18n/<locale>.json` 的 `thumbnail`，`render` 再為每個語言畫 `thumbnails/<locale>.jpg`。但全自動工人的翻譯員（`tools/video/automation/prompts.mjs` 與 `references/prompts/caption-translate.md`）還不知道這個欄位：它可能留空，`flow.mjs` 的 `sheetDone` 也不看它，所以全自動影片的語言縮圖永遠是 note「no thumbnail words」，只有手動跑 i18n 的影片才有。

## Definition of done

- [ ] 翻譯員與字幕審稿員的提示寫清楚 `thumbnail.text`：每個 `source` 有的字都要填、短到手機上讀得到、保留 `**` 強調與換行；版面塞不下（`render` 的 note）時怎麼縮短。
- [ ] 工人的 metadata 翻譯結果帶有 `thumbnail`，`i18n-merge` 沒有 thumbnail note；`sheetDone` 是否要看 thumbnail 有明確決定（建議：要，但只在 sheet 有 `thumbnail` 時）。
- [ ] 縮圖字不能讓翻譯一直重試：填不出來仍算完成（`i18n-merge` 對它只出 note，不會非零結束）。

## Steps

- [ ] 讀 `tools/video/i18n/cli.mjs` 的 `buildSheet`／`mergeThumbnail` 與 `.agents/skills/youtube-video/references/publish.md`「多語言縮圖」。
- [ ] 改提示與 `sheetDone`，補 `tools/video/automation/automation.test.mjs` 的測試。

## How to verify

`node --test tools/video/automation/automation.test.mjs`，`npm run test:tools`；一支影片跑完語言製作後 `i18n/<locale>.json` 有 `thumbnail` 與 `source_hashes.thumbnail`，`render` 印出 `thumbnails of their own: …`。

## Notes

- 2026-10-01 開票時另一個代理正在改 `prompts.mjs` 與 `flow.mjs`，所以縮圖那張票沒碰它們。
