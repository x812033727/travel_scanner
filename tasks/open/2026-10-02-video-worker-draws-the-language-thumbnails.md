---
id: 2026-10-02-video-worker-draws-the-language-thumbnails
title: Video worker draws the language thumbnails before it packages a language batch
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-02T00:29:59Z
completed_at:
branch:
depends_on:
  - 2026-10-01-video-worker-translator-fills-the-thumbnail
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Video worker draws the language thumbnails before it packages a language batch

## Why

`2026-10-01-video-worker-translator-fills-the-thumbnail` 讓全自動工人的翻譯員把縮圖字寫進 `i18n/<locale>.json`（`thumbnail` 與 `source_hashes.thumbnail`）。但語言縮圖 `thumbnails/<locale>.jpg` 只有 `render` 會畫，而工人的 `languages()`（`tools/video/automation/flow.mjs`）在翻譯完只跑 `captions` 與 `package`，`render` 只在「frames rendered」那一步跑過一次，那時還沒有任何翻譯。結果 `package` 對每個語言都寫 `skipped_thumbnail_locales.<locale> = "not drawn yet; run render"`（`tools/video/package/cli.mjs` 的 `localeThumbnails`），全自動影片的上傳包永遠沒有語言縮圖，即使縮圖字已經翻好。

## Definition of done

- [ ] 一支全自動影片的語言批次送出前，翻好縮圖字的語言在 `upload/thumbnails/<locale>.jpg` 有自己的縮圖，`metadata.json` 的 `thumbnails` 列出它。
- [ ] 重畫只畫縮圖（畫格快取命中，不重畫場景），不讓已核准的 final（`visual_hash`、`final.mp4`）失效；如果會，寫明怎麼避開。
- [ ] 縮圖畫不出來（字型缺字、版面塞不下）仍只是 note，語言批次照送，不重試。
- [ ] 清理過工作區（`tidied_at`）的影片不跑 render。

## Steps

- [ ] 讀 `tools/video/render/cli.mjs` 的 `localizedThumbnails` 與快取、`tools/video/core/state.mjs` 怎麼判斷 render 過期，確認在 final 核准後重跑 render 的影響。
- [ ] 在 `languages()` 的 `captions`／`package` 前，只在有語言的縮圖字是最新但沒畫（或畫的時候字不同）時跑 `render`。
- [ ] 補 `tools/video/automation/automation.test.mjs`：假的 `render` 寫 `thumbnail_locales`，上傳包帶著 `thumbnails/en.jpg`。

## How to verify

`node --test tools/video/automation/automation.test.mjs`，`npm run test:tools`；一支全自動影片勾了某語言的標題說明，語言批次送出後 `upload/metadata.json` 的 `thumbnails` 有那個語言。

## Notes

- 2026-10-02 由 `2026-10-01-video-worker-translator-fills-the-thumbnail` 的代理發現：那張票只讓縮圖字進到 `i18n`，畫圖不在它的 Definition of done 裡。
