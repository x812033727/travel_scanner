---
id: 2026-10-01-video-worker-translator-fills-the-thumbnail
title: Video worker translator fills the thumbnail words on the metadata sheet
status: done
priority: P2
area: tools
owner: claude-opus-5-5-thumb-text
claimed_at: 2026-10-02T00:19:42Z
created_at: 2026-10-01T15:22:53Z
completed_at: 2026-10-02T00:33:12Z
branch: claude/worker-thumbnail-text
depends_on:
  - 2026-09-28-video-localized-thumbnails
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/flow.mjs
  - .agents/skills/youtube-video/references/prompts/caption-translate.md
  - .agents/skills/youtube-video/references/prompts/caption-review.md
  - tools/video/automation/automation.test.mjs
  - tasks/open/2026-10-02-video-worker-draws-the-language-thumbnails.md
---

# Video worker translator fills the thumbnail words on the metadata sheet

## Why

`2026-09-28-video-localized-thumbnails` 讓 `i18n-sheet` 的 metadata 部件多一個 `thumbnail`（`source` 是影片縮圖的 tag／headline／sub，`text` 要填該語言的字），`i18n-merge` 寫進 `i18n/<locale>.json` 的 `thumbnail`，`render` 再為每個語言畫 `thumbnails/<locale>.jpg`。但全自動工人的翻譯員（`tools/video/automation/prompts.mjs` 與 `references/prompts/caption-translate.md`）還不知道這個欄位：它可能留空，`flow.mjs` 的 `sheetDone` 也不看它，所以全自動影片的語言縮圖永遠是 note「no thumbnail words」，只有手動跑 i18n 的影片才有。

## Definition of done

- [x] 翻譯員與字幕審稿員的提示寫清楚 `thumbnail.text`：每個 `source` 有的字都要填、短到手機上讀得到、保留 `**` 強調與換行；版面塞不下（`render` 的 note）時怎麼縮短。
- [x] 工人的 metadata 翻譯結果帶有 `thumbnail`，`i18n-merge` 沒有 thumbnail note；`sheetDone` 是否要看 thumbnail 有明確決定（建議：要，但只在 sheet 有 `thumbnail` 時）。
- [x] 縮圖字不能讓翻譯一直重試：填不出來仍算完成（`i18n-merge` 對它只出 note，不會非零結束）。

## Steps

- [x] 讀 `tools/video/i18n/cli.mjs` 的 `buildSheet`／`mergeThumbnail` 與 `.agents/skills/youtube-video/references/publish.md`「多語言縮圖」。
- [x] 改提示與 `sheetDone`，補 `tools/video/automation/automation.test.mjs` 的測試。

## How to verify

`node --test tools/video/automation/automation.test.mjs`，`npm run test:tools`；一支影片跑完語言製作後 `i18n/<locale>.json` 有 `thumbnail` 與 `source_hashes.thumbnail`，`render` 印出 `thumbnails of their own: …`。

## Notes

- 2026-10-01 開票時另一個代理正在改 `prompts.mjs` 與 `flow.mjs`，所以縮圖那張票沒碰它們。
- 2026-10-02 認領用了 `--force`：擋住的是 `2026-09-28-drama-listener-stale-check`（codex-ten-drama，PR #978 已合併）、`2026-09-28-sothatswhy-shorts-from-episode`（PR #904/#950/#962 已合併）、`2026-09-30-video-worker-moves-two-videos-at`（PR #999 已合併）三張過期認領。
- scope 加了 `automation.test.mjs`（Steps 本來就要補它的測試，SHA-256 釘住的提示雜湊也在這裡）與新開的追蹤票檔。
- **`sheetDone` 的決定：要看，但只問一次。** 只在 sheet 有 `thumbnail`（且有 `metadata` 部件）時看；縮圖字有空的就不算完成，除非這組縮圖字（`thumbnail.source` 的雜湊，`thumbnailAskHash`）已經問過翻譯員。翻譯成功合併後工人把雜湊記在 state 的 `thumbnails_asked.<locale>`，`translateLocale` 與 `channelLocale`（英文旁白影片的 zh-TW）都帶它進 `sheetDone`。所以：模型沒填也照樣完成、下一輪送語言批次，不會每輪重翻；zh-TW 縮圖之後改了字，雜湊不同，會再問一次。單純「要看」會讓沒填縮圖的語言每輪重翻、批次永遠送不出去；單純「不看」則語言在 metadata 已是最新時永遠問不到縮圖。
- 工人另外保住縮圖字：模型回的 worksheet 一律帶回 sheet 的 `thumbnail.source`／`todo`；字審員回的 worksheet 沒有 `thumbnail` 時沿用翻譯員的字（之前會被丟掉）。`i18n-merge` 的 `note: thumbnail:` 行寫進工人的 log。
- **提示改了，zh-TW 影片的翻譯員與字審員提示雜湊照 PR #1099 的規則在同一個 commit 更新**：translator `da0f9a06…` → `1e3a4cfb…`，caption_reviewer `92a50b60…` → `a0ad3493…`；shorten／reword 沒有縮圖，雜湊不變。為了讓 SOURCE_INSTRUCTIONS 的替換片語（「the zh-TW line takes」等）還找得到，新段落不含它們，也不說「zh-TW thumbnail」而說「the video's own thumbnail」；四個旁白語言的版本照樣建得出來、#1099 的測試全過。
- 驗證：`node --test tools/video/automation/automation.test.mjs tools/video/automation/prompts.test.mjs` 74/74；新測試兩支：翻譯員填了縮圖字（字審員回答時丟掉 thumbnail）→ `i18n/en.json` 有 `thumbnail` 與 `source_hashes.thumbnail`、沒有 thumbnail note、下一輪送批次；模型完全不回 thumbnail → 照樣完成、log 有 note、`thumbnails_asked.en` 記下、下一輪直接送批次（翻譯員只被叫一次）。
- **沒做的**：工人在翻譯後不會重跑 `render`，所以全自動影片的 `thumbnails/<locale>.jpg` 還是畫不出來（`package` 寫「not drawn yet; run render」）。這不在本票的 Definition of done，另開 `2026-10-02-video-worker-draws-the-language-thumbnails`。
