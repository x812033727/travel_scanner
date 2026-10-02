---
id: 2026-10-02-video-japanese-thumbnails-set-in-noto
title: Video Japanese thumbnails set in Noto Sans JP instead of the Traditional Chinese font
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-02T00:38:49Z
completed_at:
branch:
depends_on:
  - 2026-10-01-video-thumbnails-bundle-korean-and-simplified
scope:
  - tools/video/render/fonts.mjs
  - tools/video/render/render.test.mjs
  - tools/video/templates/templates.test.mjs
  - package.json
  - package-lock.json
---

# Video Japanese thumbnails set in Noto Sans JP instead of the Traditional Chinese font

## Why

語言縮圖（`thumbnails/<locale>.jpg`）裡，ko 與 zh-CN 自 `2026-10-01-video-thumbnails-bundle-korean-and-simplified` 起用自己的字型（`fonts.mjs` 的 `LOCALE_FONTS`）。ja 縮圖仍然用 Noto Sans TC、頁面 `lang="zh-Hant"` 畫：假名在 TC 的範圍內所以畫得出來，但漢字是繁中字形（例如「直」「骨」「写」的筆畫與日本的標準字形不同），日本觀眾看得出來不是日文字型。en 不受影響。

## Definition of done

- [ ] ja 的語言縮圖用 `@fontsource-variable/noto-sans-jp`（OFL-1.1，先確認）排在字型順序第一，頁面 `lang="ja"`；只用在 ja 的縮圖。
- [ ] 現有影片的投影片、主縮圖與 en/ko/zh-CN 縮圖的 frame key 不變（ja 縮圖的 key 會變，這是預期的）。
- [ ] `bundledCoverage("ja")` 只多 JP 的範圍；繁中投影片的涵蓋檢查不變。

## Steps

- [ ] `npm install -D @fontsource-variable/noto-sans-jp`，lockfile 只留那一筆（別讓本機 npm 版本改寫其他套件的 `peer`／`libc` 欄位）。
- [ ] `LOCALE_FONTS` 加 `ja: { font: "noto-sans-jp", family: "Noto Sans JP Variable", lang: "ja" }`，`FONT_PACKAGES` 加套件；`templates.mjs` 的 `page()` 與 `browser.mjs` 已經照 `LOCALE_FONTS` 走，不必改。
- [ ] `render.test.mjs`／`templates.test.mjs` 把 ja 從「跟主縮圖同一頁」的斷言移到「有自己字型」那邊。

## How to verify

`node --test tools/video/render/render.test.mjs tools/video/templates/templates.test.mjs`；照前一張票的 Notes 在一支影片的副本上加 ja 縮圖字、`VIDEO_BROWSER_CHANNEL=msedge` 跑 `render`，看 `thumbnails/ja.jpg` 的漢字字形。

## Notes

- 2026-10-02 做 ko／zh-CN 時發現，沒有一起做：不在那張票的完成定義裡。
