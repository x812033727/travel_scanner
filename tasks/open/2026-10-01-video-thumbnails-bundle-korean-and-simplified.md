---
id: 2026-10-01-video-thumbnails-bundle-korean-and-simplified
title: Video thumbnails bundle Korean and Simplified Chinese fonts for language thumbnails
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-01T15:22:56Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-localized-thumbnails
scope:
  - tools/video/render/fonts.mjs
  - tools/video/templates/theme.css
  - tools/video/render/browser.mjs
  - package.json
  - package-lock.json
---

# Video thumbnails bundle Korean and Simplified Chinese fonts for language thumbnails

## Why

語言縮圖（`2026-09-28-video-localized-thumbnails`）只用內建的 Noto Sans TC 與 JetBrains Mono 畫。2026-10-01 在 vibe-coding-first-website-2026 的副本實測：韓文縮圖「바이브 코딩／코드 없이」有 14 個音節內建字型沒有，`render` 把 ko 記成 note 不畫，所以韓文市場永遠拿不到自己的縮圖；簡中縮圖畫得出來，但「写、码、线、费、编、围」等簡體字和旁邊的字粗細明顯不同（unicode-range 有涵蓋，實際字形看起來是別的字型或較細的字重），不夠格上傳。

## Definition of done

- [ ] 韓文縮圖能畫：Hangul 由內建字型涵蓋（例如 `@fontsource-variable/noto-sans-kr`），`render` 不再把 ko 記成缺字。
- [ ] 簡中縮圖的簡體字與其他字同一套字型、同樣粗細（例如 `@fontsource-variable/noto-sans-sc`），只用在該語言的縮圖，繁中投影片的字型與畫面鍵不變（現有影片的 frame key 不能動）。
- [ ] 字型涵蓋檢查（`tools/video/render/fonts.mjs`）照語言判斷：繁中投影片仍然拒絕簡體字。

## Steps

- [ ] 查 fontsource 套件授權與大小；決定是否只在縮圖頁面載入（`thumbnailHtml` 加 `lang` 與字型 class）。
- [ ] `render.test.mjs` 補測試；用一支影片的副本實際畫 ko 與 zh-CN 看圖。

## How to verify

`node --test tools/video/render/render.test.mjs`；照 `2026-09-28-video-localized-thumbnails` 的 Notes 在副本上 `i18n-sheet`／`i18n-merge`／`render`，看 `thumbnails/ko.jpg`、`thumbnails/zh-CN.jpg`。

## Notes

- 加套件會動 `package.json`／`package-lock.json`，開工前確認沒有別的票持有它們。
